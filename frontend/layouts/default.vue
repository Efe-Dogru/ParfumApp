<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Home, User, Briefcase, Search } from 'lucide-vue-next'
import TubelightNavbar from '@/components/ui/TubelightNavbar.vue'
import FooterSection from '@/components/ui/FooterSection.vue'

interface Perfume {
  id: number
  name: string
  brand: string
  year: string
  image_url: string
}

const isDark = ref(false)
const searchQuery = ref('')
const isSearchOpen = ref(false)
const searchResults = ref<Perfume[]>([])
const isLoading = ref(false)

const { searchPerfumes } = useApi()

const navItems = [
  { name: 'Home', url: '/', icon: Home },
  { name: 'Browse', url: '/browse', icon: Briefcase },
  { name: 'Search', url: '/search', icon: Search },
  { name: 'About', url: '/about', icon: User }
]

const toggleDarkMode = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark')
  localStorage.setItem('darkMode', isDark.value ? 'dark' : 'light')
}

const fetchSearchResults = async (query: string) => {
  if (!query) {
    searchResults.value = []
    return
  }
  
  try {
    isLoading.value = true
    const { data } = await searchPerfumes(query)
    searchResults.value = data
  } catch (error) {
    console.error('Search error:', error)
    searchResults.value = []
  } finally {
    isLoading.value = false
  }
}

// Debounced search
let searchTimeout: NodeJS.Timeout
const handleSearch = (event: Event) => {
  const target = event.target as HTMLInputElement
  searchQuery.value = target.value
  isSearchOpen.value = !!target.value
  
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchSearchResults(target.value)
  }, 500)
}

onMounted(() => {
  // Check for saved dark mode preference
  const savedMode = localStorage.getItem('darkMode')
  isDark.value = savedMode === 'dark'
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  }

  // Close search dropdown when clicking outside
  document.addEventListener('click', (e) => {
    const searchContainer = document.querySelector('.search-container')
    if (searchContainer && !searchContainer.contains(e.target as Node)) {
      isSearchOpen.value = false
    }
  })
})

// Cleanup
onUnmounted(() => {
  clearTimeout(searchTimeout)
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- Header with TubelightNavbar -->
    <div class="mb-16">
      <TubelightNavbar :items="navItems">
        <!-- Search Bar -->
        <div class="relative search-container mx-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Search perfumes..."
              v-model="searchQuery"
              @input="handleSearch"
              class="w-64 px-4 py-2 rounded-lg bg-background border border-input focus:outline-none focus:ring-2 focus:ring-ring"
            />
            <div v-if="isLoading" class="absolute right-3 top-2.5">
              <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
            </div>
          </div>
          
          <!-- Search Results Dropdown -->
          <div
            v-if="isSearchOpen && searchResults.length > 0"
            class="absolute z-50 w-full mt-2 bg-background border border-input rounded-lg shadow-lg"
          >
            <div class="max-h-96 overflow-y-auto">
              <NuxtLink
                v-for="result in searchResults"
                :key="result.id"
                :to="'/perfume/' + result.id"
                class="block px-4 py-2 hover:bg-accent cursor-pointer"
                @click="isSearchOpen = false"
              >
                <div class="flex items-center space-x-3">
                  <img
                    v-if="result.image_url"
                    :src="result.image_url"
                    :alt="result.name"
                    class="w-10 h-10 object-cover rounded"
                  />
                  <div>
                    <div class="font-medium">{{ result.name }}</div>
                    <div class="text-sm text-muted-foreground">{{ result.brand }} ({{ result.year }})</div>
                  </div>
                </div>
              </NuxtLink>
            </div>
          </div>
        </div>
      </TubelightNavbar>
    </div>

    <!-- Dark Mode Toggle -->
    <button
      @click="toggleDarkMode"
      class="fixed top-4 right-4 rounded-full p-2 hover:bg-accent z-50"
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
        class="w-6 h-6"
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
        class="w-6 h-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"
        />
      </svg>
    </button>

    <!-- Main content -->
    <main class="container mx-auto px-4 pt-8">
      <slot />
    </main>

    <!-- Footer -->
    <FooterSection />
  </div>
</template> 