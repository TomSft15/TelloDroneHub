/**
 * Format file size in human-readable format
 * @param {number} bytes 
 * @returns {string}
 */
exports.formatFileSize = (bytes) => {
    if (bytes < 1024) {
      return bytes + ' B';
    } else if (bytes < 1024 * 1024) {
      return (bytes / 1024).toFixed(2) + ' KB';
    } else if (bytes < 1024 * 1024 * 1024) {
      return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    } else {
      return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
    }
  };
  
  /**
   * Format seconds into readable duration HH:MM:SS
   * @param {number} seconds 
   * @returns {string}
   */
  exports.formatDuration = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    
    return [
      hours.toString().padStart(2, '0'),
      minutes.toString().padStart(2, '0'),
      remainingSeconds.toString().padStart(2, '0')
    ].join(':');
  };
  
  /**
   * Parse query parameters for pagination
   * @param {Object} query 
   * @returns {Object}
   */
  exports.getPaginationOptions = (query) => {
    const page = parseInt(query.page, 10) || 1;
    const limit = parseInt(query.limit, 10) || 10;
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    
    return {
      page,
      limit,
      startIndex,
      endIndex,
      skip: startIndex
    };
  };
  