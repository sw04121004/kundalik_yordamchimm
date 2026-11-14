<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import {
  Cloud, CloudDrizzle, CloudFog, CloudLightning, CloudRain, CloudSnow,
  CloudSun, Droplets, MapPin, Moon, RefreshCw, Search, Sun, Wind,
} from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import api from '../api/axios'
import { extractErrorMessage } from '../api/errors'
import { useI18n } from '../i18n'

const LOCATION_KEY = 'qulay_weather_location'
const DEFAULT_LOCATION = {
  name: 'Toshkent', admin1: 'Toshkent shahri', country: "O'zbekiston",
  country_code: 'UZ', lat: 41.3111, lon: 69.2797,
}
const { language, locale: currentLocale } = useI18n()
// The weather API accepts only Uzbek, Russian and English. Other UI languages
// use English weather descriptions until translations are available.
const weatherApiLanguage = computed(() => ['uz', 'ru', 'en'].includes(language.value) ? language.value : 'en')
const numberFormat = computed(() => new Intl.NumberFormat(currentLocale(), { maximumFractionDigits: 1 }))
const translations = {
  uz: {
    title: "Ob-havo", subtitle: "Shaharni qidiring va yaqin kunlar prognozini ko'ring",
    city: "Shahar nomi", country: "Mamlakat", allCountries: "Barcha mamlakatlar",
    searchPlaceholder: "Shaharni kiriting...", notFound: "Shahar topilmadi",
    current: "Hozirgi ob-havo", feels: "His qilinishi", humidity: "Namlik",
    wind: "Shamol", precipitation: "Yog'in", pressure: "Bosim",
    updated: "Yangilangan", refresh: "Yangilash", hourly: "Keyingi 24 soat",
    daily: "14 kunlik prognoz", rainChance: "Yog'in ehtimoli", high: "Yuqori",
    low: "Past", sunrise: "Quyosh chiqishi", sunset: "Quyosh botishi",
    loading: "Ob-havo yuklanmoqda...", error: "Ob-havo ma'lumotini olib bo'lmadi.",
  },
  ru: {
    title: "Погода", subtitle: "Найдите город и посмотрите прогноз на ближайшие дни",
    city: "Название города", country: "Страна", allCountries: "Все страны",
    searchPlaceholder: "Введите город...", notFound: "Город не найден",
    current: "Сейчас", feels: "Ощущается как", humidity: "Влажность",
    wind: "Ветер", precipitation: "Осадки", pressure: "Давление",
    updated: "Обновлено", refresh: "Обновить", hourly: "Ближайшие 24 часа",
    daily: "Прогноз на 14 дней", rainChance: "Вероятность осадков", high: "Макс.",
    low: "Мин.", sunrise: "Восход", sunset: "Закат", loading: "Загружаем погоду...",
    error: "Не удалось загрузить погоду.",
  },
  en: {
    title: "Weather", subtitle: "Find a city and see the forecast for the coming days",
    city: "City name", country: "Country", allCountries: "All countries",
    searchPlaceholder: "Enter a city...", notFound: "City not found",
    current: "Current weather", feels: "Feels like", humidity: "Humidity",
    wind: "Wind", precipitation: "Precipitation", pressure: "Pressure",
    updated: "Updated", refresh: "Refresh", hourly: "Next 24 hours",
    daily: "14-day forecast", rainChance: "Chance of precipitation", high: "High",
    low: "Low", sunrise: "Sunrise", sunset: "Sunset", loading: "Loading weather...",
    error: "Could not load weather information.",
  },
}
translations.ru = {
  title: '\u041f\u043e\u0433\u043e\u0434\u0430', subtitle: '\u041d\u0430\u0439\u0434\u0438\u0442\u0435 \u0433\u043e\u0440\u043e\u0434 \u0438 \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0438\u0442\u0435 \u043f\u0440\u043e\u0433\u043d\u043e\u0437 \u043d\u0430 \u0431\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u0434\u043d\u0438',
  city: '\u0413\u043e\u0440\u043e\u0434', country: '\u0421\u0442\u0440\u0430\u043d\u0430', allCountries: '\u0412\u0441\u0435 \u0441\u0442\u0440\u0430\u043d\u044b', searchPlaceholder: '\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0433\u043e\u0440\u043e\u0434...', notFound: '\u0413\u043e\u0440\u043e\u0434 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d',
  current: '\u0421\u0435\u0439\u0447\u0430\u0441', feels: '\u041e\u0449\u0443\u0449\u0430\u0435\u0442\u0441\u044f \u043a\u0430\u043a', humidity: '\u0412\u043b\u0430\u0436\u043d\u043e\u0441\u0442\u044c', wind: '\u0412\u0435\u0442\u0435\u0440', precipitation: '\u041e\u0441\u0430\u0434\u043a\u0438', pressure: '\u0414\u0430\u0432\u043b\u0435\u043d\u0438\u0435',
  updated: '\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u043e', refresh: '\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c', hourly: '\u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 24 \u0447\u0430\u0441\u0430', daily: '\u041f\u0440\u043e\u0433\u043d\u043e\u0437 \u043d\u0430 14 \u0434\u043d\u0435\u0439', rainChance: '\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c \u043e\u0441\u0430\u0434\u043a\u043e\u0432', high: '\u041c\u0430\u043a\u0441.', low: '\u041c\u0438\u043d.', sunrise: '\u0412\u043e\u0441\u0445\u043e\u0434', sunset: '\u0417\u0430\u043a\u0430\u0442', loading: '\u0417\u0430\u0433\u0440\u0443\u0436\u0430\u0435\u043c \u043f\u043e\u0433\u043e\u0434\u0443...', error: '\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043f\u043e\u0433\u043e\u0434\u0443.',
}
const t = computed(() => translations[language.value] || translations.en)
const countryOptions = [
  ['UZ', 'O‘zbekiston'], ['KZ', 'Qozog‘iston'], ['KG', 'Qirg‘iziston'], ['TJ', 'Tojikiston'],
  ['RU', 'Rossiya'], ['TR', 'Turkiya'], ['US', 'AQSh'], ['GB', 'Buyuk Britaniya'],
  ['AF', 'Afg‘oniston'], ['CN', 'Xitoy'], ['IN', 'Hindiston'], ['IR', 'Eron'],
  ['AE', 'BAA'], ['SA', 'Saudiya Arabistoni'], ['DE', 'Germaniya'], ['FR', 'Fransiya'],
]
const location = ref(null)
const cityQuery = ref('')
const country = ref('')
const suggestions = ref([])
const searched = ref(false)
const searchLoading = ref(false)
const loading = ref(false)
const forecast = ref(null)
const error = ref('')
const lastUpdated = ref('')
let searchTimer
let refreshTimer
let searchRequestId = 0

const locationLabel = computed(() => {
  if (!location.value) return ''
  return [location.value.name, location.value.admin1, location.value.country].filter(Boolean).join(', ')
})

function weatherDescription(code) {
  const descriptions = {
    uz: { 0: 'Ochiq', 1: 'Asosan ochiq', 2: 'Qisman bulutli', 3: 'Bulutli', 45: 'Tuman', 48: 'Qirovli tuman', 51: 'Mayda shivalama', 53: 'Shivalama', 55: 'Kuchli shivalama', 56: 'Muzli shivalama', 57: 'Kuchli muzli shivalama', 61: 'Yengil yomg‘ir', 63: 'Yomg‘ir', 65: 'Kuchli yomg‘ir', 66: 'Muzli yomg‘ir', 67: 'Kuchli muzli yomg‘ir', 71: 'Yengil qor', 73: 'Qor', 75: 'Kuchli qor', 77: 'Qor donachalari', 80: 'Yengil jala', 81: 'Jala', 82: 'Kuchli jala', 85: 'Qor jala', 86: 'Kuchli qor jala', 95: 'Momaqaldiroq', 96: 'Do‘l bilan momaqaldiroq', 99: 'Kuchli do‘l bilan momaqaldiroq' },
    ru: { 0: 'Ясно', 1: 'Преимущественно ясно', 2: 'Переменная облачность', 3: 'Облачно', 45: 'Туман', 48: 'Изморозь и туман', 51: 'Слабая морось', 53: 'Морось', 55: 'Сильная морось', 56: 'Ледяная морось', 57: 'Сильная ледяная морось', 61: 'Небольшой дождь', 63: 'Дождь', 65: 'Сильный дождь', 66: 'Ледяной дождь', 67: 'Сильный ледяной дождь', 71: 'Небольшой снег', 73: 'Снег', 75: 'Сильный снег', 77: 'Снежные зёрна', 80: 'Небольшой ливень', 81: 'Ливень', 82: 'Сильный ливень', 85: 'Снегопад', 86: 'Сильный снегопад', 95: 'Гроза', 96: 'Гроза с градом', 99: 'Сильная гроза с градом' },
    en: { 0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 45: 'Fog', 48: 'Rime fog', 51: 'Light drizzle', 53: 'Drizzle', 55: 'Heavy drizzle', 56: 'Freezing drizzle', 57: 'Heavy freezing drizzle', 61: 'Light rain', 63: 'Rain', 65: 'Heavy rain', 66: 'Freezing rain', 67: 'Heavy freezing rain', 71: 'Light snow', 73: 'Snow', 75: 'Heavy snow', 77: 'Snow grains', 80: 'Light showers', 81: 'Showers', 82: 'Heavy showers', 85: 'Snow showers', 86: 'Heavy snow showers', 95: 'Thunderstorm', 96: 'Thunderstorm with hail', 99: 'Heavy thunderstorm with hail' },
  }
  descriptions.ru = {
    0: '\u042f\u0441\u043d\u043e', 1: '\u041f\u0440\u0435\u0438\u043c\u0443\u0449\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e \u044f\u0441\u043d\u043e', 2: '\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f \u043e\u0431\u043b\u0430\u0447\u043d\u043e\u0441\u0442\u044c', 3: '\u041e\u0431\u043b\u0430\u0447\u043d\u043e', 45: '\u0422\u0443\u043c\u0430\u043d', 48: '\u0418\u043d\u0435\u0439\u043d\u044b\u0439 \u0442\u0443\u043c\u0430\u043d', 51: '\u0421\u043b\u0430\u0431\u0430\u044f \u043c\u043e\u0440\u043e\u0441\u044c', 53: '\u041c\u043e\u0440\u043e\u0441\u044c', 55: '\u0421\u0438\u043b\u044c\u043d\u0430\u044f \u043c\u043e\u0440\u043e\u0441\u044c', 56: '\u041b\u0435\u0434\u044f\u043d\u0430\u044f \u043c\u043e\u0440\u043e\u0441\u044c', 57: '\u0421\u0438\u043b\u044c\u043d\u0430\u044f \u043b\u0435\u0434\u044f\u043d\u0430\u044f \u043c\u043e\u0440\u043e\u0441\u044c', 61: '\u041d\u0435\u0431\u043e\u043b\u044c\u0448\u043e\u0439 \u0434\u043e\u0436\u0434\u044c', 63: '\u0414\u043e\u0436\u0434\u044c', 65: '\u0421\u0438\u043b\u044c\u043d\u044b\u0439 \u0434\u043e\u0436\u0434\u044c', 66: '\u041b\u0435\u0434\u044f\u043d\u043e\u0439 \u0434\u043e\u0436\u0434\u044c', 67: '\u0421\u0438\u043b\u044c\u043d\u044b\u0439 \u043b\u0435\u0434\u044f\u043d\u043e\u0439 \u0434\u043e\u0436\u0434\u044c', 71: '\u041d\u0435\u0431\u043e\u043b\u044c\u0448\u043e\u0439 \u0441\u043d\u0435\u0433', 73: '\u0421\u043d\u0435\u0433', 75: '\u0421\u0438\u043b\u044c\u043d\u044b\u0439 \u0441\u043d\u0435\u0433', 77: '\u0421\u043d\u0435\u0436\u043d\u044b\u0435 \u0437\u0435\u0440\u043d\u0430', 80: '\u041d\u0435\u0431\u043e\u043b\u044c\u0448\u043e\u0439 \u043b\u0438\u0432\u0435\u043d\u044c', 81: '\u041b\u0438\u0432\u0435\u043d\u044c', 82: '\u0421\u0438\u043b\u044c\u043d\u044b\u0439 \u043b\u0438\u0432\u0435\u043d\u044c', 85: '\u0421\u043d\u0435\u0433\u043e\u043f\u0430\u0434', 86: '\u0421\u0438\u043b\u044c\u043d\u044b\u0439 \u0441\u043d\u0435\u0433\u043e\u043f\u0430\u0434', 95: '\u0413\u0440\u043e\u0437\u0430', 96: '\u0413\u0440\u043e\u0437\u0430 \u0441 \u0433\u0440\u0430\u0434\u043e\u043c', 99: '\u0421\u0438\u043b\u044c\u043d\u0430\u044f \u0433\u0440\u043e\u0437\u0430 \u0441 \u0433\u0440\u0430\u0434\u043e\u043c',
  }
  const words = descriptions[language.value] || descriptions.en
  if (words[code] !== undefined) return words[code]
  if ([51, 53, 55, 56, 57].includes(code)) return words[53]
  if ([61, 63, 65, 66, 67].includes(code)) return words[63]
  if ([71, 73, 75, 77].includes(code)) return words[73]
  if ([80, 81, 82].includes(code)) return words[81]
  if ([85, 86].includes(code)) return words[85]
  if ([95, 96, 99].includes(code)) return words[95]
  return words[3]
}

function weatherIcon(code, isDay = true) {
  if (code === 0) return isDay ? Sun : Moon
  if (code === 1 || code === 2) return CloudSun
  if (code === 3) return Cloud
  if (code === 45 || code === 48) return CloudFog
  if ([51, 53, 55, 56, 57].includes(code)) return CloudDrizzle
  if ([61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return CloudRain
  if ([71, 73, 75, 77, 85, 86].includes(code)) return CloudSnow
  if ([95, 96, 99].includes(code)) return CloudLightning
  return Cloud
}

function formatDay(value) {
  const [year, month, day] = value.split('-').map(Number)
  return new Intl.DateTimeFormat(currentLocale(), { weekday: 'short', day: 'numeric', month: 'short' })
    .format(new Date(year, month - 1, day))
}

function formatNumber(value) {
  return numberFormat.value.format(Number(value))
}

function searchCity() {
  const requestId = ++searchRequestId
  clearTimeout(searchTimer)
  suggestions.value = []
  searched.value = false
  searchLoading.value = false
  if (cityQuery.value.trim().length < 2) return
  searchTimer = setTimeout(async () => {
    searchLoading.value = true
    try {
      const { data } = await api.get('/weather/search/', {
        params: { q: cityQuery.value.trim(), country: country.value, lang: weatherApiLanguage.value },
      })
      if (requestId === searchRequestId) {
        suggestions.value = data.results || []
        searched.value = true
      }
    } catch (requestError) {
      if (requestId === searchRequestId) error.value = extractErrorMessage(requestError, t.value.error)
    } finally {
      if (requestId === searchRequestId) searchLoading.value = false
    }
  }, 300)
}

function selectLocation(item) {
  searchRequestId += 1
  clearTimeout(searchTimer)
  searchLoading.value = false
  location.value = item
  cityQuery.value = [item.name, item.admin1, item.country].filter(Boolean).join(', ')
  suggestions.value = []
  searched.value = false
  localStorage.setItem(LOCATION_KEY, JSON.stringify(item))
  loadForecast()
}

async function loadForecast() {
  if (!location.value) return
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/weather/forecast/', {
      params: { lat: location.value.lat, lon: location.value.lon, lang: weatherApiLanguage.value },
    })
    forecast.value = data
    lastUpdated.value = new Intl.DateTimeFormat(currentLocale(), { hour: '2-digit', minute: '2-digit' }).format(new Date())
  } catch (requestError) {
    error.value = extractErrorMessage(requestError, t.value.error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  let savedLocation
  try {
    savedLocation = JSON.parse(localStorage.getItem(LOCATION_KEY) || 'null')
  } catch {
    savedLocation = null
  }
  const savedIsValid = savedLocation && Number.isFinite(Number(savedLocation.lat)) && Number.isFinite(Number(savedLocation.lon))
  location.value = savedIsValid ? savedLocation : DEFAULT_LOCATION
  cityQuery.value = [location.value.name, location.value.admin1, location.value.country].filter(Boolean).join(', ')
  if (!savedIsValid) localStorage.setItem(LOCATION_KEY, JSON.stringify(DEFAULT_LOCATION))
  loadForecast()
  refreshTimer = window.setInterval(loadForecast, 10 * 60 * 1000)
})

onUnmounted(() => {
  clearTimeout(searchTimer)
  clearInterval(refreshTimer)
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-[#111318]">
    <AppHeader />
    <main class="max-w-5xl mx-auto px-4 sm:px-6 py-8 sm:py-10">
      <header class="mb-8 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-5">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <span class="w-11 h-11 rounded-full flex items-center justify-center bg-brand-100 dark:bg-brand-900/50 text-brand-700 dark:text-brand-300">
              <Sun class="w-6 h-6" aria-hidden="true" />
            </span>
            <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">{{ t.title }}</h1>
          </div>
          <p class="text-sm text-slate-600 dark:text-slate-300">{{ t.subtitle }}</p>
        </div>
        <button type="button" class="btn-secondary self-start sm:self-auto" :disabled="loading" @click="loadForecast">
          <RefreshCw class="w-4 h-4" :class="loading ? 'animate-spin' : ''" aria-hidden="true" />
          {{ t.refresh }}
        </button>
      </header>

      <section class="card p-4 sm:p-5 mb-6" aria-label="Shahar qidirish">
        <div class="grid grid-cols-1 sm:grid-cols-[minmax(0,1fr)_220px] gap-4">
          <div class="relative">
            <label for="weather-city" class="label">{{ t.city }}</label>
            <div class="relative">
              <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" aria-hidden="true" />
              <input id="weather-city" v-model="cityQuery" class="input pl-10" type="search" autocomplete="off" :placeholder="t.searchPlaceholder" @input="searchCity" @focus="searchCity" />
            </div>
            <ul v-if="suggestions.length || (searched && !searchLoading)" class="absolute z-30 top-full left-0 right-0 mt-1 max-h-64 overflow-y-auto rounded-xl border border-slate-200 bg-white shadow-lg dark:border-white/10 dark:bg-[#222b28]" role="listbox">
              <li v-for="item in suggestions" :key="`${item.country_code}:${item.lat}:${item.lon}`" role="option" aria-selected="false">
                <button type="button" class="w-full px-4 py-3 text-left text-sm text-slate-800 hover:bg-brand-50 dark:text-slate-100 dark:hover:bg-brand-900/30" @mousedown.prevent="selectLocation(item)">
                  {{ [item.name, item.admin1, item.country].filter(Boolean).join(', ') }}
                </button>
              </li>
              <li v-if="searched && !suggestions.length" class="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">{{ t.notFound }}</li>
            </ul>
          </div>
          <div>
            <label for="weather-country" class="label">{{ t.country }}</label>
            <input id="weather-country" v-model="country" class="input" list="weather-country-options" maxlength="2" autocapitalize="characters" placeholder="UZ" @input="searchCity" />
            <datalist id="weather-country-options">
              <option v-for="option in countryOptions" :key="option[0]" :value="option[0]" :label="option[1]" />
            </datalist>
          </div>
        </div>
        <p v-if="searchLoading" class="mt-2 text-xs text-slate-500" role="status">{{ t.loading }}</p>
      </section>

      <p v-if="error" class="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-200" role="alert">{{ error }}</p>

      <section v-if="loading && !forecast" class="card p-6 sm:p-8 mb-6 animate-pulse" aria-label="Yuklanmoqda">
        <div class="h-5 w-44 rounded bg-slate-200 dark:bg-slate-700 mb-5"></div>
        <div class="h-14 w-32 rounded bg-slate-200 dark:bg-slate-700 mb-4"></div>
        <div class="h-4 w-56 rounded bg-slate-200 dark:bg-slate-700"></div>
      </section>

      <template v-if="forecast">
        <section class="card p-5 sm:p-8 mb-6 overflow-hidden relative">
          <div class="absolute -top-24 -right-20 w-64 h-64 rounded-full bg-gradient-to-br from-brand-100/70 to-amber-100/40 dark:from-brand-900/30 dark:to-amber-900/10 blur-3xl pointer-events-none"></div>
          <div class="relative flex flex-col sm:flex-row sm:items-center justify-between gap-6">
            <div>
              <p class="text-sm font-semibold text-slate-600 dark:text-slate-300">{{ t.current }}</p>
              <h2 class="mt-1 text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2"><MapPin class="w-4 h-4 text-brand-600" aria-hidden="true" />{{ locationLabel }}</h2>
              <div class="mt-5 flex items-center gap-4">
                <component :is="weatherIcon(forecast.current.weather_code, forecast.current.is_day)" class="w-14 h-14 text-brand-600 dark:text-brand-300" :stroke-width="1.5" aria-hidden="true" />
                <div>
                  <p class="text-5xl font-bold tracking-tight text-slate-900 dark:text-white">{{ formatNumber(Math.round(forecast.current.temperature)) }}°</p>
                  <p class="text-sm text-slate-600 dark:text-slate-300">{{ weatherDescription(forecast.current.weather_code) }}</p>
                </div>
              </div>
              <p class="mt-3 text-sm text-slate-600 dark:text-slate-300">{{ t.feels }} {{ formatNumber(Math.round(forecast.current.apparent_temperature)) }}°</p>
              <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t.updated }}: {{ lastUpdated }}</p>
            </div>
            <div class="grid grid-cols-2 gap-x-7 gap-y-5 sm:min-w-64">
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-brand-50 dark:bg-brand-900/40 text-brand-700 dark:text-brand-300"><Droplets class="w-5 h-5" aria-hidden="true" /></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t.humidity }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ forecast.current.humidity }}%</p></div></div>
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-sky-50 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300"><Wind class="w-5 h-5" aria-hidden="true" /></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t.wind }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ formatNumber(forecast.current.wind_speed) }} {{ forecast.units.wind_speed }}</p></div></div>
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-amber-50 dark:bg-amber-900/25 text-amber-700 dark:text-amber-300"><CloudRain class="w-5 h-5" aria-hidden="true" /></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t.precipitation }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ formatNumber(forecast.current.precipitation) }} {{ forecast.units.precipitation }}</p></div></div>
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-violet-50 dark:bg-violet-900/25 text-violet-700 dark:text-violet-300"><span class="text-sm font-bold">hPa</span></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t.pressure }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ formatNumber(Math.round(forecast.current.pressure)) }} {{ forecast.units.pressure }}</p></div></div>
            </div>
          </div>
        </section>

        <section class="card p-5 sm:p-6 mb-6">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-4">{{ t.hourly }}</h2>
          <div class="flex gap-3 overflow-x-auto pb-2">
            <div v-for="hour in forecast.hourly" :key="hour.time" class="min-w-[76px] rounded-xl bg-brand-50/60 dark:bg-brand-900/20 px-3 py-3 text-center">
              <p class="text-xs text-slate-600 dark:text-slate-300">{{ hour.time.slice(11, 16) }}</p>
              <component :is="weatherIcon(hour.weather_code)" class="w-5 h-5 mx-auto my-2 text-brand-700 dark:text-brand-300" aria-hidden="true" />
              <p class="font-semibold text-slate-800 dark:text-slate-100">{{ formatNumber(Math.round(hour.temperature)) }}°</p>
              <p class="mt-1 text-[11px] text-sky-700 dark:text-sky-300">{{ hour.precipitation_probability ?? 0 }}%</p>
            </div>
          </div>
        </section>

        <section class="card p-5 sm:p-6">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-3">{{ t.daily }}</h2>
          <div class="divide-y divide-slate-100 dark:divide-white/10">
            <div v-for="(day, index) in forecast.daily" :key="day.date" class="grid grid-cols-[minmax(80px,1fr)_36px_minmax(90px,1fr)_48px] sm:grid-cols-[minmax(130px,1fr)_40px_minmax(120px,1fr)_90px_90px] items-center gap-3 py-3">
              <p class="text-sm font-medium text-slate-700 dark:text-slate-200">{{ index === 0 ? (language === 'ru' ? 'Сегодня' : language === 'en' ? 'Today' : 'Bugun') : formatDay(day.date) }}</p>
              <component :is="weatherIcon(day.weather_code)" class="w-5 h-5 text-brand-700 dark:text-brand-300" aria-hidden="true" />
              <div class="flex items-center gap-2 text-sm"><span class="font-semibold text-slate-900 dark:text-white">{{ formatNumber(Math.round(day.temperature_max)) }}°</span><span class="text-slate-500 dark:text-slate-400">{{ formatNumber(Math.round(day.temperature_min)) }}°</span></div>
              <p class="text-right text-xs text-sky-700 dark:text-sky-300">{{ day.precipitation_probability ?? 0 }}%</p>
              <p class="hidden sm:block text-right text-xs text-slate-500 dark:text-slate-400">{{ t.sunrise }} {{ day.sunrise?.slice(11, 16) }} · {{ t.sunset }} {{ day.sunset?.slice(11, 16) }}</p>
            </div>
          </div>
        </section>
      </template>

      <p v-else-if="!loading && !error" class="py-12 text-center text-slate-600 dark:text-slate-300">{{ t.notFound }}</p>
      <p class="mt-6 text-center text-xs text-slate-500 dark:text-slate-400">
        Ob-havo ma'lumotlari: <a class="font-semibold text-brand-700 dark:text-brand-300 underline" href="https://open-meteo.com" target="_blank" rel="noopener noreferrer">Open-Meteo.com</a>
      </p>
    </main>
  </div>
</template>
