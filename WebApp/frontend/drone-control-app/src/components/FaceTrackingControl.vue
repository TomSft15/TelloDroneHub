<template>
    <div class="face-tracking-control">
      <div class="control-card">
        <div class="card-header">
          <h3><i class="fas fa-eye"></i> Suivi Facial Automatique</h3>
          <div class="status-indicator" :class="{ 'is-active': isTracking }">
            <span class="status-dot"></span>
            <span class="status-text">{{ isTracking ? 'Activé' : 'Désactivé' }}</span>
          </div>
        </div>
        
        <div class="card-content">
          <div class="tracking-controls">
            <div class="control-description">
              <p>Le suivi facial automatique permet au drone de détecter et suivre un visage en effectuant des rotations et des ajustements de hauteur. 
                 Le drone pivote et se déplace verticalement pour garder le visage centré dans le champ de vision.</p>
            </div>
            
            <div class="control-actions">
              <button 
                @click="toggleFaceTracking" 
                :disabled="!isDroneConnected || isLoading"
                :class="{ 'btn-active': isTracking, 'btn-inactive': !isTracking }"
                class="btn-large">
                <i :class="isLoading ? 'fas fa-spinner fa-spin' : (isTracking ? 'fas fa-eye-slash' : 'fas fa-eye')"></i>
                {{ isTracking ? 'Désactiver le suivi' : 'Activer le suivi' }}
              </button>
            </div>
            
            <div v-if="isTracking" class="tracking-status">
              <div class="status-item">
                <div class="status-label">Statut de détection:</div>
                <div class="status-value">
                  <span class="detection-indicator" :class="{ 'face-detected': faceDetected }">
                    {{ faceDetected ? 'Visage détecté' : 'Aucun visage détecté' }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-if="!isDroneConnected" class="warning-message">
              <i class="fas fa-exclamation-triangle"></i>
              <p>Connectez-vous à un drone pour utiliser le suivi facial</p>
              <router-link to="/connect" class="btn-connect">
                <i class="fas fa-plug"></i> Connecter un drone
              </router-link>
            </div>
          </div>
          
          <div v-if="showAdvancedSettings" class="advanced-settings">
            <h4>Paramètres avancés</h4>
            
            <div class="settings-grid">
              <div class="setting-item">
                <label for="detection-frequency">Fréquence de détection (secondes)</label>
                <div class="setting-control">
                  <input 
                    type="range" 
                    id="detection-frequency" 
                    v-model.number="settings.detection_frequency" 
                    min="0.1" 
                    max="1" 
                    step="0.1" 
                    :disabled="!isDroneConnected || isTracking">
                  <span class="setting-value">{{ settings.detection_frequency.toFixed(1) }}s</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="rotation-speed">Vitesse de rotation horizontale</label>
                <div class="setting-control">
                  <input 
                    type="range" 
                    id="rotation-speed" 
                    v-model.number="settings.rotation_speed" 
                    min="10" 
                    max="50" 
                    step="5" 
                    :disabled="!isDroneConnected || isTracking">
                  <span class="setting-value">{{ settings.rotation_speed }}</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="vertical-speed">Vitesse de déplacement vertical</label>
                <div class="setting-control">
                  <input 
                    type="range" 
                    id="vertical-speed" 
                    v-model.number="settings.vertical_speed" 
                    min="10" 
                    max="50" 
                    step="5" 
                    :disabled="!isDroneConnected || isTracking">
                  <span class="setting-value">{{ settings.vertical_speed }}</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="deadzone-x">Zone morte horizontale (pixels)</label>
                <div class="setting-control">
                  <input 
                    type="range" 
                    id="deadzone-x" 
                    v-model.number="settings.deadzone_x" 
                    min="10" 
                    max="100" 
                    step="10" 
                    :disabled="!isDroneConnected || isTracking">
                  <span class="setting-value">{{ settings.deadzone_x }}px</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="deadzone-y">Zone morte verticale (pixels)</label>
                <div class="setting-control">
                  <input 
                    type="range" 
                    id="deadzone-y" 
                    v-model.number="settings.deadzone_y" 
                    min="10" 
                    max="100" 
                    step="10" 
                    :disabled="!isDroneConnected || isTracking">
                  <span class="setting-value">{{ settings.deadzone_y }}px</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="face-size">Taille minimale du visage</label>
                <div class="setting-control">
                  <input 
                    type="range" 
                    id="face-size" 
                    v-model.number="settings.face_size_min" 
                    min="30" 
                    max="100" 
                    step="10" 
                    :disabled="!isDroneConnected || isTracking">
                  <span class="setting-value">{{ settings.face_size_min }}px</span>
                </div>
              </div>
            </div>
            
            <div class="settings-actions">
              <button 
                @click="saveSettings" 
                class="btn-save" 
                :disabled="!isDroneConnected || isTracking || isSaving">
                <i :class="isSaving ? 'fas fa-spinner fa-spin' : 'fas fa-save'"></i> 
                Enregistrer les paramètres
              </button>
              
              <button 
                @click="resetSettings" 
                class="btn-reset" 
                :disabled="!isDroneConnected || isTracking">
                <i class="fas fa-undo"></i> 
                Réinitialiser
              </button>
            </div>
          </div>
          
          <div class="toggle-advanced">
            <button @click="showAdvancedSettings = !showAdvancedSettings" class="btn-text">
              <i :class="showAdvancedSettings ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
              {{ showAdvancedSettings ? 'Masquer les paramètres avancés' : 'Afficher les paramètres avancés' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import faceTrackingService from '../services/faceTrackingService';
  import axios from 'axios';
  
  export default {
    name: 'FaceTrackingControl',
    data() {
      return {
        isTracking: false,
        isDroneConnected: false,
        isLoading: false,
        isSaving: false,
        faceDetected: false,
        showAdvancedSettings: false,
        settings: {
          detection_frequency: 0.2,
          rotation_speed: 20,
          vertical_speed: 20,
          deadzone_x: 50,
          deadzone_y: 40,
          face_size_min: 50
        },
        defaultSettings: {
          detection_frequency: 0.2,
          rotation_speed: 20,
          vertical_speed: 20,
          deadzone_x: 50,
          deadzone_y: 40,
          face_size_min: 50
        },
        statusInterval: null
      };
    },
    methods: {
      async toggleFaceTracking() {
        if (!this.isDroneConnected) return;
        
        this.isLoading = true;
        
        try {
          if (this.isTracking) {
            // Désactiver le suivi
            const response = await faceTrackingService.stopFaceTracking();
            if (response.data.success) {
              this.isTracking = false;
              this.$notify && this.$notify.info('Suivi facial désactivé');
              this.stopStatusPolling();
            } else {
              this.$notify && this.$notify.error(`Erreur: ${response.data.message}`);
            }
          } else {
            // Activer le suivi
            const response = await faceTrackingService.startFaceTracking();
            if (response.data.success) {
              this.isTracking = true;
              this.$notify && this.$notify.success('Suivi facial activé');
              this.startStatusPolling();
            } else {
              this.$notify && this.$notify.error(`Erreur: ${response.data.message}`);
            }
          }
        } catch (error) {
          console.error('Erreur lors de la modification de l\'état du suivi:', error);
          this.$notify && this.$notify.error('Erreur de communication avec le serveur');
        } finally {
          this.isLoading = false;
        }
      },
      
      async saveSettings() {
        if (!this.isDroneConnected || this.isTracking) return;
        
        this.isSaving = true;
        
        try {
          const response = await faceTrackingService.updateSettings(this.settings);
          if (response.data.success) {
            this.$notify && this.$notify.success('Paramètres enregistrés');
          } else {
            this.$notify && this.$notify.error(`Erreur: ${response.data.message}`);
          }
        } catch (error) {
          console.error('Erreur lors de la mise à jour des paramètres:', error);
          this.$notify && this.$notify.error('Erreur de communication avec le serveur');
        } finally {
          this.isSaving = false;
        }
      },
      
      resetSettings() {
        this.settings = { ...this.defaultSettings };
        this.$notify && this.$notify.info('Paramètres réinitialisés');
      },
      
      async checkFaceTrackingStatus() {
        try {
          const response = await faceTrackingService.getFaceTrackingStatus();
          const status = response.data;
          
          this.isTracking = status.is_tracking;
          this.faceDetected = status.face_detected;
          
          // Mise à jour des paramètres si nécessaire
          if (!this.isTracking) {
            this.settings = { ...status.settings };
          }
          
          // Si le suivi est actif, démarrer le polling
          if (this.isTracking && !this.statusInterval) {
            this.startStatusPolling();
          } else if (!this.isTracking && this.statusInterval) {
            this.stopStatusPolling();
          }
        } catch (error) {
          console.error('Erreur lors de la récupération du statut:', error);
        }
      },
      
      async checkDroneConnection() {
        try {
          const response = await axios.get('http://localhost:5000/status');
          this.isDroneConnected = response.data.connected;
        } catch (error) {
          console.error('Erreur lors de la vérification de la connexion du drone:', error);
          this.isDroneConnected = false;
        }
      },
      
      startStatusPolling() {
        // Arrêter l'intervalle précédent si existant
        this.stopStatusPolling();
        
        // Démarrer un nouvel intervalle
        this.statusInterval = setInterval(() => {
          this.checkFaceTrackingStatus();
        }, 500); // Mise à jour toutes les 500ms
      },
      
      stopStatusPolling() {
        if (this.statusInterval) {
          clearInterval(this.statusInterval);
          this.statusInterval = null;
        }
      }
    },
    
    async mounted() {
      await this.checkDroneConnection();
      await this.checkFaceTrackingStatus();
      
      // Vérifier la connexion du drone et le statut du suivi toutes les 3 secondes
      setInterval(() => {
        this.checkDroneConnection();
      }, 3000);
    },
    
    beforeUnmount() {
      this.stopStatusPolling();
    }
  };
  </script>
  
  <style scoped>
  .face-tracking-control {
    max-width: 1000px;
    margin: 0 auto;
  }
  
  .control-card {
    background-color: white;
    border-radius: var(--border-radius-md);
    box-shadow: var(--card-shadow);
    margin-bottom: 2rem;
    overflow: hidden;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 1.5rem;
    background-color: var(--light-gray);
  }
  
  .card-header h3 {
    margin: 0;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .card-header h3 i {
    color: var(--primary-color);
  }
  
  .card-content {
    padding: 1.5rem;
  }
  
  .status-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    font-size: 0.9rem;
    background-color: var(--light-gray);
    color: var(--dark-gray);
  }
  
  .status-indicator.is-active {
    background-color: var(--success-color);
    color: white;
  }
  
  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--dark-gray);
  }
  
  .status-indicator.is-active .status-dot {
    background-color: white;
  }
  
  .tracking-controls {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .control-description p {
    color: var(--dark-gray);
    line-height: 1.6;
  }
  
  .control-actions {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
  }
  
  .btn-large {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.8rem 1.5rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    font-size: 1rem;
    min-width: 250px;
    justify-content: center;
  }
  
  .btn-active {
    background-color: var(--success-color);
    color: white;
  }
  
  .btn-inactive {
    background-color: var(--primary-color);
    color: white;
  }
  
  .btn-large:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .tracking-status {
    background-color: var(--light-gray);
    border-radius: var(--border-radius-md);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .status-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .status-label {
    font-weight: 500;
    color: var(--text-color);
  }
  
  .detection-indicator {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    background-color: #f8d7da;
    color: #721c24;
    font-size: 0.9rem;
    font-weight: 500;
  }
  
  .detection-indicator.face-detected {
    background-color: #d4edda;
    color: #155724;
  }
  
  .warning-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1.5rem;
    border-radius: var(--border-radius-sm);
    color: #856404;
  }
  
  .warning-message i {
    font-size: 2rem;
    color: #ffc107;
  }
  
  .btn-connect {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
  }
  
  /* Advanced Settings */
  .advanced-settings {
    margin-top: 2rem;
    background-color: var(--light-gray);
    border-radius: var(--border-radius-md);
    padding: 1.5rem;
  }
  
  .advanced-settings h4 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: var(--text-color);
    font-size: 1.1rem;
    border-bottom: 1px solid var(--medium-gray);
    padding-bottom: 0.5rem;
  }
  
  .settings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .setting-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .setting-item label {
    font-weight: 500;
    color: var(--text-color);
  }
  
  .setting-control {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .setting-control input {
    flex: 1;
  }
  
  .setting-value {
    min-width: 40px;
    font-weight: 600;
    color: var(--primary-color);
    text-align: right;
  }
  
  .settings-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
  
  .btn-save, .btn-reset {
    padding: 0.6rem 1.2rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .btn-save {
    background-color: var(--success-color);
    color: white;
  }
  
  .btn-reset {
    background-color: var(--medium-gray);
    color: var(--text-color);
  }
  
  .btn-save:disabled, .btn-reset:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .toggle-advanced {
    margin-top: 1.5rem;
    text-align: center;
  }
  
  .btn-text {
    background: none;
    border: none;
    color: var(--primary-color);
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    padding: 0.5rem 1rem;
  }
  
  .btn-text:hover {
    text-decoration: underline;
  }
  
  /* Media queries */
  @media (max-width: 768px) {
    .settings-grid {
      grid-template-columns: 1fr;
    }
    
    .settings-actions {
      flex-direction: column;
    }
    
    .btn-save, .btn-reset {
      width: 100%;
      justify-content: center;
    }
  }
  </style>