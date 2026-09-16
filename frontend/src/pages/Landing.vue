<script setup>
import { computed } from 'vue'

const capabilities = [
  { icon: '🤖', title: 'AI Yordamchi', desc: 'Dasturlash, ta’lim, matn, tarjima, CV va g‘oyalar bo‘yicha suhbat' },
  { icon: '🧮', title: 'Hisob-kitob qilish', desc: 'Foiz, oddiy va o‘rtacha qiymat hisob-kitoblari' },
  { icon: '🔄', title: 'Birliklarni konvertatsiya qilish', desc: 'Uzunlik, og‘irlik va harorat birliklari' },
  { icon: '📅', title: 'Sana va vaqtni hisoblash', desc: 'Sanalar farqi va kunlarni hisoblash' },
  { icon: '📝', title: 'Matn bilan ishlash', desc: 'So‘z sanash, registr va tozalash vositalari' },
  { icon: '🔐', title: 'Parol yaratish', desc: 'Kuchli va xavfsiz parollar generatori' },
  { icon: '🎲', title: 'Tasodifiy son yaratish', desc: 'Istalgan oraliqda random sonlar' },
  { icon: '🖼️', title: 'Rasmlar bilan ishlash', desc: 'Rasm o‘lchami, formati va hajmini o‘zgartirish' },
]

const steps = [
  { icon: '1️⃣', title: 'Ro‘yxatdan o‘ting', desc: 'Bir necha soniyada bepul hisob yarating' },
  { icon: '2️⃣', title: 'Kerakli vositani tanlang', desc: 'Qidiring yoki kategoriyalar orqali toping, yoki AI yordamchidan so‘rang' },
  { icon: '3️⃣', title: 'Natijani darhol oling', desc: 'Hisob-kitob, konvertatsiya yoki AI javobi — bir zumda' },
]

// Hero sarlavhasi so'z-bo'yicha animatsiya bilan chiqishi uchun
const heroWords = computed(() =>
  'Kundalik ishlaringiz uchun kerakli'.split(' ').map((w, i) => ({ text: w, delay: i * 0.05 }))
)
</script>

<template>
  <div class="min-h-screen overflow-hidden dark:bg-slate-950">
    <!-- Header -->
    <header class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-extrabold shadow-soft">
          Q
        </div>
        <span class="font-extrabold text-lg text-slate-800 dark:text-slate-100">Kundalik Yordamchi</span>
      </div>
      <div class="flex items-center gap-2">
        <router-link :to="{ name: 'login' }" class="btn-secondary !px-4 !py-2 text-sm">Kirish</router-link>
        <router-link :to="{ name: 'register' }" class="btn-primary !px-4 !py-2 text-sm">Ro‘yxatdan o‘tish</router-link>
      </div>
    </header>

    <!-- Hero -->
    <section class="relative">
      <div class="absolute inset-x-0 -top-24 h-96 bg-gradient-to-b from-brand-100/70 to-transparent dark:from-brand-900/20 -z-10"></div>
      <div class="max-w-4xl mx-auto px-4 sm:px-6 pt-16 pb-20 text-center">
        <div class="inline-flex items-center gap-1.5 bg-brand-50 dark:bg-slate-800 text-brand-700 dark:text-brand-300 text-xs font-semibold px-3 py-1.5 rounded-full mb-6 animate-fadeUp">
          ✨ 100% bepul online xizmatlar
        </div>
        <h1 class="text-3xl sm:text-5xl font-extrabold text-slate-800 dark:text-slate-100 leading-tight">
          <span v-for="(w, i) in heroWords" :key="i" class="word-in mr-2" :style="{ animationDelay: `${w.delay}s` }">{{ w.text }}</span>
          <span class="word-in bg-gradient-to-r from-brand-500 to-brand-700 bg-clip-text text-transparent" style="animation-delay: 0.28s">online xizmatlar</span>
          <span class="word-in" style="animation-delay: 0.34s"> — bitta joyda.</span>
        </h1>
        <p class="mt-5 text-slate-500 dark:text-slate-400 text-base sm:text-lg max-w-2xl mx-auto animate-fadeUp" style="animation-delay: 0.4s">
          Hisoblang, konvertatsiya qiling, matn va rasmlarni tahrirlang, parol generatsiya qiling — barchasi tez,
          qulay va butunlay bepul.
        </p>
        <div class="mt-8 flex items-center justify-center gap-3 flex-wrap animate-fadeUp" style="animation-delay: 0.48s">
          <router-link :to="{ name: 'register' }" class="btn-primary text-base">
            Xizmatlardan foydalanish
          </router-link>
          <router-link :to="{ name: 'login' }" class="btn-secondary text-base">
            Kirish
          </router-link>
        </div>
      </div>
    </section>

    <!-- AI Assistant highlight -->
    <section class="max-w-5xl mx-auto px-4 sm:px-6 pb-20">
      <div
        v-reveal
        class="card p-6 sm:p-8 bg-gradient-to-br from-brand-600 to-brand-800 border-none shadow-soft animate-softPulse hover:scale-[1.01] transition-transform duration-300"
      >
        <div class="flex items-center gap-5 flex-wrap">
          <div class="w-16 h-16 rounded-2xl bg-white/15 flex items-center justify-center text-4xl shrink-0">🤖</div>
          <div class="flex-1 min-w-[240px]">
            <h2 class="text-white font-extrabold text-xl sm:text-2xl">AI Yordamchi bilan tanishing</h2>
            <p class="text-brand-100 text-sm sm:text-base mt-1.5 max-w-xl">
              Dasturlash, ta’lim, matn, tarjima, CV va g‘oyalar bo‘yicha yordam — tabiiy, xato-nuqsonli
              o‘zbekcha yozsangiz ham tushunadi. "kodim ishlameyapti" desangiz ham yetarli.
            </p>
          </div>
          <router-link :to="{ name: 'register' }" class="btn-secondary shrink-0">Sinab ko‘rish →</router-link>
        </div>
      </div>
    </section>

    <!-- Capabilities -->
    <section class="max-w-6xl mx-auto px-4 sm:px-6 pb-24">
      <div v-reveal class="text-center mb-10">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-800 dark:text-slate-100">Kundalik Yordamchi nimalar qila oladi?</h2>
        <p class="text-slate-500 dark:text-slate-400 mt-2">Sizga foydali bo‘lgan vositalarning bir qismi</p>
      </div>
      <div v-reveal class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 stagger-children">
        <div
          v-for="item in capabilities"
          :key="item.title"
          class="group card p-5 hover:-translate-y-1 hover:shadow-soft transition-all duration-200"
        >
          <div class="w-11 h-11 rounded-xl bg-brand-50 dark:bg-slate-700 flex items-center justify-center text-2xl mb-3 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-6">
            {{ item.icon }}
          </div>
          <h3 class="font-semibold text-slate-800 dark:text-slate-100">{{ item.title }}</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 leading-snug">{{ item.desc }}</p>
        </div>
      </div>

      <div v-reveal class="text-center mt-14">
        <router-link :to="{ name: 'register' }" class="btn-primary text-base">
          Hoziroq bepul boshlash
        </router-link>
      </div>
    </section>

    <!-- How it works -->
    <section class="max-w-5xl mx-auto px-4 sm:px-6 pb-24">
      <div v-reveal class="text-center mb-10">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-800 dark:text-slate-100">Kundalik Yordamchi qanday ishlaydi?</h2>
      </div>
      <div v-reveal class="grid grid-cols-1 sm:grid-cols-3 gap-6 stagger-children">
        <div
          v-for="step in steps"
          :key="step.title"
          class="text-center"
        >
          <div class="text-3xl mb-3">{{ step.icon }}</div>
          <h3 class="font-bold text-slate-800 dark:text-slate-100">{{ step.title }}</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1.5 max-w-xs mx-auto">{{ step.desc }}</p>
        </div>
      </div>
    </section>

    <footer class="border-t border-slate-100 dark:border-slate-800 py-8 text-center text-sm text-slate-400">
      © 2026 Kundalik Yordamchi. Barcha xizmatlar bepul va reklamasiz.
    </footer>
  </div>
</template>
