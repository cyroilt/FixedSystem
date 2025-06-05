<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="container">
      <div class="navbar-content">
        <router-link to="/" class="navbar-brand">
          <i class="fas fa-university"></i>
          <span>Faculty Portal</span>
        </router-link>
        
        <div class="navbar-menu" :class="{ 'active': mobileMenuOpen }">
          <router-link to="/" class="navbar-link" @click="closeMobileMenu">
            <i class="fas fa-home"></i>
            Главная
          </router-link>
          <router-link to="/recordings" class="navbar-link" @click="closeMobileMenu">
            <i class="fas fa-video"></i>
            Записи
          </router-link>
          
          <div v-if="isAuthenticated" class="navbar-dropdown">
            <button class="navbar-link dropdown-toggle user-menu-toggle">
              <AvatarPlaceholder
                :src="userAvatar"
                :name="user?.username || 'User'"
                :alt="user?.username || 'User Avatar'"
                size="small"
                variant="circle"
                :show-status="true"
                status="online"
                class="user-avatar"
              />
              <span class="username">{{ user?.username || 'User' }}</span>
              <i class="fas fa-chevron-down"></i>
            </button>
            <div class="dropdown-menu">
              <div class="dropdown-header">
                <AvatarPlaceholder
                  :src="userAvatar"
                  :name="user?.username || 'User'"
                  :alt="user?.username || 'User Avatar'"
                  size="medium"
                  variant="circle"
                  class="dropdown-avatar"
                />
                <div class="user-info">
                  <div class="user-name">{{ user?.username || 'User' }}</div>
                  <div class="user-email">{{ user?.email || '' }}</div>
                  <div class="user-role">{{ getRoleDisplayName(user?.role) }}</div>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <router-link to="/profile" class="dropdown-item">
                <i class="fas fa-user"></i>
                Профиль
              </router-link>
              <router-link v-if="isModerator" to="/recordings/new" class="dropdown-item">
                <i class="fas fa-plus"></i>
                Новая запись
              </router-link>
              <router-link v-if="isAdmin" to="/admin" class="dropdown-item">
                <i class="fas fa-cog"></i>
                Админ панель
              </router-link>
              <div class="dropdown-divider"></div>
              <button @click="logout" class="dropdown-item logout-item">
                <i class="fas fa-sign-out-alt"></i>
                Выйти
              </button>
            </div>
          </div>
          
          <div v-else class="navbar-auth">
            <router-link to="/login" class="navbar-link" @click="closeMobileMenu">
              <i class="fas fa-sign-in-alt"></i>
              Войти
            </router-link>
            <router-link to="/register" class="btn btn-primary" @click="closeMobileMenu">
              Регистрация
            </router-link>
          </div>
        </div>
        
        <button class="mobile-menu-toggle" @click="toggleMobileMenu">
          <i class="fas fa-bars"></i>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'
import AvatarPlaceholder from './AvatarPlaceholder.vue'

export default {
  name: 'Navbar',
  components: {
    AvatarPlaceholder
  },
  data() {
    return {
      isScrolled: false,
      mobileMenuOpen: false
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'isModerator']),
    user() {
      return this.$store.state.user
    },
    userAvatar() {
      // Safely access avatar property with fallback
      return this.user?.avatar || this.user?.avatar_url || null
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 50
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    logout() {
      this.$store.dispatch('logout')
      this.$router.push('/')
      this.closeMobileMenu()
    },
    getRoleDisplayName(role) {
      const roleNames = {
        'admin': 'Администратор',
        'moderator': 'Модератор',
        'user': 'Пользователь'
      }
      return roleNames[role] || 'Пользователь'
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(30, 60, 114, 0.95);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.navbar.scrolled {
  background: rgba(30, 60, 114, 0.98);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.navbar-brand {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #ffd700;
  font-size: 1.5rem;
  font-weight: bold;
  transition: all 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.05);
}

.navbar-brand i {
  margin-right: 0.5rem;
  font-size: 1.8rem;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.navbar-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #ffffff;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.navbar-link:hover {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

.navbar-link i {
  margin-right: 0.5rem;
}

.navbar-dropdown {
  position: relative;
}

.user-menu-toggle {
  gap: 0.75rem;
  padding: 0.5rem 1rem;
}

.user-avatar {
  margin-right: 0.5rem;
}

.username {
    max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-toggle:hover + .dropdown-menu,
.dropdown-menu:hover {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: rgba(30, 60, 114, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 0;
  min-width: 280px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.dropdown-avatar {
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  color: #ffffff;
  font-size: 1rem;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-email {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-role {
  font-size: 0.75rem;
  color: #ffd700;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dropdown-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  color: #ffffff;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  text-align: left;
}

.dropdown-item:hover {
  background: rgba(255, 215, 0, 0.1);
  color: #ffd700;
}

.dropdown-item i {
  margin-right: 0.75rem;
  width: 16px;
  text-align: center;
}

.logout-item {
  color: #ff6b6b;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-item:hover {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.navbar-auth {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mobile-menu-toggle {
  display: none;
  background: none;
  border: none;
  color: #ffffff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.mobile-menu-toggle:hover {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: block;
  }
  
  .navbar-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: rgba(30, 60, 114, 0.98);
    backdrop-filter: blur(10px);
    flex-direction: column;
    padding: 1rem;
    gap: 0;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-20px);
    transition: all 0.3s ease;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .navbar-menu.active {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
  
  .navbar-link {
    width: 100%;
    justify-content: flex-start;
    margin-bottom: 0.5rem;
    padding: 0.75rem 1rem;
  }
  
  .navbar-auth {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
  
  .navbar-dropdown {
    width: 100%;
  }
  
  .user-menu-toggle {
    width: 100%;
    justify-content: flex-start;
  }
  
  .dropdown-menu {
    position: static;
    opacity: 1;
    visibility: visible;
    transform: none;
    background: rgba(255, 255, 255, 0.1);
    margin-top: 0.5rem;
    min-width: auto;
    width: 100%;
  }
  
  .dropdown-header {
    padding: 1rem;
  }
  
  .dropdown-item {
    padding: 0.75rem 1rem;
  }
}

@media (max-width: 480px) {
  .navbar-brand span {
    display: none;
  }
  
  .username {
    max-width: 80px;
  }
  
  .dropdown-header {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .user-info {
    text-align: center;
  }
}
</style>

