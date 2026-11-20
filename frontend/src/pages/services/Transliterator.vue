<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'
import { ArrowLeftRight, Copy, Check } from 'lucide-vue-next'
import { useToolText } from '../../utils/toolText'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('transliterator'))

const tx = useToolText({
  uz: {
    title: "Transliterator & Tarjimon",
    desc: "Lotin va Kirill alifbosini bir-biriga o‘giring yoki boshqa tillarga tarjima qiling",
    hint: "Matnni kiriting va o‘girish rejimini tanlang — natija darhol ko‘rinadi.",
    latin: "Lotin",
    cyrillic: "Kirill (Rus/O'zb)",
    btnToTranslate: "Boshqa tillarga tarjima",
    btnToTranslit: "Lotin & Kirillga qaytish",
    placeholderLatin: "Bu yerga lotincha yozing...",
    placeholderCyrillic: "Бу ерга кирилча ёзинг...",
    placeholderTranslate: "Tarjima qilish uchun matn kiriting...",
    placeholderResult: "Natija bu yerda chiqadi...",
    errTranslate: "Tarjima qilishda xatolik yuz berdi.",
    errNetwork: "Tarmoq xatoligi yuz berdi.",
    langUz: "O'zbekcha",
    langRu: "Ruscha",
    langEn: "Inglizcha",
    langDe: "Nemischa",
    langFr: "Fransuzcha",
  },
  ru: {
    title: "Транслитератор и Переводчик",
    desc: "Конвертация между латиницей и кириллицей или перевод на другие языки",
    hint: "Введите текст и выберите режим — результат появится сразу.",
    latin: "Латиница",
    cyrillic: "Кириллица (Рус/Узб)",
    btnToTranslate: "Перевод на другие языки",
    btnToTranslit: "Вернуться к транслитерации",
    placeholderLatin: "Введите текст латиницей...",
    placeholderCyrillic: "Введите текст кириллицей...",
    placeholderTranslate: "Введите текст для перевода...",
    placeholderResult: "Результат появится здесь...",
    errTranslate: "Ошибка при переводе.",
    errNetwork: "Ошибка сети.",
    langUz: "Узбекский",
    langRu: "Русский",
    langEn: "Английский",
    langDe: "Немецкий",
    langFr: "Французский",
  },
  en: {
    title: "Transliterator & Translator",
    desc: "Convert between Latin and Cyrillic script or translate to other languages",
    hint: "Enter text and select mode — result updates immediately.",
    latin: "Latin",
    cyrillic: "Cyrillic (Rus/Uzb)",
    btnToTranslate: "Translate to other languages",
    btnToTranslit: "Back to transliteration",
    placeholderLatin: "Type in Latin script here...",
    placeholderCyrillic: "Type in Cyrillic script here...",
    placeholderTranslate: "Enter text to translate...",
    placeholderResult: "Result appears here...",
    errTranslate: "Error translating text.",
    errNetwork: "Network error occurred.",
    langUz: "Uzbek",
    langRu: "Russian",
    langEn: "English",
    langDe: "German",
    langFr: "French",
  },
})

const text = ref('')
const result = ref('')
const mode = ref('latinToCyrillic')
const copied = ref(false)

const fromLang = ref('uz')
const toLang = ref('en')
const isTranslating = ref(false)

const languages = computed(() => [
  { code: 'uz', name: tx.value.langUz },
  { code: 'ru', name: tx.value.langRu },
  { code: 'en', name: tx.value.langEn },
  { code: 'de', name: tx.value.langDe },
  { code: 'fr', name: tx.value.langFr },
])

const cyrillicToLatinMap = {
  'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'J', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'T': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'X', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': "'", 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'Ў': "O'", 'Қ': 'Q', 'Ғ': "G'", 'Ҳ': 'H',
  'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': "'", 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ў': "o'", 'қ': 'q', 'ғ': "g'", 'ҳ': 'h'
}

const latinToCyrillicMap = {
  'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е', 'Yo': 'Ё', 'J': 'Ж', 'Z': 'З', 'I': 'И', 'Y': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'F': 'Ф', 'X': 'Х', 'Ts': 'Ц', 'Ch': 'Ч', 'Sh': 'Ш', 'Shch': 'Щ', "E'": 'Э', 'Yu': 'Ю', 'Ya': 'Я', "O'": 'Ў', 'Q': 'Қ', "G'": 'Ғ', 'H': 'Ҳ',
  'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'yo': 'ё', 'j': 'ж', 'z': 'з', 'i': 'и', 'y': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'x': 'х', 'ts': 'ц', 'ch': 'ч', 'sh': 'ш', 'shch': 'щ', "e'": 'э', 'yu': 'ю', 'ya': 'я', "o'": 'ў', 'q': 'қ', "g'": 'ғ', 'h': 'ҳ'
}

async function translateText() {
  if (!text.value.trim()) {
    result.value = ''
    return
  }
  isTranslating.value = true
  try {
    const res = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(text.value)}&langpair=${fromLang.value}|${toLang.value}`)
    const data = await res.json()
    if (data && data.responseData) {
      result.value = data.responseData.translatedText
    } else {
      result.value = tx.value.errTranslate
    }
  } catch (err) {
    result.value = tx.value.errNetwork
  } finally {
    isTranslating.value = false
  }
}

let debounceTimer = null
function convert() {
  if (mode.value === 'translate') {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      translateText()
    }, 600)
    return
  }

  let output = text.value
  if (mode.value === 'latinToCyrillic') {
    output = output.replace(/Shch/g, 'Щ').replace(/shch/g, 'щ')
      .replace(/Ch/g, 'Ч').replace(/ch/g, 'ч')
      .replace(/Sh/g, 'Ш').replace(/sh/g, 'ш')
      .replace(/Yo/g, 'Ё').replace(/yo/g, 'ё')
      .replace(/Yu/g, 'Ю').replace(/yu/g, 'ю')
      .replace(/Ya/g, 'Я').replace(/ya/g, 'я')
      .replace(/Ts/g, 'Ц').replace(/ts/g, 'ц')
      .replace(/O['`ʻ’]/g, 'Ў').replace(/o['`ʻ’]/g, 'ў')
      .replace(/G['`ʻ’]/g, 'Ғ').replace(/g['`ʻ’]/g, 'ғ')

    let res = ''
    for (let i = 0; i < output.length; i++) {
      const char = output[i]
      res += latinToCyrillicMap[char] !== undefined ? latinToCyrillicMap[char] : char
    }
    result.value = res
  } else if (mode.value === 'cyrillicToLatin') {
    let res = ''
    for (let i = 0; i < output.length; i++) {
      const char = output[i]
      res += cyrillicToLatinMap[char] !== undefined ? cyrillicToLatinMap[char] : char
    }
    result.value = res
  }
}

function toggleMode() {
  if (mode.value === 'latinToCyrillic') {
    mode.value = 'cyrillicToLatin'
  } else if (mode.value === 'cyrillicToLatin') {
    mode.value = 'latinToCyrillic'
  } else {
    const temp = fromLang.value
    fromLang.value = toLang.value
    toLang.value = temp
  }
  const tempText = text.value
  text.value = result.value
  result.value = tempText
  convert()
}

function copyResult() {
  if (!result.value) return
  navigator.clipboard.writeText(result.value)
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 2000)
}
</script>

<template>
  <ToolShell icon="🔄" :title="tx.title" :description="tx.desc" :hint="tx.hint">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div class="flex items-center justify-between mb-2 px-1 flex-wrap gap-2">
        <div class="flex items-center gap-3">
          <select v-if="mode === 'translate'" v-model="fromLang" @change="convert" class="input w-auto text-sm">
            <option v-for="lang in languages" :key="lang.code" :value="lang.code">{{ lang.name }}</option>
          </select>
          <span v-else class="font-bold text-sm" :class="mode === 'latinToCyrillic' ? 'text-brand-600 dark:text-brand-400' : 'text-slate-500'">{{ tx.latin }}</span>

          <button @click="toggleMode" class="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
            <ArrowLeftRight class="w-4 h-4 text-slate-700 dark:text-slate-300" />
          </button>

          <select v-if="mode === 'translate'" v-model="toLang" @change="convert" class="input w-auto text-sm">
            <option v-for="lang in languages" :key="lang.code" :value="lang.code">{{ lang.name }}</option>
          </select>
          <span v-else class="font-bold text-sm" :class="mode === 'cyrillicToLatin' ? 'text-brand-600 dark:text-brand-400' : 'text-slate-500'">{{ tx.cyrillic }}</span>
        </div>
        <button @click="mode = 'translate'; text = ''; result = '';" v-if="mode !== 'translate'" class="btn-secondary text-sm">{{ tx.btnToTranslate }}</button>
        <button @click="mode = 'latinToCyrillic'; text = ''; result = '';" v-else class="btn-secondary text-sm">{{ tx.btnToTranslit }}</button>
      </div>

      <div>
        <textarea
          v-model="text"
          @input="convert"
          class="input min-h-[120px] resize-y text-base"
          :placeholder="mode === 'latinToCyrillic' ? tx.placeholderLatin : (mode === 'cyrillicToLatin' ? tx.placeholderCyrillic : tx.placeholderTranslate)"
        ></textarea>
      </div>

      <div class="relative mt-4">
        <textarea
          v-model="result"
          readonly
          class="input min-h-[120px] resize-y bg-slate-50 dark:bg-slate-800 text-base border-dashed"
          :placeholder="tx.placeholderResult"
        ></textarea>
        <button
          v-if="result"
          @click="copyResult"
          class="absolute top-3 right-3 p-2 rounded-lg bg-white dark:bg-slate-700 shadow-sm border border-slate-200 dark:border-slate-600 text-slate-500 hover:text-brand-600 transition-colors"
        >
          <Check v-if="copied" class="w-4 h-4 text-green-500" />
          <Copy v-else class="w-4 h-4" />
        </button>
      </div>
    </div>
  </ToolShell>
</template>
