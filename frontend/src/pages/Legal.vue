<script setup>
import { computed } from 'vue'
import AppHeader from '../components/AppHeader.vue'
import { useI18n } from '../i18n'
import { useRoute } from 'vue-router'
const { language } = useI18n()
const route = useRoute()
const copy = {
  uz: { privacy: 'Maxfiylik siyosati', terms: 'Foydalanish shartlari', data: 'Hisob ma’lumotlari, rejalaringiz, moliya yozuvlari va AI suhbatlari xizmatni ko‘rsatish uchun saqlanadi. Profil sahifasidan akkauntni o‘chirishingiz mumkin; bunda unga tegishli ma’lumotlar ham o‘chadi.', third: 'AI so‘rovlari tanlangan AI provayderiga, ob-havo so‘rovlari Open-Meteo xizmatiga yuboriladi. Shaxsiy yoki maxfiy ma’lumotlarni so‘rovlarga kiritmang.', use: 'Xizmatlardan o‘z javobgarligingiz doirasida foydalaning. Hisob ma’lumotlarini sir saqlang va noqonuniy yoki zararli maqsadda foydalanmang. AI va tashqi ob-havo ma’lumotlari xato yoki kechikkan bo‘lishi mumkin; muhim qarorlar oldidan mustaqil tekshiring.', contact: 'Aloqa', contactText: 'Loyiha bo‘yicha savollar va maxfiylik so‘rovlari uchun GitHub repository Issues bo‘limidan foydalaning.' },
  ru: { privacy: 'Политика конфиденциальности', terms: 'Условия использования', data: 'Для работы сервиса хранятся данные аккаунта, планы, финансовые записи и переписки с ИИ. Аккаунт и связанные с ним данные можно удалить в профиле.', third: 'Запросы ИИ передаются выбранному провайдеру ИИ, а запросы погоды — Open-Meteo. Не вводите личные или конфиденциальные сведения в запросы.', use: 'Используйте сервис на собственную ответственность. Храните данные входа в тайне и не используйте сервис незаконно или во вред. Ответы ИИ и внешние данные погоды могут быть ошибочными или запаздывать; проверяйте важные сведения самостоятельно.', contact: 'Контакты', contactText: 'По вопросам проекта и конфиденциальности используйте раздел Issues репозитория GitHub.' },
  en: { privacy: 'Privacy policy', terms: 'Terms of use', data: 'Account details, plans, finance records, and AI conversations are stored to provide the service. You can delete your account and its associated data from the profile page.', third: 'AI prompts are sent to the selected AI provider, and weather requests are sent to Open-Meteo. Do not include personal or confidential information in prompts.', use: 'Use the service responsibly. Keep your credentials private and do not use the service unlawfully or harmfully. AI responses and external weather data may be inaccurate or delayed; independently verify important information.', contact: 'Contact', contactText: 'For project questions and privacy requests, use the GitHub repository Issues page.' }
}
const text = computed(() => copy[language.value] || copy.uz)
const isPrivacy = computed(() => route.path.endsWith('/privacy'))
</script>
<template>
  <AppHeader />
  <main class="max-w-3xl mx-auto px-4 py-12 space-y-8">
    <h1 class="text-3xl font-bold">{{ isPrivacy ? text.privacy : text.terms }}</h1>
    <section v-if="isPrivacy" class="card p-6 space-y-4"><p>{{ text.data }}</p><p>{{ text.third }}</p></section>
    <section v-else class="card p-6"><p>{{ text.use }}</p></section>
    <section class="card p-6"><h2 class="text-xl font-semibold mb-2">{{ text.contact }}</h2><p>{{ text.contactText }}</p><a class="text-brand-700 underline" href="https://github.com/sw04121004/kundalik_yordamchimm/issues">GitHub Issues</a></section>
  </main>
</template>
