<script setup>
import { ref, watch, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('sana-farqi'))

const startDate = ref('')
const endDate = ref('')
const excludeWeekends = ref(false)
const error = ref('')
const result = ref(null)
const DAY_MS = 24 * 60 * 60 * 1000

function utcDate(year, month, day) {
  const date = new Date(0)
  date.setUTCHours(0, 0, 0, 0)
  date.setUTCFullYear(year, month, day)
  return date
}

function parseDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return null
  const parts = value.split('-').map(Number)
  if (parts.length !== 3 || parts.some((part) => !Number.isInteger(part))) return null
  const [year, month, day] = parts
  const date = utcDate(year, month - 1, day)
  if (date.getUTCFullYear() !== year || date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) return null
  return date
}

function addMonthsClamped(date, monthCount) {
  const totalMonths = date.getUTCFullYear() * 12 + date.getUTCMonth() + monthCount
  const year = Math.floor(totalMonths / 12)
  const month = totalMonths - year * 12
  const lastDay = utcDate(year, month + 1, 0).getUTCDate()
  return utcDate(year, month, Math.min(date.getUTCDate(), lastDay))
}

function calendarParts(start, end) {
  let totalMonths = (end.getUTCFullYear() - start.getUTCFullYear()) * 12 + end.getUTCMonth() - start.getUTCMonth()
  let cursor = addMonthsClamped(start, totalMonths)
  if (cursor > end) {
    totalMonths--
    cursor = addMonthsClamped(start, totalMonths)
  }
  const years = Math.floor(totalMonths / 12)
  const months = totalMonths % 12

  const days = (end.getTime() - cursor.getTime()) / DAY_MS
  return `${years} yil, ${months} oy, ${days} kun`
}

function calculate() {
  error.value = ''
  result.value = null

  if (!startDate.value && !endDate.value) return
  if (!startDate.value || !endDate.value) return

  if (!startDate.value || !endDate.value) {
    error.value = 'Iltimos, ikkala sanani ham tanlang.'
    return
  }

  const start = parseDate(startDate.value)
  const end = parseDate(endDate.value)
  if (!start || !end) {
    error.value = 'Kiritilgan sanalardan biri yaroqsiz.'
    return
  }
  if (start > end) {
    error.value = 'Boshlanish sanasi tugash sanasidan keyin bo‘lmasligi kerak.'
    return
  }

  const calendarDays = (end.getTime() - start.getTime()) / DAY_MS
  const daysInclusive = calendarDays + 1
  let countedDays = daysInclusive
  if (excludeWeekends.value) {
    const fullWeeks = Math.floor(daysInclusive / 7)
    countedDays = fullWeeks * 5
    const remainingDays = daysInclusive % 7
    for (let offset = 0; offset < remainingDays; offset++) {
      const weekday = (start.getUTCDay() + offset) % 7
      if (weekday !== 0 && weekday !== 6) countedDays++
    }
  }

  result.value = {
    calendarDays,
    countedDays,
    countedDaysLabel: excludeWeekends.value ? 'Ish kunlari (shanba-yakshanba chiqarilgan)' : 'Oraliqdagi barcha sanalar',
    calendarParts: calendarParts(start, end),
  }
}

watch([startDate, endDate, excludeWeekends], calculate)

function reset() {
  startDate.value = ''
  endDate.value = ''
  excludeWeekends.value = false
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell
    icon="📅"
    title="Sana farqi"
    description="Ikki sana orasidagi kalendar va ish kunlarini hisoblang"
    hint="Kalendar farqi — sanalar orasidagi o‘tgan kunlar. Oraliqdagi kunlar sonida boshlanish va tugash sanalari ham qo‘shiladi. Faqat shanba-yakshanbani chiqarish mumkin; rasmiy bayramlar alohida tekshirilmaydi."
  >
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="label">Boshlanish sanasi</label>
          <input v-model="startDate" type="date" class="input" />
        </div>
        <div>
          <label class="label">Tugash sanasi</label>
          <input v-model="endDate" type="date" class="input" />
        </div>
      </div>

      <label class="flex items-center gap-2 cursor-pointer pt-2">
        <input v-model="excludeWeekends" type="checkbox" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500 border-slate-300 dark:border-slate-600 dark:bg-slate-700">
        <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Ish kunlarini sanash (shanba-yakshanbani chiqarish)</span>
      </label>

      <button class="btn-secondary w-full" @click="reset">Tozalash</button>

      <transition name="page-fade">
        <div v-if="result" class="mt-5 grid grid-cols-1 sm:grid-cols-2 gap-3 animate-resultPop">
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Kalendar farqi</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ result.calendarDays }} kun</p>
          </div>
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">{{ result.countedDaysLabel }}</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ result.countedDays }} kun</p>
          </div>
          <div class="sm:col-span-2 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 text-center animate-resultPop">
            <p class="text-xs font-medium text-brand-600 uppercase tracking-wide">Yil, oy va kun hisobida</p>
            <p class="text-xl font-extrabold text-brand-800 mt-1">{{ result.calendarParts }}</p>
          </div>
        </div>
      </transition>
    </div>
  </ToolShell>
</template>
