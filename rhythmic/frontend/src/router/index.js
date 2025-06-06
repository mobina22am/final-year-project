import { createRouter, createWebHistory } from 'vue-router';

import StartPage from '@/components/StartPage.vue';
import SignUp from '@/components/SignUp.vue';
import Login from '@/components/LogIn.vue';
import MainPage from '@/components/MainPage.vue';
import Profile from '@/components/UpdateProfile.vue';
import GetNotes from '@/components/GetNotes.vue';
import FindASong from '@/components/FindASong.vue';
import ChooseInstrument from '@/components/ChooseInstrument.vue'; 
import GeneratedNotes from '@/components/GeneratedNotes.vue';
import AccessFolder from '@/components/AccessFolder.vue';
import ForgotCredentials from '@/components/ForgotCredentials.vue';
import ResetPassword from '@/components/ResetPassword.vue';

const routes = [
  { path: '/', name: 'StartPage', component: StartPage },
  { path: '/signup', name: 'SignUp', component: SignUp},
  { path: '/login', name: 'LogIn', component: Login},
  { path: '/mainpage', name: 'MainPage', component: MainPage},
  { path: '/profile', name: 'Profile', component: Profile},
  { path: '/getnotes', name: 'GetNotes', component: GetNotes},
  { path: '/findasong', name: 'FindASong', component: FindASong},
  { path: '/chooseinstrument', name: 'ChooseInstrument', component: ChooseInstrument},
  { path: '/generatednotes', name: 'GeneratedNotes', component: GeneratedNotes},
  { path: '/accessfolder', name: 'AccessFolder', component: AccessFolder},
  { path: '/forgotcredentials', name: 'ForgotCredentials', component: ForgotCredentials},
  { path: '/resetpassword', name: 'ResetPassword', component: ResetPassword}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

