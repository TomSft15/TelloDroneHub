const droneService = require('../../services/droneService');
const Drone = require('../../models/Drone');
const logger = require('../../utils/logger');

/**
 * Handle drone-related socket events
 * @param {Object} io - Socket.io instance
 * @param {Object} socket - Socket connection
 */
module.exports = (io, socket) => {
  /**
   * Subscribe to updates for a specific drone
   */
  socket.on('drone:subscribe', async (droneId) => {
    try {
      // Check if user has access to this drone
      const drone = await Drone.findById(droneId);
      if (!drone) {
        socket.emit('drone:error', { message: 'Drone not found' });
        return;
      }
      
      // Check ownership if not admin
      if (socket.user.role !== 'admin' && drone.owner.toString() !== socket.user.id) {
        socket.emit('drone:error', { message: 'Not authorized to access this drone' });
        return;
      }
      
      // Join drone-specific room
      socket.join(`drone:${droneId}`);
      logger.info(`User ${socket.user.email} subscribed to drone ${droneId}`);
      
      // Send initial telemetry
      try {
        const telemetry = await droneService.getTelemetry(droneId);
        socket.emit('drone:telemetry', telemetry);
      } catch (error) {
        logger.error(`Error sending initial telemetry: ${error.message}`);
      }
    } catch (error) {
      logger.error(`Error in drone:subscribe: ${error.message}`);
      socket.emit('drone:error', { message: 'Failed to subscribe to drone updates' });
    }
  });
  
  /**
   * Unsubscribe from updates for a specific drone
   */
  socket.on('drone:unsubscribe', (droneId) => {
    socket.leave(`drone:${droneId}`);
    logger.info(`User ${socket.user.email} unsubscribed from drone ${droneId}`);
  });
  
  /**
   * Send a command to the drone
   */
  socket.on('drone:command', async ({ droneId, command, params }) => {
    try {
      // Check if user has access to this drone
      const drone = await Drone.findById(droneId);
      if (!drone) {
        socket.emit('drone:error', { message: 'Drone not found' });
        return;
      }
      
      // Check ownership if not admin
      if (socket.user.role !== 'admin' && drone.owner.toString() !== socket.user.id) {
        socket.emit('drone:error', { message: 'Not authorized to control this drone' });
        return;
      }
      
      // Check if drone is flying (except for takeoff command)
      if (command !== 'takeoff' && drone.status !== 'flying') {
        socket.emit('drone:error', { message: 'Cannot send command: Drone is not flying' });
        return;
      }
      
      // Send the command to the drone service
      const result = await droneService.sendCommand(droneId, command, params);
      
      // Send the result back to just this client
      socket.emit('drone:command:result', result);
      
      // Send updated telemetry to all subscribers
      const telemetry = await droneService.getTelemetry(droneId);
      io.to(`drone:${droneId}`).emit('drone:telemetry', telemetry);
    } catch (error) {
      logger.error(`Error in drone:command: ${error.message}`);
      socket.emit('drone:error', { message: `Failed to send command: ${error.message}` });
    }
  });
  
  /**
   * Request telemetry update
   */
  socket.on('drone:telemetry:request', async ({ droneId }) => {
    try {
      // Check if user has access to this drone
      const drone = await Drone.findById(droneId);
      if (!drone) {
        socket.emit('drone:error', { message: 'Drone not found' });
        return;
      }
      
      // Check ownership if not admin
      if (socket.user.role !== 'admin' && drone.owner.toString() !== socket.user.id) {
        socket.emit('drone:error', { message: 'Not authorized to access this drone telemetry' });
        return;
      }
      
      // Get telemetry and send it only to the requesting client
      const telemetry = await droneService.getTelemetry(droneId);
      socket.emit('drone:telemetry', telemetry);
    } catch (error) {
      logger.error(`Error in drone:telemetry:request: ${error.message}`);
      socket.emit('drone:error', { message: `Failed to get telemetry: ${error.message}` });
    }
  });
  
  /**
   * Setup a mock telemetry update interval for connected drones
   * In a real application, this would be driven by actual drone updates
   */
  const telemetryInterval = setInterval(async () => {
    try {
      // Get list of rooms this socket is in
      const rooms = Array.from(socket.rooms);
      
      // Find drone rooms
      const droneRooms = rooms.filter(room => room.startsWith('drone:'));
      
      // Send telemetry updates for each drone
      for (const room of droneRooms) {
        const droneId = room.split(':')[1];
        
        try {
          const telemetry = await droneService.getTelemetry(droneId);
          // Only send if there's a real-time connection
          if (telemetry.connected) {
            io.to(room).emit('drone:telemetry', telemetry);
          }
        } catch (error) {
          logger.warn(`Error updating telemetry for drone ${droneId}: ${error.message}`);
        }
      }
    } catch (error) {
      logger.error(`Error in telemetry interval: ${error.message}`);
    }
  }, 1000); // Update every second
  
  // Clean up on disconnect
  socket.on('disconnect', () => {
    clearInterval(telemetryInterval);
  });
};
