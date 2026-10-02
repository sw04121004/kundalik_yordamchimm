import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/static/',
  plugins: [vue()],
  build: {
    outDir: '../backend/static/frontend',
    emptyOutDir: true,
  },
  server: {
    port: 5173,
  },
})
