<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import ThemeSwitcher from './ThemeSwitcher.vue'

const router = useRouter()
const auth = useAuthStore()
const menuOpen = ref(false)

function handleLogout() {
  auth.logout()
  router.push({ name: 'landing' })
}
</script>

<template>
  <header class="sticky top-0 z-40 backdrop-blur-md bg-white/80 dark:bg-slate-900/70 border-b border-slate-100 dark:border-white/5 transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
      <router-link :to="{ name: 'dashboard' }" class="flex items-center gap-2 shrink-0 group">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-extrabold shadow-soft group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300 animate-float">
          Q
        </div>
        <span class="font-extrabold text-lg text-slate-800 dark:text-slate-100 hidden sm:inline">Kundalik Yordamchi</span>
      </router-link>

      <nav class="hidden md:flex items-center gap-1">
        <router-link
          :to="{ name: 'dashboard' }"
          class="relative px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          :class="$route.name === 'dashboard' ? 'text-brand-700 dark:text-brand-300' : 'text-slate-500 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-300'"
        >
          <span
            v-if="$route.name === 'dashboard'"
            class="absolute inset-0 rounded-lg bg-brand-50 dark:bg-white/5 -z-10"
            :style="{ boxShadow: 'inset 0 0 0 1px rgb(var(--brand-500) / 0.25), 0 0 16px -4px rgb(var(--brand-500) / 0.35)' }"
          ></span>
          Xizmatlar
        </router-link>
        <router-link
          :to="{ name: 'ai-assistant' }"
          class="relative px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-1.5"
          :class="$route.name === 'ai-assistant' ? 'text-brand-700 dark:text-brand-300' : 'text-slate-500 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-300'"
        >
          <span
            v-if="$route.name === 'ai-assistant'"
            class="absolute inset-0 rounded-lg bg-brand-50 dark:bg-white/5 -z-10"
            :style="{ boxShadow: 'inset 0 0 0 1px rgb(var(--brand-500) / 0.25), 0 0 16px -4px rgb(var(--brand-500) / 0.35)' }"
          ></span>
          🤖 AI Yordamchi
        </router-link>
        <router-link
          :to="{ name: 'planner' }"
          class="relative px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-1.5"
          :class="$route.name === 'planner' ? 'text-brand-700 dark:text-brand-300' : 'text-slate-500 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-300'"
        >
          <span
            v-if="$route.name === 'planner'"
            class="absolute inset-0 rounded-lg bg-brand-50 dark:bg-white/5 -z-10"
            :style="{ boxShadow: 'inset 0 0 0 1px rgb(var(--brand-500) / 0.25), 0 0 16px -4px rgb(var(--brand-500) / 0.35)' }"
          ></span>
          📅 Reja
        </router-link>
      </nav>

      <div class="flex items-center gap-2 sm:gap-3">
        <span v-if="auth.user" class="hidden lg:block text-sm text-slate-500 dark:text-slate-400">
          Salom, <span class="font-semibold text-slate-700 dark:text-slate-200">{{ auth.user.first_name || auth.user.username }}</span>
        </span>
        <ThemeSwitcher />
        <div class="relative">
          <button
            class="w-9 h-9 rounded-full bg-brand-100 dark:bg-white/5 text-brand-700 dark:text-brand-300 font-bold flex items-center justify-center hover:bg-brand-200 dark:hover:bg-white/10 transition-all duration-200 hover:scale-105 active:scale-95"
            @click="menuOpen = !menuOpen"
          >
            {{ (auth.user?.username || 'U').charAt(0).toUpperCase() }}
          </button>
          <transition name="pop">
            <div
              v-if="menuOpen"
              class="absolute right-0 mt-3 w-48 glass-surface p-2 text-sm z-50 origin-top-right"
              @click="menuOpen = false"
            >
              <router-link
                :to="{ name: 'ai-assistant' }"
                class="md:hidden w-full text-left px-3 py-2 rounded-lg hover:bg-brand-50 dark:hover:bg-white/5 text-slate-600 dark:text-slate-300 font-medium transition-colors duration-200 flex items-center gap-1.5"
              >
                🤖 AI Yordamchi
              </router-link>
              <router-link
                :to="{ name: 'planner' }"
                class="md:hidden w-full text-left px-3 py-2 rounded-lg hover:bg-brand-50 dark:hover:bg-white/5 text-slate-600 dark:text-slate-300 font-medium transition-colors duration-200 flex items-center gap-1.5"
              >
                📅 Reja
              </router-link>
              <router-link
                :to="{ name: 'profile' }"
                class="w-full text-left px-3 py-2 rounded-lg hover:bg-brand-50 dark:hover:bg-white/5 text-slate-600 dark:text-slate-300 font-medium transition-colors duration-200 flex items-center gap-1.5"
              >
                👤 Profil
              </router-link>
              <button
                class="w-full text-left px-3 py-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-500/10 text-red-600 dark:text-red-400 font-medium transition-colors duration-200"
                @click="handleLogout"
              >
                Chiqish
              </button>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </header>
</template>
