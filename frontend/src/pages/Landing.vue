<script setup>
import { computed } from 'vue'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import { useI18n } from '../i18n'

const { language } = useI18n()
const catalogCopy = {
  'AI Yordamchi': ['AI-помощник', 'AI assistant'], 'Dasturlash, ta’lim, matn, tarjima, CV va g‘oyalar bo‘yicha suhbat': ['Помощь с программированием, учёбой, текстами, переводами, резюме и идеями', 'Help with coding, learning, writing, translation, CVs, and ideas'],
  'Hisob-kitob qilish': ['Расчёты', 'Calculations'], 'Foiz, oddiy va o‘rtacha qiymat hisob-kitoblari': ['Проценты, простые и средние значения', 'Percentages, basic and average calculations'],
  'Birliklarni konvertatsiya qilish': ['Конвертация единиц', 'Unit conversion'], 'Uzunlik, og‘irlik va harorat birliklari': ['Единицы длины, веса и температуры', 'Length, weight, and temperature units'],
  'Sana va vaqtni hisoblash': ['Расчёт даты и времени', 'Date and time calculations'], 'Sanalar farqi va kunlarni hisoblash': ['Разница между датами и подсчёт дней', 'Date differences and day counts'],
  'Matn bilan ishlash': ['Работа с текстом', 'Text tools'], 'So‘z sanash, registr va tozalash vositalari': ['Подсчёт слов, смена регистра и очистка текста', 'Word count, case conversion, and text cleanup'],
  'Parol yaratish': ['Генератор паролей', 'Password generator'], 'Kuchli va xavfsiz parollar generatori': ['Создание надёжных паролей', 'Generate strong, secure passwords'],
  'Tasodifiy son yaratish': ['Случайные числа', 'Random numbers'], 'Istalgan oraliqda random sonlar': ['Случайные числа в заданном диапазоне', 'Random numbers in a chosen range'],
  'Rasmlar bilan ishlash': ['Работа с изображениями', 'Image tools'], 'Rasm o‘lchami, formati va hajmini o‘zgartirish': ['Изменение размера, формата и веса изображения', 'Resize, convert, and compress images'],
  'Ro‘yxatdan o‘ting': ['Зарегистрируйтесь', 'Sign up'], 'Bir necha soniyada bepul hisob yarating': ['Создайте бесплатный аккаунт за несколько секунд', 'Create a free account in seconds'],
  'Kerakli vositani tanlang': ['Выберите нужный инструмент', 'Choose a tool'], 'Qidiring yoki kategoriyalar orqali toping, yoki AI yordamchidan so‘rang': ['Найдите инструмент в каталоге или спросите AI-помощника', 'Search the catalog or ask the AI assistant'],
  'Natijani darhol oling': ['Получите результат сразу', 'Get your result instantly'], 'Hisob-kitob, konvertatsiya yoki AI javobi — bir zumda': ['Расчёт, конвертация или ответ AI — сразу', 'Calculations, conversion, or an AI answer in moments'],
}
function localizeCatalog(text) { return language.value === 'uz' ? text : catalogCopy[text]?.[language.value === 'ru' ? 0 : 1] || text }
const copy = computed(() => ({
  uz: { login:'Kirish', register:"Ro‘yxatdan o‘tish", badge:'✨ 100% bepul onlayn xizmatlar', lead:'Kundalik ishlaringiz uchun kerakli', online:'onlayn xizmatlar', end:' — bitta joyda.', intro:'Hisoblang, konvertatsiya qiling, matn va rasmlarni tahrirlang, parol yarating — barchasi tez, qulay va bepul.', use:'Xizmatlardan foydalanish', aiTitle:'AI Yordamchi bilan tanishing', aiText:'Dasturlash, ta’lim, matn, tarjima, CV va g‘oyalar bo‘yicha tabiiy yordam oling.', try:'Sinab ko‘rish →', what:'Kundalik Yordamchi nimalar qila oladi?', sub:'Sizga foydali bo‘ladigan vositalar', start:'Hoziroq bepul boshlash', how:'Kundalik Yordamchi qanday ishlaydi?', privacy:'Maxfiylik', terms:'Foydalanish shartlari', contact:'Aloqa', footer:'Barcha xizmatlar bepul va reklamasiz.' },
  ru: { login:'Войти', register:'Регистрация', badge:'✨ 100% бесплатные онлайн-сервисы', lead:'Всё необходимое для повседневных дел', online:'онлайн-сервисы', end:' — в одном месте.', intro:'Считайте, конвертируйте, редактируйте тексты и изображения, создавайте пароли — быстро, удобно и бесплатно.', use:'Перейти к сервисам', aiTitle:'Попробуйте AI-помощника', aiText:'Помощь с программированием, учёбой, текстами, переводами, резюме и идеями.', try:'Попробовать →', what:'Что умеет Kundalik Yordamchi?', sub:'Полезные инструменты на каждый день', start:'Начать бесплатно', how:'Как работает Kundalik Yordamchi?', privacy:'Конфиденциальность', terms:'Условия использования', contact:'Контакты', footer:'Все сервисы бесплатны и без рекламы.' },
  en: { login:'Sign in', register:'Sign up', badge:'✨ 100% free online tools', lead:'Everything you need for everyday tasks', online:'online tools', end:' — all in one place.', intro:'Calculate, convert, edit text and images, and generate passwords — quickly, easily, and for free.', use:'Explore services', aiTitle:'Meet your AI assistant', aiText:'Get help with coding, learning, writing, translation, CVs, and ideas.', try:'Try it →', what:'What can Kundalik Yordamchi do?', sub:'A selection of useful everyday tools', start:'Get started for free', how:'How does Kundalik Yordamchi work?', privacy:'Privacy', terms:'Terms of use', contact:'Contact', footer:'All services are free and ad-free.' },
}[language.value] || { login:'Kirish', register:'Ro‘yxatdan o‘tish', badge:'✨ 100% bepul onlayn xizmatlar', lead:'Kundalik ishlaringiz uchun kerakli', online:'onlayn xizmatlar', end:' — bitta joyda.', intro:'Hisoblang, konvertatsiya qiling, matn va rasmlarni tahrirlang, parol yarating — barchasi tez, qulay va bepul.', use:'Xizmatlardan foydalanish', aiTitle:'AI Yordamchi bilan tanishing', aiText:'Dasturlash, ta’lim, matn, tarjima, CV va g‘oyalar bo‘yicha tabiiy yordam oling.', try:'Sinab ko‘rish →', what:'Kundalik Yordamchi nimalar qila oladi?', sub:'Sizga foydali bo‘ladigan vositalar', start:'Hoziroq bepul boshlash', how:'Kundalik Yordamchi qanday ishlaydi?', privacy:'Maxfiylik', terms:'Foydalanish shartlari', contact:'Aloqa', footer:'Barcha xizmatlar bepul va reklamasiz.' }))

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
  copy.value.lead.split(' ').map((w, i) => ({ text: w, delay: i * 0.05 }))
)
</script>

<template>
  <div class="landing-page min-h-screen overflow-hidden dark:bg-slate-950">
    <!-- Header -->
    <header class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <LanguageSwitcher />
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-extrabold shadow-soft">
          Q
        </div>
        <span class="font-extrabold text-lg text-slate-800 dark:text-slate-100">{{ language === 'ru' ? 'Ежедневный помощник' : language === 'en' ? 'Daily Assistant' : 'Kundalik Yordamchi' }}</span>
      </div>
      <div class="flex items-center gap-2">
        <router-link :to="{ name: 'login' }" class="btn-secondary !px-4 !py-2 text-sm">{{ copy.login }}</router-link>
        <router-link :to="{ name: 'register' }" class="btn-primary !px-4 !py-2 text-sm">{{ copy.register }}</router-link>
      </div>
    </header>

    <!-- Hero -->
    <section class="relative">
      <div class="absolute inset-x-0 -top-24 h-96 bg-gradient-to-b from-brand-100/70 to-transparent dark:from-brand-900/20 -z-10"></div>
      <div class="max-w-4xl mx-auto px-4 sm:px-6 pt-16 pb-20 text-center">
        <div class="inline-flex items-center gap-1.5 bg-brand-50 dark:bg-slate-800 text-brand-700 dark:text-brand-300 text-xs font-semibold px-3 py-1.5 rounded-full mb-6 animate-fadeUp">
          {{ copy.badge }}
        </div>
        <h1 class="text-3xl sm:text-5xl font-extrabold text-slate-800 dark:text-slate-100 leading-tight">
          <span v-for="(w, i) in heroWords" :key="i" class="word-in mr-2" :style="{ animationDelay: `${w.delay}s` }">{{ w.text }}</span>
          <span class="word-in bg-gradient-to-r from-brand-500 to-brand-700 bg-clip-text text-transparent" style="animation-delay: 0.28s">{{ copy.online }}</span>
          <span class="word-in" style="animation-delay: 0.34s">{{ copy.end }}</span>
        </h1>
        <p class="mt-5 text-slate-500 dark:text-slate-400 text-base sm:text-lg max-w-2xl mx-auto animate-fadeUp" style="animation-delay: 0.4s">
          {{ copy.intro }}
        </p>
        <div class="mt-8 flex items-center justify-center gap-3 flex-wrap animate-fadeUp" style="animation-delay: 0.48s">
          <router-link :to="{ name: 'register' }" class="btn-primary text-base">
            {{ copy.use }}
          </router-link>
          <router-link :to="{ name: 'login' }" class="btn-secondary text-base">
            {{ copy.login }}
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
            <h2 class="text-white font-extrabold text-xl sm:text-2xl">{{ copy.aiTitle }}</h2>
            <p class="text-brand-100 text-sm sm:text-base mt-1.5 max-w-xl">
              {{ copy.aiText }}
            </p>
          </div>
          <router-link :to="{ name: 'register' }" class="btn-secondary shrink-0">{{ copy.try }}</router-link>
        </div>
      </div>
    </section>

    <!-- Capabilities -->
    <section class="max-w-6xl mx-auto px-4 sm:px-6 pb-24">
      <div v-reveal class="text-center mb-10">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-800 dark:text-slate-100">{{ copy.what }}</h2>
        <p class="text-slate-500 dark:text-slate-400 mt-2">{{ copy.sub }}</p>
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
          <h3 class="font-semibold text-slate-800 dark:text-slate-100">{{ localizeCatalog(item.title) }}</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 leading-snug">{{ localizeCatalog(item.desc) }}</p>
        </div>
      </div>

      <div v-reveal class="text-center mt-14">
        <router-link :to="{ name: 'register' }" class="btn-primary text-base">
          {{ copy.start }}
        </router-link>
      </div>
    </section>

    <!-- How it works -->
    <section class="max-w-5xl mx-auto px-4 sm:px-6 pb-24">
      <div v-reveal class="text-center mb-10">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-800 dark:text-slate-100">{{ copy.how }}</h2>
      </div>
      <div v-reveal class="grid grid-cols-1 sm:grid-cols-3 gap-6 stagger-children">
        <div
          v-for="step in steps"
          :key="step.title"
          class="text-center"
        >
          <div class="text-3xl mb-3">{{ step.icon }}</div>
          <h3 class="font-bold text-slate-800 dark:text-slate-100">{{ localizeCatalog(step.title) }}</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1.5 max-w-xs mx-auto">{{ localizeCatalog(step.desc) }}</p>
        </div>
      </div>
    </section>

    <footer class="border-t border-slate-100 dark:border-slate-800 py-8 text-center text-sm text-slate-400">
      <nav class="mb-3 flex justify-center gap-5"><router-link to="/privacy" class="underline">{{ copy.privacy }}</router-link><router-link to="/terms" class="underline">{{ copy.terms }}</router-link><a href="https://github.com/sw04121004/kundalik_yordamchimm/issues" class="underline">{{ copy.contact }}</a></nav>
      © 2026 {{ language === 'ru' ? 'Ежедневный помощник' : language === 'en' ? 'Daily Assistant' : 'Kundalik Yordamchi' }}. {{ copy.footer }}
    </footer>
  </div>
</template>
