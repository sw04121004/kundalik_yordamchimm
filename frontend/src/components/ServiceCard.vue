<script setup>
import { computed } from 'vue'
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
    class="p-5 flex flex-col gap-3.5 hover:-translate-y-2.5 hover:scale-[1.03] hover:shadow-[0_20px_40px_-15px_rgba(var(--brand-500),0.3)] dark:hover:shadow-[0_20px_45px_-15px_rgba(var(--brand-500),0.4)] transition-all duration-300 ease-out cursor-pointer group relative overflow-hidden bg-white/95 dark:bg-[#161c28]/95 backdrop-blur-xl border border-slate-200/90 dark:border-slate-800/90 hover:border-brand-400 dark:hover:border-brand-400 rounded-2xl"
  >
    <!-- Dynamic Theme Accent Glow Ring on Card -->
    <div class="absolute inset-0 rounded-2xl border-2 border-brand-400/0 group-hover:border-brand-400/40 dark:group-hover:border-brand-400/50 transition-all duration-300 pointer-events-none"></div>

    <!-- Dynamic Theme Accent Bottom Line with Pulsing Glow -->
    <div class="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-brand-400 dark:via-brand-300 to-transparent opacity-40 group-hover:opacity-100 group-hover:h-[4px] group-hover:shadow-[0_0_12px_rgb(var(--brand-400))] transition-all duration-300"></div>

    <!-- Dynamic Theme Ambient Glow Expanding on Hover -->
    <div class="absolute -right-6 -bottom-6 w-36 h-36 rounded-full bg-brand-500/0 group-hover:bg-brand-500/25 blur-2xl transition-all duration-500 pointer-events-none group-hover:scale-150"></div>
    <div class="absolute -left-6 -top-6 w-28 h-28 rounded-full bg-brand-400/0 group-hover:bg-brand-400/20 blur-xl transition-all duration-500 pointer-events-none group-hover:scale-125"></div>

    <!-- Shimmer light sweep across card on hover -->
    <div class="absolute inset-0 -translate-x-full group-hover:translate-x-full duration-700 ease-in-out bg-gradient-to-r from-transparent via-brand-300/20 dark:via-brand-400/15 to-transparent transition-transform pointer-events-none"></div>

    <!-- Favorite star button with spring scale & spin -->
    <button
      v-if="showFavorite && slug"
      class="absolute top-3 right-3 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-125 focus:outline-none z-10 hover:bg-brand-50 dark:hover:bg-brand-950/40 active:rotate-45"
      :class="isFavorite ? 'text-amber-400 scale-110' : 'text-slate-300 dark:text-slate-600 opacity-0 group-hover:opacity-100'"
      :title="isFavorite ? 'Sevimlilardan olib tashlash' : 'Sevimlilarga qo\'shish'"
      @click="toggleFavorite"
    >
      <svg class="w-4 h-4 fill-current transition-transform duration-300" viewBox="0 0 24 24">
        <path v-if="isFavorite" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        <path v-else stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
      </svg>
    </button>

    <!-- Dynamic Theme Glowing Icon Box -->
    <div class="w-13 h-13 rounded-2xl bg-gradient-to-br from-brand-400/20 via-brand-500/20 to-brand-600/20 dark:from-brand-500/30 dark:via-brand-600/25 dark:to-brand-700/25 border border-brand-300/50 dark:border-brand-400/40 flex items-center justify-center text-2xl transition-all duration-300 group-hover:scale-115 group-hover:rotate-6 group-hover:shadow-[0_0_20px_rgb(var(--brand-500)/0.4)] group-hover:border-brand-400 group-hover:from-brand-400/35 dark:group-hover:from-brand-500/45 shrink-0">
      <span class="transform transition-transform duration-300 group-hover:scale-110 select-none">{{ icon }}</span>
    </div>

    <!-- Text -->
    <div class="pr-4 relative z-10">
      <h3 class="font-bold text-sm text-slate-800 dark:text-slate-100 group-hover:text-brand-600 dark:group-hover:text-brand-300 transition-colors leading-snug">{{ name }}</h3>
      <p v-if="description" class="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed line-clamp-2">{{ description }}</p>
    </div>
  </component>
</template>
