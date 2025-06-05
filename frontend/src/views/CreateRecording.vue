<template>
  <div class="create-recording">
    <div class="container">
      <div class="form-header" data-aos="fade-up">
        <h1>{{ isEditing ? 'Редактировать запись' : 'Создать новую запись' }}</h1>
        <p>{{ isEditing ? 'Внесите изменения в запись' : 'Добавьте новую запись в портал' }}</p>
      </div>

      <form @submit.prevent="handleSubmit" class="recording-form" data-aos="fade-up" data-aos-delay="100">
        <div class="form-card">
          <!-- Title -->
          <div class="form-group">
            <label for="title" class="form-label required">
              <i class="fas fa-heading"></i>
              Заголовок
            </label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              class="form-input"
              placeholder="Введите заголовок записи"
              required
              maxlength="255"
            >
            <div class="char-count">{{ form.title.length }}/255</div>
          </div>

          <!-- Category -->
          <div class="form-group">
            <label for="category" class="form-label">
              <i class="fas fa-tag"></i>
              Категория
            </label>
            <select id="category" v-model="form.category_id" class="form-select">
              <option value="">Выберите категорию</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Content -->
          <div class="form-group">
            <label for="content" class="form-label required">
              <i class="fas fa-align-left"></i>
              Содержание
            </label>
            <div class="editor-toolbar">
              <button type="button" @click="formatText('bold')" class="toolbar-btn" title="Жирный">
                <i class="fas fa-bold"></i>
              </button>
              <button type="button" @click="formatText('italic')" class="toolbar-btn" title="Курсив">
                <i class="fas fa-italic"></i>
              </button>
              <button type="button" @click="formatText('underline')" class="toolbar-btn" title="Подчеркнутый">
                <i class="fas fa-underline"></i>
              </button>
              <div class="toolbar-divider"></div>
              <button type="button" @click="insertList('ul')" class="toolbar-btn" title="Маркированный список">
                <i class="fas fa-list-ul"></i>
              </button>
              <button type="button" @click="insertList('ol')" class="toolbar-btn" title="Нумерованный список">
                <i class="fas fa-list-ol"></i>
              </button>
            </div>
            <textarea
              id="content"
              ref="contentEditor"
              v-model="form.content"
              class="form-textarea"
              placeholder="Введите содержание записи..."
              required
              rows="12"
            ></textarea>
            <div class="char-count">{{ form.content.length }} символов</div>
          </div>

          <!-- Image Upload -->
          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-image"></i>
              Изображение
            </label>
            <div class="file-upload-area" @drop="handleImageDrop" @dragover.prevent @dragenter.prevent>
              <input
                ref="imageInput"
                type="file"
                accept="image/*"
                @change="handleImageSelect"
                class="file-input"
              >
              
              <div v-if="!imagePreview" class="upload-placeholder" @click="$refs.imageInput.click()">
                <i class="fas fa-cloud-upload-alt"></i>
                <p>Перетащите изображение сюда или нажмите для выбора</p>
                <span class="upload-hint">Поддерживаются форматы: JPG, PNG, GIF (макс. 5MB)</span>
              </div>
              
              <div v-else class="image-preview">
                <img :src="imagePreview" alt="Preview">
                <div class="image-actions">
                  <button type="button" @click="removeImage" class="btn btn-danger btn-sm">
                    <i class="fas fa-trash"></i>
                    Удалить
                  </button>
                  <button type="button" @click="$refs.imageInput.click()" class="btn btn-secondary btn-sm">
                    <i class="fas fa-edit"></i>
                    Заменить
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Video Upload -->
          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-video"></i>
              Видео
            </label>
            <div class="file-upload-area" @drop="handleVideoDrop" @dragover.prevent @dragenter.prevent>
              <input
                ref="videoInput"
                type="file"
                accept="video/*"
                @change="handleVideoSelect"
                class="file-input"
              >
              
              <div v-if="!videoPreview" class="upload-placeholder" @click="$refs.videoInput.click()">
                <i class="fas fa-video"></i>
                <p>Перетащите видео сюда или нажмите для выбора</p>
                <span class="upload-hint">Поддерживаются форматы: MP4, AVI, MOV (макс. 50MB)</span>
              </div>
              
              <div v-else class="video-preview">
                <video :src="videoPreview" controls preload="metadata"></video>
                <div class="video-actions">
                  <button type="button" @click="removeVideo" class="btn btn-danger btn-sm">
                    <i class="fas fa-trash"></i>
                    Удалить
                  </button>
                  <button type="button" @click="$refs.videoInput.click()" class="btn btn-secondary btn-sm">
                    <i class="fas fa-edit"></i>
                    Заменить
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Tags -->
          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-hashtag"></i>
              Теги
            </label>
            <div class="tags-input-container">
              <div class="selected-tags">
                <span
                  v-for="tag in selectedTags"
                  :key="tag.id"
                  class="selected-tag"
                >
                  {{ tag.name }}
                  <button type="button" @click="removeTag(tag)" class="tag-remove">
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
                @keydown.comma.prevent="addTag"
              >
            </div>
            <div class="tags-suggestions" v-if="suggestedTags.length > 0">
              <span
                v-for="tag in suggestedTags"
                :key="tag.id"
                class="suggested-tag"
                @click="selectSuggestedTag(tag)"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <router-link to="/recordings" class="btn btn-secondary">
              <i class="fas fa-arrow-left"></i>
              Отмена
            </router-link>
            <button type="button" @click="saveDraft" class="btn btn-outline" :disabled="loading">
              <i class="fas fa-save"></i>
              Сохранить черновик
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
              <i class="fas fa-spinner fa-spin" v-if="loading"></i>
              <i class="fas fa-check" v-else></i>
              {{ isEditing ? 'Обновить' : 'Опубликовать' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  name: 'CreateRecording',
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
      suggestedTags: [],
      imagePreview: null,
      videoPreview: null,
      isEditing: false,
      recordingId: null
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isModerator']),
    ...mapState(['categories', 'tags', 'loading', 'error']),
    isFormValid() {
      return this.form.title.trim() && this.form.content.trim()
    }
  },
  async created() {
    if (!this.isAuthenticated || !this.isModerator) {
      this.$router.push('/login')
      return
    }

    this.recordingId = this.$route.params.id
    this.isEditing = !!this.recordingId

    await this.fetchCategories()
    await this.fetchTags()

    if (this.isEditing) {
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
        this.suggestedTags = this.tags
      } catch (error) {
        console.error('Error fetching tags:', error)
      }
    },
    async loadRecording() {
      try {
        const recording = await this.$store.dispatch('fetchRecording', this.recordingId)
        this.form.title = recording.title
        this.form.content = recording.content
        this.form.category_id = recording.category_id
        this.selectedTags = recording.tags || []
        
        if (recording.image_path) {
          this.imagePreview = recording.image_path
        }
        if (recording.video_path) {
          this.videoPreview = recording.video_path
        }
      } catch (error) {
        console.error('Error loading recording:', error)
        this.$router.push('/recordings')
      }
    },
    handleImageSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.processImageFile(file)
      }
    },
    handleImageDrop(event) {
      event.preventDefault()
      const file = event.dataTransfer.files[0]
      if (file && file.type.startsWith('image/')) {
        this.processImageFile(file)
      }
    },
    processImageFile(file) {
      if (file.size > 5 * 1024 * 1024) {
        alert('Размер изображения не должен превышать 5MB')
        return
      }

      this.form.image = file
      const reader = new FileReader()
      reader.onload = (e) => {
        this.imagePreview = e.target.result
      }
      reader.readAsDataURL(file)
    },
    handleVideoSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.processVideoFile(file)
      }
    },
    handleVideoDrop(event) {
      event.preventDefault()
      const file = event.dataTransfer.files[0]
      if (file && file.type.startsWith('video/')) {
        this.processVideoFile(file)
      }
    },
    processVideoFile(file) {
      if (file.size > 50 * 1024 * 1024) {
        alert('Размер видео не должен превышать 50MB')
        return
      }

      this.form.video = file
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
    addTag() {
      const tagName = this.tagInput.trim()
      if (!tagName) return

      const existingTag = this.selectedTags.find(tag => 
        tag.name.toLowerCase() === tagName.toLowerCase()
      )
      if (existingTag) {
        this.tagInput = ''
        return
      }

      const suggestedTag = this.suggestedTags.find(tag => 
        tag.name.toLowerCase() === tagName.toLowerCase()
      )

      if (suggestedTag) {
        this.selectedTags.push(suggestedTag)
      } else {
        this.selectedTags.push({
          id: Date.now(),
          name: tagName,
          isNew: true
        })
      }

      this.tagInput = ''
    },
    selectSuggestedTag(tag) {
      const exists = this.selectedTags.find(selected => selected.id === tag.id)
      if (!exists) {
        this.selectedTags.push(tag)
      }
    },
    removeTag(tagToRemove) {
      this.selectedTags = this.selectedTags.filter(tag => tag.id !== tagToRemove.id)
    },
    formatText(command) {
      const textarea = this.$refs.contentEditor
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selectedText = textarea.value.substring(start, end)

      let formattedText = ''
      switch (command) {
        case 'bold':
          formattedText = `**${selectedText}**`
          break
        case 'italic':
          formattedText = `*${selectedText}*`
          break
        case 'underline':
          formattedText = `__${selectedText}__`
          break
      }

      const newContent = textarea.value.substring(0, start) + formattedText + textarea.value.substring(end)
      this.form.content = newContent

      this.$nextTick(() => {
        textarea.focus()
        textarea.setSelectionRange(start + formattedText.length, start + formattedText.length)
      })
    },
    insertList(type) {
      const textarea = this.$refs.contentEditor
      const start = textarea.selectionStart
      const listItem = type === 'ul' ? '- ' : '1. '
      
      const newContent = textarea.value.substring(0, start) + listItem + textarea.value.substring(start)
      this.form.content = newContent

      this.$nextTick(() => {
        textarea.focus()
        textarea.setSelectionRange(start + listItem.length, start + listItem.length)
      })
    },
    async saveDraft() {
      // Implementation for saving draft
      console.log('Saving draft...')
    },
    async handleSubmit() {
      if (!this.isFormValid) return

      try {
        const formData = new FormData()
        formData.append('title', this.form.title)
        formData.append('content', this.form.content)
        
        if (this.form.category_id) {
          formData.append('category_id', this.form.category_id)
        }
        
        if (this.form.image) {
          formData.append('image', this.form.image)
        }
        
        if (this.form.video) {
          formData.append('video', this.form.video)
        }

        formData.append('tags', JSON.stringify(this.selectedTags))

        let response
        if (this.isEditing) {
          response = await this.$store.dispatch('updateRecording', {
            id: this.recordingId,
            data: formData
          })
        } else {
          response = await this.$store.dispatch('createRecording', formData)
        }

        this.$router.push(`/recordings/${response.id}`)
      } catch (error) {
        console.error('Error saving recording:', error)
        alert('Произошла ошибка при сохранении записи')
      }
    }
  }
}
</script>


<style scoped>
.create-recording {
  padding: 2rem 0;
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
}

.form-header p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
}

.recording-form {
  max-width: 800px;
  margin: 0 auto;
}

.form-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.form-group {
  margin-bottom: 2rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.form-label.required::after {
  content: '*';
  color: #ff6b6b;
  margin-left: 0.25rem;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-select option {
  background: #1e3c72;
  color: #ffffff;
}

.form-textarea {
  resize: vertical;
  min-height: 200px;
  line-height: 1.6;
}

.char-count {
  text-align: right;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 0.5rem;
}

.editor-toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.toolbar-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toolbar-btn:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.toolbar-divider {
  width: 1px;
  background: rgba(255, 255, 255, 0.2);
  margin: 0 0.5rem;
}

.file-upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.file-upload-area:hover {
  border-color: #ffd700;
  background: rgba(255, 215, 0, 0.05);
}

.file-input {
  display: none;
}

.upload-placeholder {
  cursor: pointer;
  color: rgba(255, 255, 255, 0.8);
}

.upload-placeholder i {
  font-size: 3rem;
  color: #ffd700;
  margin-bottom: 1rem;
}

.upload-placeholder p {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.upload-hint {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

.image-preview,
.video-preview {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 12px;
}

.video-preview video {
  width: 100%;
  max-height: 300px;
  border-radius: 12px;
}

.image-actions,
.video-actions {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-preview:hover .image-actions,
.video-preview:hover .video-actions {
  opacity: 1;
}

.tags-input-container {
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  min-height: 60px;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  transition: all 0.3s ease;
}

.tags-input-container:focus-within {
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.selected-tag {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.tag-remove {
  background: none;
  border: none;
  color: #ffd700;
  margin-left: 0.5rem;
  cursor: pointer;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.tag-remove:hover {
  background: rgba(255, 215, 0, 0.3);
}

.tag-input {
  flex: 1;
  background: none;
  border: none;
  color: #ffffff;
  font-size: 1rem;
  padding: 0.5rem;
  min-width: 150px;
}

.tag-input:focus {
  outline: none;
}

.tag-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.tags-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.suggested-tag {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.suggested-tag:hover {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .form-card {
    padding: 2rem 1.5rem;
  }
  
  .form-header h1 {
    font-size: 2rem;
  }
  
  .editor-toolbar {
    flex-wrap: wrap;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .tags-input-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .tag-input {
    min-width: auto;
  }
}
</style>
