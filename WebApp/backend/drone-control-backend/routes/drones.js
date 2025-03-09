const express = require('express');
const { check } = require('express-validator');
const { 
  getDrones, 
  getDrone, 
  createDrone, 
  updateDrone, 
  deleteDrone,
  startFlight,
  endFlight,
  sendCommand,
  getTelemetry,
  updateKeyBindings,
  getFlightLogs
} = require('../controllers/droneController');
const { getDroneMedia, uploadMedia } = require('../controllers/mediaController');
const { protect, authorize } = require('../middlewares/auth');
const { validateRequest } = require('../middlewares/validation');
const { mediaUpload } = require('../controllers/mediaController');

const router = express.Router();

// Apply authentication to all routes
router.use(protect);

// Basic drone routes
router.get('/', getDrones);

router.post('/', [
  check('name', 'Name is required').not().isEmpty(),
  check('model', 'Model is required').not().isEmpty(),
  check('serialNumber', 'Serial number is required').not().isEmpty()
], validateRequest, createDrone);

router.get('/:id', getDrone);
router.put('/:id', updateDrone);
router.delete('/:id', deleteDrone);

// Flight control routes
router.post('/:id/flight/start', startFlight);
router.post('/:id/flight/end', endFlight);
router.post('/:id/command', sendCommand);

// Telemetry routes
router.get('/:id/telemetry', getTelemetry);

// Configuration routes
router.put('/:id/keyboard-bindings', updateKeyBindings);

// Flight logs
router.get('/:id/flight-logs', getFlightLogs);

// Media routes
router.get('/:droneId/media', getDroneMedia);
router.post('/:droneId/media', mediaUpload, uploadMedia);

module.exports = router;
