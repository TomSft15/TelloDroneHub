// src/services/faceRecognitionService.js
import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000';

/**
 * Service de gestion de la reconnaissance faciale
 */
class FaceRecognitionService {
  /**
   * Démarre la reconnaissance faciale
   * @returns {Promise} La réponse de l'API
   */
  async startFaceRecognition() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/start`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors du démarrage de la reconnaissance faciale:', error);
      throw error;
    }
  }

  /**
   * Arrête la reconnaissance faciale
   * @returns {Promise} La réponse de l'API
   */
  async stopFaceRecognition() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/stop`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de l\'arrêt de la reconnaissance faciale:', error);
      throw error;
    }
  }

  /**
   * Obtient le statut de la reconnaissance faciale
   * @returns {Promise} Le statut
   */
  async getStatus() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/status`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération du statut:', error);
      throw error;
    }
  }

  /**
   * Ajoute une nouvelle personne à la base de données de reconnaissance
   * @param {File} file - Le fichier image contenant le visage
   * @param {Object} personData - Les informations sur la personne (nom)
   * @returns {Promise} La réponse de l'API
   */
  async addPerson(file, personData) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('name', personData.name);
      
      const response = await axios.post(`${API_URL}/face_recognition/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.data.success) {
        // this.stopFaceRecognition(); // Arrêter la reconnaissance pour recharger les visages
        // this.startFaceRecognition(); // Redémarrer la reconnaissance
        return {
          success: true,
          data: {
            id: Date.now(), // ID temporaire pour l'affichage
            name: personData.name,
            relation: personData.relation || 'other',
            image: URL.createObjectURL(file), // URL temporaire pour l'affichage
            dateAdded: new Date().toISOString()
          },
          message: response.data.message
        };
      } else {
        throw new Error(response.data.message);
      }
    } catch (error) {
      console.error('Erreur lors de l\'ajout d\'une personne:', error);
      throw error;
    }
  }
  
  /**
   * Récupère la liste des personnes enregistrées
   * @returns {Promise} La liste des personnes
   */
  async getPeople() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/people`);
      
      if (response.data.success) {
        // Adapter le format de réponse pour correspondre à l'interface
        const people = response.data.people.map(person => ({
          id: person.name, // utiliser le nom comme ID
          name: person.name,
          relation: 'other', // valeur par défaut car non fournie par l'API
          image: `${API_URL}/pictures_faces/${person.name}_profile.jpg`, // construction d'un chemin probable
          dateAdded: new Date().toISOString() // valeur par défaut car non fournie par l'API
        }));
        
        return {
          success: true,
          data: people
        };
      } else {
        throw new Error('Erreur lors de la récupération des personnes');
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des personnes:', error);
      throw error;
    }
  }
  
  /**
   * Supprime une personne de la base de données
   * @param {string} personId - Le nom de la personne à supprimer
   * @returns {Promise} La réponse de l'API
   */
  async deletePerson(personId) {
    try {
      const response = await axios.delete(`${API_URL}/face_recognition/people/${personId}`);
      
      return {
        success: response.data.success,
        message: response.data.message
      };
    } catch (error) {
      console.error('Erreur lors de la suppression d\'une personne:', error);
      throw error;
    }
  }
  
  /**
   * Capture un visage depuis le flux vidéo actuel
   * @param {string} name - Nom de la personne
   * @returns {Promise} La réponse de l'API
   */
  async captureFacePhoto(name) {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/capture/${name}`);
      
      return {
        success: response.data.success,
        message: response.data.message
      };
    } catch (error) {
      console.error('Erreur lors de la capture de la photo:', error);
      throw error;
    }
  }
  
  /**
   * Obtient les détections actuelles du drone
   * @returns {Promise} Les détections
   */
  async getDroneDetections() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/drone_detections`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des détections:', error);
      throw error;
    }
  }
  
  /**
   * Obtient l'historique des détections
   * @returns {Promise} L'historique
   */
  async getDetectionHistory() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/detection_history`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'historique:', error);
      throw error;
    }
  }
  
  /**
   * Recharge les visages connus
   * @returns {Promise} La réponse de l'API
   */
  async reloadFaces() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/reload`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors du rechargement des visages:', error);
      throw error;
    }
  }
  
  /**
   * Récupère les paramètres de reconnaissance
   * @returns {Promise} Les paramètres
   */
  async getSettings() {
    try {
      const response = await axios.get(`${API_URL}/face_recognition/settings`);
      
      return {
        success: true,
        data: response.data.settings || {
          enabled: true,
          autoTracking: false,
          confidenceThreshold: 75,
          soundNotification: true
        }
      };
    } catch (error) {
      console.error('Erreur lors de la récupération des paramètres:', error);
      throw error;
    }
  }
  
  /**
   * Enregistre les paramètres de reconnaissance
   * @param {Object} settings - Les paramètres à enregistrer
   * @returns {Promise} La réponse de l'API
   */
  async saveSettings(settings) {
    try {
      const response = await axios.post(`${API_URL}/face_recognition/settings`, settings);
      
      return {
        success: response.data.success,
        message: response.data.message,
        data: settings
      };
    } catch (error) {
      console.error('Erreur lors de l\'enregistrement des paramètres:', error);
      throw error;
    }
  }
}

export default new FaceRecognitionService();