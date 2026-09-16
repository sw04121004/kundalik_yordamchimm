<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'

const expression = ref('')
const history = ref([])
const errorMsg = ref('')

function safeEvaluate(expr) {
  if (!expr || !expr.trim()) return null
  let cleaned = expr.trim()

  cleaned = cleaned.replace(/(\d+(\.\d+)?)\s*\+\s*(\d+(\.\d+)?)%/g, '($1 * (1 + $3/100))')
  cleaned = cleaned.replace(/(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)%/g, '($1 * (1 - $3/100))')
  cleaned = cleaned.replace(/(\d+(\.\d+)?)%/g, '($1 / 100)')
  cleaned = cleaned.replace(/\^/g, '**')
  cleaned = cleaned.replace(/sqrt\(([^)]+)\)/gi, 'Math.sqrt($1)')
  cleaned = cleaned.replace(/sin\(([^)]+)\)/gi, 'Math.sin($1 * Math.PI / 180)')
  cleaned = cleaned.replace(/cos\(([^)]+)\)/gi, 'Math.cos($1 * Math.PI / 180)')
  cleaned = cleaned.replace(/abs\(([^)]+)\)/gi, 'Math.abs($1)')
  cleaned = cleaned.replace(/log\(([^)]+)\)/gi, 'Math.log10($1)')

  if (/[^0-9\.\+\-\*\/\(\)\sMath\.\,sqrt|sin|cos|abs|log]/.test(cleaned.replace(/Math\.(sqrt|sin|cos|abs|log10|PI)/g, ''))) {
    throw new Error("Noto'g'ri belgi kiritildi")
  }

  const fn = new Function(`return ${cleaned}`)
  const res = fn()
  if (typeof res !== 'number' || isNaN(res) || !isFinite(res)) {
    throw new Error("Hisoblab bo'lmadi")
  }
  return Number(res.toFixed(6))
}

const result = computed(() => {
  errorMsg.value = ''
  if (!expression.value) return null
  try {
    return safeEvaluate(expression.value)
  } catch (err) {
    errorMsg.value = err.message || "Hisoblashda xatolik"
    return null
  }
})

function formatNum(num) {
  if (num === null || num === undefined) return ''
  return new Intl.NumberFormat('uz-UZ').format(num)
}

function calculate() {
  if (result.value !== null) {
    history.value.unshift({
      id: Date.now(),
      expr: expression.value,
      res: result.value
    })
    if (history.value.length > 10) history.value.pop()
  }
}

function applyPreset(presetExpr) {
  expression.value = presetExpr
}

function reuse(item) {
  expression.value = item.expr
}

function copyResult(res) {
  navigator.clipboard.writeText(res.toString())
}
</script>

<template>
  <ToolShell
    icon="🧠"
    title="Hisoblab ber (Aqlli Universal Hisoblagich)"
    description="Matnli, foizli va murakkab formulalarni bir zumda hisoblang"
    hint="Masalan: 150000 + 15% (QQS) yoki sqrt(144) + 5^2 kabi formulalarni yozing"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <!-- Input & Result Display -->
      <div>
        <label class="label">Matnli formula yoki misolni kiriting</label>
        <div class="relative">
          <input
            v-model="expression"
            type="text"
            autocomplete="off"
            class="input text-lg font-mono tracking-wide pr-12"
            placeholder="Masalan: (250000 * 3) + 12%"
            @keyup.enter="calculate"
          />
          <button
            v-if="expression"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
            @click="expression = ''"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- Quick Presets -->
      <div>
        <label class="label text-xs">Tezkor namunalar</label>
        <div class="flex flex-wrap gap-2">
          <button
            class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-brand-50 hover:text-brand-600 transition"
            @click="applyPreset('500000 + 12%')"
          >
            +12% QQS
          </button>
          <button
            class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-brand-50 hover:text-brand-600 transition"
            @click="applyPreset('1200000 - 20%')"
          >
            -20% Chegirma
          </button>
          <button
            class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-brand-50 hover:text-brand-600 transition"
            @click="applyPreset('sqrt(144) + 10^2')"
          >
            sqrt(144) + 10^2
          </button>
          <button
            class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-brand-50 hover:text-brand-600 transition"
            @click="applyPreset('sin(30) + cos(60)')"
          >
            Trigonometriya
          </button>
        </div>
      </div>

      <!-- Calculated Result Display -->
      <div v-if="result !== null" class="p-5 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-soft animate-resultPop">
        <div class="flex items-center justify-between">
          <span class="text-xs uppercase tracking-wider opacity-80">Natija</span>
          <button
            class="text-xs bg-white/20 hover:bg-white/30 px-2.5 py-1 rounded-lg transition"
            @click="copyResult(result)"
          >
            📋 Nusxalash
          </button>
        </div>
        <div class="text-3xl font-extrabold mt-1 font-mono">
          {{ formatNum(result) }}
        </div>
        <div class="text-xs opacity-80 mt-1">
          = {{ result }}
        </div>
      </div>

      <!-- Error message -->
      <div v-if="errorMsg" class="p-4 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm">
        ⚠️ {{ errorMsg }}
      </div>

      <!-- History -->
      <div v-if="history.length" class="pt-4 border-t border-slate-100 dark:border-slate-800">
        <h3 class="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">⏱️ So'nggi hisoblar</h3>
        <div class="space-y-2">
          <div
            v-for="item in history"
            :key="item.id"
            class="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
            @click="reuse(item)"
          >
            <span class="text-sm font-mono text-slate-600 dark:text-slate-400">{{ item.expr }}</span>
            <span class="text-sm font-bold text-brand-600 dark:text-brand-400 font-mono">= {{ formatNum(item.res) }}</span>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
