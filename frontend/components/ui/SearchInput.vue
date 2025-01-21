<script setup lang="ts">
import { ref } from 'vue'
import type { Perfume } from '~/composables/useCommon'

interface Props {
  modelValue: string
  placeholder?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'search'): void
}>()

const isSearchOpen = ref(false)
const searchResults = ref<Perfume[]>([])
const isLoading = ref(false)

const { searchPerfumes } = useApi()

// Debounced search
let searchTimeout: NodeJS.Timeout
const handleSearch = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
  isSearchOpen.value = !!target.value
  
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchSearchResults(target.value)
  }, 500)
}

const fetchSearchResults = async (query: string) => {
  if (!query) {
    searchResults.value = []
    return
  }
  
  try {
    isLoading.value = true
    const { data } = await searchPerfumes(query)
    searchResults.value = data
  } catch (error) {
    console.error('Search error:', error)
    searchResults.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  // Close search dropdown when clicking outside
  document.addEventListener('click', (e) => {
    const searchContainer = document.querySelector('.search-container')
    if (!searchContainer?.contains(e.target as Node)) {
      isSearchOpen.value = false
    }
  })
})

// Cleanup
onUnmounted(() => {
  clearTimeout(searchTimeout)
})
</script>

<template>
  <div class="relative search-container flex flex-col gap-2">
    <div class="relative">
      <input
        :id="placeholder"
        type="text"
        :placeholder="placeholder"
        :value="modelValue"
        @input="handleSearch"
        class="w-full px-4 py-2 rounded-lg bg-background border border-input hover:border-[#4A154B] dark:hover:border-white transition-colors focus:outline-none focus:ring-2 focus:ring-[#4A154B] dark:focus:ring-white"
      />
      <div v-if="isLoading" class="absolute right-3 top-2.5">
        <div class="animate-spin h-5 w-5 border-2 border-[#4A154B] dark:border-white border-t-transparent rounded-full"></div>
      </div>
    </div>
    
    <!-- Search Results Dropdown -->
    <div
      v-if="isSearchOpen && searchResults.length > 0"
      class="absolute z-50 w-full mt-12 bg-background border border-input rounded-lg shadow-lg"
    >
      <div class="max-h-96 overflow-y-auto">
        <NuxtLink
          v-for="result in searchResults"
          :key="result.id"
          :to="'/perfume/' + result.id"
          class="block px-4 py-2 hover:bg-accent/50 cursor-pointer transition-colors"
          @click="isSearchOpen = false"
        >
          <div class="flex items-center space-x-3">
            <img
              v-if="result.local_image_path"
              :src="`http://127.0.0.1:8000/static/${result.local_image_path?.replace('\\', '/')}`"                         
              :alt="result.name"
              class="w-10 h-10 object-cover rounded"
            />
            <div>
              <div class="font-medium">{{ result.name }}</div>
              <!-- <div class="text-sm text-muted-foreground">{{ result.brand }} ({{ result.year }})</div> -->
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template> 