<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Eye, EyeOff, ArrowLeft, MailCheck } from 'lucide-vue-next'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import FormAlert from '../components/FormAlert.vue'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'
import { useI18n } from '../i18n'

const router = useRouter()
const { t } = useI18n()

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
    notice.value = data.detail || t('forgot.sent')
    step.value = 2
  } catch (e) {
    error.value = extractErrorMessage(e, t('forgot.sendError'))
  } finally {
    busy.value = false
  }
}

async function confirmReset() {
  error.value = ''
  if (form.password.length < 8) {
    error.value = t('forgot.minLength')
    return
  }
  if (form.password !== form.password2) {
    error.value = t('forgot.mismatch')
    return
  }
  busy.value = true
  try {
    await api.post('/auth/password-reset/confirm/', {
      email: form.email.trim(),
      code: form.code.trim(),
      new_password: form.password,
      new_password2: form.password2,
    })
    router.push({ name: 'login', query: { email: form.email.trim(), reset: '1' } })
  } catch (e) {
    error.value = extractErrorMessage(e, t('forgot.codeError'))
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#f6f7f9] dark:bg-[#111318] px-4 pt-16 pb-12 sm:py-12">
    <div class="absolute top-4 right-4"><LanguageSwitcher /></div>
    <main class="w-full max-w-md card p-6 sm:p-8 animate-fadeUp">
      <div class="flex items-center justify-between mb-6">
        <router-link :to="{ name: 'login' }" class="inline-flex items-center gap-2 text-sm text-brand-700 dark:text-brand-300">
          <ArrowLeft class="w-4 h-4" />
          {{ t('forgot.back') }}
        </router-link>
        <MailCheck class="w-6 h-6 text-brand-600" aria-hidden="true" />
      </div>
      <h1 class="text-2xl font-bold text-slate-900 dark:text-white">{{ t('forgot.title') }}</h1>
      <p class="text-sm text-slate-600 dark:text-slate-300 mt-2 mb-6">{{ step === 1 ? t('forgot.description') : t('forgot.sent') }}</p>
      <FormAlert v-if="error" :message="error" class="mb-4" />
      <p v-if="notice" class="mb-4 rounded-xl border border-brand-200 bg-brand-50 p-3 text-sm text-brand-800 dark:border-brand-800 dark:bg-brand-900/30 dark:text-brand-100" role="status">{{ notice }}</p>

      <form v-if="step === 1" class="space-y-4" @submit.prevent="requestCode">
        <div>
          <label class="label" for="reset-email">{{ t('forgot.email') }}</label>
          <input id="reset-email" v-model="form.email" type="email" class="input" autocomplete="email" required />
        </div>
        <button class="btn-primary w-full !mt-6" type="submit" :disabled="busy">{{ busy ? '...' : t('forgot.send') }}</button>
      </form>

      <form v-else class="space-y-4" @submit.prevent="confirmReset">
        <div>
          <label class="label" for="reset-code">{{ t('forgot.code') }}</label>
          <input id="reset-code" v-model="form.code" class="input" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]{6}" maxlength="6" required @input="error = ''" />
        </div>
        <div>
          <label class="label" for="reset-password">{{ t('forgot.newPassword') }}</label>
          <div class="relative">
            <input id="reset-password" v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input pr-11" minlength="8" autocomplete="new-password" required @input="error = ''" />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" :aria-label="showPassword ? t('profile.password.hide') : t('profile.password.show')" @click="showPassword = !showPassword">
              <Eye v-if="!showPassword" class="w-5 h-5" />
              <EyeOff v-else class="w-5 h-5" />
            </button>
          </div>
        </div>
        <div>
          <label class="label" for="reset-password-confirm">{{ t('forgot.confirmPassword') }}</label>
          <div class="relative">
            <input id="reset-password-confirm" v-model="form.password2" :type="showPassword2 ? 'text' : 'password'" class="input pr-11" minlength="8" autocomplete="new-password" required @input="error = ''" />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" :aria-label="showPassword2 ? t('profile.password.hide') : t('profile.password.show')" @click="showPassword2 = !showPassword2">
              <Eye v-if="!showPassword2" class="w-5 h-5" />
              <EyeOff v-else class="w-5 h-5" />
            </button>
          </div>
        </div>
        <button class="btn-primary w-full !mt-6" type="submit" :disabled="busy">{{ busy ? '...' : t('forgot.save') }}</button>
      </form>

      <div v-if="step === 2" class="mt-6 text-center">
        <button class="text-sm text-brand-700 underline dark:text-brand-300 font-medium hover:text-brand-800" type="button" :disabled="busy" @click="step = 1; notice = ''; error = ''">{{ t('forgot.send') }}</button>
      </div>
    </main>
  </div>
</template>
