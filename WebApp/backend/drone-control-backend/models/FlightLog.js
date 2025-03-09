const mongoose = require('mongoose');

const FlightLogSchema = new mongoose.Schema({
  drone: {
    type: mongoose.Schema.ObjectId,
    ref: 'Drone',
    required: true,
  },
  startTime: {
    type: Date,
    required: true,
  },
  endTime: {
    type: Date,
    default: null,
  },
  duration: {
    type: Number, // in seconds
    default: 0,
  },
  maxAltitude: {
    type: Number, // in meters
    default: 0,
  },
  maxSpeed: {
    type: Number, // in m/s
    default: 0,
  },
  distance: {
    type: Number, // in meters
    default: 0,
  },
  path: [{
    longitude: Number,
    latitude: Number,
    altitude: Number,
    timestamp: Date,
  }],
  batteryConsumption: {
    type: Number, // percentage
    default: 0,
  },
  controlMode: {
    type: String,
    enum: ['voice', 'gesture', 'vision', 'keyboard'],
    default: 'keyboard',
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('FlightLog', FlightLogSchema);
