from flask_restx import Namespace, Resource, fields
from services.drone_service import DroneService

# Création du namespace
status_ns = Namespace('status', description='Statut du drone')

# Modèles pour la documentation Swagger
drone_data_model = status_ns.model('DroneData', {
    'battery': fields.Integer(description='Pourcentage de batterie'),
    'temperature': fields.Integer(description='Température en Celsius'),
    'flight_time': fields.Integer(description='Temps de vol en secondes'),
    'height': fields.Integer(description='Hauteur en cm'),
    'speed': fields.Integer(description='Vitesse en cm/s'),
    'signal': fields.Integer(description='Force du signal')
})

status_model = status_ns.model('Status', {
    'connected': fields.Boolean(description='Si le drone est connecté'),
    'drone_data': fields.Nested(drone_data_model)
})

# Initialisation du service
drone_service = DroneService()

@status_ns.route('')
class StatusResource(Resource):
    @status_ns.doc(description='Obtenir le statut de connexion du drone')
    @status_ns.response(200, 'Succès', status_model)
    def get(self):
        """Obtenir le statut de connexion du drone"""
        return {
            "connected": drone_service.connected,
            "drone_data": drone_service.get_drone_data()
        }

@status_ns.route('/drone_data')
class DroneDataResource(Resource):
    @status_ns.doc(description='Obtenir les données télémétriques du drone')
    @status_ns.response(200, 'Succès', drone_data_model)
    def get(self):
        """Obtenir les données télémétriques du drone"""
        return drone_service.get_drone_data()