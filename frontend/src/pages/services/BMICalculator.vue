<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('bmi-hisoblagich'))

const weight = ref('')
const height = ref('')
const error = ref('')
const result = ref(null)

function categoryFor(bmi) {
  if (bmi < 18.5) return { label: 'Kam vaznli', color: 'text-sky-600', bg: 'bg-sky-50' }
  if (bmi < 25) return { label: 'Me’yorida', color: 'text-emerald-600', bg: 'bg-emerald-50' }
  if (bmi < 30) return { label: 'Ortiqcha vazn', color: 'text-amber-600', bg: 'bg-amber-50' }
  return { label: 'Semizlik', color: 'text-red-600', bg: 'bg-red-50' }
}

function calculate() {
  error.value = ''
  result.value = null

  const w = parseFloat(weight.value)
  const hCm = parseFloat(height.value)

  if (weight.value === '' || height.value === '') {
    error.value = 'Iltimos, vazn va bo‘yingizni kiriting.'
    return
  }
  if (Number.isNaN(w) || Number.isNaN(hCm) || w <= 0 || hCm <= 0) {
    error.value = 'Iltimos, to‘g‘ri musbat qiymatlar kiriting.'
    return
  }

  const hMeters = hCm / 100
  const bmi = w / (hMeters * hMeters)
  const rounded = Math.round(bmi * 10) / 10

  result.value = { bmi: rounded, ...categoryFor(rounded) }
}

function reset() {
  weight.value = ''
  height.value = ''
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell
    icon="⚕️"
    title="Tana massa indeksi (BMI)"
    description="Bo‘y va vaznga qarab BMI’ni aniqlang"
    hint="Vazningizni (kg) va bo‘yingizni (sm) kiriting, «Hisoblash»ni bosing — BMI va uning tavsifi chiqadi."
  >
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Vazn (kg)</label>
          <input v-model="weight" type="number" class="input" placeholder="masalan: 68" @keyup.enter="calculate" />
        </div>
        <div>
          <label class="label">Bo‘y (sm)</label>
          <input v-model="height" type="number" class="input" placeholder="masalan: 172" @keyup.enter="calculate" />
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <transition name="page-fade">
        <div
          v-if="result"
          class="mt-5 rounded-xl border px-5 py-4 text-center animate-resultPop"
          :class="[result.bg, 'border-transparent dark:bg-slate-700/60']"
        >
          <p class="text-xs font-medium uppercase tracking-wide" :class="result.color">BMI natijangiz</p>
          <p class="text-3xl font-extrabold mt-1" :class="result.color">{{ result.bmi }}</p>
          <p class="text-sm font-semibold mt-1" :class="result.color">{{ result.label }}</p>
        </div>
      </transition>

      <p class="text-xs text-slate-400 dark:text-slate-500 text-center pt-1">
        Bu natija umumiy ma’lumot uchun, tibbiy tashxis emas.
      </p>
    </div>
  </ToolShell>
</template>
