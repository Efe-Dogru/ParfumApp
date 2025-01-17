<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

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
    <!-- Header -->
    <header class="border-b">
      <div class="container mx-auto px-4">
        <div class="flex h-16 items-center">
          <!-- Left: Logo -->
          <div class="w-1/4">
            <NuxtLink to="/" class="text-2xl font-bold">Parfum App</NuxtLink>
          </div>
          
          <!-- Middle: Navigation -->
          <nav class="flex-1 flex items-center justify-center space-x-8">
            <NuxtLink
              to="/"
              class="text-sm font-medium hover:text-primary"
            >
              Home
            </NuxtLink>
            <NuxtLink
              to="/browse"
              class="text-sm font-medium hover:text-primary"
            >
              Browse
            </NuxtLink>
            <NuxtLink
              to="/about"
              class="text-sm font-medium hover:text-primary"
            >
              About Us
            </NuxtLink>
          </nav>

          <!-- Right: Search and Dark Mode -->
          <div class="w-1/4 flex items-center justify-end space-x-4">
            <div class="relative search-container">
              <input
                v-model="searchQuery"
                @input="handleSearch"
                type="search"
                placeholder="Search..."
                class="w-64 px-4 py-2 rounded-lg bg-background border border-border focus:outline-none focus:ring-2 focus:ring-primary"
              />
              
              <!-- Search Dropdown -->
              <div v-if="isSearchOpen" class="absolute top-full left-0 w-[500px] mt-2 bg-background border border-border rounded-lg shadow-lg z-50">
                <!-- Loading State -->
                <div v-if="isLoading" class="p-4 text-center text-muted-foreground">
                  Loading...
                </div>

                <!-- No Results -->
                <div v-else-if="searchResults.length === 0 && searchQuery" class="p-4 text-center text-muted-foreground">
                  No results found for "{{ searchQuery }}"
                </div>

                <!-- Search Results -->
                <div v-else class="max-h-[400px] overflow-y-auto">
                  <NuxtLink
                    v-for="result in searchResults"
                    :key="result.id"
                    :to="`/perfume/${result.id}`"
                    class="flex items-center space-x-4 p-4 hover:bg-accent cursor-pointer border-b border-border last:border-b-0"
                  >
                    <div class="w-12 h-12 bg-gray-200 rounded-lg overflow-hidden">
                      <img 
                        :src="result.image_url" 
                        :alt="result.name"
                        class="w-full h-full object-cover"
                      />
                    </div>
                    <div>
                      <h3 class="font-medium">{{ result.name }}</h3>
                      <div class="text-sm text-muted-foreground">
                        {{ result.brand }} · {{ result.year }}
                      </div>
                    </div>
                  </NuxtLink>
                </div>
              </div>
            </div>
            
            <button
              @click="toggleDarkMode"
              class="rounded-full p-2 hover:bg-accent"
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
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main>
      <slot />
    </main>
  </div>
</template> 