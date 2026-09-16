<script setup>
import { ref, onUnmounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const isRunning = ref(false)
const seconds = ref(0)
const taskName = ref('')
const history = ref([])
let timer = null

function toggleTimer() {
  if (isRunning.value) {
    clearInterval(timer)
    isRunning.value = false
    if (seconds.value > 0) {
      history.value.unshift({
        title: taskName.value.trim() || 'Nomsiz vazifa',
        time: formatTime(seconds.value),
        date: new Date().toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' })
      })
    }
  } else {
    isRunning.value = true
    timer = setInterval(() => {
      seconds.value++
    }, 1000)
  }
}

function resetTimer() {
  clearInterval(timer)
  isRunning.value = false
  seconds.value = 0
}

function formatTime(totalSec) {
  const h = String(Math.floor(totalSec / 3600)).padStart(2, '0')
  const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0')
  const s = String(totalSec % 60).padStart(2, '0')
  return `${h}:${m}:${s}`
}

onUnmounted(() => clearInterval(timer))
</script>

<template>
  <ToolShell icon="⏱️" title="Vaqt trekeri" description="Kunlik vazifalarga ketgan vaqtni o'lchash va nazorat qilish" hint="Vazifa nomini yozing va taymerni ishga tushiring.">
    <template #header><AppHeader /></template>

    <div class="space-y-6 text-center">
      <div class="text-5xl sm:text-6xl font-black font-mono tracking-wider text-slate-800 dark:text-slate-100 py-4">
        {{ formatTime(seconds) }}
      </div>

      <div class="max-w-md mx-auto">
        <input v-model="taskName" type="text" placeholder="Qaysi vazifa ustida ishlayapsiz?" class="input text-center" :disabled="isRunning" />
      </div>

      <div class="flex justify-center gap-3">
        <button
          class="btn-primary !px-8 !py-3 text-base"
          :class="isRunning ? '!from-amber-500 !to-amber-600' : ''"
          @click="toggleTimer"
        >
          {{ isRunning ? '⏸ To\'xtatish' : '▶ Boshlash' }}
        </button>
        <button class="btn-secondary !px-5" @click="resetTimer">
          Tozalash
        </button>
      </div>

      <div v-if="history.length" class="text-left pt-6 border-t border-slate-100 dark:border-slate-800">
        <h3 class="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">Bugungi qaydlar</h3>
        <div class="space-y-2">
          <div v-for="(h, idx) in history" :key="idx" class="flex justify-between items-center p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800">
            <span class="text-sm font-semibold text-slate-700 dark:text-slate-200">{{ h.title }}</span>
            <div class="flex items-center gap-3">
              <span class="text-xs text-slate-400">{{ h.date }}</span>
              <span class="text-sm font-mono font-bold text-brand-600 dark:text-brand-400">{{ h.time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
