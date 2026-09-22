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
        const backendMsg = error.response?.data ? Object.values(error.response.data).flat().join(' ') : null
        const message = backendMsg || "Ro‘yxatdan o‘tishda xatolik yuz berdi."
        return { success: false, message }
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
        const backendMsg = error.response?.data ? Object.values(error.response.data).flat().join(' ') : null
        const message = backendMsg || "Login yoki parol noto‘g‘ri."
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
