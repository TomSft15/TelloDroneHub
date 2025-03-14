import os
import cv2
import numpy as np
import threading
import queue
import time
from config import KNOWN_FACES_DIR, FACE_RECOGNITION_INTERVAL, MAX_QUEUE_SIZE

class FaceRecognitionService:
    """Service for facial recognition from drone video stream"""

    _instance = None

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(FaceRecognitionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the face recognition service"""
        if self._initialized:
            return

        self._initialized = True
        self.video_service = None  # Will be initialized lazily
        self.known_faces = {}  # Dictionary of {name: face_encoding}
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Create the directory for known faces if it doesn't exist
        os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

        # Recognition results
        self.current_recognitions = []
        self.recognition_lock = threading.Lock()

        # Frame processing queue and thread
        self.frame_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)
        self._recognition_thread = None
        self._frame_processing_thread = None
        self._running = False

        # Frame count and processing interval
        self.frame_counter = 0
        self.process_every_n_frames = FACE_RECOGNITION_INTERVAL

        # Load known faces
        self.load_known_faces()

    def _get_video_service(self):
        """Get the video service instance (lazy initialization)"""
        if self.video_service is None:
            from services.video_service import VideoService
            self.video_service = VideoService()
        return self.video_service

    def load_known_faces(self):
        """Load known faces from the file system"""
        try:
            # Reset known faces
            self.known_faces = {}

            # Load face encodings for each image in the known faces directory
            for filename in os.listdir(KNOWN_FACES_DIR):
                # Only process image files
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Extract name from filename (e.g., "john_doe.jpg" -> "john_doe")
                    name = os.path.splitext(filename)[0]

                    # Load image and extract face encoding
                    image_path = os.path.join(KNOWN_FACES_DIR, filename)
                    image = cv2.imread(image_path)

                    if image is None:
                        print(f"Warning: Could not load image {image_path}")
                        continue

                    # Convert to RGB for face detection
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    # Detect faces
                    faces = self.face_cascade.detectMultiScale(
                        rgb_image,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30)
                    )

                    # If a face is found, use the first one
                    if len(faces) > 0:
                        x, y, w, h = faces[0]
                        face_roi = rgb_image[y:y+h, x:x+w]

                        # Calculate face encoding
                        face_encoding = self._calculate_face_encoding(face_roi)

                        # Store the encoding
                        self.known_faces[name] = face_encoding

            return True, f"Loaded {len(self.known_faces)} known faces"
        except Exception as e:
            return False, f"Error loading known faces: {str(e)}"

    def _calculate_face_encoding(self, face_image):
        """
        Calculate a simple face encoding using OpenCV
        For a POC, we'll use a simple approach: resize to a standard size and flatten
        A more robust approach would use dedicated face recognition libraries
        """
        # Resize to a standard size
        resized_face = cv2.resize(face_image, (100, 100))
        # Convert to grayscale
        gray_face = cv2.cvtColor(resized_face, cv2.COLOR_RGB2GRAY)
        # Flatten to a 1D array
        return gray_face.flatten()

    def start_recognition(self):
        """Start the face recognition process"""
        if self._running:
            return True, "Face recognition already running"

        # Mark as running before starting threads
        self._running = True

        # Clear the queue in case there are old frames
        with self.frame_queue.mutex:
            self.frame_queue.queue.clear()

        # Start the frame collection thread
        self._frame_collection_thread = threading.Thread(
            target=self._collect_frames, 
            daemon=True,
            name="FrameCollector"
        )
        self._frame_collection_thread.start()

        # Start the recognition thread
        self._recognition_thread = threading.Thread(
            target=self._recognition_worker, 
            daemon=True,
            name="FaceRecognizer"
        )
        self._recognition_thread.start()

        return True, "Face recognition started"

    def stop_recognition(self):
        """Stop the face recognition process"""
        if not self._running:
            return True, "Face recognition already stopped"

        # Signal threads to stop
        self._running = False

        # Clear the queue to unblock any waiting threads
        try:
            while True:
                self.frame_queue.get_nowait()
                self.frame_queue.task_done()
        except queue.Empty:
            pass

        # Wait for the threads to finish if they're running
        if self._frame_collection_thread and self._frame_collection_thread.is_alive():
            self._frame_collection_thread.join(timeout=2.0)

        if self._recognition_thread and self._recognition_thread.is_alive():
            self._recognition_thread.join(timeout=2.0)

        return True, "Face recognition stopped"

    def _collect_frames(self):
        """Thread to collect frames from the video service at regular intervals"""
        video_service = self._get_video_service()

        while self._running:
            try:
                # Skip frames based on counter
                self.frame_counter += 1
                if self.frame_counter % self.process_every_n_frames != 0:
                    time.sleep(0.01)  # Short sleep to prevent tight looping
                    continue

                # Reset counter to prevent overflow
                if self.frame_counter > 1000:
                    self.frame_counter = 0

                # Get the current frame if available
                with video_service.frame_lock:
                    if video_service.frame is None:
                        time.sleep(0.1)
                        continue

                    current_frame = video_service.frame.copy()

                # Try to add the frame to the queue, but don't block if full
                try:
                    self.frame_queue.put_nowait(current_frame)
                except queue.Full:
                    # If queue is full, skip this frame
                    pass

            except Exception as e:
                print(f"Error collecting frames: {e}")
                time.sleep(0.1)

    def _recognition_worker(self):
        """Worker thread to process frames from the queue"""
        while self._running:
            try:
                # Get a frame from the queue with timeout
                try:
                    frame = self.frame_queue.get(timeout=1.0)
                except queue.Empty:
                    continue

                # Process the frame
                self._process_frame(frame)

                # Mark task as done
                self.frame_queue.task_done()

            except Exception as e:
                print(f"Error in recognition worker: {e}")
                time.sleep(0.1)

    def _process_frame(self, frame):
        """Process a single frame for face recognition"""
        try:
            # Convert to RGB for face detection
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                rgb_frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            # Create new recognitions list
            new_recognitions = []

            # Process each detected face
            for (x, y, w, h) in faces:
                face_roi = rgb_frame[y:y+h, x:x+w]

                # Calculate face encoding
                face_encoding = self._calculate_face_encoding(face_roi)

                # Compare with known faces
                name = self._identify_face(face_encoding)

                # Add to recognitions
                new_recognitions.append({
                    'name': name,
                    'position': (x, y, w, h)
                })

            # Update current recognitions thread-safely
            with self.recognition_lock:
                self.current_recognitions = new_recognitions

        except Exception as e:
            print(f"Error processing frame: {e}")

    def _identify_face(self, face_encoding):
        """
        Identify a face by comparing its encoding with known faces
        Returns the name of the closest match, or "Unknown" if no close match
        """
        if not self.known_faces:
            return "Unknown"

        min_distance = float('inf')
        best_match = "Unknown"

        # Compare with each known face
        for name, known_encoding in self.known_faces.items():
            # Calculate Euclidean distance
            distance = np.linalg.norm(face_encoding - known_encoding)

            # Check if this is the closest match so far
            if distance < min_distance:
                min_distance = distance
                best_match = name

        # If the best match is too far away, mark as unknown
        # This threshold may need adjustment based on testing
        if min_distance > 8000:
            return "Unknown"

        return best_match

    def get_current_recognitions(self):
        """Get the current face recognition results"""
        with self.recognition_lock:
            return self.current_recognitions.copy()

    def upload_face(self, file, name):
        """
        Upload a new face image

        Parameters:
        file: The image file object
        name: The name to associate with the face

        Returns:
        (bool, str): Success status and message
        """
        try:
            # Create filename from name
            filename = f"{name.lower().replace(' ', '_')}.jpg"
            file_path = os.path.join(KNOWN_FACES_DIR, filename)

            # Save the file
            file.save(file_path)

            # Reload known faces
            success, message = self.load_known_faces()

            return success, f"Face uploaded for {name}" if success else message

        except Exception as e:
            return False, f"Error uploading face: {str(e)}"

    def delete_face(self, name):
        """
        Delete a face from known faces

        Parameters:
        name: The name of the face to delete

        Returns:
        (bool, str): Success status and message
        """
        try:
            # Find the file for this name
            filename = f"{name.lower().replace(' ', '_')}.jpg"
            file_path = os.path.join(KNOWN_FACES_DIR, filename)

            # Check if file exists
            if not os.path.exists(file_path):
                return False, f"No face found for {name}"

            # Delete the file
            os.remove(file_path)

            # Reload known faces
            self.load_known_faces()

            return True, f"Face deleted for {name}"

        except Exception as e:
            return False, f"Error deleting face: {str(e)}"

    def get_known_faces(self):
        """Get a list of all known faces"""
        return list(self.known_faces.keys())