<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('rasm-olchamini-ozgartirish'))

const fileInput = ref(null)
const originalImage = ref(null)
const originalName = ref('')
const originalSize = ref(0)
const originalDims = ref({ w: 0, h: 0 })

const width = ref('')
const height = ref('')
const keepRatio = ref(true)
const format = ref('image/jpeg')
const quality = ref(0.85)

const error = ref('')
const outputUrl = ref('')
const outputSize = ref(0)

function formatBytes(bytes) {
  if (!bytes) return '0 KB'
  const kb = bytes / 1024
  if (kb < 1024) return `${kb.toFixed(1)} KB`
  return `${(kb / 1024).toFixed(2)} MB`
}

function handleFileChange(e) {
  error.value = ''
  outputUrl.value = ''
  const file = e.target.files?.[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    error.value = 'Iltimos, faqat rasm faylini tanlang.'
    return
  }

  originalName.value = file.name
  originalSize.value = file.size

  const reader = new FileReader()
  reader.onload = (ev) => {
    const img = new Image()
    img.onload = () => {
      originalImage.value = img
      originalDims.value = { w: img.width, h: img.height }
      width.value = img.width
      height.value = img.height
    }
    img.onerror = () => {
      error.value = 'Rasmni o‘qib bo‘lmadi.'
    }
    img.src = ev.target.result
  }
  reader.onerror = () => {
    error.value = 'Faylni o‘qishda xatolik yuz berdi.'
  }
  reader.readAsDataURL(file)
}

function onWidthChange() {
  if (keepRatio.value && originalDims.value.w) {
    const ratio = originalDims.value.h / originalDims.value.w
    height.value = Math.round(width.value * ratio)
  }
}

function onHeightChange() {
  if (keepRatio.value && originalDims.value.h) {
    const ratio = originalDims.value.w / originalDims.value.h
    width.value = Math.round(height.value * ratio)
  }
}

function process() {
  error.value = ''
  outputUrl.value = ''

  if (!originalImage.value) {
    error.value = 'Iltimos, avval rasm tanlang.'
    return
  }

  const w = parseInt(width.value, 10)
  const h = parseInt(height.value, 10)
  if (!w || !h || w <= 0 || h <= 0) {
    error.value = 'Iltimos, to‘g‘ri o‘lcham kiriting.'
    return
  }

  const canvas = document.createElement('canvas')
  canvas.width = w
  canvas.height = h
  const ctx = canvas.getContext('2d')
  ctx.drawImage(originalImage.value, 0, 0, w, h)

  canvas.toBlob(
    (blob) => {
      if (!blob) {
        error.value = 'Rasmni qayta ishlashda xatolik yuz berdi.'
        return
      }
      outputUrl.value = URL.createObjectURL(blob)
      outputSize.value = blob.size
    },
    format.value,
    format.value === 'image/png' ? undefined : quality.value
  )
}

function reset() {
  originalImage.value = null
  originalName.value = ''
  originalSize.value = 0
  originalDims.value = { w: 0, h: 0 }
  width.value = ''
  height.value = ''
  outputUrl.value = ''
  outputSize.value = 0
  error.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

function downloadName() {
  const ext = format.value.split('/')[1]
  const base = originalName.value.replace(/\.[^.]+$/, '') || 'qulay-rasm'
  return `${base}-qulay.${ext}`
}
</script>

<template>
  <ToolShell icon="🖼️" title="Rasm o‘lchamini o‘zgartirish" description="Rasm o‘lchami, formati va hajmini o‘zgartiring" hint="Avval rasm tanlang, keyin kerakli o‘lcham, format va sifatni sozlab, «O‘zgartirish»ni bosing — natijani yuklab olishingiz mumkin.">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-5">
      <div>
        <label class="label">Rasm tanlang</label>
        <input ref="fileInput" type="file" accept="image/*" class="input !py-2" @change="handleFileChange" />
      </div>

      <div v-if="originalImage" class="space-y-5">
        <div class="flex items-center gap-4 flex-wrap text-sm text-slate-500">
          <span>Asl o‘lcham: <strong class="text-slate-700">{{ originalDims.w }}×{{ originalDims.h }}</strong></span>
          <span>Hajmi: <strong class="text-slate-700">{{ formatBytes(originalSize) }}</strong></span>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Kenglik (px)</label>
            <input v-model.number="width" type="number" class="input" @input="onWidthChange" />
          </div>
          <div>
            <label class="label">Balandlik (px)</label>
            <input v-model.number="height" type="number" class="input" @input="onHeightChange" />
          </div>
        </div>

        <label class="flex items-center gap-2 text-sm text-slate-600">
          <input type="checkbox" v-model="keepRatio" class="rounded text-brand-600 focus:ring-brand-400" />
          Nisbatni saqlash
        </label>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Format</label>
            <select v-model="format" class="input">
              <option value="image/jpeg">JPEG</option>
              <option value="image/png">PNG</option>
              <option value="image/webp">WEBP</option>
            </select>
          </div>
          <div v-if="format !== 'image/png'">
            <label class="label">Sifat: {{ Math.round(quality * 100) }}%</label>
            <input v-model.number="quality" type="range" min="0.1" max="1" step="0.05" class="w-full accent-brand-600 mt-3" />
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button class="btn-primary flex-1" @click="process">O‘zgartirish</button>
          <button class="btn-secondary" @click="reset">Tozalash</button>
        </div>
      </div>

      <transition name="page-fade">
        <div v-if="outputUrl" class="rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 p-4 animate-resultPop">
          <p class="text-xs font-medium text-brand-600 uppercase tracking-wide mb-3">Natija</p>
          <img :src="outputUrl" alt="Natija" class="max-w-full rounded-lg border border-brand-100 mb-3" />
          <div class="flex items-center justify-between flex-wrap gap-2">
            <span class="text-sm text-slate-500">Yangi hajm: <strong class="text-slate-700">{{ formatBytes(outputSize) }}</strong></span>
            <a :href="outputUrl" :download="downloadName()" class="btn-secondary !px-4 !py-2 text-sm">Yuklab olish</a>
          </div>
        </div>
      </transition>
    </div>
  </ToolShell>

</template>
