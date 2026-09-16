<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import ResultBox from '../../components/ResultBox.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('kun-hisoblagich'))

const baseDate = ref('')
const days = ref('')
const mode = ref('add') // add | subtract
const error = ref('')
const result = ref(null)

const weekdays = ['Yakshanba', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba']
const UZ_MONTHS = [
  'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
  'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr',
]

function calculate() {
  error.value = ''
  result.value = null

  if (!baseDate.value || days.value === '') {
    error.value = 'Iltimos, sana va kunlar sonini kiriting.'
    return
  }

  const n = parseInt(days.value, 10)
  if (Number.isNaN(n) || n < 0) {
    error.value = 'Iltimos, musbat butun son kiriting.'
    return
  }

  const date = new Date(baseDate.value)
  if (Number.isNaN(date.getTime())) {
    error.value = 'Sana formati noto‘g‘ri.'
    return
  }

  const delta = mode.value === 'add' ? n : -n
  date.setDate(date.getDate() + delta)

  // Brauzerning o'zbekcha locale qo'llab-quvvatlashiga tayanmasdan qo'lda formatlaymiz
  const formatted = `${date.getDate()}-${UZ_MONTHS[date.getMonth()]} ${date.getFullYear()}`
  const weekday = weekdays[date.getDay()]
  result.value = `${formatted}, ${weekday}`
}

function reset() {
  baseDate.value = ''
  days.value = ''
  mode.value = 'add'
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell icon="⏱️" title="Kun hisoblagich" description="Sanaga kun qo‘shing yoki ayiring" hint="Boshlang‘ich sanani tanlang, necha kun qo‘shish yoki ayirishni kiriting — yangi sana darhol hisoblanadi.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Boshlang‘ich sana</label>
        <input v-model="baseDate" type="date" class="input" />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Amal</label>
          <select v-model="mode" class="input">
            <option value="add">Qo‘shish (+)</option>
            <option value="subtract">Ayirish (−)</option>
          </select>
        </div>
        <div>
          <label class="label">Kunlar soni</label>
          <input v-model="days" type="number" min="0" class="input" placeholder="masalan: 30" />
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <ResultBox label="Yangi sana" :value="result" />
    </div>
  </ToolShell>

</template>
