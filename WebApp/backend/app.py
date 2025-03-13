from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import threading
import time
import socket
import subprocess
import sys
from flask_restx import Api, Resource, fields
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the frontend

# Initialize Swagger/Flask-RestX
api = Api(app, version='1.0', title='Drone Control API',
          description='API for controlling a Tello drone',
          doc='/swagger')  # Swagger UI will be available at /swagger

# Define namespaces for logical grouping
drone_ns = api.namespace('drone', description='Drone operations')
video_ns = api.namespace('video', description='Video streaming')
status_ns = api.namespace('status', description='Drone status')

# Create models for documentation
drone_data_model = api.model('DroneData', {
    'battery': fields.Integer(description='Battery percentage'),
    'temperature': fields.Integer(description='Temperature in Celsius'),
    'flight_time': fields.Integer(description='Flight time in seconds'),
    'height': fields.Integer(description='Height in cm'),
    'speed': fields.Integer(description='Speed in cm/s'),
    'signal': fields.Integer(description='Signal strength')
})

status_model = api.model('Status', {
    'connected': fields.Boolean(description='If drone is connected'),
    'drone_data': fields.Nested(drone_data_model)
})

response_model = api.model('Response', {
    'success': fields.Boolean(description='Operation success status'),
    'message': fields.String(description='Response message')
})

# Variables globales
drone = None
connected = False
frame = None
frame_lock = threading.Lock()
drone_data = {
    "battery": 0,
    "temperature": 0,
    "flight_time": 0,
    "height": 0,
    "speed": 0,
    "signal": 0
}

def check_for_existing_processes():
    # Vérifier si des processus utilisent le port 8889
    try:
        if sys.platform == "linux" or sys.platform == "darwin":
            output = subprocess.check_output(["lsof", "-i:8889"]).decode()
            if output:
                print("Port 8889 déjà utilisé. Veuillez fermer les applications utilisant ce port.")
                print(output)
                return True
        elif sys.platform == "win32":
            output = subprocess.check_output(["netstat", "-ano"]).decode()
            if "8889" in output:
                print("Port 8889 déjà utilisé. Veuillez fermer les applications utilisant ce port.")
                return True
    except:
        # Si la commande échoue, continuez
        pass
    return False

def connect_drone():
    global drone, connected
    
    if check_for_existing_processes():
        return False
    
    try:
        # Essayez d'importer la bibliothèque djitellopy
        from djitellopy import Tello
        
        # Créez une nouvelle socket UDP pour vérifier si le port est disponible
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.settimeout(1)
        
        try:
            test_socket.bind(('', 8889))  # Essayez de lier au port
            test_socket.close()  # Si réussi, fermez-le
        except OSError:
            print("Le port 8889 est déjà utilisé. Impossible de se connecter au drone.")
            return False
        
        # Initialisation du drone
        drone = Tello()
        
        # Tentative de connexion
        try:
            drone.connect()
            connected = True
            print("Drone connecté avec succès!")
            return True
        except Exception as e:
            print(f"Erreur lors de la connexion au drone: {e}")
            return False
            
    except ImportError:
        print("La bibliothèque djitellopy n'est pas installée. Veuillez l'installer avec pip.")
        return False
    except Exception as e:
        print(f"Erreur lors de l'initialisation du drone: {e}")
        return False

def update_drone_data():
    global drone_data, drone, connected
    
    if not drone or not connected:
        return
        
    while connected:
        try:
            drone_data["battery"] = drone.get_battery()
            drone_data["temperature"] = drone.get_temperature()
            drone_data["flight_time"] = drone.get_flight_time()
            drone_data["height"] = drone.get_height()
            drone_data["speed"] = drone.get_speed_x()
            drone_data["signal"] = 100  # À remplacer par la vraie valeur si disponible
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {e}")
        time.sleep(1)

def video_stream():
    global frame, drone, connected
    
    if not drone or not connected:
        return
    
    drone.streamon()
    
    while connected:
        try:
            current_frame = drone.get_frame_read().frame
            if current_frame is not None:
                with frame_lock:
                    frame = current_frame.copy()
                    frame = cv2.resize(frame, (640, 480))
        except Exception as e:
            print(f"Erreur lors de la récupération de la vidéo: {e}")
            time.sleep(0.1)

def generate_frames():
    global frame
    while True:
        if not connected or frame is None:
            # Générer une image "Pas de signal"
            no_signal = create_no_signal_frame()
            ret, buffer = cv2.imencode('.jpg', no_signal)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.5)
            continue
            
        with frame_lock:
            if frame is None:
                time.sleep(0.1)
                continue
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def create_no_signal_frame():
    # Créer une image "Pas de signal"
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    # Ajouter du texte
    cv2.putText(img, "Pas de signal vidéo", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return img

# API Routes with Swagger documentation
@drone_ns.route('/connect')
class DroneConnect(Resource):
    @api.doc(description='Connect to the drone')
    @api.response(200, 'Success', response_model)
    def get(self):
        """Connect to the drone"""
        if connect_drone():
            # Lancement des threads pour les données et la vidéo
            threading.Thread(target=update_drone_data, daemon=True).start()
            threading.Thread(target=video_stream, daemon=True).start()
            return {"success": True, "message": "Drone connecté"}
        return {"success": False, "message": "Échec de la connexion"}

@api.route('/test')
class TestAPI(Resource):
    @api.doc(description='Test if API is accessible')
    def get(self):
        """Test if the API is accessible"""
        return {
            "status": "success",
            "message": "API is accessible"
        }

@status_ns.route('')
class StatusResource(Resource):
    @api.doc(description='Get drone connection status')
    @api.response(200, 'Success', status_model)
    def get(self):
        """Get drone connection status"""
        return {
            "connected": connected,
            "drone_data": drone_data
        }

@video_ns.route('/feed')
class VideoFeed(Resource):
    @api.doc(description='Get video feed from drone')
    def get(self):
        """Get video feed from drone"""
        # This returns a streaming response, which needs different handling
        return Response(generate_frames(), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')

@status_ns.route('/drone_data')
class DroneDataResource(Resource):
    @api.doc(description='Get drone telemetry data')
    @api.response(200, 'Success', drone_data_model)
    def get(self):
        """Get drone telemetry data"""
        return drone_data

@drone_ns.route('/takeoff')
class Takeoff(Resource):
    @api.doc(description='Takeoff the drone')
    @api.response(200, 'Success', response_model)
    def get(self):
        """Command the drone to takeoff"""
        if not connected or not drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone.takeoff()
            return {"success": True, "message": "Décollage réussi"}
        except Exception as e:
            return {"success": False, "message": f"Erreur: {str(e)}"}

@drone_ns.route('/land')
class Land(Resource):
    @api.doc(description='Land the drone')
    @api.response(200, 'Success', response_model)
    def get(self):
        """Command the drone to land"""
        if not connected or not drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone.land()
            return {"success": True, "message": "Atterrissage réussi"}
        except Exception as e:
            return {"success": False, "message": f"Erreur: {str(e)}"}

# Add more endpoints here following the same format

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
