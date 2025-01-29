import { createRouter, createWebHistory } from 'vue-router';

import StartPage from '@/components/StartPage.vue';
import SignUp from '@/components/SignUp.vue';

const routes = [
  { path: '/', name: 'StartPage', component: StartPage },
  { path: '/signup', name: 'SignUp', component: SignUp}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

