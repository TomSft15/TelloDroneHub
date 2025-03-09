import io from 'socket.io-client';

const SOCKET_URL = process.env.VUE_APP_SOCKET_URL || 'http://localhost:3000';

let socket = null;

// Initialiser la connexion socket
export const initializeSocket = () => {
  const token = localStorage.getItem('token');
  
  // Fermer la connexion précédente si elle existe
  if (socket) {
    socket.disconnect();
  }
  
  // Créer une nouvelle connexion avec le token d'authentification
  socket = io(SOCKET_URL, {
    auth: {
      token
    }
  });
  
  // Gestion des événements de base
  socket.on('connect', () => {
    console.log('Socket connected');
  });
  
  socket.on('disconnect', () => {
    console.log('Socket disconnected');
  });
  
  socket.on('error', (error) => {
    console.error('Socket error:', error);
  });
  
  return socket;
};

// Obtenir l'instance du socket
export const getSocket = () => {
  if (!socket) {
    return initializeSocket();
  }
  return socket;
};

// S'abonner aux mises à jour d'un drone
export const subscribeToDrone = (droneId, callback) => {
  const socket = getSocket();
  socket.emit('drone:subscribe', droneId);
  
  // Écouter les mises à jour de télémétrie
  socket.on('drone:telemetry', (telemetry) => {
    callback(telemetry);
  });
};

// Envoyer une commande à un drone
export const sendDroneCommand = (droneId, command, params = {}) => {
  const socket = getSocket();
  return new Promise((resolve, reject) => {
    // Écouter le résultat de la commande
    socket.once('drone:command:result', (result) => {
      resolve(result);
    });
    
    // Écouter les erreurs
    socket.once('drone:error', (error) => {
      reject(error);
    });
    
    // Envoyer la commande
    socket.emit('drone:command', { droneId, command, params });
  });
};
