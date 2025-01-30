<script setup lang="ts">
import { useNotes } from '@/composables/useNotes'
import { useBucketImages } from '@/composables/useShared'
import type { NoteDetails } from '~/types/note'
import { Separator } from '@/components/ui/separator'
import { Skeleton } from '@/components/ui/skeleton'
import { Droplets, Flower2, Info, Heart } from 'lucide-vue-next'
import { 
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator 
} from '@/components/ui/breadcrumb'
import { NuxtLink } from '#components'
import { Badge } from '@/components/ui/badge'

const route = useRoute()
const { getNoteDetails } = useNotes()
const note = ref<NoteDetails | null>(null)
const imageUrl = ref<string>('')
const loading = ref(true)

// Helper function to capitalize words
const capitalizeWords = (str: string) => {
  return str
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

onMounted(async () => {
  try {
    const id = parseInt(route.params.id as string)
    note.value = await getNoteDetails(id)
    if (note.value?.image_filename) {
      imageUrl.value = await useBucketImages('notes_images', note.value.image_filename)
    }
  } catch (error) {
    console.error('Error fetching note:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="container mx-auto py-12">
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
        <Skeleton class="h-10 w-72" />
        <Skeleton class="h-4 w-48" />
      </div>

      <!-- Main content skeleton -->
      <div class="grid gap-16 lg:grid-cols-12">
        <div class="lg:col-span-5">
          <Skeleton class="aspect-square rounded-lg" />
        </div>
        <div class="lg:col-span-7">
          <div class="space-y-6">
            <Skeleton class="h-4 w-full" v-for="n in 4" :key="n" />
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="note" class="space-y-8">
      <!-- Breadcrumb -->
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <NuxtLink to="/" class="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors">
              Home
            </NuxtLink>
          </BreadcrumbItem>
          
          <BreadcrumbSeparator />
          
          <BreadcrumbItem>
            <NuxtLink to="/notes" class="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors">
              Notes
            </NuxtLink>
          </BreadcrumbItem>
          
          <BreadcrumbSeparator />
          
          <BreadcrumbItem>
            <BreadcrumbPage class="text-sm">{{ note.name }}</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>

      <!-- Header Section -->
      <div class="mb-8">
        <h1 class="text-4xl font-light mb-2">{{ capitalizeWords(note.name) }}</h1>
        <p class="text-sm text-muted-foreground">{{ note.family?.name }} Note</p>
      </div>

      <div class="grid gap-16 lg:grid-cols-12">
        <!-- Left Column - Image -->
        <div class="lg:col-span-5">
          <div class="aspect-square rounded-lg overflow-hidden bg-muted">
            <img 
              v-if="imageUrl"
              :src="imageUrl"
              :alt="note.name"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground">
              <Droplets class="w-12 h-12" />
            </div>
          </div>
        </div>

        <!-- Right Column - Content -->
        <div class="lg:col-span-7 space-y-8">
          <!-- Description -->
          <div v-if="note.description" class="space-y-2">
            <h2 class="text-lg font-medium flex items-center gap-2">
              <Info class="w-4 h-4" />
              Description
            </h2>
            <p class="text-muted-foreground">{{ note.description }}</p>
          </div>

          <!-- Moods -->
          <div v-if="note.moods?.length" class="space-y-2">
            <h2 class="text-lg font-medium flex items-center gap-2">
              <Heart class="w-4 h-4" />
              Moods
            </h2>
            <div class="flex flex-wrap gap-2">
              <Badge 
                v-for="moodRelation in note.moods" 
                :key="moodRelation.mood.id"
                variant="outline"
                class="text-sm border border-secondary-600 bg-secondary/10 px-6"
              >
                {{ moodRelation.mood.name }}
              </Badge>
            </div>
          </div>

          <!-- Source -->
          <div v-if="note.source" class="space-y-2">
            <h2 class="text-lg font-medium flex items-center gap-2">
              <Flower2 class="w-4 h-4" />
              Source
            </h2>
            <p class="text-muted-foreground">{{ note.source }}</p>
          </div>

          <!-- Cultural Significance -->
          <div v-if="note.cultural_significance" class="space-y-2">
            <h2 class="text-lg font-medium">Cultural Significance</h2>
            <p class="text-muted-foreground">{{ note.cultural_significance }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="text-center py-12">
      <p class="text-muted-foreground">Note not found</p>
    </div>
  </div>
</template>