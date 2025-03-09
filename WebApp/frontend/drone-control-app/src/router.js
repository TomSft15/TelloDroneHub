import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './components/views/HomeView.vue';
import VoiceControlView from './components/views/VoiceControlView.vue';
import GestureControlView from './components/views/GestureControlView.vue';
import VisionControlView from './components/views/VisionControlView.vue';
import DashboardView from './components/views/DashboardView.vue';
import KeyboardConfigView from './components/views/KeyboardConfigView.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/voice-control', component: VoiceControlView },
  { path: '/gesture-control', component: GestureControlView },
  { path: '/vision-control', component: VisionControlView },
  { path: '/dashboard', component: DashboardView },
  { path: '/keyboard-config', component: KeyboardConfigView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
