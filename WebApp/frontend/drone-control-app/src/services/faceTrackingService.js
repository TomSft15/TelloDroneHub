import axios from 'axios';

const API_URL = 'http://localhost:5000';

export default {
  /**
   * Démarre le suivi de visage
   * @returns {Promise<Object>} Réponse de l'API
   */
  startFaceTracking() {
    return axios.get(`${API_URL}/face_tracking/start`);
  },
  
  /**
   * Arrête le suivi de visage
   * @returns {Promise<Object>} Réponse de l'API
   */
  stopFaceTracking() {
    return axios.get(`${API_URL}/face_tracking/stop`);
  },
  
  /**
   * Obtient l'état actuel du suivi de visage
   * @returns {Promise<Object>} État du suivi de visage
   */
  getFaceTrackingStatus() {
    return axios.get(`${API_URL}/face_tracking/status`);
  },
  
  /**
   * Met à jour les paramètres du suivi de visage
   * @param {Object} settings - Paramètres à mettre à jour
   * @returns {Promise<Object>} Réponse de l'API
   */
  updateSettings(settings) {
    return axios.post(`${API_URL}/face_tracking/settings`, settings);
  }
};