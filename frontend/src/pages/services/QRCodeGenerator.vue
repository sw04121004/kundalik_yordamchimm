<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

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
    error.value = 'Iltimos, matn yoki havola kiriting.'
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
  <ToolShell
    icon="🔳"
    title="QR-kod generatori"
    description="Matn yoki havoladan QR-kod yarating"
    hint="Matn yoki havola (link) kiriting, «Yaratish»ni bosing — QR-kod darhol paydo bo‘ladi, uni yuklab olishingiz mumkin."
  >
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-4">
      <div>
        <label class="label">Matn yoki havola</label>
        <input
          v-model="text"
          type="text"
          class="input"
          placeholder="masalan: https://example.com yoki istalgan matn"
          @keyup.enter="generate"
        />
      </div>

      <div>
        <label class="label">O‘lcham: {{ size }}×{{ size }} px</label>
        <input v-model="size" type="range" min="150" max="500" step="50" class="w-full accent-brand-600" />
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="generate">Yaratish</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>

      <transition name="page-fade">
        <div
          v-if="qrUrl"
          class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 p-5 flex flex-col items-center gap-4 animate-resultPop"
        >
          <img :src="qrUrl" :alt="generatedText" class="rounded-lg border border-white shadow-sm bg-white" />
          <a :href="qrUrl" :download="'qulay-qr-kod.png'" class="btn-secondary text-sm">Yuklab olish</a>
        </div>
      </transition>

      <p class="text-xs text-slate-400 dark:text-slate-500 text-center pt-1">
        QR-kod tashqi (bepul) xizmat orqali yaratiladi, shuning uchun internet aloqasi kerak bo‘ladi.
      </p>
    </div>
  </ToolShell>
</template>
