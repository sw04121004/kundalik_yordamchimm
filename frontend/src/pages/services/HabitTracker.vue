<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const habits = ref([
  { id: 1, name: 'Kitob o\'qish (20 daqiqa)', icon: '📖', days: [true, true, true, false, true, false, false] },
  { id: 2, name: 'Ertalabki badantarbiya', icon: '🏃', days: [true, false, true, true, true, false, false] },
  { id: 3, name: '2 litr suv ichish', icon: '💧', days: [true, true, true, true, false, false, false] },
])

const newHabitName = ref('')
const weekDays = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya']

function addHabit() {
  if (!newHabitName.value.trim()) return
  habits.value.push({
    id: Date.now(),
    name: newHabitName.value.trim(),
    icon: '✨',
    days: [false, false, false, false, false, false, false]
  })
  newHabitName.value = ''
}

function toggleDay(habit, idx) {
  habit.days[idx] = !habit.days[idx]
}

function removeHabit(id) {
  habits.value = habits.value.filter(h => h.id !== id)
}
</script>

<template>
  <ToolShell icon="✅" title="Odatlar taqvimi" description="Kunlik foydali odatlarni shakllantiring va haftalik natijalarni kuzating" hint="Yangi odat qo'shing va haftaning har bir kunida bajarganingizni belgilab boring.">
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

        <div v-for="h in habits" :key="h.id" class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3">
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
            <button class="w-6 text-slate-300 hover:text-red-500 text-sm ml-1" @click="removeHabit(h.id)">✕</button>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
