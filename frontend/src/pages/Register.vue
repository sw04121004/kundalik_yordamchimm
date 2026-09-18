<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import FormAlert from '../components/FormAlert.vue'
import { Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({ username: '', email: '', password: '', password_confirm: '' })
const error = ref('')
const submitting = ref(false)
const showPassword = ref(false)
const showPasswordConfirm = ref(false)

async function handleSubmit() {
  error.value = ''
  if (!form.username.trim() || !form.email.trim() || !form.password || !form.password_confirm) {
    error.value = "Iltimos, barcha maydonlarni to'ldiring."
    return
  }
  if (form.password !== form.password_confirm) {
    error.value = "Parollar mos kelmadi."
    return
  }
  submitting.value = true
  const result = await auth.register(form)
  submitting.value = false
  if (result.success) {
    router.push({ name: 'dashboard' })
  } else {
    error.value = result.message
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#f4f6fb] dark:bg-[#0d1117] px-4 py-12">
    <div class="w-full max-w-md animate-fadeUp">
      <div class="text-center mb-8">
        <router-link :to="{ name: 'landing' }" class="inline-flex items-center gap-2.5 mb-5 group focus:outline-none rounded-xl">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-extrabold shadow-sm group-hover:scale-105 transition-transform"
            style="background: linear-gradient(135deg, rgb(var(--brand-500)), rgb(var(--brand-700)))">
            Q
          </div>
          <span class="font-bold text-xl text-slate-800 dark:text-slate-100 tracking-tight">Kundalik</span>
        </router-link>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white">Ro'yxatdan o'tish</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm mt-1">Yangi hisob yarating</p>
      </div>

      <div class="card p-6 sm:p-8">
        <FormAlert :message="error" class="mb-5" />
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <label class="label">Foydalanuvchi nomi</label>
            <input v-model="form.username" type="text" class="input" placeholder="aziz_dev" />
          </div>
          <div>
            <label class="label">Pochta manzili</label>
            <input v-model="form.email" type="email" class="input" placeholder="aziz@example.com" />
          </div>
          <div>
            <label class="label">Parol</label>
            <div class="relative">
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" />
              <button type="button" @click="showPassword = !showPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 focus:outline-none">
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <div>
            <label class="label">Parolni tasdiqlang</label>
            <div class="relative">
              <input v-model="form.password_confirm" :type="showPasswordConfirm ? 'text' : 'password'" class="input pr-10" placeholder="••••••••" />
              <button type="button" @click="showPasswordConfirm = !showPasswordConfirm" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 focus:outline-none">
                <Eye v-if="!showPasswordConfirm" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <button type="submit" class="btn-primary w-full mt-4" :disabled="submitting">
            <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            {{ submitting ? 'Yaratilmoqda...' : "Ro'yxatdan o'tish" }}
          </button>
        </form>

        <p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-5">
          Hisobingiz bormi?
          <router-link :to="{ name: 'login' }" class="text-brand-600 dark:text-brand-400 font-semibold hover:underline ml-1">Kirish</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
