<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { usePlannerStore } from '../store/planner'
import AppHeader from '../components/AppHeader.vue'
import FormAlert from '../components/FormAlert.vue'

const planner = usePlannerStore()
const form = reactive({ title: '', due_date: '', due_time: '' })
const submitting = ref(false)

onMounted(() => planner.fetchTasks())

function todayISO() {
  const d = new Date()
  return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10)
}
const today = todayISO()

async function addTask() {
  if (!form.title.trim()) { planner.error = 'Vazifa nomini kiriting.'; return }
  if (form.due_date && form.due_date < today) { planner.error = "O'tib ketgan sanaga qo'shib bo'lmaydi."; return }
  submitting.value = true
  const result = await planner.createTask({
    title: form.title.trim(),
    due_date: form.due_date || null,
    due_time: form.due_time || null,
  })
  submitting.value = false
  if (result.success) { form.title = ''; form.due_date = ''; form.due_time = '' }
}

const groups = computed(() => {
  const todayList = [], upcoming = [], someday = []
  for (const t of planner.tasks) {
    if (!t.due_date) someday.push(t)
    else if (t.due_date === today) todayList.push(t)
    else if (t.due_date > today) upcoming.push(t)
    else if (!t.is_done) todayList.push(t)
  }
  return [
    { label: '☀️ Bugun', items: todayList },
    { label: '📅 Kelgusida', items: upcoming },
    { label: '🗂️ Sanasiz', items: someday },
  ].filter(g => g.items.length)
})

const UZ_MONTHS = ['yanvar','fevral','mart','aprel','may','iyun','iyul','avgust','sentabr','oktabr','noyabr','dekabr']
function formatDate(d) {
  if (!d) return ''
  const [, m, day] = d.split('-').map(Number)
  return `${day}-${UZ_MONTHS[m - 1]}`
}
function formatTime(t) { return t ? t.slice(0, 5) : '' }
</script>

<template>
  <div class="min-h-screen bg-[#f4f6fb] dark:bg-[#0d1117]">
    <AppHeader />

    <main class="max-w-2xl mx-auto px-4 sm:px-6 py-10 animate-fadeUp">
      <!-- Back -->
      <router-link :to="{ name: 'dashboard' }" class="inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 transition-colors mb-6">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        Orqaga
      </router-link>

      <!-- Title -->
      <div class="flex items-center gap-3 mb-6">
        <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shadow-sm text-white"
          style="background: linear-gradient(135deg, rgb(var(--brand-500)), rgb(var(--brand-700)))">📅</div>
        <div>
          <h1 class="text-xl font-bold text-slate-900 dark:text-white">Reja / To-do</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400">Kunlik vazifalaringiz</p>
        </div>
      </div>

      <!-- Add task form -->
      <div class="card p-5 mb-8">
        <FormAlert :message="planner.error" class="mb-4" />
        <form class="space-y-3" @submit.prevent="addTask">
          <input
            v-model="form.title"
            type="text"
            class="input"
            placeholder="Yangi vazifa... (masalan: Ingliz tili 30 daqiqa)"
          />
          <div class="grid grid-cols-2 gap-3">
            <input v-model="form.due_date" type="date" class="input" :min="today" />
            <input v-model="form.due_time" type="time" class="input" />
          </div>
          <button type="submit" class="btn-primary w-full" :disabled="submitting">
            <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            {{ submitting ? "Qo'shilmoqda..." : "+ Vazifa qo'shish" }}
          </button>
        </form>
      </div>

      <!-- Loading -->
      <div v-if="planner.loading" class="text-center py-12 text-slate-400">
        <div class="w-7 h-7 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin mx-auto mb-3"></div>
        Yuklanmoqda...
      </div>

      <!-- Empty state -->
      <div v-else-if="!planner.tasks.length" class="text-center py-16 border-2 border-dashed border-slate-200 dark:border-slate-700/50 rounded-2xl">
        <div class="text-4xl mb-3 opacity-40">🗒️</div>
        <p class="font-semibold text-slate-600 dark:text-slate-400">Hali vazifalar yo'q</p>
        <p class="text-sm text-slate-400 mt-1">Birinchi vazifangizni qo'shing</p>
      </div>

      <!-- Task groups -->
      <div v-else class="space-y-6 stagger-children">
        <section v-for="group in groups" :key="group.label">
          <h2 class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">{{ group.label }}</h2>
          <div class="card divide-y divide-slate-100 dark:divide-slate-800/80 overflow-hidden">
            <div
              v-for="(task, idx) in group.items"
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
                <div v-if="task.due_date || task.due_time" class="flex items-center gap-1.5 mt-0.5">
                  <span v-if="task.due_date" class="text-[11px] font-medium text-slate-400">{{ formatDate(task.due_date) }}</span>
                  <span v-if="task.due_time" class="text-[11px] font-semibold text-brand-600 dark:text-brand-400">{{ formatTime(task.due_time) }}</span>
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
