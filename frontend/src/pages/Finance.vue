<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'
import FormAlert from '../components/FormAlert.vue'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'
import { useAuthStore } from '../store/auth'
import { useI18n } from '../i18n'

const auth = useAuthStore()
const { t, locale } = useI18n()

const categories = computed(() => [
  { id: 'salary', name: t('finance.cat.salary'), icon: '💰', type: 'income' },
  { id: 'food', name: t('finance.cat.food'), icon: '🛒', type: 'expense' },
  { id: 'transport', name: t('finance.cat.transport'), icon: '🚕', type: 'expense' },
  { id: 'bills', name: t('finance.cat.bills'), icon: '⚡', type: 'expense' },
  { id: 'fun', name: t('finance.cat.fun'), icon: '🎬', type: 'expense' },
  { id: 'other', name: t('finance.cat.other'), icon: '📦', type: 'expense' },
])

const MAX_TRANSACTION_AMOUNT = 1_000_000_000_000

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
      note: transaction.description || (transaction.type === 'income' ? t('finance.typeIncome') : t('finance.typeExpense')),
    }))
  } catch (requestError) {
    error.value = extractErrorMessage(requestError, t('finance.loadError'))
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
    localStorage.setItem(markerKey, 'done')
  } catch (migrationError) {
    error.value = `${extractErrorMessage(migrationError, t('finance.loadError'))}`.trim()
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
    error.value = t('finance.amountLimit')
  } else if (error.value === t('finance.amountLimit')) {
    error.value = ''
  }
}

async function addTransaction() {
  const num = Number(newTx.value.amount)
  if (isNaN(num) || num <= 0) return
  if (num > MAX_TRANSACTION_AMOUNT) {
    error.value = t('finance.amountLimit')
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
      note: data.description || (data.type === 'income' ? t('finance.typeIncome') : t('finance.typeExpense')),
    })
    window.dispatchEvent(new Event('finance-transactions-updated'))
    newTx.value.amount = ''
    newTx.value.note = ''
  } catch (requestError) {
    error.value = extractErrorMessage(requestError, t('finance.saveError'))
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
    error.value = extractErrorMessage(requestError, t('finance.deleteError'))
  }
}

const totalIncome = computed(() => {
  return transactions.value
    .filter(item => item.type === 'income')
    .reduce((sum, item) => sum + item.amount, 0)
})

const totalExpense = computed(() => {
  return transactions.value
    .filter(item => item.type === 'expense')
    .reduce((sum, item) => sum + item.amount, 0)
})

const balance = computed(() => totalIncome.value - totalExpense.value)

function formatSum(val) {
  return new Intl.NumberFormat(locale()).format(val) + " " + t('common.currency')
}

function getCatMeta(catId) {
  return categories.value.find(c => c.id === catId) || { name: t('finance.cat.other'), icon: '💸' }
}
</script>

<template>
  <ToolShell
    icon="💰"
    :title="t('finance.title')"
    :description="t('finance.description')"
    :hint="t('finance.hint')"
  >
    <template #header>
      <AppHeader />
    </template>

    <div class="space-y-6">
      <FormAlert :message="error" />

      <!-- Summary Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="finance-summary finance-summary-primary">
          <span class="text-xs uppercase tracking-wider text-slate-600 dark:text-slate-300">{{ t('finance.balance') }}</span>
          <div class="text-2xl font-bold mt-2 font-mono text-slate-900 dark:text-white">
            {{ formatSum(balance) }}
          </div>
        </div>
        <div class="finance-summary finance-summary-income">
          <span class="text-xs uppercase tracking-wider text-slate-600 dark:text-slate-300">{{ t('finance.income') }}</span>
          <div class="text-2xl font-bold mt-2 font-mono text-slate-900 dark:text-white">
            +{{ formatSum(totalIncome) }}
          </div>
        </div>
        <div class="finance-summary finance-summary-expense">
          <span class="text-xs uppercase tracking-wider text-slate-600 dark:text-slate-300">{{ t('finance.expense') }}</span>
          <div class="text-2xl font-bold mt-2 font-mono text-slate-900 dark:text-white">
            -{{ formatSum(totalExpense) }}
          </div>
        </div>
      </div>

      <!-- Add Transaction Form -->
      <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 space-y-4">
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <span>➕</span> {{ t('finance.addTitle') }}
        </h3>
        <form class="space-y-3" @submit.prevent="addTransaction">
          <div class="grid grid-cols-2 gap-3">
            <button
              type="button"
              class="py-2 rounded-xl text-sm font-semibold transition"
              :class="newTx.type === 'expense' ? 'bg-rose-500 text-white shadow-sm' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'"
              @click="newTx.type = 'expense'"
            >
              {{ t('finance.typeExpense') }}
            </button>
            <button
              type="button"
              class="py-2 rounded-xl text-sm font-semibold transition"
              :class="newTx.type === 'income' ? 'bg-emerald-500 text-white shadow-sm' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'"
              @click="newTx.type = 'income'"
            >
              {{ t('finance.typeIncome') }}
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="label text-xs">{{ t('finance.amount') }}</label>
              <input v-model="newTx.amount" type="number" min="0" max="1000000000000" step="1000" class="input font-mono" placeholder="100 000" required @input="validateTransactionAmount" />
            </div>
            <div>
              <label class="label text-xs">{{ t('finance.category') }}</label>
              <select v-model="newTx.category" class="input">
                <option v-for="c in categories" :key="c.id" :value="c.id">
                  {{ c.icon }} {{ c.name }}
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="label text-xs">{{ t('finance.note') }}</label>
            <input v-model="newTx.note" type="text" class="input" :placeholder="t('finance.noteHint')" />
          </div>

          <button type="submit" class="btn-primary w-full !py-2.5" :disabled="saving">
            {{ saving ? t('finance.saving') : t('finance.save') }}
          </button>
        </form>
      </div>

      <!-- Transactions History List -->
      <div>
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 mb-3">{{ t('finance.history') }}</h3>
        <div v-if="loading" class="text-center text-slate-400 py-6 text-sm">
          {{ t('finance.historyLoading') }}
        </div>
        <div v-else-if="!transactions.length" class="text-center text-slate-400 py-6 text-sm">
          {{ t('finance.historyEmpty') }}
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="tx in transactions"
            :key="tx.id"
            class="flex items-center justify-between p-3.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/50 shadow-sm"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-xl shrink-0">
                {{ getCatMeta(tx.category).icon }}
              </div>
              <div>
                <p class="text-sm font-bold text-slate-800 dark:text-slate-100">{{ tx.note }}</p>
                <p class="text-xs text-slate-400">{{ getCatMeta(tx.category).name }} · {{ tx.date }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span
                class="font-mono font-bold text-sm"
                :class="tx.type === 'income' ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-800 dark:text-slate-100'"
              >
                {{ tx.type === 'income' ? '+' : '-' }}{{ formatSum(tx.amount) }}
              </span>
              <button
                class="text-slate-300 hover:text-rose-500 transition text-sm"
                :title="t('finance.delete')"
                @click="deleteTx(tx.id)"
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
