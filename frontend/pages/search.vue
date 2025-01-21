<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import type { Perfume } from '~/composables/useCommon'

useHead({
  title: 'Search Perfumes - Parfum App',
  meta: [
    { name: 'description', content: 'Search for your perfect perfume' }
  ]
})

const searchQuery = ref('')
const isLoading = ref(false)
const searchResults: Ref<Perfume[]> = ref([])

</script>

<template>
 
</template> 