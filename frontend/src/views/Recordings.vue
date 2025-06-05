<template>
  <div class="recordings bg-darker-gradient particles-bg">
    <div class="container">
      <!-- Header Section -->
      <div class="recordings-header animate-fade-in-up" data-aos="fade-up">
        <h1 class="animate-glow">Записи факультета</h1>
        <p class="animate-fade-in-up animate-stagger-2">Просмотрите все записи и материалы факультета</p>
      </div>

      <!-- Filters Section -->
      <div class="filters-section animate-slide-in-up" data-aos="fade-up" data-aos-delay="100">
        <div class="filters-card hover-glow">
          <div class="search-box animate-scale-in">
            <i class="fas fa-search animate-pulse"></i>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Поиск записей..."
              class="search-input animate-shimmer"
              @input="debouncedSearch"
            >
          </div>
          
          <div class="filter-controls">
            <select v-model="filters.category" class="filter-select hover-lift animate-fade-in-left animate-stagger-1" @change="applyFilters">
              <option value="">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            
            <select v-model="filters.sortBy" class="filter-select hover-lift animate-fade-in-left animate-stagger-2" @change="applyFilters">
              <option value="created_at">По дате создания</option>
              <option value="title">По названию</option>
              <option value="updated_at">По дате обновления</option>
            </select>
            
            <select v-model="filters.sortOrder" class="filter-select hover-lift animate-fade-in-left animate-stagger-3" @change="applyFilters">
              <option value="desc">По убыванию</option>
              <option value="asc">По возрастанию</option>
            </select>
            
            <button @click="clearFilters" class="btn btn-secondary clear-filters hover-scale animate-bounce-in">
              <i class="fas fa-times animate-rotate-in"></i>
              Очистить
            </button>
          </div>
        </div>
      </div>

      <!-- Add New Recording Button -->
      <div v-if="isModerator" class="add-recording-section animate-zoom-in" data-aos="fade-up" data-aos-delay="200">
        <router-link to="/recordings/new" class="btn btn-primary hover-glow animate-pulse">
          <i class="fas fa-plus animate-rotate-in"></i>
          Добавить запись
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading animate-bounce-in">
        <div class="loading-spinner"></div>
        <p class="loading-dots">Загрузка записей</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state animate-fade-in-up">
        <i class="fas fa-exclamation-triangle animate-float"></i>
        <h3 class="animate-fade-in-up animate-stagger-2">Ошибка загрузки</h3>
        <p class="animate-fade-in-up animate-stagger-3">{{ error }}</p>
        <button @click="fetchRecordings" class="btn btn-primary hover-lift animate-bounce-in">
          Попробовать снова
        </button>
      </div>

      <!-- Recordings Grid -->
      <div v-else-if="recordings.length > 0" class="recordings-grid">
        <div
          v-for="(recording, index) in recordings"
          :key="recording.id"
          class="recording-card hover-lift animate-fade-in-up"
          :class="`animate-stagger-${Math.min(index + 1, 5)}`"
          data-aos="fade-up"
          :data-aos-delay="index * 50"
          @click="viewRecording(recording.id)"
        >
          <div class="recording-image" v-if="recording.image_path">
            <img 
              :src="getImageUrl(recording.image_path)" 
              :alt="recording.title"
              @error="handleImageError"
              loading="lazy"
              class="animate-scale-in"
            >
            <div class="recording-overlay animate-fade-in-up">
              <i class="fas fa-play animate-pulse"></i>
            </div>
          </div>
          <div v-else class="recording-placeholder animate-shimmer">
            <i class="fas fa-image animate-float"></i>
            <span>Нет изображения</span>
          </div>
          
          <div class="recording-content">
            <div class="recording-meta animate-fade-in-up">
              <span v-if="recording.category" class="recording-category animate-slide-in-up">
                <i class="fas fa-tag"></i>
                {{ recording.category.name }}
              </span>
              <span class="recording-date animate-fade-in-right">
                <i class="fas fa-calendar"></i>
                {{ formatDate(recording.created_at) }}
              </span>
            </div>
            
            <h3 class="recording-title animate-fade-in-left">{{ recording.title }}</h3>
            <p class="recording-excerpt animate-fade-in-right">{{ truncateText(recording.content, 120) }}</p>
            
            <div class="recording-tags animate-slide-in-up" v-if="recording.tags && recording.tags.length > 0">
              <span
                v-for="(tag, tagIndex) in recording.tags.slice(0, 3)"
                :key="tag.id"
                class="tag hover-scale"
                :class="`animate-fade-in-up animate-stagger-${tagIndex + 1}`"
              >
                {{ tag.name }}
              </span>
              <span v-if="recording.tags.length > 3" class="tag-more animate-bounce-in">
                +{{ recording.tags.length - 3 }}
              </span>
            </div>

            <div class="recording-footer animate-fade-in-up">
              <div class="recording-stats">
                <span v-if="recording.views" class="recording-views animate-fade-in-left">
                  <i class="fas fa-eye"></i>
                  {{ recording.views }}
                </span>
                <span v-if="recording.video_path" class="has-video animate-fade-in-right">
                  <i class="fas fa-video animate-pulse"></i>
                  Видео
                </span>
              </div>
              
              <div class="recording-actions" v-if="canEditRecording(recording)">
                <button
                  @click.stop="editRecording(recording.id)"
                  class="action-btn edit-btn hover-scale animate-rotate-in"
                  title="Редактировать"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button
                  @click.stop="deleteRecording(recording)"
                  class="action-btn delete-btn hover-scale animate-rotate-in animate-stagger-2"
                  title="Удалить"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else class="no-results animate-bounce-in">
        <i class="fas fa-search animate-float"></i>
        <h3 class="animate-fade-in-up animate-stagger-2">Записи не найдены</h3>
        <p class="animate-fade-in-up animate-stagger-3">Попробуйте изменить параметры поиска или фильтры</p>
        <button @click="clearFilters" class="btn btn-primary hover-glow animate-pulse">
          Сбросить фильтры
        </button>
      </div>

            <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination animate-slide-in-up" data-aos="fade-up">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="pagination-btn hover-scale animate-fade-in-left"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        
        <span
          v-for="page in visiblePages"
          :key="page"
          @click="changePage(page)"
          class="pagination-number hover-glow animate-zoom-in"
          :class="{ active: page === currentPage, [`animate-stagger-${page}`]: page <= 5 }"
        >
          {{ page }}
        </span>
        
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="pagination-btn hover-scale animate-fade-in-right"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay animate-fade-in-up" @click="showDeleteModal = false">
      <div class="modal animate-zoom-in" @click.stop>
        <div class="modal-header animate-slide-in-up">
          <h3 class="animate-glow">Подтверждение удаления</h3>
          <button @click="showDeleteModal = false" class="modal-close hover-scale animate-rotate-in">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body animate-fade-in-up animate-stagger-2">
          <p class="animate-fade-in-left">Вы уверены, что хотите удалить запись "{{ recordingToDelete?.title }}"?</p>
          <p class="warning animate-fade-in-right animate-stagger-3">Это действие нельзя отменить.</p>
        </div>
        <div class="modal-footer animate-slide-in-up animate-stagger-4">
          <button @click="showDeleteModal = false" class="btn btn-secondary hover-scale">
            Отмена
          </button>
          <button @click="confirmDelete" class="btn btn-danger hover-glow animate-pulse">
            <i class="fas fa-trash animate-rotate-in"></i>
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import { debounce } from 'lodash'

export default {
  name: 'Recordings',
  data() {
    return {
      filters: {
        search: '',
        category: '',
        sortBy: 'created_at',
        sortOrder: 'desc'
      },
      currentPage: 1,
      totalPages: 1,
      showDeleteModal: false,
      recordingToDelete: null
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'isModerator']),
    ...mapState(['user', 'recordings', 'categories', 'loading', 'error']),
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, this.currentPage + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    },
    debouncedSearch() {
      return debounce(this.applyFilters, 500)
    }
  },
  async created() {
    await this.fetchCategories()
    await this.fetchRecordings()
  },
  mounted() {
    this.initializeAnimations()
  },
  methods: {
    initializeAnimations() {
      // Add intersection observer for staggered animations
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in-view')
            // Add staggered delay for grid items
            const index = Array.from(entry.target.parentNode.children).indexOf(entry.target)
            entry.target.style.animationDelay = `${index * 0.1}s`
          }
        })
      }, observerOptions)

      // Observe recording cards
      setTimeout(() => {
        document.querySelectorAll('.recording-card').forEach(el => {
          observer.observe(el)
        })
      }, 100)
    },
    async fetchRecordings() {
      try {
        const params = {
          page: this.currentPage,
          search: this.filters.search,
          category: this.filters.category,
          sort_by: this.filters.sortBy,
          sort_order: this.filters.sortOrder
        }
        
        const response = await this.$store.dispatch('fetchRecordings', params)
        this.totalPages = response.totalPages || Math.ceil((response.total || this.recordings.length) / 10)
        
        // Re-initialize animations after data load
        this.$nextTick(() => {
          this.initializeAnimations()
        })
      } catch (error) {
        console.error('Error fetching recordings:', error)
      }
    },
    async fetchCategories() {
      try {
        await this.$store.dispatch('fetchCategories')
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },
    async applyFilters() {
      this.currentPage = 1
      await this.fetchRecordings()
    },
    async changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        await this.fetchRecordings()
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    clearFilters() {
      this.filters = {
        search: '',
        category: '',
        sortBy: 'created_at',
        sortOrder: 'desc'
      }
      this.applyFilters()
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
        if (placeholder && placeholder.classList.contains('recording-placeholder')) {
          placeholder.style.display = 'flex'
        }
      }
    },
    viewRecording(id) {
      this.$router.push(`/recordings/${id}`)
    },
    editRecording(id) {
      this.$router.push(`/recordings/${id}/edit`)
    },
    deleteRecording(recording) {
      this.recordingToDelete = recording
      this.showDeleteModal = true
    },
    async confirmDelete() {
      try {
        await this.$store.dispatch('deleteRecording', this.recordingToDelete.id)
        this.showDeleteModal = false
        this.recordingToDelete = null
        await this.fetchRecordings()
      } catch (error) {
        console.error('Error deleting recording:', error)
      }
    },
    canEditRecording(recording) {
      if (!this.isAuthenticated) return false
      if (this.isAdmin) return true
      if (this.isModerator && recording.user_id === this.user.id) return true
      return false
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
.recordings {
  padding: 2rem 0;
  min-height: 100vh;
  position: relative;
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
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}

.error-state p {
  margin-bottom: 2rem;
  line-height: 1.6;
}

.recordings-header {
  text-align: center;
  margin-bottom: 3rem;
}

.recordings-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}

.recordings-header p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.filters-section {
  margin-bottom: 2rem;
}

.filters-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.filters-card:hover {
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.search-box {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 215, 0, 0.6);
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
}

.search-input:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
  background: rgba(0, 0, 0, 0.5);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-select {
  padding: 0.75rem 1rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9rem;
  min-width: 150px;
  transition: all 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #ffd700;
  background: rgba(0, 0, 0, 0.5);
}

.filter-select option {
  background: #0a0a0a;
  color: #ffffff;
}

.clear-filters {
  margin-left: auto;
}

.add-recording-section {
  text-align: center;
  margin-bottom: 2rem;
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
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.recording-card {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.recording-card:hover {
  border-color: rgba(255, 215, 0, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
}

.recording-image {
  position: relative;
  height: 200px;
  overflow: hidden;
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
  background: rgba(0, 0, 0, 0.3);
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

.recording-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.recording-card:hover .recording-overlay {
  opacity: 1;
}

.recording-overlay i {
  font-size: 3rem;
  color: #ffd700;
}

.recording-content {
  padding: 1.5rem;
}

.recording-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.5rem;
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
  transition: all 0.3s ease;
}

.recording-category:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: scale(1.05);
}

.recording-category i {
  margin-right: 0.5rem;
}

.recording-date {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.recording-date i {
  margin-right: 0.5rem;
}

.recording-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #ffffff;
  line-height: 1.4;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

.recording-excerpt {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.recording-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tag:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border-color: rgba(255, 215, 0, 0.3);
}

.tag-more {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.recording-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.recording-stats {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.recording-views,
.has-video {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.recording-views i,
.has-video i {
  margin-right: 0.5rem;
}

.has-video {
  color: #ffd700;
}

.recording-actions {
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.recording-card:hover .recording-actions {
  opacity: 1;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.edit-btn {
  background: rgba(52, 152, 219, 0.8);
  color: #ffffff;
}

.edit-btn:hover {
  background: rgba(52, 152, 219, 1);
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
}

.delete-btn {
  background: rgba(231, 76, 60, 0.8);
  color: #ffffff;
}

.delete-btn:hover {
  background: rgba(231, 76, 60, 1);
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.6);
}

.no-results i {
  font-size: 4rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.3);
}

.no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.8);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.pagination-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.4);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
  color: #ffd700;
  transform: scale(1.1);
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination-number {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.4);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.pagination-number:hover {
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
  color: #ffd700;
  transform: scale(1.1);
}

.pagination-number.active {
  background: #ffd700;
  border-color: #ffd700;
  color: #0a0a0a;
  font-weight: 600;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
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

/* Custom animation for intersection observer */
.animate-in-view {
  animation: slideInFromBottom 0.8s ease-out forwards;
}

@media (max-width: 768px) {
  .recordings-header h1 {
    font-size: 2rem;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-select {
    min-width: auto;
  }
  
  .clear-filters {
    margin-left: 0;
  }
  
  .recordings-grid {
    grid-template-columns: 1fr;
  }
  
  .recording-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .recording-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .pagination {
    flex-wrap: wrap;
  }
  
  .modal {
    margin: 1rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}
</style>

