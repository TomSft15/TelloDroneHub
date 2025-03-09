const Drone = require('../models/Drone');
const FlightLog = require('../models/FlightLog');
const logger = require('../utils/logger');

/**
 * Get flight statistics for a drone
 * @param {String} droneId 
 * @returns {Promise<Object>}
 */
exports.getFlightStatistics = async (droneId) => {
  try {
    const drone = await Drone.findById(droneId);
    if (!drone) {
      throw new Error('Drone not found');
    }
    
    // Get all completed flight logs
    const flightLogs = await FlightLog.find({
      drone: droneId,
      endTime: { $ne: null }
    });
    
    if (flightLogs.length === 0) {
      return {
        totalFlights: 0,
        totalFlightTime: 0,
        avgFlightTime: 0,
        totalDistance: 0,
        maxAltitude: 0,
        maxSpeed: 0
      };
    }
    
    // Calculate statistics
    const totalFlights = flightLogs.length;
    const totalFlightTime = flightLogs.reduce((acc, log) => acc + log.duration, 0);
    const avgFlightTime = totalFlightTime / totalFlights;
    const totalDistance = flightLogs.reduce((acc, log) => acc + log.distance, 0);
    const maxAltitude = Math.max(...flightLogs.map(log => log.maxAltitude));
    const maxSpeed = Math.max(...flightLogs.map(log => log.maxSpeed));
    
    return {
      totalFlights,
      totalFlightTime,
      avgFlightTime,
      totalDistance,
      maxAltitude,
      maxSpeed
    };
  } catch (error) {
    logger.error(`Error getting flight statistics: ${error.message}`);
    throw error;
  }
};

/**
 * Get flight path data for a specific flight log
 * @param {String} flightLogId 
 * @returns {Promise<Object>}
 */
exports.getFlightPath = async (flightLogId) => {
  try {
    const flightLog = await FlightLog.findById(flightLogId);
    if (!flightLog) {
      throw new Error('Flight log not found');
    }
    
    return {
      startTime: flightLog.startTime,
      endTime: flightLog.endTime,
      duration: flightLog.duration,
      path: flightLog.path,
      distance: flightLog.distance,
      maxAltitude: flightLog.maxAltitude,
      maxSpeed: flightLog.maxSpeed,
      controlMode: flightLog.controlMode
    };
  } catch (error) {
    logger.error(`Error getting flight path: ${error.message}`);
    throw error;
  }
};

/**
 * Generate flight report data for a drone
 * @param {String} droneId 
 * @param {Object} timeFrame - { startDate, endDate }
 * @returns {Promise<Object>}
 */
exports.generateFlightReport = async (droneId, timeFrame) => {
  try {
    const { startDate, endDate } = timeFrame;
    
    // Get completed flights within time frame
    const query = {
      drone: droneId,
      endTime: { $ne: null }
    };
    
    if (startDate) {
      query.startTime = { $gte: new Date(startDate) };
    }
    
    if (endDate) {
      query.endTime = { ...query.endTime, $lte: new Date(endDate) };
    }
    
    const flightLogs = await FlightLog.find(query).sort('startTime');
    
    if (flightLogs.length === 0) {
      return {
        period: { start: startDate, end: endDate },
        flights: 0,
        data: []
      };
    }
    
    // Generate daily statistics
    const dailyStats = {};
    flightLogs.forEach(log => {
      const date = log.startTime.toISOString().split('T')[0];
      
      if (!dailyStats[date]) {
        dailyStats[date] = {
          date,
          flights: 0,
          totalDuration: 0,
          totalDistance: 0
        };
      }
      
      dailyStats[date].flights += 1;
      dailyStats[date].totalDuration += log.duration;
      dailyStats[date].totalDistance += log.distance;
    });
    
    return {
      period: {
        start: startDate || flightLogs[0].startTime,
        end: endDate || flightLogs[flightLogs.length - 1].endTime
      },
      flights: flightLogs.length,
      data: Object.values(dailyStats)
    };
  } catch (error) {
    logger.error(`Error generating flight report: ${error.message}`);
    throw error;
  }
};
