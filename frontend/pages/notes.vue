<script setup lang="ts">
import { useApi } from '~/composables/useApi'
import type { Note } from '~/composables/useCommon'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const { getNotes, searchNotes } = useApi()
const Notes = ref<Note[]>([])
const loading = ref(true)
const currentPage = ref(parseInt(route.query.page as string) || 1)
const itemsPerPage = 42 // 6 columns * 7 rows
const searchQuery = ref((route.query.q as string) || '')

// Filter states initialized from route query
const filters = reactive({
  q: (route.query.q as string) || '',
  family: (route.query.family as string) || '',
  mood: (route.query.mood as string) || ''
})

// Filter options
const familyOptions = [
  'Floral', 'Woody', 'Fresh', 'Oriental', 'Aromatic', 'Citrus', 
  'Fruity', 'Green', 'Spicy', 'Sweet', 'Earthy', 'Musky'
]
const moodOptions = [
  'Romantic', 'Fresh', 'Energetic', 'Relaxing', 'Sensual', 
  'Mysterious', 'Elegant', 'Playful', 'Sophisticated', 'Cozy'
]

// Update URL with current state
const updateUrlQuery = () => {
  const query = {
    page: currentPage.value.toString(),
    ...Object.fromEntries(
      Object.entries(filters).filter(([_, value]) => value !== '')
    )
  }
  router.push({ query })
}

const fetchNotes = async (page: number) => {
  loading.value = true
  try {
    if (searchQuery.value) {
      const response = await searchNotes(searchQuery.value)
      Notes.value = response.data
    } else {
      const response = await getNotes({
        page,
        limit: itemsPerPage,
        family: filters.family,
        mood: filters.mood
      })
      Notes.value = response.data
    }
    updateUrlQuery()
  } catch (error) {
    console.error('Error fetching notes:', error)
  } finally {
    loading.value = false
  }
}

const visiblePages = computed(() => {
  const pages = new Set([1]) // Always include page 1
  const current = currentPage.value
  
  // Add current page and adjacent pages
  if (current > 1) pages.add(current - 1)
  pages.add(current)
  if (Notes.value.length === itemsPerPage) pages.add(current + 1)
  
  return Array.from(pages).sort((a, b) => a - b)
})

const showEllipsis = computed(() => {
  return visiblePages.value.some((page, index, arr) => {
    return arr[index + 1] && arr[index + 1] - page > 1
  })
})

const goToPage = (page: number) => {
  if (page !== currentPage.value && page > 0 && (Notes.value.length === itemsPerPage || page < currentPage.value)) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
    fetchNotes(page)
  }
}

// Debounced search
let searchTimeout: NodeJS.Timeout
const handleSearch = (event: Event) => {
  const target = event.target as HTMLInputElement
  filters.q = target.value
  searchQuery.value = target.value
  
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchNotes(1)
  }, 500)
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchNotes(1)
}

onMounted(() => {
  fetchNotes(currentPage.value)
})

onUnmounted(() => {
  clearTimeout(searchTimeout)
})
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-4">Browse Notes</h1>
    
    <!-- Main Filters -->
    <div class="grid grid-cols-1 md:grid-cols-[1.5fr,1fr,1fr] gap-4 mb-6">
      <!-- Search -->
      <div>
        <input
          v-model="filters.q"
          type="text"
          placeholder="Search notes..."
          @input="handleSearch"
          class="w-full px-4 py-2 rounded-lg bg-background border border-input hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
        />
      </div>

      <!-- Family Filter -->
      <div class="relative select-wrapper">
        <select
          v-model="filters.family"
          @change="handleFilterChange"
          class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
        >
          <option value="">Any Family</option>
          <option v-for="family in familyOptions" :key="family" :value="family">
            {{ family }}
          </option>
        </select>
      </div>

      <!-- Mood Filter -->
      <div class="relative select-wrapper">
        <select
          v-model="filters.mood"
          @change="handleFilterChange"
          class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
        >
          <option value="">Any Mood</option>
          <option v-for="mood in moodOptions" :key="mood" :value="mood">
            {{ mood }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
    </div>
    <div v-else>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <NuxtLink 
          v-for="note in Notes" 
          :key="note.id" 
          :to="`/note/${note.id}`" 
          class="group border rounded-lg overflow-hidden hover:shadow-lg transition-shadow bg-card"
        >
          <div class="aspect-square w-full">
            <img 
              :src="`http://127.0.0.1:8000/static/notes_images/${note.image_filename}`"
              :alt="note.name"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="p-2">
            <h2 class="text-sm font-medium group-hover:text-primary truncate font-mono">{{ note.name }}</h2>
            <p v-if="note.family" class="text-xs text-muted-foreground truncate">{{ note.family }}</p>
          </div>
        </NuxtLink>
      </div>

      <!-- Pagination -->
      <nav role="navigation" aria-label="pagination" class="mx-auto flex w-full justify-center mt-8">
        <ul class="flex flex-row items-center gap-1">
          <li>
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1 || loading"
              class="inline-flex h-10 items-center justify-center gap-1 pl-2.5 rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground"
              aria-label="Go to previous page"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                <path d="m15 18-6-6 6-6"/>
              </svg>
              <span>Previous</span>
            </button>
          </li>
          <li v-for="page in visiblePages" :key="page">
            <a
              href="#"
              @click.prevent="goToPage(page)"
              :class="[
                'inline-flex h-10 w-10 items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
                currentPage === page ? 'border border-input bg-background hover:bg-accent hover:text-accent-foreground' : 'hover:bg-accent hover:text-accent-foreground'
              ]"
              :aria-current="currentPage === page ? 'page' : undefined"
            >
              {{ page }}
            </a>
          </li>
          <li v-if="showEllipsis">
            <span aria-hidden class="flex h-9 w-9 items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                <circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>
              </svg>
              <span class="sr-only">More pages</span>
            </span>
          </li>
          <li>
            <button
              @click="goToPage(currentPage + 1)"
              :disabled="Notes.length === 0 || loading"
              class="inline-flex h-10 items-center justify-center gap-1 pr-2.5 rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground"
              aria-label="Go to next page"
            >
              <span>Next</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                <path d="m9 18 6-6-6-6"/>
              </svg>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<style scoped>
.select-wrapper {
  position: relative;
}

.select-wrapper::after {
  content: '';
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid currentColor;
  pointer-events: none;
}
</style> 