<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useAuthStore } from '../../store/auth'
import { useI18n } from '../../i18n'

const auth = useAuthStore()
const { t } = useI18n()

const storageKey = computed(() => {
  return auth.user?.id ? `qulay_goals_${auth.user.id}` : 'qulay_goals_guest'
})

const goals = ref([])

function loadGoals() {
  const saved = localStorage.getItem(storageKey.value)
  if (saved) {
    try {
      goals.value = JSON.parse(saved)
      return
    } catch (e) {
      goals.value = []
    }
  } else {
    goals.value = []
  }
}

onMounted(() => {
  loadGoals()
})

watch(() => auth.user?.id, () => {
  loadGoals()
})

watch(goals, (newVal) => {
  localStorage.setItem(storageKey.value, JSON.stringify(newVal))
}, { deep: true })

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
    date: date.value || t('Muddat belgilanmagan'),
    history: [{ date: new Date().toISOString().slice(0,10), action: t('Yaratildi') || 'Yaratildi' }]
  })
  title.value = ''
  date.value = ''
}

function removeGoal(id) {
  goals.value = goals.value.filter(g => g.id !== id)
}

function logProgress(g) {
  if (!g.history) g.history = []
  g.history.unshift({ date: new Date().toISOString().slice(0,10), action: `Progress: ${g.progress}%` })
}
</script>

<template>
  <ToolShell icon="🎯" :title="t('Maqsadlar doskasi')" :description="t('Katta hayotiy va professional maqsadlarni belgilang hamda rivojlanishni kuzating')" :hint="t('Maqsad qo\'shing va har safar natijaga erishganingizda progress foizini oshirib boring. Barcha ma\'lumotlar xotirada saqlanadi.')">
    <template #header><AppHeader /></template>

    <div class="space-y-6 animate-fadeUp">
      <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 space-y-3 card-hover-lift">
        <input v-model="title" type="text" :placeholder="t('Maqsad nomi...')" class="input" />
        <div class="grid grid-cols-2 gap-3">
          <select v-model="category" class="input">
            <option value="Shaxsiy">{{ t('Shaxsiy') }}</option>
            <option value="O'qish">{{ t('O\'qish') }}</option>
            <option value="Kasb">{{ t('Kasb & Biznes') }}</option>
            <option value="Moliya">{{ t('Moliya') }}</option>
            <option value="Salomatlik">{{ t('Salomatlik') }}</option>
          </select>
          <input v-model="date" type="date" class="input" />
        </div>
        <button class="btn-primary w-full animate-popIn" @click="addGoal">{{ t('Maqsadni saqlash') }}</button>
      </div>

      <div class="space-y-4">
        <div v-for="g in goals" :key="g.id" class="p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700 shadow-sm space-y-3 card-hover-lift animate-slideInBottom">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 dark:bg-brand-900/40 dark:text-brand-300">{{ t(g.category) || g.category }}</span>
              <h3 class="font-bold text-base text-slate-800 dark:text-slate-100 mt-1.5">{{ g.title }}</h3>
            </div>
            <button class="text-slate-300 hover:text-red-500 transition-colors" @click="removeGoal(g.id)">❌</button>
          </div>

          <div>
            <div class="flex justify-between text-xs font-semibold text-slate-500 mb-1">
              <span>{{ t('Bajarilish darajasi') }}</span>
              <span class="text-brand-600 dark:text-brand-400 font-bold">{{ g.progress }}%</span>
            </div>
            <input v-model.number="g.progress" @change="logProgress(g)" type="range" min="0" max="100" step="5" class="w-full accent-brand-600 cursor-pointer" />
          </div>

          <div class="flex justify-between text-xs text-slate-400 pt-1 border-t border-slate-100 dark:border-slate-700/50">
            <span>{{ t('Muddat:') }} {{ g.date }}</span>
            <span v-if="g.progress === 100" class="text-green-500 font-bold animate-bounceSoft">{{ t('🎉 Erishildi!') }}</span>
          </div>
          
          <div v-if="g.history && g.history.length > 0" class="mt-2 text-[10px] text-slate-400">
            <p class="font-semibold mb-1">{{ t('Tarix:') }}</p>
            <ul class="space-y-0.5 pl-2">
              <li v-for="(h, idx) in g.history.slice(0,3)" :key="idx">- {{ h.date }}: {{ h.action }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
