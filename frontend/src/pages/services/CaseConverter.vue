<script setup>
import { ref, onMounted } from 'vue'
import ToolShell from '../../components/ToolShell.vue'
import AppHeader from '../../components/AppHeader.vue'
import { useServicesStore } from '../../store/services'

const servicesStore = useServicesStore()
onMounted(() => servicesStore.logUsage('harf-ozgartirish'))

const text = ref('')

function toUpper() {
  text.value = text.value.toUpperCase()
}
function toLower() {
  text.value = text.value.toLowerCase()
}
function toTitleCase() {
  text.value = text.value
    .toLowerCase()
    .replace(/(^|\s)\S/g, (char) => char.toUpperCase())
}
function toSentenceCase() {
  const lower = text.value.toLowerCase()
  text.value = lower.replace(/(^\s*\w|[.!?]\s*\w)/g, (char) => char.toUpperCase())
}
function invertCase() {
  text.value = text.value
    .split('')
    .map((c) => (c === c.toUpperCase() ? c.toLowerCase() : c.toUpperCase()))
    .join('')
}

function reset() {
  text.value = ''
}
</script>

<template>
  <ToolShell icon="🔡" title="Katta/kichik harf o‘zgartirish" description="Matnni turli registrga o‘zgartiring" hint="Avval matningizni kiriting, so‘ng kerakli tugmani bosing (BOSH HARF, kichik harf va h.k.) — natija shu yerning o‘zida ko‘rinadi.">
    <template #header><AppHeader /></template>

    <div class="space-y-4">
      <div>
        <label class="label">Matningizni kiriting</label>
        <textarea
          v-model="text"
          rows="7"
          class="input resize-none"
          placeholder="Matnni shu yerga kiriting..."
        ></textarea>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <button class="btn-secondary" @click="toUpper">BOSH HARF</button>
        <button class="btn-secondary" @click="toLower">kichik harf</button>
        <button class="btn-secondary" @click="toTitleCase">Har Bir So‘z</button>
        <button class="btn-secondary" @click="toSentenceCase">Gap boshi</button>
        <button class="btn-secondary" @click="invertCase">tEsKaRi</button>
        <button class="btn-secondary" @click="reset">Tozalash</button>
      </div>
    </div>
  </ToolShell>

</template>
