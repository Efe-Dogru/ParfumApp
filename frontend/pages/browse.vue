<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import type { Perfume } from '~/composables/useCommon'

useHead({
  title: 'Browse Perfumes - Parfum App',
  meta: [
    { name: 'description', content: 'Browse our collection of perfumes' }
  ]
})

// Placeholder for perfume data
const perfumes: Ref<Perfume[]> = ref([
  { id: 1, name: 'Sample Perfume 1', description: 'A delightful fragrance' },
  { id: 2, name: 'Sample Perfume 2', description: 'An enchanting scent' },
  { id: 3, name: 'Sample Perfume 3', description: 'A mysterious aroma' },
])
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold tracking-tight">Browse Perfumes</h1>
      <div class="flex items-center space-x-2">
        <button class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2">
          Filter
        </button>
        <button class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2">
          Sort
        </button>
      </div>
    </div>

    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div
        v-for="perfume in perfumes"
        :key="perfume.id"
        class="rounded-lg border bg-card text-card-foreground shadow-sm"
      >
        <div class="p-6">
          <h3 class="text-lg font-semibold">{{ perfume.name }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ perfume.description }}
          </p>
          <div class="mt-4 flex items-center justify-end">
            <NuxtLink
              :to="`/perfume/${perfume.id}`"
              class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            >
              View Details
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> 