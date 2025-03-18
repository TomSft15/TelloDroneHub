<template>
    <div class="connection-page">
      <div class="page-header">
        <h1><font-awesome-icon icon="wifi" class="icon-margin"/> Connexion au Drone</h1>
        <p class="page-description">Connectez-vous à votre drone Tello via WiFi pour commencer à voler.</p>
      </div>
  
      <div class="connection-container">
        <div class="connection-card">
          <div class="card-header">
            <h2><font-awesome-icon icon="plug" class="icon-margin"/> État de la connexion</h2>
            <div class="connection-status" :class="{ 'connected': isConnected, 'disconnected': !isConnected }">
              <span class="status-indicator"></span>
              <span class="status-text">{{ connectionStatus }}</span>
            </div>
          </div>
  
          <div class="connection-steps">
            <div class="step" :class="{ 'completed': wifiConnected, 'active': !wifiConnected }">
              <div class="step-number">1</div>
              <div class="step-content">
                <h3>Connectez-vous au réseau WiFi du drone</h3>
                <p>Activez votre drone Tello et connectez-vous au réseau WiFi "TELLO-XXXXXX" depuis les paramètres WiFi de votre appareil.</p>
                <div class="info-box">
                  <font-awesome-icon icon="info-circle" class="icon-margin"/>
                  <p>Le mot de passe par défaut est vide. Le SSID du réseau commence généralement par "TELLO-" suivi du numéro de série.</p>
                </div>
                <button @click="checkWifiConnection" class="btn-primary">
                  <font-awesome-icon icon="sync-alt" :icon="{ 'spinner': checkingWifi }" class="icon-margin"/>
                  Vérifier la connexion WiFi
                </button>
              </div>
            </div>
  
            <div class="step" :class="{ 'completed': isConnected, 'active': wifiConnected && !isConnected, 'disabled': !wifiConnected }">
              <div class="step-number">2</div>
              <div class="step-content">
                <h3>Connecter l'application au drone</h3>
                <p>Une fois connecté au réseau WiFi du drone, établissez la connexion entre l'application et le drone.</p>
                
                <div class="connection-form">
                  <div class="form-group">
                    <label for="droneIp">Adresse IP du drone</label>
                    <input 
                      type="text" 
                      id="droneIp" 
                      v-model="droneIp" 
                      placeholder="192.168.10.1" 
                      :disabled="!wifiConnected || isConnected"
                    >
                  </div>
                  <div class="form-group">
                    <label for="dronePort">Port</label>
                    <input 
                      type="number" 
                      id="dronePort" 
                      v-model="dronePort" 
                      placeholder="8889" 
                      :disabled="!wifiConnected || isConnected"
                    >
                  </div>
                </div>
  
                <button 
                  @click="connectToDrone" 
                  class="btn-primary" 
                  :disabled="!wifiConnected || connecting || isConnected"
                >
                  <font-awesome-icon class='icon-margin' icon="link" :icon="{ 'spin': connecting }"/>
                  {{ isConnected ? 'Connecté' : connecting ? 'Connexion en cours...' : 'Connecter au drone' }}
                </button>
                
                <button 
                  v-if="isConnected" 
                  @click="disconnectDrone" 
                  class="btn-outline btn-danger"
                >
                  <font-awesome-icon icon="unlink" class="icon-margin"/> Déconnecter
                </button>
              </div>
            </div>
  
            <div class="step" :class="{ 'active': isConnected, 'disabled': !isConnected }">
              <div class="step-number">3</div>
              <div class="step-content">
                <h3>Prêt à décoller!</h3>
                <p>Votre drone est maintenant connecté. Vous pouvez commencer à utiliser les contrôles.</p>
                
                <div class="drone-info" v-if="isConnected && droneInfo">
                  <h4>Informations du drone</h4>
                  <div class="info-grid">
                    <div class="info-item">
                      <span class="info-label">Batterie</span>
                      <span class="info-value">{{ droneInfo.battery }}%</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">Temp.</span>
                      <span class="info-value">{{ droneInfo.temp }}°C</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">Altitude</span>
                      <span class="info-value">{{ droneInfo.height }}cm</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">Version</span>
                      <span class="info-value">{{ droneInfo.sdk }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="action-buttons" v-if="isConnected">
                  <router-link to="/dashboard" class="btn-primary">
                    <font-awesome-icon icon="tachometer-alt" class="icon-margin"/> Tableau de bord
                  </router-link>
                  <router-link to="/voice-control" class="btn-outline">
                    <font-awesome-icon icon="microphone" class="icon-margin"/> Contrôle vocal
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <div class="connection-help">
          <div class="help-card">
            <div class="card-header">
              <h3><font-awesome-icon icon="question-circle" class="icon-margin"/> Aide à la connexion</h3>
            </div>
            <div class="help-content">
              <div class="help-item">
                <h4>Je ne vois pas le réseau TELLO</h4>
                <p>Assurez-vous que votre drone est allumé et que son voyant clignote en jaune. Redémarrez le drone si nécessaire.</p>
              </div>
              <div class="help-item">
                <h4>Impossible de se connecter au réseau</h4>
                <p>Essayez de redémarrer votre drone et votre appareil. Assurez-vous que le drone est suffisamment chargé.</p>
              </div>
              <div class="help-item">
                <h4>Connection refusée</h4>
                <p>Vérifiez que l'adresse IP et le port sont corrects. L'adresse IP par défaut du Tello est généralement 192.168.10.1 et le port 8889.</p>
              </div>
              <div class="help-item">
                <h4>Déconnexions fréquentes</h4>
                <p>Assurez-vous qu'il n'y a pas d'interférences WiFi à proximité et que votre drone est suffisamment chargé.</p>
              </div>
              <div class="troubleshoot-button">
                <button class="btn-text" @click="showAdvancedTroubleshooting = !showAdvancedTroubleshooting">
                  <font-awesome-icon icon="tools" class="icon-margin"/>
                  {{ showAdvancedTroubleshooting ? 'Masquer' : 'Afficher' }} le dépannage avancé
                </button>
              </div>
              <div v-if="showAdvancedTroubleshooting" class="advanced-troubleshooting">
                <h4>Dépannage avancé</h4>
                <div class="code-block">
                  <p>Ouvrez la console de développement pour voir les logs de connexion</p>
                  <div class="command-line">
                    <code>ping 192.168.10.1</code>
                  </div>
                  <p>Cette commande vérifie si vous pouvez atteindre le drone</p>
                  <button class="btn-small" @click="runNetworkDiagnostic">
                    <font-awesome-icon class="icon-margin" icon="stethoscope"/> Exécuter diagnostic réseau
                  </button>
                </div>
              </div>
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
    name: 'DroneConnection',
    data() {
        return {
        droneIp: '192.168.10.1',
        dronePort: 8889,
        isConnected: false,
        connecting: false,
        checkingWifi: false,
        wifiConnected: false,
        connectionError: null,
        showAdvancedTroubleshooting: false,
        droneInfo: null,
        dataUpdateInterval: null
        }
    },
    computed: {
      connectionStatus() {
        if (this.isConnected) {
          return 'Connecté';
        } else if (this.connecting) {
          return 'Connexion en cours...';
        } else if (this.connectionError) {
          return `Erreur: ${this.connectionError}`;
        } else {
          return 'Déconnecté';
        }
      }
    },
    methods: {
      async checkWifiConnection() {
        this.checkingWifi = true;
        
        try {
          // Nous allons simplement tester si le serveur Flask est accessible
          await axios.get(`${API_URL}/test`);
          this.wifiConnected = true;
          console.log('Vérification WiFi réussie');
        } catch (error) {
          console.error('Erreur de vérification WiFi:', error);
          this.wifiConnected = false;
        } finally {
          this.checkingWifi = false;
        }
      },
      
      async connectToDrone() {
        if (!this.wifiConnected) {
            return;
        }
        this.connecting = true;
        this.connectionError = null;
        
        try {
            // Appeler l'API pour connecter le drone
            const response = await axios.get(`${API_URL}/drone/connect`);
            
            if (response.data.success) {
            this.isConnected = true;
            // Récupérer les informations initiales
            await this.fetchDroneInfo();
            // Commencer à obtenir régulièrement les mises à jour
            this.startPollingData();
            
            // Stocker l'état de connexion dans localStorage
            localStorage.setItem('droneConnected', 'true');
            
            // Déclencher un événement avec l'émetteur
            emitter.emit('drone-connected', {
                ip: this.droneIp,
                port: this.dronePort,
                info: this.droneInfo
            });
            } else {
            this.connectionError = response.data.message || 'Échec de la connexion';
            }
        } catch (error) {
            this.connectionError = error.message || 'Échec de la connexion';
            console.error('Erreur de connexion:', error);
        } finally {
            this.connecting = false;
        }
      },
      
      async fetchDroneInfo() {
        try {
          const response = await axios.get(`${API_URL}/status/drone_data`);
          this.droneInfo = {
            battery: response.data.battery || 0,
            temp: response.data.temperature || 0,
            height: response.data.height || 0,
            sdk: 'v2.0' // Cette information peut ne pas être disponible via l'API
          };
        } catch (error) {
          console.error("Erreur lors de la récupération des informations:", error);
        }
      },
      
      startPollingData() {
        // Récupérer régulièrement les données du drone
        this.dataUpdateInterval = setInterval(async () => {
          if (!this.isConnected) {
            clearInterval(this.dataUpdateInterval);
            return;
          }
          
          try {
            const response = await axios.get(`${API_URL}/status/drone_data`);
            this.droneInfo = {
              battery: response.data.battery || 0,
              temp: response.data.temperature || 0,
              height: response.data.height || 0,
              sdk: 'v2.0'
            };
          } catch (error) {
            console.error("Erreur lors de la récupération des données:", error);
            // Si plusieurs erreurs consécutives, considérer le drone comme déconnecté
            this.consecutiveErrors = (this.consecutiveErrors || 0) + 1;
            if (this.consecutiveErrors > 3) {
              this.disconnectDrone();
            }
          }
        }, 1000);
      },
      
      async disconnectDrone() {
        try {
            // Réinitialiser l'état local
            this.isConnected = false;
            this.droneInfo = null;
            
            // Nettoyer les intervalles
            if (this.dataUpdateInterval) {
            clearInterval(this.dataUpdateInterval);
            this.dataUpdateInterval = null;
            }
            
            // Informer le localStorage
            localStorage.removeItem('droneConnected');
            
            console.log('Déconnexion du drone');
            
            // Utiliser l'émetteur pour propager l'événement
            emitter.emit('drone-disconnected');
            
        } catch (error) {
            console.error("Erreur lors de la déconnexion:", error);
        }
      },

      
      runNetworkDiagnostic() {
        console.log('Exécution du diagnostic réseau...');
        
        // Vérifier la connectivité au serveur Flask
        axios.get(`${API_URL}/test`)
          .then(response => {
            console.log('Serveur accessible:', response.data);
            alert(`Diagnostic réseau terminé: Serveur accessible`);
          })
          .catch(error => {
            console.error('Serveur inaccessible:', error);
            alert(`Diagnostic réseau terminé: Serveur inaccessible. Vérifiez la connexion.`);
          });
      }
    },
    
    async mounted() {
        // Vérifier si le drone était connecté précédemment
        const wasConnected = localStorage.getItem('droneConnected') === 'true';
        
        if (wasConnected) {
        try {
            // Vérifier l'état actuel du drone
            const response = await axios.get(`${API_URL}/drone/status`);
            if (response.data.connected) {
            this.isConnected = true;
            this.wifiConnected = true;
            await this.fetchDroneInfo();
            this.startPollingData();
            } else {
            localStorage.removeItem('droneConnected');
            }
        } catch (error) {
            console.error("Erreur lors de la vérification de l'état du drone:", error);
            localStorage.removeItem('droneConnected');
        }
        }
    },

    
    beforeUnmount() {
        // Nettoyer les intervalles lors de la destruction du composant
        if (this.dataUpdateInterval) {
        clearInterval(this.dataUpdateInterval);
        }
    }

  };
  </script>  
  
  <style scoped>
  /* Connection Page Styles */
  .connection-page {
    padding: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .page-header {
    margin-bottom: 2rem;
    text-align: left;
  }
  
  .page-header h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    color: #2c3e50;
  }
  
  .page-header h1 i {
    margin-right: 0.75rem;
    color: #3498db;
  }
  
  .page-description {
    font-size: 1.1rem;
    color: #6c757d;
    max-width: 700px;
  }
  
  .connection-container {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
  }
  
  @media (max-width: 992px) {
    .connection-container {
      grid-template-columns: 1fr;
    }
  }
  
  .connection-card, .help-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
  }
  
  .card-header h2, .card-header h3 {
    margin: 0;
    font-weight: 600;
    color: #2c3e50;
    display: flex;
    align-items: center;
  }
  
  .card-header h2 i, .card-header h3 i {
    margin-right: 0.75rem;
    color: #3498db;
  }
  
  .connection-status {
    display: flex;
    align-items: center;
    font-weight: 600;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.875rem;
  }
  
  .connection-status.connected {
    background-color: #d4edda;
    color: #155724;
  }
  
  .connection-status.disconnected {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 0.5rem;
  }
  
  .connected .status-indicator {
    background-color: #28a745;
    box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.3);
  }
  
  .disconnected .status-indicator {
    background-color: #dc3545;
    box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.3);
  }
  
  /* Connection Steps */
  .connection-steps {
    padding: 1.5rem;
  }
  
  .step {
    display: flex;
    margin-bottom: 2rem;
    position: relative;
  }
  
  .step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 3rem;
    left: 1.25rem;
    height: calc(100% - 2rem);
    width: 2px;
    background: #e9ecef;
  }
  
  .step.completed:not(:last-child)::after {
    background: #3498db;
  }
  
  .step-number {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: #e9ecef;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    margin-right: 1rem;
    flex-shrink: 0;
    color: #6c757d;
    border: 2px solid #ced4da;
  }
  
  .step.active .step-number {
    background: #fff;
    color: #3498db;
    border: 2px solid #3498db;
    box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.2);
  }
  
  .step.completed .step-number {
    background: #3498db;
    color: white;
    border-color: #3498db;
  }
  
  .step-content {
    flex: 1;
  }
  
  .step.disabled {
    opacity: 0.6;
    pointer-events: none;
  }
  
  .step.disabled button {
    pointer-events: none;
  }
  
  .step h3 {
    font-size: 1.25rem;
    margin-top: 0;
    margin-bottom: 0.75rem;
    color: #2c3e50;
  }
  
  .step.completed h3 {
    color: #28a745;
  }
  
  .info-box {
    background: #e1f5fe;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
    display: flex;
    align-items: flex-start;
  }
  
  .info-box i {
    color: #03a9f4;
    margin-right: 0.75rem;
    margin-top: 0.2rem;
    font-size: 1.1rem;
  }
  
  .info-box p {
    margin: 0;
    font-size: 0.9rem;
    color: #01579b;
  }
  
  .connection-form {
    margin: 1.5rem 0;
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 6px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #495057;
    font-size: 0.875rem;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }
  
  .form-group input:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  }
  
  .form-group input:disabled {
    background-color: #e9ecef;
    cursor: not-allowed;
  }

  .icon-margin {
    margin-right: 12px;
  }
  
  /* Buttons */
  .btn-primary {
    background: #3498db;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
    font-size: 1rem;
    text-decoration: none;
  }
  
  .btn-primary:hover {
    background: #2980b9;
  }
  
  .btn-primary:disabled {
    background: #95a5a6;
    cursor: not-allowed;
  }
  
  .btn-primary i {
    margin-right: 0.75rem;
  }
  
  .btn-outline {
    background: transparent;
    color: #3498db;
    border: 2px solid #3498db;
    padding: 0.7rem 1.5rem;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    font-size: 1rem;
    text-decoration: none;
    margin-left: 0.5rem;
  }
  
  .btn-outline:hover {
    background: rgba(52, 152, 219, 0.1);
  }
  
  .btn-outline i {
    margin-right: 0.75rem;
  }
  
  .btn-danger {
    color: #e74c3c;
    border-color: #e74c3c;
  }
  
  .btn-danger:hover {
    background: rgba(231, 76, 60, 0.1);
  }
  
  .btn-text {
    background: transparent;
    border: none;
    color: #3498db;
    cursor: pointer;
    padding: 0.5rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    transition: color 0.2s;
  }
  
  .btn-text:hover {
    color: #2980b9;
    text-decoration: underline;
  }
  
  .btn-text i {
    margin-right: 0.5rem;
  }
  
  .btn-small {
    padding: 0.4rem 0.75rem;
    font-size: 0.875rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    font-weight: 500;
    margin-top: 0.5rem;
  }
  
  .btn-small i {
    margin-right: 0.5rem;
  }
  
  /* Drone Info */
  .drone-info {
    background: #f8f9fa;
    padding: 1.25rem;
    border-radius: 6px;
    margin: 1rem 0 1.5rem 0;
  }
  
  .drone-info h4 {
    margin-top: 0;
    margin-bottom: 1rem;
    font-size: 1.1rem;
    color: #2c3e50;
    border-bottom: 1px solid #dee2e6;
    padding-bottom: 0.75rem;
  }
  
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 1rem;
  }
  
  .info-item {
    display: flex;
    flex-direction: column;
  }
  
  .info-label {
    font-size: 0.875rem;
    color: #6c757d;
    margin-bottom: 0.25rem;
  }
  
  .info-value {
    font-weight: bold;
    color: #2c3e50;
    font-size: 1.25rem;
  }
  
  .action-buttons {
    margin-top: 1.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }
  
  /* Help Section */
  .help-content {
    padding: 1.5rem;
  }
  
  .help-item {
    margin-bottom: 1.5rem;
  }
  
  .help-item h4 {
    font-size: 1rem;
    margin-top: 0;
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }
  
  .help-item p {
    margin: 0;
    font-size: 0.925rem;
    color: #495057;
  }
  
  .troubleshoot-button {
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .advanced-troubleshooting {
    margin-top: 1.5rem;
  }
  
  .code-block {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 1.25rem;
    border-radius: 6px;
    font-family: 'Courier New', Courier, monospace;
    margin-top: 0.5rem;
  }
  
  .code-block p {
    margin: 0.5rem 0;
    color: #bdc3c7;
  }
  
  .command-line {
    background: rgba(255, 255, 255, 0.1);
    padding: 0.75rem;
    border-radius: 3px;
    margin: 0.75rem 0;
  }
  
  .command-line code {
    color: #e74c3c;
  }
  
  /* Animation for spinner */
  @keyframes spinner {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  
  .spinner {
    animation: fa-spin 2s linear infinite;
  }
  </style>
  
  