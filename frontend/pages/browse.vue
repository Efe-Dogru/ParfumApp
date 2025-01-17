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

const nextPage = () => {
  if (perfumes.value.length === itemsPerPage) {
    currentPage.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
    fetchPerfumes(currentPage.value)
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
    fetchPerfumes(currentPage.value)
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
      <div class="flex justify-center items-center space-x-4 mt-8">
        <button 
          @click="previousPage" 
          :disabled="currentPage === 1 || loading"
          class="px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <span class="text-sm text-muted-foreground">
          Page {{ currentPage }}
        </span>
        <button 
          @click="nextPage" 
          :disabled="perfumes.length < itemsPerPage || loading"
          class="px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template> 