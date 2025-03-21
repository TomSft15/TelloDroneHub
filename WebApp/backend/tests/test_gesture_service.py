import unittest
import numpy as np
from unittest.mock import patch, MagicMock, call
from services.gesture_service import GestureService
from services.drone_service import DroneService

class TestGestureService(unittest.TestCase):
    """Tests for the GestureService class"""

    def setUp(self):
        """Set up test environment before each test"""
        # Reset singleton instances
        GestureService._instance = None
        DroneService._instance = None

        # Create mock for DroneService
        self.drone_service_patcher = patch('services.gesture_service.DroneService')
        self.mock_drone_service_class = self.drone_service_patcher.start()
        self.mock_drone_service = MagicMock()
        self.mock_drone_service_class.return_value = self.mock_drone_service

        # Mock MediaPipe
        self.mp_hands_patcher = patch('services.gesture_service.mp.solutions.hands')
        self.mock_mp_hands = self.mp_hands_patcher.start()

        self.mp_drawing_patcher = patch('services.gesture_service.mp.solutions.drawing_utils')
        self.mock_mp_drawing = self.mp_drawing_patcher.start()

        # Setup mock drone and connection status
        self.mock_drone = MagicMock()
        self.mock_drone_service.drone = self.mock_drone
        self.mock_drone_service.connected = True

        # Initialize service
        self.service = GestureService()

        # Patch threading to avoid running actual threads
        self.thread_patcher = patch('services.gesture_service.threading.Thread')
        self.mock_thread = self.thread_patcher.start()

    def tearDown(self):
        """Clean up after each test"""
        self.drone_service_patcher.stop()
        self.mp_hands_patcher.stop()
        self.mp_drawing_patcher.stop()
        self.thread_patcher.stop()

    def test_start_gesture_detection_success(self):
        """Test successful start of gesture detection"""
        # Act
        success, message = self.service.start_gesture_detection()

        # Assert
        self.assertTrue(success)
        self.assertTrue("démarrée" in message.lower() or "started" in message.lower())
        self.assertTrue(self.service.is_running)
        self.mock_thread.assert_called_once()
        self.mock_thread.return_value.start.assert_called_once()

    def test_start_gesture_detection_already_running(self):
        """Test starting gesture detection when already running"""
        # Arrange
        self.service.is_running = True

        # Act
        success, message = self.service.start_gesture_detection()

        # Assert
        self.assertTrue(success)
        self.assertTrue("déjà active" in message.lower() or "already active" in message.lower())
        self.mock_thread.assert_not_called()

    def test_start_gesture_detection_drone_not_connected(self):
        """Test starting gesture detection when drone is not connected"""
        # Arrange
        self.mock_drone_service.connected = False

        # Act
        success, message = self.service.start_gesture_detection()

        # Assert
        self.assertFalse(success)
        self.assertTrue("non connecté" in message.lower() or "not connected" in message.lower())
        self.assertFalse(self.service.is_running)

    def test_start_gesture_detection_exception(self):
        """Test starting gesture detection with exception"""
        # Arrange
        self.mock_thread.side_effect = Exception("Test error")

        # Act
        success, message = self.service.start_gesture_detection()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())
        self.assertFalse(self.service.is_running)

    def test_stop_gesture_detection_success(self):
        """Test successful stop of gesture detection"""
        # Arrange
        self.service.is_running = True

        # Act
        success, message = self.service.stop_gesture_detection()

        # Assert
        self.assertTrue(success)
        self.assertTrue("arrêtée" in message.lower() or "stopped" in message.lower())
        self.assertFalse(self.service.is_running)

    def test_stop_gesture_detection_already_stopped(self):
        """Test stopping gesture detection when already stopped"""
        # Arrange
        self.service.is_running = False

        # Act
        success, message = self.service.stop_gesture_detection()

        # Assert
        self.assertTrue(success)
        self.assertTrue("déjà arrêtée" in message.lower() or "already stopped" in message.lower())

    def test_stop_gesture_detection_exception(self):
        """Test stopping gesture detection with exception"""
        # Arrange
        self.service.is_running = True
        # Mock exception in stop logic
        with patch('builtins.print', side_effect=Exception("Test error")):
            # Act
            success, message = self.service.stop_gesture_detection()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())

    def test_count_fingers_up_left_hand(self):
        """Test counting fingers up for left hand"""
        # Arrange
        # Create mock hand positions
        # Format: [id, x, y] for each landmark
        # Simulate hand with thumb, index and middle fingers up (others down)
        hand_position = [
            [0, 50, 100],  # Wrist
            # Thumb
            [1, 40, 90], [2, 30, 80], [3, 20, 70], [4, 10, 80],  # Thumb tip x > base x for left hand
            # Index finger
            [5, 60, 90], [6, 60, 80], [7, 60, 70], [8, 60, 50],  # Tip y < base y (up)
            # Middle finger
            [9, 70, 90], [10, 70, 80], [11, 70, 70], [12, 70, 50],  # Tip y < base y (up)
            # Ring finger
            [13, 80, 90], [14, 80, 80], [15, 80, 70], [16, 80, 90],  # Tip y > base y (down)
            # Pinky
            [17, 90, 90], [18, 90, 80], [19, 90, 70], [20, 90, 90]   # Tip y > base y (down)
        ]

        # Act
        fingers, count = self.service._count_fingers_up(hand_position, "Left")

        # Assert
        self.assertEqual(fingers, [1, 1, 1, 0, 0])  # [thumb, index, middle, ring, pinky]
        self.assertEqual(count, 3)  # 3 fingers up

    def test_count_fingers_up_right_hand(self):
        """Test counting fingers up for right hand"""
        # Arrange
        # Create mock hand positions for right hand
        # Simulate hand with index, middle and ring fingers up (thumb and pinky down)
        hand_position = [
            [0, 50, 100],  # Wrist
            # Thumb
            [1, 40, 90], [2, 30, 80], [3, 20, 70], [4, 30, 80],  # Thumb tip x > base x (down for right hand)
            # Index finger
            [5, 60, 90], [6, 60, 80], [7, 60, 70], [8, 60, 50],  # Tip y < base y (up)
            # Middle finger
            [9, 70, 90], [10, 70, 80], [11, 70, 70], [12, 70, 50],  # Tip y < base y (up)
            # Ring finger
            [13, 80, 90], [14, 80, 80], [15, 80, 70], [16, 80, 50],  # Tip y < base y (up)
            # Pinky
            [17, 90, 90], [18, 90, 80], [19, 90, 70], [20, 90, 90]   # Tip y > base y (down)
        ]

        # Act
        fingers, count = self.service._count_fingers_up(hand_position, "Right")

        # Assert
        self.assertEqual(fingers, [0, 1, 1, 1, 0])  # [thumb, index, middle, ring, pinky]
        self.assertEqual(count, 3)  # 3 fingers up

    def test_handle_sign_open_hand(self):
        """Test handle sign with open hand (takeoff)"""
        # Arrange
        # All fingers up
        fingers = [1, 1, 1, 1, 1]
        hand_position = [[i, 10*i, 10*i] for i in range(21)]  # Dummy positions

        # Act
        result = self.service._handle_sign(fingers, hand_position)

        # Assert
        self.assertEqual(result, "takeoff")

    def test_handle_sign_closed_fist(self):
        """Test handle sign with closed fist (land)"""
        # Arrange
        # All fingers down
        fingers = [0, 0, 0, 0, 0]
        hand_position = [[i, 10*i, 10*i] for i in range(21)]  # Dummy positions

        # Act
        result = self.service._handle_sign(fingers, hand_position)

        # Assert
        self.assertEqual(result, "land")

    def test_handle_sign_index_only(self):
        """Test handle sign with only index finger (flip_left)"""
        # Arrange
        # Only index finger up
        fingers = [0, 1, 0, 0, 0]
        hand_position = [[i, 10*i, 10*i] for i in range(21)]  # Dummy positions

        # Act
        result = self.service._handle_sign(fingers, hand_position)

        # Assert
        self.assertEqual(result, "flip_left")

    def test_handle_sign_index_middle(self):
        """Test handle sign with index and middle fingers (flip_right)"""
        # Arrange
        # Index and middle fingers up
        fingers = [0, 1, 1, 0, 0]
        hand_position = [[i, 10*i, 10*i] for i in range(21)]  # Dummy positions

        # Act
        result = self.service._handle_sign(fingers, hand_position)

        # Assert
        self.assertEqual(result, "flip_right")

    def test_handle_sign_thumb_highest(self):
        """Test handle sign with thumb at highest position (monte)"""
        # Arrange
        fingers = [1, 0, 0, 0, 0]  # Only thumb up
        # Create a hand position where thumb tip (index 4) is higher (lower y) than any other point
        hand_position = [[i, 10*i, 100] for i in range(21)]  # All points at y=100
        hand_position[4][2] = 10  # Thumb tip at y=10 (highest point)

        # Act
        result = self.service._handle_sign(fingers, hand_position)

        # Assert
        self.assertEqual(result, "monte")

    def test_handle_sign_thumb_lowest(self):
        """Test handle sign with thumb at lowest position (descend)"""
        # Arrange
        fingers = [1, 0, 0, 0, 0]  # Only thumb up
        # Create a hand position where thumb tip (index 4) is lower (higher y) than any other point
        hand_position = [[i, 10*i, 100] for i in range(21)]  # All points at y=100
        hand_position[4][2] = 200  # Thumb tip at y=200 (lowest point)

        # Act
        result = self.service._handle_sign(fingers, hand_position)

        # Assert
        self.assertEqual(result, "descend")

    def test_execute_gesture_command_takeoff(self):
        """Test execute gesture command for takeoff"""
        # Arrange
        gesture = "takeoff"

        # Act
        self.service._execute_gesture_command(gesture)

        # Assert
        self.mock_drone_service.takeoff.assert_called_once()

    def test_execute_gesture_command_land(self):
        """Test execute gesture command for land"""
        # Arrange
        gesture = "land"

        # Act
        self.service._execute_gesture_command(gesture)

        # Assert
        self.mock_drone_service.land.assert_called_once()

    def test_execute_gesture_command_moveUp(self):
        """Test execute gesture command for moveUp"""
        # Arrange
        gesture = "monte"

        # Act
        self.service._execute_gesture_command(gesture)

        # Assert
        expected_calls = [
            call(0, 0, 50, 0),  # Move up
            call(0, 0, 0, 0)    # Stop movement
        ]
        self.assertEqual(self.mock_drone.send_rc_control.call_count, 2)
        self.mock_drone.send_rc_control.assert_has_calls(expected_calls)

    def test_execute_gesture_command_drone_not_connected(self):
        """Test execute gesture command when drone is not connected"""
        # Arrange
        self.mock_drone_service.connected = False
        gesture = "takeoff"

        # Act
        self.service._execute_gesture_command(gesture)

        # Assert
        self.mock_drone_service.takeoff.assert_not_called()

    def test_execute_gesture_command_exception(self):
        """Test execute gesture command with exception"""
        # Arrange
        gesture = "takeoff"
        self.mock_drone_service.takeoff.side_effect = Exception("Test error")

        # Act
        with patch('services.gesture_service.logger.error') as mock_logger:
            self.service._execute_gesture_command(gesture)

        # Assert
        mock_logger.assert_called_once()
        self.assertIn("error", mock_logger.call_args[0][0].lower())

    def test_get_status(self):
        """Test getting gesture service status"""
        # Arrange
        self.service.is_running = True
        self.service.gesture_cooldown = 2.5
        self.service.last_gesture_time = 100

        # Act
        status = self.service.get_status()

        # Assert
        self.assertEqual(status['is_running'], True)
        self.assertEqual(status['cooldown'], 2.5)
        self.assertEqual(status['last_gesture_time'], 100)
        self.assertIn('time_until_next', status)

    def test_set_cooldown_valid(self):
        """Test setting valid cooldown value"""
        # Act
        success, message = self.service.set_cooldown(3.0)

        # Assert
        self.assertTrue(success)
        self.assertEqual(self.service.gesture_cooldown, 3.0)
        self.assertTrue("défini à" in message.lower() or "set to" in message.lower())

    def test_set_cooldown_too_low(self):
        """Test setting cooldown value that is too low"""
        # Arrange
        original_cooldown = self.service.gesture_cooldown

        # Act
        success, message = self.service.set_cooldown(0.1)

        # Assert
        self.assertFalse(success)
        self.assertEqual(self.service.gesture_cooldown, original_cooldown)
        self.assertTrue("inférieur" in message.lower() or "less than" in message.lower())

    def test_set_cooldown_too_high(self):
        """Test setting cooldown value that is too high"""
        # Arrange
        original_cooldown = self.service.gesture_cooldown

        # Act
        success, message = self.service.set_cooldown(15.0)

        # Assert
        self.assertFalse(success)
        self.assertEqual(self.service.gesture_cooldown, original_cooldown)
        self.assertTrue("supérieur" in message.lower() or "more than" in message.lower())

    def test_set_cooldown_invalid_type(self):
        """Test setting cooldown with invalid type"""
        # Arrange
        original_cooldown = self.service.gesture_cooldown

        # Act
        success, message = self.service.set_cooldown("not a number")

        # Assert
        self.assertFalse(success)
        self.assertEqual(self.service.gesture_cooldown, original_cooldown)
        self.assertTrue("invalide" in message.lower() or "invalid" in message.lower())

    def test_singleton_pattern(self):
        """Test that GestureService follows singleton pattern"""
        # Act
        service1 = GestureService()
        service2 = GestureService()

        # Assert
        self.assertIs(service1, service2)
        self.assertIs(service1, self.service)

if __name__ == '__main__':
    unittest.main()