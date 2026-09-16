<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store/auth'
import FormAlert from '../components/FormAlert.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const form = reactive({ username: '', password: '' })
const error = ref('')
const submitting = ref(false)

async function handleSubmit() {
  error.value = ''
  if (!form.username.trim() || !form.password) {
    error.value = "Iltimos, barcha maydonlarni to'ldiring."
    return
  }
  submitting.value = true
  const result = await auth.login(form)
  submitting.value = false
  if (result.success) {
    router.push(route.query.next || { name: 'dashboard' })
  } else {
    error.value = result.message
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#f4f6fb] dark:bg-[#0d1117] px-4 py-12">
    <div class="w-full max-w-sm animate-fadeUp">

      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link :to="{ name: 'landing' }" class="inline-flex items-center gap-2.5 mb-5 group focus:outline-none rounded-xl">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-extrabold shadow-sm group-hover:scale-105 transition-transform"
            style="background: linear-gradient(135deg, rgb(var(--brand-500)), rgb(var(--brand-700)))">
            Q
          </div>
          <span class="font-bold text-xl text-slate-800 dark:text-slate-100 tracking-tight">Kundalik</span>
        </router-link>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white">Xush kelibsiz!</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm mt-1">Hisobingizga kiring</p>
      </div>

      <!-- Card -->
      <div class="card p-6 sm:p-8">
        <FormAlert :message="error" class="mb-5" />
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <label class="label">Foydalanuvchi nomi</label>
            <input v-model="form.username" type="text" class="input" placeholder="aziz_dev" autocomplete="username" />
          </div>
          <div>
            <label class="label">Parol</label>
            <input v-model="form.password" type="password" class="input" placeholder="••••••••" autocomplete="current-password" />
          </div>
          <button type="submit" class="btn-primary w-full mt-2" :disabled="submitting">
            <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            {{ submitting ? 'Kirilmoqda...' : 'Kirish' }}
          </button>
        </form>

        <p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-5">
          Hisobingiz yo'qmi?
          <router-link :to="{ name: 'register' }" class="text-brand-600 dark:text-brand-400 font-semibold hover:underline ml-1">Ro'yxatdan o'ting</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
