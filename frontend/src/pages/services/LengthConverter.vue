<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('uzunlik-konvertori'))

// base unit: meters
const units = {
  mm: { label: 'Millimetr (mm)', factor: 0.001 },
  cm: { label: 'Santimetr (sm)', factor: 0.01 },
  m: { label: 'Metr (m)', factor: 1 },
  km: { label: 'Kilometr (km)', factor: 1000 },
  inch: { label: 'Dyuym (inch)', factor: 0.0254 },
  ft: { label: 'Fut (ft)', factor: 0.3048 },
  mile: { label: 'Milya (mile)', factor: 1609.34 },
}

const value = ref('')
const from = ref('m')
const to = ref('km')
const error = ref('')

const result = computed(() => {
  error.value = ''
  if (value.value === '') return null
  const num = parseFloat(value.value)
  if (Number.isNaN(num)) {
    error.value = 'Iltimos, faqat raqam kiriting.'
    return null
  }
  const meters = num * units[from.value].factor
  const converted = meters / units[to.value].factor
  return Math.round(converted * 1e6) / 1e6
})

function reset() {
  value.value = ''
  from.value = 'm'
  to.value = 'km'
  error.value = ''
}

function swap() {
  ;[from.value, to.value] = [to.value, from.value]
}
</script>

<template>
  <ToolShell icon="📏" title="Uzunlik konvertori" description="Metr, kilometr, milya va boshqa birliklar" hint="Qiymatni kiriting, «Dan» va «Ga» birliklarini tanlang — natija avtomatik hisoblanadi.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Qiymat</label>
        <input v-model="value" type="number" class="input" placeholder="masalan: 100" />
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
