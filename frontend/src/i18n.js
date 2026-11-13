import { ref, watch } from 'vue'

const language = ref(['uz', 'ru', 'en'].includes(localStorage.getItem('qulay_language')) ? localStorage.getItem('qulay_language') : 'uz')
const messages = {
  uz: {},
  ru: {
    'Xizmatlar': 'Сервисы', 'AI Yordamchi': 'AI-помощник', 'Reja': 'Планировщик', 'Profil': 'Профиль', 'Chiqish': 'Выйти', 'Salom,': 'Здравствуйте,',
    'Akkaunt menyusini ochish': 'Открыть меню аккаунта', 'Xush kelibsiz!': 'Добро пожаловать!', 'Hisobingizga kiring': 'Войдите в аккаунт', 'Foydalanuvchi nomi': 'Имя пользователя', 'Parol': 'Пароль', 'Kirilmoqda...': 'Входим...', 'Kirish': 'Войти', "Hisobingiz yo'qmi?": 'Нет аккаунта?', "Ro'yxatdan o'ting": 'Зарегистрироваться', 'Roʻyxatdan oʻting': 'Зарегистрироваться', 'Ro‘yxatdan o‘ting': 'Зарегистрироваться', 'Yangi hisob yarating': 'Создайте новый аккаунт', 'Ro‘yxatdan o‘tish': 'Регистрация', "Ro'yxatdan o'tish": 'Регистрация', 'Ism': 'Имя', 'Pochta manzili': 'Электронная почта', 'Parolni tasdiqlang': 'Подтвердите пароль', 'Yaratilmoqda...': 'Создаём...', 'Hisobingiz bormi?': 'Уже есть аккаунт?'
  },
  en: {
    'Xizmatlar': 'Services', 'AI Yordamchi': 'AI Assistant', 'Reja': 'Planner', 'Profil': 'Profile', 'Chiqish': 'Log out', 'Salom,': 'Hello,',
    'Akkaunt menyusini ochish': 'Open account menu', 'Xush kelibsiz!': 'Welcome!', 'Hisobingizga kiring': 'Sign in to your account', 'Foydalanuvchi nomi': 'Username', 'Parol': 'Password', 'Kirilmoqda...': 'Signing in...', 'Kirish': 'Sign in', "Hisobingiz yo'qmi?": 'Don’t have an account?', "Ro'yxatdan o'ting": 'Sign up', 'Roʻyxatdan oʻting': 'Sign up', 'Ro‘yxatdan o‘ting': 'Sign up', 'Yangi hisob yarating': 'Create a new account', 'Ro‘yxatdan o‘tish': 'Sign up', "Ro'yxatdan o'tish": 'Sign up', 'Ism': 'Name', 'Pochta manzili': 'Email address', 'Parolni tasdiqlang': 'Confirm password', 'Yaratilmoqda...': 'Creating...', 'Hisobingiz bormi?': 'Already have an account?'
  }
}
export function setLanguage(value) {
  if (!['uz', 'ru', 'en'].includes(value)) return
  language.value = value
  localStorage.setItem('qulay_language', value)
  document.documentElement.lang = value
}
export function initLanguage() { setLanguage(language.value) }
export function useI18n() {
  const t = (key) => messages[language.value]?.[key] || key
  return { language, setLanguage, t, locale: () => ({ uz: 'uz-UZ', ru: 'ru-RU', en: 'en-US' })[language.value] }
}
watch(language, (value) => { document.documentElement.lang = value })
