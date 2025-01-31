<script setup lang="ts">
import { useApi } from '~/composables/useApi'
import type { Note } from '~/composables/useCommon'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const { getNotes, searchNotes, getNoteFamilies, getNoteMoods } = useApi()

interface Filters {
  q: string;
  family: string;
  mood: string;
}

const Notes = ref<Note[]>([])
const loading = ref(true)
const currentPage = ref(parseInt(route.query.page as string) || 1)
const itemsPerPage = 42 // 6 columns * 7 rows

// Filter states initialized from route query
const filters = reactive<Filters>({
  q: (route.query.q as string) || '',
  family: (route.query.family as string) || '',
  mood: (route.query.mood as string) || ''
})

// Filter options
const familyOptions = ref<string[]>([])
const moodOptions = ref<string[]>([])

// Add new computed property for active filters
const activeFilters = computed(() => {
  return Object.entries(filters)
    .filter(([_, value]) => value !== '')
    .map(([key, value]) => ({
      key,
      value,
      label: getFilterLabel(key as keyof Filters, value)
    }))
})

// Helper function to get readable labels for filters
const getFilterLabel = (key: keyof Filters, value: string) => {
  const labels: Record<keyof Filters, string> = {
    q: 'Search',
    family: 'Family',
    mood: 'Mood'
        }
  return `${labels[key]}: ${value}`
  }

// Function to remove a filter
const removeFilter = (key: keyof Filters) => {
  filters[key] = ''
  handleFilterChange()
}

// Fetch filter options
const fetchFilterOptions = async () => {
  try {
    const [familiesResponse, moodsResponse] = await Promise.all([
      getNoteFamilies(),
      getNoteMoods()
    ])
    familyOptions.value = familiesResponse.data.map((f: any) => f.name)
    moodOptions.value = moodsResponse.data.map((m: any) => m.name)
  } catch (error) {
    console.error('Error fetching filter options:', error)
  }
}

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
    const response = await getNotes({
      ...filters,
      page,
      limit: itemsPerPage
    })
    Notes.value = response.data
    currentPage.value = page
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
const handleSearch = async (event: Event) => {
  const target = event.target as HTMLInputElement
  filters.q = target.value

  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    currentPage.value = 1
    loading.value = true
    try {
      if (filters.q) {
        const response = await searchNotes(filters.q)
        Notes.value = response.data
      } else {
        // If search is empty, revert to normal notes listing
        await fetchNotes(1)
      }
    } catch (error) {
      console.error('Error searching notes:', error)
    } finally {
      loading.value = false
    }
  }, 500)
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchNotes(1)
}

onMounted(() => {
  fetchNotes(currentPage.value)
  fetchFilterOptions()
})

onUnmounted(() => {
  clearTimeout(searchTimeout)
})
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <div class="relative">
      <h1 class="text-2xl font-bold mb-4">Browse Notes</h1>
      
      <!-- Main Filters -->
      <div class="space-y-6">
        <!-- Search and Filters -->
        <div class="grid grid-cols-1 md:grid-cols-[1.5fr,1fr,1fr] gap-4">
          <!-- Search -->
          <div class="relative">
            <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-muted-foreground">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
              </svg>
            </div>
            <input
              v-model="filters.q"
              type="text"
        placeholder="Search notes..."
        @input="handleSearch"
              class="w-full pl-10 pr-4 py-2.5 rounded-lg bg-background border border-input hover:border-[#4A154B] dark:hover:border-white transition-all focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
      />
    </div>
    
          <!-- Family Filter -->
          <div class="relative select-wrapper">
            <select
              v-model="filters.family"
              @change="handleFilterChange"
              class="w-full px-4 py-2.5 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-all focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white cursor-pointer"
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
              class="w-full px-4 py-2.5 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-all focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white cursor-pointer"
            >
              <option value="">Any Mood</option>
              <option v-for="mood in moodOptions" :key="mood" :value="mood">
                {{ mood }}
              </option>
            </select>
          </div>
        </div>

        <!-- Active Filters Area -->
        <div class="min-h-[48px] transition-all">
          <!-- Active Filters -->
          <div v-if="activeFilters.length > 0" class="flex flex-wrap gap-2">
            <div
              v-for="filter in activeFilters"
              :key="filter.key"
              class="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-[#4A154B] text-white text-sm"
            >
              <span>{{ filter.label }}</span>
              <button
                @click="removeFilter(filter.key as keyof Filters)"
                class="hover:bg-white/20 rounded-full p-0.5 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
                </svg>
              </button>
            </div>
            <button
              @click="(Object.keys(filters) as Array<keyof Filters>).forEach(key => filters[key] = ''); handleFilterChange()"
              class="inline-flex items-center gap-1 px-3 py-1 rounded-full border border-[#4A154B] text-[#4A154B] hover:bg-[#4A154B] hover:text-white transition-colors text-sm"
            >
              Clear All
            </button>
          </div>
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
                :disabled="Notes.length < itemsPerPage || loading"
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
  width: 8px;
  height: 8px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  rotate: 45deg;
  pointer-events: none;
  opacity: 0.7;
}

.select-wrapper:hover::after {
  opacity: 1;
}
</style> 