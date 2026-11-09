<script setup>
import { computed } from 'vue'
import { Star, Wrench } from 'lucide-vue-next'
import { useServicesStore } from '../store/services'

const props = defineProps({
  icon: { type: String, default: '⚙️' },
  name: { type: String, required: true },
  description: { type: String, default: '' },
  to: { type: [String, Object], default: '#' },
  route: { type: String, default: '' },
  slug: { type: String, default: '' },
  showFavorite: { type: Boolean, default: true },
})

const servicesStore = useServicesStore()
const isFavorite = computed(() => props.slug ? servicesStore.isFavorite(props.slug) : false)
const target = computed(() => props.route || props.to || '#')

function toggleFavorite(event) {
  event.preventDefault()
  event.stopPropagation()
  if (props.slug) servicesStore.toggleFavorite(props.slug)
}
</script>

<template>
  <component
    :is="target === '#' ? 'div' : 'router-link'"
    :to="target !== '#' ? target : undefined"
    class="p-4 flex flex-col gap-3 hover:-translate-y-0.5 hover:shadow-md transition-all duration-200 cursor-pointer group relative bg-white dark:bg-[#191c22] border border-slate-200/80 dark:border-white/10 hover:border-brand-500/50 rounded-xl"
  >
    <button
      v-if="showFavorite && slug"
      class="absolute top-3 right-3 w-8 h-8 rounded-lg flex items-center justify-center transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 z-10 hover:bg-slate-100 dark:hover:bg-white/10"
      :class="isFavorite ? 'text-amber-600 dark:text-amber-400' : 'text-slate-400 dark:text-slate-500'"
      :title="isFavorite ? 'Sevimlilardan olib tashlash' : 'Sevimlilarga qo\'shish'"
      @click="toggleFavorite"
    >
      <Star class="w-4 h-4" :fill="isFavorite ? 'currentColor' : 'none'" aria-hidden="true" />
    </button>

    <div class="w-10 h-10 rounded-lg bg-brand-50 dark:bg-brand-900/30 border border-brand-100 dark:border-brand-800/70 flex items-center justify-center text-brand-700 dark:text-brand-300 transition-transform duration-200 group-hover:scale-105 shrink-0">
      <Wrench class="w-5 h-5" aria-hidden="true" />
    </div>

    <div class="pr-4 relative z-10">
      <h3 class="font-semibold text-sm text-slate-800 dark:text-slate-100 group-hover:text-brand-700 dark:group-hover:text-brand-300 transition-colors leading-snug">{{ name }}</h3>
      <p v-if="description" class="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed line-clamp-2">{{ description }}</p>
    </div>
  </component>
</template>
