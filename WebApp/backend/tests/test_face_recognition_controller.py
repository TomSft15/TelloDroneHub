import unittest
import json
import base64
import io
import os
import cv2
import numpy as np
from unittest.mock import patch, MagicMock
from flask import Flask
from controllers.face_recognition_controller import face_recognition_ns

class TestFaceRecognitionController(unittest.TestCase):
    """Tests for the FaceRecognitionController endpoints"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a Flask app
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        
        # Register the namespace
        face_recognition_ns.init_app(self.app)
        
        # Create a test client
        self.client = self.app.test_client()
        
        # Create a sample image for testing
        self.test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.rectangle(self.test_img, (30, 30), (70, 70), (255, 255, 255), -1)  # Simple shape
        
        # Convert to binary for file upload
        _, img_encoded = cv2.imencode('.jpg', self.test_img)
        self.test_img_bytes = img_encoded.tobytes()
        
        # Mock the FaceRecognitionService
        self.service_patcher = patch('controllers.face_recognition_controller.FaceRecognitionService')
        self.mock_service = self.service_patcher.start()
        self.mock_service.return_value.start_recognition.return_value = (True, "Recognition started")
        self.mock_service.return_value.stop_recognition.return_value = (True, "Recognition stopped")
        self.mock_service.return_value.add_face.return_value = (True, "Face added successfully")
        self.mock_service.return_value.get_recognized_faces.return_value = [
            {
                "name": "Test Person",
                "confidence": 0.85,
                "location": {"top": 10, "right": 60, "bottom": 70, "left": 20},
                "timestamp": 1616161616.123
            }
        ]
        self.mock_service.return_value.load_known_faces.return_value = True
    
    def tearDown(self):
        """Clean up after each test"""
        self.service_patcher.stop()
    
    def test_start_recognition_endpoint(self):
        """Test the start recognition endpoint"""
        # Act
        response = self.client.get('/face_recognition/start')
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Recognition started")
        self.mock_service.return_value.start_recognition.assert_called_once()
    
    def test_stop_recognition_endpoint(self):
        """Test the stop recognition endpoint"""
        # Act
        response = self.client.get('/face_recognition/stop')
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Recognition stopped")
        self.mock_service.return_value.stop_recognition.assert_called_once()
    
    def test_add_face_endpoint(self):
        """Test the add_face endpoint with file upload"""
        # Arrange
        test_data = {
            'name': 'Test Person',
        }
        test_files = {
            'file': (io.BytesIO(self.test_img_bytes), 'test.jpg')
        }
        
        # Act
        response = self.client.post(
            '/face_recognition/add_face',
            data=test_data,
            content_type='multipart/form-data',
            buffered=True,
            files=test_files
        )
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Face added successfully")
        self.mock_service.return_value.add_face.assert_called_once()
    
    def test_add_face_base64_endpoint(self):
        """Test the add_face_base64 endpoint"""
        # Arrange
        base64_img = base64.b64encode(self.test_img_bytes).decode('utf-8')
        test_data = {
            'image_data': base64_img,
            'name': 'Test Person'
        }
        
        # Act
        response = self.client.post(
            '/face_recognition/add_face_base64',
            json=test_data,
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Face added successfully")
        self.mock_service.return_value.add_face.assert_called_once()
    
    def test_add_face_base64_endpoint_with_data_uri(self):
        """Test the add_face_base64 endpoint with data URI format"""
        # Arrange
        base64_img = base64.b64encode(self.test_img_bytes).decode('utf-8')
        data_uri = f"data:image/jpeg;base64,{base64_img}"
        test_data = {
            'image_data': data_uri,
            'name': 'Test Person'
        }
        
        # Act
        response = self.client.post(
            '/face_recognition/add_face_base64',
            json=test_data,
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Face added successfully")
        self.mock_service.return_value.add_face.assert_called_once()
    
    def test_present_endpoint(self):
        """Test the present endpoint to get recognized faces"""
        # Act
        response = self.client.get('/face_recognition/present')
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['faces']), 1)
        self.assertEqual(data['faces'][0]['name'], "Test Person")
        self.assertAlmostEqual(data['faces'][0]['confidence'], 0.85)
        self.mock_service.return_value.get_recognized_faces.assert_called_once()
    
    def test_reload_endpoint(self):
        """Test the reload endpoint to reload known faces"""
        # Act
        response = self.client.get('/face_recognition/reload')
        data = json.loads(response.data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Known faces reloaded successfully")
        self.mock_service.return_value.load_known_faces.assert_called_once()
    
    def test_add_face_missing_file(self):
        """Test the add_face endpoint with missing file"""
        # Arrange
        test_data = {
            'name': 'Test Person'
        }
        
        # Act
        response = self.client.post(
            '/face_recognition/add_face',
            data=test_data,
            content_type='multipart/form-data'
        )
        
        # Assert
        self.assertEqual(response.status_code, 400)
    
    def test_add_face_base64_missing_data(self):
        """Test the add_face_base64 endpoint with missing data"""
        # Arrange
        test_data = {
            'name': 'Test Person'
            # Missing image_data
        }
        
        # Act
        response = self.client.post(
            '/face_recognition/add_face_base64',
            json=test_data,
            content_type='application/json'
        )
        
        # Assert
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()