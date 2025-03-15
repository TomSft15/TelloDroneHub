import DroneService from '../services/DroneService';

export default {
  data() {
    return {
      keyboardEnabled: false,
      keyCommands: {
        'ArrowUp': 'moveUp',            // Monter
        'ArrowDown': 'moveDown',        // Descendre
        'ArrowLeft': 'rotateLeft',      // Rotation gauche
        'ArrowRight': 'rotateRight',    // Rotation droite
        'z': 'moveForward',             // Avancer
        's': 'moveBackward',            // Reculer
        'q': 'moveLeft',                // Aller à gauche
        'd': 'moveRight',               // Aller à droite
        'a': 'takeoff',                 // Décollage
        'e': 'land',                    // Atterrissage
        'p': 'emergencyStop',           // Arrêt d'urgence
        't': 'flipForward',             // Front flip
        'g': 'flipBackward',            // Back flip
        'f': 'flipLeft',                // Left flip
        'h': 'flipRight',               // Right flip
        'i': 'speechRecognition',       // Speech recognition
        'm': 'quit'                     // Quitter le programme
      },
      keyboardStatus: 'Contrôles clavier désactivés'
    };
  },
  methods: {
    enableKeyboardControls() {
      if (!this.keyboardEnabled) {
        window.addEventListener('keydown', this.handleKeyDown);
        this.keyboardEnabled = true;
        this.keyboardStatus = 'Contrôles clavier activés';
        console.log('Contrôles clavier activés');
      }
    },
    disableKeyboardControls() {
      if (this.keyboardEnabled) {
        window.removeEventListener('keydown', this.handleKeyDown);
        this.keyboardEnabled = false;
        this.keyboardStatus = 'Contrôles clavier désactivés';
        console.log('Contrôles clavier désactivés');
      }
    },
    handleKeyDown(event) {
      // Ignorer les événements si on est dans un champ de saisie
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
      }
      
      const command = this.keyCommands[event.key];
      if (command) {
        this.executeCommand(command);
        // Éviter les actions par défaut du navigateur (comme le défilement)
        event.preventDefault();
      }
    },
    executeCommand(command) {
      console.log(`Exécution de la commande: ${command}`);
      
      // Exécuter la commande appropriée
      switch (command) {
        case 'moveUp':
          DroneService.moveUp();
          break;
        case 'moveDown':
          DroneService.moveDown();
          break;
        case 'moveLeft':
          DroneService.moveLeft();
          break;
        case 'moveRight':
          DroneService.moveRight();
          break;
        case 'moveForward':
          DroneService.moveForward();
          break;
        case 'moveBackward':
          DroneService.moveBackward();
          break;
        case 'rotateLeft':
          DroneService.rotateLeft();
          break;
        case 'rotateRight':
          DroneService.rotateRight();
          break;
        case 'takeoff':
          DroneService.takeoff();
          break;
        case 'land':
          DroneService.land();
          break;
        case 'emergencyStop':
          DroneService.emergencyStop();
          break;
        case 'flipForward':
          DroneService.flipForward();
          break;
        case 'flipBackward':
          DroneService.flipBackward();
          break;
        case 'flipLeft':
          DroneService.flipLeft();
          break;
        case 'flipRight':
          DroneService.flipRight();
          break;
        case 'speechRecognition':
          DroneService.speechRecognition();
          break;
        case 'quit':
          DroneService.quit();
          break;
        default:
          console.warn(`Commande non reconnue: ${command}`);
      }
    }
  },
  beforeUnmount() {
    // Nettoyer les écouteurs d'événements quand le composant est détruit
    this.disableKeyboardControls();
  }
};