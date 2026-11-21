<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { useI18n, language } from '../../i18n'

const { t } = useI18n()
const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('ogirlik-konvertori'))

// base unit: grams
const UNITS_DATA = {
  mg: {
    factor: 0.001,
    uz: 'Milligramm (mg)',
    ru: 'Миллиграмм (мг)',
    en: 'Milligram (mg)',
  },
  g: {
    factor: 1,
    uz: 'Gramm (g)',
    ru: 'Грамм (г)',
    en: 'Gram (g)',
  },
  kg: {
    factor: 1000,
    uz: 'Kilogramm (kg)',
    ru: 'Килограмм (кг)',
    en: 'Kilogram (kg)',
  },
  ton: {
    factor: 1000000,
    uz: 'Tonna (t)',
    ru: 'Тонна (т)',
    en: 'Ton (t)',
  },
  lb: {
    factor: 453.59237,
    uz: 'Funt (lb)',
    ru: 'Фунт (lb)',
    en: 'Pound (lb)',
  },
  oz: {
    factor: 28.349523125,
    uz: 'Untsiya (oz)',
    ru: 'Унция (oz)',
    en: 'Ounce (oz)',
  },
}

const units = computed(() => {
  const lang = ['uz', 'ru', 'en'].includes(language.value) ? language.value : 'uz'
  const res = {}
  for (const [key, item] of Object.entries(UNITS_DATA)) {
    res[key] = {
      label: item[lang] || item.uz,
      factor: item.factor,
    }
  }
  return res
})

const value = ref('')
const from = ref('kg')
const to = ref('lb')
const error = ref('')

const result = computed(() => {
  error.value = ''
  if (value.value === '') return null
  const num = parseFloat(value.value)
  if (!Number.isFinite(num) || num < 0) {
    error.value = t('tool.ogirlik-konvertori.error')
    return null
  }
  const grams = num * units.value[from.value].factor
  const converted = grams / units.value[to.value].factor
  return Math.round(converted * 1e6) / 1e6
})

function reset() {
  value.value = ''
  from.value = 'kg'
  to.value = 'lb'
  error.value = ''
}

function swap() {
  ;[from.value, to.value] = [to.value, from.value]
}
</script>

<template>
  <ToolShell slug="ogirlik-konvertori" icon="⚖️" title="svc.ogirlik-konvertori.name" description="svc.ogirlik-konvertori.desc">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">{{ t('tool.ogirlik-konvertori.val') }}</label>
        <input v-model="value" type="number" class="input" placeholder="70" />
      </div>

      <div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-end">
        <div>
          <label class="label">{{ t('tool.ogirlik-konvertori.from') }}</label>
          <select v-model="from" class="input">
            <option v-for="(u, key) in units" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
        <button class="btn-secondary !px-3 !py-2.5 mb-0.5" @click="swap" :title="t('tool.ogirlik-konvertori.swap')">⇄</button>
        <div>
          <label class="label">{{ t('tool.ogirlik-konvertori.to') }}</label>
          <select v-model="to" class="input">
            <option v-for="(u, key) in units" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
      </div>

      <button class="btn-secondary w-full" @click="reset">{{ t('common.clear') }}</button>

      <transition name="page-fade">
        <div v-if="result !== null" class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop">
          <p class="text-xs font-medium text-brand-600 dark:text-brand-300 uppercase tracking-wide">{{ t('common.result') }}</p>
          <p class="text-2xl font-extrabold text-brand-800 dark:text-brand-200 mt-1 break-words">
            {{ value }} {{ units[from]?.label.split(' ')[0] }} = {{ result }} {{ units[to]?.label.split(' ')[0] }}
          </p>
        </div>
      </transition>
    </div>
  </ToolShell>

</template>
