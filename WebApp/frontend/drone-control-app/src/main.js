import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import notificationPlugin from './plugins/notification';

const app = createApp(App);

// Installation du plugin de notification
app.use(notificationPlugin);

// Créer un bus d'événements simple pour Vue 3
app.config.globalProperties.$bus = createEventBus();

function createEventBus() {
  const emitter = createEmitter();
  
  return {
    $on: (event, callback) => {
      emitter.on(event, callback);
    },
    $off: (event, callback) => {
      emitter.off(event, callback);
    },
    $emit: (event, ...args) => {
      emitter.emit(event, ...args);
    }
  };
}

function createEmitter() {
  const events = new Map();
  
  return {
    on(event, callback) {
      if (!events.has(event)) {
        events.set(event, []);
      }
      events.get(event).push(callback);
    },
    off(event, callback) {
      if (!events.has(event)) return;
      const callbacks = events.get(event);
      const index = callbacks.indexOf(callback);
      if (index !== -1) callbacks.splice(index, 1);
    },
    emit(event, ...args) {
      if (!events.has(event)) return;
      events.get(event).forEach(callback => callback(...args));
    }
  };
}

app.use(router);
app.mount('#app');