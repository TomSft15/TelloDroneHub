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
      keyboardStatus: 'Contrôles clavier désactivés',
      keyLastPressed: {}, // Stocke le dernier moment où une touche a été pressée
      keyCommandCooldown: 500, // Délai en millisecondes entre les commandes (500ms par défaut)
      pressedKeys: {} // Garde trace des touches actuellement enfoncées
    };
  },
  methods: {
    enableKeyboardControls() {
      if (!this.keyboardEnabled) {
        window.addEventListener('keydown', this.handleKeyDown);
        window.addEventListener('keyup', this.handleKeyUp);
        this.keyboardEnabled = true;
        this.keyboardStatus = 'Contrôles clavier activés';
        console.log('Contrôles clavier activés');
      }
    },
    disableKeyboardControls() {
      if (this.keyboardEnabled) {
        window.removeEventListener('keydown', this.handleKeyDown);
        window.removeEventListener('keyup', this.handleKeyUp);
        this.keyboardEnabled = false;
        this.keyboardStatus = 'Contrôles clavier désactivés';
        console.log('Contrôles clavier désactivés');
        this.pressedKeys = {};
      }
    },
    handleKeyDown(event) {

      if (!this.keyboardEnabled) {
        return;
      }
      // Ignorer les événements si on est dans un champ de saisie
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA' || event.target.isContentEditable) {
        return;
      }
      
      const key = event.key;
      const command = this.keyCommands[key];

      if (command) {
        // Enregistrer la touche comme étant enfoncée
        this.pressedKeys[key] = true;
        
        // Vérifier le délai depuis la dernière pression
        const currentTime = Date.now();
        if (!this.keyLastPressed[key] || (currentTime - this.keyLastPressed[key]) > this.keyCommandCooldown) {
          this.executeCommand(command);
          // Mettre à jour le timestamp de la dernière pression pour cette touche
          this.keyLastPressed[key] = currentTime;
        }
        
        // Éviter les actions par défaut du navigateur (comme le défilement)
        event.preventDefault();
      }
    },
    handleKeyUp(event) {
      if (!this.keyboardEnabled) {
        return;
      }

      const key = event.key;
      
      // Pour certaines commandes, il peut être utile d'envoyer une commande d'arrêt
      // quand la touche est relâchée (par exemple pour les mouvements)
      const command = this.keyCommands[key];
      if (command && (command.startsWith('move') || command.startsWith('rotate'))) {
        // Envoyer une commande pour arrêter le mouvement
        this.stopMovement();
      }
      delete this.pressedKeys[key];
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
    },
    stopMovement() {
      // Cette fonction sera appelée lorsqu'une touche de mouvement est relâchée
      // Pour arrêter le mouvement, on peut utiliser un appel API spécifique
      // ou simplement appeler une méthode du service drone
      
      // Envoyer une commande "hover" ou équivalente
      console.log("Arrêt du mouvement");
      
      // Si vous avez une API qui gère cela, utilisez-la
      // Par exemple:
      DroneService.hover();
    },
    // La méthode suivante permet de régler le délai entre les commandes
    setCommandCooldown(milliseconds) {
      if (milliseconds >= 100 && milliseconds <= 2000) {
        this.keyCommandCooldown = milliseconds;
        console.log(`Délai entre les commandes défini à ${milliseconds}ms`);
      } else {
        console.warn("Le délai doit être compris entre 100ms et 2000ms");
      }
    }
  },
  beforeUnmount() {
    // Nettoyer les écouteurs d'événements quand le composant est détruit
    this.disableKeyboardControls();
  }
};