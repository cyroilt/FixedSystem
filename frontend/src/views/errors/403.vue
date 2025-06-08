<template>
  <div class="error-page bg-space-gradient">
    <div class="container">
      <div class="error-content">
        <!-- Animated Error Icon -->
        <div class="error-icon-container animate-bounce-in">
          <div class="error-icon">
            <i class="fas fa-shield-alt animate-pulse"></i>
            <div class="error-number animate-glow">403</div>
          </div>
          <div class="icon-particles">
            <div class="particle particle-1 animate-float"></div>
            <div
              class="particle particle-2 animate-float animate-stagger-2"
            ></div>
            <div
              class="particle particle-3 animate-float animate-stagger-4"
            ></div>
          </div>
        </div>

        <!-- Error Message -->
        <div class="error-message animate-fade-in-up animate-stagger-2">
          <h1 class="error-title animate-glow">Доступ запрещен</h1>
          <p class="error-description animate-fade-in-up animate-stagger-3">
            У вас недостаточно прав для доступа к этой странице. Обратитесь к
            администратору для получения необходимых разрешений.
          </p>
        </div>

        <!-- Error Details -->
        <div class="error-details animate-fade-in-up animate-stagger-4">
          <div class="detail-card hover-lift">
            <i class="fas fa-user-shield"></i>
            <h3>Требуется авторизация</h3>
            <p>Для доступа к этому ресурсу необходимы специальные права</p>
          </div>
          <div class="detail-card hover-lift animate-stagger-1">
            <i class="fas fa-key"></i>
            <h3>Проверьте права доступа</h3>
            <p>
              Убедитесь, что ваша учетная запись имеет необходимые разрешения
            </p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="error-actions animate-fade-in-up animate-stagger-5">
          <button @click="goBack" class="btn btn-secondary hover-lift">
            <i class="fas fa-arrow-left"></i>
            Назад
          </button>
          <router-link to="/" class="btn btn-primary hover-glow animate-pulse">
            <i class="fas fa-home"></i>
            На главную
          </router-link>
          <router-link
            v-if="!isAuthenticated"
            to="/login"
            class="btn btn-outline hover-scale"
          >
            <i class="fas fa-sign-in-alt"></i>
            Войти
          </router-link>
        </div>

        <!-- Help Section -->
        <div class="help-section animate-fade-in-up animate-stagger-6">
          <div class="help-card">
            <h4>
              <i class="fas fa-question-circle"></i>
              Нужна помощь?
            </h4>
            <p>
              Если вы считаете, что это ошибка, свяжитесь с нашей службой
              поддержки
            </p>
            <div class="help-actions">
              <a href="mailto:support@faculty.edu" class="help-link hover-glow">
                <i class="fas fa-envelope"></i>
                Написать в поддержку
              </a>
              <a href="tel:+7XXXXXXXXX" class="help-link hover-glow">
                <i class="fas fa-phone"></i>
                Позвонить
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Background Animation -->
    <div class="background-animation">
      <div class="floating-shape shape-1 animate-float"></div>
      <div class="floating-shape shape-2 animate-float animate-stagger-3"></div>
      <div class="floating-shape shape-3 animate-float animate-stagger-5"></div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Error403',
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  mounted() {
    this.initializeAnimations()
  },
  methods: {
    goBack() {
      if (window.history.length > 1) {
        this.$router.go(-1)
      } else {
        this.$router.push('/')
      }
    },
    initializeAnimations() {
      // Add intersection observer for error page animations
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

      // Observe error elements
      document.querySelectorAll('.detail-card, .help-card').forEach((el) => {
        observer.observe(el)
      })
    }
  }
}
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  position: relative;
  overflow: hidden;
}

.error-content {
  text-align: center;
  max-width: 800px;
  position: relative;
  z-index: 2;
}

.error-icon-container {
  position: relative;
  margin-bottom: 3rem;
}

.error-icon {
  position: relative;
  display: inline-block;
  padding: 2rem;
}

.error-icon i {
  font-size: 6rem;
  color: #ff6b6b;
  margin-bottom: 1rem;
  display: block;
  text-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
}

.error-number {
  font-size: 8rem;
  font-weight: 900;
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(255, 107, 107, 0.3);
  line-height: 1;
}

.icon-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, rgba(255, 107, 107, 0.6), transparent);
  border-radius: 50%;
}

.particle-1 {
  top: 20%;
  left: 20%;
  animation-duration: 4s;
}

.particle-2 {
  top: 60%;
  right: 20%;
  animation-duration: 6s;
}

.particle-3 {
  bottom: 30%;
  left: 60%;
  animation-duration: 5s;
}

.error-message {
  margin-bottom: 3rem;
}

.error-title {
  font-size: 3rem;
  font-weight: 700;
  color: #ff6b6b;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
}

.error-description {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.error-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.detail-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 107, 107, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.detail-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 107, 107, 0.1),
    transparent
  );
  transition: left 0.6s ease;
}

.detail-card:hover::before {
  left: 100%;
}

.detail-card:hover {
  border-color: rgba(255, 107, 107, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.detail-card i {
  font-size: 2.5rem;
  color: #ff6b6b;
  margin-bottom: 1rem;
  display: block;
}

.detail-card h3 {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.detail-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.help-section {
  margin-top: 2rem;
}

.help-card {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

.help-card h4 {
  color: #ffd700;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.help-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.help-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.help-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.help-link:hover {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
  border-color: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.3;
}

.shape-1 {
  width: 120px;
  height: 120px;
  top: 10%;
  left: 10%;
  background: radial-gradient(circle, rgba(255, 107, 107, 0.4), transparent);
  animation-duration: 8s;
}

.shape-2 {
  width: 80px;
  height: 80px;
  top: 70%;
  right: 15%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2), transparent);
  animation-duration: 6s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 70%;
  background: radial-gradient(circle, rgba(255, 107, 107, 0.3), transparent);
  animation-duration: 7s;
}

/* Animations */
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
    opacity: 0.7;
  }
}

@keyframes glow {
  0%,
  100% {
    text-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
  }
  50% {
    text-shadow: 0 0 40px rgba(255, 107, 107, 0.6);
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

.animate-bounce-in {
  animation: bounceIn 1s ease-out;
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out;
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

.animate-stagger-1 {
  animation-delay: 0.1s;
}
.animate-stagger-2 {
  animation-delay: 0.2s;
}
.animate-stagger-3 {
  animation-delay: 0.3s;
}
.animate-stagger-4 {
  animation-delay: 0.4s;
}
.animate-stagger-5 {
  animation-delay: 0.5s;
}
.animate-stagger-6 {
  animation-delay: 0.6s;
}

.hover-lift:hover {
  transform: translateY(-3px);
}

.hover-scale:hover {
  transform: scale(1.05);
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

/* Responsive Design */
@media (max-width: 768px) {
  .error-title {
    font-size: 2.5rem;
  }

  .error-number {
    font-size: 6rem;
  }

  .error-icon i {
    font-size: 4rem;
  }

  .error-description {
    font-size: 1.1rem;
  }

  .error-details {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .error-actions {
    flex-direction: column;
    align-items: center;
  }

  .help-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .error-page {
    padding: 1rem 0;
  }

  .error-title {
    font-size: 2rem;
  }

  .error-number {
    font-size: 4rem;
  }

  .detail-card,
  .help-card {
    padding: 1.5rem;
  }
}
</style>
