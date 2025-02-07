import { createRouter, createWebHistory } from 'vue-router';

import StartPage from '@/components/StartPage.vue';
import SignUp from '@/components/SignUp.vue';
import Login from '@/components/LogIn.vue';
import MainPage from '@/components/MainPage.vue';
import Profile from '@/components/UpdateProfile.vue';

const routes = [
  { path: '/', name: 'StartPage', component: StartPage },
  { path: '/signup', name: 'SignUp', component: SignUp},
  { path: '/login', name: 'LogIn', component: Login},
  { path: '/mainpage', name: 'MainPage', component: MainPage},
  { path: '/profile', name: 'Profile', component: Profile},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

