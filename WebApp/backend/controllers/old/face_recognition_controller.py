from flask import request
from flask_restx import Namespace, Resource, fields
from services.face_recognition_service import FaceRecognitionService
from werkzeug.datastructures import FileStorage
import base64

# Create namespace
face_recognition_ns = Namespace('face_recognition', description='Face recognition operations')

# Response model for Swagger documentation
response_model = face_recognition_ns.model('Response', {
    'success': fields.Boolean(description='Operation success status'),
    'message': fields.String(description='Response message')
})

# Face model for Swagger documentation
face_model = face_recognition_ns.model('Face', {
    'name': fields.String(description='Person name'),
    'confidence': fields.Float(description='Recognition confidence score (0-1)'),
    'location': fields.Raw(description='Face location in the frame'),
    'timestamp': fields.Float(description='Recognition timestamp')
})

faces_model = face_recognition_ns.model('Faces', {
    'faces': fields.List(fields.Nested(face_model)),
    'count': fields.Integer(description='Number of faces recognized')
})

# File upload parser
upload_parser = face_recognition_ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Image file')
upload_parser.add_argument('name', type=str, required=True, help='Person name')

# Initialize service
face_recognition_service = FaceRecognitionService()

@face_recognition_ns.route('/start')
class StartRecognition(Resource):
    @face_recognition_ns.doc(description='Start face recognition')
    @face_recognition_ns.response(200, 'Success', response_model)
    def get(self):
        """Start face recognition"""
        success, message = face_recognition_service.start_recognition()
        return {"success": success, "message": message}

@face_recognition_ns.route('/stop')
class StopRecognition(Resource):
    @face_recognition_ns.doc(description='Stop face recognition')
    @face_recognition_ns.response(200, 'Success', response_model)
    def get(self):
        """Stop face recognition"""
        success, message = face_recognition_service.stop_recognition()
        return {"success": success, "message": message}

@face_recognition_ns.route('/add_face')
class AddFace(Resource):
    @face_recognition_ns.doc(description='Add a new face to recognize')
    @face_recognition_ns.expect(upload_parser)
    @face_recognition_ns.response(200, 'Success', response_model)
    def post(self):
        """Add a new face to recognize"""
        args = upload_parser.parse_args()
        file = args['file']
        name = args['name']

        if not file:
            return {"success": False, "message": "No file provided"}, 400

        try:
            image_data = file.read()
            success, message = face_recognition_service.add_face(image_data, name)

            return {"success": success, "message": message}
        except Exception as e:
            return {"success": False, "message": f"Error processing image: {str(e)}"}, 500

@face_recognition_ns.route('/add_face_base64')
class AddFaceBase64(Resource):
    @face_recognition_ns.doc(description='Add a new face using base64 image data')
    @face_recognition_ns.expect(face_recognition_ns.model('Base64Image', {
        'image_data': fields.String(description='Base64 encoded image data', required=True),
        'name': fields.String(description='Person name', required=True)
    }))
    @face_recognition_ns.response(200, 'Success', response_model)
    def post(self):
        """Add a new face using base64 image data"""
        data = request.json
        if not data or 'image_data' not in data or 'name' not in data:
            return {"success": False, "message": "Missing image data or name"}, 400

        try:
            # Extract base64 data after the "data:image/..." prefix if present
            image_data = data['image_data']
            if ',' in image_data:
                image_data = image_data.split(',', 1)[1]

            # Decode base64 data
            binary_data = base64.b64decode(image_data)

            success, message = face_recognition_service.add_face(binary_data, data['name'])

            return {"success": success, "message": message}
        except Exception as e:
            return {"success": False, "message": f"Error processing image: {str(e)}"}, 500

@face_recognition_ns.route('/present')
class RecognizedFaces(Resource):
    @face_recognition_ns.doc(description='Get currently recognized faces')
    @face_recognition_ns.response(200, 'Success', faces_model)
    def get(self):
        """Get currently recognized faces"""
        faces = face_recognition_service.get_recognized_faces()
        return {
            "faces": faces,
            "count": len(faces)
        }

@face_recognition_ns.route('/reload')
class ReloadFaces(Resource):
    @face_recognition_ns.doc(description='Reload known faces from disk')
    @face_recognition_ns.response(200, 'Success', response_model)
    def get(self):
        """Reload known faces from disk"""
        success = face_recognition_service.load_known_faces()
        return {
            "success": success,
            "message": "Known faces reloaded successfully" if success else "No faces found or error occurred"
        }