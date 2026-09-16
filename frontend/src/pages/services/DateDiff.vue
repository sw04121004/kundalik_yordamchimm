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
const error = ref('')
const result = ref(null)

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
    error.value = 'Sana formati noto‘g‘ri.'
    return
  }

  const diffMs = Math.abs(end - start)
  const totalDays = Math.round(diffMs / (1000 * 60 * 60 * 24))

  const years = Math.floor(totalDays / 365)
  const remainderAfterYears = totalDays % 365
  const months = Math.floor(remainderAfterYears / 30)
  const days = remainderAfterYears % 30

  result.value = {
    totalDays,
    weeks: Math.floor(totalDays / 7),
    approx: `${years} yil, ${months} oy, ${days} kun (taxminan)`,
  }
}

function reset() {
  startDate.value = ''
  endDate.value = ''
  result.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell icon="📅" title="Sana farqi" description="Ikki sana orasidagi farqni hisoblang" hint="Ikkita sanani tanlang — ular orasidagi farq kun, hafta va taxminiy yil/oy/kun ko‘rinishida chiqadi.">
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

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <transition name="page-fade">
        <div v-if="result" class="mt-5 grid grid-cols-1 sm:grid-cols-2 gap-3 animate-resultPop">
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Jami kunlar</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ result.totalDays }} kun</p>
          </div>
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Haftalar</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ result.weeks }} hafta</p>
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
