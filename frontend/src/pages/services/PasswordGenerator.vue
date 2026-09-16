<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('parol-generatori'))

const length = ref(14)
const useUpper = ref(true)
const useLower = ref(true)
const useNumbers = ref(true)
const useSymbols = ref(true)

const password = ref('')
const error = ref('')
const copied = ref(false)

const CHARSETS = {
  upper: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  lower: 'abcdefghijklmnopqrstuvwxyz',
  numbers: '0123456789',
  symbols: '!@#$%^&*()_-+=?',
}

function strengthLabel(pw) {
  if (pw.length >= 14) return { label: 'Kuchli', color: 'text-emerald-600' }
  if (pw.length >= 10) return { label: 'O‘rtacha', color: 'text-amber-600' }
  return { label: 'Zaif', color: 'text-red-600' }
}

function generate() {
  error.value = ''
  copied.value = false

  let pool = ''
  if (useUpper.value) pool += CHARSETS.upper
  if (useLower.value) pool += CHARSETS.lower
  if (useNumbers.value) pool += CHARSETS.numbers
  if (useSymbols.value) pool += CHARSETS.symbols

  if (!pool) {
    error.value = 'Kamida bitta belgi turini tanlang.'
    password.value = ''
    return
  }

  const len = Math.min(Math.max(parseInt(length.value, 10) || 8, 4), 64)
  const array = new Uint32Array(len)
  crypto.getRandomValues(array)

  password.value = Array.from(array, (n) => pool[n % pool.length]).join('')
}

async function copyPassword() {
  if (!password.value) return
  try {
    await navigator.clipboard.writeText(password.value)
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
  } catch {
    error.value = 'Nusxalashda xatolik yuz berdi.'
  }
}

onMounted(generate)
</script>

<template>
  <ToolShell icon="🔐" title="Kuchli parol generatori" description="Xavfsiz va murakkab parol yarating" hint="Uzunlik va belgi turlarini sozlang — parol avtomatik yaratiladi, «Nusxalash» orqali darhol nusxa olishingiz mumkin.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-5">
      <div>
        <label class="label">Uzunligi: {{ length }} belgi</label>
        <input v-model="length" type="range" min="6" max="32" class="w-full accent-brand-600" />
      </div>

      <div class="grid grid-cols-2 gap-3 text-sm text-slate-600">
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useUpper" class="rounded text-brand-600 focus:ring-brand-400" /> Katta harflar (A-Z)
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useLower" class="rounded text-brand-600 focus:ring-brand-400" /> Kichik harflar (a-z)
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useNumbers" class="rounded text-brand-600 focus:ring-brand-400" /> Raqamlar (0-9)
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useSymbols" class="rounded text-brand-600 focus:ring-brand-400" /> Belgilar (!@#$)
        </label>
      </div>

      <button class="btn-primary w-full" @click="generate">Parol yaratish</button>

      <div v-if="password" :key="password" class="rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop">
        <div class="flex items-center justify-between gap-3">
          <p class="text-lg font-extrabold text-brand-800 font-mono break-all">{{ password }}</p>
          <button class="shrink-0 btn-secondary !px-3 !py-2 text-sm" @click="copyPassword">
            {{ copied ? '✓ Nusxalandi' : 'Nusxalash' }}
          </button>
        </div>
        <p class="text-xs mt-2 font-semibold" :class="strengthLabel(password).color">
          Kuch darajasi: {{ strengthLabel(password).label }}
        </p>
      </div>
    </div>
  </ToolShell>

</template>
