<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useToolText } from '../../utils/toolText'

const tx = useToolText({
  uz: {
    title: "Fonni o'chirish",
    desc: "Rasmning orqa fonini shaffof (transparent PNG) formatiga o'tkazing",
    hint: "Oq yoki bir xil rangdagi orqa fonga ega rasmni yuklang, tizim uni avtomatik shaffof qiladi.",
    chooseFile: "Rasm tanlang",
    tolerance: "Sezgirlik (aniqlik darajasi):",
    download: "Shaffof PNG yuklab olish",
  },
  ru: {
    title: "Удаление фона",
    desc: "Преобразование фона изображения в прозрачный (transparent PNG)",
    hint: "Загрузите изображение с белым или однотонным фоном, система сделает его прозрачным.",
    chooseFile: "Выберите изображение",
    tolerance: "Чувствительность (уровень точности):",
    download: "Скачать прозрачный PNG",
  },
  en: {
    title: "Background Remover",
    desc: "Make image background transparent (PNG format)",
    hint: "Upload an image with a solid or white background, and it will be made transparent automatically.",
    chooseFile: "Choose image",
    tolerance: "Tolerance (precision level):",
    download: "Download transparent PNG",
  },
})

const imageSrc = ref(null)
const outputUrl = ref('')
const tolerance = ref(30)
const fileName = ref('')
const canvasRef = ref(null)

function handleFile(e) {
  const file = e.target.files?.[0]
  if (!file) return
  fileName.value = file.name
  const reader = new FileReader()
  reader.onload = (ev) => {
    imageSrc.value = ev.target.result
    processBg()
  }
  reader.readAsDataURL(file)
}

function processBg() {
  if (!imageSrc.value) return
  const img = new Image()
  img.onload = () => {
    const canvas = document.createElement('canvas')
    canvas.width = img.width
    canvas.height = img.height
    const ctx = canvas.getContext('2d')
    ctx.drawImage(img, 0, 0)

    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height)
    const data = imgData.data

    const bgR = data[0], bgG = data[1], bgB = data[2]
    const tol = tolerance.value

    for (let i = 0; i < data.length; i += 4) {
      const r = data[i]
      const g = data[i + 1]
      const b = data[i + 2]
      if (Math.abs(r - bgR) < tol && Math.abs(g - bgG) < tol && Math.abs(b - bgB) < tol) {
        data[i + 3] = 0
      }
    }

    ctx.putImageData(imgData, 0, 0)
    outputUrl.value = canvas.toDataURL('image/png')
  }
  img.src = imageSrc.value
}
</script>

<template>
  <ToolShell icon="✂️" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <div>
        <label class="label">{{ tx.chooseFile }}</label>
        <input type="file" accept="image/*" class="input !py-2" @change="handleFile" />
      </div>

      <div v-if="imageSrc" class="space-y-4">
        <div>
          <div class="flex justify-between text-sm font-semibold mb-1">
            <span>{{ tx.tolerance }} {{ tolerance }}</span>
          </div>
          <input v-model.number="tolerance" type="range" min="5" max="80" class="w-full accent-brand-600" @input="processBg" />
        </div>

        <div v-if="outputUrl" class="text-center p-4 rounded-xl border border-dashed border-slate-300 dark:border-slate-700 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] dark:bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:16px_16px]">
          <img :src="outputUrl" alt="Result" class="max-h-64 mx-auto mb-4" />
          <a :href="outputUrl" :download="`shaffof-${fileName}.png`" class="btn-primary !px-8 !py-2.5 inline-block">
            {{ tx.download }}
          </a>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
