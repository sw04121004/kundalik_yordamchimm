<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'
import { useToolText } from '../../utils/toolText'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('harf-ozgartirish'))

const tx = useToolText({
  uz: {
    title: "Katta/kichik harf o‘zgartirish",
    desc: "Matnni turli registrga o‘zgartiring",
    hint: "Avval matningizni kiriting, so‘ng kerakli tugmani bosing (BOSH HARF, kichik harf va h.k.) — natija shu yerning o‘zida ko‘rinadi.",
    label: "Matningizni kiriting",
    placeholder: "Matnni shu yerga kiriting...",
    upper: "BOSH HARF",
    lower: "kichik harf",
    titleCase: "Har Bir So‘z",
    sentenceCase: "Gap boshi",
    invert: "tEsKaRi",
    clear: "Tozalash",
  },
  ru: {
    title: "Смена регистра",
    desc: "Преобразование текста в разный регистр",
    hint: "Сначала введите текст, затем нажмите нужную кнопку (ПРОПИСНЫЕ, строчные и т.д.) — результат появится на месте.",
    label: "Введите текст",
    placeholder: "Введите текст сюда...",
    upper: "ПРОПИСНЫЕ",
    lower: "строчные",
    titleCase: "Каждое Слово",
    sentenceCase: "В начале предложения",
    invert: "иНВЕРСИЯ",
    clear: "Очистить",
  },
  en: {
    title: "Case Converter",
    desc: "Change text between different letter cases",
    hint: "Enter your text, then click the desired button (UPPERCASE, lowercase, etc.) — result appears right here.",
    label: "Enter your text",
    placeholder: "Enter text here...",
    upper: "UPPERCASE",
    lower: "lowercase",
    titleCase: "Title Case",
    sentenceCase: "Sentence case",
    invert: "iNVERT cASE",
    clear: "Clear",
  },
})

const text = ref('')

function toUpper() {
  text.value = text.value.toUpperCase()
}
function toLower() {
  text.value = text.value.toLowerCase()
}
function toTitleCase() {
  text.value = text.value
    .toLowerCase()
    .replace(/(^|\s)\S/g, (char) => char.toUpperCase())
}
function toSentenceCase() {
  const lower = text.value.toLowerCase()
  text.value = lower.replace(/(^\s*\w|[.!?]\s*\w)/g, (char) => char.toUpperCase())
}
function invertCase() {
  text.value = text.value
    .split('')
    .map((c) => (c === c.toUpperCase() ? c.toLowerCase() : c.toUpperCase()))
    .join('')
}

function reset() {
  text.value = ''
}
</script>

<template>
  <ToolShell icon="🔤" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div>
        <label class="label">{{ tx.label }}</label>
        <textarea
          v-model="text"
          rows="7"
          class="input resize-none"
          :placeholder="tx.placeholder"
        ></textarea>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <button class="btn-secondary" @click="toUpper">{{ tx.upper }}</button>
        <button class="btn-secondary" @click="toLower">{{ tx.lower }}</button>
        <button class="btn-secondary" @click="toTitleCase">{{ tx.titleCase }}</button>
        <button class="btn-secondary" @click="toSentenceCase">{{ tx.sentenceCase }}</button>
        <button class="btn-secondary" @click="invertCase">{{ tx.invert }}</button>
        <button class="btn-secondary" @click="reset">{{ tx.clear }}</button>
      </div>
    </div>
  </ToolShell>
</template>
