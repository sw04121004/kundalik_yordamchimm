<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import { useAiStore } from '../store/ai'

const router = useRouter()
const aiStore = useAiStore()

const docText = ref('')

const wordCount = computed(() => {
  if (!docText.value.trim()) return 0
  return docText.value.trim().split(/\s+/).length
})

const charCount = computed(() => docText.value.length)

const readTime = computed(() => Math.ceil(wordCount.value / 200))

function cleanDoc() {
  if (!docText.value) return
  docText.value = docText.value
    .replace(/[ \t]+/g, ' ')
    .replace(/\n\s*\n+/g, '\n\n')
    .trim()
}

async function askDocAI(type) {
  if (!docText.value.trim()) return
  const prompts = {
    summarize: `Ushbu hujjat/matnni qisqacha xulosalab bering:\n\n${docText.value}`,
    grammar: `Ushbu matnning imlo va grammatik xatolarini tekshirib, tuzatilgan variantini bering:\n\n${docText.value}`,
    translate: `Ushbu hujjatni o'zbek tiliga (yoki ingliz tiliga) professional tarjima qilib bering:\n\n${docText.value}`
  }

  const res = await aiStore.startConversation('document')
  if (res.success && aiStore.current) {
    await aiStore.sendMessage(aiStore.current.id, prompts[type] || prompts.summarize)
    router.push({ name: 'ai-assistant' })
  }
}
</script>

<template>
  <ToolShell
    icon="📄"
    title="Hujjat va Matn Ishlovchisi (Hujjat AI)"
    description="Hujjatlarni tahlil qilish, qisqartirish va tahrirlash"
    hint="Matnni joylang va statistikani ko'ring hamda AI bilan tahlil qiling"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <!-- Textarea Input -->
      <div>
        <label class="label">Hujjat matnini kiriting</label>
        <textarea
          v-model="docText"
          rows="6"
          class="input font-mono text-sm leading-relaxed"
          placeholder="Bu yerga hujjat matnini nusxalab joylang..."
        ></textarea>
      </div>

      <!-- Live Stats Bar -->
      <div class="grid grid-cols-3 gap-3 text-center">
        <div class="p-3 rounded-xl bg-slate-100 dark:bg-slate-800">
          <span class="text-xs text-slate-400 uppercase font-semibold">So'zlar</span>
          <div class="text-lg font-bold text-slate-800 dark:text-slate-100 font-mono">{{ wordCount }}</div>
        </div>
        <div class="p-3 rounded-xl bg-slate-100 dark:bg-slate-800">
          <span class="text-xs text-slate-400 uppercase font-semibold">Belgilar</span>
          <div class="text-lg font-bold text-slate-800 dark:text-slate-100 font-mono">{{ charCount }}</div>
        </div>
        <div class="p-3 rounded-xl bg-slate-100 dark:bg-slate-800">
          <span class="text-xs text-slate-400 uppercase font-semibold">O'qish vaqti</span>
          <div class="text-lg font-bold text-slate-800 dark:text-slate-100 font-mono">~{{ readTime }} min</div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="flex flex-wrap gap-2">
        <button class="btn-secondary text-xs !py-2" @click="cleanDoc">
          🧹 Matnni tozalash
        </button>
        <button
          class="btn-primary text-xs !py-2"
          :disabled="!docText.trim()"
          @click="askDocAI('summarize')"
        >
          📝 AI bilan xulosalash
        </button>
        <button
          class="btn-primary text-xs !py-2"
          :disabled="!docText.trim()"
          @click="askDocAI('grammar')"
        >
          ✍️ Grammatikani tekshirish
        </button>
        <button
          class="btn-primary text-xs !py-2"
          :disabled="!docText.trim()"
          @click="askDocAI('translate')"
        >
          🌐 Tarjima qilish
        </button>
      </div>
    </div>
  </ToolShell>
</template>
