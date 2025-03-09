/**
 * Validate a drone's serial number format
 * @param {string} serialNumber 
 * @returns {boolean}
 */
exports.isValidDroneSerial = (serialNumber) => {
    // Example: DR-12345-XYZ
    const regex = /^DR-\d{5}-[A-Z]{3}$/;
    return regex.test(serialNumber);
  };
  
  /**
   * Validate if the provided key binding is valid
   * @param {Object} keyBindings 
   * @returns {boolean}
   */
  exports.isValidKeyBindings = (keyBindings) => {
    if (!keyBindings || typeof keyBindings !== 'object') {
      return false;
    }
    
    // Define valid commands
    const validCommands = [
      'moveUp', 'moveDown', 'moveLeft', 'moveRight',
      'moveForward', 'moveBackward', 'rotateLeft', 'rotateRight',
      'takeoff', 'land', 'emergencyStop', 'hover',
      'capturePhoto', 'startRecording', 'stopRecording',
      'increaseAltitude', 'decreaseAltitude',
      'increaseSpeed', 'decreaseSpeed', 'returnToHome'
    ];
    
    // Check each command has a valid key binding
    for (const [key, command] of Object.entries(keyBindings)) {
      if (!validCommands.includes(command)) {
        return false;
      }
    }
    
    // Check for duplicate commands
    const commands = Object.values(keyBindings);
    const uniqueCommands = new Set(commands);
    return commands.length === uniqueCommands.size;
  };
  