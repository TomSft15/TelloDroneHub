import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import notificationPlugin from './plugins/notification';

// Import Font Awesome core
import { library } from '@fortawesome/fontawesome-svg-core';
// Import specific icons
import { 
  faExpand, 
  faCamera, 
  faTachometerAlt, 
  faSignal,
  faBatteryThreeQuarters,
  faTemperatureHigh,
  faClock,
  faTimes,
  faDownload,
  faTrash,
  faRocket,
  faPlug,
  faHandPaper,
  faMicrophone,
  faEye,
  faCheckCircle,
  faDesktop,
  faArrowRight,
  faVideoSlash,
  faSyncAlt,
  faCircle,
  faBatteryHalf,
  faChevronRight,
  faImage,
  faCheckDouble,
  faKeyboard,
  faMicrophoneSlash,
  faStop,
  faFistRaised,
  faThumbsUp,
  faThumbsDown,
  faArrowUp,
  faArrowDown,
  faArrowCircleUp,
  faArrowCircleDown,
  faArrowCircleLeft,
  faArrowCircleRight,
  faExclamationTriangle,
  faCog,
  faInfoCircle,
  faSpinner,
  faWifi,
  faLink,
  faUnlink,
  faQuestionCircle,
  faTools,
  faStethoscope,
  faSave,
  faUndo,
  faFileExport,
  faPencilAlt,
  faArrowLeft,
  faRedo,
  faPlaneArrival,
  faStopCircle,
  faPowerOff,
  faPlay,
  faUserPlus,
  faUsers,
  faCloudUploadAlt,
  faCrosshairs,
  faTrashAlt,
  faCheck,
  // Add other icons you need
} from '@fortawesome/free-solid-svg-icons';
// Import Font Awesome component
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

// Add icons to the library
library.add(
  faExpand, 
  faCamera, 
  faTachometerAlt, 
  faSignal,
  faBatteryThreeQuarters,
  faTemperatureHigh,
  faClock,
  faTimes,
  faDownload,
  faTrash,
  faRocket,
  faPlug,
  faHandPaper,
  faMicrophone,
  faEye,
  faCheckCircle,
  faDesktop,
  faArrowRight,
  faVideoSlash,
  faSyncAlt,
  faCircle,
  faBatteryHalf,
  faChevronRight,
  faImage,
  faCheckDouble,
  faKeyboard,
  faMicrophoneSlash,
  faStop,
  faFistRaised,
  faThumbsUp,
  faThumbsDown,
  faArrowUp,
  faArrowDown,
  faArrowRight,
  faArrowLeft,
  faArrowCircleUp,
  faArrowCircleDown,
  faArrowCircleLeft,
  faArrowCircleRight,
  faExclamationTriangle,
  faCog,
  faInfoCircle,
  faSpinner,
  faWifi,
  faLink,
  faUnlink,
  faQuestionCircle,
  faTools,
  faStethoscope,
  faSave,
  faUndo,
  faRedo,
  faPlaneArrival,
  faStopCircle,
  faPowerOff,
  faPlay,
  faFileExport,
  faPencilAlt,
  faUserPlus,
  faUsers,
  faCloudUploadAlt,
  faCrosshairs,
  faTrashAlt,
  faCheck,
  // Add other icons you added above
);

const app = createApp(App);

// Register Font Awesome component globally
app.component('font-awesome-icon', FontAwesomeIcon);

// Installation du plugin de notification
app.use(notificationPlugin);

// Rest of your code...
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