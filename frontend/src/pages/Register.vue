<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import FormAlert from '../components/FormAlert.vue'
import { Eye, EyeOff } from 'lucide-vue-next'
import { useI18n } from '../i18n'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'

const router = useRouter()
const auth = useAuthStore()
const { t } = useI18n()

const form = reactive({ username: '', email: '', password: '', password2: '', first_name: '' })
const error = ref('')
const submitting = ref(false)
const showPassword = ref(false)
const showPasswordConfirm = ref(false)
const fieldErrors = reactive({
  username: '',
  email: '',
  password: '',
  password2: '',
  first_name: ''
})

async function handleSubmit() {
  error.value = ''
  Object.keys(fieldErrors).forEach(k => fieldErrors[k] = '')
  if (!form.username.trim() || !form.email.trim() || !form.password || !form.password2) {
    error.value = t('register.fillAll')
    return
  }
  if (form.password !== form.password2) {
    error.value = t('register.passwordMismatch')
    return
  }
  submitting.value = true
  const result = await auth.register(form)
  submitting.value = false
  if (result.success) {
    router.push({ name: 'dashboard' })
  } else {
    let hasFieldErrors = false
    if (result.errors) {
      Object.entries(result.errors).forEach(([key, msgs]) => {
        if (fieldErrors.hasOwnProperty(key)) {
          fieldErrors[key] = Array.isArray(msgs) ? msgs.join(' ') : msgs
          hasFieldErrors = true
        }
      })
    }
    error.value = hasFieldErrors ? '' : result.message
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#f6f7f9] dark:bg-[#111318] px-4 pt-16 pb-12 sm:py-12">
    <div class="absolute top-4 right-4"><LanguageSwitcher /></div>
    <div class="w-full max-w-md animate-fadeUp">
      <div class="text-center mb-8">
        <router-link :to="{ name: 'landing' }" class="inline-flex items-center gap-2.5 mb-5 group focus:outline-none rounded-xl">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-extrabold shadow-sm group-hover:scale-105 transition-transform"
            style="background: linear-gradient(135deg, rgb(var(--brand-500)), rgb(var(--brand-700)))">
            Q
          </div>
          <span class="font-bold text-xl text-slate-800 dark:text-slate-100 tracking-tight">{{ t('app.name') }}</span>
        </router-link>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white">{{ t('register.title') }}</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm mt-1">{{ t('register.subtitle') }}</p>
      </div>

      <div class="card p-6 sm:p-8">
        <FormAlert :message="error" class="mb-5" />
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <label class="label">{{ t('register.username') }}</label>
            <input v-model="form.username" type="text" class="input" placeholder="aziz_dev" />
            <p v-if="fieldErrors.username" class="text-red-500 text-sm mt-1">{{ fieldErrors.username }}</p>
          </div>
          <div>
            <label class="label">{{ t('register.name') }}</label>
            <input v-model="form.first_name" type="text" class="input" placeholder="Aziz" />
            <p v-if="fieldErrors.first_name" class="text-red-500 text-sm mt-1">{{ fieldErrors.first_name }}</p>
          </div>
          <div>
            <label class="label">{{ t('register.email') }}</label>
            <input v-model="form.email" type="email" class="input" placeholder="aziz@example.com" />
            <p v-if="fieldErrors.email" class="text-red-500 text-sm mt-1">{{ fieldErrors.email }}</p>
          </div>
          <div>
            <label class="label">{{ t('register.password') }}</label>
            <div class="relative">
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" minlength="8" />
              <p v-if="fieldErrors.password" class="text-red-500 text-sm mt-1">{{ fieldErrors.password }}</p>
              <button type="button" @click="showPassword = !showPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 focus:outline-none" :aria-label="showPassword ? t('profile.password.hide') : t('profile.password.show')">
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <div>
            <label class="label">{{ t('register.confirmPassword') }}</label>
            <div class="relative">
              <input v-model="form.password2" :type="showPasswordConfirm ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" />
              <p v-if="fieldErrors.password2" class="text-red-500 text-sm mt-1">{{ fieldErrors.password2 }}</p>
              <button type="button" @click="showPasswordConfirm = !showPasswordConfirm" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 focus:outline-none" :aria-label="showPasswordConfirm ? t('profile.password.hide') : t('profile.password.show')">
                <Eye v-if="!showPasswordConfirm" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <button type="submit" class="btn-primary w-full !mt-6" :disabled="submitting">
            <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            {{ submitting ? t('register.submitting') : t('register.submit') }}
          </button>
        </form>

        <p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
          {{ t('register.hasAccount') }}
          <router-link :to="{ name: 'login' }" class="text-brand-600 dark:text-brand-400 font-semibold hover:underline ml-1">{{ t('register.login') }}</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
