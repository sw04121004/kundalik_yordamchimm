import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { revealDirective } from './directives/reveal'
import { vTilt, vMagnet, vRipple, vGlow } from './directives/fx'
import './assets/main.css'
import './assets/animations.css'
import { initLanguage } from './i18n'
initLanguage()
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}))
}

const app = createApp(App)

app.config.errorHandler = () => {
  window.dispatchEvent(new Event('app-unexpected-error'))
}
window.addEventListener('unhandledrejection', (event) => {
  event.preventDefault()
  window.dispatchEvent(new Event('app-unexpected-error'))
})

app.use(createPinia())
app.use(router)
app.directive('reveal', revealDirective)
app.directive('tilt', vTilt)
app.directive('magnet', vMagnet)
app.directive('ripple', vRipple)
app.directive('glow', vGlow)
app.mount('#app')
