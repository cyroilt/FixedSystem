import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Recordings from '../views/Recordings.vue'
import CreateRecording from '../views/CreateRecording.vue'
import RecordingDetail from '../views/RecordingDetail.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/recordings',
    name: 'Recordings',
    component: Recordings
  },
  {
    path: '/recordings/new',
    name: 'NewRecording',
    component: CreateRecording,
    meta: { requiresAuth: true, requiresModerator: true }
  },
  {
    path: '/recordings/:id/',
    name: 'RecordingDetail',
    component: RecordingDetail,
    meta: { requiresAuth: true, requiresModerator: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isAuthenticated) {
      next('/login')
    } else if (to.matched.some(record => record.meta.requiresAdmin)) {
      if (store.getters.isAdmin) {
        next()
      } else {
        next('/')
      }
    } else if (to.matched.some(record => record.meta.requiresModerator)) {
      if (store.getters.isModerator) {
        next()
      } else {
        next('/')
      }
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router