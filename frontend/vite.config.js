import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8081,
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Change to 5000 if using default Flask port
        changeOrigin: true,
        secure: false,
      }
    }
  }
})