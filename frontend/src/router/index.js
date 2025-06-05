import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Import views
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Recordings from '../views/Recordings.vue'
import RecordingDetail from '../views/RecordingDetail.vue'
import RecordingForm from '../components/RecordingForm.vue'
import Profile from '../views/Profile.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Главная - Faculty Portal'
    }
  },
  {
    path:'/admin',
    name: 'Admin',
    component: Profile,
    meta: {
      title: 'Админка - Faculty Portal',
      requiresAuth: true,
    }
  },

  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Вход - Faculty Portal',
      requiresGuest: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: 'Регистрация - Faculty Portal',
      requiresGuest: true
    }
  },
  {
    path: '/recordings',
    name: 'Recordings',
    component: Recordings,
    meta: {
      title: 'Записи - Faculty Portal'
    }
  },
  {
    path: '/recordings/new',
    name: 'CreateRecording',
    component: RecordingForm,
    meta: {
      title: 'Создать запись - Faculty Portal',
      requiresAuth: true,
      requiresModerator: true
    }
  },
  {
    path: '/recordings/:id',
    name: 'RecordingDetail',
    component: RecordingDetail,
    props: true,
    meta: {
      title: 'Запись - Faculty Portal'
    }
  },
  {
    path: '/recordings/:id/edit',
    name: 'EditRecording',
    component: RecordingForm,
    props: route => ({ recordingId: route.params.id }),
    meta: {
      title: 'Редактировать запись - Faculty Portal',
      requiresAuth: true,
      requiresModerator: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: {
      title: 'Профиль - Faculty Portal',
      requiresAuth: true
    }
  },
  // Error pages
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('../views/errors/404.vue'),
    meta: {
      title: 'Страница не найдена - Faculty Portal'
    }
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('../views/errors/403.vue'),
    meta: {
      title: 'Доступ запрещен - Faculty Portal'
    }
  },
  {
    path: '/500',
    name: 'ServerError',
    component: () => import('../views/errors/500.vue'),
    meta: {
      title: 'Ошибка сервера - Faculty Portal'
    }
  },
  // Catch all route - must be last
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  // Set page title
  document.title = to.meta.title || 'Faculty Portal'
  
  // Check if user is authenticated
  const isAuthenticated = store.getters.isAuthenticated
  const isAdmin = store.getters.isAdmin
  const isModerator = store.getters.isModerator
  
  // Handle guest-only routes
  if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
    return
  }
  
  // Handle auth-required routes
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({
      name: 'Login',
      query: { redirect: to.fullPath }
    })
    return
  }
  
  // Handle admin-only routes
  if (to.meta.requiresAdmin && !isAdmin) {
    next('/403')
    return
  }
  
  // Handle moderator-only routes
  if (to.meta.requiresModerator && !isModerator) {
    next('/403')
    return
  }
  
  // Add loading state
  store.commit('SET_LOADING', true)
  
  next()
})

router.afterEach((to, from) => {
  // Remove loading state
  store.commit('SET_LOADING', false)
  
  // Track page views (for analytics)
  if (typeof gtag !== 'undefined') {
    gtag('config', 'GA_MEASUREMENT_ID', {
      page_title: to.meta.title,
      page_location: window.location.href
    })
  }
})

// Handle navigation errors
router.onError((error) => {
  console.error('Router error:', error)
  
  if (error.name === 'ChunkLoadError') {
    // Handle chunk loading errors (usually from code splitting)
    window.location.reload()
  }
})

export default router
