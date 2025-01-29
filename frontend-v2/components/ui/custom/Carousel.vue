<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import type { Perfume } from '~/types/api'

interface Props {
  items: Perfume[]
  loading: boolean
  hasMore: boolean
  onLoadMore: () => Promise<void>
}

const props = defineProps<Props>()

const containerRef = ref<HTMLElement | null>(null)
const currentIndex = ref(0)
const isAnimating = ref(false)
const itemWidth = 200 // Width of each item + gap (from your CSS)
const itemsPerView = 5 // Number of items visible at once

const canScrollLeft = computed(() => currentIndex.value > 0)
const canScrollRight = computed(() => {
  const maxIndex = Math.max(0, props.items.length - itemsPerView)
  return currentIndex.value < maxIndex || props.hasMore
})

const scrollTo = async (index: number, loadMore = false) => {
  if (isAnimating.value) return

  // Check if we need to load more items
  if (loadMore && props.hasMore && !props.loading) {
    await props.onLoadMore()
  }

  isAnimating.value = true
  currentIndex.value = index

  if (containerRef.value) {
    containerRef.value.style.transform = `translateX(-${index * itemWidth}px)`
  }

  setTimeout(() => {
    isAnimating.value = false
  }, 300) // Match this with the CSS transition duration
}

const scrollPrev = () => {
  if (canScrollLeft.value) {
    scrollTo(Math.max(0, currentIndex.value - itemsPerView))
  }
}

const scrollNext = () => {
  if (canScrollRight.value) {
    const nextIndex = currentIndex.value + itemsPerView
    const needsMoreItems = nextIndex + itemsPerView > props.items.length
    scrollTo(nextIndex, needsMoreItems)
  }
}

// Reset position when items change
watch(() => props.items, () => {
  if (containerRef.value) {
    containerRef.value.style.transform = `translateX(-${currentIndex.value * itemWidth}px)`
  }
}, { deep: true })
</script>

<template>
  <div class="relative group">
    <!-- Previous Button -->
    <Button
      v-show="canScrollLeft"
      class="absolute left-5 top-1/2 -translate-y-1/2 -translate-x-4 z-10 rounded-full w-12 h-12 p-0 bg-background hover:bg-muted shadow-lg hover:shadow-xl border border-border transition-all duration-200"
      @click="scrollPrev"
    >
      <ChevronLeft class="h-5 w-5 text-foreground" />
    </Button>

    <!-- Carousel Container -->
    <div class="overflow-hidden">
      <div
        ref="containerRef"
        class="flex transition-transform duration-300 ease-in-out"
        :style="{ gap: '24px' }"
      >
        <slot :items="items" />
      </div>
    </div>

    <!-- Next Button -->
    <Button
      v-show="canScrollRight"
      class="absolute right-5 top-1/2 -translate-y-1/2 translate-x-4 z-10 rounded-full w-12 h-12 p-0 bg-background hover:bg-muted shadow-lg hover:shadow-xl transition-all duration-200"
      @click="scrollNext"
    >
      <ChevronRight class="h-5 w-5 text-foreground" />
    </Button>
  </div>
</template>

<style scoped>
.overflow-hidden {
  overflow: hidden;
  margin: 0 -16px;
  padding: 0 16px;
}
</style>
