<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Eye, EyeOff, ArrowLeft, MailCheck } from 'lucide-vue-next'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import FormAlert from '../components/FormAlert.vue'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'
import { useI18n } from '../i18n'

const router = useRouter()
const { language } = useI18n()
const translations = {
  uz: { title: 'Parolni tiklash', description: 'Akkauntingizga boglangan email manzilni kiriting. Sizga bir martalik kod yuboramiz.', email: 'Email manzil', send: 'Kod yuborish', sent: 'Agar email akkauntga tegishli bulsa, tiklash kodi yuborildi.', code: 'Emailga kelgan 6 xonali kod', password: 'Yangi parol', confirm: 'Yangi parolni tasdiqlang', save: 'Parolni yangilash', success: 'Parolingiz yangilandi. Endi yangi parol bilan kiring.', back: 'Kirishga qaytish', mismatch: 'Parollar mos kelmadi.', min: 'Parol kamida 8 belgidan iborat bolsin.' },
  ru: { title: 'Восстановление пароля', description: 'Введите email аккаунта. Мы отправим одноразовый код.', email: 'Электронная почта', send: 'Отправить код', sent: 'Если адрес привязан к аккаунту, код отправлен.', code: '6-значный код из письма', password: 'Новый пароль', confirm: 'Подтвердите новый пароль', save: 'Обновить пароль', success: 'Пароль обновлён. Войдите с новым паролем.', back: 'Вернуться ко входу', mismatch: 'Пароли не совпадают.', min: 'Пароль должен содержать не менее 8 символов.' },
  en: { title: 'Reset password', description: 'Enter the email address on your account. We will send a one-time code.', email: 'Email address', send: 'Send code', sent: 'If this email belongs to an account, a reset code has been sent.', code: '6-digit code from email', password: 'New password', confirm: 'Confirm new password', save: 'Update password', success: 'Your password was updated. Sign in with the new password.', back: 'Back to sign in', mismatch: 'Passwords do not match.', min: 'Password must contain at least 8 characters.' },
}
translations.ru = {
  title: '\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u0430\u0440\u043e\u043b\u044f',
  description: '\u0412\u0432\u0435\u0434\u0438\u0442\u0435 email \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430. \u041c\u044b \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u043c \u043e\u0434\u043d\u043e\u0440\u0430\u0437\u043e\u0432\u044b\u0439 \u043a\u043e\u0434.',
  email: '\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u043f\u043e\u0447\u0442\u0430', send: '\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u043a\u043e\u0434',
  sent: '\u0415\u0441\u043b\u0438 email \u043f\u0440\u0438\u0432\u044f\u0437\u0430\u043d \u043a \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0443, \u043a\u043e\u0434 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d.',
  code: '6-\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u043a\u043e\u0434 \u0438\u0437 \u043f\u0438\u0441\u044c\u043c\u0430', password: '\u041d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c', confirm: '\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u043d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c',
  save: '\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u043f\u0430\u0440\u043e\u043b\u044c', success: '\u041f\u0430\u0440\u043e\u043b\u044c \u043e\u0431\u043d\u043e\u0432\u043b\u0451\u043d. \u0412\u043e\u0439\u0434\u0438\u0442\u0435 \u0441 \u043d\u043e\u0432\u044b\u043c \u043f\u0430\u0440\u043e\u043b\u0435\u043c.',
  back: '\u041d\u0430\u0437\u0430\u0434 \u043a\u043e \u0432\u0445\u043e\u0434\u0443', mismatch: '\u041f\u0430\u0440\u043e\u043b\u0438 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442.', min: '\u041f\u0430\u0440\u043e\u043b\u044c \u0434\u043e\u043b\u0436\u0435\u043d \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0442\u044c \u043d\u0435 \u043c\u0435\u043d\u0435\u0435 8 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432.'
}
translations.uz.mismatch = 'Parollar mos kelmadi.'
const t = computed(() => translations[language.value] || translations.en)
const form = reactive({ email: '', code: '', password: '', password2: '' })
const step = ref(1)
const busy = ref(false)
const error = ref('')
const notice = ref('')
const showPassword = ref(false)
const showPassword2 = ref(false)

async function requestCode() {
  error.value = ''
  busy.value = true
  try {
    const { data } = await api.post('/auth/password-reset/request/', { email: form.email.trim() })
    notice.value = data.detail || t.value.sent
    step.value = 2
  } catch (e) {
    error.value = extractErrorMessage(e, 'Emailga kod yuborilmadi. Email sozlamalarini tekshiring yoki keyinroq qayta urinib koring.')
  } finally { busy.value = false }
}

async function confirmReset() {
  error.value = ''
  if (form.password.length < 8) { error.value = t.value.min; return }
  if (form.password !== form.password2) { error.value = t.value.mismatch; return }
  busy.value = true
  try {
    await api.post('/auth/password-reset/confirm/', {
      email: form.email.trim(), code: form.code.trim(), new_password: form.password, new_password2: form.password2,
    })
    router.push({ name: 'login', query: { email: form.email.trim(), reset: '1' } })
  } catch (e) {
    error.value = extractErrorMessage(e, 'Kod yaroqsiz yoki muddati tugagan. Yangi kod sorang.')
  } finally { busy.value = false }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#f6f7f9] dark:bg-[#111318] px-4 py-12">
    <div class="absolute top-4 right-4"><LanguageSwitcher /></div>
    <main class="w-full max-w-md card p-6 sm:p-8">
      <div class="flex items-center justify-between mb-6">
        <router-link :to="{ name: 'login' }" class="inline-flex items-center gap-2 text-sm text-brand-700 dark:text-brand-300"><ArrowLeft class="w-4 h-4" />{{ t.back }}</router-link>
        <MailCheck class="w-6 h-6 text-brand-600" aria-hidden="true" />
      </div>
      <h1 class="text-2xl font-bold text-slate-900 dark:text-white">{{ t.title }}</h1>
      <p class="text-sm text-slate-600 dark:text-slate-300 mt-2 mb-6">{{ step === 1 ? t.description : t.sent }}</p>
      <FormAlert v-if="error" :message="error" class="mb-4" />
      <p v-if="notice" class="mb-4 rounded-xl border border-brand-200 bg-brand-50 p-3 text-sm text-brand-800 dark:border-brand-800 dark:bg-brand-900/30 dark:text-brand-100" role="status">{{ notice }}</p>
      <form v-if="step === 1" class="space-y-4" @submit.prevent="requestCode">
        <label class="label" for="reset-email">{{ t.email }}</label>
        <input id="reset-email" v-model="form.email" type="email" class="input" autocomplete="email" required />
        <button class="btn-primary w-full" type="submit" :disabled="busy">{{ busy ? '...' : t.send }}</button>
      </form>
      <form v-else class="space-y-4" @submit.prevent="confirmReset">
        <div><label class="label" for="reset-code">{{ t.code }}</label><input id="reset-code" v-model="form.code" class="input" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]{6}" maxlength="6" required /></div>
        <div><label class="label" for="reset-password">{{ t.password }}</label><div class="relative"><input id="reset-password" v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input pr-11" minlength="8" autocomplete="new-password" required /><button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" :aria-label="showPassword ? 'Hide password' : 'Show password'" @click="showPassword = !showPassword"><Eye v-if="!showPassword" class="w-5 h-5"/><EyeOff v-else class="w-5 h-5"/></button></div></div>
        <div><label class="label" for="reset-password-confirm">{{ t.confirm }}</label><div class="relative"><input id="reset-password-confirm" v-model="form.password2" :type="showPassword2 ? 'text' : 'password'" class="input pr-11" minlength="8" autocomplete="new-password" required /><button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" :aria-label="showPassword2 ? 'Hide password' : 'Show password'" @click="showPassword2 = !showPassword2"><Eye v-if="!showPassword2" class="w-5 h-5"/><EyeOff v-else class="w-5 h-5"/></button></div></div>
        <button class="btn-primary w-full" type="submit" :disabled="busy">{{ busy ? '...' : t.save }}</button>
      </form>
      <button v-if="step === 2" class="mt-4 text-sm text-brand-700 underline dark:text-brand-300" type="button" :disabled="busy" @click="step = 1; notice = ''; error = ''">{{ t.send }}</button>
    </main>
  </div>
</template>
