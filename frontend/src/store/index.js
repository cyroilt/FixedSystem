import { createStore } from 'vuex'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

// Set up axios interceptor for auth token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
    recordings: [],
    categories: [],
    tags: [],
    loading: false,
    error: null
  },

  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },

    SET_TOKEN(state, token) {
      state.token = token
      state.isAuthenticated = !!token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },

    SET_RECORDINGS(state, recordings) {
      state.recordings = recordings
    },

    ADD_RECORDING(state, recording) {
      state.recordings.unshift(recording)
    },

    UPDATE_RECORDING(state, updatedRecording) {
      const index = state.recordings.findIndex(
        (r) => r.id === updatedRecording.id
      )
      if (index !== -1) {
        state.recordings.splice(index, 1, updatedRecording)
      }
    },

    DELETE_RECORDING(state, recordingId) {
      state.recordings = state.recordings.filter((r) => r.id !== recordingId)
    },

    SET_CATEGORIES(state, categories) {
      state.categories = categories
    },

    SET_TAGS(state, tags) {
      state.tags = tags
    },

    SET_LOADING(state, loading) {
      state.loading = loading
    },

    SET_ERROR(state, error) {
      state.error = error
    },

    CLEAR_ERROR(state) {
      state.error = null
    },

    LOGOUT(state) {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
    }
  },

  actions: {
    async login({ commit }, credentials) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')

        const response = await axios.post(`${API_BASE_URL}/login`, credentials)
        const { access_token, user } = response.data

        commit('SET_TOKEN', access_token)
        commit('SET_USER', user)

        return { success: true }
      } catch (error) {
        const message = error.response?.data?.message || 'Login failed'
        commit('SET_ERROR', message)
        return { success: false, message }
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async register({ commit }, userData) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')

        await axios.post(`${API_BASE_URL}/register`, userData)
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.message || 'Registration failed'
        commit('SET_ERROR', message)
        return { success: false, message }
      } finally {
        commit('SET_LOADING', false)
      }
    },

    logout({ commit }) {
      commit('LOGOUT')
    },

    async fetchRecordings({ commit }, params = {}) {
      try {
        commit('SET_LOADING', true)
        const response = await axios.get(`${API_BASE_URL}/recordings`, {
          params
        })
        commit('SET_RECORDINGS', response.data.recordings || response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch recordings')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async fetchRecording({ commit }, id) {
      try {
        const response = await axios.get(`${API_BASE_URL}/recordings/${id}`)
        return response.data
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch recording')
        throw error
      }
    },

    async createRecording({ commit }, formData) {
      try {
        commit('SET_LOADING', true)
        const response = await axios.post(
          `${API_BASE_URL}/recordings/create`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to create recording'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async updateRecording({ commit }, { id, data }) {
      try {
        commit('SET_LOADING', true)
        const response = await axios.put(
          `${API_BASE_URL}/recordings/${id}/update`,
          data
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to update recording'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async deleteRecording({ commit }, id) {
      try {
        await axios.delete(`${API_BASE_URL}/recordings/${id}/delete`)
        commit('DELETE_RECORDING', id)
        return { success: true }
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to delete recording'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async fetchCategories({ commit }) {
      try {
        const response = await axios.get(`${API_BASE_URL}/categories`)
        commit('SET_CATEGORIES', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch categories')
        throw error
      }
    },

    async fetchTags({ commit }) {
      try {
        const response = await axios.get(`${API_BASE_URL}/tags`)
        commit('SET_TAGS', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch tags')
        throw error
      }
    },

    async createCategory({ commit }, categoryData) {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/categories/create`,
          categoryData
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to create category'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async createTag({ commit }, tagData) {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/tags/create`,
          tagData
        )
        return response.data
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to create tag'
        commit('SET_ERROR', message)
        throw error
      }
    },

    // Profile-related actions
    async fetchUserProfile({ commit }, userId) {
      try {
        const response = await axios.get(`${API_BASE_URL}/users/${userId}`)
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to fetch user profile'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async fetchUserStats({ commit }, userId) {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/users/${userId}/stats`
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to fetch user stats'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async fetchUserRecordings({ commit }, userId) {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/users/${userId}/recordings`
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to fetch user recordings'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async fetchUserActivity({ commit }, userId) {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/users/${userId}/activity`
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to fetch user activity'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async fetchUserSettings({ commit }) {
      try {
        const response = await axios.get(`${API_BASE_URL}/user/settings`)
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to fetch user settings'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async updateUserSettings({ commit }, settings) {
      try {
        const response = await axios.put(
          `${API_BASE_URL}/user/settings`,
          settings
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to update user settings'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async updateUserProfile({ commit }, profileData) {
      try {
        const response = await axios.put(
          `${API_BASE_URL}/user/profile`,
          profileData
        )

        // Update the user in state if it's the current user
        if (commit.state && commit.state.user) {
          const updatedUser = {
            ...commit.state.user,
            username: profileData.username,
            email: profileData.email,
            bio: profileData.bio
          }
          commit('SET_USER', updatedUser)
        }

        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to update profile'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async changePassword({ commit }, passwordData) {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/user/change-password`,
          passwordData
        )
        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to change password'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async uploadAvatar({ commit }, formData) {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/user/avatar`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )

        // Update the user avatar in state
        if (commit.state && commit.state.user) {
          const updatedUser = {
            ...commit.state.user,
            avatar: response.data.avatar_url
          }
          commit('SET_USER', updatedUser)
        }

        return response.data
      } catch (error) {
        const message =
          error.response?.data?.message || 'Failed to upload avatar'
        commit('SET_ERROR', message)
        throw error
      }
    },

    async fetchLatestRecordings({ commit }, limit = 5) {
      try {
        const response = await axios.get(`${API_BASE_URL}/recordings/latest`, {
          params: { limit }
        })
        return response.data
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch latest recordings')
        throw error
      }
    },

    async fetchRelatedRecordings({ commit }, { recordingId, limit = 3 }) {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/recordings/${recordingId}/related`,
          {
            params: { limit }
          }
        )
        return response.data
      } catch (error) {
        commit('SET_ERROR', 'Failed to fetch related recordings')
        throw error
      }
    },

    // Initialize app - check if user is logged in
    async initializeApp({ commit, state }) {
      if (state.token) {
        try {
          // Verify token is still valid by making a request
          // You might want to add a /api/verify-token endpoint
          commit('SET_TOKEN', state.token)
          // Optionally fetch user data here if needed
        } catch (error) {
          // Token is invalid, clear it
          commit('LOGOUT')
        }
      }
    }
  },

  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    currentUser: (state) => state.user,
    isAdmin: (state) => state.user?.role === 'admin',
    isModerator: (state) =>
      state.user?.role === 'moderator' || state.user?.role === 'admin',
    canCreateRecordings: (state) =>
      ['admin', 'moderator'].includes(state.user?.role),
    recordingsByCategory: (state) => (categoryId) => {
      return state.recordings.filter(
        (recording) => recording.category?.id === categoryId
      )
    },
    recordingsByTag: (state) => (tagId) => {
      return state.recordings.filter((recording) =>
        recording.tags?.some((tag) => tag.id === tagId)
      )
    }
  }
})
