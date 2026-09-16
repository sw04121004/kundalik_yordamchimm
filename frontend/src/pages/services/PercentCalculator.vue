<script setup>
import { ref, computed, onMounted } from 'vue'
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

  const n = parseFloat(number.value)
  const p = parseFloat(percent.value)

  if (number.value === '' || percent.value === '') {
    error.value = 'Iltimos, ikkala maydonni ham to‘ldiring.'
    return
  }
  if (Number.isNaN(n) || Number.isNaN(p)) {
    error.value = 'Iltimos, faqat raqam kiriting.'
    return
  }

  const value = (n * p) / 100
  result.value = `${n} sonining ${p}% i = ${round(value)}`
}

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
  <ToolShell icon="🧮" title="Foiz hisoblagich" description="Sondan foizni tez va aniq hisoblang" hint="Son va foiz qiymatini kiriting, «Hisoblash»ni bosing — natija pastda chiqadi.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Son</label>
        <input v-model="number" type="number" class="input" placeholder="masalan: 250" @keyup.enter="calculate" />
      </div>
      <div>
        <label class="label">Foiz (%)</label>
        <input v-model="percent" type="number" class="input" placeholder="masalan: 15" @keyup.enter="calculate" />
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <ResultBox :value="result" />
    </div>
  </ToolShell>

</template>
