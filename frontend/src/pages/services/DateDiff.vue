<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('sana-farqi'))

const startDate = ref('')
const endDate = ref('')
const excludeWeekends = ref(false)
const excludeHolidays = ref(false)
const error = ref('')
const result = ref(null)

const UZ_HOLIDAYS = [
  '01-01', // Yangi yil
  '03-08', // Xotin-qizlar kuni
  '03-21', // Navro'z
  '05-09', // Xotira va qadrlash
  '09-01', // Mustaqillik
  '10-01', // O'qituvchilar
  '12-08', // Konstitutsiya
]

function calculate() {
  error.value = ''
  result.value = null

  if (!startDate.value || !endDate.value) {
    error.value = 'Iltimos, ikkala sanani ham tanlang.'
    return
  }

  const start = new Date(startDate.value)
  const end = new Date(endDate.value)

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    error.value = 'Sana formati noto??g??ri.'
    return
  }
  
  if (start > end) {
    error.value = 'Boshlanish sanasi tugash sanasidan kichik bo\'lishi kerak.'
    return
  }

  let totalDays = 0;
  let workDays = 0;
  let holidayCount = 0;
  
  const current = new Date(start)
  
  while (current <= end) {
    totalDays++;
    const dayOfWeek = current.getDay();
    const mm = String(current.getMonth() + 1).padStart(2, '0');
    const dd = String(current.getDate()).padStart(2, '0');
    const mmdd = `${mm}-${dd}`;
    
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    const isHoliday = UZ_HOLIDAYS.includes(mmdd);
    
    if (isHoliday) holidayCount++;
    
    let shouldCount = true;
    if (excludeWeekends.value && isWeekend) shouldCount = false;
    if (excludeHolidays.value && isHoliday) shouldCount = false;
    
    if (shouldCount) {
      workDays++;
    }
    
    current.setDate(current.getDate() + 1);
  }

  // To count absolute difference excluding first day if we want mathematical diff, 
  // but usually for work days people include boundaries. Let's do absolute days minus 1 for total
  // to match standard Math.abs(end - start)
  const diffMs = Math.abs(end - start)
  const mathDays = Math.round(diffMs / (1000 * 60 * 60 * 24))

  const years = Math.floor(mathDays / 365)
  const remainderAfterYears = mathDays % 365
  const months = Math.floor(remainderAfterYears / 30)
  const days = remainderAfterYears % 30

  result.value = {
    mathDays,
    calculatedDays: workDays,
    holidays: holidayCount,
    weeks: Math.floor(mathDays / 7),
    approx: `${years} yil, ${months} oy, ${days} kun (taxminan)`,
  }
}

function reset() {
  startDate.value = ''
  endDate.value = ''
  excludeWeekends.value = false
  excludeHolidays.value = false
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell icon="📅" title="Sana farqi" description="Ikki sana orasidagi farqni hisoblang" hint="Kunlar va ish kunlarini hisoblash uchun qo'shimcha parametrlardan foydalanishingiz mumkin.">
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
      
      <div class="flex flex-col gap-2 pt-2">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="excludeWeekends" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500 border-slate-300 dark:border-slate-600 dark:bg-slate-700">
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Shanba va Yakshanbani hisoblamaslik (Ish kunlari)</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="excludeHolidays" class="w-4 h-4 text-brand-600 rounded focus:ring-brand-500 border-slate-300 dark:border-slate-600 dark:bg-slate-700">
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Bayram kunlarini hisoblamaslik</span>
        </label>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <transition name="page-fade">
        <div v-if="result" class="mt-5 grid grid-cols-1 sm:grid-cols-2 gap-3 animate-resultPop">
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Kalendar bo'yicha</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ result.mathDays }} kun farq</p>
          </div>
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Tanlovga asosan chiqdi</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ result.calculatedDays }} kun (ish/kunlar)</p>
          </div>
          <div v-if="result.holidays > 0" class="sm:col-span-2 text-center text-xs text-slate-500">
            Shu oraliqda {{ result.holidays }} ta bayram kuni bor.
          </div>
          <div class="sm:col-span-2 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 text-center animate-resultPop">
            <p class="text-xs font-medium text-brand-600 uppercase tracking-wide">Taxminiy farq</p>
            <p class="text-xl font-extrabold text-brand-800 mt-1">{{ result.approx }}</p>
          </div>
        </div>
      </transition>
    </div>
  </ToolShell>
</template>
