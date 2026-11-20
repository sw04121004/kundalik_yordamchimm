import { language } from '../i18n'

const DEFAULT_MESSAGES = {
  fallback: {
    uz: "Xatolik yuz berdi. Qaytadan urinib ko'ring.",
    ru: "Произошла ошибка. Повторите попытку.",
    en: "An error occurred. Please try again.",
  },
  network: {
    uz: "Internetga ulanib bo'lmadi. Aloqani tekshirib, qayta urinib ko'ring.",
    ru: "Не удалось подключиться к интернету. Проверьте соединение и повторите попытку.",
    en: "Could not connect to the internet. Please check your connection and try again.",
  },
  unauthorized: {
    uz: "Sessiya tugagan. Qayta kiring.",
    ru: "Сессия истекла. Пожалуйста, войдите снова.",
    en: "Session expired. Please log in again.",
  },
  forbidden: {
    uz: "Bu amalni bajarish uchun ruxsat yo'q.",
    ru: "У вас нет разрешения на выполнение этого действия.",
    en: "You do not have permission to perform this action.",
  },
  notFound: {
    uz: "So'ralgan ma'lumot topilmadi.",
    ru: "Запрошенные данные не найдены.",
    en: "The requested data was not found.",
  },
  rateLimit: {
    uz: "So'rovlar limiti tugadi. Birozdan so'ng qayta urinib ko'ring.",
    ru: "Лимит запросов исчерпан. Повторите попытку позже.",
    en: "Rate limit exceeded. Please try again later.",
  },
  server: {
    uz: "Serverda vaqtinchalik xatolik yuz berdi. Keyinroq qayta urinib ko'ring.",
    ru: "На сервере произошла временная ошибка. Повторите попытку позже.",
    en: "A temporary server error occurred. Please try again later.",
  },
}

const KNOWN_BACKEND_ERRORS = [
  {
    match: (msg) => /Email yuborish sozlanmagan/i.test(msg),
    translations: {
      uz: "Email yuborish sozlanmagan. Administrator pochta xizmatini sozlashi kerak.",
      ru: "Отправка почты не настроена. Администратор должен настроить почтовую службу.",
      en: "Email sending is not configured. The administrator must configure the mail service.",
    },
  },
  {
    match: (msg) => /Ob-havo xizmati vaqtincha ishlamayapti/i.test(msg),
    translations: {
      uz: "Ob-havo xizmati vaqtincha ishlamayapti. Keyinroq qayta urinib ko'ring.",
      ru: "Служба погоды временно недоступна. Повторите попытку позже.",
      en: "Weather service is temporarily unavailable. Please try again later.",
    },
  },
  {
    match: (msg) => /Login yoki parol noto'g'ri/i.test(msg),
    translations: {
      uz: "Login yoki parol noto'g'ri.",
      ru: "Неверный логин или пароль.",
      en: "Incorrect username or password.",
    },
  },
]

function getActiveLang() {
  const lang = language?.value || (typeof localStorage !== 'undefined' ? localStorage.getItem('qulay_language') : 'uz')
  return ['uz', 'ru', 'en'].includes(lang) ? lang : 'uz'
}

function translateKnownError(message, lang) {
  if (!message || typeof message !== 'string') return message
  for (const item of KNOWN_BACKEND_ERRORS) {
    if (item.match(message)) {
      return item.translations[lang] || item.translations.uz
    }
  }
  return message
}

function safePlainMessage(value) {
  return typeof value === 'string'
    && value.length <= 300
    && !/[<>]/.test(value)
    && !/(traceback|stack trace|exception|internal server|django|sql error|request was throttled)/i.test(value)
}

export function extractErrorMessage(error, fallback = null) {
  const lang = getActiveLang()
  const defaultFallback = DEFAULT_MESSAGES.fallback[lang]
  const finalFallback = fallback || defaultFallback
  const status = error?.response?.status
  const data = error?.response?.data

  if (!error?.response) return DEFAULT_MESSAGES.network[lang]
  if (status === 401) return DEFAULT_MESSAGES.unauthorized[lang]
  if (status === 403) return DEFAULT_MESSAGES.forbidden[lang]
  if (status === 404) return DEFAULT_MESSAGES.notFound[lang]
  if (status === 429) return DEFAULT_MESSAGES.rateLimit[lang]
  if (status === 503 && safePlainMessage(data?.detail)) {
    return translateKnownError(data.detail, lang)
  }
  if (status >= 500) return DEFAULT_MESSAGES.server[lang]

  if (status === 400 && data && typeof data === 'object') {
    const values = data.detail ? [data.detail] : Object.values(data).flat(Infinity)
    const message = values.find(safePlainMessage)
    if (message) return translateKnownError(message, lang)
  }
  return finalFallback
}

export function extractFieldErrors(error) {
  const lang = getActiveLang()
  const data = error?.response?.data
  if (error?.response?.status !== 400 || !data || typeof data !== 'object') return {}
  return Object.fromEntries(Object.entries(data).flatMap(([field, raw]) => {
    const messages = (Array.isArray(raw) ? raw : [raw]).flat(Infinity).filter(safePlainMessage)
    return messages.length ? [[field, messages.map(m => translateKnownError(m, lang)).join(' ')]] : []
  }))
}
