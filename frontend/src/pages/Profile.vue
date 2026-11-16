<script setup>
import { reactive, ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import AppHeader from '../components/AppHeader.vue'
import FormAlert from '../components/FormAlert.vue'
import { Eye, EyeOff } from 'lucide-vue-next'
import { useI18n } from '../i18n'

const router = useRouter()
const auth = useAuthStore()
const { t } = useI18n()

const profileForm = reactive({
  first_name: '',
  email: '',
})
const profileError = ref('')
const profileSuccess = ref('')
const profileSubmitting = ref(false)

onMounted(() => {
  profileForm.first_name = auth.user?.first_name || ''
  profileForm.email = auth.user?.email || ''
})

async function saveProfile() {
  profileError.value = ''
  profileSuccess.value = ''
  profileSubmitting.value = true
  const result = await auth.updateProfile(profileForm)
  profileSubmitting.value = false
  if (result.success) {
    profileSuccess.value = t('profile.saved')
  } else {
    profileError.value = result.message
  }
}

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password2: '',
})
const passwordError = ref('')
const passwordSuccess = ref('')
const passwordSubmitting = ref(false)
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showPasswordConfirm = ref(false)
const showDeletePassword = ref(false)
const showDeleteDialog = ref(false)
const deletePassword = ref('')
const deleteConfirmation = ref('')
const deleteError = ref('')
const deleteSubmitting = ref(false)

const deleteConfirmWord = computed(() => t('profile.danger.dialog.confirmWord'))

async function savePassword() {
  passwordError.value = ''
  passwordSuccess.value = ''

  if (!passwordForm.old_password || !passwordForm.new_password || !passwordForm.new_password2) {
    passwordError.value = t('profile.password.fillAll')
    return
  }
  if (passwordForm.new_password.length < 8) {
    passwordError.value = t('profile.password.minLength')
    return
  }
  if (passwordForm.new_password !== passwordForm.new_password2) {
    passwordError.value = t('profile.password.mismatch')
    return
  }

  passwordSubmitting.value = true
  const result = await auth.changePassword(passwordForm)
  passwordSubmitting.value = false

  if (result.success) {
    passwordSuccess.value = t('profile.password.changed')
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.new_password2 = ''
  } else {
    passwordError.value = result.message
  }
}

function closeDeleteDialog() {
  if (deleteSubmitting.value) return
  showDeleteDialog.value = false
  deletePassword.value = ''
  deleteConfirmation.value = ''
  deleteError.value = ''
  showDeletePassword.value = false
}

async function deleteAccount() {
  deleteError.value = ''
  if (!deletePassword.value) {
    deleteError.value = t('profile.danger.dialog.noPassword')
    return
  }
  const expected = deleteConfirmWord.value.toLowerCase()
  const entered = deleteConfirmation.value.trim().toLowerCase()
  if (entered !== expected && entered !== "o'chirish" && entered !== "o‘chirish" && entered !== "delete" && entered !== "удалить") {
    deleteError.value = t('profile.danger.dialog.wrongConfirm')
    return
  }

  deleteSubmitting.value = true
  const result = await auth.deleteAccount(deletePassword.value)
  deleteSubmitting.value = false
  if (result.success) {
    await router.replace({ name: 'landing' })
  } else {
    deleteError.value = result.message
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-brand-50/60 to-slate-50 dark:from-[#1b2230] dark:to-[#111318]">
    <AppHeader />

    <main class="max-w-2xl mx-auto px-4 sm:px-6 py-10 animate-fadeUp">
      <router-link
        :to="{ name: 'dashboard' }"
        class="inline-flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400 hover:text-brand-600 transition mb-6"
      >
        ← {{ t('profile.back') }}
      </router-link>

      <div class="flex items-center gap-3 mb-6">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-2xl shadow-soft text-white font-extrabold">
          {{ (auth.user?.username || 'U').charAt(0).toUpperCase() }}
        </div>
        <div>
          <h1 class="text-xl font-extrabold text-slate-800 dark:text-slate-100">{{ t('profile.title') }}</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400">{{ auth.user?.username }}</p>
        </div>
      </div>

      <div class="card p-6 sm:p-7 mb-6">
        <h2 class="font-bold text-slate-800 dark:text-slate-100 mb-4">{{ t('profile.personal') }}</h2>
        <FormAlert :message="profileError" />
        <FormAlert :message="profileSuccess" type="success" />
        <form class="space-y-4" @submit.prevent="saveProfile">
          <div>
            <label class="label">{{ t('profile.name') }}</label>
            <input v-model="profileForm.first_name" type="text" class="input" :placeholder="t('profile.name')" />
          </div>
          <div>
            <label class="label">{{ t('profile.email') }}</label>
            <input v-model="profileForm.email" type="email" class="input" placeholder="email@example.com" />
          </div>
          <button type="submit" class="btn-primary" :disabled="profileSubmitting">
            {{ profileSubmitting ? '...' : t('profile.save') }}
          </button>
        </form>
      </div>

      <div class="card p-6 sm:p-7">
        <h2 class="font-bold text-slate-800 dark:text-slate-100 mb-4">{{ t('profile.password.title') }}</h2>
        <FormAlert :message="passwordError" />
        <FormAlert :message="passwordSuccess" type="success" />
        <form class="space-y-4" @submit.prevent="savePassword">
          <div>
            <label class="label">{{ t('profile.password.current') }}</label>
            <div class="relative">
              <input v-model="passwordForm.old_password" :type="showOldPassword ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" autocomplete="current-password" />
              <button type="button" :aria-label="showOldPassword ? t('profile.password.hide') : t('profile.password.show')" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300" @click="showOldPassword = !showOldPassword">
                <Eye v-if="!showOldPassword" class="w-5 h-5" /><EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <div>
            <label class="label">{{ t('profile.password.new') }}</label>
            <div class="relative">
              <input v-model="passwordForm.new_password" :type="showNewPassword ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" autocomplete="new-password" />
              <button type="button" :aria-label="showNewPassword ? t('profile.password.hide') : t('profile.password.show')" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300" @click="showNewPassword = !showNewPassword">
                <Eye v-if="!showNewPassword" class="w-5 h-5" /><EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <div>
            <label class="label">{{ t('profile.password.confirm') }}</label>
            <div class="relative">
              <input v-model="passwordForm.new_password2" :type="showPasswordConfirm ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" autocomplete="new-password" />
              <button type="button" :aria-label="showPasswordConfirm ? t('profile.password.hide') : t('profile.password.show')" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300" @click="showPasswordConfirm = !showPasswordConfirm">
                <Eye v-if="!showPasswordConfirm" class="w-5 h-5" /><EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <button type="submit" class="btn-primary" :disabled="passwordSubmitting">
            {{ passwordSubmitting ? t('profile.password.submitting') : t('profile.password.submit') }}
          </button>
        </form>
      </div>

      <section class="card p-6 sm:p-7 mt-6 border border-red-200 dark:border-red-900/60">
        <h2 class="font-bold text-red-700 dark:text-red-400 mb-2">{{ t('profile.danger.title') }}</h2>
        <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">{{ t('profile.danger.description') }}</p>
        <button type="button" class="btn-secondary !border-red-300 !text-red-700 hover:!bg-red-50 dark:!border-red-900 dark:!text-red-400 dark:hover:!bg-red-950/30" @click="showDeleteDialog = true">
          {{ t('profile.danger.button') }}
        </button>
      </section>
    </main>

    <div v-if="showDeleteDialog" class="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/60 px-4 py-8" @click.self="closeDeleteDialog" @keydown.esc.stop="closeDeleteDialog" tabindex="-1">
      <section role="dialog" aria-modal="true" aria-labelledby="delete-account-title" class="card w-full max-w-md p-6 sm:p-7 shadow-2xl">
        <h2 id="delete-account-title" class="text-lg font-extrabold text-red-700 dark:text-red-400 mb-2">{{ t('profile.danger.dialog.title') }}</h2>
        <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">{{ t('profile.danger.dialog.warning') }}</p>
        <FormAlert :message="deleteError" />
        <form class="space-y-4" @submit.prevent="deleteAccount">
          <div>
            <label for="delete-account-password" class="label">{{ t('profile.password.current') }}</label>
            <div class="relative">
              <input id="delete-account-password" v-model="deletePassword" :type="showDeletePassword ? 'text' : 'password'" class="input pr-10" autocomplete="current-password" required />
              <button type="button" :aria-label="showDeletePassword ? t('profile.password.hide') : t('profile.password.show')" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300" @click="showDeletePassword = !showDeletePassword">
                <Eye v-if="!showDeletePassword" class="w-5 h-5" /><EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <div>
            <label for="delete-account-confirmation" class="label">{{ t('profile.danger.dialog.confirmLabel') }}</label>
            <input id="delete-account-confirmation" v-model="deleteConfirmation" type="text" class="input" :placeholder="deleteConfirmWord" autocomplete="off" required />
          </div>
          <div class="flex justify-end gap-3">
            <button type="button" class="btn-secondary" :disabled="deleteSubmitting" @click="closeDeleteDialog">{{ t('profile.danger.dialog.cancel') }}</button>
            <button type="submit" class="btn-primary !bg-red-600 hover:!bg-red-700" :disabled="deleteSubmitting">
              {{ deleteSubmitting ? t('profile.danger.dialog.submitting') : t('profile.danger.dialog.submit') }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>
