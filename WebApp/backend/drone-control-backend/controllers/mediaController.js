const Media = require('../models/Media');
const Drone = require('../models/Drone');
const mediaService = require('../services/mediaService');
const logger = require('../utils/logger');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const config = require('../config/config');

// Configure multer for file storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const dir = 'uploads/media';
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    cb(null, dir);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

// Filter files by type
const fileFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'video/mp4', 'video/quicktime'];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type. Only JPEG, PNG, and MP4 files are allowed.'), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: config.maxUploadSize }
});

exports.mediaUpload = upload.single('mediaFile');

// @desc    Get all media for a drone
// @route   GET /api/drones/:droneId/media
// @access  Private
exports.getDroneMedia = async (req, res, next) => {
  try {
    const drone = await Drone.findById(req.params.droneId);
    
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
        error: 'Not authorized to view this drone media'
      });
    }
    
    // Filter media by type if provided
    const filter = { drone: req.params.droneId };
    if (req.query.type) {
      filter.type = req.query.type;
    }
    
    const media = await Media.find(filter).sort('-createdAt');
    
    res.status(200).json({
      success: true,
      count: media.length,
      data: media
    });
  } catch (err) {
    logger.error(`Error in getDroneMedia: ${err.message}`);
    next(err);
  }
};

// @desc    Upload media file for a drone
// @route   POST /api/drones/:droneId/media
// @access  Private
exports.uploadMedia = async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: 'Please upload a file'
      });
    }
    
    const drone = await Drone.findById(req.params.droneId);
    
    if (!drone) {
      // Clean up file if drone not found
      fs.unlinkSync(req.file.path);
      return res.status(404).json({
        success: false,
        error: 'Drone not found'
      });
    }
    
    // Check ownership if not admin
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      // Clean up file if not authorized
      fs.unlinkSync(req.file.path);
      return res.status(403).json({
        success: false,
        error: 'Not authorized to upload media for this drone'
      });
    }
    
    // Determine media type
    const type = req.file.mimetype.startsWith('image/') ? 'photo' : 'video';
    
    // Get resolution/duration if possible
    let resolution = { width: 0, height: 0 };
    let duration = 0;
    
    if (type === 'photo' || type === 'video') {
      try {
        const mediaInfo = await mediaService.getMediaInfo(req.file.path, type);
        if (mediaInfo) {
          resolution = mediaInfo.resolution || resolution;
          duration = mediaInfo.duration || duration;
        }
      } catch (error) {
        logger.warn(`Failed to get media info: ${error.message}`);
      }
    }
    
    // Create media record
    const media = await Media.create({
      drone: req.params.droneId,
      type,
      filename: req.file.filename,
      filepath: req.file.path,
      size: req.file.size,
      mimeType: req.file.mimetype,
      resolution,
      duration,
      location: req.body.location ? JSON.parse(req.body.location) : null,
    });
    
    res.status(201).json({
      success: true,
      data: media
    });
  } catch (err) {
    // Clean up file on error
    if (req.file) {
      fs.unlinkSync(req.file.path);
    }
    
    logger.error(`Error in uploadMedia: ${err.message}`);
    next(err);
  }
};

// @desc    Get media file by ID
// @route   GET /api/media/:id
// @access  Private
exports.getMedia = async (req, res, next) => {
  try {
    const media = await Media.findById(req.params.id);
    
    if (!media) {
      return res.status(404).json({
        success: false,
        error: 'Media not found'
      });
    }
    
    // Check ownership by verifying drone ownership
    const drone = await Drone.findById(media.drone);
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Associated drone not found'
      });
    }
    
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to view this media'
      });
    }
    
    res.status(200).json({
      success: true,
      data: media
    });
  } catch (err) {
    logger.error(`Error in getMedia: ${err.message}`);
    next(err);
  }
};

// @desc    Delete media
// @route   DELETE /api/media/:id
// @access  Private
exports.deleteMedia = async (req, res, next) => {
  try {
    const media = await Media.findById(req.params.id);
    
    if (!media) {
      return res.status(404).json({
        success: false,
        error: 'Media not found'
      });
    }
    
    // Check ownership by verifying drone ownership
    const drone = await Drone.findById(media.drone);
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Associated drone not found'
      });
    }
    
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to delete this media'
      });
    }
    
    // Delete the file
    if (fs.existsSync(media.filepath)) {
      fs.unlinkSync(media.filepath);
    }
    
    // Delete database record
    await media.remove();
    
    res.status(200).json({
      success: true,
      data: {}
    });
  } catch (err) {
    logger.error(`Error in deleteMedia: ${err.message}`);
    next(err);
  }
};

// @desc    Stream/download media file
// @route   GET /api/media/:id/stream
// @access  Private
exports.streamMedia = async (req, res, next) => {
  try {
    const media = await Media.findById(req.params.id);
    
    if (!media) {
      return res.status(404).json({
        success: false,
        error: 'Media not found'
      });
    }
    
    // Check ownership by verifying drone ownership
    const drone = await Drone.findById(media.drone);
    if (!drone) {
      return res.status(404).json({
        success: false,
        error: 'Associated drone not found'
      });
    }
    
    if (req.user.role !== 'admin' && drone.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        error: 'Not authorized to access this media'
      });
    }
    
    if (!fs.existsSync(media.filepath)) {
      return res.status(404).json({
        success: false,
        error: 'Media file not found on server'
      });
    }
    
    // For video streaming
    if (media.type === 'video') {
      const stat = fs.statSync(media.filepath);
      const fileSize = stat.size;
      const range = req.headers.range;
      
      if (range) {
        const parts = range.replace(/bytes=/, "").split("-");
        const start = parseInt(parts[0], 10);
        const end = parts[1] 
          ? parseInt(parts[1], 10)
          : fileSize-1;
        
        const chunksize = (end-start)+1;
        const file = fs.createReadStream(media.filepath, {start, end});
        const head = {
          'Content-Range': `bytes ${start}-${end}/${fileSize}`,
          'Accept-Ranges': 'bytes',
          'Content-Length': chunksize,
          'Content-Type': media.mimeType,
        };
        
        res.writeHead(206, head);
        file.pipe(res);
      } else {
        const head = {
          'Content-Length': fileSize,
          'Content-Type': media.mimeType,
        };
        
        res.writeHead(200, head);
        fs.createReadStream(media.filepath).pipe(res);
      }
    }
    // For images or direct download
    else {
      res.sendFile(path.resolve(media.filepath));
    }
  } catch (err) {
    logger.error(`Error in streamMedia: ${err.message}`);
    next(err);
  }
};
