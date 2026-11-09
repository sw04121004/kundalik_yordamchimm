<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import FormAlert from '../components/FormAlert.vue'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()

const categories = [
  { id: 'salary', name: 'Maosh / Daromad', icon: '💰', type: 'income' },
  { id: 'food', name: 'Oziq-ovqat va bozor', icon: '🛒', type: 'expense' },
  { id: 'transport', name: 'Transport / Yonilg\'i', icon: '🚕', type: 'expense' },
  { id: 'bills', name: 'Kommunal / Aloqa', icon: '⚡', type: 'expense' },
  { id: 'fun', name: 'Hordiq va ko\'ngilochar', icon: '🎬', type: 'expense' },
  { id: 'other', name: 'Boshqa xarajatlar', icon: '📦', type: 'expense' },
]
const MAX_TRANSACTION_AMOUNT = 1_000_000_000_000
const AMOUNT_LIMIT_MESSAGE = 'Summa 1 trillion so‘mdan oshmasligi kerak.'

const transactions = ref([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')

const newTx = ref({
  type: 'expense',
  category: 'food',
  amount: '',
  note: ''
})

async function fetchTransactions() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/transactions/')
    transactions.value = data.map((transaction) => ({
      ...transaction,
      amount: Number(transaction.amount),
      note: transaction.description || (transaction.type === 'income' ? 'Kirim' : 'Chiqim'),
    }))
  } catch (requestError) {
    error.value = extractErrorMessage(requestError, 'Amallarni yuklab bo‘lmadi.')
  } finally {
    loading.value = false
  }
}

async function migrateLegacyTransactions() {
  if (!auth.user?.id) return
  const userId = String(auth.user.id)
  const sourceKey = `qulay_finance_txs_${userId}`
  const markerKey = `qulay_finance_migrated_v1_${userId}`
  if (localStorage.getItem(markerKey)) return

  const raw = localStorage.getItem(sourceKey)
  if (raw === null) {
    localStorage.setItem(markerKey, 'done')
    return
  }

  try {
    const legacy = JSON.parse(raw)
    if (!Array.isArray(legacy)) throw new Error('Eski moliya ma’lumotlari ro‘yxat shaklida emas.')
    const payload = legacy.map((item, index) => ({
      legacy_id: String(item.id ?? `index-${index}`),
      type: item.type,
      amount: item.amount,
      category: String(item.category ?? 'other'),
      description: String(item.note ?? item.description ?? '').slice(0, 255),
      date: item.date,
    }))
    for (let start = 0; start < payload.length; start += 500) {
      await api.post('/transactions/import-legacy/', { transactions: payload.slice(start, start + 500) })
    }
    // Keep the original browser records as a recovery copy; marker only prevents repeat work.
    localStorage.setItem(markerKey, 'done')
  } catch (migrationError) {
    error.value = `Eski moliya yozuvlarini ko‘chirish amalga oshmadi. Brauzer nusxasi saqlangan. ${extractErrorMessage(migrationError, '')}`.trim()
  }
}

onMounted(async () => {
  if (auth.access && !auth.user) await auth.fetchMe()
  await migrateLegacyTransactions()
  await fetchTransactions()
})

function localDateISO() {
  const date = new Date()
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  return date.toISOString().slice(0, 10)
}

function validateTransactionAmount() {
  if (Number(newTx.value.amount) > MAX_TRANSACTION_AMOUNT) {
    error.value = AMOUNT_LIMIT_MESSAGE
  } else if (error.value === AMOUNT_LIMIT_MESSAGE) {
    error.value = ''
  }
}

async function addTransaction() {
  const num = Number(newTx.value.amount)
  if (isNaN(num) || num <= 0) return
  if (num > MAX_TRANSACTION_AMOUNT) {
    error.value = AMOUNT_LIMIT_MESSAGE
    return
  }

  saving.value = true
  error.value = ''
  try {
    const description = newTx.value.note.trim()
    const { data } = await api.post('/transactions/', {
      type: newTx.value.type,
      category: newTx.value.category,
      amount: num,
      description,
      date: localDateISO(),
    })
    transactions.value.unshift({
      ...data,
      amount: Number(data.amount),
      note: data.description || (data.type === 'income' ? 'Kirim' : 'Chiqim'),
    })
    window.dispatchEvent(new Event('finance-transactions-updated'))
    newTx.value.amount = ''
    newTx.value.note = ''
  } catch (requestError) {
    error.value = extractErrorMessage(requestError, 'O‘tkazmani saqlab bo‘lmadi.')
  } finally {
    saving.value = false
  }
}

async function deleteTx(id) {
  error.value = ''
  try {
    await api.delete(`/transactions/${id}/`)
    transactions.value = transactions.value.filter((transaction) => transaction.id !== id)
    window.dispatchEvent(new Event('finance-transactions-updated'))
  } catch (requestError) {
    error.value = extractErrorMessage(requestError, 'O‘tkazmani o‘chirib bo‘lmadi.')
  }
}

const totalIncome = computed(() => {
  return transactions.value
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)
})

const totalExpense = computed(() => {
  return transactions.value
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)
})

const balance = computed(() => totalIncome.value - totalExpense.value)

function formatSum(val) {
  return new Intl.NumberFormat('uz-UZ').format(val) + " so'm"
}

function getCatMeta(catId) {
  return categories.find(c => c.id === catId) || { name: 'Boshqa', icon: '💸' }
}
</script>

<template>
  <ToolShell
    icon="💰"
    title="Mening pulim (Moliya Hisoblagich)"
    description="Daromad va xarajatlaringizni nazorat qiling hamda byudjetni rejalashtiring"
    hint="Kirim va chiqimlarni kiriting, umumiy balansingiz va xarajatlar tahlilini kuzatib boring"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <FormAlert :message="error" />

      <!-- Summary Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="finance-summary finance-summary-primary">
          <span class="text-xs uppercase tracking-wider text-slate-600 dark:text-slate-300">Balans</span>
          <div class="text-2xl font-bold mt-2 font-mono text-slate-900 dark:text-white">
            {{ formatSum(balance) }}
          </div>
        </div>
        <div class="finance-summary finance-summary-income">
          <span class="text-xs uppercase tracking-wider text-slate-600 dark:text-slate-300">Jami Kirim</span>
          <div class="text-2xl font-bold mt-2 font-mono text-slate-900 dark:text-white">
            +{{ formatSum(totalIncome) }}
          </div>
        </div>
        <div class="finance-summary finance-summary-expense">
          <span class="text-xs uppercase tracking-wider text-slate-600 dark:text-slate-300">Jami Chiqim</span>
          <div class="text-2xl font-bold mt-2 font-mono text-slate-900 dark:text-white">
            -{{ formatSum(totalExpense) }}
          </div>
        </div>
      </div>

      <!-- Add Transaction Form -->
      <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 space-y-4">
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <span>➕</span> Yangi o'tkazma qo'shish
        </h3>
        <form class="space-y-3" @submit.prevent="addTransaction">
          <div class="grid grid-cols-2 gap-3">
            <button
              type="button"
              class="py-2 rounded-xl text-sm font-semibold transition"
              :class="newTx.type === 'expense' ? 'bg-rose-500 text-white shadow-sm' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'"
              @click="newTx.type = 'expense'"
            >
              🔻 Chiqim (Xarajat)
            </button>
            <button
              type="button"
              class="py-2 rounded-xl text-sm font-semibold transition"
              :class="newTx.type === 'income' ? 'bg-emerald-500 text-white shadow-sm' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'"
              @click="newTx.type = 'income'"
            >
              🟢 Kirim (Daromad)
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="label text-xs">Summa (so'mda)</label>
              <input v-model="newTx.amount" type="number" min="0" max="1000000000000" step="1000" class="input font-mono" placeholder="100 000" required @input="validateTransactionAmount" />
            </div>
            <div>
              <label class="label text-xs">Kategoriya</label>
              <select v-model="newTx.category" class="input">
                <option v-for="c in categories" :key="c.id" :value="c.id">
                  {{ c.icon }} {{ c.name }}
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="label text-xs">Izoh (ixtiyoriy)</label>
            <input v-model="newTx.note" type="text" class="input" placeholder="Masalan: Tushlik va kofe" />
          </div>

          <button type="submit" class="btn-primary w-full !py-2.5" :disabled="saving">
            {{ saving ? 'Saqlanmoqda...' : '+ Saqlash' }}
          </button>
        </form>
      </div>

      <!-- Transactions History List -->
      <div>
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 mb-3">📋 Amallar tarixi</h3>
        <div v-if="loading" class="text-center text-slate-400 py-6 text-sm">
          Ma’lumotlar yuklanmoqda...
        </div>
        <div v-else-if="!transactions.length" class="text-center text-slate-400 py-6 text-sm">
          Hali hech qanday o'tkazma kiritilmadi.
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="t in transactions"
            :key="t.id"
            class="flex items-center justify-between p-3.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/50 shadow-sm"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-xl shrink-0">
                {{ getCatMeta(t.category).icon }}
              </div>
              <div>
                <p class="text-sm font-bold text-slate-800 dark:text-slate-100">{{ t.note }}</p>
                <p class="text-xs text-slate-400">{{ getCatMeta(t.category).name }} · {{ t.date }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span
                class="font-mono font-bold text-sm"
                :class="t.type === 'income' ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-800 dark:text-slate-100'"
              >
                {{ t.type === 'income' ? '+' : '-' }}{{ formatSum(t.amount) }}
              </span>
              <button
                class="text-slate-300 hover:text-rose-500 transition text-sm"
                title="O'chirish"
                @click="deleteTx(t.id)"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </ToolShell>
</template>
