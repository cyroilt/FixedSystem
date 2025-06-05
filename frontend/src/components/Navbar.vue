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
            <button class="navbar-link dropdown-toggle">
              <i class="fas fa-user"></i>
              {{ user.username }}
              <i class="fas fa-chevron-down"></i>
            </button>
            <div class="dropdown-menu">
              <router-link v-if="isModerator" to="/recordings/new" class="dropdown-item">
                <i class="fas fa-plus"></i>
                Новая запись
              </router-link>
              <router-link v-if="isAdmin" to="/admin" class="dropdown-item">
                <i class="fas fa-cog"></i>
                Админ панель
              </router-link>
              <button @click="logout" class="dropdown-item">
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

export default {
  name: 'Navbar',
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
  border-radius: 8px;
  padding: 0.5rem 0;
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.dropdown-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: #ffffff;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.dropdown-item:hover {
  background: rgba(255, 215, 0, 0.1);
  color: #ffd700;
}

.dropdown-item i {
  margin-right: 0.5rem;
  width: 16px;
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
  }
  
  .navbar-auth {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
  
  .dropdown-menu {
    position: static;
    opacity: 1;
    visibility: visible;
    transform: none;
    background: rgba(255, 255, 255, 0.1);
    margin-top: 0.5rem;
  }
}
</style>
