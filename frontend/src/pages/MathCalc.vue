<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'

const activeTab = ref('quad') // quad, pythagoras, geometry, linear

// Kvadrat tenglama state
const quadA = ref(1)
const quadB = ref(-5)
const quadC = ref(6)

const quadResult = computed(() => {
  const a = Number(quadA.value)
  const b = Number(quadB.value)
  const c = Number(quadC.value)

  if (isNaN(a) || isNaN(b) || isNaN(c) || a === 0) {
    return { valid: false, msg: "a koeffitsiyenti 0 bo'lmasligi kerak" }
  }

  const d = b * b - 4 * a * c
  if (d < 0) {
    return { valid: true, d, count: 0, msg: "Diskriminant D < 0. Haqiqiy ildizlar yo'q." }
  } else if (d === 0) {
    const x = -b / (2 * a)
    return { valid: true, d, count: 1, x1: x, x2: x, msg: `D = 0. Bitta ildiz: x = ${x}` }
  } else {
    const x1 = (-b + Math.sqrt(d)) / (2 * a)
    const x2 = (-b - Math.sqrt(d)) / (2 * a)
    return { valid: true, d, count: 2, x1, x2, msg: `D = ${d}. Ildizlar: x₁ = ${x1}, x₂ = ${x2}` }
  }
})

// Pifagor state
const pythA = ref(3)
const pythB = ref(4)
const pythC = ref(0)
const pythMode = ref('c') // 'c' (gipotenuza), 'a' (katet), 'b' (katet)

const pythResult = computed(() => {
  const a = Number(pythA.value)
  const b = Number(pythB.value)
  const c = Number(pythC.value)

  if (pythMode.value === 'c') {
    if (a <= 0 || b <= 0) return null
    return Math.sqrt(a * a + b * b)
  } else if (pythMode.value === 'a') {
    if (c <= 0 || b <= 0 || c <= b) return null
    return Math.sqrt(c * c - b * b)
  } else {
    if (c <= 0 || a <= 0 || c <= a) return null
    return Math.sqrt(c * c - a * a)
  }
})

// Geometriya state
const geomShape = ref('circle') // circle, triangle, sphere
const circleR = ref(5)
const triBase = ref(6)
const triHeight = ref(4)
const sphereR = ref(3)

const geomResult = computed(() => {
  if (geomShape.value === 'circle') {
    const r = Number(circleR.value)
    if (r <= 0) return null
    return {
      area: (Math.PI * r * r).toFixed(2),
      len: (2 * Math.PI * r).toFixed(2)
    }
  } else if (geomShape.value === 'triangle') {
    const b = Number(triBase.value)
    const h = Number(triHeight.value)
    if (b <= 0 || h <= 0) return null
    return { area: (0.5 * b * h).toFixed(2) }
  } else if (geomShape.value === 'sphere') {
    const r = Number(sphereR.value)
    if (r <= 0) return null
    return {
      volume: ((4 / 3) * Math.PI * Math.pow(r, 3)).toFixed(2),
      area: (4 * Math.PI * r * r).toFixed(2)
    }
  }
  return null
})

// Chiziqli tenglama state (ax + b = c)
const linA = ref(2)
const linB = ref(4)
const linC = ref(10)

const linResult = computed(() => {
  const a = Number(linA.value)
  const b = Number(linB.value)
  const c = Number(linC.value)
  if (a === 0) return null
  return (c - b) / a
})
</script>

<template>
  <ToolShell
    icon="📏"
    title="7-11 Sinf Kalkulyatori"
    description="Algebra, Geometriya va Fizika formulalarini tezkor yechish"
    hint="Kvadrat tenglama, Pifagor teoremasi yoki geometrik shakllar yuzasini hisoblang"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <!-- Tabs -->
      <div class="flex border-b border-slate-200 dark:border-slate-800 gap-2 pb-2 overflow-x-auto">
        <button
          class="px-4 py-2 rounded-xl text-sm font-semibold transition"
          :class="activeTab === 'quad' ? 'bg-brand-500 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'"
          @click="activeTab = 'quad'"
        >
          Kvadrat tenglama
        </button>
        <button
          class="px-4 py-2 rounded-xl text-sm font-semibold transition"
          :class="activeTab === 'pythagoras' ? 'bg-brand-500 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'"
          @click="activeTab = 'pythagoras'"
        >
          Pifagor teoremasi
        </button>
        <button
          class="px-4 py-2 rounded-xl text-sm font-semibold transition"
          :class="activeTab === 'geometry' ? 'bg-brand-500 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'"
          @click="activeTab = 'geometry'"
        >
          Geometriya
        </button>
        <button
          class="px-4 py-2 rounded-xl text-sm font-semibold transition"
          :class="activeTab === 'linear' ? 'bg-brand-500 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'"
          @click="activeTab = 'linear'"
        >
          Chiziqli tenglama
        </button>
      </div>

      <!-- 1. Kvadrat Tenglama -->
      <div v-if="activeTab === 'quad'" class="space-y-4">
        <p class="text-sm text-slate-500 dark:text-slate-400 font-mono">Formulasi: ax² + bx + c = 0</p>
        <div class="grid grid-cols-3 gap-3">
          <div>
            <label class="label text-xs">a koeffitsiyent</label>
            <input v-model="quadA" type="number" class="input font-mono" />
          </div>
          <div>
            <label class="label text-xs">b koeffitsiyent</label>
            <input v-model="quadB" type="number" class="input font-mono" />
          </div>
          <div>
            <label class="label text-xs">c koeffitsiyent</label>
            <input v-model="quadC" type="number" class="input font-mono" />
          </div>
        </div>

        <div v-if="quadResult.valid" class="p-5 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white space-y-2">
          <div class="text-xs uppercase opacity-80">Bosqichma-bosqich yechim</div>
          <div class="text-lg font-mono font-bold">D = b² - 4ac = {{ quadResult.d }}</div>
          <div class="text-base">{{ quadResult.msg }}</div>
          <div v-if="quadResult.count > 0" class="pt-2 border-t border-white/20 font-mono text-sm">
            <span v-if="quadResult.count === 2">
              x₁ = ({{ -quadB }} + √{{ quadResult.d }}) / {{ 2 * quadA }} = <b>{{ quadResult.x1.toFixed(3) }}</b><br />
              x₂ = ({{ -quadB }} - √{{ quadResult.d }}) / {{ 2 * quadA }} = <b>{{ quadResult.x2.toFixed(3) }}</b>
            </span>
            <span v-else>
              x = {{ quadResult.x1 }}
            </span>
          </div>
        </div>
      </div>

      <!-- 2. Pifagor Teoremasi -->
      <div v-if="activeTab === 'pythagoras'" class="space-y-4">
        <p class="text-sm text-slate-500 dark:text-slate-400 font-mono">Formulasi: a² + b² = c²</p>
        <div class="flex gap-3">
          <label class="inline-flex items-center gap-1.5 text-sm cursor-pointer">
            <input v-model="pythMode" type="radio" value="c" /> Gipotenuza (c) ni topish
          </label>
          <label class="inline-flex items-center gap-1.5 text-sm cursor-pointer">
            <input v-model="pythMode" type="radio" value="a" /> Katet (a) ni topish
          </label>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div v-if="pythMode !== 'a'">
            <label class="label text-xs">a (katet)</label>
            <input v-model="pythA" type="number" min="0" class="input" />
          </div>
          <div v-if="pythMode !== 'b'">
            <label class="label text-xs">b (katet)</label>
            <input v-model="pythB" type="number" min="0" class="input" />
          </div>
          <div v-if="pythMode !== 'c'">
            <label class="label text-xs">c (gipotenuza)</label>
            <input v-model="pythC" type="number" min="0" class="input" />
          </div>
        </div>

        <div v-if="pythResult !== null" class="p-5 rounded-2xl bg-brand-500 text-white">
          <span class="text-xs opacity-80 uppercase">Natija</span>
          <div class="text-2xl font-extrabold font-mono mt-1">
            {{ pythMode.toUpperCase() }} = {{ pythResult.toFixed(3) }}
          </div>
        </div>
      </div>

      <!-- 3. Geometriya -->
      <div v-if="activeTab === 'geometry'" class="space-y-4">
        <div class="flex gap-2">
          <button
            class="px-3 py-1.5 rounded-lg text-xs font-semibold"
            :class="geomShape === 'circle' ? 'bg-brand-500 text-white' : 'bg-slate-100 dark:bg-slate-800'"
            @click="geomShape = 'circle'"
          >
            Doira / Aylana
          </button>
          <button
            class="px-3 py-1.5 rounded-lg text-xs font-semibold"
            :class="geomShape === 'triangle' ? 'bg-brand-500 text-white' : 'bg-slate-100 dark:bg-slate-800'"
            @click="geomShape = 'triangle'"
          >
            Uchburchak
          </button>
          <button
            class="px-3 py-1.5 rounded-lg text-xs font-semibold"
            :class="geomShape === 'sphere' ? 'bg-brand-500 text-white' : 'bg-slate-100 dark:bg-slate-800'"
            @click="geomShape = 'sphere'"
          >
            Shar (Sfera)
          </button>
        </div>

        <div v-if="geomShape === 'circle'" class="space-y-3">
          <label class="label">Radius (r)</label>
          <input v-model="circleR" type="number" min="0" class="input" />
        </div>

        <div v-if="geomShape === 'triangle'" class="grid grid-cols-2 gap-3">
          <div>
            <label class="label">Asosi (a)</label>
            <input v-model="triBase" type="number" min="0" class="input" />
          </div>
          <div>
            <label class="label">Balandlik (h)</label>
            <input v-model="triHeight" type="number" min="0" class="input" />
          </div>
        </div>

        <div v-if="geomShape === 'sphere'" class="space-y-3">
          <label class="label">Radius (r)</label>
          <input v-model="sphereR" type="number" min="0" class="input" />
        </div>

        <div v-if="geomResult" class="p-5 rounded-2xl bg-brand-500 text-white space-y-1">
          <div v-if="geomResult.area">Yuzi (S): <b>{{ geomResult.area }}</b></div>
          <div v-if="geomResult.len">Uzunligi (L): <b>{{ geomResult.len }}</b></div>
          <div v-if="geomResult.volume">Hajmi (V): <b>{{ geomResult.volume }}</b></div>
        </div>
      </div>

      <!-- 4. Chiziqli tenglama -->
      <div v-if="activeTab === 'linear'" class="space-y-4">
        <p class="text-sm text-slate-500 dark:text-slate-400 font-mono">Formulasi: ax + b = c</p>
        <div class="grid grid-cols-3 gap-3">
          <div>
            <label class="label text-xs">a</label>
            <input v-model="linA" type="number" class="input font-mono" />
          </div>
          <div>
            <label class="label text-xs">b</label>
            <input v-model="linB" type="number" class="input font-mono" />
          </div>
          <div>
            <label class="label text-xs">c</label>
            <input v-model="linC" type="number" class="input font-mono" />
          </div>
        </div>

        <div v-if="linResult !== null" class="p-5 rounded-2xl bg-brand-500 text-white">
          <span class="text-xs opacity-80 uppercase">Natija</span>
          <div class="text-2xl font-extrabold font-mono mt-1">x = {{ linResult }}</div>
          <div class="text-xs opacity-80 mt-1">Tekshirish: {{ linA }} * ({{ linResult }}) + {{ linB }} = {{ linC }}</div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
