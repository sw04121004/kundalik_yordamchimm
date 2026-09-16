<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const imageSrc = ref(null)
const fileName = ref('')
const rotation = ref(0)
const flipH = ref(false)
const flipV = ref(false)
const outputUrl = ref('')

function handleFile(e) {
  const file = e.target.files?.[0]
  if (!file) return
  fileName.value = file.name
  rotation.value = 0
  flipH.value = false
  flipV.value = false
  const reader = new FileReader()
  reader.onload = (ev) => {
    imageSrc.value = ev.target.result
    render()
  }
  reader.readAsDataURL(file)
}

function rotateRight() {
  rotation.value = (rotation.value + 90) % 360
  render()
}

function rotateLeft() {
  rotation.value = (rotation.value + 270) % 360
  render()
}

function toggleFlipH() {
  flipH.value = !flipH.value
  render()
}

function toggleFlipV() {
  flipV.value = !flipV.value
  render()
}

function render() {
  if (!imageSrc.value) return
  const img = new Image()
  img.onload = () => {
    const canvas = document.createElement('canvas')
    const rad = (rotation.value * Math.PI) / 180
    const isSideways = rotation.value === 90 || rotation.value === 270

    canvas.width = isSideways ? img.height : img.width
    canvas.height = isSideways ? img.width : img.height

    const ctx = canvas.getContext('2d')
    ctx.translate(canvas.width / 2, canvas.height / 2)
    ctx.rotate(rad)
    ctx.scale(flipH.value ? -1 : 1, flipV.value ? -1 : 1)
    ctx.drawImage(img, -img.width / 2, -img.height / 2)

    outputUrl.value = canvas.toDataURL('image/png')
  }
  img.src = imageSrc.value
}
</script>

<template>
  <ToolShell icon="🔃" title="Rasmni aylantirish va akslantirish" description="Rasmni 90°, 180°, 270° gradusga burish hamda ko'zgu kabi akslantirish" hint="Rasmni yuklang va kerakli burish yoki akslantirish tugmalarini bosing.">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <div>
        <label class="label">Rasm tanlang</label>
        <input type="file" accept="image/*" class="input !py-2" @change="handleFile" />
      </div>

      <div v-if="imageSrc" class="space-y-4">
        <div class="flex flex-wrap justify-center gap-2">
          <button class="btn-secondary text-sm !py-2" @click="rotateLeft">↺ 90° Chapga</button>
          <button class="btn-secondary text-sm !py-2" @click="rotateRight">↻ 90° O'ngga</button>
          <button class="btn-secondary text-sm !py-2" :class="flipH ? '!border-brand-500 !bg-brand-50 dark:!bg-brand-900/30' : ''" @click="toggleFlipH">⇄ Gorizontal ko'zgu</button>
          <button class="btn-secondary text-sm !py-2" :class="flipV ? '!border-brand-500 !bg-brand-50 dark:!bg-brand-900/30' : ''" @click="toggleFlipV">⇅ Vertikal ko'zgu</button>
        </div>

        <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 text-center space-y-3">
          <img :src="outputUrl || imageSrc" alt="Preview" class="max-h-72 mx-auto rounded-lg shadow-sm" />
          <div>
            <a :href="outputUrl" :download="`aylantirilgan-${fileName || 'rasm'}.png`" class="btn-primary !px-8 !py-2.5 inline-block">
              Yuklab olish (PNG)
            </a>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
