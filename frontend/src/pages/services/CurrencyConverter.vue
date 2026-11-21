<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'
import { useI18n, language } from '../../i18n'
import { RefreshCw } from 'lucide-vue-next'
import { fetchOfficialCurrencyRates } from '../../api/currencyRates'

const { t } = useI18n()
const servicesStore = useServicesStore()
const rates = ref([])
const loadingRates = ref(true)
const rateError = ref('')
const rateDate = ref('')
const value = ref('')
const from = ref('USD')
const to = ref('UZS')
let refreshTimer

function getCurrencyName(item) {
  if (!item) return ''
  const lang = language.value
  return item[`name_${lang}`] || item.name || item.code
}

async function fetchRates() {
  loadingRates.value = true
  rateError.value = ''
  try {
    rates.value = await fetchOfficialCurrencyRates()
    if (!rates.value.some((item) => item.code === from.value)) from.value = 'USD'
    if (!rates.value.some((item) => item.code === to.value)) to.value = 'UZS'
    rateDate.value = rates.value[0]?.date || ''
  } catch (err) {
    rates.value = []
    rateDate.value = ''
    rateError.value = err.message || t('tool.valyuta-konvertori.rateError')
  } finally {
    loadingRates.value = false
  }
}

onMounted(() => {
  servicesStore.logUsage('valyuta-konvertori')
  fetchRates()
  // CBU publishes official rates daily; refresh periodically while this page stays open.
  refreshTimer = window.setInterval(fetchRates, 60 * 60 * 1000)
})
onUnmounted(() => window.clearInterval(refreshTimer))

const result = computed(() => {
  if (!rates.value.length || value.value === '') return null
  const amount = Number(value.value)
  const fromRate = rates.value.find((item) => item.code === from.value)?.rate
  const toRate = rates.value.find((item) => item.code === to.value)?.rate
  if (!Number.isFinite(amount) || !fromRate || !toRate) return null
  const converted = amount * fromRate / toRate
  return new Intl.NumberFormat('uz-UZ', { maximumFractionDigits: converted > 1000 ? 2 : 4 }).format(converted)
})

function reset() {
  value.value = ''
  from.value = 'USD'
  to.value = 'UZS'
}

function swap() {
  ;[from.value, to.value] = [to.value, from.value]
}
</script>

<template>
  <ToolShell slug="valyuta-konvertori" icon="💱" title="svc.valyuta-konvertori.name" description="svc.valyuta-konvertori.desc">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div class="flex items-center justify-between gap-3 px-4 py-2.5 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-800">
        <div class="text-xs font-medium">
          <span v-if="loadingRates" class="text-slate-500 flex items-center gap-1"><RefreshCw class="w-3.5 h-3.5 animate-spin" /> {{ t('tool.valyuta-konvertori.loading') }}</span>
          <span v-else-if="rateError" class="text-amber-600 dark:text-amber-400">{{ rateError }}</span>
          <span v-else class="text-green-600 dark:text-green-400">{{ t('tool.valyuta-konvertori.official') }}</span>
        </div>
        <div class="text-[10px] text-slate-400 text-right">{{ t('tool.valyuta-konvertori.date') }}<br><span class="font-bold">{{ rateDate || '—' }}</span></div>
      </div>

      <button class="btn-secondary w-full" @click="fetchRates">{{ rateError ? t('tool.valyuta-konvertori.retry') : t('tool.valyuta-konvertori.refresh') }}</button>

      <div>
        <label class="label">{{ t('tool.valyuta-konvertori.val') }}</label>
        <input v-model="value" type="number" min="0" class="input" placeholder="100" />
      </div>

      <div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-end">
        <div>
          <label class="label">{{ t('tool.valyuta-konvertori.from') }}</label>
          <select v-model="from" class="input" :disabled="!rates.length">
            <option v-for="item in rates" :key="item.code" :value="item.code">{{ getCurrencyName(item) }} ({{ item.code }})</option>
          </select>
        </div>
        <button class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-brand-600 flex items-center justify-center shrink-0 mb-0.5" @click="swap" :title="t('tool.valyuta-konvertori.swap')" :disabled="!rates.length">
          <RefreshCw class="w-4 h-4" />
        </button>
        <div>
          <label class="label">{{ t('tool.valyuta-konvertori.to') }}</label>
          <select v-model="to" class="input" :disabled="!rates.length">
            <option v-for="item in rates" :key="item.code" :value="item.code">{{ getCurrencyName(item) }} ({{ item.code }})</option>
          </select>
        </div>
      </div>

      <button class="btn-secondary w-full" @click="reset">{{ t('common.clear') }}</button>

      <div v-if="result !== null" class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4">
        <p class="text-xs font-medium text-brand-600 dark:text-brand-300 uppercase tracking-wide">{{ t('common.result') }} ({{ to }})</p>
        <p class="text-2xl font-extrabold text-brand-800 dark:text-brand-200 mt-1 break-words">{{ value }} {{ from }} = {{ result }} {{ to }}</p>
      </div>
    </div>
  </ToolShell>
</template>
