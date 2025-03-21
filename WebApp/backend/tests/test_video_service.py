import unittest
import cv2
import numpy as np
from unittest.mock import patch, MagicMock
from services.video_service import VideoService
from services.drone_service import DroneService

class TestVideoService(unittest.TestCase):
    """Tests for the VideoService class"""

    def setUp(self):
        """Set up test environment before each test"""
        # Reset singleton instances
        VideoService._instance = None
        DroneService._instance = None

        # Create mock for DroneService
        self.drone_service_patcher = patch('services.video_service.DroneService')
        self.mock_drone_service_class = self.drone_service_patcher.start()
        self.mock_drone_service = MagicMock()
        self.mock_drone_service_class.return_value = self.mock_drone_service

        # Setup mock drone
        self.mock_drone = MagicMock()
        self.mock_drone_service.drone = self.mock_drone
        self.mock_drone_service.connected = True

        # Initialize service
        self.service = VideoService()

    def tearDown(self):
        """Clean up after each test"""
        self.drone_service_patcher.stop()

    def test_start_video_stream_success(self):
        """Test successful video stream start"""
        # Act
        success, message = self.service.start_video_stream()

        # Assert
        self.assertTrue(success)
        self.assertTrue("démarré" in message.lower() or "started" in message.lower())
        self.assertTrue(self.service._streaming)
        self.mock_drone.streamon.assert_called_once()
        self.assertIsNotNone(self.service._video_thread)

    def test_start_video_stream_already_streaming(self):
        """Test starting video stream when already streaming"""
        # Arrange
        self.service._streaming = True

        # Act
        success, message = self.service.start_video_stream()

        # Assert
        self.assertTrue(success)
        self.assertTrue("déjà actif" in message.lower() or "already active" in message.lower())
        self.mock_drone.streamon.assert_not_called()

    def test_start_video_stream_drone_not_connected(self):
        """Test starting video stream when drone is not connected"""
        # Arrange
        self.mock_drone_service.connected = False

        # Act
        success, message = self.service.start_video_stream()

        # Assert
        self.assertFalse(success)
        self.assertTrue("non connecté" in message.lower() or "not connected" in message.lower())
        self.assertFalse(self.service._streaming)

    def test_start_video_stream_exception(self):
        """Test starting video stream with exception"""
        # Arrange
        self.mock_drone.streamon.side_effect = Exception("Test error")

        # Act
        success, message = self.service.start_video_stream()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())
        self.assertFalse(self.service._streaming)

    def test_stop_video_stream_success(self):
        """Test successful video stream stop"""
        # Arrange
        self.service._streaming = True

        # Act
        success, message = self.service.stop_video_stream()

        # Assert
        self.assertTrue(success)
        self.assertTrue("arrêté" in message.lower() or "stopped" in message.lower())
        self.assertFalse(self.service._streaming)
        self.mock_drone.streamoff.assert_called_once()

    def test_stop_video_stream_already_stopped(self):
        """Test stopping video stream when already stopped"""
        # Arrange
        self.service._streaming = False

        # Act
        success, message = self.service.stop_video_stream()

        # Assert
        self.assertTrue(success)
        self.assertTrue("déjà arrêté" in message.lower() or "already stopped" in message.lower())
        self.mock_drone.streamoff.assert_not_called()

    def test_stop_video_stream_exception(self):
        """Test stopping video stream with exception"""
        # Arrange
        self.service._streaming = True
        self.mock_drone.streamoff.side_effect = Exception("Test error")

        # Act
        success, message = self.service.stop_video_stream()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())
        self.assertFalse(self.service._streaming)

    def test_capture_video_frame_available(self):
        """Test capturing video with frame available"""
        # Arrange
        # Create a test frame
        test_frame = np.zeros((100, 100, 3), dtype=np.uint8)

        # Mock get_frame_read to return a frame
        mock_frame_read = MagicMock()
        mock_frame_read.frame = test_frame
        self.mock_drone.get_frame_read.return_value = mock_frame_read

        # Create a threadsafe mock to capture frame updates
        self.service._streaming = True
        self.service.frame = None

        # Act
        # Simulate a single iteration of the capture loop
        with patch('services.video_service.time.sleep', return_value=None):
            self.service._capture_video()

        # Assert
        self.assertIsNotNone(self.service.frame)
        self.assertEqual(self.service.frame.shape[:2], (test_frame.shape[0], test_frame.shape[1]))
        self.mock_drone.get_frame_read.assert_called_once()

    def test_capture_video_exception(self):
        """Test capturing video with exception"""
        # Arrange
        self.mock_drone.get_frame_read.side_effect = Exception("Test error")
        self.service._streaming = True

        # Act
        # Use a try/except to prevent test from hanging
        try:
            with patch('services.video_service.time.sleep', return_value=None):
                with patch('services.video_service.print', return_value=None):  # Suppress print
                    self.service._capture_video()
        except:
            pass

        # Assert
        self.mock_drone.get_frame_read.assert_called()

    def test_generate_frames_no_frame(self):
        """Test generating frames when no frame is available"""
        # Arrange
        self.service.frame = None

        # Act
        generator = self.service.generate_frames()
        frame_data = next(generator)

        # Assert
        self.assertTrue(frame_data.startswith(b'--frame\r\n'))
        self.assertTrue(b'Content-Type: image/jpeg' in frame_data)

    def test_generate_frames_with_frame(self):
        """Test generating frames when a frame is available"""
        # Arrange
        test_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.service.frame = test_frame

        # Act
        generator = self.service.generate_frames()
        with patch('cv2.imencode', return_value=(True, b'test_encoded_image')):
            frame_data = next(generator)

        # Assert
        self.assertTrue(frame_data.startswith(b'--frame\r\n'))
        self.assertTrue(b'Content-Type: image/jpeg' in frame_data)
        self.assertTrue(b'test_encoded_image' in frame_data)

    def test_create_no_signal_frame(self):
        """Test creating a 'no signal' frame"""
        # Act
        frame = self.service._create_no_signal_frame()

        # Assert
        self.assertIsNotNone(frame)
        self.assertEqual(frame.shape[2], 3)  # Should be a color image
        # Check that the image is mostly black (no signal)
        self.assertTrue(np.mean(frame) < 50)  # Average pixel value should be low

    def test_singleton_pattern(self):
        """Test that VideoService follows singleton pattern"""
        # Act
        service1 = VideoService()
        service2 = VideoService()

        # Assert
        self.assertIs(service1, service2)
        self.assertIs(service1, self.service)

if __name__ == '__main__':
    unittest.main()

