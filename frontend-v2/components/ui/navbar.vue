<!-- components/NavBar.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import type { LucideIcon } from 'lucide-vue-next'
import { useTheme } from '#imports'
import { Menu, Sun, Moon, X } from 'lucide-vue-next'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '~/components/ui/dropdown-menu'
import { Button } from '~/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '~/components/ui/sheet'

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
const isVisible = ref(true)
const lastScrollY = ref(0)
const { isDark, toggleDarkMode } = useTheme()
const selectedLanguage = ref({ flag: '🇺🇸', name: 'English', code: 'en' })
const languages = [
  { flag: '🇺🇸', name: 'English', code: 'en' },
  { flag: '🇧🇪', name: 'Nederlands', code: 'nl' },
]
const isOpen = ref(false)

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
  const currentScrollY = window.scrollY
  
  // Update background visibility
  isScrolled.value = currentScrollY > 20
  
  // Determine if navbar should be visible
  // Don't hide navbar when at the top of the page
  if (currentScrollY < 20) {
    isVisible.value = true
  } else {
    // Hide on scroll down, show on scroll up
    isVisible.value = currentScrollY < lastScrollY.value
  }
  
  lastScrollY.value = currentScrollY
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
  <div :class="[
    'w-full flex justify-center fixed top-0 left-0 right-0 z-50 p-2 sm:p-4 transition-transform duration-300',
    !isVisible && 'transform -translate-y-full'
  ]">
    <header :class="[
      'w-full max-w-7xl rounded-lg sm:rounded-2xl transition-all duration-300',
      isScrolled ? 'bg-background/20 backdrop-blur-xl border border-card/20' : ''
    ]">
      <nav class="flex items-center justify-between px-4 py-2 sm:px-8 sm:py-4">
        <!-- Logo -->
        <NuxtLink to="/" class="text-xl font-bold">ParfumApp</NuxtLink>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center gap-6">
          <NuxtLink
            v-for="item in items"
            :key="item.name"
            :to="item.url"
            class="text-sm text-muted-foreground dark:text-white transition-colors hover:text-primary dark:hover:text-primary"
          >
            {{ item.name }}
          </NuxtLink>
        </div>

        <!-- Right side buttons -->
        <div class="flex items-center gap-1">
          <!-- Theme toggle -->
          <Button variant="outline" size="icon" class="h-9 w-9" @click="toggleDarkMode" aria-label="Toggle theme">
            <Sun class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span class="sr-only">Toggle dark mode</span>
          </Button>

          <!-- Language selector -->
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="outline" class="w-fit md:min-w-[127px]">
                <span class="text-lg align-middle mr-1">{{ selectedLanguage.flag }}</span>
                <span class="align-middle hidden md:inline mr-1">{{ selectedLanguage.name }}</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem v-for="lang in languages" :key="lang.code" @click="selectedLanguage = lang">
                <span class="text-lg mr-2">{{ lang.flag }}</span>
                <span>{{ lang.name }}</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <!-- Mobile menu button -->
          <Sheet v-model:open="isOpen">
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" class="h-9 w-9 md:hidden" aria-label="menu-button">
                <Menu class="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" class="w-[300px] sm:w-[400px]">
              <SheetHeader>
                <SheetTitle>Menu</SheetTitle>
              </SheetHeader>
              <div class="flex flex-col gap-4 mt-6">
                <NuxtLink
                  v-for="item in items"
                  :key="item.name"
                  :to="item.url"
                  class="text-lg font-medium text-muted-foreground dark:text-white transition-colors hover:text-primary dark:hover:text-primary"
                  @click="isOpen = false"
                >
                  {{ item.name }}
                </NuxtLink>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </nav>
    </header>
  </div>
</template>

<style scoped>
.router-link-active {
  @apply text-primary;
}
</style>