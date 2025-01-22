<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Home, User, Briefcase, Search } from 'lucide-vue-next'
import { useRoute } from 'vue-router'
import TubelightNavbar from '@/components/ui/TubelightNavbar.vue'
import FooterSection from '@/components/ui/FooterSection.vue'
import SearchInput from '@/components/ui/SearchInput.vue'

const route = useRoute()
const isIndexPage = computed(() => {
  const isIndex = route.path === '/' || route.path === ''
  return isIndex
})

interface Perfume {
  id: number
  name: string
  brand: string
  year: string
  image_url: string
}

const searchQuery = ref('')
const isSearchOpen = ref(false)
const searchResults = ref<Perfume[]>([])
const isLoading = ref(false)

const { searchPerfumes } = useApi()

const navItems = [
  { name: 'Home', url: '/', icon: Home },
  { name: 'Browse', url: '/browse', icon: Briefcase },
  // { name: 'Search', url: '/search', icon: Search },
  { name: 'Notes', url: '/notes', icon: User },
  { name: 'Feedback', url: '/feedback', icon: User },
  { name: 'About', url: '/about', icon: User },
]

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
      <TubelightNavbar :items="navItems" :is-index-page="isIndexPage" class="" />
    </div>

    <!-- Main content -->
    <main class="container mx-auto px-4 pt-8">
      <slot />
    </main>

    <!-- Footer -->
    <FooterSection />
  </div>
</template> 