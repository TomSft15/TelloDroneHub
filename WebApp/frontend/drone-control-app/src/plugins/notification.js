// src/plugins/notification.js
import { createApp } from 'vue';
import NotificationSystem from '../components/NotificationSystem.vue';

export default {
  install: (app) => {
    // Créer une instance du composant de notification
    const notificationContainer = document.createElement('div');
    document.body.appendChild(notificationContainer);
    
    const notificationApp = createApp(NotificationSystem);
    const notificationInstance = notificationApp.mount(notificationContainer);
    
    // Ajouter les méthodes à l'instance Vue globale
    app.config.globalProperties.$notify = {
      show: (message, options = {}) => {
        const { type = 'info', title = null, duration = 5000 } = options;
        return notificationInstance.add(message, type, title, duration);
      },
      success: (message, title = null, duration = 5000) => {
        return notificationInstance.success(message, title, duration);
      },
      error: (message, title = null, duration = 8000) => {
        return notificationInstance.error(message, title, duration);
      },
      info: (message, title = null, duration = 5000) => {
        return notificationInstance.info(message, title, duration);
      },
      warning: (message, title = null, duration = 7000) => {
        return notificationInstance.warning(message, title, duration);
      },
      close: (id) => {
        notificationInstance.removeById(id);
      }
    };
    
    // Ajouter le plugin au context global sous forme de fonction utilitaire
    app.provide('notify', app.config.globalProperties.$notify);
  }
};