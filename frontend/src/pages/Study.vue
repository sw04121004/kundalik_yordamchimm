<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import { useAiStore } from '../store/ai'

const router = useRouter()
const aiStore = useAiStore()

const flashcards = ref([
  { id: 1, front: 'Apple', back: 'Olma' },
  { id: 2, front: 'Knowledge', back: 'Bilim / Ilm' },
  { id: 3, front: 'Perseverance', back: 'Matonat / Qat\'iyat' },
])

const newFront = ref('')
const newBack = ref('')

const currentIndex = ref(0)
const isFlipped = ref(false)

function addCard() {
  if (!newFront.value.trim() || !newBack.value.trim()) return
  flashcards.value.push({
    id: Date.now(),
    front: newFront.value.trim(),
    back: newBack.value.trim()
  })
  newFront.value = ''
  newBack.value = ''
}

function nextCard() {
  isFlipped.value = false
  if (currentIndex.value < flashcards.value.length - 1) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
}

async function askStudyAI() {
  const res = await aiStore.startConversation('study')
  if (res.success && aiStore.current) {
    await aiStore.sendMessage(aiStore.current.id, "Manga ingliz tili grammatikasi va lug'at boyligimni oshirish uchun samarali mashqlar tavsiya eting.")
    router.push({ name: 'ai-assistant' })
  }
}
</script>

<template>
  <ToolShell
    icon="📚"
    title="O'qish va Ta'lim Yordamchisi"
    description="Flashcard (yodlash kartalari) va AI yordamida bilimingizni oshiring"
    hint="So'zlarni tez va samarali yodlash uchun kartochkalarni bosing"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <!-- Flashcard Quiz Display -->
      <div v-if="flashcards.length" class="text-center space-y-4">
        <div
          class="w-full h-48 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white flex flex-col items-center justify-center p-6 shadow-soft cursor-pointer transition-transform duration-300 hover:scale-[1.02]"
          @click="isFlipped = !isFlipped"
        >
          <span class="text-xs uppercase tracking-wider opacity-75 mb-2">
            {{ isFlipped ? 'Javob / Tarjima' : 'Savol / So\'z' }} (Kartochka {{ currentIndex + 1 }}/{{ flashcards.length }})
          </span>
          <span class="text-2xl font-bold">
            {{ isFlipped ? flashcards[currentIndex].back : flashcards[currentIndex].front }}
          </span>
          <span class="text-xs opacity-75 mt-4">🔄 O'girish uchun bosing</span>
        </div>

        <button class="btn-primary !px-6 !py-2 text-sm" @click="nextCard">
          Keyingi kartochka ➔
        </button>
      </div>

      <!-- Add New Flashcard Form -->
      <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 space-y-3">
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <span>➕</span> Yangi yodlash kartasi qo'shish
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <input v-model="newFront" type="text" class="input" placeholder="Savol yoki So'z (masalan: Hello)" />
          <input v-model="newBack" type="text" class="input" placeholder="Javob yoki Tarjima (masalan: Salom)" />
        </div>
        <button class="btn-secondary w-full !py-2.5 text-sm" @click="addCard">
          + Kartochka qo'shish
        </button>
      </div>

      <!-- Study AI Banner -->
      <div class="p-4 rounded-xl bg-brand-50 dark:bg-brand-900/20 border border-brand-100 dark:border-brand-900/30 flex items-center justify-between gap-3">
        <span class="text-sm font-medium text-brand-800 dark:text-brand-300">
          🎓 Imtihonga tayyorgarlik yoki mavzuni tushunishda AI'dan yordam oling.
        </span>
        <button class="btn-primary text-xs shrink-0" @click="askStudyAI">
          O'qish AI →
        </button>
      </div>
    </div>
  </ToolShell>
</template>
