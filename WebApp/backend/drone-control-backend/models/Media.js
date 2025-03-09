const mongoose = require('mongoose');

const MediaSchema = new mongoose.Schema({
  drone: {
    type: mongoose.Schema.ObjectId,
    ref: 'Drone',
    required: true,
  },
  type: {
    type: String,
    enum: ['photo', 'video'],
    required: true,
  },
  filename: {
    type: String,
    required: true,
  },
  filepath: {
    type: String,
    required: true,
  },
  size: {
    type: Number, // in bytes
    required: true,
  },
  mimeType: {
    type: String,
    required: true,
  },
  resolution: {
    width: Number,
    height: Number,
  },
  duration: { // for videos only
    type: Number, // in seconds
    default: 0,
  },
  location: {
    longitude: Number,
    latitude: Number,
    altitude: Number,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Media', MediaSchema);
