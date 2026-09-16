<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const rates = ref([
  { code: 'USD', name: 'AQSH Dollari', rate: 12850, flag: '🇺🇸', change: '+15.00' },
  { code: 'EUR', name: 'Yevro', rate: 13950, flag: '🇪🇺', change: '-20.00' },
  { code: 'RUB', name: 'Rossiya Rubli', rate: 138, flag: '🇷🇺', change: '+0.50' },
  { code: 'KZT', name: 'Qozog\'iston Tengesi', rate: 26.5, flag: '🇰🇿', change: '+0.10' },
  { code: 'TRY', name: 'Turk Lirasi', rate: 375, flag: '🇹🇷', change: '-1.20' },
  { code: 'CNY', name: 'Xitoy Yuani', rate: 1770, flag: '🇨🇳', change: '+2.00' },
])

const amount = ref(100)
const selectedCode = ref('USD')

function getConverted(rate) {
  return ((amount.value || 0) * rate).toLocaleString('uz-UZ')
}
</script>

<template>
  <ToolShell icon="💱" title="Valyuta kurslari" description="Markaziy bank va asosiy valyutalar bo'yicha jonli kurslar" hint="Valyuta miqdorini kiriting va boshqa valyutalardagi qiymatini tezkor ko'ring.">
    <template #header><AppHeader /></template>

    <div class="space-y-6">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Miqdor</label>
          <input v-model.number="amount" type="number" class="input" min="1" />
        </div>
        <div>
          <label class="label">Asosiy valyuta</label>
          <select v-model="selectedCode" class="input">
            <option v-for="c in rates" :key="c.code" :value="c.code">{{ c.flag }} {{ c.code }} - {{ c.name }}</option>
          </select>
        </div>
      </div>

      <div class="divide-y divide-slate-100 dark:divide-slate-800">
        <div v-for="item in rates" :key="item.code" class="py-3 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-2xl">{{ item.flag }}</span>
            <div>
              <p class="font-bold text-slate-800 dark:text-slate-100 text-sm">{{ item.code }} <span class="text-xs font-normal text-slate-400">({{ item.name }})</span></p>
              <p class="text-xs text-slate-500">1 {{ item.code }} = {{ item.rate.toLocaleString('uz-UZ') }} so'm</p>
            </div>
          </div>
          <div class="text-right">
            <p class="font-bold text-brand-600 dark:text-brand-400 text-sm">{{ ((amount || 0) * (item.rate / (rates.find(r => r.code === selectedCode)?.rate || 1))).toFixed(2) }} {{ item.code }}</p>
            <span :class="item.change.startsWith('+') ? 'text-green-500' : 'text-red-500'" class="text-xs font-medium">{{ item.change }}</span>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
