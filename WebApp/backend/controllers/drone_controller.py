from flask_restx import Namespace, Resource, fields
from services.drone_service import DroneService
from services.video_service import VideoService

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
            
        return {"success": success, "message": message}

@drone_ns.route('/disconnect')
class DroneDisconnect(Resource):
    @drone_ns.doc(description='Déconnecter du drone')
    @drone_ns.response(200, 'Succès', response_model)
    def get(self):
        """Déconnecter du drone"""
        # Arrêter le streaming vidéo d'abord
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

# Vous pouvez ajouter d'autres endpoints ici pour les commandes supplémentaires
# comme les mouvements, la rotation, etc.