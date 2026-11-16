<script setup>
import { computed } from 'vue'
import AppHeader from '../components/AppHeader.vue'
import { useI18n } from '../i18n'
import { useRoute } from 'vue-router'

const { t } = useI18n()
const route = useRoute()
const isPrivacy = computed(() => route.path.endsWith('/privacy'))
</script>

<template>
  <AppHeader />
  <main class="max-w-3xl mx-auto px-4 py-12 space-y-8">
    <h1 class="text-3xl font-bold text-slate-900 dark:text-white">{{ isPrivacy ? t('legal.privacy') : t('legal.terms') }}</h1>
    <section v-if="isPrivacy" class="card p-6 space-y-4">
      <p class="text-slate-700 dark:text-slate-300 leading-relaxed">{{ t('legal.data') }}</p>
      <p class="text-slate-700 dark:text-slate-300 leading-relaxed">{{ t('legal.third') }}</p>
    </section>
    <section v-else class="card p-6">
      <p class="text-slate-700 dark:text-slate-300 leading-relaxed">{{ t('legal.use') }}</p>
    </section>
    <section class="card p-6">
      <h2 class="text-xl font-semibold mb-2 text-slate-900 dark:text-white">{{ t('legal.contact') }}</h2>
      <p class="text-slate-700 dark:text-slate-300 mb-3">{{ t('legal.contactText') }}</p>
      <a class="text-brand-700 dark:text-brand-300 underline font-semibold" href="https://github.com/sw04121004/kundalik_yordamchimm/issues" target="_blank" rel="noopener noreferrer">GitHub Issues</a>
    </section>
  </main>
</template>
