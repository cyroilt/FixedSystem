<template>
  <div class="login">
    <div class="container">
      <div class="login-wrapper">
        <div class="login-card" data-aos="fade-up">
          <div class="login-header">
            <h1>Вход в систему</h1>
            <p>Войдите в свой аккаунт для доступа к порталу</p>
          </div>
          
          <div v-if="error" class="error">
            {{ error }}
          </div>
          
          <form @submit.prevent="handleLogin" class="login-form">
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
              >
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
                >
                <button
                  type="button"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                >
                  <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>
            
            <button
              type="submit"
              class="btn btn-primary login-btn"
              :disabled="loading"
            >
              <i v-if="loading" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-sign-in-alt"></i>
              {{ loading ? 'Вход...' : 'Войти' }}
            </button>
          </form>
          
          <div class="login-footer">
            <p>Нет аккаунта? 
              <router-link to="/register" class="link">Зарегистрироваться</router-link>
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
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      showPassword: false
    }
  },
  computed: {
    ...mapState(['loading', 'error'])
  },
  methods: {
    async handleLogin() {
      try {
        const result = await this.$store.dispatch('login', this.form)
        if (result.success) {
          // Redirect to intended page or home
          const redirect = this.$route.query.redirect || '/'
          this.$router.push(redirect)
        }
      } catch (error) {
        console.error('Login error:', error)
      }
    }
  }
}
</script>

<style scoped>
.login {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100%;
}

.login-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  width: 100%;
  max-width: 450px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.login-form {
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

.login-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  margin-top: 1rem;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.login-footer p {
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
  .login-card {
    padding: 2rem;
    margin: 1rem;
  }
  
  .login-header h1 {
    font-size: 1.75rem;
  }
}
</style>