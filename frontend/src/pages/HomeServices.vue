<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import { useAiStore } from '../store/ai'

const router = useRouter()
const aiStore = useAiStore()

const stains = [
  { id: 'coffee', name: 'Qahva / Choy ☕', solution: 'Iliq suvga ozgina idish yuvish vositasi va sirka (vinegar) solib, dog\' ustiga surting. 10 minutdan so\'ng yuving.' },
  { id: 'grease', name: 'Yog\' / Ovqat 🍔', solution: 'Dog\' ustiga darhol kraxmal yoki soda seping (yog\'ni shimib oladi). 15 daqiqadan so\'ng sovunli issiq suvda yuving.' },
  { id: 'ink', name: 'Siyoh / Ruchka 🖊️', solution: 'Spirt (antiseptik) yoki lak tozalagich bilan paxtani ho\'llab, dog\'ni yengil arting.' },
  { id: 'blood', name: 'Qon 🩸', solution: 'FAQAT sovuq suvda yuving! Issiq suv qonni matoga yopishtirib qo\'yadi. Vodorod peroksid ham yordam beradi.' },
  { id: 'wine', name: 'Sharbat / Vino 🍷', solution: 'Ustiga tuz seping. So\'ng gazlangan mineral suv yoki mineral ichimlik bilan arting va yuving.' }
]

const selectedStain = ref('coffee')

async function askHomeAI() {
  const res = await aiStore.startConversation('home')
  if (res.success && aiStore.current) {
    await aiStore.sendMessage(aiStore.current.id, "Uyni toza saqlash, maishiy texnika parvarishi va mebellarni tozalash bo'yicha maslahatlar bering.")
    router.push({ name: 'ai-assistant' })
  }
}
</script>

<template>
  <ToolShell
    icon="🏠"
    title="Uy AI va Maishiy Yordamchi"
    description="Uyni toza saqlash, dog'larni ketkazish va maishiy masalalarga tezkor yechimlar"
    hint="Turli murakkab dog'larni osongina yo'qotish bo'yicha amaliy maslahatlar"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <!-- Stain remover helper -->
      <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/50 shadow-sm space-y-4">
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <span>🧼</span> Dog'larni ketkazish bo'yicha tezkor qo'llanma
        </h3>
        
        <div class="flex flex-wrap gap-2">
          <button
            v-for="s in stains"
            :key="s.id"
            class="px-3 py-2 rounded-xl text-xs sm:text-sm font-medium transition"
            :class="selectedStain === s.id ? 'bg-brand-500 text-white shadow-sm' : 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'"
            @click="selectedStain = s.id"
          >
            {{ s.name }}
          </button>
        </div>

        <div class="p-4 rounded-xl bg-brand-50 dark:bg-brand-900/20 text-brand-800 dark:text-brand-200 text-sm leading-relaxed border border-brand-100 dark:border-brand-900/30">
          💡 <b>Yechim:</b> {{ stains.find(s => s.id === selectedStain)?.solution }}
        </div>
      </div>

      <!-- AI Home Assistant shortcut -->
      <div class="p-5 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-between gap-4 flex-wrap">
        <div>
          <h4 class="font-bold text-base">Uy bo'yicha savolingiz bormi?</h4>
          <p class="text-xs text-brand-100 mt-1">Santexnika, elektr, mebel va maishiy texnikalarni ta'mirlash bo'yicha AI'dan so'rang.</p>
        </div>
        <button class="btn-secondary text-sm shrink-0" @click="askHomeAI">
          🤖 AI Yordamchini ochish →
        </button>
      </div>
    </div>
  </ToolShell>
</template>
