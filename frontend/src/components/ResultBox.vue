<script setup>
import { computed } from 'vue'
import { useI18n } from '../i18n'

const props = defineProps({
  label: { type: String, default: '' },
  value: { type: [String, Number], default: '' },
})

const { t } = useI18n()

const displayLabel = computed(() => {
  if (props.label && props.label !== 'Natija') {
    return t(props.label) || props.label
  }
  return t('common.result')
})
</script>

<template>
  <div
    v-if="value !== '' && value !== null && value !== undefined"
    :key="value"
    class="mt-5 rounded-xl bg-gradient-to-br from-brand-50 to-brand-100/60 dark:from-slate-700 dark:to-slate-700/60 border border-brand-100 dark:border-slate-600 px-5 py-4 animate-resultPop"
  >
    <p class="text-xs font-medium text-brand-600 dark:text-brand-300 uppercase tracking-wide">{{ displayLabel }}</p>
    <p class="text-2xl font-extrabold text-brand-800 dark:text-brand-200 mt-1 break-words">{{ value }}</p>
  </div>
</template>
