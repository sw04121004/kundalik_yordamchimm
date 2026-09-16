<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import ResultBox from '../../components/ResultBox.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('oddiy-kalkulyator'))

const a = ref('')
const b = ref('')
const operation = ref('+')
const result = ref(null)
const error = ref('')

const operations = [
  { value: '+', label: '+' },
  { value: '-', label: '−' },
  { value: '*', label: '×' },
  { value: '/', label: '÷' },
]

function calculate() {
  error.value = ''
  result.value = null

  const x = parseFloat(a.value)
  const y = parseFloat(b.value)

  if (a.value === '' || b.value === '') {
    error.value = 'Iltimos, ikkala sonni ham kiriting.'
    return
  }
  if (Number.isNaN(x) || Number.isNaN(y)) {
    error.value = 'Iltimos, faqat raqam kiriting.'
    return
  }

  let value
  switch (operation.value) {
    case '+':
      value = x + y
      break
    case '-':
      value = x - y
      break
    case '*':
      value = x * y
      break
    case '/':
      if (y === 0) {
        error.value = 'Nolga bo‘lish mumkin emas.'
        return
      }
      value = x / y
      break
  }
  result.value = Math.round(value * 100000) / 100000
}

function reset() {
  a.value = ''
  b.value = ''
  operation.value = '+'
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell icon="➗" title="Oddiy kalkulyator" description="Qo‘shish, ayirish, ko‘paytirish, bo‘lish" hint="Ikkita sonni kiriting, amalni tanlang (+, −, ×, ÷) va «Hisoblash»ni bosing.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div class="grid grid-cols-3 gap-3 items-end">
        <div class="col-span-1">
          <label class="label">1-son</label>
          <input v-model="a" type="number" class="input" placeholder="0" @keyup.enter="calculate" />
        </div>
        <div class="col-span-1">
          <label class="label">Amal</label>
          <select v-model="operation" class="input">
            <option v-for="op in operations" :key="op.value" :value="op.value">{{ op.label }}</option>
          </select>
        </div>
        <div class="col-span-1">
          <label class="label">2-son</label>
          <input v-model="b" type="number" class="input" placeholder="0" @keyup.enter="calculate" />
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <ResultBox :value="result" />
    </div>
  </ToolShell>

</template>
