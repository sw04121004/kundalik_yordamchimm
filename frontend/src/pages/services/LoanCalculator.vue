<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useToolText } from '../../utils/toolText'
import { useI18n } from '../../i18n'

const { t } = useI18n()

const tx = useToolText({
  uz: {
    title: "Kredit kalkulyatori",
    desc: "Kiritilgan shartlar bo‘yicha taxminiy annuitet to‘lovini hisoblang",
    hint: "Kredit summasi, bankingiz taklif qilgan stavka va muddatni kiriting — hisob darhol yangilanadi.",
    note: "Banklarning foiz stavkalari jonli olinmaydi. Bankingiz taklifini kiriting; hisob annuitet formulasiga asoslangan, komissiya, sug‘urta va bankning individual jadvalini qamramaydi.",
    loanAmount: "Kredit summasi",
    annualRate: "Yillik foiz stavkasi (%)",
    durationMonths: "Muddat (oy)",
    placeholderRate: "masalan: 24",
    placeholderMonths: "masalan: 12",
    promptInput: "To‘g‘ri hisob uchun summa, stavka va muddatni kiriting.",
    monthlyPayment: "Oylik to'lov (annuitet):",
    totalPayment: "Jami to'lanadigan summa:",
    totalInterest: "Jami foiz ustamasi:",
  },
  ru: {
    title: "Кредитный калькулятор",
    desc: "Расчёт аннуитетного платежа по заданным условиям",
    hint: "Введите сумму кредита, предложенную банком ставку и срок — результат рассчитается сразу.",
    note: "Процентные ставки банков не берутся автоматически. Введите предложение банка; расчёт основан на аннуитете и не включает комиссии и страховку.",
    loanAmount: "Сумма кредита",
    annualRate: "Годовая процентная ставка (%)",
    durationMonths: "Срок (месяцев)",
    placeholderRate: "например: 24",
    placeholderMonths: "например: 12",
    promptInput: "Введите сумму, ставку и срок для точного расчёта.",
    monthlyPayment: "Ежемесячный платёж (аннуитет):",
    totalPayment: "Всего к выплате:",
    totalInterest: "Сумма процентов:",
  },
  en: {
    title: "Loan Calculator",
    desc: "Estimate monthly annuity payments based on loan terms",
    hint: "Enter loan amount, your bank's interest rate and term — calculation updates immediately.",
    note: "Bank interest rates are not fetched live. Enter your bank's offer; calculation uses standard annuity formula and excludes commissions or insurance.",
    loanAmount: "Loan amount",
    annualRate: "Annual interest rate (%)",
    durationMonths: "Term (months)",
    placeholderRate: "e.g. 24",
    placeholderMonths: "e.g. 12",
    promptInput: "Enter amount, interest rate, and term to calculate.",
    monthlyPayment: "Monthly payment (annuity):",
    totalPayment: "Total payment amount:",
    totalInterest: "Total interest:",
  },
})

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
  return `${(val || 0).toLocaleString('uz-UZ')} ${t('common.currency')}`
}
</script>

<template>
  <ToolShell icon="🏦" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <p class="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700/40 p-3 text-xs text-amber-800 dark:text-amber-200">{{ tx.note }}</p>
      <div>
        <label class="label">{{ tx.loanAmount }} ({{ t('common.currency') }})</label>
        <input v-model="amount" type="number" min="1" class="input" step="1000000" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">{{ tx.annualRate }}</label>
          <input v-model="rate" type="number" min="0" max="100" class="input" step="0.1" :placeholder="tx.placeholderRate" />
        </div>
        <div>
          <label class="label">{{ tx.durationMonths }}</label>
          <input v-model="months" type="number" min="1" max="600" class="input" step="1" :placeholder="tx.placeholderMonths" />
        </div>
      </div>

      <p v-if="monthlyPayment === null" class="text-sm text-slate-500 dark:text-slate-400">{{ tx.promptInput }}</p>
      <div v-else class="rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-800 dark:to-slate-800/80 border border-brand-100 dark:border-slate-700 p-5 space-y-3 mt-4">
        <div class="flex justify-between items-center text-sm">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.monthlyPayment }}</span>
          <span class="text-lg font-bold text-brand-700 dark:text-brand-300">{{ formatMoney(monthlyPayment) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.totalPayment }}</span>
          <span class="font-semibold text-slate-800 dark:text-slate-200">{{ formatMoney(totalPayment) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.totalInterest }}</span>
          <span class="font-semibold text-amber-600 dark:text-amber-400">+{{ formatMoney(totalInterest) }}</span>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
