from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource

from controllers.drone_controller import drone_ns
from controllers.video_controller import video_ns
from controllers.status_controller import status_ns
from controllers.face_controller import face_ns
from controllers.health_controller import health_ns

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS to allow requests from the frontend

    # Initialize Swagger/Flask-RestX
    api = Api(app, version='1.0', title='Drone Control API',
            description='API for controlling a Tello drone with face recognition',
            doc='/swagger')  # Swagger UI will be available at /swagger

    # Register namespaces
    api.add_namespace(drone_ns)
    api.add_namespace(video_ns)
    api.add_namespace(status_ns)
    api.add_namespace(face_ns)
    api.add_namespace(health_ns)

    # Test endpoint
    @api.route('/test')
    class TestAPI(Resource):
        @api.doc(description='Test if API is accessible')
        def get(self):
            """Test if the API is accessible"""
            return {
                "status": "success",
                "message": "API is accessible"
            }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)