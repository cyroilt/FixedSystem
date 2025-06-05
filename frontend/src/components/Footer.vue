<template>
  <footer class="footer bg-space-gradient">
    <div class="container">
      <!-- Main Footer Content -->
      <div class="footer-content">
        <!-- Brand Section -->
        <div class="footer-section brand-section animate-fade-in-up">
          <div class="footer-brand">
            <i class="fas fa-university animate-pulse"></i>
            <h3 class="animate-glow">Faculty Portal</h3>
          </div>
          <p class="brand-description animate-fade-in-up animate-stagger-1">
            Современная система управления записями факультета с удобным интерфейсом 
            и передовыми технологиями для эффективной работы.
          </p>
          <div class="social-links animate-fade-in-up animate-stagger-2">
            <a href="#" class="social-link hover-lift" title="Facebook">
              <i class="fab fa-facebook-f"></i>
            </a>
            <a href="#" class="social-link hover-lift" title="Twitter">
              <i class="fab fa-twitter"></i>
            </a>
            <a href="#" class="social-link hover-lift" title="LinkedIn">
              <i class="fab fa-linkedin-in"></i>
            </a>
            <a href="#" class="social-link hover-lift" title="Instagram">
              <i class="fab fa-instagram"></i>
            </a>
            <a href="#" class="social-link hover-lift" title="YouTube">
              <i class="fab fa-youtube"></i>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="footer-section animate-fade-in-up animate-stagger-1">
          <h4 class="section-title">
            <i class="fas fa-link"></i>
            Быстрые ссылки
          </h4>
          <ul class="footer-links">
            <li class="animate-slide-in-left animate-stagger-1">
              <router-link to="/" class="footer-link hover-glow">
                <i class="fas fa-home"></i>
                Главная
              </router-link>
            </li>
            <li class="animate-slide-in-left animate-stagger-2">
              <router-link to="/recordings" class="footer-link hover-glow">
                <i class="fas fa-video"></i>
                Все записи
              </router-link>
            </li>
            <li class="animate-slide-in-left animate-stagger-3" v-if="!isAuthenticated">
              <router-link to="/login" class="footer-link hover-glow">
                <i class="fas fa-sign-in-alt"></i>
                Войти
              </router-link>
            </li>
            <li class="animate-slide-in-left animate-stagger-4" v-if="!isAuthenticated">
              <router-link to="/register" class="footer-link hover-glow">
                <i class="fas fa-user-plus"></i>
                Регистрация
              </router-link>
            </li>
            <li class="animate-slide-in-left animate-stagger-3" v-if="isAuthenticated">
              <router-link to="/profile" class="footer-link hover-glow">
                <i class="fas fa-user-circle"></i>
                Профиль
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Categories -->
        <div class="footer-section animate-fade-in-up animate-stagger-2">
          <h4 class="section-title">
            <i class="fas fa-tags"></i>
            Категории
          </h4>
          <ul class="footer-links">
            <li class="animate-slide-in-left animate-stagger-1">
              <a href="#" class="footer-link hover-glow">
                <i class="fas fa-graduation-cap"></i>
                Учебная деятельность
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-2">
              <a href="#" class="footer-link hover-glow">
                <i class="fas fa-flask"></i>
                Научная деятельность
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-3">
              <a href="#" class="footer-link hover-glow">
                <i class="fas fa-briefcase"></i>
                Служебная деятельность
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-4">
              <a href="#" class="footer-link hover-glow">
                <i class="fas fa-users"></i>
                Работа с личным составом
              </a>
            </li>
            <li class="animate-slide-in-left animate-stagger-5">
              <a href="#" class="footer-link hover-glow">
                <i class="fas fa-running"></i>
                Спортивная деятельность
              </a>
            </li>
          </ul>
        </div>

        <!-- Contact Info -->
        <div class="footer-section animate-fade-in-up animate-stagger-3">
          <h4 class="section-title">
            <i class="fas fa-address-book"></i>
            Контактная информация
          </h4>
          <div class="contact-info">
            <div class="contact-item animate-fade-in-right animate-stagger-1">
              <i class="fas fa-envelope contact-icon"></i>
              <div class="contact-details">
                <span class="contact-label">Email:</span>
                <a href="mailto:info@faculty.edu" class="contact-link hover-glow">
                  info@faculty.edu
                </a>
              </div>
            </div>
            <div class="contact-item animate-fade-in-right animate-stagger-2">
              <i class="fas fa-phone contact-icon"></i>
              <div class="contact-details">
                <span class="contact-label">Телефон:</span>
                <a href="tel:+7XXXXXXXXX" class="contact-link hover-glow">
                  +7 (XXX) XXX-XX-XX
                </a>
              </div>
            </div>
            <div class="contact-item animate-fade-in-right animate-stagger-3">
              <i class="fas fa-map-marker-alt contact-icon"></i>
              <div class="contact-details">
                <span class="contact-label">Адрес:</span>
                <span class="contact-text">
                  г. Москва, ул. Примерная, д. 123
                </span>
              </div>
            </div>
            <div class="contact-item animate-fade-in-right animate-stagger-4">
              <i class="fas fa-clock contact-icon"></i>
              <div class="contact-details">
                <span class="contact-label">Режим работы:</span>
                <span class="contact-text">
                  Пн-Пт: 9:00 - 18:00
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics Section -->
      <div class="footer-stats animate-fade-in-up animate-stagger-4">
        <div class="stat-item hover-glow animate-zoom-in animate-stagger-1">
          <div class="stat-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-content">
                        <div class="stat-number animate-pulse">1000+</div>
            <div class="stat-label">Пользователей</div>
          </div>
        </div>
        <div class="stat-item hover-glow animate-zoom-in animate-stagger-2">
          <div class="stat-icon">
            <i class="fas fa-video"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number animate-pulse">500+</div>
            <div class="stat-label">Записей</div>
          </div>
        </div>
        <div class="stat-item hover-glow animate-zoom-in animate-stagger-3">
          <div class="stat-icon">
            <i class="fas fa-download"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number animate-pulse">10K+</div>
            <div class="stat-label">Загрузок</div>
          </div>
        </div>
        <div class="stat-item hover-glow animate-zoom-in animate-stagger-4">
          <div class="stat-icon">
            <i class="fas fa-star"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number animate-pulse">4.9</div>
            <div class="stat-label">Рейтинг</div>
          </div>
        </div>
      </div>

      <!-- Newsletter Section -->
      <div class="newsletter-section animate-fade-in-up animate-stagger-5">
        <div class="newsletter-content">
          <div class="newsletter-info">
            <h3 class="newsletter-title animate-glow">
              <i class="fas fa-bell"></i>
              Подписка на обновления
            </h3>
            <p class="newsletter-description">
              Получайте уведомления о новых записях и важных событиях факультета
            </p>
          </div>
          <form class="newsletter-form" @submit.prevent="subscribeNewsletter">
            <div class="form-group">
              <input
                v-model="newsletterEmail"
                type="email"
                placeholder="Введите ваш email"
                class="newsletter-input"
                required
              >
              <button type="submit" class="newsletter-btn hover-lift" :disabled="subscribing">
                <i class="fas fa-paper-plane" v-if="!subscribing"></i>
                <i class="fas fa-spinner animate-spin" v-else></i>
                {{ subscribing ? 'Подписка...' : 'Подписаться' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer-bottom animate-fade-in-up animate-stagger-6">
        <div class="footer-bottom-content">
          <div class="copyright">
            <p>&copy; {{ currentYear }} Faculty Portal. Все права защищены.</p>
            <p class="version-info">Версия 2.0.0</p>
          </div>
          <div class="footer-bottom-links">
            <a href="#" class="bottom-link hover-glow">Политика конфиденциальности</a>
            <a href="#" class="bottom-link hover-glow">Условия использования</a>
            <a href="#" class="bottom-link hover-glow">Поддержка</a>
          </div>
          <div class="tech-info">
            <span class="tech-badge">
              <i class="fab fa-vuejs"></i>
              Vue.js
            </span>
            <span class="tech-badge">
              <i class="fab fa-python"></i>
              Flask
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Animated Background Elements -->
    <div class="footer-particles">
      <div class="particle particle-1 animate-float"></div>
      <div class="particle particle-2 animate-float animate-stagger-2"></div>
      <div class="particle particle-3 animate-float animate-stagger-4"></div>
      <div class="particle particle-4 animate-float animate-stagger-6"></div>
    </div>

    <!-- Back to Top Button -->
    <button 
      v-if="showBackToTop" 
      @click="scrollToTop" 
      class="back-to-top hover-lift animate-bounce-in"
      title="Наверх"
    >
      <i class="fas fa-chevron-up"></i>
    </button>
  </footer>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Footer',
  data() {
    return {
      newsletterEmail: '',
      subscribing: false,
      showBackToTop: false,
      currentYear: new Date().getFullYear()
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
    async subscribeNewsletter() {
      if (!this.newsletterEmail) return
      
      this.subscribing = true
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Show success message
        this.$toast?.success('Подписка оформлена успешно!')
        this.newsletterEmail = ''
      } catch (error) {
        console.error('Newsletter subscription error:', error)
        this.$toast?.error('Ошибка при оформлении подписки')
      } finally {
        this.subscribing = false
      }
    },
    initializeAnimations() {
      // Add intersection observer for footer animations
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in-view')
          }
        })
      }, observerOptions)

      // Observe footer elements
      document.querySelectorAll('.footer-section, .stat-item, .newsletter-section').forEach(el => {
        observer.observe(el)
      })
    }
  }
}
</script>

<style scoped>
.footer {
  background: linear-gradient(135deg, 
    rgba(30, 60, 114, 0.95) 0%, 
    rgba(16, 42, 79, 0.98) 50%, 
    rgba(10, 25, 47, 1) 100%);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 4rem 0 0;
  margin-top: 4rem;
  position: relative;
  overflow: hidden;
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
  opacity: 0.4;
}

.particle-1 {
  width: 8px;
  height: 8px;
  top: 20%;
  left: 10%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.6), transparent);
  animation-duration: 6s;
}

.particle-2 {
  width: 12px;
  height: 12px;
  top: 60%;
  right: 15%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent);
  animation-duration: 8s;
}

.particle-3 {
  width: 6px;
  height: 6px;
  bottom: 30%;
  left: 70%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.5), transparent);
  animation-duration: 7s;
}

.particle-4 {
  width: 10px;
  height: 10px;
  top: 40%;
  right: 60%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent);
  animation-duration: 9s;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-section {
  position: relative;
}

.brand-section {
  max-width: 350px;
}

.footer-brand {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.footer-brand i {
  font-size: 2.5rem;
  color: #ffd700;
  margin-right: 1rem;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-brand h3 {
  color: #ffd700;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.brand-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.7;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.social-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.2), transparent);
  transition: left 0.5s ease;
}

.social-link:hover::before {
  left: 100%;
}

.social-link:hover {
  background: rgba(255, 215, 0, 0.2);
  border-color: rgba(255, 215, 0, 0.4);
  color: #ffd700;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
}

.section-title {
  color: #ffd700;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title i {
  font-size: 1.1rem;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.75rem;
}

.footer-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.footer-link::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(90deg, rgba(255, 215, 0, 0.1), transparent);
  transition: width 0.3s ease;
}

.footer-link:hover::before {
  width: 100%;
}

.footer-link:hover {
  color: #ffd700;
  transform: translateX(5px);
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.footer-link i {
  width: 18px;
  text-align: center;
  font-size: 0.9rem;
  transition: transform 0.3s ease;
}

.footer-link:hover i {
  transform: scale(1.2);
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.contact-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.contact-icon {
  width: 20px;
  height: 20px;
  color: #ffd700;
  font-size: 1rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.contact-details {
  flex: 1;
}

.contact-label {
  display: block;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.contact-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
    transition: all 0.3s ease;
  font-weight: 500;
}

.contact-link:hover {
  color: #ffd700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.contact-text {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.footer-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
  padding: 2rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.stat-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
  transition: left 0.6s ease;
}

.stat-item:hover::before {
  left: 100%;
}

.stat-item:hover {
  transform: translateY(-5px);
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.stat-item:hover .stat-icon {
  transform: scale(1.1) rotate(10deg);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
}

.stat-icon i {
  font-size: 1.5rem;
  color: #1a1a2e;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.25rem;
  text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  font-size: 0.95rem;
}

.newsletter-section {
  background: rgba(0, 0, 0, 0.4);
  border-radius: 20px;
  padding: 2.5rem;
  margin-bottom: 3rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  position: relative;
  overflow: hidden;
}

.newsletter-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, 
    rgba(255, 215, 0, 0.05) 0%, 
    transparent 50%, 
    rgba(255, 215, 0, 0.05) 100%);
  pointer-events: none;
}

.newsletter-content {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 2rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.newsletter-title {
  color: #ffd700;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.newsletter-title i {
  font-size: 1.3rem;
}

.newsletter-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin: 0;
}

.newsletter-form {
  min-width: 350px;
}

.form-group {
  display: flex;
  gap: 1rem;
  align-items: stretch;
}

.newsletter-input {
  flex: 1;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.newsletter-input:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
  background: rgba(255, 255, 255, 0.15);
}

.newsletter-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.newsletter-btn {
  padding: 1rem 2rem;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border: none;
  border-radius: 12px;
  color: #1a1a2e;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.newsletter-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
}

.newsletter-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.footer-bottom {
  padding: 2rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  font-size: 0.9rem;
}

.version-info {
  font-size: 0.8rem !important;
  color: rgba(255, 255, 255, 0.4) !important;
  margin-top: 0.25rem !important;
}

.footer-bottom-links {
  display: flex;
  gap: 2rem;
  justify-content: center;
}

.bottom-link {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  padding: 0.5rem;
  border-radius: 6px;
}

.bottom-link:hover {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

.tech-info {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.tech-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tech-badge:hover {
  background: rgba(255, 215, 0, 0.1);
  border-color: rgba(255, 215, 0, 0.3);
  color: #ffd700;
}

.tech-badge i {
  font-size: 1rem;
}

.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 50px;
  height: 50px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border: none;
  border-radius: 50%;
  color: #1a1a2e;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
  z-index: 1000;
}

.back-to-top:hover {
  transform: translateY(-5px) scale(1.1);
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.5);
}

/* Animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes glow {
  0%, 100% {
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  }
  50% {
    text-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out;
}

.animate-slide-in-left {
  animation: slideInLeft 0.6s ease-out;
}

.animate-fade-in-right {
  animation: fadeInRight 0.6s ease-out;
}

.animate-zoom-in {
  animation: zoomIn 0.6s ease-out;
}

.animate-bounce-in {
  animation: bounceIn 0.8s ease-out;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite alternate;
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-stagger-1 { animation-delay: 0.1s; }
.animate-stagger-2 { animation-delay: 0.2s; }
.animate-stagger-3 { animation-delay: 0.3s; }
.animate-stagger-4 { animation-delay: 0.4s; }
.animate-stagger-5 { animation-delay: 0.5s; }
.animate-stagger-6 { animation-delay: 0.6s; }

.hover-lift:hover {
  transform: translateY(-3px);
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: repeat(2, 1fr);
    gap: 2.5rem;
  }
  
  .footer-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .newsletter-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .newsletter-form {
    min-width: auto;
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
    max-width: none;
  }
  
  .footer-stats {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .stat-item {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .newsletter-section {
    padding: 2rem;
      }
  
  .form-group {
    flex-direction: column;
    gap: 1rem;
  }
  
  .newsletter-btn {
    justify-content: center;
  }
  
  .footer-bottom-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    text-align: center;
  }
  
  .footer-bottom-links {
    flex-direction: column;
    gap: 1rem;
  }
  
  .tech-info {
    justify-content: center;
  }
  
  .back-to-top {
    bottom: 1.5rem;
    right: 1.5rem;
    width: 45px;
    height: 45px;
  }
  
  .social-links {
    justify-content: center;
  }
  
  .contact-item {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .contact-icon {
    margin-top: 0;
  }
}

@media (max-width: 480px) {
  .footer {
    padding: 2rem 0 0;
  }
  
  .footer-content {
    gap: 1.5rem;
  }
  
  .footer-section {
    padding: 0 1rem;
  }
  
  .newsletter-section {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .newsletter-title {
    font-size: 1.3rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .footer-brand {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .footer-brand h3 {
    font-size: 1.5rem;
  }
  
  .social-links {
    gap: 0.75rem;
  }
  
  .social-link {
    width: 40px;
    height: 40px;
  }
  
  .stat-item {
    padding: 1.25rem;
  }
  
  .stat-number {
    font-size: 1.75rem;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
  }
  
  .stat-icon i {
    font-size: 1.3rem;
  }
  
  .back-to-top {
    bottom: 1rem;
    right: 1rem;
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .tech-badge {
    padding: 0.4rem 0.8rem;
    font-size: 0.75rem;
  }
  
  .footer-bottom {
    padding: 1.5rem 0;
  }
  
  .bottom-link {
    font-size: 0.85rem;
    padding: 0.4rem;
  }
}

/* Custom scrollbar for newsletter input */
.newsletter-input::-webkit-scrollbar {
  width: 4px;
}

.newsletter-input::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.newsletter-input::-webkit-scrollbar-thumb {
  background: rgba(255, 215, 0, 0.5);
  border-radius: 2px;
}

.newsletter-input::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 215, 0, 0.7);
}

/* Loading state for newsletter */
.newsletter-btn .fas.fa-spinner {
  animation: spin 1s linear infinite;
}

/* Enhanced focus states for accessibility */
.footer-link:focus,
.social-link:focus,
.bottom-link:focus,
.newsletter-input:focus,
.newsletter-btn:focus,
.back-to-top:focus {
  outline: 2px solid rgba(255, 215, 0, 0.5);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .footer {
    background: #000000;
    border-top-color: #ffffff;
  }
  
  .footer-section,
  .stat-item,
  .newsletter-section {
    background: #1a1a1a;
    border-color: #ffffff;
  }
  
  .section-title,
  .footer-brand h3,
  .newsletter-title {
    color: #ffff00;
  }
  
  .footer-link,
  .contact-link,
  .bottom-link {
    color: #ffffff;
  }
  
  .footer-link:hover,
  .contact-link:hover,
  .bottom-link:hover {
    color: #ffff00;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .animate-fade-in-up,
  .animate-slide-in-left,
  .animate-fade-in-right,
  .animate-zoom-in,
  .animate-bounce-in,
  .animate-pulse,
  .animate-glow,
  .animate-float,
  .animate-spin {
    animation: none;
  }
  
  .hover-lift:hover,
  .social-link:hover,
  .stat-item:hover,
  .newsletter-btn:hover,
  .back-to-top:hover {
    transform: none;
  }
  
  .particle {
    display: none;
  }
}

/* Print styles */
@media print {
  .footer {
    background: white !important;
    color: black !important;
    box-shadow: none !important;
    border-top: 1px solid black !important;
  }
  
  .footer-particles,
  .back-to-top,
  .newsletter-section {
    display: none !important;
  }
  
  .footer-link,
  .contact-link,
  .bottom-link {
    color: black !important;
    text-decoration: underline !important;
  }
  
  .section-title,
  .footer-brand h3 {
    color: black !important;
  }
  
  .social-link {
    border: 1px solid black !important;
    background: white !important;
    color: black !important;
  }
}
</style>


