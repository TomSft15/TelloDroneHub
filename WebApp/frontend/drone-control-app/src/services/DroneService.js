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
  
  takeoff() {
    return axios.get(`${API_URL}/drone/takeoff`);
  },
  
  land() {
    return axios.get(`${API_URL}/drone/land`);
  },
  
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
  
  emergencyStop() {
    return axios.get(`${API_URL}/drone/emergency`);
  },
  
  speechRecognition() {
    return axios.get(`${API_URL}/drone/speech`);
  },
  
  quit() {
    return axios.get(`${API_URL}/drone/quit`);
  },
  
  // Méthode pour le hover
  hover() {
    return axios.get(`${API_URL}/drone/hover`);
  },
  
  // Méthode pour la caméra
  capturePhoto() {
    return axios.get(`${API_URL}/drone/capture_photo`);
  },
  
  startRecording() {
    return axios.get(`${API_URL}/drone/start_recording`);
  },
  
  stopRecording() {
    return axios.get(`${API_URL}/drone/stop_recording`);
  },
  
  // Autres fonctionnalités
  increaseAltitude() {
    return axios.get(`${API_URL}/drone/increase_altitude`);
  },
  
  decreaseAltitude() {
    return axios.get(`${API_URL}/drone/decrease_altitude`);
  },
  
  increaseSpeed() {
    return axios.get(`${API_URL}/drone/increase_speed`);
  },
  
  decreaseSpeed() {
    return axios.get(`${API_URL}/drone/decrease_speed`);
  },
  
  returnToHome() {
    return axios.get(`${API_URL}/drone/return_home`);
  },
  
  getVideoUrl() {
    return `${API_URL}/video/feed?timestamp=${new Date().getTime()}`;
  }
};