<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const goals = ref([
  { id: 1, title: 'IELTS dan 7.5 olish', category: 'O\'qish', progress: 65, date: '2026-12-01' },
  { id: 2, title: 'Yangi mashina uchun jamg\'arma', category: 'Moliya', progress: 40, date: '2027-05-01' },
  { id: 3, title: 'Vue & Django dasturlashni to\'liq o\'rganish', category: 'Kasb', progress: 90, date: '2026-10-15' },
])

const title = ref('')
const category = ref('Shaxsiy')
const date = ref('')

function addGoal() {
  if (!title.value.trim()) return
  goals.value.push({
    id: Date.now(),
    title: title.value.trim(),
    category: category.value,
    progress: 0,
    date: date.value || 'Muddat belgilanmagan'
  })
  title.value = ''
  date.value = ''
}

function removeGoal(id) {
  goals.value = goals.value.filter(g => g.id !== id)
}
</script>

<template>
  <ToolShell icon="🎯" title="Maqsadlar doskasi" description="Katta hayotiy va professional maqsadlarni belgilang hamda rivojlanishni kuzating" hint="Maqsad qo'shing va har safar natijaga erishganingizda progress foizini oshirib boring.">
    <template #header><AppHeader /></template>

    <div class="space-y-6">
      <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 space-y-3">
        <input v-model="title" type="text" placeholder="Maqsad nomi..." class="input" />
        <div class="grid grid-cols-2 gap-3">
          <select v-model="category" class="input">
            <option value="Shaxsiy">Shaxsiy</option>
            <option value="O'qish">O'qish</option>
            <option value="Kasb">Kasb & Biznes</option>
            <option value="Moliya">Moliya</option>
            <option value="Salomatlik">Salomatlik</option>
          </select>
          <input v-model="date" type="date" class="input" />
        </div>
        <button class="btn-primary w-full" @click="addGoal">Maqsadni saqlash</button>
      </div>

      <div class="space-y-4">
        <div v-for="g in goals" :key="g.id" class="p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700 shadow-sm space-y-3">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 dark:bg-brand-900/40 dark:text-brand-300">{{ g.category }}</span>
              <h3 class="font-bold text-base text-slate-800 dark:text-slate-100 mt-1.5">{{ g.title }}</h3>
            </div>
            <button class="text-slate-300 hover:text-red-500" @click="removeGoal(g.id)">✕</button>
          </div>

          <div>
            <div class="flex justify-between text-xs font-semibold text-slate-500 mb-1">
              <span>Bajarilish darajasi</span>
              <span class="text-brand-600 dark:text-brand-400 font-bold">{{ g.progress }}%</span>
            </div>
            <input v-model.number="g.progress" type="range" min="0" max="100" class="w-full accent-brand-600" />
          </div>

          <div class="flex justify-between text-xs text-slate-400 pt-1 border-t border-slate-100 dark:border-slate-700/50">
            <span>Muddat: {{ g.date }}</span>
            <span v-if="g.progress === 100" class="text-green-500 font-bold">🎉 Erishildi!</span>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
