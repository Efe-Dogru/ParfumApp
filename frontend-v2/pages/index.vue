<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { usePerfumes } from '@/composables/usePerfumes'
import type { Perfume } from '~/types/perfume'
import { useBucketImages } from '@/composables/useShared'
import { ref, onMounted } from 'vue'
import { NuxtLink } from '#components'

const { getTrendingPerfumes, getTopRatedPerfumes, getMostLovedPerfumes } = usePerfumes()

const trendingPerfumes = ref<Perfume[]>([])
const topRatedPerfumes = ref<Perfume[]>([])
const mostLovedPerfumes = ref<Perfume[]>([])
const imageUrls = ref<Record<string, string>>({})

const loadImages = async () => {
    const allPerfumes = [...trendingPerfumes.value, ...topRatedPerfumes.value, ...mostLovedPerfumes.value]
    for (const perfume of allPerfumes) {
        if (perfume.local_image_path && !imageUrls.value[perfume.local_image_path]) {
            imageUrls.value[perfume.local_image_path] = await useBucketImages('perfume_images', perfume.local_image_path)
        }
    }
}

onMounted(async () => {
    trendingPerfumes.value = await getTrendingPerfumes()
    topRatedPerfumes.value = await getTopRatedPerfumes()
    mostLovedPerfumes.value = await getMostLovedPerfumes()
    await loadImages()
})
</script>

<template>
        <CustomHeroSection />
        <div class="container mx-auto px-4 py-8 space-y-12">
            <!-- Trending Now Section -->
            <section>
                <h2 class="text-2xl font-bold mb-6">Trending Now</h2>
                <div class="relative">
                    <div class="flex overflow-x-auto gap-6 pb-4 snap-x snap-mandatory hide-scrollbar">
                        <NuxtLink 
                            v-for="perfume in trendingPerfumes" 
                            :key="perfume.id" 
                            :to="`/perfume/${perfume.id}`"
                            class="flex-none w-[200px] snap-start group hover:opacity-95 transition-opacity"
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
                    </div>
                </div>
            </section>

            <!-- Top Rated Section -->
            <section>
                <h2 class="text-2xl font-bold mb-6">Top Rated</h2>
                <div class="relative">
                    <div class="flex overflow-x-auto gap-6 pb-4 snap-x snap-mandatory hide-scrollbar">
                        <NuxtLink 
                            v-for="perfume in topRatedPerfumes" 
                            :key="perfume.id" 
                            :to="`/perfume/${perfume.id}`"
                            class="flex-none w-[200px] snap-start group hover:opacity-95 transition-opacity"
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
                    </div>
                </div>
            </section>

            <!-- Most Loved Section -->
            <section>
                <h2 class="text-2xl font-bold mb-6">Most Loved</h2>
                <div class="relative">
                    <div class="flex overflow-x-auto gap-6 pb-4 snap-x snap-mandatory hide-scrollbar">
                        <NuxtLink 
                            v-for="perfume in mostLovedPerfumes" 
                            :key="perfume.id" 
                            :to="`/perfume/${perfume.id}`"
                            class="flex-none w-[200px] snap-start group hover:opacity-95 transition-opacity"
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
                    </div>
                </div>
            </section>
    </div>
</template>

<style scoped>
.hide-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
.hide-scrollbar::-webkit-scrollbar {
    display: none;
}
</style>