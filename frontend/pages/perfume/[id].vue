<script setup lang="ts">
import { useApi } from '~/composables/useApi'
import type { Perfume } from '~/composables/useCommon'

const route = useRoute()
const { getPerfumeById } = useApi()

const perfume = ref<Perfume | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await getPerfumeById(route.params.id as string)
    perfume.value = response.data
  } catch (err) {
    error.value = 'Failed to load perfume details'
    console.error('Error fetching perfume:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
    </div>

    <div v-else-if="error" class="flex justify-center items-center py-8">
      <div class="text-red-500">{{ error }}</div>
    </div>

    <div v-else-if="perfume" class="mx-auto">
      <div class="flex justify-between items-start mb-8">
        <div>
          <h1 class="text-4xl font-bold mb-2">{{ perfume.name }}</h1>
          <p class="text-xl text-muted-foreground">{{ perfume.brand?.name }}</p>
          <p v-if="perfume.perfumer" class="text-sm text-muted-foreground mt-1">By {{ perfume.perfumer   }}</p>
        </div>
      </div>

      <div class="grid gap-8 md:grid-cols-2">
        <div class="space-y-6">
          <!-- Left Column -->
          <div class="aspect-square rounded-lg overflow-hidden">
            <img 
            :src="`http://127.0.0.1:8000/static/${perfume.local_image_path?.replace('\\', '/')}`"                         
            :alt="perfume.name"
              class="w-full h-full object-cover"
            />
          </div>

          <div>
            <h2 class="text-2xl font-semibold mb-4">Description</h2>
            <p class="text-muted-foreground">{{ perfume.description }}</p>
          </div>

          <div v-if="perfume.inspiration" class="border-t pt-4">
            <h2 class="text-xl font-semibold mb-2">Inspiration</h2>
            <p class="text-muted-foreground">{{ perfume.inspiration }}</p>
          </div>

          <div class="border-t pt-4">
            <h2 class="text-xl font-semibold mb-4">Details</h2>
            <div class="grid grid-cols-2 gap-4">
              <div v-if="perfume.type">
                <p class="font-medium">Type</p>
                <p class="text-muted-foreground">{{ perfume.type }}</p>
              </div>
              <div v-if="perfume.gender">
                <p class="font-medium">Gender</p>
                <p class="text-muted-foreground">{{ perfume.gender }}</p>
              </div>
              <div v-if="perfume.family">
                <p class="font-medium">Family</p>
                <p class="text-muted-foreground">{{ perfume.family }}</p>
              </div>
              <div v-if="perfume.concentration">
                <p class="font-medium">Concentration</p>
                <p class="text-muted-foreground">{{ perfume.concentration }}</p>
              </div>
              <div v-if="perfume.release_year">
                <p class="font-medium">Release Year</p>
                <p class="text-muted-foreground">{{ perfume.release_year }}</p>
              </div>
              <div v-if="perfume.longevity">
                <p class="font-medium">Longevity</p>
                <p class="text-muted-foreground">{{ perfume.longevity }}</p>
              </div>
              <div v-if="perfume.sillage">
                <p class="font-medium">Sillage</p>
                <p class="text-muted-foreground">{{ perfume.sillage }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <!-- Right Column -->
          <div v-if="perfume.main_accords?.length" class="border-b pb-6">
            <h2 class="text-2xl font-semibold mb-4">Main Accords</h2>
            <div class="flex flex-wrap gap-2">
              <!-- <span 
                v-for="accord in perfume.main_accords" 
                :key="accord.id"
                class="px-3 py-1 rounded-full bg-primary/10 text-primary"
              >
                {{ accord.name.charAt(0).toUpperCase() + accord.name.slice(1) }}

              </span> -->
            </div>
          </div>

          <div class="space-y-6">
            <div v-if="perfume.top_notes?.length">
              <h2 class="text-xl font-semibold mb-2">Top Notes</h2>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="note in perfume.top_notes" 
                  :key="note.id"
                  class="px-3 py-1 rounded-full bg-primary/10 text-primary"
                >
                  {{ note.name.charAt(0).toUpperCase() + note.name.slice(1) }}
                </span>
              </div>
            </div>

            <div v-if="perfume.middle_notes?.length">
              <h2 class="text-xl font-semibold mb-2">Middle Notes</h2>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="note in perfume.middle_notes" 
                  :key="note.id"
                  class="px-3 py-1 rounded-full bg-primary/10 text-primary"
                >
                  {{ note.name.charAt(0).toUpperCase() + note.name.slice(1) }}
                </span>
              </div>
            </div>

            <div v-if="perfume.base_notes?.length">
              <h2 class="text-xl font-semibold mb-2">Base Notes</h2>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="note in perfume.base_notes" 
                  :key="note.id"
                  class="px-3 py-1 rounded-full bg-primary/10 text-primary"
                >
                  {{ note.name.charAt(0).toUpperCase() + note.name.slice(1) }}
                </span>
              </div>
            </div>
          </div>

          <div class="space-y-6 border-t pt-6">
            <div v-if="perfume.occasion?.length">
              <h2 class="text-xl font-semibold mb-2">Best For</h2>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="occasion in perfume.occasion" 
                  :key="occasion"
                  class="px-3 py-1 rounded-full bg-accent text-accent-foreground"
                >
                  {{ occasion.charAt(0).toUpperCase() + occasion.slice(1) }}
                </span>
              </div>
            </div>

            <div v-if="perfume.season?.length">
              <h2 class="text-xl font-semibold mb-2">Ideal Seasons</h2>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="season in perfume.season" 
                  :key="season"
                  class="px-3 py-1 rounded-full bg-accent text-accent-foreground"
                >
                  {{ season.charAt(0).toUpperCase() + season.slice(1) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8">
        <NuxtLink 
          to="/browse"
          class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
        >
          Back to Browse
        </NuxtLink>
      </div>
    </div>
  </div>
</template> 