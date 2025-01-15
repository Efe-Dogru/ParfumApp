<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import type { Perfume } from '~/composables/useCommon'

const route = useRoute()
const perfumeId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id

// Placeholder for perfume data fetching
const perfume: Ref<Perfume> = ref({
  id: perfumeId,
  name: 'Sample Perfume',
  description: 'A delightful fragrance that combines floral and woody notes.',
  brand: 'Luxury Brand',
  year: 2023,
  notes: {
    top: ['Bergamot', 'Lemon', 'Orange'],
    heart: ['Rose', 'Jasmine', 'Lavender'],
    base: ['Vanilla', 'Musk', 'Sandalwood']
  }
})

useHead({
  title: `${perfume.value.name} - Parfum App`,
  meta: [
    { name: 'description', content: perfume.value.description }
  ]
})
</script>

<template>
  <div class="space-y-8">
    <div class="flex items-center space-x-4">
      <NuxtLink
        to="/browse"
        class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
      >
        Back to Browse
      </NuxtLink>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="space-y-4">
        <h1 class="text-3xl font-bold">{{ perfume.name }}</h1>
        <p class="text-lg text-muted-foreground">{{ perfume.description }}</p>
        
        <div class="space-y-2">
          <p><strong>Brand:</strong> {{ perfume.brand }}</p>
          <p><strong>Year:</strong> {{ perfume.year }}</p>
        </div>
      </div>

      <div class="space-y-6">
        <div class="rounded-lg border p-6">
          <h2 class="text-xl font-semibold mb-4">Fragrance Notes</h2>
          
          <div class="space-y-4">
            <div>
              <h3 class="font-medium mb-2">Top Notes</h3>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="note in perfume.notes?.top"
                  :key="note"
                  class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                >
                  {{ note }}
                </span>
              </div>
            </div>

            <div>
              <h3 class="font-medium mb-2">Heart Notes</h3>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="note in perfume.notes?.heart"
                  :key="note"
                  class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                >
                  {{ note }}
                </span>
              </div>
            </div>

            <div>
              <h3 class="font-medium mb-2">Base Notes</h3>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="note in perfume.notes?.base"
                  :key="note"
                  class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:focus-offset-2"
                >
                  {{ note }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> 