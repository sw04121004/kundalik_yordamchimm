<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import ResultBox from '../../components/ResultBox.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

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

  if (number.value === '' || percent.value === '') {
    error.value = 'Iltimos, ikkala maydonni ham to‘ldiring.'
    return
  }
  if (!Number.isFinite(n) || !Number.isFinite(p)) {
    error.value = 'Iltimos, faqat raqam kiriting.'
    return
  }

  const value = (n * p) / 100
  if (!Number.isFinite(value)) {
    error.value = 'Natija son chegarasidan oshib ketdi.'
    return
  }
  result.value = `${n} sonining ${p}% i = ${round(value)}`
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
  <ToolShell icon="🧮" title="Foiz hisoblagich" description="Sondan foizni tez va aniq hisoblang" hint="Son va foizni kiriting — natija darhol hisoblanadi.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Son</label>
        <input v-model="number" type="number" class="input" placeholder="masalan: 250" />
      </div>
      <div>
        <label class="label">Foiz (%)</label>
        <input v-model="percent" type="number" class="input" placeholder="masalan: 15" />
      </div>

      <button class="btn-secondary w-full" @click="reset">Tozalash</button>

      <ResultBox :value="result" />
    </div>
  </ToolShell>

</template>
