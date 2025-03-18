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
      <!-- Section Caméra et Flux Vidéo -->
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

      <!-- Section Statistiques de Vol -->
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

      <!-- Section des Données de Vol -->
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
              <span class="mode-badge">{{ currentControlMode }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Photos Récentes -->
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

      <!-- NOUVELLE SECTION: Modes de contrôle -->
      <div class="control-modes grid-item large">
        <div class="card-header">
          <h2>Modes de contrôle</h2>
          <div class="header-actions">
            <button class="btn-text" @click="toggleAllModes(true)" :disabled="isAllModesEnabled">
              <i class="fas fa-check-double"></i> Tout activer
            </button>
            <button class="btn-text" @click="toggleAllModes(false)" :disabled="isNoModeEnabled">
              <i class="fas fa-times"></i> Tout désactiver
            </button>
          </div>
        </div>
        <div class="control-content">
          <div class="control-modes-grid">
            <!-- Mode contrôle clavier -->
            <div class="mode-card" :class="{ 'mode-active': keyboardEnabled }">
              <div class="mode-header">
                <div class="mode-title">
                  <i class="fas fa-keyboard"></i>
                  <h3>Contrôle par clavier</h3>
                </div>
                <div class="mode-toggle">
                  <label class="switch">
                    <input type="checkbox" v-model="keyboardEnabled" @change="handleKeyboardToggle">
                    <span class="slider round"></span>
                  </label>
                </div>
              </div>
              <div class="mode-content" v-if="keyboardEnabled">
                <div class="key-grid">
                  <div class="key-group">
                    <div class="key-item">
                      <span class="key">↑</span>
                      <span class="key-label">Monter</span>
                    </div>
                    <div class="key-item">
                      <span class="key">↓</span>
                      <span class="key-label">Descendre</span>
                    </div>
                    <div class="key-item">
                      <span class="key">←</span>
                      <span class="key-label">Rotation gauche</span>
                    </div>
                    <div class="key-item">
                      <span class="key">→</span>
                      <span class="key-label">Rotation droite</span>
                    </div>
                  </div>
                  <div class="key-group">
                    <div class="key-item">
                      <span class="key">Z</span>
                      <span class="key-label">Avancer</span>
                    </div>
                    <div class="key-item">
                      <span class="key">S</span>
                      <span class="key-label">Reculer</span>
                    </div>
                    <div class="key-item">
                      <span class="key">Q</span>
                      <span class="key-label">Dépl. gauche</span>
                    </div>
                    <div class="key-item">
                      <span class="key">D</span>
                      <span class="key-label">Dépl. droite</span>
                    </div>
                  </div>
                  <div class="key-group">
                    <div class="key-item">
                      <span class="key">A</span>
                      <span class="key-label">Décollage</span>
                    </div>
                    <div class="key-item">
                      <span class="key">E</span>
                      <span class="key-label">Atterrissage</span>
                    </div>
                    <div class="key-item">
                      <span class="key">P</span>
                      <span class="key-label">Arrêt d'urgence</span>
                    </div>
                    <div class="key-item">
                      <span class="key key-space">Space</span>
                      <span class="key-label">Vol stationnaire</span>
                    </div>
                  </div>
                </div>
                <div class="mode-actions">
                  <router-link to="/keyboard-config" class="btn-outline">
                    <i class="fas fa-cog"></i> Configurer
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Mode contrôle vocal -->
            <div class="mode-card" :class="{ 'mode-active': voiceEnabled }">
              <div class="mode-header">
                <div class="mode-title">
                  <i class="fas fa-microphone"></i>
                  <h3>Contrôle vocal</h3>
                </div>
                <div class="mode-toggle">
                  <label class="switch">
                    <input type="checkbox" v-model="voiceEnabled" @change="handleVoiceToggle" :disabled="!recognitionEnabled">
                    <span class="slider round"></span>
                  </label>
                </div>
              </div>
              <div class="mode-content" v-if="voiceEnabled">
                <div class="voice-status">
                  <div class="status-indicator" :class="{ 'is-active': isListening }">
                    <i class="fas" :class="isListening ? 'fa-microphone' : 'fa-microphone-slash'"></i>
                    <span>{{ isListening ? 'Écoute active' : 'Écoute inactive' }}</span>
                  </div>
                  <div class="mic-visualizer">
                    <div class="wave-container" :class="{ 'active': isListening }">
                      <div class="wave"></div>
                      <div class="wave"></div>
                      <div class="wave"></div>
                    </div>
                  </div>
                  <button @click="toggleSpeechRecognition" class="btn-speech" :class="{ 'btn-active': isListening, 'btn-inactive': !isListening }">
                    <i :class="isListening ? 'fas fa-stop' : 'fas fa-microphone'"></i>
                    {{ isListening ? 'Arrêter' : 'Démarrer' }} l'écoute
                  </button>
                </div>
                <div v-if="recognizedText" class="recognized-text">
                  Commande: "{{ recognizedText }}"
                </div>
              </div>
              <div class="mode-not-available" v-if="!recognitionEnabled">
                <p>La reconnaissance vocale n'est pas disponible sur ce navigateur.</p>
              </div>
            </div>

            <!-- Mode contrôle gestuel -->
            <div class="mode-card" :class="{ 'mode-active': gestureEnabled }">
              <div class="mode-header">
                <div class="mode-title">
                  <i class="fas fa-hand-paper"></i>
                  <h3>Contrôle gestuel</h3>
                </div>
                <div class="mode-toggle">
                  <label class="switch">
                    <input type="checkbox" v-model="gestureEnabled" @change="handleGestureToggle" :disabled="!isDroneConnected">
                    <span class="slider round"></span>
                  </label>
                </div>
              </div>
              <div class="mode-content" v-if="gestureEnabled">
                <div class="gesture-status">
                  <div class="status-indicator" :class="{ 'is-active': isGestureEnabled }">
                    <span class="status-dot"></span>
                    <span class="status-text">{{ isGestureEnabled ? 'Activé' : 'Désactivé' }}</span>
                  </div>
                  <button 
                    @click="toggleGestureRecognition" 
                    :disabled="!isDroneConnected || isGestureLoading"
                    :class="{ 'btn-active': isGestureEnabled, 'btn-inactive': !isGestureEnabled }"
                    class="btn-medium">
                    <i :class="isGestureLoading ? 'fas fa-spinner fa-spin' : (isGestureEnabled ? 'fas fa-hand-paper' : 'fas fa-play')"></i>
                    {{ isGestureEnabled ? 'Désactiver' : 'Activer' }}
                  </button>
                </div>
                <div class="gestures-mini-grid">
                  <div class="gesture-item">
                    <div class="gesture-image">
                      <i class="fas fa-hand-paper"></i>
                    </div>
                    <p>Décollage</p>
                  </div>
                  <div class="gesture-item">
                    <div class="gesture-image">
                      <i class="fas fa-fist-raised"></i>
                    </div>
                    <p>Atterrissage</p>
                  </div>
                  <div class="gesture-item">
                    <div class="gesture-image">
                      <i class="fas fa-thumbs-up"></i>
                    </div>
                    <p>Monter</p>
                  </div>
                  <div class="gesture-item">
                    <div class="gesture-image">
                      <i class="fas fa-thumbs-down"></i>
                    </div>
                    <p>Descendre</p>
                  </div>
                </div>
              </div>
              <div class="mode-not-available" v-if="!isDroneConnected">
                <p>Connectez-vous à un drone pour utiliser le contrôle gestuel.</p>
              </div>
            </div>

            <!-- Mode vision et suivi -->
            <div class="mode-card" :class="{ 'mode-active': visionEnabled }">
              <div class="mode-header">
                <div class="mode-title">
                  <i class="fas fa-eye"></i>
                  <h3>Vision et suivi</h3>
                </div>
                <div class="mode-toggle">
                  <label class="switch">
                    <input type="checkbox" v-model="visionEnabled" @change="handleVisionToggle" :disabled="!isDroneConnected">
                    <span class="slider round"></span>
                  </label>
                </div>
              </div>
              <div class="mode-content" v-if="visionEnabled">
                <!-- Intégration du composant FaceTrackingControl -->
                <FaceTrackingControl/>
              </div>
              <div class="mode-not-available" v-if="!isDroneConnected">
                <p>Connectez-vous à un drone pour utiliser la vision et le suivi.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Contrôles du Drone -->
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
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import emitter from '../../eventBus';
import keyboardControls from '../../mixins/keyboardControls';
import gestureService from '../../services/gestureService';
import FaceTrackingControl from '../../components/FaceTrackingControl.vue';


const API_URL = 'http://localhost:5000';

export default {
  name: 'DashboardViewPage',
  mixins: [keyboardControls],
  components: {
    FaceTrackingControl
  },
  data() {
    return {
      isConnected: false,
      videoUrl: `${API_URL}/video/feed`,
      videoRefreshKey: 0,
      droneData: {
        battery: 0,
        temperature: 0,
        flight_time: 0,
        height: 0,
        speed: 0,
        signal: 0
      },
      keyboardEnabled: false,      // Activé par défaut
      voiceEnabled: false,
      gestureEnabled: false,
      visionEnabled: false,
      isFaceTrackingEnabled: false,
      isFaceTrackingLoading: false,
      capturedImages: [],
      dataUpdateInterval: null,
      consecutiveErrors: 0,
      videoErrorCount: 0,
      maxVideoErrors: 3,
      isRecording: false,
      recordingTime: '00:00',
      recordingInterval: null,
      recordingStartTime: 0,
      
      // Modes de contrôle
      controlModes: [
        { id: 'keyboard', name: 'Clavier', icon: 'fas fa-keyboard' },
        { id: 'voice', name: 'Voix', icon: 'fas fa-microphone' },
        { id: 'gesture', name: 'Gestes', icon: 'fas fa-hand-paper' },
        { id: 'vision', name: 'Vision', icon: 'fas fa-eye' }
      ],
      
      // Voice control
      isListening: false,
      recognizedText: '',
      recognitionEnabled: true,
      commandsMap: {
        'décollage': 'takeoff',
        'décoller': 'takeoff',
        'envole': 'takeoff',
        'atterrissage': 'land',
        'atterrir': 'land',
        'poser': 'land',
        'avance': 'moveForward',
        'recule': 'moveBackward',
        'gauche': 'moveLeft',
        'droite': 'moveRight',
        'monte': 'moveUp',
        'descend': 'moveDown',
        'descendre': 'moveDown',
        'tourne à gauche': 'rotateLeft',
        'rotation gauche': 'rotateLeft',
        'tourne à droite': 'rotateRight',
        'rotation droite': 'rotateRight',
        'looping en avant': 'flipForward',
        'looping avant': 'flipForward',
        'looping en arrière': 'flipBackward',
        'looping arrière': 'flipBackward',
        'looping à gauche': 'flipLeft',
        'looping gauche': 'flipLeft',
        'looping à droite': 'flipRight',
        'looping droite': 'flipRight',
        'stop': 'emergencyStop',
        'arrêt': 'emergencyStop',
        'urgence': 'emergencyStop'
      },
      recognition: null,
      recognitionTimeout: null,
      
      // Gesture control
      isGestureEnabled: false,
      isDroneConnected: false,
      isGestureLoading: false,
      gestureStatus: null,
      statusInterval: null,
      
      // Vision control
      faceRecognitionExpanded: false,
      faceTrackingExpanded: false,
      isDragging: false,
      previewImage: null,
      selectedFile: null,
      personName: '',
      personRelation: 'family',
      people: []
    };
  },
  computed: {
    formattedTimeUntilNext() {
      if (!this.gestureStatus) return '0.0s';
      
      const time = this.gestureStatus.time_until_next.toFixed(1);
      return `${time}s`;
    },
    canSavePerson() {
      return this.previewImage !== null && this.personName.trim() !== '';
    },
    isAllModesEnabled() {
      return this.keyboardEnabled && this.voiceEnabled && 
            this.gestureEnabled && this.visionEnabled;
    },
    isNoModeEnabled() {
      return !this.keyboardEnabled && !this.voiceEnabled && 
            !this.gestureEnabled && !this.visionEnabled;
    }
  },
  watch: {
    keyboardEnabled(newVal) {
      if (newVal) {
        this.enableKeyboardControls();
      } else {
        this.disableKeyboardControls();
      }
    },
    voiceEnabled(newVal) {
      if (newVal) {
        this.checkSpeechRecognitionSupport();
      } else if (this.isListening) {
        this.stopSpeechRecognition();
      }
    },
    gestureEnabled(newVal) {
      if (newVal && !this.isGestureEnabled) {
        this.toggleGestureRecognition();
      } else if (!newVal && this.isGestureEnabled) {
        this.toggleGestureRecognition();
      }
    },
    visionEnabled(newVal) {
      if (!newVal && this.isFaceTrackingEnabled) {
        this.toggleFaceTracking();
      }
    }
  },
  mounted() {
    // Vérifier l'état de la connexion au chargement
    this.checkDroneStatus();
    
    // Vérifier si la reconnaissance vocale est supportée
    this.checkSpeechRecognitionSupport();
    
    // Charger la liste des personnes connues (pour la vision)
    this.loadPeople();

    this.loadSavedImages();
    
    // Écouter les événements avec l'émetteur
    emitter.on('drone-connected', () => {
      this.checkDroneStatus();
    });
    
    emitter.off('drone-disconnected', () => {
      this.isConnected = false;
      if (this.dataUpdateInterval) {
        clearInterval(this.dataUpdateInterval);
      }
    });
    
    // Activer les contrôles clavier par défaut
    this.enableKeyboardControls();
  },
  beforeUnmount() {
    // Nettoyer les écouteurs d'événements
    emitter.off('drone-connected');
    emitter.off('drone-disconnected');
    
    // Nettoyer les intervalles
    if (this.dataUpdateInterval) {
      clearInterval(this.dataUpdateInterval);
    }
    
    if (this.statusInterval) {
      clearInterval(this.statusInterval);
    }
    
    // Arrêter la reconnaissance vocale si active
    if (this.isListening) {
      this.stopSpeechRecognition();
    }
    
    // Nettoyer les écouteurs d'événements du clavier
    this.disableKeyboardControls();
  },
  methods: {
    // Méthodes principales du dashboard
    async checkDroneStatus() {
      try {
        const response = await axios.get(`${API_URL}/status`);
        this.isConnected = response.data.connected;
        this.isDroneConnected = response.data.connected;
        
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
        this.isDroneConnected = false;
        localStorage.removeItem('droneConnected');
      }
    },

    toggleAllModes(enabled) {
      this.keyboardEnabled = enabled;
      this.voiceEnabled = enabled && this.recognitionEnabled;
      this.gestureEnabled = enabled && this.isDroneConnected;
      this.visionEnabled = enabled && this.isDroneConnected;
    },
  
    handleKeyboardToggle() {
      if (this.keyboardEnabled) {
        this.enableKeyboardControls();
      } else {
        this.disableKeyboardControls();
      }
    },
    
    handleVoiceToggle() {
      if (!this.voiceEnabled && this.isListening) {
        this.stopSpeechRecognition();
      }
    },
    
    handleGestureToggle() {
      if (this.gestureEnabled !== this.isGestureEnabled) {
        this.toggleGestureRecognition();
      }
    },
    
    handleVisionToggle() {
      // Si on désactive la vision et que le suivi facial est actif, on le désactive aussi
      if (!this.visionEnabled && this.isFaceTrackingEnabled) {
        this.toggleFaceTracking();
      }
    },
    
    // Méthode pour le suivi facial
    async toggleFaceTracking() {
      if (!this.isDroneConnected) return;
      
      this.isFaceTrackingLoading = true;
      
      try {
        // Utilisez votre API de suivi facial ici
        const response = await axios.get(`${API_URL}/face_tracking/${this.isFaceTrackingEnabled ? 'stop' : 'start'}`);
        
        if (response.data.success) {
          this.isFaceTrackingEnabled = !this.isFaceTrackingEnabled;
          this.$notify && this.$notify.info(`Suivi facial ${this.isFaceTrackingEnabled ? 'activé' : 'désactivé'}`);
        } else {
          this.$notify && this.$notify.error(`Erreur: ${response.data.message}`);
        }
      } catch (error) {
        console.error('Erreur lors de la modification du suivi facial:', error);
        this.$notify && this.$notify.error('Erreur de communication avec le serveur');
      } finally {
        this.isFaceTrackingLoading = false;
      }
    },
    
    async connectDrone() {
      // Rediriger l'utilisateur vers la page de connexion
      this.$router.push('/connect');
    },
    
    refreshVideo() {
      // Force le rafraîchissement du flux vidéo avec un timestamp pour éviter la mise en cache
      this.videoUrl = `${API_URL}/video/feed?timestamp=${new Date().getTime()}`;
      // Réinitialiser le compteur d'erreurs si la vidéo se charge correctement
      this.videoErrorCount = 0;
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
              this.isDroneConnected = false;
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
    
    async takePhoto() {
      try {
        // Faire une requête au serveur pour capturer l'image
        const response = await axios.get(`${API_URL}/drone/capture_photo`);
        
        if (response.data && response.data.success) {
          // Générer un nom unique pour l'image
          const timestamp = new Date().toISOString().replace(/:/g, '-');
          const imageName = `capture_${timestamp}.jpg`;
          
          // Vérifier si l'image est déjà en base64
          let imageData = response.data.image;
          
          // Si l'image n'a pas le préfixe data:image, on l'ajoute
          if (imageData && !imageData.startsWith('data:image')) {
            imageData = `data:image/jpeg;base64,${imageData}`;
          }
          
          // Ajouter à notre collection d'images
          this.capturedImages.unshift({
            src: imageData,
            name: imageName
          });
          
          // Sauvegarder les images dans le localStorage
          localStorage.setItem('droneImages', JSON.stringify(this.capturedImages.slice(0, 20)));
          
          console.log('Photo capturée avec succès');
          alert('Photo capturée !');
          
          return true;
        } else {
          alert('Erreur lors de la capture: ' + (response.data.message || 'Erreur inconnue'));
          return false;
        }
      } catch (error) {
        console.error("Erreur lors de la capture de la photo:", error);
        alert('Impossible de capturer la photo: ' + (error.message || 'Erreur inconnue'));
        return false;
      }
    },

    loadSavedImages() {
      try {
        // Récupérer les images sauvegardées dans le localStorage
        const savedImages = localStorage.getItem('droneImages');
        if (savedImages) {
          const parsedImages = JSON.parse(savedImages);
          
          // Vérifier que chaque image a le bon format pour l'élément src
          this.capturedImages = parsedImages.map(img => {
            // Si l'image n'a pas le préfixe data:image, on l'ajoute
            if (img.src && !img.src.startsWith('data:image')) {
              return {
                ...img,
                src: `data:image/jpeg;base64,${img.src}`
              };
            }
            return img;
          });
          
          console.log(`${this.capturedImages.length} images chargées du localStorage`);
        } else {
          this.capturedImages = [];
        }
      } catch (error) {
        console.error("Erreur lors du chargement des images sauvegardées:", error);
        this.capturedImages = [];
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
    },
    
    stopRecording() {
      if (!this.isRecording) return;
      
      this.isRecording = false;
      clearInterval(this.recordingInterval);
      const finalRecordingTime = this.recordingTime;
      this.recordingTime = '00:00';
      
      console.log(`Enregistrement terminé: ${finalRecordingTime}`);
    },
    
    // Méthodes pour changer de mode de contrôle
    switchControlMode(mode) {
      this.currentControlMode = mode;
    },
    
    // Méthodes de contrôle vocal
    checkSpeechRecognitionSupport() {
      // Vérifier si le navigateur supporte l'API Web Speech
      this.recognitionEnabled = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
      
      if (!this.recognitionEnabled && this.currentControlMode === 'voice') {
        console.warn('La reconnaissance vocale n\'est pas supportée par ce navigateur.');
      }
    },
    
    toggleSpeechRecognition() {
      if (!this.recognitionEnabled) {
        alert('La reconnaissance vocale n\'est pas disponible sur ce navigateur.');
        return;
      }
      
      if (this.isListening) {
        this.stopSpeechRecognition();
      } else {
        this.startSpeechRecognition();
      }
    },
    
    startSpeechRecognition() {
      // S'assurer qu'aucune instance précédente n'est en cours
      this.stopSpeechRecognition();
      
      try {
        // Création de l'objet de reconnaissance vocale
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configuration
        this.recognition.lang = 'fr-FR';
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.maxAlternatives = 1;
        
        // Événements
        this.recognition.onstart = () => {
          this.isListening = true;
          console.log('Reconnaissance vocale démarrée');
        };
        
        this.recognition.onresult = (event) => {
          // Vérifier que l'événement et les résultats sont valides
          if (event && event.results && event.results[0]) {
            const transcript = event.results[0][0].transcript.toLowerCase().trim();
            console.log('Texte reconnu:', transcript);
            this.recognizedText = transcript;
            
            // Rechercher la commande correspondante
            this.processVoiceCommand(transcript);
          }
        };
        
        this.recognition.onerror = (event) => {
          console.error('Erreur de reconnaissance vocale:', event.error);
          this.isListening = false;
        };
        
        this.recognition.onend = () => {
          console.log('Reconnaissance vocale terminée');
          
          // Redémarrer automatiquement la reconnaissance si elle était active
          if (this.isListening && this.recognition) {
            // Attendre un court instant avant de redémarrer
            this.recognitionTimeout = setTimeout(() => {
              // Vérifier à nouveau que le composant est monté et que l'utilisateur n'a pas désactivé l'écoute
              if (this.isListening && this.recognition) {
                try {
                  this.recognition.start();
                } catch (e) {
                  console.error('Erreur lors du redémarrage de la reconnaissance:', e);
                  this.isListening = false;
                }
              }
            }, 500);
          } else {
            this.isListening = false;
          }
        };
        
        // Démarrer la reconnaissance
        this.recognition.start();
      } catch (error) {
        console.error('Erreur lors de l\'initialisation de la reconnaissance vocale:', error);
        this.isListening = false;
        this.recognition = null;
      }
    },
    
    stopSpeechRecognition() {
      // Arrêter tous les timeouts
      if (this.recognitionTimeout) {
        clearTimeout(this.recognitionTimeout);
        this.recognitionTimeout = null;
      }
      
      // Arrêter la reconnaissance
      if (this.recognition) {
        try {
          this.recognition.stop();
        } catch (error) {
          console.error('Erreur lors de l\'arrêt de la reconnaissance vocale:', error);
        }
        
        // Nettoyer les références
        this.recognition = null;
      }
      
      this.isListening = false;
    },
    
    processVoiceCommand(text) {
      let commandFound = false;
      
      // Rechercher dans le mappage des commandes
      for (const [phrase, command] of Object.entries(this.commandsMap)) {
        if (text.includes(phrase)) {
          console.log(`Commande vocale détectée: "${phrase}" => ${command}`);
          this.sendCommand(command);
          commandFound = true;
          break;
        }
      }
      
      if (!commandFound) {
        console.log('Aucune commande reconnue dans:', text);
      }
    },
    
    // Méthodes de contrôle gestuel
    async toggleGestureRecognition() {
      this.isGestureLoading = true;
      
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
        this.isGestureLoading = false;
      }
    },
    
    async checkGestureStatus() {
      try {
        const response = await gestureService.getGestureStatus();
        this.gestureStatus = response.data;
        this.isGestureEnabled = response.data.is_running;
      } catch (error) {
        console.error('Erreur lors de la récupération du statut de la reconnaissance:', error);
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
    },
    
    // Méthodes de contrôle par vision
    toggleFaceRecognitionSection() {
      this.faceRecognitionExpanded = !this.faceRecognitionExpanded;
    },
    
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    
    onDragOver(event) {
      this.isDragging = true;
    },
    
    onDragLeave(event) {
      this.isDragging = false;
    },
    
    onDrop(event) {
      this.isDragging = false;
      
      if (event.dataTransfer.files.length) {
        this.handleFile(event.dataTransfer.files[0]);
      }
    },
    
    onFileSelected(event) {
      if (event.target.files.length) {
        this.handleFile(event.target.files[0]);
      }
    },
    
    handleFile(file) {
      // Vérifier le type de fichier
      const acceptedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
      
      if (!acceptedTypes.includes(file.type)) {
        alert('Format de fichier non supporté. Veuillez utiliser JPG, PNG ou WEBP.');
        return;
      }
      
      // Vérifier la taille du fichier (max 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        alert('Le fichier est trop volumineux. Taille maximale: 5MB');
        return;
      }
      
      // Prévisualiser l'image
      this.selectedFile = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewImage = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    removeImage() {
      this.previewImage = null;
      this.selectedFile = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },
    
    savePerson() {
      if (!this.canSavePerson) return;
      
      // Créer un nouvel objet personne
      const newPerson = {
        id: Date.now(),
        name: this.personName,
        relation: this.personRelation,
        image: this.previewImage,
        dateAdded: new Date().toISOString()
      };
      
      // Ajouter à la liste
      this.people.unshift(newPerson);
      
      // Sauvegarder dans le localStorage
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      storedPeople.unshift(newPerson);
      localStorage.setItem('recognitionPeople', JSON.stringify(storedPeople));
      
      // Réinitialiser le formulaire
      this.resetForm();
      
      // Notification de succès
      this.$notify && this.$notify.success('Personne ajoutée avec succès');
    },
    
    resetForm() {
      this.removeImage();
      this.personName = '';
      this.personRelation = 'family';
    },
    
    loadPeople() {
      // Récupérer du localStorage
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      this.people = storedPeople;
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
  background-color: #e74c3c;
}

.connection-status.connected .status-indicator {
  background-color: #27ae60;
  box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.3);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 1.5rem;
}

.face-tracking-section {
  margin-top: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h4 {
  margin: 0;
  color: var(--text-color);
  font-size: 1.1rem;
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

/* Camera Feed */
.camera-content {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  background-color: #1e1e1e;
  overflow: hidden;
}

.camera-content img {
  width: 100%;
  height: 100%;
  min-height: 400px;
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

/* Controls */
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

.empty-photo {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--light-gray);
  color: var(--medium-gray);
  font-size: 2rem;
}

/* Control Modes Section */
.control-modes {
  border-top: 3px solid var(--primary-color);
}

.mode-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.mode-btn {
  padding: 0.4rem 0.8rem;
  background-color: var(--light-gray);
  color: var(--dark-gray);
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.mode-btn:hover {
  background-color: rgba(52, 152, 219, 0.2);
  color: var(--primary-color);
}

.mode-btn.active {
  background-color: var(--primary-color);
  color: white;
}

.control-content {
  padding: 1.5rem;
}

.control-panel {
  min-height: 300px;
}

/* Keyboard Control */
.keyboard-instructions {
  background-color: var(--light-gray);
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
}

.keyboard-instructions h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.key-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.key-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.key-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.key {
  width: 40px;  /* Taille standard pour la plupart des touches */
  height: 40px;
  background-color: white;
  border: 1px solid var(--medium-gray);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  box-shadow: 0 2px 0 var(--medium-gray);
  font-size: 0.9rem;
}

.key-label {
  font-size: 0.9rem;
  color: var(--text-color);
}

.key-item:has(.key:contains("Space")) .key {
  width: 80px;  /* Élargir la touche espace */
  font-size: 0.85rem;  /* Réduire légèrement la taille de police */
}

/* Pour les navigateurs qui ne supportent pas :has ou :contains */
.key-space {
  width: 80px !important;
}

.keyboard-toggle {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

/* Voice Control */
.voice-control {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.voice-recognition {
  background-color: var(--light-gray);
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
}

.recognition-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.recognition-header h4 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-color);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
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

.mic-visualizer {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.mic-icon {
  width: 64px;
  height: 64px;
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.pulse {
  animation: pulse 2s infinite;
}

.wave-container {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 40px;
}

.wave {
  width: 4px;
  height: 5px;
  background-color: var(--primary-color);
  border-radius: 2px;
}

.wave-container.active .wave {
  animation: wave 1.2s infinite ease-in-out;
}

.wave-container.active .wave:nth-child(2) {
  animation-delay: 0.2s;
}

.wave-container.active .wave:nth-child(3) {
  animation-delay: 0.4s;
}

.wave-container.active .wave:nth-child(4) {
  animation-delay: 0.6s;
}

.wave-container.active .wave:nth-child(5) {
  animation-delay: 0.8s;
}

.recognized-text {
  background-color: white;
  padding: 1rem;
  border-radius: var(--border-radius-md);
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 500;
  color: var(--text-color);
}

.btn-speech {
  display: block;
  width: 100%;
  padding: 0.8rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.btn-active, .btn-inactive {
  padding: 0.8rem 1rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.btn-inactive {
  background-color: var(--primary-color);
  color: white;
}

.btn-active {
  background-color: #e74c3c;
  color: white;
}

.voice-commands {
  background-color: white;
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
  box-shadow: var(--card-shadow);
}

.voice-commands h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-color);
  border-bottom: 1px solid var(--light-gray);
  padding-bottom: 0.5rem;
}

.commands-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.command-category h5 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: var(--primary-color);
  font-size: 1rem;
}

.command-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--light-gray);
}

.command-item:last-child {
  border-bottom: none;
}

.command-phrase {
  font-weight: 500;
  color: var(--text-color);
}

.command-action {
  font-size: 0.9rem;
  color: var(--dark-gray);
}

/* Gesture Control */
.gesture-control {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.gesture-status {
  background-color: var(--light-gray);
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.btn-large {
  padding: 0.8rem 1.2rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-width: 250px;
}

.btn-large:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.gesture-guide {
  background-color: white;
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
  box-shadow: var(--card-shadow);
}

.gesture-guide h4 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: var(--text-color);
  border-bottom: 1px solid var(--light-gray);
  padding-bottom: 0.5rem;
}

.gestures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.gesture-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-sm);
  transition: all 0.2s ease;
}

.gesture-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.gesture-image {
  width: 60px;
  height: 60px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.gesture-description h5 {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  color: var(--text-color);
}

.gesture-description p {
  margin: 0;
  font-size: 0.8rem;
  color: var(--primary-color);
}

/* Vision Control */
.vision-control {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.vision-options {
  background-color: var(--light-gray);
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
}

.option-group {
  margin-bottom: 1.5rem;
}

.option-group:last-child {
  margin-bottom: 0;
}

.option-group h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.option-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn-outline {
  padding: 0.6rem 1rem;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
  background-color: transparent;
  border-radius: var(--border-radius-sm);
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-outline:hover {
  background-color: var(--primary-color);
  color: white;
}

.btn-outline.active {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--dark-gray);
}

.face-recognition-toggle {
  display: flex;
  justify-content: center;
}

.face-recognition {
  background-color: white;
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
  box-shadow: var(--card-shadow);
  margin-top: 1.5rem;
}

.upload-area {
  border: 2px dashed var(--medium-gray);
  border-radius: var(--border-radius-md);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  position: relative;
  transition: all 0.3s ease;
  background-color: var(--light-gray);
}

.upload-area.drag-over {
  background-color: rgba(52, 152, 219, 0.05);
  border-color: var(--primary-color);
}

.upload-area.has-image {
  padding: 1rem;
}

.upload-placeholder {
  text-align: center;
}

.upload-placeholder i {
  font-size: 2rem;
  color: var(--medium-gray);
  margin-bottom: 1rem;
}

.upload-placeholder p {
  color: var(--dark-gray);
  margin-bottom: 0.5rem;
}

.browse-link {
  color: var(--primary-color);
  cursor: pointer;
  text-decoration: underline;
}

.file-input {
  display: none;
}

.preview-container {
  position: relative;
  width: 100%;
  max-width: 200px;
}

.preview-image {
  width: 100%;
  height: auto;
  border-radius: var(--border-radius-sm);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-remove-image {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: var(--accent-color);
  color: white;
  border: 2px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  padding: 0;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.person-form {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.form-group {
  flex: 1;
}

.person-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--medium-gray);
  border-radius: var(--border-radius-sm);
  font-size: 1rem;
}

.form-controls {
  display: flex;
  align-items: flex-end;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-dark);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Animations */
@keyframes pulse {
  0% {
    opacity: 1;
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.4);
  }
  70% {
    opacity: 0.9;
    box-shadow: 0 0 0 10px rgba(52, 152, 219, 0);
  }
  100% {
    opacity: 1;
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0);
  }
}

@keyframes wave {
  0%, 100% {
    height: 5px;
  }
  50% {
    height: 32px;
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
  
  .key-grid {
    flex-direction: column;
  }
  
  .gestures-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .person-form {
    flex-direction: column;
  }
}

@media screen and (max-width: 480px) {
  .mode-selector {
    flex-direction: column;
  }
  
  .mode-btn {
    width: 100%;
  }
  
  .gestures-grid {
    grid-template-columns: 1fr;
  }
}

.header-actions {
  display: flex;
  gap: 1rem;
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
  padding: 0.4rem 0.8rem;
  border-radius: var(--border-radius-sm);
  transition: all 0.2s ease;
}

.btn-text:hover:not(:disabled) {
  background-color: rgba(52, 152, 219, 0.1);
}

.btn-text:disabled {
  color: var(--medium-gray);
  cursor: not-allowed;
}

.control-modes-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.mode-card {
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.mode-card.mode-active {
  background-color: white;
  border-color: var(--primary-color);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.1);
}

.mode-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background-color: rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.mode-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.mode-title i {
  color: var(--primary-color);
  font-size: 1.2rem;
}

.mode-title h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--text-color);
  font-weight: 600;
}

.mode-toggle {
  display: flex;
  align-items: center;
}

.mode-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.mode-not-available {
  padding: 1.5rem;
  color: var(--dark-gray);
  text-align: center;
  font-style: italic;
}

.mode-not-available p {
  margin: 0;
}

.mode-actions {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

/* Switch toggle */
.switch {
  position: relative;
  display: inline-block;
  width: 52px;
  height: 26px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--medium-gray);
  transition: all 0.3s ease;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

input:checked + .slider {
  background-color: var(--primary-color);
}

input:focus + .slider {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(52, 152, 219, 0.2);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

input:checked + .slider:before {
  animation: switch-on 0.3s ease-out;
}


input:disabled + .slider {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--light-gray);
}

input:disabled + .slider:before {
  background-color: #e0e0e0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

@keyframes switch-on {
  0% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(28px);
  }
  100% {
    transform: translateX(26px);
  }
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.switch:hover .slider:before {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
}

.switch:hover input:checked + .slider {
  background-color: #2980b9; /* Version légèrement plus foncée du primary-color */
}

.switch:hover input:disabled + .slider {
  /* Pas de changement sur le hover lorsque désactivé */
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
}

/* Accessibilité - focus visible */
.switch input:focus-visible + .slider {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Key grid simplifié */
.key-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.key-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.key-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.key {
  width: 30px;
  height: 30px;
  font-size: 0.8rem;
}

.key-label {
  font-size: 0.8rem;
}

/* Voice control */
.voice-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.mic-visualizer {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40px;
  width: 100%;
}

.btn-medium {
  padding: 0.6rem 1rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

/* Gesture control */
.gestures-mini-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
}

.gesture-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.gesture-image {
  width: 40px;
  height: 40px;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.gesture-item p {
  font-size: 0.75rem;
  margin: 0;
}

/* Vision control */
.vision-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.vision-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

/* Responsive design */
@media screen and (max-width: 992px) {
  .control-modes-grid {
    grid-template-columns: 1fr;
  }
  
  .gestures-mini-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-text {
    width: 100%;
    justify-content: center;
  }
  
  .vision-status {
    flex-direction: column;
  }
}


</style>