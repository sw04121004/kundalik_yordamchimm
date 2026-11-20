<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useToolText } from '../../utils/toolText'
import { useI18n } from '../../i18n'

const { t } = useI18n()

const tx = useToolText({
  uz: {
    title: "Omonat va jamg‘arma kalkulyatori",
    desc: "Kiritilgan stavka bo‘yicha taxminiy daromadni hisoblang",
    hint: "Summani, bankingiz taklif qilgan yillik stavkani va muddatni kiriting — natija darhol yangilanadi.",
    note: "Bank omonat stavkalari bu yerda jonli olinmaydi. Bankingiz taklifidagi stavkani kiriting; natija taxminiy va soliq hamda bank shartlarini hisobga olmaydi.",
    initialAmount: "Boshlang'ich summa",
    annualRate: "Yillik foiz stavkasi (%)",
    durationMonths: "Muddat (oy)",
    placeholderRate: "masalan: 20",
    placeholderMonths: "masalan: 12",
    capitalize: "Oylik kapitalizatsiya (foiz ustiga foiz qo'shilishi)",
    promptInput: "To‘g‘ri hisob uchun summa, stavka va muddatni kiriting.",
    profit: "Taxminiy daromad:",
    monthlyAvg: "O'rtacha oylik daromad:",
    total: "Muddat oxirida jami summa:",
  },
  ru: {
    title: "Калькулятор вкладов и накоплений",
    desc: "Расчёт доходности по вкладу с учётом процентной ставки",
    hint: "Введите сумму, годовую ставку вашего банка и срок — расчёт обновится сразу.",
    note: "Ставки вкладов не берутся автоматически. Введите предложение банка; расчёт приблизительный и не учитывает налоги и условия банка.",
    initialAmount: "Начальная сумма",
    annualRate: "Годовая процентная ставка (%)",
    durationMonths: "Срок (месяцев)",
    placeholderRate: "например: 20",
    placeholderMonths: "например: 12",
    capitalize: "Ежемесячная капитализация (проценты на проценты)",
    promptInput: "Введите сумму, ставку и срок для расчёта.",
    profit: "Примерный доход:",
    monthlyAvg: "Средний доход в месяц:",
    total: "Итоговая сумма в конце срока:",
  },
  en: {
    title: "Deposit & Savings Calculator",
    desc: "Calculate estimated deposit returns based on interest rate",
    hint: "Enter deposit amount, annual rate, and duration — result calculates instantly.",
    note: "Bank deposit rates are not fetched live. Enter your bank's rate; result is approximate and excludes taxes or special conditions.",
    initialAmount: "Initial deposit amount",
    annualRate: "Annual interest rate (%)",
    durationMonths: "Term (months)",
    placeholderRate: "e.g. 20",
    placeholderMonths: "e.g. 12",
    capitalize: "Monthly capitalization (compound interest)",
    promptInput: "Enter deposit amount, rate, and term to calculate.",
    profit: "Estimated interest earnings:",
    monthlyAvg: "Average monthly return:",
    total: "Total amount at maturity:",
  },
})

const depositAmount = ref('')
const annualRate = ref('')
const durationMonths = ref('')
const capitalize = ref(true)

const result = computed(() => {
  if (depositAmount.value === '' || annualRate.value === '' || durationMonths.value === '') return null
  const p = Number(depositAmount.value)
  const r = Number(annualRate.value) / 100
  const m = Number(durationMonths.value)
  if (!Number.isFinite(p) || !Number.isFinite(r) || !Number.isInteger(m) || p <= 0 || r < 0 || m < 1 || m > 600) return null

  if (capitalize.value) {
    const total = p * Math.pow(1 + r / 12, m)
    const profit = total - p
    return {
      total: Math.round(total),
      profit: Math.round(profit),
      monthlyAvg: Math.round(profit / m)
    }
  } else {
    const profit = p * r * (m / 12)
    return {
      total: Math.round(p + profit),
      profit: Math.round(profit),
      monthlyAvg: Math.round(profit / m)
    }
  }
})

function formatMoney(val) {
  return `${(val || 0).toLocaleString('uz-UZ')} ${t('common.currency')}`
}
</script>

<template>
  <ToolShell icon="📈" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <p class="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700/40 p-3 text-xs text-amber-800 dark:text-amber-200">{{ tx.note }}</p>
      <div>
        <label class="label">{{ tx.initialAmount }} ({{ t('common.currency') }})</label>
        <input v-model="depositAmount" type="number" class="input" step="1000000" min="1" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">{{ tx.annualRate }}</label>
          <input v-model="annualRate" type="number" class="input" step="0.1" min="0" max="100" :placeholder="tx.placeholderRate" />
        </div>
        <div>
          <label class="label">{{ tx.durationMonths }}</label>
          <input v-model="durationMonths" type="number" class="input" step="1" min="1" max="600" :placeholder="tx.placeholderMonths" />
        </div>
      </div>

      <label class="flex items-center gap-2.5 text-sm text-slate-700 dark:text-slate-300 cursor-pointer pt-1">
        <input v-model="capitalize" type="checkbox" class="rounded text-brand-600 focus:ring-brand-400 w-4 h-4" />
        <span>{{ tx.capitalize }}</span>
      </label>

      <p v-if="!result" class="text-sm text-slate-500 dark:text-slate-400">{{ tx.promptInput }}</p>
      <div v-else class="rounded-2xl bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-slate-800 dark:to-slate-800/80 border border-emerald-100 dark:border-slate-700 p-5 space-y-3 mt-4 shadow-sm">
        <div class="flex justify-between items-center text-sm">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.profit }}</span>
          <span class="text-xl font-extrabold text-emerald-600 dark:text-emerald-400">+{{ formatMoney(result.profit) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2.5">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.monthlyAvg }}</span>
          <span class="font-semibold text-slate-800 dark:text-slate-200">{{ formatMoney(result.monthlyAvg) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm border-t border-slate-200/60 dark:border-slate-700/60 pt-2.5">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.total }}</span>
          <span class="text-base font-bold text-slate-900 dark:text-white">{{ formatMoney(result.total) }}</span>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
