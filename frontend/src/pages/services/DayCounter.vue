<script setup>
import { ref, watch, onMounted } from 'vue'
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

  if (!baseDate.value && days.value === '') return
  if (!baseDate.value || days.value === '') return

  const n = Number(days.value)
  if (!Number.isSafeInteger(n) || n < 0) {
    error.value = 'Iltimos, nol yoki undan katta butun son kiriting.'
    return
  }

  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(baseDate.value)
  if (!match) {
    error.value = 'Sana formati noto‘g‘ri.'
    return
  }
  const [, year, month, day] = match
  const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)))
  if (date.getUTCFullYear() !== Number(year) || date.getUTCMonth() !== Number(month) - 1 || date.getUTCDate() !== Number(day)) {
    error.value = 'Kiritilgan sana mavjud emas.'
    return
  }

  const delta = mode.value === 'add' ? n : -n
  date.setUTCDate(date.getUTCDate() + delta)
  if (!Number.isFinite(date.getTime())) {
    error.value = 'Hisoblangan sana ruxsat etilgan oraliqdan tashqarida.'
    return
  }

  // Brauzerning o'zbekcha locale qo'llab-quvvatlashiga tayanmasdan qo'lda formatlaymiz
  const formatted = `${date.getUTCDate()}-${UZ_MONTHS[date.getUTCMonth()]} ${date.getUTCFullYear()}`
  const weekday = weekdays[date.getUTCDay()]
  result.value = `${formatted}, ${weekday}`
}

watch([baseDate, days, mode], calculate)

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

      <button class="btn-secondary w-full" @click="reset">Tozalash</button>

      <ResultBox label="Yangi sana" :value="result" />
    </div>
  </ToolShell>

</template>
