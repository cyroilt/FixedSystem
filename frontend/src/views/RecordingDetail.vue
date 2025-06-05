<template>
  <div class="recording-detail">
    <div class="container">
      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка записи...</p>
      </div>

      <!-- Recording Content -->
      <div v-else-if="recording" class="recording-content">
        <!-- Header -->
        <div class="recording-header" data-aos="fade-up">
          <div class="breadcrumb">
            <router-link to="/" class="breadcrumb-link">Главная</router-link>
            <i class="fas fa-chevron-right"></i>
            <router-link to="/recordings" class="breadcrumb-link">Записи</router-link>
            <i class="fas fa-chevron-right"></i>
            <span class="breadcrumb-current">{{ recording.title }}</span>
          </div>
          
          <div class="recording-meta">
            <div class="meta-left">
                            <span v-if="recording.category" class="recording-category">
                <i class="fas fa-tag"></i>
                {{ recording.category.name }}
              </span>
              <span class="recording-date">
                <i class="fas fa-calendar"></i>
                {{ formatDate(recording.created_at) }}
              </span>
              <span v-if="recording.updated_at !== recording.created_at" class="recording-updated">
                <i class="fas fa-edit"></i>
                Обновлено {{ formatDate(recording.updated_at) }}
              </span>
            </div>
            
            <div class="meta-right" v-if="canEditRecording">
              <button @click="editRecording" class="btn btn-secondary">
                <i class="fas fa-edit"></i>
                Редактировать
              </button>
              <button @click="deleteRecording" class="btn btn-danger">
                <i class="fas fa-trash"></i>
                Удалить
              </button>
            </div>
          </div>
          
          <h1 class="recording-title">{{ recording.title }}</h1>
        </div>

        <!-- Main Image -->
        <div v-if="recording.image_path" class="recording-image" data-aos="fade-up" data-aos-delay="100">
          <img :src="recording.image_path" :alt="recording.title" @click="openImageModal">
          <div class="image-overlay">
            <i class="fas fa-expand"></i>
          </div>
        </div>

        <!-- Content -->
        <div class="recording-body" data-aos="fade-up" data-aos-delay="200">
          <div class="content-text" v-html="formattedContent"></div>
        </div>

        <!-- Video Section -->
        <div v-if="recording.video_path" class="recording-video" data-aos="fade-up" data-aos-delay="300">
          <h3>Видео</h3>
          <div class="video-container">
            <video :src="recording.video_path" controls preload="metadata">
              Ваш браузер не поддерживает воспроизведение видео.
            </video>
          </div>
        </div>

        <!-- Tags -->
        <div v-if="recording.tags && recording.tags.length > 0" class="recording-tags" data-aos="fade-up" data-aos-delay="400">
          <h3>Теги</h3>
          <div class="tags-list">
            <span v-for="tag in recording.tags" :key="tag.id" class="tag">
              <i class="fas fa-hashtag"></i>
              {{ tag.name }}
            </span>
          </div>
        </div>

        <!-- Author Info -->
        <div v-if="recording.user" class="author-info" data-aos="fade-up" data-aos-delay="500">
          <div class="author-card">
            <div class="author-avatar">
              <i class="fas fa-user"></i>
            </div>
            <div class="author-details">
              <h4>Автор</h4>
              <p class="author-name">{{ recording.user.username }}</p>
              <p class="author-role">{{ getUserRole(recording.user) }}</p>
            </div>
          </div>
        </div>

        <!-- Related Recordings -->
        <div v-if="relatedRecordings.length > 0" class="related-recordings" data-aos="fade-up" data-aos-delay="600">
          <h3>Похожие записи</h3>
          <div class="related-grid">
            <div
              v-for="related in relatedRecordings"
              :key="related.id"
              class="related-card"
              @click="viewRecording(related.id)"
            >
              <div class="related-image" v-if="related.image_path">
                <img :src="related.image_path" :alt="related.title">
              </div>
              <div class="related-content">
                <h4>{{ related.title }}</h4>
                <p>{{ truncateText(related.content, 80) }}</p>
                <span class="related-date">{{ formatDate(related.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Not Found -->
      <div v-else class="not-found">
        <i class="fas fa-exclamation-triangle"></i>
        <h2>Запись не найдена</h2>
        <p>Возможно, запись была удалена или у вас нет прав для её просмотра.</p>
        <router-link to="/recordings" class="btn btn-primary">
          <i class="fas fa-arrow-left"></i>
          Вернуться к записям
        </router-link>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="modal-overlay" @click="closeImageModal">
      <div class="image-modal" @click.stop>
        <button @click="closeImageModal" class="modal-close">
          <i class="fas fa-times"></i>
        </button>
        <img :src="recording.image_path" :alt="recording.title">
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Подтверждение удаления</h3>
          <button @click="showDeleteModal = false" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>Вы уверены, что хотите удалить запись "{{ recording.title }}"?</p>
          <p class="warning">Это действие нельзя отменить.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn btn-secondary">
            Отмена
          </button>
          <button @click="confirmDelete" class="btn btn-danger">
            <i class="fas fa-trash"></i>
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  name: 'RecordingDetail',
  data() {
    return {
      recording: null,
      relatedRecordings: [],
      loading: false,
      showImageModal: false,
      showDeleteModal: false
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'isModerator']),
    ...mapState(['user']),
    canEditRecording() {
      if (!this.isAuthenticated || !this.recording) return false
      if (this.isAdmin) return true
      if (this.isModerator && this.recording.user_id === this.user.id) return true
      return false
    },
    formattedContent() {
      if (!this.recording.content) return ''
      return this.recording.content.replace(/\n/g, '<br>')
    }
  },
  async created() {
    await this.fetchRecording()
    await this.fetchRelatedRecordings()
  },
  watch: {
    '$route.params.id': {
      handler() {
        this.fetchRecording()
        this.fetchRelatedRecordings()
      },
      immediate: false
    }
  },
  methods: {
    async fetchRecording() {
      this.loading = true
      try {
        const id = this.$route.params.id
        this.recording = await this.$store.dispatch('fetchRecording', id)
      } catch (error) {
        console.error('Error fetching recording:', error)
        this.recording = null
      } finally {
        this.loading = false
      }
    },
    async fetchRelatedRecordings() {
      if (!this.recording) return
      
      try {
        const params = {
          category: this.recording.category?.id,
          exclude: this.recording.id,
          limit: 3
        }
        this.relatedRecordings = await this.$store.dispatch('fetchRelatedRecordings', params)
      } catch (error) {
        console.error('Error fetching related recordings:', error)
      }
    },
    editRecording() {
      this.$router.push(`/recordings/${this.recording.id}/edit`)
    },
    deleteRecording() {
      this.showDeleteModal = true
    },
    async confirmDelete() {
      try {
        await this.$store.dispatch('deleteRecording', this.recording.id)
        this.showDeleteModal = false
        this.$router.push('/recordings')
      } catch (error) {
        console.error('Error deleting recording:', error)
      }
    },
    viewRecording(id) {
      this.$router.push(`/recordings/${id}`)
    },
    openImageModal() {
      this.showImageModal = true
    },
    closeImageModal() {
      this.showImageModal = false
    },
    getUserRole(user) {
      if (user.role === 'admin') return 'Администратор'
      if (user.role === 'moderator') return 'Модератор'
      return 'Пользователь'
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
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.recording-detail {
  padding: 2rem 0;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.breadcrumb-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.3s ease;
}

.breadcrumb-link:hover {
  color: #ffd700;
}

.breadcrumb i {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
}

.breadcrumb-current {
  color: #ffd700;
  font-weight: 500;
}

.recording-header {
  margin-bottom: 3rem;
}

.recording-meta {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.meta-left {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.meta-right {
  display: flex;
  gap: 0.5rem;
}

.recording-category {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 600;
}

.recording-category i {
  margin-right: 0.5rem;
}

.recording-date,
.recording-updated {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.recording-date i,
.recording-updated i {
  margin-right: 0.5rem;
}

.recording-title {
  font-size: 3rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.2;
  margin: 0;
}

.recording-image {
  position: relative;
  margin-bottom: 3rem;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  max-height: 500px;
}

.recording-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.recording-image:hover img {
  transform: scale(1.05);
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

.recording-image:hover .image-overlay {
  opacity: 1;
}

.image-overlay i {
  font-size: 2rem;
  color: #ffd700;
}

.recording-body {
  margin-bottom: 3rem;
}

.content-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.9);
}

.content-text ::v-deep p {
  margin-bottom: 1.5rem;
}

.recording-video {
  margin-bottom: 3rem;
}

.recording-video h3 {
  font-size: 1.5rem;
  color: #ffd700;
  margin-bottom: 1rem;
}

.video-container {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  background: #000;
}

.video-container video {
  width: 100%;
  height: auto;
  max-height: 500px;
}

.recording-tags {
  margin-bottom: 3rem;
}

.recording-tags h3 {
  font-size: 1.5rem;
  color: #ffd700;
  margin-bottom: 1rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tag:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.tag i {
  margin-right: 0.5rem;
  font-size: 0.8rem;
}

.author-info {
  margin-bottom: 3rem;
}

.author-card {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.author-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1.5rem;
  flex-shrink: 0;
}

.author-avatar i {
  font-size: 2rem;
  color: #1e3c72;
}

.author-details h4 {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.author-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.author-role {
  color: #ffd700;
  font-size: 0.9rem;
  font-weight: 500;
}

.related-recordings h3 {
  font-size: 1.5rem;
  color: #ffd700;
  margin-bottom: 2rem;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.related-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
}

.related-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.related-image {
  height: 150px;
  overflow: hidden;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.related-card:hover .related-image img {
  transform: scale(1.1);
}

.related-content {
  padding: 1.5rem;
}

.related-content h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.related-content p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.related-date {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.not-found {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
}

.not-found i {
  font-size: 4rem;
  color: #ffd700;
  margin-bottom: 2rem;
}

.not-found h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #ffffff;
}

.not-found p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.image-modal {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-modal img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.modal {
  background: rgba(30, 60, 114, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  color: #ffd700;
  margin: 0;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: #ffffff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 1001;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: scale(1.1);
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1rem;
  line-height: 1.6;
}

.warning {
  color: #ff6b6b !important;
  font-weight: 500;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .recording-title {
    font-size: 2rem;
  }
  
  .recording-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .meta-left {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .meta-right {
    width: 100%;
    justify-content: flex-start;
  }
  
  .author-card {
    flex-direction: column;
    text-align: center;
  }
  
  .author-avatar {
    margin-right: 0;
    margin-bottom: 1rem;
  }
  
  .related-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}
</style>

