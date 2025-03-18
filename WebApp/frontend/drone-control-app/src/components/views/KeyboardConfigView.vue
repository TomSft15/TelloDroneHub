<template>
    <div class="config-container">
      <div class="page-header">
        <h1><i class="fas fa-keyboard"></i> Configuration des contrôles clavier</h1>
        <div class="header-actions">
          <button class="btn-save" @click="saveConfiguration">
            <i class="fas fa-save"></i> Enregistrer la configuration
          </button>
          <button class="btn-reset" @click="resetConfiguration">
            <i class="fas fa-undo"></i> Réinitialiser
          </button>
        </div>
      </div>
  
      <div class="config-intro card">
        <div class="card-content">
          <h2>Personnalisez vos commandes</h2>
          <p>Modifiez les touches du clavier pour adapter le contrôle de votre drone à vos préférences. 
             Cliquez sur "Modifier" à côté d'une commande pour lui assigner une nouvelle touche.</p>
        </div>
      </div>
  
      <div class="keyboard-layout card">
        <div class="card-header">
          <h2>Disposition du clavier</h2>
        </div>
        <div class="keyboard-visualization">
          <div class="keyboard-row">
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('Escape') }">ESC</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F1') }">F1</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F2') }">F2</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F3') }">F3</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F4') }">F4</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F5') }">F5</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F6') }">F6</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F7') }">F7</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F8') }">F8</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F9') }">F9</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F10') }">F10</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F11') }">F11</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('F12') }">F12</div>
          </div>
          <div class="keyboard-row">
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('`') }">`</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('1') }">1</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('2') }">2</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('3') }">3</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('4') }">4</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('5') }">5</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('6') }">6</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('7') }">7</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('8') }">8</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('9') }">9</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('0') }">0</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('-') }">-</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('=') }">=</div>
            <div class="key key-wide" :class="{ 'key-assigned': isKeyAssigned('Backspace') }">⌫</div>
          </div>
          <div class="keyboard-row">
            <div class="key key-wide" :class="{ 'key-assigned': isKeyAssigned('Tab') }">Tab</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('q') }">Q</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('w') }">W</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('e') }">E</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('r') }">R</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('t') }">T</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('y') }">Y</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('u') }">U</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('i') }">I</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('o') }">O</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('p') }">P</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('[') }">[</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned(']') }">]</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('\\') }">\\</div>
          </div>
          <div class="keyboard-row">
            <div class="key key-wide" :class="{ 'key-assigned': isKeyAssigned('CapsLock') }">Caps</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('a') }">A</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('s') }">S</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('d') }">D</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('f') }">F</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('g') }">G</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('h') }">H</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('j') }">J</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('k') }">K</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('l') }">L</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned(';') }">;</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('\'') }">'</div>
            <div class="key key-wide" :class="{ 'key-assigned': isKeyAssigned('Enter') }">Enter</div>
          </div>
          <div class="keyboard-row">
            <div class="key key-extra-wide" :class="{ 'key-assigned': isKeyAssigned('Shift') }">Shift</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('z') }">Z</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('x') }">X</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('c') }">C</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('v') }">V</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('b') }">B</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('n') }">N</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('m') }">M</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned(',') }">,</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('.') }">.</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('/') }">/</div>
            <div class="key key-extra-wide" :class="{ 'key-assigned': isKeyAssigned('ShiftRight') }">Shift</div>
          </div>
          <div class="keyboard-row">
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('Control') }">Ctrl</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('Meta') }">Win</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('Alt') }">Alt</div>
            <div class="key key-ultra-wide" :class="{ 'key-assigned': isKeyAssigned(' ') }">Space</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('AltRight') }">Alt</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('ContextMenu') }">Menu</div>
            <div class="key" :class="{ 'key-assigned': isKeyAssigned('ControlRight') }">Ctrl</div>
          </div>
        </div>
      </div>
  
      <div class="shortcuts-list card">
        <div class="card-header">
          <h2>Commandes actuelles</h2>
          <button class="btn-outline" @click="exportConfiguration">
            <i class="fas fa-file-export"></i> Exporter
          </button>
        </div>
        <div class="card-content">
          <div class="list-filter">
            <input type="text" placeholder="Rechercher une commande..." v-model="searchQuery" class="search-input">
            <select v-model="categoryFilter" class="category-select">
              <option value="">Toutes les catégories</option>
              <option value="movement">Mouvement</option>
              <option value="camera">Caméra</option>
              <option value="emergency">Urgence</option>
            </select>
          </div>
          
          <table class="shortcuts-table">
            <thead>
              <tr>
                <th>Action</th>
                <th>Touche</th>
                <th>Catégorie</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(action, key) in filteredBindings" :key="key">
                <td>
                  <div class="action-info">
                    <i class="action-icon" :class="getActionIcon(action)"></i>
                    <span class="action-name">{{ displayActionName(action) }}</span>
                  </div>
                </td>
                <td class="key-cell">
                  <div class="key-display">{{ displayKeyName(key) }}</div>
                </td>
                <td>
                  <span class="category-badge" :class="'category-' + getActionCategory(action)">
                    {{ getActionCategory(action) }}
                  </span>
                </td>
                <td class="actions-cell">
                  <button class="btn-edit" @click="startRebinding(key)">
                    <i class="fas fa-pencil-alt"></i> Modifier
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div v-if="isRebinding" class="rebind-modal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Modifier la touche</h3>
            <button @click="cancelRebinding" class="btn-close">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="rebind-info">
              <p class="rebind-label">Action : <strong>{{ displayActionName(keyBindings[currentRebindKey]) }}</strong></p>
              <p class="rebind-current">Touche actuelle : <span class="current-key">{{ displayKeyName(currentRebindKey) }}</span></p>
            </div>
            <div class="rebind-key-prompt">
              <div class="key-icon">
                <i class="fas fa-keyboard"></i>
              </div>
              <p>Appuyez sur une touche pour l'assigner à cette action</p>
              <p class="rebind-hint">(Appuyez sur Échap pour annuler)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'KeyboardConfigView',
    data() {
      return {
        keyBindings: {
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
        defaultBindings: {},
        isRebinding: false,
        currentRebindKey: null,
        searchQuery: '',
        categoryFilter: '',
        actionNames: {
          'moveUp': 'Se déplacer vers le haut',
          'moveDown': 'Se déplacer vers le bas',
          'moveLeft': 'Se déplacer à gauche',
          'moveRight': 'Se déplacer à droite',
          'moveForward': 'Avancer',
          'moveBackward': 'Reculer',
          'rotateLeft': 'Tourner à gauche',
          'rotateRight': 'Tourner à droite',
          'takeoff': 'Décoller',
          'land': 'Atterrir',
          'hover': 'Maintenir la position',
          'emergencyStop': 'Arrêt d\'urgence',
          'flipForward': 'Looping avant',
          'flipBackward': 'Looping arrière',
          'flipLeft': 'Looping à gauche',
          'flipRight': 'Looping à droite',
          'speechRecognition': 'Reconnaissance vocale',
          'quit': 'Quitter le programme'
        },
        keyNames: {
          'ArrowUp': '↑',
          'ArrowDown': '↓',
          'ArrowLeft': '←',
          'ArrowRight': '→',
          'Escape': 'Échap',
          ' ': 'Espace'
        },
        actionCategories: {
          'moveUp': 'movement',
          'moveDown': 'movement',
          'moveLeft': 'movement',
          'moveRight': 'movement',
          'moveForward': 'movement',
          'moveBackward': 'movement',
          'rotateLeft': 'movement',
          'rotateRight': 'movement',
          'takeoff': 'movement',
          'land': 'movement',
          'flipForward': 'movement',
          'flipBackward': 'movement',
          'flipLeft': 'movement',
          'flipRight': 'movement',
          'hover': 'movement',
          'emergencyStop': 'emergency',
          'speechRecognition': 'control',
          'quit': 'system'
        },
        actionIcons: {
          'moveUp': 'fas fa-arrow-up',
          'moveDown': 'fas fa-arrow-down',
          'moveLeft': 'fas fa-arrow-left',
          'moveRight': 'fas fa-arrow-right',
          'moveForward': 'fas fa-arrow-circle-up',
          'moveBackward': 'fas fa-arrow-circle-down',
          'rotateLeft': 'fas fa-undo',
          'rotateRight': 'fas fa-redo',
          'takeoff': 'fas fa-rocket',
          'land': 'fas fa-plane-arrival',
          'hover': 'fas fa-crosshairs',
          'emergencyStop': 'fas fa-stop-circle',
          'flipForward': 'fas fa-sync-alt',
          'flipBackward': 'fas fa-sync-alt',
          'flipLeft': 'fas fa-sync-alt',
          'flipRight': 'fas fa-sync-alt',
          'speechRecognition': 'fas fa-microphone',
          'quit': 'fas fa-power-off'
        }

      };
    },
    computed: {
      filteredBindings() {
        let result = {};
        
        for (const [key, action] of Object.entries(this.keyBindings)) {
          // Filter by search query
          if (this.searchQuery && 
              !this.displayActionName(action).toLowerCase().includes(this.searchQuery.toLowerCase()) && 
              !this.displayKeyName(key).toLowerCase().includes(this.searchQuery.toLowerCase())) {
            continue;
          }
          
          // Filter by category
          if (this.categoryFilter && this.getActionCategory(action) !== this.categoryFilter) {
            continue;
          }
          
          result[key] = action;
        }
        
        return result;
      }
    },
    created() {
      // Save default bindings for reset functionality
      this.defaultBindings = { ...this.keyBindings };
      
      // Load from localStorage if available
      const savedBindings = localStorage.getItem('keyboardBindings');
      if (savedBindings) {
        try {
          this.keyBindings = JSON.parse(savedBindings);
        } catch (e) {
          console.error('Failed to parse saved bindings', e);
        }
      }
    },
    methods: {
      displayKeyName(key) {
        return this.keyNames[key] || key.toUpperCase();
      },
      displayActionName(action) {
        return this.actionNames[action] || action;
      },
      getActionCategory(action) {
        return this.actionCategories[action] || 'other';
      },
      getActionIcon(action) {
        return this.actionIcons[action] || 'fas fa-question-circle';
      },
      isKeyAssigned(key) {
        return Object.keys(this.keyBindings).includes(key);
      },
      startRebinding(key) {
        this.isRebinding = true;
        this.currentRebindKey = key;
        window.addEventListener('keydown', this.handleRebindKey);
      },
      cancelRebinding() {
        this.isRebinding = false;
        window.removeEventListener('keydown', this.handleRebindKey);
      },
      handleRebindKey(event) {
        if (event.key === 'Escape' && this.currentRebindKey !== 'Escape') {
          // Cancel rebinding
          this.cancelRebinding();
          return;
        }
        
        const oldAction = this.keyBindings[this.currentRebindKey];
        const oldKey = this.currentRebindKey;
        const newKey = event.key;
        
        // Check if the new key is already assigned
        if (this.keyBindings[newKey]) {
          const confirmSwap = confirm(
            `La touche "${this.displayKeyName(newKey)}" est déjà assignée à "${this.displayActionName(this.keyBindings[newKey])}". ` +
            `Voulez-vous échanger les deux assignations?`
          );
          
          if (confirmSwap) {
            // Swap the two key assignments
            const newKeyAction = this.keyBindings[newKey];
            delete this.keyBindings[oldKey];
            delete this.keyBindings[newKey];
            
            this.keyBindings[newKey] = oldAction;
            this.keyBindings[oldKey] = newKeyAction;
          }
        } else {
          // Remove old association and add new one
          delete this.keyBindings[oldKey];
          this.keyBindings[newKey] = oldAction;
        }
        
        // End rebinding
        this.cancelRebinding();
        event.preventDefault();
      },
      saveConfiguration() {
        localStorage.setItem('keyboardBindings', JSON.stringify(this.keyBindings));
        alert('Configuration enregistrée avec succès!');
      },
      resetConfiguration() {
        if (confirm('Êtes-vous sûr de vouloir réinitialiser la configuration aux paramètres par défaut?')) {
          this.keyBindings = { ...this.defaultBindings };
          localStorage.removeItem('keyboardBindings');
          alert('Configuration réinitialisée!');
        }
      },
      exportConfiguration() {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.keyBindings, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "drone_keyboard_config.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
      }
    },
    beforeDestroy() {
      if (this.isRebinding) {
        window.removeEventListener('keydown', this.handleRebindKey);
      }
    }
  };
  </script>
  
  <style scoped>
  .config-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .page-header h1 {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0;
    color: var(--text-color);
  }
  
  .page-header h1 i {
    color: var(--primary-color);
  }
  
  .header-actions {
    display: flex;
    gap: 1rem;
  }
  
  .btn-save, .btn-reset, .btn-outline {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    transition: all 0.2s ease;
  }
  
  .btn-save {
    background-color: var(--success-color);
    color: white;
  }
  
  .btn-reset {
    background-color: var(--light-gray);
    color: var(--dark-gray);
  }
  
  .btn-outline {
    border: 1px solid var(--primary-color);
    color: var(--primary-color);
    background-color: transparent;
  }
  
  .btn-save:hover {
    background-color: #27ae60;
  }
  
  .btn-reset:hover {
    background-color: var(--medium-gray);
  }
  
  .btn-outline:hover {
    background-color: var(--primary-color);
    color: white;
  }
  
  .card {
    background-color: white;
    border-radius: var(--border-radius-md);
    box-shadow: var(--card-shadow);
    margin-bottom: 2rem;
    overflow: hidden;
  }
  
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 1.5rem;
    background-color: var(--light-gray);
    border-bottom: 1px solid var(--medium-gray);
  }
  
  .card-header h2 {
    margin: 0;
    font-size: 1.25rem;
    color: var(--text-color);
  }
  
  .card-content {
    padding: 1.5rem;
  }
  
  /* Config Intro */
  .config-intro .card-content {
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .config-intro h2 {
    color: var(--primary-color);
    margin-bottom: 1rem;
  }
  
  .config-intro p {
    color: var(--dark-gray);
    line-height: 1.6;
  }
  
  /* Keyboard Visualization */
  .keyboard-layout {
    overflow-x: auto;
    margin-bottom: 2rem;
  }
  
  .keyboard-visualization {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
  }
  
  .keyboard-row {
    display: flex;
    gap: 0.25rem;
  }
  
  .key {
    width: 40px;
    height: 40px;
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 0 #d1d5db;
    font-size: 0.75rem;
    color: #374151;
    font-weight: 600;
    transition: all 0.2s;
  }
  
  .key-wide {
    width: 65px;
  }
  
  .key-extra-wide {
    width: 85px;
  }
  
  .key-ultra-wide {
    width: 240px;
  }
  
  .key-assigned {
    background-color: #e8f5e9;
    border-color: #66bb6a;
    box-shadow: 0 2px 0 #66bb6a;
    color: #2e7d32;
  }
  
  /* Shortcuts List */
  .list-filter {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .search-input, .category-select {
    padding: 0.6rem 1rem;
    border: 1px solid var(--medium-gray);
    border-radius: var(--border-radius-sm);
    flex: 1;
    font-size: 0.9rem;
  }
  
  .search-input:focus, .category-select:focus {
    border-color: var(--primary-color);
    outline: none;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
  
  .shortcuts-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .shortcuts-table th, .shortcuts-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--light-gray);
  }
  
  .shortcuts-table th {
    font-weight: 600;
    color: var(--dark-gray);
    background-color: var(--light-gray);
  }
  
  .action-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .action-icon {
    width: 24px;
    height: 24px;
    background-color: var(--light-gray);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary-color);
    font-size: 0.8rem;
  }
  
  .action-name {
    font-weight: 500;
  }
  
  .key-cell {
    width: 120px;
  }
  
  .key-display {
    background-color: var(--light-gray);
    padding: 0.4rem 0.75rem;
    border-radius: var(--border-radius-sm);
    display: inline-block;
    font-family: monospace;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-color);
    min-width: 30px;
    text-align: center;
  }
  
  .category-badge {
    padding: 0.3rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .category-movement {
    background-color: rgba(52, 152, 219, 0.2);
    color: #2980b9;
  }
  
  .category-camera {
    background-color: rgba(155, 89, 182, 0.2);
    color: #8e44ad;
  }
  
  .category-emergency {
    background-color: rgba(231, 76, 60, 0.2);
    color: #c0392b;
  }
  
  .actions-cell {
    width: 100px;
  }
  
  .btn-edit {
    padding: 0.4rem 0.75rem;
    background-color: var(--light-gray);
    color: var(--dark-gray);
    border-radius: var(--border-radius-sm);
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }
  
  .btn-edit:hover {
    background-color: var(--primary-color);
    color: white;
  }
  
/* Rebind Modal */
.rebind-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background-color: white;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 500px;
  overflow: hidden;
  animation: modal-appear 0.3s ease-out;
}

@keyframes modal-appear {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background-color: var(--primary-color);
  color: white;
}

.modal-header h3 {
  margin: 0;
  color: white;
  font-size: 1.25rem;
}

.btn-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.25rem;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.btn-close:hover {
  opacity: 1;
  background: none;
  transform: scale(1.1);
  box-shadow: none;
}

.modal-body {
  padding: 2rem;
}

.rebind-info {
  margin-bottom: 2rem;
}

.rebind-label, .rebind-current {
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
  color: var(--text-color);
}

.current-key {
  background-color: var(--light-gray);
  padding: 0.3rem 0.6rem;
  border-radius: var(--border-radius-sm);
  font-family: monospace;
  font-weight: 600;
  margin-left: 0.5rem;
}

.rebind-key-prompt {
  padding: 2rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  text-align: center;
}

.key-icon {
  width: 64px;
  height: 64px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  color: var(--primary-color);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  70% {
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
}

.rebind-key-prompt p {
  margin-bottom: 0.75rem;
  color: var(--text-color);
  font-size: 1.1rem;
}

.rebind-hint {
  color: var(--dark-gray);
  font-size: 0.9rem !important;
}

/* Responsive Design */
@media screen and (max-width: 992px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
}

@media screen and (max-width: 768px) {
  .list-filter {
    flex-direction: column;
  }
  
  .shortcuts-table th, .shortcuts-table td {
    padding: 0.75rem;
  }
  
  .shortcuts-table {
    font-size: 0.9rem;
  }
  
  .key-display {
    font-size: 0.8rem;
  }
  
  .action-name {
    font-size: 0.9rem;
  }
}

@media screen and (max-width: 576px) {
  .header-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .btn-save, .btn-reset {
    width: 100%;
    justify-content: center;
  }
  
  .modal-content {
    width: 90%;
  }
}
</style>
