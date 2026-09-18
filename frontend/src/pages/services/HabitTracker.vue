<script setup>
import { ref, watch } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const getSavedHabits = () => {
  const saved = localStorage.getItem('qulay_habits')
  if (saved) return JSON.parse(saved)
  return [
    { id: 1, name: 'Kitob o\'qish (20 daqiqa)', icon: '📖', days: [true, true, true, false, true, false, false], history: [] },
    { id: 2, name: 'Ertalabki badantarbiya', icon: '🏃', days: [true, false, true, true, true, false, false], history: [] },
    { id: 3, name: '2 litr suv ichish', icon: '💧', days: [true, true, true, true, false, false, false], history: [] },
  ]
}

const habits = ref(getSavedHabits())

watch(habits, (newVal) => {
  localStorage.setItem('qulay_habits', JSON.stringify(newVal))
}, { deep: true })

const newHabitName = ref('')
const weekDays = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya']

function addHabit() {
  if (!newHabitName.value.trim()) return
  habits.value.push({
    id: Date.now(),
    name: newHabitName.value.trim(),
    icon: '✨',
    days: [false, false, false, false, false, false, false],
    history: [{ date: new Date().toISOString().slice(0,10), action: 'Yaratildi' }]
  })
  newHabitName.value = ''
}

function toggleDay(habit, idx) {
  habit.days[idx] = !habit.days[idx]
  if (!habit.history) habit.history = []
  const status = habit.days[idx] ? 'Bajarildi' : 'Bekor qilindi'
  habit.history.unshift({ date: new Date().toISOString().slice(0,10), action: `${weekDays[idx]} kuni ${status}` })
}

function removeHabit(id) {
  habits.value = habits.value.filter(h => h.id !== id)
}
</script>

<template>
  <ToolShell icon="🗓" title="Odatlar taqvimi" description="Kunlik foydali odatlarni shakllantiring va haftalik natijalarni kuzating" hint="Yangi odat qo'shing va haftaning har bir kunida bajarganingizni belgilab boring. Ma'lumotlar xotirada saqlanadi.">
    <template #header><AppHeader /></template>

    <div class="space-y-6">
      <div class="flex gap-2">
        <input v-model="newHabitName" type="text" placeholder="Yangi odat qo'shish (masalan: 10 ta inglizcha so'z)" class="input flex-1" @keydown.enter="addHabit" />
        <button class="btn-primary" @click="addHabit">Qo'shish</button>
      </div>

      <div class="space-y-3">
        <div class="flex items-center justify-end gap-2 px-3 text-xs font-bold text-slate-400 uppercase">
          <span v-for="d in weekDays" :key="d" class="w-8 text-center">{{ d }}</span>
          <span class="w-6"></span>
        </div>

        <div v-for="h in habits" :key="h.id" class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-2.5 flex-1 min-w-0">
              <span class="text-xl">{{ h.icon }}</span>
              <span class="font-semibold text-sm text-slate-800 dark:text-slate-200 truncate">{{ h.name }}</span>
            </div>

            <div class="flex items-center gap-2">
              <button
                v-for="(done, idx) in h.days"
                :key="idx"
                class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs transition-all"
                :class="done ? 'bg-green-500 text-white shadow-sm scale-105' : 'bg-slate-200 dark:bg-slate-700 text-transparent hover:bg-slate-300 dark:hover:bg-slate-600'"
                @click="toggleDay(h, idx)"
              >
                ✓
              </button>
              <button class="w-6 text-slate-300 hover:text-red-500 text-sm ml-1" @click="removeHabit(h.id)">❌</button>
            </div>
          </div>
          
          <div v-if="h.history && h.history.length > 0" class="mt-3 pt-2 border-t border-slate-200 dark:border-slate-700 text-[10px] text-slate-400">
            <span class="font-semibold">So'nggi harakatlar:</span>
            <span v-for="(hist, idx) in h.history.slice(0,3)" :key="idx" class="ml-2 bg-white dark:bg-slate-800 px-1.5 py-0.5 rounded">
              {{ hist.action }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
