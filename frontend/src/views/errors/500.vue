<template>
  <div class="error-page bg-space-gradient">
    <div class="container">
      <div class="error-content">
        <!-- Animated Error Icon -->
        <div class="error-icon-container animate-bounce-in">
          <div class="error-icon">
            <i class="fas fa-exclamation-triangle animate-pulse"></i>
            <div class="error-number animate-glow">500</div>
          </div>
          <div class="icon-particles">
            <div class="particle particle-1 animate-float"></div>
            <div class="particle particle-2 animate-float animate-stagger-2"></div>
            <div class="particle particle-3 animate-float animate-stagger-4"></div>
            <div class="particle particle-4 animate-float animate-stagger-6"></div>
            <div class="particle particle-5 animate-float animate-stagger-8"></div>
          </div>
        </div>

        <!-- Error Message -->
        <div class="error-message animate-fade-in-up animate-stagger-2">
          <h1 class="error-title animate-glow">Внутренняя ошибка сервера</h1>
          <p class="error-description animate-fade-in-up animate-stagger-3">
            Произошла непредвиденная ошибка на сервере. Наша команда уже работает над устранением проблемы. 
            Попробуйте обновить страницу или вернуться позже.
          </p>
        </div>

        <!-- Error Details -->
        <div class="error-details animate-fade-in-up animate-stagger-4">
          <div class="detail-card hover-lift">
            <i class="fas fa-server"></i>
            <h3>Проблема с сервером</h3>
            <p>Временные технические неполадки на стороне сервера</p>
          </div>
          <div class="detail-card hover-lift animate-stagger-1">
            <i class="fas fa-tools"></i>
            <h3>Ведутся работы</h3>
            <p>Наши специалисты уже работают над решением проблемы</p>
          </div>
          <div class="detail-card hover-lift animate-stagger-2">
            <i class="fas fa-clock"></i>
            <h3>Временная проблема</h3>
            <p>Обычно такие проблемы решаются в течение нескольких минут</p>
          </div>
        </div>

        <!-- Status Section -->
        <div class="status-section animate-fade-in-up animate-stagger-5">
          <div class="status-card">
            <h3>
              <i class="fas fa-heartbeat"></i>
              Статус системы
            </h3>
            <div class="status-items">
              <div class="status-item">
                <div class="status-indicator status-error"></div>
                <span class="status-label">Веб-сервер</span>
                <span class="status-value">Недоступен</span>
              </div>
              <div class="status-item">
                <div class="status-indicator status-warning"></div>
                <span class="status-label">База данных</span>
                <span class="status-value">Проверяется</span>
              </div>
              <div class="status-item">
                <div class="status-indicator status-success"></div>
                <span class="status-label">CDN</span>
                <span class="status-value">Работает</span>
              </div>
            </div>
            <div class="status-footer">
              <small>Последнее обновление: {{ currentTime }}</small>
              <button @click="refreshStatus" class="refresh-btn hover-scale">
                <i class="fas fa-sync-alt" :class="{ 'animate-spin': refreshing }"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="error-actions animate-fade-in-up animate-stagger-6">
          <button @click="reloadPage" class="btn btn-primary hover-glow animate-pulse">
            <i class="fas fa-redo"></i>
            Обновить страницу
          </button>
          <button @click="goBack" class="btn btn-secondary hover-lift">
            <i class="fas fa-arrow-left"></i>
            Назад
          </button>
          <router-link to="/" class="btn btn-outline hover-scale">
            <i class="fas fa-home"></i>
            На главную
          </router-link>
        </div>

                <!-- Help Section -->
        <div class="help-section animate-fade-in-up animate-stagger-7">
          <div class="help-card">
            <h4>
              <i class="fas fa-question-circle"></i>
              Что делать?
            </h4>
            <div class="help-steps">
              <div class="help-step">
                <div class="step-number">1</div>
                <div class="step-content">
                  <h5>Подождите несколько минут</h5>
                  <p>Проблема может решиться автоматически</p>
                </div>
              </div>
              <div class="help-step">
                <div class="step-number">2</div>
                <div class="step-content">
                  <h5>Обновите страницу</h5>
                  <p>Нажмите F5 или кнопку "Обновить"</p>
                </div>
              </div>
              <div class="help-step">
                <div class="step-number">3</div>
                <div class="step-content">
                  <h5>Очистите кэш браузера</h5>
                  <p>Ctrl+F5 для принудительного обновления</p>
                </div>
              </div>
              <div class="help-step">
                <div class="step-number">4</div>
                <div class="step-content">
                  <h5>Обратитесь в поддержку</h5>
                  <p>Если проблема не решается</p>
                </div>
              </div>
            </div>
            <div class="help-actions">
              <a href="mailto:support@faculty.edu" class="help-link hover-glow">
                <i class="fas fa-envelope"></i>
                Написать в поддержку
              </a>
              <a href="tel:+7XXXXXXXXX" class="help-link hover-glow">
                <i class="fas fa-phone"></i>
                Позвонить
              </a>
              <button @click="reportError" class="help-link hover-glow">
                <i class="fas fa-bug"></i>
                Сообщить об ошибке
              </button>
            </div>
          </div>
        </div>

        <!-- Error Report Modal -->
        <div v-if="showReportModal" class="modal-overlay" @click="showReportModal = false">
          <div class="modal" @click.stop>
            <div class="modal-header">
              <h3>Сообщить об ошибке</h3>
              <button @click="showReportModal = false" class="modal-close">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitErrorReport">
                <div class="form-group">
                  <label>Ваш email (необязательно)</label>
                  <input v-model="errorReport.email" type="email" class="form-input" placeholder="email@example.com">
                </div>
                <div class="form-group">
                  <label>Описание проблемы</label>
                  <textarea v-model="errorReport.description" class="form-textarea" rows="4" 
                    placeholder="Опишите, что вы делали когда произошла ошибка..."></textarea>
                </div>
                <div class="form-group">
                  <label>
                    <input v-model="errorReport.includeTechnicalInfo" type="checkbox">
                    Включить техническую информацию
                  </label>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button @click="showReportModal = false" class="btn btn-secondary">
                Отмена
              </button>
              <button @click="submitErrorReport" class="btn btn-primary" :disabled="!errorReport.description.trim()">
                <i class="fas fa-paper-plane"></i>
                Отправить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Background Animation -->
    <div class="background-animation">
      <div class="floating-shape shape-1 animate-float"></div>
      <div class="floating-shape shape-2 animate-float animate-stagger-3"></div>
      <div class="floating-shape shape-3 animate-float animate-stagger-5"></div>
      <div class="floating-shape shape-4 animate-float animate-stagger-7"></div>
      <div class="floating-shape shape-5 animate-float animate-stagger-9"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Error500',
  data() {
    return {
      currentTime: '',
      refreshing: false,
      showReportModal: false,
      errorReport: {
        email: '',
        description: '',
        includeTechnicalInfo: true
      }
    }
  },
  mounted() {
    this.updateTime()
    this.timeInterval = setInterval(this.updateTime, 1000)
    this.initializeAnimations()
  },
  beforeUnmount() {
    if (this.timeInterval) {
      clearInterval(this.timeInterval)
    }
  },
  methods: {
    updateTime() {
      this.currentTime = new Date().toLocaleTimeString('ru-RU')
    },
    async refreshStatus() {
      this.refreshing = true
      // Simulate status check
      await new Promise(resolve => setTimeout(resolve, 2000))
      this.refreshing = false
    },
    goBack() {
      if (window.history.length > 1) {
        this.$router.go(-1)
      } else {
        this.$router.push('/')
      }
    },
    reloadPage() {
      window.location.reload()
    },
    reportError() {
      this.showReportModal = true
    },
    async submitErrorReport() {
      try {
        // Here you would send the error report to your backend
        console.log('Error report:', this.errorReport)
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Reset form and close modal
        this.errorReport = {
          email: '',
          description: '',
          includeTechnicalInfo: true
        }
        this.showReportModal = false
        
        // Show success message (you could use a toast notification)
        alert('Спасибо! Ваше сообщение об ошибке отправлено.')
      } catch (error) {
        console.error('Failed to submit error report:', error)
        alert('Не удалось отправить сообщение. Попробуйте позже.')
      }
    },
    initializeAnimations() {
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in-view')
          }
        })
      }, observerOptions)

      document.querySelectorAll('.detail-card, .status-card, .help-card').forEach(el => {
        observer.observe(el)
      })
    }
  }
}
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  position: relative;
  overflow: hidden;
}

.error-content {
  text-align: center;
  max-width: 1000px;
  position: relative;
  z-index: 2;
}

.error-icon-container {
  position: relative;
  margin-bottom: 3rem;
}

.error-icon {
  position: relative;
  display: inline-block;
  padding: 2rem;
}

.error-icon i {
  font-size: 6rem;
  color: #ff9500;
  margin-bottom: 1rem;
  display: block;
  text-shadow: 0 0 30px rgba(255, 149, 0, 0.5);
}

.error-number {
  font-size: 8rem;
  font-weight: 900;
  background: linear-gradient(45deg, #ff9500, #ffb347);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(255, 149, 0, 0.3);
  line-height: 1;
}

.icon-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, rgba(255, 149, 0, 0.6), transparent);
  border-radius: 50%;
}

.particle-1 {
  top: 20%;
  left: 20%;
  animation-duration: 4s;
}

.particle-2 {
  top: 60%;
  right: 20%;
  animation-duration: 6s;
}

.particle-3 {
  bottom: 30%;
  left: 60%;
  animation-duration: 5s;
}

.particle-4 {
  top: 40%;
  right: 40%;
  animation-duration: 7s;
}

.particle-5 {
  bottom: 50%;
  left: 30%;
  animation-duration: 8s;
}

.error-message {
  margin-bottom: 3rem;
}

.error-title {
  font-size: 3rem;
  font-weight: 700;
  color: #ff9500;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 20px rgba(255, 149, 0, 0.3);
}

.error-description {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  max-width: 700px;
  margin: 0 auto;
}

.error-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.detail-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 149, 0, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.detail-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 149, 0, 0.1), transparent);
  transition: left 0.6s ease;
}

.detail-card:hover::before {
  left: 100%;
}

.detail-card:hover {
  border-color: rgba(255, 149, 0, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.detail-card i {
  font-size: 2.5rem;
  color: #ff9500;
  margin-bottom: 1rem;
  display: block;
}

.detail-card h3 {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.detail-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

.status-section {
  margin-bottom: 3rem;
}

.status-card {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.status-card h3 {
  color: #ffd700;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.status-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-success {
  background: #4ade80;
  box-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
}

.status-warning {
  background: #fbbf24;
  box-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
}

.status-error {
  background: #ef4444;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
}

.status-label {
  flex: 1;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.status-value {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.status-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.status-footer small {
  color: rgba(255, 255, 255, 0.6);
}

.refresh-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  color: #ffd700;
    background: rgba(255, 215, 0, 0.1);
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.help-section {
  margin-top: 2rem;
}

.help-card {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  max-width: 700px;
  margin: 0 auto;
  text-align: left;
}

.help-card h4 {
  color: #ffd700;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.help-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.help-step {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.help-step:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 149, 0, 0.3);
}

.step-number {
  width: 32px;
  height: 32px;
  background: linear-gradient(45deg, #ff9500, #ffb347);
  color: #1a1a2e;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.step-content h5 {
  color: #ffffff;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.step-content p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0;
}

.help-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.help-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  font-size: 0.9rem;
  cursor: pointer;
}

.help-link:hover {
  color: #ff9500;
  background: rgba(255, 149, 0, 0.1);
  border-color: rgba(255, 149, 0, 0.3);
  transform: translateY(-2px);
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.3;
}

.shape-1 {
  width: 120px;
  height: 120px;
  top: 10%;
  left: 10%;
  background: radial-gradient(circle, rgba(255, 149, 0, 0.4), transparent);
  animation-duration: 8s;
}

.shape-2 {
  width: 80px;
  height: 80px;
  top: 70%;
  right: 15%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2), transparent);
  animation-duration: 6s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 70%;
  background: radial-gradient(circle, rgba(255, 149, 0, 0.3), transparent);
  animation-duration: 7s;
}

.shape-4 {
  width: 60px;
  height: 60px;
  top: 30%;
  right: 30%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent);
  animation-duration: 9s;
}

.shape-5 {
  width: 90px;
  height: 90px;
  bottom: 40%;
  left: 20%;
  background: radial-gradient(circle, rgba(255, 149, 0, 0.2), transparent);
  animation-duration: 10s;
}

/* Modal Styles */
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
  color: #ff9500;
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

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  resize: vertical;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #ff9500;
  box-shadow: 0 0 0 3px rgba(255, 149, 0, 0.2);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-group label input[type="checkbox"] {
  width: auto;
  margin-right: 0.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes glow {
  0%, 100% {
    text-shadow: 0 0 20px rgba(255, 149, 0, 0.3);
  }
  50% {
    text-shadow: 0 0 40px rgba(255, 149, 0, 0.6);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
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

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-bounce-in {
  animation: bounceIn 1s ease-out;
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite alternate;
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-stagger-1 { animation-delay: 0.1s; }
.animate-stagger-2 { animation-delay: 0.2s; }
.animate-stagger-3 { animation-delay: 0.3s; }
.animate-stagger-4 { animation-delay: 0.4s; }
.animate-stagger-5 { animation-delay: 0.5s; }
.animate-stagger-6 { animation-delay: 0.6s; }
.animate-stagger-7 { animation-delay: 0.7s; }
.animate-stagger-8 { animation-delay: 0.8s; }
.animate-stagger-9 { animation-delay: 0.9s; }

.hover-lift:hover {
  transform: translateY(-3px);
}

.hover-scale:hover {
  transform: scale(1.05);
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(255, 149, 0, 0.3);
}

/* Responsive Design */
@media (max-width: 768px) {
  .error-title {
    font-size: 2.5rem;
  }
  
  .error-number {
    font-size: 6rem;
  }
  
  .error-icon i {
    font-size: 4rem;
  }
  
  .error-description {
    font-size: 1.1rem;
  }
  
  .error-details {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .help-steps {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .help-actions {
    flex-direction: column;
  }
  
  .status-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .status-footer {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .error-page {
    padding: 1rem 0;
  }
  
  .error-title {
    font-size: 2rem;
  }
  
  .error-number {
    font-size: 4rem;
  }
  
  .detail-card,
  .status-card,
  .help-card {
    padding: 1.5rem;
  }
  
  .help-step {
    padding: 0.75rem;
  }
  
  .modal {
    margin: 1rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .animate-bounce-in,
  .animate-fade-in-up,
  .animate-pulse,
  .animate-glow,
  .animate-float,
  .animate-spin {
    animation: none;
  }
  
  .hover-lift:hover,
  .hover-scale:hover {
    transform: none;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .error-page {
    background: #000000;
  }
  
  .detail-card,
  .status-card,
  .help-card,
  .modal {
    background: #1a1a1a;
    border-color: #ffffff;
  }
  
  .error-title,
  .error-number {
    color: #ffff00;
  }
  
  .help-link,
  .form-input,
  .form-textarea {
    border-color: #ffffff;
    color: #ffffff;
  }
}
</style>

