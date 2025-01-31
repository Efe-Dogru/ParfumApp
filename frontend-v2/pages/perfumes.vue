<script setup lang="ts">
import { usePerfumes } from '@/composables/usePerfumes'
import type { Perfume, Brand, Concentration } from '~/types/perfume'
import { Button } from '@/components/ui/button'
import {
  Pagination,
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
} from '@/components/ui/pagination'
import { useBucketImages } from '@/composables/useShared'
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { Skeleton } from '@/components/ui/skeleton'
import { NuxtLink } from '#components'
import Input from '@/components/ui/input/Input.vue'
import { XIcon, FilterIcon, SlidersHorizontal } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog'

// Define the directive at the top
const vObserveVisibility = {
  mounted: (el: HTMLElement, { value }: { value: (el: HTMLElement) => void }) => {
    value(el)
  }
}

const { getPerfumes, searchPerfume, getBrands, getConcentrations } = usePerfumes()
const currentPage = ref(1)
const searchQuery = ref('')
const searchTimeout = ref<NodeJS.Timeout | null>(null)
const itemsPerPage = 42
const totalItems = ref(0)
const perfumes = ref<Perfume[] | null>(null)
const imageUrls = ref<Record<string, string>>({})
const loading = ref(true)
const observer = ref<IntersectionObserver | null>(null)

// Add gender filter data
const selectedGender = ref('')
const selectedBrand = ref('')
const selectedConcentration = ref('')
const selectedSeason = ref('')
const selectedYear = ref('')

const genderOptions = [
  { value: 'all', label: 'All Genders' },
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'unisex', label: 'Unisex' },
]

const brandOptions = ref([
  { value: 'all', label: 'All Brands' }
])

const concentrationOptions = ref([
  { value: 'all', label: 'All Concentrations' }
])

const seasonOptions = [
  { value: 'all', label: 'All Seasons' },
  { value: 'spring', label: 'Spring' },
  { value: 'summer', label: 'Summer' },
  { value: 'fall', label: 'Fall' },
  { value: 'winter', label: 'Winter' },
]

const yearOptions = [
  { value: 'all', label: 'All Years' },
  { value: '2024', label: '2024' },
  { value: '2023', label: '2023' },
  { value: '2022', label: '2022' },
  { value: '2021', label: '2021' },
]

const loadImage = async (perfume: Perfume) => {
  if (perfume.local_image_path && !imageUrls.value[perfume.local_image_path]) {
    try {
      imageUrls.value[perfume.local_image_path] = await useBucketImages('perfume_images', perfume.local_image_path)
    } catch (error) {
      console.error('Error loading image:', error)
    }
  }
}

const setupIntersectionObserver = () => {
  if (process.client) {
    observer.value = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const perfumeId = entry.target.getAttribute('data-perfume-id')
          const perfume = perfumes.value?.find(p => p.id.toString() === perfumeId)
          if (perfume) {
            loadImage(perfume)
            observer.value?.unobserve(entry.target)
          }
        }
      })
    }, {
      root: null,
      rootMargin: '50px',
      threshold: 0.1
    })
  }
}

const observeImage = (el: HTMLElement) => {
  if (observer.value && process.client) {
    observer.value.observe(el)
  }
}

onMounted(() => {
  setupIntersectionObserver()
})

onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
})

const fetchPerfumes = async (page: number) => {
  loading.value = true
  try {
    const filters = {
      gender: selectedGender.value,
      brand_id: selectedBrand.value,
      concentration_id: selectedConcentration.value,
      season: selectedSeason.value
    }
    const result = await getPerfumes(page, itemsPerPage, filters)
    perfumes.value = result.data
    totalItems.value = (result.count / itemsPerPage) * 10
  } catch (error) {
    console.error('Error fetching perfumes:', error)
  } finally {
    loading.value = false
  }
}

// Function to fetch and set brand options
const fetchBrandOptions = async () => {
  try {
    const brands = await getBrands()
    brandOptions.value = [
      { value: 'all', label: 'All Brands' },
      ...brands.map((brand: Brand) => ({
        value: brand.id.toString(),
        label: brand.name
      }))
    ]
  } catch (error) {
    console.error('Error fetching brands:', error)
  }
}

// Function to fetch and set concentration options
const fetchConcentrationOptions = async () => {
  try {
    const concentrations = await getConcentrations()
    concentrationOptions.value = [
      { value: 'all', label: 'All Concentrations' },
      ...concentrations.map((concentration: Concentration) => ({
        value: concentration.id.toString(),
        label: concentration.name
      }))
    ]
  } catch (error) {
    console.error('Error fetching concentrations:', error)
  }
}

// Update onMounted to include concentration fetching
onMounted(async () => {
  await Promise.all([
    fetchPerfumes(currentPage.value),
    fetchBrandOptions(),
    fetchConcentrationOptions()
  ])
})

watch(currentPage, async (newPage) => {
  await fetchPerfumes(newPage)
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

const handleSearch = async (event: Event) => {
  const query = (event.target as HTMLInputElement).value
  searchQuery.value = query

  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  searchTimeout.value = setTimeout(async () => {
    loading.value = true
    try {
      const filters = {
        gender: selectedGender.value,
        brand_id: selectedBrand.value,
        concentration_id: selectedConcentration.value, 
        season: selectedSeason.value
      }
      if (query.trim()) {
        const result = await searchPerfume(query, filters)
        perfumes.value = result.data
        totalItems.value = result.data?.length || 0
      } else {
        await fetchPerfumes(currentPage.value)
      }
    } catch (error) {
      console.error('Error searching perfumes:', error)
    } finally {
      loading.value = false
    }
  }, 300)
}

// Add watchers for filter changes
watch([selectedGender, selectedBrand, selectedConcentration, selectedSeason], async () => {
  currentPage.value = 1  // Always reset to page 1
  await fetchPerfumes(1) // Immediately fetch with new filters
})

// Add these refs for advanced filters
const showAdvancedFilters = ref(false)
const selectedType = ref('all')
const selectedFamily = ref('all')
const selectedCountry = ref('all')
const selectedReleaseYear = ref('all')
const selectedSillage = ref('all')
const selectedPerfumer = ref('all')

// Add these options for advanced filters
const typeOptions = [
  { value: 'all', label: 'All Types' },
  { value: 'designer', label: 'Designer' },
  { value: 'niche', label: 'Niche' },
  { value: 'celebrity', label: 'Celebrity' },
]

const familyOptions = [
  { value: 'all', label: 'All Families' },
  { value: 'floral', label: 'Floral' },
  { value: 'oriental', label: 'Oriental' },
  { value: 'woody', label: 'Woody' },
  { value: 'fresh', label: 'Fresh' },
  { value: 'aromatic', label: 'Aromatic' },
]

const countryOptions = [
  { value: 'all', label: 'All Countries' },
  { value: 'france', label: 'France' },
  { value: 'italy', label: 'Italy' },
  { value: 'usa', label: 'United States' },
  { value: 'uk', label: 'United Kingdom' },
]

const sillageOptions = [
  { value: 'all', label: 'All Sillage' },
  { value: 'intimate', label: 'Intimate' },
  { value: 'moderate', label: 'Moderate' },
  { value: 'strong', label: 'Strong' },
  { value: 'enormous', label: 'Enormous' },
]

const perfumerOptions = [
  { value: 'all', label: 'All Perfumers' },
  { value: 'francis-kurkdjian', label: 'Francis Kurkdjian' },
  { value: 'olivier-polge', label: 'Olivier Polge' },
  { value: 'christine-nagel', label: 'Christine Nagel' },
  { value: 'alberto-morillas', label: 'Alberto Morillas' },
]

const releaseYearOptions = [
  { value: 'all', label: 'All Years' },
  ...Array.from({ length: 24 }, (_, i) => ({
    value: `${2024 - i}`,
    label: `${2024 - i}`
  }))
]

// Add computed property for active filters
const activeFilters = computed(() => {
  const filters = []
  
  if (selectedGender.value && selectedGender.value !== 'all') {
    filters.push({
      type: 'gender',
      value: selectedGender.value,
      label: genderOptions.find(opt => opt.value === selectedGender.value)?.label
    })
  }
  
  if (selectedConcentration.value && selectedConcentration.value !== 'all') {
    filters.push({
      type: 'concentration',
      value: selectedConcentration.value,
      label: concentrationOptions.value.find(opt => opt.value === selectedConcentration.value)?.label
    })
  }
  
  if (selectedBrand.value && selectedBrand.value !== 'all') {
    filters.push({
      type: 'brand',
      value: selectedBrand.value,
      label: brandOptions.value.find(opt => opt.value === selectedBrand.value)?.label
    })
  }
  
  if (selectedSeason.value && selectedSeason.value !== 'all') {
    filters.push({
      type: 'season',
      value: selectedSeason.value,
      label: seasonOptions.find(opt => opt.value === selectedSeason.value)?.label
    })
  }

  // Add advanced filters
  if (selectedType.value && selectedType.value !== 'all') {
    filters.push({
      type: 'type',
      value: selectedType.value,
      label: typeOptions.find(opt => opt.value === selectedType.value)?.label
    })
  }

  if (selectedFamily.value && selectedFamily.value !== 'all') {
    filters.push({
      type: 'family',
      value: selectedFamily.value,
      label: familyOptions.find(opt => opt.value === selectedFamily.value)?.label
    })
  }

  if (selectedCountry.value && selectedCountry.value !== 'all') {
    filters.push({
      type: 'country',
      value: selectedCountry.value,
      label: countryOptions.find(opt => opt.value === selectedCountry.value)?.label
    })
  }

  if (selectedReleaseYear.value && selectedReleaseYear.value !== 'all') {
    filters.push({
      type: 'release_year',
      value: selectedReleaseYear.value,
      label: `Year: ${selectedReleaseYear.value}`
    })
  }

  if (selectedSillage.value && selectedSillage.value !== 'all') {
    filters.push({
      type: 'sillage',
      value: selectedSillage.value,
      label: sillageOptions.find(opt => opt.value === selectedSillage.value)?.label
    })
  }

  if (selectedPerfumer.value && selectedPerfumer.value !== 'all') {
    filters.push({
      type: 'perfumer',
      value: selectedPerfumer.value,
      label: perfumerOptions.find(opt => opt.value === selectedPerfumer.value)?.label
    })
  }

  return filters
})

const removeFilter = (filterType: string) => {
  switch (filterType) {
    case 'gender':
      selectedGender.value = 'all'
      break
    case 'concentration':
      selectedConcentration.value = 'all'
      break
    case 'brand':
      selectedBrand.value = 'all'
      break
    case 'season':
      selectedSeason.value = 'all'
      break
    case 'type':
      selectedType.value = 'all'
      break
    case 'family':
      selectedFamily.value = 'all'
      break
    case 'country':
      selectedCountry.value = 'all'
      break
    case 'release_year':
      selectedReleaseYear.value = 'all'
      break
    case 'sillage':
      selectedSillage.value = 'all'
      break
    case 'perfumer':
      selectedPerfumer.value = 'all'
      break
  }
}

const clearAllFilters = () => {
  selectedGender.value = 'all'
  selectedBrand.value = 'all'
  selectedConcentration.value = 'all'
  selectedSeason.value = 'all'
  selectedYear.value = 'all'
  searchQuery.value = ''
  // Clear advanced filters
  selectedType.value = 'all'
  selectedFamily.value = 'all'
  selectedCountry.value = 'all'
  selectedReleaseYear.value = 'all'
  selectedSillage.value = 'all'
  selectedPerfumer.value = 'all'
}
</script>

<template>
    <div class="container mx-auto px-4">
      <!-- Combined search and filters section -->
      <div class="space-y-4">
        <div class="flex flex-wrap items-center gap-4">
          <Input 
            v-model="searchQuery"
            placeholder="Search perfumes..."
            @input="handleSearch"
            class="w-full max-w-xs"
          />
          <CustomComboBox
            v-model="selectedGender"
            :items="genderOptions"
            placeholder="Gender"
            search-placeholder="Search genders..."
          />
          <CustomComboBox
            v-model="selectedConcentration"  
            :items="concentrationOptions"  
            placeholder="Concentration"
            search-placeholder="Search concentration..."
          />
          <CustomComboBox
            v-model="selectedBrand"
            :items="brandOptions"
            placeholder="Brand"
            search-placeholder="Search brands..."
          />
          <CustomComboBox
            v-model="selectedSeason"
            :items="seasonOptions"
            placeholder="Season"
            search-placeholder="Search seasons..."
          />
          <Dialog v-model:open="showAdvancedFilters">
            <DialogTrigger as-child>
              <Button variant="outline" class="gap-2">
                <SlidersHorizontal class="h-4 w-4" />
                Advanced Filters
              </Button>
            </DialogTrigger>
            <DialogContent class="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle>Advanced Filters</DialogTitle>
                <DialogDescription>
                  Apply additional filters to refine your search
                </DialogDescription>
              </DialogHeader>
              <div class="grid gap-4 py-4">
                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-2">
                    <CustomComboBox
                      v-model="selectedType"
                      :items="typeOptions"
                      placeholder="Select type"
                    />
                  </div>
                  <div class="space-y-2">
                    <CustomComboBox
                      v-model="selectedFamily"
                      :items="familyOptions"
                      placeholder="Select family"
                    />
                  </div>
                  <div class="space-y-2">
                    <CustomComboBox
                      v-model="selectedCountry"
                      :items="countryOptions"
                      placeholder="Select country"
                    />
                  </div>
                  <div class="space-y-2">
                    <CustomComboBox
                      v-model="selectedReleaseYear"
                      :items="releaseYearOptions"
                      placeholder="Select year"
                    />
                  </div>
                  <div class="space-y-2">
                    <CustomComboBox
                      v-model="selectedSillage"
                      :items="sillageOptions"
                      placeholder="Select sillage"
                    />
                  </div>
                  <div class="space-y-2">
                    <CustomComboBox
                      v-model="selectedPerfumer"
                      :items="perfumerOptions"
                      placeholder="Select perfumer"
                    />
                  </div>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Active filters and Clear All -->
        <div v-if="activeFilters.length > 0 || searchQuery" class="flex flex-wrap items-center gap-4">
          <div class="flex flex-wrap gap-2">
            <Badge 
              variant="destructive"
              class="flex items-center gap-1 px-3 py-1 cursor-pointer"
              @click="clearAllFilters"
            >
              Clear All
              <XIcon class="h-3 w-3" />
            </Badge>
            <Badge 
              v-for="filter in activeFilters" 
              :key="filter.type"
              variant="secondary"
              class="flex items-center gap-1 px-3 py-1"
            >
              {{ filter.label }}
              <button 
                @click="removeFilter(filter.type)"
                class="ml-1 hover:text-destructive"
              >
                <XIcon class="h-3 w-3" />
              </button>
            </Badge>
            <Badge
              v-if="searchQuery"
              variant="secondary"
              class="flex items-center gap-1 px-3 py-1"
            >
              Search: {{ searchQuery }}
              <button 
                @click="searchQuery = ''"
                class="ml-1 hover:text-destructive"
              >
                <XIcon class="h-3 w-3" />
              </button>
            </Badge>
          </div>
        </div>

        <!-- Filter icon separator -->
        <div class="flex items-center gap-2 py-4">
          <FilterIcon class="h-5 w-5 text-muted-foreground" />
          <div class="h-px flex-1 bg-border"></div>
        </div>
      </div>
      
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <template v-if="loading">
          <div v-for="n in itemsPerPage" :key="n" class="flex-none space-y-3">
            <div class="relative overflow-hidden rounded-lg aspect-square">
              <Skeleton class="w-full h-full absolute inset-0" />
            </div>
            <div class="space-y-2">
              <Skeleton class="h-5 w-3/4" />
              <Skeleton class="h-4 w-1/2" />
            </div>
          </div>
        </template>
        <template v-else>
          <NuxtLink 
            v-for="perfume in perfumes || []" 
            :key="perfume.id" 
            :to="`/perfume/${perfume.id}`"
            class="flex-none group hover:opacity-95 transition-opacity"
          >
            <div 
              :data-perfume-id="perfume.id"
              v-observe-visibility="observeImage"
              class="relative overflow-hidden rounded-lg aspect-square mb-3"
            >
              <img 
                v-if="imageUrls[perfume.local_image_path]"
                :src="imageUrls[perfume.local_image_path]" 
                :alt="perfume.name"
                class="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
              />
              <div v-else class="w-full h-full flex items-center justify-center">
                <Skeleton class="w-full h-full" />
              </div>
            </div>
            <h3 class="font-medium text-foreground">{{ perfume.brands.name }}</h3>
            <p class="text-sm text-muted-foreground">{{ perfume.name }}</p>
          </NuxtLink>
        </template>
      </div>

      <div class="flex justify-center mt-6">
        <Pagination 
          v-slot="{ page }" 
          :total="totalItems"
          :per-page="itemsPerPage"
          :sibling-count="0" 
          show-edges 
          :default-page="1"
          :page="currentPage"
          @update:page="currentPage = $event"
        >
          <PaginationList v-slot="{ items }" class="flex items-center gap-1">
            <PaginationFirst class="w-9 h-9 p-0" />
            <PaginationPrev class="w-9 h-9 p-0" />

            <template v-for="(item, index) in items">
              <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
                <Button class="w-9 h-9 p-0" :variant="item.value === page ? 'default' : 'outline'">
                  {{ item.value }}
                </Button>
              </PaginationListItem>
              <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>

            <PaginationNext class="w-9 h-9 p-0" />
            <PaginationLast class="w-9 h-9 p-0" />
          </PaginationList>
        </Pagination>
      </div>
    </div>
</template>

<style scoped>
.dialog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
</style>