<template>
  <div class="recording-detail bg-darker-gradient particles-bg">
    <div class="container">
      <!-- Loading State -->
      <div v-if="loading" class="loading animate-bounce-in">
        <div class="loading-spinner"></div>
        <p class="loading-dots">Загрузка записи</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state animate-fade-in-up">
        <i class="fas fa-exclamation-triangle animate-float"></i>
        <h3>Ошибка загрузки</h3>
        <p>{{ error }}</p>
        <button @click="fetchRecording" class="btn btn-primary hover-glow">
          Попробовать снова
        </button>
      </div>

      <!-- Recording Content -->
      <div v-else-if="recording" class="recording-content">
        <!-- Header -->
        <div class="recording-header animate-fade-in-up">
          <div class="breadcrumb animate-slide-in-up">
            <router-link to="/recordings" class="breadcrumb-link hover-glow">
              <i class="fas fa-arrow-left"></i>
              Назад к записям
            </router-link>
          </div>

          <h1 class="recording-title animate-glow">{{ recording.title }}</h1>

          <div class="recording-meta animate-fade-in-up animate-stagger-2">
            <div class="meta-item">
              <i class="fas fa-calendar animate-pulse"></i>
              <span>{{ formatDate(recording.created_at) }}</span>
            </div>
            <div class="meta-item" v-if="recording.category">
              <i class="fas fa-tag"></i>
              <span>{{ recording.category.name }}</span>
            </div>
            <div class="meta-item" v-if="recording.user">
              <i class="fas fa-user"></i>
              <span>{{ recording.user.username }}</span>
            </div>
            <div class="meta-item" v-if="recording.views">
              <i class="fas fa-eye"></i>
              <span>{{ recording.views }} просмотров</span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div
            v-if="canEditRecording"
            class="action-buttons animate-fade-in-up animate-stagger-3"
          >
            <button
              @click="editRecording"
              class="btn btn-secondary hover-scale"
            >
              <i class="fas fa-edit"></i>
              Редактировать
            </button>
            <button @click="deleteRecording" class="btn btn-danger hover-glow">
              <i class="fas fa-trash"></i>
              Удалить
            </button>
          </div>
        </div>

        <!-- Media Content -->
        <div class="media-section">
          <!-- Image -->
          <div
            v-if="recording.image_path"
            class="image-container animate-scale-in"
          >
            <img
              :src="getImageUrl(recording.image_path)"
              :alt="recording.title"
              @error="handleImageError"
              class="recording-image hover-scale"
            />
          </div>

          <!-- Video -->
          <div
            v-if="recording.video_path"
            class="video-container animate-scale-in animate-stagger-2"
          >
            <video
              :src="getVideoUrl(recording.video_path)"
              controls
              preload="metadata"
              class="recording-video"
              @error="handleVideoError"
            >
              Ваш браузер не поддерживает воспроизведение видео.
            </video>
          </div>
        </div>

        <!-- Content -->
        <div class="content-section animate-fade-in-up animate-stagger-3">
          <div
            class="content-text"
            v-html="formatContent(recording.content)"
          ></div>
        </div>

        <!-- Tags -->
        <div
          v-if="recording.tags && recording.tags.length > 0"
          class="tags-section animate-slide-in-up animate-stagger-4"
        >
          <h3>Теги</h3>
          <div class="tags-list">
            <span
              v-for="(tag, index) in recording.tags"
              :key="tag.id"
              class="tag hover-scale animate-fade-in-up"
              :class="`animate-stagger-${Math.min(index + 1, 5)}`"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>

        <!-- Related Recordings -->
        <div
          v-if="relatedRecordings.length > 0"
          class="related-section animate-fade-in-up animate-stagger-5"
        >
          <h3>Похожие записи</h3>
          <div class="related-grid">
            <div
              v-for="(related, index) in relatedRecordings"
              :key="related.id"
              class="related-card hover-lift animate-fade-in-up"
              :class="`animate-stagger-${index + 1}`"
              @click="viewRecording(related.id)"
            >
              <div class="related-image" v-if="related.image_path">
                <img
                  :src="getImageUrl(related.image_path)"
                  :alt="related.title"
                />
              </div>
              <div v-else class="related-placeholder">
                <i class="fas fa-image"></i>
              </div>
              <div class="related-content">
                <h4>{{ related.title }}</h4>
                <p>{{ truncateText(related.content, 80) }}</p>
                <span class="related-date">{{
                  formatDate(related.created_at)
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="modal-overlay animate-fade-in-up"
      @click="showDeleteModal = false"
    >
      <div class="modal animate-zoom-in" @click.stop>
        <div class="modal-header">
          <h3 class="animate-glow">Подтверждение удаления</h3>
          <button
            @click="showDeleteModal = false"
            class="modal-close hover-scale"
          >
            <i class="fas fa-times animate-rotate-in"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>Вы уверены, что хотите удалить эту запись?</p>
          <p class="warning">Это действие нельзя отменить.</p>
        </div>
        <div class="modal-footer">
          <button
            @click="showDeleteModal = false"
            class="btn btn-secondary hover-scale"
          >
            Отмена
          </button>
          <button @click="confirmDelete" class="btn btn-danger hover-glow">
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
      error: null,
      showDeleteModal: false
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'isModerator']),
    ...mapState(['user']),
    canEditRecording() {
      if (!this.isAuthenticated || !this.recording) return false
      if (this.isAdmin) return true
      if (this.isModerator && this.recording.user_id === this.user.id)
        return true
      return false
    }
  },
  async created() {
    await this.fetchRecording()
    await this.fetchRelatedRecordings()
  },
  methods: {
    async fetchRecording() {
      this.loading = true
      this.error = null

      try {
        const id = this.$route.params.id
        this.recording = await this.$store.dispatch('fetchRecording', id)
      } catch (error) {
        this.error =
          error.response?.data?.message || 'Не удалось загрузить запись'
        console.error('Error fetching recording:', error)
      } finally {
        this.loading = false
      }
    },
    async fetchRelatedRecordings() {
      try {
        const id = this.$route.params.id
        this.relatedRecordings = await this.$store.dispatch(
          'fetchRelatedRecordings',
          {
            recordingId: id,
            limit: 3
          }
        )
      } catch (error) {
        console.error('Error fetching related recordings:', error)
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
    getVideoUrl(videoPath) {
      if (!videoPath) return null
      if (videoPath.startsWith('http')) return videoPath
      if (videoPath.startsWith('/uploads/')) {
        return `http://localhost:5000${videoPath}`
      }
      return `http://localhost:5000/uploads/${videoPath}`
    },
    handleImageError(event) {
      console.error('Image failed to load:', event.target.src)
      event.target.style.display = 'none'
    },
    handleVideoError(event) {
      console.error('Video failed to load:', event.target.src)
      event.target.style.display = 'none'
    },
    formatContent(content) {
      if (!content) return ''
      // Convert line breaks to HTML
      return content.replace(/\n/g, '<br>')
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
    },
    truncateText(text, length) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    },
    viewRecording(id) {
      this.$router.push(`/recordings/${id}`)
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
    }
  }
}
</script>

<style scoped>
.recording-detail {
  padding: 2rem 0;
  min-height: 100vh;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
}

.loading p {
  margin-top: 1rem;
  font-size: 1.1rem;
}

.error-state {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
}

.error-state i {
  font-size: 4rem;
  color: #ff6b6b;
  margin-bottom: 1rem;
}

.error-state h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #ffffff;
}

.recording-header {
  margin-bottom: 3rem;
}

.breadcrumb {
  margin-bottom: 1rem;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.breadcrumb-link:hover {
  color: #ffd700;
}

.breadcrumb-link i {
  margin-right: 0.5rem;
}

.recording-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.recording-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 2rem;
}

.meta-item {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.meta-item i {
  margin-right: 0.5rem;
  color: #ffd700;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.media-section {
  margin-bottom: 3rem;
}

.image-container,
.video-container {
  margin-bottom: 2rem;
}

.recording-image {
  width: 100%;
  max-width: 800px;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  transition: transform 0.3s ease;
}

.recording-video {
  width: 100%;
  max-width: 800px;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.content-section {
  margin-bottom: 3rem;
}

.content-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(0, 0, 0, 0.3);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.tags-section {
  margin-bottom: 3rem;
}

.tags-section h3 {
  font-size: 1.5rem;
  color: #ffd700;
  margin-bottom: 1rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
}

.tag:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: scale(1.05);
}

.related-section h3 {
  font-size: 1.5rem;
  color: #ffd700;
  margin-bottom: 2rem;
  text-align: center;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.related-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.related-card:hover {
  border-color: rgba(255, 215, 0, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
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

.related-placeholder {
  height: 150px;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.4);
}

.related-placeholder i {
  font-size: 2rem;
}

.related-content {
  padding: 1.5rem;
}

.related-content h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.related-content p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.related-date {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
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
  backdrop-filter: blur(10px);
}

.modal {
  background: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
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
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.modal-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.modal-close:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
  transform: rotate(90deg);
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
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.3);
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
    gap: 1rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .related-grid {
    grid-template-columns: 1fr;
  }

  .modal {
    margin: 1rem;
  }

  .modal-footer {
    flex-direction: column;
  }
}
</style>
