import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { revealDirective } from './directives/reveal'
import './assets/main.css'
import './assets/animations.css'

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
app.mount('#app')
