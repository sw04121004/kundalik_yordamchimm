<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import { useAiStore } from '../store/ai'

const router = useRouter()
const aiStore = useAiStore()

const availableIngredients = [
  'Tuxum 🥚', 'Kartoshka 🥔', 'Piyoz 🧅', 'Pomidor 🍅',
  'Go\'sht 🥩', 'Sut 🥛', 'Un 🌾', 'Pishloq 🧀',
  'Sabzi 🥕', 'Guruch 🍚', 'Sarimsoq 🧄', 'Ko\'katlar 🌿'
]

const selectedIngredients = ref([])

function toggleIngredient(item) {
  const clean = item.split(' ')[0]
  const idx = selectedIngredients.value.indexOf(clean)
  if (idx >= 0) {
    selectedIngredients.value.splice(idx, 1)
  } else {
    selectedIngredients.value.push(clean)
  }
}

async function askKitchenAI() {
  const prompt = selectedIngredients.value.length
    ? `Menda quyidagi masalliqlar bor: ${selectedIngredients.value.join(', ')}. Ushbu masalliqlardan qanday mazali taomlar pishirishim mumkin? Retseptini bering.`
    : `Oshxona bo'yicha maslahat va oson tayyorlanadigan milliy va xalqaro retseptlar tavsiya eting.`

  const res = await aiStore.startConversation('kitchen')
  if (res.success && aiStore.current) {
    await aiStore.sendMessage(aiStore.current.id, prompt)
    router.push({ name: 'ai-assistant' })
  }
}

// Kitchen conversions
const convQty = ref(1)
const convUnit = ref('stakan')

const convResult = computed(() => {
  const q = Number(convQty.value) || 0
  if (convUnit.value === 'stakan') {
    return `${q * 200} ml (suyuqlik) / ${q * 130} g (un) / ${q * 200} g (shakar)`
  } else if (convUnit.value === 'osh_qoshiq') {
    return `${q * 15} ml (suyuqlik) / ${q * 15} g (shakar) / ${q * 10} g (un)`
  } else if (convUnit.value === 'choy_qoshiq') {
    return `${q * 5} ml (suyuqlik) / ${q * 5} g (shakar) / ${q * 3} g (un)`
  }
  return ''
})
</script>

<template>
  <ToolShell
    icon="🍳"
    title="Oshxona AI va Retseptlar Yordamchisi"
    description="Masalliqlaringizga qarab retseptlar toping va oshxona o'lchovlarini hisoblang"
    hint="Bordir masalliqlaringizni tanlang va AI sizga eng mos retseptni tavsiya etadi"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <!-- Ingredient selector card -->
      <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/50 shadow-sm space-y-4">
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <span>🧺</span> Sizda qaysi masalliqlar bor?
        </h3>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="ing in availableIngredients"
            :key="ing"
            class="px-3 py-2 rounded-xl text-xs sm:text-sm font-medium transition border"
            :class="selectedIngredients.includes(ing.split(' ')[0])
              ? 'bg-brand-500 text-white border-brand-500 shadow-sm'
              : 'bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:border-brand-400'"
            @click="toggleIngredient(ing)"
          >
            {{ ing }}
          </button>
        </div>

        <button
          class="btn-primary w-full !py-3 flex items-center justify-center gap-2"
          @click="askKitchenAI"
        >
          <span>🤖</span> AI'dan retsept so'rash →
        </button>
      </div>

      <!-- Quick Kitchen Unit Converter -->
      <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 space-y-3">
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <span>⚖️</span> Oshxona o'lchov kalkulyatori
        </h3>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="label text-xs">Miqdor</label>
            <input v-model="convQty" type="number" min="0.1" step="0.5" class="input font-mono" />
          </div>
          <div>
            <label class="label text-xs">O'lchov birligi</label>
            <select v-model="convUnit" class="input">
              <option value="stakan">Stakan (200ml)</option>
              <option value="osh_qoshiq">Osh qoshiq (15ml)</option>
              <option value="choy_qoshiq">Choy qoshiq (5ml)</option>
            </select>
          </div>
        </div>
        <div class="p-3 rounded-xl bg-brand-50 dark:bg-brand-900/20 text-brand-700 dark:text-brand-300 text-sm font-medium">
          = {{ convResult }}
        </div>
      </div>
    </div>
  </ToolShell>
</template>
