<template>
  <section class="relative min-h-[95vh] w-full bg-gradient-to-bl from-primary-200 via-primary-600 to-primary-950 overflow-hidden">
    <!-- Wave Background -->
    <div class="absolute inset-0 z-0">
      <div class="wave wave1"></div>
      <div class="wave wave2"></div>
      <div class="wave wave3"></div>
    </div>
    <div class="container mx-auto px-4 py-20 min-h-[95vh] relative z-10">
      <!-- Left Column - Stats -->
      <div class="absolute -left-24 bottom-32 max-w-xs">
        <div class="max-w-md">
          <div class="border-l-2 border-secondary pl-4 mb-12">
            <p class="text-white/70 text-md">
              Discover the perfect fragrance for you with our wide selection of perfumes.
            </p>
          </div>

          <div class="space-y-6">
            <div>
              <h3 class="text-6xl font-afterglow text-secondary mb-1">200<span class="text-secondary-300">+</span></h3>
              <p class="text-white/80 text-lg">Perfumes</p>
            </div>
            <div>
              <h3 class="text-6xl font-afterglow text-secondary mb-1">15M<span class="text-secondary-300">+</span></h3>
              <p class="text-white/80 text-lg">Customers</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Center Column - Search -->
      <div class="max-w-5xl mx-auto text-center pt-36">
        <h1 class="text-5xl md:text-7xl lg:text-8xl font-afterglow mb-6 bg-gradient-to-r from-secondary via-secondary-300 to-secondary bg-clip-text text-transparent">
          Discover Your Signature
        </h1>
        <h1 class="text-5xl md:text-7xl font-afterglow mb-6 bg-gradient-to-r from-secondary via-secondary-300 to-secondary bg-clip-text text-transparent">
          Scent
        </h1>

        <!-- <p class="text-lg md:text-xl font-afterglow text-primary-800 mb-12">
          Explore our curated collection of luxury fragrances and find the perfect perfume that tells your story.
        </p> -->

        <!-- Advanced Search Bar -->
        <div class="relative max-w-3xl mx-auto p-[2px] rounded-lg bg-gradient-to-r from-secondary via-secondary-300 to-secondary mb-8">
          <div class="bg-primary-700 flex items-center max-w-4xl mx-auto rounded-lg divide-x divide-gray-600">
            <!-- Search Input -->
            <div class="flex-1 min-w-[200px] px-2 py-2">
              <Command class="rounded-lg border-0 shadow-none bg-primary-700">
                  <CommandInput class="h-10 text-white placeholder:text-gray-400" placeholder="Search perfumes..." />
              </Command>
            </div>

            <!-- Location Combobox -->
            <div class="flex-1 min-w-[200px] px-2 py-2">
              <Popover>
                <PopoverTrigger as-child>
                  <Button variant="ghost" role="combobox" class="w-full h-10 justify-between bg-primary-700 text-white hover:bg-primary-600 hover:text-white">
                      {{ selectedLocation || "Select location..." }}
                      <ChevronDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                  </Button>
                </PopoverTrigger>
                <PopoverContent class="w-full p-0">
                  <Command class="bg-primary-700">
                    <CommandInput class="text-white placeholder:text-gray-400" placeholder="Search location..." />
                    <CommandGroup class="text-white">
                      <CommandItem
                        v-for="location in locations"
                        :key="location"
                        :value="location"
                        @select="selectedLocation = location"
                        class="hover:bg-primary-600"
                      >
                        {{ location }}
                      </CommandItem>
                    </CommandGroup>
                  </Command>
                </PopoverContent>
              </Popover>
            </div>

            <!-- Date Combobox -->
            <div class="flex-1 min-w-[200px] px-2 py-2">
              <Popover>
                <PopoverTrigger as-child>
                  <Button variant="ghost" role="combobox" class="w-full h-10 justify-between bg-primary-700 text-white hover:bg-primary-600 hover:text-white">
                      {{ selectedDate || "Select date..." }}
                      <ChevronDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                  </Button>
                </PopoverTrigger>
                <PopoverContent class="w-full p-0">
                  <Command class="bg-primary-700">
                    <CommandInput class="text-white placeholder:text-gray-400" placeholder="Search date..." />
                    <CommandGroup class="text-white">
                      <CommandItem
                        v-for="date in dates"
                        :key="date"
                        :value="date"
                        @select="selectedDate = date"
                        class="hover:bg-primary-600"
                      >
                        {{ date }}
                      </CommandItem>
                    </CommandGroup>
                  </Command>
                </PopoverContent>
              </Popover>
            </div>

            <!-- Search Button -->
            <div class="px-2 py-2">
              <Button variant="secondary" >
                Search
              </Button>
            </div>

          </div>
        </div>

        <!-- Shop Now Section -->
        <div class="flex items-center justify-center gap-4 mt-12">
          <div class="w-24 h-[1px] bg-gradient-to-r from-transparent via-secondary to-secondary"></div>
          <Button variant="outline" class="border-secondary text-secondary bg-primary-700 hover:bg-secondary hover:text-white px-8 py-2 text-lg font-afterglow">
            Browse all!
          </Button>
          <div class="w-24 h-[1px] bg-gradient-to-l from-transparent via-secondary to-secondary"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem } from '@/components/ui/command'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { ChevronDown } from 'lucide-vue-next'

const selectedLocation = ref('')
const selectedDate = ref('')

// Example data - replace with your actual data
const locations = [
  'New York',
  'London',
  'Paris',
  'Tokyo',
  'Sydney'
]

const dates = [
  'Today',
  'Tomorrow',
  'This Week',
  'This Month',
  'Custom Date'
]
</script>

<style scoped>
.wave {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0.4;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.2));
  mask: url("data:image/svg+xml,%3Csvg viewBox='0 0 1000 300' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M 0 300 Q 150 250 300 300 T 600 300 T 1000 300 L 1000 0 L 0 0 Z' fill='white'/%3E%3C/svg%3E") repeat-x;
  mask-size: 1000px 300px;
  transform-origin: top;
}

.wave1 {
  animation: wave 20s cubic-bezier(0.36, 0.45, 0.63, 0.53) infinite;
  z-index: 1;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.3));
}

.wave2 {
  animation: wave 25s cubic-bezier(0.36, 0.45, 0.63, 0.53) -.125s infinite, swell 7s ease -1.25s infinite;
  opacity: 0.3;
  z-index: 2;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.2));
}

.wave3 {
  animation: wave 30s cubic-bezier(0.36, 0.45, 0.63, 0.53) -.25s infinite, swell 10s ease -2.5s infinite;
  opacity: 0.2;
  z-index: 3;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.1));
}

@keyframes wave {
  0% { mask-position: 1000px 0; }
  100% { mask-position: 0 0; }
}

@keyframes swell {
  0%, 100% { transform: translateY(-20px) scaleY(1); }
  50% { transform: translateY(20px) scaleY(1.1); }
}
</style>
