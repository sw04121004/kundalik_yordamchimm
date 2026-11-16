<script setup>
import { SUPPORTED_LANGUAGES, useI18n } from '../i18n'

const { language, setLanguage } = useI18n()

const displayLabels = {
  uz: "O'z",
  ru: "Ру",
  en: "En",
}
</script>

<template>
  <div class="inline-flex items-center rounded-xl border border-slate-200 dark:border-white/10 p-0.5 bg-white/70 dark:bg-slate-800/70 shadow-sm backdrop-blur-sm" role="group" aria-label="Tilni tanlash">
    <button
      v-for="item in SUPPORTED_LANGUAGES"
      :key="item.code"
      type="button"
      class="px-2 py-1 rounded-lg text-xs font-bold transition-all duration-150"
      :class="language === item.code
        ? 'bg-brand-500 text-white shadow-sm scale-105'
        : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5'"
      :aria-pressed="language === item.code"
      @click="setLanguage(item.code)"
    >
      {{ displayLabels[item.code] || item.code.toUpperCase() }}
    </button>
  </div>
</template>
