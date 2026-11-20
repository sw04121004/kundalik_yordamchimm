<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useAuthStore } from './store/auth'
import { useThemeStore } from './store/theme'
import { usePlannerStore } from './store/planner'
import { useI18n } from './i18n'

const auth = useAuthStore()
const theme = useThemeStore()
const planner = usePlannerStore()
const { t } = useI18n()
const globalError = ref('')
const showGlobalError = (event) => {
  globalError.value = event?.detail?.message || t('common.unexpectedError')
}

// Foydalanuvchi tizimga kirishi bilanoq avtomatik rejalarni yuklash va eslatmalarni boshlash
watch(
  () => auth.isAuthenticated,
  (isAuth) => {
    if (isAuth) {
      auth.fetchMe()
      planner.fetchTasks().then(() => {
        planner.startNotifications()
      })
    } else {
      planner.stopNotifications()
    }
  },
  { immediate: true }
)

onMounted(() => {
  window.addEventListener('app-unexpected-error', showGlobalError)
  theme.init()
})

onUnmounted(() => window.removeEventListener('app-unexpected-error', showGlobalError))
</script>

<template>
  <div v-if="globalError" class="fixed top-4 left-1/2 -translate-x-1/2 z-[100] w-[calc(100%-2rem)] max-w-lg rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-800 shadow-lg dark:border-red-900/60 dark:bg-red-950/90 dark:text-red-200" role="alert">
    <div class="flex items-start justify-between gap-3">
      <span>{{ globalError }}</span>
      <button type="button" class="shrink-0 rounded px-1 text-lg leading-5" :aria-label="t('common.closeAlert')" @click="globalError = ''">×</button>
    </div>
  </div>

  <!-- In-app Planner Reminder Modal/Toast -->
  <transition name="toast-slide">
    <div
      v-if="planner.activeReminder"
      class="fixed top-5 left-1/2 -translate-x-1/2 z-[110] w-[calc(100%-2rem)] max-w-md card p-4 sm:p-5 shadow-2xl border-2 border-brand-500 bg-white/95 dark:bg-[#1b202a]/95 backdrop-blur-md"
      role="alert"
    >
      <div class="flex items-start gap-3">
        <div class="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-600 dark:text-brand-400 flex items-center justify-center shrink-0 text-xl">
          ⏰
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-xs font-bold text-brand-600 dark:text-brand-400 uppercase tracking-wider mb-0.5">
            {{ t('planner.reminder.dueTitle') }}
          </p>
          <h3 class="text-base font-bold text-slate-900 dark:text-white truncate">
            {{ planner.activeReminder.title }}
          </h3>
          <p v-if="planner.activeReminder.due_time" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 font-mono">
            {{ planner.activeReminder.due_time.slice(0, 5) }}
          </p>
        </div>
        <button
          type="button"
          class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-lg leading-none p-1"
          @click="planner.dismissReminder()"
        >
          ×
        </button>
      </div>

      <div class="flex items-center gap-2 mt-4">
        <button
          type="button"
          class="btn-primary flex-1 text-xs py-2 px-3"
          @click="planner.toggleTask(planner.activeReminder)"
        >
          ✓ {{ t('planner.reminder.done') }}
        </button>
        <button
          type="button"
          class="btn-secondary flex-1 text-xs py-2 px-3"
          @click="planner.snoozeTask(planner.activeReminder, 10)"
        >
          ⏱️ {{ t('planner.reminder.snooze10') }}
        </button>
      </div>
    </div>
  </transition>

  <!-- Overdue tasks summary banner on initial load -->
  <transition name="toast-slide">
    <div
      v-if="planner.overdueSummaryCount > 0 && !planner.activeReminder"
      class="fixed bottom-5 right-5 z-[90] max-w-sm card p-3 sm:p-4 shadow-xl border border-amber-300 dark:border-amber-700/60 bg-amber-50/95 dark:bg-amber-950/90 backdrop-blur-md flex items-center gap-3 text-sm text-amber-900 dark:text-amber-100"
      role="status"
    >
      <span class="text-xl">⚠️</span>
      <div class="flex-1 min-w-0">
        <p class="font-medium text-xs sm:text-sm">
          {{ planner.overdueSummaryCount }} {{ t('planner.reminder.overdueSummary') }}
        </p>
      </div>
      <router-link
        :to="{ name: 'planner' }"
        class="text-xs font-bold underline shrink-0 hover:text-amber-700 dark:hover:text-amber-300"
        @click="planner.clearOverdueSummary()"
      >
        {{ t('nav.planner') }}
      </router-link>
      <button
        type="button"
        class="text-amber-700 dark:text-amber-300 hover:text-amber-900 text-base leading-none px-1"
        @click="planner.clearOverdueSummary()"
      >
        ×
      </button>
    </div>
  </transition>

  <router-view v-slot="{ Component }">
    <transition name="page-fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>
