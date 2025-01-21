<!-- components/NavBar.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import type { LucideIcon } from 'lucide-vue-next'

interface NavItem {
  name: string
  url: string
  icon: LucideIcon
}

interface Props {
  items: NavItem[]
  className?: string
  isIndexPage: boolean
}

const props = defineProps<Props>()
const route = useRoute()
const isScrolled = ref(false)
const isMobile = ref(false)

// Check if we're in browser environment
const isBrowser = typeof window !== 'undefined'

// Define handleScroll first
const handleScroll = () => {
  if (!isBrowser) return
  if (props.isIndexPage) {
    isScrolled.value = window.scrollY > 20
  }
}

const handleResize = () => {
  if (!isBrowser) return
  isMobile.value = window.innerWidth < 768
}

// Then use it in the watcher
watch(
  () => route.path,
  () => {
    if (!isBrowser) return
    
    if (!props.isIndexPage) {
      isScrolled.value = false
      window.removeEventListener('scroll', handleScroll)
    } else {
      handleScroll()
      window.addEventListener('scroll', handleScroll)
    }
  },
  { immediate: true }
)

// Compute active tab based on current route
const activeTab = computed(() => {
  const currentPath = route.path
  const activeItem = props.items.find(item => item.url === currentPath)
  return activeItem ? activeItem.name : props.items[0].name
})

onMounted(() => {
  if (!isBrowser) return
  
  handleResize()
  window.addEventListener('resize', handleResize)
  
  if (props.isIndexPage) {
    handleScroll()
    window.addEventListener('scroll', handleScroll)
  }
})

onUnmounted(() => {
  if (!isBrowser) return
  
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50',
      props.isIndexPage
        ? isScrolled
          ? 'bg-background/95 border-b border-border backdrop-blur shadow-sm'
          : 'bg-transparent'
        : 'bg-background border-b border-border'
    ]"
  >
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center space-x-2">
          <span class="text-xl font-bold !text-[#4A154B] dark:!text-white">Parfum</span>
        </NuxtLink>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-1">
          <NuxtLink
            v-for="item in items"
            :key="item.name"
            :to="item.url"
            :class="[
              'px-4 py-2 rounded-md text-sm font-medium relative after:transition-all after:duration-300 after:ease-in-out',
              activeTab === item.name
                ? '!text-[#4A154B] dark:!text-white after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-[#4A154B] dark:after:bg-white after:transform after:scale-x-100'
                : 'text-foreground/80 hover:!text-[#4A154B] dark:hover:!text-white hover:bg-muted/50 after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-[#4A154B] dark:after:bg-white after:transform after:scale-x-0'
            ]"
          >
            {{ item.name }}
          </NuxtLink>
        </div>

        <!-- Right Side Buttons -->
        <div class="flex items-center">
          <!-- Search slot -->
          <div class="mr-6">
            <slot></slot>
          </div>

          <!-- Theme toggle button -->
          <div class="flex items-center justify-center w-9 h-9">
            <slot name="theme-toggle"></slot>
          </div>
        </div>

        <!-- Mobile Menu Button -->
        <button
          class="md:hidden inline-flex items-center justify-center rounded-md text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 w-9"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="4" x2="20" y1="12" y2="12" />
            <line x1="4" x2="20" y1="6" y2="6" />
            <line x1="4" x2="20" y1="18" y2="18" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu (Hidden by default) -->
    <div
      v-if="isMobile"
      class="md:hidden"
      :class="[props.isIndexPage && isScrolled ? 'border-b border-border' : '']"
    >
      <div class="px-2 pt-2 pb-3 space-y-1">
        <NuxtLink
          v-for="item in items"
          :key="item.name"
          :to="item.url"
          :class="[
            'block px-3 py-2 rounded-md text-base font-medium relative after:transition-all after:duration-300 after:ease-in-out',
            activeTab === item.name
              ? '!text-[#4A154B] dark:!text-white bg-primary/5 after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-[#4A154B] dark:after:bg-white after:transform after:scale-x-100'
              : 'text-foreground/80 hover:!text-[#4A154B] dark:hover:!text-white hover:bg-muted/50 after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-[#4A154B] dark:after:bg-white after:transform after:scale-x-0'
          ]"
        >
          <span class="flex items-center space-x-2">
            <component :is="item.icon" :size="18" :stroke-width="2" />
            <span>{{ item.name }}</span>
          </span>
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.router-link-active {
  @apply text-primary;
}
</style>