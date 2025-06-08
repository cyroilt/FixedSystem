<template>
  <div class="admin">
    <div class="container">
      <!-- Admin Header -->
      <div class="admin-header" data-aos="fade-up">
        <h1>Панель администратора</h1>
        <p>Управление порталом и контентом</p>
      </div>

      <!-- Admin Navigation -->
      <div class="admin-nav" data-aos="fade-up" data-aos-delay="100">
        <button
          v-for="tab in adminTabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="['nav-btn', { active: activeTab === tab.key }]"
        >
          <i :class="tab.icon"></i>
          {{ tab.label }}
          <span v-if="tab.badge" class="badge">{{ tab.badge }}</span>
        </button>
      </div>

      <!-- Tab Content -->
      <div class="admin-content" data-aos="fade-up" data-aos-delay="200">
        <!-- Dashboard Tab -->
        <div v-if="activeTab === 'dashboard'" class="dashboard-tab">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-users"></i>
              </div>
              <div class="stat-info">
                <h3>{{ stats.totalUsers }}</h3>
                <p>Всего пользователей</p>
                <span class="stat-change positive"
                  >+{{ stats.newUsersToday }} сегодня</span
                >
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-file-alt"></i>
              </div>
              <div class="stat-info">
                <h3>{{ stats.totalRecordings }}</h3>
                <p>Всего записей</p>
                <span class="stat-change positive"
                  >+{{ stats.newRecordingsToday }} сегодня</span
                >
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-eye"></i>
              </div>
              <div class="stat-info">
                <h3>{{ formatNumber(stats.totalViews) }}</h3>
                <p>Всего просмотров</p>
                <span class="stat-change positive"
                  >+{{ formatNumber(stats.viewsToday) }} сегодня</span
                >
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-exclamation-triangle"></i>
              </div>
              <div class="stat-info">
                <h3>{{ stats.pendingReports }}</h3>
                <p>Жалобы на рассмотрении</p>
                <span
                  class="stat-change negative"
                  v-if="stats.pendingReports > 0"
                  >Требует внимания</span
                >
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="recent-activity">
            <h3>Последняя активность</h3>
            <div class="activity-list">
              <div
                v-for="activity in recentActivity"
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-icon">
                  <i :class="getActivityIcon(activity.type)"></i>
                </div>
                <div class="activity-content">
                  <p class="activity-text">{{ activity.description }}</p>
                  <span class="activity-time">{{
                    formatDate(activity.created_at, 'relative')
                  }}</span>
                </div>
                <div class="activity-actions" v-if="activity.actionable">
                  <button
                    @click="handleActivityAction(activity)"
                    class="btn btn-sm btn-primary"
                  >
                    Просмотреть
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Users Tab -->
        <div v-if="activeTab === 'users'" class="users-tab">
          <div class="tab-header">
            <h3>Управление пользователями</h3>
            <div class="tab-actions">
              <div class="search-box">
                <i class="fas fa-search"></i>
                <input
                  v-model="userSearch"
                  type="text"
                  placeholder="Поиск пользователей..."
                  class="search-input"
                />
              </div>
              <select v-model="userFilter" class="filter-select">
                <option value="all">Все пользователи</option>
                <option value="admin">Администраторы</option>
                <option value="moderator">Модераторы</option>
                <option value="user">Обычные пользователи</option>
                <option value="banned">Заблокированные</option>
              </select>
            </div>
          </div>

          <div class="users-table">
            <table>
              <thead>
                <tr>
                  <th>Пользователь</th>
                  <th>Email</th>
                  <th>Роль</th>
                  <th>Регистрация</th>
                  <th>Статус</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>
                    <div class="user-info">
                      <div class="user-avatar">
                        <i class="fas fa-user"></i>
                      </div>
                      <div>
                        <div class="user-name">{{ user.username }}</div>
                        <div class="user-id">ID: {{ user.id }}</div>
                      </div>
                    </div>
                  </td>
                  <td>{{ user.email }}</td>
                  <td>
                    <select
                      v-model="user.role"
                      @change="updateUserRole(user)"
                      class="role-select"
                      :disabled="user.id === currentUser.id"
                    >
                      <option value="user">Пользователь</option>
                      <option value="moderator">Модератор</option>
                      <option value="admin">Администратор</option>
                    </select>
                  </td>
                  <td>{{ formatDate(user.created_at) }}</td>
                  <td>
                    <span :class="['status-badge', user.status]">
                      {{ getStatusLabel(user.status) }}
                    </span>
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button
                        @click="viewUser(user)"
                        class="action-btn view-btn"
                        title="Просмотреть профиль"
                      >
                        <i class="fas fa-eye"></i>
                      </button>
                      <button
                        @click="toggleUserStatus(user)"
                        :class="[
                          'action-btn',
                          user.status === 'active' ? 'ban-btn' : 'unban-btn'
                        ]"
                        :title="
                          user.status === 'active'
                            ? 'Заблокировать'
                            : 'Разблокировать'
                        "
                        :disabled="user.id === currentUser.id"
                      >
                        <i
                          :class="
                            user.status === 'active'
                              ? 'fas fa-ban'
                              : 'fas fa-check'
                          "
                        ></i>
                      </button>
                      <button
                        @click="deleteUser(user)"
                        class="action-btn delete-btn"
                        title="Удалить пользователя"
                        :disabled="user.id === currentUser.id"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="pagination" v-if="userPagination.totalPages > 1">
            <button
              @click="loadUsers(userPagination.currentPage - 1)"
              :disabled="userPagination.currentPage === 1"
              class="pagination-btn"
            >
              <i class="fas fa-chevron-left"></i>
            </button>
            <span class="pagination-info">
              Страница {{ userPagination.currentPage }} из
              {{ userPagination.totalPages }}
            </span>
            <button
              @click="loadUsers(userPagination.currentPage + 1)"
              :disabled="
                userPagination.currentPage === userPagination.totalPages
              "
              class="pagination-btn"
            >
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>

        <!-- Recordings Tab -->
        <div v-if="activeTab === 'recordings'" class="recordings-tab">
          <div class="tab-header">
            <h3>Управление записями</h3>
            <div class="tab-actions">
              <div class="search-box">
                <i class="fas fa-search"></i>
                <input
                  v-model="recordingSearch"
                  type="text"
                  placeholder="Поиск записей..."
                  class="search-input"
                />
              </div>
              <select v-model="recordingFilter" class="filter-select">
                <option value="all">Все записи</option>
                <option value="published">Опубликованные</option>
                <option value="draft">Черновики</option>
                <option value="pending">На модерации</option>
                <option value="reported">С жалобами</option>
              </select>
            </div>
          </div>

          <div class="recordings-grid">
            <div
              v-for="recording in filteredRecordings"
              :key="recording.id"
              class="recording-card"
            >
              <div class="recording-image" v-if="recording.image_path">
                <img :src="recording.image_path" :alt="recording.title" />
              </div>
              <div class="recording-content">
                <div class="recording-meta">
                  <span :class="['recording-status', recording.status]">
                    {{ getStatusLabel(recording.status) }}
                  </span>
                  <span class="recording-date">{{
                    formatDate(recording.created_at)
                  }}</span>
                </div>
                <h4 class="recording-title">{{ recording.title }}</h4>
                <p class="recording-author">
                  Автор: {{ recording.author?.username }}
                </p>
                <p class="recording-excerpt">
                  {{ truncateText(recording.content, 100) }}
                </p>
                <div class="recording-stats">
                  <span
                    ><i class="fas fa-eye"></i> {{ recording.views || 0 }}</span
                  >
                  <span
                    ><i class="fas fa-heart"></i>
                    {{ recording.likes || 0 }}</span
                  >
                  <span
                    v-if="recording.reports_count > 0"
                    class="reports-count"
                  >
                    <i class="fas fa-flag"></i> {{ recording.reports_count }}
                  </span>
                </div>
              </div>
              <div class="recording-actions">
                <button
                  @click="viewRecording(recording.id)"
                  class="action-btn view-btn"
                >
                  <i class="fas fa-eye"></i>
                </button>
                <button
                  @click="editRecording(recording.id)"
                  class="action-btn edit-btn"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button
                  @click="toggleRecordingStatus(recording)"
                  :class="[
                    'action-btn',
                    recording.status === 'published'
                      ? 'hide-btn'
                      : 'publish-btn'
                  ]"
                >
                  <i
                    :class="
                      recording.status === 'published'
                        ? 'fas fa-eye-slash'
                        : 'fas fa-check'
                    "
                  ></i>
                </button>
                <button
                  @click="deleteRecording(recording)"
                  class="action-btn delete-btn"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Reports Tab -->
        <div v-if="activeTab === 'reports'" class="reports-tab">
          <div class="tab-header">
            <h3>Жалобы и модерация</h3>
            <div class="tab-actions">
              <select v-model="reportFilter" class="filter-select">
                <option value="pending">Ожидают рассмотрения</option>
                <option value="resolved">Рассмотренные</option>
                <option value="all">Все жалобы</option>
              </select>
            </div>
          </div>

          <div class="reports-list">
            <div
              v-for="report in filteredReports"
              :key="report.id"
              class="report-card"
            >
              <div class="report-header">
                <div class="report-info">
                  <h4>{{ getReportTypeLabel(report.type) }}</h4>
                  <p class="report-meta">
                    От: {{ report.reporter?.username }} •
                    {{ formatDate(report.created_at, 'relative') }}
                  </p>
                </div>
                <span :class="['report-status', report.status]">
                  {{ getStatusLabel(report.status) }}
                </span>
              </div>

              <div class="report-content">
                <p class="report-reason">{{ report.reason }}</p>
                <div class="report-target" v-if="report.recording">
                  <h5>Запись: {{ report.recording.title }}</h5>
                  <p>Автор: {{ report.recording.author?.username }}</p>
                </div>
              </div>

              <div class="report-actions" v-if="report.status === 'pending'">
                <button
                  @click="resolveReport(report, 'dismissed')"
                  class="btn btn-secondary"
                >
                  Отклонить
                </button>
                <button
                  @click="resolveReport(report, 'action_taken')"
                  class="btn btn-primary"
                >
                  Принять меры
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Settings Tab -->
        <div v-if="activeTab === 'settings'" class="settings-tab">
          <div class="settings-sections">
            <div class="settings-section">
              <h3>Общие настройки</h3>
              <div class="setting-group">
                <label class="setting-label">
                  Название сайта
                  <input
                    v-model="siteSettings.siteName"
                    type="text"
                    class="setting-input"
                  />
                </label>
              </div>
              <div class="setting-group">
                <label class="setting-label">
                  Описание сайта
                  <textarea
                    v-model="siteSettings.siteDescription"
                    class="setting-textarea"
                    rows="3"
                  ></textarea>
                </label>
              </div>
              <div class="setting-group">
                <label class="setting-checkbox">
                  <input
                    v-model="siteSettings.registrationEnabled"
                    type="checkbox"
                  />
                  <span class="checkmark"></span>
                  Разрешить регистрацию новых пользователей
                </label>
              </div>
            </div>

            <div class="settings-section">
              <h3>Модерация контента</h3>
              <div class="setting-group">
                <label class="setting-checkbox">
                  <input
                    v-model="moderationSettings.autoModeration"
                    type="checkbox"
                  />
                  <span class="checkmark"></span>
                  Автоматическая модерация
                </label>
              </div>
              <div class="setting-group">
                <label class="setting-checkbox">
                  <input
                    v-model="moderationSettings.requireApproval"
                    type="checkbox"
                  />
                  <span class="checkmark"></span>
                  Требовать одобрение новых записей
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
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  name: 'Admin',
  data() {
    return {
      activeTab: 'dashboard',
      stats: {
        totalUsers: 0,
        newUsersToday: 0,
        totalRecordings: 0,
        newRecordingsToday: 0,
        totalViews: 0,
        viewsToday: 0,
        pendingReports: 0
      },
      recentActivity: [],
      users: [],
      recordings: [],
      reports: [],
      userSearch: '',
      userFilter: 'all',
      recordingSearch: '',
      recordingFilter: 'all',
      reportFilter: 'pending',
      userPagination: {
        currentPage: 1,
        totalPages: 1,
        perPage: 20
      },
      siteSettings: {
        siteName: '',
        siteDescription: '',
        registrationEnabled: true
      },
      moderationSettings: {
        autoModeration: false,
        requireApproval: false
      },
      adminTabs: [
        {
          key: 'dashboard',
          label: 'Панель управления',
          icon: 'fas fa-tachometer-alt'
        },
        { key: 'users', label: 'Пользователи', icon: 'fas fa-users' },
        { key: 'recordings', label: 'Записи', icon: 'fas fa-file-alt' },
        { key: 'reports', label: 'Жалобы', icon: 'fas fa-flag', badge: 0 },
        { key: 'settings', label: 'Настройки', icon: 'fas fa-cog' }
      ]
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin']),
    ...mapState(['user']),
    currentUser() {
      return this.user
    },
    filteredUsers() {
      let filtered = this.users

      if (this.userSearch) {
        const search = this.userSearch.toLowerCase()
        filtered = filtered.filter(
          (user) =>
            user.username.toLowerCase().includes(search) ||
            user.email.toLowerCase().includes(search)
        )
      }

      if (this.userFilter !== 'all') {
        if (this.userFilter === 'banned') {
          filtered = filtered.filter((user) => user.status === 'banned')
        } else {
          filtered = filtered.filter((user) => user.role === this.userFilter)
        }
      }

      return filtered
    },
    filteredRecordings() {
      let filtered = this.recordings

      if (this.recordingSearch) {
        const search = this.recordingSearch.toLowerCase()
        filtered = filtered.filter(
          (recording) =>
            recording.title.toLowerCase().includes(search) ||
            recording.content.toLowerCase().includes(search) ||
            recording.author?.username.toLowerCase().includes(search)
        )
      }

      if (this.recordingFilter !== 'all') {
        if (this.recordingFilter === 'reported') {
          filtered = filtered.filter((recording) => recording.reports_count > 0)
        } else {
          filtered = filtered.filter(
            (recording) => recording.status === this.recordingFilter
          )
        }
      }

      return filtered
    },
    filteredReports() {
      if (this.reportFilter === 'all') return this.reports
      return this.reports.filter(
        (report) => report.status === this.reportFilter
      )
    }
  },
  async created() {
    if (!this.isAdmin) {
      this.$router.push('/')
      return
    }

    await this.loadDashboardData()
    this.updateReportsBadge()
  },
  watch: {
    activeTab(newTab) {
      switch (newTab) {
        case 'users':
          this.loadUsers()
          break
        case 'recordings':
          this.loadRecordings()
          break
        case 'reports':
          this.loadReports()
          break
        case 'settings':
          this.loadSettings()
          break
      }
    }
  },
  methods: {
    async loadDashboardData() {
      try {
        this.stats = await this.$store.dispatch('admin/fetchStats')
        this.recentActivity = await this.$store.dispatch(
          'admin/fetchRecentActivity'
        )
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      }
    },
    async loadUsers(page = 1) {
      try {
        const response = await this.$store.dispatch('admin/fetchUsers', {
          page,
          perPage: this.userPagination.perPage,
          search: this.userSearch,
          filter: this.userFilter
        })
        this.users = response.data
        this.userPagination = {
          currentPage: response.currentPage,
          totalPages: response.totalPages,
          perPage: response.perPage
        }
      } catch (error) {
        console.error('Error loading users:', error)
      }
    },
    async loadRecordings() {
      try {
        this.recordings = await this.$store.dispatch('admin/fetchRecordings', {
          search: this.recordingSearch,
          filter: this.recordingFilter
        })
      } catch (error) {
        console.error('Error loading recordings:', error)
      }
    },
    async loadReports() {
      try {
        this.reports = await this.$store.dispatch('admin/fetchReports', {
          filter: this.reportFilter
        })
      } catch (error) {
        console.error('Error loading reports:', error)
      }
    },
    async loadSettings() {
      try {
        const settings = await this.$store.dispatch('admin/fetchSettings')
        this.siteSettings = settings.site
        this.moderationSettings = settings.moderation
      } catch (error) {
        console.error('Error loading settings:', error)
      }
    },
    async updateUserRole(user) {
      try {
        await this.$store.dispatch('admin/updateUserRole', {
          userId: user.id,
          role: user.role
        })
        this.$toast.success('Роль пользователя обновлена')
      } catch (error) {
        console.error('Error updating user role:', error)
        this.$toast.error('Ошибка при обновлении роли')
      }
    },
    async toggleUserStatus(user) {
      const newStatus = user.status === 'active' ? 'banned' : 'active'
      const action = newStatus === 'banned' ? 'заблокировать' : 'разблокировать'

      if (
        !confirm(
          `Вы уверены, что хотите ${action} пользователя ${user.username}?`
        )
      ) {
        return
      }

      try {
        await this.$store.dispatch('admin/updateUserStatus', {
          userId: user.id,
          status: newStatus
        })
        user.status = newStatus
        this.$toast.success(
          `Пользователь ${user.username} ${
            newStatus === 'banned' ? 'заблокирован' : 'разблокирован'
          }`
        )
      } catch (error) {
        console.error('Error updating user status:', error)
        this.$toast.error('Ошибка при изменении статуса пользователя')
      }
    },
    async deleteUser(user) {
      if (
        !confirm(
          `Вы уверены, что хотите удалить пользователя ${user.username}? Это действие необратимо.`
        )
      ) {
        return
      }

      try {
        await this.$store.dispatch('admin/deleteUser', user.id)
        this.users = this.users.filter((u) => u.id !== user.id)
        this.$toast.success('Пользователь удален')
      } catch (error) {
        console.error('Error deleting user:', error)
        this.$toast.error('Ошибка при удалении пользователя')
      }
    },
    viewUser(user) {
      this.$router.push(`/profile/${user.id}`)
    },
    viewRecording(id) {
      this.$router.push(`/recordings/${id}`)
    },
    editRecording(id) {
      this.$router.push(`/recordings/${id}/edit`)
    },
    async toggleRecordingStatus(recording) {
      const newStatus = recording.status === 'published' ? 'draft' : 'published'
      const action = newStatus === 'published' ? 'опубликовать' : 'скрыть'

      if (
        !confirm(
          `Вы уверены, что хотите ${action} запись "${recording.title}"?`
        )
      ) {
        return
      }

      try {
        await this.$store.dispatch('admin/updateRecordingStatus', {
          recordingId: recording.id,
          status: newStatus
        })
        recording.status = newStatus
        this.$toast.success(
          `Запись ${newStatus === 'published' ? 'опубликована' : 'скрыта'}`
        )
      } catch (error) {
        console.error('Error updating recording status:', error)
        this.$toast.error('Ошибка при изменении статуса записи')
      }
    },
    async deleteRecording(recording) {
      if (
        !confirm(
          `Вы уверены, что хотите удалить запись "${recording.title}"? Это действие необратимо.`
        )
      ) {
        return
      }

      try {
        await this.$store.dispatch('admin/deleteRecording', recording.id)
        this.recordings = this.recordings.filter((r) => r.id !== recording.id)
        this.$toast.success('Запись удалена')
      } catch (error) {
        console.error('Error deleting recording:', error)
        this.$toast.error('Ошибка при удалении записи')
      }
    },
    async resolveReport(report, resolution) {
      try {
        await this.$store.dispatch('admin/resolveReport', {
          reportId: report.id,
          resolution
        })
        report.status = 'resolved'
        report.resolution = resolution
        this.updateReportsBadge()
        this.$toast.success('Жалоба рассмотрена')
      } catch (error) {
        console.error('Error resolving report:', error)
        this.$toast.error('Ошибка при рассмотрении жалобы')
      }
    },
    async saveSettings() {
      try {
        await this.$store.dispatch('admin/updateSettings', {
          site: this.siteSettings,
          moderation: this.moderationSettings
        })
        this.$toast.success('Настройки сохранены')
      } catch (error) {
        console.error('Error saving settings:', error)
        this.$toast.error('Ошибка при сохранении настроек')
      }
    },
    handleActivityAction(activity) {
      switch (activity.type) {
        case 'new_report':
          this.activeTab = 'reports'
          break
        case 'new_user':
          this.activeTab = 'users'
          break
        case 'new_recording':
          this.viewRecording(activity.target_id)
          break
        default:
          break
      }
    },
    updateReportsBadge() {
      const pendingReports = this.reports.filter(
        (r) => r.status === 'pending'
      ).length
      const reportsTab = this.adminTabs.find((tab) => tab.key === 'reports')
      if (reportsTab) {
        reportsTab.badge = pendingReports > 0 ? pendingReports : null
      }
    },
    getActivityIcon(type) {
      const icons = {
        new_user: 'fas fa-user-plus',
        new_recording: 'fas fa-file-plus',
        new_report: 'fas fa-flag',
        user_banned: 'fas fa-user-slash',
        recording_deleted: 'fas fa-trash'
      }
      return icons[type] || 'fas fa-circle'
    },
    getStatusLabel(status) {
      const labels = {
        active: 'Активен',
        banned: 'Заблокирован',
        published: 'Опубликовано',
        draft: 'Черновик',
        pending: 'На модерации',
        resolved: 'Рассмотрено',
        dismissed: 'Отклонено',
        action_taken: 'Приняты меры'
      }
      return labels[status] || status
    },
    getReportTypeLabel(type) {
      const labels = {
        spam: 'Спам',
        inappropriate: 'Неподходящий контент',
        harassment: 'Домогательства',
        copyright: 'Нарушение авторских прав',
        other: 'Другое'
      }
      return labels[type] || type
    },
    formatNumber(num) {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    },
    formatDate(dateString, format = 'default') {
      const date = new Date(dateString)

      if (format === 'relative') {
        const now = new Date()
        const diff = now - date
        const minutes = Math.floor(diff / (1000 * 60))
        const hours = Math.floor(diff / (1000 * 60 * 60))
        const days = Math.floor(diff / (1000 * 60 * 60 * 24))

        if (minutes < 1) return 'Только что'
        if (minutes < 60) return `${minutes} мин назад`
        if (hours < 24) return `${hours} ч назад`
        if (days < 7) return `${days} дн назад`
        return date.toLocaleDateString('ru-RU')
      }

      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    truncateText(text, length) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
  }
}
</script>

<style scoped>
.admin {
  padding: 2rem 0;
  min-height: 100vh;
}

.admin-header {
  text-align: center;
  margin-bottom: 3rem;
}

.admin-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 1rem;
}

.admin-header p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.admin-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow-x: auto;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  border-radius: 12px;
  transition: all 0.3s ease;
  white-space: nowrap;
  position: relative;
}

.nav-btn:hover {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

.nav-btn.active {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.2);
}

.badge {
  background: #ef4444;
  color: #ffffff;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

.admin-content {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
}

/* Dashboard Styles */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 215, 0, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffd700;
  font-size: 1.5rem;
}

.stat-info h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 0.5rem 0;
}

.stat-info p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 0.5rem 0;
}

.stat-change {
  font-size: 0.8rem;
  font-weight: 600;
}

.stat-change.positive {
  color: #22c55e;
}

.stat-change.negative {
  color: #ef4444;
}

.recent-activity {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 2rem;
}

.recent-activity h3 {
  color: #ffd700;
  margin-bottom: 2rem;
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-bottom: 1rem;
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
  margin: 0 0 0.25rem 0;
}

.activity-time {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.activity-actions {
  flex-shrink: 0;
}

/* Tab Header Styles */
.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.tab-header h3 {
  color: #ffd700;
  margin: 0;
  font-size: 1.5rem;
}

.tab-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  position: relative;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.5);
}

.search-input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  width: 250px;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.filter-select {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
}

.filter-select option {
  background: #1e3c72;
  color: #ffffff;
}

/* Users Table Styles */
.users-table {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.users-table table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.users-table th {
  background: rgba(255, 255, 255, 0.1);
  color: #ffd700;
  font-weight: 600;
}

.users-table td {
  color: rgba(255, 255, 255, 0.9);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255, 215, 0, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffd700;
}

.user-name {
  font-weight: 600;
  color: #ffffff;
}

.user-id {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.role-select {
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: #ffffff;
}

.role-select option {
  background: #1e3c72;
  color: #ffffff;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.active {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.status-badge.banned {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
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

.view-btn {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.view-btn:hover {
  background: #3b82f6;
  color: #ffffff;
}

.edit-btn {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.edit-btn:hover {
  background: #fbbf24;
  color: #1e3c72;
}

.ban-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.ban-btn:hover {
  background: #ef4444;
  color: #ffffff;
}

.unban-btn {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.unban-btn:hover {
  background: #22c55e;
  color: #ffffff;
}

.delete-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.delete-btn:hover {
  background: #ef4444;
  color: #ffffff;
}

.hide-btn {
  background: rgba(156, 163, 175, 0.2);
  color: #9ca3af;
}

.hide-btn:hover {
  background: #9ca3af;
  color: #ffffff;
}

.publish-btn {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.publish-btn:hover {
  background: #22c55e;
  color: #ffffff;
}

/* Pagination Styles */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  color: rgba(255, 255, 255, 0.8);
}

/* Recordings Grid Styles */
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
  position: relative;
  transition: all 0.3s ease;
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
  margin-bottom: 0.5rem;
}

.recording-author {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
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

.reports-count {
  color: #ef4444 !important;
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

/* Reports Styles */
.reports-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.report-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.report-info h4 {
  color: #ffd700;
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}

.report-meta {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin: 0;
}

.report-status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.report-status.pending {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.report-status.resolved {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.report-content {
  margin-bottom: 1.5rem;
}

.report-reason {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border-left: 3px solid #ffd700;
}

.report-target {
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 8px;
}

.report-target h5 {
  color: #ffffff;
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.report-target p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 0.9rem;
}

.report-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* Settings Styles */
.settings-sections {
  max-width: 800px;
}

.settings-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.settings-section h3 {
  color: #ffd700;
  margin: 0 0 2rem 0;
  font-size: 1.3rem;
}

.setting-group {
  margin-bottom: 1.5rem;
}

.setting-label {
  display: block;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.setting-input,
.setting-textarea {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.setting-input:focus,
.setting-textarea:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.setting-input::placeholder,
.setting-textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.setting-textarea {
  resize: vertical;
  font-family: inherit;
}

.setting-checkbox {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
}

.setting-checkbox input[type='checkbox'] {
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
  flex-shrink: 0;
}

.setting-checkbox input[type='checkbox']:checked + .checkmark {
  background: #ffd700;
  border-color: #ffd700;
}

.setting-checkbox input[type='checkbox']:checked + .checkmark::after {
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
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Button Styles */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #1e3c72;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #ffed4e, #ffd700);
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  .recordings-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .admin {
    padding: 1rem 0;
  }

  .admin-nav {
    flex-direction: column;
    gap: 0.5rem;
  }

  .nav-btn {
    justify-content: center;
  }

  .tab-header {
    flex-direction: column;
    align-items: stretch;
  }

  .tab-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .search-input {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .recordings-grid {
    grid-template-columns: 1fr;
  }

  .users-table {
    overflow-x: auto;
  }

  .users-table table {
    min-width: 800px;
  }

  .report-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .report-actions {
    justify-content: stretch;
    flex-direction: column;
  }

  .action-buttons {
    justify-content: center;
  }

  .admin-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .admin-header h1 {
    font-size: 2rem;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
  }

  .activity-item {
    flex-direction: column;
    text-align: center;
  }

  .user-info {
    flex-direction: column;
    text-align: center;
  }
}

/* Loading and Empty States */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem;
  color: rgba(255, 255, 255, 0.7);
}

.loading-state i {
  font-size: 2rem;
  margin-right: 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.7);
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
  line-height: 1.6;
}

/* Scrollbar Styling */
.activity-list::-webkit-scrollbar,
.admin-nav::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

.activity-list::-webkit-scrollbar-track,
.admin-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.activity-list::-webkit-scrollbar-thumb,
.admin-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 215, 0, 0.5);
  border-radius: 3px;
}

.activity-list::-webkit-scrollbar-thumb:hover,
.admin-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 215, 0, 0.7);
}
</style>
