import { ref } from 'vue'

// Create a shared state
const isDark = ref(false)

export const useTheme = () => {
  const toggleDarkMode = () => {
    isDark.value = !isDark.value
    document.documentElement.classList.toggle('dark')
    localStorage.setItem('darkMode', isDark.value ? 'dark' : 'light')
  }

  const initTheme = () => {
    const savedMode = localStorage.getItem('darkMode')
    isDark.value = savedMode === 'dark'
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return {
    isDark,
    toggleDarkMode,
    initTheme
  }
} 