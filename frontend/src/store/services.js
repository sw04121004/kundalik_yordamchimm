import { defineStore } from 'pinia'
import api from '../api/axios'

export const useServicesStore = defineStore('services', {
  state: () => ({
    categories: [],
    loaded: false,
    loading: false,

    favorites: [], // array of Favorite objects: { id, service, created_at }
    favoritesLoaded: false,
  }),

  getters: {
    allServices: (state) => state.categories.flatMap((c) => c.services),
    favoriteSlugs: (state) => new Set(state.favorites.map((f) => f.service.slug)),
  },

  actions: {
    async fetchCategories(force = false) {
      console.log('🔵 fetchCategories called, loaded:', this.loaded, 'force:', force);
      if (this.loaded && !force) return;
      this.loading = true;
      console.log('🔵 Starting API request to /categories/');
      try {
        const { data } = await api.get('/categories/');
        console.log('🔵 API response received, items:', data.results.length);
        this.categories = data.results;
        this.loaded = true;
      } catch (error) {
        console.error('❗ Kategoriyalarni yuklashda xatolik:', error);
      } finally {
        this.loading = false; this.loaded = true;
        console.log('🔵 fetchCategories finished, loading:', this.loading);
      }
    },

    async logUsage(serviceSlug) {
      try {
        await api.post('/usage/', { service_slug: serviceSlug })
      } catch (error) {
        // usage logging is best-effort, ignore failures silently
      }
    },

    async fetchFavorites(force = false) {
      if (this.favoritesLoaded && !force) return
      try {
        const { data } = await api.get('/favorites/')
        this.favorites = data
        this.favoritesLoaded = true
      } catch (error) {
        console.error('Sevimlilarni yuklashda xatolik:', error)
      }
    },

    isFavorite(serviceSlug) {
      return this.favoriteSlugs.has(serviceSlug)
    },

    async toggleFavorite(serviceSlug) {
      const alreadyFavorite = this.isFavorite(serviceSlug)
      try {
        if (alreadyFavorite) {
          await api.delete(`/favorites/${serviceSlug}/`)
          this.favorites = this.favorites.filter((f) => f.service.slug !== serviceSlug)
        } else {
          const { data } = await api.post('/favorites/', { service_slug: serviceSlug })
          this.favorites.push(data)
        }
      } catch (error) {
        console.error('Sevimlini yangilashda xatolik:', error)
      }
    },
  },
})
