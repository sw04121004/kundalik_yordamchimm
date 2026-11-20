import { defineStore } from 'pinia'
import api from '../api/axios'
import { extractErrorMessage, extractFieldErrors } from '../api/errors'
import { useAiStore } from './ai'
import { usePlannerStore } from './planner'
import { useServicesStore } from './services'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    access: localStorage.getItem('qulay_access') || null,
    refresh: localStorage.getItem('qulay_refresh') || null,
    loading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.access,
  },

  actions: {
    setTokens(access, refresh) {
      this.access = access
      this.refresh = refresh
      localStorage.setItem('qulay_access', access)
      localStorage.setItem('qulay_refresh', refresh)
    },

    clearTokens() {
      this.access = null
      this.refresh = null
      this.user = null
      localStorage.removeItem('qulay_access')
      localStorage.removeItem('qulay_refresh')
    },

    async register(payload) {
      this.loading = true
      try {
        const { data } = await api.post('/auth/register/', payload)
        this.setTokens(data.access, data.refresh)
        this.user = data.user
        await this.fetchMe()
        return { success: true }
      } catch (error) {
        const backendErrors = extractFieldErrors(error)
        const message = extractErrorMessage(error, "Ro'yxatdan o'tishda xatolik yuz berdi.")
        return { success: false, message, errors: backendErrors }
      } finally {
        this.loading = false
      }
    },

    async login(payload) {
      this.loading = true
      try {
        const { data } = await api.post('/auth/login/', payload)
        this.setTokens(data.access, data.refresh)
        await this.fetchMe()
        return { success: true }
      } catch (error) {
        const message = error.response?.status === 401
          ? "Login yoki parol noto'g'ri."
          : extractErrorMessage(error, "Login yoki parol noto'g'ri.")
        return { success: false, message }
      } finally {
        this.loading = false
      }
    },

    async fetchMe() {
      try {
        const { data } = await api.get('/auth/me/')
        this.user = data
      } catch (error) {
        // token invalid, log the user out silently
        this.clearTokens()
      }
    },

    async updateProfile(payload) {
      this.loading = true
      try {
        const { data } = await api.patch('/auth/me/', payload)
        this.user = data
        return { success: true }
      } catch (error) {
        return { success: false, message: extractErrorMessage(error, 'Profilni yangilab bo‘lmadi.') }
      } finally {
        this.loading = false
      }
    },

    async changePassword(payload) {
      this.loading = true
      try {
        await api.post('/auth/change-password/', payload)
        return { success: true }
      } catch (error) {
        return { success: false, message: extractErrorMessage(error, 'Parolni o‘zgartirib bo‘lmadi.') }
      } finally {
        this.loading = false
      }
    },

    clearSession() {
      const currentUserId = this.user?.id
      this.clearTokens()
      // Oldingi foydalanuvchining shaxsiy ma'lumotlari (AI suhbatlari, sevimlilar, reja)
      // xotirada qolib ketmasligi uchun tegishli store'larni tozalaymiz
      useAiStore().$reset()
      usePlannerStore().$reset()
      useServicesStore().$patch({ favorites: [], favoritesLoaded: false, categories: [], loaded: false })

      // Eski umumiy (id-siz) kalitlarni ham, guest kalitlarni ham to'liq tozalash
      const legacyKeys = [
        'qulay_goals', 'qulay_goals_guest',
        'qulay_habits', 'qulay_habits_guest',
        'pomodoroState', 'pomodoroState_guest',
        'pomodoro_state', 'pomodoro_state_guest',
        'qulay_weather_location', 'qulay_weather_location_guest',
        'qulay_notified_guest',
      ]
      legacyKeys.forEach(k => localStorage.removeItem(k))

      // Joriy foydalanuvchiga tegishli kalitlarni tozalash
      if (currentUserId) {
        localStorage.removeItem(`qulay_goals_${currentUserId}`)
        localStorage.removeItem(`qulay_habits_${currentUserId}`)
        localStorage.removeItem(`pomodoroState_${currentUserId}`)
        localStorage.removeItem(`pomodoro_state_${currentUserId}`)
        localStorage.removeItem(`qulay_notified_${currentUserId}`)
        localStorage.removeItem(`qulay_weather_location_${currentUserId}`)
        localStorage.removeItem(`qulay_finance_txs_${currentUserId}`)
        localStorage.removeItem(`qulay_finance_migrated_v1_${currentUserId}`)
      }

      // Har qanday boshqa qulay_* foydalanuvchi ma'lumotlari bo'lsa (faqat 4 ta qurilma sozlamasi qoladi)
      // Qurilma sozlamalari: qulay_language, qulay_accent, qulay_dark, qulay_animations
      try {
        const preserveKeys = new Set(['qulay_language', 'qulay_accent', 'qulay_dark', 'qulay_animations'])
        const keysToRemove = []
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i)
          if (key && !preserveKeys.has(key)) {
            if (key.startsWith('qulay_') || key.startsWith('pomodoro')) {
              keysToRemove.push(key)
            }
          }
        }
        keysToRemove.forEach(k => localStorage.removeItem(k))
      } catch {}
    },

    async logout() {
      try {
        if (this.refresh) await api.post('/auth/logout/', { refresh: this.refresh })
      } catch {
        // Always clear this browser session even if the server cannot be reached.
      } finally {
        this.clearSession()
      }
    },

    async deleteAccount(currentPassword, confirmation = '') {
      this.loading = true
      try {
        const payload = { current_password: currentPassword }
        if (confirmation) payload.confirmation = confirmation
        await api.delete('/auth/account/', { data: payload })
        this.clearSession()
        return { success: true }
      } catch (error) {
        return { success: false, message: extractErrorMessage(error, 'Akkauntni o‘chirib bo‘lmadi.') }
      } finally {
        this.loading = false
      }
    },
  },
})

if (typeof window !== 'undefined') {
  window.addEventListener('auth-session-expired', () => {
    try {
      const auth = useAuthStore()
      auth.clearSession()
    } catch {
      // pinia might not be ready yet
    }
  })
}
