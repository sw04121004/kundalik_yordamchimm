<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useAuthStore } from './store/auth'
import { useThemeStore } from './store/theme'
import { usePlannerStore } from './store/planner'

const auth = useAuthStore()
const theme = useThemeStore()
const planner = usePlannerStore()
const globalError = ref('')
const showGlobalError = () => { globalError.value = "Kutilmagan xatolik yuz berdi. Sahifani yangilab yoki birozdan so'ng qayta urinib ko'ring." }

onMounted(() => {
  window.addEventListener('app-unexpected-error', showGlobalError)
  theme.init()
  if (auth.isAuthenticated) {
    auth.fetchMe()
    planner.fetchTasks().then(() => {
      planner.startNotifications()
    })
  }
})

onUnmounted(() => window.removeEventListener('app-unexpected-error', showGlobalError))
</script>

<template>
  <div v-if="globalError" class="fixed top-4 left-1/2 -translate-x-1/2 z-[100] w-[calc(100%-2rem)] max-w-lg rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-800 shadow-lg dark:border-red-900/60 dark:bg-red-950/90 dark:text-red-200" role="alert">
    <div class="flex items-start justify-between gap-3">
      <span>{{ globalError }}</span>
      <button type="button" class="shrink-0 rounded px-1 text-lg leading-5" aria-label="Xabarni yopish" @click="globalError = ''">×</button>
    </div>
  </div>
  <router-view v-slot="{ Component }">
    <transition name="page-fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>
