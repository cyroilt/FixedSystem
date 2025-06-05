<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content" data-aos="fade-up">
          <h1 class="hero-title animate__animated animate__fadeInUp">
            Добро пожаловать в Faculty Portal
          </h1>
          <p class="hero-subtitle animate__animated animate__fadeInUp animate__delay-1s">
            Современная система управления записями факультета с удобным интерфейсом
          </p>
          <div class="hero-buttons animate__animated animate__fadeInUp animate__delay-2s">
            <router-link to="/recordings" class="btn btn-primary">
              <i class="fas fa-video"></i>
              Просмотреть записи
            </router-link>
            <router-link v-if="!isAuthenticated" to="/register" class="btn btn-secondary">
              <i class="fas fa-user-plus"></i>
              Присоединиться
            </router-link>
          </div>
        </div>
      </div>
      <div class="hero-background">
        <div class="floating-shapes">
          <div class="shape shape-1"></div>
          <div class="shape shape-2"></div>
          <div class="shape shape-3"></div>
        </div>
      </div>
    </section>

    <!-- Faculty History Section -->
    <section class="faculty-history">
      <div class="container">
        <h2 class="section-title" data-aos="fade-up">История факультета</h2>
        <div class="history-content" data-aos="fade-up" data-aos-delay="200">
          <div class="history-text">
            <p>
              Наш факультет был основан в 1950 году и с тех пор является ведущим 
              образовательным учреждением в области высшего образования. За более 
              чем 70 лет работы мы подготовили тысячи высококвалифицированных специалистов.
            </p>
            <p>
              Сегодня факультет продолжает развиваться, внедряя современные технологии 
              и методы обучения, поддерживая высокие стандарты качества образования.
            </p>
          </div>
          <div class="history-stats">
            <div class="stat-item" data-aos="zoom-in" data-aos-delay="300">
              <div class="stat-number">70+</div>
              <div class="stat-label">Лет опыта</div>
            </div>
            <div class="stat-item" data-aos="zoom-in" data-aos-delay="400">
              <div class="stat-number">5000+</div>
              <div class="stat-label">Выпускников</div>
            </div>
            <div class="stat-item" data-aos="zoom-in" data-aos-delay="500">
              <div class="stat-number">50+</div>
              <div class="stat-label">Преподавателей</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Latest Recordings Section -->
    <section class="latest-recordings">
      <div class="container">
        <h2 class="section-title" data-aos="fade-up">Последние записи</h2>
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Загрузка записей...</p>
        </div>
        <div v-else-if="latestRecordings.length > 0" class="recordings-grid">
          <div 
            v-for="(recording, index) in latestRecordings" 
            :key="recording.id"
            class="recording-card"
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
              >
              <div class="image-overlay">
                <i class="fas fa-eye"></i>
              </div>
            </div>
            <div class="recording-content">
              <div class="recording-category" v-if="recording.category">
                <i class="fas fa-tag"></i>
                {{ recording.category.name }}
              </div>
              <h3 class="recording-title">{{ recording.title }}</h3>
              <p class="recording-excerpt">{{ truncateText(recording.content, 100) }}</p>
              <div class="recording-meta">
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
        <div v-else class="no-recordings">
          <i class="fas fa-video"></i>
          <p>Пока нет записей</p>
        </div>
        <div class="section-footer" data-aos="fade-up">
          <router-link to="/recordings" class="btn btn-primary">
            <i class="fas fa-arrow-right"></i>
            Посмотреть все записи
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <h2 class="section-title" data-aos="fade-up">Возможности портала</h2>
        <div class="features-grid">
          <div class="feature-card" data-aos="fade-up" data-aos-delay="100">
            <div class="feature-icon">
              <i class="fas fa-video"></i>
            </div>
            <h3>Мультимедийные записи</h3>
            <p>Поддержка текста, изображений и видео в одной записи</p>
          </div>
          <div class="feature-card" data-aos="fade-up" data-aos-delay="200">
            <div class="feature-icon">
              <i class="fas fa-tags"></i>
            </div>
            <h3>Система категорий</h3>
            <p>Удобная организация контента по категориям и тегам</p>
          </div>
          <div class="feature-card" data-aos="fade-up" data-aos-delay="300">
            <div class="feature-icon">
              <i class="fas fa-users"></i>
            </div>
            <h3>Управление пользователями</h3>
            <p>Система ролей для администраторов и модераторов</p>
          </div>
          <div class="feature-card" data-aos="fade-up" data-aos-delay="400">
            <div class="feature-icon">
              <i class="fas fa-mobile-alt"></i>
            </div>
            <h3>Адаптивный дизайн</h3>
            <p>Отлично работает на всех устройствах</p>
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
    ...mapGetters(['isAuthenticated', 'getFileUrl'])
  },
  async created() {
    await this.fetchLatestRecordings()
  },
  async mounted() {
    await this.fetchLatestRecordings()
  },
  methods: {
    async fetchLatestRecordings() {
      this.loading = true
      try {
        this.latestRecordings = await this.$store.dispatch('fetchLatestRecordings')
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
      // You can set a default image here
      // event.target.src = '/path/to/default-image.jpg'
      event.target.style.display = 'none'
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
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  background: rgba(255, 215, 0, 0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 100px;
  height: 100px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 10%;
  animation-delay: 2s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.section-title {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 3rem;
  color: #ffd700;
  font-weight: 700;
}

.faculty-history {
  padding: 5rem 0;
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

.history-stats {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.latest-recordings {
  padding: 5rem 0;
}

.recordings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.recording-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
}

.recording-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
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

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
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
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
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
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

.feature-icon i {
  font-size: 2rem;
  color: #1e3c72;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #ffffff;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
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
