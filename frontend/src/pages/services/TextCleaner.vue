<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('matnni-tozalash'))

const text = ref('')
const removeEmptyLines = ref(true)
const trimLines = ref(true)
const collapseSpaces = ref(true)

function clean() {
  let lines = text.value.split('\n')

  if (trimLines.value) {
    lines = lines.map((l) => l.trim())
  }
  if (removeEmptyLines.value) {
    lines = lines.filter((l) => l.length > 0)
  }

  let result = lines.join('\n')

  if (collapseSpaces.value) {
    result = result.replace(/[ \t]+/g, ' ')
  }

  text.value = result
}

function reset() {
  text.value = ''
}
</script>

<template>
  <ToolShell icon="🧹" title="Matnni tozalash" description="Ortiqcha bo‘shliq va bo‘sh qatorlarni tozalang" hint="Matnni joylashtiring, kerakli katakchalarni belgilang va «Tozalash»ni bosing — ortiqcha bo‘shliqlar olib tashlanadi.">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div>
        <label class="label">Matningizni kiriting</label>
        <textarea
          v-model="text"
          rows="8"
          class="input resize-none"
          placeholder="Tozalanadigan matnni shu yerga joylashtiring..."
        ></textarea>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 text-sm text-slate-600">
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="trimLines" class="rounded text-brand-600 focus:ring-brand-400" />
          Qator boshi/oxiridagi bo‘shliqlar
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="removeEmptyLines" class="rounded text-brand-600 focus:ring-brand-400" />
          Bo‘sh qatorlarni olib tashlash
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="collapseSpaces" class="rounded text-brand-600 focus:ring-brand-400" />
          Ortiqcha bo‘shliqlarni siqish
        </label>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="clean">Tozalash</button>
        <button class="btn-secondary" @click="reset">Bekor qilish</button>
      </div>
    </div>
  </ToolShell>

</template>
