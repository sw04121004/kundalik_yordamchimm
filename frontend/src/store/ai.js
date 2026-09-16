import { defineStore } from 'pinia'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'

export const PURPOSES = [
  { value: 'general', label: 'Umumiy AI', icon: '🤖' },
  { value: 'kitchen', label: 'Oshxona AI', icon: '🍳' },
  { value: 'study', label: 'O\'qish AI', icon: '📚' },
  { value: 'document', label: 'Hujjat AI', icon: '📄' },
  { value: 'translation', label: 'Tarjima AI', icon: '🌍' },
  { value: 'home', label: 'Uy AI', icon: '🏠' },
  { value: 'finance', label: 'Moliya AI', icon: '💰' },
  { value: 'programming', label: 'Kod AI', icon: '💻' },
  { value: 'ideas', label: 'G\'oya AI', icon: '💡' },
  { value: 'cv', label: 'CV / Ish AI', icon: '💼' },
]

export function purposeMeta(value) {
  return PURPOSES.find((p) => p.value === value) || PURPOSES[0]
}

export const useAiStore = defineStore('ai', {
  state: () => ({
    conversations: [],
    conversationsLoaded: false,
    conversationsLoading: false,

    current: null, // full conversation detail incl. messages
    currentLoading: false,

    sending: false,
    error: '',
    aiConfigured: true,
  }),

  actions: {
    async fetchConversations(force = false) {
      if (this.conversationsLoaded && !force) return
      this.conversationsLoading = true
      try {
        const { data } = await api.get('/ai/conversations/')
        this.conversations = data
        this.conversationsLoaded = true
      } catch (error) {
        console.error('Suhbatlarni yuklashda xatolik:', error)
      } finally {
        this.conversationsLoading = false
      }
    },

    async startConversation(purpose) {
      this.error = ''
      try {
        const { data } = await api.post('/ai/conversations/', { purpose })
        this.conversations.unshift({ ...data, last_message: null })
        this.current = { ...data, messages: [] }
        return { success: true, conversation: data }
      } catch (error) {
        const message = extractErrorMessage(error, 'Yangi suhbat yaratib bo‘lmadi.')
        this.error = message
        return { success: false, message }
      }
    },

    async openConversation(id) {
      this.currentLoading = true
      this.error = ''
      try {
        const { data } = await api.get(`/ai/conversations/${id}/`)
        this.current = data
        return { success: true }
      } catch (error) {
        const message = extractErrorMessage(error, 'Suhbatni ochib bo‘lmadi.')
        this.error = message
        return { success: false, message }
      } finally {
        this.currentLoading = false
      }
    },

    async sendMessage(conversationId, content) {
      this.error = ''
      this.sending = true

      // optimistic append of the user's own message
      const optimisticMessage = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content,
        created_at: new Date().toISOString(),
      }
      if (this.current && this.current.id === conversationId) {
        this.current.messages.push(optimisticMessage)
      }

      try {
        const { data } = await api.post(`/ai/conversations/${conversationId}/messages/`, { content })

        if (this.current && this.current.id === conversationId) {
          // replace optimistic message with the confirmed one, then add the reply
          const idx = this.current.messages.findIndex((m) => m.id === optimisticMessage.id)
          if (idx !== -1) this.current.messages.splice(idx, 1, data.user_message)
          this.current.messages.push(data.assistant_message)
          this.current.title = data.conversation_title
        }

        this.aiConfigured = data.ai_configured

        const listEntry = this.conversations.find((c) => c.id === conversationId)
        if (listEntry) {
          listEntry.title = data.conversation_title
          listEntry.last_message = data.assistant_message.content.slice(0, 90)
        }

        return { success: true, ai_ok: data.ai_ok }
      } catch (error) {
        // roll back the optimistic message on failure
        if (this.current && this.current.id === conversationId) {
          this.current.messages = this.current.messages.filter((m) => m.id !== optimisticMessage.id)
        }
        const message = extractErrorMessage(error, 'Xabar yuborilmadi. Qaytadan urinib ko‘ring.')
        this.error = message
        return { success: false, message }
      } finally {
        this.sending = false
      }
    },

    async deleteConversation(id) {
      try {
        await api.delete(`/ai/conversations/${id}/`)
        this.conversations = this.conversations.filter((c) => c.id !== id)
        if (this.current?.id === id) this.current = null
        return { success: true }
      } catch (error) {
        return { success: false, message: extractErrorMessage(error, 'Suhbatni o‘chirib bo‘lmadi.') }
      }
    },

    reset() {
      this.current = null
    },
  },
})
