<script setup>
import { ref } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'

const imageSrc = ref(null)
const quality = ref(60)
const originalSize = ref(0)
const compressedSize = ref(0)
const outputUrl = ref('')
const fileName = ref('')

function handleFile(e) {
  const file = e.target.files?.[0]
  if (!file) return
  fileName.value = file.name
  originalSize.value = file.size
  const reader = new FileReader()
  reader.onload = (ev) => {
    imageSrc.value = ev.target.result
    compress()
  }
  reader.readAsDataURL(file)
}

function compress() {
  if (!imageSrc.value) return
  const img = new Image()
  img.onload = () => {
    const canvas = document.createElement('canvas')
    canvas.width = img.width
    canvas.height = img.height
    const ctx = canvas.getContext('2d')
    ctx.drawImage(img, 0, 0)
    canvas.toBlob(
      (blob) => {
        if (!blob) return
        compressedSize.value = blob.size
        outputUrl.value = URL.createObjectURL(blob)
      },
      'image/jpeg',
      quality.value / 100
    )
  }
  img.src = imageSrc.value
}

function formatBytes(bytes) {
  if (!bytes) return '0 KB'
  const kb = bytes / 1024
  if (kb < 1024) return `${kb.toFixed(1)} KB`
  return `${(kb / 1024).toFixed(2)} MB`
}
</script>

<template>
  <ToolShell icon="🗜️" title="Rasmni siqish" description="Rasm sifatini deyarli yo'qotmagan holda uning hajmini bir necha barobar kichraytiring" hint="Rasmni yuklang va sifat darajasini o'zgartiring.">
    <template #header><AppHeader /></template>

    <div class="space-y-5">
      <div>
        <label class="label">Rasm tanlang</label>
        <input type="file" accept="image/*" class="input !py-2" @change="handleFile" />
      </div>

      <div v-if="imageSrc" class="space-y-4">
        <div>
          <div class="flex justify-between text-sm font-semibold mb-1">
            <span>Sifat darajasi: {{ quality }}%</span>
            <span class="text-brand-600 dark:text-brand-400 font-bold">
              {{ originalSize ? `Tejam: -${Math.round((1 - compressedSize / originalSize) * 100)}%` : '' }}
            </span>
          </div>
          <input v-model.number="quality" type="range" min="10" max="90" step="5" class="w-full accent-brand-600" @input="compress" />
        </div>

        <div class="grid grid-cols-2 gap-3 p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 text-center">
          <div>
            <p class="text-xs text-slate-400">Asl hajmi</p>
            <p class="font-bold text-slate-700 dark:text-slate-200">{{ formatBytes(originalSize) }}</p>
          </div>
          <div>
            <p class="text-xs text-slate-400">Yangi hajmi</p>
            <p class="font-bold text-green-600 dark:text-green-400">{{ formatBytes(compressedSize) }}</p>
          </div>
        </div>

        <div v-if="outputUrl" class="text-center pt-2">
          <a :href="outputUrl" :download="`siqilgan-${fileName}`" class="btn-primary !px-8 !py-2.5 inline-block w-full">
            Yuklab olish
          </a>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
