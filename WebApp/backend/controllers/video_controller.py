from flask import Response
from flask_restx import Namespace, Resource, fields
from services.video_service import VideoService

# Create namespace
video_ns = Namespace('video', description='Drone video stream')

# Response model for Swagger documentation
response_model = video_ns.model('Response', {
    'success': fields.Boolean(description='Operation success status'),
    'message': fields.String(description='Response message')
})

# Initialize service
video_service = VideoService()

@video_ns.route('/feed')
class VideoFeed(Resource):
    @video_ns.doc(description='Get the drone video stream')
    def get(self):
        """Get the drone video stream"""
        # Return a continuous MJPEG stream
        return Response(video_service.generate_frames(), 
                      mimetype='multipart/x-mixed-replace; boundary=frame')

@video_ns.route('/start')
class StartVideo(Resource):
    @video_ns.doc(description='Start video streaming')
    @video_ns.response(200, 'Success', response_model)
    def get(self):
        """Start video streaming"""
        success, message = video_service.start_video_stream()
        return {"success": success, "message": message}

@video_ns.route('/stop')
class StopVideo(Resource):
    @video_ns.doc(description='Stop video streaming')
    @video_ns.response(200, 'Success', response_model)
    def get(self):
        """Stop video streaming"""
        success, message = video_service.stop_video_stream()
        return {"success": success, "message": message}

@video_ns.route('/faces/show')
class ShowFaces(Resource):
    @video_ns.doc(description='Show face recognition overlay in video')
    @video_ns.response(200, 'Success', response_model)
    def get(self):
        """Show face recognition overlay in video"""
        success, message = video_service.enable_face_overlay()
        return {"success": success, "message": message}

@video_ns.route('/faces/hide')
class HideFaces(Resource):
    @video_ns.doc(description='Hide face recognition overlay in video')
    @video_ns.response(200, 'Success', response_model)
    def get(self):
        """Hide face recognition overlay in video"""
        success, message = video_service.disable_face_overlay()
        return {"success": success, "message": message}