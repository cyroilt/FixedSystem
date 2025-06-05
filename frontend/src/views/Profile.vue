<template>
  <div class="profile">
    <div class="container">
      <!-- Profile Header -->
      <div class="profile-header" data-aos="fade-up">
        <div class="profile-avatar">
          <div class="avatar-circle">
            <i class="fas fa-user"></i>
          </div>
          <button v-if="isOwnProfile" @click="showAvatarModal = true" class="avatar-edit">
            <i class="fas fa-camera"></i>
          </button>
        </div>
        
        <div class="profile-info">
          <h1 class="profile-name">{{ profileUser.username }}</h1>
          <p class="profile-role">{{ getUserRole(profileUser) }}</p>
          <p class="profile-email">{{ profileUser.email }}</p>
          
          <div class="profile-stats">
            <div class="stat">
              <span class="stat-number">{{ userStats.recordings }}</span>
              <span class="stat-label">Записей</span>
            </div>
            <div class="stat">
              <span class="stat-number">{{ userStats.views }}</span>
              <span class="stat-label">Просмотров</span>
            </div>
            <div class="stat">
              <span class="stat-number">{{ formatDate(profileUser.created_at, 'short') }}</span>
              <span class="stat-label">Регистрация</span>
            </div>
          </div>
          
          <div v-if="isOwnProfile" class="profile-actions">
            <button @click="showEditModal = true" class="btn btn-primary">
              <i class="fas fa-edit"></i>
              Редактировать профиль
            </button>
            <button @click="showPasswordModal = true" class="btn btn-secondary">
              <i class="fas fa-key"></i>
              Сменить пароль
            </button>
          </div>
        </div>
      </div>

      <!-- Profile Content -->
      <div class="profile-content">
        <!-- Navigation Tabs -->
        <div class="profile-tabs" data-aos="fade-up" data-aos-delay="100">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="['tab-btn', { active: activeTab === tab.key }]"
          >
            <i :class="tab.icon"></i>
            {{ tab.label }}
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content" data-aos="fade-up" data-aos-delay="200">
          <!-- Recordings Tab -->
          <div v-if="activeTab === 'recordings'" class="recordings-tab">
            <div class="tab-header">
              <h3>Мои записи</h3>
              <div class="tab-filters">
                <select v-model="recordingsFilter" class="filter-select">
                  <option value="all">Все записи</option>
                  <option value="published">Опубликованные</option>
                  <option value="draft">Черновики</option>
                </select>
              </div>
            </div>
            
            <div v-if="userRecordings.length > 0" class="recordings-grid">
              <div
                v-for="recording in filteredRecordings"
                :key="recording.id"
                class="recording-card"
                @click="viewRecording(recording.id)"
              >
                <div class="recording-image" v-if="recording.image_path">
                  <img :src="recording.image_path" :alt="recording.title">
                </div>
                <div class="recording-content">
                  <div class="recording-meta">
                    <span class="recording-status" :class="recording.status">
                      {{ getStatusLabel(recording.status) }}
                    </span>
                    <span class="recording-date">{{ formatDate(recording.created_at) }}</span>
                  </div>
                  <h4 class="recording-title">{{ recording.title }}</h4>
                  <p class="recording-excerpt">{{ truncateText(recording.content, 100) }}</p>
                  <div class="recording-stats">
                    <span><i class="fas fa-eye"></i> {{ recording.views || 0 }}</span>
                    <span><i class="fas fa-heart"></i> {{ recording.likes || 0 }}</span>
                  </div>
                </div>
                <div v-if="isOwnProfile" class="recording-actions">
                  <button @click.stop="editRecording(recording.id)" class="action-btn edit-btn">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click.stop="deleteRecording(recording.id)" class="action-btn delete-btn">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <i class="fas fa-file-alt"></i>
              <h3>Нет записей</h3>
              <p>{{ isOwnProfile ? 'Вы еще не создали ни одной записи' : 'Пользователь не создал ни одной записи' }}</p>
              <router-link v-if="isOwnProfile" to="/recordings/create" class="btn btn-primary">
                <i class="fas fa-plus"></i>
                Создать запись
              </router-link>
            </div>
          </div>

          <!-- Activity Tab -->
          <div v-if="activeTab === 'activity'" class="activity-tab">
            <h3>Активность</h3>
            <div class="activity-timeline">
              <div
                v-for="activity in userActivity"
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-icon">
                  <i :class="getActivityIcon(activity.type)"></i>
                </div>
                <div class="activity-content">
                  <p class="activity-text">{{ activity.description }}</p>
                  <span class="activity-time">{{ formatDate(activity.created_at, 'relative') }}</span>
                </div>
              </div>
            </div>
            
            <div v-if="userActivity.length === 0" class="empty-state">
              <i class="fas fa-clock"></i>
              <h3>Нет активности</h3>
              <p>История активности пуста</p>
            </div>
          </div>

          <!-- Settings Tab (only for own profile) -->
          <div v-if="activeTab === 'settings' && isOwnProfile" class="settings-tab">
            <h3>Настройки</h3>
            <div class="settings-sections">
              <div class="settings-section">
                <h4>Уведомления</h4>
                <div class="setting-item">
                  <label class="setting-label">
                    <input type="checkbox" v-model="settings.emailNotifications">
                    <span class="checkmark"></span>
                    Email уведомления
                  </label>
                </div>
                <div class="setting-item">
                  <label class="setting-label">
                    <input type="checkbox" v-model="settings.pushNotifications">
                    <span class="checkmark"></span>
                    Push уведомления
                  </label>
                </div>
              </div>
              
              <div class="settings-section">
                <h4>Приватность</h4>
                <div class="setting-item">
                  <label class="setting-label">
                    <input type="checkbox" v-model="settings.publicProfile">
                    <span class="checkmark"></span>
                    Публичный профиль
                  </label>
                </div>
                <div class="setting-item">
                  <label class="setting-label">
                    <input type="checkbox" v-model="settings.showEmail">
                    <span class="checkmark"></span>
                    Показывать email
                  </label>
                </div>
              </div>
              
              <div class="settings-actions">
                <button @click="saveSettings" class="btn btn-primary">
                  <i class="fas fa-save"></i>
                  Сохранить настройки
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Редактировать профиль</h3>
          <button @click="showEditModal = false" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateProfile">
            <div class="form-group">
              <label class="form-label">Имя пользователя</label>
              <input
                v-model="editForm.username"
                type="text"
                class="form-input"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">Email</label>
              <input
                v-model="editForm.email"
                type="email"
                class="form-input"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">О себе</label>
              <textarea
                v-model="editForm.bio"
                class="form-textarea"
                rows="4"
                placeholder="Расскажите о себе..."
              ></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button @click="showEditModal = false" class="btn btn-secondary">
            Отмена
          </button>
          <button @click="updateProfile" class="btn btn-primary">
            <i class="fas fa-save"></i>
            Сохранить
          </button>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="showPasswordModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Сменить пароль</h3>
          <button @click="showPasswordModal = false" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="changePassword">
            <div class="form-group">
              <label class="form-label">Текущий пароль</label>
              <input
                v-model="passwordForm.currentPassword"
                type="password"
                class="form-input"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label">Новый пароль</label>
              <input
                v-model="passwordForm.newPassword"
                type="password"
                class="form-input"
                required
                minlength="6"
              >
            </div>
            <div class="form-group">
              <label class="form-label">Подтвердите новый пароль</label>
              <input
                v-model="passwordForm.confirmPassword"
                type="password"
                class="form-input"
                required
              >
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button @click="showPasswordModal = false" class="btn btn-secondary">
            Отмена
          </button>
          <button @click="changePassword" class="btn btn-primary">
            <i class="fas fa-key"></i>
            Сменить пароль
          </button>
        </div>
      </div>
    </div>

    <!-- Avatar Upload Modal -->
    <div v-if="showAvatarModal" class="modal-overlay" @click="showAvatarModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Изменить аватар</h3>
          <button @click="showAvatarModal = false" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="avatar-upload">
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              @change="handleAvatarSelect"
              class="file-input"
            >
            <div class="upload-area" @click="$refs.avatarInput.click()">
              <i class="fas fa-camera"></i>
              <p>Выберите изображение</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAvatarModal = false" class="btn btn-secondary">
            Отмена
          </button>
          <button @click="uploadAvatar" class="btn btn-primary">
            <i class="fas fa-upload"></i>
            Загрузить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  name: 'Profile',
  data() {
    return {
      profileUser: {},
      userStats: {
        recordings: 0,
        views: 0
      },
      userRecordings: [],
      userActivity: [],
      activeTab: 'recordings',
      recordingsFilter: 'all',
      settings: {
        emailNotifications: true,
        pushNotifications: false,
        publicProfile: true,
        showEmail: false
      },
      showEditModal: false,
      showPasswordModal: false,
      showAvatarModal: false,
      editForm: {
        username: '',
        email: '',
        bio: ''
      },
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      avatarFile: null,
      tabs: [
        { key: 'recordings', label: 'Записи', icon: 'fas fa-file-alt' },
        { key: 'activity', label: 'Активность', icon: 'fas fa-clock' },
        { key: 'settings', label: 'Настройки', icon: 'fas fa-cog' }
      ]
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin']),
    ...mapState(['user']),
    isOwnProfile() {
      return this.isAuthenticated && this.user && this.profileUser.id === this.user.id
    },
    filteredRecordings() {
      if (this.recordingsFilter === 'all') return this.userRecordings
      return this.userRecordings.filter(recording => recording.status === this.recordingsFilter)
    }
  },
  async created() {
    const userId = this.$route.params.id || (this.user && this.user.id)
    if (!userId) {
      this.$router.push('/login')
      return
    }
    
    await this.loadProfile(userId)
    
    // Remove settings tab if not own profile
    if (!this.isOwnProfile) {
      this.tabs = this.tabs.filter(tab => tab.key !== 'settings')
    }
  },
  watch: {
    '$route.params.id': {
      handler(newId) {
        const userId = newId || (this.user && this.user.id)
        if (userId) {
          this.loadProfile(userId)
        }
      }
    }
  },
  methods: {
    async loadProfile(userId) {
      try {
        this.profileUser = await this.$store.dispatch('fetchUserProfile', userId)
        this.userStats = await this.$store.dispatch('fetchUserStats', userId)
        this.userRecordings = await this.$store.dispatch('fetchUserRecordings', userId)
        this.userActivity = await this.$store.dispatch('fetchUserActivity', userId)
        
        if (this.isOwnProfile) {
          this.editForm = {
            username: this.profileUser.username,
            email: this.profileUser.email,
            bio: this.profileUser.bio || ''
          }
          
          // Load user settings
          this.settings = await this.$store.dispatch('fetchUserSettings')
        }
      } catch (error) {
        console.error('Error loading profile:', error)
        this.$router.push('/404')
      }
    },
    async updateProfile() {
      try {
        await this.$store.dispatch('updateUserProfile', this.editForm)
        this.profileUser = { ...this.profileUser, ...this.editForm }
        this.showEditModal = false
      } catch (error) {
        console.error('Error updating profile:', error)
        alert('Ошибка при обновлении профиля')
      }
    },
    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        alert('Пароли не совпадают')
        return
      }
      
      try {
        await this.$store.dispatch('changePassword', {
          currentPassword: this.passwordForm.currentPassword,
          newPassword: this.passwordForm.newPassword
        })
        
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        this.showPasswordModal = false
        alert('Пароль успешно изменен')
      } catch (error) {
        console.error('Error changing password:', error)
        alert('Ошибка при смене пароля')
      }
    },
    async saveSettings() {
      try {
        await this.$store.dispatch('updateUserSettings', this.settings)
        alert('Настройки сохранены')
      } catch (error) {
        console.error('Error saving settings:', error)
        alert('Ошибка при сохранении настроек')
      }
    },
    handleAvatarSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.avatarFile = file
      }
    },
    async uploadAvatar() {
      if (!this.avatarFile) return
      
      try {
        const formData = new FormData()
        formData.append('avatar', this.avatarFile)
        
        await this.$store.dispatch('uploadAvatar', formData)
        this.showAvatarModal = false
        this.avatarFile = null
        
        // Reload profile to get updated avatar
        await this.loadProfile(this.profileUser.id)
      } catch (error) {
        console.error('Error uploading avatar:', error)
        alert('Ошибка при загрузке аватара')
      }
    },
    viewRecording(id) {
      this.$router.push(`/recordings/${id}`)
    },
    editRecording(id) {
      this.$router.push(`/recordings/${id}/edit`)
    },
    async deleteRecording(id) {
      if (!confirm('Вы уверены, что хотите удалить эту запись?')) return
      
      try {
        await this.$store.dispatch('deleteRecording', id)
        this.userRecordings = this.userRecordings.filter(r => r.id !== id)
      } catch (error) {
        console.error('Error deleting recording:', error)
        alert('Ошибка при удалении записи')
      }
    },
    getUserRole(user) {
      if (user.role === 'admin') return 'Администратор'
      if (user.role === 'moderator') return 'Модератор'
      return 'Пользователь'
    },
    getStatusLabel(status) {
      const labels = {
        published: 'Опубликовано',
        draft: 'Черновик',
        pending: 'На модерации'
      }
      return labels[status] || status
    },
    getActivityIcon(type) {
      const icons = {
        created_recording: 'fas fa-plus',
        updated_recording: 'fas fa-edit',
        deleted_recording: 'fas fa-trash',
        login: 'fas fa-sign-in-alt',
        profile_update: 'fas fa-user-edit'
      }
      return icons[type] || 'fas fa-circle'
    },
    truncateText(text, length) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    },
    formatDate(dateString, format = 'default') {
      const date = new Date(dateString)
      
      if (format === 'short') {
        return date.toLocaleDateString('ru-RU', {
          month: 'short',
          year: 'numeric'
        })
      }
      
      if (format === 'relative') {
        const now = new Date()
        const diff = now - date
        const days = Math.floor(diff / (1000 * 60 * 60 * 24))
        
        if (days === 0) return 'Сегодня'
        if (days === 1) return 'Вчера'
        if (days < 7) return `${days} дней назад`
        if (days < 30) return `${Math.floor(days / 7)} недель назад`
        return date.toLocaleDateString('ru-RU')
      }
      
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
.profile {
  padding: 2rem 0;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 3rem;
  margin-bottom: 4rem;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.profile-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-circle {
  width: 120px;
  height: 120px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #1e3c72;
}

.avatar-edit {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  background: #ffd700;
  border: none;
  border-radius: 50%;
  color: #1e3c72;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.avatar-edit:hover {
  transform: scale(1.1);
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.profile-role {
  color: #ffd700;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.profile-email {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
}

.profile-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffd700;
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.profile-actions {
  display: flex;
  gap: 1rem;
}

.profile-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.tab-btn {
  padding: 1rem 2rem;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-btn:hover {
  color: #ffd700;
}

.tab-btn.active {
  color: #ffd700;
  border-bottom-color: #ffd700;
}

.tab-content {
  min-height: 400px;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.tab-header h3 {
  color: #ffd700;
  font-size: 1.5rem;
  margin: 0;
}

.tab-filters {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9rem;
}

.filter-select option {
  background: #1e3c72;
  color: #ffffff;
}

.recordings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
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
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.recording-image {
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

.recording-content {
  padding: 1.5rem;
}

.recording-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.recording-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.recording-status.published {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.recording-status.draft {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.recording-status.pending {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.recording-date {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.recording-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.recording-excerpt {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.recording-stats {
  display: flex;
  gap: 1rem;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.recording-stats span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.recording-actions {
  position: absolute;
  top: 1rem;
  right: 1rem;
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
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.edit-btn {
  background: rgba(59, 130, 246, 0.8);
  color: #ffffff;
}

.edit-btn:hover {
  background: #3b82f6;
  transform: scale(1.1);
}

.delete-btn {
  background: rgba(239, 68, 68, 0.8);
  color: #ffffff;
}

.delete-btn:hover {
  background: #ef4444;
  transform: scale(1.1);
}

.activity-timeline {
  max-height: 600px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-bottom: 1rem;
  border-left: 3px solid #ffd700;
}

.activity-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 215, 0, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffd700;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.activity-time {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.settings-sections {
  max-width: 600px;
}

.settings-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.settings-section h4 {
  color: #ffd700;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.setting-item {
  margin-bottom: 1rem;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  font-size: 1rem;
}

.setting-label input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
}

.setting-label input[type="checkbox"]:checked + .checkmark {
  background: #ffd700;
  border-color: #ffd700;
}

.setting-label input[type="checkbox"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 2px;
  width: 6px;
  height: 10px;
  border: solid #1e3c72;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.settings-actions {
  text-align: right;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
}

.empty-state i {
  font-size: 4rem;
  color: #ffd700;
  margin-bottom: 2rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #ffffff;
}

.empty-state p {
  font-size: 1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
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
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.modal-close:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.avatar-upload {
  text-align: center;
}

.file-input {
  display: none;
}

.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 3rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #ffd700;
  background: rgba(255, 215, 0, 0.05);
}

.upload-area i {
  font-size: 3rem;
  color: #ffd700;
  margin-bottom: 1rem;
}

.upload-area p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }
  
  .profile-stats {
    justify-content: center;
  }
  
  .profile-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .profile-tabs {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .tab-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .recordings-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}
</style>
