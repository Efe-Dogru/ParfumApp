<script setup lang="ts">
import { useApi } from '~/composables/useApi'
import type { Note } from '~/composables/useCommon'

const route = useRoute()
const { getNoteById } = useApi()

const note = ref<Note | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await getNoteById(route.params.id as string)
    note.value = response.data
  } catch (err) {
    error.value = 'Failed to load note details'
    console.error('Error fetching note:', err)
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

    <div v-else-if="note" class="mx-auto">
      <div class="flex justify-between items-start mb-8">
        <div>
          <h1 class="text-4xl font-bold mb-2">{{ note.name }}</h1>
        </div>
      </div>

      <div class="grid gap-8 md:grid-cols-2">
        <div class="space-y-6">
          <!-- Left Column -->
          <div v-if="note.image_filename" class="aspect-square rounded-lg overflow-hidden">
            <img 
              :src="`http://127.0.0.1:8000/static/notes_images/${note.image_filename}`"
              :alt="note.name"
              class="w-full h-full object-cover"
            />
          </div>
          <div v-else class="aspect-square rounded-lg overflow-hidden bg-accent flex items-center justify-center">
            <span class="text-4xl text-accent-foreground">{{ note.name.charAt(0).toUpperCase() }}</span>
          </div>
        </div>

        <div class="space-y-6">
          <!-- Right Column -->
          <div class="space-y-6">
            <div>
              <h2 class="text-xl font-semibold mb-2">Found in Perfumes</h2>
              <div class="grid grid-cols-1 gap-4">
                <!-- This section will be implemented when we add the related perfumes functionality -->
                <div class="p-4 rounded-lg border">
                  <p class="text-muted-foreground">Coming soon: List of perfumes containing this note</p>
                </div>
              </div>
            </div>

            <div>
              <h2 class="text-xl font-semibold mb-2">Common Note Combinations</h2>
              <div class="grid grid-cols-1 gap-4">
                <!-- This section will be implemented when we add note combinations functionality -->
                <div class="p-4 rounded-lg border">
                  <p class="text-muted-foreground">Coming soon: Common note combinations</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8">
        <NuxtLink 
          to="/notes"
          class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
        >
          Back to Notes
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
