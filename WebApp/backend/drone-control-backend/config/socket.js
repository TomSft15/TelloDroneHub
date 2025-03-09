const logger = require('../utils/logger');
const droneHandler = require('../socket/handlers/droneHandler');
const authMiddleware = require('../middlewares/auth');

module.exports = (io) => {
  // Middleware pour authentifier les connexions socket
  io.use(async (socket, next) => {
    try {
      const token = socket.handshake.auth.token;
      if (!token) {
        return next(new Error('Authentication error: Token missing'));
      }

      const user = await authMiddleware.verifySocketToken(token);
      socket.user = user;
      next();
    } catch (error) {
      next(new Error('Authentication error: Invalid token'));
    }
  });

  // Gestionnaire des événements de drone
  io.on('connection', (socket) => {
    logger.info(`New client connected: ${socket.id}, User: ${socket.user?.email}`);

    // Enregistre le gestionnaire de drone
    droneHandler(io, socket);

    socket.on('disconnect', () => {
      logger.info(`Client disconnected: ${socket.id}`);
    });
  });
};
