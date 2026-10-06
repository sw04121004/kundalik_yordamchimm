<script setup>
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import AppHeader from '../components/AppHeader.vue'
import { useAiStore, PURPOSES, purposeMeta } from '../store/ai'

const aiStore = useAiStore()
const route = useRoute()
const router = useRouter()

const STARTER_PROMPTS = {
  kitchen: ["Uyda bor mahsulotlarimdan ovqat topib ber", "Bugungi kechki ovqat uchun menyu tuz"],
  study: ["Bu mavzuni oddiy qilib tushuntir", "Imtihon uchun test tuzib ber"],
  document: ["Bu hujjatni qisqacha tushuntir", "Rasmiy matn qilib yozib ber"],
  finance: ["Bugungi xarajatlarimni tahlil qil", "Byudjet rejasini tuz"],
  programming: ["Bu koddagi xatoni top", "Kodimni tushuntirib ber"],
  translation: ["Bu matnni ingliz tiliga tarjima qil"],
  home: ["Bugun uyda nimalar qilishim kerak?"],
  general: ["Menga yordam bering", "Qanday imkoniyatlaringiz bor?"]
}

function renderMarkdown(text) {
  if (!text) return ''
  return marked(text)
}

const draft = ref('')
const sidebarOpen = ref(false)
const messagesEnd = ref(null)
const textareaRef = ref(null)
const isRecording = ref(false)
const recordingTime = ref(0)
const voiceError = ref('')
let speechRecognition = null
let recordingTimer = null

onMounted(async () => {
  await aiStore.fetchConversations()
  if (route.query.q && route.query.p) {
    const p = route.query.p
    const q = route.query.q
    const result = await aiStore.startConversation(p)
    if (result.success) {
      draft.value = q
      // give it a tiny delay to ensure everything is mounted
      setTimeout(() => send(), 100)
      router.replace({ query: {} })
    }
  }
})

function scrollToBottom() {
  nextTick(() => messagesEnd.value?.scrollIntoView({ behavior: 'smooth', block: 'end' }))
}

watch(() => aiStore.current?.messages?.length, () => scrollToBottom())

function stopRecording() {
  isRecording.value = false
  window.clearInterval(recordingTimer)
  recordingTimer = null
  if (speechRecognition) {
    try { speechRecognition.stop() } catch { /* Recognition may already have stopped. */ }
  }
}

function toggleRecord() {
  voiceError.value = ''
  if (isRecording.value) {
    stopRecording()
    return
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SpeechRecognition) {
    voiceError.value = 'Bu brauzer ovozni matnga aylantirishni qo‘llamaydi. Chrome yoki Edge brauzerida sinab ko‘ring.'
    return
  }

  speechRecognition = new SpeechRecognition()
  speechRecognition.lang = 'uz-UZ'
  speechRecognition.continuous = true
  speechRecognition.interimResults = true
  speechRecognition.onstart = () => {
    isRecording.value = true
    recordingTime.value = 0
    recordingTimer = window.setInterval(() => recordingTime.value++, 1000)
  }
  speechRecognition.onresult = (event) => {
    let transcript = ''
    for (let index = event.resultIndex; index < event.results.length; index++) {
      if (event.results[index].isFinal) transcript += event.results[index][0].transcript
    }
    if (transcript.trim()) {
      draft.value = `${draft.value.trim()} ${transcript.trim()}`.trim()
      nextTick(() => textareaRef.value && autoResize(textareaRef.value))
    }
  }
  speechRecognition.onerror = (event) => {
    const messages = {
      'not-allowed': 'Mikrofonga ruxsat berilmadi. Brauzer sozlamalaridan ruxsat bering.',
      'service-not-allowed': 'Brauzer ovoz xizmatidan foydalanishga ruxsat bermadi.',
      network: 'Ovozni matnga aylantirish xizmati tarmoqqa ulanmayapti.',
      'no-speech': 'Ovoz aniqlanmadi. Qayta urinib ko‘ring.',
    }
    voiceError.value = messages[event.error] || 'Ovoz yozishda xatolik yuz berdi.'
    stopRecording()
  }
  speechRecognition.onend = () => {
    isRecording.value = false
    window.clearInterval(recordingTimer)
    recordingTimer = null
  }

  try {
    speechRecognition.start()
  } catch {
    voiceError.value = 'Mikrofonni ishga tushirib bo‘lmadi. Qayta urinib ko‘ring.'
    stopRecording()
  }
}

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0')
  const remainder = (seconds % 60).toString().padStart(2, '0')
  return `${minutes}:${remainder}`
}

onUnmounted(() => {
  window.clearInterval(recordingTimer)
  if (speechRecognition) speechRecognition.stop()
})

async function pickPurpose(purposeValue) {
  const result = await aiStore.startConversation(purposeValue)
  if (result.success) {
    sidebarOpen.value = false
    await nextTick()
    textareaRef.value?.focus()
  }
}

async function openConversation(id) {
  await aiStore.openConversation(id)
  sidebarOpen.value = false
}

function startNew() {
  aiStore.reset()
  sidebarOpen.value = false
}

async function send() {
  const text = draft.value.trim()
  if (!text || aiStore.sending || !aiStore.current) return

  if (isRecording.value) stopRecording()
  draft.value = ''
  await aiStore.sendMessage(aiStore.current.id, text)
}

function saveMessageAsPdf(content) {
  const printWindow = window.open('', '_blank')
  if (!printWindow) {
    aiStore.error = 'PDF oynasini ochib bo‘lmadi. Brauzerda qalqib chiquvchi oynalarga ruxsat bering.'
    return
  }
  const escaped = content.replace(/[&<>]/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;',
  })[char])
  printWindow.document.write(`<!doctype html><html lang="uz"><head><meta charset="utf-8"><title>AI javobi</title><style>body{font:16px/1.6 Arial,sans-serif;max-width:800px;margin:40px auto;padding:0 24px;color:#111}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}@media print{body{margin:0 auto}}</style></head><body><h1>AI javobi</h1><pre>${escaped}</pre></body></html>`)
  printWindow.document.close()
  printWindow.focus()
  printWindow.print()
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

async function removeConversation(id) {
  if (!confirm("Ushbu suhbatni o'chirmoqchimisiz?")) return
  await aiStore.deleteConversation(id)
}

function formatTime(iso) {
  try { return new Date(iso).toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' }) }
  catch { return '' }
}

function autoResize(el) {
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 160) + 'px'
}
</script>

<template>
  <div class="min-h-screen bg-[#f4f6fb] dark:bg-[#0d1117] flex flex-col">
    <AppHeader />

    <div class="flex-1 flex max-w-5xl w-full mx-auto px-4 sm:px-6 py-5 gap-4" style="min-height: calc(100vh - 4rem)">

      <!-- Sidebar desktop -->
      <aside class="hidden md:flex md:w-72 shrink-0 flex-col card overflow-hidden">
        <div class="p-4 border-b border-slate-100 dark:border-white/5">
          <button class="btn-primary w-full text-sm justify-center" @click="startNew">+ Yangi suhbat</button>
        </div>
        <div class="flex-1 overflow-y-auto p-2 space-y-1">
          <p v-if="aiStore.conversationsLoading" class="text-sm text-slate-400 px-3 py-4 text-center">Yuklanmoqda...</p>
          <p v-else-if="!aiStore.conversations.length" class="text-sm text-slate-400 px-3 py-6 text-center">Hali suhbatlar yo'q.</p>
          <div
            v-for="conv in aiStore.conversations"
            :key="conv.id"
            class="group w-full flex items-start gap-2.5 px-3 py-2.5 rounded-xl transition-all duration-150 cursor-pointer relative"
            :class="aiStore.current?.id === conv.id
              ? 'bg-brand-50 dark:bg-white/5'
              : 'hover:bg-slate-50 dark:hover:bg-white/5'"
            @click="openConversation(conv.id)"
          >
            <div class="absolute left-0 top-2 bottom-2 w-0.5 bg-brand-500 rounded-full transition-opacity duration-150"
              :class="aiStore.current?.id === conv.id ? 'opacity-100' : 'opacity-0'"></div>
            <span class="text-base shrink-0 mt-0.5">{{ purposeMeta(conv.purpose).icon }}</span>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-slate-700 dark:text-slate-200 truncate">{{ conv.title }}</p>
              <p v-if="conv.last_message" class="text-xs text-slate-400 truncate mt-0.5">{{ conv.last_message }}</p>
            </div>
            <button
              class="opacity-0 group-hover:opacity-100 shrink-0 mt-0.5 w-5 h-5 flex items-center justify-center text-slate-300 hover:text-red-500 transition-all rounded"
              @click.stop="removeConversation(conv.id)"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>
        </div>
      </aside>

      <!-- Mobile sidebar overlay -->
      <transition name="page-fade">
        <div v-if="sidebarOpen" class="md:hidden fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm" @click.self="sidebarOpen = false">
          <div class="absolute left-0 top-0 bottom-0 w-72 bg-white dark:bg-slate-900 border-r border-slate-100 dark:border-slate-700/60 p-4 flex flex-col">
            <div class="flex items-center justify-between mb-4">
              <h2 class="font-bold text-slate-800 dark:text-white">Suhbatlar</h2>
              <button class="w-8 h-8 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-500" @click="sidebarOpen = false">×</button>
            </div>
            <button class="btn-primary w-full text-sm justify-center mb-4" @click="startNew">+ Yangi suhbat</button>
            <div class="flex-1 overflow-y-auto space-y-1">
              <div
                v-for="conv in aiStore.conversations"
                :key="conv.id"
                class="flex items-start gap-2.5 px-3 py-2.5 rounded-xl hover:bg-slate-50 dark:hover:bg-white/5 cursor-pointer"
                @click="openConversation(conv.id)"
              >
                <span class="text-base shrink-0">{{ purposeMeta(conv.purpose).icon }}</span>
                <p class="text-sm font-semibold text-slate-700 dark:text-slate-200 truncate">{{ conv.title }}</p>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- Main chat -->
      <main class="flex-1 flex flex-col min-w-0 card overflow-hidden relative">

        <!-- Mobile topbar -->
        <div class="md:hidden flex items-center justify-between px-4 py-3 border-b border-slate-100 dark:border-white/5">
          <button class="text-sm font-semibold text-slate-600 dark:text-slate-300 flex items-center gap-1.5" @click="sidebarOpen = true">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
            Suhbatlar
          </button>
          <button class="text-sm font-semibold text-brand-600 dark:text-brand-400" @click="startNew">+ Yangi</button>
        </div>

        <!-- Purpose picker -->
        <div v-if="!aiStore.current" class="flex-1 flex items-center justify-center p-6 overflow-y-auto">
          <div class="max-w-2xl w-full animate-fadeUp">
            <div class="text-center mb-8">
              <div class="w-16 h-16 rounded-2xl bg-brand-50 dark:bg-brand-900/30 flex items-center justify-center text-4xl mx-auto mb-4 animate-float">🤖</div>
              <h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">AI Yordamchi</h1>
              <p class="text-slate-500 dark:text-slate-400">Qaysi sohada yordam kerak?</p>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
              <button
                v-for="p in PURPOSES"
                :key="p.value"
                class="card p-4 flex flex-col items-center gap-2.5 hover:-translate-y-0.5 hover:shadow-md transition-all duration-200 focus:outline-none"
                @click="pickPurpose(p.value)"
              >
                <span class="text-3xl">{{ p.icon }}</span>
                <span class="text-xs font-semibold text-slate-700 dark:text-slate-200 text-center leading-tight">{{ p.label }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Active conversation -->
        <template v-else>
          <!-- Chat header -->
          <div class="flex items-center gap-3 px-4 sm:px-5 py-3 border-b border-slate-100 dark:border-white/5">
            <div class="w-9 h-9 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-xl shrink-0">{{ purposeMeta(aiStore.current.purpose).icon }}</div>
            <div class="min-w-0">
              <p class="text-sm font-bold text-slate-800 dark:text-slate-100 truncate">{{ aiStore.current.title }}</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">{{ purposeMeta(aiStore.current.purpose).label }}</p>
            </div>
          </div>

          <!-- AI not configured warning -->
          <div v-if="!aiStore.aiConfigured" class="mx-4 sm:mx-5 mt-4 flex gap-2.5 p-3.5 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700/40 text-amber-800 dark:text-amber-200 text-xs font-medium">
            <span class="shrink-0">⚠️</span>
            <p>AI hozircha ulanmagan. Administrator backend/.env da <code class="bg-amber-100 dark:bg-amber-900/50 px-1 py-0.5 rounded font-mono">AI_API_KEY</code> ni to'ldirishi kerak.</p>
          </div>

          <!-- Messages -->
          <div class="flex-1 overflow-y-auto px-4 sm:px-5 py-5 space-y-4">
            
            <div v-if="!aiStore.current.messages.length" class="mt-8 mb-4 animate-fadeUp max-w-xl mx-auto w-full">
              <p class="text-center text-slate-400 text-sm mb-6">Yoki quyidagilardan birini tanlang:</p>
              <div class="flex flex-wrap justify-center gap-2.5">
                <button
                  v-for="(prompt, i) in (STARTER_PROMPTS[aiStore.current.purpose] || STARTER_PROMPTS['general'])"
                  :key="i"
                  @click="draft = prompt; send()"
                  class="inline-flex items-center text-left px-4 py-2.5 rounded-full text-sm font-medium transition-all duration-300 cursor-pointer shadow-sm hover:shadow-md hover:shadow-brand-500/20 active:scale-95 border border-brand-200/50 dark:border-brand-500/30 bg-gradient-to-br from-white dark:from-[#1e2330] to-brand-50/50 dark:to-brand-900/20 text-brand-700 dark:text-brand-300 hover:border-brand-300 dark:hover:border-brand-500/50 hover:-translate-y-0.5 focus:outline-none"
                >
                  <span class="mr-2 opacity-70">💡</span> {{ prompt }}
                </button>
              </div>
            </div>

            <div
              v-for="msg in aiStore.current.messages"
              :key="msg.id"
              class="flex animate-fadeUp flex-col"
              :class="msg.role === 'user' ? 'items-end' : 'items-start'"
            >
              <!-- User bubble -->
              <div v-if="msg.role === 'user'"
                class="max-w-[80%] sm:max-w-[65%] rounded-2xl rounded-br-sm px-4 py-3 text-sm leading-relaxed text-white whitespace-pre-wrap flex flex-col items-end"
                style="background: linear-gradient(135deg, rgb(var(--brand-500)), rgb(var(--brand-600)))"
              >
                <span v-if="msg.content">{{ msg.content }}</span>
                <div class="text-[10px] text-white/60 mt-1.5 text-right w-full">{{ formatTime(msg.created_at) }}</div>
              </div>

              <!-- Assistant bubble -->
              <div v-else
                class="max-w-[80%] sm:max-w-[70%] rounded-2xl rounded-bl-sm bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/60 px-4 py-3 shadow-sm text-sm text-slate-800 dark:text-slate-200 prose prose-sm dark:prose-invert max-w-none"
              >
                <div v-html="renderMarkdown(msg.content)" class="ai-prose"></div>
                <div class="text-[10px] text-slate-400 mt-1.5">{{ formatTime(msg.created_at) }}</div>
                <button
                  class="mt-2 text-xs font-medium text-brand-600 dark:text-brand-400 hover:underline"
                  @click="saveMessageAsPdf(msg.content)"
                >PDF qilib saqlash</button>
              </div>
            </div>

            <!-- Typing indicator -->
            <div v-if="aiStore.sending" class="flex justify-start animate-fadeUp">
              <div class="bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/60 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-brand-400 animate-bounce" style="animation-delay:0ms"></span>
                <span class="w-2 h-2 rounded-full bg-brand-400 animate-bounce" style="animation-delay:150ms"></span>
                <span class="w-2 h-2 rounded-full bg-brand-400 animate-bounce" style="animation-delay:300ms"></span>
              </div>
            </div>

            <div ref="messagesEnd" class="h-2"></div>
          </div>

          <!-- Error -->
          <p v-if="aiStore.error" class="px-4 sm:px-5 pb-2 text-xs text-red-500 font-medium">{{ aiStore.error }}</p>

          <!-- Input Area -->
          <div class="px-4 sm:px-5 py-3 border-t border-slate-100 dark:border-white/5 bg-white dark:bg-[#161b26] relative">
            <p class="text-[11px] text-slate-500 dark:text-slate-400 mb-2">AI tashqi modeldan javob oladi; javoblar xato yoki eskirgan bo‘lishi mumkin va jonli manbalar avtomatik tekshirilmaydi.</p>
            <p v-if="isRecording" class="text-xs text-red-500 mb-2" role="status">🔴 Ovoz yozilmoqda · {{ formatDuration(recordingTime) }} · gapni matnga aylantiryapti</p>
            <p v-else-if="voiceError" class="text-xs text-amber-600 dark:text-amber-400 mb-2" role="alert">{{ voiceError }}</p>
            <p v-else class="text-[10px] text-slate-400 mb-2">Mikrofon gapirganingizni matnga aylantiradi; yuborishdan oldin matnni tekshiring.</p>
            <!-- Input Box -->
            <div class="flex items-end gap-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700/60 rounded-2xl px-3 py-2 transition-all focus-within:border-brand-500/50 focus-within:ring-2 focus-within:ring-brand-500/10">
              <button
                type="button"
                class="shrink-0 w-10 h-10 rounded-xl flex items-center justify-center transition-colors mb-0.5"
                :class="isRecording ? 'text-red-500 bg-red-50 dark:bg-red-500/10' : 'text-slate-400 hover:text-brand-600 hover:bg-slate-100 dark:hover:bg-slate-800'"
                :aria-label="isRecording ? 'Ovoz yozishni to‘xtatish' : 'Ovoz yozishni boshlash'"
                :title="isRecording ? 'To‘xtatish' : 'Ovoz bilan yozish'"
                @click="toggleRecord"
              >
                <svg v-if="!isRecording" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18.5a6.5 6.5 0 006.5-6.5m-13 0a6.5 6.5 0 006.5 6.5m0 0V22m0-3.5H8.5m3.5 0h3.5M9 12V5a3 3 0 016 0v7a3 3 0 01-6 0z"/></svg>
                <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
              </button>
              <textarea
                ref="textareaRef"
                v-model="draft"
                rows="1"
                class="w-full bg-transparent border-none resize-none focus:ring-0 outline-none text-sm text-slate-800 dark:text-slate-100 placeholder-slate-400 max-h-40 py-2 leading-relaxed"
                placeholder="Xabaringizni yozing..."
                @keydown="handleKeydown"
                @input="autoResize($event.target)"
              ></textarea>
              <button
                class="shrink-0 w-10 h-10 rounded-xl flex items-center justify-center text-white transition-all hover:opacity-90 active:scale-95 disabled:opacity-40 mb-0.5"
                style="background: linear-gradient(135deg, rgb(var(--brand-500)), rgb(var(--brand-700)))"
                :disabled="!draft.trim() || aiStore.sending"
                @click="send"
              >
                <svg class="w-4 h-4 rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 19V5m-7 7l7-7 7 7"/></svg>
              </button>
            </div>
          </div>
        </template>
      </main>
    </div>
  </div>
</template>

<style scoped>
:deep(.ai-prose p:first-child) { margin-top: 0; }
:deep(.ai-prose p:last-child) { margin-bottom: 0; }
:deep(.ai-prose pre) {
  background: #0d1117 !important;
  border-radius: 0.625rem;
  padding: 0.875rem 1rem;
  overflow-x: auto;
  margin: 0.75rem 0;
}
:deep(.ai-prose code:not(pre code)) {
  background: rgb(var(--brand-50));
  color: rgb(var(--brand-700));
  padding: 0.1em 0.35em;
  border-radius: 0.25rem;
  font-size: 0.875em;
}
html.dark :deep(.ai-prose code:not(pre code)) {
  background: rgb(var(--brand-900) / 0.4);
  color: rgb(var(--brand-300));
}
</style>
