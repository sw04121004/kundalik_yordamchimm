<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const imageSrc = ref(null)
const fileName = ref('')
const grayscale = ref(0)
const brightness = ref(100)
const contrast = ref(100)
const sepia = ref(0)
const blur = ref(0)
const outputUrl = ref('')

function handleFile(e) {
  const file = e.target.files?.[0]
  if (!file) return
  fileName.value = file.name
  resetFilters()
  const reader = new FileReader()
  reader.onload = (ev) => {
    imageSrc.value = ev.target.result
    render()
  }
  reader.readAsDataURL(file)
}

function resetFilters() {
  grayscale.value = 0
  brightness.value = 100
  contrast.value = 100
  sepia.value = 0
  blur.value = 0
  render()
}

function render() {
  if (!imageSrc.value) return
  const img = new Image()
  img.onload = () => {
    const canvas = document.createElement('canvas')
    canvas.width = img.width
    canvas.height = img.height
    const ctx = canvas.getContext('2d')

    ctx.filter = `grayscale(${grayscale.value}%) brightness(${brightness.value}%) contrast(${contrast.value}%) sepia(${sepia.value}%) blur(${blur.value}px)`
    ctx.drawImage(img, 0, 0)

    outputUrl.value = canvas.toDataURL('image/jpeg', 0.92)
  }
  img.src = imageSrc.value
}
</script>

<template>
  <ToolShell icon="🎨" title="Rasm filtrlari va ranglar" description="Rasmga qora-oq, retro (sepia), yorqinlik, kontrast va xiralashtirish effektlarini bering" hint="Rasmni yuklang va kerakli slayderlar orqali filtrni sozlang.">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <div>
        <label class="label">Rasm tanlang</label>
        <input type="file" accept="image/*" class="input !py-2" @change="handleFile" />
      </div>

      <div v-if="imageSrc" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800">
          <div>
            <div class="flex justify-between text-xs font-semibold mb-1">
              <span>Qora-oq (Grayscale)</span>
              <span>{{ grayscale }}%</span>
            </div>
            <input v-model.number="grayscale" type="range" min="0" max="100" class="w-full accent-brand-600" @input="render" />
          </div>

          <div>
            <div class="flex justify-between text-xs font-semibold mb-1">
              <span>Retro (Sepia)</span>
              <span>{{ sepia }}%</span>
            </div>
            <input v-model.number="sepia" type="range" min="0" max="100" class="w-full accent-brand-600" @input="render" />
          </div>

          <div>
            <div class="flex justify-between text-xs font-semibold mb-1">
              <span>Yorqinlik (Brightness)</span>
              <span>{{ brightness }}%</span>
            </div>
            <input v-model.number="brightness" type="range" min="20" max="200" class="w-full accent-brand-600" @input="render" />
          </div>

          <div>
            <div class="flex justify-between text-xs font-semibold mb-1">
              <span>Kontrast (Contrast)</span>
              <span>{{ contrast }}%</span>
            </div>
            <input v-model.number="contrast" type="range" min="20" max="200" class="w-full accent-brand-600" @input="render" />
          </div>
        </div>

        <div class="flex justify-end">
          <button class="btn-secondary !text-xs !py-1.5" @click="resetFilters">Filtrlarni tozalash</button>
        </div>

        <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 text-center space-y-3">
          <img :src="outputUrl || imageSrc" alt="Preview" class="max-h-72 mx-auto rounded-lg shadow-sm" />
          <div>
            <a :href="outputUrl" :download="`filtr-${fileName || 'rasm'}.jpg`" class="btn-primary !px-8 !py-2.5 inline-block">
              Saqlash va Yuklab olish
            </a>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
