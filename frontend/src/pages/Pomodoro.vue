<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import { useAuthStore } from '../store/auth'
import { useToolText } from '../utils/toolText'

const auth = useAuthStore()

const tx = useToolText({
  uz: {
    title: "Pomodoro Taymer",
    desc: "Diqqatni bir joyga jamlab samarali ishlash usuli",
    hint: "25 daqiqa to'liq diqqat bilan ishlang, so'ng 5 daqiqa dam oling",
    work: "👨‍💻 Ish (25m)",
    shortBreak: "☕ Qisqa tanaffus (5m)",
    longBreak: "🌴 Uzun tanaffus (15m)",
    focus: "Fokuslaning",
    ready: "Tayyor",
    placeholder: "Qaysi vazifa ustida ishlayapsiz? (Masalan: Matematika 3-mashq)",
    start: "▶️ Boshlash",
    pause: "⏸️ Pauza",
    reset: "🔄 Qayta o'rnatish",
    completed: "🎯 Bajarilgan Pomodorolar:",
  },
  ru: {
    title: "Помодоро Таймер",
    desc: "Метод концентрации внимания для эффективной работы",
    hint: "25 минут сфокусированной работы, затем 5 минут отдыха",
    work: "👨‍💻 Работа (25м)",
    shortBreak: "☕ Короткий перерыв (5м)",
    longBreak: "🌴 Длинный перерыв (15м)",
    focus: "Фокусируйтесь",
    ready: "Готов",
    placeholder: "Над какой задачей вы работаете? (Например: Задача 3)",
    start: "▶️ Старт",
    pause: "⏸️ Пауза",
    reset: "🔄 Сбросить",
    completed: "🎯 Завершено Помодоро:",
  },
  en: {
    title: "Pomodoro Timer",
    desc: "Focus technique for effective and distraction-free work",
    hint: "Work with full focus for 25 minutes, then take a 5-minute break",
    work: "👨‍💻 Work (25m)",
    shortBreak: "☕ Short break (5m)",
    longBreak: "🌴 Long break (15m)",
    focus: "Stay focused",
    ready: "Ready",
    placeholder: "What are you working on? (e.g.: Chapter 3 review)",
    start: "▶️ Start",
    pause: "⏸️ Pause",
    reset: "🔄 Reset",
    completed: "🎯 Completed Pomodoros:",
  },
})

const modes = computed(() => [
  { id: 'work', label: tx.value.work, minutes: 25 },
  { id: 'short', label: tx.value.shortBreak, minutes: 5 },
  { id: 'long', label: tx.value.longBreak, minutes: 15 },
])

const storageKey = computed(() => {
  return auth.user?.id ? `pomodoroState_${auth.user.id}` : 'pomodoroState_guest'
})

const activeMode = ref('work')
const timeLeft = ref(25 * 60)
const isRunning = ref(false)
const taskTitle = ref('')
const completedCount = ref(0)
let timerInterval = null

const totalDuration = computed(() => {
  const modeObj = modes.value.find(m => m.id === activeMode.value)
  return (modeObj ? modeObj.minutes : 25) * 60
})

const minutesFormatted = computed(() => {
  const m = Math.floor(timeLeft.value / 60)
  return m < 10 ? `0${m}` : `${m}`
})

const secondsFormatted = computed(() => {
  const s = timeLeft.value % 60
  return s < 10 ? `0${s}` : `${s}`
})

const progressPercent = computed(() => {
  return ((totalDuration.value - timeLeft.value) / totalDuration.value) * 100
})

function saveState() {
  const state = {
    activeMode: activeMode.value,
    timeLeft: timeLeft.value,
    isRunning: isRunning.value,
    taskTitle: taskTitle.value,
    completedCount: completedCount.value
  }
  localStorage.setItem(storageKey.value, JSON.stringify(state))
}

function loadState() {
  const savedState = localStorage.getItem(storageKey.value)
  if (savedState) {
    try {
      const state = JSON.parse(savedState)
      activeMode.value = state.activeMode || 'work'
      timeLeft.value = typeof state.timeLeft === 'number' ? state.timeLeft : 25 * 60
      isRunning.value = false
      taskTitle.value = state.taskTitle || ''
      completedCount.value = state.completedCount || 0
    } catch (e) {
      resetDefaults()
    }
  } else {
    resetDefaults()
  }
}

function resetDefaults() {
  activeMode.value = 'work'
  timeLeft.value = 25 * 60
  isRunning.value = false
  taskTitle.value = ''
  completedCount.value = 0
}

function setMode(modeId) {
  stopTimer()
  activeMode.value = modeId
  const modeObj = modes.value.find(m => m.id === modeId)
  timeLeft.value = (modeObj ? modeObj.minutes : 25) * 60
}

function startTimer() {
  if (isRunning.value) return
  isRunning.value = true
  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      stopTimer()
      playBeep()
      if (activeMode.value === 'work') {
        completedCount.value++
      }
    }
  }, 1000)
}

function stopTimer() {
  isRunning.value = false
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

function resetTimer() {
  setMode(activeMode.value)
}

function playBeep() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = 'sine'
    osc.frequency.setValueAtTime(587.33, ctx.currentTime)
    gain.gain.setValueAtTime(0.3, ctx.currentTime)
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.start()
    osc.stop(ctx.currentTime + 1.2)
  } catch (e) {
    // Audio Context blocked or unavailable
  }
}

onMounted(() => {
  loadState()
  watch([activeMode, timeLeft, isRunning, taskTitle, completedCount], saveState, { deep: true })
})

watch(() => auth.user?.id, () => {
  loadState()
})

onUnmounted(() => {
  stopTimer()
  saveState()
})
</script>

<template>
  <ToolShell
    icon="🍅"
    :title="tx.title"
    :description="tx.desc"
    :hint="tx.hint"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6 text-center animate-fadeUp">
      <!-- Mode selection buttons -->
      <div class="inline-flex p-1.5 rounded-2xl bg-slate-100 dark:bg-slate-800 gap-1 card-hover-lift">
        <button
          v-for="m in modes"
          :key="m.id"
          class="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition cursor-pointer"
          :class="activeMode === m.id ? 'bg-brand-500 text-white shadow-sm scale-105' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
          @click="setMode(m.id)"
        >
          {{ m.label }}
        </button>
      </div>

      <!-- Circular Timer Display -->
      <div class="relative w-56 h-56 mx-auto flex items-center justify-center my-4 animate-scaleIn">
        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50" cy="50" r="42"
            stroke="currentColor" stroke-width="6"
            class="text-slate-100 dark:text-slate-800"
            fill="transparent"
          />
          <circle
            cx="50" cy="50" r="42"
            stroke="currentColor" stroke-width="6"
            class="text-brand-500 transition-all duration-1000 ease-linear"
            fill="transparent"
            stroke-linecap="round"
            :stroke-dasharray="264"
            :stroke-dashoffset="264 - (264 * progressPercent) / 100"
          />
        </svg>

        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-4xl sm:text-5xl font-extrabold font-mono text-slate-800 dark:text-slate-100 tracking-tighter">
            {{ minutesFormatted }}:{{ secondsFormatted }}
          </span>
          <span class="text-xs text-slate-400 mt-1 uppercase font-semibold tracking-wider">
            {{ isRunning ? tx.focus : tx.ready }}
          </span>
        </div>
      </div>

      <!-- Task Input -->
      <div class="max-w-md mx-auto">
        <input
          v-model="taskTitle"
          type="text"
          class="input text-center text-sm"
          :placeholder="tx.placeholder"
        />
      </div>

      <!-- Controls -->
      <div class="flex justify-center gap-3">
        <button
          v-if="!isRunning"
          class="btn-primary !px-8 !py-3 text-base shadow-soft animate-popIn"
          @click="startTimer"
        >
          {{ tx.start }}
        </button>
        <button
          v-else
          class="px-8 py-3 rounded-xl bg-amber-500 text-white font-semibold shadow-soft hover:bg-amber-600 transition"
          @click="stopTimer"
        >
          {{ tx.pause }}
        </button>
        <button
          class="btn-secondary !px-4 !py-3 text-sm"
          @click="resetTimer"
        >
          {{ tx.reset }}
        </button>
      </div>

      <!-- Session Stats -->
      <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-center gap-6 text-sm">
        <div class="flex items-center gap-2">
          <span>{{ tx.completed }}</span>
          <span class="font-bold text-brand-600 dark:text-brand-400 text-lg">{{ completedCount }}</span>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
