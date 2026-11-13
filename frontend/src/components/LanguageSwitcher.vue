<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { Globe2 } from 'lucide-vue-next'
import { SUPPORTED_LANGUAGES, useI18n } from '../i18n'

const { language, setLanguage } = useI18n()
const open = ref(false)
const root = ref(null)
const core = ['uz', 'ru', 'en']
const quick = computed(() => [...new Set([...(core.includes(language.value) ? [language.value] : [language.value]), ...core])])
const otherLanguages = computed(() => SUPPORTED_LANGUAGES.filter((item) => !core.includes(item.code)))
function outside(event) { if (root.value && !root.value.contains(event.target)) open.value = false }
function keydown(event) { if (event.key === 'Escape') open.value = false }
function choose(code) { setLanguage(code); open.value = false }
onMounted(() => { document.addEventListener('mousedown', outside); document.addEventListener('keydown', keydown) })
onUnmounted(() => { document.removeEventListener('mousedown', outside); document.removeEventListener('keydown', keydown) })
</script>
<template>
  <div ref="root" class="relative inline-flex items-center rounded-lg border border-slate-200 dark:border-white/10 p-0.5" role="group" aria-label="Language">
    <button v-for="code in quick" :key="code" type="button" class="px-1.5 py-1 rounded-md text-xs font-semibold uppercase transition-colors" :class="language === code ? 'bg-brand-100 text-brand-800 dark:bg-brand-900 dark:text-brand-100' : 'text-slate-500 hover:text-slate-800 dark:hover:text-white'" :aria-pressed="language === code" @click="choose(code)">{{ code }}</button>
    <button type="button" class="ml-0.5 p-1.5 rounded-md text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10" aria-label="More languages" aria-haspopup="listbox" :aria-expanded="open" @click="open = !open"><Globe2 class="w-4 h-4" /></button>
    <div v-if="open" class="absolute right-0 top-full mt-2 z-[70] w-48 max-h-72 overflow-auto rounded-xl border border-slate-200 bg-white p-1 shadow-xl dark:border-white/10 dark:bg-slate-900" role="listbox" aria-label="More languages">
      <button v-for="item in otherLanguages" :key="item.code" type="button" role="option" class="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm hover:bg-brand-50 dark:hover:bg-white/10" :aria-selected="language === item.code" @click="choose(item.code)"><span>{{ item.label }}</span><span class="text-xs uppercase text-slate-400">{{ item.code }}</span></button>
    </div>
  </div>
</template>
