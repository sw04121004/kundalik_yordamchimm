<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import FormAlert from '../components/FormAlert.vue'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({ username: '', email: '', first_name: '', password: '', password2: '' })
const error = ref('')
const submitting = ref(false)

function validate() {
  if (!form.username.trim()) return "Foydalanuvchi nomini kiriting."
  if (form.username.trim().length < 3) return "Foydalanuvchi nomi kamida 3 belgidan iborat bo\u2019lishi kerak."
  if (!form.password) return "Parolni kiriting."
  if (form.password.length < 6) return "Parol kamida 6 belgidan iborat bo\u2019lishi kerak."
  if (form.password !== form.password2) return "Parollar bir xil emas."
  if (form.email && !/^\S+@\S+\.\S+$/.test(form.email)) return "Email formati noto\u2018g\u2019ri."
  return ""
}

async function handleSubmit() {
  error.value = validate()
  if (error.value) return
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
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white">Hisob yarating</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm mt-1">Bepul, bir necha soniyada</p>
      </div>

      <!-- Card -->
      <div class="card p-6 sm:p-8">
        <FormAlert :message="error" class="mb-5" />
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <label class="label">Foydalanuvchi nomi <span class="text-red-500">*</span></label>
            <input v-model="form.username" type="text" class="input" placeholder="aziz_dev" autocomplete="username" />
          </div>
          <div>
            <label class="label">Ism <span class="text-slate-400 font-normal text-xs">(ixtiyoriy)</span></label>
            <input v-model="form.first_name" type="text" class="input" placeholder="Azizbek" />
          </div>
          <div>
            <label class="label">Email <span class="text-slate-400 font-normal text-xs">(ixtiyoriy)</span></label>
            <input v-model="form.email" type="email" class="input" placeholder="aziz@mail.com" autocomplete="email" />
          </div>
          <div>
            <label class="label">Parol <span class="text-red-500">*</span></label>
            <input v-model="form.password" type="password" class="input" placeholder="Kamida 6 ta belgi" autocomplete="new-password" />
          </div>
          <div>
            <label class="label">Parolni tasdiqlang <span class="text-red-500">*</span></label>
            <input v-model="form.password2" type="password" class="input" placeholder="••••••••" autocomplete="new-password" />
          </div>

          <button type="submit" class="btn-primary w-full mt-2" :disabled="submitting">
            <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            {{ submitting ? "Yaratilmoqda..." : "Ro\u2019yxatdan o\u2019tish" }}
          </button>
        </form>

        <p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-5">
          Hisobingiz bormi?
          <router-link :to="{ name: 'login' }" class="text-brand-600 dark:text-brand-400 font-semibold hover:underline ml-1">Kiring</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
