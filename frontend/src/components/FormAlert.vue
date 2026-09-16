<script setup>
defineProps({
  message: { type: String, default: '' },
  type: { type: String, default: 'error' }, // 'error' | 'success'
})
</script>

<template>
  <transition name="page-fade">
    <div
      v-if="message"
      class="rounded-xl px-4 py-3 text-sm font-medium mb-4"
      :class="[
        type === 'error'
          ? 'bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 border border-red-100 dark:border-red-900/50 animate-shake'
          : 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-600 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-900/50',
      ]"
    >
      {{ message }}
    </div>
  </transition>
</template>
