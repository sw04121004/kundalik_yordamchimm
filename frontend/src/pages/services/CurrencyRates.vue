<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { fetchOfficialCurrencyRates } from '../../api/currencyRates'
import { useToolText } from '../../utils/toolText'
import { useI18n } from '../../i18n'

const { t } = useI18n()

const tx = useToolText({
  uz: {
    title: "Valyuta kurslari",
    desc: "O‘zbekiston Markaziy bankining rasmiy kurslari",
    hint: "Rasmiy kurslar kunlik e’lon qilinadi; ular bankdagi sotib olish yoki sotish narxidan farq qilishi mumkin.",
    amount: "Miqdor",
    baseCurrency: "Asosiy valyuta",
    loading: "Markaziy bank kurslari olinmoqda…",
    source: "Manba: O‘zbekiston Respublikasi Markaziy banki · amal qilish sanasi:",
    refresh: "Kursni yangilash",
    retry: "Qayta urinish",
    cbuArchive: "Markaziy bank kurslari",
    errOldNotShown: "Eski kurslar ko‘rsatilmaydi.",
    errFetch: "Kurslarni hozir olib bo‘lmadi.",
    currencySum: "so‘m",
  },
  ru: {
    title: "Курсы валют",
    desc: "Официальные курсы Центрального банка Узбекистана",
    hint: "Официальные курсы публикуются ежедневно; они могут отличаться от курсов покупки/продажи в коммерческих банках.",
    amount: "Сумма",
    baseCurrency: "Базовая валюта",
    loading: "Загрузка курсов Центрального банка…",
    source: "Источник: Центральный банк Республики Узбекистан · дата действия:",
    refresh: "Обновить курс",
    retry: "Повторить попытку",
    cbuArchive: "Курсы Центрального банка",
    errOldNotShown: "Устаревшие курсы не отображаются.",
    errFetch: "Не удалось получить курсы валют.",
    currencySum: "сум",
  },
  en: {
    title: "Currency Rates",
    desc: "Official exchange rates of the Central Bank of Uzbekistan",
    hint: "Official rates are published daily; they may differ from buy/sell rates in commercial banks.",
    amount: "Amount",
    baseCurrency: "Base currency",
    loading: "Loading Central Bank rates…",
    source: "Source: Central Bank of the Republic of Uzbekistan · effective date:",
    refresh: "Refresh rates",
    retry: "Try again",
    cbuArchive: "Central Bank rates",
    errOldNotShown: "Outdated rates are not shown.",
    errFetch: "Could not retrieve currency rates.",
    currencySum: "UZS",
  },
})

const rates = ref([])
const amount = ref(100)
const selectedCode = ref('USD')
const loading = ref(true)
const error = ref('')
let refreshTimer

const selectedRate = computed(() => rates.value.find((item) => item.code === selectedCode.value)?.rate || 1)
const updatedDate = computed(() => rates.value[0]?.date || '')

function format(value, digits = 2) {
  return new Intl.NumberFormat(undefined, { maximumFractionDigits: digits }).format(value)
}

async function loadRates() {
  loading.value = true
  error.value = ''
  try {
    rates.value = await fetchOfficialCurrencyRates()
    if (!rates.value.some((item) => item.code === selectedCode.value)) selectedCode.value = 'USD'
  } catch (err) {
    rates.value = []
    error.value = err.message || tx.value.errFetch
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRates()
  refreshTimer = window.setInterval(loadRates, 60 * 60 * 1000)
})
onUnmounted(() => window.clearInterval(refreshTimer))
</script>

<template>
  <ToolShell icon="💱" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-6">
      <div class="flex flex-wrap items-end gap-4">
        <div class="flex-1 min-w-36">
          <label class="label">{{ tx.amount }}</label>
          <input v-model.number="amount" type="number" min="0" class="input" />
        </div>
        <div class="flex-1 min-w-44">
          <label class="label">{{ tx.baseCurrency }}</label>
          <select v-model="selectedCode" class="input" :disabled="!rates.length">
            <option v-for="item in rates" :key="item.code" :value="item.code">{{ item.code }} — {{ item.name }}</option>
          </select>
        </div>
      </div>

      <div class="text-xs text-slate-500 dark:text-slate-400">
        <span v-if="loading">{{ tx.loading }}</span>
        <span v-else-if="error" class="text-amber-600 dark:text-amber-400">{{ error }} {{ tx.errOldNotShown }}</span>
        <span v-else>{{ tx.source }} {{ updatedDate }}</span>
      </div>
      <button v-if="!loading" class="btn-secondary" @click="loadRates">{{ tx.refresh }}</button>

      <div v-if="error" class="flex gap-3">
        <button class="btn-secondary" @click="loadRates">{{ tx.retry }}</button>
        <a class="btn-secondary" href="https://cbu.uz/uz/arkhiv-kursov-valyut/" target="_blank" rel="noopener noreferrer">{{ tx.cbuArchive }}</a>
      </div>

      <div v-if="rates.length" class="divide-y divide-slate-100 dark:divide-slate-800">
        <div v-for="item in rates" :key="item.code" class="py-3 flex items-center justify-between gap-3">
          <div class="min-w-0">
            <p class="font-bold text-slate-800 dark:text-slate-100 text-sm">{{ item.code }} <span class="text-xs font-normal text-slate-400">({{ item.name }})</span></p>
            <p class="text-xs text-slate-500">1 {{ item.code }} = {{ format(item.rate, 4) }} {{ tx.currencySum }}</p>
          </div>
          <div class="text-right shrink-0">
            <p class="font-bold text-brand-600 dark:text-brand-400 text-sm">{{ format((Number(amount) || 0) * selectedRate / item.rate) }} {{ item.code }}</p>
            <span v-if="item.code !== 'UZS' && item.change !== 0" :class="item.change > 0 ? 'text-green-500' : 'text-red-500'" class="text-xs font-medium">{{ item.change > 0 ? '+' : '' }}{{ format(item.change, 4) }} {{ tx.currencySum }}</span>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
