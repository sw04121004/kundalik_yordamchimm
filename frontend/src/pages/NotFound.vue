<script setup>
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-brand-50/60 to-slate-50 dark:from-slate-900 dark:to-slate-950 px-4">
    <div class="text-center animate-fadeUp">
      <div class="text-6xl mb-4">🔎</div>
      <h1 class="text-2xl font-extrabold text-slate-800 dark:text-slate-100">Sahifa topilmadi</h1>
      <p class="text-slate-500 dark:text-slate-400 mt-2">Siz izlagan sahifa mavjud emas yoki ko‘chirilgan.</p>
      <router-link :to="{ name: 'landing' }" class="btn-primary inline-flex mt-6">Bosh sahifaga qaytish</router-link>
    </div>
  </div>
</template>
