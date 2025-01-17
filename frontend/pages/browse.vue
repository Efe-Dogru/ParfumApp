<script setup lang="ts">
import { useApi } from '~/composables/useApi'
import type { Perfume } from '~/composables/useCommon'

const { getPerfumes } = useApi()
const perfumes = ref<Perfume[]>([])
const loading = ref(true)
const currentPage = ref(1)
const itemsPerPage = 42 // 6 columns * 7 rows

const fetchPerfumes = async (page: number) => {
  loading.value = true
  try {
    const response = await getPerfumes(page, itemsPerPage)
    perfumes.value = response.data
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

onMounted(() => {
  fetchPerfumes(currentPage.value)
})
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-4">Browse Perfumes</h1>
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
              src="assets/images/perfume-placeholder.jpg" 
              :alt="perfume.name"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="p-2">
            <h2 class="text-sm font-medium group-hover:text-primary truncate">{{ perfume.name }}</h2>
            <p class="text-xs text-muted-foreground truncate">{{ perfume.brand }}</p>
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