<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '../store/auth'
import AppHeader from '../components/AppHeader.vue'
import FormAlert from '../components/FormAlert.vue'

const auth = useAuthStore()

const profileForm = reactive({
  first_name: auth.user?.first_name || '',
  email: auth.user?.email || '',
})
const profileError = ref('')
const profileSuccess = ref('')
const profileSubmitting = ref(false)

async function saveProfile() {
  profileError.value = ''
  profileSuccess.value = ''
  profileSubmitting.value = true
  const result = await auth.updateProfile(profileForm)
  profileSubmitting.value = false
  if (result.success) {
    profileSuccess.value = 'Profil muvaffaqiyatli yangilandi.'
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

async function savePassword() {
  passwordError.value = ''
  passwordSuccess.value = ''

  if (!passwordForm.old_password || !passwordForm.new_password || !passwordForm.new_password2) {
    passwordError.value = 'Iltimos, barcha maydonlarni to‘ldiring.'
    return
  }
  if (passwordForm.new_password.length < 6) {
    passwordError.value = 'Yangi parol kamida 6 belgidan iborat bo‘lishi kerak.'
    return
  }
  if (passwordForm.new_password !== passwordForm.new_password2) {
    passwordError.value = 'Yangi parollar mos kelmadi.'
    return
  }

  passwordSubmitting.value = true
  const result = await auth.changePassword(passwordForm)
  passwordSubmitting.value = false

  if (result.success) {
    passwordSuccess.value = 'Parol muvaffaqiyatli o‘zgartirildi.'
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.new_password2 = ''
  } else {
    passwordError.value = result.message
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-brand-50/60 to-slate-50 dark:from-slate-900 dark:to-slate-950">
    <AppHeader />

    <main class="max-w-2xl mx-auto px-4 sm:px-6 py-10 animate-fadeUp">
      <router-link
        :to="{ name: 'dashboard' }"
        class="inline-flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400 hover:text-brand-600 transition mb-6"
      >
        ← Orqaga
      </router-link>

      <div class="flex items-center gap-3 mb-6">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-2xl shadow-soft text-white font-extrabold">
          {{ (auth.user?.username || 'U').charAt(0).toUpperCase() }}
        </div>
        <div>
          <h1 class="text-xl font-extrabold text-slate-800 dark:text-slate-100">Profil</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400">{{ auth.user?.username }}</p>
        </div>
      </div>

      <div class="card p-6 sm:p-7 mb-6">
        <h2 class="font-bold text-slate-800 dark:text-slate-100 mb-4">Shaxsiy ma’lumotlar</h2>
        <FormAlert :message="profileError" />
        <FormAlert :message="profileSuccess" type="success" />
        <form class="space-y-4" @submit.prevent="saveProfile">
          <div>
            <label class="label">Ism</label>
            <input v-model="profileForm.first_name" type="text" class="input" placeholder="Ismingiz" />
          </div>
          <div>
            <label class="label">Email</label>
            <input v-model="profileForm.email" type="email" class="input" placeholder="email@example.com" />
          </div>
          <button type="submit" class="btn-primary" :disabled="profileSubmitting">
            {{ profileSubmitting ? 'Saqlanmoqda...' : 'Saqlash' }}
          </button>
        </form>
      </div>

      <div class="card p-6 sm:p-7">
        <h2 class="font-bold text-slate-800 dark:text-slate-100 mb-4">Parolni o‘zgartirish</h2>
        <FormAlert :message="passwordError" />
        <FormAlert :message="passwordSuccess" type="success" />
        <form class="space-y-4" @submit.prevent="savePassword">
          <div>
            <label class="label">Joriy parol</label>
            <input v-model="passwordForm.old_password" type="password" class="input" placeholder="••••••••" />
          </div>
          <div>
            <label class="label">Yangi parol</label>
            <input v-model="passwordForm.new_password" type="password" class="input" placeholder="••••••••" />
          </div>
          <div>
            <label class="label">Yangi parolni tasdiqlang</label>
            <input v-model="passwordForm.new_password2" type="password" class="input" placeholder="••••••••" />
          </div>
          <button type="submit" class="btn-primary" :disabled="passwordSubmitting">
            {{ passwordSubmitting ? 'O‘zgartirilmoqda...' : 'Parolni o‘zgartirish' }}
          </button>
        </form>
      </div>
    </main>
  </div>
</template>
