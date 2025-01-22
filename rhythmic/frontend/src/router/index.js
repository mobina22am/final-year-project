import { createRouter, createWebHistory } from 'vue-router';

import TestObject from '../components/test.vue'

const routes = [
  { path: '/', name: 'TestObject', component: TestObject }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

