<template>
  <div class="avatar-placeholder" :class="[size, variant]" :style="avatarStyle">
    <img 
      v-if="src && !imageError" 
      :src="src" 
      :alt="alt"
      @error="handleImageError"
      @load="handleImageLoad"
      class="avatar-image"
    >
    <div v-else class="avatar-fallback">
      <i v-if="icon" :class="icon" class="avatar-icon"></i>
      <span v-else-if="initials" class="avatar-initials">{{ initials }}</span>
      <i v-else class="fas fa-user avatar-icon"></i>
    </div>
    <div v-if="showStatus && status" class="avatar-status" :class="status"></div>
  </div>
</template>

<script>
export default {
  name: 'AvatarPlaceholder',
  props: {
    src: {
      type: String,
      default: null
    },
    alt: {
      type: String,
      default: 'Avatar'
    },
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large', 'xl'].includes(value)
    },
    variant: {
      type: String,
      default: 'circle',
      validator: value => ['circle', 'rounded', 'square'].includes(value)
    },
    name: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: null
    },
    backgroundColor: {
      type: String,
      default: null
    },
    textColor: {
      type: String,
      default: null
    },
    showStatus: {
      type: Boolean,
      default: false
    },
    status: {
      type: String,
      default: 'offline',
      validator: value => ['online', 'offline', 'away', 'busy'].includes(value)
    }
  },
  data() {
    return {
      imageError: false,
      imageLoaded: false
    }
  },
  computed: {
    initials() {
      if (!this.name) return ''
      return this.name
        .split(' ')
        .map(word => word.charAt(0).toUpperCase())
        .slice(0, 2)
        .join('')
    },
    avatarStyle() {
      const style = {}
      if (this.backgroundColor) {
        style.backgroundColor = this.backgroundColor
      }
      if (this.textColor) {
        style.color = this.textColor
      }
      return style
    }
  },
  watch: {
    src() {
      this.imageError = false
      this.imageLoaded = false
    }
  },
  methods: {
    handleImageError() {
      this.imageError = true
      this.$emit('error')
    },
    handleImageLoad() {
      this.imageLoaded = true
      this.$emit('load')
    },
    generateColorFromName(name) {
      if (!name) return '#6b7280'
      
      const colors = [
        '#ef4444', '#f97316', '#f59e0b', '#eab308',
        '#84cc16', '#22c55e', '#10b981', '#14b8a6',
        '#06b6d4', '#0ea5e9', '#3b82f6', '#6366f1',
        '#8b5cf6', '#a855f7', '#d946ef', '#ec4899'
      ]
      
      let hash = 0
      for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash)
      }
      
      return colors[Math.abs(hash) % colors.length]
    }
  },
  mounted() {
    if (!this.backgroundColor && this.name) {
      this.$el.style.backgroundColor = this.generateColorFromName(this.name)
    }
  }
}
</script>

<style scoped>
.avatar-placeholder {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-weight: 600;
  overflow: hidden;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.avatar-placeholder.small {
  width: 32px;
  height: 32px;
  font-size: 0.75rem;
}

.avatar-placeholder.medium {
  width: 48px;
  height: 48px;
  font-size: 1rem;
}

.avatar-placeholder.large {
  width: 64px;
  height: 64px;
  font-size: 1.25rem;
}

.avatar-placeholder.xl {
  width: 96px;
  height: 96px;
  font-size: 1.5rem;
}

.avatar-placeholder.circle {
  border-radius: 50%;
}

.avatar-placeholder.rounded {
  border-radius: 12px;
}

.avatar-placeholder.square {
  border-radius: 4px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.avatar-initials {
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.avatar-icon {
  opacity: 0.8;
}

.avatar-status {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 25%;
  height: 25%;
  border-radius: 50%;
  border: 2px solid #ffffff;
  min-width: 8px;
  min-height: 8px;
}

.avatar-status.online {
  background: #10b981;
}

.avatar-status.offline {
  background: #6b7280;
}

.avatar-status.away {
  background: #f59e0b;
}

.avatar-status.busy {
  background: #ef4444;
}

/* Hover effects */
.avatar-placeholder:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Loading animation */
.avatar-placeholder.loading {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Dark theme support */
@media (prefers-color-scheme: dark) {
  .avatar-placeholder.loading {
    background: linear-gradient(90deg, #374151 25%, #4b5563 50%, #374151 75%);
    background-size: 200% 100%;
  }
}
</style>