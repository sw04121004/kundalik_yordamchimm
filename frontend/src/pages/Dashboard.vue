<script setup>
import { computed, onMounted, ref } from 'vue'
import { useServicesStore } from '../store/services'
import { useAiStore, purposeMeta } from '../store/ai'
import { useAuthStore } from '../store/auth'
import { usePlannerStore } from '../store/planner'
import AppHeader from '../components/AppHeader.vue'
import ServiceCard from '../components/ServiceCard.vue'

const servicesStore = useServicesStore()
const aiStore = useAiStore()
const auth = useAuthStore()
const planner = usePlannerStore()
const search = ref('')

onMounted(() => {
  servicesStore.fetchCategories()
  servicesStore.fetchFavorites()
  aiStore.fetchConversations()
  planner.fetchToday()
})

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 6)  return { icon: '🌙', text: 'Xayrli tun' }
  if (h < 12) return { icon: '☀️', text: 'Xayrli tong' }
  if (h < 18) return { icon: '🌤️', text: 'Xayrli kun' }
  return { icon: '🌇', text: 'Xayrli kech' }
})

const AI_ONLY_SLUGS = new Set(['oshxona-ai', 'uy-ai', 'oqish-ai', 'hujjat-ai'])

const filteredCategories = computed(() => {
  const q = search.value.trim().toLowerCase()
  return servicesStore.categories
    .map(cat => ({
      ...cat,
      services: cat.services.filter(s =>
        !AI_ONLY_SLUGS.has(s.slug) && (!q || s.name.toLowerCase().includes(q))
      ),
    }))
    .filter(cat => cat.services.length > 0)
})

const hasResults = computed(() => filteredCategories.value.some(c => c.services.length > 0))
const isSearching = computed(() => search.value.trim().length > 0)

const favoriteServices = computed(() => servicesStore.favorites.map(f => f.service))
const recentConversations = computed(() => aiStore.conversations.slice(0, 3))
</script>

<template>
  <div class="relative min-h-screen bg-[#f8f9fc] dark:bg-[#0c0f17] text-slate-800 dark:text-slate-100 transition-colors duration-500 overflow-x-hidden">
    
    <!-- Floating Background Glow Orbs Powered 100% by Selected Theme -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <!-- Chap tomondagi asosiy tanlangan rang nuri (Left Theme Aura) -->
      <div class="glow-orb w-[40rem] h-[55rem] top-10 -left-48 bg-brand-500/25 dark:bg-brand-500/20 blur-[120px] rounded-full animate-floatSlow transition-colors duration-700 pointer-events-none"></div>
      <div class="glow-orb w-[30rem] h-[35rem] top-1/2 -left-28 bg-brand-400/20 dark:bg-brand-600/15 blur-[100px] rounded-full animate-pulseGlow transition-colors duration-700 pointer-events-none" style="animation-delay: -2s"></div>

      <!-- O'ng tomondagi qo'shimcha mayin nurlar -->
      <div class="glow-orb w-[32rem] h-[32rem] -top-24 -right-24 bg-brand-500/20 dark:bg-brand-500/15 blur-[110px] animate-floatSlow transition-colors duration-700"></div>
      <div class="glow-orb w-[28rem] h-[28rem] bottom-10 right-1/4 bg-brand-400/15 dark:bg-brand-400/10 blur-[100px] animate-floatSlow transition-colors duration-700" style="animation-delay: -4s"></div>
    </div>

    <div class="relative z-10">
      <AppHeader />

      <main class="max-w-5xl mx-auto px-4 sm:px-6 py-8">

        <!-- Greeting + Search (Centered, Dynamic to Selected Theme) -->
        <section class="mb-12 animate-fadeUp text-center flex flex-col items-center">
          <div class="inline-flex items-center justify-center gap-3 mb-2 px-6 py-2.5 rounded-2xl bg-white/80 dark:bg-[#161b26]/80 backdrop-blur-xl border border-brand-300/40 dark:border-brand-500/30 shadow-lg shadow-brand-500/10 hover:scale-105 transition-all duration-300">
            <span class="text-3xl animate-bounceSoft">{{ greeting.icon }}</span>
            <h1 class="text-2xl sm:text-3xl font-black text-slate-800 dark:text-slate-100 tracking-tight">
              {{ greeting.text }}<span v-if="auth.user?.first_name || auth.user?.username">, {{ auth.user.first_name || auth.user.username }}</span>!
            </h1>
          </div>
          <p class="text-slate-500 dark:text-slate-400 text-sm sm:text-base mb-6 font-medium">Sizga bugun nimada yordam beramiz?</p>

          <!-- Search Bar with glowing aura from Selected Theme -->
          <div class="relative w-full max-w-xl mx-auto group">
            <div class="absolute -inset-1 rounded-2xl bg-gradient-to-r from-brand-500/30 via-brand-400/30 to-brand-600/30 opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 transition-opacity duration-500 blur-lg pointer-events-none"></div>
            <div class="relative">
              <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none group-hover:text-brand-500 group-hover:scale-110 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              <input
                v-model="search"
                type="text"
                class="input !pl-11 !py-3.5 !rounded-2xl shadow-sm text-sm bg-white/90 dark:bg-[#161b26]/90 backdrop-blur-xl border-slate-200/80 dark:border-slate-700/80 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-400 transition-all duration-300"
                placeholder="Masalan: foiz hisoblash, rasm o'lchamini o'zgartirish, maosh..."
              />
              <button v-if="search" @click="search=''" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 focus:outline-none transition-transform hover:scale-125">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
          </div>
        </section>

        <!-- Mening kunim (My Day widgets) reacting to Selected Theme -->
        <section v-if="!isSearching" class="mb-10 animate-fadeUp">
          <h2 class="text-sm font-extrabold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-3.5 flex items-center gap-2">
            <span class="text-lg animate-wiggle">☀️</span> Mening kunim
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            <!-- Planner Widget -->
            <router-link :to="{ name: 'planner' }" class="card p-5 hover:-translate-y-1.5 hover:shadow-xl hover:shadow-brand-500/15 hover:border-brand-400/50 transition-all duration-300 group relative overflow-hidden bg-white/95 dark:bg-[#161b26]/95 backdrop-blur-xl border border-slate-200/80 dark:border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-2.5">
                  <div class="w-10 h-10 rounded-xl bg-brand-50 dark:bg-brand-950/40 border border-brand-200/50 dark:border-brand-500/30 flex items-center justify-center text-xl group-hover:scale-115 group-hover:rotate-6 transition-all duration-300">📅</div>
                  <div>
                    <p class="text-sm font-bold text-slate-800 dark:text-slate-100 group-hover:text-brand-500 dark:group-hover:text-brand-300 transition-colors">Bugungi rejangiz</p>
                    <p class="text-xs text-slate-500 dark:text-slate-400">Kunlik vazifalar</p>
                  </div>
                </div>
                <span v-if="planner.todayTotal > 0" class="text-xs font-extrabold px-2.5 py-1 rounded-full bg-brand-100 text-brand-800 dark:bg-brand-950/60 dark:text-brand-300 border border-brand-200/60 dark:border-brand-500/30">
                  {{ planner.todayDone }}/{{ planner.todayTotal }} bajarildi
                </span>
              </div>

              <template v-if="planner.todayTotal > 0">
                <div class="h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden mb-3 p-0.5">
                  <div
                    class="h-full rounded-full transition-all duration-700 shadow-sm"
                    style="background: linear-gradient(90deg, rgb(var(--brand-400)), rgb(var(--brand-600)))"
                    :style="{ width: Math.max(planner.todayPercent, 5) + '%' }"
                  ></div>
                </div>
                <ul class="space-y-1.5">
                  <li v-for="task in planner.todayTasks.slice(0,3)" :key="task.id" class="flex items-center gap-2 text-sm">
                    <span :class="task.is_done ? 'text-green-500 scale-110' : 'text-slate-300 dark:text-slate-600'" class="transition-transform">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    </span>
                    <span :class="task.is_done ? 'text-slate-400 line-through' : 'text-slate-700 dark:text-slate-300'" class="truncate font-medium">{{ task.title }}</span>
                    <span v-if="task.due_time" class="ml-auto text-xs text-slate-400 shrink-0 font-mono">{{ task.due_time.slice(0,5) }}</span>
                  </li>
                </ul>
              </template>
              <p v-else class="text-sm text-slate-400 dark:text-slate-500 py-1">Bugunga reja yo'q. Yangi vazifa qo'shish uchun bosing →</p>
            </router-link>

            <!-- Finance Widget -->
            <router-link :to="{ name: 'finance' }" class="card p-5 hover:-translate-y-1.5 hover:shadow-xl hover:shadow-brand-500/15 hover:border-brand-400/50 transition-all duration-300 group relative overflow-hidden bg-white/95 dark:bg-[#161b26]/95 backdrop-blur-xl border border-slate-200/80 dark:border-slate-800">
              <div class="absolute -right-6 -bottom-6 w-32 h-32 bg-brand-500/10 dark:bg-brand-500/15 rounded-full blur-2xl group-hover:scale-125 transition-transform duration-500"></div>
              <div class="flex items-center justify-between mb-4 relative z-10">
                <div class="flex items-center gap-2.5">
                  <div class="w-10 h-10 rounded-xl bg-brand-50 dark:bg-brand-950/40 border border-brand-200/50 dark:border-brand-500/30 flex items-center justify-center text-xl group-hover:scale-115 group-hover:rotate-6 transition-all duration-300">💰</div>
                  <div>
                    <p class="text-sm font-bold text-slate-800 dark:text-slate-100 group-hover:text-brand-500 dark:group-hover:text-brand-300 transition-colors">Mening pulim</p>
                    <p class="text-xs text-slate-500 dark:text-slate-400">Moliya va byudjet</p>
                  </div>
                </div>
                <span class="text-[11px] font-extrabold px-2.5 py-0.5 bg-brand-100 text-brand-700 dark:bg-brand-950/60 dark:text-brand-300 border border-brand-300/40 rounded-full animate-pulse">Yangi xizmat</span>
              </div>
              <p class="text-3xl font-black text-slate-900 dark:text-white relative z-10 tracking-tight">0 <span class="text-base font-normal text-slate-400">so'm</span></p>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 relative z-10 group-hover:text-brand-500 dark:group-hover:text-brand-400 transition-colors">Bugungi xarajatlar. Byudjetni rejalashtirish uchun kiring →</p>
            </router-link>
          </div>
        </section>

        <!-- AI Assistant Banner (100% Dynamic to Selected Theme) -->
        <router-link
          v-if="!isSearching"
          :to="{ name: 'ai-assistant' }"
          class="block rounded-2xl p-6 mb-12 shadow-xl shadow-brand-500/20 hover:-translate-y-1.5 hover:shadow-2xl hover:shadow-brand-500/35 transition-all duration-300 animate-fadeUp group relative overflow-hidden border border-brand-300/40 dark:border-brand-500/30"
          style="background: linear-gradient(135deg, rgb(var(--brand-500)) 0%, rgb(var(--brand-600)) 45%, rgb(var(--brand-800)) 100%)"
        >
          <!-- Shimmer light sweep -->
          <div class="absolute inset-0 w-1/2 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmerSweep pointer-events-none"></div>

          <div class="relative flex items-center justify-between gap-5 z-10">
            <div class="flex items-center gap-4 sm:gap-5 min-w-0">
              <div class="w-14 h-14 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-3xl shrink-0 group-hover:scale-115 group-hover:rotate-6 transition-all duration-300 shadow-md">
                <span class="animate-bounceSoft">🤖</span>
              </div>
              <div class="min-w-0">
                <h2 class="text-white font-black text-lg sm:text-xl leading-tight">AI Yordamchi</h2>
                <p class="text-white/90 text-xs sm:text-sm mt-1 line-clamp-1 font-medium">Dasturlash, ta'lim, matn, tarjima, CV va g'oyalar bo'yicha — istagan tilda, tabiiy yozing.</p>
              </div>
            </div>
            
            <div class="shrink-0 flex items-center gap-2 bg-slate-900/90 text-white font-extrabold text-xs sm:text-sm px-4 sm:px-5 py-2.5 rounded-xl group-hover:bg-slate-950 group-hover:scale-105 transition-all shadow-lg">
              <span>Suhbatni boshlash</span>
              <span class="group-hover:translate-x-1.5 transition-transform duration-300">→</span>
            </div>
          </div>
        </router-link>

        <!-- Favorites (If Any) -->
        <section v-if="!isSearching && favoriteServices.length" class="mb-12 animate-fadeUp">
          <h2 class="text-sm font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
            <span class="text-amber-400 animate-wiggle">⭐</span> Sevimlilar
          </h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 stagger-children">
            <ServiceCard v-for="svc in favoriteServices" :key="svc.id" v-bind="svc" />
          </div>
        </section>

        <!-- Recent AI Conversations -->
        <section v-if="!isSearching && recentConversations.length" class="mb-12 animate-fadeUp">
          <h2 class="text-sm font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
            <span class="text-lg">💬</span> So'nggi suhbatlar
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 stagger-children">
            <router-link
              v-for="conv in recentConversations"
              :key="conv.id"
              :to="{ name: 'ai-assistant' }"
              class="card p-4 hover:-translate-y-1 hover:shadow-lg hover:border-brand-400/50 transition-all duration-300 group bg-white/90 dark:bg-[#161b26]/90 backdrop-blur-xl border border-slate-200/80 dark:border-slate-800"
            >
              <span class="text-2xl block mb-2 group-hover:scale-115 group-hover:rotate-6 transition-transform duration-300">{{ purposeMeta(conv.purpose).icon }}</span>
              <p class="font-bold text-slate-800 dark:text-slate-100 text-sm truncate group-hover:text-brand-500 dark:group-hover:text-brand-300 transition-colors">{{ conv.title }}</p>
              <p v-if="conv.last_message" class="text-xs text-slate-400 mt-1 truncate">{{ conv.last_message }}</p>
            </router-link>
          </div>
        </section>

        <!-- Search empty state -->
        <div v-if="isSearching && !hasResults" class="text-center py-20 animate-fadeUp">
          <div class="text-5xl mb-3 animate-bounceSoft">🔍</div>
          <p class="font-bold text-slate-700 dark:text-slate-300 text-lg">Hech qanday xizmat topilmadi</p>
          <p class="text-sm text-slate-400 mt-1">Boshqa so'z bilan qidirib ko'ring</p>
        </div>

        <!-- All Services by Category (With dynamic selected theme lighting & rich animations) -->
        <div v-if="servicesStore.loading" class="text-center py-12 text-slate-400">
          <div class="inline-block w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mb-3"></div>
          <p class="text-sm font-medium">Xizmatlar yuklanmoqda...</p>
        </div>
        
        <div v-else class="space-y-12">
          <section v-for="cat in filteredCategories" :key="cat.id" class="animate-fadeUp">
            <h2 class="text-sm font-extrabold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2.5 group">
              <span class="text-xl group-hover:scale-125 group-hover:rotate-12 transition-transform duration-300 inline-block">{{ cat.icon }}</span>
              <span class="group-hover:text-brand-500 dark:group-hover:text-brand-300 transition-colors duration-300">{{ cat.name }}</span>
            </h2>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 stagger-children">
              <ServiceCard v-for="svc in cat.services" :key="svc.id" v-bind="svc" />
            </div>
          </section>
        </div>

      </main>
    </div>
  </div>
</template>
