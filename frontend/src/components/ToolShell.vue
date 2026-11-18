<script setup>
import { computed } from 'vue'
import { Sparkles } from 'lucide-vue-next'
import { useI18n } from '../i18n'

const { t } = useI18n()

const props = defineProps({
  icon: { type: String, default: '⚙️' },
  title: { type: String, required: true },
  description: { type: String, default: '' },
  hint: { type: String, default: '' },
  slug: { type: String, default: '' },
})

const displayTitle = computed(() => {
  if (props.slug) {
    const byTool = t(`tool.${props.slug}.title`)
    if (byTool && byTool !== `tool.${props.slug}.title`) return byTool
    const bySvc = t(`svc.${props.slug}.name`)
    if (bySvc && bySvc !== `svc.${props.slug}.name`) return bySvc
  }
  return t(props.title) || props.title
})

const displayDescription = computed(() => {
  if (props.slug) {
    const byTool = t(`tool.${props.slug}.desc`)
    if (byTool && byTool !== `tool.${props.slug}.desc`) return byTool
    const bySvc = t(`svc.${props.slug}.desc`)
    if (bySvc && bySvc !== `svc.${props.slug}.desc`) return bySvc
  }
  return t(props.description) || props.description
})

const displayHint = computed(() => {
  if (props.slug) {
    const bySlug = t(`tool.${props.slug}.hint`)
    if (bySlug && bySlug !== `tool.${props.slug}.hint`) return bySlug
  }
  return t(props.hint) || props.hint
})
</script>

<template>
  <div class="relative min-h-screen bg-gradient-to-b from-brand-50/60 to-slate-50 dark:from-[#1b2230] dark:to-[#111318] overflow-hidden">
    <div class="hidden dark:block absolute pointer-events-none w-72 h-72 -top-10 -right-10 rounded-full bg-brand-500/10 blur-3xl" aria-hidden="true"></div>
    <slot name="header" />
    <main class="relative max-w-2xl mx-auto px-4 sm:px-6 py-10 animate-fadeUp">
      <router-link
        :to="{ name: 'dashboard' }"
        class="inline-flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400 hover:text-brand-600 transition mb-6"
      >
        ← {{ t('common.back') }}
      </router-link>

      <div class="flex items-center gap-3 mb-2">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-100 to-emerald-50 dark:from-brand-900/60 dark:to-emerald-950/50 border border-brand-200/70 dark:border-brand-700/50 flex items-center justify-center text-brand-700 dark:text-brand-300 shadow-sm animate-fadeUp transition-transform duration-300 hover:scale-105">
          <Sparkles class="w-6 h-6" aria-hidden="true" />
        </div>
        <div>
          <h1 class="text-xl font-extrabold text-slate-800 dark:text-slate-100">{{ displayTitle }}</h1>
          <p v-if="displayDescription" class="text-sm text-slate-500 dark:text-slate-400">{{ displayDescription }}</p>
        </div>
      </div>

      <div
        v-if="displayHint"
        class="mt-5 flex items-start gap-2.5 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-900/40 text-amber-800 dark:text-amber-300 text-sm px-4 py-3 animate-fadeUp"
      >
        <span class="text-base leading-none mt-0.5">💡</span>
        <span>{{ displayHint }}</span>
      </div>

      <div class="glass-surface p-6 sm:p-7 mt-6 animate-fadeUp">
        <slot />
      </div>
    </main>
  </div>
</template>
