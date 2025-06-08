<template>
  <div class="error-page bg-space-gradient">
    <div class="container">
      <div class="error-content">
        <!-- Animated Error Icon -->
        <div class="error-icon-container animate-bounce-in">
          <div class="error-icon">
            <i class="fas fa-search animate-pulse"></i>
            <div class="error-number animate-glow">404</div>
          </div>
          <div class="icon-particles">
            <div class="particle particle-1 animate-float"></div>
            <div
              class="particle particle-2 animate-float animate-stagger-2"
            ></div>
            <div
              class="particle particle-3 animate-float animate-stagger-4"
            ></div>
            <div
              class="particle particle-4 animate-float animate-stagger-6"
            ></div>
          </div>
        </div>

        <!-- Error Message -->
        <div class="error-message animate-fade-in-up animate-stagger-2">
          <h1 class="error-title animate-glow">Страница не найдена</h1>
          <p class="error-description animate-fade-in-up animate-stagger-3">
            К сожалению, запрашиваемая страница не существует или была
            перемещена. Проверьте правильность введенного адреса или
            воспользуйтесь навигацией.
          </p>
        </div>

        <!-- Search Section -->
        <div class="search-section animate-fade-in-up animate-stagger-4">
          <div class="search-card">
            <h3>
              <i class="fas fa-search"></i>
              Поиск по сайту
            </h3>
            <form @submit.prevent="performSearch" class="search-form">
              <div class="search-input-group">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Введите поисковый запрос..."
                  class="search-input"
                />
                <button
                  type="submit"
                  class="search-btn hover-lift"
                  :disabled="!searchQuery.trim()"
                >
                  <i class="fas fa-search"></i>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Popular Pages -->
        <div class="popular-pages animate-fade-in-up animate-stagger-5">
          <h3 class="section-title">
            <i class="fas fa-star"></i>
            Популярные страницы
          </h3>
          <div class="pages-grid">
            <router-link to="/" class="page-card hover-lift">
              <div class="page-icon">
                <i class="fas fa-home"></i>
              </div>
              <div class="page-info">
                <h4>Главная страница</h4>
                <p>Добро пожаловать в Faculty Portal</p>
              </div>
            </router-link>
            <router-link to="/recordings" class="page-card hover-lift">
              <div class="page-icon">
                <i class="fas fa-video"></i>
              </div>
              <div class="page-info">
                <h4>Все записи</h4>
                <p>Просмотр всех записей факультета</p>
              </div>
            </router-link>
            <router-link
              v-if="!isAuthenticated"
              to="/login"
              class="page-card hover-lift"
            >
              <div class="page-icon">
                <i class="fas fa-sign-in-alt"></i>
              </div>
              <div class="page-info">
                <h4>Вход в систему</h4>
                <p>Авторизация пользователей</p>
              </div>
            </router-link>
            <router-link
              v-if="!isAuthenticated"
              to="/register"
              class="page-card hover-lift"
            >
              <div class="page-icon">
                <i class="fas fa-user-plus"></i>
              </div>
              <div class="page-info">
                <h4>Регистрация</h4>
                <p>Создание новой учетной записи</p>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="error-actions animate-fade-in-up animate-stagger-6">
          <button @click="goBack" class="btn btn-secondary hover-lift">
            <i class="fas fa-arrow-left"></i>
            Назад
          </button>
          <router-link to="/" class="btn btn-primary hover-glow animate-pulse">
            <i class="fas fa-home"></i>
            На главную
          </router-link>
          <button @click="reloadPage" class="btn btn-outline hover-scale">
            <i class="fas fa-redo"></i>
            Обновить
          </button>
        </div>

        <!-- Help Section -->
        <div class="help-section animate-fade-in-up animate-stagger-7">
          <div class="help-card">
            <h4>
              <i class="fas fa-life-ring"></i>
              Нужна помощь?
            </h4>
            <p>Если проблема повторяется, обратитесь в службу поддержки</p>
            <div class="help-actions">
              <a href="mailto:support@faculty.edu" class="help-link hover-glow">
                <i class="fas fa-envelope"></i>
                Написать в поддержку
              </a>
              <router-link to="/recordings" class="help-link hover-glow">
                <i class="fas fa-video"></i>
                Просмотреть записи
              </router-link>
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
      <div class="floating-shape shape-4 animate-float animate-stagger-7"></div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Error404',
  data() {
    return {
      searchQuery: ''
    }
  },
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
    reloadPage() {
      window.location.reload()
    },
    performSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({
          path: '/recordings',
          query: { search: this.searchQuery.trim() }
        })
      }
    },
    initializeAnimations() {
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

      document
        .querySelectorAll('.page-card, .search-card, .help-card')
        .forEach((el) => {
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
  max-width: 900px;
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
  color: #ffd700;
  margin-bottom: 1rem;
  display: block;
  text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
}

.error-number {
  font-size: 8rem;
  font-weight: 900;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(255, 215, 0, 0.3);
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
  background: radial-gradient(circle, rgba(255, 215, 0, 0.6), transparent);
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

.particle-4 {
  top: 40%;
  right: 40%;
  animation-duration: 7s;
}

.error-message {
  margin-bottom: 3rem;
}

.error-title {
  font-size: 3rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.error-description {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.search-section {
  margin-bottom: 3rem;
}

.search-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 215, 0, 0.2);
  max-width: 500px;
  margin: 0 auto;
}

.search-card h3 {
  color: #ffd700;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.search-input-group {
  display: flex;
  gap: 0.5rem;
}

.search-input {
  flex: 1;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-btn {
  padding: 1rem 1.5rem;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border: none;
  border-radius: 12px;
  color: #1a1a2e;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
}

.search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.popular-pages {
  margin-bottom: 3rem;
}

.section-title {
  color: #ffd700;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.pages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.page-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  overflow: hidden;
}

.page-card::before {
  content: '';
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
  transition: left 0.6s ease;
}

.page-card:hover::before {
  left: 100%;
}

.page-card:hover {
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
}

.page-icon {
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

.page-card:hover .page-icon {
  transform: scale(1.1) rotate(10deg);
}

.page-icon i {
  font-size: 1.5rem;
  color: #1a1a2e;
}

.page-info {
  flex: 1;
  text-align: left;
}

.page-info h4 {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.page-info p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0;
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
  background: radial-gradient(circle, rgba(255, 215, 0, 0.4), transparent);
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
  background: radial-gradient(circle, rgba(255, 215, 0, 0.3), transparent);
  animation-duration: 7s;
}

.shape-4 {
  width: 60px;
  height: 60px;
  top: 30%;
  right: 30%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent);
  animation-duration: 9s;
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
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  }
  50% {
    text-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
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
.animate-stagger-7 {
  animation-delay: 0.7s;
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

  .pages-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .page-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .page-info {
    text-align: center;
  }

  .error-actions {
    flex-direction: column;
    align-items: center;
  }

  .help-actions {
    flex-direction: column;
  }

  .search-input-group {
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

  .search-card,
  .help-card {
    padding: 1.5rem;
  }

  .page-card {
    padding: 1.25rem;
  }
}
</style>
