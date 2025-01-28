<!-- components/NavBar.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import type { LucideIcon } from 'lucide-vue-next'
import { useTheme } from '#imports'

interface NavItem {
  name: string
  url: string
  icon: LucideIcon
}

interface Props {
  items: NavItem[]
  className?: string
}

const props = defineProps<Props>()
const route = useRoute()
const isScrolled = ref(false)
const { isDark, toggleDarkMode } = useTheme()

// Compute active tab based on current route
const activeTab = computed(() => {
  const currentPath = route.path
  
  // Handle perfume detail pages
  if (currentPath.startsWith('/perfume/')) {
    return 'Perfumes'
  }

  const activeItem = props.items.find(item => {
    // Exact match for home page
    if (item.url === '/') {
      return currentPath === '/'
    }
    // For other pages, check if the current path starts with the item's URL
    return currentPath.startsWith(item.url)
  })

  return activeItem ? activeItem.name : props.items[0].name
})

const isMobile = ref(false)

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div
    :class="[
      'fixed sm:top-0 left-1/2 -translate-x-1/2 z-50 mb-6 sm:pt-6 mx-auto container',
      className
    ]"
  >
    <div 
      :class="[
        'flex items-center gap-3 rounded-xl p-3 w-full relative transition-all duration-300',
        isScrolled ? 'bg-background/5 border-border backdrop-blur-xl shadow-lg' : ''
      ]"
    >
      <!-- Center navigation links -->
      <div class="flex items-center gap-3 mx-auto">
        <NuxtLink
          v-for="item in items"
          :key="item.name"
          :to="item.url"
          :class="[
            'relative cursor-pointer text-m font-semibold px-6 py-2 rounded-xl transition-all duration-300',
            'text-foreground/80 hover:text-primary',
            { 'bg-muted text-primary': activeTab === item.name }
          ]"
        >
          <span class="hidden md:inline">{{ item.name }}</span>
          <span class="md:hidden">
            <component :is="item.icon" :size="18" :stroke-width="2.5" />
          </span>
        </NuxtLink>
      </div>

      <!-- Right side content -->
      <div class="flex items-center gap-3 absolute right-3">
        <!-- Add slot for additional content like search bar -->
        <slot></slot>
        
        <!-- Dark mode toggle button -->
        <button
          @click="toggleDarkMode"
          class="rounded-xl p-2 hover:bg-accent transition-colors"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          <!-- Sun icon for light mode -->
          <svg
            v-if="isDark"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-5 h-5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
            />
          </svg>
          <!-- Moon icon for dark mode -->
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-5 h-5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.router-link-active {
  @apply text-primary;
}
</style>