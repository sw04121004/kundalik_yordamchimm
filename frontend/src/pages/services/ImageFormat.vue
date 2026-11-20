<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useToolText } from '../../utils/toolText'

const tx = useToolText({
  uz: {
    title: "Format konvertori",
    desc: "Rasmlarni PNG, JPG, WEBP formatlariga tez va oson o'tkazing",
    hint: "Rasmni yuklang, kerakli yangi formatni tanlang va «Konvertatsiya» tugmasini bosing.",
    chooseFile: "Rasm tanlang",
    targetFormat: "Qaysi formatga o'tkazilsin?",
    convertBtn: "Konvertatsiya qilish",
    readyMsg: "Muvaffaqiyatli tayyorlandi!",
    download: "Yuklab olish",
  },
  ru: {
    title: "Конвертер форматов",
    desc: "Быстрая конвертация изображений в форматы PNG, JPG, WEBP",
    hint: "Загрузите изображение, выберите новый формат и нажмите «Конвертировать».",
    chooseFile: "Выберите изображение",
    targetFormat: "В какой формат конвертировать?",
    convertBtn: "Конвертировать",
    readyMsg: "Успешно сконвертировано!",
    download: "Скачать",
  },
  en: {
    title: "Image Format Converter",
    desc: "Easily convert images between PNG, JPG, and WEBP formats",
    hint: "Upload an image, choose target format, and click 'Convert'.",
    chooseFile: "Choose image",
    targetFormat: "Target format:",
    convertBtn: "Convert",
    readyMsg: "Converted successfully!",
    download: "Download",
  },
})

const fileInput = ref(null)
const imageSrc = ref(null)
const targetFormat = ref('image/png')
const outputUrl = ref('')
const fileName = ref('')

function handleFile(e) {
  const file = e.target.files?.[0]
  if (!file) return
  fileName.value = file.name.replace(/\.[^/.]+$/, "")
  const reader = new FileReader()
  reader.onload = (ev) => {
    imageSrc.value = ev.target.result
    outputUrl.value = ''
  }
  reader.readAsDataURL(file)
}

function convert() {
  if (!imageSrc.value) return
  const img = new Image()
  img.onload = () => {
    const canvas = document.createElement('canvas')
    canvas.width = img.width
    canvas.height = img.height
    const ctx = canvas.getContext('2d')
    ctx.drawImage(img, 0, 0)
    outputUrl.value = canvas.toDataURL(targetFormat.value)
  }
  img.src = imageSrc.value
}
</script>

<template>
  <ToolShell icon="🔄" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <div>
        <label class="label">{{ tx.chooseFile }}</label>
        <input ref="fileInput" type="file" accept="image/*" class="input !py-2" @change="handleFile" />
      </div>

      <div v-if="imageSrc" class="space-y-4">
        <div>
          <label class="label">{{ tx.targetFormat }}</label>
          <select v-model="targetFormat" class="input">
            <option value="image/png">PNG (.png)</option>
            <option value="image/jpeg">JPEG (.jpg)</option>
            <option value="image/webp">WEBP (.webp)</option>
          </select>
        </div>

        <button class="btn-primary w-full" @click="convert">{{ tx.convertBtn }}</button>
      </div>

      <div v-if="outputUrl" class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 text-center space-y-3 animate-fadeUp">
        <p class="text-xs font-bold text-green-600 uppercase">{{ tx.readyMsg }}</p>
        <img :src="outputUrl" alt="Result" class="max-h-60 mx-auto rounded-lg shadow-sm" />
        <a :href="outputUrl" :download="`${fileName}-qulay.${targetFormat.split('/')[1]}`" class="btn-primary !px-6 !py-2 inline-block">
          {{ tx.download }}
        </a>
      </div>
    </div>
  </ToolShell>
</template>
