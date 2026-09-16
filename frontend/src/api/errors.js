export function extractErrorMessage(error, fallback = "Xatolik yuz berdi. Qaytadan urinib ko‘ring.") {
  const data = error?.response?.data
  if (!data) return error?.message || fallback

  if (typeof data === 'string') return data
  if (data.detail) return data.detail

  const firstKey = Object.keys(data)[0]
  if (firstKey) {
    const value = data[firstKey]
    const text = Array.isArray(value) ? value[0] : value
    if (typeof text === 'string') return text
  }
  return fallback
}
