<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const depositAmount = ref(10000000)
const annualRate = ref(21)
const durationMonths = ref(12)
const capitalize = ref(true)

const result = computed(() => {
  const p = Number(depositAmount.value) || 0
  const r = (Number(annualRate.value) || 0) / 100
  const m = Number(durationMonths.value) || 1

  if (capitalize.value) {
    // Compound monthly interest: A = P * (1 + r/12)^m
    const total = p * Math.pow(1 + r / 12, m)
    const profit = total - p
    return {
      total: Math.round(total),
      profit: Math.round(profit),
      monthlyAvg: Math.round(profit / m)
    }
  } else {
    // Simple interest
    const profit = p * r * (m / 12)
    return {
      total: Math.round(p + profit),
      profit: Math.round(profit),
      monthlyAvg: Math.round(profit / m)
    }
  }
})

function formatMoney(val) {
  return (val || 0).toLocaleString('uz-UZ') + ' so\'m'
}
</script>

<template>
  <ToolShell icon="📈" title="Omonat va Jamg'arma kalkulyatori" description="Bank depozitlari va omonatlardan olinadigan sof daromadni hisoblang" hint="Boshlang'ich summa, yillik foiz va muddatni kiriting — jami foydangiz avtomatik hisoblanadi.">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <div>
        <label class="label">Boshlang'ich summa (so'm)</label>
        <input v-model.number="depositAmount" type="number" class="input" step="1000000" min="100000" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Yillik foiz stavkasi (%)</label>
          <input v-model.number="annualRate" type="number" class="input" step="0.5" min="1" max="100" />
        </div>
        <div>
          <label class="label">Muddat (oy)</label>
          <input v-model.number="durationMonths" type="number" class="input" step="1" min="1" max="60" />
        </div>
      </div>

      <label class="flex items-center gap-2.5 text-sm text-slate-700 dark:text-slate-300 cursor-pointer pt-1">
        <input v-model="capitalize" type="checkbox" class="rounded text-brand-600 focus:ring-brand-400 w-4 h-4" />
        <span>Oylik kapitalizatsiya (foiz ustiga foiz qo'shilishi)</span>
      </label>

      <div class="rounded-2xl bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-slate-800 dark:to-slate-800/80 border border-emerald-100 dark:border-slate-700 p-5 space-y-3 mt-4 shadow-sm">
        <div class="flex justify-between items-center text-sm">
          <span class="text-slate-500 dark:text-slate-400">Sof foyda (daromad):</span>
          <span class="text-xl font-extrabold text-emerald-600 dark:text-emerald-400">+{{ formatMoney(result.profit) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2.5">
          <span class="text-slate-500 dark:text-slate-400">O'rtacha oylik daromad:</span>
          <span class="font-semibold text-slate-800 dark:text-slate-200">{{ formatMoney(result.monthlyAvg) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2.5">
          <span class="text-slate-500 dark:text-slate-400">Muddat oxirida jami summa:</span>
          <span class="text-base font-bold text-slate-900 dark:text-white">{{ formatMoney(result.total) }}</span>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
