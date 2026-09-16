<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('valyuta-konvertori'))

// TAXMINIY KURSLAR — 1 birlik = shuncha USD.
// Bu kurslar tashqi API'ga ulanmasdan ishlashi uchun qo'lda kiritilgan va
// vaqt o'tishi bilan eskiradi. Yangilash uchun shu obyektdagi raqamlarni
// joriy bozor kursiga moslab tahrirlang.
const RATES_TO_USD = {
  USD: { label: 'AQSH dollari (USD)', rate: 1 },
  UZS: { label: "O'zbek so'mi (UZS)", rate: 1 / 12700 },
  EUR: { label: 'Yevro (EUR)', rate: 1.08 },
  RUB: { label: 'Rossiya rubli (RUB)', rate: 1 / 92 },
  GBP: { label: 'Angliya funti (GBP)', rate: 1.27 },
  KZT: { label: 'Qozog\u2019iston tengesi (KZT)', rate: 1 / 480 },
}

const LAST_UPDATED = '2026-yil boshi (taxminiy)'

const value = ref('')
const from = ref('USD')
const to = ref('UZS')
const error = ref('')

const result = computed(() => {
  error.value = ''
  if (value.value === '') return null
  const num = parseFloat(value.value)
  if (Number.isNaN(num)) {
    error.value = 'Iltimos, faqat raqam kiriting.'
    return null
  }
  const usd = num * RATES_TO_USD[from.value].rate
  const converted = usd / RATES_TO_USD[to.value].rate
  return Math.round(converted * 100) / 100
})

function reset() {
  value.value = ''
  from.value = 'USD'
  to.value = 'UZS'
  error.value = ''
}

function swap() {
  ;[from.value, to.value] = [to.value, from.value]
}
</script>

<template>
  <ToolShell
    icon="💱"
    title="Valyuta konvertori"
    description="So‘m, dollar, yevro va boshqa valyutalar"
    hint="Qiymatni kiriting, valyutalarni tanlang — natija taxminiy kurs asosida hisoblanadi (pastdagi eslatmaga qarang)."
  >
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Qiymat</label>
        <input v-model="value" type="number" class="input" placeholder="masalan: 100" />
      </div>

      <div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-end">
        <div>
          <label class="label">Dan</label>
          <select v-model="from" class="input">
            <option v-for="(u, key) in RATES_TO_USD" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
        <button class="btn-secondary !px-3 !py-2.5 mb-0.5" @click="swap" title="Almashtirish">⇄</button>
        <div>
          <label class="label">Ga</label>
          <select v-model="to" class="input">
            <option v-for="(u, key) in RATES_TO_USD" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
      </div>

      <button class="btn-secondary w-full" @click="reset">Tozalash</button>

      <transition name="page-fade">
        <div v-if="result !== null" class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop">
          <p class="text-xs font-medium text-brand-600 dark:text-brand-300 uppercase tracking-wide">Natija</p>
          <p class="text-2xl font-extrabold text-brand-800 dark:text-brand-200 mt-1 break-words">
            {{ value }} {{ from }} ≈ {{ result }} {{ to }}
          </p>
        </div>
      </transition>

      <p class="text-xs text-slate-400 dark:text-slate-500 text-center pt-1">
        ⚠️ Kurslar taxminiy va real vaqtda yangilanmaydi (oxirgi tahrir: {{ LAST_UPDATED }}). Aniq kurs uchun bankingiz
        yoki rasmiy manbaga murojaat qiling.
      </p>
    </div>
  </ToolShell>
</template>
