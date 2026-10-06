<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import FormAlert from '../../components/FormAlert.vue' // FormAlert ni import qilamiz

const salary = ref(5000000)
const taxRate = ref('')
const pensionRate = ref('')
const error = ref('')

function calculateSalary() {
  error.value = ''
  if (taxRate.value === '' || pensionRate.value === '') return null
  const taxPercent = Number(taxRate.value)
  const pensionPercent = Number(pensionRate.value)
  if (!Number.isFinite(salary.value) || salary.value <= 0) {
    error.value = 'Maoshni musbat son bilan kiriting.'
    return { tax: 0, pension: 0, netSalary: 0 }
  }
  if (salary.value > 1_000_000_000) {
    error.value = 'Kiritilgan maosh juda katta. Maksimal 1 milliard so\'m.'
    return { tax: 0, pension: 0, netSalary: 0 }
  }
  if (![taxPercent, pensionPercent].every(Number.isFinite) || taxPercent < 0 || taxPercent > 100 || pensionPercent < 0 || pensionPercent > 100) {
    error.value = 'Soliq va pensiya stavkalarini 0 dan 100 foizgacha kiriting.'
    return null
  }
  const pensionValue = salary.value * pensionPercent / 100
  const taxValue = Math.max(0, salary.value * taxPercent / 100 - pensionValue)
  const netSalaryValue = salary.value - taxValue - pensionValue
  return { tax: taxValue, pension: pensionValue, netSalary: netSalaryValue }
}

const calculatedValues = computed(() => calculateSalary()) // Yangi computed property

const tax = computed(() => calculatedValues.value?.tax ?? 0)
const pension = computed(() => calculatedValues.value?.pension ?? 0)
const netSalary = computed(() => calculatedValues.value?.netSalary ?? 0)

function formatMoney(amount) {
  if (typeof amount !== 'number' || isNaN(amount)) return '0 so\'m'
  return amount.toLocaleString('uz-UZ') + ' so\'m'
}
</script>

<template>
  <ToolShell title="Oylik maosh hisoblagich" icon="💵" description="O‘zbekiston soliq rezidenti uchun taxminiy sof maosh (imtiyozlarsiz)">
    <div class="space-y-6">
      <FormAlert :message="error" />
      <p class="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700/40 p-3 text-xs text-amber-800 dark:text-amber-200">Soliq va INPS stavkalari saytdan jonli olinmaydi. Amaldagi stavkalarni rasmiy manbadan tekshirib kiriting; imtiyozlar va alohida holatlar hisobga olinmaydi.</p>
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Hisoblangan (brutto) maosh</label>
        <div class="relative">
          <input 
            v-model.number="salary" 
            type="number" 
            class="w-full pl-4 pr-12 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-500/50"
            min="0"
            :max="1_000_000_000" 
          >
          <span class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">so'm</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">JShDS stavkasi (%)</label>
          <input v-model="taxRate" type="number" min="0" max="100" step="0.1" placeholder="rasmiy stavka" class="input" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">INPS stavkasi (%)</label>
          <input v-model="pensionRate" type="number" min="0" max="100" step="0.1" placeholder="rasmiy stavka" class="input" />
        </div>
      </div>

      <p v-if="!calculatedValues" class="text-sm text-slate-500">Hisobni ko‘rish uchun brutto maosh va stavkalarni kiriting.</p>
      <div v-else class="bg-slate-50 dark:bg-slate-800/50 p-6 rounded-2xl space-y-4">
        <div class="flex justify-between items-center pb-4 border-b border-slate-200 dark:border-slate-700">
          <span class="text-slate-500">JShDS (INPS ayirilgach, {{ taxRate }}%)</span>
          <span class="font-medium text-red-500">- {{ formatMoney(tax) }}</span>
        </div>
        <div class="flex justify-between items-center pb-4 border-b border-slate-200 dark:border-slate-700">
          <span class="text-slate-500">INPS / jamg‘arib boriladigan pensiya ({{ pensionRate }}%)</span>
          <span class="font-medium text-red-500">- {{ formatMoney(pension) }}</span>
        </div>
        <div class="flex justify-between items-center pt-2">
          <span class="font-bold text-lg text-slate-800 dark:text-slate-200">Qo'lga tegadigan (Sof)</span>
          <span class="font-bold text-xl text-brand-600 dark:text-brand-400">{{ formatMoney(netSalary) }}</span>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
