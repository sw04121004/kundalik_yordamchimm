<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { useI18n } from '../../i18n'

const { t } = useI18n()
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
  if (pw.length >= 14) return { key: 'tool.parol-generatori.strong', color: 'text-emerald-600' }
  if (pw.length >= 10) return { key: 'tool.parol-generatori.medium', color: 'text-amber-600' }
  return { key: 'tool.parol-generatori.weak', color: 'text-red-600' }
}


function generate() {
  error.value = ''
  copied.value = false

  let pool = ''
  const requiredChars = []

  if (useUpper.value) {
    pool += CHARSETS.upper
    requiredChars.push(CHARSETS.upper[Math.floor(Math.random() * CHARSETS.upper.length)])
  }
  if (useLower.value) {
    pool += CHARSETS.lower
    requiredChars.push(CHARSETS.lower[Math.floor(Math.random() * CHARSETS.lower.length)])
  }
  if (useNumbers.value) {
    pool += CHARSETS.numbers
    requiredChars.push(CHARSETS.numbers[Math.floor(Math.random() * CHARSETS.numbers.length)])
  }
  if (useSymbols.value) {
    pool += CHARSETS.symbols
    requiredChars.push(CHARSETS.symbols[Math.floor(Math.random() * CHARSETS.symbols.length)])
  }

  if (!pool) {
    error.value = t('tool.parol-generatori.minOne')
    password.value = ''
    return
  }

  const len = Math.min(Math.max(parseInt(length.value, 10) || 8, 4), 64)
  
  let generatedPassword = ''
  // Required characters first
  for (let i = 0; i < requiredChars.length; i++) {
    generatedPassword += requiredChars[i]
  }

  // Fill the rest of the password length
  const remainingLength = len - requiredChars.length
  const array = new Uint32Array(remainingLength)
  crypto.getRandomValues(array)
  
  for (let i = 0; i < remainingLength; i++) {
    generatedPassword += pool[array[i] % pool.length]
  }

  // Shuffle the password to mix required characters
  password.value = generatedPassword.split('').sort(() => Math.random() - 0.5).join('')
}

async function copyPassword() {
  if (!password.value) return
  try {
    await navigator.clipboard.writeText(password.value)
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
  } catch {
    error.value = t('tool.parol-generatori.copyError')
  }
}

onMounted(generate)
</script>

<template>
  <ToolShell slug="parol-generatori" icon="🔐" title="svc.parol-generatori.name" description="svc.parol-generatori.desc">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-5">
      <div>
        <label class="label">{{ t('tool.parol-generatori.length') }}: {{ length }}</label>
        <input v-model="length" type="range" min="6" max="32" class="w-full accent-brand-600" />
      </div>

      <div class="grid grid-cols-2 gap-3 text-sm text-slate-600">
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useUpper" class="rounded text-brand-600 focus:ring-brand-400" /> {{ t('tool.parol-generatori.upper') }}
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useLower" class="rounded text-brand-600 focus:ring-brand-400" /> {{ t('tool.parol-generatori.lower') }}
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useNumbers" class="rounded text-brand-600 focus:ring-brand-400" /> {{ t('tool.parol-generatori.numbers') }}
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="useSymbols" class="rounded text-brand-600 focus:ring-brand-400" /> {{ t('tool.parol-generatori.symbols') }}
        </label>
      </div>

      <button class="btn-primary w-full" @click="generate">{{ t('tool.parol-generatori.generate') }}</button>

      <div v-if="password" :key="password" class="rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop">
        <div class="flex items-center justify-between gap-3">
          <p class="text-lg font-extrabold text-brand-800 font-mono break-all">{{ password }}</p>
          <button class="shrink-0 btn-secondary !px-3 !py-2 text-sm" @click="copyPassword">
            {{ copied ? '✔ ' + t('common.copied') : t('common.copy') }}
          </button>
        </div>
        <p class="text-xs mt-2 font-semibold" :class="strengthLabel(password).color">
          {{ t('tool.parol-generatori.strength') }}: {{ t(strengthLabel(password).key) }}
        </p>
      </div>
    </div>
  </ToolShell>

</template>
