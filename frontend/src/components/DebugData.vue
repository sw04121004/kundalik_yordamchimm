<template>
  <pre class="bg-white/80 dark:bg-[#111] p-4 rounded-md overflow-auto text-sm">
    {{ JSON.stringify($store.useServicesStore().categories, null, 2) }}
  </pre>
</template>

<script setup>
import { useServicesStore } from '../store/services'
const servicesStore = useServicesStore()
</script>

<style scoped>
pre { max-height: 400px; }
</style>
