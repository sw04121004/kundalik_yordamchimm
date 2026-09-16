<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('ogirlik-konvertori'))

// base unit: grams
const units = {
  mg: { label: 'Milligramm (mg)', factor: 0.001 },
  g: { label: 'Gramm (g)', factor: 1 },
  kg: { label: 'Kilogramm (kg)', factor: 1000 },
  ton: { label: 'Tonna (t)', factor: 1000000 },
  lb: { label: 'Funt (lb)', factor: 453.592 },
  oz: { label: 'Untsiya (oz)', factor: 28.3495 },
}

const value = ref('')
const from = ref('kg')
const to = ref('lb')
const error = ref('')

const result = computed(() => {
  error.value = ''
  if (value.value === '') return null
  const num = parseFloat(value.value)
  if (Number.isNaN(num)) {
    error.value = 'Iltimos, faqat raqam kiriting.'
    return null
  }
  const grams = num * units[from.value].factor
  const converted = grams / units[to.value].factor
  return Math.round(converted * 1e6) / 1e6
})

function reset() {
  value.value = ''
  from.value = 'kg'
  to.value = 'lb'
  error.value = ''
}

function swap() {
  ;[from.value, to.value] = [to.value, from.value]
}
</script>

<template>
  <ToolShell icon="⚖️" title="Og‘irlik konvertori" description="Kilogramm, gramm, funt va boshqa birliklar" hint="Qiymatni kiriting, «Dan» va «Ga» birliklarini tanlang — natija avtomatik hisoblanadi.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Qiymat</label>
        <input v-model="value" type="number" class="input" placeholder="masalan: 70" />
      </div>

      <div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-end">
        <div>
          <label class="label">Dan</label>
          <select v-model="from" class="input">
            <option v-for="(u, key) in units" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
        <button class="btn-secondary !px-3 !py-2.5 mb-0.5" @click="swap" title="Almashtirish">⇄</button>
        <div>
          <label class="label">Ga</label>
          <select v-model="to" class="input">
            <option v-for="(u, key) in units" :key="key" :value="key">{{ u.label }}</option>
          </select>
        </div>
      </div>

      <button class="btn-secondary w-full" @click="reset">Tozalash</button>

      <transition name="page-fade">
        <div v-if="result !== null" class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop">
          <p class="text-xs font-medium text-brand-600 uppercase tracking-wide">Natija</p>
          <p class="text-2xl font-extrabold text-brand-800 mt-1 break-words">
            {{ value }} {{ units[from].label.split(' ')[0] }} = {{ result }} {{ units[to].label.split(' ')[0] }}
          </p>
        </div>
      </transition>
    </div>
  </ToolShell>

</template>
