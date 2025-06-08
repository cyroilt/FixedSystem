<template>
  <nav class="navbar" :class="{ scrolled: isScrolled }">
    <div class="container">
      <div class="navbar-content">
        <router-link to="/" class="navbar-brand animate-glow">
          <div class="brand-icon-wrapper">
            <i class="fas fa-university animate-pulse"></i>
            <div class="brand-particles">
              <div class="particle particle-1"></div>
              <div class="particle particle-2"></div>
              <div class="particle particle-3"></div>
            </div>
          </div>
          <span class="brand-text">Faculty Portal</span>
        </router-link>

        <div class="navbar-menu" :class="{ active: mobileMenuOpen }">
          <router-link
            to="/"
            class="navbar-link hover-lift"
            @click="closeMobileMenu"
          >
            <div class="link-content">
              <i class="fas fa-home"></i>
              <span>Главная</span>
              <div class="link-glow"></div>
            </div>
          </router-link>
          <router-link
            to="/recordings"
            class="navbar-link hover-lift"
            @click="closeMobileMenu"
          >
            <div class="link-content">
              <i class="fas fa-video"></i>
              <span>Записи</span>
              <div class="link-glow"></div>
            </div>
          </router-link>
          <router-link
            to="/wall-print"
            class="navbar-link hover-lift"
            @click="closeMobileMenu"
          >
            <div class="link-content">
              <i class="fas fa-newspaper"></i>
              <span>Стенная печать</span>
              <div class="link-glow"></div>
            </div>
          </router-link>
          <router-link
            to="/command"
            class="navbar-link hover-lift"
            @click="closeMobileMenu"
          >
            <div class="link-content">
              <i class="fas fa-users-cog"></i>
              <span>Командование</span>
              <div class="link-glow"></div>
            </div>
          </router-link>

          <div v-if="isAuthenticated" class="navbar-dropdown">
            <button
              class="navbar-link dropdown-toggle user-menu-toggle hover-lift"
              @mouseenter="showDropdown"
              @mouseleave="hideDropdown"
            >
              <div class="user-menu-content">
                <div class="avatar-wrapper">
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
                  <div class="avatar-glow"></div>
                </div>
                <span class="username">{{ user?.username || 'User' }}</span>
                <i class="fas fa-chevron-down dropdown-arrow"></i>
                <div class="user-menu-glow"></div>
              </div>
            </button>
            <div
              class="dropdown-menu"
              :class="{ show: dropdownVisible }"
              @mouseenter="showDropdown"
              @mouseleave="hideDropdown"
            >
              <div class="dropdown-header">
                <div class="dropdown-bg-effect"></div>
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
                  <div class="user-role">
                    {{ getRoleDisplayName(user?.role) }}
                  </div>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <router-link to="/profile" class="dropdown-item hover-glow">
                <i class="fas fa-user"></i>
                <span>Профиль</span>
                <div class="item-glow"></div>
              </router-link>
              <router-link
                v-if="isModerator"
                to="/recordings/new"
                class="dropdown-item hover-glow"
              >
                <i class="fas fa-plus"></i>
                <span>Новая запись</span>
                <div class="item-glow"></div>
              </router-link>
              <router-link
                v-if="isAdmin"
                to="/admin"
                class="dropdown-item hover-glow"
              >
                <i class="fas fa-cog"></i>
                <span>Админ панель</span>
                <div class="item-glow"></div>
              </router-link>
              <div class="dropdown-divider"></div>
              <button
                @click="logout"
                class="dropdown-item logout-item hover-glow"
              >
                <i class="fas fa-sign-out-alt"></i>
                <span>Выйти</span>
                <div class="item-glow logout-glow"></div>
              </button>
            </div>
          </div>

          <div v-else class="navbar-auth">
            <router-link
              to="/login"
              class="navbar-link auth-link hover-lift"
              @click="closeMobileMenu"
            >
              <div class="link-content">
                <i class="fas fa-sign-in-alt"></i>
                <span>Войти</span>
                <div class="link-glow"></div>
              </div>
            </router-link>
            <router-link
              to="/register"
              class="btn btn-primary auth-btn hover-scale"
              @click="closeMobileMenu"
            >
              <span>Регистрация</span>
              <div class="btn-particles">
                <div class="btn-particle"></div>
                <div class="btn-particle"></div>
                <div class="btn-particle"></div>
              </div>
            </router-link>
          </div>
        </div>

        <button
          class="mobile-menu-toggle hover-scale"
          @click="toggleMobileMenu"
        >
          <div class="hamburger-wrapper">
            <i class="fas fa-bars"></i>
            <div class="hamburger-glow"></div>
          </div>
        </button>
      </div>
    </div>

    <!-- Navbar Background Effects -->
    <div class="navbar-particles">
      <div class="nav-particle nav-particle-1"></div>
      <div class="nav-particle nav-particle-2"></div>
      <div class="nav-particle nav-particle-3"></div>
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
      mobileMenuOpen: false,
      dropdownVisible: false,
      dropdownTimer: null
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'isModerator']),
    user() {
      return this.$store.state.user
    },
    userAvatar() {
      return this.user?.avatar || this.user?.avatar_url || null
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
    if (this.dropdownTimer) {
      clearTimeout(this.dropdownTimer)
    }
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
    showDropdown() {
      if (this.dropdownTimer) {
        clearTimeout(this.dropdownTimer)
      }
      this.dropdownVisible = true
    },
    hideDropdown() {
      this.dropdownTimer = setTimeout(() => {
        this.dropdownVisible = false
      }, 150) // Small delay to prevent flickering
    },
    logout() {
      this.$store.dispatch('logout')
      this.$router.push('/')
      this.closeMobileMenu()
      this.dropdownVisible = false
    },
    getRoleDisplayName(role) {
      const roleNames = {
        admin: 'Администратор',
        moderator: 'Модератор',
        user: 'Пользователь'
      }
      return roleNames[role] || 'Пользователь'
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed !important;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: linear-gradient(
    135deg,
    rgba(30, 60, 114, 0.95) 0%,
    rgba(16, 42, 79, 0.98) 50%,
    rgba(10, 25, 47, 0.99) 100%
  );
  backdrop-filter: blur(20px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: visible; /* Changed from hidden to visible */
  height: 80px; /* Fixed height to prevent changes */
}

.navbar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 215, 0, 0.05),
    transparent
  );
  animation: shimmerEffect 3s ease-in-out infinite;
}

.navbar.scrolled {
  background: linear-gradient(
    135deg,
    rgba(30, 60, 114, 0.98) 0%,
    rgba(16, 42, 79, 1) 50%,
    rgba(10, 25, 47, 1) 100%
  );
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5);
  border-bottom-color: rgba(255, 215, 0, 0.3);
}

.navbar-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.nav-particle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.4), transparent);
  animation: floatParticle 8s ease-in-out infinite;
}

.nav-particle-1 {
  width: 4px;
  height: 4px;
  top: 20%;
  left: 15%;
  animation-delay: 0s;
}

.nav-particle-2 {
  width: 6px;
  height: 6px;
  top: 60%;
  right: 25%;
  animation-delay: 2s;
}

.nav-particle-3 {
  width: 3px;
  height: 3px;
  bottom: 30%;
  left: 70%;
  animation-delay: 4s;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  position: relative;
  z-index: 2;
  height: 100%; /* Ensure content takes full height */
}

.navbar-brand {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #ffd700;
  font-size: 1.5rem;
  font-weight: 700;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.brand-icon-wrapper {
  position: relative;
  margin-right: 0.75rem;
}

.brand-icon-wrapper i {
  font-size: 2rem;
  position: relative;
  z-index: 2;
}

.brand-particles {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  pointer-events: none;
}

.brand-particles .particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(255, 215, 0, 0.6);
  border-radius: 50%;
  animation: brandParticle 3s ease-in-out infinite;
}

.brand-particles .particle-1 {
  top: 0;
  left: 50%;
  animation-delay: 0s;
}

.brand-particles .particle-2 {
  top: 50%;
  right: 0;
  animation-delay: 1s;
}

.brand-particles .particle-3 {
  bottom: 0;
  left: 0;
  animation-delay: 2s;
}

.brand-text {
  background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s ease infinite;
}

.navbar-brand:hover {
  transform: scale(1.05);
  text-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar-link {
  position: relative;
  text-decoration: none;
  color: #ffffff;
  font-weight: 500;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 12px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  overflow: hidden;
}

.link-content {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.25rem;
  position: relative;
  z-index: 2;
  gap: 0.5rem;
}

.link-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 215, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.navbar-link:hover .link-glow {
  opacity: 1;
}

.navbar-link:hover {
  color: #ffd700;
  text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
  transform: translateY(-2px);
}

.navbar-link i {
  font-size: 1rem;
  transition: all 0.3s ease;
}

.navbar-link:hover i {
  transform: scale(1.1);
}

.navbar-dropdown {
  position: relative;
  height: 100%; /* Ensure dropdown container has full height */
}

.user-menu-toggle {
  padding: 0 !important;
}

.user-menu-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  position: relative;
  z-index: 2;
}

.avatar-wrapper {
  position: relative;
}

.user-avatar {
  position: relative;
  z-index: 2;
}

.avatar-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 35px;
  height: 35px;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.3), transparent);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.user-menu-toggle:hover .avatar-glow {
  opacity: 1;
  animation: avatarPulse 2s ease-in-out infinite;
}

.username {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 600;
}

.dropdown-arrow {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.user-menu-toggle:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.user-menu-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 215, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.user-menu-toggle:hover .user-menu-glow {
  opacity: 1;
}

.dropdown-menu {
  position: absolute !important;
  top: calc(100% + 10px) !important; /* Position below the navbar */
  right: 0;
  background: linear-gradient(
    135deg,
    rgba(30, 60, 114, 0.98) 0%,
    rgba(16, 42, 79, 0.99) 100%
  );
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 0;
  min-width: 320px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-15px) scale(0.95);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  z-index: 9999 !important; /* Very high z-index to ensure it's above everything */
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0) scale(1);
}

.dropdown-menu::before {
  content: '';
  position: absolute;
  top: -8px;
  right: 20px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid rgba(30, 60, 114, 0.98);
}

.dropdown-bg-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    rgba(255, 215, 0, 0.05),
    transparent,
    rgba(255, 215, 0, 0.03)
  );
  animation: dropdownShimmer 4s ease-in-out infinite;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.dropdown-avatar {
  flex-shrink: 0;
  position: relative;
  z-index: 2;
}

.user-info {
  flex: 1;
  min-width: 0;
  position: relative;
  z-index: 2;
}

.user-name {
  font-weight: 700;
  color: #ffffff;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}

.user-email {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-role {
  font-size: 0.8rem;
  color: #ffd700;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: rgba(255, 215, 0, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  display: inline-block;
}

.dropdown-divider {
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 215, 0, 0.3),
    transparent
  );
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 1rem 2rem;
  text-decoration: none;
  color: #ffffff;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 1rem;
  text-align: left;
  position: relative;
  overflow: hidden;
  font-weight: 500;
}

.dropdown-item span {
  position: relative;
  z-index: 2;
}

.item-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 215, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.dropdown-item:hover .item-glow {
  opacity: 1;
}

.dropdown-item:hover {
  color: #ffd700;
  text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
  transform: translateX(5px);
}

.dropdown-item i {
  margin-right: 1rem;
  width: 20px;
  text-align: center;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.dropdown-item:hover i {
  transform: scale(1.2);
  color: #ffd700;
}

.logout-item {
  color: #ff6b6b;
  border-top: 1px solid rgba(255, 107, 107, 0.2);
  margin-top: 0.5rem;
}

.logout-glow {
  background: rgba(255, 107, 107, 0.1) !important;
}

.logout-item:hover {
  color: #ff6b6b;
  text-shadow: 0 0 15px rgba(255, 107, 107, 0.4);
}

.logout-item:hover i {
  color: #ff6b6b;
}

.navbar-auth {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-link {
  color: rgba(255, 255, 255, 0.9);
}

.auth-btn {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #1a1a2e;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
}

.btn-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.btn-particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(26, 26, 46, 0.4);
  border-radius: 50%;
  animation: btnParticleFloat 2s ease-in-out infinite;
}

.btn-particle:nth-child(1) {
  top: 20%;
  left: 30%;
  animation-delay: 0s;
}

.btn-particle:nth-child(2) {
  top: 60%;
  right: 25%;
  animation-delay: 0.7s;
}

.btn-particle:nth-child(3) {
  bottom: 30%;
  left: 60%;
  animation-delay: 1.4s;
}

.auth-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.5);
}

.mobile-menu-toggle {
  display: none;
  background: none;
  border: none;
  color: #ffffff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.75rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.hamburger-wrapper {
  position: relative;
  z-index: 2;
}

.hamburger-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 215, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.mobile-menu-toggle:hover .hamburger-glow {
  opacity: 1;
}

.mobile-menu-toggle:hover {
  color: #ffd700;
  transform: scale(1.1);
}

/* Animations */
@keyframes shimmerEffect {
  0%,
  100% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
}

@keyframes floatParticle {
  0%,
  100% {
    transform: translateY(0px);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

@keyframes brandParticle {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.5);
    opacity: 1;
  }
}

@keyframes gradientShift {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes avatarPulse {
  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
  }
}

@keyframes dropdownShimmer {
  0%,
  100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

@keyframes btnParticleFloat {
  0%,
  100% {
    transform: translateY(0px) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-5px) scale(1.2);
    opacity: 1;
  }
}

/* Hover Effects */
.hover-lift:hover {
  transform: translateY(-2px);
}

.hover-scale:hover {
  transform: scale(1.05);
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .navbar-menu {
    gap: 0.75rem;
  }

  .link-content {
    padding: 0.6rem 1rem;
  }

  .user-menu-content {
    padding: 0.6rem 1rem;
  }
}

@media (max-width: 900px) {
  .navbar-menu {
    gap: 0.5rem;
  }

  .navbar-link {
    font-size: 0.9rem;
  }

  .link-content {
    padding: 0.5rem 0.8rem;
  }

  .username {
    max-width: 100px;
  }
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
    background: linear-gradient(
      135deg,
      rgba(30, 60, 114, 0.98) 0%,
      rgba(16, 42, 79, 0.99) 100%
    );
    backdrop-filter: blur(20px);
    flex-direction: column;
    padding: 2rem;
    gap: 0;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-20px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-top: 1px solid rgba(255, 215, 0, 0.2);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    z-index: 999;
  }

  .navbar-menu.active {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }

  .navbar-link {
    width: 100%;
    margin-bottom: 1rem;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .link-content {
    justify-content: flex-start;
    padding: 1rem 1.5rem;
    width: 100%;
  }

  .navbar-auth {
    flex-direction: column;
    width: 100%;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .auth-btn {
    width: 100%;
    text-align: center;
    justify-content: center;
    padding: 1rem 1.5rem;
  }

  .navbar-dropdown {
    width: 100%;
    position: static;
  }

  .user-menu-toggle {
    width: 100%;
    margin-bottom: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
  }

  .user-menu-content {
    justify-content: flex-start;
    padding: 1rem 1.5rem;
    width: 100%;
  }

  .dropdown-menu {
    position: static !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    background: rgba(255, 255, 255, 0.08);
    margin-top: 0;
    min-width: auto;
    width: 100%;
    border-radius: 12px;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2);
  }

  .dropdown-menu::before {
    display: none;
  }

  .dropdown-header {
    padding: 1.5rem;
  }

  .dropdown-item {
    padding: 1rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .navbar {
    height: 70px;
  }

  .navbar-brand {
    font-size: 1.3rem;
  }

  .brand-text {
    display: none;
  }

  .brand-icon-wrapper i {
    font-size: 1.8rem;
  }

  .username {
    max-width: 80px;
  }

  .dropdown-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.25rem;
  }

  .user-info {
    text-align: center;
  }

  .navbar-menu {
    padding: 1.5rem;
  }

  .link-content {
    padding: 0.875rem 1.25rem;
  }

  .dropdown-item {
    padding: 0.875rem 1.25rem;
  }

  .mobile-menu-toggle {
    padding: 0.5rem;
  }
}

@media (max-width: 360px) {
  .navbar {
    height: 65px;
  }

  .navbar-brand {
    font-size: 1.2rem;
  }

  .brand-icon-wrapper i {
    font-size: 1.6rem;
  }

  .navbar-menu {
    padding: 1.25rem;
  }

  .dropdown-menu {
    min-width: 280px;
  }

  .user-name {
    font-size: 1rem;
  }

  .user-email {
    font-size: 0.85rem;
  }

  .user-role {
    font-size: 0.75rem;
    padding: 0.2rem 0.6rem;
  }
}

/* Enhanced focus states for accessibility */
.navbar-link:focus-visible,
.dropdown-item:focus-visible,
.mobile-menu-toggle:focus-visible,
.auth-btn:focus-visible {
  outline: 3px solid rgba(255, 215, 0, 0.8);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .navbar {
    background: #000000;
    border-bottom-color: #ffffff;
  }

  .navbar-link,
  .dropdown-item {
    color: #ffffff;
    border: 1px solid #ffffff;
  }

  .navbar-link:hover,
  .dropdown-item:hover {
    color: #ffff00;
    background: #333333;
  }

  .navbar-brand {
    color: #ffff00;
  }

  .dropdown-menu {
    background: #1a1a1a;
    border-color: #ffffff;
  }

  .auth-btn {
    background: #ffff00;
    color: #000000;
    border: 2px solid #ffffff;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .navbar,
  .navbar-link,
  .dropdown-menu,
  .auth-btn,
  .mobile-menu-toggle {
    transition: none;
  }

  .shimmerEffect,
  .floatParticle,
  .brandParticle,
  .gradientShift,
  .avatarPulse,
  .dropdownShimmer,
  .btnParticleFloat {
    animation: none;
  }

  .navbar-particles,
  .brand-particles,
  .btn-particles {
    display: none;
  }

  .hover-lift:hover,
  .hover-scale:hover {
    transform: none;
  }
}

/* Print styles */
@media print {
  .navbar {
    position: static !important;
    background: white !important;
    color: black !important;
    box-shadow: none !important;
    border-bottom: 2px solid black !important;
  }

  .navbar-particles,
  .brand-particles,
  .btn-particles,
  .dropdown-menu,
  .mobile-menu-toggle {
    display: none !important;
  }

  .navbar-link,
  .navbar-brand {
    color: black !important;
  }

  .auth-btn {
    background: white !important;
    color: black !important;
    border: 1px solid black !important;
  }
}

/* Performance optimizations */
.navbar * {
  will-change: auto;
}

.navbar .hover-lift:hover,
.navbar .hover-scale:hover,
.navbar .dropdown-menu {
  will-change: transform;
}

.navbar .animate-pulse,
.navbar .animate-glow {
  will-change: opacity, text-shadow;
}

/* Custom scrollbar for dropdown if needed */
.dropdown-menu::-webkit-scrollbar {
  width: 6px;
}

.dropdown-menu::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.dropdown-menu::-webkit-scrollbar-thumb {
  background: rgba(255, 215, 0, 0.5);
  border-radius: 3px;
}

.dropdown-menu::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 215, 0, 0.7);
}

/* Ensure dropdown doesn't affect navbar height */
.navbar-dropdown .dropdown-menu {
  position: absolute !important;
  top: calc(100% + 10px) !important;
  transform-origin: top center;
}

/* Additional mobile optimizations */
@media (max-width: 768px) and (orientation: landscape) {
  .navbar {
    height: 60px;
  }

  .navbar-content {
    padding: 0.5rem 0;
  }

  .navbar-brand {
    font-size: 1.2rem;
  }

  .brand-icon-wrapper i {
    font-size: 1.5rem;
  }
}

/* Ultra-wide screen optimizations */
@media (min-width: 1920px) {
  .navbar-content {
    max-width: 1600px;
    margin: 0 auto;
  }

  .navbar-menu {
    gap: 2rem;
  }

  .link-content {
    padding: 0.875rem 1.5rem;
  }

  .dropdown-menu {
    min-width: 360px;
  }
}

/* Touch device optimizations */
@media (hover: none) and (pointer: coarse) {
  .navbar-link,
  .dropdown-item {
    min-height: 44px;
    display: flex;
    align-items: center;
  }

  .hover-lift:hover,
  .hover-scale:hover,
  .hover-glow:hover {
    transform: none;
    box-shadow: none;
  }

  .dropdown-menu {
    position: static !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
  }
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
  .navbar {
    background: linear-gradient(
      135deg,
      rgba(15, 30, 57, 0.98) 0%,
      rgba(8, 21, 39, 1) 50%,
      rgba(5, 12, 23, 1) 100%
    );
  }

  .dropdown-menu {
    background: linear-gradient(
      135deg,
      rgba(15, 30, 57, 0.99) 0%,
      rgba(8, 21, 39, 1) 100%
    );
  }
}

/* Loading states */
.navbar.loading {
  pointer-events: none;
}

.navbar.loading * {
  opacity: 0.7;
}

/* Error states */
.navbar.error {
  border-bottom-color: rgba(255, 107, 107, 0.5);
}

/* Success states */
.navbar.success {
  border-bottom-color: rgba(72, 187, 120, 0.5);
}

/* Animation delays for staggered effects */
.navbar-link:nth-child(1) {
  animation-delay: 0.1s;
}
.navbar-link:nth-child(2) {
  animation-delay: 0.2s;
}
.navbar-link:nth-child(3) {
  animation-delay: 0.3s;
}
.navbar-link:nth-child(4) {
  animation-delay: 0.4s;
}

/* Ensure proper z-index stacking */
.navbar {
  z-index: 1000;
}

.dropdown-menu {
  z-index: 1001;
}

.mobile-menu-toggle {
  z-index: 1002;
}

/* Final mobile menu adjustments */
@media (max-width: 768px) {
  .navbar-menu {
    z-index: 999;
  }

  .navbar-menu.active {
    z-index: 999;
  }
}
</style>
