const mongoose = require('mongoose');

const DroneSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Please add a name'],
    trim: true,
    maxlength: [50, 'Name cannot be more than 50 characters'],
  },
  model: {
    type: String,
    required: [true, 'Please add a model'],
    trim: true,
  },
  serialNumber: {
    type: String,
    required: [true, 'Please add a serial number'],
    unique: true,
    trim: true,
  },
  owner: {
    type: mongoose.Schema.ObjectId,
    ref: 'User',
    required: true,
  },
  status: {
    type: String,
    enum: ['active', 'inactive', 'maintenance', 'flying'],
    default: 'inactive',
  },
  batteryLevel: {
    type: Number,
    min: [0, 'Battery level cannot be less than 0'],
    max: [100, 'Battery level cannot be more than 100'],
    default: 100,
  },
  lastConnection: {
    type: Date,
    default: null,
  },
  firmware: {
    type: String,
    default: '1.0.0',
  },
  keyBindings: {
    type: Object,
    default: {
      'ArrowUp': 'moveUp',
      'ArrowDown': 'moveDown',
      'ArrowLeft': 'moveLeft',
      'ArrowRight': 'moveRight',
      'w': 'moveForward',
      's': 'moveBackward',
      'a': 'rotateLeft',
      'd': 'rotateRight',
      't': 'takeoff',
      'l': 'land',
      'Escape': 'emergencyStop',
      'Space': 'hover',
      'c': 'capturePhoto',
      'v': 'startRecording',
      'b': 'stopRecording',
      '1': 'increaseAltitude',
      '2': 'decreaseAltitude',
      '3': 'increaseSpeed',
      '4': 'decreaseSpeed',
      'r': 'returnToHome'
    },
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
}, {
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Virtuals for flight logs and media
DroneSchema.virtual('flightLogs', {
  ref: 'FlightLog',
  localField: '_id',
  foreignField: 'drone',
  justOne: false,
});

DroneSchema.virtual('media', {
  ref: 'Media',
  localField: '_id',
  foreignField: 'drone',
  justOne: false,
});

// Cascade delete flight logs and media when a drone is deleted
DroneSchema.pre('remove', async function(next) {
  await this.model('FlightLog').deleteMany({ drone: this._id });
  await this.model('Media').deleteMany({ drone: this._id });
  next();
});

module.exports = mongoose.model('Drone', DroneSchema);
