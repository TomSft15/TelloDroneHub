from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from services.face_recognition_service import FaceRecognitionService
from services.video_service import VideoService
from services.drone_service import DroneService
from flask import jsonify
from datetime import datetime, timedelta

# Création du namespace
face_recognition_ns = Namespace('face_recognition', description='Opérations de reconnaissance faciale')

# Modèle de réponse pour la documentation Swagger
response_model = face_recognition_ns.model('Response', {
    'success': fields.Boolean(description='Statut de succès de l\'opération'),
    'message': fields.String(description='Message de réponse')
})

# Modèle pour les paramètres de configuration
settings_model = face_recognition_ns.model('FaceRecognitionSettings', {
    'confidence_threshold': fields.Float(description='Seuil de confiance pour la reconnaissance (0-1)'),
    'detection_interval': fields.Float(description='Intervalle entre les détections (secondes)'),
    'enable_tracking': fields.Boolean(description='Activer le suivi automatique'),
    'recognition_scale': fields.Float(description='Facteur de mise à l\'échelle pour la reconnaissance')
})

# Modèle pour les informations d'une personne
person_model = face_recognition_ns.model('Person', {
    'name': fields.String(description='Nom de la personne')
})

# Modèle pour le statut de la reconnaissance
status_model = face_recognition_ns.model('FaceRecognitionStatus', {
    'is_active': fields.Boolean(description='État d\'activation de la reconnaissance'),
    'known_faces_count': fields.Integer(description='Nombre de visages connus'),
    'known_faces': fields.List(fields.String, description='Liste des personnes connues'),
    'current_detections': fields.List(fields.Raw, description='Détections actuelles'),
    'settings': fields.Raw(description='Paramètres actuels')
})

# Modèle pour les informations d'une personne détectée
detected_person_model = face_recognition_ns.model('DetectedPerson', {
    'name': fields.String(description='Nom de la personne'),
    'confidence': fields.Float(description='Niveau de confiance (0-1)'),
    'position': fields.Raw(description='Position du visage dans l\'image'),
    'timestamp': fields.String(description='Horodatage de la détection')
})

# Modèle pour les statistiques de détection
detection_stats_model = face_recognition_ns.model('DetectionStats', {
    'total_faces_detected': fields.Integer(description='Nombre total de visages détectés'),
    'recognized_faces_count': fields.Integer(description='Nombre de visages reconnus'),
    'unknown_faces_count': fields.Integer(description='Nombre de visages inconnus')
})

# Modèle pour la réponse complète de détection du drone
detection_response_model = face_recognition_ns.model('DroneDetectionResponse', {
    'success': fields.Boolean(description='Statut de succès de l\'opération'),
    'is_drone_connected': fields.Boolean(description='État de connexion du drone'),
    'is_recognition_active': fields.Boolean(description='État d\'activation de la reconnaissance'),
    'current_detections': fields.List(fields.Nested(detected_person_model), description='Détections actuelles'),
    'recent_detections': fields.List(fields.String, description='Personnes détectées récemment'),
    'stats': fields.Nested(detection_stats_model, description='Statistiques de détection'),
    'battery_level': fields.Integer(description='Niveau de batterie du drone (%)'),
    'last_update': fields.String(description='Dernière mise à jour')
})

# Parser pour le téléchargement de fichiers
upload_parser = face_recognition_ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Fichier image')
upload_parser.add_argument('name', type=str, required=True, help='Nom de la personne')

# Initialisation des services
face_recognition_service = FaceRecognitionService()
video_service = VideoService()
drone_service = DroneService()

# Initialisation des services associés
face_recognition_service.init_services(video_service, drone_service)

@face_recognition_ns.route('/start')
class StartFaceRecognition(Resource):
    @face_recognition_ns.doc(description='Démarrer la reconnaissance faciale')
    @face_recognition_ns.response(200, 'Succès', response_model)
    def get(self):
        """Démarrer la reconnaissance faciale"""
        success, message = face_recognition_service.start_face_recognition()
        return {"success": success, "message": message}

@face_recognition_ns.route('/stop')
class StopFaceRecognition(Resource):
    @face_recognition_ns.doc(description='Arrêter la reconnaissance faciale')
    @face_recognition_ns.response(200, 'Succès', response_model)
    def get(self):
        """Arrêter la reconnaissance faciale"""
        success, message = face_recognition_service.stop_face_recognition()
        return {"success": success, "message": message}

@face_recognition_ns.route('/status')
class FaceRecognitionStatus(Resource):
    @face_recognition_ns.doc(description='Obtenir le statut de la reconnaissance faciale')
    @face_recognition_ns.response(200, 'Succès', status_model)
    def get(self):
        """Obtenir le statut de la reconnaissance faciale"""
        return face_recognition_service.get_recognition_status()

@face_recognition_ns.route('/settings')
class FaceRecognitionSettings(Resource):
    @face_recognition_ns.doc(description='Obtenir les paramètres de la reconnaissance faciale')
    @face_recognition_ns.response(200, 'Succès', settings_model)
    def get(self):
        """Obtenir les paramètres de la reconnaissance faciale"""
        return {"settings": face_recognition_service.settings}
    
    @face_recognition_ns.doc(description='Mettre à jour les paramètres de la reconnaissance faciale')
    @face_recognition_ns.expect(settings_model)
    @face_recognition_ns.response(200, 'Succès', response_model)
    def post(self):
        """Mettre à jour les paramètres de la reconnaissance faciale"""
        settings = face_recognition_ns.payload
        success, message = face_recognition_service.update_settings(settings)
        return {"success": success, "message": message}

@face_recognition_ns.route('/reload')
class ReloadFaces(Resource):
    @face_recognition_ns.doc(description='Recharger les visages connus depuis le dossier')
    @face_recognition_ns.response(200, 'Succès', response_model)
    def get(self):
        """Recharger les visages connus depuis le dossier"""
        success, message = face_recognition_service.load_known_faces()
        return {"success": success, "message": message}

@face_recognition_ns.route('/people')
class PeopleList(Resource):
    @face_recognition_ns.doc(description='Obtenir la liste des personnes connues')
    @face_recognition_ns.response(200, 'Succès')
    def get(self):
        """Obtenir la liste des personnes connues"""
        status = face_recognition_service.get_recognition_status()
        return {
            "success": True, 
            "people": [{"name": name} for name in status["known_faces"]]
        }

@face_recognition_ns.route('/people/<string:name>')
class Person(Resource):
    @face_recognition_ns.doc(description='Supprimer une personne')
    @face_recognition_ns.response(200, 'Succès', response_model)
    def delete(self, name):
        """Supprimer une personne"""
        success, message = face_recognition_service.delete_person(name)
        return {"success": success, "message": message}

@face_recognition_ns.route('/upload')
class UploadFace(Resource):
    @face_recognition_ns.doc(description='Télécharger une photo de visage')
    @face_recognition_ns.expect(upload_parser)
    @face_recognition_ns.response(200, 'Succès', response_model)
    def post(self):
        """Télécharger une photo de visage"""
        args = upload_parser.parse_args()
        file = args['file']
        name = args['name']
        
        success, message = face_recognition_service.add_person_from_uploaded_file(file, name)
        return {"success": success, "message": message}

@face_recognition_ns.route('/capture/<string:name>')
class CaptureFace(Resource):
    @face_recognition_ns.doc(description='Capturer une photo du flux vidéo actuel')
    @face_recognition_ns.response(200, 'Succès', response_model)
    def get(self, name):
        """Capturer une photo du flux vidéo actuel"""
        success, message = face_recognition_service.capture_face_photo(name)
        return {"success": success, "message": message}

@face_recognition_ns.route('/drone_detections')
class DroneDetection(Resource):
    @face_recognition_ns.doc(description='Obtenir les détections actuelles du drone')
    @face_recognition_ns.response(200, 'Succès', detection_response_model)
    def get(self):
        """Obtenir les détections actuelles et récentes du drone"""
        try:
            # Récupérer les détections actuelles
            current_detections = face_recognition_service.current_detections
            
            # Calculer les détections récentes (dernière minute)
            recent_detections = []
            now = datetime.now()
            one_minute_ago = now - timedelta(minutes=1)
            
            # Filtrer les dernières détections par personne dans la dernière minute
            for name, detection_time in face_recognition_service.last_detection.items():
                if isinstance(detection_time, datetime) and detection_time > one_minute_ago:
                    recent_detections.append(name)
            
            # Calculer les statistiques
            total_faces = len(current_detections)
            recognized_faces = len([d for d in current_detections if d["name"] != "Inconnu"])
            unknown_faces = total_faces - recognized_faces
            
            # Obtenir l'état du drone
            is_drone_connected = False
            battery_level = 0
            
            if drone_service and hasattr(drone_service, 'connected') and drone_service.connected:
                is_drone_connected = True
                try:
                    battery_level = drone_service.drone.get_battery()
                except:
                    battery_level = 0
            
            # Construire la réponse
            response = {
                "success": True,
                "is_drone_connected": is_drone_connected,
                "is_recognition_active": face_recognition_service.is_recognition_active,
                "current_detections": current_detections,
                "recent_detections": recent_detections,
                "stats": {
                    "total_faces_detected": total_faces,
                    "recognized_faces_count": recognized_faces,
                    "unknown_faces_count": unknown_faces
                },
                "battery_level": battery_level,
                "last_update": now.isoformat()
            }
            
            return jsonify(response)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Une erreur est survenue lors de la récupération des détections du drone"
            }, 500

@face_recognition_ns.route('/detection_history')
class DroneDetectionHistory(Resource):
    @face_recognition_ns.doc(description='Obtenir l\'historique des détections du drone')
    def get(self):
        """Obtenir l'historique des détections du drone"""
        try:
            # Cette fonction pourrait être étendue pour stocker et récupérer
            # un historique plus complet des détections dans une base de données
            
            # Pour l'instant, nous retournons simplement les dernières détections par personne
            detection_history = []
            
            for name, timestamp in face_recognition_service.last_detection.items():
                if isinstance(timestamp, datetime):
                    detection_history.append({
                        "name": name,
                        "last_seen": timestamp.isoformat()
                    })
            
            return {
                "success": True,
                "detection_history": detection_history
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Une erreur est survenue lors de la récupération de l'historique des détections"
            }, 500