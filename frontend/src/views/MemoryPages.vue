<template>
  <div class="memory-pages">
    <!-- Hero Section -->
    <section class="memory-hero">
      <div class="container">
        <h1 class="memory-title">Страницы памяти</h1>
        <p class="memory-subtitle">
          Вечная память героям Великой Отечественной войны
        </p>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="container">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.veterans }}</div>
            <div class="stat-label">Ветеранов</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-calendar-alt"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.events }}</div>
            <div class="stat-label">Событий</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-crosshairs"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.battles }}</div>
            <div class="stat-label">Сражений</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-shield-alt"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.units }}</div>
            <div class="stat-label">Воинских частей</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Map Section -->
    <section class="container">
      <div class="memory-card">
        <h2 class="section-title">
          <i class="fas fa-map-marked-alt"></i>
          Интерактивная карта военных действий
        </h2>

        <!-- Timeline Control -->
        <div class="timeline-control">
          <div class="timeline-header">
            <h3 class="timeline-title">
              <i class="fas fa-clock"></i>
              Временная шкала: {{ currentDate }}
            </h3>
            <div class="timeline-info">
              Событие {{ currentTimelineIndex + 1 }} из
              {{ timelineDates.length }}
            </div>
          </div>

          <div class="timeline-slider-container">
            <input
              type="range"
              class="timeline-slider"
              :min="0"
              :max="timelineDates.length - 1"
              v-model="currentTimelineIndex"
              @input="updateMapData"
            />
            <div class="timeline-labels">
              <span>1939</span>
              <span>1945</span>
            </div>
          </div>
        </div>

        <!-- Map Container -->
        <div class="map-container" ref="mapContainer">
          <div class="map-controls">
            <button
              @click="toggleEvents"
              :class="['btn', 'btn-memory', { active: showEvents }]"
            >
              <i class="fas fa-map-pin"></i>
              {{ showEvents ? 'Скрыть события' : 'Показать события' }}
            </button>
            <button
              @click="toggleFrontlines"
              :class="['btn', 'btn-memory', { active: showFrontlines }]"
            >
              <i class="fas fa-route"></i>
              {{
                showFrontlines ? 'Скрыть линии фронта' : 'Показать линии фронта'
              }}
            </button>
          </div>
          <div id="war-map" class="war-map"></div>
        </div>
      </div>
    </section>

    <!-- Veterans Section -->
    <section class="container">
      <div class="memory-card">
        <div class="veterans-header">
          <h2 class="section-title">
            <i class="fas fa-medal"></i>
            Наши герои
          </h2>
          <div class="veterans-controls">
            <div class="search-container">
              <i class="fas fa-search search-icon"></i>
              <input
                type="text"
                v-model="veteranSearch"
                placeholder="Поиск ветеранов..."
                class="form-input memory-input search-input"
                @input="searchVeterans"
              />
            </div>
            <button
              v-if="canAddVeteran"
              @click="showAddVeteranModal = true"
              class="btn btn-memory add-veteran-btn"
            >
              <i class="fas fa-plus"></i>
              Добавить ветерана
            </button>
          </div>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="spinner memory-spinner"></div>
          <p>Загрузка данных о ветеранах...</p>
        </div>

        <div v-else-if="veterans.length === 0" class="empty-state">
          <i class="fas fa-users fa-4x"></i>
          <h3>Ветераны не найдены</h3>
          <p>Попробуйте изменить параметры поиска</p>
        </div>

        <div v-else class="veterans-grid">
          <div
            v-for="veteran in veterans"
            :key="veteran.id"
            class="veteran-card memory-card"
          >
            <div class="veteran-photo-container">
              <img
                v-if="veteran.photo_path"
                :src="getImageUrl(veteran.photo_path)"
                :alt="veteran.full_name"
                class="veteran-photo"
              />
              <div v-else class="veteran-photo-placeholder">
                <i class="fas fa-user"></i>
              </div>
            </div>

            <div class="veteran-info">
              <h3 class="veteran-name">{{ veteran.full_name }}</h3>

              <div class="veteran-dates">
                <i class="fas fa-calendar"></i>
                {{ formatDate(veteran.birth_date) }} -
                {{ formatDate(veteran.death_date) }}
              </div>

              <div v-if="veteran.position" class="veteran-position">
                <i class="fas fa-star"></i>
                {{ veteran.position.name }}
              </div>

              <div v-if="veteran.unit" class="veteran-unit">
                <i class="fas fa-shield-alt"></i>
                <strong>Воинская часть:</strong> {{ veteran.unit }}
              </div>

              <div v-if="veteran.biography" class="veteran-biography">
                <i class="fas fa-book"></i>
                {{ veteran.biography }}
              </div>

              <div v-if="veteran.awards" class="veteran-awards">
                <i class="fas fa-medal"></i>
                <strong>Награды:</strong> {{ veteran.awards }}
              </div>

              <div v-if="veteran.battles" class="veteran-battles">
                <i class="fas fa-crosshairs"></i>
                <strong>Участие в боях:</strong> {{ veteran.battles }}
              </div>

              <div v-if="canEditVeteran" class="veteran-actions">
                <button
                  @click="editVeteran(veteran)"
                  class="btn btn-secondary btn-sm"
                >
                  <i class="fas fa-edit"></i>
                  Редактировать
                </button>
                <button
                  @click="deleteVeteran(veteran)"
                  class="btn btn-danger btn-sm"
                >
                  <i class="fas fa-trash"></i>
                  Удалить
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-container">
          <nav class="pagination">
            <button
              v-for="page in totalPages"
              :key="page"
              @click="loadVeterans(page)"
              :class="[
                'btn',
                'pagination-btn',
                currentPage === page ? 'btn-memory active' : 'btn-secondary'
              ]"
            >
              {{ page }}
            </button>
          </nav>
        </div>
      </div>
    </section>

    <!-- Add Veteran Modal -->
    <div v-if="showAddVeteranModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content memory-card" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">
            <i class="fas fa-user-plus"></i>
            Добавить ветерана
          </h3>
          <button @click="closeModal" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <form @submit.prevent="addVeteran" class="veteran-form">
          <div class="form-grid">
            <div class="form-group">
              <label class="memory-form-label">
                <i class="fas fa-user"></i>
                Полное имя *
              </label>
              <input
                type="text"
                v-model="newVeteran.full_name"
                class="form-input memory-input"
                required
              />
            </div>

            <div class="form-group">
              <label class="memory-form-label">
                <i class="fas fa-birthday-cake"></i>
                Дата рождения
              </label>
              <input
                type="date"
                v-model="newVeteran.birth_date"
                class="form-input memory-input"
              />
            </div>

            <div class="form-group">
              <label class="memory-form-label">
                <i class="fas fa-cross"></i>
                Дата смерти
              </label>
              <input
                type="date"
                v-model="newVeteran.death_date"
                class="form-input memory-input"
              />
            </div>

            <div class="form-group">
              <label class="memory-form-label">
                <i class="fas fa-star"></i>
                Воинское звание
              </label>
              <select
                v-model="newVeteran.position_id"
                class="form-select memory-input"
              >
                <option value="">Выберите звание</option>
                <option
                  v-for="position in militaryPositions"
                  :key="position.id"
                  :value="position.id"
                >
                  {{ position.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="memory-form-label">
              <i class="fas fa-shield-alt"></i>
              Воинская часть
            </label>
            <input
              type="text"
              v-model="newVeteran.unit"
              class="form-input memory-input"
            />
          </div>

          <div class="form-group">
            <label class="memory-form-label">
              <i class="fas fa-book"></i>
              Биография
            </label>
            <textarea
              v-model="newVeteran.biography"
              class="form-input memory-input form-textarea"
              rows="4"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="memory-form-label">
              <i class="fas fa-medal"></i>
              Награды
            </label>
            <textarea
              v-model="newVeteran.awards"
              class="form-input memory-input"
              rows="2"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="memory-form-label">
              <i class="fas fa-crosshairs"></i>
              Участие в боях
            </label>
            <textarea
              v-model="newVeteran.battles"
              class="form-input memory-input"
              rows="2"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="memory-form-label">
              <i class="fas fa-image"></i>
              Фотография
            </label>
            <input
              type="file"
              @change="handlePhotoUpload"
              accept="image/*"
              class="form-input memory-input file-input"
            />
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              <i class="fas fa-times"></i>
              Отмена
            </button>
            <button type="submit" class="btn btn-memory" :disabled="submitting">
              <i class="fas fa-save"></i>
              {{ submitting ? 'Сохранение...' : 'Сохранить' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MemoryPages',
  data() {
    return {
      stats: {
        veterans: 0,
        events: 0,
        battles: 0,
        units: 0
      },
      veterans: [],
      loading: false,
      veteranSearch: '',
      currentPage: 1,
      totalPages: 1,
      showAddVeteranModal: false,
      submitting: false,
      newVeteran: {
        full_name: '',
        birth_date: '',
        death_date: '',
        position_id: '',
        unit: '',
        biography: '',
        awards: '',
        battles: '',
        photo: null
      },
      militaryPositions: [],

      // Map data
      map: null,
      timelineDates: [],
      currentTimelineIndex: 0,
      currentDate: '',
      showEvents: true,
      showFrontlines: true,
      mapEvents: [],
      mapFrontlines: [],
      eventMarkers: [],
      frontlineLayer: null,
      searchTimeout: null
    }
  },
  computed: {
    canAddVeteran() {
      return (
        this.$store.getters.isAuthenticated &&
        ['admin', 'moderator'].includes(this.$store.getters.userRole)
      )
    },
    canEditVeteran() {
      return (
        this.$store.getters.isAuthenticated &&
        ['admin', 'moderator'].includes(this.$store.getters.userRole)
      )
    }
  },
  mounted() {
    document.body.classList.add('memory-pages')
    this.loadStats()
    this.loadVeterans()
    this.loadMilitaryPositions()
    this.loadTimelineData()
    this.$nextTick(() => {
      this.initMap()
    })
  },
  beforeUnmount() {
    document.body.classList.remove('memory-pages')
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout)
    }
  },
  methods: {
    async loadStats() {
      try {
        const response = await axios.get('/api/memory-pages/stats')
        this.stats = response.data
      } catch (error) {
        console.error('Error loading stats:', error)
        this.$store.dispatch('showNotification', {
          type: 'error',
          message: 'Ошибка загрузки статистики'
        })
      }
    },

    async loadVeterans(page = 1) {
      this.loading = true
      try {
        const params = {
          page,
          per_page: 6,
          search: this.veteranSearch
        }

        const response = await axios.get('/api/veterans', { params })
        this.veterans = response.data.veterans
        this.currentPage = response.data.page
        this.totalPages = response.data.total_pages
      } catch (error) {
        console.error('Error loading veterans:', error)
        this.$store.dispatch('showNotification', {
          type: 'error',
          message: 'Ошибка загрузки данных о ветеранах'
        })
      } finally {
        this.loading = false
      }
    },

    async loadMilitaryPositions() {
      try {
        const response = await axios.get('/api/military-positions')
        this.militaryPositions = response.data
      } catch (error) {
        console.error('Error loading military positions:', error)
      }
    },

    async loadTimelineData() {
      try {
        const response = await axios.get('/api/ww2/timeline')
        this.timelineDates = response.data
        if (this.timelineDates.length > 0) {
          this.currentDate = this.timelineDates[0]
          this.loadMapData()
        }
      } catch (error) {
        console.error('Error loading timeline:', error)
        this.$store.dispatch('showNotification', {
          type: 'error',
          message: 'Ошибка загрузки временной шкалы'
        })
      }
    },

    async loadMapData() {
      try {
        // Load events
        const eventsResponse = await axios.get('/api/ww2/events', {
          params: {
            start_date: '1939-01-01',
            end_date: this.currentDate
          }
        })
        this.mapEvents = eventsResponse.data

        // Load frontlines
        const frontlinesResponse = await axios.get('/api/ww2/frontlines', {
          params: {
            date: this.currentDate,
            theater: 'Eastern'
          }
        })
        this.mapFrontlines = frontlinesResponse.data

        this.updateMapDisplay()
      } catch (error) {
        console.error('Error loading map data:', error)
        this.$store.dispatch('showNotification', {
          type: 'error',
          message: 'Ошибка загрузки данных карты'
        })
      }
    },

    initMap() {
      // Initialize Leaflet map
      if (typeof L !== 'undefined') {
        this.map = L.map('war-map').setView([55.7558, 37.6176], 4)

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(this.map)

        this.updateMapDisplay()
      } else {
        // Load Leaflet if not available
        this.loadLeaflet()
      }
    },

    loadLeaflet() {
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css'
      document.head.appendChild(link)

      const script = document.createElement('script')
      script.src = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js'
      script.onload = () => {
        this.$nextTick(() => {
          this.initMap()
        })
      }
      document.head.appendChild(script)
    },

    updateMapDisplay() {
      if (!this.map) return

      // Clear existing markers and layers
      this.eventMarkers.forEach((marker) => this.map.removeLayer(marker))
      this.eventMarkers = []

      if (this.frontlineLayer) {
        this.map.removeLayer(this.frontlineLayer)
        this.frontlineLayer = null
      }

      // Add event markers
      if (this.showEvents) {
        this.mapEvents.forEach((event) => {
          const marker = L.marker([event.latitude, event.longitude]).bindPopup(`
              <div class="map-popup">
                <h4>${event.title}</h4>
                <p><strong>Дата:</strong> ${this.formatDate(event.date)}</p>
                <p>${event.description}</p>
              </div>
            `)

          marker.addTo(this.map)
          this.eventMarkers.push(marker)
        })
      }

      // Add frontlines
      if (this.showFrontlines && this.mapFrontlines.length > 0) {
        const frontline = this.mapFrontlines[0]
        this.frontlineLayer = L.polyline(frontline.coordinates, {
          color: '#DC143C',
          weight: 3,
          opacity: 0.8
        }).addTo(this.map)
      }
    },

    updateMapData() {
      if (this.timelineDates.length > 0) {
        this.currentDate = this.timelineDates[this.currentTimelineIndex]
        this.loadMapData()
      }
    },

    toggleEvents() {
      this.showEvents = !this.showEvents
      this.updateMapDisplay()
    },

    toggleFrontlines() {
      this.showFrontlines = !this.showFrontlines
      this.updateMapDisplay()
    },

    searchVeterans() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout)
      }
      this.searchTimeout = setTimeout(() => {
        this.loadVeterans(1)
      }, 500)
    },

    async addVeteran() {
      this.submitting = true
      try {
        const formData = new FormData()
        Object.keys(this.newVeteran).forEach((key) => {
          if (key !== 'photo' && this.newVeteran[key]) {
            formData.append(key, this.newVeteran[key])
          }
        })

        if (this.newVeteran.photo) {
          formData.append('photo', this.newVeteran.photo)
        }

        await axios.post('/api/veterans/create', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.$store.getters.token}`
          }
        })

        this.$store.dispatch('showNotification', {
          type: 'success',
          message: 'Ветеран успешно добавлен'
        })

        this.closeModal()
        this.loadVeterans()
        this.loadStats()
      } catch (error) {
        console.error('Error adding veteran:', error)
        this.$store.dispatch('showNotification', {
          type: 'error',
          message:
            error.response?.data?.message || 'Ошибка при добавлении ветерана'
        })
      } finally {
        this.submitting = false
      }
    },

    editVeteran(veteran) {
      // TODO: Implement edit functionality
      console.log('Edit veteran:', veteran)
      this.$store.dispatch('showNotification', {
        type: 'info',
        message: 'Функция редактирования будет добавлена в следующем обновлении'
      })
    },

    async deleteVeteran(veteran) {
      if (
        !confirm(
          `Вы уверены, что хотите удалить запись о ${veteran.full_name}?`
        )
      ) {
        return
      }

      try {
        await axios.delete(`/api/veterans/${veteran.id}/delete`, {
          headers: {
            Authorization: `Bearer ${this.$store.getters.token}`
          }
        })

        this.$store.dispatch('showNotification', {
          type: 'success',
          message: 'Ветеран успешно удален'
        })

        this.loadVeterans()
        this.loadStats()
      } catch (error) {
        console.error('Error deleting veteran:', error)
        this.$store.dispatch('showNotification', {
          type: 'error',
          message:
            error.response?.data?.message || 'Ошибка при удалении ветерана'
        })
      }
    },

    handlePhotoUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.newVeteran.photo = file
      }
    },

    closeModal() {
      this.showAddVeteranModal = false
      this.newVeteran = {
        full_name: '',
        birth_date: '',
        death_date: '',
        position_id: '',
        unit: '',
        biography: '',
        awards: '',
        battles: '',
        photo: null
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'Неизвестно'

      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },

    getImageUrl(path) {
      return `${process.env.VUE_APP_API_URL || 'http://localhost:5000'}${path}`
    }
  }
}
</script>

<style scoped>
.memory-pages {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: white;
}

.memory-hero {
  background: linear-gradient(
    135deg,
    rgba(139, 0, 0, 0.9),
    rgba(220, 20, 60, 0.8)
  );
  padding: 4rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.memory-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="stars" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="rgba(255,215,0,0.3)"/></pattern></defs><rect width="100" height="100" fill="url(%23stars)"/></svg>');
  opacity: 0.3;
}

.memory-title {
  font-size: 3.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 1;
}

.memory-subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  position: relative;
  z-index: 1;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.stat-card {
  background: linear-gradient(
    145deg,
    rgba(255, 215, 0, 0.1),
    rgba(220, 20, 60, 0.1)
  );
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: #ffd700;
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
}

.stat-icon {
  font-size: 2.5rem;
  color: #ffd700;
  flex-shrink: 0;
}

.stat-content {
  text-align: left;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  line-height: 1;
}
.stat-label {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 0.5rem;
}

.memory-card {
  background: linear-gradient(
    145deg,
    rgba(139, 0, 0, 0.9),
    rgba(220, 20, 60, 0.8)
  );
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 215, 0, 0.5);
  border-radius: 20px;
  padding: 2rem;
  margin: 2rem 0;
}

.section-title {
  color: #ffd700;
  margin-bottom: 2rem;
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.timeline-control {
  margin-bottom: 2rem;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.timeline-title {
  color: #ffd700;
  font-size: 1.3rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.timeline-info {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.timeline-slider-container {
  position: relative;
}

.timeline-slider {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.2);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.timeline-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

.timeline-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

.timeline-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.map-container {
  position: relative;
  height: 500px;
  border-radius: 15px;
  overflow: hidden;
  border: 2px solid rgba(255, 215, 0, 0.3);
}

.map-controls {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
  display: flex;
  gap: 0.5rem;
}

.war-map {
  height: 100%;
  width: 100%;
}

.veterans-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.veterans-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-container {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.6);
  z-index: 1;
}

.search-input {
  padding-left: 3rem !important;
  width: 300px;
}

.add-veteran-btn {
  white-space: nowrap;
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
}

.memory-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 215, 0, 0.3);
  border-top: 4px solid #ffd700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
}

.empty-state i {
  color: rgba(255, 215, 0, 0.5);
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: #ffd700;
  margin-bottom: 0.5rem;
}

.veterans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.veteran-card {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.veteran-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
}

.veteran-photo-container {
  flex-shrink: 0;
}

.veteran-photo {
  width: 120px;
  height: 150px;
  object-fit: cover;
  border-radius: 12px;
  border: 3px solid rgba(255, 215, 0, 0.5);
}

.veteran-photo-placeholder {
  width: 120px;
  height: 150px;
  background: rgba(255, 215, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffd700;
  font-size: 3rem;
  border-radius: 12px;
  border: 3px solid rgba(255, 215, 0, 0.5);
}

.veteran-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.veteran-name {
  color: #ffd700;
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0;
}

.veteran-dates,
.veteran-position,
.veteran-unit,
.veteran-biography,
.veteran-awards,
.veteran-battles {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.95rem;
  line-height: 1.5;
}

.veteran-dates {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.veteran-position {
  color: #ffd700;
  font-weight: 500;
}

.veteran-unit,
.veteran-awards,
.veteran-battles {
  color: rgba(255, 255, 255, 0.8);
}

.veteran-biography {
  color: rgba(255, 255, 255, 0.8);
  font-style: italic;
}

.veteran-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.pagination {
  display: flex;
  gap: 0.5rem;
}

.pagination-btn {
  min-width: 45px;
  height: 45px;
  border-radius: 10px;
  font-weight: 500;
}

.pagination-btn.active {
  background: #ffd700 !important;
  color: #1a1a2e !important;
  border-color: #ffd700 !important;
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
  padding: 2rem;
}

.modal-content {
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
}

.modal-title {
  color: #ffd700;
  margin: 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.modal-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.modal-close:hover {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

.veteran-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.memory-form-label {
  color: #ffd700;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-input,
.form-select,
.form-textarea {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.file-input {
  padding: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px solid rgba(255, 215, 0, 0.3);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-size: 0.95rem;
}

.btn-memory {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #1a1a2e;
  border: 2px solid transparent;
}

.btn-memory:hover {
  background: linear-gradient(135deg, #ffed4e, #ffd700);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
}

.btn-memory.active {
  background: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-danger {
  background: linear-gradient(135deg, #dc2626, #ef4444);
  color: white;
  border: 2px solid transparent;
}

.btn-danger:hover {
  background: linear-gradient(135deg, #b91c1c, #dc2626);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(220, 38, 38, 0.4);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Map popup styles */
:global(.map-popup) {
  color: #1a1a2e;
}

:global(.map-popup h4) {
  color: #dc2626;
  margin-bottom: 0.5rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .memory-title {
    font-size: 2.5rem;
  }

  .memory-subtitle {
    font-size: 1.2rem;
  }

  .container {
    padding: 0 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .stat-content {
    text-align: center;
  }

  .veterans-header {
    flex-direction: column;
    align-items: stretch;
  }

  .veterans-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .veterans-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .veteran-card {
    flex-direction: column;
    text-align: center;
  }

  .veteran-info {
    align-items: center;
    text-align: center;
  }

  .veteran-actions {
    justify-content: center;
  }

  .timeline-header {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }

  .map-controls {
    position: static;
    margin-bottom: 1rem;
    justify-content: center;
  }

  .map-container {
    height: 400px;
  }

  .modal-overlay {
    padding: 1rem;
  }

  .modal-content {
    max-height: 95vh;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }

  .section-title {
    font-size: 1.5rem;
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .memory-title {
    font-size: 2rem;
  }

  .memory-subtitle {
    font-size: 1rem;
  }

  .memory-card {
    padding: 1rem;
  }

  .veteran-photo,
  .veteran-photo-placeholder {
    width: 100px;
    height: 120px;
  }

  .veteran-name {
    font-size: 1.1rem;
  }

  .map-controls {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

/* Animation for loading states */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.veteran-card {
  animation: fadeIn 0.5s ease-out;
}

.stat-card {
  animation: fadeIn 0.5s ease-out;
}

/* Scrollbar styling for modal */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: rgba(255, 215, 0, 0.5);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 215, 0, 0.7);
}

/* Focus styles for accessibility */
.btn:focus,
.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: 2px solid #ffd700;
  outline-offset: 2px;
}

/* Print styles */
@media print {
  .memory-pages {
    background: white !important;
    color: black !important;
  }

  .memory-card {
    background: white !important;
    border: 1px solid #ccc !important;
  }

  .btn,
  .modal-overlay,
  .map-container {
    display: none !important;
  }

  .veteran-card {
    break-inside: avoid;
    page-break-inside: avoid;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .memory-card {
    border-width: 3px;
  }

  .btn-memory {
    background: #ffd700;
    color: #000;
  }

  .form-input,
  .form-select,
  .form-textarea {
    border-width: 3px;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .veteran-card,
  .stat-card,
  .btn {
    animation: none;
    transition: none;
  }

  .memory-spinner {
    animation: none;
  }

  .btn:hover,
  .veteran-card:hover,
  .stat-card:hover {
    transform: none;
  }
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .form-input::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }
}
</style>
