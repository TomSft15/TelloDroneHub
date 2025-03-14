<template>
  <div class="notification-system">
    <transition-group name="notification">
      <div 
        v-for="(notification, index) in notifications" 
        :key="notification.id" 
        class="notification-toast"
        :class="`notification-${notification.type}`"
      >
        <div class="notification-icon">
          <i :class="getIcon(notification.type)"></i>
        </div>
        <div class="notification-content">
          <div v-if="notification.title" class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
        </div>
        <button @click="removeNotification(index)" class="notification-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  name: 'NotificationSystem',
  data() {
    return {
      notifications: [],
      counter: 0
    };
  },
  methods: {
    /**
     * Ajoute une notification
     * @param {string} message - Le message à afficher
     * @param {string} type - Le type de notification (success, error, info, warning)
     * @param {string} title - Titre facultatif
     * @param {number} duration - Durée d'affichage en millisecondes
     */
    add(message, type = 'info', title = null, duration = 5000) {
      const id = this.counter++;
      
      // Ajouter la notification
      this.notifications.push({
        id,
        message,
        type,
        title,
        timer: duration > 0 ? setTimeout(() => {
          this.removeById(id);
        }, duration) : null
      });
      
      // Limiter le nombre de notifications (maximum 5)
      if (this.notifications.length > 5) {
        const oldest = this.notifications.shift();
        if (oldest.timer) clearTimeout(oldest.timer);
      }
      
      return id;
    },
    
    /**
     * Affiche une notification de succès
     */
    success(message, title = null, duration = 5000) {
      return this.add(message, 'success', title, duration);
    },
    
    /**
     * Affiche une notification d'erreur
     */
    error(message, title = null, duration = 8000) {
      return this.add(message, 'error', title, duration);
    },
    
    /**
     * Affiche une notification d'information
     */
    info(message, title = null, duration = 5000) {
      return this.add(message, 'info', title, duration);
    },
    
    /**
     * Affiche une notification d'avertissement
     */
    warning(message, title = null, duration = 7000) {
      return this.add(message, 'warning', title, duration);
    },
    
    /**
     * Supprime une notification par son index
     */
    removeNotification(index) {
      if (index >= 0 && index < this.notifications.length) {
        const notification = this.notifications[index];
        if (notification.timer) clearTimeout(notification.timer);
        this.notifications.splice(index, 1);
      }
    },
    
    /**
     * Supprime une notification par son ID
     */
    removeById(id) {
      const index = this.notifications.findIndex(n => n.id === id);
      if (index !== -1) {
        this.removeNotification(index);
      }
    },
    
    /**
     * Retourne l'icône à utiliser selon le type de notification
     */
    getIcon(type) {
      const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle',
        warning: 'fas fa-exclamation-triangle'
      };
      return icons[type] || icons.info;
    }
  }
};
</script>

<style scoped>
.notification-system {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 350px;
}

.notification-toast {
  display: flex;
  align-items: flex-start;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background-color: white;
  margin-bottom: 8px;
  animation: slide-in 0.3s ease-out forwards;
}

.notification-success {
  border-left: 5px solid #2ecc71;
}

.notification-error {
  border-left: 5px solid #e74c3c;
}

.notification-info {
  border-left: 5px solid #3498db;
}

.notification-warning {
  border-left: 5px solid #f39c12;
}

.notification-icon {
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.notification-success .notification-icon {
  color: #2ecc71;
}

.notification-error .notification-icon {
  color: #e74c3c;
}

.notification-info .notification-icon {
  color: #3498db;
}

.notification-warning .notification-icon {
  color: #f39c12;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 16px;
  color: #333;
}

.notification-message {
  color: #555;
  font-size: 14px;
  line-height: 1.4;
}

.notification-close {
  background: transparent;
  border: none;
  color: #95a5a6;
  cursor: pointer;
  font-size: 16px;
  margin-left: 8px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.notification-close:hover {
  color: #7f8c8d;
}

/* Animations */
.notification-enter-active, .notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

@keyframes slide-in {
  0% {
    opacity: 0;
    transform: translateX(30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>