import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './components/views/HomeView.vue';
import DashboardView from './components/views/DashboardView.vue';
import KeyboardConfigView from './components/views/KeyboardConfigView.vue';
import DroneConnection from './components/views/DroneConnection.vue';
import DroneCamera from './components/DroneCamera.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/dashboard', component: DashboardView },
  { path: '/keyboard-config', component: KeyboardConfigView },
  { path: '/connect', component: DroneConnection },
  { path: '/drone-camera', component: DroneCamera },
  
  // Rediriger les anciennes routes vers le dashboard
  { path: '/voice-control', redirect: '/dashboard' },
  { path: '/gesture-control', redirect: '/dashboard' },
  { path: '/vision-control', redirect: '/dashboard' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.path === '/dashboard') {
    // Vérifier si le drone est connecté
    const isDroneConnected = 'true';
    
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