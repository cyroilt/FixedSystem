<template>
  <div class="recordings">
    <div class="container">
      <!-- Header Section -->
      <div class="recordings-header" data-aos="fade-up">
        <h1>Записи факультета</h1>
        <p>Просмотрите все записи и материалы факультета</p>
      </div>

      <!-- Filters Section -->
      <div class="filters-section" data-aos="fade-up" data-aos-delay="100">
        <div class="filters-card">
          <div class="search-box">
            <i class="fas fa-search"></i>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Поиск записей..."
              class="search-input"
              @input="debouncedSearch"
            >
          </div>
          
          <div class="filter-controls">
            <select v-model="filters.category" class="filter-select" @change="applyFilters">
              <option value="">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            
            <select v-model="filters.sortBy" class="filter-select" @change="applyFilters">
              <option value="created_at">По дате создания</option>
              <option value="title">По названию</option>
              <option value="updated_at">По дате обновления</option>
            </select>
            
            <select v-model="filters.sortOrder" class="filter-select" @change="applyFilters">
              <option value="desc">По убыванию</option>
              <option value="asc">По возрастанию</option>
            </select>
            
            <button @click="clearFilters" class="btn btn-secondary clear-filters">
              <i class="fas fa-times"></i>
              Очистить
            </button>
          </div>
        </div>
      </div>

      <!-- Add New Recording Button -->
      <div v-if="isModerator" class="add-recording-section" data-aos="fade-up" data-aos-delay="200">
        <router-link to="/recordings/new" class="btn btn-primary">
          <i class="fas fa-plus"></i>
          Добавить запись
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка записей...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <i class="fas fa-exclamation-triangle"></i>
        <h3>Ошибка загрузки</h3>
        <p>{{ error }}</p>
        <button @click="fetchRecordings" class="btn btn-primary">
          Попробовать снова
        </button>
      </div>

      <!-- Recordings Grid -->
      <div v-else-if="recordings.length > 0" class="recordings-grid">
        <div
          v-for="(recording, index) in recordings"
          :key="recording.id"
          class="recording-card"
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
            >
            <div class="recording-overlay">
              <i class="fas fa-play"></i>
            </div>
          </div>
          <div v-else class="recording-placeholder">
            <i class="fas fa-image"></i>
            <span>Нет изображения</span>
          </div>
          
          <div class="recording-content">
            <div class="recording-meta">
              <span v-if="recording.category" class="recording-category">
                <i class="fas fa-tag"></i>
                {{ recording.category.name }}
              </span>
              <span class="recording-date">
                <i class="fas fa-calendar"></i>
                {{ formatDate(recording.created_at) }}
              </span>
            </div>
            
            <h3 class="recording-title">{{ recording.title }}</h3>
            <p class="recording-excerpt">{{ truncateText(recording.content, 120) }}</p>
            
            <div class="recording-tags" v-if="recording.tags && recording.tags.length > 0">
              <span
                v-for="tag in recording.tags.slice(0, 3)"
                :key="tag.id"
                class="tag"
              >
                {{ tag.name }}
              </span>
              <span v-if="recording.tags.length > 3" class="tag-more">
                +{{ recording.tags.length - 3 }}
              </span>
            </div>

            <div class="recording-footer">
              <div class="recording-stats">
                <span v-if="recording.views" class="recording-views">
                  <i class="fas fa-eye"></i>
                  {{ recording.views }}
                </span>
                <span v-if="recording.video_path" class="has-video">
                  <i class="fas fa-video"></i>
                  Видео
                </span>
              </div>
              
              <div class="recording-actions" v-if="canEditRecording(recording)">
                <button
                  @click.stop="editRecording(recording.id)"
                  class="action-btn edit-btn"
                  title="Редактировать"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button
                  @click.stop="deleteRecording(recording)"
                  class="action-btn delete-btn"
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
      <div v-else class="no-results">
        <i class="fas fa-search"></i>
        <h3>Записи не найдены</h3>
        <p>Попробуйте изменить параметры поиска или фильтры</p>
        <button @click="clearFilters" class="btn btn-primary">
          Сбросить фильтры
        </button>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination" data-aos="fade-up">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        
        <span
          v-for="page in visiblePages"
          :key="page"
          @click="changePage(page)"
          class="pagination-number"
          :class="{ active: page === currentPage }"
        >
          {{ page }}
        </span>
        
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
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
          <p>Вы уверены, что хотите удалить запись "{{ recordingToDelete?.title }}"?</p>
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
    ...mapGetters(['isAuthenticated', 'isAdmin', 'isModerator', 'getFileUrl']),
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
  methods: {
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
      } catch (error) {
        console.error('Error fetching recordings:', error)
      }
    },
    async fetchCategories() {      try {
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
      // Hide the image and show placeholder
      const imageContainer = event.target.closest('.recording-image')
      if (imageContainer) {
        imageContainer.style.display = 'none'
        // Show placeholder if it exists
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
}

.recordings-header p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.filters-section {
  margin-bottom: 2rem;
}

.filters-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
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
  color: rgba(255, 255, 255, 0.6);
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
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

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-select {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
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
}

.filter-select option {
  background: #1e3c72;
  color: #ffffff;
}

.clear-filters {
  margin-left: auto;
}

.add-recording-section {
  text-align: center;
  margin-bottom: 2rem;
}

.recordings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
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
  position: relative;
}

.recording-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
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
  background: rgba(255, 255, 255, 0.05);
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
  background: rgba(0, 0, 0, 0.5);
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
}

.tag-more {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
}

.recording-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
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
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  font-size: 0.8rem;
}

.edit-btn {
  background: rgba(52, 152, 219, 0.8);
  color: #ffffff;
}

.edit-btn:hover {
  background: rgba(52, 152, 219, 1);
  transform: scale(1.1);
}

.delete-btn {
  background: rgba(231, 76, 60, 0.8);
  color: #ffffff;
}

.delete-btn:hover {
  background: rgba(231, 76, 60, 1);
  transform: scale(1.1);
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
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
  color: #ffd700;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-number {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.pagination-number:hover {
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
  color: #ffd700;
}

.pagination-number.active {
  background: #ffd700;
  border-color: #ffd700;
  color: #1e3c72;
    font-weight: 600;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
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


