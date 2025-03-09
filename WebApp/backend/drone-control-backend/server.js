const app = require('./app');
const http = require('http');
const socketIO = require('socket.io');
const socketConfig = require('./config/socket');
const { connectDB } = require('./config/database');
const logger = require('./utils/logger');
const config = require('./config/config');

const server = http.createServer(app);
const io = socketIO(server, {
  cors: {
    origin: config.corsOrigins,
    methods: ['GET', 'POST']
  }
});

// Configure socket.io
socketConfig(io);

// Connect to database
connectDB();

const PORT = config.port || 3000;

server.listen(PORT, () => {
  logger.info(`Server running on port ${PORT} in ${process.env.NODE_ENV} mode`);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  logger.error(`Error: ${err.message}`);
  // Close server & exit process
  server.close(() => process.exit(1));
});