import os
import threading
import psutil
import time
from flask_restx import Namespace, Resource, fields
from services.video_service import VideoService
from services.face_recognition_service import FaceRecognitionService

# Create namespace
health_ns = Namespace('health', description='System health monitoring')

# Models for Swagger documentation
thread_model = health_ns.model('Thread', {
    'name': fields.String(description='Thread name'),
    'is_alive': fields.Boolean(description='Whether the thread is running')
})

health_model = health_ns.model('Health', {
    'cpu_usage': fields.Float(description='CPU usage percentage'),
    'memory_usage': fields.Float(description='Memory usage in MB'),
    'video_fps': fields.Float(description='Video frames per second'),
    'thread_count': fields.Integer(description='Number of active threads'),
    'threads': fields.List(fields.Nested(thread_model), description='List of important threads'),
    'timestamp': fields.Float(description='Time of health check')
})

# Initialize services
video_service = VideoService()
face_service = FaceRecognitionService()

@health_ns.route('')
class HealthCheck(Resource):
    @health_ns.doc(description='Get system health information')
    @health_ns.response(200, 'Success', health_model)
    def get(self):
        """Get system health information"""
        # Get CPU and memory usage
        process = psutil.Process(os.getpid())
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_info = process.memory_info()
        memory_usage = memory_info.rss / (1024 * 1024)  # Convert to MB

        # Get video FPS
        video_fps = video_service.get_fps()

        # Get thread information
        all_threads = threading.enumerate()
        important_thread_names = [
            "MainThread", 
            "VideoCaptureThread", 
            "FrameCollector", 
            "FaceRecognizer"
        ]
        important_threads = [
            {"name": t.name, "is_alive": t.is_alive()} 
            for t in all_threads 
            if t.name in important_thread_names
        ]

        # Return health data
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "video_fps": video_fps,
            "thread_count": len(all_threads),
            "threads": important_threads,
            "timestamp": time.time()
        }