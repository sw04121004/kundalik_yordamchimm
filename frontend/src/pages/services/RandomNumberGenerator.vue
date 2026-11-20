<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import ResultBox from '../../components/ResultBox.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { useToolText } from '../../utils/toolText'
import { useI18n } from '../../i18n'

const { t } = useI18n()
const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('random-son-generatori'))

const tx = useToolText({
  uz: {
    title: "Random son generatori",
    desc: "Berilgan oraliqda tasodifiy son yarating",
    hint: "Minimal va maksimal qiymatlarni, nechta son kerakligini kiriting va «Yaratish»ni bosing.",
    min: "Minimal",
    max: "Maksimal",
    count: "Nechta son",
    allowDuplicates: "Takrorlanishga ruxsat",
    generate: "Yaratish",
    result: "Natija",
    errInteger: "Iltimos, faqat butun son kiriting.",
    errMinMax: "Minimal qiymat maksimaldan kichik bo‘lishi kerak.",
    errRange: "Takrorlanmas sonlar uchun diapazon yetarli emas.",
  },
  ru: {
    title: "Генератор случайных чисел",
    desc: "Генерация случайных чисел в заданном диапазоне",
    hint: "Введите минимальное и максимальное значения, количество чисел и нажмите «Сгенерировать».",
    min: "Минимум",
    max: "Максимум",
    count: "Количество чисел",
    allowDuplicates: "Разрешить повторы",
    generate: "Сгенерировать",
    result: "Результат",
    errInteger: "Пожалуйста, вводите только целые числа.",
    errMinMax: "Минимальное значение должно быть меньше максимального.",
    errRange: "В этом диапазоне недостаточно уникальных чисел.",
  },
  en: {
    title: "Random Number Generator",
    desc: "Generate random numbers in a specified range",
    hint: "Enter minimum and maximum values, quantity, and click «Generate».",
    min: "Minimum",
    max: "Maximum",
    count: "Number count",
    allowDuplicates: "Allow duplicates",
    generate: "Generate",
    result: "Result",
    errInteger: "Please enter integers only.",
    errMinMax: "Minimum value must be less than maximum.",
    errRange: "Not enough unique numbers in this range.",
  },
})

const min = ref(1)
const max = ref(100)
const allowDuplicates = ref(true)
const count = ref(1)
const error = ref('')
const results = ref([])

function generate() {
  error.value = ''
  results.value = []

  const lo = parseInt(min.value, 10)
  const hi = parseInt(max.value, 10)
  const n = Math.min(Math.max(parseInt(count.value, 10) || 1, 1), 50)

  if (Number.isNaN(lo) || Number.isNaN(hi)) {
    error.value = tx.value.errInteger
    return
  }
  if (lo >= hi) {
    error.value = tx.value.errMinMax
    return
  }

  const range = hi - lo + 1
  if (!allowDuplicates.value && n > range) {
    error.value = tx.value.errRange
    return
  }

  const generated = new Set()
  const output = []
  let guard = 0
  while (output.length < n && guard < 10000) {
    guard += 1
    const value = lo + Math.floor(Math.random() * range)
    if (!allowDuplicates.value) {
      if (generated.has(value)) continue
      generated.add(value)
    }
    output.push(value)
  }
  results.value = output
}

function reset() {
  min.value = 1
  max.value = 100
  count.value = 1
  allowDuplicates.value = true
  results.value = []
  error.value = ''
}
</script>

<template>
  <ToolShell icon="🎲" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">{{ tx.min }}</label>
          <input v-model="min" type="number" class="input" />
        </div>
        <div>
          <label class="label">{{ tx.max }}</label>
          <input v-model="max" type="number" class="input" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4 items-end">
        <div>
          <label class="label">{{ tx.count }}</label>
          <input v-model="count" type="number" min="1" max="50" class="input" />
        </div>
        <label class="flex items-center gap-2 text-sm text-slate-600 mb-2.5">
          <input type="checkbox" v-model="allowDuplicates" class="rounded text-brand-600 focus:ring-brand-400" />
          {{ tx.allowDuplicates }}
        </label>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="generate">{{ tx.generate }}</button>
        <button class="btn-secondary" @click="reset">{{ t('common.clear') }}</button>
      </div>

      <transition name="page-fade">
        <div v-if="results.length" class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop">
          <p class="text-xs font-medium text-brand-600 uppercase tracking-wide mb-2">{{ tx.result }}</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="(n, i) in results"
              :key="i"
              class="px-3 py-1.5 rounded-lg bg-white border border-brand-200 text-brand-800 font-bold"
            >
              {{ n }}
            </span>
          </div>
        </div>
      </transition>
    </div>
  </ToolShell>

</template>
