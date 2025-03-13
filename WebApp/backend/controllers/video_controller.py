from flask import Response
from flask_restx import Namespace, Resource, fields
from services.video_service import VideoService

# Création du namespace
video_ns = Namespace('video', description='Flux vidéo du drone')

# Modèle de réponse pour la documentation Swagger
response_model = video_ns.model('Response', {
    'success': fields.Boolean(description='Statut de succès de l\'opération'),
    'message': fields.String(description='Message de réponse')
})

# Initialisation du service
video_service = VideoService()

@video_ns.route('/feed')
class VideoFeed(Resource):
    @video_ns.doc(description='Obtenir le flux vidéo du drone')
    def get(self):
        """Obtenir le flux vidéo du drone"""
        # Retourne un flux MJPEG en continu
        return Response(video_service.generate_frames(), 
                      mimetype='multipart/x-mixed-replace; boundary=frame')

@video_ns.route('/start')
class StartVideo(Resource):
    @video_ns.doc(description='Démarrer le streaming vidéo')
    @video_ns.response(200, 'Succès', response_model)
    def get(self):
        """Démarrer le streaming vidéo"""
        success, message = video_service.start_video_stream()
        return {"success": success, "message": message}

@video_ns.route('/stop')
class StopVideo(Resource):
    @video_ns.doc(description='Arrêter le streaming vidéo')
    @video_ns.response(200, 'Succès', response_model)
    def get(self):
        """Arrêter le streaming vidéo"""
        success, message = video_service.stop_video_stream()
        return {"success": success, "message": message}