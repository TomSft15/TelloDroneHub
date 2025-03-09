const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const helmet = require('helmet');
const errorHandler = require('./middlewares/errorHandler');
const config = require('./config/config');

// Route imports
const authRoutes = require('./routes/auth');
const droneRoutes = require('./routes/drones');
const userRoutes = require('./routes/users');
const mediaRoutes = require('./routes/media');

const app = express();

// Middlewares
app.use(helmet());
app.use(cors({
  origin: config.corsOrigins
}));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Logging
if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
}

// Static folder for media
app.use('/uploads', express.static('uploads'));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/drones', droneRoutes);
app.use('/api/users', userRoutes);
app.use('/api/media', mediaRoutes);

// API health check
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'Drone Control API is up and running' });
});

// Error handling
app.use(errorHandler);

module.exports = app;