<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { fetchOfficialCurrencyRates } from '../../api/currencyRates'

const rates = ref([])
const amount = ref(100)
const selectedCode = ref('USD')
const loading = ref(true)
const error = ref('')
let refreshTimer

const selectedRate = computed(() => rates.value.find((item) => item.code === selectedCode.value)?.rate || 1)
const updatedDate = computed(() => rates.value[0]?.date || '')

function format(value, digits = 2) {
  return new Intl.NumberFormat('uz-UZ', { maximumFractionDigits: digits }).format(value)
}

async function loadRates() {
  loading.value = true
  error.value = ''
  try {
    rates.value = await fetchOfficialCurrencyRates()
    if (!rates.value.some((item) => item.code === selectedCode.value)) selectedCode.value = 'USD'
  } catch (err) {
    rates.value = []
    error.value = err.message || 'Kurslarni hozir olib bo‘lmadi.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRates()
  // CBU publishes official rates daily; refresh periodically while this page stays open.
  refreshTimer = window.setInterval(loadRates, 60 * 60 * 1000)
})
onUnmounted(() => window.clearInterval(refreshTimer))
</script>

<template>
  <ToolShell icon="💱" title="Valyuta kurslari" description="O‘zbekiston Markaziy bankining rasmiy kurslari" hint="Rasmiy kurslar kunlik e’lon qilinadi; ular bankdagi sotib olish yoki sotish narxidan farq qilishi mumkin.">
    <template #header><AppHeader /></template>

    <div class="space-y-6">
      <div class="flex flex-wrap items-end gap-4">
        <div class="flex-1 min-w-36">
          <label class="label">Miqdor</label>
          <input v-model.number="amount" type="number" min="0" class="input" />
        </div>
        <div class="flex-1 min-w-44">
          <label class="label">Asosiy valyuta</label>
          <select v-model="selectedCode" class="input" :disabled="!rates.length">
            <option v-for="item in rates" :key="item.code" :value="item.code">{{ item.code }} — {{ item.name }}</option>
          </select>
        </div>
      </div>

      <div class="text-xs text-slate-500 dark:text-slate-400">
        <span v-if="loading">Markaziy bank kurslari olinmoqda…</span>
        <span v-else-if="error" class="text-amber-600 dark:text-amber-400">{{ error }} Eski kurslar ko‘rsatilmaydi.</span>
        <span v-else>Manba: O‘zbekiston Respublikasi Markaziy banki · amal qilish sanasi: {{ updatedDate }}</span>
      </div>
      <button v-if="!loading" class="btn-secondary" @click="loadRates">Kursni yangilash</button>

      <div v-if="error" class="flex gap-3">
        <button class="btn-secondary" @click="loadRates">Qayta urinish</button>
        <a class="btn-secondary" href="https://cbu.uz/uz/arkhiv-kursov-valyut/" target="_blank" rel="noopener noreferrer">Markaziy bank kurslari</a>
      </div>

      <div v-if="rates.length" class="divide-y divide-slate-100 dark:divide-slate-800">
        <div v-for="item in rates" :key="item.code" class="py-3 flex items-center justify-between gap-3">
          <div class="min-w-0">
            <p class="font-bold text-slate-800 dark:text-slate-100 text-sm">{{ item.code }} <span class="text-xs font-normal text-slate-400">({{ item.name }})</span></p>
            <p class="text-xs text-slate-500">1 {{ item.code }} = {{ format(item.rate, 4) }} so‘m</p>
          </div>
          <div class="text-right shrink-0">
            <p class="font-bold text-brand-600 dark:text-brand-400 text-sm">{{ format((Number(amount) || 0) * selectedRate / item.rate) }} {{ item.code }}</p>
            <span v-if="item.code !== 'UZS' && item.change !== 0" :class="item.change > 0 ? 'text-green-500' : 'text-red-500'" class="text-xs font-medium">{{ item.change > 0 ? '+' : '' }}{{ format(item.change, 4) }} so‘m</span>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
