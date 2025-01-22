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
  <div class="min-h-screen bg-background">
    <div class="container mx-auto px-4 py-12">
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>

      <div v-else-if="error" class="flex justify-center items-center py-8">
        <div class="text-red-500">{{ error }}</div>
      </div>

      <div v-else-if="perfume" class="mx-auto max-w-6xl">
        <!-- Header Section -->
        <div class="mb-8">
          <p class="text-sm uppercase tracking-wider text-muted-foreground mb-2">{{ perfume.brand?.name }}</p>
          <h1 class="text-4xl font-light mb-2">{{ perfume.name }}</h1>
          <p v-if="perfume.perfumer" class="text-sm text-muted-foreground">
            By {{ perfume.perfumer?.name }}
          </p>
        </div>

        <div class="grid gap-16 lg:grid-cols-12">
          <!-- Left Column - Image -->
          <div class="lg:col-span-5">
            <div class="aspect-square">
              <img 
                :src="`http://127.0.0.1:8000/static/${perfume.local_image_path?.replace('\\', '/')}`"
                :alt="perfume.name"
                class="w-full h-full object-cover"
              />
            </div>
          </div>

          <!-- Right Column - Content -->
          <div class="lg:col-span-7 space-y-12">
            <!-- Main Accords -->
            <div v-if="perfume.main_accords?.length">
              <h2 class="text-sm uppercase tracking-wider mb-6">Main Accords</h2>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="accord in perfume.main_accords" 
                  :key="accord.id"
                  class="px-3 py-1 text-sm border border-border rounded-sm"
                >
                  {{ accord.name.charAt(0).toUpperCase() + accord.name.slice(1) }}
                </span>
              </div>
            </div>

            <!-- Notes Pyramid -->
            <div class="space-y-8">
              <div v-if="perfume.top_notes?.length">
                <h2 class="text-sm uppercase tracking-wider mb-4">Top Notes</h2>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="note in perfume.top_notes" 
                    :key="note.id"
                    class="px-3 py-1 text-sm border border-border rounded-sm"
                  >
                    {{ note.name.charAt(0).toUpperCase() + note.name.slice(1) }}
                  </span>
                </div>
              </div>

              <div v-if="perfume.middle_notes?.length">
                <h2 class="text-sm uppercase tracking-wider mb-4">Middle Notes</h2>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="note in perfume.middle_notes" 
                    :key="note.id"
                    class="px-3 py-1 text-sm border border-border rounded-sm"
                  >
                    {{ note.name.charAt(0).toUpperCase() + note.name.slice(1) }}
                  </span>
                </div>
              </div>

              <div v-if="perfume.base_notes?.length">
                <h2 class="text-sm uppercase tracking-wider mb-4">Base Notes</h2>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="note in perfume.base_notes" 
                    :key="note.id"
                    class="px-3 py-1 text-sm border border-border rounded-sm"
                  >
                    {{ note.name.charAt(0).toUpperCase() + note.name.slice(1) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

      <!-- Description & Inspiration -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 border-t border-border pt-8 mt-12">
        <div v-if="perfume.description" class="prose prose-sm max-w-none">
          <h2 class="text-sm uppercase tracking-wider mb-4">Description</h2>
          <p class="text-muted-foreground leading-relaxed">{{ perfume.description }}</p>
        </div>
        <div v-if="perfume.inspiration" class="prose prose-sm max-w-none border-l border-border pl-6">
          <h2 class="text-sm uppercase tracking-wider mb-4">Inspiration</h2>
          <p class="text-muted-foreground leading-relaxed">{{ perfume.inspiration }}</p>
        </div>
      </div>

        <!-- Details & Best For -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 border-t border-border pt-8 mt-8">
          <div>
            <h2 class="text-sm uppercase tracking-wider mb-4">Details</h2>
            <div class="grid grid-cols-2 gap-y-6 gap-x-12">
              <div v-if="perfume.type">
                <p class="text-xs uppercase text-muted-foreground mb-1">Type</p>
                <p>{{ perfume.type?.name }}</p>
              </div>
              <div v-if="perfume.gender">
                <p class="text-xs uppercase text-muted-foreground mb-1">Gender</p>
                <p>{{ perfume.gender }}</p>
              </div>
              <div v-if="perfume.family">
                <p class="text-xs uppercase text-muted-foreground mb-1">Family</p>
                <p>{{ perfume.family?.name }}</p>
              </div>
              <div v-if="perfume.concentration">
                <p class="text-xs uppercase text-muted-foreground mb-1">Concentration</p>
                <p>{{ perfume.concentration?.name }}</p>
              </div>
              <div v-if="perfume.release_year">
                <p class="text-xs uppercase text-muted-foreground mb-1">Release Year</p>
                <p>{{ perfume.release_year }}</p>
              </div>
              <div v-if="perfume.longevity">
                <p class="text-xs uppercase text-muted-foreground mb-1">Longevity</p>
                <p>{{ perfume.longevity }}</p>
              </div>
              <div v-if="perfume.sillage">
                <p class="text-xs uppercase text-muted-foreground mb-1">Sillage</p>
                <p>{{ perfume.sillage }}</p>
              </div>
            </div>
          </div>

          <div>
            <h2 class="text-sm uppercase tracking-wider mb-4">Best For</h2>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="occasion in perfume.occasion" 
                :key="occasion"
                class="px-3 py-1 text-sm border border-border rounded-sm"
              >
                {{ occasion.charAt(0).toUpperCase() + occasion.slice(1) }}
              </span>
            </div>
            <h2 class="text-sm uppercase tracking-wider mt-8 mb-4">Ideal Seasons</h2>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="season in perfume.season" 
                :key="season"
                class="px-3 py-1 text-sm border border-border rounded-sm"
              >
                {{ season.charAt(0).toUpperCase() + season.slice(1) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Back Button -->
        <div class="mt-16">
          <NuxtLink 
            to="/browse"
            class="text-sm uppercase tracking-wider hover:text-primary transition-colors"
          >
            ← Back to Browse
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Remove all previous styles */
</style> 