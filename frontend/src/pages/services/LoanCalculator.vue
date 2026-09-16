<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const amount = ref(20000000)
const rate = ref(24)
const months = ref(12)

const monthlyPayment = computed(() => {
  const p = amount.value
  const r = (rate.value / 100) / 12
  const n = months.value
  if (!p || !r || !n) return 0
  const pay = p * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
  return Math.round(pay)
})

const totalPayment = computed(() => monthlyPayment.value * months.value)
const totalInterest = computed(() => Math.max(0, totalPayment.value - amount.value))

function formatMoney(val) {
  return (val || 0).toLocaleString('uz-UZ') + ' so\'m'
}
</script>

<template>
  <ToolShell icon="🏦" title="Kredit kalkulyatori" description="Kredit oylik to'lovlarini va umumiy foizni hisoblang" hint="Kredit summasi, yillik foiz va muddatni kiriting — oylik to'lov avtomatik hisoblanadi.">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <div>
        <label class="label">Kredit summasi (so'm)</label>
        <input v-model.number="amount" type="number" class="input" step="1000000" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Yillik foiz stavkasi (%)</label>
          <input v-model.number="rate" type="number" class="input" step="0.5" />
        </div>
        <div>
          <label class="label">Muddat (oy)</label>
          <input v-model.number="months" type="number" class="input" step="1" />
        </div>
      </div>

      <div class="rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-800 dark:to-slate-800/80 border border-brand-100 dark:border-slate-700 p-5 space-y-3 mt-4">
        <div class="flex justify-between items-center text-sm">
          <span class="text-slate-500 dark:text-slate-400">Oylik to'lov (annuitet):</span>
          <span class="text-lg font-bold text-brand-700 dark:text-brand-300">{{ formatMoney(monthlyPayment) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2">
          <span class="text-slate-500 dark:text-slate-400">Jami to'lanadigan summa:</span>
          <span class="font-semibold text-slate-800 dark:text-slate-200">{{ formatMoney(totalPayment) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2">
          <span class="text-slate-500 dark:text-slate-400">Jami foiz ustamasi:</span>
          <span class="font-semibold text-amber-600 dark:text-amber-400">+{{ formatMoney(totalInterest) }}</span>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
