import axios from 'axios';

const API_URL = 'http://localhost:5000';

export default {
  connectDrone() {
    return axios.get(`${API_URL}/drone/connect`);
  },
  
  disconnectDrone() {
    return axios.get(`${API_URL}/drone/disconnect`);
  },
  
  getDroneData() {
    return axios.get(`${API_URL}/status/drone_data`);
  },
  
  // Commandes de base
  takeoff() {
    return axios.get(`${API_URL}/drone/takeoff`);
  },
  
  land() {
    return axios.get(`${API_URL}/drone/land`);
  },
  
  // Commandes de mouvement
  moveUp() {
    return axios.get(`${API_URL}/drone/move/up`);
  },
  
  moveDown() {
    return axios.get(`${API_URL}/drone/move/down`);
  },
  
  moveLeft() {
    return axios.get(`${API_URL}/drone/move/left`);
  },
  
  moveRight() {
    return axios.get(`${API_URL}/drone/move/right`);
  },
  
  moveForward() {
    return axios.get(`${API_URL}/drone/move/forward`);
  },
  
  moveBackward() {
    return axios.get(`${API_URL}/drone/move/backward`);
  },
  
  rotateLeft() {
    return axios.get(`${API_URL}/drone/rotate/left`);
  },
  
  rotateRight() {
    return axios.get(`${API_URL}/drone/rotate/right`);
  },
  
  // Commandes de flip
  flipForward() {
    return axios.get(`${API_URL}/drone/flip/forward`);
  },
  
  flipBackward() {
    return axios.get(`${API_URL}/drone/flip/backward`);
  },
  
  flipLeft() {
    return axios.get(`${API_URL}/drone/flip/left`);
  },
  
  flipRight() {
    return axios.get(`${API_URL}/drone/flip/right`);
  },

  hover() {
    return axios.get(`${API_URL}/drone/hover`);
  },
  
  // Commandes spéciales
  emergencyStop() {
    return axios.get(`${API_URL}/drone/emergency`);
  },
  
  speechRecognition() {
    return axios.get(`${API_URL}/drone/speech`);
  },
  
  quit() {
    return axios.get(`${API_URL}/drone/quit`);
  },
  
  // Flux vidéo
  getVideoUrl() {
    return `${API_URL}/video/feed?timestamp=${new Date().getTime()}`;
  }
};