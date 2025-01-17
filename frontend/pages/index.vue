<script setup lang="ts">
import { ref, onMounted, onUnmounted, watchEffect } from 'vue'

useHead({
  title: 'Home - Parfum App',
  meta: [
    { name: 'description', content: 'Discover and explore your perfect fragrance with Parfum App' }
  ]
})

const titleNumber = ref(0)
const titles = ["Dream ", "Perfect ", "Signature ", "Next ", "Unique", "Ideal", "Favorite"]

const updateTitle = () => {
  titleNumber.value = (titleNumber.value + 1) % titles.length
}

let interval: NodeJS.Timeout

onMounted(() => {
  interval = setInterval(updateTitle, 4000)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<template>
  <div class="space-y-8">
    <section class="py-12 md:py-24">
      <div class="container flex flex-col items-center text-center">
        <h1 class="text-3xl font-bold leading-tight tracking-tighter md:text-5xl lg:text-6xl lg:leading-[1.1] text-center">
          <span class="block">Discover Your</span>
          <div class="relative h-[1.2em] overflow-hidden my-4">
            <TransitionGroup name="slide" tag="div" class="absolute inset-0 flex justify-center items-center">
              <span
                v-for="(title, index) in titles"
                :key="title"
                v-show="titleNumber === index"
                class="absolute font-semibold pb-1"
              >
                {{ title }}
              </span>
            </TransitionGroup>
          </div>
          <span class="block">Fragrance</span>
        </h1>
        <p class="mt-4 max-w-[700px] text-lg text-muted-foreground">
          Explore our curated collection of perfumes, find your signature scent, and learn about the art of fragrance.
        </p>
        <div class="mt-6 flex flex-wrap justify-center gap-4">
          <NuxtLink
            to="/browse"
            class="inline-flex h-10 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground ring-offset-background transition-colors hover:bg-primary/90"
          >
            Browse Collection
          </NuxtLink>
          <NuxtLink
            to="/search"
            class="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground"
          >
            Search Perfumes
          </NuxtLink>
        </div>
      </div>
    </section>

    <section class="py-8 md:py-16">
      <div class="container mb-12">
        <h2 class="mb-8 text-2xl font-bold tracking-tight">Featured Perfumes</h2>
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Placeholder for featured perfumes -->
          <div class="rounded-lg border bg-card text-card-foreground shadow-sm">
            <div class="p-6">
              <h3 class="text-lg font-semibold">Coming Soon</h3>
              <p class="text-sm text-muted-foreground">
                Featured perfumes will be displayed here
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="container mb-16">
        <h2 class="mb-8 text-2xl font-bold tracking-tight">Newest Perfumes</h2>
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Placeholder for featured perfumes -->
          <div class="rounded-lg border bg-card text-card-foreground shadow-sm">
            <div class="p-6">
              <h3 class="text-lg font-semibold">Coming Soon</h3>
              <p class="text-sm text-muted-foreground">
                Featured perfumes will be displayed here
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="container mb-12">
        <h2 class="mb-8 text-2xl font-bold tracking-tight">Most Popular Perfumes</h2>
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Placeholder for featured perfumes -->
          <div class="rounded-lg border bg-card text-card-foreground shadow-sm">
            <div class="p-6">
              <h3 class="text-lg font-semibold">Coming Soon</h3>
              <p class="text-sm text-muted-foreground">
                Featured perfumes will be displayed here
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template> 

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style> 