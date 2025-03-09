const Drone = require('../models/Drone');
const FlightLog = require('../models/FlightLog');
const droneService = require('../services/droneService');
const logger = require('../utils/logger');

// @desc    Get all drones
// @route   GET /api/drones
// @access  Private
exports.getDrones = async (req, res, next) => {
  try {
    // Filter by user if not admin
    const filter = req.user.role === 'admin' ? {} : { owner: req.user.id };
    
    const drones = await Drone.find(filter);
    
    res.status(200).json({
      success: true,
      count: drones.length,
      data: drones
    });
  } catch (err) {
    logger.error(`Error in getDrones: ${err.message}`);
    next(err);
  }
};

// @desc    Get single drone
// @route   GET /api/drones/:id
// @access  Private
exports.getDrone = async (req, res, next) => {
  try {
    const drone = await Drone.findById(req.params.id)
      .populate('flightLogs')
      .populate('media');
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to view this drone'
      });
    }
    
    res.status(200).json({
      success: true,
      data: drone
    });
  } catch (err) {
    logger.error(`Error in getDrone: ${err.message}`);
    next(err);
  }
};

// @desc    Create new drone
// @route   POST /api/drones
// @access  Private
exports.createDrone = async (req, res, next) => {
  try {
    // Add owner to drone data
    req.body.owner = req.user.id;
    
    const drone = await Drone.create(req.body);
    
    res.status(201).json({
      success: true,
      data: drone
    });
  } catch (err) {
    logger.error(`Error in createDrone: ${err.message}`);
    next(err);
  }
};

// @desc    Update drone
// @route   PUT /api/drones/:id
// @access  Private
exports.updateDrone = async (req, res, next) => {
  try {
    let drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to update this drone'
      });
    }
    
    // Don't allow owner change
    if (req.body.owner) {
      delete req.body.owner;
    }
    
    drone = await Drone.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true
    });
    
    res.status(200).json({
      success: true,
      data: drone
    });
  } catch (err) {
    logger.error(`Error in updateDrone: ${err.message}`);
    next(err);
  }
};

// @desc    Delete drone
// @route   DELETE /api/drones/:id
// @access  Private
exports.deleteDrone = async (req, res, next) => {
  try {
    const drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to delete this drone'
      });
    }
    
    await drone.remove();
    
    res.status(200).json({
      success: true,
      data: {}
    });
  } catch (err) {
    logger.error(`Error in deleteDrone: ${err.message}`);
    next(err);
  }
};

// @desc    Start drone flight
// @route   POST /api/drones/:id/flight/start
// @access  Private
exports.startFlight = async (req, res, next) => {
  try {
    const drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to fly this drone'
      });
    }
    
    // Check if drone is already flying
    if (drone.status === 'flying') {
      return res.status(400).json({
        success: false,
        error: 'Drone is already flying'
      });
    }
    
    // Create a flight log
    const flightLog = await FlightLog.create({
      drone: drone._id,
      startTime: new Date(),
      controlMode: req.body.controlMode || 'keyboard'
    });
    
    // Update drone status
    drone.status = 'flying';
    drone.lastConnection = new Date();
    await drone.save();
    
    // Connect to drone via service
    const connectionResult = await droneService.connectDrone(drone._id);
    
    res.status(200).json({
      success: true,
      data: {
        drone,
        flightLog,
        connection: connectionResult
      }
    });
  } catch (err) {
    logger.error(`Error in startFlight: ${err.message}`);
    next(err);
  }
};

// @desc    End drone flight
// @route   POST /api/drones/:id/flight/end
// @access  Private
exports.endFlight = async (req, res, next) => {
  try {
    const drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to control this drone'
      });
    }
    
    // Check if drone is flying
    if (drone.status !== 'flying') {
      return res.status(400).json({
        success: false,
        error: 'Drone is not flying'
      });
    }
    
    // Find the active flight log
        // Find the active flight log
    const flightLog = await FlightLog.findOne({ 
      drone: drone._id,
      endTime: null 
    }).sort('-startTime');
    
    if (!flightLog) {
      logger.warn(`No active flight log found for drone ${drone._id}`);
    } else {
      // Update flight log
      const endTime = new Date();
      const duration = (endTime - flightLog.startTime) / 1000; // in seconds
      
      flightLog.endTime = endTime;
      flightLog.duration = duration;
      // Additional metrics would be updated during flight
      await flightLog.save();
    }
    
    // Update drone status
    drone.status = 'inactive';
    drone.lastConnection = new Date();
    // Simulating battery consumption
    drone.batteryLevel = Math.max(0, drone.batteryLevel - Math.floor(Math.random() * 10) - 5);
    await drone.save();
    
    // Disconnect drone via service
    await droneService.disconnectDrone(drone._id);
    
    res.status(200).json({
      success: true,
      data: {
        drone,
        flightLog
      }
    });
  } catch (err) {
    logger.error(`Error in endFlight: ${err.message}`);
    next(err);
  }
};

// @desc    Send command to drone
// @route   POST /api/drones/:id/command
// @access  Private
exports.sendCommand = async (req, res, next) => {
  try {
    const { command, params } = req.body;
    const drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to control this drone'
      });
    }
    
    // Check if drone is flying
    if (drone.status !== 'flying') {
      return res.status(400).json({
        success: false,
        error: 'Cannot send command: Drone is not flying'
      });
    }
    
    // Send command to drone via service
    const result = await droneService.sendCommand(drone._id, command, params);
    
    res.status(200).json({
      success: true,
      command,
      result
    });
  } catch (err) {
    logger.error(`Error in sendCommand: ${err.message}`);
    next(err);
  }
};

// @desc    Get drone telemetry
// @route   GET /api/drones/:id/telemetry
// @access  Private
exports.getTelemetry = async (req, res, next) => {
  try {
    const drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to view this drone telemetry'
      });
    }
    
    // Get telemetry from service
    const telemetry = await droneService.getTelemetry(drone._id);
    
    res.status(200).json({
      success: true,
      data: telemetry
    });
  } catch (err) {
    logger.error(`Error in getTelemetry: ${err.message}`);
    next(err);
  }
};

// @desc    Update drone keyboard bindings
// @route   PUT /api/drones/:id/keyboard-bindings
// @access  Private
exports.updateKeyBindings = async (req, res, next) => {
  try {
    const { keyBindings } = req.body;
    let drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to update this drone'
      });
    }
    
    // Update key bindings
    drone = await Drone.findByIdAndUpdate(
      req.params.id,
      { keyBindings },
      { new: true, runValidators: true }
    );
    
    res.status(200).json({
      success: true,
      data: drone.keyBindings
    });
  } catch (err) {
    logger.error(`Error in updateKeyBindings: ${err.message}`);
    next(err);
  }
};

// @desc    Get drone flight logs
// @route   GET /api/drones/:id/flight-logs
// @access  Private
exports.getFlightLogs = async (req, res, next) => {
  try {
    const drone = await Drone.findById(req.params.id);
    
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to view this drone logs'
      });
    }
    
    const flightLogs = await FlightLog.find({ drone: req.params.id })
                                      .sort('-startTime');
    
    res.status(200).json({
      success: true,
      count: flightLogs.length,
      data: flightLogs
    });
  } catch (err) {
    logger.error(`Error in getFlightLogs: ${err.message}`);
    next(err);
  }
};
