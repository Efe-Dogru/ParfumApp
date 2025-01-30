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
const selectedCategory = ref('')
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

const categoryOptions = ref([
  { value: 'all', label: 'All Categories' }
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
      concentration_id: selectedCategory.value,
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
    categoryOptions.value = [
      { value: 'all', label: 'All Categories' },
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
        concentration_id: selectedCategory.value,
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
watch([selectedGender, selectedBrand, selectedCategory, selectedSeason], async () => {
  currentPage.value = 1  // Always reset to page 1
  await fetchPerfumes(1) // Immediately fetch with new filters
})
</script>

<template>
    <div class="container mx-auto px-4">
      <!-- Combined search and filters section -->
      <div class="flex flex-wrap items-center gap-4 mb-4">
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
          v-model="selectedCategory"
          :items="categoryOptions"
          placeholder="Category"
          search-placeholder="Search categories..."
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
          :sibling-count="1" 
          show-edges 
          :default-page="1"
          :page="currentPage"
          @update:page="currentPage = $event"
        >
          <PaginationList v-slot="{ items }" class="flex items-center gap-1">
            <PaginationFirst />
            <PaginationPrev />

            <template v-for="(item, index) in items">
              <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
                <Button class="w-10 h-10 p-0" :variant="item.value === page ? 'default' : 'outline'">
                  {{ item.value }}
                </Button>
              </PaginationListItem>
              <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>

            <PaginationNext />
            <PaginationLast />
          </PaginationList>
        </Pagination>
    </div>
  </div>
</template>