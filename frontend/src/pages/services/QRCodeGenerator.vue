<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { useI18n } from '../../i18n'

const { t } = useI18n()
const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('qr-kod-generatori'))

const text = ref('')
const size = ref(300)
const error = ref('')
const generatedText = ref('')

const qrUrl = computed(() => {
  if (!generatedText.value) return ''
  const encoded = encodeURIComponent(generatedText.value)
  return `https://api.qrserver.com/v1/create-qr-code/?size=${size.value}x${size.value}&data=${encoded}`
})

function generate() {
  error.value = ''
  if (!text.value.trim()) {
    error.value = t('tool.qr-kod-generatori.errorEmpty')
    generatedText.value = ''
    return
  }
  generatedText.value = text.value.trim()
}

function reset() {
  text.value = ''
  generatedText.value = ''
  error.value = ''
}
</script>

<template>
  <ToolShell slug="qr-kod-generatori" icon="📱" title="svc.qr-kod-generatori.name" description="svc.qr-kod-generatori.desc">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4 animate-fadeUp">
      <div>
        <label class="label">{{ t('tool.qr-kod-generatori.label') }}</label>
        <input
          v-model="text"
          type="text"
          class="input"
          :placeholder="t('tool.qr-kod-generatori.placeholder')"
          @keyup.enter="generate"
        />
      </div>

      <div>
        <label class="label">{{ t('tool.qr-kod-generatori.size') }}: {{ size }}×{{ size }} px</label>
        <input v-model="size" type="range" min="150" max="500" step="50" class="w-full accent-brand-600 cursor-pointer" />
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1 animate-popIn" @click="generate">{{ t('tool.qr-kod-generatori.generate') }}</button>
        <button class="btn-secondary" @click="reset">{{ t('common.clear') }}</button>
      </div>

      <transition name="page-fade">
        <div
          v-if="qrUrl"
          class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 p-5 flex flex-col items-center gap-4 card-hover-lift animate-scaleIn"
        >
          <img :src="qrUrl" :alt="generatedText" class="rounded-lg border border-white shadow-sm bg-white" />
          <a :href="qrUrl" :download="'qulay-qr-kod.png'" class="btn-secondary text-sm">{{ t('tool.qr-kod-generatori.download') }}</a>
        </div>
      </transition>
    </div>
  </ToolShell>
</template>
