<template>
  <div class="min-h-screen bg-background">
    <header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div class="container flex h-14 items-center">
        <NuxtLink to="/" class="mr-6 flex items-center space-x-2">
          <span class="font-bold">Parfum App</span>
        </NuxtLink>
        <nav class="flex items-center space-x-6 text-sm font-medium">
          <NuxtLink
            to="/"
            class="transition-colors hover:text-foreground/80 text-foreground"
          >
            Home
          </NuxtLink>
          <NuxtLink
            to="/browse"
            class="transition-colors hover:text-foreground/80 text-foreground"
          >
            Browse
          </NuxtLink>
          <NuxtLink
            to="/search"
            class="transition-colors hover:text-foreground/80 text-foreground"
          >
            Search
          </NuxtLink>
        </nav>
      </div>
    </header>

    <main class="container py-6">
      <slot />
    </main>

    <footer class="border-t py-6 md:py-0">
      <div class="container flex h-14 items-center">
        <p class="text-sm text-foreground/60">
          &copy; {{ new Date().getFullYear() }} Parfum App. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template> 