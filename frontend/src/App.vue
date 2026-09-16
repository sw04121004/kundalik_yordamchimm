<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './store/auth'
import { useThemeStore } from './store/theme'

const auth = useAuthStore()
const theme = useThemeStore()

onMounted(() => {
  theme.init()
  if (auth.isAuthenticated) {
    auth.fetchMe()
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
