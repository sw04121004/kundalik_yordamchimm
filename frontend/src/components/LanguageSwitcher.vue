<script setup>
import { useI18n } from '../i18n'
const { language, setLanguage } = useI18n()
</script>
<template>
  <div class="inline-flex items-center gap-0.5 rounded-lg border border-slate-200 dark:border-white/10 p-0.5" role="group" aria-label="Language">
    <button v-for="item in ['uz', 'ru', 'en']" :key="item" type="button" class="px-1.5 py-1 rounded-md text-xs font-semibold uppercase transition-colors" :class="language === item ? 'bg-brand-100 text-brand-800 dark:bg-brand-900 dark:text-brand-100' : 'text-slate-500'" :aria-pressed="language === item" @click="setLanguage(item)">{{ item }}</button>
  </div>
</template>
