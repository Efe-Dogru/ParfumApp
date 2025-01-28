<script setup lang="ts">
import { usePerfumes } from '@/composables/usePerfumes'
import type { Perfume } from '~/types/api'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
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
import { useBucketImages } from '@/composables/useShared'
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { Skeleton } from '@/components/ui/skeleton'
import { NuxtLink } from '#components'

// Define the directive at the top
const vObserveVisibility = {
  mounted: (el: HTMLElement, { value }: { value: (el: HTMLElement) => void }) => {
    value(el)
  }
}

const { getPerfumes } = usePerfumes()
const currentPage = ref(1)
const itemsPerPage = 42
const totalItems = ref(0)
const perfumes = ref<Perfume[] | null>(null)
const imageUrls = ref<Record<string, string>>({})
const loading = ref(true)
const observer = ref<IntersectionObserver | null>(null)

const loadImage = async (perfume: Perfume) => {
  if (perfume.local_image_path && !imageUrls.value[perfume.local_image_path]) {
    try {
      imageUrls.value[perfume.local_image_path] = await useBucketImages('perfume_images', perfume.local_image_path)
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
          const perfumeId = entry.target.getAttribute('data-perfume-id')
          const perfume = perfumes.value?.find(p => p.id.toString() === perfumeId)
          if (perfume) {
            loadImage(perfume)
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

onMounted(() => {
  setupIntersectionObserver()
})

onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
})

const fetchPerfumes = async (page: number) => {
  loading.value = true
  try {
    const result = await getPerfumes(page, itemsPerPage)
    perfumes.value = result.data
    totalItems.value = result.count
  } catch (error) {
    console.error('Error fetching perfumes:', error)
  } finally {
    loading.value = false
  }
}

// Move initialization to onMounted
onMounted(async () => {
  await fetchPerfumes(currentPage.value)
})

watch(currentPage, async (newPage) => {
  await fetchPerfumes(newPage)
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>

<template>
  <div class="space-y-6">
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      <template v-if="loading">
        <Card v-for="n in itemsPerPage" :key="n" class="overflow-hidden">
          <CardHeader>
            <Skeleton class="w-full h-[200px]" />
          </CardHeader>
          <CardContent>
            <Skeleton class="h-6 w-3/4 mb-2" />
          </CardContent>
          <CardFooter>
            <Skeleton class="h-6 w-1/2" />
          </CardFooter>
        </Card>
      </template>
      <template v-else>
        <NuxtLink 
          v-for="perfume in perfumes || []" 
          :key="perfume.id" 
          :to="`/perfume/${perfume.id}`"
          class="block h-full"
        >
          <Card class="overflow-hidden hover:shadow-lg transition-shadow h-full">
            <CardHeader>
              <div 
                :data-perfume-id="perfume.id"
                v-observe-visibility="observeImage"
                class="w-full h-[200px] bg-muted"
              >
                <img 
                  v-if="imageUrls[perfume.local_image_path]"
                  :src="imageUrls[perfume.local_image_path]" 
                  :alt="perfume.name"
                  class="w-full h-full object-cover rounded-t-lg"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <Skeleton class="w-full h-full" />
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <CardTitle class="text-xl">{{ perfume.name }}</CardTitle>
            </CardContent>
            <CardFooter>
              <CardTitle class="text-xl mb-2">{{ perfume.brands.name }}</CardTitle>
            </CardFooter>
          </Card>
        </NuxtLink>
      </template>
    </div>

    <div class="flex justify-center mt-6">
      <Pagination 
        v-slot="{ page }" 
        :total="100"
        :per-page="itemsPerPage"
        :sibling-count="1" 
        show-edges 
        :default-page="1"
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