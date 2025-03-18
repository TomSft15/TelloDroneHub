from flask_restx import Namespace, Resource, fields
from services.face_tracking_service import FaceTrackingService
from services.drone_service import DroneService

# Création du namespace
face_tracking_ns = Namespace('face_tracking', description='Opérations de suivi de visage')

# Modèle de réponse pour la documentation Swagger
response_model = face_tracking_ns.model('Response', {
    'success': fields.Boolean(description='Statut de succès de l\'opération'),
    'message': fields.String(description='Message de réponse')
})

# Modèle de statut pour la documentation Swagger
status_model = face_tracking_ns.model('FaceTrackingStatus', {
    'is_tracking': fields.Boolean(description='État de fonctionnement du suivi'),
    'settings': fields.Raw(description='Paramètres de suivi'),
    'face_detected': fields.Boolean(description='Indique si un visage est actuellement détecté')
})

# Modèle pour la mise à jour des paramètres
settings_model = face_tracking_ns.model('Settings', {
    'detection_frequency': fields.Float(description='Fréquence de détection en secondes'),
    'rotation_speed': fields.Integer(description='Vitesse de rotation (0-100)'),
    'deadzone_x': fields.Integer(description='Zone morte de détection horizontale (pixels)'),
    'face_size_min': fields.Integer(description='Taille minimale du visage à détecter')
})

# Initialisation du service
face_tracking_service = FaceTrackingService()
drone_service = DroneService()

# Initialiser le service de suivi avec le service drone
face_tracking_service.init_drone_service(drone_service)

@face_tracking_ns.route('/start')
class FaceTrackingStart(Resource):
    @face_tracking_ns.doc(description='Démarrer le suivi de visage')
    @face_tracking_ns.response(200, 'Succès', response_model)
    def get(self):
        """Démarrer le suivi de visage"""
        success, message = face_tracking_service.start_face_tracking()
        return {"success": success, "message": message}

@face_tracking_ns.route('/stop')
class FaceTrackingStop(Resource):
    @face_tracking_ns.doc(description='Arrêter le suivi de visage')
    @face_tracking_ns.response(200, 'Succès', response_model)
    def get(self):
        """Arrêter le suivi de visage"""
        success, message = face_tracking_service.stop_face_tracking()
        return {"success": success, "message": message}

@face_tracking_ns.route('/status')
class FaceTrackingStatus(Resource):
    @face_tracking_ns.doc(description='Obtenir l\'état du suivi de visage')
    @face_tracking_ns.response(200, 'Succès', status_model)
    def get(self):
        """Obtenir l'état du suivi de visage"""
        return face_tracking_service.get_status()

@face_tracking_ns.route('/settings')
class FaceTrackingSettings(Resource):
    @face_tracking_ns.doc(description='Mettre à jour les paramètres de suivi')
    @face_tracking_ns.expect(settings_model)
    @face_tracking_ns.response(200, 'Succès', response_model)
    def post(self):
        """Mettre à jour les paramètres de suivi"""
        settings = face_tracking_ns.payload
        success, message = face_tracking_service.update_settings(settings)
        return {"success": success, "message": message}