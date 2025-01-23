<script setup lang="ts">
import { useApi } from '~/composables/useApi'
import type { Perfume } from '~/composables/useCommon'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const { searchPerfumes, getTypes, getFamilies, getConcentrations, getPerfumers, getCountries, getBrands } = useApi()
const perfumes = ref<Perfume[]>([])
const loading = ref(true)
const currentPage = ref(parseInt(route.query.page as string) || 1)
const itemsPerPage = 42 // 6 columns * 7 rows
const showAdvancedFilters = ref(false)
const advancedFiltersRef = ref<HTMLElement | null>(null)

// Filter states initialized from route query
const filters = reactive({
  q: (route.query.q as string) || '',
  gender: (route.query.gender as string) || '',
  category: (route.query.category as string) || '',
  brand: (route.query.brand as string) || '',
  country: (route.query.country as string) || '',
  type: (route.query.type as string) || '',
  family: (route.query.family as string) || '',
  concentration: (route.query.concentration as string) || '',
  perfumer: (route.query.perfumer as string) || ''
})

// Filter options
const genderOptions = ['Male', 'Female', 'Unisex']
const categoryOptions = ['Designer', 'Niche', 'Luxury']
const brandOptions = ref<string[]>([])
const countryOptions = ref<string[]>([])
const typeOptions = ref<string[]>([])
const familyOptions = ref<string[]>([])
const concentrationOptions = ref<string[]>([])
const perfumerOptions = ref<string[]>([])

// Fetch filter options
const fetchFilterOptions = async () => {
  try {
    const [typesRes, familiesRes, concentrationsRes, perfumersRes, countriesRes, brandsRes] = await Promise.all([
      getTypes(),
      getFamilies(),
      getConcentrations(),
      getPerfumers(),
      getCountries(),
      getBrands()
    ])
    
    typeOptions.value = typesRes.data.map((type: any) => type.name)
    familyOptions.value = familiesRes.data.map((family: any) => family.name)
    concentrationOptions.value = concentrationsRes.data.map((conc: any) => conc.name)
    perfumerOptions.value = perfumersRes.data.map((perfumer: any) => perfumer.name)
    countryOptions.value = countriesRes.data.map((country: any) => country.name)
    brandOptions.value = brandsRes.data.map((brand: any) => brand.name)
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

const fetchPerfumes = async (page: number) => {
  loading.value = true
  try {
    const response = await searchPerfumes({
      ...filters,
      page,
      limit: itemsPerPage
    })
    perfumes.value = response.data
    currentPage.value = page
    updateUrlQuery()
  } catch (error) {
    console.error('Error fetching perfumes:', error)
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
  if (perfumes.value.length === itemsPerPage) pages.add(current + 1)
  
  return Array.from(pages).sort((a, b) => a - b)
})

const showEllipsis = computed(() => {
  return visiblePages.value.some((page, index, arr) => {
    return arr[index + 1] && arr[index + 1] - page > 1
  })
})

const goToPage = (page: number) => {
  if (page !== currentPage.value && page > 0 && (perfumes.value.length === itemsPerPage || page < currentPage.value)) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
    fetchPerfumes(page)
  }
}

// Debounced search with URL update
let searchTimeout: NodeJS.Timeout
const handleSearch = (event: Event) => {
  const target = event.target as HTMLInputElement
  filters.q = target.value
  
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchPerfumes(1)
  }, 500)
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchPerfumes(1)
}

// Handle click outside for advanced filters
const handleClickOutside = (event: MouseEvent) => {
  if (
    showAdvancedFilters.value &&
    advancedFiltersRef.value &&
    !advancedFiltersRef.value.contains(event.target as Node) &&
    !(event.target as HTMLElement).closest('button')
  ) {
    showAdvancedFilters.value = false
  }
}

onMounted(async () => {
  await fetchFilterOptions()
  // Initial fetch using route query parameters
  fetchPerfumes(currentPage.value)
  window.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  clearTimeout(searchTimeout)
  window.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <div class="relative">
      <h1 class="text-2xl font-bold mb-4">Browse Perfumes</h1>
      
      <!-- Main Filters -->
      <div class="grid grid-cols-1 md:grid-cols-[1.5fr,1fr,1fr,1fr,1fr,auto] gap-4 mb-6">
        <!-- Search -->
        <div>
          <input
            v-model="filters.q"
            type="text"
            placeholder="Search perfumes..."
            @input="handleSearch"
            class="w-full px-4 py-2 rounded-lg bg-background border border-input hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
          />
        </div>

        <!-- Gender Filter -->
        <div class="relative select-wrapper">
          <select
            v-model="filters.gender"
            @change="handleFilterChange"
            class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
          >
            <option value="">Any Gender</option>
            <option v-for="gender in genderOptions" :key="gender" :value="gender">
              {{ gender }}
            </option>
          </select>
        </div>

        <!-- Category Filter -->
        <div class="relative select-wrapper">
          <select
            v-model="filters.category"
            @change="handleFilterChange"
            class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
          >
            <option value="">Any Category</option>
            <option v-for="category in categoryOptions" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>

        <!-- Brand Filter -->
        <div class="relative select-wrapper">
          <select
            v-model="filters.brand"
            @change="handleFilterChange"
            class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
          >
            <option value="">Any Brand</option>
            <option v-for="brand in brandOptions" :key="brand" :value="brand">
              {{ brand }}
            </option>
          </select>
        </div>

        <!-- Country Filter -->
        <div class="relative select-wrapper">
          <select
            v-model="filters.country"
            @change="handleFilterChange"
            class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
          >
            <option value="">Any Country</option>
            <option v-for="country in countryOptions" :key="country" :value="country">
              {{ country }}
            </option>
          </select>
        </div>

        <!-- Advanced Filters Toggle -->
        <button
          @click="showAdvancedFilters = !showAdvancedFilters"
          class="w-10 h-10 rounded-lg border border-input flex items-center justify-center hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
          :class="{ 'bg-accent': showAdvancedFilters }"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M3 6h18"/>
            <path d="M7 12h10"/>
            <path d="M10 18h4"/>
          </svg>
        </button>
      </div>

      <!-- Advanced Filters Panel -->
      <div
        v-if="showAdvancedFilters"
        ref="advancedFiltersRef"
        class="absolute right-0 z-50 w-full md:w-[600px] mt-2 p-6 bg-background border rounded-lg shadow-lg"
      >
        <div class="space-y-4">
          <h3 class="text-lg font-semibold mb-4">Advanced Filters</h3>
          
          <!-- Type Filter -->
          <div class="space-y-2">
            <label class="text-sm font-medium">Type</label>
            <div class="relative select-wrapper">
              <select
                v-model="filters.type"
                @change="handleFilterChange"
                class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
              >
                <option value="">Any Type</option>
                <option v-for="type in typeOptions" :key="type" :value="type">
                  {{ type }}
                </option>
              </select>
            </div>
          </div>

          <!-- Family Filter -->
          <div class="space-y-2">
            <label class="text-sm font-medium">Family</label>
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
          </div>

          <!-- Concentration Filter -->
          <div class="space-y-2">
            <label class="text-sm font-medium">Concentration</label>
            <div class="relative select-wrapper">
              <select
                v-model="filters.concentration"
                @change="handleFilterChange"
                class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
              >
                <option value="">Any Concentration</option>
                <option v-for="conc in concentrationOptions" :key="conc" :value="conc">
                  {{ conc }}
                </option>
              </select>
            </div>
          </div>

          <!-- Perfumer Filter -->
          <div class="space-y-2">
            <label class="text-sm font-medium">Perfumer</label>
            <div class="relative select-wrapper">
              <select
                v-model="filters.perfumer"
                @change="handleFilterChange"
                class="w-full px-4 py-2 rounded-lg bg-background border border-input appearance-none hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
              >
                <option value="">Any Perfumer</option>
                <option v-for="perfumer in perfumerOptions" :key="perfumer" :value="perfumer">
                  {{ perfumer }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
    </div>
    <div v-else>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <NuxtLink 
          v-for="perfume in perfumes" 
          :key="perfume.id" 
          :to="`/perfume/${perfume.id}`" 
          class="group border rounded-lg overflow-hidden hover:shadow-lg transition-shadow bg-card"
        >
          <div class="aspect-square w-full">
            <img 
            :src="`http://127.0.0.1:8000/static/${perfume.local_image_path?.replace('\\', '/')}`"                         
            :alt="perfume.name"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="p-2">
            <h2 class="text-sm font-medium group-hover:text-primary truncate font-mono">{{ perfume.name + ' ' + perfume.concentration?.name}}</h2>
            <p class="text-xs text-muted-foreground truncate">{{ perfume.brand?.name }}</p>
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
              :disabled="perfumes.length < itemsPerPage || loading"
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