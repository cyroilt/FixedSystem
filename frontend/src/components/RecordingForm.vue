<template>
  <div class="recording-form bg-darker-gradient particles-bg">
    <div class="container">
      <div class="form-header animate-fade-in-up">
        <h1 class="animate-glow">
          {{ isEdit ? 'Редактировать запись' : 'Создать новую запись' }}
        </h1>
        <p>
          {{
            isEdit
              ? 'Внесите изменения в запись'
              : 'Заполните форму для создания новой записи'
          }}
        </p>
      </div>

      <form
        @submit.prevent="submitForm"
        class="recording-form-content animate-fade-in-up animate-stagger-2"
      >
        <!-- Title Field -->
        <div class="form-group animate-slide-in-up">
          <label for="title" class="form-label">
            <i class="fas fa-heading"></i>
            Название записи *
          </label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            class="form-input hover-glow"
            placeholder="Введите название записи"
            required
            :class="{ error: errors.title }"
          />
          <span
            v-if="errors.title"
            class="error-message animate-fade-in-left"
            >{{ errors.title }}</span
          >
        </div>

        <!-- Content Field -->
        <div class="form-group animate-slide-in-up animate-stagger-2">
          <label for="content" class="form-label">
            <i class="fas fa-align-left"></i>
            Содержание
          </label>
          <textarea
            id="content"
            v-model="form.content"
            class="form-textarea hover-glow"
            placeholder="Введите содержание записи"
            rows="6"
            :class="{ error: errors.content }"
          ></textarea>
          <span
            v-if="errors.content"
            class="error-message animate-fade-in-left"
            >{{ errors.content }}</span
          >
        </div>

        <!-- Category Field -->
        <div class="form-group animate-slide-in-up animate-stagger-3">
          <label for="category" class="form-label">
            <i class="fas fa-tag"></i>
            Категория
          </label>
          <select
            id="category"
            v-model="form.category_id"
            class="form-select hover-glow"
            :class="{ error: errors.category_id }"
          >
            <option value="">Выберите категорию</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
          <span
            v-if="errors.category_id"
            class="error-message animate-fade-in-left"
            >{{ errors.category_id }}</span
          >
        </div>

        <!-- Tags Field -->
        <div class="form-group animate-slide-in-up animate-stagger-4">
          <label class="form-label">
            <i class="fas fa-tags"></i>
            Теги
          </label>
          <div class="tags-input-container">
            <div class="selected-tags">
              <span
                v-for="tag in selectedTags"
                :key="tag.id"
                class="selected-tag hover-scale animate-bounce-in"
              >
                {{ tag.name }}
                <button
                  type="button"
                  @click="removeTag(tag)"
                  class="remove-tag"
                >
                  <i class="fas fa-times"></i>
                </button>
              </span>
            </div>
            <input
              v-model="tagInput"
              type="text"
              class="tag-input"
              placeholder="Введите тег и нажмите Enter"
              @keydown.enter.prevent="addTag"
              @input="filterTags"
            />
            <div
              v-if="filteredTags.length > 0"
              class="tag-suggestions animate-fade-in-up"
            >
              <div
                v-for="tag in filteredTags"
                :key="tag.id"
                class="tag-suggestion hover-glow"
                @click="selectTag(tag)"
              >
                {{ tag.name }}
              </div>
            </div>
          </div>
        </div>

        <!-- Image Upload -->
        <div class="form-group animate-slide-in-up animate-stagger-5">
          <label class="form-label">
            <i class="fas fa-image"></i>
            Изображение
          </label>
          <div class="file-upload-container">
            <input
              ref="imageInput"
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              class="file-input"
              id="image-upload"
            />
            <label for="image-upload" class="file-upload-label hover-lift">
              <i class="fas fa-cloud-upload-alt"></i>
              <span>{{
                form.image ? 'Изменить изображение' : 'Выбрать изображение'
              }}</span>
            </label>
            <div
              v-if="form.image || imagePreview"
              class="image-preview animate-scale-in"
            >
              <img
                :src="imagePreview || getImageUrl(form.image)"
                alt="Preview"
                class="preview-image"
              />
              <button
                type="button"
                @click="removeImage"
                class="remove-preview hover-scale"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
          <span
            v-if="errors.image"
            class="error-message animate-fade-in-left"
            >{{ errors.image }}</span
          >
        </div>

        <!-- Video Upload -->
        <div class="form-group animate-slide-in-up animate-stagger-6">
          <label class="form-label">
            <i class="fas fa-video"></i>
            Видео
          </label>
          <div class="file-upload-container">
            <input
              ref="videoInput"
              type="file"
              accept="video/*"
              @change="handleVideoUpload"
              class="file-input"
              id="video-upload"
            />
            <label for="video-upload" class="file-upload-label hover-lift">
              <i class="fas fa-video"></i>
              <span>{{ form.video ? 'Изменить видео' : 'Выбрать видео' }}</span>
            </label>
            <div
              v-if="form.video || videoPreview"
              class="video-preview animate-scale-in"
            >
              <video
                :src="videoPreview || getVideoUrl(form.video)"
                controls
                class="preview-video"
              ></video>
              <button
                type="button"
                @click="removeVideo"
                class="remove-preview hover-scale"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
          <span
            v-if="errors.video"
            class="error-message animate-fade-in-left"
            >{{ errors.video }}</span
          >
        </div>

        <!-- Form Actions -->
        <div class="form-actions animate-fade-in-up animate-stagger-7">
          <button
            type="button"
            @click="$router.go(-1)"
            class="btn btn-secondary hover-scale"
            :disabled="loading"
          >
            <i class="fas fa-arrow-left"></i>
            Отмена
          </button>
          <button
            type="submit"
            class="btn btn-primary hover-glow"
            :disabled="loading || !isFormValid"
            :class="{ 'animate-pulse': loading }"
          >
            <i class="fas fa-spinner animate-spin" v-if="loading"></i>
            <i class="fas fa-save" v-else></i>
            {{ loading ? 'Сохранение...' : isEdit ? 'Обновить' : 'Создать' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

export default {
  name: 'RecordingForm',
  props: {
    recordingId: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      form: {
        title: '',
        content: '',
        category_id: '',
        image: null,
        video: null
      },
      selectedTags: [],
      tagInput: '',
      filteredTags: [],
      imagePreview: null,
      videoPreview: null,
      loading: false,
      errors: {}
    }
  },
  computed: {
    ...mapState(['categories', 'tags']),
    ...mapGetters(['isModerator']),
    isEdit() {
      return !!this.recordingId
    },
    isFormValid() {
      return this.form.title.trim().length > 0
    }
  },
  async created() {
    await this.fetchCategories()
    await this.fetchTags()

    if (this.isEdit) {
      await this.loadRecording()
    }
  },
  methods: {
    async fetchCategories() {
      try {
        await this.$store.dispatch('fetchCategories')
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },
    async fetchTags() {
      try {
        await this.$store.dispatch('fetchTags')
      } catch (error) {
        console.error('Error fetching tags:', error)
      }
    },
    async loadRecording() {
      try {
        this.loading = true
        const recording = await this.$store.dispatch(
          'fetchRecording',
          this.recordingId
        )

        this.form = {
          title: recording.title || '',
          content: recording.content || '',
          category_id: recording.category?.id || '',
          image: recording.image_path || null,
          video: recording.video_path || null
        }

        this.selectedTags = recording.tags || []
      } catch (error) {
        console.error('Error loading recording:', error)
        this.$router.push('/recordings')
      } finally {
        this.loading = false
      }
    },
    filterTags() {
      if (!this.tagInput.trim()) {
        this.filteredTags = []
        return
      }

      const input = this.tagInput.toLowerCase()
      this.filteredTags = this.tags
        .filter(
          (tag) =>
            tag.name.toLowerCase().includes(input) &&
            !this.selectedTags.some((selected) => selected.id === tag.id)
        )
        .slice(0, 5)
    },
    selectTag(tag) {
      this.selectedTags.push(tag)
      this.tagInput = ''
      this.filteredTags = []
    },
    addTag() {
      const tagName = this.tagInput.trim()
      if (!tagName) return

      // Check if tag already exists
      const existingTag = this.tags.find(
        (tag) => tag.name.toLowerCase() === tagName.toLowerCase()
      )

      if (existingTag) {
        this.selectTag(existingTag)
      } else {
        // Create new tag
        const newTag = {
          id: `new_${Date.now()}`,
          name: tagName,
          isNew: true
        }
        this.selectedTags.push(newTag)
        this.tagInput = ''
        this.filteredTags = []
      }
    },
    removeTag(tagToRemove) {
      this.selectedTags = this.selectedTags.filter(
        (tag) => tag.id !== tagToRemove.id
      )
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      // Validate file type
      if (!file.type.startsWith('image/')) {
        this.errors.image = 'Пожалуйста, выберите изображение'
        return
      }

      // Validate file size (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        this.errors.image = 'Размер изображения не должен превышать 5MB'
        return
      }

      this.form.image = file
      this.errors.image = null

      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        this.imagePreview = e.target.result
      }
      reader.readAsDataURL(file)
    },
    handleVideoUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      // Validate file type
      if (!file.type.startsWith('video/')) {
        this.errors.video = 'Пожалуйста, выберите видео файл'
        return
      }

      // Validate file size (50MB max)
      if (file.size > 50 * 1024 * 1024) {
        this.errors.video = 'Размер видео не должен превышать 50MB'
        return
      }

      this.form.video = file
      this.errors.video = null

      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        this.videoPreview = e.target.result
      }
      reader.readAsDataURL(file)
    },
    removeImage() {
      this.form.image = null
      this.imagePreview = null
      this.$refs.imageInput.value = ''
    },
    removeVideo() {
      this.form.video = null
      this.videoPreview = null
      this.$refs.videoInput.value = ''
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
    validateForm() {
      this.errors = {}

      if (!this.form.title.trim()) {
        this.errors.title = 'Название обязательно для заполнения'
      }

      return Object.keys(this.errors).length === 0
    },
    async submitForm() {
      if (!this.validateForm()) return

      this.loading = true

      try {
        const formData = new FormData()
        formData.append('title', this.form.title.trim())
        formData.append('content', this.form.content.trim())

        if (this.form.category_id) {
          formData.append('category_id', this.form.category_id)
        }

        if (this.selectedTags.length > 0) {
          formData.append('tags', JSON.stringify(this.selectedTags))
        }

        if (this.form.image instanceof File) {
          formData.append('image', this.form.image)
        }

        if (this.form.video instanceof File) {
          formData.append('video', this.form.video)
        }

        if (this.isEdit) {
          await this.$store.dispatch('updateRecording', {
            id: this.recordingId,
            data: formData
          })
        } else {
          const result = await this.$store.dispatch('createRecording', formData)
          if (result.success) {
            this.$router.push(`/recordings/${result.id}`)
            return
          }
        }

        this.$router.push('/recordings')
      } catch (error) {
        console.error('Error submitting form:', error)
        this.errors.submit =
          error.response?.data?.message || 'Произошла ошибка при сохранении'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.recording-form {
  padding: 2rem 0;
  min-height: 100vh;
}

.form-header {
  text-align: center;
  margin-bottom: 3rem;
}

.form-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.form-header p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.recording-form-content {
  max-width: 800px;
  margin: 0 auto;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.form-group {
  margin-bottom: 2rem;
}

.form-label {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #ffd700;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.form-label i {
  margin-right: 0.5rem;
  width: 20px;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 1rem 1.25rem;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
  background: rgba(0, 0, 0, 0.5);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.form-select option {
  background: #0a0a0a;
  color: #ffffff;
}

.form-input.error,
.form-textarea.error,
.form-select.error {
  border-color: #ff6b6b;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2);
}

.error-message {
  display: block;
  color: #ff6b6b;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  font-weight: 500;
}

.tags-input-container {
  position: relative;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.selected-tag {
  display: flex;
  align-items: center;
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.5rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
}

.remove-tag {
  background: none;
  border: none;
  color: #ffd700;
  margin-left: 0.5rem;
  cursor: pointer;
  padding: 0;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.remove-tag:hover {
  color: #ff6b6b;
  transform: scale(1.2);
}

.tag-input {
  width: 100%;
  padding: 1rem 1.25rem;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.tag-input:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.tag-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  margin-top: 0.5rem;
}

.tag-suggestion {
  padding: 0.75rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tag-suggestion:hover {
  background: rgba(255, 215, 0, 0.1);
  color: #ffd700;
}

.tag-suggestion:last-child {
  border-bottom: none;
}

.file-upload-container {
  position: relative;
}

.file-input {
  display: none;
}

.file-upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(0, 0, 0, 0.3);
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.7);
}

.file-upload-label:hover {
  border-color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
  color: #ffd700;
}

.file-upload-label i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.image-preview,
.video-preview {
  position: relative;
  margin-top: 1rem;
  border-radius: 12px;
  overflow: hidden;
}

.preview-image,
.preview-video {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 12px;
}

.remove-preview {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 32px;
  height: 32px;
  background: rgba(255, 107, 107, 0.9);
  border: none;
  border-radius: 50%;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.remove-preview:hover {
  background: #ff6b6b;
  transform: scale(1.1);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .recording-form-content {
    padding: 1.5rem;
    margin: 0 1rem;
  }

  .form-header h1 {
    font-size: 2rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .selected-tags {
    gap: 0.25rem;
  }

  .selected-tag {
    font-size: 0.8rem;
    padding: 0.4rem 0.6rem;
  }
}

@media (max-width: 480px) {
  .recording-form {
    padding: 1rem 0;
  }

  .recording-form-content {
    padding: 1rem;
  }

  .form-input,
  .form-textarea,
  .form-select,
  .tag-input {
    padding: 0.75rem 1rem;
  }
}
</style>
