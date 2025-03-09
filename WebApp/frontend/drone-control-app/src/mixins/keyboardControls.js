export default {
    data() {
      return {
        keyboardEnabled: false,
        keyCommands: {
          'ArrowUp': 'moveUp',
          'ArrowDown': 'moveDown',
          'ArrowLeft': 'moveLeft',
          'ArrowRight': 'moveRight',
          'w': 'moveForward',
          's': 'moveBackward',
          'a': 'rotateLeft',
          'd': 'rotateRight',
          't': 'takeoff',
          'l': 'land',
          'Escape': 'emergencyStop'
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
        this.sendCommand(command);
      }
    },
    beforeDestroy() {
      // Nettoyer les écouteurs d'événements quand le composant est détruit
      this.disableKeyboardControls();
    }
  };
  