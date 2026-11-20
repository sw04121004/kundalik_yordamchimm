<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import ResultBox from '../../components/ResultBox.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { useI18n } from '../../i18n'

const { t } = useI18n()
const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('foiz-hisoblagich'))

const number = ref('')
const percent = ref('')
const result = ref(null)
const error = ref('')

function calculate() {
  error.value = ''
  result.value = null

  if (number.value === '' && percent.value === '') return
  if (number.value === '' || percent.value === '') return

  const n = parseFloat(number.value)
  const p = parseFloat(percent.value)

  if (!Number.isFinite(n) || !Number.isFinite(p)) {
    error.value = t('tool.foiz-hisoblagich.errorNumeric')
    return
  }
  if (p < 0) {
    error.value = t('tool.foiz-hisoblagich.errorPercent')
    return
  }

  const value = (n * p) / 100
  if (!Number.isFinite(value)) {
    error.value = t('tool.oddiy-kalkulyator.errorOverflow')
    return
  }
  result.value = `${n} × ${p}% = ${round(value)}`
}

watch([number, percent], calculate)

function round(num) {
  return Math.round(num * 10000) / 10000
}

function reset() {
  number.value = ''
  percent.value = ''
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell slug="foiz-hisoblagich" icon="🧮" title="svc.foiz-hisoblagich.name" description="svc.foiz-hisoblagich.desc">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">{{ t('tool.foiz-hisoblagich.number') }}</label>
        <input v-model="number" type="number" class="input" placeholder="250" />
      </div>
      <div>
        <label class="label">{{ t('tool.foiz-hisoblagich.percent') }}</label>
        <input v-model="percent" type="number" class="input" placeholder="15" />
      </div>

      <button class="btn-secondary w-full" @click="reset">{{ t('common.clear') }}</button>

      <ResultBox :value="result" />
    </div>
  </ToolShell>

</template>
