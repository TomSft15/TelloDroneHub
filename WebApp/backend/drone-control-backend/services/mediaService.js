const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);
const fs = require('fs');
const path = require('path');
const logger = require('../utils/logger');

/**
 * Get media information (resolution, duration) using ffprobe
 * @param {String} filepath 
 * @param {String} type 
 * @returns {Promise<Object>}
 */
exports.getMediaInfo = async (filepath, type) => {
  try {
    // Check if ffprobe is installed
    try {
      await execPromise('ffprobe -version');
    } catch (err) {
      logger.warn('ffprobe not installed, skipping media info extraction');
      return null;
    }
    
    if (!fs.existsSync(filepath)) {
      throw new Error('File does not exist');
    }
    
    // Run ffprobe with output formatted as JSON
    const cmd = `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of json "${filepath}"`;
    const { stdout } = await execPromise(cmd);
    const info = JSON.parse(stdout);
    
    const stream = info.streams && info.streams[0];
    if (!stream) {
      throw new Error('No video stream found');
    }
    
    return {
      resolution: {
        width: parseInt(stream.width) || 0,
        height: parseInt(stream.height) || 0,
      },
      duration: parseFloat(stream.duration) || 0,
    };
  } catch (error) {
    logger.error(`Error getting media info: ${error.message}`);
    return {
      resolution: { width: 0, height: 0 },
      duration: 0,
    };
  }
};

/**
 * Generate a thumbnail for video or image
 * @param {String} filepath 
 * @param {String} type 
 * @returns {Promise<String>} thumbnail filepath
 */
exports.generateThumbnail = async (filepath, type) => {
  try {
    // Check if ffmpeg is installed
    try {
      await execPromise('ffmpeg -version');
    } catch (err) {
      logger.warn('ffmpeg not installed, skipping thumbnail generation');
      return null;
    }
    
    if (!fs.existsSync(filepath)) {
      throw new Error('File does not exist');
    }
    
    const fileName = path.basename(filepath, path.extname(filepath));
    const thumbnailDir = path.join(path.dirname(filepath), 'thumbnails');
    const thumbnailPath = path.join(thumbnailDir, `${fileName}_thumb.jpg`);
    
    // Create thumbnails directory if it doesn't exist
    if (!fs.existsSync(thumbnailDir)) {
      fs.mkdirSync(thumbnailDir, { recursive: true });
    }
    
    let cmd;
    if (type === 'video') {
      // Extract thumbnail from middle of video
      cmd = `ffmpeg -i "${filepath}" -ss 00:00:01.000 -vframes 1 -vf scale=320:-1 "${thumbnailPath}"`;
    } else {
      // Resize image for thumbnail
      cmd = `ffmpeg -i "${filepath}" -vf scale=320:-1 "${thumbnailPath}"`;
    }
    
    await execPromise(cmd);
    return thumbnailPath;
  } catch (error) {
    logger.error(`Error generating thumbnail: ${error.message}`);
    return null;
  }
};
