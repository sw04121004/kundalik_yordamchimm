<script setup>
import { useI18n } from '../i18n'
const { t } = useI18n()
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-brand-50/60 to-slate-50 dark:from-slate-900 dark:to-slate-950 px-4">
    <div class="text-center animate-fadeUp">
      <div class="text-6xl mb-4">🔎</div>
      <h1 class="text-2xl font-extrabold text-slate-800 dark:text-slate-100">{{ t('notfound.title') }}</h1>
      <p class="text-slate-500 dark:text-slate-400 mt-2">{{ t('notfound.description') }}</p>
      <router-link :to="{ name: 'landing' }" class="btn-primary inline-flex mt-6">{{ t('notfound.back') }}</router-link>
    </div>
  </div>
</template>
