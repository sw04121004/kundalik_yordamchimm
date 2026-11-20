<script setup>
import { ref, computed } from 'vue'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import { useToolText } from '../utils/toolText'
import { useI18n } from '../i18n'

const { t } = useI18n()

const tx = useToolText({
  uz: {
    title: "Hisoblab ber (Aqlli Universal Hisoblagich)",
    desc: "Matnli, foizli va murakkab formulalarni bir zumda hisoblang",
    hint: "Masalan: 150000 + 15% (QQS) yoki sqrt(144) + 5^2 kabi formulalarni yozing",
    inputLabel: "Matnli formula yoki misolni kiriting",
    placeholder: "Masalan: (250000 * 3) + 12%",
    presetsLabel: "Tezkor namunalar",
    presetVat: "+12% QQS",
    presetDiscount: "-20% Chegirma",
    presetTrig: "Trigonometriya",
    result: "Natija",
    copy: "📋 Nusxalash",
    copied: "✓ Nusxalandi",
    recent: "⏱️ So'nggi hisoblar",
    errParenExtra: "Noto'g'ri joylashgan qavs: ')' ortiqcha",
    errParenBalance: "Qavslar muvozanati buzilgan: '(' yoki ')' yetishmayapti",
    errInvalidChar: "Noto'g'ri belgi kiritildi",
    errCannotCalc: "Hisoblab bo'lmadi",
    errSyntax: "Hisoblashda sintaktik xatolik",
  },
  ru: {
    title: "Умный калькулятор (Универсальный)",
    desc: "Мгновенный расчёт текстовых, процентных и сложных формул",
    hint: "Например: 150000 + 15% (НДС) или sqrt(144) + 5^2",
    inputLabel: "Введите текстовую формулу или выражение",
    placeholder: "Например: (250000 * 3) + 12%",
    presetsLabel: "Быстрые примеры",
    presetVat: "+12% НДС",
    presetDiscount: "-20% Скидка",
    presetTrig: "Тригонометрия",
    result: "Результат",
    copy: "📋 Копировать",
    copied: "✓ Скопировано",
    recent: "⏱️ Недавние вычисления",
    errParenExtra: "Лишняя скобка ')'",
    errParenBalance: "Нарушен баланс скобок: отсутствует '(' или ')'",
    errInvalidChar: "Введен недопустимый символ",
    errCannotCalc: "Не удалось вычислить",
    errSyntax: "Синтаксическая ошибка в выражении",
  },
  en: {
    title: "Smart Calculator (Universal)",
    desc: "Calculate text, percentage, and complex formulas instantly",
    hint: "For example: 150000 + 15% (VAT) or sqrt(144) + 5^2",
    inputLabel: "Enter text formula or expression",
    placeholder: "For example: (250000 * 3) + 12%",
    presetsLabel: "Quick examples",
    presetVat: "+12% VAT",
    presetDiscount: "-20% Discount",
    presetTrig: "Trigonometry",
    result: "Result",
    copy: "📋 Copy",
    copied: "✓ Copied",
    recent: "⏱️ Recent calculations",
    errParenExtra: "Extra parenthesis ')'",
    errParenBalance: "Mismatched parentheses: missing '(' or ')'",
    errInvalidChar: "Invalid character entered",
    errCannotCalc: "Could not calculate",
    errSyntax: "Syntax error in expression",
  },
})

const expression = ref('')
const history = ref([])
const errorMsg = ref('')
const copied = ref(false)

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

  // Qavslar muvozanatini tekshirish
  let balance = 0;
  for (let i = 0; i < cleaned.length; i++) {
    if (cleaned[i] === '(') balance++;
    else if (cleaned[i] === ')') balance--;
    if (balance < 0) {
      throw new Error(tx.value.errParenExtra)
    }
  }
  if (balance !== 0) {
    throw new Error(tx.value.errParenBalance)
  }

  if (/[^0-9\.\+\-\*\/\(\)\sMath\.\,sqrt|sin|cos|abs|log]/.test(cleaned.replace(/Math\.(sqrt|sin|cos|abs|log10|PI)/g, ''))) {
    throw new Error(tx.value.errInvalidChar)
  }

  try {
    const fn = new Function(`return ${cleaned}`)
    const res = fn()
    if (typeof res !== 'number' || isNaN(res) || !isFinite(res)) {
      throw new Error(tx.value.errCannotCalc)
    }
    return Number(res.toFixed(6))
  } catch (e) {
    throw new Error(tx.value.errSyntax + ": " + e.message)
  }
}

const result = computed(() => {
  errorMsg.value = ''
  if (!expression.value) return null
  try {
    return safeEvaluate(expression.value)
  } catch (err) {
    errorMsg.value = err.message || tx.value.errCannotCalc
    return null
  }
})

function formatNum(num) {
  if (num === null || num === undefined) return ''
  return new Intl.NumberFormat().format(num)
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
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>

<template>
  <ToolShell
    icon="🧠"
    :title="tx.title"
    :description="tx.desc"
    :hint="tx.hint"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <!-- Input & Result Display -->
      <div>
        <label class="label">{{ tx.inputLabel }}</label>
        <div class="relative">
          <input
            v-model="expression"
            type="text"
            autocomplete="off"
            class="input text-lg font-mono tracking-wide pr-12"
            :placeholder="tx.placeholder"
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
        <label class="label text-xs">{{ tx.presetsLabel }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-brand-50 hover:text-brand-600 transition"
            @click="applyPreset('500000 + 12%')"
          >
            {{ tx.presetVat }}
          </button>
          <button
            class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-brand-50 hover:text-brand-600 transition"
            @click="applyPreset('1200000 - 20%')"
          >
            {{ tx.presetDiscount }}
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
            {{ tx.presetTrig }}
          </button>
        </div>
      </div>

      <!-- Calculated Result Display -->
      <div v-if="result !== null" class="p-5 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-soft animate-resultPop">
        <div class="flex items-center justify-between">
          <span class="text-xs uppercase tracking-wider opacity-80">{{ tx.result }}</span>
          <button
            class="text-xs bg-white/20 hover:bg-white/30 px-2.5 py-1 rounded-lg transition"
            @click="copyResult(result)"
          >
            {{ copied ? tx.copied : tx.copy }}
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
        <h3 class="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">{{ tx.recent }}</h3>
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
