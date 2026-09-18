<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'
import { ArrowLeftRight, Copy, Check } from 'lucide-vue-next'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('transliterator'))

const text = ref('')
const result = ref('')
const mode = ref('latinToCyrillic')
const copied = ref(false)

// O'zbek lotin va kirill harflari xaritasi
const cyrillicToLatinMap = {
  'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'J', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'X', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '\'', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'Ў': 'O\'', 'Қ': 'Q', 'Ғ': 'G\'', 'Ҳ': 'H',
  'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '\'', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ў': 'o\'', 'қ': 'q', 'ғ': 'g\'', 'ҳ': 'h'
}

const latinToCyrillicMap = {
  'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е', 'Yo': 'Ё', 'J': 'Ж', 'Z': 'З', 'I': 'И', 'Y': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'F': 'Ф', 'X': 'Х', 'Ts': 'Ц', 'Ch': 'Ч', 'Sh': 'Ш', 'Shch': 'Щ', 'E\'': 'Э', 'Yu': 'Ю', 'Ya': 'Я', 'O\'': 'Ў', 'Q': 'Қ', 'G\'': 'Ғ', 'H': 'Ҳ',
  'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'yo': 'ё', 'j': 'ж', 'z': 'з', 'i': 'и', 'y': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'x': 'х', 'ts': 'ц', 'ch': 'ч', 'sh': 'ш', 'shch': 'щ', 'e\'': 'э', 'yu': 'ю', 'ya': 'я', 'o\'': 'ў', 'q': 'қ', 'g\'': 'ғ', 'h': 'ҳ'
}

function convert() {
  let output = text.value
  
  if (mode.value === 'cyrillicToLatin') {
    // Special rules for 'Е' and 'е' at the beginning of words
    output = output.replace(/\bЕ/g, 'Ye').replace(/\bе/g, 'ye');
    
    let resultText = ''
    for (let i = 0; i < output.length; i++) {
      resultText += cyrillicToLatinMap[output[i]] !== undefined ? cyrillicToLatinMap[output[i]] : output[i]
    }
    result.value = resultText
  } else {
    // Replace multi-character combinations first
    const multiChars = Object.keys(latinToCyrillicMap).filter(k => k.length > 1).sort((a, b) => b.length - a.length)
    
    for (const lat of multiChars) {
      const regex = new RegExp(lat.replace(/'/g, "\\'"), 'g')
      output = output.replace(regex, latinToCyrillicMap[lat])
    }
    
    let resultText = ''
    for (let i = 0; i < output.length; i++) {
      resultText += latinToCyrillicMap[output[i]] !== undefined ? latinToCyrillicMap[output[i]] : output[i]
    }
    result.value = resultText
  }
}

function toggleMode() {
  mode.value = mode.value === 'cyrillicToLatin' ? 'latinToCyrillic' : 'cyrillicToLatin'
  const temp = text.value
  text.value = result.value
  result.value = ''
  if (text.value) convert()
}

async function copyResult() {
  if (!result.value) return
  try {
    await navigator.clipboard.writeText(result.value)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
  } catch (err) {}
}
</script>

<template>
  <ToolShell icon="🔄" title="Kirill & Lotin / Tarjimon" description="Matnlarni alifbolar orasida tezda o'giring" hint="Boshqa tillar (Nemis, Fransuz, Ingliz, Rus) va murakkab tarjimalar uchun AI Yordamchidan so'rang!">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div class="flex items-center justify-between mb-2 px-1">
        <div class="flex items-center gap-3">
          <span class="font-bold text-sm" :class="mode === 'latinToCyrillic' ? 'text-brand-600 dark:text-brand-400' : 'text-slate-500'">Lotin</span>
          <button @click="toggleMode" class="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
            <ArrowLeftRight class="w-4 h-4 text-slate-700 dark:text-slate-300" />
          </button>
          <span class="font-bold text-sm" :class="mode === 'cyrillicToLatin' ? 'text-brand-600 dark:text-brand-400' : 'text-slate-500'">Kirill (Rus/O'zb)</span>
        </div>
      </div>

      <div>
        <textarea
          v-model="text"
          @input="convert"
          class="input min-h-[120px] resize-y text-base"
          :placeholder="mode === 'latinToCyrillic' ? 'Bu yerga lotincha yozing...' : 'Бу ерга кирилча ёзинг...'"
        ></textarea>
      </div>

      <div class="relative mt-4">
        <textarea
          v-model="result"
          readonly
          class="input min-h-[120px] resize-y bg-slate-50 dark:bg-slate-800 text-base border-dashed"
          placeholder="Natija bu yerda chiqadi..."
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
      
      <div class="mt-6 p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800/50">
        <h3 class="font-bold text-blue-800 dark:text-blue-300 mb-1">🌍 Boshqa tillarga tarjima kerakmi?</h3>
        <p class="text-sm text-blue-600 dark:text-blue-400">
          Nemis, Fransuz, Rus yoki har qanday boshqa tilga tarjima qilish uchun orqaga qaytib <b>AI Yordamchi</b> ga o'ting. Unga shunchaki <i>"Shu matnni fransuz tiliga tarjima qilib ber"</i> desangiz bas!
        </p>
      </div>
    </div>
  </ToolShell>
</template>
