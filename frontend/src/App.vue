<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer
  },
  created() {
    this.$store.dispatch('fetchCategories')
    this.$store.dispatch('fetchTags')
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  min-height: 100vh;
  color: #ffffff;
}

/* Memory Pages specific styling */
body.memory-pages {
  background: linear-gradient(
    135deg,
    #8b0000 0%,
    #dc143c 25%,
    #ff4500 50%,
    #ff6347 75%,
    #ffa500 100%
  );
  animation: memoryGradient 10s ease infinite;
}

@keyframes memoryGradient {
  0%,
  100% {
    background: linear-gradient(
      135deg,
      #8b0000 0%,
      #dc143c 25%,
      #ff4500 50%,
      #ff6347 75%,
      #ffa500 100%
    );
  }
  25% {
    background: linear-gradient(
      135deg,
      #dc143c 0%,
      #ff4500 25%,
      #ff6347 50%,
      #ffa500 75%,
      #ffd700 100%
    );
  }
  50% {
    background: linear-gradient(
      135deg,
      #ff4500 0%,
      #ff6347 25%,
      #ffa500 50%,
      #ffd700 75%,
      #dc143c 100%
    );
  }
  75% {
    background: linear-gradient(
      135deg,
      #ff6347 0%,
      #ffa500 25%,
      #ffd700 50%,
      #8b0000 75%,
      #dc143c 100%
    );
  }
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 80px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
  text-align: center;
}

.btn-primary {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #1e3c72;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
}

/* Memory Pages button styling */
.btn-memory {
  background: linear-gradient(45deg, #ffd700, #ffa500);
  color: #8b0000;
  border: 2px solid #ffd700;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.btn-memory:hover {
  background: linear-gradient(45deg, #ffa500, #ff6347);
  color: #ffffff;
  border-color: #ff6347;
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(255, 165, 0, 0.4);
}

.btn-secondary {
  background: transparent;
  color: #ffd700;
  border: 2px solid #ffd700;
}

.btn-secondary:hover {
  background: #ffd700;
  color: #1e3c72;
}

.btn-danger {
  background: linear-gradient(45deg, #ff4757, #ff6b7a);
  color: white;
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 71, 87, 0.3);
}

.card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

/* Memory Pages card styling */
.memory-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  border: 2px solid rgba(255, 215, 0, 0.3);
  box-shadow: 0 8px 32px rgba(139, 0, 0, 0.3);
  transition: all 0.4s ease;
}

.memory-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 25px 50px rgba(139, 0, 0, 0.4);
  border-color: rgba(255, 215, 0, 0.6);
}

.veteran-card {
  background: linear-gradient(
    145deg,
    rgba(255, 255, 255, 0.1),
    rgba(255, 215, 0, 0.1)
  );
  border: 2px solid rgba(255, 215, 0, 0.4);
  position: relative;
  overflow: hidden;
}

.veteran-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 215, 0, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.veteran-card:hover::before {
  left: 100%;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #ffd700;
}

/* Memory Pages form styling */
.memory-form-label {
  color: #ffd700;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  font-size: 16px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

/* Memory Pages input styling */
.memory-input {
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 215, 0, 0.3);
  color: #ffffff;
  font-weight: 500;
}

.memory-input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.3);
  background: rgba(255, 255, 255, 0.2);
}

.memory-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-select:focus {
  outline: none;
  border-color: #ffd700;
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.loading {
  text-align: center;
  padding: 40px;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top: 4px solid #ffd700;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

/* Memory Pages spinner */
.memory-spinner {
  border: 4px solid rgba(255, 215, 0, 0.3);
  border-top: 4px solid #ffd700;
  animation: spin 1s linear infinite, pulse 2s ease-in-out infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.error {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid rgba(255, 71, 87, 0.3);
}

.success {
  background: rgba(46, 213, 115, 0.2);
  color: #2ed573;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid rgba(46, 213, 115, 0.3);
}

/* Memory Pages alerts */
.memory-success {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.5);
  font-weight: bold;
}

.memory-error {
  background: rgba(220, 20, 60, 0.2);
  color: #ffb6c1;
  border: 1px solid rgba(220, 20, 60, 0.5);
  font-weight: bold;
}

/* Map container styling */
.map-container {
  height: 600px;
  border-radius: 20px;
  overflow: hidden;
  border: 3px solid rgba(255, 215, 0, 0.4);
  box-shadow: 0 10px 40px rgba(139, 0, 0, 0.3);
  position: relative;
}

.map-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1000;
  background: rgba(139, 0, 0, 0.8);
  padding: 15px;
  border-radius: 10px;
  border: 2px solid rgba(255, 215, 0, 0.5);
}

.timeline-control {
  background: rgba(139, 0, 0, 0.9);
  color: #ffd700;
  padding: 20px;
  border-radius: 15px;
  margin: 20px 0;
  border: 2px solid rgba(255, 215, 0, 0.4);
}

.timeline-slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: rgba(255, 215, 0, 0.3);
  outline: none;
  -webkit-appearance: none;
}

.timeline-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #8b0000;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.timeline-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: 2px solid #8b0000;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

/* Stats cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.stat-card {
  background: linear-gradient(
    145deg,
    rgba(139, 0, 0, 0.3),
    rgba(220, 20, 60, 0.2)
  );
  border: 2px solid rgba(255, 215, 0, 0.4);
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 215, 0, 0.1) 0%,
    transparent 70%
  );
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(139, 0, 0, 0.4);
  border-color: rgba(255, 215, 0, 0.8);
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #ffd700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 1;
}

.stat-label {
  font-size: 1.2rem;
  color: #ffffff;
  margin-top: 10px;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

/* Hero section for memory pages */
.memory-hero {
  background: linear-gradient(rgba(139, 0, 0, 0.7), rgba(220, 20, 60, 0.7)),
    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><polygon fill="%23FFD700" points="500,50 600,300 850,300 650,450 750,700 500,550 250,700 350,450 150,300 400,300"/></svg>');
  background-size: 100px 100px, cover;
  background-position: center;
  padding: 100px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.memory-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 215, 0, 0.1) 50%,
    transparent 70%
  );
  animation: heroShine 8s ease-in-out infinite;
}

@keyframes heroShine {
  0%,
  100% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
}

.memory-title {
  font-size: 4rem;
  font-weight: bold;
  color: #ffd700;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.memory-subtitle {
  font-size: 1.5rem;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 1;
}

/* Veteran photo styling */
.veteran-photo {
  width: 150px;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  border: 3px solid #ffd700;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.veteran-photo:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
}

.veteran-info {
  flex: 1;
  margin-left: 20px;
}

.veteran-name {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ffd700;
  margin-bottom: 10px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.veteran-dates {
  font-size: 1.1rem;
  color: #ffb6c1;
  margin-bottom: 15px;
  font-style: italic;
}

.veteran-position {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 5px 15px;
  border-radius: 20px;
  display: inline-block;
  font-weight: bold;
  margin-bottom: 15px;
  border: 1px solid rgba(255, 215, 0, 0.4);
}

.veteran-unit {
  color: #ffffff;
  font-weight: 600;
  margin-bottom: 10px;
}

.veteran-biography {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  margin-bottom: 15px;
}

.veteran-awards {
  background: rgba(220, 20, 60, 0.2);
  padding: 10px 15px;
  border-radius: 10px;
  border-left: 4px solid #ffd700;
  margin-bottom: 10px;
}

.veteran-battles {
  background: rgba(255, 69, 0, 0.2);
  padding: 10px 15px;
  border-radius: 10px;
  border-left: 4px solid #ffd700;
}

/* Animation classes */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active {
  transition: all 0.5s ease;
}

.slide-up-enter-from {
  transform: translateY(30px);
  opacity: 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }

  .btn {
    padding: 10px 20px;
    font-size: 14px;
  }

  .card,
  .memory-card {
    padding: 16px;
  }

  .memory-title {
    font-size: 2.5rem;
  }

  .memory-subtitle {
    font-size: 1.2rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }

  .stat-number {
    font-size: 2rem;
  }

  .stat-label {
    font-size: 1rem;
  }

  .veteran-photo {
    width: 120px;
    height: 160px;
  }

  .veteran-info {
    margin-left: 15px;
  }

  .veteran-name {
    font-size: 1.4rem;
  }

  .map-container {
    height: 400px;
  }

  .map-controls {
    position: relative;
    top: 0;
    left: 0;
    margin-bottom: 20px;
  }
}

@media (max-width: 480px) {
  .memory-title {
    font-size: 2rem;
  }

  .memory-subtitle {
    font-size: 1rem;
  }

  .veteran-card {
    flex-direction: column;
    text-align: center;
  }

  .veteran-info {
    margin-left: 0;
    margin-top: 15px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

/* Print styles for memory pages */
@media print {
  body.memory-pages {
    background: white !important;
    color: black !important;
  }

  .memory-card {
    background: white !important;
    border: 2px solid #8b0000 !important;
    box-shadow: none !important;
  }

  .veteran-name {
    color: #8b0000 !important;
  }

  .memory-title {
    color: #8b0000 !important;
  }
}
</style>
