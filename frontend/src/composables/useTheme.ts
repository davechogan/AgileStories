import { ref, watch } from 'vue'
import { useStorage } from '@vueuse/core'

export function useTheme() {
  const theme = useStorage('theme', 'light')
  const isDark = ref(theme.value === 'dark')

  watch(isDark, (value) => {
    theme.value = value ? 'dark' : 'light'
    document.documentElement.classList.toggle('dark', value)
  })

  return {
    isDark,
    toggleTheme: () => isDark.value = !isDark.value
  }
} 