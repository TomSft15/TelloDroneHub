<template>
    <div class="drone-camera-view">
      <div class="view-header">
        <h1><i class="fas fa-video"></i> Flux Vidéo du Drone</h1>
        <div class="view-controls">
          <button class="btn-status" :class="{ 'btn-connected': camera.connected }" @click="toggleCameraConnection">
            <i :class="camera.connected ? 'fas fa-link' : 'fas fa-unlink'"></i>
            {{ camera.connected ? 'Connecté' : 'Déconnecté' }}
          </button>
        </div>
      </div>
  
      <div class="view-content">
        <div class="camera-section">
          <DroneCamera 
            ref="droneCamera"
            :droneId="droneId"
            :autoConnect="autoConnect"
            @camera-status-change="onCameraStatusChange"
            @photo-captured="onPhotoCaptured"
            @recording-started="onRecordingStarted"
            @recording-stopped="onRecordingStopped"
          />
          
          <div class="camera-actions">
            <button class="action-btn" @click="capturePhoto" :disabled="!camera.connected">
              <i class="fas fa-camera"></i> Prendre une photo
            </button>
            <button class="action-btn" @click="toggleRecording" :disabled="!camera.connected" 
                    :class="{ 'recording': camera.isRecording }">
              <i :class="camera.isRecording ? 'fas fa-stop' : 'fas fa-video'"></i>
              {{ camera.isRecording ? 'Arrêter l\'enregistrement' : 'Démarrer l\'enregistrement' }}
            </button>
          </div>
        </div>
        
        <div class="info-section">
          <div class="card info-card">
            <div class="card-header">
              <h3>Paramètres de la Caméra</h3>
            </div>
            <div class="card-content">
              <div class="parameter-row">
                <div class="parameter-label">Statut</div>
                <div class="parameter-value">
                  <span class="status-indicator" :class="{ 'status-on': camera.connected }"></span>
                  {{ camera.connected ? 'Connecté' : 'Déconnecté' }}
                </div>
              </div>
              <div class="parameter-row">
                <div class="parameter-label">Résolution</div>
                <div class="parameter-value">720p</div>
              </div>
              <div class="parameter-row">
                <div class="parameter-label">FPS</div>
                <div class="parameter-value">30</div>
              </div>
              <div class="parameter-row">
                <div class="parameter-label">Mode</div>
                <div class="parameter-value">{{ camera.isRecording ? 'Enregistrement' : 'Visualisation' }}</div>
              </div>
            </div>
          </div>
          
          <div class="card storage-card">
            <div class="card-header">
              <h3>Stockage</h3>
            </div>
            <div class="card-content">
              <div class="storage-stats">
                <div class="storage-item">
                  <i class="fas fa-camera"></i>
                  <div class="storage-count">{{ capturedPhotos.length }}</div>
                  <div class="storage-label">Photos</div>
                </div>
                <div class="storage-item">
                  <i class="fas fa-film"></i>
                  <div class="storage-count">{{ recordings.length }}</div>
                  <div class="storage-label">Vidéos</div>
                </div>
              </div>
              
              <div class="storage-meter">
                <div class="meter-label">Espace utilisé</div>
                <div class="meter-bar">
                  <div class="meter-fill" :style="{ width: storageUsage + '%' }"></div>
                </div>
                <div class="meter-value">{{ storageUsage }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="recent-captures" v-if="capturedPhotos.length > 0">
        <h3>Photos Récentes</h3>
        <div class="captures-grid">
          <div v-for="(photo, index) in recentPhotos" :key="index" class="capture-item">
            <img :src="photo.src" alt="Photo capturée" @click="showPhotoDetails(photo)" />
            <div class="capture-time">{{ formatTimestamp(photo.timestamp) }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import DroneCamera from '../DroneCamera.vue';
  
  export default {
    name: 'DroneCameraView',
    components: {
      DroneCamera
    },
    props: {
      droneId: {
        type: String,
        default: 'simulation'
      },
      autoConnect: {
        type: Boolean,
        default: true
      }
    },
    
    setup(props) {
      const droneCameraRef = ref(null);
      const camera = ref({
        connected: false,
        isRecording: false,
        recordingTime: '00:00'
      });
      const capturedPhotos = ref([]);
      const recordings = ref([]);
      const storageUsage = ref(12); // Simulation de l'utilisation du stockage
      
      // Photos récentes (limitées aux 4 dernières)
      const recentPhotos = computed(() => {
        return capturedPhotos.value.slice(-4).reverse();
      });
      
      // Méthodes pour gérer la caméra
      const toggleCameraConnection = () => {
        if (camera.value.connected) {
          droneCameraRef.value.disconnectCamera();
        } else {
          droneCameraRef.value.connectCamera();
        }
      };
      
      const capturePhoto = () => {
        if (droneCameraRef.value) {
          droneCameraRef.value.capturePhoto();
        }
      };
      
      const toggleRecording = () => {
        if (droneCameraRef.value) {
          droneCameraRef.value.toggleRecording();
        }
      };
      
      // Méthodes pour gérer les événements de la caméra
      const onCameraStatusChange = (status) => {
        camera.value.connected = status.connected;
      };
      
      const onPhotoCaptured = (photo) => {
        capturedPhotos.value.push(photo);
        // Augmenter l'utilisation du stockage (simulation)
        storageUsage.value = Math.min(100, storageUsage.value + 1);
      };
      
      const onRecordingStarted = () => {
        camera.value.isRecording = true;
      };
      
      const onRecordingStopped = (recordingInfo) => {
        camera.value.isRecording = false;
        recordings.value.push({
          id: Date.now(),
          timestamp: new Date().toISOString(),
          duration: recordingInfo.duration
        });
        // Augmenter l'utilisation du stockage (simulation)
        storageUsage.value = Math.min(100, storageUsage.value + 5);
      };
      
      // Afficher les détails d'une photo
      const showPhotoDetails = (photo) => {
        // Cette fonction pourrait ouvrir une modal ou naviguer vers une page détaillée
        console.log('Affichage des détails de la photo:', photo);
        alert(`Photo capturée le ${formatTimestamp(photo.timestamp)}`);
      };
      
      // Formater un timestamp
      const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      };
      
      onMounted(() => {
        // Vous pourriez charger les photos précédentes depuis une API ici
        console.log('Vue de la caméra du drone montée');
      });
      
      return {
        droneCameraRef,
        camera,
        capturedPhotos,
        recordings,
        storageUsage,
        recentPhotos,
        toggleCameraConnection,
        capturePhoto,
        toggleRecording,
        onCameraStatusChange,
        onPhotoCaptured,
        onRecordingStarted,
        onRecordingStopped,
        showPhotoDetails,
        formatTimestamp
      };
    }
  };
  </script>
  
  <style scoped>
  .drone-camera-view {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }
  
  .view-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--light-gray);
  }
  
  .view-header h1 {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0;
    color: var(--text-color);
  }
  
  .view-header h1 i {
    color: var(--primary-color);
  }
  
  .btn-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    background-color: var(--light-gray);
    color: var(--dark-gray);
    transition: all 0.2s ease;
  }
  
  .btn-connected {
    background-color: var(--success-color);
    color: white;
  }
  
  .view-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
  }
  
  .camera-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .camera-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .action-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    background-color: var(--primary-color);
    color: white;
    transition: all 0.2s ease;
  }
  
  .action-btn:hover {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
  }
  
  .action-btn:disabled {
    background-color: var(--medium-gray);
    color: var(--dark-gray);
    cursor: not-allowed;
    transform: none;
  }
  
  .action-btn.recording {
    background-color: var(--accent-color);
    animation: pulse 2s infinite;
  }
  
  .info-section {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .card {
    background-color: white;
    border-radius: var(--border-radius-md);
    box-shadow: var(--card-shadow);
    overflow: hidden;
  }
  
  .card-header {
    padding: 1rem;
    background-color: var(--light-gray);
    border-bottom: 1px solid var(--medium-gray);
  }
  
  .card-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-color);
  }
  
  .card-content {
    padding: 1rem;
  }
  
  .parameter-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--light-gray);
  }
  
  .parameter-row:last-child {
    border-bottom: none;
  }
  
  .parameter-label {
    color: var(--dark-gray);
  }
  
  .parameter-value {
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: var(--medium-gray);
  }
  
  .status-on {
    background-color: var(--success-color);
  }
  
  .storage-stats {
    display: flex;
    justify-content: space-around;
    margin-bottom: 1.5rem;
  }
  
  .storage-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .storage-item i {
    font-size: 1.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
  }
  
  .storage-count {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-color);
  }
  
  .storage-label {
    font-size: 0.9rem;
    color: var(--dark-gray);
  }
  
  .storage-meter {
    margin-top: 1rem;
  }
  
  .meter-label {
    font-size: 0.9rem;
    color: var(--dark-gray);
    margin-bottom: 0.5rem;
  }
  
  .meter-bar {
    height: 10px;
    background-color: var(--light-gray);
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }
  
  .meter-fill {
    height: 100%;
    background-color: var(--primary-color);
    border-radius: 5px;
  }
  
  .meter-value {
    text-align: right;
    font-size: 0.9rem;
    color: var(--dark-gray);
  }
  
  .recent-captures {
    margin-top: 2rem;
  }
  
  .recent-captures h3 {
    margin-bottom: 1rem;
    color: var(--text-color);
  }
  
  .captures-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .capture-item {
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--card-shadow);
    position: relative;
    cursor: pointer;
    transition: transform 0.2s ease;
  }
  
  .capture-item:hover {
    transform: translateY(-5px);
  }
  
  .capture-item img {
    width: 100%;
    aspect-ratio: 4/3;
    object-fit: cover;
    display: block;
  }
  
  .capture-time {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 0.5rem;
    font-size: 0.8rem;
    text-align: center;
  }
  
  @keyframes pulse {
    0% {
      opacity: 1;
      box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4);
    }
    70% {
      opacity: 0.9;
      box-shadow: 0 0 0 10px rgba(231, 76, 60, 0);
    }
    100% {
      opacity: 1;
      box-shadow: 0 0 0 0 rgba(231, 76, 60, 0);
    }
  }
  
  @media (max-width: 768px) {
    .view-content {
      grid-template-columns: 1fr;
    }
    
    .camera-actions {
      flex-direction: column;
    }
    
    .captures-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  </style>