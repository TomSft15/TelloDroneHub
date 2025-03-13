// Service de simulation pour le drone Tello
// À placer dans src/services/droneSimulationService.js

import io from 'socket.io-client';

class DroneSimulationService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.videoStream = null;
    this.telemetryData = {
      battery: 100,
      height: 0,
      speed: 0,
      flightTime: 0,
      temperature: 25,
      signal: 95
    };
    this.eventListeners = {
      connect: [],
      disconnect: [],
      telemetry: [],
      video: [],
      error: []
    };
    
    // Timer pour la simulation de télémétrie
    this.telemetryTimer = null;
    this.videoTimer = null;
    
    // Images factices pour la simulation vidéo
    this.simulationImages = [];
    this.currentImageIndex = 0;
  }

  // Se connecter au serveur socket.io
  connect() {
    return new Promise((resolve, reject) => {
      try {
        const socketUrl = process.env.VUE_APP_SOCKET_URL || 'http://localhost:3000';
        this.socket = io(socketUrl);
        
        this.socket.on('connect', () => {
          console.log('Socket.IO connected');
          this.isConnected = true;
          this._notifyListeners('connect', { status: 'connected' });
          resolve({ status: 'connected' });
        });
        
        this.socket.on('disconnect', () => {
          console.log('Socket.IO disconnected');
          this.isConnected = false;
          this.stopVideoStream();
          this.stopTelemetry();
          this._notifyListeners('disconnect', { status: 'disconnected' });
        });
        
        this.socket.on('video_frame', (frameData) => {
          this._notifyListeners('video', { frame: `data:image/jpeg;base64,${frameData}` });
        });
        
        this.socket.on('error', (error) => {
          console.error('Socket error:', error);
          this._notifyListeners('error', { error });
        });
        
      } catch (error) {
        console.error('Error connecting to socket:', error);
        reject(error);
      }
    });
  }

  // Déconnecter du serveur socket.io
  disconnect() {
    if (this.socket) {
      this.stopVideoStream();
      this.stopTelemetry();
      this.socket.disconnect();
      this.isConnected = false;
      this._notifyListeners('disconnect', { status: 'disconnected' });
    }
  }

  // Demander la connexion avec le drone (simulation)
  connectDrone() {
    if (!this.isConnected || !this.socket) {
      return this.connect().then(() => this.connectDrone());
    }
    
    this.socket.emit('connect_camera', { droneId: 'simulation' });
    return Promise.resolve({ status: 'drone_connected' });
  }

  // Déconnecter du drone (simulation)
  disconnectDrone() {
    if (this.socket) {
      this.socket.emit('disconnect_camera', { droneId: 'simulation' });
    }
    this.stopVideoStream();
    this.stopTelemetry();
    return Promise.resolve({ status: 'drone_disconnected' });
  }

  // Démarrer le flux vidéo simulé sans serveur socket
  startLocalVideoSimulation() {
    if (this.videoTimer) {
      this.stopVideoStream();
    }
    
    // Générer ou charger les images de simulation
    this._loadSimulationImages().then(() => {
      if (this.simulationImages.length === 0) {
        console.error('Aucune image de simulation disponible');
        return;
      }
      
      const fps = 10; // Images par seconde
      this.videoTimer = setInterval(() => {
        if (this.simulationImages.length > 0) {
          const currentImage = this.simulationImages[this.currentImageIndex];
          this._notifyListeners('video', { frame: currentImage });
          this.currentImageIndex = (this.currentImageIndex + 1) % this.simulationImages.length;
        }
      }, 1000 / fps);
    });
  }

  // Charger les images de simulation
  async _loadSimulationImages() {
    // Version simplifiée : utiliser des couleurs aléatoires pour les images
    if (this.simulationImages.length === 0) {
      const canvasSize = 640;
      const frameCount = 30;
      
      for (let i = 0; i < frameCount; i++) {
        const canvas = document.createElement('canvas');
        canvas.width = canvasSize;
        canvas.height = canvasSize * 0.75; // Ratio 4:3
        
        const ctx = canvas.getContext('2d');
        
        // Ciel
        const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        gradient.addColorStop(0, '#87CEEB');
        gradient.addColorStop(1, '#E0F7FA');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Horizon/sol
        ctx.fillStyle = '#8BC34A';
        ctx.fillRect(0, canvas.height * 0.7, canvas.width, canvas.height * 0.3);
        
        // Dessiner un carré qui se déplace horizontalement (simulation d'un objet)
        const x = (canvas.width / frameCount) * i;
        ctx.fillStyle = 'rgba(255, 0, 0, 0.7)';
        ctx.fillRect(x, canvas.height * 0.6, 40, 40);
        
        // Ajouter un timestamp
        const timestamp = new Date().toISOString();
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(10, 10, 250, 25);
        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.fillText(`Simulation locale - Frame ${i} - ${timestamp}`, 15, 25);
        
        // Convertir le canvas en data URL
        this.simulationImages.push(canvas.toDataURL('image/jpeg'));
      }
    }
  }

  // Arrêter le flux vidéo simulé
  stopVideoStream() {
    if (this.videoTimer) {
      clearInterval(this.videoTimer);
      this.videoTimer = null;
    }
  }

  // Démarrer la télémétrie simulée
  startTelemetry() {
    if (this.telemetryTimer) {
      this.stopTelemetry();
    }
    
    this.telemetryTimer = setInterval(() => {
      // Mettre à jour les données de télémétrie avec des valeurs simulées
      this.telemetryData.battery = Math.max(0, this.telemetryData.battery - 0.05);
      this.telemetryData.height = this._fluctuate(this.telemetryData.height, 0.5, 0, 120);
      this.telemetryData.speed = this._fluctuate(this.telemetryData.speed, 0.2, 0, 15);
      this.telemetryData.flightTime += 1;
      this.telemetryData.temperature = this._fluctuate(this.telemetryData.temperature, 0.1, 20, 40);
      this.telemetryData.signal = this._fluctuate(this.telemetryData.signal, 1, 80, 100);
      
      this._notifyListeners('telemetry', { ...this.telemetryData });
    }, 1000);
  }

  // Fonction utilitaire pour faire fluctuer une valeur entre min et max
  _fluctuate(value, change, min, max) {
    const newValue = value + (Math.random() * change * 2 - change);
    return Math.min(max, Math.max(min, newValue));
  }

  // Arrêter la télémétrie simulée
  stopTelemetry() {
    if (this.telemetryTimer) {
      clearInterval(this.telemetryTimer);
      this.telemetryTimer = null;
    }
  }

  // Envoyer une commande au drone (simulation)
  sendCommand(command, params = {}) {
    console.log(`Sending command: ${command}`, params);
    
    if (!this.isConnected || !this.socket) {
      return Promise.reject(new Error('Not connected to socket server'));
    }
    
    return new Promise((resolve, reject) => {
      // Simuler un délai de réponse
      setTimeout(() => {
        // Traiter la commande et mettre à jour les données de télémétrie
        switch (command) {
          case 'takeoff':
            this.telemetryData.height = 50;
            break;
          case 'land':
            this.telemetryData.height = 0;
            this.telemetryData.speed = 0;
            break;
          case 'up':
            this.telemetryData.height = Math.min(120, this.telemetryData.height + 20);
            break;
          case 'down':
            this.telemetryData.height = Math.max(0, this.telemetryData.height - 20);
            break;
          case 'forward':
            this.telemetryData.speed = 10;
            break;
          case 'back':
            this.telemetryData.speed = 5;
            break;
          default:
            // Autres commandes
            break;
        }
        
        this._notifyListeners('telemetry', { ...this.telemetryData });
        resolve({ status: 'success', command });
      }, 500);
    });
  }

  // Capture d'écran (simulation)
  captureScreenshot() {
    if (this.simulationImages.length > 0) {
      const randomIndex = Math.floor(Math.random() * this.simulationImages.length);
      return Promise.resolve({
        image: this.simulationImages[randomIndex],
        timestamp: new Date().toISOString()
      });
    }
    return Promise.reject(new Error('No simulation images available'));
  }

  // Ajouter un écouteur d'événement
  addEventListener(event, callback) {
    if (this.eventListeners[event]) {
      this.eventListeners[event].push(callback);
    }
  }

  // Supprimer un écouteur d'événement
  removeEventListener(event, callback) {
    if (this.eventListeners[event]) {
      this.eventListeners[event] = this.eventListeners[event].filter(cb => cb !== callback);
    }
  }

  // Notifier tous les écouteurs d'un événement
  _notifyListeners(event, data) {
    if (this.eventListeners[event]) {
      this.eventListeners[event].forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in ${event} event listener:`, error);
        }
      });
    }
  }
}

export default new DroneSimulationService();