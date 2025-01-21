<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import type { Perfume } from '~/composables/useCommon'

useHead({
  title: 'Search Perfumes - Parfum App',
  meta: [
    { name: 'description', content: 'Search for your perfect perfume' }
  ]
})

const searchQuery = ref('')
const isLoading = ref(false)
const searchResults: Ref<Perfume[]> = ref([])

const handleSearch = () => {
  if (!searchQuery.value.trim()) return
  
  isLoading.value = true
  // TODO: Implement actual search functionality
  setTimeout(() => {
    searchResults.value = [
      { id: 1, name: 'Sample Result 1', description: 'A matching fragrance' },
      { id: 2, name: 'Sample Result 2', description: 'Another matching scent' },
    ]
    isLoading.value = false
  }, 1000)
}
</script>

<template>
  <div class="space-y-8 mt-6">
    <div class="flex flex-col items-center text-center">
      <h1 class="text-3xl font-bold tracking-tight">Search Perfumes</h1>
      <p class="mt-4 text-lg text-muted-foreground">
        Find your perfect fragrance by searching our collection
      </p>
    </div>

    <div class="mx-auto max-w-2xl">
      <div class="flex space-x-2">
        <SearchInput
          v-model="searchQuery"
          placeholder="Search by name, brand, or notes..."
          @search="handleSearch"
        />
        <button
          class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
          :disabled="isLoading"
          @click="handleSearch"
        >
          <span v-if="isLoading">Searching...</span>
          <span v-else>Search</span>
        </button>
      </div>
    </div>

    <div v-if="searchResults.length > 0" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="result in searchResults"
        :key="result.id"
        class="rounded-lg border bg-card text-card-foreground shadow-sm"
      >
        <div class="p-6">
          <h3 class="text-lg font-semibold">{{ result.name }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ result.description }}
          </p>
          <div class="mt-4 flex items-center justify-end">
            <NuxtLink
              :to="`/perfume/${result.id}`"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            >
              View Details
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else-if="searchQuery && !isLoading"
      class="text-center text-muted-foreground"
    >
      No results found for "{{ searchQuery }}"
    </div>
  </div>
</template> 