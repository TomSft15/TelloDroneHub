import os
import cv2
import face_recognition
import threading
import time
import numpy as np
import logging
from datetime import datetime
from services.drone_service import DroneService
from services.video_service import VideoService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('face_recognition')

class FaceRecognitionService:
    """Service for facial recognition using the drone's camera"""

    _instance = None

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(FaceRecognitionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the facial recognition service"""
        if self._initialized:
            return

        self._initialized = True
        self.drone_service = DroneService()
        self.video_service = VideoService()
        self.is_running = False
        self.recognition_thread = None
        self.stop_event = threading.Event()

        # Face recognition data
        self.known_faces_dir = "known_faces"
        self.known_face_encodings = []
        self.known_face_names = []
        self.recognized_faces = []
        self.last_recognition_time = 0
        self.recognition_cooldown = 1.0  # Seconds between recognition attempts

        # Ensure known_faces directory exists
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            logger.info(f"Created directory {self.known_faces_dir}")

        # Load known faces on initialization
        self.load_known_faces()

    def load_known_faces(self):
        """Load known faces from the known_faces directory"""
        # Clear existing data
        self.known_face_encodings = []
        self.known_face_names = []

        logger.info(f"Loading known faces from {self.known_faces_dir}")

        # Check if directory exists
        if not os.path.exists(self.known_faces_dir):
            logger.warning(f"Directory {self.known_faces_dir} does not exist")
            return False

        # Get all image files
        valid_extensions = ['.jpg', '.jpeg', '.png']
        count = 0

        for filename in os.listdir(self.known_faces_dir):
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                # Extract person name from filename (without extension)
                person_name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.known_faces_dir, filename)

                try:
                    # Load and encode the face
                    face_image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(face_image)

                    if len(face_encodings) > 0:
                        # Take the first face found
                        face_encoding = face_encodings[0]
                        self.known_face_encodings.append(face_encoding)
                        self.known_face_names.append(person_name)
                        count += 1
                        logger.info(f"Loaded face for {person_name}")
                    else:
                        logger.warning(f"No face detected in {filename}")
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")

        logger.info(f"Loaded {count} known faces")
        return count > 0

    def add_face(self, image_data, person_name):
        """
        Add a new face to the known_faces directory

        Args:
            image_data: Binary image data
            person_name: Name of the person

        Returns:
            tuple: (success, message)
        """
        try:
            # Ensure the name is valid for a filename
            person_name = "".join(c for c in person_name if c.isalnum() or c in ' _-').strip()
            if not person_name:
                return False, "Invalid person name"

            # Create filename with timestamp to avoid overwriting
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{person_name}_{timestamp}.jpg"
            file_path = os.path.join(self.known_faces_dir, filename)

            # Convert image data to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Check if a face is present
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)

            if not face_locations:
                return False, "No face detected in the image"

            # Save the image
            cv2.imwrite(file_path, image)

            # Reload known faces
            self.load_known_faces()

            return True, f"Face for {person_name} added successfully"
        except Exception as e:
            logger.error(f"Error adding face: {e}")
            return False, f"Error adding face: {str(e)}"

    def start_recognition(self):
        """Start the face recognition process"""
        if self.is_running:
            return True, "Face recognition is already running"

        if not self.drone_service.connected or not self.drone_service.drone:
            return False, "Drone not connected"

        # Check if we have any known faces
        if not self.known_face_encodings:
            success = self.load_known_faces()
            if not success:
                return False, "No known faces found. Please add faces first."

        try:
            # Reset the stop event
            self.stop_event.clear()
            self.is_running = True

            # Start the recognition thread
            self.recognition_thread = threading.Thread(target=self._recognition_loop, daemon=True)
            self.recognition_thread.start()

            logger.info("Face recognition started")
            return True, "Face recognition started"
        except Exception as e:
            self.is_running = False
            logger.error(f"Error starting face recognition: {e}")
            return False, f"Error starting face recognition: {str(e)}"

    def stop_recognition(self):
        """Stop the face recognition process"""
        if not self.is_running:
            return True, "Face recognition is already stopped"

        try:
            # Signal the thread to stop
            self.stop_event.set()

            # Wait for thread to end (with timeout)
            if self.recognition_thread and self.recognition_thread.is_alive():
                self.recognition_thread.join(timeout=1.0)

            self.is_running = False
            self.recognized_faces = []

            logger.info("Face recognition stopped")
            return True, "Face recognition stopped"
        except Exception as e:
            logger.error(f"Error stopping face recognition: {e}")
            return False, f"Error stopping face recognition: {str(e)}"

    def get_recognized_faces(self):
        """Get currently recognized faces"""
        return self.recognized_faces

    def _recognition_loop(self):
        """Main loop for face recognition"""
        logger.info("Starting face recognition loop")

        while not self.stop_event.is_set() and self.drone_service.connected:
            try:
                current_time = time.time()

                # Limit recognition frequency
                if current_time - self.last_recognition_time < self.recognition_cooldown:
                    time.sleep(0.01)  # Short pause to avoid high CPU usage
                    continue

                # Get current frame from video service
                with self.video_service.frame_lock:
                    if self.video_service.frame is None:
                        time.sleep(0.1)
                        continue

                    frame = self.video_service.frame.copy()

                # Convert to RGB for face_recognition
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Find faces in the frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                # Reset recognized faces for this frame
                current_faces = []

                # Check each face against known faces
                for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                    # Compare with known faces
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = 0

                    # Use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            confidence = 1 - face_distances[best_match_index]

                    # Add to recognized faces if confidence is high enough
                    if name != "Unknown" and confidence > 0.6:
                        # Create a dict with name, confidence, and face location
                        face_info = {
                            "name": name,
                            "confidence": float(confidence),
                            "location": {
                                "top": top,
                                "right": right,
                                "bottom": bottom,
                                "left": left
                            },
                            "timestamp": current_time
                        }
                        current_faces.append(face_info)

                # Update recognized faces
                self.recognized_faces = current_faces
                self.last_recognition_time = current_time

            except Exception as e:
                logger.error(f"Error in face recognition loop: {e}")
                time.sleep(0.5)  # Longer pause on error

        logger.info("Face recognition loop ended")
        self.is_running = False