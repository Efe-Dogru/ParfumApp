<script setup lang="ts">
useHead({
  title: 'Fragrance Notes - Parfum App',
  meta: [
    { name: 'description', content: 'Explore different fragrance notes and accords' }
  ]
})
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <div class="mx-auto">
      <h1 class="text-4xl font-bold mb-8">Fragrance Notes</h1>
      
      <div class="space-y-8">
        <!-- Introduction -->
        <section class="prose dark:prose-invert">
          <p class="text-lg text-muted-foreground">
            Explore the building blocks of fragrances. From fresh citrus to warm amber, 
            discover the notes that create your favorite scents.
          </p>
        </section>

        <!-- Note Categories -->
        <section class="grid gap-6">
          <h2 class="text-2xl font-semibold">Note Categories</h2>
          <div class="grid md:grid-cols-3 gap-6">
            <div class="p-6 rounded-lg border bg-card">
              <h3 class="text-xl font-medium mb-2">Top Notes</h3>
              <p class="text-muted-foreground">
                The initial impression of a fragrance, typically light and fresh.
              </p>
            </div>
            <div class="p-6 rounded-lg border bg-card">
              <h3 class="text-xl font-medium mb-2">Heart Notes</h3>
              <p class="text-muted-foreground">
                The main character of the fragrance that emerges after the top notes fade.
              </p>
            </div>
            <div class="p-6 rounded-lg border bg-card">
              <h3 class="text-xl font-medium mb-2">Base Notes</h3>
              <p class="text-muted-foreground">
                The foundation that gives the fragrance its depth and longevity.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
