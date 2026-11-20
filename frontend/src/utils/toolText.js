import { computed } from 'vue'
import { language } from '../i18n'

export function useToolText(dict) {
  return computed(() => {
    const lang = language.value
    return dict[lang] || dict.uz || {}
  })
}
