import os
import cv2
import threading
import time
import numpy as np
import logging
import pickle
from datetime import datetime
from services.drone_service import DroneService
from services.video_service import VideoService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('face_recognition')

class FaceRecognitionService:
    """Service for facial recognition using the drone's camera with OpenCV"""

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
        self.model_data_dir = "model_data"
        self.face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(self.face_cascade_path)

        # Create face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Recognition data
        self.known_faces = []
        self.known_names = []
        self.recognized_faces = []
        self.last_recognition_time = 0
        self.recognition_cooldown = 1.0  # Seconds between recognition attempts

        # Ensure directories exist
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            logger.info(f"Created directory {self.known_faces_dir}")

        if not os.path.exists(self.model_data_dir):
            os.makedirs(self.model_data_dir)
            logger.info(f"Created directory {self.model_data_dir}")

        # Load known faces on initialization
        self.load_known_faces()

    def _prepare_training_data(self):
        """Prepare training data from face images"""
        faces = []
        labels = []
        label_ids = {}
        current_id = 0

        # Process each image in the known_faces directory
        valid_extensions = ['.jpg', '.jpeg', '.png']

        for filename in os.listdir(self.known_faces_dir):
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                # Get person name from filename
                person_name = os.path.splitext(filename)[0]
                if '_' in person_name:  # Handle timestamp in filename
                    person_name = person_name.split('_')[0]

                # Assign a numeric ID to each name
                if person_name not in label_ids:
                    label_ids[person_name] = current_id
                    current_id += 1

                # Load and process image
                image_path = os.path.join(self.known_faces_dir, filename)
                image = cv2.imread(image_path)

                if image is None:
                    logger.warning(f"Could not read image: {image_path}")
                    continue

                # Convert to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces
                face_rects = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                # Process each face
                for (x, y, w, h) in face_rects:
                    roi = gray[y:y+h, x:x+w]
                    faces.append(roi)
                    labels.append(label_ids[person_name])

        # Create reverse mapping from ID to name
        id_to_name = {v: k for k, v in label_ids.items()}

        return faces, labels, id_to_name

    def train_recognizer(self):
        """Train the face recognizer with known faces"""
        faces, labels, id_to_name = self._prepare_training_data()

        if len(faces) == 0:
            logger.warning("No faces found for training")
            return False

        # Convert labels to numpy array
        labels = np.array(labels)

        # Train the recognizer
        self.recognizer.train(faces, labels)

        # Save the trained model
        model_path = os.path.join(self.model_data_dir, "trained_model.yml")
        self.recognizer.save(model_path)

        # Save the label mapping
        label_map_path = os.path.join(self.model_data_dir, "label_map.pkl")
        with open(label_map_path, 'wb') as f:
            pickle.dump(id_to_name, f)

        # Store the mapping in memory
        self.known_names = id_to_name

        logger.info(f"Trained recognizer with {len(faces)} faces of {len(id_to_name)} people")
        return True

    def load_known_faces(self):
        """Load known faces and trained model"""
        model_path = os.path.join(self.model_data_dir, "trained_model.yml")
        label_map_path = os.path.join(self.model_data_dir, "label_map.pkl")

        # Check if we have a trained model
        if os.path.exists(model_path) and os.path.exists(label_map_path):
            try:
                # Load the face recognizer model
                self.recognizer.read(model_path)

                # Load the label mapping
                with open(label_map_path, 'rb') as f:
                    self.known_names = pickle.load(f)

                logger.info(f"Loaded trained model with {len(self.known_names)} people")
                return True
            except Exception as e:
                logger.error(f"Error loading trained model: {e}")

        # If no model exists or loading failed, try to train a new one
        return self.train_recognizer()

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

            if image is None:
                return False, "Invalid image data"

            # Check if a face is present
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) == 0:
                return False, "No face detected in the image"

            # Save the image
            cv2.imwrite(file_path, image)
            logger.info(f"Saved face image for {person_name} to {file_path}")

            # Retrain the recognizer
            success = self.train_recognizer()

            if not success:
                return False, "Failed to train recognizer with the new face"

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
        if not self.known_names:
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
        confidence_threshold = 70  # Lower values are better for LBPH

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

                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

                # Reset recognized faces for this frame
                current_faces = []

                # Process each face
                for (x, y, w, h) in faces:
                    # Extract face region
                    face_roi = gray[y:y+h, x:x+w]

                    # Predict the person
                    try:
                        label_id, confidence = self.recognizer.predict(face_roi)

                        # Lower confidence values are better in LBPH
                        recognition_confidence = max(0, 1 - (confidence / 100))

                        # If confidence is good enough
                        if confidence < confidence_threshold and label_id in self.known_names:
                            name = self.known_names[label_id]

                            # Create face info
                            face_info = {
                                "name": name,
                                "confidence": float(recognition_confidence),
                                "location": {
                                    "top": y,
                                    "right": x + w,
                                    "bottom": y + h,
                                    "left": x
                                },
                                "timestamp": current_time
                            }
                            current_faces.append(face_info)
                    except Exception as e:
                        logger.error(f"Error during face prediction: {e}")

                # Update recognized faces
                self.recognized_faces = current_faces
                self.last_recognition_time = current_time

            except Exception as e:
                logger.error(f"Error in face recognition loop: {e}")
                time.sleep(0.5)  # Longer pause on error

        logger.info("Face recognition loop ended")
        self.is_running = False