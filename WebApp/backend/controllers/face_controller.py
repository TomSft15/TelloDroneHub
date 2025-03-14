import time
from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from services.face_recognition_service import FaceRecognitionService

# Create namespace
face_ns = Namespace('face', description='Face recognition operations')

# Models for Swagger documentation
response_model = face_ns.model('Response', {
    'success': fields.Boolean(description='Operation success status'),
    'message': fields.String(description='Response message')
})

recognition_result_model = face_ns.model('RecognitionResult', {
    'name': fields.String(description='Name of the recognized person or "Unknown"'),
    'position': fields.List(fields.Integer, description='Face position [x, y, width, height]')
})

recognitions_model = face_ns.model('Recognitions', {
    'recognitions': fields.List(fields.Nested(recognition_result_model)),
    'timestamp': fields.Float(description='Timestamp of the recognition')
})

known_faces_model = face_ns.model('KnownFaces', {
    'faces': fields.List(fields.String, description='Names of known faces')
})

# File upload parser
upload_parser = face_ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Face image file')
upload_parser.add_argument('name', location='form', type=str, required=True, help='Name of the person')

# Initialize service
face_service = FaceRecognitionService()

@face_ns.route('/start')
class StartRecognition(Resource):
    @face_ns.doc(description='Start face recognition')
    @face_ns.response(200, 'Success', response_model)
    def get(self):
        """Start face recognition"""
        success, message = face_service.start_recognition()
        return {"success": success, "message": message}

@face_ns.route('/stop')
class StopRecognition(Resource):
    @face_ns.doc(description='Stop face recognition')
    @face_ns.response(200, 'Success', response_model)
    def get(self):
        """Stop face recognition"""
        success, message = face_service.stop_recognition()
        return {"success": success, "message": message}

@face_ns.route('/current')
class CurrentRecognitions(Resource):
    @face_ns.doc(description='Get current face recognition results')
    @face_ns.response(200, 'Success', recognitions_model)
    def get(self):
        """Get current face recognition results"""
        recognitions = face_service.get_current_recognitions()
        return {
            "recognitions": recognitions,
            "timestamp": time.time()
        }

@face_ns.route('/upload')
class UploadFace(Resource):
    @face_ns.doc(description='Upload a face image', parser=upload_parser)
    @face_ns.response(200, 'Success', response_model)
    def post(self):
        """Upload a face image"""
        args = upload_parser.parse_args()
        file = args['file']
        name = args['name']

        success, message = face_service.upload_face(file, name)
        return {"success": success, "message": message}

@face_ns.route('/delete/<string:name>')
class DeleteFace(Resource):
    @face_ns.doc(description='Delete a face')
    @face_ns.response(200, 'Success', response_model)
    def delete(self, name):
        """Delete a face"""
        success, message = face_service.delete_face(name)
        return {"success": success, "message": message}

@face_ns.route('/list')
class ListFaces(Resource):
    @face_ns.doc(description='List all known faces')
    @face_ns.response(200, 'Success', known_faces_model)
    def get(self):
        """List all known faces"""
        faces = face_service.get_known_faces()
        return {"faces": faces}

@face_ns.route('/reload')
class ReloadFaces(Resource):
    @face_ns.doc(description='Reload known faces')
    @face_ns.response(200, 'Success', response_model)
    def get(self):
        """Reload known faces"""
        success, message = face_service.load_known_faces()
        return {"success": success, "message": message}