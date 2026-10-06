<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const amount = ref('')
const rate = ref('')
const months = ref('')

const monthlyPayment = computed(() => {
  if (amount.value === '' || rate.value === '' || months.value === '') return null
  const p = Number(amount.value)
  const r = (Number(rate.value) / 100) / 12
  const n = Number(months.value)
  if (!Number.isFinite(p) || !Number.isFinite(r) || !Number.isInteger(n) || p <= 0 || r < 0 || n <= 0 || n > 600) return null
  if (r === 0) return Math.round(p / n)
  const pay = p * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
  return Math.round(pay)
})

const totalPayment = computed(() => monthlyPayment.value === null ? null : monthlyPayment.value * Number(months.value))
const totalInterest = computed(() => totalPayment.value === null ? null : Math.max(0, totalPayment.value - Number(amount.value)))

function formatMoney(val) {
  return (val || 0).toLocaleString('uz-UZ') + ' so\'m'
}
</script>

<template>
  <ToolShell icon="🏦" title="Kredit kalkulyatori" description="Kiritilgan shartlar bo‘yicha taxminiy annuitet to‘lovini hisoblang" hint="Kredit summasi, bankingiz taklif qilgan stavka va muddatni kiriting — hisob darhol yangilanadi.">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <p class="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700/40 p-3 text-xs text-amber-800 dark:text-amber-200">Banklarning foiz stavkalari jonli olinmaydi. Bankingiz taklifini kiriting; hisob annuitet formulasiga asoslangan, komissiya, sug‘urta va bankning individual jadvalini qamramaydi.</p>
      <div>
        <label class="label">Kredit summasi (so'm)</label>
        <input v-model="amount" type="number" min="1" class="input" step="1000000" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Yillik foiz stavkasi (%)</label>
          <input v-model="rate" type="number" min="0" max="100" class="input" step="0.1" placeholder="masalan: 24" />
        </div>
        <div>
          <label class="label">Muddat (oy)</label>
          <input v-model="months" type="number" min="1" max="600" class="input" step="1" placeholder="masalan: 12" />
        </div>
      </div>

      <p v-if="monthlyPayment === null" class="text-sm text-slate-500">To‘g‘ri hisob uchun summa, stavka va muddatni kiriting.</p>
      <div v-else class="rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-800 dark:to-slate-800/80 border border-brand-100 dark:border-slate-700 p-5 space-y-3 mt-4">
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
