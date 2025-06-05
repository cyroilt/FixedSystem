import { createStore } from 'vuex'
import axios from 'axios'

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:5000/api'
})

// Helper function to get full URL for uploaded files
const getFileUrl = (filePath) => {
  if (!filePath) return null
  if (filePath.startsWith('http')) return filePath
  if (filePath.startsWith('/uploads/')) {
    return `http://localhost:5000${filePath}`
  }
  return `http://localhost:5000/uploads/${filePath}`
}

// Add request interceptor to include auth token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token'),
    recordings: [],
    categories: [],
    tags: [],
    loading: false,
    error: null
  },
  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin: state => state.user && state.user.role === 'admin',
    isModerator: state => state.user && (state.user.role === 'admin' || state.user.role === 'moderator'),
    latestRecordings: state => state.recordings.slice(0, 5),
    // Add helper getter for file URLs
    getFileUrl: () => getFileUrl
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    CLEAR_AUTH(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('token')
    },
    SET_RECORDINGS(state, recordings) {
      // Process recordings to ensure proper file URLs
      state.recordings = recordings.map(recording => ({
        ...recording,
        image_path: getFileUrl(recording.image_path),
        video_path: getFileUrl(recording.video_path)
      }))
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
    ADD_RECORDING(state, recording) {
      // Process recording to ensure proper file URLs
      const processedRecording = {
        ...recording,
        image_path: getFileUrl(recording.image_path),
        video_path: getFileUrl(recording.video_path)
      }
      state.recordings.unshift(processedRecording)
    },
    UPDATE_RECORDING(state, updatedRecording) {
      const processedRecording = {
        ...updatedRecording,
        image_path: getFileUrl(updatedRecording.image_path),
        video_path: getFileUrl(updatedRecording.video_path)
      }
      const index = state.recordings.findIndex(r => r.id === processedRecording.id)
      if (index !== -1) {
        state.recordings.splice(index, 1, processedRecording)
      }
    },
    DELETE_RECORDING(state, recordingId) {
      state.recordings = state.recordings.filter(r => r.id !== recordingId)
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await api.post('/login', credentials)
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
        commit('SET_ERROR', null)
        
        await api.post('/register', userData)
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
      commit('CLEAR_AUTH')
    },
    
    async fetchRecordings({ commit }, params = {}) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const queryParams = new URLSearchParams()
        Object.keys(params).forEach(key => {
          if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
            queryParams.append(key, params[key])
          }
        })
        
        const response = await api.get(`/recordings?${queryParams.toString()}`)
        commit('SET_RECORDINGS', response.data.recordings)
        
        return {
          data: response.data.recordings.map(recording => ({
            ...recording,
            image_path: getFileUrl(recording.image_path),
            video_path: getFileUrl(recording.video_path)
          })),
          total: response.data.total,
          totalPages: response.data.total_pages,
          currentPage: response.data.page
        }
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to fetch recordings'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchRecording({ commit }, id) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await api.get(`/recordings/${id}`)
        const recording = {
          ...response.data,
          image_path: getFileUrl(response.data.image_path),
          video_path: getFileUrl(response.data.video_path)
        }
        return recording
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to fetch recording'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchLatestRecordings({ commit }) {
      try {
        commit('SET_ERROR', null)
        const response = await api.get('/recordings/latest')
        const recordings = response.data.map(recording => ({
          ...recording,
          image_path: getFileUrl(recording.image_path),
          video_path: getFileUrl(recording.video_path)
        }))
        return recordings
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to fetch latest recordings'
        commit('SET_ERROR', message)
        return []
      }
    },
    
    async fetchRelatedRecordings({ commit }, params) {
      try {
        const { recordingId, limit = 3 } = params
        const response = await api.get(`/recordings/${recordingId}/related?limit=${limit}`)
        const recordings = response.data.map(recording => ({
          ...recording,
          image_path: getFileUrl(recording.image_path),
          video_path: getFileUrl(recording.video_path)
        }))
        return recordings
      } catch (error) {
        console.error('Error fetching related recordings:', error)
        return []
      }
    },
    
    async createRecording({ commit }, formData) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        // Create axios instance with proper headers
        const api = axios.create({
          baseURL: 'http://localhost:5000/api',
          headers: {
            'Authorization': `Bearer ${this.state.token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        
        const response = await api.post('/recordings/create', formData)
        
        return { success: true, id: response.data.id }
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to create recording'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    
    async updateRecording({ commit }, { id, data }) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await api.put(`/recordings/${id}/update`, data, {
          headers: {
            'Content-Type': data instanceof FormData ? 'multipart/form-data' : 'application/json'
          }
        })
        
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to update recording'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async deleteRecording({ commit }, id) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        await api.delete(`/recordings/${id}/delete`)
        commit('DELETE_RECORDING', id)
        
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to delete recording'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchCategories({ commit }) {
      try {
        commit('SET_ERROR', null)
        const response = await api.get('/categories')
        commit('SET_CATEGORIES', response.data)
        return response.data
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to fetch categories'
        commit('SET_ERROR', message)
        return []
      }
    },
    
    async createCategory({ commit }, categoryData) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await api.post('/categories/create', categoryData)
        return { success: true, id: response.data.id }
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to create category'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchTags({ commit }) {
      try {
        commit('SET_ERROR', null)
        const response = await api.get('/tags')
        commit('SET_TAGS', response.data)
        return response.data
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to fetch tags'
        commit('SET_ERROR', message)
        return []
      }
    },
    
    async createTag({ commit }, tagData) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await api.post('/tags/create', tagData)
        return { success: true, id: response.data.id }
      } catch (error) {
        const message = error.response?.data?.message || 'Failed to create tag'
        commit('SET_ERROR', message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // User profile actions (for future implementation)
    async fetchUserProfile({ commit }, userId) {
      try {
        const response = await api.get(`/users/${userId}/profile`)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async updateUserProfile({ commit }, profileData) {
      try {
        const response = await api.put('/users/profile', profileData)
        commit('SET_USER', { ...this.state.user, ...profileData })
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async changePassword({ commit }, passwordData) {
      try {
        const response = await api.put('/users/change-password', passwordData)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async fetchUserStats({ commit }, userId) {
      try {
        const response = await api.get(`/users/${userId}/stats`)
        return response.data
      } catch (error) {
        return { recordings: 0, views: 0 }
      }
    },
    
    async fetchUserRecordings({ commit }, userId) {
      try {
        const response = await api.get(`/users/${userId}/recordings`)
        return response.data
      } catch (error) {
        return []
      }
    },
    
    async fetchUserActivity({ commit }, userId) {
      try {
        const response = await api.get(`/users/${userId}/activity`)
        return response.data
      } catch (error) {
        return []
      }
    },
    
    async fetchUserSettings({ commit }) {
      try {
        const response = await api.get('/users/settings')
        return response.data
      } catch (error) {
        return {
          emailNotifications: true,
          pushNotifications: false,
          publicProfile: true,
          showEmail: false
        }
      }
    },
    
    async updateUserSettings({ commit }, settings) {
      try {
        const response = await api.put('/users/settings', settings)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async uploadAvatar({ commit }, formData) {
      try {
        const response = await api.post('/users/avatar', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } catch (error) {
        throw error
      }
    }
  }
})