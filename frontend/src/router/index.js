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
import WallPrint from '../views/WallPrint.vue'
import Command from '../views/Command.vue'
import MemoryPages from '../views/MemoryPages.vue'
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
    path: '/admin',
    name: 'Admin',
    beforeEnter() {
      // Redirect to backend admin panel
      window.location.href = 'http://localhost:5000/admin'
    },
    meta: {
      title: 'Админка - Faculty Portal',
      requiresAuth: true,
      requiresAdmin: true
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
    path: '/memory-pages',
    name: 'MemoryPages',
    component: MemoryPages
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
    props: (route) => ({ recordingId: route.params.id }),
    meta: {
      title: 'Редактировать запись - Faculty Portal',
      requiresAuth: true,
      requiresModerator: true
    }
  },
  {
    path: '/wall-print',
    name: 'WallPrint',
    component: WallPrint,
    meta: {
      title: 'Стенная печать - Faculty Portal'
    }
  },
  {
    path: '/command',
    name: 'Command',
    component: Command,
    meta: {
      title: 'Командование - Faculty Portal'
    }
  },
  {
    path: '/profile/:userId?',
    name: 'Profile',
    component: Profile,
    props: (route) => ({ userId: route.params.userId }),
    meta: {
      title: 'Профиль - Faculty Portal'
    }
  },
  {
    path: '/users/:userId',
    name: 'UserProfile',
    component: Profile,
    props: (route) => ({ userId: route.params.userId }),
    meta: {
      title: 'Профиль пользователя - Faculty Portal'
    }
  },
  // Add this route to your existing routes array
  {
    path: '/faculty-history',
    name: 'FacultyHistory',
    component: () => import('@/views/FacultyHistory.vue'),
    meta: {
      title: 'История Факультета'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  // Initialize store if not already done
  if (!store.state.isAuthenticated && store.state.token) {
    await store.dispatch('initializeApp')
  }

  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title
  }

  // Check authentication requirements
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // Check guest-only routes
  if (to.meta.requiresGuest && store.getters.isAuthenticated) {
    next({ name: 'Home' })
    return
  }

  // Check admin requirements
  if (to.meta.requiresAdmin && !store.getters.isAdmin) {
    next({ name: 'Home' })
    return
  }

  // Check moderator requirements
  if (to.meta.requiresModerator && !store.getters.isModerator) {
    next({ name: 'Home' })
    return
  }

  next()
})

export default router
