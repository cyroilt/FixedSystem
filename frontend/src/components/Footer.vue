<template>
  <footer class="footer bg-space-gradient">
    <div class="container">
      <!-- Animated Background Elements -->
      <div class="footer-particles">
        <div class="particle particle-1 animate-float"></div>
        <div class="particle particle-2 animate-float animate-stagger-2"></div>
        <div class="particle particle-3 animate-float animate-stagger-4"></div>
        <div class="particle particle-4 animate-float animate-stagger-6"></div>
        <div class="particle particle-5 animate-float animate-stagger-3"></div>
        <div class="particle particle-6 animate-float animate-stagger-5"></div>
      </div>

      <!-- Main Footer Content -->
      <div class="footer-content">
        <!-- Brand Section -->
        <div class="footer-section brand-section animate-fade-in-up">
          <div class="footer-brand">
            <div class="brand-icon-container">
              <i class="fas fa-university animate-pulse"></i>
              <div class="brand-glow"></div>
            </div>
            <h3 class="animate-glow">Faculty Portal</h3>
          </div>
          <p class="brand-description animate-fade-in-up animate-stagger-1">
            Современная система управления записями факультета с удобным
            интерфейсом и передовыми технологиями для эффективной работы и
            инновационного развития образовательного процесса.
          </p>
        </div>

        <!-- Quick Links -->
        <div class="footer-section animate-fade-in-up animate-stagger-1">
          <h4 class="section-title">
            <div class="title-icon">
              <i class="fas fa-link"></i>
              <div class="icon-glow"></div>
            </div>
            Быстрые ссылки
          </h4>
          <ul class="footer-links">
            <li class="animate-slide-in-left animate-stagger-1">
              <router-link to="/" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-home"></i>
                  <span>Главная</span>
                  <div class="link-trail"></div>
                </div>
              </router-link>
            </li>
            <li class="animate-slide-in-left animate-stagger-2">
              <router-link to="/recordings" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-video"></i>
                  <span>Все записи</span>
                  <div class="link-trail"></div>
                </div>
              </router-link>
            </li>
            <li class="animate-slide-in-left animate-stagger-3">
              <router-link to="/wall-print" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-newspaper"></i>
                  <span>Стенная печать</span>
                  <div class="link-trail"></div>
                </div>
              </router-link>
            </li>
            <li class="animate-slide-in-left animate-stagger-4">
              <router-link to="/command" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-users-cog"></i>
                  <span>Командование</span>
                  <div class="link-trail"></div>
                </div>
              </router-link>
            </li>
            <li
              class="animate-slide-in-left animate-stagger-5"
              v-if="!isAuthenticated"
            >
              <router-link to="/login" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-sign-in-alt"></i>
                  <span>Войти</span>
                  <div class="link-trail"></div>
                </div>
              </router-link>
            </li>
            <li
              class="animate-slide-in-left animate-stagger-6"
              v-if="!isAuthenticated"
            >
              <router-link to="/register" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-user-plus"></i>
                  <span>Регистрация</span>
                  <div class="link-trail"></div>
                </div>
              </router-link>
            </li>
            <li
              class="animate-slide-in-left animate-stagger-5"
              v-if="isAuthenticated"
            >
              <router-link to="/profile" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-user-circle"></i>
                  <span>Профиль</span>
                  <div class="link-trail"></div>
                </div>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Categories -->
        <div class="footer-section animate-fade-in-up animate-stagger-2">
          <h4 class="section-title">
            <div class="title-icon">
              <i class="fas fa-tags"></i>
              <div class="icon-glow"></div>
            </div>
            Категории
          </h4>
          <ul class="footer-links">
            <li class="animate-slide-in-left animate-stagger-1">
              <a href="#" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-graduation-cap"></i>
                  <span>Учебная деятельность</span>
                  <div class="link-trail"></div>
                </div>
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-2">
              <a href="#" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-flask"></i>
                  <span>Научная деятельность</span>
                  <div class="link-trail"></div>
                </div>
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-3">
              <a href="#" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-briefcase"></i>
                  <span>Служебная деятельность</span>
                  <div class="link-trail"></div>
                </div>
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-4">
              <a href="#" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-users"></i>
                  <span>Работа с личным составом</span>
                  <div class="link-trail"></div>
                </div>
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-5">
              <a href="#" class="footer-link hover-glow">
                <div class="link-wrapper">
                  <i class="fas fa-running"></i>
                  <span>Спортивная деятельность</span>
                  <div class="link-trail"></div>
                </div>
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer-bottom animate-fade-in-up animate-stagger-6">
        <div class="footer-bottom-content">
          <div class="copyright">
            <p>&copy; {{ currentYear }} Faculty Portal. Все права защищены.</p>
            <p class="version-info">
              <i class="fas fa-code-branch"></i>
              Версия 2.0.0 - Build {{ buildNumber }}
            </p>
          </div>
          <div class="footer-bottom-links">
            <a href="#" class="bottom-link hover-glow">
              <span>Политика конфиденциальности</span>
              <div class="bottom-link-glow"></div>
            </a>
            <a href="#" class="bottom-link hover-glow">
              <span>Условия использования</span>
              <div class="bottom-link-glow"></div>
            </a>
            <a href="#" class="bottom-link hover-glow">
              <span>Поддержка</span>
              <div class="bottom-link-glow"></div>
            </a>
          </div>
          <div class="tech-info">
            <div class="tech-badge hover-scale">
              <i class="fab fa-vuejs"></i>
              <span>Vue.js</span>
              <div class="tech-glow"></div>
            </div>
            <div class="tech-badge hover-scale">
              <i class="fab fa-python"></i>
              <span>Flask</span>
              <div class="tech-glow"></div>
            </div>
            <div class="tech-badge hover-scale">
              <i class="fas fa-database"></i>
              <span>PostgreSQL</span>
              <div class="tech-glow"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Back to Top Button -->
    <button
      v-if="showBackToTop"
      @click="scrollToTop"
      class="back-to-top hover-lift animate-bounce-in"
      title="Наверх"
    >
      <i class="fas fa-chevron-up"></i>
      <div class="back-to-top-glow"></div>
      <div class="back-to-top-particles">
        <div class="btt-particle"></div>
        <div class="btt-particle"></div>
        <div class="btt-particle"></div>
      </div>
    </button>
  </footer>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Footer',
  data() {
    return {
      showBackToTop: false,
      currentYear: new Date().getFullYear(),
      buildNumber: Math.random().toString(36).substr(2, 9).toUpperCase()
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
    this.initializeAnimations()
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.showBackToTop = window.scrollY > 500
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    },
    initializeAnimations() {
      // Add intersection observer for footer animations
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in-view')
          }
        })
      }, observerOptions)

      // Observe footer elements
      document.querySelectorAll('.footer-section').forEach((el) => {
        observer.observe(el)
      })
    }
  }
}
</script>

<style scoped>
.footer {
  background: linear-gradient(
    135deg,
    rgba(30, 60, 114, 0.95) 0%,
    rgba(16, 42, 79, 0.98) 25%,
    rgba(10, 25, 47, 1) 75%,
    rgba(5, 15, 35, 1) 100%
  );
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 215, 0, 0.2);
  padding: 5rem 0 0;
  margin-top: 4rem;
  position: relative;
  overflow: hidden;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    rgba(255, 215, 0, 0.03) 0%,
    transparent 25%,
    rgba(255, 215, 0, 0.02) 50%,
    transparent 75%,
    rgba(255, 215, 0, 0.03) 100%
  );
  pointer-events: none;
  animation: backgroundShimmer 8s ease-in-out infinite;
}

.footer-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.particle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
}

.particle-1 {
  width: 8px;
  height: 8px;
  top: 15%;
  left: 10%;
  background: radial-gradient(
    circle,
    rgba(255, 215, 0, 0.6),
    rgba(255, 215, 0, 0.2),
    transparent
  );
  animation-duration: 8s;
}

.particle-2 {
  width: 12px;
  height: 12px;
  top: 40%;
  right: 15%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.4),
    rgba(255, 255, 255, 0.1),
    transparent
  );
  animation-duration: 10s;
}

.particle-3 {
  width: 6px;
  height: 6px;
  bottom: 30%;
  left: 70%;
  background: radial-gradient(
    circle,
    rgba(255, 215, 0, 0.5),
    rgba(255, 215, 0, 0.1),
    transparent
  );
  animation-duration: 7s;
}

.particle-4 {
  width: 10px;
  height: 10px;
  top: 60%;
  right: 60%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent);
  animation-duration: 9s;
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

.particle-5 {
  width: 4px;
  height: 4px;
  top: 25%;
  left: 50%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.7), transparent);
  animation-duration: 6s;
}

.particle-6 {
  width: 14px;
  height: 14px;
  bottom: 15%;
  right: 30%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.2),
    rgba(255, 255, 255, 0.05),
    transparent
  );
  animation-duration: 11s;
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 4rem;
  margin-bottom: 4rem;
  position: relative;
  z-index: 2;
}

.footer-section {
  position: relative;
}

.brand-section {
  max-width: 450px;
}

.footer-brand {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1.5rem;
}

.brand-icon-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-icon-container i {
  font-size: 3rem;
  color: #ffd700;
  background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease infinite;
  position: relative;
  z-index: 2;
}

.brand-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: radial-gradient(
    circle,
    rgba(255, 215, 0, 0.3),
    rgba(255, 215, 0, 0.1),
    transparent
  );
  border-radius: 50%;
  animation: brandGlow 3s ease-in-out infinite;
}

.footer-brand h3 {
  color: #ffd700;
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 0 25px rgba(255, 215, 0, 0.4);
  background: linear-gradient(
    45deg,
    #ffd700,
    #ffed4e,
    #ffd700,
    #ffb347,
    #ffd700
  );
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: advancedGradientShift 6s ease infinite;
}

.brand-description {
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.8;
  margin-bottom: 0;
  font-size: 1.1rem;
  font-weight: 400;
  text-align: justify;
}

.section-title {
  color: #ffd700;
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

.title-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-icon i {
  font-size: 1.2rem;
  position: relative;
  z-index: 2;
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 30px;
  height: 30px;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.2), transparent);
  border-radius: 50%;
  animation: iconPulse 2s ease-in-out infinite;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 1rem;
}

.footer-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: block;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}

.link-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  position: relative;
  z-index: 2;
}

.link-trail {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 215, 0, 0.1),
    transparent
  );
  transition: left 0.5s ease;
}

.footer-link:hover .link-trail {
  left: 100%;
}

.footer-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 215, 0, 0.05);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 10px;
}

.footer-link:hover::before {
  opacity: 1;
}

.footer-link:hover {
  color: #ffd700;
  transform: translateX(8px);
  text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
}

.footer-link i {
  width: 20px;
  text-align: center;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.footer-link:hover i {
  transform: scale(1.2) rotate(5deg);
  color: #ffd700;
}

.footer-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #ffd700, #ffed4e);
  transition: width 0.4s ease;
}

.footer-link:hover::after {
  width: 100%;
}

.footer-bottom {
  padding: 3rem 0;
  border-top: 1px solid rgba(255, 215, 0, 0.2);
  position: relative;
  z-index: 2;
}

.footer-bottom::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 215, 0, 0.5),
    transparent
  );
}

.footer-bottom-content {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 2rem;
  align-items: center;
}

.copyright {
  text-align: left;
}

.copyright p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.version-info {
  font-size: 0.9rem !important;
  color: rgba(255, 255, 255, 0.5) !important;
  margin-top: 0.75rem !important;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.version-info i {
  font-size: 0.8rem;
  color: rgba(255, 215, 0, 0.6);
}

.footer-bottom-links {
  display: flex;
  gap: 2rem;
  justify-content: center;
}

.bottom-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 1rem;
  transition: all 0.3s ease;
  padding: 0.75rem 1.25rem;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  font-weight: 500;
}

.bottom-link-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 215, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 10px;
}

.bottom-link:hover .bottom-link-glow {
  opacity: 1;
}

.bottom-link:hover {
  color: #ffd700;
  text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
  transform: translateY(-2px);
}

.tech-info {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.tech-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.tech-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    rgba(255, 215, 0, 0.15),
    rgba(255, 215, 0, 0.05)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 25px;
}

.tech-badge:hover .tech-glow {
  opacity: 1;
}

.tech-badge:hover {
  background: rgba(255, 215, 0, 0.1);
  border-color: rgba(255, 215, 0, 0.4);
  color: #ffd700;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
}

.tech-badge i {
  font-size: 1.1rem;
}

.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 60px;
  height: 60px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border: none;
  border-radius: 50%;
  color: #1a1a2e;
  font-size: 1.4rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 6px 25px rgba(255, 215, 0, 0.4);
  z-index: 1000;
  position: relative;
  overflow: hidden;
}

.back-to-top-glow {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.4), transparent);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.back-to-top:hover .back-to-top-glow {
  opacity: 1;
  animation: backToTopGlow 2s ease-in-out infinite;
}

.back-to-top-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.btt-particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(26, 26, 46, 0.5);
  border-radius: 50%;
  animation: bttParticleFloat 2s ease-in-out infinite;
}

.btt-particle:nth-child(1) {
  top: 20%;
  left: 30%;
  animation-delay: 0s;
}

.btt-particle:nth-child(2) {
  top: 60%;
  right: 25%;
  animation-delay: 0.7s;
}

.btt-particle:nth-child(3) {
  bottom: 30%;
  left: 60%;
  animation-delay: 1.4s;
}

.back-to-top:hover {
  transform: translateY(-8px) scale(1.15);
  box-shadow: 0 15px 45px rgba(255, 215, 0, 0.6);
}

.back-to-top i {
  position: relative;
  z-index: 2;
}

/* Enhanced Animations */
@keyframes backgroundShimmer {
  0%,
  100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

@keyframes brandGlow {
  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.6;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
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

@keyframes advancedGradientShift {
  0% {
    background-position: 0% 50%;
  }
  25% {
    background-position: 100% 50%;
  }
  50% {
    background-position: 100% 100%;
  }
  75% {
    background-position: 0% 100%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes iconPulse {
  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.4;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0.8;
  }
}

@keyframes backToTopGlow {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

@keyframes bttParticleFloat {
  0%,
  100% {
    transform: translateY(0px) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-8px) scale(1.2);
    opacity: 1;
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

@keyframes glow {
  0%,
  100% {
    text-shadow: 0 0 25px rgba(255, 215, 0, 0.4);
  }
  50% {
    text-shadow: 0 0 35px rgba(255, 215, 0, 0.7);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Animation Classes */
.animate-fade-in-up {
  animation: fadeInUp 1s ease-out;
}

.animate-slide-in-left {
  animation: slideInLeft 0.8s ease-out;
}

.animate-bounce-in {
  animation: bounceIn 1s ease-out;
}

.animate-pulse {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-glow {
  animation: glow 3s ease-in-out infinite alternate;
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

/* Stagger Delays */
.animate-stagger-1 {
  animation-delay: 0.2s;
}
.animate-stagger-2 {
  animation-delay: 0.4s;
}
.animate-stagger-3 {
  animation-delay: 0.6s;
}
.animate-stagger-4 {
  animation-delay: 0.8s;
}
.animate-stagger-5 {
  animation-delay: 1s;
}
.animate-stagger-6 {
  animation-delay: 1.2s;
}

/* Hover Effects */
.hover-lift:hover {
  transform: translateY(-5px);
}

.hover-glow:hover {
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
}

.hover-scale:hover {
  transform: scale(1.05);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .footer-content {
    grid-template-columns: 1.5fr 1fr 1fr;
    gap: 3rem;
  }

  .footer-brand h3 {
    font-size: 2rem;
  }

  .brand-icon-container i {
    font-size: 2.5rem;
  }
}

@media (max-width: 900px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
  }

  .brand-section {
    grid-column: 1 / -1;
    max-width: none;
    text-align: center;
    margin-bottom: 2rem;
  }

  .footer-brand {
    justify-content: center;
  }

  .section-title {
    justify-content: center;
  }

  .footer-bottom-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }

  .tech-info {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .footer {
    padding: 3rem 0 0;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }

  .brand-section {
    margin-bottom: 1rem;
  }

  .footer-brand {
    flex-direction: column;
    gap: 1rem;
  }

  .footer-brand h3 {
    font-size: 1.8rem;
  }

  .brand-icon-container i {
    font-size: 2.2rem;
  }

  .footer-bottom-links {
    flex-direction: column;
    gap: 1rem;
  }

  .tech-info {
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .back-to-top {
    bottom: 1.5rem;
    right: 1.5rem;
    width: 55px;
    height: 55px;
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .footer {
    padding: 2rem 0 0;
  }

  .footer-content {
    gap: 1.5rem;
    padding: 0 1rem;
  }

  .footer-brand h3 {
    font-size: 1.6rem;
  }

  .brand-icon-container i {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.2rem;
  }

  .footer-link {
    font-size: 0.95rem;
  }

  .link-wrapper {
    padding: 0.6rem 0.8rem;
  }

  .bottom-link {
    font-size: 0.9rem;
    padding: 0.6rem 1rem;
  }

  .tech-badge {
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
  }

  .back-to-top {
    bottom: 1rem;
    right: 1rem;
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }

  .footer-bottom {
    padding: 2rem 0;
  }

  .copyright p {
    font-size: 0.9rem;
  }

  .version-info {
    font-size: 0.8rem !important;
  }
}

@media (max-width: 360px) {
  .footer-brand {
    gap: 0.75rem;
  }

  .footer-brand h3 {
    font-size: 1.4rem;
  }

  .brand-icon-container i {
    font-size: 1.8rem;
  }

  .section-title {
    font-size: 1.1rem;
    flex-direction: column;
    gap: 0.5rem;
  }

  .tech-info {
    flex-direction: column;
    align-items: center;
  }

  .tech-badge {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }

  .back-to-top {
    width: 45px;
    height: 45px;
    font-size: 1.1rem;
  }
}

/* Enhanced focus states for accessibility */
.footer-link:focus-visible,
.bottom-link:focus-visible,
.tech-badge:focus-visible,
.back-to-top:focus-visible {
  outline: 3px solid rgba(255, 215, 0, 0.8);
  outline-offset: 3px;
  border-radius: 8px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .footer {
    background: #000000;
    border-top-color: #ffffff;
  }

  .footer-section {
    background: #1a1a1a;
    border: 1px solid #ffffff;
    border-radius: 8px;
    padding: 1rem;
  }

  .section-title,
  .footer-brand h3 {
    color: #ffff00;
  }

  .footer-link,
  .bottom-link {
    color: #ffffff;
  }

  .footer-link:hover,
  .bottom-link:hover {
    color: #ffff00;
    background: #333333;
  }

  .tech-badge {
    background: #333333;
    border-color: #ffffff;
    color: #ffffff;
  }

  .tech-badge:hover {
    background: #ffff00;
    color: #000000;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .animate-fade-in-up,
  .animate-slide-in-left,
  .animate-bounce-in,
  .animate-pulse,
  .animate-glow,
  .animate-float,
  .brand-glow,
  .icon-glow,
  .back-to-top-glow,
  .tech-glow,
  .bottom-link-glow {
    animation: none;
  }

  .hover-lift:hover,
  .hover-scale:hover,
  .footer-link:hover,
  .tech-badge:hover,
  .back-to-top:hover {
    transform: none;
  }

  .particle,
  .back-to-top-particles {
    display: none;
  }

  .footer::before {
    display: none;
  }
}

/* Print styles */
@media print {
  .footer {
    background: white !important;
    color: black !important;
    box-shadow: none !important;
    border-top: 2px solid black !important;
  }

  .footer-particles,
  .back-to-top,
  .brand-glow,
  .icon-glow,
  .tech-glow,
  .bottom-link-glow,
  .back-to-top-particles {
    display: none !important;
  }

  .footer-link,
  .bottom-link {
    color: black !important;
    text-decoration: underline !important;
  }

  .section-title,
  .footer-brand h3 {
    color: black !important;
  }

  .tech-badge {
    border: 1px solid black !important;
    background: white !important;
    color: black !important;
  }

  .footer-content {
    grid-template-columns: repeat(3, 1fr) !important;
  }
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
  .footer {
    background: linear-gradient(
      135deg,
      rgba(15, 30, 57, 0.98) 0%,
      rgba(8, 21, 39, 1) 25%,
      rgba(5, 12, 23, 1) 75%,
      rgba(2, 8, 18, 1) 100%
    );
  }

  .tech-badge {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.15);
  }
}

/* Performance optimizations */
.footer * {
  will-change: auto;
}

.footer .animate-float,
.footer .animate-pulse,
.footer .animate-glow {
  will-change: transform, opacity;
}

.footer .hover-lift:hover,
.footer .hover-scale:hover {
  will-change: transform;
}

/* Custom selection colors */
::selection {
  background: rgba(255, 215, 0, 0.3);
  color: #ffffff;
}

::-moz-selection {
  background: rgba(255, 215, 0, 0.3);
  color: #ffffff;
}

/* Tooltip styles for back to top button */
.back-to-top[title]:hover::after {
  content: attr(title);
  position: absolute;
  bottom: 120%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.9);
  color: #ffffff;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  white-space: nowrap;
  z-index: 1001;
  pointer-events: none;
}

.back-to-top[title]:hover::before {
  content: '';
  position: absolute;
  bottom: 110%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: rgba(0, 0, 0, 0.9);
  z-index: 1001;
  pointer-events: none;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Intersection observer animations */
.animate-in-view {
  animation: slideInFromBottom 1s ease-out forwards;
}

@keyframes slideInFromBottom {
  from {
    opacity: 0;
    transform: translateY(60px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Enhanced mobile touch targets */
@media (max-width: 768px) {
  .footer-link,
  .bottom-link,
  .tech-badge {
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

/* Ultra-wide screen optimizations */
@media (min-width: 1920px) {
  .footer-content {
    max-width: 1600px;
    margin: 0 auto 4rem auto;
  }
}
</style>
