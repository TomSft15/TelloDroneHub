import unittest
import os
import shutil
import tempfile
import cv2
import numpy as np
from unittest.mock import patch, MagicMock
from services.face_recognition_service import FaceRecognitionService

class TestFaceRecognitionService(unittest.TestCase):
    """Tests for the FaceRecognitionService class"""

    def setUp(self):
        """Set up test environment before each test"""
        # Create temporary directories for testing
        self.test_base_dir = tempfile.mkdtemp()
        self.test_known_faces_dir = os.path.join(self.test_base_dir, 'known_faces')
        self.test_model_data_dir = os.path.join(self.test_base_dir, 'model_data')

        os.makedirs(self.test_known_faces_dir, exist_ok=True)
        os.makedirs(self.test_model_data_dir, exist_ok=True)

        # Create a test image with a face
        self.test_face_img = np.zeros((300, 300, 3), dtype=np.uint8)
        # Draw a simple face-like shape
        cv2.circle(self.test_face_img, (150, 150), 100, (255, 255, 255), -1)  # Head
        cv2.circle(self.test_face_img, (120, 120), 15, (0, 0, 0), -1)  # Left eye
        cv2.circle(self.test_face_img, (180, 120), 15, (0, 0, 0), -1)  # Right eye
        cv2.ellipse(self.test_face_img, (150, 180), (50, 20), 0, 0, 180, (0, 0, 0), -1)  # Mouth

        # Convert to binary for add_face input
        _, self.test_face_data = cv2.imencode('.jpg', self.test_face_img)
        self.test_face_data = self.test_face_data.tobytes()

        # Patch face cascade for detection
        self.patcher = patch('cv2.CascadeClassifier')
        self.mock_cascade = self.patcher.start()
        self.mock_cascade.return_value.detectMultiScale.return_value = [(50, 50, 200, 200)]  # Mock detected face

        # Patch recognizer
        self.recognizer_patcher = patch('cv2.face.LBPHFaceRecognizer_create')
        self.mock_recognizer = self.recognizer_patcher.start()
        self.mock_recognizer.return_value.predict.return_value = (0, 50)  # Mock prediction (id, confidence)

        # Initialize service with test directories
        with patch.object(FaceRecognitionService, '__new__', lambda cls: object.__new__(cls)):
            self.service = FaceRecognitionService()
            self.service._initialized = True
            self.service.known_faces_dir = self.test_known_faces_dir
            self.service.model_data_dir = self.test_model_data_dir
            self.service.face_cascade = self.mock_cascade.return_value
            self.service.recognizer = self.mock_recognizer.return_value
            self.service.known_names = {0: 'Test Person'}
            self.service.drone_service = MagicMock()
            self.service.video_service = MagicMock()
            self.service.recognition_thread = None

    def tearDown(self):
        """Clean up after each test"""
        # Remove test directories
        shutil.rmtree(self.test_base_dir)

        # Stop patchers
        self.patcher.stop()
        self.recognizer_patcher.stop()

    def test_add_face_success(self):
        """Test adding a face with valid image and name"""
        # Arrange
        person_name = "Test Person"

        # Act
        success, message = self.service.add_face(self.test_face_data, person_name)

        # Assert
        self.assertTrue(success)
        self.assertIn("added successfully", message)
        # Check if file was created
        files = os.listdir(self.test_known_faces_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].startswith(person_name))

    def test_add_face_no_face_detected(self):
        """Test adding an image with no face"""
        # Arrange
        # Override the mock to return no faces
        self.mock_cascade.return_value.detectMultiScale.return_value = []

        # Act
        success, message = self.service.add_face(self.test_face_data, "Test Person")

        # Assert
        self.assertFalse(success)
        self.assertIn("No face detected", message)
        # Check no file was created
        files = os.listdir(self.test_known_faces_dir)
        self.assertEqual(len(files), 0)

    def test_add_face_invalid_name(self):
        """Test adding a face with invalid name"""
        # Act
        success, message = self.service.add_face(self.test_face_data, "")

        # Assert
        self.assertFalse(success)
        self.assertIn("Invalid person name", message)

    def test_start_recognition_success(self):
        """Test starting recognition with proper setup"""
        # Arrange
        self.service.drone_service.connected = True
        self.service.drone_service.drone = MagicMock()

        # Act
        with patch.object(self.service, 'load_known_faces', return_value=True):
            success, message = self.service.start_recognition()

        # Assert
        self.assertTrue(success)
        self.assertIn("started", message)
        self.assertTrue(self.service.is_running)
        # Clean up
        self.service.stop_recognition()

    def test_start_recognition_drone_not_connected(self):
        """Test starting recognition without drone connection"""
        # Arrange
        self.service.drone_service.connected = False

        # Act
        success, message = self.service.start_recognition()

        # Assert
        self.assertFalse(success)
        self.assertIn("not connected", message)
        self.assertFalse(self.service.is_running)

    def test_start_recognition_no_known_faces(self):
        """Test starting recognition without known faces"""
        # Arrange
        self.service.drone_service.connected = True
        self.service.drone_service.drone = MagicMock()

        # Act
        with patch.object(self.service, 'load_known_faces', return_value=False):
            success, message = self.service.start_recognition()

        # Assert
        self.assertFalse(success)
        self.assertIn("No known faces", message)
        self.assertFalse(self.service.is_running)

    def test_stop_recognition(self):
        """Test stopping recognition"""
        # Arrange - start recognition first
        self.service.drone_service.connected = True
        self.service.drone_service.drone = MagicMock()
        with patch.object(self.service, 'load_known_faces', return_value=True):
            self.service.start_recognition()

        # Act
        success, message = self.service.stop_recognition()

        # Assert
        self.assertTrue(success)
        self.assertIn("stopped", message)
        self.assertFalse(self.service.is_running)

    def test_recognition_loop_behavior(self):
        """Test the recognition loop behavior"""
        # Arrange
        self.service.drone_service.connected = True
        self.service.drone_service.drone = MagicMock()
        self.service.video_service.frame = np.zeros((100, 100, 3), dtype=np.uint8)

        # Mock the stop event to let the loop run briefly
        self.service.stop_event = MagicMock()
        self.service.stop_event.is_set.side_effect = [False, False, True]  # Run loop 2 times then stop

        # Act
        self.service._recognition_loop()

        # Assert
        # Check that face detection was called
        self.mock_cascade.return_value.detectMultiScale.assert_called()
        # Check that prediction was called if a face was detected
        self.mock_recognizer.return_value.predict.assert_called()
        # Check faces were added to recognized_faces
        self.assertEqual(len(self.service.recognized_faces), 1)

    def test_get_recognized_faces(self):
        """Test getting recognized faces"""
        # Arrange
        test_faces = [{"name": "Test Person", "confidence": 0.5}]
        self.service.recognized_faces = test_faces

        # Act
        result = self.service.get_recognized_faces()

        # Assert
        self.assertEqual(result, test_faces)

if __name__ == '__main__':
    unittest.main()