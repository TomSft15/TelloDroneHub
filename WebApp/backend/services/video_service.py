import threading
import time
import cv2
import numpy as np
from config import VIDEO_WIDTH, VIDEO_HEIGHT
from services.drone_service import DroneService

class VideoService:
    """Service for managing the drone's video stream"""

    _instance = None

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(VideoService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the video service"""
        if self._initialized:
            return

        self._initialized = True
        self.drone_service = DroneService()
        self.frame = None
        self.frame_lock = threading.Lock()
        self._video_thread = None
        self._streaming = False
        self.face_service = None  # Will be lazily initialized
        self.show_faces = False

        # Frame statistics for monitoring
        self.frame_count = 0
        self.fps = 0
        self.last_update_time = time.time()

    def start_video_stream(self):
        """Start video streaming from the drone"""
        if self._streaming:
            return True, "Video streaming already active"

        if not self.drone_service.connected or not self.drone_service.drone:
            return False, "Drone not connected"

        try:
            self.drone_service.drone.streamon()
            self._streaming = True

            # Reset statistics
            self.frame_count = 0
            self.fps = 0
            self.last_update_time = time.time()

            # Start the video capture thread
            self._video_thread = threading.Thread(
                target=self._capture_video, 
                daemon=True,
                name="VideoCaptureThread"
            )
            self._video_thread.start()

            return True, "Video streaming started"
        except Exception as e:
            return False, f"Error starting video stream: {str(e)}"

    def stop_video_stream(self):
        """Stop video streaming"""
        if not self._streaming:
            return True, "Video streaming already stopped"

        try:
            if self.drone_service.connected and self.drone_service.drone:
                self.drone_service.drone.streamoff()

            self._streaming = False

            # Wait for the video thread to finish
            if self._video_thread and self._video_thread.is_alive():
                self._video_thread.join(timeout=2.0)

            return True, "Video streaming stopped"
        except Exception as e:
            return False, f"Error stopping video stream: {str(e)}"

    def _capture_video(self):
        """Capture video frames in the background"""
        while self._streaming and self.drone_service.connected:
            try:
                # Get the frame from the drone
                frame_reader = self.drone_service.drone.get_frame_read()
                if frame_reader is None:
                    time.sleep(0.1)
                    continue

                current_frame = frame_reader.frame
                if current_frame is None:
                    time.sleep(0.1)
                    continue

                # Update frame count and calculate FPS
                self.frame_count += 1
                current_time = time.time()
                time_diff = current_time - self.last_update_time

                if time_diff >= 1.0:  # Update FPS every second
                    self.fps = self.frame_count / time_diff
                    self.frame_count = 0
                    self.last_update_time = current_time

                with self.frame_lock:
                    # Process the frame
                    self.frame = current_frame.copy()
                    self.frame = cv2.resize(self.frame, (VIDEO_WIDTH, VIDEO_HEIGHT))

                    # Add face recognition overlay if enabled
                    if self.show_faces:
                        # Lazy-load face service if needed
                        if self.face_service is None:
                            from services.face_recognition_service import FaceRecognitionService
                            self.face_service = FaceRecognitionService()

                        # Get current recognitions from the face service
                        recognitions = self.face_service.get_current_recognitions()

                        # Draw recognition results on frame
                        self._draw_recognitions(self.frame, recognitions)

                        # Add FPS information
                        cv2.putText(
                            self.frame, 
                            f"FPS: {self.fps:.1f}", 
                            (10, 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5, 
                            (0, 255, 0), 
                            1
                        )

            except Exception as e:
                print(f"Error capturing video: {e}")
                time.sleep(0.1)

    def _draw_recognitions(self, frame, recognitions):
        """Draw face recognition results on the frame"""
        for rec in recognitions:
            try:
                x, y, w, h = rec['position']
                name = rec['name']

                # Draw rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Draw name with background for better visibility
                text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                cv2.rectangle(
                    frame, 
                    (x, y - text_size[1] - 10), 
                    (x + text_size[0], y), 
                    (0, 255, 0), 
                    -1
                )
                cv2.putText(
                    frame, 
                    name, 
                    (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.9, 
                    (0, 0, 0), 
                    2
                )
            except Exception as e:
                print(f"Error drawing recognition: {e}")

    def generate_frames(self):
        """Generator that produces frames for MJPEG streaming"""
        while True:
            # If no connection or no frame, generate a "No signal" image
            if not self.drone_service.connected or self.frame is None:
                no_signal = self._create_no_signal_frame()
                ret, buffer = cv2.imencode('.jpg', no_signal)
                if ret:
                    yield (b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                time.sleep(0.5)
                continue

            # Safely get a copy of the current frame
            with self.frame_lock:
                if self.frame is None:
                    time.sleep(0.1)
                    continue

                frame_copy = self.frame.copy()

            # Encode the frame to JPEG
            try:
                ret, buffer = cv2.imencode('.jpg', frame_copy)
                if not ret:
                    time.sleep(0.1)
                    continue

                # Yield the frame for streaming
                yield (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            except Exception as e:
                print(f"Error encoding frame: {e}")
                time.sleep(0.1)

    def _create_no_signal_frame(self):
        """Create a 'No signal' image"""
        img = np.zeros((VIDEO_HEIGHT, VIDEO_WIDTH, 3), dtype=np.uint8)
        cv2.putText(
            img, 
            "No video signal", 
            (VIDEO_WIDTH//4, VIDEO_HEIGHT//2), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (255, 255, 255), 
            2
        )
        return img

    def enable_face_overlay(self):
        """Enable face recognition overlay on video"""
        self.show_faces = True

        # Lazy-load and start the face service if needed
        if self.face_service is None:
            from services.face_recognition_service import FaceRecognitionService
            self.face_service = FaceRecognitionService()

        # Make sure recognition is running
        self.face_service.start_recognition()

        return True, "Face recognition overlay enabled"

    def disable_face_overlay(self):
        """Disable face recognition overlay on video"""
        self.show_faces = False

        # Don't stop the recognition service - just hide the overlay
        # This allows the recognition to continue in the background if needed

        return True, "Face recognition overlay disabled"

    def get_fps(self):
        """Get the current frames per second rate"""
        return self.fps