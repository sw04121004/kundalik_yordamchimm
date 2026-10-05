import axios from 'axios'

const defaultBase = import.meta.env.DEV
  ? 'http://127.0.0.1:8000'
  : window.location.origin

export const API_BASE_URL = `${(import.meta.env.VITE_API_BASE_URL || defaultBase).replace(/\/$/, '')}/api`

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const access = localStorage.getItem('qulay_access')
  if (access) {
    config.headers.Authorization = `Bearer ${access}`
  }
  return config
})

let isRefreshing = false
let queue = []

function processQueue(error, token = null) {
  queue.forEach(({ resolve, reject }) => {
    if (error) reject(error)
    else resolve(token)
  })
  queue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const isAuthEndpoint =
      originalRequest?.url?.includes('/auth/login') ||
      originalRequest?.url?.includes('/auth/register') ||
      originalRequest?.url?.includes('/auth/refresh')

    if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      const refresh = localStorage.getItem('qulay_refresh')
      if (!refresh) {
        localStorage.removeItem('qulay_access')
        localStorage.removeItem('qulay_refresh')
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject })
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const { data } = await axios.post(`${API_BASE_URL}/auth/refresh/`, { refresh })
        localStorage.setItem('qulay_access', data.access)
        if (data.refresh) {
          localStorage.setItem('qulay_refresh', data.refresh)
        }
        processQueue(null, data.access)
        originalRequest.headers.Authorization = `Bearer ${data.access}`
        return api(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        localStorage.removeItem('qulay_access')
        localStorage.removeItem('qulay_refresh')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default api
