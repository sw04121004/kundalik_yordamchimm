<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store/auth'
import FormAlert from '../components/FormAlert.vue'
import { Eye, EyeOff } from 'lucide-vue-next'
import { useI18n } from '../i18n'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const { t, language } = useI18n()
const resetComplete = computed(() => route.query.reset === '1')

const form = reactive({ username: typeof route.query.email === 'string' ? route.query.email : '', password: '' })
const error = ref('')
const submitting = ref(false)
const showPassword = ref(false)

async function handleSubmit() {
  error.value = ''
  if (!form.username.trim() || !form.password) {
    error.value = "Iltimos, barcha maydonlarni to'ldiring."
    return
  }
  submitting.value = true
  const result = await auth.login({ ...form, username: form.username.trim() })
  submitting.value = false
  if (result.success) {
    router.push(route.query.next || { name: 'dashboard' })
  } else {
    error.value = result.message
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#f6f7f9] dark:bg-[#111318] px-4 py-12">
    <div class="absolute top-4 right-4"><LanguageSwitcher /></div>
    <div class="w-full max-w-sm animate-fadeUp">
      <div class="text-center mb-8">
        <router-link :to="{ name: 'landing' }" class="inline-flex items-center gap-2.5 mb-5 group focus:outline-none rounded-xl">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-extrabold shadow-sm group-hover:scale-105 transition-transform"
            style="background: linear-gradient(135deg, rgb(var(--brand-500)), rgb(var(--brand-700)))">
            Q
          </div>
          <span class="font-bold text-xl text-slate-800 dark:text-slate-100 tracking-tight">Kundalik</span>
        </router-link>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white">{{ t('Xush kelibsiz!') }}</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm mt-1">{{ t('Hisobingizga kiring') }}</p>
      </div>

      <div class="card p-6 sm:p-8">
        <FormAlert :message="error" class="mb-5" />
        <p v-if="resetComplete" class="mb-4 rounded-xl bg-emerald-50 p-3 text-sm text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-100" role="status">{{ language === 'ru' ? 'Пароль обновлён. Войдите с новым паролем.' : language === 'en' ? 'Password updated. Sign in with your new password.' : 'Parol yangilandi. Yangi parol bilan kiring.' }}</p>
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <label class="label">{{ t('Foydalanuvchi nomi') }}</label>
            <input v-model="form.username" type="text" class="input" placeholder="aziz_dev" autocomplete="username" />
          </div>
          <div>
            <label class="label">{{ t('Parol') }}</label>
            <div class="relative">
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" autocomplete="current-password" />
              <button type="button" @click="showPassword = !showPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 focus:outline-none">
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <button type="submit" class="btn-primary w-full mt-2" :disabled="submitting">
            <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            {{ submitting ? t('Kirilmoqda...') : t('Kirish') }}
          </button>
        </form>

        <div class="text-right -mt-2">
          <router-link :to="{ name: 'forgot-password' }" class="text-sm text-brand-700 dark:text-brand-300 font-semibold hover:underline">{{ t('Parolni unutdingizmi?') }}</router-link>
        </div>

        <p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-5">
          {{ t("Hisobingiz yo'qmi?") }}
          <router-link :to="{ name: 'register' }" class="text-brand-600 dark:text-brand-400 font-semibold hover:underline ml-1">{{ t("Ro'yxatdan o'ting") }}</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
