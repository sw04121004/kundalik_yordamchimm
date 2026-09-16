<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('ortacha-qiymat'))

const numbersText = ref('')
const error = ref('')
const stats = ref(null)

function calculate() {
  error.value = ''
  stats.value = null

  const parts = numbersText.value
    .split(/[,\s]+/)
    .map((p) => p.trim())
    .filter(Boolean)

  if (parts.length === 0) {
    error.value = 'Iltimos, kamida bitta son kiriting.'
    return
  }

  const numbers = parts.map(Number)
  if (numbers.some((n) => Number.isNaN(n))) {
    error.value = 'Faqat raqamlarni vergul yoki bo‘shliq bilan ajratib kiriting.'
    return
  }

  const sum = numbers.reduce((acc, n) => acc + n, 0)
  const avg = sum / numbers.length
  const max = Math.max(...numbers)
  const min = Math.min(...numbers)

  stats.value = {
    count: numbers.length,
    sum: round(sum),
    avg: round(avg),
    max,
    min,
  }
}

function round(num) {
  return Math.round(num * 10000) / 10000
}

function reset() {
  numbersText.value = ''
  stats.value = null
  error.value = ''
}
</script>

<template>
  <ToolShell icon="📊" title="O‘rtacha qiymat hisoblagich" description="Sonlar ro‘yxatining o‘rtachasini toping" hint="Sonlarni vergul yoki bo‘shliq bilan ajratib kiriting (masalan: 12, 45, 33) — yig‘indi, eng katta/kichik va o‘rtacha qiymat avtomatik chiqadi.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Sonlar (vergul yoki bo‘shliq bilan ajrating)</label>
        <textarea
          v-model="numbersText"
          rows="4"
          class="input resize-none"
          placeholder="masalan: 12, 45, 33, 20, 8"
        ></textarea>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="calculate">Hisoblash</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <transition name="page-fade">
        <div v-if="stats" class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5 animate-resultPop">
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Soni</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.count }}</p>
          </div>
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Yig‘indi</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.sum }}</p>
          </div>
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Eng katta</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.max }}</p>
          </div>
          <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-4 py-3 text-center">
            <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">Eng kichik</p>
            <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.min }}</p>
          </div>
          <div class="col-span-2 sm:col-span-4 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 text-center animate-resultPop">
            <p class="text-xs font-medium text-brand-600 uppercase tracking-wide">O‘rtacha qiymat</p>
            <p class="text-2xl font-extrabold text-brand-800 dark:text-brand-200 mt-1">{{ stats.avg }}</p>
          </div>
        </div>
      </transition>
    </div>
  </ToolShell>

</template>
