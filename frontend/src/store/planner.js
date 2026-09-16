import { defineStore } from 'pinia'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'

function todayISO() {
  const d = new Date()
  const offset = d.getTimezoneOffset()
  const local = new Date(d.getTime() - offset * 60 * 1000)
  return local.toISOString().slice(0, 10)
}

export const usePlannerStore = defineStore('planner', {
  state: () => ({
    tasks: [], // full list (used by the Reja page)
    todayTasks: [], // just today's tasks (used by the dashboard widget)
    loading: false,
    error: '',
  }),

  getters: {
    todayDone: (state) => state.todayTasks.filter((t) => t.is_done).length,
    todayTotal: (state) => state.todayTasks.length,
    todayPercent: (state) => {
      if (!state.todayTasks.length) return 0
      const done = state.todayTasks.filter((t) => t.is_done).length
      return Math.round((done / state.todayTasks.length) * 100)
    },
  },

  actions: {
    async fetchTasks() {
      this.loading = true
      try {
        const { data } = await api.get('/planner/tasks/')
        this.tasks = data
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
        const message = extractErrorMessage(error, 'Vazifa qo‘shib bo‘lmadi.')
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
      } catch (error) {
        console.error('Vazifani yangilashda xatolik:', error)
      }
    },

    async deleteTask(id) {
      try {
        await api.delete(`/planner/tasks/${id}/`)
        this.tasks = this.tasks.filter((t) => t.id !== id)
        this.todayTasks = this.todayTasks.filter((t) => t.id !== id)
      } catch (error) {
        console.error('Vazifani o‘chirishda xatolik:', error)
      }
    },
  },
})
