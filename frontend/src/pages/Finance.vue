<script setup>
import { ref, computed, onMounted } from 'vue'
import ToolShell from '../components/ToolShell.vue'
import AppHeader from '../components/AppHeader.vue'

const categories = [
  { id: 'salary', name: 'Maosh / Daromad', icon: '💰', type: 'income' },
  { id: 'food', name: 'Oziq-ovqat va bozor', icon: '🛒', type: 'expense' },
  { id: 'transport', name: 'Transport / Yonilg\'i', icon: '🚖', type: 'expense' },
  { id: 'bills', name: 'Kommunal / Aloqa', icon: '⚡', type: 'expense' },
  { id: 'fun', name: 'Hordiq va ko\'ngilochar', icon: '🎬', type: 'expense' },
  { id: 'other', name: 'Boshqa xarajatlar', icon: '📦', type: 'expense' },
]

const transactions = ref([
  { id: 1, type: 'income', category: 'salary', amount: 3500000, note: 'Oylik maosh', date: new Date().toISOString().slice(0, 10) },
  { id: 2, type: 'expense', category: 'food', amount: 120000, note: 'KORZINKA bozor-ochar', date: new Date().toISOString().slice(0, 10) },
  { id: 3, type: 'expense', category: 'transport', amount: 30000, note: 'Taksi va metro', date: new Date().toISOString().slice(0, 10) }
])

const newTx = ref({
  type: 'expense',
  category: 'food',
  amount: '',
  note: ''
})

onMounted(() => {
  const saved = localStorage.getItem('qulay_finance_txs')
  if (saved) {
    try { transactions.value = JSON.parse(saved) } catch (e) {}
  }
})

function saveTxs() {
  localStorage.setItem('qulay_finance_txs', JSON.stringify(transactions.value))
}

function addTransaction() {
  const num = Number(newTx.value.amount)
  if (isNaN(num) || num <= 0) return

  transactions.value.unshift({
    id: Date.now(),
    type: newTx.value.type,
    category: newTx.value.category,
    amount: num,
    note: newTx.value.note.trim() || (newTx.value.type === 'income' ? 'Kirim' : 'Chiqim'),
    date: new Date().toISOString().slice(0, 10)
  })

  saveTxs()
  newTx.value.amount = ''
  newTx.value.note = ''
}

function deleteTx(id) {
  transactions.value = transactions.value.filter(t => t.id !== id)
  saveTxs()
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
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="p-4 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-soft">
          <span class="text-xs uppercase tracking-wider opacity-80">Balans</span>
          <div class="text-2xl font-extrabold mt-1 font-mono">
            {{ formatSum(balance) }}
          </div>
        </div>
        <div class="p-4 rounded-2xl bg-emerald-500 text-white shadow-soft">
          <span class="text-xs uppercase tracking-wider opacity-80">Jami Kirim</span>
          <div class="text-2xl font-extrabold mt-1 font-mono">
            +{{ formatSum(totalIncome) }}
          </div>
        </div>
        <div class="p-4 rounded-2xl bg-rose-500 text-white shadow-soft">
          <span class="text-xs uppercase tracking-wider opacity-80">Jami Chiqim</span>
          <div class="text-2xl font-extrabold mt-1 font-mono">
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
              <input v-model="newTx.amount" type="number" min="0" step="1000" class="input font-mono" placeholder="100 000" required />
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

          <button type="submit" class="btn-primary w-full !py-2.5">
            + Saqlash
          </button>
        </form>
      </div>

      <!-- Transactions History List -->
      <div>
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100 mb-3">📋 Amallar tarixi</h3>
        <div v-if="!transactions.length" class="text-center text-slate-400 py-6 text-sm">
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
