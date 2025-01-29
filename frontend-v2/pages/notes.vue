<script setup lang="ts">
import type { Note } from '~/types/note'
import { useNotes } from '@/composables/useNotes'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { NuxtLink } from '#components'
import Input from '@/components/ui/input/Input.vue'
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { useBucketImages } from '@/composables/useShared'
import {
  Pagination,
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
} from '@/components/ui/pagination'

// Define the directive
const vObserveVisibility = {
  mounted: (el: HTMLElement, { value }: { value: (el: HTMLElement) => void }) => {
    value(el)
  }
}

const { getNotes, searchNotes, getNoteFamilies } = useNotes()
const notes = ref<Note[] | null>(null)
const searchQuery = ref('')
const searchTimeout = ref<NodeJS.Timeout | null>(null)
const loading = ref(true)
const imageUrls = ref<Record<string, string>>({})
const currentPage = ref(1)
const itemsPerPage = 42
const totalItems = ref(0)

// Filters
const selectedFamily = ref('')
const selectedMood = ref('')

const familyOptions = ref([
  { value: 'all', label: 'All Families' }
])

const moodOptions = [
  { value: 'all', label: 'All Moods' },
  { value: 'romantic', label: 'Romantic' },
  { value: 'energetic', label: 'Energetic' },
  { value: 'relaxing', label: 'Relaxing' },
  { value: 'mysterious', label: 'Mysterious' },
  { value: 'fresh', label: 'Fresh' },
]

// Image loading with Intersection Observer
const observer = ref<IntersectionObserver | null>(null)

const loadImage = async (note: Note) => {
  if (note.image_filename && !imageUrls.value[note.image_filename]) {
    try {
      imageUrls.value[note.image_filename] = await useBucketImages('notes_images', note.image_filename)
    } catch (error) {
      console.error('Error loading image:', error)
    }
  }
}

const setupIntersectionObserver = () => {
  if (process.client) {
    observer.value = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const noteId = entry.target.getAttribute('data-note-id')
          const note = notes.value?.find(n => n.id.toString() === noteId)
          if (note) {
            loadImage(note)
            observer.value?.unobserve(entry.target)
          }
        }
      })
    }, {
      root: null,
      rootMargin: '50px',
      threshold: 0.1
    })
  }
}

const observeImage = (el: HTMLElement) => {
  if (observer.value && process.client) {
    observer.value.observe(el)
  }
}

const fetchNotes = async (page: number) => {
  loading.value = true
  try {
    const filters = {
      family_id: selectedFamily.value
    }
    const result = await getNotes(page, itemsPerPage, filters)
    notes.value = result.data
    totalItems.value = (result.count / itemsPerPage) * 10
  } catch (error) {
    console.error('Error fetching notes:', error)
  } finally {
    loading.value = false
  }
}

// Function to fetch and set family options
const fetchFamilyOptions = async () => {
  try {
    const families = await getNoteFamilies()
    familyOptions.value = [
      { value: 'all', label: 'All Families' },
      ...families.map((family: { id: number, name: string }) => ({
        value: family.id.toString(),
        label: family.name
      }))
    ]
  } catch (error) {
    console.error('Error fetching families:', error)
  }
}

onMounted(async () => {
  setupIntersectionObserver()
  await Promise.all([
    fetchNotes(currentPage.value),
    fetchFamilyOptions()
  ])
})

onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
})

const handleSearch = async (event: Event) => {
  const query = (event.target as HTMLInputElement).value
  searchQuery.value = query

  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  searchTimeout.value = setTimeout(async () => {
    loading.value = true
    try {
      const filters = {
        family_id: selectedFamily.value
      }
      if (query.trim()) {
        const result = await searchNotes(query, filters)
        notes.value = result.data
        totalItems.value = (result.count / itemsPerPage) * 10
      } else {
        await fetchNotes(currentPage.value)
      }
    } catch (error) {
      console.error('Error searching notes:', error)
    } finally {
      loading.value = false
    }
  }, 300)
}

watch(currentPage, async (newPage) => {
  await fetchNotes(newPage)
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

// Watch for filter changes
watch([selectedFamily], async () => {
  currentPage.value = 1
  await fetchNotes(1)
})
</script>

<template>
  <div class="container mx-auto px-4">
    <!-- Search and filters section -->
    <div class="flex flex-wrap items-center gap-4 mb-4">
      <Input 
        v-model="searchQuery"
        placeholder="Search notes..."
        @input="handleSearch"
        class="w-full max-w-xs"
      />
      <CustomComboBox
        v-model="selectedFamily"
        :items="familyOptions"
        placeholder="Family"
        search-placeholder="Search families..."
      />
      <CustomComboBox
        v-model="selectedMood"
        :items="moodOptions"
        placeholder="Mood"
        search-placeholder="Search moods..."
      />
    </div>
    
    <!-- Notes grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      <template v-if="loading">
        <div v-for="n in itemsPerPage" :key="n" class="flex-none space-y-3">
          <div class="relative overflow-hidden rounded-lg aspect-square">
            <Skeleton class="w-full h-full absolute inset-0" />
          </div>
          <div class="space-y-2">
            <Skeleton class="h-5 w-3/4" />
          </div>
        </div>
      </template>
      <template v-else>
        <NuxtLink 
          v-for="note in notes" 
          :key="note.id" 
          :to="`/note/${note.id}`"
          class="flex-none group hover:opacity-95 transition-opacity"
        >
          <div 
            :data-note-id="note.id"
            v-observe-visibility="observeImage"
            class="relative overflow-hidden rounded-lg aspect-square mb-3"
          >
            <img 
              v-if="imageUrls[note.image_filename]"
              :src="imageUrls[note.image_filename]" 
              :alt="note.name"
              class="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
            />
            <div v-else class="w-full h-full flex items-center justify-center">
              <Skeleton class="w-full h-full" />
            </div>
          </div>
          <h3 class="font-medium text-foreground">{{ note.name }}</h3>
        </NuxtLink>
      </template>
    </div>

    <div class="flex justify-center mt-6">
      <Pagination 
        v-slot="{ page }" 
        :total="totalItems"
        :per-page="itemsPerPage"
        :sibling-count="1" 
        show-edges 
        :default-page="1"
        :page="currentPage"
        @update:page="currentPage = $event"
      >
        <PaginationList v-slot="{ items }" class="flex items-center gap-1">
          <PaginationFirst />
          <PaginationPrev />

          <template v-for="(item, index) in items">
            <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
              <Button class="w-10 h-10 p-0" :variant="item.value === page ? 'default' : 'outline'">
                {{ item.value }}
              </Button>
            </PaginationListItem>
            <PaginationEllipsis v-else :key="item.type" :index="index" />
          </template>

          <PaginationNext />
          <PaginationLast />
        </PaginationList>
      </Pagination>
    </div>
  </div>
</template>