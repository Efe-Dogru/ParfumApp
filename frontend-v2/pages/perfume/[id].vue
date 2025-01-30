<script setup lang="ts">
import { usePerfumes } from '@/composables/usePerfumes'
import { useBucketImages } from '@/composables/useShared'
import type { PerfumeDetails } from '~/types/perfume'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Skeleton } from '@/components/ui/skeleton'
import { Droplets, Wind, Clock, Calendar, User2, Flower2, Sparkles, Flame, Heart, Sun, CloudSun, CloudRain, Snowflake, MapPin, GlassWater, Info } from 'lucide-vue-next'
import { 
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator 
} from '@/components/ui/breadcrumb'
import { NuxtLink } from '#components'

const route = useRoute()
const { getPerfumeDetails } = usePerfumes()
const perfume = ref<PerfumeDetails | null>(null)
const imageUrl = ref<string>('')
const loading = ref(true)
const perfumeNotes = computed(() => perfume.value?.notes || [])

// Helper function to capitalize words
const capitalizeWords = (str: string) => {
  return str
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

// Helper function to filter notes by type
const filterNotesByType = (notes: PerfumeDetails['notes'], type: 'top' | 'middle' | 'base') => {
  return notes.filter(n => n.note_type === type)
}

// Helper function to get note image URL
const getNoteImageUrl = async (filename: string | null) => {
  if (!filename) return null
  return await useBucketImages('notes_images', filename)
}

// We need to track note image URLs
const noteImageUrls = ref<Record<string, string>>({})

onMounted(async () => {
  try {
    const id = parseInt(route.params.id as string)
    perfume.value = await getPerfumeDetails(id)
    if (perfume.value?.local_image_path) {
      imageUrl.value = await useBucketImages('perfume_images', perfume.value.local_image_path)
    }
    
    // Load all note images
    for (const note of perfume.value?.notes || []) {
      if (note.notes.image_filename) {
        noteImageUrls.value[note.note_id] = await getNoteImageUrl(note.notes.image_filename) || ''
      }
    }
  } catch (error) {
    console.error('Error fetching perfume:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="container mx-auto py-12">
    <div class="">
      <div v-if="loading" class="space-y-8">
        <!-- Breadcrumb skeleton -->
        <div class="flex items-center space-x-2">
          <Skeleton class="h-4 w-20" />
          <Skeleton class="h-4 w-4" />
          <Skeleton class="h-4 w-24" />
          <Skeleton class="h-4 w-4" />
          <Skeleton class="h-4 w-32" />
        </div>

        <!-- Header skeleton -->
        <div class="space-y-3">
          <Skeleton class="h-5 w-36" />
          <Skeleton class="h-10 w-72" />
          <Skeleton class="h-4 w-48" />
        </div>

        <!-- Main content skeleton -->
        <div class="grid gap-16 lg:grid-cols-12">
          <!-- Image skeleton -->
          <div class="lg:col-span-5">
            <div class="aspect-square rounded-lg overflow-hidden">
              <Skeleton class="w-full h-full" />
            </div>
          </div>

          <!-- Content skeleton -->
          <div class="lg:col-span-7 space-y-12">
            <!-- Notes skeleton -->
            <div class="space-y-8">
              <div v-for="section in 3" :key="section" class="space-y-4">
                <Skeleton class="h-5 w-32" />
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div v-for="note in 5" :key="note" class="flex flex-col items-center space-y-2">
                    <Skeleton class="w-16 h-16 rounded-full" />
                    <Skeleton class="h-4 w-16" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Accords skeleton -->
            <div class="space-y-4">
              <Skeleton class="h-5 w-40" />
              <div class="flex flex-wrap gap-3">
                <Skeleton v-for="n in 5" :key="n" class="h-6 w-24 rounded-full" />
              </div>
            </div>

            <!-- Details grid skeleton -->
            <div class="grid grid-cols-2 gap-y-6 gap-x-12">
              <div v-for="n in 4" :key="n" class="space-y-2">
                <Skeleton class="h-4 w-24" />
                <Skeleton class="h-5 w-32" />
              </div>
            </div>
          </div>
        </div>

        <!-- Description skeleton -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 mt-8">
          <div class="space-y-4">
            <Skeleton class="h-5 w-32" />
            <Skeleton class="h-32 w-full" />
          </div>
          <div class="space-y-4 lg:border-l lg:border-border lg:pl-6">
            <Skeleton class="h-5 w-32" />
            <Skeleton class="h-32 w-full" />
          </div>
        </div>
      </div>

      <div v-else-if="perfume" class="space-y-8">
        <!-- Breadcrumb -->
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem>
              <NuxtLink to="/" class="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors">
                <!-- <Home class="w-4 h-4" /> -->
                Home
              </NuxtLink>
            </BreadcrumbItem>
            
            <BreadcrumbSeparator />
            
            <BreadcrumbItem>
              <NuxtLink to="/perfumes" class="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors">
                <!-- <Search class="w-4 h-4" /> -->
                Browse
              </NuxtLink>
            </BreadcrumbItem>
            
            <BreadcrumbSeparator />
            
            <BreadcrumbItem>
              <BreadcrumbPage class="text-sm">{{ perfume.name }}</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        <!-- Header Section -->
        <div class="mb-8">
          <p class="text-sm uppercase tracking-wider text-muted-foreground mb-2">{{ perfume.brands.name }}</p>
          <h1 class="text-4xl font-light mb-2">
            {{ perfume.name }} 
            <span class="text-muted-foreground text-2xl">{{ perfume.concentration.name }}</span>
          </h1>
          <p v-if="perfume.perfumer.name" class="text-sm text-muted-foreground">
            By {{ perfume.perfumer.name }}
          </p>
        </div>

        <div class="grid gap-16 lg:grid-cols-12">
          <!-- Left Column - Image -->
          <div class="lg:col-span-5">
            <div class="aspect-square rounded-lg overflow-hidden bg-muted">
              <img 
                v-if="imageUrl"
                :src="imageUrl"
                :alt="perfume.name"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground">
                No image available
              </div>
            </div>
          </div>

          <!-- Right Column - Content -->
          <div class="lg:col-span-7 space-y-12">
            <!-- Notes Pyramid -->
            <div class="space-y-8">
              <!-- Top Notes -->
              <div v-if="filterNotesByType(perfume.notes, 'top').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Sparkles class="w-4 h-4" />
                  Top Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfume.notes, 'top')" 
                    :key="`${note.note_id}-${note.note_type}`"
                    class="flex flex-col items-center group"
                  >
                    <div 
                      class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all"
                      :title="note.notes.name"
                    >
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground">
                        <img 
                          v-if="note.notes.image_filename && noteImageUrls[note.note_id]"
                          :src="noteImageUrls[note.note_id]"
                          :alt="note.notes.name"
                          class="w-full h-full object-cover"
                        />
                        <Droplets v-else class="w-6 h-6" />
                      </div>
                    </div>
                    <span class="text-sm text-center">{{ capitalizeWords(note.notes.name) }}</span>
                  </div>
                </div>
              </div>

              <!-- Middle Notes -->
              <div v-if="filterNotesByType(perfume.notes, 'middle').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Heart class="w-4 h-4" />
                  Middle Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfume.notes, 'middle')" 
                    :key="`${note.note_id}-${note.note_type}`"
                    class="flex flex-col items-center group"
                  >
                    <div 
                      class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all"
                      :title="note.notes.name"
                    >
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground">
                        <img 
                          v-if="note.notes.image_filename && noteImageUrls[note.note_id]"
                          :src="noteImageUrls[note.note_id]"
                          :alt="note.notes.name"
                          class="w-full h-full object-cover"
                        />
                        <Flower2 v-else class="w-6 h-6" />
                      </div>
                    </div>
                    <span class="text-sm text-center">{{ capitalizeWords(note.notes.name) }}</span>
                  </div>
                </div>
              </div>

              <!-- Base Notes -->
              <div v-if="filterNotesByType(perfume.notes, 'base').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Flame class="w-4 h-4" />
                  Base Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfume.notes, 'base')" 
                    :key="`${note.note_id}-${note.note_type}`"
                    class="flex flex-col items-center group"
                  >
                    <div 
                      class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all"
                      :title="note.notes.name"
                    >
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground">
                        <img 
                          v-if="note.notes.image_filename && noteImageUrls[note.note_id]"
                          :src="noteImageUrls[note.note_id]"
                          :alt="note.notes.name"
                          class="w-full h-full object-cover"
                        />
                        <GlassWater v-else class="w-6 h-6" />
                      </div>
                    </div>
                    <span class="text-sm text-center">{{ capitalizeWords(note.notes.name) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Main Accords -->
            <div v-if="perfume.accords?.length">
              <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                <Droplets class="w-4 h-4" />
                Main Accords
              </h2>
              <div class="flex flex-wrap gap-3">
                <Badge 
                  v-for="accord in perfume.accords" 
                  :key="accord.main_accords.id"
                  variant="secondary"
                  class="text-sm border border-secondary-600 bg-secondary/10 px-6 text-black dark:text-white dark:bg-secondary-600"
                >
                  {{ capitalizeWords(accord.main_accords.name) }}
                </Badge>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-y-6 gap-x-12">
              <div v-if="perfume.category">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Droplets class="w-3 h-3" />
                  Category
                </p>
                <p>{{ capitalizeWords(perfume.category) }}</p>
              </div>
              <div v-if="perfume.gender">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <User2 class="w-3 h-3" />
                  Gender
                </p>
                <p>{{ capitalizeWords(perfume.gender) }}</p>
              </div>
              <div v-if="perfume.release_year">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Calendar class="w-3 h-3" />
                  Release Year
                </p>
                <p>{{ perfume.release_year }}</p>
              </div>
              <div v-if="perfume.longevity">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Clock class="w-3 h-3" />
                  Longevity
                </p>
                <p>{{ capitalizeWords(perfume.longevity) }}</p>
              </div>
              <div v-if="perfume.sillage">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Wind class="w-3 h-3" />
                  Sillage
                </p>
                <p>{{ capitalizeWords(perfume.sillage) }}</p>
              </div>
              <div v-if="perfume.country">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <MapPin class="w-3 h-3" />
                  Country
                </p>
                <p>{{ perfume.country.name }}</p>
              </div>
              <div v-if="perfume.family">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Flower2 class="w-3 h-3" />
                  Family
                </p>
                <p>{{ perfume.family.name }}</p>
              </div>
              <div v-if="perfume.type">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Droplets class="w-3 h-3" />
                  Type
                </p>
                <p>{{ perfume.type.name }}</p>
              </div>
            </div>

            <div>
              <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                <MapPin class="w-4 h-4" />
                Best For
              </h2>
              <div class="flex flex-wrap gap-2">
                <Badge 
                  v-for="occasion in perfume.occasion" 
                  :key="occasion"
                  variant="outline"
                  class="capitalize"
                >
                  {{ capitalizeWords(occasion) }}
                </Badge>
              </div>

              <h2 class="text-sm uppercase tracking-wider mt-8 mb-4 flex items-center gap-2">
                <Sun class="w-4 h-4" />
                Ideal Seasons
              </h2>
              <div class="flex flex-wrap gap-2">
                <Badge 
                  v-for="season in perfume.season" 
                  :key="season"
                  variant="outline"
                  class="capitalize inline-flex items-center gap-1"
                >
                  <component 
                    :is="season.toLowerCase() === 'summer' ? Sun : 
                         season.toLowerCase() === 'spring' ? CloudSun :
                         season.toLowerCase() === 'fall' ? CloudRain :
                         Snowflake" 
                    class="w-3 h-3"
                  />
                  {{ capitalizeWords(season) }}
                </Badge>
              </div>
            </div>
          </div>
        </div>

        <Separator class="my-8" />
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div v-if="perfume.description" class="prose prose-sm max-w-none">
            <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
              <Info class="w-4 h-4" />
              Description
            </h2>
            <p class="text-muted-foreground leading-relaxed">{{ perfume.description }}</p>
          </div>
          <div v-if="perfume.inspiration" class="prose prose-sm max-w-none lg:border-l lg:border-border lg:pl-6">
            <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
              <Flower2 class="w-4 h-4" />
              Inspiration
            </h2>
            <p class="text-muted-foreground leading-relaxed">{{ perfume.inspiration }}</p>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12">
        <h2 class="text-2xl font-bold">Perfume not found</h2>
      </div>
    </div>
  </div>
</template>