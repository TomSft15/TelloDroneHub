const Drone = require('../models/Drone');
const FlightLog = require('../models/FlightLog');
const logger = require('../utils/logger');

// Mock data for drone telemetry
let droneTelemetry = {};

/**
 * Connect to a drone
 * @param {String} droneId 
 * @returns {Promise<Object>}
 */
exports.connectDrone = async (droneId) => {
  try {
    const drone = await Drone.findById(droneId);
    if (!drone) {
      throw new Error('Drone not found');
    }
    
    // Initialize telemetry for this drone
    droneTelemetry[droneId] = {
      battery: drone.batteryLevel,
      altitude: 0,
      speed: 0,
      position: {
        latitude: 48.8584, // Mock coordinates (Paris)
        longitude: 2.2945,
        altitude: 0
      },
      orientation: {
        pitch: 0,
        roll: 0,
        yaw: 0
      },
      status: 'connected',
      lastUpdated: new Date()
    };
    
    logger.info(`Connected to drone: ${droneId}`);
    
    return { success: true, message: 'Connected to drone' };
  } catch (error) {
    logger.error(`Error connecting to drone ${droneId}: ${error.message}`);
    throw error;
  }
};

/**
 * Disconnect from a drone
 * @param {String} droneId 
 * @returns {Promise<Object>}
 */
exports.disconnectDrone = async (droneId) => {
  try {
    const drone = await Drone.findById(droneId);
    if (!drone) {
      throw new Error('Drone not found');
    }
    
    // Clean up telemetry for this drone
    if (droneTelemetry[droneId]) {
      delete droneTelemetry[droneId];
    }
    
    logger.info(`Disconnected from drone: ${droneId}`);
    
    return { success: true, message: 'Disconnected from drone' };
  } catch (error) {
    logger.error(`Error disconnecting from drone ${droneId}: ${error.message}`);
    throw error;
  }
};

/**
 * Send a command to a drone
 * @param {String} droneId 
 * @param {String} command 
 * @param {Object} params 
 * @returns {Promise<Object>}
 */
exports.sendCommand = async (droneId, command, params = {}) => {
  try {
    if (!droneTelemetry[droneId]) {
      throw new Error('Drone not connected');
    }
    
    // Simulate command processing
    logger.info(`Command sent to drone ${droneId}: ${command}`, { params });
    
    // Update telemetry based on command
    const telemetry = droneTelemetry[droneId];
    
    switch (command) {
      case 'takeoff':
        telemetry.altitude = 1.0;
        telemetry.status = 'flying';
        break;
      case 'land':
        telemetry.altitude = 0;
        telemetry.speed = 0;
        telemetry.status = 'landed';
        break;
      case 'moveUp':
        telemetry.altitude += 0.5;
        break;
      case 'moveDown':
        telemetry.altitude = Math.max(0, telemetry.altitude - 0.5);
        break;
      case 'moveForward':
        telemetry.position.latitude += 0.0001;
        telemetry.speed = 2;
        break;
      case 'moveBackward':
        telemetry.position.latitude -= 0.0001;
        telemetry.speed = 2;
        break;
      case 'moveLeft':
        telemetry.position.longitude -= 0.0001;
        telemetry.speed = 2;
        break;
      case 'moveRight':
        telemetry.position.longitude += 0.0001;
        telemetry.speed = 2;
        break;
      case 'rotateLeft':
        telemetry.orientation.yaw = (telemetry.orientation.yaw - 10) % 360;
        break;
      case 'rotateRight':
        telemetry.orientation.yaw = (telemetry.orientation.yaw + 10) % 360;
        break;
      case 'hover':
        telemetry.speed = 0;
        break;
      case 'emergencyStop':
        telemetry.speed = 0;
        telemetry.status = 'emergency';
        break;
      case 'returnToHome':
        telemetry.status = 'returning';
        // Simulate gradual return
        setTimeout(() => {
          if (droneTelemetry[droneId]) {
            droneTelemetry[droneId].status = 'landed';
            droneTelemetry[droneId].altitude = 0;
            droneTelemetry[droneId].speed = 0;
          }
        }, 5000);
        break;
      default:
        logger.warn(`Unknown command: ${command}`);
    }
    
    telemetry.lastUpdated = new Date();
    
    // Simulate battery usage
    telemetry.battery -= 0.1;
    if (telemetry.battery < 0) telemetry.battery = 0;
    
    // Update flight log with new position
    try {
      const flightLog = await FlightLog.findOne({ 
        drone: droneId,
        endTime: null 
      }).sort('-startTime');
      
      if (flightLog) {
        // Add position to path
        flightLog.path.push({
          longitude: telemetry.position.longitude,
          latitude: telemetry.position.latitude,
          altitude: telemetry.altitude,
          timestamp: new Date()
        });
        
        // Update flight statistics
        flightLog.maxAltitude = Math.max(flightLog.maxAltitude, telemetry.altitude);
        flightLog.maxSpeed = Math.max(flightLog.maxSpeed, telemetry.speed);
        
        // Calculate distance (very simplified)
        if (flightLog.path.length > 1) {
          const lastPos = flightLog.path[flightLog.path.length - 2];
          const newPos = flightLog.path[flightLog.path.length - 1];
          
          // Simple Euclidean distance (not accurate for geographic coordinates but sufficient for mock)
          const distance = Math.sqrt(
            Math.pow(newPos.longitude - lastPos.longitude, 2) +
            Math.pow(newPos.latitude - lastPos.latitude, 2)
          ) * 111000; // Rough conversion to meters
          
          flightLog.distance += distance;
        }
        
        await flightLog.save();
      }
    } catch (error) {
      logger.warn(`Failed to update flight log: ${error.message}`);
    }
    
    // Return command result
    return {
      success: true,
      command,
      result: `Command ${command} executed successfully`,
      newState: {
        status: telemetry.status,
        altitude: telemetry.altitude,
        speed: telemetry.speed
      }
    };
  } catch (error) {
    logger.error(`Error sending command to drone ${droneId}: ${error.message}`);
    throw error;
  }
};

/**
 * Get real-time telemetry data from a drone
 * @param {String} droneId 
 * @returns {Promise<Object>}
 */
exports.getTelemetry = async (droneId) => {
  try {
    // Check if drone exists
    const drone = await Drone.findById(droneId);
    if (!drone) {
      throw new Error('Drone not found');
    }
    
    // If not connected, return last known data from database
    if (!droneTelemetry[droneId]) {
      return {
        battery: drone.batteryLevel,
        status: drone.status,
        lastConnection: drone.lastConnection,
        connected: false
      };
    }
    
    // Return current telemetry
    return {
      ...droneTelemetry[droneId],
      connected: true
    };
  } catch (error) {
    logger.error(`Error getting telemetry for drone ${droneId}: ${error.message}`);
    throw error;
  }
};
