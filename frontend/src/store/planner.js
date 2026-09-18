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
    tasks: [], // full list
    todayTasks: [], // just today's
    loading: false,
    error: '',
    notificationsStarted: false
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
        this.todayTasks = data.filter(t => t.due_date === todayISO())
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
        console.error("Vazifani o'chirishda xatolik:", error)
      }
    },

    startNotifications() {
      if (this.notificationsStarted) return;
      this.notificationsStarted = true;

      if (!('Notification' in window)) return;
      
      // Request permission only on user interaction if needed, but here we just ask if not denied
      if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
        Notification.requestPermission();
      }
      
      setInterval(() => {
        if (Notification.permission !== 'granted') return;
        const now = new Date();
        const currentTime = now.toTimeString().slice(0, 5); // HH:MM
        const currentDate = todayISO();
        
        // We only notify for today's tasks to optimize checking
        this.todayTasks.forEach(task => {
          if (!task.is_done && task.due_date === currentDate && task.due_time) {
            const taskTime = task.due_time.slice(0, 5);
            if (taskTime === currentTime && !task.notified) {
              const notification = new Notification("Reja vaqti keldi!", {
                body: task.title,
                icon: '/favicon.ico'
              });
              task.notified = true;
              
              notification.onclick = () => {
                window.focus();
                notification.close();
              };
            }
          }
        });
      }, 30000); // every 30 seconds
    }
  },
})
