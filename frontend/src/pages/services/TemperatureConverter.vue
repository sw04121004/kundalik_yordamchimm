<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { useI18n } from '../../i18n'

const { t } = useI18n()
const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('harorat-konvertori'))

const units = {
  c: 'Selsiy (°C)',
  f: 'Farengeyt (°F)',
  k: 'Kelvin (K)',
}

const value = ref('')
const from = ref('c')
const to = ref('f')
const error = ref('')

function toCelsius(val, unit) {
  if (unit === 'c') return val
  if (unit === 'f') return ((val - 32) * 5) / 9
  if (unit === 'k') return val - 273.15
}

function fromCelsius(celsius, unit) {
  if (unit === 'c') return celsius
  if (unit === 'f') return (celsius * 9) / 5 + 32
  if (unit === 'k') return celsius + 273.15
}

const result = computed(() => {
  error.value = ''
  if (value.value === '') return null
  const num = parseFloat(value.value)
  if (!Number.isFinite(num)) {
    error.value = t('tool.harorat-konvertori.errorValid')
    return null
  }
  const celsius = toCelsius(num, from.value)
  if (celsius < -273.15) {
    error.value = t('tool.harorat-konvertori.errorZero')
    return null
  }
  const converted = fromCelsius(celsius, to.value)
  return Math.round(converted * 100) / 100
})

function reset() {
  value.value = ''
  from.value = 'c'
  to.value = 'f'
  error.value = ''
}

function swap() {
  ;[from.value, to.value] = [to.value, from.value]
}
</script>

<template>
  <ToolShell slug="harorat-konvertori" icon="🌡️" title="svc.harorat-konvertori.name" description="svc.harorat-konvertori.desc">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">{{ t('tool.harorat-konvertori.val') }}</label>
        <input v-model="value" type="number" class="input" placeholder="36.6" />
      </div>

      <div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-end">
        <div>
          <label class="label">{{ t('tool.harorat-konvertori.from') }}</label>
          <select v-model="from" class="input">
            <option v-for="(label, key) in units" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>
        <button class="btn-secondary !px-3 !py-2.5 mb-0.5" @click="swap" :title="t('tool.harorat-konvertori.swap')">⇄</button>
        <div>
          <label class="label">{{ t('tool.harorat-konvertori.to') }}</label>
          <select v-model="to" class="input">
            <option v-for="(label, key) in units" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>
      </div>

      <button class="btn-secondary w-full" @click="reset">{{ t('common.clear') }}</button>

      <transition name="page-fade">
        <div v-if="result !== null" class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop">
          <p class="text-xs font-medium text-brand-600 uppercase tracking-wide">{{ t('common.result') }}</p>
          <p class="text-2xl font-extrabold text-brand-800 mt-1 break-words">
            {{ value }}° {{ from.toUpperCase() }} = {{ result }}° {{ to.toUpperCase() }}
          </p>
        </div>
      </transition>
    </div>
  </ToolShell>

</template>
