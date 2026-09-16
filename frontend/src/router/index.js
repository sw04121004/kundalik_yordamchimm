import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('../pages/Landing.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../pages/Login.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../pages/Register.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../pages/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/ai',
    name: 'ai-assistant',
    component: () => import('../pages/AIAssistant.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../pages/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/planner',
    name: 'planner',
    component: () => import('../pages/Planner.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/bmi',
    name: 'bmi',
    component: () => import('../pages/services/BMICalculator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/currency',
    name: 'currency',
    component: () => import('../pages/services/CurrencyConverter.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/qr-code',
    name: 'qr-code',
    component: () => import('../pages/services/QRCodeGenerator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/percent',
    name: 'percent',
    component: () => import('../pages/services/PercentCalculator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/calculator',
    name: 'calculator',
    component: () => import('../pages/services/SimpleCalculator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/average',
    name: 'average',
    component: () => import('../pages/services/AverageCalculator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/length',
    name: 'length',
    component: () => import('../pages/services/LengthConverter.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/weight',
    name: 'weight',
    component: () => import('../pages/services/WeightConverter.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/temperature',
    name: 'temperature',
    component: () => import('../pages/services/TemperatureConverter.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/date-diff',
    name: 'date-diff',
    component: () => import('../pages/services/DateDiff.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/day-counter',
    name: 'day-counter',
    component: () => import('../pages/services/DayCounter.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/text-counter',
    name: 'text-counter',
    component: () => import('../pages/services/TextCounter.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/case-converter',
    name: 'case-converter',
    component: () => import('../pages/services/CaseConverter.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/text-cleaner',
    name: 'text-cleaner',
    component: () => import('../pages/services/TextCleaner.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/password-generator',
    name: 'password-generator',
    component: () => import('../pages/services/PasswordGenerator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/random-number',
    name: 'random-number',
    component: () => import('../pages/services/RandomNumberGenerator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/image-resizer',
    name: 'image-resizer',
    component: () => import('../pages/services/ImageResizer.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/salary-calc',
    name: 'salary-calc',
    component: () => import('../pages/services/SalaryCalculator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/loan-calculator',
    name: 'loan-calculator',
    component: () => import('../pages/services/LoanCalculator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/currency-rates',
    name: 'currency-rates',
    component: () => import('../pages/services/CurrencyRates.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/time-tracker',
    name: 'time-tracker',
    component: () => import('../pages/services/TimeTracker.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/habit-tracker',
    name: 'habit-tracker',
    component: () => import('../pages/services/HabitTracker.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/goal-board',
    name: 'goal-board',
    component: () => import('../pages/services/GoalBoard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/image-format',
    name: 'image-format',
    component: () => import('../pages/services/ImageFormat.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/image-compress',
    name: 'image-compress',
    component: () => import('../pages/services/ImageCompress.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/image-bg-remove',
    name: 'image-bg-remove',
    component: () => import('../pages/services/ImageBgRemove.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/image-rotate',
    name: 'image-rotate',
    component: () => import('../pages/services/ImageRotate.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/image-filters',
    name: 'image-filters',
    component: () => import('../pages/services/ImageFilters.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools/deposit-calculator',
    name: 'deposit-calculator',
    component: () => import('../pages/services/DepositCalculator.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/finance',
    name: 'finance',
    component: () => import('../pages/Finance.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/kitchen',
    name: 'kitchen',
    component: () => import('../pages/Kitchen.vue'),
  },
  {
    path: '/home-services',
    name: 'home-services',
    component: () => import('../pages/HomeServices.vue'),
  },
  {
    path: '/study',
    name: 'study',
    component: () => import('../pages/Study.vue'),
  },
  {
    path: '/document',
    name: 'document',
    component: () => import('../pages/DocumentAI.vue'),
  },
  {
    path: '/tools/universal-calc',
    name: 'universal-calc',
    component: () => import('../pages/UniversalCalc.vue'),
  },
  {
    path: '/tools/math-calc',
    name: 'math-calc',
    component: () => import('../pages/MathCalc.vue'),
  },
  {
    path: '/tools/pomodoro',
    name: 'pomodoro',
    component: () => import('../pages/Pomodoro.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../pages/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { next: to.fullPath } }
  }
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }
  return true
})

export default router
