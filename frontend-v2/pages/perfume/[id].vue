<script setup lang="ts">
import { usePerfumes } from '@/composables/usePerfumes'
import { useBucketImages } from '@/composables/useShared'
import { useNotes } from '@/composables/useNotes'
import type { Perfume, PerfumeNote } from '~/types/api'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Skeleton } from '@/components/ui/skeleton'
import { Home, Search, Droplets, Wind, Clock, Calendar, User2, Flower2, Sparkles, Flame, Heart, Sun, CloudSun, CloudRain, Snowflake, MapPin, GlassWater, Info } from 'lucide-vue-next'

const route = useRoute()
const { getPerfume } = usePerfumes()
const { getPerfumeNotes } = useNotes()
const perfume = ref<Perfume | null>(null)
const imageUrl = ref<string>('')
const loading = ref(true)
const perfumeNotes = ref<PerfumeNote[]>([])

// Helper function to capitalize words
const capitalizeWords = (str: string) => {
  return str
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

// Helper function to get accord class
const getAccordClass = (accordName: string) => {
  const classes = {
    // Woody & Earthy tones
    woody: 'bg-amber-200 dark:bg-amber-800 text-amber-900 dark:text-amber-100',
    earthy: 'bg-stone-200 dark:bg-stone-800 text-stone-900 dark:text-stone-100',
    // ... add more accord classes as needed
  }
  const key = accordName.toLowerCase() as keyof typeof classes
  return classes[key] || 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
}

// Helper function to filter notes by type
const filterNotesByType = (notes: PerfumeNote[], type: 'top' | 'middle' | 'base') => {
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
    perfume.value = await getPerfume(id)
    if (perfume.value?.local_image_path) {
      imageUrl.value = await useBucketImages('perfume_images', perfume.value.local_image_path)
    }
    perfumeNotes.value = await getPerfumeNotes(id)
    
    // Load all note images
    for (const note of perfumeNotes.value) {
      if (note.note.image_filename) {
        noteImageUrls.value[note.note.id] = await getNoteImageUrl(note.note.image_filename) || ''
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
  <div class="min-h-screen bg-background">
    <div class="container mx-auto px-4 py-12">
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="space-y-4 w-full">
          <Skeleton class="h-[400px] w-full" />
          <Skeleton class="h-12 w-3/4" />
          <Skeleton class="h-8 w-1/2" />
          <Skeleton class="h-32 w-full" />
        </div>
      </div>

      <div v-else-if="perfume" class="space-y-8">
        <!-- Breadcrumb -->
        <div class="flex items-center space-x-2 text-sm text-muted-foreground">
          <NuxtLink to="/" class="hover:text-primary transition-colors inline-flex items-center gap-1">
            <Home class="w-4 h-4" />
            Home
          </NuxtLink>
          <span>/</span>
          <NuxtLink to="/perfumes" class="hover:text-primary transition-colors inline-flex items-center gap-1">
            <Search class="w-4 h-4" />
            Browse
          </NuxtLink>
          <span>/</span>
          <span class="text-foreground">{{ perfume.name }}</span>
        </div>

        <!-- Header Section -->
        <div class="mb-8">
          <p class="text-sm uppercase tracking-wider text-muted-foreground mb-2">{{ perfume.brands?.name }}</p>
          <h1 class="text-4xl font-light mb-2">{{ perfume.name }}</h1>
          <p v-if="perfume.perfumer" class="text-sm text-muted-foreground">
            By {{ perfume.perfumer }}
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
              <div v-if="filterNotesByType(perfumeNotes, 'top').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Sparkles class="w-4 h-4" />
                  Top Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfumeNotes, 'top')" 
                    :key="`${note.perfume_id}-${note.note_id}-${note.note_type}`"
                    class="flex flex-col items-center group"
                  >
                    <div 
                      class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all"
                      :title="note.note.description || note.note.name"
                    >
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground">
                        <img 
                          v-if="note.note.image_filename && noteImageUrls[note.note.id]"
                          :src="noteImageUrls[note.note.id]"
                          :alt="note.note.name"
                          class="w-full h-full object-cover"
                        />
                        <Droplets v-else class="w-6 h-6" />
                      </div>
                    </div>
                    <span class="text-sm text-center">{{ capitalizeWords(note.note.name) }}</span>
                  </div>
                </div>
              </div>

              <!-- Middle Notes -->
              <div v-if="filterNotesByType(perfumeNotes, 'middle').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Heart class="w-4 h-4" />
                  Middle Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfumeNotes, 'middle')" 
                    :key="`${note.perfume_id}-${note.note_id}-${note.note_type}`"
                    class="flex flex-col items-center group"
                  >
                    <div 
                      class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all"
                      :title="note.note.description || note.note.name"
                    >
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground">
                        <img 
                          v-if="note.note.image_filename && noteImageUrls[note.note.id]"
                          :src="noteImageUrls[note.note.id]"
                          :alt="note.note.name"
                          class="w-full h-full object-cover"
                        />
                        <Flower2 v-else class="w-6 h-6" />
                      </div>
                    </div>
                    <span class="text-sm text-center">{{ capitalizeWords(note.note.name) }}</span>
                  </div>
                </div>
              </div>

              <!-- Base Notes -->
              <div v-if="filterNotesByType(perfumeNotes, 'base').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Flame class="w-4 h-4" />
                  Base Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfumeNotes, 'base')" 
                    :key="`${note.perfume_id}-${note.note_id}-${note.note_type}`"
                    class="flex flex-col items-center group"
                  >
                    <div 
                      class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all"
                      :title="note.note.description || note.note.name"
                    >
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground">
                        <img 
                          v-if="note.note.image_filename && noteImageUrls[note.note.id]"
                          :src="noteImageUrls[note.note.id]"
                          :alt="note.note.name"
                          class="w-full h-full object-cover"
                        />
                        <GlassWater v-else class="w-6 h-6" />
                      </div>
                    </div>
                    <span class="text-sm text-center">{{ capitalizeWords(note.note.name) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Main Accords -->
            <div v-if="perfume.main_accords?.length">
              <h2 class="text-sm uppercase tracking-wider mb-6">Main Accords</h2>
              <div class="flex flex-wrap gap-3">
                <Badge 
                  v-for="(accord, index) in perfume.main_accords" 
                  :key="index"
                  variant="secondary"
                  :class="getAccordClass(String(accord))"
                >
                  {{ String(accord).charAt(0).toUpperCase() + String(accord).slice(1) }}
                </Badge>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-y-6 gap-x-12">
              <div v-if="perfume.category">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Droplets class="w-3 h-3" />
                  Category
                </p>
                <p>{{ perfume.category }}</p>
              </div>
              <div v-if="perfume.gender">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <User2 class="w-3 h-3" />
                  Gender
                </p>
                <p>{{ perfume.gender }}</p>
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
                <p>{{ perfume.longevity }}</p>
              </div>
              <div v-if="perfume.sillage">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Wind class="w-3 h-3" />
                  Sillage
                </p>
                <p>{{ perfume.sillage }}</p>
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
                  {{ occasion }}
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
                  {{ season }}
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