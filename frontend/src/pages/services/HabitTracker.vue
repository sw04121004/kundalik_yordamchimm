<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useAuthStore } from '../../store/auth'
import { useToolText } from '../../utils/toolText'

const auth = useAuthStore()

const tx = useToolText({
  uz: {
    title: "Odatlar taqvimi",
    desc: "Kunlik foydali odatlarni shakllantiring va haftalik natijalarni kuzating",
    hint: "Yangi odat qo'shing va haftaning har bir kunida bajarganingizni belgilab boring. Ma'lumotlar xotirada saqlanadi.",
    placeholder: "Yangi odat qo'shish (masalan: 10 ta inglizcha so'z)",
    addBtn: "Qo'shish",
    weekDays: ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya'],
    created: "Yaratildi",
    completed: "Bajarildi",
    cancelled: "Bekor qilindi",
    recentActions: "So'nggi harakatlar:",
  },
  ru: {
    title: "Трекер привычек",
    desc: "Формируйте полезные привычки и отслеживайте результаты за неделю",
    hint: "Добавьте привычку и отмечайте её выполнение каждый день недели. Данные сохраняются.",
    placeholder: "Добавить привычку (например: 10 английских слов)",
    addBtn: "Добавить",
    weekDays: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
    created: "Создано",
    completed: "Выполнено",
    cancelled: "Отменено",
    recentActions: "Последние действия:",
  },
  en: {
    title: "Habit Tracker",
    desc: "Build productive daily habits and track weekly consistency",
    hint: "Add a habit and check off each day you complete it. Data is saved automatically.",
    placeholder: "Add new habit (e.g.: learn 10 English words)",
    addBtn: "Add",
    weekDays: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
    created: "Created",
    completed: "Done",
    cancelled: "Cancelled",
    recentActions: "Recent activity:",
  },
})

const storageKey = computed(() => {
  return auth.user?.id ? `qulay_habits_${auth.user.id}` : 'qulay_habits_guest'
})

const habits = ref([])

function loadHabits() {
  const saved = localStorage.getItem(storageKey.value)
  if (saved) {
    try {
      habits.value = JSON.parse(saved)
      return
    } catch (e) {
      habits.value = []
    }
  } else {
    habits.value = []
  }
}

onMounted(() => {
  loadHabits()
})

watch(() => auth.user?.id, () => {
  loadHabits()
})

watch(habits, (newVal) => {
  localStorage.setItem(storageKey.value, JSON.stringify(newVal))
}, { deep: true })

const newHabitName = ref('')

function addHabit() {
  if (!newHabitName.value.trim()) return
  habits.value.push({
    id: Date.now(),
    name: newHabitName.value.trim(),
    icon: '✨',
    days: [false, false, false, false, false, false, false],
    history: [{ date: new Date().toISOString().slice(0,10), action: tx.value.created }]
  })
  newHabitName.value = ''
}

function toggleDay(habit, idx) {
  habit.days[idx] = !habit.days[idx]
  if (!habit.history) habit.history = []
  const status = habit.days[idx] ? tx.value.completed : tx.value.cancelled
  habit.history.unshift({ date: new Date().toISOString().slice(0,10), action: `${tx.value.weekDays[idx]}: ${status}` })
}

function removeHabit(id) {
  habits.value = habits.value.filter(h => h.id !== id)
}
</script>

<template>
  <ToolShell icon="📅" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-6 animate-fadeUp">
      <div class="flex gap-2">
        <input v-model="newHabitName" type="text" :placeholder="tx.placeholder" class="input flex-1" @keydown.enter="addHabit" />
        <button class="btn-primary animate-popIn" @click="addHabit">{{ tx.addBtn }}</button>
      </div>

      <div class="space-y-3">
        <div class="flex items-center justify-end gap-2 px-3 text-xs font-bold text-slate-400 uppercase">
          <span v-for="d in tx.weekDays" :key="d" class="w-8 text-center">{{ d }}</span>
          <span class="w-6"></span>
        </div>

        <div v-for="h in habits" :key="h.id" class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 card-hover-lift animate-slideInBottom">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-2.5 flex-1 min-w-0">
              <span class="text-xl">{{ h.icon }}</span>
              <span class="font-semibold text-sm text-slate-800 dark:text-slate-200 truncate">{{ h.name }}</span>
            </div>

            <div class="flex items-center gap-2">
              <button
                v-for="(done, idx) in h.days"
                :key="idx"
                class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs transition-all cursor-pointer"
                :class="done ? 'bg-green-500 text-white shadow-sm scale-105' : 'bg-slate-200 dark:bg-slate-700 text-transparent hover:bg-slate-300 dark:hover:bg-slate-600'"
                @click="toggleDay(h, idx)"
              >
                ✓
              </button>
              <button class="w-6 text-slate-300 hover:text-red-500 text-sm ml-1 transition-colors" @click="removeHabit(h.id)">✕</button>
            </div>
          </div>
          
          <div v-if="h.history && h.history.length > 0" class="mt-3 pt-2 border-t border-slate-200 dark:border-slate-700 text-[10px] text-slate-400">
            <span class="font-semibold">{{ tx.recentActions }}</span>
            <span v-for="(hist, idx) in h.history.slice(0,3)" :key="idx" class="ml-2 bg-white dark:bg-slate-800 px-1.5 py-0.5 rounded">
              {{ hist.action }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
