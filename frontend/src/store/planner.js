import { defineStore } from 'pinia'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'
import { useAuthStore } from './auth'
import {
  getTaskTriggerTimestamp,
  getTaskStatus,
  isTaskDue,
  isTaskAlreadyNotified,
  markTaskNotified,
  clearTaskNotified,
  clearAllNotifiedForUser,
} from '../utils/plannerReminders'

function todayISO() {
  const d = new Date()
  const offset = d.getTimezoneOffset()
  const local = new Date(d.getTime() - offset * 60 * 1000)
  return local.toISOString().slice(0, 10)
}

let reminderInterval = null
let titleBlinkInterval = null
let originalTitle = typeof document !== 'undefined' ? document.title : 'Qulay.uz'

function playReminderBeep() {
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext
    if (!AudioContextClass) return
    const ctx = new AudioContextClass()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = 'sine'
    osc.frequency.setValueAtTime(587.33, ctx.currentTime) // D5
    osc.frequency.setValueAtTime(880, ctx.currentTime + 0.12) // A5
    gain.gain.setValueAtTime(0.18, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.45)
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.start()
    osc.stop(ctx.currentTime + 0.45)
  } catch {}
}

function startTitleBlink(message) {
  if (typeof document === 'undefined' || titleBlinkInterval) return
  originalTitle = document.title
  let isAlt = false
  titleBlinkInterval = setInterval(() => {
    document.title = isAlt ? `⏰ ${message}` : originalTitle
    isAlt = !isAlt
  }, 1000)
}

function stopTitleBlink() {
  if (titleBlinkInterval) {
    clearInterval(titleBlinkInterval)
    titleBlinkInterval = null
    if (typeof document !== 'undefined') {
      document.title = originalTitle
    }
  }
}

export const usePlannerStore = defineStore('planner', {
  state: () => ({
    tasks: [], // full list
    todayTasks: [], // just today's
    loading: false,
    error: '',
    notificationsStarted: false,
    activeReminder: null, // task object for active modal/toast
    overdueSummaryCount: 0,
    notificationPermission: typeof window !== 'undefined' && 'Notification' in window ? Notification.permission : 'unsupported',
  }),

  getters: {
    todayDone: (state) => state.todayTasks.filter((t) => t.is_done).length,
    todayTotal: (state) => state.todayTasks.length,
    todayPercent: (state) => {
      if (!state.todayTasks.length) return 0
      const done = state.todayTasks.filter((t) => t.is_done).length
      return Math.round((done / state.todayTasks.length) * 100)
    },
    overdueTasks: (state) => {
      const now = Date.now()
      return state.tasks.filter(t => getTaskStatus(t, now) === 'overdue')
    },
    approachingTasks: (state) => {
      const now = Date.now()
      return state.tasks.filter(t => getTaskStatus(t, now) === 'approaching')
    },
  },

  actions: {
    async fetchTasks() {
      this.loading = true
      try {
        const { data } = await api.get('/planner/tasks/')
        this.tasks = data
        this.todayTasks = data.filter(t => t.due_date === todayISO())
        this.checkOverdueSummary()
      } catch (error) {
        console.error('Vazifalarni yuklashda xatolik:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchToday() {
      try {
        const { data } = await api.get('/planner/tasks/', { params: { date: todayISO() } })
        this.todayTasks = data
      } catch (error) {
        console.error('Bugungi rejani yuklashda xatolik:', error)
      }
    },

    async createTask(payload) {
      this.error = ''
      try {
        const { data } = await api.post('/planner/tasks/', payload)
        this.tasks.unshift(data)
        if (payload.due_date === todayISO()) this.todayTasks.push(data)
        return { success: true }
      } catch (error) {
        const message = extractErrorMessage(error, "Vazifa qo'shib bo'lmadi.")
        this.error = message
        return { success: false, message }
      }
    },

    async toggleTask(task) {
      try {
        const { data } = await api.patch(`/planner/tasks/${task.id}/`, { is_done: !task.is_done })
        const applyUpdate = (list) => {
          const idx = list.findIndex((t) => t.id === task.id)
          if (idx !== -1) list.splice(idx, 1, data)
        }
        applyUpdate(this.tasks)
        applyUpdate(this.todayTasks)

        // Agar vazifa bajarilgan bo'lsa, eslatmani yopish
        if (data.is_done && this.activeReminder?.id === task.id) {
          this.dismissReminder()
        }
        // Agar qayta bajarilmagan qilinsa, qayta eslatish uchun tozalash
        if (!data.is_done) {
          const auth = useAuthStore()
          clearTaskNotified(auth.user?.id, task.id)
        }
      } catch (error) {
        console.error('Vazifani yangilashda xatolik:', error)
      }
    },

    async deleteTask(id) {
      try {
        await api.delete(`/planner/tasks/${id}/`)
        this.tasks = this.tasks.filter((t) => t.id !== id)
        this.todayTasks = this.todayTasks.filter((t) => t.id !== id)
        if (this.activeReminder?.id === id) {
          this.dismissReminder()
        }
      } catch (error) {
        console.error("Vazifani o'chirishda xatolik:", error)
      }
    },

    async snoozeTask(task, minutes = 10) {
      const now = new Date(Date.now() + minutes * 60 * 1000)
      const offset = now.getTimezoneOffset()
      const local = new Date(now.getTime() - offset * 60 * 1000)
      const newDate = local.toISOString().slice(0, 10)
      const newTime = local.toTimeString().slice(0, 5)

      try {
        const { data } = await api.patch(`/planner/tasks/${task.id}/`, {
          due_date: newDate,
          due_time: newTime,
        })
        const applyUpdate = (list) => {
          const idx = list.findIndex((t) => t.id === task.id)
          if (idx !== -1) list.splice(idx, 1, data)
        }
        applyUpdate(this.tasks)
        applyUpdate(this.todayTasks)
      } catch (e) {
        console.error('Kechiktirishda xatolik:', e)
      } finally {
        this.dismissReminder()
      }
    },

    dismissReminder() {
      this.activeReminder = null
      stopTitleBlink()
    },

    clearOverdueSummary() {
      this.overdueSummaryCount = 0
    },

    async requestNotificationPermission() {
      if (typeof window === 'undefined' || !('Notification' in window)) {
        this.notificationPermission = 'unsupported'
        return 'unsupported'
      }
      try {
        const res = await Notification.requestPermission()
        this.notificationPermission = res
        return res
      } catch (e) {
        this.notificationPermission = Notification.permission
        return Notification.permission
      }
    },

    checkOverdueSummary() {
      const now = Date.now()
      const count = this.tasks.filter(t => !t.is_done && getTaskStatus(t, now) === 'overdue').length
      this.overdueSummaryCount = count
    },

    checkReminders() {
      const nowMs = Date.now()
      const auth = useAuthStore()
      const userId = auth.user?.id

      // Har bir eslatma tekshiruvida proсрочка (overdue) sonini ham yangilab turish
      this.checkOverdueSummary()

      for (const task of this.tasks) {
        if (task.is_done) continue
        const triggerMs = getTaskTriggerTimestamp(task)
        if (!triggerMs) continue

        // Agar vazifa vaqti yetgan bo'lsa (yoki o'tib ketgan, lekin 12 soat ichida)
        if (isTaskDue(task, nowMs)) {
          if (!isTaskAlreadyNotified(userId, task.id, triggerMs)) {
            // Eslatma berish!
            markTaskNotified(userId, task.id, triggerMs)
            this.activeReminder = task
            playReminderBeep()
            startTitleBlink(task.title)

            // Brauzer tizimli bildirishnomasi (ruxsat bo'lsa)
            if (typeof window !== 'undefined' && 'Notification' in window && Notification.permission === 'granted') {
              try {
                const notif = new Notification('Qulay.uz — Reja eslatmasi', {
                  body: task.title,
                  icon: '/favicon.ico',
                  tag: `task-${task.id}`,
                })
                notif.onclick = () => {
                  window.focus()
                  notif.close()
                }
              } catch {}
            }
            break // Bitta tsiklda bitta asosiy eslatma ko'rsatiladi
          }
        }
      }
    },

    clearNotifiedStorage() {
      const auth = useAuthStore()
      clearAllNotifiedForUser(auth.user?.id)
      this.activeReminder = null
      stopTitleBlink()
    },

    stopNotifications() {
      this.notificationsStarted = false
      if (reminderInterval) {
        clearInterval(reminderInterval)
        reminderInterval = null
      }
      this.activeReminder = null
      this.overdueSummaryCount = 0
      stopTitleBlink()
    },

    startNotifications() {
      if (this.notificationsStarted) return
      this.notificationsStarted = true

      // Har 15 soniyada eslatmalarni tekshirish, har 60 soniyada vazifalarni yangilash
      let pollCounter = 0
      if (!reminderInterval) {
        reminderInterval = setInterval(() => {
          this.checkReminders()
          pollCounter++
          if (pollCounter >= 4) { // 4 * 15s = 60s
            pollCounter = 0
            const auth = useAuthStore()
            if (auth.isAuthenticated) {
              this.fetchTasks()
            }
          }
        }, 15000)
      }

      // Tab qayta ochilganda yoki fokus olganda zudlik bilan tekshirish
      if (typeof window !== 'undefined') {
        window.addEventListener('visibilitychange', () => {
          if (document.visibilityState === 'visible') {
            const auth = useAuthStore()
            if (auth.isAuthenticated) {
              this.fetchTasks().then(() => this.checkReminders())
            } else {
              this.checkReminders()
            }
          }
        })
        window.addEventListener('focus', () => {
          this.checkReminders()
        })
      }

      // Boshlanishida bir marta tekshirish
      this.checkReminders()
    },
  },
})
