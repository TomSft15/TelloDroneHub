from flask_restx import Namespace, Resource, fields
from services.gesture_service import GestureService

# Création du namespace
gesture_ns = Namespace('gesture', description='Opérations de reconnaissance gestuelle')

# Modèle de réponse pour la documentation Swagger
response_model = gesture_ns.model('Response', {
    'success': fields.Boolean(description='Statut de succès de l\'opération'),
    'message': fields.String(description='Message de réponse')
})

# Modèle de statut pour la documentation Swagger
status_model = gesture_ns.model('GestureStatus', {
    'is_running': fields.Boolean(description='État de fonctionnement de la détection'),
    'cooldown': fields.Float(description='Temps de refroidissement entre les gestes (en secondes)'),
    'last_gesture_time': fields.Float(description='Timestamp du dernier geste détecté'),
    'time_until_next': fields.Float(description='Temps restant avant le prochain geste (en secondes)')
})

# Modèle pour la mise à jour du cooldown
cooldown_model = gesture_ns.model('Cooldown', {
    'seconds': fields.Float(description='Temps de refroidissement en secondes (entre 0.5 et 10)')
})

# Initialisation du service
gesture_service = GestureService()

@gesture_ns.route('/start')
class GestureStart(Resource):
    @gesture_ns.doc(description='Démarrer la reconnaissance des gestes')
    @gesture_ns.response(200, 'Succès', response_model)
    def get(self):
        """Démarrer la reconnaissance des gestes"""
        success, message = gesture_service.start_gesture_detection()
        return {"success": success, "message": message}

@gesture_ns.route('/stop')
class GestureStop(Resource):
    @gesture_ns.doc(description='Arrêter la reconnaissance des gestes')
    @gesture_ns.response(200, 'Succès', response_model)
    def get(self):
        """Arrêter la reconnaissance des gestes"""
        success, message = gesture_service.stop_gesture_detection()
        return {"success": success, "message": message}

@gesture_ns.route('/status')
class GestureStatus(Resource):
    @gesture_ns.doc(description='Obtenir l\'état de la reconnaissance des gestes')
    @gesture_ns.response(200, 'Succès', status_model)
    def get(self):
        """Obtenir l'état de la reconnaissance des gestes"""
        return gesture_service.get_status()

@gesture_ns.route('/cooldown')
class GestureCooldown(Resource):
    @gesture_ns.doc(description='Définir le temps de refroidissement entre les gestes')
    @gesture_ns.expect(cooldown_model)
    @gesture_ns.response(200, 'Succès', response_model)
    def post(self):
        """Définir le temps de refroidissement entre les gestes"""
        seconds = gesture_ns.payload.get('seconds', 3.0)
        success, message = gesture_service.set_cooldown(seconds)
        return {"success": success, "message": message}