<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('soz-belgi-sanagich'))

const text = ref('')

const stats = computed(() => {
  const t = text.value
  const words = t.trim() ? t.trim().split(/\s+/).length : 0
  const chars = t.length
  const charsNoSpaces = t.replace(/\s/g, '').length
  const lines = t ? t.split(/\n/).length : 0
  const sentences = t.trim() ? (t.match(/[.!?]+/g) || []).length : 0
  return { words, chars, charsNoSpaces, lines, sentences }
})

function reset() {
  text.value = ''
}
</script>

<template>
  <ToolShell icon="🔤" title="So‘z va belgi sanagich" description="Matndagi so‘z, belgi va qatorlar sonini bilib oling" hint="Matningizni pastdagi maydonga yozing yoki joylashtiring — so‘z, belgi va gaplar soni real vaqtda hisoblanadi.">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div>
        <label class="label">Matningizni kiriting</label>
        <textarea
          v-model="text"
          rows="8"
          class="input resize-none"
          placeholder="Matnni shu yerga kiriting yoki joylashtiring..."
        ></textarea>
      </div>

      <button class="btn-secondary w-full" @click="reset">Tozalash</button>

      <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 mt-2">
        <div class="rounded-xl bg-brand-50 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 font-medium">So‘zlar</p>
          <p class="text-lg font-extrabold text-brand-800">{{ stats.words }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 font-medium">Belgilar</p>
          <p class="text-lg font-extrabold text-brand-800">{{ stats.chars }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 font-medium">Belgilar (bo‘shliqsiz)</p>
          <p class="text-lg font-extrabold text-brand-800">{{ stats.charsNoSpaces }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 font-medium">Qatorlar</p>
          <p class="text-lg font-extrabold text-brand-800">{{ stats.lines }}</p>
        </div>
        <div class="rounded-xl bg-brand-50 px-3 py-3 text-center">
          <p class="text-xs text-brand-600 font-medium">Gaplar</p>
          <p class="text-lg font-extrabold text-brand-800">{{ stats.sentences }}</p>
        </div>
      </div>
    </div>
  </ToolShell>

</template>
