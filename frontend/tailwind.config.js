/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Primary colors
        primary: '#4A154B', // Deep plum
        secondary: '#FFB347', // Warm gold/amber
        accent: '#FFF8E7', // Soft cream
        
        // Semantic colors
        background: {
          DEFAULT: '#FFFFFF',
          dark: '#1A1A1A',
        },
        foreground: {
          DEFAULT: '#1A1A1A',
          dark: '#FFFFFF',
        },
        muted: {
          DEFAULT: '#6B7280',
          foreground: '#9CA3AF',
        },
        input: {
          DEFAULT: '#E5E7EB',
          dark: '#374151',
        },
        ring: {
          DEFAULT: '#4A154B',
          dark: '#FFB347',
        },
      },
    },
  },
  plugins: [],
} 