<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'
import { useToolText } from '../../utils/toolText'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('matnni-tozalash'))

const tx = useToolText({
  uz: {
    title: "Matnni tozalash",
    desc: "Ortiqcha bo‘shliq va bo‘sh qatorlarni tozalang",
    hint: "Matnni joylashtiring, kerakli katakchalarni belgilang va «Tozalash»ni bosing — ortiqcha bo‘shliqlar olib tashlanadi.",
    label: "Matningizni kiriting",
    placeholder: "Tozalanadigan matnni shu yerga joylashtiring...",
    trim: "Qator boshi/oxiridagi bo‘shliqlar",
    removeEmpty: "Bo‘sh qatorlarni olib tashlash",
    collapse: "Ortiqcha bo‘shliqlarni siqish",
    cleanBtn: "Tozalash",
    resetBtn: "Bekor qilish",
  },
  ru: {
    title: "Очистка текста",
    desc: "Удаление лишних пробелов и пустых строк",
    hint: "Вставьте текст, выберите нужные параметры и нажмите «Очистить» — лишние пробелы и строки удалятся.",
    label: "Введите текст",
    placeholder: "Вставьте текст для очистки сюда...",
    trim: "Пробелы в начале/конце строк",
    removeEmpty: "Удалять пустые строки",
    collapse: "Сжимать повторяющиеся пробелы",
    cleanBtn: "Очистить",
    resetBtn: "Сбросить",
  },
  en: {
    title: "Text Cleaner",
    desc: "Remove extra whitespace and blank lines",
    hint: "Paste your text, check the desired options and click 'Clean' — extra spaces and blank lines will be removed.",
    label: "Enter your text",
    placeholder: "Paste text to clean here...",
    trim: "Trim leading/trailing line spaces",
    removeEmpty: "Remove empty lines",
    collapse: "Collapse duplicate spaces",
    cleanBtn: "Clean",
    resetBtn: "Reset",
  },
})

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
  <ToolShell icon="🧹" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div>
        <label class="label">{{ tx.label }}</label>
        <textarea
          v-model="text"
          rows="8"
          class="input resize-none"
          :placeholder="tx.placeholder"
        ></textarea>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 text-sm text-slate-600 dark:text-slate-300">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="trimLines" class="rounded text-brand-600 focus:ring-brand-400" />
          {{ tx.trim }}
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="removeEmptyLines" class="rounded text-brand-600 focus:ring-brand-400" />
          {{ tx.removeEmpty }}
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="collapseSpaces" class="rounded text-brand-600 focus:ring-brand-400" />
          {{ tx.collapse }}
        </label>
      </div>

      <div class="flex gap-3 pt-2">
        <button class="btn-primary flex-1" @click="clean">{{ tx.cleanBtn }}</button>
        <button class="btn-secondary" @click="reset">{{ tx.resetBtn }}</button>
      </div>
    </div>
  </ToolShell>
</template>
