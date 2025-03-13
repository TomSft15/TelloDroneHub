import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './components/views/HomeView.vue';
import VoiceControlView from './components/views/VoiceControlView.vue';
import GestureControlView from './components/views/GestureControlView.vue';
import VisionControlView from './components/views/VisionControlView.vue';
import DashboardView from './components/views/DashboardView.vue';
import KeyboardConfigView from './components/views/KeyboardConfigView.vue';
import DroneConnection from './components/views/DroneConnection.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/voice-control', component: VoiceControlView },
  { path: '/gesture-control', component: GestureControlView },
  { path: '/vision-control', component: VisionControlView },
  { path: '/dashboard', component: DashboardView },
  { path: '/keyboard-config', component: KeyboardConfigView },
  { path: '/connect', component: DroneConnection },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.path === '/dashboard') {
    // Vérifier si le drone est connecté
    const isDroneConnected = localStorage.getItem('droneConnected') === 'true';
    
    // Si pas connecté et que l'utilisateur va au tableau de bord,
    // rediriger vers la page de connexion
    if (!isDroneConnected) {
      next('/connect');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
