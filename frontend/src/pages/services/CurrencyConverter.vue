<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { RefreshCw } from 'lucide-vue-next'

const servicesStore = useServicesStore()

// Boshlang'ich (offline) kurslar - agar internet yoki API ishlamay qolsa
const RATES_TO_USD = reactive({
  USD: { label: 'AQSH dollari (USD)', rate: 1 },
  UZS: { label: "O'zbek so'mi (UZS)", rate: 1 / 12700 },
  EUR: { label: 'Yevro (EUR)', rate: 1.08 },
  RUB: { label: 'Rossiya rubli (RUB)', rate: 1 / 92 },
  GBP: { label: 'Angliya funti (GBP)', rate: 1.27 },
  KZT: { label: 'Qozog\u2019iston tengesi (KZT)', rate: 1 / 480 },
  TRY: { label: 'Turk lirasi (TRY)', rate: 1 / 34 },
  CNY: { label: 'Xitoy yuani (CNY)', rate: 1 / 7.2 },
})

const loadingRates = ref(true)
const apiError = ref(false)
const lastUpdated = ref('Yuklanmoqda...')

async function fetchRates() {
  loadingRates.value = true
  apiError.value = false
  try {
    const res = await fetch('https://api.exchangerate-api.com/v4/latest/USD')
    if (!res.ok) throw new Error('API xatosi')
    const data = await res.json()
    
    if (data && data.rates) {
      // Yangi real kurslarni o'zlashtiramiz (1 USD ga nisbatan)
      // Bizning formula "1 birlik valyuta = X USD"
      Object.keys(RATES_TO_USD).forEach(currency => {
        if (currency !== 'USD' && data.rates[currency]) {
          RATES_TO_USD[currency].rate = 1 / data.rates[currency]
        }
      })
      
      const date = new Date(data.time_last_updated * 1000)
      lastUpdated.value = date.toLocaleString('uz-UZ', { 
        year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
      })
    }
  } catch (err) {
    console.error('Kurslarni yuklashda xatolik:', err)
    apiError.value = true
    lastUpdated.value = 'Oflayn (Eski kurslar)'
  } finally {
    loadingRates.value = false
  }
}

onMounted(() => {
  servicesStore.logUsage('valyuta-konvertori')
  fetchRates()
})

const value = ref('')
const from = ref('USD')
const to = ref('UZS')
const error = ref('')

const result = computed(() => {
  error.value = ''
  if (value.value === '') return null
  const num = parseFloat(value.value)
  if (Number.isNaN(num)) {
    error.value = 'Iltimos, faqat raqam kiriting.'
    return null
  }
  const usd = num * RATES_TO_USD[from.value].rate
  const converted = usd / RATES_TO_USD[to.value].rate
  
  // Formatlash - agar summa katta bo'lsa butun, kichik bo'lsa tiyinlari bilan
  if (converted > 1000) {
    return new Intl.NumberFormat('uz-UZ', { maximumFractionDigits: 2 }).format(converted)
  }
  return new Intl.NumberFormat('uz-UZ', { maximumFractionDigits: 4 }).format(converted)
})

function reset() {
  value.value = ''
  from.value = 'USD'
  to.value = 'UZS'
  error.value = ''
}

function swap() {
  const temp = from.value
  from.value = to.value
  to.value = temp
}
</script>

<template>
  <ToolShell
    icon="💱"
    title="Valyuta konvertori"
    description="So'm, dollar, yevro va boshqa valyutalar o'rtasida konvertatsiya"
    hint="Qiymatni kiriting, valyutalarni tanlang — natija real vaqt rejimidagi bozor kursi asosida hisoblanadi."
  >
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <!-- Status Bar -->
      <div class="flex items-center justify-between px-4 py-2.5 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-2 text-xs font-medium">
          <span v-if="loadingRates" class="text-slate-500 flex items-center gap-1">
            <RefreshCw class="w-3.5 h-3.5 animate-spin" /> Yangilanmoqda...
          </span>
          <span v-else-if="apiError" class="text-amber-600 dark:text-amber-400">
            ⚠️ Oflayn kurslar
          </span>
          <span v-else class="text-green-600 dark:text-green-400 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Real vaqt kursi
          </span>
        </div>
        <div class="text-[10px] text-slate-400 text-right">
          Oxirgi yangilanish:<br/> <span class="font-bold">{{ lastUpdated }}</span>
        </div>
      </div>

      <div>
        <label class="label">Qiymat</label>
        <input v-model="value" type="number" class="input" placeholder="masalan: 100" />
      </div>

      <div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-end">
        <div>
          <label class="label">Dan</label>
          <select v-model="from" class="input">
            <option v-for="(u, key) in RATES_TO_USD" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
        <button class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 hover:bg-brand-50 dark:hover:bg-brand-900/30 transition-all flex items-center justify-center shrink-0 mb-0.5" @click="swap" title="Almashtirish">
          <RefreshCw class="w-4 h-4" />
        </button>
        <div>
          <label class="label">Ga</label>
          <select v-model="to" class="input">
            <option v-for="(u, key) in RATES_TO_USD" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
      </div>

      <button class="btn-secondary w-full" @click="reset">Tozalash</button>

      <transition name="page-fade">
        <div v-if="result !== null" class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop relative overflow-hidden">
          <div class="absolute right-0 top-0 bottom-0 opacity-10 flex items-center justify-center text-7xl font-black pointer-events-none -mr-4 select-none">
            {{ to === 'UZS' ? 'SUM' : to }}
          </div>
          <div class="relative z-10">
            <p class="text-xs font-medium text-brand-600 dark:text-brand-300 uppercase tracking-wide">Natija ({{ to }})</p>
            <p class="text-2xl font-extrabold text-brand-800 dark:text-brand-200 mt-1 break-words">
              <span class="text-sm font-semibold opacity-70 mr-1">{{ value }} {{ from }} =</span>
              <br/>
              {{ result }} {{ to }}
            </p>
          </div>
        </div>
      </transition>
    </div>
  </ToolShell>
</template>
