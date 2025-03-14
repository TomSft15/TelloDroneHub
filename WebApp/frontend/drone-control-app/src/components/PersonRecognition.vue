<template>
  <div class="person-recognition">
    <div class="section-header">
      <h2><i class="fas fa-user-plus"></i> Reconnaissance faciale</h2>
      <p class="section-description">
        Ajoutez des photos de personnes pour que le drone puisse les reconnaître en vol.
      </p>
    </div>

    <div class="recognition-container">
      <div class="upload-section card">
        <div class="card-header">
          <h3>Ajouter une personne</h3>
        </div>
        <div class="card-content">
          <div class="upload-area" 
               :class="{ 'drag-over': isDragging }"
               @dragover.prevent="onDragOver"
               @dragleave.prevent="onDragLeave"
               @drop.prevent="onDrop">
            <div v-if="!previewImage" class="upload-placeholder">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>Glissez et déposez une photo de visage, ou <span class="browse-link" @click="triggerFileInput">parcourez</span></p>
              <p class="file-formats">Formats acceptés: JPG, PNG, JPEG, WEBP</p>
            </div>
            <div v-else class="preview-container">
              <img :src="previewImage" alt="Aperçu de l'image" class="preview-image" />
              <button class="btn-remove" @click="removeImage">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <input type="file" 
                  ref="fileInput" 
                  class="file-input" 
                  accept=".jpg,.jpeg,.png,.webp" 
                  @change="onFileSelected" />
          </div>
          
          <div class="person-form" :class="{ 'disabled': !previewImage }">
            <div class="form-group">
              <label for="personName">Nom de la personne</label>
              <input type="text" 
                    id="personName" 
                    v-model="personName" 
                    placeholder="Ex: Jean Dupont" 
                    :disabled="!previewImage" />
            </div>
            <div class="form-group">
              <label for="personRelation">Relation</label>
              <select id="personRelation" v-model="personRelation" :disabled="!previewImage">
                <option value="family">Famille</option>
                <option value="friend">Ami</option>
                <option value="colleague">Collègue</option>
                <option value="other">Autre</option>
              </select>
            </div>
            <div class="form-controls">
              <button class="btn-primary" 
                      @click="savePerson" 
                      :disabled="!canSave">
                <i class="fas fa-save"></i> Enregistrer
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="recognition-database card">
        <div class="card-header">
          <h3>Personnes enregistrées</h3>
          <div class="header-actions">
            <button class="btn-refresh" @click="loadPeople">
              <i class="fas fa-sync-alt"></i>
            </button>
            <div class="search-box">
              <input type="text" placeholder="Rechercher..." v-model="searchQuery" />
              <i class="fas fa-search"></i>
            </div>
          </div>
        </div>
        <div class="card-content">
          <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Chargement des données...</p>
          </div>
          
          <div v-else-if="people.length === 0" class="empty-state">
            <i class="fas fa-users-slash"></i>
            <p>Aucune personne enregistrée</p>
            <p class="hint">Ajoutez des personnes à l'aide du formulaire ci-contre.</p>
          </div>
          
          <div v-else class="people-grid">
            <div v-for="person in filteredPeople" :key="person.id" class="person-card">
              <div class="person-image">
                <img :src="person.image" :alt="person.name" />
                <div class="person-badges">
                  <span class="badge" :class="`relation-${person.relation}`">
                    {{ getRelationLabel(person.relation) }}
                  </span>
                </div>
              </div>
              <div class="person-info">
                <h4>{{ person.name }}</h4>
                <p class="person-date">Ajouté le {{ formatDate(person.dateAdded) }}</p>
              </div>
              <div class="person-actions">
                <button class="btn-icon btn-edit" @click="editPerson(person)">
                  <i class="fas fa-pencil-alt"></i>
                </button>
                <button class="btn-icon btn-delete" @click="deletePerson(person)">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="recognition-settings card">
      <div class="card-header">
        <h3>Paramètres de reconnaissance</h3>
      </div>
      <div class="card-content">
        <div class="settings-grid">
          <div class="setting-item">
            <div class="setting-label">
              <h4>Reconnaissance active</h4>
              <p>Activer la reconnaissance des personnes pendant le vol</p>
            </div>
            <div class="setting-control">
              <label class="switch">
                <input type="checkbox" v-model="settings.enabled">
                <span class="slider round"></span>
              </label>
            </div>
          </div>
          
          <div class="setting-item">
            <div class="setting-label">
              <h4>Suivi automatique</h4>
              <p>Le drone suit automatiquement les personnes reconnues</p>
            </div>
            <div class="setting-control">
              <label class="switch">
                <input type="checkbox" v-model="settings.autoTracking" :disabled="!settings.enabled">
                <span class="slider round"></span>
              </label>
            </div>
          </div>
          
          <div class="setting-item">
            <div class="setting-label">
              <h4>Confiance minimale</h4>
              <p>Seuil de confiance pour la reconnaissance (en %)</p>
            </div>
            <div class="setting-control">
              <div class="range-control">
                <input type="range" min="50" max="95" v-model.number="settings.confidenceThreshold" :disabled="!settings.enabled">
                <span class="range-value">{{ settings.confidenceThreshold }}%</span>
              </div>
            </div>
          </div>
          
          <div class="setting-item">
            <div class="setting-label">
              <h4>Notifications sonores</h4>
              <p>Émettre un son lors de la reconnaissance d'une personne</p>
            </div>
            <div class="setting-control">
              <label class="switch">
                <input type="checkbox" v-model="settings.soundNotification" :disabled="!settings.enabled">
                <span class="slider round"></span>
              </label>
            </div>
          </div>
        </div>
        
        <div class="settings-footer">
          <button class="btn-primary" @click="saveSettings">
            <i class="fas fa-save"></i> Enregistrer les paramètres
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import faceRecognitionService from '../services/faceRecognitionService';

export default {
  name: 'PersonRecognition',
  data() {
    return {
      isDragging: false,
      previewImage: null,
      selectedFile: null,
      personName: '',
      personRelation: 'family',
      people: [],
      loading: true,
      searchQuery: '',
      settings: {
        enabled: true,
        autoTracking: false,
        confidenceThreshold: 75,
        soundNotification: true
      },
      isSaving: false,
      savingSettings: false,
      notification: {
        show: false,
        message: '',
        type: 'info',
        timeout: null
      }
    }
  },
  computed: {
    canSave() {
      return this.previewImage !== null && this.personName.trim() !== '' && !this.isSaving;
    },
    filteredPeople() {
      if (!this.searchQuery) return this.people;
      
      const query = this.searchQuery.toLowerCase();
      return this.people.filter(person => 
        person.name.toLowerCase().includes(query) || 
        this.getRelationLabel(person.relation).toLowerCase().includes(query)
      );
    }
  },
  mounted() {
    this.loadPeople();
    this.loadSettings();
  },
  methods: {
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
      };
      reader.readAsDataURL(file);
    },
    removeImage() {
      this.previewImage = null;
      this.selectedFile = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },
    async savePerson() {
      if (!this.canSave || this.isSaving) return;
      
      this.isSaving = true;
      
      try {
        // Utiliser le service pour ajouter la personne
        const personData = {
          name: this.personName,
          relation: this.personRelation
        };
        
        const response = await faceRecognitionService.addPerson(this.selectedFile, personData);
        
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
    },
    async loadPeople() {
      this.loading = true;
      
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
      } finally {
        this.loading = false;
      }
    },
    async editPerson(person) {
      // Pour l'interface utilisateur améliorée, nous pourrions utiliser un modal ici
      // Pour l'instant, on garde la version simple avec prompt
      const newName = prompt('Modifier le nom:', person.name);
      
      if (newName && newName.trim() !== '') {
        try {
          const response = await faceRecognitionService.updatePerson(person.id, {
            name: newName
          });
          
          if (response.success) {
            // Mettre à jour la liste locale
            const index = this.people.findIndex(p => p.id === person.id);
            if (index !== -1) {
              this.people[index].name = newName;
            }
            
            this.showNotification('Personne modifiée avec succès', 'success');
          } else {
            throw new Error(response.message || 'Erreur lors de la modification');
          }
        } catch (error) {
          console.error('Erreur lors de la modification:', error);
          this.showNotification('Erreur lors de la modification', 'error');
        }
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
    async loadSettings() {
      try {
        const response = await faceRecognitionService.getSettings();
        
        if (response.success) {
          this.settings = response.data;
        } else {
          throw new Error(response.message || 'Erreur lors du chargement des paramètres');
        }
      } catch (error) {
        console.error('Erreur lors du chargement des paramètres:', error);
        // On garde les paramètres par défaut
      }
    },
    async saveSettings() {
      if (this.savingSettings) return;
      
      this.savingSettings = true;
      
      try {
        const response = await faceRecognitionService.saveSettings(this.settings);
        
        if (response.success) {
          this.showNotification('Paramètres enregistrés avec succès', 'success');
        } else {
          throw new Error(response.message || 'Erreur lors de l\'enregistrement des paramètres');
        }
      } catch (error) {
        console.error('Erreur lors de l\'enregistrement des paramètres:', error);
        this.showNotification('Erreur lors de l\'enregistrement des paramètres', 'error');
      } finally {
        this.savingSettings = false;
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
    }
  }
}
</script>

<style scoped>
.person-recognition {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-color);
  margin-bottom: 0.75rem;
}

.section-header h2 i {
  color: var(--primary-color);
}

.section-description {
  color: var(--dark-gray);
  font-size: 1.1rem;
  max-width: 700px;
}

.recognition-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background-color: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--card-shadow);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background-color: var(--light-gray);
  border-bottom: 1px solid var(--medium-gray);
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--text-color);
}

.card-content {
  padding: 1.5rem;
}

/* Upload Section */
.upload-area {
  border: 2px dashed var(--medium-gray);
  border-radius: var(--border-radius-md);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
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
  font-size: 3rem;
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

.preview-container {
  position: relative;
  width: 100%;
  max-width: 200px;
}

.preview-image {
  width: 100%;
  height: auto;
  border-radius: var(--border-radius-sm);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-remove {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: var(--accent-color);
  color: white;
  border: 2px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  padding: 0;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.person-form {
  opacity: 1;
  transition: opacity 0.3s ease;
}

.person-form.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.form-group {
  margin-bottom: 1.5rem;
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
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-group input:disabled,
.form-group select:disabled {
  background-color: var(--light-gray);
  cursor: not-allowed;
}

.form-controls {
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-md);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background-color: var(--medium-gray);
  cursor: not-allowed;
  transform: none;
}

/* Recognition Database */
.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-refresh {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  color: var(--dark-gray);
  border: 1px solid var(--medium-gray);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-refresh:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
  transform: rotate(180deg);
}

.search-box {
  position: relative;
}

.search-box input {
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  border: 1px solid var(--medium-gray);
  border-radius: 20px;
  font-size: 0.9rem;
}

.search-box i {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--medium-gray);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--light-gray);
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  text-align: center;
  color: var(--medium-gray);
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state .hint {
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.people-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}

.person-card {
  background-color: var(--light-gray);
  border-radius: var(--border-radius-md);
  overflow: hidden;
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
  padding: 0.25rem 0.5rem;
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

.person-info h4 {
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
  justify-content: space-between;
  padding: 0 0.75rem 0.75rem;
}

.btn-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit {
  background-color: rgba(52, 152, 219, 0.2);
  color: #3498db;
}

.btn-delete {
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.btn-edit:hover {
  background-color: #3498db;
  color: white;
}

.btn-delete:hover {
  background-color: #e74c3c;
  color: white;
}

/* Recognition Settings */
.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--light-gray);
  border-radius: var(--border-radius-sm);
}

.setting-label {
  flex: 1;
}

.setting-label h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: var(--text-color);
}

.setting-label p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--dark-gray);
}

/* Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 24px;
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
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: var(--primary-color);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--primary-color);
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
}

/* Range input */
.range-control {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.range-control input {
  flex: 1;
}

.range-value {
  font-weight: 600;
  color: var(--text-color);
  min-width: 40px;
  text-align: right;
}

.settings-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

/* Responsive */
@media screen and (max-width: 992px) {
  .recognition-container {
    grid-template-columns: 1fr;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 576px) {
  .people-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>