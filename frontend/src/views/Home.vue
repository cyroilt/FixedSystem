<template>
  <div class="home bg-darker-gradient particles-bg">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content animate-fade-in-up">
          <h1 class="hero-title animate-glow">
            Добро пожаловать в Faculty Portal
          </h1>
          <p class="hero-subtitle animate-fade-in-up animate-stagger-2">
            Современная система управления записями факультета с удобным
            интерфейсом
          </p>
          <div class="hero-buttons animate-slide-in-up animate-stagger-3">
            <router-link
              to="/recordings"
              class="btn btn-primary hover-lift animate-pulse"
            >
              <i class="fas fa-video"></i>
              Просмотреть записи
            </router-link>
            <router-link
              v-if="!isAuthenticated"
              to="/register"
              class="btn btn-secondary hover-scale"
            >
              <i class="fas fa-user-plus"></i>
              Присоединиться
            </router-link>
          </div>
        </div>
      </div>
      <div class="hero-background">
        <div class="floating-shapes">
          <div class="shape shape-1 animate-float"></div>
          <div class="shape shape-2 animate-float animate-stagger-2"></div>
          <div class="shape shape-3 animate-float animate-stagger-4"></div>
          <div class="shape shape-4 animate-rotate-in animate-stagger-3"></div>
          <div class="shape shape-5 animate-bounce-in animate-stagger-5"></div>
        </div>
      </div>
    </section>

    <!-- Faculty History Section -->
    <section class="faculty-history bg-space-gradient">
      <div class="container">
        <h2 class="section-title animate-fade-in-up" data-aos="fade-up">
          История третьего факультета
        </h2>
        <div class="history-content" data-aos="fade-up" data-aos-delay="200">
          <div class="history-text">
            <p class="animate-fade-in-left animate-stagger-1">
              История третьего факультета берет свое начало с 1992 года. До
              этого времени были батальоны, но с преобразованием высшего
              военного училища в военный институт правительственной связи,
              вместо батальонов появились факультеты.
            </p>
            <p class="animate-fade-in-left animate-stagger-2">
              Первым начальником третьего факультета стал полковник Лукьянцев
              Виктор Федорович, который являлся с 1988 по 1992 гг. командиром
              первого батальона. На смену ему пришел полковник Иванов Владимир
              Николаевич, при котором в 1998 году произвелся первый набор
              курсантов из числа девушек по специальности «Автоматизированные
              системы управления».
            </p>
            <p class="animate-fade-in-left animate-stagger-3">
              С 2014 года по настоящее время начальником третьего факультета
              является полковник Беляков Эдуард Викторович, кандидат технических
              наук, доцент.
            </p>
            <div class="history-action">
              <router-link
                to="/faculty-history"
                class="btn btn-outline-primary hover-glow animate-pulse"
              >
                <i class="fas fa-book-open"></i>
                Подробная история
              </router-link>
            </div>
          </div>
          <div class="history-stats">
            <div
              class="stat-item hover-glow animate-zoom-in animate-stagger-1"
              data-aos="zoom-in"
              data-aos-delay="300"
            >
              <div class="stat-number animate-pulse">30+</div>
              <div class="stat-label">Лет истории</div>
            </div>
            <div
              class="stat-item hover-glow animate-zoom-in animate-stagger-2"
              data-aos="zoom-in"
              data-aos-delay="400"
            >
              <div class="stat-number animate-pulse">3</div>
              <div class="stat-label">Кафедры</div>
            </div>
            <div
              class="stat-item hover-glow animate-zoom-in animate-stagger-3"
              data-aos="zoom-in"
              data-aos-delay="500"
            >
              <div class="stat-number animate-pulse">1998</div>
              <div class="stat-label">Первый набор девушек</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Latest Recordings Section -->
    <section class="latest-recordings bg-animated-gradient">
      <div class="container">
        <h2 class="section-title animate-fade-in-up" data-aos="fade-up">
          Последние записи
        </h2>
        <div v-if="loading" class="loading animate-bounce-in">
          <div class="loading-spinner"></div>
          <p class="loading-dots">Загрузка записей</p>
        </div>
        <div v-else-if="latestRecordings.length > 0" class="recordings-grid">
          <div
            v-for="(recording, index) in latestRecordings"
            :key="recording.id"
            class="recording-card hover-lift animate-fade-in-up"
            :class="`animate-stagger-${index + 1}`"
            data-aos="fade-up"
            :data-aos-delay="index * 100"
            @click="viewRecording(recording.id)"
          >
            <div class="recording-image" v-if="recording.image_path">
              <img
                :src="getImageUrl(recording.image_path)"
                :alt="recording.title"
                @error="handleImageError"
                loading="lazy"
                class="animate-scale-in"
              />
              <div class="image-overlay animate-fade-in-up">
                <i class="fas fa-eye animate-pulse"></i>
              </div>
            </div>
            <div v-else class="recording-placeholder animate-shimmer">
              <i class="fas fa-image animate-rotate-in"></i>
              <span>Нет изображения</span>
            </div>
            <div class="recording-content">
              <div
                class="recording-category animate-slide-in-up"
                v-if="recording.category"
              >
                <i class="fas fa-tag"></i>
                {{ recording.category.name }}
              </div>
              <h3 class="recording-title animate-fade-in-left">
                {{ recording.title }}
              </h3>
              <p class="recording-excerpt animate-fade-in-right">
                {{ truncateText(recording.content, 100) }}
              </p>
              <div class="recording-meta animate-fade-in-up">
                <span class="recording-date">
                  <i class="fas fa-calendar"></i>
                  {{ formatDate(recording.created_at) }}
                </span>
                <span v-if="recording.views" class="recording-views">
                  <i class="fas fa-eye"></i>
                  {{ recording.views }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-recordings animate-bounce-in">
          <i class="fas fa-video animate-float"></i>
          <p>Пока нет записей</p>
        </div>
        <div class="section-footer animate-slide-in-up" data-aos="fade-up">
          <router-link
            to="/recordings"
            class="btn btn-primary hover-glow animate-pulse"
          >
            <i class="fas fa-arrow-right"></i>
            Посмотреть все записи
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features bg-space-gradient">
      <div class="container">
        <h2 class="section-title animate-fade-in-up" data-aos="fade-up">
          Возможности портала
        </h2>
        <div class="features-grid">
          <div
            class="feature-card hover-lift animate-flip-in animate-stagger-1"
            data-aos="fade-up"
            data-aos-delay="100"
          >
            <div class="feature-icon animate-rotate-in">
              <i class="fas fa-video"></i>
            </div>
            <h3 class="animate-fade-in-up">Мультимедийные записи</h3>
            <p class="animate-fade-in-up animate-stagger-2">
              Поддержка текста, изображений и видео в одной записи
            </p>
          </div>
          <div
            class="feature-card hover-lift animate-flip-in animate-stagger-2"
            data-aos="fade-up"
            data-aos-delay="200"
          >
            <div class="feature-icon animate-rotate-in animate-stagger-2">
              <i class="fas fa-tags"></i>
            </div>
            <h3 class="animate-fade-in-up animate-stagger-2">
              Система категорий
            </h3>
            <p class="animate-fade-in-up animate-stagger-3">
              Удобная организация контента по категориям и тегам
            </p>
          </div>
          <div
            class="feature-card hover-lift animate-flip-in animate-stagger-3"
            data-aos="fade-up"
            data-aos-delay="300"
          >
            <div class="feature-icon animate-rotate-in animate-stagger-3">
              <i class="fas fa-users"></i>
            </div>
            <h3 class="animate-fade-in-up animate-stagger-3">
              Управление пользователями
            </h3>
            <p class="animate-fade-in-up animate-stagger-4">
              Система ролей для администраторов и модераторов
            </p>
          </div>
          <div
            class="feature-card hover-lift animate-flip-in animate-stagger-4"
            data-aos="fade-up"
            data-aos-delay="400"
          >
            <div class="feature-icon animate-rotate-in animate-stagger-4">
              <i class="fas fa-mobile-alt"></i>
            </div>
            <h3 class="animate-fade-in-up animate-stagger-4">
              Адаптивный дизайн
            </h3>
            <p class="animate-fade-in-up animate-stagger-5">
              Отлично работает на всех устройствах
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Home',
  data() {
    return {
      latestRecordings: [],
      loading: false
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  async created() {
    await this.fetchLatestRecordings()
  },
  async mounted() {
    await this.fetchLatestRecordings()
    this.initializeAnimations()
  },
  methods: {
    initializeAnimations() {
      // Add intersection observer for custom animations
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

      // Observe all animatable elements
      document
        .querySelectorAll('.recording-card, .feature-card, .stat-item')
        .forEach((el) => {
          observer.observe(el)
        })
    },
    async fetchLatestRecordings() {
      this.loading = true
      try {
        this.latestRecordings = await this.$store.dispatch(
          'fetchLatestRecordings'
        )
      } catch (error) {
        console.error('Error fetching latest recordings:', error)
      } finally {
        this.loading = false
      }
    },
    getImageUrl(imagePath) {
      if (!imagePath) return null
      if (imagePath.startsWith('http')) return imagePath
      if (imagePath.startsWith('/uploads/')) {
        return `http://localhost:5000${imagePath}`
      }
      return `http://localhost:5000/uploads/${imagePath}`
    },
    handleImageError(event) {
      console.error('Image failed to load:', event.target.src)
      const imageContainer = event.target.closest('.recording-image')
      if (imageContainer) {
        imageContainer.style.display = 'none'
        const placeholder = imageContainer.nextElementSibling
        if (
          placeholder &&
          placeholder.classList.contains('recording-placeholder')
        ) {
          placeholder.style.display = 'flex'
        }
      }
    },
    viewRecording(id) {
      this.$router.push(`/recordings/${id}`)
    },
    truncateText(text, length) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  position: relative;
}

.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-content {
  text-align: center;
  z-index: 2;
  position: relative;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s ease infinite;
}
.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: rgba(255, 255, 255, 0.9);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
}

.shape-1 {
  width: 100px;
  height: 100px;
  top: 20%;
  left: 10%;
  background: radial-gradient(
    circle,
    rgba(255, 215, 0, 0.3),
    rgba(255, 215, 0, 0.1)
  );
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 10%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.2),
    rgba(255, 255, 255, 0.05)
  );
}

.shape-3 {
  width: 80px;
  height: 80px;
  bottom: 20%;
  left: 20%;
  background: radial-gradient(
    circle,
    rgba(255, 215, 0, 0.4),
    rgba(255, 215, 0, 0.1)
  );
}

.shape-4 {
  width: 120px;
  height: 120px;
  top: 30%;
  right: 30%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15), transparent);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}

.shape-5 {
  width: 60px;
  height: 60px;
  bottom: 40%;
  right: 20%;
  background: radial-gradient(
    circle,
    rgba(255, 215, 0, 0.5),
    rgba(255, 215, 0, 0.2)
  );
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

.section-title {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 3rem;
  color: #ffd700;
  font-weight: 700;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.faculty-history {
  padding: 5rem 0;
  position: relative;
}

.history-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  align-items: center;
}

.history-text p {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
}

.history-action {
  margin-top: 2rem;
}

.history-stats {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.latest-recordings {
  padding: 5rem 0;
  position: relative;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.8);
}

.loading p {
  margin-top: 1rem;
  font-size: 1.1rem;
}

.recordings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.recording-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.recording-card:hover {
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}

.recording-image {
  height: 200px;
  overflow: hidden;
  position: relative;
}

.recording-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.recording-card:hover .recording-image img {
  transform: scale(1.1);
}

.recording-placeholder {
  height: 200px;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.4);
  gap: 0.5rem;
}

.recording-placeholder i {
  font-size: 2rem;
}

.recording-placeholder span {
  font-size: 0.9rem;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.recording-card:hover .image-overlay {
  opacity: 1;
}

.image-overlay i {
  font-size: 2rem;
  color: #ffd700;
}

.recording-content {
  padding: 1.5rem;
}

.recording-category {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.recording-category i {
  margin-right: 0.5rem;
}

.recording-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #ffffff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

.recording-excerpt {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.recording-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.recording-date i,
.recording-views i {
  margin-right: 0.5rem;
}

.recording-views {
  display: flex;
  align-items: center;
}

.no-recordings {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.6);
}

.no-recordings i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.3);
}

.section-footer {
  text-align: center;
}

.features {
  padding: 5rem 0;
  position: relative;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
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
  transition: left 0.5s ease;
}

.feature-card:hover::before {
  left: 100%;
}

.feature-card:hover {
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(10deg);
  box-shadow: 0 15px 40px rgba(255, 215, 0, 0.5);
}

.feature-icon i {
  font-size: 2rem;
  color: #1a1a2e;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #ffffff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

.feature-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

/* Custom animation classes for intersection observer */
.animate-in-view {
  animation: slideInFromBottom 0.8s ease-out forwards;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .history-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .history-stats {
    flex-direction: row;
    justify-content: space-around;
  }

  .section-title {
    font-size: 2rem;
  }

  .recordings-grid {
    grid-template-columns: 1fr;
  }

  .recording-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>
