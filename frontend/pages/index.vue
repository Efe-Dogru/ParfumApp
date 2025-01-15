<script setup lang="ts">
useHead({
  title: 'Home - Parfum App',
  meta: [
    { name: 'description', content: 'Discover and explore your perfect fragrance with Parfum App' }
  ]
})
</script>

<template>
  <div class="space-y-8">
    <section class="py-12 md:py-24">
      <div class="container flex flex-col items-center text-center">
        <h1 class="text-3xl font-bold leading-tight tracking-tighter md:text-5xl lg:text-6xl lg:leading-[1.1]">
          Discover Your Perfect Fragrance
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

    <section class="py-8 md:py-12">
      <div class="container">
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
    </section>
  </div>
</template> 