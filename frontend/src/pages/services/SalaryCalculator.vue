<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useToolText } from '../../utils/toolText'
import { useI18n } from '../../i18n'

const { t } = useI18n()

const tx = useToolText({
  uz: {
    title: "Oylik maosh hisoblagich",
    desc: "O‘zbekiston soliq rezidenti uchun taxminiy sof maosh (imtiyozlarsiz)",
    note: "Soliq va INPS stavkalari saytdan jonli olinmaydi. Amaldagi stavkalarni rasmiy manbadan tekshirib kiriting; imtiyozlar va alohida holatlar hisobga olinmaydi.",
    grossSalary: "Hisoblangan (brutto) maosh",
    taxRate: "JShDS stavkasi (%)",
    pensionRate: "INPS stavkasi (%)",
    placeholderRate: "rasmiy stavka",
    promptToCalc: "Hisobni ko‘rish uchun brutto maosh va stavkalarni kiriting.",
    taxDeduct: "JShDS (INPS ayirilgach, {r}%)",
    pensionDeduct: "INPS / jamg‘arib boriladigan pensiya ({r}%)",
    netSalary: "Qo'lga tegadigan (Sof)",
    errPositive: "Maoshni musbat son bilan kiriting.",
    errMax: "Kiritilgan maosh juda katta. Maksimal 1 milliard so'm.",
    errRates: "Soliq va pensiya stavkalarini 0 dan 100 foizgacha kiriting.",
  },
  ru: {
    title: "Калькулятор зарплаты",
    desc: "Примерный расчёт чистой зарплаты для резидента Узбекистана",
    note: "Ставки налогов и ИНПС не берутся автоматически. Введите действующие ставки из официальных источников; льготы не учитываются.",
    grossSalary: "Начисленная (брутто) зарплата",
    taxRate: "Ставка НДФЛ (%)",
    pensionRate: "Ставка ИНПС (%)",
    placeholderRate: "официальная ставка",
    promptToCalc: "Введите брутто-зарплату и ставки для расчёта.",
    taxDeduct: "НДФЛ (после вычета ИНПС, {r}%)",
    pensionDeduct: "ИНПС / накопительная пенсия ({r}%)",
    netSalary: "На руки (чистая зарплата)",
    errPositive: "Введите зарплату положительным числом.",
    errMax: "Введённая зарплата слишком велика. Максимум 1 млрд сум.",
    errRates: "Введите ставки налога и пенсии от 0 до 100%.",
  },
  en: {
    title: "Salary Calculator",
    desc: "Estimated net salary calculation for Uzbekistan tax residents",
    note: "Tax and INPS pension rates are not fetched live. Enter official current rates; deductions or exemptions are not included.",
    grossSalary: "Gross salary",
    taxRate: "Income tax rate (%)",
    pensionRate: "INPS pension rate (%)",
    placeholderRate: "official rate",
    promptToCalc: "Enter gross salary and rates to calculate.",
    taxDeduct: "Income tax (after INPS, {r}%)",
    pensionDeduct: "INPS / funded pension ({r}%)",
    netSalary: "Net take-home pay",
    errPositive: "Please enter a positive salary amount.",
    errMax: "Salary entered is too high. Max 1 billion sum.",
    errRates: "Please enter tax and pension rates between 0 and 100%.",
  },
})

const salary = ref(5000000)
const taxRate = ref('')
const pensionRate = ref('')
const errorKey = ref('')

function calculateSalary() {
  errorKey.value = ''
  if (taxRate.value === '' || pensionRate.value === '') return null
  const taxPercent = Number(taxRate.value)
  const pensionPercent = Number(pensionRate.value)
  if (!Number.isFinite(salary.value) || salary.value <= 0) {
    errorKey.value = 'errPositive'
    return { tax: 0, pension: 0, netSalary: 0 }
  }
  if (salary.value > 1_000_000_000) {
    errorKey.value = 'errMax'
    return { tax: 0, pension: 0, netSalary: 0 }
  }
  if (![taxPercent, pensionPercent].every(Number.isFinite) || taxPercent < 0 || taxPercent > 100 || pensionPercent < 0 || pensionPercent > 100) {
    errorKey.value = 'errRates'
    return null
  }
  const pensionValue = salary.value * pensionPercent / 100
  const taxValue = Math.max(0, salary.value * taxPercent / 100 - pensionValue)
  const netSalaryValue = salary.value - taxValue - pensionValue
  return { tax: taxValue, pension: pensionValue, netSalary: netSalaryValue }
}

const calculatedValues = computed(() => calculateSalary())

const tax = computed(() => calculatedValues.value?.tax ?? 0)
const pension = computed(() => calculatedValues.value?.pension ?? 0)
const netSalary = computed(() => calculatedValues.value?.netSalary ?? 0)

function formatMoney(amount) {
  if (typeof amount !== 'number' || isNaN(amount)) return '0 ' + t('common.currency')
  return amount.toLocaleString('uz-UZ') + ' ' + t('common.currency')
}
</script>

<template>
  <ToolShell :title="tx.title" icon="💵" :description="tx.desc">
    <template #header><AppHeader /></template>
    <div class="space-y-6">
      <FormAlert :message="errorKey ? tx[errorKey] : ''" />
      <p class="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700/40 p-3 text-xs text-amber-800 dark:text-amber-200">{{ tx.note }}</p>
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">{{ tx.grossSalary }}</label>
        <div class="relative">
          <input 
            v-model.number="salary" 
            type="number" 
            class="w-full pl-4 pr-16 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-500/50 text-slate-800 dark:text-slate-100"
            min="0"
            :max="1_000_000_000" 
          >
          <span class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-sm">{{ t('common.currency') }}</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">{{ tx.taxRate }}</label>
          <input v-model="taxRate" type="number" min="0" max="100" step="0.1" :placeholder="tx.placeholderRate" class="input" />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">{{ tx.pensionRate }}</label>
          <input v-model="pensionRate" type="number" min="0" max="100" step="0.1" :placeholder="tx.placeholderRate" class="input" />
        </div>
      </div>

      <p v-if="!calculatedValues" class="text-sm text-slate-500 dark:text-slate-400">{{ tx.promptToCalc }}</p>
      <div v-else class="bg-slate-50 dark:bg-slate-800/50 p-6 rounded-2xl space-y-4">
        <div class="flex justify-between items-center pb-4 border-b border-slate-200 dark:border-slate-700">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.taxDeduct.replace('{r}', taxRate) }}</span>
          <span class="font-medium text-red-500">- {{ formatMoney(tax) }}</span>
        </div>
        <div class="flex justify-between items-center pb-4 border-b border-slate-200 dark:border-slate-700">
          <span class="text-slate-500 dark:text-slate-400">{{ tx.pensionDeduct.replace('{r}', pensionRate) }}</span>
          <span class="font-medium text-red-500">- {{ formatMoney(pension) }}</span>
        </div>
        <div class="flex justify-between items-center pt-2">
          <span class="font-bold text-lg text-slate-800 dark:text-slate-200">{{ tx.netSalary }}</span>
          <span class="font-bold text-xl text-brand-600 dark:text-brand-400">{{ formatMoney(netSalary) }}</span>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
