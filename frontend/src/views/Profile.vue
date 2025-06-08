<template>
  <div class="profile bg-darker-gradient particles-bg">
    <div v-if="isAdmin" class="admin-access-banner">
      <div class="container">
        <div
          class="alert alert-info d-flex justify-content-between align-items-center"
        >
          <div>
            <i class="fas fa-crown me-2"></i>
            <strong>Administrator Access</strong> - You have admin privileges
          </div>
          <a
            :href="adminPanelUrl"
            target="_blank"
            class="btn btn-primary btn-sm"
          >
            <i class="fas fa-cog me-1"></i>
            Open Admin Panel
          </a>
        </div>
      </div>
    </div>
    <div class="container">
      <!-- Profile Header -->
      <div class="profile-header animate-fade-in-up">
        <div class="profile-avatar">
          <img
            v-if="profileUser.avatar"
            :src="profileUser.avatar"
            :alt="profileUser.username"
            class="avatar-image hover-scale"
          />
          <div v-else class="avatar-placeholder animate-pulse">
            <i class="fas fa-user"></i>
          </div>
          <button
            v-if="isOwnProfile"
            @click="showAvatarUpload = true"
            class="avatar-edit hover-glow"
            title="Изменить аватар"
          >
            <i class="fas fa-camera"></i>
          </button>
        </div>

        <div class="profile-info">
          <h1 class="profile-name animate-glow">{{ profileUser.username }}</h1>
          <p
            class="profile-email"
            v-if="!isOwnProfile || userSettings.showEmail"
          >
            {{ profileUser.email }}
          </p>
          <div class="profile-badges">
            <span class="badge" :class="getRoleBadgeClass(profileUser.role)">
              <i :class="getRoleIcon(profileUser.role)"></i>
              {{ getRoleText(profileUser.role) }}
            </span>
            <span class="badge badge-date">
              <i class="fas fa-calendar"></i>
              Регистрация: {{ formatDate(profileUser.created_at) }}
            </span>
          </div>
        </div>

        <div v-if="isOwnProfile" class="profile-actions">
          <button
            @click="showEditModal = true"
            class="btn btn-primary hover-scale"
          >
            <i class="fas fa-edit"></i>
            Редактировать профиль
          </button>
          <button
            @click="showSettingsModal = true"
            class="btn btn-secondary hover-glow"
          >
            <i class="fas fa-cog"></i>
            Настройки
          </button>
        </div>
      </div>

      <!-- Profile Stats -->
      <div class="profile-stats animate-fade-in-up animate-stagger-2">
        <div class="stat-card hover-lift animate-scale-in">
          <div class="stat-icon">
            <i class="fas fa-video"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ userStats.recordings || 0 }}</div>
            <div class="stat-label">Записей</div>
          </div>
        </div>

        <div class="stat-card hover-lift animate-scale-in animate-stagger-2">
          <div class="stat-icon">
            <i class="fas fa-eye"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ userStats.total_views || 0 }}</div>
            <div class="stat-label">Всего просмотров</div>
          </div>
        </div>

        <div class="stat-card hover-lift animate-scale-in animate-stagger-3">
          <div class="stat-icon">
            <i class="fas fa-thumbs-up"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ userStats.likes || 0 }}</div>
            <div class="stat-label">Лайков</div>
          </div>
        </div>

        <div class="stat-card hover-lift animate-scale-in animate-stagger-4">
          <div class="stat-icon">
            <i class="fas fa-star"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ userStats.rating || 0 }}</div>
            <div class="stat-label">Рейтинг</div>
          </div>
        </div>
      </div>

      <!-- Profile Tabs -->
      <div class="profile-tabs animate-fade-in-up animate-stagger-3">
        <div class="tabs-header">
          <button
            v-for="tab in availableTabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="tab-button hover-glow"
            :class="{ active: activeTab === tab.id }"
          >
            <i :class="tab.icon"></i>
            {{ tab.label }}
          </button>
        </div>

        <div class="tabs-content">
          <!-- User Recordings Tab -->
          <div
            v-if="activeTab === 'recordings'"
            class="tab-content animate-fade-in-up"
          >
            <div v-if="loadingRecordings" class="loading">
              <div class="loading-spinner"></div>
              <p class="loading-dots">Загрузка записей</p>
            </div>

            <div v-else-if="userRecordings.length > 0" class="recordings-grid">
              <div
                v-for="(recording, index) in userRecordings"
                :key="recording.id"
                class="recording-card hover-lift animate-fade-in-up"
                :class="`animate-stagger-${Math.min(index + 1, 5)}`"
                @click="viewRecording(recording.id)"
              >
                <div class="recording-image" v-if="recording.image_path">
                  <img
                    :src="getImageUrl(recording.image_path)"
                    :alt="recording.title"
                  />
                </div>
                <div v-else class="recording-placeholder">
                  <i class="fas fa-video"></i>
                </div>

                <div class="recording-content">
                  <h3 class="recording-title">{{ recording.title }}</h3>
                  <p class="recording-excerpt">
                    {{ truncateText(recording.content, 100) }}
                  </p>
                  <div class="recording-meta">
                    <span class="recording-date">
                      <i class="fas fa-calendar"></i>
                      {{ formatDate(recording.created_at) }}
                    </span>
                    <span class="recording-views">
                      <i class="fas fa-eye"></i>
                      {{ recording.views || 0 }}
                    </span>
                    <span class="recording-category" v-if="recording.category">
                      <i class="fas fa-folder"></i>
                      {{ recording.category.name }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="empty-state">
              <i class="fas fa-video animate-float"></i>
              <h3>Нет записей</h3>
              <p>
                {{
                  isOwnProfile
                    ? 'Вы еще не создали ни одной записи'
                    : 'Пользователь еще не создал записей'
                }}
              </p>
              <router-link
                v-if="isOwnProfile && isModerator"
                to="/recordings/new"
                class="btn btn-primary"
              >
                <i class="fas fa-plus"></i>
                Создать первую запись
              </router-link>
            </div>
          </div>

          <!-- Activity Tab -->
          <div
            v-if="activeTab === 'activity'"
            class="tab-content animate-fade-in-up"
          >
            <div v-if="loadingActivity" class="loading">
              <div class="loading-spinner"></div>
              <p class="loading-dots">Загрузка активности</p>
            </div>

            <div v-else-if="userActivity.length > 0" class="activity-list">
              <div
                v-for="(activity, index) in userActivity"
                :key="activity.id"
                class="activity-item hover-lift animate-slide-in-left"
                :class="`animate-stagger-${Math.min(index + 1, 5)}`"
              >
                <div
                  class="activity-icon"
                  :class="getActivityIconClass(activity.type)"
                >
                  <i :class="getActivityIcon(activity.type)"></i>
                </div>
                <div class="activity-content">
                  <div class="activity-text">
                    {{ getActivityText(activity) }}
                  </div>
                  <div class="activity-date">
                    {{ formatRelativeDate(activity.created_at) }}
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="empty-state">
              <i class="fas fa-history animate-float"></i>
              <h3>Нет активности</h3>
              <p>
                {{
                  isOwnProfile
                    ? 'У вас пока нет активности'
                    : 'У пользователя пока нет активности'
                }}
              </p>
            </div>
          </div>

          <!-- Settings Tab (only for own profile) -->
          <div
            v-if="activeTab === 'settings' && isOwnProfile"
            class="tab-content animate-fade-in-up"
          >
            <div class="settings-section">
              <h3>Уведомления</h3>
              <div class="settings-group">
                <div class="setting-item">
                  <label class="setting-label">
                    <input
                      v-model="userSettings.emailNotifications"
                      type="checkbox"
                      class="setting-checkbox"
                      @change="updateSettings"
                    />
                    <span class="checkmark"></span>
                    Email уведомления
                  </label>
                  <p class="setting-description">
                    Получать уведомления на email
                  </p>
                </div>

                <div class="setting-item">
                  <label class="setting-label">
                    <input
                      v-model="userSettings.pushNotifications"
                      type="checkbox"
                      class="setting-checkbox"
                      @change="updateSettings"
                    />
                    <span class="checkmark"></span>
                    Push уведомления
                  </label>
                  <p class="setting-description">
                    Получать push уведомления в браузере
                  </p>
                </div>
              </div>
            </div>

            <div class="settings-section">
              <h3>Приватность</h3>
              <div class="settings-group">
                <div class="setting-item">
                  <label class="setting-label">
                    <input
                      v-model="userSettings.publicProfile"
                      type="checkbox"
                      class="setting-checkbox"
                      @change="updateSettings"
                    />
                    <span class="checkmark"></span>
                    Публичный профиль
                  </label>
                  <p class="setting-description">
                    Разрешить другим пользователям видеть ваш профиль
                  </p>
                </div>

                <div class="setting-item">
                  <label class="setting-label">
                    <input
                      v-model="userSettings.showEmail"
                      type="checkbox"
                      class="setting-checkbox"
                      @change="updateSettings"
                    />
                    <span class="checkmark"></span>
                    Показывать email
                  </label>
                  <p class="setting-description">
                    Показывать email адрес в профиле
                  </p>
                </div>
              </div>
            </div>

            <div class="settings-section danger-zone">
              <h3>Опасная зона</h3>
              <div class="settings-group">
                <button
                  @click="showChangePasswordModal = true"
                  class="btn btn-warning"
                >
                  <i class="fas fa-key"></i>
                  Изменить пароль
                </button>
                <button
                  @click="showDeleteAccountModal = true"
                  class="btn btn-danger"
                >
                  <i class="fas fa-trash"></i>
                  Удалить аккаунт
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals remain the same -->
    <!-- Edit Profile Modal -->
    <div
      v-if="showEditModal"
      class="modal-overlay animate-fade-in"
      @click="showEditModal = false"
    >
      <div class="modal animate-zoom-in" @click.stop>
        <div class="modal-header">
          <h3 class="animate-glow">Редактировать профиль</h3>
          <button
            @click="showEditModal = false"
            class="modal-close hover-scale"
          >
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
              />
            </div>
            <div class="form-group">
              <label class="form-label">Email</label>
              <input
                v-model="editForm.email"
                type="email"
                class="form-input"
                required
              />
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
          <button
            @click="updateProfile"
            class="btn btn-primary"
            :disabled="updatingProfile"
          >
            <i class="fas fa-spinner animate-spin" v-if="updatingProfile"></i>
            <i class="fas fa-save" v-else></i>
            {{ updatingProfile ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <div
      v-if="showChangePasswordModal"
      class="modal-overlay animate-fade-in"
      @click="showChangePasswordModal = false"
    >
      <div class="modal animate-zoom-in" @click.stop>
        <div class="modal-header">
          <h3 class="animate-glow">Изменить пароль</h3>
          <button
            @click="showChangePasswordModal = false"
            class="modal-close hover-scale"
          >
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
              />
            </div>
            <div class="form-group">
              <label class="form-label">Новый пароль</label>
              <input
                v-model="passwordForm.newPassword"
                type="password"
                class="form-input"
                required
                minlength="6"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Подтвердите новый пароль</label>
              <input
                v-model="passwordForm.confirmPassword"
                type="password"
                class="form-input"
                required
              />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            @click="showChangePasswordModal = false"
            class="btn btn-secondary"
          >
            Отмена
          </button>
          <button
            @click="changePassword"
            class="btn btn-primary"
            :disabled="changingPassword"
          >
            <i class="fas fa-spinner animate-spin" v-if="changingPassword"></i>
            <i class="fas fa-key" v-else></i>
            {{ changingPassword ? 'Изменение...' : 'Изменить пароль' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Avatar Upload Modal -->
    <div
      v-if="showAvatarUpload"
      class="modal-overlay animate-fade-in"
      @click="showAvatarUpload = false"
    >
      <div class="modal animate-zoom-in" @click.stop>
        <div class="modal-header">
          <h3 class="animate-glow">Изменить аватар</h3>
          <button
            @click="showAvatarUpload = false"
            class="modal-close hover-scale"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="avatar-upload-container">
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              @change="handleAvatarUpload"
              class="file-input"
              id="avatar-upload"
            />
            <label for="avatar-upload" class="avatar-upload-label hover-lift">
              <i class="fas fa-cloud-upload-alt"></i>
              <span>Выбрать изображение</span>
            </label>
            <div v-if="avatarPreview" class="avatar-preview animate-scale-in">
              <img
                :src="avatarPreview"
                alt="Avatar Preview"
                class="preview-avatar"
              />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAvatarUpload = false" class="btn btn-secondary">
            Отмена
          </button>
          <button
            @click="uploadAvatar"
            class="btn btn-primary"
            :disabled="!avatarFile || uploadingAvatar"
          >
            <i class="fas fa-spinner animate-spin" v-if="uploadingAvatar"></i>
            <i class="fas fa-upload" v-else></i>
            {{ uploadingAvatar ? 'Загрузка...' : 'Загрузить' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import axios from 'axios'

export default {
  name: 'Profile',
  props: {
    userId: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      activeTab: 'recordings',
      targetUser: null,
      userStats: {},
      userRecordings: [],
      userActivity: [],
      userSettings: {
        emailNotifications: true,
        pushNotifications: false,
        publicProfile: true,
        showEmail: false
      },
      loadingRecordings: false,
      loadingActivity: false,
      loadingProfile: false,
      showEditModal: false,
      showSettingsModal: false,
      showChangePasswordModal: false,
      showAvatarUpload: false,
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
      avatarPreview: null,
      updatingProfile: false,
      changingPassword: false,
      uploadingAvatar: false,
      tabs: [
        { id: 'recordings', label: 'Записи', icon: 'fas fa-video' },
        { id: 'activity', label: 'Активность', icon: 'fas fa-history' },
        { id: 'settings', label: 'Настройки', icon: 'fas fa-cog' }
      ]
    }
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated', 'isModerator', 'isAdmin']),
    adminPanelUrl() {
      return 'http://localhost:5000/admin'
    },
    isOwnProfile() {
      return !this.userId || this.userId == this.user?.id
    },
    profileUser() {
      return this.isOwnProfile ? this.user : this.targetUser
    },
    availableTabs() {
      if (this.isOwnProfile) {
        return this.tabs
      }
      return this.tabs.filter((tab) => tab.id !== 'settings')
    }
  },
  async created() {
    await this.loadProfileData()
  },
  watch: {
    activeTab(newTab) {
      if (newTab === 'recordings' && this.userRecordings.length === 0) {
        this.fetchUserRecordings()
      } else if (newTab === 'activity' && this.userActivity.length === 0) {
        this.fetchUserActivity()
      }
    },
    userId: {
      handler() {
        this.loadProfileData()
      },
      immediate: false
    }
  },
  methods: {
    async loadProfileData() {
      this.loadingProfile = true
      try {
        // If viewing another user's profile, fetch their data
        if (!this.isOwnProfile) {
          await this.fetchTargetUser()
        }

        // Load user stats
        const targetUserId = this.userId || this.user?.id
        if (targetUserId) {
          await this.fetchUserStats(targetUserId)

          // Load user settings if own profile
          if (this.isOwnProfile) {
            await this.fetchUserSettings()
            this.editForm = {
              username: this.user.username,
              email: this.user.email,
              bio: this.user.bio || ''
            }
          }

          // Load initial tab data
          if (this.activeTab === 'recordings') {
            await this.fetchUserRecordings()
          }
        }
      } catch (error) {
        console.error('Error loading profile data:', error)
        this.$toast.error('Ошибка загрузки профиля')
      } finally {
        this.loadingProfile = false
      }
    },

    async fetchTargetUser() {
      try {
        const response = await axios.get(`/api/users/${this.userId}`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`
          }
        })
        this.targetUser = response.data
      } catch (error) {
        console.error('Error fetching target user:', error)
        this.$toast.error('Пользователь не найден')
        this.$router.push('/')
      }
    },

    async fetchUserStats(userId) {
      try {
        const response = await axios.get(`/api/users/${userId}/stats`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`
          }
        })
        this.userStats = response.data
      } catch (error) {
        console.error('Error fetching user stats:', error)
        this.userStats = {
          recordings: 0,
          total_views: 0,
          likes: 0,
          rating: 0
        }
      }
    },

    async fetchUserRecordings() {
      this.loadingRecordings = true
      try {
        const targetUserId = this.userId || this.user?.id
        const response = await axios.get(
          `/api/users/${targetUserId}/recordings`,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`
            }
          }
        )
        this.userRecordings = response.data
      } catch (error) {
        console.error('Error fetching user recordings:', error)
        this.userRecordings = []
      } finally {
        this.loadingRecordings = false
      }
    },

    async fetchUserActivity() {
      this.loadingActivity = true
      try {
        const targetUserId = this.userId || this.user?.id
        const response = await axios.get(
          `/api/users/${targetUserId}/activity`,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`
            }
          }
        )
        this.userActivity = response.data
      } catch (error) {
        console.error('Error fetching user activity:', error)
        this.userActivity = []
      } finally {
        this.loadingActivity = false
      }
    },

    async fetchUserSettings() {
      try {
        const response = await axios.get('/api/user/settings', {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`
          }
        })
        this.userSettings = { ...this.userSettings, ...response.data }
      } catch (error) {
        console.error('Error fetching user settings:', error)
      }
    },

    async updateProfile() {
      if (
        this.editForm.username.trim() === '' ||
        this.editForm.email.trim() === ''
      ) {
        this.$toast.error('Имя пользователя и email обязательны')
        return
      }

      this.updatingProfile = true
      try {
        await this.$store.dispatch('updateUserProfile', this.editForm)
        this.showEditModal = false
        this.$toast.success('Профиль обновлен успешно')
      } catch (error) {
        console.error('Error updating profile:', error)
        this.$toast.error('Ошибка обновления профиля')
      } finally {
        this.updatingProfile = false
      }
    },

    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.$toast.error('Пароли не совпадают')
        return
      }

      if (this.passwordForm.newPassword.length < 6) {
        this.$toast.error('Пароль должен содержать минимум 6 символов')
        return
      }

      this.changingPassword = true
      try {
        await axios.post('/api/user/change-password', this.passwordForm, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`
          }
        })
        this.showChangePasswordModal = false
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        this.$toast.success('Пароль изменен успешно')
      } catch (error) {
        console.error('Error changing password:', error)
        this.$toast.error(
          error.response?.data?.message || 'Ошибка изменения пароля'
        )
      } finally {
        this.changingPassword = false
      }
    },

    async updateSettings() {
      try {
        await axios.put('/api/user/settings', this.userSettings, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`
          }
        })
        this.$toast.success('Настройки сохранены')
      } catch (error) {
        console.error('Error updating settings:', error)
        this.$toast.error('Ошибка сохранения настроек')
      }
    },

    handleAvatarUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      if (!file.type.startsWith('image/')) {
        this.$toast.error('Пожалуйста, выберите изображение')
        return
      }

      if (file.size > 2 * 1024 * 1024) {
        this.$toast.error('Размер изображения не должен превышать 2MB')
        return
      }

      this.avatarFile = file

      const reader = new FileReader()
      reader.onload = (e) => {
        this.avatarPreview = e.target.result
      }
      reader.readAsDataURL(file)
    },

    async uploadAvatar() {
      if (!this.avatarFile) return

      this.uploadingAvatar = true
      try {
        const formData = new FormData()
        formData.append('avatar', this.avatarFile)

        await axios.post('/api/user/avatar', formData, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
            'Content-Type': 'multipart/form-data'
          }
        })

        this.showAvatarUpload = false
        this.avatarFile = null
        this.avatarPreview = null
        this.$toast.success('Аватар загружен успешно')

        // Refresh user data
        await this.$store.dispatch('fetchUser')
      } catch (error) {
        console.error('Error uploading avatar:', error)
        this.$toast.error('Ошибка загрузки аватара')
      } finally {
        this.uploadingAvatar = false
      }
    },

    viewRecording(id) {
      this.$router.push(`/recordings/${id}`)
    },

    getImageUrl(imagePath) {
      if (!imagePath) return null
      if (imagePath.startsWith('http')) return imagePath
      if (imagePath.startsWith('/uploads/')) {
        return `http://localhost:5000${imagePath}`
      }
      return `http://localhost:5000/uploads/${imagePath}`
    },

    getRoleBadgeClass(role) {
      const classes = {
        admin: 'badge-admin',
        moderator: 'badge-moderator',
        user: 'badge-user'
      }
      return classes[role] || 'badge-user'
    },

    getRoleIcon(role) {
      const icons = {
        admin: 'fas fa-crown',
        moderator: 'fas fa-shield-alt',
        user: 'fas fa-user'
      }
      return icons[role] || 'fas fa-user'
    },

    getRoleText(role) {
      const texts = {
        admin: 'Администратор',
        moderator: 'Модератор',
        user: 'Пользователь'
      }
      return texts[role] || 'Пользователь'
    },

    getActivityIconClass(type) {
      const classes = {
        create: 'activity-create',
        update: 'activity-update',
        delete: 'activity-delete',
        view: 'activity-view'
      }
      return classes[type] || 'activity-default'
    },

    getActivityIcon(type) {
      const icons = {
        create: 'fas fa-plus',
        update: 'fas fa-edit',
        delete: 'fas fa-trash',
        view: 'fas fa-eye'
      }
      return icons[type] || 'fas fa-circle'
    },

    getActivityText(activity) {
      const texts = {
        create: `Создал запись "${activity.title}"`,
        update: `Обновил запись "${activity.title}"`,
        delete: `Удалил запись "${activity.title}"`,
        view: `Просмотрел запись "${activity.title}"`
      }
      return texts[activity.type] || 'Неизвестное действие'
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
    },

    formatRelativeDate(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date

      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)

      if (minutes < 1) return 'Только что'
      if (minutes < 60) return `${minutes} мин назад`
      if (hours < 24) return `${hours} ч назад`
      if (days < 7) return `${days} дн назад`

      return this.formatDate(dateString)
    }
  }
}
</script>
<style scoped>
recording-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.admin-access-banner {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  padding: 1rem 0;
}
.recording-date,
.recording-views,
.recording-category {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.recording-category {
  background: rgba(255, 215, 0, 0.1);
  color: #ffd700;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
}

.loading-profile {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  flex-direction: column;
  gap: 1rem;
}

.profile-error {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.6);
}

.profile-error i {
  font-size: 4rem;
  margin-bottom: 1rem;
  color: #e74c3c;
}

@media (max-width: 768px) {
  .recording-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .recording-category {
    align-self: flex-end;
  }
}
.profile {
  padding: 2rem 0;
  min-height: 100vh;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 3rem;
  padding: 2rem;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-image,
.avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.avatar-image {
  object-fit: cover;
}

.avatar-placeholder {
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 3rem;
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.avatar-edit:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.profile-email {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 1rem;
}

.profile-badges {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.badge i {
  margin-right: 0.5rem;
}

.badge-admin {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.badge-moderator {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.3);
}

.badge-user {
  background: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.badge-date {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.profile-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #1e3c72;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.profile-tabs {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.tabs-header {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-button {
  flex: 1;
  padding: 1.5rem;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.tab-button:hover {
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.05);
}

.tab-button.active {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
  border-bottom: 2px solid #ffd700;
}

.tabs-content {
  padding: 2rem;
}

.recordings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.recording-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.recording-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 215, 0, 0.3);
}

.recording-image {
  height: 150px;
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
  height: 150px;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.4);
  font-size: 2rem;
}

.recording-content {
  padding: 1.5rem;
}

.recording-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.recording-excerpt {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.recording-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
}

.recording-date,
.recording-views {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateX(5px);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.activity-create {
  background: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
}

.activity-update {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
}

.activity-delete {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.activity-view {
  background: rgba(155, 89, 182, 0.2);
  color: #9b59b6;
}

.activity-default {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.activity-date {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
}

.settings-section {
  margin-bottom: 2rem;
}

.settings-section h3 {
  color: #ffd700;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.setting-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.setting-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
}

.setting-checkbox {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  margin-right: 0.75rem;
  position: relative;
  transition: all 0.3s ease;
}

.setting-checkbox:checked + .checkmark {
  background: #ffd700;
  border-color: #ffd700;
}

.setting-checkbox:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #1e3c72;
  font-weight: bold;
  font-size: 0.8rem;
}

.setting-description {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  margin: 0;
}

.danger-zone {
  border: 1px solid rgba(231, 76, 60, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  background: rgba(231, 76, 60, 0.05);
}

.danger-zone h3 {
  color: #e74c3c;
  border-bottom-color: rgba(231, 76, 60, 0.3);
}

.danger-zone .settings-group {
  flex-direction: row;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.6);
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.3);
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.8);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.6);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-left: 4px solid #ffd700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.loading-dots::after {
  content: '';
  animation: dots 1.5s steps(5, end) infinite;
}

@keyframes dots {
  0%,
  20% {
    content: '.';
  }
  40% {
    content: '..';
  }
  60% {
    content: '...';
  }
  90%,
  100% {
    content: '';
  }
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
  font-size: 1.3rem;
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
  color: #ffd700;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
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

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.avatar-upload-container {
  text-align: center;
}

.file-input {
  display: none;
}

.avatar-upload-label {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.7);
}

.avatar-upload-label:hover {
  border-color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
  color: #ffd700;
}

.avatar-upload-label i {
  font-size: 2rem;
}

.avatar-preview {
  margin-top: 1rem;
}

.preview-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #ffd700;
}

/* Animations */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

.animate-zoom-in {
  animation: zoomIn 0.3s ease-out;
}

.animate-scale-in {
  animation: scaleIn 0.4s ease-out;
}

.animate-slide-in-left {
  animation: slideInLeft 0.5s ease-out;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite alternate;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-spin {
  animation: spin 1s linear infinite;
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

.hover-scale:hover {
  transform: scale(1.05);
}

.hover-lift:hover {
  transform: translateY(-5px);
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
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

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.3);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes glow {
  from {
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  }
  to {
    text-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }

  .profile-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .tabs-header {
    flex-direction: column;
  }

  .tab-button {
    padding: 1rem;
  }

  .recordings-grid {
    grid-template-columns: 1fr;
  }

  .danger-zone .settings-group {
    flex-direction: column;
  }

  .modal {
    margin: 1rem;
  }

  .modal-footer {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .profile {
    padding: 1rem 0;
  }

  .profile-header {
    padding: 1.5rem;
  }

  .profile-name {
    font-size: 2rem;
  }

  .profile-stats {
    grid-template-columns: 1fr;
  }

  .tabs-content {
    padding: 1rem;
  }
}
</style>
