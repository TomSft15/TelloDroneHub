<template>
  <div class="control-page">
    <div class="page-header">
      <h1><i class="fas fa-hand-paper"></i> Contrôle Gestuel</h1>
      <p class="page-description">
        Contrôlez votre drone avec des mouvements de mains captés par votre caméra.
        Activez la reconnaissance de gestes et utilisez les gestes pré-définis pour piloter le drone.
      </p>
    </div>

    <!-- Carte de contrôle de la reconnaissance de gestes -->
    <div class="control-card">
      <div class="card-header">
        <h2><i class="fas fa-sign-language"></i> Reconnaissance de Gestes</h2>
        <div class="status-indicator" :class="{ 'is-active': isGestureEnabled }">
          <span class="status-dot"></span>
          <span class="status-text">{{ isGestureEnabled ? 'Activée' : 'Désactivée' }}</span>
        </div>
      </div>
      <div class="card-content">
        <div class="gesture-controls">
          <div class="control-actions">
            <button 
              @click="toggleGestureRecognition" 
              :disabled="!isDroneConnected || isLoading"
              :class="{ 'btn-active': isGestureEnabled, 'btn-inactive': !isGestureEnabled }"
              class="btn-large">
              <i :class="isLoading ? 'fas fa-spinner fa-spin' : (isGestureEnabled ? 'fas fa-hand-paper' : 'fas fa-play')"></i>
              {{ isGestureEnabled ? 'Désactiver la reconnaissance' : 'Activer la reconnaissance' }}
            </button>
            
            <div class="cooldown-control">
              <label for="cooldown">Temps entre les gestes (secondes)</label>
              <div class="cooldown-slider">
                <input 
                  type="range" 
                  id="cooldown" 
                  v-model="cooldownTime" 
                  min="0.5" 
                  max="10" 
                  step="0.5" 
                  :disabled="!isDroneConnected || !isGestureEnabled">
                <span class="cooldown-value">{{ cooldownTime }}s</span>
              </div>
              <button 
                @click="updateCooldown" 
                class="btn-small"
                :disabled="!isDroneConnected || !isGestureEnabled || isUpdatingCooldown">
                <i :class="isUpdatingCooldown ? 'fas fa-spinner fa-spin' : 'fas fa-save'"></i> 
                Appliquer
              </button>
            </div>
          </div>
          
          <div v-if="isGestureEnabled && gestureStatus" class="status-info">
            <div class="status-item">
              <div class="status-label">Temps restant avant le prochain geste</div>
              <div class="status-value">{{ formattedTimeUntilNext }}</div>
            </div>
          </div>
          
          <div v-if="!isDroneConnected" class="warning-message">
            <i class="fas fa-exclamation-triangle"></i>
            <p>Connectez-vous à un drone pour utiliser la reconnaissance de gestes</p>
            <router-link to="/connect" class="btn-connect">
              <i class="fas fa-plug"></i> Connecter un drone
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Guide des gestes -->
    <div class="control-card">
      <div class="card-header">
        <h2><i class="fas fa-book"></i> Guide des Gestes</h2>
      </div>
      <div class="card-content">
        <div class="gestures-guide">
          <div class="gesture-row">
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-hand-paper"></i>
              </div>
              <div class="gesture-description">
                <h3>Main ouverte (5 doigts)</h3>
                <p>Décollage</p>
              </div>
            </div>
            
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-fist-raised"></i>
              </div>
              <div class="gesture-description">
                <h3>Poing fermé</h3>
                <p>Atterrissage</p>
              </div>
            </div>
            
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-thumbs-up"></i>
              </div>
              <div class="gesture-description">
                <h3>Pouce en haut</h3>
                <p>Monter</p>
              </div>
            </div>
            
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-thumbs-down"></i>
              </div>
              <div class="gesture-description">
                <h3>Pouce en bas</h3>
                <p>Descendre</p>
              </div>
            </div>
          </div>
          
          <div class="gesture-row">
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-hand-peace"></i>
              </div>
              <div class="gesture-description">
                <h3>Signe V (index et majeur)</h3>
                <p>Avancer</p>
              </div>
            </div>
            
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-check-circle"></i>
              </div>
              <div class="gesture-description">
                <h3>Signe OK</h3>
                <p>Reculer</p>
              </div>
            </div>
            
            <div class="gesture-item">
              <div class="gesture-image rotation-left">
                <i class="fas fa-hand-point-up"></i>
              </div>
              <div class="gesture-description">
                <h3>Index pointé à gauche</h3>
                <p>Se déplacer à gauche</p>
              </div>
            </div>
            
            <div class="gesture-item">
              <div class="gesture-image rotation-right">
                <i class="fas fa-hand-point-up"></i>
              </div>
              <div class="gesture-description">
                <h3>Index pointé à droite</h3>
                <p>Se déplacer à droite</p>
              </div>
            </div>
          </div>
          
          <div class="gesture-row">
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-hand-point-up"></i>
              </div>
              <div class="gesture-description">
                <h3>Index pointé vers le haut</h3>
                <p>Vol stationnaire</p>
              </div>
            </div>
            
            <div class="gesture-item">
              <div class="gesture-image">
                <i class="fas fa-sign-language"></i>
              </div>
              <div class="gesture-description">
                <h3>Signe rock (cornes)</h3>
                <p>Looping avant</p>
              </div>
            </div>
          </div>
          
          <div class="gesture-tips">
            <h3><i class="fas fa-lightbulb"></i> Conseils pour la reconnaissance</h3>
            <ul>
              <li>Assurez-vous d'être dans un endroit bien éclairé</li>
              <li>Gardez vos mains à une distance d'environ 50 cm de la caméra</li>
              <li>Faites des gestes clairs et précis</li>
              <li>Attendez le temps de refroidissement entre chaque commande</li>
              <li>En cas d'urgence, utilisez le poing fermé pour atterrir</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Composant principal de contrôle -->
    <ControlMode mode="Gesture" />
  </div>
</template>

<script>
import ControlMode from '../ControlMode.vue';
import gestureService from '../../services/gestureService';
import axios from 'axios';

export default {
  components: {
    ControlMode,
  },
  data() {
    return {
      isGestureEnabled: false,
      isDroneConnected: false,
      isLoading: false,
      isUpdatingCooldown: false,
      cooldownTime: 3.0,
      gestureStatus: null,
      statusInterval: null
    };
  },
  computed: {
    formattedTimeUntilNext() {
      if (!this.gestureStatus) return '0.0s';
      
      const time = this.gestureStatus.time_until_next.toFixed(1);
      return `${time}s`;
    }
  },
  methods: {
    async toggleGestureRecognition() {
      this.isLoading = true;
      
      try {
        if (this.isGestureEnabled) {
          // Désactiver la reconnaissance
          const response = await gestureService.stopGestureRecognition();
          if (response.data.success) {
            this.isGestureEnabled = false;
            this.$notify && this.$notify.info('Reconnaissance de gestes désactivée');
            this.stopStatusPolling();
          } else {
            this.$notify && this.$notify.error(`Erreur: ${response.data.message}`);
          }
        } else {
          // Activer la reconnaissance
          const response = await gestureService.startGestureRecognition();
          if (response.data.success) {
            this.isGestureEnabled = true;
            this.$notify && this.$notify.success('Reconnaissance de gestes activée');
            this.startStatusPolling();
          } else {
            this.$notify && this.$notify.error(`Erreur: ${response.data.message}`);
          }
        }
      } catch (error) {
        console.error('Erreur lors de la modification de l\'état de la reconnaissance:', error);
        this.$notify && this.$notify.error('Erreur de communication avec le serveur');
      } finally {
        this.isLoading = false;
      }
    },
    
    async updateCooldown() {
      this.isUpdatingCooldown = true;
      
      try {
        const response = await gestureService.setCooldown(this.cooldownTime);
        if (response.data.success) {
          this.$notify && this.$notify.success(`Temps de refroidissement mis à jour: ${this.cooldownTime}s`);
        } else {
          this.$notify && this.$notify.error(`Erreur: ${response.data.message}`);
        }
      } catch (error) {
        console.error('Erreur lors de la mise à jour du temps de refroidissement:', error);
        this.$notify && this.$notify.error('Erreur de communication avec le serveur');
      } finally {
        this.isUpdatingCooldown = false;
      }
    },
    
    async checkGestureStatus() {
      try {
        const response = await gestureService.getGestureStatus();
        this.gestureStatus = response.data;
        this.isGestureEnabled = response.data.is_running;
        this.cooldownTime = response.data.cooldown;
      } catch (error) {
        console.error('Erreur lors de la récupération du statut de la reconnaissance:', error);
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
        this.checkGestureStatus();
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
    await this.checkGestureStatus();
    
    if (this.isGestureEnabled) {
      this.startStatusPolling();
    }
  },
  beforeUnmount() {
    this.stopStatusPolling();
  }
};
</script>

<style scoped>
.control-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--light-gray);
  padding-bottom: 1.5rem;
}

.page-header h1 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-color);
  margin-bottom: 0.75rem;
}

.page-header h1 i {
  color: var(--accent-color);
}

.page-description {
  color: var(--dark-gray);
  font-size: 1.1rem;
  max-width: 700px;
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

.card-header h2 {
  margin: 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-header h2 i {
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

.gesture-controls {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.control-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: flex-start;
}

.btn-large {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.2rem;
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

.cooldown-control {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 300px;
}

.cooldown-control label {
  font-weight: 500;
  color: var(--text-color);
}

.cooldown-slider {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cooldown-slider input {
  flex: 1;
}

.cooldown-value {
  font-weight: 600;
  color: var(--primary-color);
  min-width: 40px;
}

.btn-small {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  font-size: 0.9rem;
  background-color: var(--primary-color);
  color: white;
  align-self: flex-start;
}

.btn-small:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.status-info {
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  padding: 1rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-label {
  font-weight: 500;
  color: var(--text-color);
}

.status-value {
  font-weight: 600;
  color: var(--primary-color);
  font-size: 1.1rem;
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

/* Guide des gestes */
.gestures-guide {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.gesture-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.gesture-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  transition: transform 0.2s;
}

.gesture-item:hover {
  transform: translateY(-5px);
}

.gesture-image {
  width: 80px;
  height: 80px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.rotation-left {
  transform: rotate(-90deg);
}

.rotation-right {
  transform: rotate(90deg);
}

.gesture-description {
  text-align: center;
}

.gesture-description h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: var(--text-color);
}

.gesture-description p {
  margin: 0;
  color: var(--primary-color);
  font-weight: 500;
}

.gesture-tips {
  background-color: #e8f4fd;
  border-radius: var(--border-radius-md);
  padding: 1.5rem;
  margin-top: 1rem;
}

.gesture-tips h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary-color);
  font-size: 1.1rem;
  margin-top: 0;
  margin-bottom: 1rem;
}

.gesture-tips ul {
  margin: 0;
  padding-left: 1.5rem;
}

.gesture-tips li {
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.gesture-tips li:last-child {
  margin-bottom: 0;
}

/* Responsive styles */
@media (max-width: 768px) {
  .control-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .btn-large {
    width: 100%;
  }
  
  .cooldown-control {
    width: 100%;
  }
  
  .gesture-row {
    grid-template-columns: 1fr;
  }
}
</style>