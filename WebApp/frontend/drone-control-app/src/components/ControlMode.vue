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
                <span class="key">W</span>
                <span class="key">A</span>
                <span class="key">S</span>
                <span class="key">D</span>
              </div>
              <span class="instruction-label">Avancer/Gauche/Reculer/Droite</span>
            </div>
            
            <div class="instruction-item">
              <span class="key">T</span>
              <span class="instruction-label">Décollage</span>
            </div>
            
            <div class="instruction-item">
              <span class="key">L</span>
              <span class="instruction-label">Atterrissage</span>
            </div>
            
            <div class="instruction-item">
              <span class="key key-long">ESC</span>
              <span class="instruction-label">Arrêt d'urgence</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Mode-specific control interfaces -->
      <div v-if="mode === 'voice'" class="control-card">
        <div class="card-header">
          <h3><i class="fas fa-microphone"></i> Commandes Vocales</h3>
        </div>
        
        <div class="control-buttons">
          <button class="btn-primary" @click="sendCommand('takeoff')">
            <i class="fas fa-rocket"></i> Décollage
          </button>
          <button class="btn-warning" @click="sendCommand('land')">
            <i class="fas fa-plane-arrival"></i> Atterrissage
          </button>
          <button class="btn-info" @click="sendCommand('moveForward')">
            <i class="fas fa-arrow-up"></i> Avancer
          </button>
        </div>
        
        <div class="voice-recognition">
          <div class="mic-visualizer">
            <div class="mic-icon pulse">
              <i class="fas fa-microphone"></i>
            </div>
            <div class="wave-container">
              <div class="wave"></div>
              <div class="wave"></div>
              <div class="wave"></div>
            </div>
          </div>
          <div class="voice-status">Dites "Décoller" pour démarrer le vol</div>
        </div>
      </div>
      
      <div v-if="mode === 'gesture'" class="control-card">
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
      
      <div v-if="mode === 'vision'" class="control-card">
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
  import keyboardControls from '../mixins/keyboardControls';
  
  export default {
    props: {
      mode: String,
    },
    mixins: [keyboardControls],
    data() {
      return {
        showKeyboardInstructions: true
      };
    },
    methods: {
      sendCommand(command) {
        alert(`Command sent: ${command}`);
        // Remplacer par des appels API réels pour contrôler le drone
      },
      toggleKeyboardControls() {
        if (this.keyboardEnabled) {
          this.disableKeyboardControls();
        } else {
          this.enableKeyboardControls();
        }
      }
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
  
  .control-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1.5rem;
  }
  
  .btn-primary, .btn-warning, .btn-info {
    padding: 0.8rem 1.5rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 150px;
    justify-content: center;
  }
  
  .btn-primary {
    background-color: var(--primary-color);
    color: white;
  }
  
  .btn-warning {
    background-color: var(--warning-color);
    color: white;
  }
  
  .btn-info {
    background-color: var(--light-gray);
    color: var(--text-color);
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
  
  /* Voice interface */
  .voice-recognition {
    padding: 2rem 1.5rem;
    text-align: center;
  }
  
  .mic-visualizer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
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
    background-color: var(--primary-color);
    border-radius: 2px;
    animation: wave 1.2s infinite ease-in-out;
  }
  
  .wave:nth-child(2) {
    animation-delay: 0.2s;
  }
  
  .wave:nth-child(3) {
    animation-delay: 0.4s;
  }
  
  @keyframes wave {
    0%, 100% {
      height: 8px;
    }
    50% {
      height: 32px;
    }
  }
  
  .voice-status {
    font-size: 1.2rem;
    color: var(--text-color);
  }
  
  /* Gesture interface */
  .gesture-display {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .camera-preview {
    position: relative;
    width: 100%;
    height: 0;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
    overflow: hidden;
    border-radius: var(--border-radius-md);
    background-color: black;
  }
  
  .camera-preview img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
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
  }
  </style>
  