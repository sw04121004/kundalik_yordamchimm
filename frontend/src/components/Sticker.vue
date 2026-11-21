<template>
  <img
    :src="src"
    :alt="alt"
    class="inline-block w-8 h-8 md:w-10 md:h-10 object-cover rounded-full transition-transform duration-300 hover:scale-110 hover:rotate-3 animate-pulseBounce"
  />
</template>

<script setup lang="ts">
interface Props {
  src: string;
  alt?: string;
}
defineProps<Props>();
</script>

<style scoped>
@keyframes pulseBounce {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-3px) scale(1.05); }
}
.animate-pulseBounce { animation: pulseBounce 1.8s ease-in-out infinite; }
</style>
