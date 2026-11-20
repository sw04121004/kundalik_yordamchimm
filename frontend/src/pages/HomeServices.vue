<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import FormAlert from '../components/FormAlert.vue'
import { useAuthStore } from '../store/auth'
import { useAiStore } from '../store/ai'
import { useI18n, language } from '../i18n'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const aiStore = useAiStore()
const { t } = useI18n()

const STAINS_DICT = {
  uz: [
    { id: 'coffee', name: 'Qahva / Choy ☕', solution: "Iliq suvga ozgina idish yuvish vositasi va sirka (vinegar) solib, dog' ustiga surting. 10 minutdan so'ng yuving." },
    { id: 'grease', name: "Yog' / Ovqat 🍔", solution: "Dog' ustiga darhol kraxmal yoki soda seping (yog'ni shimib oladi). 15 daqiqadan so'ng sovunli issiq suvda yuving." },
    { id: 'ink', name: 'Siyoh / Ruchka 🖊️', solution: "Spirt (antiseptik) yoki lak tozalagich bilan paxtani ho'llab, dog'ni yengil arting." },
    { id: 'blood', name: 'Qon 🩸', solution: "FAQAT sovuq suvda yuving! Issiq suv qonni matoga yopishtirib qo'yadi. Vodorod peroksid ham yordam beradi." },
    { id: 'wine', name: 'Sharbat / Vino 🍷', solution: "Ustiga tuz seping. So'ng gazlangan mineral suv yoki mineral ichimlik bilan arting va yuving." }
  ],
  ru: [
    { id: 'coffee', name: 'Кофе / Чай ☕', solution: "Смешайте тёплую воду с небольшим количеством средства для посуды и уксуса, нанесите на пятно. Смойте через 10 минут." },
    { id: 'grease', name: "Жир / Еда 🍔", solution: "Сразу посыпьте пятно содой или крахмалом (они впитают жир). Через 15 минут постирайте в тёплой мыльной воде." },
    { id: 'ink', name: 'Чернила / Ручка 🖊️', solution: "Смочите ватный диск спиртом или средством для снятия лака и аккуратно протрите пятно." },
    { id: 'blood', name: 'Кровь 🩸', solution: "Стирайте ТОЛЬКО в холодной воде! Горячая вода закрепляет кровь в ткани. Также помогает перекись водорода." },
    { id: 'wine', name: 'Сок / Вино 🍷', solution: "Посыпьте солью, затем протрите газированной минеральной водой и промойте." }
  ],
  en: [
    { id: 'coffee', name: 'Coffee / Tea ☕', solution: "Apply warm water with a bit of dish soap and vinegar to the stain. Wash off after 10 minutes." },
    { id: 'grease', name: "Grease / Food 🍔", solution: "Immediately sprinkle baking soda or starch onto the stain. Wash with warm soapy water after 15 minutes." },
    { id: 'ink', name: 'Ink / Pen 🖊️', solution: "Dab the stain gently with a cotton pad soaked in rubbing alcohol or nail polish remover." },
    { id: 'blood', name: 'Blood 🩸', solution: "Wash ONLY with cold water! Hot water sets the blood into fabric permanently. Hydrogen peroxide also helps." },
    { id: 'wine', name: 'Juice / Wine 🍷', solution: "Sprinkle salt over the spill, then blot with sparkling water and rinse." }
  ]
}

const stains = computed(() => {
  const lang = ['uz', 'ru', 'en'].includes(language.value) ? language.value : 'uz'
  return STAINS_DICT[lang] || STAINS_DICT.uz
})

const selectedStain = ref('coffee')

async function askHomeAI() {
  if (!auth.isAuthenticated) {
    await router.push({ name: 'login', query: { next: route.fullPath } })
    return
  }

  aiStore.error = ''
  const res = await aiStore.startConversation('home')
  if (res.success && aiStore.current) {
    await aiStore.sendMessage(aiStore.current.id, t('home.prompt'))
    router.push({ name: 'ai-assistant' })
  }
}
</script>

<template>
  <ToolShell
    icon="🏠"
    :title="t('home.title')"
    :description="t('home.description')"
    :hint="t('home.hint')"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <FormAlert :message="aiStore.error" />

      <!-- Stain remover helper -->
      <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/50 shadow-sm space-y-4">
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <span>🧼</span> {{ t('home.stainsTitle') }}
        </h3>
        
        <div class="flex flex-wrap gap-2">
          <button
            v-for="s in stains"
            :key="s.id"
            class="px-3 py-2 rounded-xl text-xs sm:text-sm font-medium transition"
            :class="selectedStain === s.id ? 'bg-brand-500 text-white shadow-sm' : 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'"
            @click="selectedStain = s.id"
          >
            {{ s.name }}
          </button>
        </div>

        <div class="p-4 rounded-xl bg-brand-50 dark:bg-brand-900/20 text-brand-800 dark:text-brand-200 text-sm leading-relaxed border border-brand-100 dark:border-brand-900/30">
          💡 <b>{{ t('home.solution') }}</b> {{ stains.find(s => s.id === selectedStain)?.solution }}
        </div>
      </div>

      <!-- AI Home Assistant shortcut -->
      <div class="p-5 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-between gap-4 flex-wrap">
        <div>
          <h4 class="font-bold text-base">{{ t('home.haveQuestion') }}</h4>
          <p class="text-xs text-brand-100 mt-1">{{ t('home.questionDesc') }}</p>
        </div>
        <button class="btn-secondary text-sm shrink-0" @click="askHomeAI">
          {{ t('home.askAi') }}
        </button>
      </div>
    </div>
  </ToolShell>
</template>
