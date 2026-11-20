<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'
import { useToolText } from '../../utils/toolText'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('soz-belgi-sanagich'))

const tx = useToolText({
  uz: {
    title: "So‘z va belgi sanagich",
    desc: "Matndagi so‘z, belgi va qatorlar sonini bilib oling",
    hint: "Matningizni pastdagi maydonga yozing yoki joylashtiring — so‘z, belgi va gaplar soni real vaqtda hisoblanadi.",
    label: "Matningizni kiriting",
    placeholder: "Matnni shu yerga kiriting yoki joylashtiring...",
    clear: "Tozalash",
    words: "So‘zlar",
    chars: "Belgilar",
    charsNoSpaces: "Belgilar (bo‘shliqsiz)",
    lines: "Qatorlar",
    sentences: "Gaplar",
  },
  ru: {
    title: "Счётчик слов и символов",
    desc: "Подсчёт слов, символов и строк в тексте",
    hint: "Введите или вставьте текст в поле ниже — количество слов, символов и предложений посчитается в реальном времени.",
    label: "Введите текст",
    placeholder: "Введите или вставьте текст сюда...",
    clear: "Очистить",
    words: "Слов",
    chars: "Символов",
    charsNoSpaces: "Без пробелов",
    lines: "Строк",
    sentences: "Предложений",
  },
  en: {
    title: "Word & Character Counter",
    desc: "Count words, characters, and lines in text",
    hint: "Type or paste your text into the field below — words, characters, and sentences are counted in real time.",
    label: "Enter your text",
    placeholder: "Type or paste text here...",
    clear: "Clear",
    words: "Words",
    chars: "Characters",
    charsNoSpaces: "Chars (no spaces)",
    lines: "Lines",
    sentences: "Sentences",
  },
})

const text = ref('')

const stats = computed(() => {
  const t = text.value
  const words = t.trim() ? t.trim().split(/\s+/).length : 0
  const chars = t.length
  const charsNoSpaces = t.replace(/\s/g, '').length
  const lines = t ? t.split(/\n/).length : 0
  const sentences = t.trim() ? (t.match(/[.!?]+/g) || []).length : 0
  return { words, chars, charsNoSpaces, lines, sentences }
})

function reset() {
  text.value = ''
}
</script>

<template>
  <ToolShell icon="🔡" :title="tx.title" :description="tx.desc" :hint="tx.hint">
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

      <button class="btn-secondary w-full" @click="reset">{{ tx.clear }}</button>

      <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 mt-2">
        <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">{{ tx.words }}</p>
          <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.words }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">{{ tx.chars }}</p>
          <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.chars }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">{{ tx.charsNoSpaces }}</p>
          <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.charsNoSpaces }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">{{ tx.lines }}</p>
          <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.lines }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 dark:bg-slate-700 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 dark:text-brand-300 font-medium">{{ tx.sentences }}</p>
          <p class="text-lg font-extrabold text-brand-800 dark:text-brand-200">{{ stats.sentences }}</p>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
