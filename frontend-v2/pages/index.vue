<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { usePerfumes } from '@/composables/usePerfumes'
import HeroSection from '@/components/ui/custom/HeroSection.vue'
import type { Perfume } from '~/types/api'
import { useBucketImages } from '@/composables/useShared'
import { ref, onMounted } from 'vue'
import { NuxtLink } from '#components'
import { Skeleton } from '@/components/ui/skeleton'
import Carousel from '@/components/ui/custom/Carousel.vue'
import AnimatedLogoCloud from '@/components/ui/custom/AnimatedLogoCloud.vue'

// Import brand logos
import ChanelLogo from '~/assets/images/Chanel.png'
import DiorLogo from '~/assets/images/Dior.png'
import BvlgariLogo from '~/assets/images/Bvlgari.png'
import HermesLogo from '~/assets/images/Hermes.png'
import TomFordLogo from '~/assets/images/TomFord.png'
import VersaceLogo from '~/assets/images/Versace.png'
import PradaLogo from '~/assets/images/Prada.png'
import GivenchyLogo from '~/assets/images/Givenchy.png'
import ValentinoLogo from '~/assets/images/Valentino.png'
import YSLLogo from '~/assets/images/YvesSaintLaurent.png'
import AzzaroLogo from '~/assets/images/Azzaro.png'

const { getTrendingPerfumes, getTopRatedPerfumes, getMostLovedPerfumes } = usePerfumes()

const trendingPerfumes = ref<Perfume[]>([])
const topRatedPerfumes = ref<Perfume[]>([])
const mostLovedPerfumes = ref<Perfume[]>([])
const imageUrls = ref<Record<string, string>>({})

const loading = ref({
    trending: false,
    topRated: false,
    mostLoved: false
})

const currentPage = ref({
    trending: 1,
    topRated: 1,
    mostLoved: 1
})

const hasMore = ref({
    trending: true,
    topRated: true,
    mostLoved: true
})

const brandLogos = ref([
  {
    name: 'Chanel',
    path: ChanelLogo
  },
  {
    name: 'Dior',
    path: DiorLogo
  },
  {
    name: 'Bvlgari',
    path: BvlgariLogo
  },
  {
    name: 'Hermes',
    path: HermesLogo
  },
  {
    name: 'Tom Ford',
    path: TomFordLogo
  },
  {
    name: 'Versace',
    path: VersaceLogo
  },
  {
    name: 'Prada',
    path: PradaLogo
  },
  {
    name: 'Givenchy',
    path: GivenchyLogo
  },
  {
    name: 'Valentino',
    path: ValentinoLogo
  },
  {
    name: 'YSL',
    path: YSLLogo
  },
  {
    name: 'Azzaro',
    path: AzzaroLogo
  }
])

const loadMore = async (section: 'trending' | 'topRated' | 'mostLoved') => {
    if (loading.value[section] || !hasMore.value[section]) return

    loading.value[section] = true
    try {
        let newPerfumes: Perfume[] = []
        switch (section) {
            case 'trending':
                newPerfumes = await getTrendingPerfumes(currentPage.value[section])
                break
            case 'topRated':
                newPerfumes = await getTopRatedPerfumes(currentPage.value[section])
                break
            case 'mostLoved':
                newPerfumes = await getMostLovedPerfumes(currentPage.value[section])
                break
        }

        if (newPerfumes.length === 0) {
            hasMore.value[section] = false
        } else {
            switch (section) {
                case 'trending':
                    trendingPerfumes.value.push(...newPerfumes)
                    break
                case 'topRated':
                    topRatedPerfumes.value.push(...newPerfumes)
                    break
                case 'mostLoved':
                    mostLovedPerfumes.value.push(...newPerfumes)
                    break
            }
            currentPage.value[section]++
            await loadImages(newPerfumes)
        }
    } finally {
        loading.value[section] = false
    }
}

const loadImages = async (perfumes: Perfume[]) => {
    for (const perfume of perfumes) {
        if (perfume.local_image_path && !imageUrls.value[perfume.local_image_path]) {
            imageUrls.value[perfume.local_image_path] = await useBucketImages('perfume_images', perfume.local_image_path)
        }
    }
}

onMounted(async () => {
    await Promise.all([
        loadMore('trending'),
        loadMore('topRated'),
        loadMore('mostLoved')
    ])
})
</script>

<template>
    <HeroSection />
    <div class="container mx-auto px-4 py-8 space-y-12">
        <!-- Trending Now Section -->
        <section>
            <div class="mb-6">
                <h2 class="text-2xl font-bold font-afterglow">Trending Now</h2>
                <div class="w-36 h-[2px] mt-2 bg-gradient-to-r from-transparent via-secondary to-secondary"></div>
            </div>
            <div class="relative">
                <template v-if="!loading.trending || trendingPerfumes.length > 0">
                    <Carousel
                        :items="trendingPerfumes"
                        :loading="loading.trending"
                        :has-more="hasMore.trending"
                        :on-load-more="() => loadMore('trending')"
                    >
                        <template #default="{ items }">
                            <NuxtLink 
                                v-for="perfume in items" 
                                :key="perfume.id" 
                                :to="`/perfume/${perfume.id}`"
                                class="flex-none w-[200px] group hover:opacity-95 transition-opacity"
                            >
                                <div class="relative overflow-hidden rounded-lg aspect-square mb-3">
                                    <img 
                                        :src="imageUrls[perfume.local_image_path]"
                                        :alt="perfume.name"
                                        class="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
                                    />
                                </div>
                                <h3 class="font-medium text-foreground">{{ perfume.brands?.name }}</h3>
                                <p class="text-sm text-muted-foreground">{{ perfume.name }}</p>
                            </NuxtLink>
                        </template>
                    </Carousel>
                </template>
                <template v-if="loading.trending && trendingPerfumes.length === 0">
                    <div class="flex gap-6">
                        <div v-for="n in 5" :key="n" class="flex-none w-[200px]">
                            <Skeleton class="aspect-square mb-3 rounded-lg" />
                            <Skeleton class="h-4 w-3/4 mb-2" />
                            <Skeleton class="h-4 w-1/2" />
                        </div>
                    </div>
                </template>
            </div>
        </section>

        <!-- Top Rated Section -->
        <section>
            <div class="mb-6">
                <h2 class="text-2xl font-bold font-afterglow">Top Rated</h2>
                <div class="w-36 h-[2px] mt-2 bg-gradient-to-r from-transparent via-secondary to-secondary"></div>
            </div>
            <div class="relative">
                <template v-if="!loading.topRated || topRatedPerfumes.length > 0">
                    <Carousel
                        :items="topRatedPerfumes"
                        :loading="loading.topRated"
                        :has-more="hasMore.topRated"
                        :on-load-more="() => loadMore('topRated')"
                    >
                        <template #default="{ items }">
                            <NuxtLink 
                                v-for="perfume in items" 
                                :key="perfume.id" 
                                :to="`/perfume/${perfume.id}`"
                                class="flex-none w-[200px] group hover:opacity-95 transition-opacity"
                            >
                                <div class="relative overflow-hidden rounded-lg aspect-square mb-3">
                                    <img 
                                        :src="imageUrls[perfume.local_image_path]"
                                        :alt="perfume.name"
                                        class="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
                                    />
                                </div>
                                <h3 class="font-medium text-foreground">{{ perfume.brands?.name }}</h3>
                                <p class="text-sm text-muted-foreground">{{ perfume.name }}</p>
                            </NuxtLink>
                        </template>
                    </Carousel>
                </template>
                <template v-if="loading.topRated && topRatedPerfumes.length === 0">
                    <div class="flex gap-6">
                        <div v-for="n in 5" :key="n" class="flex-none w-[200px]">
                            <Skeleton class="aspect-square mb-3 rounded-lg" />
                            <Skeleton class="h-4 w-3/4 mb-2" />
                            <Skeleton class="h-4 w-1/2" />
                        </div>
                    </div>
                </template>
            </div>
        </section>

        <!-- Most Loved Section -->
        <section>
            <div class="mb-6">
                <h2 class="text-2xl font-bold font-afterglow">Most Loved</h2>
                <div class="w-36 h-[2px] mt-2 bg-gradient-to-r from-transparent via-secondary to-secondary"></div>
            </div>
            <div class="relative">
                <template v-if="!loading.mostLoved || mostLovedPerfumes.length > 0">
                    <Carousel
                        :items="mostLovedPerfumes"
                        :loading="loading.mostLoved"
                        :has-more="hasMore.mostLoved"
                        :on-load-more="() => loadMore('mostLoved')"
                    >
                        <template #default="{ items }">
                            <NuxtLink 
                                v-for="perfume in items" 
                                :key="perfume.id" 
                                :to="`/perfume/${perfume.id}`"
                                class="flex-none w-[200px] group hover:opacity-95 transition-opacity"
                            >
                                <div class="relative overflow-hidden rounded-lg aspect-square mb-3">
                                    <img 
                                        :src="imageUrls[perfume.local_image_path]"
                                        :alt="perfume.name"
                                        class="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
                                    />
                                </div>
                                <h3 class="font-medium text-foreground">{{ perfume.brands?.name }}</h3>
                                <p class="text-sm text-muted-foreground">{{ perfume.name }}</p>
                            </NuxtLink>
                        </template>
                    </Carousel>
                </template>
                <template v-if="loading.mostLoved && mostLovedPerfumes.length === 0">
                    <div class="flex gap-6">
                        <div v-for="n in 5" :key="n" class="flex-none w-[200px]">
                            <Skeleton class="aspect-square mb-3 rounded-lg" />
                            <Skeleton class="h-4 w-3/4 mb-2" />
                            <Skeleton class="h-4 w-1/2" />
                        </div>
                    </div>
                </template>
            </div>
        </section>
        <section class="py-8">
            <AnimatedLogoCloud
                :logos="brandLogos"
                title="Trusted by Luxury Brands"
                class="opacity-75"
            />
            
        </section>
    </div>
</template>

<style scoped>
</style>