<template>
  <div class="register">
    <div class="container">
      <div class="register-wrapper">
        <div class="register-card" data-aos="fade-up">
          <div class="register-header">
            <h1>Регистрация</h1>
            <p>Создайте аккаунт для доступа к порталу</p>
          </div>

          <div v-if="error" class="error">
            {{ error }}
          </div>

          <div v-if="success" class="success">
            Регистрация успешна! Теперь вы можете войти в систему.
          </div>

          <form @submit.prevent="handleRegister" class="register-form">
            <div class="form-group">
              <label for="username" class="form-label">
                <i class="fas fa-user"></i>
                Имя пользователя
              </label>
              <input
                id="username"
                v-model="form.username"
                type="text"
                class="form-input"
                placeholder="Введите имя пользователя"
                required
                minlength="3"
              />
            </div>

            <div class="form-group">
              <label for="email" class="form-label">
                <i class="fas fa-envelope"></i>
                Email
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="form-input"
                placeholder="Введите email"
                required
              />
            </div>

            <div class="form-group">
              <label for="password" class="form-label">
                <i class="fas fa-lock"></i>
                Пароль
              </label>
              <div class="password-input">
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Введите пароль"
                  required
                  minlength="6"
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                >
                  <i
                    :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"
                  ></i>
                </button>
              </div>
              <div class="password-strength">
                <div class="strength-bar" :class="passwordStrength.class">
                  <div
                    class="strength-fill"
                    :style="{ width: passwordStrength.width }"
                  ></div>
                </div>
                <span class="strength-text">{{ passwordStrength.text }}</span>
              </div>
            </div>

            <div class="form-group">
              <label for="confirmPassword" class="form-label">
                <i class="fas fa-lock"></i>
                Подтвердите пароль
              </label>
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                type="password"
                class="form-input"
                placeholder="Подтвердите пароль"
                required
              />
              <div
                v-if="form.confirmPassword && !passwordsMatch"
                class="field-error"
              >
                Пароли не совпадают
              </div>
            </div>

            <button
              type="submit"
              class="btn btn-primary register-btn"
              :disabled="loading || !isFormValid"
              @click="handleRegister()"
            >
              <i v-if="loading" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-user-plus"></i>
              {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
            </button>
          </form>

          <div class="register-footer">
            <p>
              Уже есть аккаунт?
              <router-link to="/login" class="link">Войти</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      showPassword: false,
      success: false
    }
  },
  computed: {
    ...mapState(['loading', 'error']),
    passwordsMatch() {
      return this.form.password === this.form.confirmPassword
    },
    passwordStrength() {
      const password = this.form.password
      if (!password) return { class: '', width: '0%', text: '' }

      let score = 0
      if (password.length >= 6) score++
      if (password.length >= 8) score++
      if (/[A-Z]/.test(password)) score++
      if (/[a-z]/.test(password)) score++
      if (/[0-9]/.test(password)) score++
      if (/[^A-Za-z0-9]/.test(password)) score++

      if (score < 2) return { class: 'weak', width: '25%', text: 'Слабый' }
      if (score < 4) return { class: 'medium', width: '50%', text: 'Средний' }
      if (score < 5) return { class: 'strong', width: '75%', text: 'Сильный' }
      return { class: 'very-strong', width: '100%', text: 'Очень сильный' }
    },
    isFormValid() {
      return (
        this.form.username.length >= 3 &&
        this.form.email &&
        this.form.password.length >= 6 &&
        this.passwordsMatch
      )
    }
  },
  methods: {
    async handleRegister() {
      if (!this.isFormValid) return
      console.log('Form data:', this.form)
      const result = await this.$store.dispatch('register', {
        username: this.form.username,
        email: this.form.email,
        password: this.form.password
      })

      if (result.success) {
        this.success = true
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      }
    }
  }
}
</script>

<style scoped>
.register {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.register-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100%;
}

.register-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  width: 100%;
  max-width: 500px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.5rem;
}

.register-header p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.register-form {
  margin-bottom: 2rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.password-input {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.password-toggle:hover {
  color: #ffd700;
}

.password-strength {
  margin-top: 0.5rem;
}

.strength-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.strength-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.strength-bar.weak .strength-fill {
  background: #ff4757;
}

.strength-bar.medium .strength-fill {
  background: #ffa502;
}

.strength-bar.strong .strength-fill {
  background: #2ed573;
}

.strength-bar.very-strong .strength-fill {
  background: #1e90ff;
}

.strength-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.field-error {
  color: #ff4757;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.register-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  margin-top: 1rem;
}

.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-footer {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.register-footer p {
  color: rgba(255, 255, 255, 0.8);
}

.link {
  color: #ffd700;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.link:hover {
  color: #ffed4e;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .register-card {
    padding: 2rem;
    margin: 1rem;
  }

  .register-header h1 {
    font-size: 1.75rem;
  }
}
</style>
