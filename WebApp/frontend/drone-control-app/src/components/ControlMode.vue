<template>
  <div class="control-module">
    <div class="control-header">
      <h2 class="control-title">{{ mode }} Control</h2>
      <div class="status-indicator" :class="{ 'is-active': keyboardEnabled }">
        <i class="fas" :class="keyboardEnabled ? 'fa-check-circle' : 'fa-times-circle'"></i>
        <span>{{ keyboardEnabled ? 'Contrôle clavier actif' : 'Contrôle clavier désactivé' }}</span>
      </div>
    </div>

    <div class="control-card keyboard-control">
      <div class="card-header">
        <h3><i class="fas fa-keyboard"></i> Contrôle Clavier</h3>
        <button @click="toggleKeyboardControls" :class="{ 'btn-active': keyboardEnabled, 'btn-inactive': !keyboardEnabled }">
          {{ keyboardEnabled ? 'Désactiver' : 'Activer' }}
        </button>
      </div>
      
      <div v-if="showKeyboardInstructions && keyboardEnabled" class="keyboard-instructions">
        <div class="instruction-grid">
          <div class="instruction-item">
            <div class="key-group">
              <span class="key">↑</span>
              <span class="key">↓</span>
              <span class="key">←</span>
              <span class="key">→</span>
            </div>
            <span class="instruction-label">Monter/Descendre/Gauche/Droite</span>
          </div>
          
          <div class="instruction-item">
            <div class="key-group">
              <span class="key">Z</span>
              <span class="key">Q</span>
              <span class="key">S</span>
              <span class="key">D</span>
            </div>
            <span class="instruction-label">Avancer/Gauche/Reculer/Droite</span>
          </div>
          
          <div class="instruction-item">
            <span class="key">A</span>
            <span class="instruction-label">Décollage</span>
          </div>
          
          <div class="instruction-item">
            <span class="key">E</span>
            <span class="instruction-label">Atterrissage</span>
          </div>
          
          <div class="instruction-item">
            <span class="key key-long">P</span>
            <span class="instruction-label">Arrêt d'urgence</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mode-specific control interfaces -->
    <div v-if="mode === 'Voice'" class="control-card">
      <div class="card-header">
        <h3><i class="fas fa-microphone"></i> Commandes Vocales</h3>
      </div>

      <div class="voice-command-groups">
        <div class="command-group">
          <h4>1. Commandes de Base</h4>
          <div class="commands-grid">
            <div class="command-item">
              <div class="command-key">Décollage</div>
              <button @click="sendCommand('takeoff')" class="btn-command">
                <i class="fas fa-rocket"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Attérissage</div>
              <button @click="sendCommand('land')" class="btn-command">
                <i class="fas fa-plane-arrival"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="command-group">
          <h4>2. Déplacements</h4>
          <div class="commands-grid">
            <div class="command-item">
              <div class="command-key">Avance</div>
              <button @click="sendCommand('moveForward')" class="btn-command">
                <i class="fas fa-arrow-up"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Recule</div>
              <button @click="sendCommand('moveBackward')" class="btn-command">
                <i class="fas fa-arrow-down"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Gauche</div>
              <button @click="sendCommand('moveLeft')" class="btn-command">
                <i class="fas fa-arrow-left"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Droite</div>
              <button @click="sendCommand('moveRight')" class="btn-command">
                <i class="fas fa-arrow-right"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="command-group">
          <h4>3. Altitude et Rotation</h4>
          <div class="commands-grid">
            <div class="command-item">
              <div class="command-key">Monte</div>
              <button @click="sendCommand('moveUp')" class="btn-command">
                <i class="fas fa-level-up-alt"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Descend</div>
              <button @click="sendCommand('moveDown')" class="btn-command">
                <i class="fas fa-level-down-alt"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Tourne à Gauche</div>
              <button @click="sendCommand('rotateLeft')" class="btn-command">
                <i class="fas fa-undo"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Tourne à Droite</div>
              <button @click="sendCommand('rotateRight')" class="btn-command">
                <i class="fas fa-redo"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="command-group">
          <h4>4. Loopings</h4>
          <div class="commands-grid">
            <div class="command-item">
              <div class="command-key">Looping en avant</div>
              <button @click="sendCommand('flipForward')" class="btn-command">
                <i class="fas fa-sync-alt rotate-y"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Looping en arrière</div>
              <button @click="sendCommand('flipBackward')" class="btn-command">
                <i class="fas fa-sync-alt rotate-y-reverse"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Looping à Gauche</div>
              <button @click="sendCommand('flipLeft')" class="btn-command">
                <i class="fas fa-sync-alt rotate-x-reverse"></i>
              </button>
            </div>
            <div class="command-item">
              <div class="command-key">Looping à Droite</div>
              <button @click="sendCommand('flipRight')" class="btn-command">
                <i class="fas fa-sync-alt rotate-x"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="command-group">
          <h4>5. Arrêt</h4>
          <div class="commands-grid">
            <div class="command-item emergency">
              <div class="command-key">Stop</div>
              <button @click="sendCommand('emergencyStop')" class="btn-command btn-emergency">
                <i class="fas fa-stop-circle"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="recognitionEnabled" class="voice-recognition">
        <div class="recognition-header">
          <h4>Reconnaissance Vocale</h4>
          <div class="status-indicator" :class="{ 'is-active': isListening }">
            <i class="fas" :class="isListening ? 'fa-microphone' : 'fa-microphone-slash'"></i>
            <span>{{ isListening ? 'Écoute active' : 'Écoute inactive' }}</span>
          </div>
        </div>
        
        <div class="mic-visualizer">
          <div class="mic-icon" :class="{ 'pulse': isListening }">
            <i class="fas fa-microphone"></i>
          </div>
          <div class="wave-container" :class="{ 'active': isListening }">
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
          </div>
        </div>
        
        <div v-if="recognizedText" class="recognized-text">
          Texte reconnu: "{{ recognizedText }}"
        </div>
        
        <button @click="toggleSpeechRecognition" class="btn-speech" :class="{ 'btn-active': isListening, 'btn-inactive': !isListening }">
          <i :class="isListening ? 'fas fa-stop' : 'fas fa-microphone'"></i>
          {{ isListening ? 'Arrêter l\'écoute' : 'Démarrer l\'écoute' }}
        </button>
      </div>
      
      <div v-else class="voice-recognition-unavailable">
        <div class="info-message">
          <i class="fas fa-exclamation-circle"></i>
          <p>La reconnaissance vocale n'est pas disponible sur ce navigateur. Veuillez utiliser Chrome, Edge ou Safari pour accéder à cette fonctionnalité.</p>
        </div>
      </div>
    </div>
    
    <div v-if="mode === 'Gesture'" class="control-card">
      <div class="card-header">
        <h3><i class="fas fa-hand-paper"></i> Contrôle Gestuel</h3>
      </div>
      
      <div class="gesture-display">
        <div class="gesture-instructions">
          <div class="gesture-item">
            <i class="fas fa-hand-paper"></i>
            <span>Main ouverte = Planer</span>
          </div>
          <div class="gesture-item">
            <i class="fas fa-thumbs-up"></i>
            <span>Pouce vers le haut = Monter</span>
          </div>
          <div class="gesture-item">
            <i class="fas fa-thumbs-down"></i>
            <span>Pouce vers le bas = Descendre</span>
          </div>
          <div class="gesture-item">
            <i class="fas fa-fist-raised"></i>
            <span>Poing fermé = Arrêt d'urgence</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="mode === 'Vision'" class="control-card">
      <div class="card-header">
        <h3><i class="fas fa-eye"></i> Vision et Suivi</h3>
      </div>
      
      <div class="vision-controls">
        <div class="camera-feed">
          <div class="detection-overlay">
            <!-- Rectangles de détection simulés -->
            <div class="detection-box person"></div>
            <div class="detection-box object"></div>
          </div>
        </div>
        
        <div class="vision-options">
          <div class="option-group">
            <h4>Mode de suivi</h4>
            <div class="option-buttons">
              <button class="btn-outline active">
                <i class="fas fa-user"></i> Personne
              </button>
              <button class="btn-outline">
                <i class="fas fa-cube"></i> Objet
              </button>
              <button class="btn-outline">
                <i class="fas fa-map-marker-alt"></i> Point GPS
              </button>
            </div>
          </div>
          
          <div class="option-group">
            <h4>Distance de suivi</h4>
            <input type="range" min="1" max="10" value="3" class="slider">
            <div class="range-labels">
              <span>Proche</span>
              <span>Éloigné</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import keyboardControls from '../mixins/keyboardControls';

export default {
  props: {
    mode: String,
  },
  mixins: [keyboardControls],
  data() {
    return {
      showKeyboardInstructions: true,
      isListening: false,
      recognizedText: '',
      recognitionEnabled: false,
      // Mappage des commandes vocales (français)
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
      recognitionTimeout: null
    };
  },
  watch: {
    // Surveiller les changements de mode pour arrêter la reconnaissance vocale
    mode(newVal, oldVal) {
      if (newVal !== oldVal && this.isListening) {
        // Si on change de mode et que la reconnaissance est active, on l'arrête
        this.stopSpeechRecognition();
      }
    }
  },
  mounted() {
    this.enableKeyboardControls();
    // Vérifier si le navigateur supporte la reconnaissance vocale
    this.checkSpeechRecognitionSupport();
  },
  methods: {
    sendCommand(command) {
      console.log(`Commande envoyée: ${command}`);
      if (this.executeCommand) {
        this.executeCommand(command);
      } else {
        console.warn(`La méthode executeCommand n'est pas disponible. Commande: ${command}`);
      }
    },
    
    toggleKeyboardControls() {
      if (this.keyboardEnabled) {
        this.disableKeyboardControls();
      } else {
        this.enableKeyboardControls();
      }
    },
    
    checkSpeechRecognitionSupport() {
      // Vérifier si le navigateur supporte l'API Web Speech
      this.recognitionEnabled = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
      
      if (!this.recognitionEnabled && this.mode === 'Voice') {
        console.warn('La reconnaissance vocale n\'est pas supportée par ce navigateur.');
      }
    },
    
    toggleSpeechRecognition() {
      if (this.keyboardEnabled) {
        this.disableKeyboardControls();
      } else {
        this.enableKeyboardControls();
      }
      if (!this.recognitionEnabled) {
        alert('La reconnaissance vocale n\'est pas disponible sur ce navigateur.');
        return;
      }
      
      if (this.isListening) {
        this.stopSpeechRecognition();
      } else {
        this.startSpeechRecognition();
      }
      this.$notify && this.$notify.info(
        this.keyboardEnabled ? 'Contrôles clavier activés' : 'Contrôles clavier désactivés'
      );
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
          // et si le composant est toujours monté (vérification avec this.isListening)
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
    }
  },
  beforeUnmount() {
    console.log('Component will unmount - cleaning up...');
    
    // Arrêter la reconnaissance vocale si elle est active
    this.stopSpeechRecognition();
    
    // Nettoyer les écouteurs d'événements du clavier
    this.disableKeyboardControls();
  }
};
</script>
  
<style scoped>
.control-module {
  max-width: 1000px;
  margin: 0 auto;
}

.control-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--light-gray);
}

.control-title {
  margin: 0;
  color: var(--primary-color);
  font-size: 1.8rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: var(--light-gray);
  border-radius: 40px;
  font-size: 0.9rem;
  color: var(--dark-gray);
  transition: all 0.3s ease;
}

.status-indicator.is-active {
  background-color: var(--success-color);
  color: white;
}

.status-indicator i {
  margin-right: 0.5rem;
  font-size: 1rem;
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
}

.card-header h3 i {
  margin-right: 0.5rem;
  color: var(--primary-color);
}

.keyboard-control {
  border-top: 4px solid var(--primary-color);
}

.btn-active, .btn-inactive {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.btn-active {
  background-color: var(--success-color);
  color: white;
}

.btn-inactive {
  background-color: var(--medium-gray);
  color: var(--text-color);
}

.keyboard-instructions {
  padding: 1.5rem;
}

.instruction-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.instruction-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-sm);
}

.key-group {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.key {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background-color: white;
  border: 1px solid var(--medium-gray);
  border-radius: var(--border-radius-sm);
  box-shadow: 0 2px 0 var(--medium-gray);
  font-weight: bold;
  color: var(--text-color);
}

.key-long {
  width: 64px;
}

.instruction-label {
  font-size: 0.9rem;
  color: var(--text-color);
}

/* Voice command styles */
.voice-command-groups {
  padding: 1.5rem;
}

.command-group {
  margin-bottom: 2rem;
}

.command-group h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-color);
  font-size: 1.1rem;
  border-bottom: 1px solid var(--light-gray);
  padding-bottom: 0.5rem;
}

.commands-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

.command-item {
  padding: 1rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: all 0.2s ease;
}

.command-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.command-item.emergency {
  background-color: #ffedea;
}

.command-key {
  font-weight: 500;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.btn-command {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: 1px solid var(--medium-gray);
  color: var(--primary-color);
  font-size: 1.1rem;
  transition: all 0.2s ease;
}

.btn-command:hover {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
  transform: scale(1.1);
}

.btn-emergency {
  color: #e74c3c;
  border-color: #e74c3c;
}

.btn-emergency:hover {
  background-color: #e74c3c;
  color: white;
}

/* Speech recognition styles */
.voice-recognition {
  padding: 1.5rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  margin: 0 1.5rem 1.5rem;
}

.voice-recognition-unavailable {
  padding: 1.5rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  margin: 0 1.5rem 1.5rem;
}

.info-message {
  display: flex;
  align-items: flex-start;
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 1rem;
  border-radius: var(--border-radius-sm);
}

.info-message i {
  color: #ffc107;
  font-size: 1.5rem;
  margin-right: 1rem;
}

.info-message p {
  margin: 0;
  color: #856404;
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

@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.7);
  }
  
  70% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(52, 152, 219, 0);
  }
  
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0);
  }
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

@keyframes wave {
  0%, 100% {
    height: 5px;
  }
  50% {
    height: 32px;
  }
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

.btn-inactive {
  background-color: var(--primary-color);
  color: white;
}

.btn-active {
  background-color: #e74c3c;
  color: white;
}

.btn-speech:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Gesture interface */
.gesture-display {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.gesture-instructions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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
}

.gesture-item i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

/* Vision interface */
.vision-controls {
  padding: 1.5rem;
}

.camera-feed {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%;
  overflow: hidden;
  border-radius: var(--border-radius-md);
  background-color: black;
  margin-bottom: 1.5rem;
}

.camera-feed img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detection-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.detection-box {
  position: absolute;
  border: 2px solid;
  border-radius: 4px;
}

.detection-box.person {
  top: 20%;
  left: 30%;
  width: 15%;
  height: 60%;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
}

.detection-box.object {
  top: 40%;
  left: 60%;
  width: 10%;
  height: 15%;
  border-color: var(--warning-color);
  box-shadow: 0 0 0 2px rgba(243, 156, 18, 0.3);
}

.vision-options {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.option-group {
  flex: 1;
  min-width: 250px;
}

.option-group h4 {
  margin-bottom: 0.5rem;
  color: var(--dark-gray);
}

.option-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn-outline {
  padding: 0.6rem 1rem;
  border: 1px solid var(--medium-gray);
  background-color: white;
  color: var(--text-color);
  border-radius: var(--border-radius-sm);
  transition: all 0.2s ease;
}

.btn-outline:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.btn-outline.active {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  background: var(--light-gray);
  outline: none;
  border-radius: 4px;
  margin: 1rem 0 0.5rem 0;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-color);
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-color);
  cursor: pointer;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--dark-gray);
}

/* Rotation icons */
.rotate-x {
  transform: rotate(90deg);
}

.rotate-x-reverse {
  transform: rotate(-90deg);
}

.rotate-y {
  transform: rotate(0deg);
}

.rotate-y-reverse {
  transform: rotate(180deg);
}

/* Media queries for responsive design */
@media screen and (max-width: 768px) {
  .control-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .status-indicator {
    margin-top: 1rem;
  }
  
  .vision-options {
    flex-direction: column;
  }
  
  .option-buttons {
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .commands-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 480px) {
  .commands-grid {
    grid-template-columns: 1fr;
  }
  
  .instruction-grid {
    grid-template-columns: 1fr;
  }
  
  .gesture-instructions {
    grid-template-columns: 1fr;
  }
}
</style>