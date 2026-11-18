import { defineStore } from 'pinia'

// 8 distinct, harmonious colors: Ko'k (standart), Binafsha, Zumrad, Atirgul, To'q sariq, Firuza, Oltin, Grafit
export const ACCENT_PRESETS = {
  blue: {
    label: "Ko'k",
    labels: { uz: "Ko'k", ru: "Синий", en: "Blue" },
    swatch: '#2563eb',
    shades: {
      50: '239 246 255',
      100: '219 234 254',
      200: '191 219 254',
      300: '147 197 253',
      400: '96 165 250',
      500: '37 99 235',
      600: '29 78 216',
      700: '29 64 175',
      800: '30 58 138',
      900: '23 37 84',
      950: '15 23 42',
    },
  },
  purple: {
    label: 'Binafsha',
    labels: { uz: 'Binafsha', ru: 'Фиолетовый', en: 'Purple' },
    swatch: '#7c3aed',
    shades: {
      50: '250 245 255',
      100: '243 232 255',
      200: '233 213 255',
      300: '216 180 254',
      400: '192 132 252',
      500: '124 58 237',
      600: '109 40 217',
      700: '91 33 182',
      800: '76 29 149',
      900: '59 7 100',
      950: '46 16 101',
    },
  },
  emerald: {
    label: 'Zumrad',
    labels: { uz: 'Zumrad', ru: 'Изумрудный', en: 'Emerald' },
    swatch: '#059669',
    shades: {
      50: '236 253 245',
      100: '209 250 229',
      200: '167 243 208',
      300: '110 231 183',
      400: '52 211 153',
      500: '5 150 105',
      600: '4 120 87',
      700: '6 95 70',
      800: '6 78 59',
      900: '4 47 36',
      950: '2 44 34',
    },
  },
  rose: {
    label: 'Atirgul',
    labels: { uz: 'Atirgul', ru: 'Розовый', en: 'Rose' },
    swatch: '#e11d48',
    shades: {
      50: '255 241 242',
      100: '255 228 230',
      200: '254 205 211',
      300: '253 164 175',
      400: '251 113 133',
      500: '225 29 72',
      600: '190 18 60',
      700: '159 18 57',
      800: '136 19 55',
      900: '76 5 25',
      950: '47 4 17',
    },
  },
  orange: {
    label: "To'q sariq",
    labels: { uz: "To'q sariq", ru: 'Оранжевый', en: 'Orange' },
    swatch: '#ea580c',
    shades: {
      50: '255 247 237',
      100: '255 237 213',
      200: '254 215 170',
      300: '253 186 116',
      400: '251 146 60',
      500: '234 88 12',
      600: '194 65 12',
      700: '154 52 18',
      800: '124 45 18',
      900: '67 20 7',
      950: '43 14 5',
    },
  },
  teal: {
    label: 'Firuza',
    labels: { uz: 'Firuza', ru: 'Бирюзовый', en: 'Teal' },
    swatch: '#0d9488',
    shades: {
      50: '240 253 250',
      100: '204 251 241',
      200: '153 246 228',
      300: '94 234 212',
      400: '45 212 191',
      500: '13 148 136',
      600: '15 118 110',
      700: '17 94 89',
      800: '19 78 74',
      900: '19 42 41',
      950: '4 47 46',
    },
  },
  amber: {
    label: 'Oltin',
    labels: { uz: 'Oltin', ru: 'Янтарный', en: 'Amber' },
    swatch: '#d97706',
    shades: {
      50: '255 251 235',
      100: '254 243 199',
      200: '253 230 138',
      300: '252 211 77',
      400: '251 191 36',
      500: '217 119 6',
      600: '180 83 9',
      700: '146 64 14',
      800: '120 53 15',
      900: '69 26 3',
      950: '45 15 2',
    },
  },
  slate: {
    label: 'Grafit',
    labels: { uz: 'Grafit', ru: 'Графитовый', en: 'Slate' },
    swatch: '#475569',
    shades: {
      50: '248 250 252',
      100: '241 245 249',
      200: '226 232 240',
      300: '203 213 225',
      400: '148 163 184',
      500: '100 116 139',
      600: '71 85 105',
      700: '51 65 85',
      800: '30 41 59',
      900: '15 23 42',
      950: '2 6 23',
    },
  },
}

const LEGACY_MIGRATION = {
  sky: 'blue',
  indigo: 'blue',
  ocean: 'teal',
  cyan: 'teal',
  green: 'emerald',
  mint: 'emerald',
  lime: 'emerald',
  red: 'rose',
  coral: 'rose',
  pink: 'rose',
  berry: 'rose',
  magenta: 'purple',
  violet: 'purple',
  lavender: 'purple',
  yellow: 'amber',
  copper: 'orange',
}

const STORAGE_KEY = 'qulay_accent'
const DARK_STORAGE_KEY = 'qulay_dark'

function resolveAccent(raw) {
  if (!raw) return 'blue'
  if (ACCENT_PRESETS[raw]) return raw
  if (LEGACY_MIGRATION[raw]) return LEGACY_MIGRATION[raw]
  return 'blue'
}

export const useThemeStore = defineStore('theme', {
  state: () => ({
    accent: resolveAccent(typeof localStorage !== 'undefined' ? localStorage.getItem(STORAGE_KEY) : null),
    isDark: typeof localStorage !== 'undefined' && localStorage.getItem(DARK_STORAGE_KEY) === 'true',
  }),

  actions: {
    applyAccent(name) {
      const safeName = resolveAccent(name)
      const preset = ACCENT_PRESETS[safeName] || ACCENT_PRESETS.blue
      if (typeof document === 'undefined') return
      const root = document.documentElement
      Object.entries(preset.shades).forEach(([shade, rgb]) => {
        root.style.setProperty(`--brand-${shade}`, rgb)
      })
    },

    setAccent(name) {
      const safeName = resolveAccent(name)
      this.accent = safeName
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, safeName)
      }
      this.applyAccent(safeName)
    },

    applyDark(isDark) {
      if (typeof document !== 'undefined') {
        document.documentElement.classList.toggle('dark', isDark)
      }
    },

    toggleDark() {
      this.isDark = !this.isDark
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(DARK_STORAGE_KEY, String(this.isDark))
      }
      this.applyDark(this.isDark)
    },

    init() {
      const saved = typeof localStorage !== 'undefined' ? localStorage.getItem(STORAGE_KEY) : null
      const valid = resolveAccent(saved)
      this.accent = valid
      if (saved !== valid && typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, valid)
      }
      this.applyAccent(this.accent)
      this.applyDark(this.isDark)
    },
  },
})
