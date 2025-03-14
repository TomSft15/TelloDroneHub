<template>
  <div class="vision-control-page">
    <div class="page-header">
      <h1><i class="fas fa-eye"></i> Vision et reconnaissance</h1>
      <p class="page-description">
        Utilisez la vision par ordinateur pour permettre au drone de détecter et suivre des personnes ou des objets.
      </p>
    </div>
    
    <!-- Section de reconnaissance faciale -->
    <div class="control-card">
      <div class="card-header">
        <h3><i class="fas fa-user-plus"></i> Ajoutez des personnes à reconnaître</h3>
        <button @click="toggleFaceRecognitionSection" 
                :class="{ 'btn-active': faceRecognitionExpanded, 'btn-inactive': !faceRecognitionExpanded }">
          {{ faceRecognitionExpanded ? 'Masquer' : 'Afficher' }}
        </button>
      </div>
      
      <div v-if="faceRecognitionExpanded" class="face-recognition">
        <div class="command-group">
          <h4>1. Ajouter une personne</h4>
          <div class="upload-area" 
               :class="{ 'drag-over': isDragging, 'has-image': previewImage }"
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
              <button class="btn-remove-image" @click="removeImage">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <input type="file" 
                  ref="fileInput" 
                  class="file-input" 
                  accept=".jpg,.jpeg,.png,.webp" 
                  @change="onFileSelected" />
          </div>
          
          <div class="commands-grid person-form-grid">
            <div class="command-item">
              <div class="command-key">Nom de la personne</div>
              <input type="text" 
                     id="personName" 
                     v-model="personName" 
                     placeholder="Ex: Jean Dupont" 
                     class="person-input"
                     :disabled="!previewImage" />
            </div>
            <div class="command-item">
              <div class="command-key">Relation</div>
              <select id="personRelation" 
                      v-model="personRelation" 
                      class="person-select"
                      :disabled="!previewImage">
                <option value="family">Famille</option>
                <option value="friend">Ami</option>
                <option value="colleague">Collègue</option>
                <option value="other">Autre</option>
              </select>
            </div>
            <div class="command-item">
              <div class="command-key">Enregistrer</div>
              <button @click="savePerson" 
                      :disabled="!canSave"
                      class="btn-command">
                <i class="fas fa-save"></i>
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="people.length > 0" class="command-group">
          <h4>2. Personnes enregistrées</h4>
          
          <div class="commands-grid">
            <div v-for="person in people" :key="person.id" class="command-item">
              <div class="person-image">
                <img :src="person.image" :alt="person.name" />
                <span class="relation-badge" :class="`relation-${person.relation}`">
                  {{ getRelationLabel(person.relation) }}
                </span>
              </div>
              <div class="command-key">{{ person.name }}</div>
              <div class="person-actions">
                <button class="btn-command" @click="editPerson(person)">
                  <i class="fas fa-pencil-alt"></i>
                </button>
                <button class="btn-command btn-emergency" @click="deletePerson(person)">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <i class="fas fa-users-slash"></i>
          <p>Aucune personne enregistrée</p>
          <p class="hint">Ajoutez une photo de personne à l'aide du formulaire ci-dessus.</p>
        </div>
      </div>
    </div>

    <!-- Composant original de contrôle -->
    <ControlMode mode="Vision" />

  </div>
</template>

<script>
import ControlMode from '../ControlMode.vue';

export default {
  name: 'VisionControlView',
  components: {
    ControlMode
  },
  data() {
    return {
      faceRecognitionExpanded: false,
      isDragging: false,
      previewImage: null,
      selectedFile: null,
      personName: '',
      personRelation: 'family',
      people: []
    };
  },
  computed: {
    canSave() {
      return this.previewImage !== null && this.personName.trim() !== '';
    }
  },
  mounted() {
    this.loadPeople();
  },
  methods: {
    toggleFaceRecognitionSection() {
      this.faceRecognitionExpanded = !this.faceRecognitionExpanded;
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
        alert('Format de fichier non supporté. Veuillez utiliser JPG, PNG ou WEBP.');
        return;
      }
      
      // Vérifier la taille du fichier (max 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        alert('Le fichier est trop volumineux. Taille maximale: 5MB');
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
    
    savePerson() {
      if (!this.canSave) return;
      
      // Créer un nouvel objet personne
      const newPerson = {
        id: Date.now(),
        name: this.personName,
        relation: this.personRelation,
        image: this.previewImage,
        dateAdded: new Date().toISOString()
      };
      
      // Ajouter à la liste
      this.people.unshift(newPerson);
      
      // Sauvegarder dans le localStorage (pour la démo)
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      storedPeople.unshift(newPerson);
      localStorage.setItem('recognitionPeople', JSON.stringify(storedPeople));
      
      // Réinitialiser le formulaire
      this.resetForm();
      
      // Notification de succès
      alert('Personne ajoutée avec succès');
    },
    
    resetForm() {
      this.removeImage();
      this.personName = '';
      this.personRelation = 'family';
    },
    
    loadPeople() {
      // Récupérer du localStorage (pour la démo)
      const storedPeople = JSON.parse(localStorage.getItem('recognitionPeople') || '[]');
      this.people = storedPeople;
    },
    
    editPerson(person) {
      // Pour la démo, proposer de changer le nom
      const newName = prompt('Modifier le nom:', person.name);
      if (newName && newName.trim() !== '') {
        const index = this.people.findIndex(p => p.id === person.id);
        if (index !== -1) {
          this.people[index].name = newName;
          
          // Mettre à jour le localStorage
          localStorage.setItem('recognitionPeople', JSON.stringify(this.people));
          alert('Personne modifiée avec succès');
        }
      }
    },
    
    deletePerson(person) {
      if (confirm(`Êtes-vous sûr de vouloir supprimer ${person.name} ?`)) {
        this.people = this.people.filter(p => p.id !== person.id);
        
        // Mettre à jour le localStorage
        localStorage.setItem('recognitionPeople', JSON.stringify(this.people));
        alert('Personne supprimée avec succès');
      }
    },
    
    getRelationLabel(relation) {
      const labels = {
        family: 'Famille',
        friend: 'Ami',
        colleague: 'Collègue',
        other: 'Autre'
      };
      return labels[relation] || 'Autre';
    }
  }
};
</script>

<style scoped>
.vision-control-page {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--light-gray);
  padding-bottom: 1.5rem;
}

.page-header h1 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-color);
  margin-bottom: 0.75rem;
}

.page-header h1 i {
  color: var(--primary-color);
}

.page-description {
  color: var(--dark-gray);
  font-size: 1.1rem;
  max-width: 700px;
}

/* Face Recognition Section */
.face-recognition {
  padding: 1.5rem;
}

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
  background-color: var(--light-gray);
}

.upload-area.drag-over {
  background-color: rgba(52, 152, 219, 0.05);
  border-color: var(--primary-color);
}

.upload-area.has-image {
  padding: 1rem;
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

.btn-remove-image {
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

.person-form-grid {
  margin-bottom: 0;
}

.person-input, 
.person-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--medium-gray);
  border-radius: var(--border-radius-sm);
  background-color: white;
  font-size: 1rem;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
}

.person-input:focus, 
.person-select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.person-input:disabled, 
.person-select:disabled {
  background-color: #f1f1f1;
  cursor: not-allowed;
}

/* Style des personnes */
.person-image {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: var(--border-radius-sm);
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.person-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.relation-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  background-color: rgba(0, 0, 0, 0.6);
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

.person-actions {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
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

/* Réutilisation des styles du ControlMode.vue */
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

.btn-command:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-emergency {
  color: #e74c3c;
  border-color: #e74c3c;
}

.btn-emergency:hover {
  background-color: #e74c3c;
  color: white;
}

/* Media queries for responsive design */
@media screen and (max-width: 768px) {
  .commands-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 480px) {
  .commands-grid {
    grid-template-columns: 1fr;
  }
}
</style>