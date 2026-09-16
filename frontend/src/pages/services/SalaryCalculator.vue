<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'

const salary = ref(5000000)

const tax = computed(() => salary.value * 0.12)
const pension = computed(() => salary.value * 0.01)
const netSalary = computed(() => salary.value - tax.value - pension.value)

function formatMoney(amount) {
  return amount.toLocaleString('uz-UZ') + ' so\'m'
}
</script>

<template>
  <ToolShell title="Oylik maosh hisoblagich" icon="💵" description="Daromad solig'i va INPS ushlanmalarini hisoblash">
    <div class="space-y-6">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Qo'lga tegadigan emas, hisoblangan (Qora) maosh</label>
        <div class="relative">
          <input 
            v-model.number="salary" 
            type="number" 
            class="w-full pl-4 pr-12 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-500/50"
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
