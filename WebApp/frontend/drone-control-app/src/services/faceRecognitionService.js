// src/services/faceRecognitionService.js
import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000';

/**
 * Service de gestion de la reconnaissance faciale
 */
class FaceRecognitionService {
  /**
   * Ajoute une nouvelle personne à la base de données de reconnaissance
   * @param {File} imageFile - Le fichier image contenant le visage
   * @param {Object} personData - Les informations sur la personne
   * @returns {Promise} La réponse de l'API
   */
  async addPerson(imageFile, personData) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      formData.append('name', personData.name);
      formData.append('relation', personData.relation);
      
      // Dans un environnement réel, nous ferions un appel API ici
      // En mode simulation, nous allons stocker dans localStorage
      
      // Simuler un délai réseau
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Convertir l'image en base64 pour stockage
      const base64Image = await this._fileToBase64(imageFile);
      
      // Récupérer les personnes existantes
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      
      // Créer une nouvelle personne
      const newPerson = {
        id: Date.now(),
        name: personData.name,
        relation: personData.relation,
        image: base64Image,
        dateAdded: new Date().toISOString()
      };
      
      // Ajouter à la liste
      storedPeople.unshift(newPerson);
      localStorage.setItem('recognitionPeople', JSON.stringify(storedPeople));
      
      return {
        success: true,
        data: newPerson
      };
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
      // Dans un environnement réel, nous ferions un appel API ici
      // En mode simulation, nous allons récupérer depuis localStorage
      
      // Simuler un délai réseau
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      
      return {
        success: true,
        data: storedPeople
      };
    } catch (error) {
      console.error('Erreur lors de la récupération des personnes:', error);
      throw error;
    }
  }
  
  /**
   * Met à jour les informations d'une personne
   * @param {string} personId - L'identifiant de la personne
   * @param {Object} personData - Les nouvelles informations
   * @returns {Promise} La réponse de l'API
   */
  async updatePerson(personId, personData) {
    try {
      // Dans un environnement réel, nous ferions un appel API ici
      // En mode simulation, nous allons mettre à jour le localStorage
      
      // Simuler un délai réseau
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      const index = storedPeople.findIndex(p => p.id === personId);
      
      if (index !== -1) {
        // Mettre à jour les propriétés
        storedPeople[index] = {
          ...storedPeople[index],
          ...personData
        };
        
        localStorage.setItem('recognitionPeople', JSON.stringify(storedPeople));
        
        return {
          success: true,
          data: storedPeople[index]
        };
      } else {
        throw new Error('Personne non trouvée');
      }
    } catch (error) {
      console.error('Erreur lors de la mise à jour d\'une personne:', error);
      throw error;
    }
  }
  
  /**
   * Supprime une personne de la base de données
   * @param {string} personId - L'identifiant de la personne à supprimer
   * @returns {Promise} La réponse de l'API
   */
  async deletePerson(personId) {
    try {
      // Dans un environnement réel, nous ferions un appel API ici
      // En mode simulation, nous allons supprimer du localStorage
      
      // Simuler un délai réseau
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      const newList = storedPeople.filter(p => p.id !== personId);
      
      localStorage.setItem('recognitionPeople', JSON.stringify(newList));
      
      return {
        success: true
      };
    } catch (error) {
      console.error('Erreur lors de la suppression d\'une personne:', error);
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
      // Dans un environnement réel, nous ferions un appel API ici
      // En mode simulation, nous allons enregistrer dans localStorage
      
      // Simuler un délai réseau
      await new Promise(resolve => setTimeout(resolve, 300));
      
      localStorage.setItem('recognitionSettings', JSON.stringify(settings));
      
      return {
        success: true,
        data: settings
      };
    } catch (error) {
      console.error('Erreur lors de l\'enregistrement des paramètres:', error);
      throw error;
    }
  }
  
  /**
   * Récupère les paramètres de reconnaissance
   * @returns {Promise} Les paramètres
   */
  async getSettings() {
    try {
      // Dans un environnement réel, nous ferions un appel API ici
      // En mode simulation, nous allons récupérer depuis localStorage
      
      // Simuler un délai réseau
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const storedSettings = JSON.parse(localStorage.getItem('recognitionSettings') || 'null');
      
      // Paramètres par défaut si aucun n'est enregistré
      const defaultSettings = {
        enabled: true,
        autoTracking: false,
        confidenceThreshold: 75,
        soundNotification: true
      };
      
      return {
        success: true,
        data: storedSettings || defaultSettings
      };
    } catch (error) {
      console.error('Erreur lors de la récupération des paramètres:', error);
      throw error;
    }
  }
  
  /**
   * Convertit un fichier en base64
   * @param {File} file - Le fichier à convertir
   * @returns {Promise<string>} La chaîne base64
   * @private
   */
  _fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }
}

export default new FaceRecognitionService();