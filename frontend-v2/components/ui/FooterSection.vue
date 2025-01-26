<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Facebook, Instagram, Linkedin, Moon, Send, Sun, Twitter } from 'lucide-vue-next'
import { useTheme } from '~/composables/useTheme'

const { isDark, toggleDarkMode, initTheme } = useTheme()

onMounted(() => {
  initTheme()
})
</script>

<template>
  <footer class="relative border-t bg-background text-foreground transition-colors duration-300">
    <div class="container mx-auto px-4 py-12 md:px-6 lg:px-8">
      <div class="grid gap-12 md:grid-cols-2 lg:grid-cols-4">
        <div class="relative">
          <h2 class="mb-4 text-3xl font-bold tracking-tight">Stay Connected</h2>
          <p class="mb-6 text-muted-foreground">
            Join our newsletter for the latest updates and exclusive offers.
          </p>
          <form class="relative">
            <input
              type="email"
              placeholder="Enter your email"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background pr-12 backdrop-blur-sm"
            />
            <button
              type="submit"
              class="absolute right-1 top-1 h-8 w-8 rounded-full bg-[#4A154B] text-white transition-transform hover:scale-105 inline-flex items-center justify-center"
            >
              <Send class="h-4 w-4" />
              <span class="sr-only">Subscribe</span>
            </button>
          </form>
          <div class="absolute -right-4 top-0 h-24 w-24 rounded-full bg-[#4A154B]/10 blur-2xl" />
        </div>
        <div>
          <h3 class="mb-4 text-lg font-semibold">Quick Links</h3>
          <nav class="space-y-2 text-sm">
            <NuxtLink to="/" class="block transition-colors hover:text-[#4A154B]">
              Home
            </NuxtLink>
            <NuxtLink to="/" class="block transition-colors hover:text-[#4A154B]">
              About Us
            </NuxtLink>
            <NuxtLink to="/perfumes" class="block transition-colors hover:text-[#4A154B]">
              Products
            </NuxtLink>
            <NuxtLink to="/notes" class="block transition-colors hover:text-[#4A154B]">
              Search
            </NuxtLink>
          </nav>
        </div>
        <div>
          <h3 class="mb-4 text-lg font-semibold">Contact Us</h3>
          <address class="space-y-2 text-sm not-italic">
            <p>123 Innovation Street</p>
            <p>Tech City, TC 12345</p>
            <p>Phone: (123) 456-7890</p>
            <p>Email: hello@example.com</p>
          </address>
        </div>
        <div class="relative">
          <h3 class="mb-4 text-lg font-semibold">Follow Us</h3>
          <div class="mb-6 flex space-x-4">
            <button class="inline-flex items-center justify-center rounded-full border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <Facebook class="h-4 w-4" />
              <span class="sr-only">Facebook</span>
            </button>
            <button class="inline-flex items-center justify-center rounded-full border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <Twitter class="h-4 w-4" />
              <span class="sr-only">Twitter</span>
            </button>
            <button class="inline-flex items-center justify-center rounded-full border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <Instagram class="h-4 w-4" />
              <span class="sr-only">Instagram</span>
            </button>
            <button class="inline-flex items-center justify-center rounded-full border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <Linkedin class="h-4 w-4" />
              <span class="sr-only">LinkedIn</span>
            </button>
          </div>
          <div class="flex items-center space-x-2">
            <Sun class="h-4 w-4" />
            <button 
              @click="toggleDarkMode"
              class="inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50"
              :class="isDark ? 'bg-[#4A154B]' : 'bg-input'"
            >
              <span
                class="pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform"
                :class="isDark ? 'translate-x-5' : 'translate-x-0'"
              />
            </button>
            <Moon class="h-4 w-4" />
            <label for="dark-mode" class="sr-only">
              Toggle dark mode
            </label>
          </div>
        </div>
      </div>
      <div class="mt-12 flex flex-col items-center justify-between gap-4 border-t pt-8 text-center md:flex-row">
        <p class="text-sm text-muted-foreground">
          © 2024 Your Company. All rights reserved.
        </p>
        <nav class="flex gap-4 text-sm">
          <a href="#" class="transition-colors hover:text-[#4A154B]">
            Privacy Policy
          </a>
          <a href="#" class="transition-colors hover:text-[#4A154B]">
            Terms of Service
          </a>
          <a href="#" class="transition-colors hover:text-[#4A154B]">
            Cookie Settings
          </a>
        </nav>
      </div>
    </div>
  </footer>
</template> 