<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useAuthStore } from '../../store/auth'
import { useToolText } from '../../utils/toolText'

const auth = useAuthStore()

const tx = useToolText({
  uz: {
    title: "Maqsadlar doskasi",
    desc: "Katta hayotiy va professional maqsadlarni belgilang hamda rivojlanishni kuzating",
    hint: "Maqsad qo'shing va har safar natijaga erishganingizda progress foizini oshirib boring. Barcha ma'lumotlar xotirada saqlanadi.",
    placeholder: "Maqsad nomi...",
    catPersonal: "Shaxsiy",
    catStudy: "O'qish",
    catCareer: "Kasb & Biznes",
    catFinance: "Moliya",
    catHealth: "Salomatlik",
    saveBtn: "Maqsadni saqlash",
    progressLabel: "Bajarilish darajasi",
    deadlineLabel: "Muddat:",
    noDeadline: "Muddat belgilanmagan",
    achieved: "🎉 Erishildi!",
    historyLabel: "Tarix:",
    created: "Yaratildi",
  },
  ru: {
    title: "Доска целей",
    desc: "Ставьте важные жизненные и карьерные цели и следите за прогрессом",
    hint: "Добавьте цель и отмечайте процент выполнения. Все данные сохраняются.",
    placeholder: "Название цели...",
    catPersonal: "Личное",
    catStudy: "Учёба",
    catCareer: "Карьера и бизнес",
    catFinance: "Финансы",
    catHealth: "Здоровье",
    saveBtn: "Сохранить цель",
    progressLabel: "Уровень выполнения",
    deadlineLabel: "Срок:",
    noDeadline: "Срок не указан",
    achieved: "🎉 Достигнуто!",
    historyLabel: "История:",
    created: "Создано",
  },
  en: {
    title: "Goal Board",
    desc: "Set major personal and professional goals and track your progress",
    hint: "Add goals and update completion percentage as you make progress. All data is saved.",
    placeholder: "Goal title...",
    catPersonal: "Personal",
    catStudy: "Study",
    catCareer: "Career & Business",
    catFinance: "Finance",
    catHealth: "Health",
    saveBtn: "Save goal",
    progressLabel: "Progress level",
    deadlineLabel: "Deadline:",
    noDeadline: "No deadline set",
    achieved: "🎉 Achieved!",
    historyLabel: "History:",
    created: "Created",
  },
})

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
const category = ref('personal')
const date = ref('')

function addGoal() {
  if (!title.value.trim()) return
  goals.value.push({
    id: Date.now(),
    title: title.value.trim(),
    category: category.value,
    progress: 0,
    date: date.value || tx.value.noDeadline,
    history: [{ date: new Date().toISOString().slice(0,10), action: tx.value.created }]
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

function getCategoryName(cat) {
  switch (cat) {
    case 'study': return tx.value.catStudy
    case 'career': return tx.value.catCareer
    case 'finance': return tx.value.catFinance
    case 'health': return tx.value.catHealth
    case 'personal':
    default:
      return tx.value.catPersonal
  }
}
</script>

<template>
  <ToolShell icon="🎯" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-6 animate-fadeUp">
      <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 space-y-3 card-hover-lift">
        <input v-model="title" type="text" :placeholder="tx.placeholder" class="input" />
        <div class="grid grid-cols-2 gap-3">
          <select v-model="category" class="input">
            <option value="personal">{{ tx.catPersonal }}</option>
            <option value="study">{{ tx.catStudy }}</option>
            <option value="career">{{ tx.catCareer }}</option>
            <option value="finance">{{ tx.catFinance }}</option>
            <option value="health">{{ tx.catHealth }}</option>
          </select>
          <input v-model="date" type="date" class="input" />
        </div>
        <button class="btn-primary w-full animate-popIn" @click="addGoal">{{ tx.saveBtn }}</button>
      </div>

      <div class="space-y-4">
        <div v-for="g in goals" :key="g.id" class="p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700 shadow-sm space-y-3 card-hover-lift animate-slideInBottom">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 dark:bg-brand-900/40 dark:text-brand-300">{{ getCategoryName(g.category) }}</span>
              <h3 class="font-bold text-base text-slate-800 dark:text-slate-100 mt-1.5">{{ g.title }}</h3>
            </div>
            <button class="text-slate-300 hover:text-red-500 transition-colors" @click="removeGoal(g.id)">✕</button>
          </div>

          <div>
            <div class="flex justify-between text-xs font-semibold text-slate-500 mb-1">
              <span>{{ tx.progressLabel }}</span>
              <span class="text-brand-600 dark:text-brand-400 font-bold">{{ g.progress }}%</span>
            </div>
            <input v-model.number="g.progress" @change="logProgress(g)" type="range" min="0" max="100" step="5" class="w-full accent-brand-600 cursor-pointer" />
          </div>

          <div class="flex justify-between text-xs text-slate-400 pt-1 border-t border-slate-100 dark:border-slate-700/50">
            <span>{{ tx.deadlineLabel }} {{ g.date }}</span>
            <span v-if="g.progress === 100" class="text-green-500 font-bold animate-bounceSoft">{{ tx.achieved }}</span>
          </div>
          
          <div v-if="g.history && g.history.length > 0" class="mt-2 text-[10px] text-slate-400">
            <p class="font-semibold mb-1">{{ tx.historyLabel }}</p>
            <ul class="space-y-0.5 pl-2">
              <li v-for="(h, idx) in g.history.slice(0,3)" :key="idx">- {{ h.date }}: {{ h.action }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
