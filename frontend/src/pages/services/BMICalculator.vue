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
const age = ref('')
const error = ref('')
const result = ref(null)

function adultCategory(bmi) {
  if (bmi < 18.5) return { label: 'Kam vaznli', color: 'text-sky-600', bg: 'bg-sky-50' }
  if (bmi < 25) return { label: 'Me’yorda', color: 'text-emerald-600', bg: 'bg-emerald-50' }
  if (bmi < 30) return { label: 'Ortiqcha vazn', color: 'text-amber-600', bg: 'bg-amber-50' }
  return { label: 'Semizlik', color: 'text-red-600', bg: 'bg-red-50' }
}

function calculate() {
  error.value = ''
  result.value = null

  const w = Number(weight.value)
  const hCm = Number(height.value)
  const years = Number(age.value)
  if (weight.value === '' || height.value === '' || age.value === '') {
    error.value = 'Iltimos, yosh, vazn va bo‘yingizni kiriting.'
    return
  }
  if (![w, hCm, years].every(Number.isFinite) || w <= 0 || hCm <= 0 || years < 0 || years > 120) {
    error.value = 'Yosh, vazn va bo‘y uchun to‘g‘ri qiymat kiriting.'
    return
  }

  const bmi = w / ((hCm / 100) ** 2)
  const rounded = Math.round(bmi * 10) / 10
  result.value = years >= 20
    ? { bmi: rounded, ...adultCategory(rounded), adult: true }
    : { bmi: rounded, adult: false }
}

function reset() {
  weight.value = ''
  height.value = ''
  age.value = ''
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell
    icon="⚕️"
    title="Tana massa indeksi (BMI)"
    description="BMI qiymatini hisoblang; yoshga mos talqinni ko‘ring"
    hint="Yosh, vazn va bo‘yni kiriting. BMI vazn (kg) / bo‘y² (m) formulasi bilan hisoblanadi."
  >
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Yosh (yil)</label>
        <input v-model="age" type="number" min="0" max="120" step="1" class="input" placeholder="masalan: 25" @keyup.enter="calculate" />
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Vazn (kg)</label>
          <input v-model="weight" type="number" min="0" step="0.1" class="input" placeholder="masalan: 68" @keyup.enter="calculate" />
        </div>
        <div>
          <label class="label">Bo‘y (sm)</label>
          <input v-model="height" type="number" min="0" step="0.1" class="input" placeholder="masalan: 172" @keyup.enter="calculate" />
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <transition name="page-fade">
        <div v-if="result" class="mt-5 rounded-xl border px-5 py-4 text-center animate-resultPop" :class="[result.bg || 'bg-slate-50', 'border-transparent dark:bg-slate-700/60']">
          <p class="text-xs font-medium uppercase tracking-wide" :class="result.color || 'text-slate-600'">BMI qiymati</p>
          <p class="text-3xl font-extrabold mt-1" :class="result.color || 'text-slate-700'">{{ result.bmi }}</p>
          <p v-if="result.adult" class="text-sm font-semibold mt-1" :class="result.color">{{ result.label }}</p>
          <p v-else class="text-sm mt-2 text-slate-600 dark:text-slate-300">
            20 yoshgacha BMI toifasi yosh va jinsga qarab o‘zgaradi. Bu yerda faqat formula bo‘yicha son ko‘rsatildi; WHO o‘sish jadvali bilan baholang.
          </p>
        </div>
      </transition>

      <p class="text-xs text-slate-400 dark:text-slate-500 text-center pt-1">
        Kattalar toifalari 20 yoshdan boshlab qo‘llanadi. Bolalar va o‘smirlar uchun yosh-jinsga mos WHO mezoni kerak; BMI tibbiy tashxis emas.
      </p>
    </div>
  </ToolShell>
</template>
