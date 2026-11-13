const SAFE_FALLBACK = "Xatolik yuz berdi. Qaytadan urinib ko'ring."

function safePlainMessage(value) {
  return typeof value === 'string'
    && value.length <= 300
    && !/[<>]/.test(value)
    && !/(traceback|stack trace|exception|internal server|django|sql error|request was throttled)/i.test(value)
}

export function extractErrorMessage(error, fallback = SAFE_FALLBACK) {
  const status = error?.response?.status
  const data = error?.response?.data

  if (!error?.response) return "Internetga ulanib bo'lmadi. Aloqani tekshirib, qayta urinib ko'ring."
  if (status === 401) return "Sessiya tugagan. Qayta kiring."
  if (status === 403) return "Bu amalni bajarish uchun ruxsat yo'q."
  if (status === 404) return "So'ralgan ma'lumot topilmadi."
  if (status === 429) return "So'rovlar limiti tugadi. Birozdan so'ng qayta urinib ko'ring."
  if (status === 503 && safePlainMessage(data?.detail)) return data.detail
  if (status >= 500) return "Serverda vaqtinchalik xatolik yuz berdi. Keyinroq qayta urinib ko'ring."

  if (status === 400 && data && typeof data === 'object') {
    const values = data.detail ? [data.detail] : Object.values(data).flat(Infinity)
    const message = values.find(safePlainMessage)
    if (message) return message
  }
  return fallback
}

export function extractFieldErrors(error) {
  const data = error?.response?.data
  if (error?.response?.status !== 400 || !data || typeof data !== 'object') return {}
  return Object.fromEntries(Object.entries(data).flatMap(([field, raw]) => {
    const messages = (Array.isArray(raw) ? raw : [raw]).flat(Infinity).filter(safePlainMessage)
    return messages.length ? [[field, messages.join(' ')]] : []
  }))
}
