<template>
    <div class="face-recognition-control">
      <div class="mode-content">
        <div v-if="!showFaceSelector && !previewImage" class="upload-section">
          <div class="upload-area" 
               :class="{ 'drag-over': isDragging }"
               @dragover.prevent="onDragOver"
               @dragleave.prevent="onDragLeave"
               @drop.prevent="onDrop">
            <div class="upload-placeholder">
              <font-awesome-icon icon="cloud-upload-alt"/>
              <p>Glissez et déposez une photo de visage, ou <span class="browse-link" @click="triggerFileInput">parcourez</span></p>
              <p class="file-formats">Formats acceptés: JPG, PNG, JPEG, WEBP</p>
            </div>
            <input type="file" 
                  ref="fileInput" 
                  class="file-input" 
                  accept=".jpg,.jpeg,.png,.webp" 
                  @change="onFileSelected" />
          </div>
        </div>
        
        <div v-if="previewImage && !showFaceSelector" class="preview-container">
          <div class="preview-controls">
            <button class="btn-cancel" @click="removeImage">
              <font-awesome-icon icon="times"/> Annuler
            </button>
            <button class="btn-primary" @click="startFaceSelection">
              <font-awesome-icon icon="crosshairs"/> Marquer le visage
            </button>
          </div>
          <div class="preview-image-container">
            <img :src="previewImage" alt="Aperçu de l'image" class="preview-image"/>
          </div>
        </div>
        
        <div v-if="showFaceSelector" class="face-selector-container">
          <div class="selector-instructions">
            <p>Positionnez et redimensionnez le cadre pour englober le visage</p>
          </div>
          <div class="selector-controls">
            <button class="btn-cancel" @click="cancelFaceSelection">
              <font-awesome-icon icon="arrow-left"/> Retour
            </button>
            <button class="btn-primary" @click="confirmFaceSelection">
              <font-awesome-icon icon="check"/> Confirmer la sélection
            </button>
          </div>
          <div class="selector-canvas-container" ref="canvasContainer">
            <img :src="previewImage" ref="selectorImage" class="selector-image"/>
            <div class="face-rectangle" 
                 ref="faceRect"
                 :style="{
                   left: `${faceRect.x}px`,
                   top: `${faceRect.y}px`,
                   width: `${faceRect.width}px`,
                   height: `${faceRect.height}px`
                 }"
                 @mousedown="startDrag"
                 @touchstart="startDrag">
              <div class="resize-handle top-left" @mousedown="startResize('topLeft')" @touchstart="startResize('topLeft')"></div>
              <div class="resize-handle top-right" @mousedown="startResize('topRight')" @touchstart="startResize('topRight')"></div>
              <div class="resize-handle bottom-left" @mousedown="startResize('bottomLeft')" @touchstart="startResize('bottomLeft')"></div>
              <div class="resize-handle bottom-right" @mousedown="startResize('bottomRight')" @touchstart="startResize('bottomRight')"></div>
            </div>
          </div>
        </div>
        
        <div v-if="confirmSelection" class="person-form">
          <div class="form-header">
            <h4>Informations sur la personne</h4>
          </div>
          <div class="form-group">
            <label for="personName">Nom de la personne</label>
            <input type="text" id="personName" v-model="personName" placeholder="Ex: Jean Dupont"/>
          </div>
          <div class="form-group">
            <label for="personRelation">Relation</label>
            <select id="personRelation" v-model="personRelation">
              <option value="family">Famille</option>
              <option value="friend">Ami</option>
              <option value="colleague">Collègue</option>
              <option value="other">Autre</option>
            </select>
          </div>
          <div class="person-actions">
            <button class="btn-cancel" @click="cancelPersonForm">
              <font-awesome-icon icon="times"/> Annuler
            </button>
            <button class="btn-primary" @click="savePerson" :disabled="!personName">
              <font-awesome-icon icon="save"/> Enregistrer
            </button>
          </div>
        </div>
        
        <div class="people-list" v-if="people.length > 0">
          <div class="list-header">
            <h4>Personnes enregistrées</h4>
            <button class="btn-refresh" @click="loadPeople">
              <font-awesome-icon icon="sync-alt"/>
            </button>
          </div>
          <div class="people-grid">
            <div v-for="person in people" :key="person.id" class="person-card">
              <div class="person-image">
                <img :src="person.image" :alt="person.name"/>
                <div class="person-badges">
                  <span class="badge" :class="`relation-${person.relation}`">
                    {{ getRelationLabel(person.relation) }}
                  </span>
                </div>
              </div>
              <div class="person-info">
                <h5>{{ person.name }}</h5>
                <p class="person-date">Ajouté le {{ formatDate(person.dateAdded) }}</p>
              </div>
              <div class="person-actions">
                <button class="btn-icon btn-delete" @click="deletePerson(person)">
                  <font-awesome-icon icon="trash-alt"/>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else-if="faceRecognitionEnabled && !previewImage && !showFaceSelector" class="empty-people">
          <font-awesome-icon icon="users"/>
          <p>Aucune personne enregistrée</p>
          <p class="hint">Ajoutez des personnes en téléchargeant leurs photos</p>
        </div>
      </div>
      
      <div v-if="!faceRecognitionEnabled" class="mode-not-available">
        <p>Activez la reconnaissance faciale pour commencer.</p>
      </div>
    </div>
  </template>
  
  <script>
  import faceRecognitionService from '../services/faceRecognitionService';
  
  export default {
    name: 'FaceRecognitionControl',
    data() {
      return {
        faceRecognitionEnabled: false,
        isDragging: false,
        previewImage: null,
        selectedFile: null,
        showFaceSelector: false,
        confirmSelection: false,
        personName: '',
        personRelation: 'family',
        people: [],
        isSaving: false,
        faceRect: {
          x: 50,
          y: 50,
          width: 200,
          height: 200
        },
        dragInfo: {
          isDragging: false,
          isResizing: false,
          resizeHandle: null,
          startX: 0,
          startY: 0,
          rectStartX: 0,
          rectStartY: 0,
          rectStartWidth: 0,
          rectStartHeight: 0
        }
      };
    },
    mounted() {
      this.loadPeople();
      
      // Ajouter les écouteurs d'événements pour le déplacement et le redimensionnement
      window.addEventListener('mousemove', this.onMouseMove);
      window.addEventListener('mouseup', this.stopDragResize);
      window.addEventListener('touchmove', this.onTouchMove, { passive: false });
      window.addEventListener('touchend', this.stopDragResize);
    },
    beforeUnmount() {
      // Nettoyer les écouteurs d'événements
      window.removeEventListener('mousemove', this.onMouseMove);
      window.removeEventListener('mouseup', this.stopDragResize);
      window.removeEventListener('touchmove', this.onTouchMove);
      window.removeEventListener('touchend', this.stopDragResize);
    },
    methods: {
      handleFaceRecognitionToggle() {
        if (this.faceRecognitionEnabled) {
          this.loadPeople();
        }
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
          this.showNotification('Format de fichier non supporté. Veuillez utiliser JPG, PNG ou WEBP.', 'error');
          return;
        }
        
        // Vérifier la taille du fichier (max 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
          this.showNotification('Le fichier est trop volumineux. Taille maximale: 5MB', 'error');
          return;
        }
        
        // Prévisualiser l'image
        this.selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewImage = e.target.result;
          
          // Réinitialiser les états
          this.showFaceSelector = false;
          this.confirmSelection = false;
        };
        reader.readAsDataURL(file);
      },
      removeImage() {
        this.previewImage = null;
        this.selectedFile = null;
        this.showFaceSelector = false;
        this.confirmSelection = false;
        
        if (this.$refs.fileInput) {
          this.$refs.fileInput.value = '';
        }
      },
      startFaceSelection() {
        this.showFaceSelector = true;
        
        // Réinitialiser la position du rectangle à une valeur par défaut centrée
        this.$nextTick(() => {
          if (this.$refs.selectorImage && this.$refs.canvasContainer) {
            const container = this.$refs.canvasContainer;
            const img = this.$refs.selectorImage;
            
            // Attendre que l'image soit chargée pour obtenir ses dimensions
            if (img.complete) {
              this.initializeFaceRect(container, img);
            } else {
              img.onload = () => {
                this.initializeFaceRect(container, img);
              };
            }
          }
        });
      },
      initializeFaceRect(container, img) {
        // Placer le rectangle au centre de l'image
        const containerRect = container.getBoundingClientRect();
        const width = Math.min(200, img.width * 0.3);
        const height = width;
        
        this.faceRect = {
          x: (containerRect.width - width) / 2,
          y: (containerRect.height - height) / 2,
          width: width,
          height: height
        };
      },
      cancelFaceSelection() {
        this.showFaceSelector = false;
      },
      confirmFaceSelection() {
        this.showFaceSelector = false;
        this.confirmSelection = true;
      },
      cancelPersonForm() {
        this.confirmSelection = false;
        this.personName = '';
        this.personRelation = 'family';
      },
      async savePerson() {
        if (!this.personName || !this.selectedFile || this.isSaving) return;
        
        this.isSaving = true;
        
        try {
          // Créer un canvas pour extraire uniquement la zone du visage
          const img = new Image();
          img.src = this.previewImage;
          
          // Attendre que l'image soit chargée
          await new Promise((resolve) => {
            if (img.complete) {
              resolve();
            } else {
              img.onload = resolve;
            }
          });
          
          // Calculer les ratios pour s'assurer que les coordonnées du rectangle sont correctes
          const imgElement = this.$refs.selectorImage;
          const displayWidth = imgElement ? imgElement.clientWidth : img.width;
          const displayHeight = imgElement ? imgElement.clientHeight : img.height;
          
          const scaleX = img.width / displayWidth;
          const scaleY = img.height / displayHeight;
          
          // Coordonnées ajustées du rectangle sur l'image originale
          const actualX = this.faceRect.x * scaleX;
          const actualY = this.faceRect.y * scaleY;
          const actualWidth = this.faceRect.width * scaleX;
          const actualHeight = this.faceRect.height * scaleY;
          
          // Créer un nouvel objet File à partir de la portion de l'image
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          
          canvas.width = actualWidth;
          canvas.height = actualHeight;
          
          ctx.drawImage(
            img,
            actualX, actualY, actualWidth, actualHeight,
            0, 0, actualWidth, actualHeight
          );
          
          // Convertir le canvas en blob
          const blob = await new Promise(resolve => {
            canvas.toBlob(resolve, 'image/jpeg', 0.95);
          });
          
          // Créer un nouveau fichier
          const faceFile = new File([blob], 'face_' + this.selectedFile.name, {
            type: 'image/jpeg'
          });
          
          // Utiliser le service pour ajouter la personne
          const personData = {
            name: this.personName,
            relation: this.personRelation
          };
          
          const response = await faceRecognitionService.addPerson(faceFile, personData);
          
          if (response.success) {
            // Ajouter à la liste locale
            this.people.unshift(response.data);
            
            // Réinitialiser le formulaire
            this.resetForm();
            
            // Notification de succès
            this.showNotification('Personne ajoutée avec succès', 'success');
          } else {
            throw new Error(response.message || 'Erreur lors de l\'ajout');
          }
        } catch (error) {
          console.error('Erreur lors de l\'ajout d\'une personne:', error);
          this.showNotification('Erreur lors de l\'ajout: ' + error.message, 'error');
        } finally {
          this.isSaving = false;
        }
      },
      resetForm() {
        this.removeImage();
        this.personName = '';
        this.personRelation = 'family';
        this.confirmSelection = false;
      },
      async loadPeople() {
        try {
          const response = await faceRecognitionService.getPeople();
          
          if (response.success) {
            this.people = response.data;
          } else {
            throw new Error(response.message || 'Erreur lors du chargement');
          }
        } catch (error) {
          console.error('Erreur lors du chargement des personnes:', error);
          this.showNotification('Erreur lors du chargement des personnes', 'error');
          this.people = [];
        }
      },
      async deletePerson(person) {
        if (confirm(`Êtes-vous sûr de vouloir supprimer ${person.name} ?`)) {
          try {
            const response = await faceRecognitionService.deletePerson(person.id);
            
            if (response.success) {
              // Mettre à jour la liste locale
              this.people = this.people.filter(p => p.id !== person.id);
              
              this.showNotification('Personne supprimée avec succès', 'info');
            } else {
              throw new Error(response.message || 'Erreur lors de la suppression');
            }
          } catch (error) {
            console.error('Erreur lors de la suppression:', error);
            this.showNotification('Erreur lors de la suppression', 'error');
          }
        }
      },
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR');
      },
      getRelationLabel(relation) {
        const labels = {
          family: 'Famille',
          friend: 'Ami',
          colleague: 'Collègue',
          other: 'Autre'
        };
        return labels[relation] || 'Autre';
      },
      showNotification(message, type = 'info') {
        // Utiliser le système de notification global
        if (this.$notify) {
          this.$notify[type](message);
        } else {
          // Fallback sur alert si le plugin n'est pas disponible
          alert(message);
        }
      },
      
      // Gestion du déplacement et du redimensionnement du rectangle
      startDrag(event) {
        event.preventDefault();
        event.stopPropagation();
        
        const pageX = event.type === 'mousedown' ? event.pageX : event.touches[0].pageX;
        const pageY = event.type === 'mousedown' ? event.pageY : event.touches[0].pageY;
        
        this.dragInfo = {
          isDragging: true,
          isResizing: false,
          startX: pageX,
          startY: pageY,
          rectStartX: this.faceRect.x,
          rectStartY: this.faceRect.y
        };
      },
      startResize(handle) {
        event.preventDefault();
        event.stopPropagation();
        
        const pageX = event.type === 'mousedown' ? event.pageX : event.touches[0].pageX;
        const pageY = event.type === 'mousedown' ? event.pageY : event.touches[0].pageY;
        
        this.dragInfo = {
          isDragging: false,
          isResizing: true,
          resizeHandle: handle,
          startX: pageX,
          startY: pageY,
          rectStartX: this.faceRect.x,
          rectStartY: this.faceRect.y,
          rectStartWidth: this.faceRect.width,
          rectStartHeight: this.faceRect.height
        };
      },
      onMouseMove(event) {
        if (!this.dragInfo.isDragging && !this.dragInfo.isResizing) return;
        
        const pageX = event.pageX;
        const pageY = event.pageY;
        
        this.handleDragResize(pageX, pageY);
      },
      onTouchMove(event) {
        if (!this.dragInfo.isDragging && !this.dragInfo.isResizing) return;
        
        event.preventDefault(); // Empêcher le défilement pendant le déplacement ou le redimensionnement
        
        const touch = event.touches[0];
        const pageX = touch.pageX;
        const pageY = touch.pageY;
        
        this.handleDragResize(pageX, pageY);
      },
      handleDragResize(pageX, pageY) {
        if (!this.$refs.canvasContainer) return;
        
        const container = this.$refs.canvasContainer.getBoundingClientRect();
        const deltaX = pageX - this.dragInfo.startX;
        const deltaY = pageY - this.dragInfo.startY;
        
        if (this.dragInfo.isDragging) {
          // Déplacement du rectangle
          let newX = this.dragInfo.rectStartX + deltaX;
          let newY = this.dragInfo.rectStartY + deltaY;
          
          // Limiter au conteneur
          newX = Math.max(0, Math.min(newX, container.width - this.faceRect.width));
          newY = Math.max(0, Math.min(newY, container.height - this.faceRect.height));
          
          this.faceRect.x = newX;
          this.faceRect.y = newY;
        } else if (this.dragInfo.isResizing) {
          // Redimensionnement du rectangle
          const handle = this.dragInfo.resizeHandle;
          let newX = this.faceRect.x;
          let newY = this.faceRect.y;
          let newWidth = this.faceRect.width;
          let newHeight = this.faceRect.height;
          
          switch (handle) {
            case 'topLeft':
              newX = this.dragInfo.rectStartX + deltaX;
              newY = this.dragInfo.rectStartY + deltaY;
              newWidth = Math.max(50, this.dragInfo.rectStartWidth - deltaX);
              newHeight = Math.max(50, this.dragInfo.rectStartHeight - deltaY);
              break;
            case 'topRight':
              newY = this.dragInfo.rectStartY + deltaY;
              newWidth = Math.max(50, this.dragInfo.rectStartWidth + deltaX);
              newHeight = Math.max(50, this.dragInfo.rectStartHeight - deltaY);
              break;
            case 'bottomLeft':
              newX = this.dragInfo.rectStartX + deltaX;
              newWidth = Math.max(50, this.dragInfo.rectStartWidth - deltaX);
              newHeight = Math.max(50, this.dragInfo.rectStartHeight + deltaY);
              break;
            case 'bottomRight':
              newWidth = Math.max(50, this.dragInfo.rectStartWidth + deltaX);
              newHeight = Math.max(50, this.dragInfo.rectStartHeight + deltaY);
              break;
          }
          
          // Limiter au conteneur
          if (newX + newWidth > container.width) {
            newWidth = container.width - newX;
          }
          if (newY + newHeight > container.height) {
            newHeight = container.height - newY;
          }
          
          // Maintenir les proportions (aspect ratio 1:1)
          const square = Math.min(newWidth, newHeight);
          
          // Mettre à jour les propriétés du rectangle
          this.faceRect.x = newX;
          this.faceRect.y = newY;
          this.faceRect.width = square;
          this.faceRect.height = square;
        }
      },
      stopDragResize() {
        this.dragInfo.isDragging = false;
        this.dragInfo.isResizing = false;
      }
    }
  };
</script>
  
<style scoped>
  .face-recognition-control {
    width: 100%;
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
  
  .slider.round {
    border-radius: 34px;
  }
  
  .slider.round:before {
    border-radius: 50%;
  }
  
  /* Upload area */
  .upload-area {
    border: 2px dashed var(--medium-gray);
    border-radius: var(--border-radius-md);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    transition: all 0.3s ease;
  }
  
  .upload-area.drag-over {
    background-color: rgba(52, 152, 219, 0.05);
    border-color: var(--primary-color);
  }
  
  .upload-placeholder {
    text-align: center;
  }
  
  .upload-placeholder i {
    font-size: 2.5rem;
    color: var(--medium-gray);
    margin-bottom: 1rem;
  }
  
  .upload-placeholder p {
    color: var(--dark-gray);
    margin-bottom: 0.5rem;
  }
  
  .file-formats {
    font-size: 0.9rem;
    color: var(--medium-gray);
  }
  
  .browse-link {
    color: var(--primary-color);
    cursor: pointer;
    text-decoration: underline;
  }
  
  .file-input {
    display: none;
  }
  
  /* Preview container */
  .preview-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .preview-controls {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
  }
  
  .preview-image-container {
    max-height: 400px;
    overflow: hidden;
    border-radius: var(--border-radius-md);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .preview-image {
    width: 100%;
    height: auto;
    display: block;
  }
  
  /* Face selector */
  .face-selector-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .selector-instructions {
    text-align: center;
    margin-bottom: 0.5rem;
  }
  
  .selector-controls {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
  }
  
  .selector-canvas-container {
    position: relative;
    width: 100%;
    height: 400px;
    overflow: hidden;
    border-radius: var(--border-radius-md);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    background-color: rgba(0, 0, 0, 0.1);
  }
  
  .selector-image {
    max-width: 100%;
    max-height: 100%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .face-rectangle {
    position: absolute;
    border: 2px solid var(--primary-color);
    background-color: rgba(52, 152, 219, 0.2);
    box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0.3);
    cursor: move;
  }
  
  .resize-handle {
    position: absolute;
    width: 10px;
    height: 10px;
    background-color: white;
    border: 2px solid var(--primary-color);
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    z-index: 2;
  }
  
  .top-left {
    top: -5px;
    left: -5px;
    cursor: nwse-resize;
  }
  
  .top-right {
    top: -5px;
    right: -5px;
    cursor: nesw-resize;
  }
  
  .bottom-left {
    bottom: -5px;
    left: -5px;
    cursor: nesw-resize;
  }
  
  .bottom-right {
    bottom: -5px;
    right: -5px;
    cursor: nwse-resize;
  }
  
  /* Person form */
  .person-form {
    background-color: var(--light-gray);
    border-radius: var(--border-radius-md);
    padding: 1.5rem;
  }
  
  .form-header {
    margin-bottom: 1rem;
  }
  
  .form-header h4 {
    font-size: 1.1rem;
    margin: 0;
    color: var(--text-color);
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-color);
  }
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--medium-gray);
    border-radius: var(--border-radius-sm);
    font-size: 1rem;
  }
  
  .form-group input:focus,
  .form-group select:focus {
    border-color: var(--primary-color);
    outline: none;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
  
  .person-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
  }
  
  /* People list */
  .people-list {
    margin-top: 1.5rem;
  }
  
  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .list-header h4 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-color);
  }
  
  .btn-refresh {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--light-gray);
    color: var(--dark-gray);
    border-radius: 50%;
    border: none;
    transition: all 0.2s ease;
  }
  
  .btn-refresh:hover {
    background-color: var(--medium-gray);
    color: var(--text-color);
    transform: rotate(180deg);
  }
  
  .people-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }
  
  .person-card {
    background-color: white;
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
  }
  
  .person-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
  
  .person-image {
    position: relative;
    aspect-ratio: 1;
    overflow: hidden;
  }
  
  .person-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .person-badges {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .badge {
    padding: 0.2rem 0.5rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
  }
  
  .relation-family {
    background-color: rgba(46, 204, 113, 0.8);
  }
  
  .relation-friend {
    background-color: rgba(52, 152, 219, 0.8);
  }
  
  .relation-colleague {
    background-color: rgba(155, 89, 182, 0.8);
  }
  
  .relation-other {
    background-color: rgba(149, 165, 166, 0.8);
  }
  
  .person-info {
    padding: 0.75rem;
  }
  
  .person-info h5 {
    margin: 0 0 0.25rem 0;
    font-size: 0.9rem;
    color: var(--text-color);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .person-date {
    margin: 0;
    font-size: 0.7rem;
    color: var(--dark-gray);
  }
  
  .person-actions {
    display: flex;
    justify-content: flex-end;
    padding: 0 0.75rem 0.75rem;
  }
  
  .btn-icon {
    width: 28px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .btn-delete {
    background-color: rgba(231, 76, 60, 0.2);
    color: #e74c3c;
  }
  
  .btn-delete:hover {
    background-color: #e74c3c;
    color: white;
  }
  
  /* Empty state */
  .empty-people {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    color: var(--medium-gray);
  }
  
  .empty-people i {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  
  .empty-people p {
    margin: 0 0 0.5rem 0;
    color: var(--dark-gray);
  }
  
  .empty-people .hint {
    font-size: 0.9rem;
  }
  
  /* Buttons */
  .btn-primary,
  .btn-cancel {
    padding: 0.75rem 1.25rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
  }
  
  .btn-primary {
    background-color: var(--primary-color);
    color: white;
    border: none;
  }
  
  .btn-primary:hover:not(:disabled) {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
  }
  
  .btn-primary:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  .btn-cancel {
    background-color: var(--light-gray);
    color: var(--dark-gray);
    border: none;
  }
  
  .btn-cancel:hover {
    background-color: var(--medium-gray);
    color: var(--text-color);
  }
  
  /* Media queries for responsiveness */
  @media (max-width: 768px) {
    .preview-controls,
    .selector-controls {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .btn-primary,
    .btn-cancel {
      width: 100%;
      justify-content: center;
    }
    
    .people-grid {
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }
    
    .selector-canvas-container {
      height: 300px;
    }
  }
</style>