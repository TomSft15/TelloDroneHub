import axios from 'axios';

const API_URL = 'http://localhost:5000';

export default {
  /**
   * Démarre la reconnaissance des gestes
   * @returns {Promise<Object>} Réponse de l'API
   */
  startGestureRecognition() {
    return axios.get(`${API_URL}/gesture/start`);
  },
  
  /**
   * Arrête la reconnaissance des gestes
   * @returns {Promise<Object>} Réponse de l'API
   */
  stopGestureRecognition() {
    return axios.get(`${API_URL}/gesture/stop`);
  },
  
  /**
   * Obtient l'état actuel de la reconnaissance des gestes
   * @returns {Promise<Object>} État de la reconnaissance des gestes
   */
  getGestureStatus() {
    return axios.get(`${API_URL}/gesture/status`);
  },
  
  /**
   * Définit le temps de refroidissement entre les gestes
   * @param {number} seconds - Temps en secondes (entre 0.5 et 10)
   * @returns {Promise<Object>} Réponse de l'API
   */
  setCooldown(seconds) {
    return axios.post(`${API_URL}/gesture/cooldown`, { seconds });
  }
};