<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './store/auth'
import { useThemeStore } from './store/theme'
import { usePlannerStore } from './store/planner'

const auth = useAuthStore()
const theme = useThemeStore()
const planner = usePlannerStore()

onMounted(() => {
  theme.init()
  if (auth.isAuthenticated) {
    auth.fetchMe()
    planner.fetchTasks().then(() => {
      planner.startNotifications()
    })
  }
})
</script>

<template>
  <router-view v-slot="{ Component }">
    <transition name="page-fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>
