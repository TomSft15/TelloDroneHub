import unittest
import numpy as np
from unittest.mock import patch, MagicMock, call
from services.face_tracking_service import FaceTrackingService

class TestFaceTrackingService(unittest.TestCase):
    """Tests for the FaceTrackingService class"""

    def setUp(self):
        """Set up test environment before each test"""
        # Reset singleton instance
        FaceTrackingService._instance = None

        # Create mock for cv2.CascadeClassifier
        self.cascade_patcher = patch('cv2.CascadeClassifier')
        self.mock_cascade_class = self.cascade_patcher.start()
        self.mock_cascade = MagicMock()
        self.mock_cascade_class.return_value = self.mock_cascade
        self.mock_cascade.empty.return_value = False  # Classifier loaded successfully

        # Create mock for cv2.data
        self.cv2_data_patcher = patch('cv2.data')
        self.mock_cv2_data = self.cv2_data_patcher.start()
        self.mock_cv2_data.haarcascades = "/mock/path/to/haarcascades/"

        # Create mock for threading.Thread
        self.thread_patcher = patch('services.face_tracking_service.threading.Thread')
        self.mock_thread = self.thread_patcher.start()

        # Initialize service
        self.service = FaceTrackingService()

        # Mock DroneService
        self.mock_drone_service = MagicMock()
        self.mock_drone = MagicMock()
        self.mock_drone_service.drone = self.mock_drone
        self.mock_drone_service.connected = True

        # Initialize the service with drone service
        self.service.init_drone_service(self.mock_drone_service)

    def tearDown(self):
        """Clean up after each test"""
        self.cascade_patcher.stop()
        self.cv2_data_patcher.stop()
        self.thread_patcher.stop()

    def test_init_loads_classifier(self):
        """Test that initialization loads face classifier"""
        # Assert
        self.mock_cascade_class.assert_called_once()
        self.assertEqual(self.service.face_cascade, self.mock_cascade)

    def test_init_fails_if_classifier_empty(self):
        """Test initialization handling when classifier fails to load"""
        # Arrange
        self.cascade_patcher.stop()

        # Setup for failed classifier load
        with patch('cv2.CascadeClassifier') as mock_cascade_class:
            mock_cascade = MagicMock()
            mock_cascade_class.return_value = mock_cascade
            mock_cascade.empty.return_value = True  # Classifier failed to load

            # Act - initialize service
            with patch('services.face_tracking_service.logger.error') as mock_logger:
                service = FaceTrackingService()

            # Assert
            mock_logger.assert_called_once()
            self.assertIsNone(service.face_cascade)

        # Restart patcher for other tests
        self.cascade_patcher = patch('cv2.CascadeClassifier')
        self.mock_cascade_class = self.cascade_patcher.start()

    def test_init_drone_service(self):
        """Test initialization with drone service"""
        # Arrange
        mock_drone_service = MagicMock()

        # Act
        self.service.init_drone_service(mock_drone_service)

        # Assert
        self.assertEqual(self.service.drone_service, mock_drone_service)

    def test_start_face_tracking_success(self):
        """Test successful start of face tracking"""
        # Act
        success, message = self.service.start_face_tracking()

        # Assert
        self.assertTrue(success)
        self.assertTrue("démarré" in message.lower() or "started" in message.lower())
        self.assertTrue(self.service.is_tracking)
        self.mock_thread.assert_called_once()
        self.mock_thread.return_value.start.assert_called_once()

    def test_start_face_tracking_already_tracking(self):
        """Test starting face tracking when already tracking"""
        # Arrange
        self.service.is_tracking = True

        # Act
        success, message = self.service.start_face_tracking()

        # Assert
        self.assertTrue(success)
        self.assertTrue("déjà actif" in message.lower() or "already active" in message.lower())
        self.mock_thread.assert_not_called()

    def test_start_face_tracking_no_classifier(self):
        """Test starting face tracking without classifier"""
        # Arrange
        self.service.face_cascade = None

        # Act
        success, message = self.service.start_face_tracking()

        # Assert
        self.assertFalse(success)
        self.assertTrue("classificateur" in message.lower() or "classifier" in message.lower())
        self.assertFalse(self.service.is_tracking)

    def test_start_face_tracking_no_drone(self):
        """Test starting face tracking without drone connected"""
        # Arrange
        self.service.drone_service.connected = False

        # Act
        success, message = self.service.start_face_tracking()

        # Assert
        self.assertFalse(success)
        self.assertTrue("non connecté" in message.lower() or "not connected" in message.lower())
        self.assertFalse(self.service.is_tracking)

    def test_start_face_tracking_exception(self):
        """Test starting face tracking with exception"""
        # Arrange
        self.mock_thread.side_effect = Exception("Test error")

        # Act
        success, message = self.service.start_face_tracking()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())
        self.assertFalse(self.service.is_tracking)

    def test_stop_face_tracking_success(self):
        """Test successful stop of face tracking"""
        # Arrange
        self.service.is_tracking = True
        self.service.tracking_thread = MagicMock()
        self.service.tracking_thread.is_alive.return_value = True

        # Act
        success, message = self.service.stop_face_tracking()

        # Assert
        self.assertTrue(success)
        self.assertTrue("arrêté" in message.lower() or "stopped" in message.lower())
        self.assertFalse(self.service.is_tracking)
        self.service.stop_event.set.assert_called_once()
        self.service.tracking_thread.join.assert_called_once()
        self.mock_drone.send_rc_control.assert_called_once_with(0, 0, 0, 0)

    def test_stop_face_tracking_already_stopped(self):
        """Test stopping face tracking when already stopped"""
        # Arrange
        self.service.is_tracking = False

        # Act
        success, message = self.service.stop_face_tracking()

        # Assert
        self.assertTrue(success)
        self.assertTrue("déjà arrêté" in message.lower() or "already stopped" in message.lower())

    def test_stop_face_tracking_exception(self):
        """Test stopping face tracking with exception"""
        # Arrange
        self.service.is_tracking = True
        self.service.stop_event.set.side_effect = Exception("Test error")

        # Act
        success, message = self.service.stop_face_tracking()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())

    def test_update_settings_valid(self):
        """Test updating tracking settings with valid values"""
        # Arrange
        new_settings = {
            'detection_frequency': 0.5,
            'rotation_speed': 30,
            'deadzone_x': 60
        }
        original_settings = self.service.tracking_settings.copy()

        # Act
        success, message = self.service.update_settings(new_settings)

        # Assert
        self.assertTrue(success)
        self.assertEqual(self.service.tracking_settings['detection_frequency'], 0.5)
        self.assertEqual(self.service.tracking_settings['rotation_speed'], 30)
        self.assertEqual(self.service.tracking_settings['deadzone_x'], 60)
        # Other settings should be unchanged
        self.assertEqual(self.service.tracking_settings['deadzone_y'], original_settings['deadzone_y'])

    def test_update_settings_invalid_type(self):
        """Test updating tracking settings with invalid type"""
        # Arrange
        new_settings = {
            'detection_frequency': "not a number",
            'rotation_speed': 30
        }
        original_settings = self.service.tracking_settings.copy()

        # Act
        success, message = self.service.update_settings(new_settings)

        # Assert
        self.assertTrue(success)  # Should still return success
        # Invalid type should be ignored
        self.assertEqual(self.service.tracking_settings['detection_frequency'], 
                        original_settings['detection_frequency'])
        # Valid setting should be updated
        self.assertEqual(self.service.tracking_settings['rotation_speed'], 30)

    def test_update_settings_unknown_setting(self):
        """Test updating tracking settings with unknown setting"""
        # Arrange
        new_settings = {
            'unknown_setting': 100,
            'rotation_speed': 30
        }

        # Act
        success, message = self.service.update_settings(new_settings)

        # Assert
        self.assertTrue(success)
        # Unknown setting should be ignored
        self.assertNotIn('unknown_setting', self.service.tracking_settings)
        # Valid setting should be updated
        self.assertEqual(self.service.tracking_settings['rotation_speed'], 30)

    def test_get_status(self):
        """Test getting face tracking status"""
        # Arrange
        self.service.is_tracking = True
        expected_keys = ['is_tracking', 'settings', 'face_detected']

        # Act
        status = self.service.get_status()

        # Assert
        self.assertTrue(status['is_tracking'])
        for key in expected_keys:
            self.assertIn(key, status)
        self.assertEqual(status['settings'], self.service.tracking_settings)

    def test_tracking_loop_with_face(self):
        """Test tracking loop when face is detected"""
        # Arrange
        # Mock frame and face detection
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.mock_drone.get_frame_read.return_value.frame = test_frame

        # Mock face detection
        self.mock_cascade.detectMultiScale.return_value = [(100, 100, 200, 200)]  # (x, y, w, h)

        # Setup tracking loop to run only once
        self.service.stop_event = MagicMock()
        self.service.stop_event.is_set.side_effect = [False, True]  # Stop after first iteration

        # Act
        with patch('services.face_tracking_service.time.time', return_value=1000):
            self.service._tracking_loop()

        # Assert
        self.mock_cascade.detectMultiScale.assert_called_once()
        self.mock_drone.send_rc_control.assert_called()  # Should have sent control commands

    def test_tracking_loop_no_face(self):
        """Test tracking loop when no face is detected"""
        # Arrange
        # Mock frame and face detection
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.mock_drone.get_frame_read.return_value.frame = test_frame

        # Mock no face detection
        self.mock_cascade.detectMultiScale.return_value = []

        # Setup tracking loop to run only once
        self.service.stop_event = MagicMock()
        self.service.stop_event.is_set.side_effect = [False, True]  # Stop after first iteration

        # Act
        with patch('services.face_tracking_service.time.time', return_value=1000):
            self.service._tracking_loop()

        # Assert
        self.mock_cascade.detectMultiScale.assert_called_once()
        # Should still send control commands (to stop movement)
        self.mock_drone.send_rc_control.assert_called_with(0, 0, 0, 0)

    def test_tracking_loop_exception(self):
        """Test tracking loop handling an exception"""
        # Arrange
        self.mock_drone.get_frame_read.side_effect = Exception("Test error")

        # Setup tracking loop to run only once
        self.service.stop_event = MagicMock()
        self.service.stop_event.is_set.side_effect = [False, True]  # Stop after first iteration

        # Act
        with patch('services.face_tracking_service.logger.error') as mock_logger:
            with patch('services.face_tracking_service.time.time', return_value=1000):
                self.service._tracking_loop()

        # Assert
        mock_logger.assert_called_once()
        self.assertFalse(self.service.is_tracking)  # Should have stopped tracking

    def test_tracking_face_center_position(self):
        """Test tracking when face is in center (deadzone)"""
        # Arrange
        # Mock frame and face detection
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.mock_drone.get_frame_read.return_value.frame = test_frame

        # Face is in the center of frame (320, 240) with size 100x100
        self.mock_cascade.detectMultiScale.return_value = [(270, 190, 100, 100)]

        # Set deadzones
        self.service.tracking_settings['deadzone_x'] = 50
        self.service.tracking_settings['deadzone_y'] = 50

        # Setup tracking loop to run only once
        self.service.stop_event = MagicMock()
        self.service.stop_event.is_set.side_effect = [False, True]

        # Act
        with patch('services.face_tracking_service.time.time', return_value=1000):
            self.service._tracking_loop()

        # Assert
        # Should send no movement command (face is in deadzone)
        self.mock_drone.send_rc_control.assert_called_with(0, 0, 0, 0)

    def test_tracking_face_right_position(self):
        """Test tracking when face is to the right of center"""
        # Arrange
        # Mock frame and face detection
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.mock_drone.get_frame_read.return_value.frame = test_frame

        # Face is to the right of center
        self.mock_cascade.detectMultiScale.return_value = [(450, 240, 100, 100)]

        # Set deadzones and speeds
        self.service.tracking_settings['deadzone_x'] = 50
        self.service.tracking_settings['rotation_speed'] = 30

        # Setup tracking loop to run only once
        self.service.stop_event = MagicMock()
        self.service.stop_event.is_set.side_effect = [False, True]

        # Act
        with patch('services.face_tracking_service.time.time', return_value=1000):
            self.service._tracking_loop()

        # Assert
        # Should have positive yaw (rotate right)
        self.mock_drone.send_rc_control.assert_called_with(0, 0, 0, 30)

    def test_tracking_face_above_position(self):
        """Test tracking when face is above center"""
        # Arrange
        # Mock frame and face detection
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.mock_drone.get_frame_read.return_value.frame = test_frame

        # Face is above center
        self.mock_cascade.detectMultiScale.return_value = [(320, 100, 100, 100)]

        # Set deadzones and speeds
        self.service.tracking_settings['deadzone_y'] = 50
        self.service.tracking_settings['vertical_speed'] = 30

        # Setup tracking loop to run only once
        self.service.stop_event = MagicMock()
        self.service.stop_event.is_set.side_effect = [False, True]

        # Act
        with patch('services.face_tracking_service.time.time', return_value=1000):
            self.service._tracking_loop()

        # Assert
        # Should have positive vertical speed (move up)
        self.mock_drone.send_rc_control.assert_called_with(0, 0, 30, 0)

    def test_singleton_pattern(self):
        """Test that FaceTrackingService follows singleton pattern"""
        # Act
        service1 = FaceTrackingService()
        service2 = FaceTrackingService()

        # Assert
        self.assertIs(service1, service2)
        self.assertIs(service1, self.service)

if __name__ == '__main__':
    unittest.main()