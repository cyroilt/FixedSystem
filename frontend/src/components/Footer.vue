<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>Faculty Portal</h3>
          <p>Система управления записями факультета с современным интерфейсом и удобной навигацией.</p>
        </div>
        <div class="footer-section">
          <h4>Быстрые ссылки</h4>
          <ul>
            <li><router-link to="/">Главная</router-link></li>
            <li><router-link to="/recordings">Все записи</router-link></li>
            <li v-if="!isAuthenticated"><router-link to="/login">Войти</router-link></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>Контакты</h4>
          <p><i class="fas fa-envelope"></i> info@faculty.edu</p>
          <p><i class="fas fa-phone"></i> +7 (XXX) XXX-XX-XX</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2024 Faculty Portal. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Footer',
  computed: {
    ...mapGetters(['isAuthenticated'])
  }
}
</script>

<style scoped>
.footer {
  background: rgba(30, 60, 114, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 3rem 0 1rem;
  margin-top: 4rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3,
.footer-section h4 {
  color: #ffd700;
  margin-bottom: 1rem;
}

.footer-section p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 0.5rem;
}

.footer-section ul li a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-section ul li a:hover {
  color: #ffd700;
}

.footer-section i {
  margin-right: 0.5rem;
  color: #ffd700;
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
</style>