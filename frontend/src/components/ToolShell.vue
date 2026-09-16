<script setup>
defineProps({
  icon: { type: String, default: '⚙️' },
  title: { type: String, required: true },
  description: { type: String, default: '' },
  hint: { type: String, default: '' },
})
</script>

<template>
  <div class="relative min-h-screen bg-gradient-to-b from-brand-50/60 to-slate-50 dark:from-slate-950 dark:to-slate-950 overflow-hidden">
    <div class="hidden dark:block absolute pointer-events-none w-72 h-72 -top-10 -right-10 rounded-full bg-brand-500/10 blur-3xl" aria-hidden="true"></div>
    <slot name="header" />
    <main class="relative max-w-2xl mx-auto px-4 sm:px-6 py-10 animate-fadeUp">
      <router-link
        :to="{ name: 'dashboard' }"
        class="inline-flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400 hover:text-brand-600 transition mb-6"
      >
        ← Orqaga
      </router-link>

      <div class="flex items-center gap-3 mb-2">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-2xl shadow-soft animate-fadeUp transition-transform duration-300 hover:scale-110 hover:rotate-6">
          {{ icon }}
        </div>
        <div>
          <h1 class="text-xl font-extrabold text-slate-800 dark:text-slate-100">{{ title }}</h1>
          <p v-if="description" class="text-sm text-slate-500 dark:text-slate-400">{{ description }}</p>
        </div>
      </div>

      <div
        v-if="hint"
        class="mt-5 flex items-start gap-2.5 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-900/40 text-amber-800 dark:text-amber-300 text-sm px-4 py-3 animate-fadeUp"
      >
        <span class="text-base leading-none mt-0.5">💡</span>
        <span>{{ hint }}</span>
      </div>

      <div class="glass-surface p-6 sm:p-7 mt-6 animate-fadeUp">
        <slot />
      </div>
    </main>
  </div>
</template>
