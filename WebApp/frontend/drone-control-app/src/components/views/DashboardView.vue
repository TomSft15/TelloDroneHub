<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1><i class="fas fa-tachometer-alt"></i> Tableau de bord du drone</h1>
      <div class="connection-status" :class="{ connected: isConnected }">
        <span class="status-indicator"></span>
        <span class="status-text">{{ isConnected ? 'Connecté' : 'Déconnecté' }}</span>
        <button v-if="!isConnected" @click="connectDrone" class="btn-connect">
          Connecter au drone
        </button>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="camera-feed grid-item large">
        <div class="card-header">
          <h2>Flux vidéo en direct</h2>
          <div class="controls">
            <button class="btn-icon" @click="toggleFullscreen"><i class="fas fa-expand-alt"></i></button>
            <button class="btn-icon" @click="takePhoto"><i class="fas fa-camera"></i></button>
          </div>
        </div>
          <div class="camera-content" ref="videoContainer">
            <img v-if="isConnected" :src="videoUrl" alt="Live feed" @error="handleVideoError">
            <div v-else class="empty-camera">
              <i class="fas fa-video-slash"></i>
              <p>Flux vidéo non disponible</p>
              <button v-if="!isConnected" @click="connectDrone" class="connect-btn">
                <i class="fas fa-plug"></i> Connecter au drone
              </button>
              <button v-else @click="refreshVideo" class="refresh-btn">
                <i class="fas fa-sync-alt"></i> Rafraîchir le flux
              </button>
            </div>
            <div class="camera-overlay">
              <div class="overlay-item altitude">{{ droneData.height }}m</div>
              <div class="overlay-item speed">{{ droneData.speed }}m/s</div>
              <div v-if="isRecording" class="overlay-item recording">
                <i class="fas fa-circle text-danger"></i> REC {{ recordingTime }}
              </div>
              <div class="overlay-item battery">
                <i class="fas fa-battery-half"></i> {{ droneData.battery }}%
              </div>
            </div>
          </div>
      </div>

      <div class="drone-controls grid-item">
        <div class="card-header">
          <h2>Contrôles du drone</h2>
        </div>
        <div class="controls-grid">
          <button @click="sendCommand('takeoff')" :disabled="!isConnected" class="control-btn">
            <i class="fas fa-arrow-up"></i> Décollage
          </button>
          <button @click="sendCommand('land')" :disabled="!isConnected" class="control-btn">
            <i class="fas fa-arrow-down"></i> Atterrissage
          </button>
          <button @click="sendCommand('move/forward/30')" :disabled="!isConnected" class="control-btn">
            <i class="fas fa-arrow-circle-up"></i> Avancer
          </button>
          <button @click="sendCommand('move/back/30')" :disabled="!isConnected" class="control-btn">
            <i class="fas fa-arrow-circle-down"></i> Reculer
          </button>
          <button @click="sendCommand('move/left/30')" :disabled="!isConnected" class="control-btn">
            <i class="fas fa-arrow-circle-left"></i> Gauche
          </button>
          <button @click="sendCommand('move/right/30')" :disabled="!isConnected" class="control-btn">
            <i class="fas fa-arrow-circle-right"></i> Droite
          </button>
          <button @click="sendCommand('emergency')" :disabled="!isConnected" class="control-btn emergency">
            <i class="fas fa-exclamation-triangle"></i> Arrêt d'urgence
          </button>
        </div>
      </div>

      <div class="flight-stats grid-item">
        <div class="card-header">
          <h2>Statistiques de vol</h2>
        </div>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon"><i class="fas fa-signal"></i></div>
            <div class="stat-value">{{ droneData.signal }}%</div>
            <div class="stat-label">Signal</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon"><i class="fas fa-battery-three-quarters"></i></div>
            <div class="stat-value">{{ droneData.battery }}%</div>
            <div class="stat-label">Batterie</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon"><i class="fas fa-temperature-high"></i></div>
            <div class="stat-value">{{ droneData.temperature }}°C</div>
            <div class="stat-label">Température</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon"><i class="fas fa-clock"></i></div>
            <div class="stat-value">{{ formatTime(droneData.flight_time) }}</div>
            <div class="stat-label">Temps de vol</div>
          </div>
        </div>
      </div>

      <div class="flight-data grid-item">
        <div class="card-header">
          <h2>Données de vol</h2>
        </div>
        <div class="data-table">
          <div class="data-row">
            <div class="data-label">Altitude</div>
            <div class="data-value">{{ droneData.height }} m</div>
          </div>
          <div class="data-row">
            <div class="data-label">Vitesse</div>
            <div class="data-value">{{ droneData.speed }} m/s</div>
          </div>
          <div class="data-row">
            <div class="data-label">Distance</div>
            <div class="data-value">{{ calculateDistance() }} m</div>
          </div>
          <div class="data-row">
            <div class="data-label">Durée de vol</div>
            <div class="data-value">{{ formatTime(droneData.flight_time) }}</div>
          </div>
          <div class="data-row">
            <div class="data-label">Mode de vol</div>
            <div class="data-value">
              <span class="mode-badge">Manuel</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Conservez les autres éléments de votre grid mais adaptez-les avec les données dynamiques -->
      
      <div class="recent-photos grid-item">
        <div class="card-header">
          <h2>Photos récentes</h2>
          <button class="btn-text">Voir toutes <i class="fas fa-chevron-right"></i></button>
        </div>
        <div class="photo-grid">
          <div v-for="(image, index) in capturedImages.slice(0, 4)" :key="index" class="photo-item">
            <img :src="image.src" :alt="image.name">
          </div>
          <!-- Éléments de remplissage si moins de 4 images -->
          <div v-for="index in Math.max(0, 4 - capturedImages.length)" :key="`empty-${index}`" class="photo-item empty-photo">
            <i class="fas fa-image"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import emitter from '../../eventBus';

const API_URL = 'http://localhost:5000';

export default {
  name: 'DashboardViewPage',
  data() {
    return {
      isConnected: false,
      videoUrl: `${API_URL}/video_feed`,
      videoRefreshKey: 0,
      droneData: {
        battery: 0,
        temperature: 0,
        flight_time: 0,
        height: 0,
        speed: 0,
        signal: 0
      },
      images: [], // Images statiques chargées
      capturedImages: [], // Images capturées durant la session
      dataUpdateInterval: null,
      consecutiveErrors: 0,
      isConnected: false,
      videoUrl: `${API_URL}/video/feed`,
      videoErrorCount: 0,
      maxVideoErrors: 3,
      isRecording: false,
      recordingTime: '00:00',
      recordingInterval: null,
      recordingStartTime: 0
    }
  },
  mounted() {
    // Vérifier l'état de la connexion au chargement
    this.checkDroneStatus();
    
    // Écouter les événements avec l'émetteur
    emitter.on('drone-connected', () => {
      this.checkDroneStatus();
    });
    
    emitter.on('drone-disconnected', () => {
      this.isConnected = false;
      if (this.dataUpdateInterval) {
        clearInterval(this.dataUpdateInterval);
      }
    });
  },
  beforeDestroy() {
    // Nettoyer les écouteurs d'événements
    emitter.off('drone-connected');
    emitter.off('drone-disconnected');
    
    // Nettoyer les intervalles
    if (this.dataUpdateInterval) {
      clearInterval(this.dataUpdateInterval);
    }
  },
  methods: {
    async checkDroneStatus() {
      try {
        const response = await axios.get(`${API_URL}/status`);
        this.isConnected = response.data.connected;
        if (this.isConnected) {
          this.droneData = response.data.drone_data;
          this.startPollingData();
          this.refreshVideo();
        } else if (localStorage.getItem('droneConnected') === 'true') {
          localStorage.removeItem('droneConnected');
        }
      } catch (error) {
        console.error("Erreur lors de la vérification de l'état du drone:", error);
        this.isConnected = false;
        localStorage.removeItem('droneConnected');
      }
    },
    
    async connectDrone() {
      // Rediriger l'utilisateur vers la page de connexion
      this.$router.push('/connection');
    },
    
    handleDroneConnected(droneInfo) {
      this.isConnected = true;
      // Mise à jour initiale des données du drone
      if (droneInfo) {
        this.droneData.battery = droneInfo.battery || this.droneData.battery;
        this.droneData.temperature = droneInfo.temp || this.droneData.temperature;
        this.droneData.height = droneInfo.height || this.droneData.height;
      }
      this.startPollingData();
      this.refreshVideo();
    },
    
    handleDroneDisconnected() {
      this.isConnected = false;
      if (this.dataUpdateInterval) {
        clearInterval(this.dataUpdateInterval);
      }
    },
    
    refreshVideo() {
      // Force le rafraîchissement du flux vidéo
      this.videoUrl = `${API_URL}/video_feed?timestamp=${new Date().getTime()}`;
    },
    
    startPollingData() {
      // Arrêter l'intervalle existant si présent
      if (this.dataUpdateInterval) {
        clearInterval(this.dataUpdateInterval);
      }
      
      // Récupérer régulièrement les données du drone
      this.dataUpdateInterval = setInterval(async () => {
        try {
          const response = await axios.get(`${API_URL}/status/drone_data`);
          this.droneData = response.data;
          this.consecutiveErrors = 0; // Réinitialiser le compteur d'erreurs
        } catch (error) {
          console.error("Erreur lors de la récupération des données:", error);
          // Si erreur persistante, considérer le drone comme déconnecté
          if (this.isConnected) {
            this.consecutiveErrors += 1;
            if (this.consecutiveErrors > 3) {
              this.isConnected = false;
              clearInterval(this.dataUpdateInterval);
              localStorage.removeItem('droneConnected');
            }
          }
        }
      }, 1000);
    },
    
    async sendCommand(command) {
      try {
        const response = await axios.get(`${API_URL}/${command}`);
        if (!response.data.success) {
          alert(response.data.message);
        }
      } catch (error) {
        console.error("Erreur lors de l'envoi de la commande:", error);
        alert("Échec de l'envoi de la commande au drone");
      }
    },
    
    // Les autres méthodes restent les mêmes (handleVideoError, takePhoto, toggleFullscreen, etc.)
    handleVideoError() {
      console.warn("Erreur dans le chargement du flux vidéo, tentative de reconnexion...");
      this.refreshVideo();
    },
    
    takePhoto() {
      if (!this.isConnected) return;
      
      // Capture l'image actuelle depuis le flux vidéo
      const video = this.$refs.videoContainer.querySelector('img');
      if (video) {
        const canvas = document.createElement('canvas');
        canvas.width = video.naturalWidth || 640;
        canvas.height = video.naturalHeight || 480;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convertir en base64
        const imgData = canvas.toDataURL('image/jpeg');
        
        // Ajouter à notre collection d'images
        this.capturedImages.unshift({
          src: imgData,
          name: `capture_${new Date().toISOString().replace(/:/g, '-')}.jpg`
        });
        
        // Notification visuelle
        this.$notify && this.$notify({
          title: 'Photo capturée',
          message: 'Image ajoutée à la galerie',
          type: 'success'
        });
        
        // Télécharger l'image
        const link = document.createElement('a');
        link.href = imgData;
        link.download = `drone_capture_${new Date().toISOString().replace(/:/g, '-')}.jpg`;
        link.click();
      }
    },
    
    toggleFullscreen() {
      const videoContainer = this.$refs.videoContainer;
      if (videoContainer) {
        if (!document.fullscreenElement) {
          if (videoContainer.requestFullscreen) {
            videoContainer.requestFullscreen();
          } else if (videoContainer.mozRequestFullScreen) { /* Firefox */
            videoContainer.mozRequestFullScreen();
          } else if (videoContainer.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
            videoContainer.webkitRequestFullscreen();
          } else if (videoContainer.msRequestFullscreen) { /* IE/Edge */
            videoContainer.msRequestFullscreen();
          }
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
          } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
          }
        }
      }
    },
    
    formatTime(seconds) {
      if (!seconds) return '00:00';
      const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
      const secs = (seconds % 60).toString().padStart(2, '0');
      return `${mins}:${secs}`;
    },
    
    calculateDistance() {
      // Cette fonction peut être implémentée plus tard si le drone fournit des données GPS
      // Pour l'instant, retournons une valeur simulée basée sur la vitesse et le temps de vol
      const distance = this.droneData.speed * this.droneData.flight_time * 0.3;
      return Math.round(distance);
    },

    handleVideoError() {
      console.warn("Erreur dans le chargement du flux vidéo, tentative de reconnexion...");
      this.videoErrorCount++;
      
      // Si trop d'erreurs consécutives, considérer que la vidéo n'est pas disponible
      if (this.videoErrorCount > this.maxVideoErrors) {
        console.error("Impossible de charger le flux vidéo après plusieurs tentatives");
      } else {
        // Attendre un peu avant de réessayer
        setTimeout(() => {
          this.refreshVideo();
        }, 2000);
      }
    },
    
    refreshVideo() {
      // Force le rafraîchissement du flux vidéo avec un timestamp pour éviter la mise en cache
      this.videoUrl = `${API_URL}/video/feed?timestamp=${new Date().getTime()}`;
      // Réinitialiser le compteur d'erreurs si la vidéo se charge correctement
      this.videoErrorCount = 0;
    },
    
    toggleRecording() {
      if (this.isRecording) {
        this.stopRecording();
      } else {
        this.startRecording();
      }
    },
    
    startRecording() {
      if (!this.isConnected) return;
      
      this.isRecording = true;
      this.recordingStartTime = Date.now();
      
      // Mettre à jour le compteur de temps d'enregistrement
      this.recordingInterval = setInterval(() => {
        const elapsedSeconds = Math.floor((Date.now() - this.recordingStartTime) / 1000);
        const minutes = Math.floor(elapsedSeconds / 60).toString().padStart(2, '0');
        const seconds = (elapsedSeconds % 60).toString().padStart(2, '0');
        this.recordingTime = `${minutes}:${seconds}`;
      }, 1000);
      
      // Envoyer la commande au backend si nécessaire
      // axios.get(`${API_URL}/video/start_recording`);
    },
    
    stopRecording() {
      if (!this.isRecording) return;
      
      this.isRecording = false;
      clearInterval(this.recordingInterval);
      const finalRecordingTime = this.recordingTime;
      this.recordingTime = '00:00';
      
      // Envoyer la commande au backend si nécessaire
      // axios.get(`${API_URL}/video/stop_recording`);
      
      // Notification de fin d'enregistrement
      console.log(`Enregistrement terminé: ${finalRecordingTime}`);
    }
  }
};
</script>
  
  <style scoped>
  .dashboard-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .dashboard-header h1 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--text-color);
  }
  
  .dashboard-header h1 i {
    color: var(--primary-color);
  }
  
  .connection-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    background-color: var(--light-gray);
  }
  
  .connection-status.connected {
    background-color: rgba(46, 204, 113, 0.2);
    color: #27ae60;
  }
  
  .connection-status .status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #27ae60;
    display: inline-block;
  }
  
  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 1.5rem;
  }

  .empty-photo {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--light-gray);
    color: var(--medium-gray);
    font-size: 2rem;
  }

  .empty-camera {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    color: var(--medium-gray);
    font-size: 3rem;
    padding: 2rem;
  }

  .empty-camera p {
    font-size: 1.2rem;
    margin: 1rem 0;
    color: var(--dark-gray);
  }

  .connect-btn, .refresh-btn {
    margin-top: 1rem;
    padding: 0.6rem 1.2rem;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--border-radius-md);
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .connect-btn:hover, .refresh-btn:hover {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
  }


  .empty-map {
    background-color: var(--light-gray);
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--medium-gray);
    font-size: 2rem;
  }

  .map-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .grid-item {
    background-color: white;
    border-radius: var(--border-radius-md);
    box-shadow: var(--card-shadow);
    overflow: hidden;
  }
  
  .large {
    grid-column: span 2;
    grid-row: span 2;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.25rem;
    background-color: var(--light-gray);
    border-bottom: 1px solid var(--medium-gray);
  }
  
  .card-header h2 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-color);
    font-weight: 600;
  }
  
  .controls {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    color: var(--dark-gray);
    border: 1px solid var(--medium-gray);
    transition: all 0.2s ease;
  }
  
  .btn-icon:hover {
    background-color: var(--light-gray);
    color: var(--primary-color);
  }
  
  .btn-text {
    background: none;
    border: none;
    color: var(--primary-color);
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    border-radius: var(--border-radius-sm);
  }
  
  .btn-text:hover {
    background-color: rgba(52, 152, 219, 0.1);
  }
  
  /* Camera Feed */
  .camera-content {
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 400px;
    background-color: #1e1e1e;
    border-radius: var(--border-radius-md);
    overflow: hidden;
  }

  .camera-content img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  

  .camera-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .overlay-item {
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    padding: 0.5rem 0.75rem;
    border-radius: var(--border-radius-sm);
    font-weight: 600;
    width: fit-content;
  }

  .overlay-item.altitude {
    align-self: flex-start;
  }

  .overlay-item.speed {
    align-self: flex-end;
  }

  .overlay-item.recording {
    align-self: flex-start;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: rgba(231, 76, 60, 0.8);
    animation: pulse 2s infinite;
  }

  .overlay-item.battery {
    align-self: flex-end;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .text-danger {
    color: #e74c3c;
  }
  
  /* Stats */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    padding: 1rem;
    gap: 1rem;
  }
  
  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1rem;
    background-color: var(--light-gray);
    border-radius: var(--border-radius-sm);
  }
  
  .stat-icon {
    font-size: 1.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.5rem;
  }
  
  .stat-label {
    font-size: 0.9rem;
    color: var(--dark-gray);
  }
  
  /* Flight Data */
  .data-table {
    padding: 1rem;
  }
  
  .data-row {
    display: flex;
    justify-content: space-between;
    padding: 0.8rem 0;
    border-bottom: 1px solid var(--light-gray);
  }
  
  .data-row:last-child {
    border-bottom: none;
  }
  
  .data-label {
    color: var(--dark-gray);
  }
  
  .data-value {
    font-weight: 500;
    color: var(--text-color);
  }
  
  .mode-badge {
    background-color: var(--primary-color);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: var(--border-radius-sm);
    font-size: 0.85rem;
  }
  
  /* GPS Location */
  .map-container {
    position: relative;
    height: 200px;
    overflow: hidden;
  }
  
  .map-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .map-marker {
    position: absolute;
    width: 24px;
    height: 24px;
    background-color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }
  
  .drone-marker {
    top: 40%;
    left: 60%;
    color: var(--primary-color);
  }
  
  .home-marker {
    top: 60%;
    left: 30%;
    color: var(--accent-color);
  }
  
  .coordinates {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    font-size: 0.9rem;
  }
  
  .coordinate-label {
    color: var(--dark-gray);
    margin-right: 0.5rem;
  }
  
  .coordinate-value {
    font-weight: 500;
    color: var(--text-color);
  }
  
  /* Photos */
  .photo-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
    padding: 1rem;
  }
  
  .photo-item {
    border-radius: var(--border-radius-sm);
    overflow: hidden;
    aspect-ratio: 1;
  }
  
  .photo-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }
  
  .photo-item:hover img {
    transform: scale(1.05);
  }

  .controls-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  padding: 1rem;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--light-gray);
  border: none;
  border-radius: var(--border-radius-sm);
  padding: 1rem 0.5rem;
  color: var(--text-color);
  font-weight: 500;
  transition: all 0.2s ease;
}

.control-btn i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

.control-btn:hover:not(:disabled) {
  background-color: var(--primary-color);
  color: white;
}

.control-btn:hover:not(:disabled) i {
  color: white;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.control-btn.emergency {
  grid-column: span 2;
  background-color: #ffeeee;
}

.control-btn.emergency i {
  color: #e74c3c;
}

.control-btn.emergency:hover:not(:disabled) {
  background-color: #e74c3c;
  color: white;
}

.control-btn.emergency:hover:not(:disabled) i {
  color: white;
}

.btn-connect {
  margin-left: 1rem;
  padding: 0.25rem 0.75rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  font-size: 0.9rem;
  cursor: pointer;
}

/* Style pour fixer la taille du flux vidéo */
.camera-content img {
  width: 100%;
  height: 100%;
  min-height: 400px;
  object-fit: cover;
  display: block;
}

/* Pour les photos capturées */
.photo-item {
  position: relative;
  overflow: hidden;
}

.photo-item::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(0deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 50%);
  pointer-events: none;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

/* Responsive */
@media screen and (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .large {
    grid-column: span 2;
  }
}

@media screen and (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .large {
    grid-column: span 1;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
  