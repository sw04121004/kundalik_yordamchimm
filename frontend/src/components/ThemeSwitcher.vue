<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useThemeStore, ACCENT_PRESETS } from '../store/theme'

const theme = useThemeStore()
const open = ref(false)
const dropdownRef = ref(null)

const currentPreset = computed(() => ACCENT_PRESETS[theme.accent] || ACCENT_PRESETS.blue)

function choose(name) {
  theme.setAccent(name)
  // Optional: automatically close after selection, or leave open for preview
  // open.value = false 
}

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    open.value = false
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})
onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<template>
  <div class="relative z-50" ref="dropdownRef">
    <button
      class="relative w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-105 active:scale-95 shadow-lg group focus:outline-none"
      title="Ko‘rinishni sozlash"
      @click="open = !open"
    >
      <span
        class="absolute inset-0 rounded-full ring-2 ring-offset-2 ring-offset-slate-50 dark:ring-offset-[#0B1120] transition-all duration-300 group-hover:ring-4"
        :style="{ '--tw-ring-color': currentPreset.swatch }"
      ></span>
      <span
        class="w-6 h-6 rounded-full transition-all duration-300"
        :style="{ background: currentPreset.swatch, boxShadow: `0 0 16px ${currentPreset.swatch}80` }"
      ></span>
    </button>

    <transition name="palette">
      <div
        v-if="open"
        class="absolute right-0 mt-4 backdrop-blur-2xl bg-white/80 dark:bg-slate-900/80 border border-white/50 dark:border-white/10 shadow-[0_8px_32px_-8px_rgba(0,0,0,0.15)] dark:shadow-[0_8px_32px_-8px_rgba(0,0,0,0.5)] p-5 rounded-2xl w-72 origin-top-right transform transition-all"
      >
        <p class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-4 px-1 flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>
          Mavzu Rangi
        </p>
        <div class="grid grid-cols-5 gap-3 mb-5">
          <button
            v-for="(preset, key) in ACCENT_PRESETS"
            :key="key"
            class="relative w-9 h-9 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-125 focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
            :style="{ background: preset.swatch, '--tw-ring-color': preset.swatch }"
            :title="preset.label"
            @click="choose(key)"
          >
            <span
              v-if="theme.accent === key"
              class="absolute -inset-1.5 rounded-full ring-2 transition-all duration-300 animate-pulse-slow"
              :style="{ '--tw-ring-color': preset.swatch }"
            ></span>
            <svg v-if="theme.accent === key" class="w-4 h-4 text-white drop-shadow-md animate-pop-in" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
          </button>
        </div>

        <div class="border-t border-slate-200/50 dark:border-slate-700/50 pt-4">
          <button
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-slate-100/50 dark:hover:bg-white/5 transition-all duration-300 group focus:outline-none"
            @click="theme.toggleDark()"
          >
            <span class="flex items-center gap-3 text-sm font-semibold text-slate-700 dark:text-slate-200">
              <span class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 transition-colors group-hover:bg-brand-50 dark:group-hover:bg-brand-900/30 text-brand-500">
                <svg v-if="theme.isDark" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
              </span>
              {{ theme.isDark ? 'Tungi rejim' : 'Kunduzgi rejim' }}
            </span>
            <span
              class="w-10 h-6 rounded-full relative transition-all duration-300 shadow-inner"
              :style="{ background: theme.isDark ? currentPreset.swatch : '' }"
              :class="theme.isDark ? 'opacity-100' : 'bg-slate-300 dark:bg-slate-600'"
            >
              <span
                class="absolute top-1 w-4 h-4 rounded-full bg-white transition-all duration-300 shadow-md"
                :class="theme.isDark ? 'left-5' : 'left-1'"
              ></span>
            </span>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.palette-enter-active,
.palette-leave-active {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.palette-enter-from,
.palette-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}
.animate-pulse-slow {
  animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
@keyframes pulse-ring {
  0% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0.5; }
}
.animate-pop-in {
  animation: pop-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}
@keyframes pop-in {
  0% { transform: scale(0.5); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
</style>
