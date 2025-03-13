<template>
  <div class="drone-camera">
    <div class="camera-container">
      <div v-if="connected" class="camera-feed">
        <img :src="currentFrame" alt="Flux vidéo du drone" class="camera-frame" />
        <div class="camera-overlay">
          <div class="status-indicator">
            <span class="status-dot" :class="{ 'connected': connected }"></span>
            <span class="status-text">{{ connected ? 'Connecté' : 'Déconnecté' }}</span>
          </div>
          <div class="camera-controls">
            <button @click="capturePhoto" class="control-btn photo-btn">
              <i class="fas fa-camera"></i>
            </button>
            <button @click="toggleRecording" class="control-btn record-btn" :class="{ 'recording': isRecording }">
              <i :class="isRecording ? 'fas fa-stop' : 'fas fa-video'"></i>
            </button>
          </div>
        </div>
        <div v-if="isRecording" class="recording-indicator">
          <span class="record-dot"></span> REC {{ recordingTime }}
        </div>
      </div>
      <div v-else class="camera-placeholder">
        <i class="fas fa-video-slash"></i>
        <p>Caméra déconnectée</p>
        <button @click="connectCamera" class="connect-btn">
          <i class="fas fa-plug"></i> Connecter la caméra
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import io from 'socket.io-client';
import droneSimulationService from '../services/droneSimulationService';

export default {
  name: 'DroneCamera',
  props: {
    droneId: {
      type: String,
      default: 'simulation'
    },
    autoConnect: {
      type: Boolean,
      default: true
    },
    useLocalSimulation: {
      type: Boolean,
      default: false
    }
  },
  
  setup(props, { emit }) {
    const socket = ref(null);
    const connected = ref(false);
    const currentFrame = ref('');
    const isRecording = ref(false);
    const recordingTime = ref('00:00');
    const recordingInterval = ref(null);
    const recordingStartTime = ref(0);
    const capturedPhotos = ref([]);
    const useSimulation = ref(props.useLocalSimulation);
    
    // Gestion de la connexion Socket.IO
    const connectSocket = () => {
      // Si on utilise la simulation locale, on ne connecte pas le socket
      if (useSimulation.value) {
        console.log('Using local simulation instead of Socket.IO');
        setupLocalSimulation();
        return;
      }
      
      const socketUrl = process.env.VUE_APP_SOCKET_URL || 'http://localhost:3000';
      
      try {
        socket.value = io(socketUrl);
        
        socket.value.on('connect', () => {
          console.log('Socket.IO connected');
          // Si le socket est connecté mais pas la caméra, on lance la connexion
          if (props.autoConnect && !connected.value) {
            connectCamera();
          }
        });
        
        socket.value.on('video_frame', (frameData) => {
          // Le serveur nous envoie une image en base64
          currentFrame.value = `data:image/jpeg;base64,${frameData}`;
        });
        
        socket.value.on('camera_status', (status) => {
          connected.value = status.connected;
          if (!status.connected) {
            stopRecording();
          }
        });
        
        socket.value.on('disconnect', () => {
          console.log('Socket.IO disconnected');
          connected.value = false;
          stopRecording();
        });
        
        socket.value.on('connect_error', (error) => {
          console.error('Socket.IO connection error:', error);
          
          // Fallback sur la simulation locale en cas d'erreur
          console.log('Falling back to local simulation');
          useSimulation.value = true;
          setupLocalSimulation();
        });
      } catch (error) {
        console.error('Error creating socket connection:', error);
        
        // Fallback sur la simulation locale en cas d'erreur
        console.log('Falling back to local simulation');
        useSimulation.value = true;
        setupLocalSimulation();
      }
    };
    
    // Configuration de la simulation locale
    const setupLocalSimulation = () => {
      // Écouteurs d'événements pour la simulation
      droneSimulationService.addEventListener('video', (data) => {
        currentFrame.value = data.frame;
      });
      
      droneSimulationService.addEventListener('connect', () => {
        if (props.autoConnect && !connected.value) {
          connectCamera();
        }
      });
      
      droneSimulationService.addEventListener('disconnect', () => {
        connected.value = false;
        stopRecording();
      });
      
      // Démarrage des services de simulation
      if (props.autoConnect) {
        droneSimulationService.startLocalVideoSimulation();
        connected.value = true;
        emit('camera-status-change', { connected: true });
      }
    };
    
    // Connecter la caméra (simulation)
    const connectCamera = () => {
      if (useSimulation.value) {
        // Utiliser le service de simulation locale
        droneSimulationService.startLocalVideoSimulation();
        droneSimulationService.startTelemetry();
        connected.value = true;
        emit('camera-status-change', { connected: true });
      } else if (socket.value && socket.value.connected) {
        socket.value.emit('connect_camera', { droneId: props.droneId });
        connected.value = true;
        emit('camera-status-change', { connected: true });
      } else {
        console.error('Socket non connecté');
        // Tentative de reconnexion du socket ou utilisation de la simulation
        connectSocket();
      }
    };
    
    // Déconnecter la caméra
    const disconnectCamera = () => {
      if (useSimulation.value) {
        // Utiliser le service de simulation locale
        droneSimulationService.stopVideoStream();
        droneSimulationService.stopTelemetry();
        connected.value = false;
        stopRecording();
        emit('camera-status-change', { connected: false });
      } else if (socket.value && socket.value.connected) {
        socket.value.emit('disconnect_camera', { droneId: props.droneId });
        connected.value = false;
        stopRecording();
        emit('camera-status-change', { connected: false });
      }
    };
    
    // Capture d'une photo
    const capturePhoto = () => {
      if (!connected.value || !currentFrame.value) return;
      
      let photo;
      
      if (useSimulation.value) {
        // Utiliser le service de simulation pour la capture
        droneSimulationService.captureScreenshot()
          .then(screenshot => {
            photo = {
              id: Date.now(),
              src: screenshot.image,
              timestamp: screenshot.timestamp
            };
            
            completePhotoCapture(photo);
          })
          .catch(error => {
            console.error('Error capturing screenshot:', error);
            // Fallback : utiliser l'image actuelle
            photo = {
              id: Date.now(),
              src: currentFrame.value,
              timestamp: new Date().toISOString()
            };
            
            completePhotoCapture(photo);
          });
      } else {
        // Utiliser l'image actuelle du flux vidéo
        photo = {
          id: Date.now(),
          src: currentFrame.value,
          timestamp: new Date().toISOString()
        };
        
        completePhotoCapture(photo);
        
        // Informer le serveur si nécessaire
        if (socket.value && socket.value.connected) {
          socket.value.emit('capture_photo', { 
            droneId: props.droneId,
            image: currentFrame.value
          });
        }
      }
    };
    
    // Fonction auxiliaire pour terminer la capture photo
    const completePhotoCapture = (photo) => {
      capturedPhotos.value.push(photo);
      emit('photo-captured', photo);
      
      // Notification de capture
      const notification = document.createElement('div');
      notification.className = 'capture-notification';
      notification.innerHTML = '<i class="fas fa-camera"></i> Photo capturée';
      document.body.appendChild(notification);
      
      setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 500);
      }, 1500);
    };
    
    // Gestion de l'enregistrement vidéo
    const toggleRecording = () => {
      if (!connected.value) return;
      
      if (isRecording.value) {
        stopRecording();
      } else {
        startRecording();
      }
    };
    
    const startRecording = () => {
      if (!connected.value) return;
      
      isRecording.value = true;
      recordingStartTime.value = Date.now();
      
      // Mettre à jour le compteur de temps d'enregistrement
      recordingInterval.value = setInterval(() => {
        const elapsedSeconds = Math.floor((Date.now() - recordingStartTime.value) / 1000);
        const minutes = Math.floor(elapsedSeconds / 60).toString().padStart(2, '0');
        const seconds = (elapsedSeconds % 60).toString().padStart(2, '0');
        recordingTime.value = `${minutes}:${seconds}`;
      }, 1000);
      
      // Informer le service ou le serveur du début de l'enregistrement
      if (useSimulation.value) {
        console.log('Starting recording simulation');
        // Dans une implémentation réelle, la simulation pourrait enregistrer les frames
      } else if (socket.value && socket.value.connected) {
        socket.value.emit('start_recording', { droneId: props.droneId });
      }
      
      emit('recording-started');
    };
    
    const stopRecording = () => {
      if (!isRecording.value) return;
      
      isRecording.value = false;
      clearInterval(recordingInterval.value);
      const finalRecordingTime = recordingTime.value;
      recordingTime.value = '00:00';
      
      // Informer le service ou le serveur de la fin de l'enregistrement
      if (useSimulation.value) {
        console.log('Stopping recording simulation');
        // Dans une implémentation réelle, la simulation pourrait sauvegarder l'enregistrement
      } else if (socket.value && socket.value.connected) {
        socket.value.emit('stop_recording', { droneId: props.droneId });
      }
      
      emit('recording-stopped', { 
        duration: finalRecordingTime,
        timestamp: new Date().toISOString()
      });
    };
    
    // Envoi d'une commande au drone
    const sendCommand = (command, params = {}) => {
      if (!connected.value) return Promise.reject(new Error('Camera not connected'));
      
      if (useSimulation.value) {
        // Utiliser le service de simulation
        return droneSimulationService.sendCommand(command, params);
      } else if (socket.value && socket.value.connected) {
        // Utiliser le socket pour envoyer la commande
        return new Promise((resolve, reject) => {
          socket.value.emit('drone_command', { 
            droneId: props.droneId, 
            command, 
            params 
          });
          
          // Attendre une réponse pendant 3 secondes max
          const timeout = setTimeout(() => {
            socket.value.off('drone_command_result');
            reject(new Error('Command timeout'));
          }, 3000);
          
          socket.value.once('drone_command_result', (result) => {
            clearTimeout(timeout);
            resolve(result);
          });
        });
      } else {
        return Promise.reject(new Error('No connection method available'));
      }
    };
    
    onMounted(() => {
      if (useSimulation.value) {
        setupLocalSimulation();
      } else {
        connectSocket();
      }
    });
    
    onBeforeUnmount(() => {
      if (isRecording.value) {
        stopRecording();
      }
      
      if (useSimulation.value) {
        droneSimulationService.stopVideoStream();
        droneSimulationService.stopTelemetry();
      }
      
      if (socket.value && socket.value.connected) {
        socket.value.disconnect();
      }
    });
    
    return {
      connected,
      currentFrame,
      isRecording,
      recordingTime,
      capturedPhotos,
      connectCamera,
      disconnectCamera,
      capturePhoto,
      toggleRecording,
      sendCommand
    };
  }
};
</script>

<style scoped>
.drone-camera {
  width: 100%;
  margin-bottom: 1.5rem;
}

.camera-container {
  width: 100%;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  background-color: #000;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.camera-feed {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
  background-color: #111;
}

.camera-frame {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1rem;
  color: white;
  pointer-events: none;
}

.camera-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  pointer-events: auto;
}

.control-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  border: 2px solid white;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover {
  transform: scale(1.1);
  background-color: rgba(0, 0, 0, 0.7);
}

.record-btn.recording {
  background-color: rgba(255, 0, 0, 0.7);
  animation: pulse 2s infinite;
}

.photo-btn:active {
  transform: scale(0.9);
  background-color: rgba(255, 255, 255, 0.3);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  width: fit-content;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #f44336;
}

.status-dot.connected {
  background-color: #4caf50;
}

.status-text {
  font-size: 0.8rem;
  font-weight: 500;
}

.recording-indicator {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: rgba(255, 0, 0, 0.7);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  font-size: 0.9rem;
}

.record-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
  animation: blink 1s infinite;
}

.camera-placeholder {
  width: 100%;
  aspect-ratio: 16/9;
  background-color: #1e1e1e;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.camera-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.camera-placeholder p {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.connect-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.connect-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.capture-notification {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 1000;
  transition: opacity 0.5s ease;
}

.capture-notification.fade-out {
  opacity: 0;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 0, 0, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
  }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>