import { defineStore } from 'pinia'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'
import { useAiStore } from './ai'
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
        return { success: true }
      } catch (error) {
        return { success: false, message: extractErrorMessage(error, "Ro‘yxatdan o‘tishda xatolik yuz berdi.") }
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
        // Login xatolarida backend kutubxonasi (SimpleJWT) ba'zan inglizcha
        // xabar qaytaradi ("No active account found..."). Foydalanuvchiga
        // har doim o'zbekcha, tushunarli xabar ko'rsatish uchun kutubxona
        // matnini emas, o'zimizning xabarimizni ishlatamiz.
        return { success: false, message: "Login yoki parol noto‘g‘ri." }
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

    logout() {
      this.clearTokens()
      // Oldingi foydalanuvchining shaxsiy ma'lumotlari (AI suhbatlari, sevimlilar)
      // xotirada qolib ketmasligi uchun tegishli store'larni tozalaymiz —
      // aks holda keyingi login qilgan boshqa foydalanuvchi ularni ko'rib qolishi mumkin.
      useAiStore().$reset()
      useServicesStore().$patch({ favorites: [], favoritesLoaded: false })
    },
  },
})
