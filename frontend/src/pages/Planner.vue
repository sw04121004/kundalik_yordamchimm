<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { usePlannerStore } from '../store/planner'
import { useI18n } from '../i18n'
import AppHeader from '../components/AppHeader.vue'
import FormAlert from '../components/FormAlert.vue'
import { CalendarDays } from 'lucide-vue-next'
import { getTaskStatus, runReminderSelfTests } from '../utils/plannerReminders'

const planner = usePlannerStore()
const { t, locale } = useI18n()
const form = reactive({ title: '', due_date: '', due_time: '' })
const submitting = ref(false)

onMounted(() => {
  planner.fetchTasks()
  runReminderSelfTests()
})

function todayISO() {
  const d = new Date()
  return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10)
}
const today = todayISO()

async function addTask() {
  if (!form.title.trim()) {
    planner.error = t('planner.error.empty')
    return
  }
  if (form.due_date && form.due_date < today) {
    planner.error = t('planner.error.pastDate')
    return
  }
  submitting.value = true
  const result = await planner.createTask({
    title: form.title.trim(),
    due_date: form.due_date || null,
    due_time: form.due_time || null,
  })
  submitting.value = false
  if (result.success) {
    form.title = ''
    form.due_date = ''
    form.due_time = ''
  }
}

const groups = computed(() => {
  const todayList = [], upcoming = [], someday = []
  for (const item of planner.tasks) {
    if (!item.due_date) someday.push(item)
    else if (item.due_date === today) todayList.push(item)
    else if (item.due_date > today) upcoming.push(item)
    else if (!item.is_done) todayList.push(item)
  }
  return [
    { label: `☀️ ${t('planner.today')}`, items: todayList },
    { label: `📅 ${t('planner.upcoming')}`, items: upcoming },
    { label: `🗂️ ${t('planner.someday')}`, items: someday },
  ].filter(g => g.items.length)
})

function formatDate(d) {
  if (!d) return ''
  const [y, m, day] = d.split('-').map(Number)
  return new Intl.DateTimeFormat(locale(), { day: 'numeric', month: 'short' }).format(new Date(y, m - 1, day))
}
function formatTime(val) { return val ? val.slice(0, 5) : '' }
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-[#111318]">
    <AppHeader />

    <main class="max-w-2xl mx-auto px-4 sm:px-6 py-10 animate-fadeUp">
      <!-- Back -->
      <router-link :to="{ name: 'dashboard' }" class="inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 transition-colors mb-6">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        {{ t('planner.back') }}
      </router-link>

      <!-- Title -->
      <div class="flex items-center gap-3 mb-6">
        <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-brand-700 dark:text-brand-300 border border-brand-200/70 dark:border-brand-700/50 shadow-sm bg-gradient-to-br from-brand-100 to-emerald-50 dark:from-brand-900/60 dark:to-emerald-950/50">
          <CalendarDays class="w-6 h-6" aria-hidden="true" />
        </div>
        <div>
          <h1 class="text-xl font-bold text-slate-900 dark:text-white">{{ t('planner.title') }}</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400">{{ t('planner.subtitle') }}</p>
        </div>
      </div>

      <!-- Notification Permission & Offline notice banner -->
      <div class="card p-4 mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs bg-white dark:bg-white/[0.02]">
        <div class="flex items-center gap-3">
          <span class="text-2xl shrink-0">🔔</span>
          <div>
            <div class="font-semibold text-slate-800 dark:text-slate-200">
              <span v-if="planner.notificationPermission === 'granted'" class="text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                <span>✓</span> {{ t('planner.reminders.enabled') }}
              </span>
              <span v-else-if="planner.notificationPermission === 'denied'" class="text-red-600 dark:text-red-400 font-bold flex items-center gap-1">
                <span>✕</span> {{ t('planner.reminders.blocked') }}
              </span>
              <span v-else-if="planner.notificationPermission === 'unsupported'" class="text-slate-500">
                {{ t('planner.reminders.unsupported') }}
              </span>
              <span v-else class="text-slate-700 dark:text-slate-300">
                {{ t('planner.reminders.enable') }}
              </span>
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
              <span v-if="planner.notificationPermission === 'denied'">
                {{ t('planner.reminders.blockedDesc') }}
              </span>
              <span v-else>
                {{ t('planner.reminders.offlineNotice') }}
              </span>
            </p>
          </div>
        </div>
        <button
          v-if="planner.notificationPermission === 'default'"
          type="button"
          class="btn-primary text-xs py-1.5 px-3 self-start sm:self-auto shrink-0"
          @click="planner.requestNotificationPermission()"
        >
          🔔 {{ t('planner.reminders.enable') }}
        </button>
      </div>

      <!-- Add task form -->
      <div class="card p-5 mb-8">
        <FormAlert :message="planner.error" class="mb-4" />
        <form class="space-y-3" @submit.prevent="addTask">
          <input
            v-model="form.title"
            type="text"
            class="input"
            :placeholder="t('planner.new')"
          />
          <div class="grid grid-cols-2 gap-3">
            <input v-model="form.due_date" type="date" class="input" :min="today" />
            <input v-model="form.due_time" type="time" class="input" />
          </div>
          <button type="submit" class="btn-primary w-full" :disabled="submitting">
            <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            {{ submitting ? '...' : `+ ${t('planner.add')}` }}
          </button>
        </form>
      </div>

      <!-- Loading -->
      <div v-if="planner.loading" class="text-center py-12 text-slate-400">
        <div class="w-7 h-7 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin mx-auto mb-3"></div>
        {{ t('planner.loading') }}
      </div>

      <!-- Empty state -->
      <div v-else-if="!planner.tasks.length" class="text-center py-16 border-2 border-dashed border-slate-200 dark:border-slate-700/50 rounded-2xl">
        <div class="text-4xl mb-3 opacity-40">🗒️</div>
        <p class="font-semibold text-slate-600 dark:text-slate-400">{{ t('planner.empty') }}</p>
        <p class="text-sm text-slate-400 mt-1">{{ t('planner.first') }}</p>
      </div>

      <!-- Task groups -->
      <div v-else class="space-y-6 stagger-children">
        <section v-for="group in groups" :key="group.label">
          <h2 class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">{{ group.label }}</h2>
          <div class="card divide-y divide-slate-100 dark:divide-slate-800/80 overflow-hidden">
            <div
              v-for="task in group.items"
              :key="task.id"
              class="flex items-center gap-3 px-4 py-3.5 group/task transition-colors hover:bg-slate-50 dark:hover:bg-white/[0.02]"
              :class="task.is_done ? 'opacity-60' : ''"
            >
              <!-- Checkbox -->
              <button
                class="w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 transition-all duration-200 focus:outline-none"
                :class="task.is_done
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-slate-300 dark:border-slate-600 hover:border-brand-500'"
                @click="planner.toggleTask(task)"
              >
                <svg v-if="task.is_done" class="w-3 h-3 animate-checkPop" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
                </svg>
              </button>

              <!-- Task info -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium truncate transition-all"
                  :class="task.is_done ? 'text-slate-400 line-through' : 'text-slate-800 dark:text-slate-100'">
                  {{ task.title }}
                </p>
                <div v-if="task.due_date || task.due_time" class="flex items-center gap-1.5 mt-0.5 flex-wrap">
                  <span v-if="task.due_date" class="text-[11px] font-medium text-slate-400">{{ formatDate(task.due_date) }}</span>
                  <span v-if="task.due_time" class="text-[11px] font-semibold text-brand-600 dark:text-brand-400 font-mono">{{ formatTime(task.due_time) }}</span>
                  <span
                    v-if="!task.is_done && getTaskStatus(task) === 'overdue'"
                    class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-100 text-red-700 dark:bg-red-950/60 dark:text-red-300 border border-red-200/50"
                  >
                    {{ t('planner.status.overdue') }}
                  </span>
                  <span
                    v-else-if="!task.is_done && getTaskStatus(task) === 'approaching'"
                    class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200/50 animate-pulse"
                  >
                    {{ t('planner.status.approaching') }}
                  </span>
                </div>
              </div>

              <!-- Delete -->
              <button
                class="w-7 h-7 rounded-lg flex items-center justify-center text-slate-300 dark:text-slate-600 opacity-0 group-hover/task:opacity-100 hover:bg-red-50 dark:hover:bg-red-500/10 hover:text-red-500 transition-all focus:outline-none focus:opacity-100"
                @click="planner.deleteTask(task.id)"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>
