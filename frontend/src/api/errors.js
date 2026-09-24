export function extractErrorMessage(error, fallback = "Xatolik yuz berdi. Qaytadan urinib ko'ring.") {
  const data = error?.response?.data;
  let rawMsg = error?.message || fallback;

  if (data) {
    if (typeof data === 'string') {
      rawMsg = data;
    } else if (data.detail) {
      rawMsg = data.detail;
    } else {
      const firstKey = Object.keys(data)[0];
      if (firstKey) {
        const value = data[firstKey];
        rawMsg = Array.isArray(value) ? value[0] : value;
      }
    }
  }
  
  if (typeof rawMsg !== 'string') return fallback;

  if (rawMsg.includes('401') || rawMsg.includes('Unauthorized') || rawMsg.includes('API_KEY')) {
    return "Xizmat vaqtinchalik ishlamayapti (API ruxsat xatosi). Administratorga murojaat qiling.";
  }
  if (rawMsg.includes('Rate limit exceeded') || rawMsg.includes('limit tugagan')) {
    return "So'rovlar limiti tugadi. Iltimos, birozdan so'ng qayta urinib ko'ring.";
  }
  if (rawMsg.includes('500') || rawMsg.includes('Internal Server Error')) {
    return "Tizimda xatolik yuz berdi. Iltimos, birozdan so'ng qayta urinib ko'ring.";
  }

  return rawMsg;
}
