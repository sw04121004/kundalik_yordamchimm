import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ command }) => ({
  // Django serves production assets from /static/, while Vite's dev server
  // should serve them from the site root so visiting /static/ can load the app.
  base: command === 'serve' ? '/' : '/static/',
  plugins: [vue()],
  build: {
    outDir: '../backend/static/frontend',
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
}))
