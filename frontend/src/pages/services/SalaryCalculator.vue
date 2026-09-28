<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import FormAlert from '../../components/FormAlert.vue' // FormAlert ni import qilamiz

const salary = ref(5000000)
const error = ref('') // Yangi error ref

function calculateSalary() {
  error.value = ''
  if (salary.value > 1_000_000_000) { // 1 milliard so'mdan katta bo'lsa
    error.value = 'Kiritilgan maosh juda katta. Maksimal 1 milliard so\'m.'
    return { tax: 0, pension: 0, netSalary: 0 }
  }
  const taxValue = salary.value * 0.12
  const pensionValue = salary.value * 0.01
  const netSalaryValue = salary.value - taxValue - pensionValue
  return { tax: taxValue, pension: pensionValue, netSalary: netSalaryValue }
}

const calculatedValues = computed(() => calculateSalary()) // Yangi computed property

const tax = computed(() => calculatedValues.value.tax)
const pension = computed(() => calculatedValues.value.pension)
const netSalary = computed(() => calculatedValues.value.netSalary)

function formatMoney(amount) {
  if (typeof amount !== 'number' || isNaN(amount)) return '0 so\'m'
  return amount.toLocaleString('uz-UZ') + ' so\'m'
}
</script>

<template>
  <ToolShell title="Oylik maosh hisoblagich" icon="💵" description="Daromad solig'i va INPS ushlanmalarini hisoblash">
    <div class="space-y-6">
      <FormAlert :message="error" />
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Qo'lga tegadigan emas, hisoblangan (Qora) maosh</label>
        <div class="relative">
          <input 
            v-model.number="salary" 
            type="number" 
            class="w-full pl-4 pr-12 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-500/50"
            :max="1_000_000_000" 
          >
          <span class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">so'm</span>
        </div>
      </div>

      <div class="bg-slate-50 dark:bg-slate-800/50 p-6 rounded-2xl space-y-4">
        <div class="flex justify-between items-center pb-4 border-b border-slate-200 dark:border-slate-700">
          <span class="text-slate-500">Daromad solig'i (12%)</span>
          <span class="font-medium text-red-500">- {{ formatMoney(tax) }}</span>
        </div>
        <div class="flex justify-between items-center pb-4 border-b border-slate-200 dark:border-slate-700">
          <span class="text-slate-500">INPS / Pensiya (1%)</span>
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
