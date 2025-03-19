from flask_restx import Namespace, Resource, fields
from services.drone_service import DroneService
from services.video_service import VideoService
from services.face_recognition_service import FaceRecognitionService
import os

# Création du namespace
drone_ns = Namespace('drone', description='Opérations du drone')

# Modèle de réponse pour la documentation Swagger
response_model = drone_ns.model('Response', {
    'success': fields.Boolean(description='Statut de succès de l\'opération'),
    'message': fields.String(description='Message de réponse')
})

# Initialisation des services
drone_service = DroneService()
video_service = VideoService()
face_recognition_service = FaceRecognitionService()

@drone_ns.route('/connect')
class DroneConnect(Resource):
    @drone_ns.doc(description='Connecter au drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Connecter au drone"""
        success, message = drone_service.connect()

        # Si la connexion est réussie, démarrer le streaming vidéo
        if success:
            video_service.start_video_stream()

            # Try to start face recognition if we have known faces
            if os.path.exists("known_faces") and len(os.listdir("known_faces")) > 0:
                face_recognition_service.start_recognition()

        return {"success": success, "message": message}

@drone_ns.route('/disconnect')
class DroneDisconnect(Resource):
    @drone_ns.doc(description='Déconnecter du drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Déconnecter du drone"""
        # Stop face recognition first
        face_recognition_service.stop_recognition()

        # Arrêter le streaming vidéo ensuite
        video_service.stop_video_stream()

        success, message = drone_service.disconnect()
        return {"success": success, "message": message}

@drone_ns.route('/takeoff')
class Takeoff(Resource):
    @drone_ns.doc(description='Faire décoller le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire décoller le drone"""
        success, message = drone_service.takeoff()
        return {"success": success, "message": message}

@drone_ns.route('/land')
class Land(Resource):
    @drone_ns.doc(description='Faire atterrir le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire atterrir le drone"""
        success, message = drone_service.land()
        return {"success": success, "message": message}

# Routes à ajouter au fichier existant WebApp/backend/controllers/drone_controller.py

@drone_ns.route('/move/up')
class MoveUp(Resource):
    @drone_ns.doc(description='Faire monter le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire monter le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(0, 0, 70, 0)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande de montée envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la montée: {str(e)}"}

@drone_ns.route('/move/down')
class MoveDown(Resource):
    @drone_ns.doc(description='Faire descendre le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire descendre le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(0, 0, -70, 0)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande de descente envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la descente: {str(e)}"}

@drone_ns.route('/move/left')
class MoveLeft(Resource):
    @drone_ns.doc(description='Déplacer le drone vers la gauche')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Déplacer le drone vers la gauche"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(-70, 0, 0, 0)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande de déplacement vers la gauche envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors du déplacement vers la gauche: {str(e)}"}

@drone_ns.route('/move/right')
class MoveRight(Resource):
    @drone_ns.doc(description='Déplacer le drone vers la droite')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Déplacer le drone vers la droite"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(70, 0, 0, 0)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande de déplacement vers la droite envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors du déplacement vers la droite: {str(e)}"}

@drone_ns.route('/move/forward')
class MoveForward(Resource):
    @drone_ns.doc(description='Faire avancer le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire avancer le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(0, 70, 0, 0)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande d'avancer envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de l'avancée: {str(e)}"}

@drone_ns.route('/move/backward')
class MoveBackward(Resource):
    @drone_ns.doc(description='Faire reculer le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire reculer le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(0, -70, 0, 0)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande de reculer envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors du recul: {str(e)}"}

@drone_ns.route('/rotate/left')
class RotateLeft(Resource):
    @drone_ns.doc(description='Faire tourner le drone vers la gauche')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire tourner le drone vers la gauche"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(0, 0, 0, -70)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande de rotation à gauche envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la rotation à gauche: {str(e)}"}

@drone_ns.route('/rotate/right')
class RotateRight(Resource):
    @drone_ns.doc(description='Faire tourner le drone vers la droite')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire tourner le drone vers la droite"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(0, 0, 0, 70)  # lr, fb, ud, yaw
            return {"success": True, "message": "Commande de rotation à droite envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la rotation à droite: {str(e)}"}

@drone_ns.route('/flip/forward')
class FlipForward(Resource):
    @drone_ns.doc(description='Faire un looping avant avec le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire un looping avant avec le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.flip_forward()
            return {"success": True, "message": "Commande de looping avant envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors du looping avant: {str(e)}"}

@drone_ns.route('/flip/backward')
class FlipBackward(Resource):
    @drone_ns.doc(description='Faire un looping arrière avec le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire un looping arrière avec le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.flip_backward()
            return {"success": True, "message": "Commande de looping arrière envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors du looping arrière: {str(e)}"}

@drone_ns.route('/flip/left')
class FlipLeft(Resource):
    @drone_ns.doc(description='Faire un looping à gauche avec le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire un looping à gauche avec le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.flip_left()
            return {"success": True, "message": "Commande de looping à gauche envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors du looping à gauche: {str(e)}"}

@drone_ns.route('/flip/right')
class FlipRight(Resource):
    @drone_ns.doc(description='Faire un looping à droite avec le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Faire un looping à droite avec le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.flip_right()
            return {"success": True, "message": "Commande de looping à droite envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors du looping à droite: {str(e)}"}

@drone_ns.route('/emergency')
class Emergency(Resource):
    @drone_ns.doc(description='Arrêt d\'urgence du drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Arrêt d'urgence du drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.emergency()
            return {"success": True, "message": "Commande d'arrêt d'urgence envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de l'arrêt d'urgence: {str(e)}"}

@drone_ns.route('/speech')
class SpeechRecognition(Resource):
    @drone_ns.doc(description='Activer la reconnaissance vocale')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Activer la reconnaissance vocale"""
        try:
            # Cette implémentation nécessiterait d'importer speechRecognitionModule
            # from speechRecognitionModule import speechToText
            # command = speechToText()
            # if command:
            #     # Traiter la commande
            #     pass
            return {"success": True, "message": "Reconnaissance vocale activée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de l'activation de la reconnaissance vocale: {str(e)}"}

@drone_ns.route('/quit')
class Quit(Resource):
    @drone_ns.doc(description='Quitter le programme')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Quitter le programme (atterrissage puis déconnexion)"""
        # Stop face recognition
        face_recognition_service.stop_recognition()

        if drone_service.connected and drone_service.drone:
            try:
                drone_service.drone.land()
                drone_service.disconnect()
            except Exception as e:
                print(f"Erreur lors de la déconnexion: {str(e)}")
        return {"success": True, "message": "Drone déconnecté et prêt à quitter"}

# Routes supplémentaires pour le hover et autres fonctionnalités

@drone_ns.route('/hover')
class Hover(Resource):
    @drone_ns.doc(description='Maintenir le drone en vol stationnaire')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Maintenir le drone en vol stationnaire"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            drone_service.drone.send_rc_control(0, 0, 0, 0)  # Arrêter tous les mouvements
            return {"success": True, "message": "Commande de vol stationnaire envoyée"}
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la commande de vol stationnaire: {str(e)}"}

@drone_ns.route('/capture_photo')
class CapturePhoto(Resource):
    @drone_ns.doc(description='Prendre une photo avec le drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Prendre une photo avec le drone"""
        if not drone_service.connected or not drone_service.drone:
            return {"success": False, "message": "Drone non connecté"}
        try:
            # Récupérer le frame actuel
            frame = drone_service.drone.get_frame_read().frame

            # Utiliser OpenCV pour convertir l'image en JPEG
            import cv2
            import os
            import base64
            from datetime import datetime
            from io import BytesIO

            # Créer le dossier photos s'il n'existe pas
            if not os.path.exists("photos"):
                os.makedirs("photos")

            # Générer un nom de fichier avec la date et l'heure
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"photos/photo_{timestamp}.jpg"

            # Sauvegarder l'image sur le disque
            cv2.imwrite(filename, frame)

            # Convertir l'image en base64 pour l'envoyer au frontend
            _, buffer = cv2.imencode('.jpg', frame)
            img_str = base64.b64encode(buffer).decode('utf-8')

            return {
                "success": True, 
                "message": f"Photo prise et sauvegardée sous {filename}",
                "image": f"data:image/jpeg;base64,{img_str}"  # Format correct pour l'affichage HTML
            }
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la prise de photo: {str(e)}"}

# Vous pouvez ajouter d'autres endpoints ici pour les commandes supplémentaires
# comme les mouvements, la rotation, etc.