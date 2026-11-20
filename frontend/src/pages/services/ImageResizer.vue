<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import FormAlert from '../../components/FormAlert.vue'
import { useServicesStore } from '../../store/services'
import { useToolText } from '../../utils/toolText'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('rasm-olchamini-ozgartirish'))

const tx = useToolText({
  uz: {
    title: "Rasm o‘lchamini o‘zgartirish",
    desc: "Rasm o‘lchami, formati va hajmini o‘zgartiring",
    hint: "Avval rasm tanlang, keyin kerakli o‘lcham, format va sifatni sozlab, «O‘zgartirish»ni bosing — natijani yuklab olishingiz mumkin.",
    chooseFile: "Rasm tanlang",
    originalSize: "Hajmi:",
    origDims: "Asl o‘lcham:",
    width: "Kenglik (px)",
    height: "Balandlik (px)",
    keepRatio: "Nisbatni saqlash",
    format: "Format",
    quality: "Sifat:",
    changeBtn: "O‘zgartirish",
    clearBtn: "Tozalash",
    result: "Natija",
    newSize: "Yangi hajm:",
    download: "Yuklab olish",
    errSelect: "Iltimos, avval rasm tanlang.",
    errDimensions: "Kenglik va balandlik musbat son bo'lishi kerak.",
    errMaxSize: "Maksimal ruxsat etilgan o'lcham {max}px. Kichikroq qiymatlar kiriting.",
    errProcess: "Rasmni qayta ishlashda xatolik yuz berdi.",
  },
  ru: {
    title: "Изменение размера фото",
    desc: "Изменение разрешения, формата и размера файла изображения",
    hint: "Выберите изображение, настройте размеры, формат и качество, затем нажмите «Изменить».",
    chooseFile: "Выберите изображение",
    originalSize: "Размер файла:",
    origDims: "Исходный размер:",
    width: "Ширина (px)",
    height: "Высота (px)",
    keepRatio: "Сохранять пропорции",
    format: "Формат",
    quality: "Качество:",
    changeBtn: "Изменить",
    clearBtn: "Сбросить",
    result: "Результат",
    newSize: "Новый размер:",
    download: "Скачать",
    errSelect: "Пожалуйста, сначала выберите изображение.",
    errDimensions: "Ширина и высота должны быть положительными числами.",
    errMaxSize: "Максимальный размер {max}px. Введите меньшие значения.",
    errProcess: "Ошибка при обработке изображения.",
  },
  en: {
    title: "Image Resizer",
    desc: "Change image dimensions, file format, and resolution",
    hint: "Select an image, configure width, height, format, and quality, then click 'Resize'.",
    chooseFile: "Choose image",
    originalSize: "File size:",
    origDims: "Original size:",
    width: "Width (px)",
    height: "Height (px)",
    keepRatio: "Keep aspect ratio",
    format: "Format",
    quality: "Quality:",
    changeBtn: "Resize",
    clearBtn: "Clear",
    result: "Result",
    newSize: "New file size:",
    download: "Download",
    errSelect: "Please select an image first.",
    errDimensions: "Width and height must be positive numbers.",
    errMaxSize: "Maximum allowed dimension is {max}px. Enter smaller values.",
    errProcess: "Error processing the image.",
  },
})

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
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + sizes[i]
}

function handleFileChange(e) {
  const file = e.target.files?.[0]
  if (!file) return

  error.value = ''
  outputUrl.value = ''
  originalName.value = file.name
  originalSize.value = file.size

  const reader = new FileReader()
  reader.onload = (event) => {
    const img = new Image()
    img.onload = () => {
      originalImage.value = img
      originalDims.value = { w: img.naturalWidth, h: img.naturalHeight }
      width.value = img.naturalWidth
      height.value = img.naturalHeight
    }
    img.src = event.target.result
  }
  reader.readAsDataURL(file)
}

function onWidthChange() {
  if (!keepRatio.value || !originalDims.value.w) return
  const ratio = originalDims.value.h / originalDims.value.w
  height.value = Math.round(Number(width.value || 0) * ratio) || ''
}

function onHeightChange() {
  if (!keepRatio.value || !originalDims.value.h) return
  const ratio = originalDims.value.w / originalDims.value.h
  width.value = Math.round(Number(height.value || 0) * ratio) || ''
}

const MAX_DIMENSION = 8000

function process() {
  error.value = ''
  if (!originalImage.value) {
    error.value = tx.value.errSelect
    return
  }
  const w = parseInt(width.value, 10)
  const h = parseInt(height.value, 10)
  if (!w || !h || w <= 0 || h <= 0) {
    error.value = tx.value.errDimensions
    return
  }
  if (w > MAX_DIMENSION || h > MAX_DIMENSION) {
    error.value = tx.value.errMaxSize.replace('{max}', MAX_DIMENSION)
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
        error.value = tx.value.errProcess
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
  <ToolShell icon="🖼️" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <FormAlert :message="error" />

    <div class="space-y-5">
      <div>
        <label class="label">{{ tx.chooseFile }}</label>
        <input ref="fileInput" type="file" accept="image/*" class="input !py-2" @change="handleFileChange" />
      </div>

      <div v-if="originalImage" class="space-y-5">
        <div class="flex items-center gap-4 flex-wrap text-sm text-slate-500">
          <span>{{ tx.origDims }} <strong class="text-slate-700 dark:text-slate-200">{{ originalDims.w }}×{{ originalDims.h }}</strong></span>
          <span>{{ tx.originalSize }} <strong class="text-slate-700 dark:text-slate-200">{{ formatBytes(originalSize) }}</strong></span>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">{{ tx.width }}</label>
            <input v-model.number="width" type="number" class="input" @input="onWidthChange" />
          </div>
          <div>
            <label class="label">{{ tx.height }}</label>
            <input v-model.number="height" type="number" class="input" @input="onHeightChange" />
          </div>
        </div>

        <label class="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300 cursor-pointer">
          <input type="checkbox" v-model="keepRatio" class="rounded text-brand-600 focus:ring-brand-400" />
          {{ tx.keepRatio }}
        </label>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">{{ tx.format }}</label>
            <select v-model="format" class="input">
              <option value="image/jpeg">JPEG</option>
              <option value="image/png">PNG</option>
              <option value="image/webp">WEBP</option>
            </select>
          </div>
          <div v-if="format !== 'image/png'">
            <label class="label">{{ tx.quality }} {{ Math.round(quality * 100) }}%</label>
            <input v-model.number="quality" type="range" min="0.1" max="1" step="0.05" class="w-full accent-brand-600 mt-3" />
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button class="btn-primary flex-1" @click="process">{{ tx.changeBtn }}</button>
          <button class="btn-secondary" @click="reset">{{ tx.clearBtn }}</button>
        </div>
      </div>

      <transition name="page-fade">
        <div v-if="outputUrl" class="rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 p-4 animate-resultPop">
          <p class="text-xs font-medium text-brand-600 uppercase tracking-wide mb-3">{{ tx.result }}</p>
          <img :src="outputUrl" alt="Result" class="max-w-full rounded-lg border border-brand-100 mb-3" />
          <div class="flex items-center justify-between flex-wrap gap-2">
            <span class="text-sm text-slate-500">{{ tx.newSize }} <strong class="text-slate-700 dark:text-slate-200">{{ formatBytes(outputSize) }}</strong></span>
            <a :href="outputUrl" :download="downloadName()" class="btn-secondary !px-4 !py-2 text-sm">{{ tx.download }}</a>
          </div>
        </div>
      </transition>
    </div>
  </ToolShell>
</template>
