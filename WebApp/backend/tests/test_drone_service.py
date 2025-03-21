import unittest
from unittest.mock import patch, MagicMock, call
from services.drone_service import DroneService

class TestDroneService(unittest.TestCase):
    """Tests for the DroneService class"""

    def setUp(self):
        """Set up test environment before each test"""
        # Reset singleton instance
        DroneService._instance = None

        # Create patchers
        self.tello_patcher = patch('services.drone_service.Tello')
        self.mock_tello = self.tello_patcher.start()

        self.check_port_patcher = patch('services.drone_service.check_port_in_use')
        self.mock_check_port = self.check_port_patcher.start()
        self.mock_check_port.return_value = False  # Port is available

        self.check_processes_patcher = patch('services.drone_service.check_for_existing_processes')
        self.mock_check_processes = self.check_processes_patcher.start()
        self.mock_check_processes.return_value = False  # No existing processes

        # Initialize service
        self.service = DroneService()

    def tearDown(self):
        """Clean up after each test"""
        self.tello_patcher.stop()
        self.check_port_patcher.stop()
        self.check_processes_patcher.stop()

    def test_connect_success(self):
        """Test successful drone connection"""
        # Arrange
        mock_drone = self.mock_tello.return_value

        # Act
        success, message = self.service.connect()

        # Assert
        self.assertTrue(success)
        self.assertTrue("succès" in message.lower() or "success" in message.lower())
        self.assertTrue(self.service.connected)
        mock_drone.connect.assert_called_once()

    def test_connect_port_in_use(self):
        """Test connection when port is in use"""
        # Arrange
        self.mock_check_port.return_value = True  # Port is in use

        # Act
        success, message = self.service.connect()

        # Assert
        self.assertFalse(success)
        self.assertTrue("port" in message.lower())
        self.assertFalse(self.service.connected)
        self.mock_tello.return_value.connect.assert_not_called()

    def test_connect_existing_processes(self):
        """Test connection when existing processes are using the port"""
        # Arrange
        self.mock_check_processes.return_value = True  # Existing processes

        # Act
        success, message = self.service.connect()

        # Assert
        self.assertFalse(success)
        self.assertTrue("processus" in message.lower() or "process" in message.lower())
        self.assertFalse(self.service.connected)
        self.mock_tello.return_value.connect.assert_not_called()

    def test_connect_exception(self):
        """Test connection handling exceptions"""
        # Arrange
        self.mock_tello.return_value.connect.side_effect = Exception("Test error")

        # Act
        success, message = self.service.connect()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())
        self.assertFalse(self.service.connected)

    def test_disconnect_success(self):
        """Test successful drone disconnection"""
        # Arrange
        self.service.connected = True
        self.service.drone = self.mock_tello.return_value
        self.service.drone.is_flying = False

        # Act
        success, message = self.service.disconnect()

        # Assert
        self.assertTrue(success)
        self.assertTrue("succès" in message.lower() or "success" in message.lower())
        self.assertFalse(self.service.connected)
        self.assertIsNone(self.service.drone)

    def test_disconnect_while_flying(self):
        """Test disconnection when drone is flying"""
        # Arrange
        self.service.connected = True
        self.service.drone = self.mock_tello.return_value
        self.service.drone.is_flying = True

        # Act
        success, message = self.service.disconnect()

        # Assert
        self.assertTrue(success)
        self.service.drone.land.assert_called_once()
        self.assertFalse(self.service.connected)
        self.assertIsNone(self.service.drone)

    def test_disconnect_not_connected(self):
        """Test disconnection when not connected"""
        # Arrange
        self.service.connected = False
        self.service.drone = None

        # Act
        success, message = self.service.disconnect()

        # Assert
        self.assertTrue(success)
        self.assertTrue("déjà déconnecté" in message.lower() or "already disconnected" in message.lower())

    def test_takeoff_success(self):
        """Test successful takeoff"""
        # Arrange
        self.service.connected = True
        self.service.drone = self.mock_tello.return_value

        # Act
        success, message = self.service.takeoff()

        # Assert
        self.assertTrue(success)
        self.service.drone.takeoff.assert_called_once()
        self.service.drone.send_rc_control.assert_called_once_with(0, 0, 0, 0)

    def test_takeoff_not_connected(self):
        """Test takeoff when not connected"""
        # Arrange
        self.service.connected = False
        self.service.drone = None

        # Act
        success, message = self.service.takeoff()

        # Assert
        self.assertFalse(success)
        self.assertTrue("non connecté" in message.lower() or "not connected" in message.lower())

    def test_takeoff_exception(self):
        """Test takeoff handling exceptions"""
        # Arrange
        self.service.connected = True
        self.service.drone = self.mock_tello.return_value
        self.service.drone.takeoff.side_effect = Exception("Test error")

        # Act
        success, message = self.service.takeoff()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())

    def test_land_success(self):
        """Test successful landing"""
        # Arrange
        self.service.connected = True
        self.service.drone = self.mock_tello.return_value

        # Act
        success, message = self.service.land()

        # Assert
        self.assertTrue(success)
        self.service.drone.land.assert_called_once()

    def test_land_not_connected(self):
        """Test landing when not connected"""
        # Arrange
        self.service.connected = False
        self.service.drone = None

        # Act
        success, message = self.service.land()

        # Assert
        self.assertFalse(success)
        self.assertTrue("non connecté" in message.lower() or "not connected" in message.lower())

    def test_land_exception(self):
        """Test landing handling exceptions"""
        # Arrange
        self.service.connected = True
        self.service.drone = self.mock_tello.return_value
        self.service.drone.land.side_effect = Exception("Test error")

        # Act
        success, message = self.service.land()

        # Assert
        self.assertFalse(success)
        self.assertTrue("error" in message.lower() or "erreur" in message.lower())

    def test_update_drone_data(self):
        """Test updating drone data"""
        # Arrange
        self.service.connected = True
        self.service.drone = self.mock_tello.return_value

        # Mock drone methods for data
        self.service.drone.get_battery.return_value = 80
        self.service.drone.get_temperature.return_value = 25
        self.service.drone.get_flight_time.return_value = 120
        self.service.drone.get_height.return_value = 50
        self.service.drone.get_speed_x.return_value = 10

        # Create mock for drone_data
        mock_drone_data = MagicMock()
        mock_drone_data.update_from_drone.return_value = True
        self.service.drone_data = mock_drone_data

        # Act
        with patch('services.drone_service.time.sleep', return_value=None) as mock_sleep:
            # Mock threading by calling method directly
            # We'll just test one iteration
            self.service._update_drone_data()

        # Assert
        mock_drone_data.update_from_drone.assert_called_once_with(self.service.drone)

    def test_get_drone_data(self):
        """Test getting drone data"""
        # Arrange
        mock_data = {'battery': 80, 'temperature': 25}
        mock_drone_data = MagicMock()
        mock_drone_data.to_dict.return_value = mock_data
        self.service.drone_data = mock_drone_data

        # Act
        result = self.service.get_drone_data()

        # Assert
        self.assertEqual(result, mock_data)
        mock_drone_data.to_dict.assert_called_once()

    def test_singleton_pattern(self):
        """Test that DroneService follows singleton pattern"""
        # Act
        service1 = DroneService()
        service2 = DroneService()

        # Assert
        self.assertIs(service1, service2)
        self.assertIs(service1, self.service)

if __name__ == '__main__':
    unittest.main()