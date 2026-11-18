<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
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
  id: 1512569,
  name: 'Toshkent', admin1: 'Toshkent shahri', country: "O'zbekiston",
  country_code: 'UZ', lat: 41.26465, lon: 69.21627,
}
const { t, language, locale: currentLocale } = useI18n()

// Ob-havo API uz, ru va en tillarini qo'llab-quvvatlaydi
const weatherApiLanguage = computed(() => ['uz', 'ru', 'en'].includes(language.value) ? language.value : 'uz')
const numberFormat = computed(() => new Intl.NumberFormat(currentLocale(), { maximumFractionDigits: 1 }))

const countryNames = {
  uz: {
    UZ: "O'zbekiston", KZ: "Qozog'iston", KG: "Qirg'iziston", TJ: "Tojikiston",
    RU: "Rossiya", TR: "Turkiya", US: "AQSh", GB: "Buyuk Britaniya",
    AF: "Afg'oniston", CN: "Xitoy", IN: "Hindiston", IR: "Eron",
    AE: "BAA", SA: "Saudiya Arabistoni", DE: "Germaniya", FR: "Fransiya",
  },
  ru: {
    UZ: "Узбекистан", KZ: "Казахстан", KG: "Кыргызстан", TJ: "Таджикистан",
    RU: "Россия", TR: "Турция", US: "США", GB: "Великобритания",
    AF: "Афганистан", CN: "Китай", IN: "Индия", IR: "Иран",
    AE: "ОАЭ", SA: "Саудовская Аравия", DE: "Германия", FR: "Франция",
  },
  en: {
    UZ: "Uzbekistan", KZ: "Kazakhstan", KG: "Kyrgyzstan", TJ: "Tajikistan",
    RU: "Russia", TR: "Turkey", US: "United States", GB: "United Kingdom",
    AF: "Afghanistan", CN: "China", IN: "India", IR: "Iran",
    AE: "UAE", SA: "Saudi Arabia", DE: "Germany", FR: "France",
  },
}
const countryOptions = computed(() => {
  const map = countryNames[language.value] || countryNames.uz
  return Object.entries(map)
})
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
    uz: { 0: 'Ochiq', 1: 'Asosan ochiq', 2: 'Qisman bulutli', 3: 'Bulutli', 45: 'Tuman', 48: 'Qirovli tuman', 51: 'Mayda shivalama', 53: 'Shivalama', 55: 'Kuchli shivalama', 56: 'Muzli shivalama', 57: 'Kuchli muzli shivalama', 61: "Yengil yomg'ir", 63: "Yomg'ir", 65: "Kuchli yomg'ir", 66: "Muzli yomg'ir", 67: "Kuchli muzli yomg'ir", 71: 'Yengil qor', 73: 'Qor', 75: 'Kuchli qor', 77: 'Qor donachalari', 80: 'Yengil jala', 81: 'Jala', 82: 'Kuchli jala', 85: 'Qor jala', 86: 'Kuchli qor jala', 95: 'Momaqaldiroq', 96: "Do'l bilan momaqaldiroq", 99: "Kuchli do'l bilan momaqaldiroq" },
    ru: { 0: 'Ясно', 1: 'Преимущественно ясно', 2: 'Переменная облачность', 3: 'Облачно', 45: 'Туман', 48: 'Изморозь и туман', 51: 'Слабая морось', 53: 'Морось', 55: 'Сильная морось', 56: 'Ледяная морось', 57: 'Сильная ледяная морось', 61: 'Небольшой дождь', 63: 'Дождь', 65: 'Сильный дождь', 66: 'Ледяной дождь', 67: 'Сильный ледяной дождь', 71: 'Небольшой снег', 73: 'Снег', 75: 'Сильный снег', 77: 'Снежные зёрна', 80: 'Небольшой ливень', 81: 'Ливень', 82: 'Сильный ливень', 85: 'Снегопад', 86: 'Сильный снегопад', 95: 'Гроза', 96: 'Гроза с градом', 99: 'Сильная гроза с градом' },
    en: { 0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 45: 'Fog', 48: 'Rime fog', 51: 'Light drizzle', 53: 'Drizzle', 55: 'Heavy drizzle', 56: 'Freezing drizzle', 57: 'Heavy freezing drizzle', 61: 'Light rain', 63: 'Rain', 65: 'Heavy rain', 66: 'Freezing rain', 67: 'Heavy freezing rain', 71: 'Light snow', 73: 'Snow', 75: 'Heavy snow', 77: 'Snow grains', 80: 'Light showers', 81: 'Showers', 82: 'Heavy showers', 85: 'Snow showers', 86: 'Heavy snow showers', 95: 'Thunderstorm', 96: 'Thunderstorm with hail', 99: 'Heavy thunderstorm with hail' },
  }
  const langKey = descriptions[language.value] ? language.value : 'uz'
  const words = descriptions[langKey]
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
      if (requestId === searchRequestId) error.value = extractErrorMessage(requestError, t('weather.error'))
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
    error.value = extractErrorMessage(requestError, t('weather.error'))
  } finally {
    loading.value = false
  }
}

async function updateLocationLanguage() {
  if (!location.value) return
  try {
    const params = { lang: weatherApiLanguage.value }
    if (location.value.id) {
      params.id = location.value.id
    } else if (location.value.name) {
      params.q = location.value.name
      if (location.value.country_code) params.country = location.value.country_code
    } else {
      return
    }
    const { data } = await api.get('/weather/search/', { params })
    const updated = data.results?.[0]
    if (updated) {
      location.value = {
        ...location.value,
        id: updated.id || location.value.id,
        name: updated.name,
        admin1: updated.admin1,
        country: updated.country,
        country_code: updated.country_code || location.value.country_code,
      }
      cityQuery.value = [location.value.name, location.value.admin1, location.value.country].filter(Boolean).join(', ')
      localStorage.setItem(LOCATION_KEY, JSON.stringify(location.value))
    }
  } catch {
    // Tarmoq xatosi bo'lsa koordinatalar bo'yicha ishlashda davom etadi
  }
}

watch(language, async () => {
  await updateLocationLanguage()
  loadForecast()
})

onMounted(async () => {
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
  await updateLocationLanguage()
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
            <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">{{ t('weather.title') }}</h1>
          </div>
          <p class="text-sm text-slate-600 dark:text-slate-300">{{ t('weather.subtitle') }}</p>
        </div>
        <button type="button" class="btn-secondary self-start sm:self-auto" :disabled="loading" @click="loadForecast">
          <RefreshCw class="w-4 h-4" :class="loading ? 'animate-spin' : ''" aria-hidden="true" />
          {{ t('weather.refresh') }}
        </button>
      </header>

      <section class="card p-4 sm:p-5 mb-6" :aria-label="t('weather.city')">
        <div class="grid grid-cols-1 sm:grid-cols-[minmax(0,1fr)_220px] gap-4">
          <div class="relative">
            <label for="weather-city" class="label">{{ t('weather.city') }}</label>
            <div class="relative">
              <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" aria-hidden="true" />
              <input id="weather-city" v-model="cityQuery" class="input pl-10" type="search" autocomplete="off" :placeholder="t('weather.searchPlaceholder')" @input="searchCity" @focus="searchCity" />
            </div>
            <ul v-if="suggestions.length || (searched && !searchLoading)" class="absolute z-30 top-full left-0 right-0 mt-1 max-h-64 overflow-y-auto rounded-xl border border-slate-200 bg-white shadow-lg dark:border-white/10 dark:bg-[#222b28]" role="listbox">
              <li v-for="item in suggestions" :key="`${item.country_code}:${item.lat}:${item.lon}`" role="option" aria-selected="false">
                <button type="button" class="w-full px-4 py-3 text-left text-sm text-slate-800 hover:bg-brand-50 dark:text-slate-100 dark:hover:bg-brand-900/30" @mousedown.prevent="selectLocation(item)">
                  {{ [item.name, item.admin1, item.country].filter(Boolean).join(', ') }}
                </button>
              </li>
              <li v-if="searched && !suggestions.length" class="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">{{ t('weather.notFound') }}</li>
            </ul>
          </div>
          <div>
            <label for="weather-country" class="label">{{ t('weather.country') }}</label>
            <input id="weather-country" v-model="country" class="input" list="weather-country-options" maxlength="2" autocapitalize="characters" placeholder="UZ" @input="searchCity" />
            <datalist id="weather-country-options">
              <option v-for="option in countryOptions" :key="option[0]" :value="option[0]" :label="option[1]" />
            </datalist>
          </div>
        </div>
        <p v-if="searchLoading" class="mt-2 text-xs text-slate-500" role="status">{{ t('weather.loading') }}</p>
      </section>

      <p v-if="error" class="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-200" role="alert">{{ error }}</p>

      <section v-if="loading && !forecast" class="card p-6 sm:p-8 mb-6 animate-pulse" :aria-label="t('common.loading')">
        <div class="h-5 w-44 rounded bg-slate-200 dark:bg-slate-700 mb-5"></div>
        <div class="h-14 w-32 rounded bg-slate-200 dark:bg-slate-700 mb-4"></div>
        <div class="h-4 w-56 rounded bg-slate-200 dark:bg-slate-700"></div>
      </section>

      <template v-if="forecast">
        <section class="card p-5 sm:p-8 mb-6 overflow-hidden relative">
          <div class="absolute -top-24 -right-20 w-64 h-64 rounded-full bg-gradient-to-br from-brand-100/70 to-amber-100/40 dark:from-brand-900/30 dark:to-amber-900/10 blur-3xl pointer-events-none"></div>
          <div class="relative flex flex-col sm:flex-row sm:items-center justify-between gap-6">
            <div>
              <p class="text-sm font-semibold text-slate-600 dark:text-slate-300">{{ t('weather.current') }}</p>
              <h2 class="mt-1 text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2"><MapPin class="w-4 h-4 text-brand-600" aria-hidden="true" />{{ locationLabel }}</h2>
              <div class="mt-5 flex items-center gap-4">
                <component :is="weatherIcon(forecast.current.weather_code, forecast.current.is_day)" class="w-14 h-14 text-brand-600 dark:text-brand-300" :stroke-width="1.5" aria-hidden="true" />
                <div>
                  <p class="text-5xl font-bold tracking-tight text-slate-900 dark:text-white">{{ formatNumber(Math.round(forecast.current.temperature)) }}°</p>
                  <p class="text-sm text-slate-600 dark:text-slate-300">{{ weatherDescription(forecast.current.weather_code) }}</p>
                </div>
              </div>
              <p class="mt-3 text-sm text-slate-600 dark:text-slate-300">{{ t('weather.feels') }} {{ formatNumber(Math.round(forecast.current.apparent_temperature)) }}°</p>
              <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('weather.updated') }}: {{ lastUpdated }}</p>
            </div>
            <div class="grid grid-cols-2 gap-x-7 gap-y-5 sm:min-w-64">
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-brand-50 dark:bg-brand-900/40 text-brand-700 dark:text-brand-300"><Droplets class="w-5 h-5" aria-hidden="true" /></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t('weather.humidity') }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ forecast.current.humidity }}%</p></div></div>
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-sky-50 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300"><Wind class="w-5 h-5" aria-hidden="true" /></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t('weather.wind') }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ formatNumber(forecast.current.wind_speed) }} {{ forecast.units.wind_speed }}</p></div></div>
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-amber-50 dark:bg-amber-900/25 text-amber-700 dark:text-amber-300"><CloudRain class="w-5 h-5" aria-hidden="true" /></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t('weather.precipitation') }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ formatNumber(forecast.current.precipitation) }} {{ forecast.units.precipitation }}</p></div></div>
              <div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full flex items-center justify-center bg-violet-50 dark:bg-violet-900/25 text-violet-700 dark:text-violet-300"><span class="text-sm font-bold">hPa</span></span><div><p class="text-xs text-slate-500 dark:text-slate-400">{{ t('weather.pressure') }}</p><p class="font-semibold text-slate-800 dark:text-slate-100">{{ formatNumber(Math.round(forecast.current.pressure)) }} {{ forecast.units.pressure }}</p></div></div>
            </div>
          </div>
        </section>

        <section class="card p-5 sm:p-6 mb-6">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-4">{{ t('weather.hourly') }}</h2>
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
          <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-3">{{ t('weather.daily') }}</h2>
          <div class="divide-y divide-slate-100 dark:divide-white/10">
            <div v-for="(day, index) in forecast.daily" :key="day.date" class="grid grid-cols-[minmax(80px,1fr)_36px_minmax(90px,1fr)_48px] sm:grid-cols-[minmax(130px,1fr)_40px_minmax(120px,1fr)_90px_90px] items-center gap-3 py-3">
              <p class="text-sm font-medium text-slate-700 dark:text-slate-200">{{ index === 0 ? t('weather.today') : formatDay(day.date) }}</p>
              <component :is="weatherIcon(day.weather_code)" class="w-5 h-5 text-brand-700 dark:text-brand-300" aria-hidden="true" />
              <div class="flex items-center gap-2 text-sm"><span class="font-semibold text-slate-900 dark:text-white">{{ formatNumber(Math.round(day.temperature_max)) }}°</span><span class="text-slate-500 dark:text-slate-400">{{ formatNumber(Math.round(day.temperature_min)) }}°</span></div>
              <p class="text-right text-xs text-sky-700 dark:text-sky-300">{{ day.precipitation_probability ?? 0 }}%</p>
              <p class="hidden sm:block text-right text-xs text-slate-500 dark:text-slate-400">{{ t('weather.sunrise') }} {{ day.sunrise?.slice(11, 16) }} · {{ t('weather.sunset') }} {{ day.sunset?.slice(11, 16) }}</p>
            </div>
          </div>
        </section>
      </template>

      <p v-else-if="!loading && !error" class="py-12 text-center text-slate-600 dark:text-slate-300">{{ t('weather.notFound') }}</p>
      <p class="mt-6 text-center text-xs text-slate-500 dark:text-slate-400">
        {{ t('weather.source') }} <a class="font-semibold text-brand-700 dark:text-brand-300 underline" href="https://open-meteo.com" target="_blank" rel="noopener noreferrer">Open-Meteo.com</a>
      </p>
    </main>
  </div>
</template>
