<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import InteractiveHoverButton from '../components/ui/InteractiveHoverButton.vue'
import { Droplets, Star, Package, Sparkles, TrendingUp, Search, MapPin, Calendar, Clock, Tag, Store } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedCategory = ref('')
const searchQuery = ref('')
const isNotesDropdownOpen = ref(false)
const notesSearchQuery = ref('')
const selectedNotes = ref<string[]>([])
const isBrandsDropdownOpen = ref(false)
const brandsSearchQuery = ref('')
const selectedBrands = ref<string[]>([])

const categories = [
  { name: 'Perfumes', icon: Droplets, path: '/browse', placeholder: 'Search for perfumes...' },
  { name: 'Brands', icon: Star, path: '/brands', placeholder: 'Search for brands...' },
  { name: 'Collections', icon: Package, path: '/collections', placeholder: 'Search for collections...' }
]

const mockNotes = [
  'Vanilla', 'Rose', 'Oud', 'Bergamot', 'Jasmine', 
  'Sandalwood', 'Amber', 'Musk', 'Lavender', 'Patchouli',
  'Cedar', 'Vetiver', 'Orange Blossom', 'Ylang-Ylang', 'Neroli'
]

const mockBrands = [
  'Chanel', 'Dior', 'Tom Ford', 'Jo Malone', 'Gucci',
  'Hermès', 'Yves Saint Laurent', 'Creed', 'Byredo', 'Le Labo',
  'Maison Francis Kurkdjian', 'Diptyque', 'Acqua di Parma', 'Versace', 'Prada'
]

const filteredNotes = computed(() => {
  if (!notesSearchQuery.value) return mockNotes
  return mockNotes.filter(note => 
    note.toLowerCase().includes(notesSearchQuery.value.toLowerCase())
  )
})

const filteredBrands = computed(() => {
  if (!brandsSearchQuery.value) return mockBrands
  return mockBrands.filter(brand => 
    brand.toLowerCase().includes(brandsSearchQuery.value.toLowerCase())
  )
})

const toggleNote = (note: string) => {
  const index = selectedNotes.value.indexOf(note)
  if (index === -1) {
    if (selectedNotes.value.length < 4) {
      selectedNotes.value.push(note)
      notesSearchQuery.value = ''
    }
  } else {
    selectedNotes.value.splice(index, 1)
  }
  if (selectedNotes.value.length === 4) {
    isNotesDropdownOpen.value = false
  }
}

const toggleBrand = (brand: string) => {
  const index = selectedBrands.value.indexOf(brand)
  if (index === -1) {
    selectedBrands.value.push(brand)
    brandsSearchQuery.value = ''
  } else {
    selectedBrands.value.splice(index, 1)
  }
}

const handleSearch = () => {
  if (!searchQuery.value) return
  
  const category = categories.find(c => c.name === selectedCategory.value)
  if (category) {
    router.push({
      path: category.path,
      query: { search: searchQuery.value }
    })
  }
}

useHead({
  title: 'Home - Parfum App',
  meta: [
    { name: 'description', content: 'Discover and explore your perfect fragrance with Parfum App' }
  ]
})

const titleNumber = ref(0)
const titles = ["Dream ", "Perfect ", "Next ", "Unique", "Ideal", "Favorite"]


const updateTitle = () => {
  titleNumber.value = (titleNumber.value + 1) % titles.length
}
let interval: NodeJS.Timeout

// Mouse follower logic
const mouseX = ref(0)
const mouseY = ref(0)
const followerX = ref(0)
const followerY = ref(0)

const updateMousePosition = (event: MouseEvent) => {
  mouseX.value = event.clientX
  mouseY.value = event.clientY
}

const updateFollowerPosition = () => {
  const dx = mouseX.value - followerX.value
  const dy = mouseY.value - followerY.value
  
  followerX.value += dx * 0.2
  followerY.value += dy * 0.2
  
  requestAnimationFrame(updateFollowerPosition)
}

const openNotesDropdown = () => {
  isBrandsDropdownOpen.value = false
  isNotesDropdownOpen.value = true
}

const openBrandsDropdown = () => {
  isNotesDropdownOpen.value = false
  isBrandsDropdownOpen.value = true
}

onMounted(() => {
  interval = setInterval(updateTitle, 4000)
  window.addEventListener('mousemove', updateMousePosition)
  updateFollowerPosition()
  document.addEventListener('click', (event) => {
    const notesDropdown = document.getElementById('notes-dropdown')
    const notesInput = document.getElementById('notes-input')
    const notesContainer = document.getElementById('notes-container')
    const brandsDropdown = document.getElementById('brands-dropdown')
    const brandsInput = document.getElementById('brands-input')
    const brandsContainer = document.getElementById('brands-container')
    
    if (!notesDropdown?.contains(event.target as Node) && 
        !notesInput?.contains(event.target as Node) && 
        !notesContainer?.contains(event.target as Node)) {
      isNotesDropdownOpen.value = false
    }
    
    if (!brandsDropdown?.contains(event.target as Node) && 
        !brandsInput?.contains(event.target as Node) && 
        !brandsContainer?.contains(event.target as Node)) {
      isBrandsDropdownOpen.value = false
    }
  })
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
  window.removeEventListener('mousemove', updateMousePosition)
})
</script>

<template>
  <div class="relative min-h-screen">
    <!-- Hero section with full-width gradient background -->
    <section class="relative min-h-[910px]">
      <div class="background-animation rounded-b-[4rem]">
        <div 
          class="mouse-follower"
          :style="{
            transform: `translate(${followerX}px, ${followerY}px) translate(-50%, -50%)`
          }"
        >
          <div v-for="n in 12" :key="n" class="sparkle"></div>
        </div>
        <div v-for="n in 20" :key="`bg-sparkle-${n}`" class="sparkle"></div>
        <div class="mist-container">
          <div v-for="n in 20" :key="n" class="mist-particle"></div>
        </div>
        <div class="luxury-overlay"></div>
      </div>
      
      <!-- Hero content -->
      <div class="relative z-10">
        <div class="container mx-auto px-4 flex flex-col items-center text-center pt-48 pb-24 md:pt-64 md:pb-32">
          <h1 class="text-3xl font-bold leading-tight tracking-tighter md:text-5xl lg:text-6xl lg:leading-[1.1] text-center">
            <div class="flex flex-col items-center">
              <span>Discover Your</span>
              <div class="flex items-center gap-3">
                <!-- <div class="relative h-[1.2em] w-[200px] overflow-hidden">
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
                </div> -->
                <span>Next Fragrance</span>
              </div>
            </div>
          </h1>
          <p class="mt-4 max-w-[700px] text-lg text-muted-foreground">
            Explore our curated collection of perfumes, find your signature scent, and learn about the art of fragrance.
          </p>

          <div class="mt-12 w-full max-w-5xl mx-auto">
            <div class="flex bg-background/80 backdrop-blur-sm rounded-full shadow-lg border border-[#18181B] dark:border-white">
              <div class="flex items-center px-4 w-[400px]">
                <Search class="w-6 h-6 text-gray-600 mr-2" />
                <input
                  type="text"
                  placeholder="Search for perfumes..."
                  class="bg-transparent border-none focus:outline-none py-4 w-full"
                />
              </div>
              <div class="flex items-center px-4 w-[300px] border-l border-[#18181B] dark:border-white">
                <Tag class="w-6 h-6 text-gray-600 mr-2 shrink-0" />
                <div id="notes-container" class="relative w-[250px]">
                  <div 
                    class="flex items-center h-[40px] cursor-pointer"
                    @click.stop="openNotesDropdown"
                  >
                    <div class="flex items-center gap-1 overflow-x-auto overflow-y-hidden whitespace-nowrap no-scrollbar px-3">
                      <div
                        v-for="note in selectedNotes"
                        :key="note"
                        class="bg-primary/10 text-xs rounded-full px-2 py-1 flex items-center gap-1 shrink-0"
                      >
                        {{ note }}
                        <button @click.stop="toggleNote(note)" class="hover:text-primary">×</button>
                      </div>
                      <input
                        id="notes-input"
                        readonly
                        :placeholder="selectedNotes.length === 0 ? 'Search notes...' : ''"
                        class="bg-transparent border-none focus:outline-none w-[100px] h-[40px] shrink-0 pointer-events-none"
                      />
                    </div>
                  </div>
                  <!-- Notes Dropdown -->
                  <div
                    id="notes-dropdown"
                    v-if="isNotesDropdownOpen && selectedNotes.length < 4"
                    class="absolute top-[45px] left-[-48px] w-[300px] max-h-[300px] bg-background rounded-lg shadow-lg border z-50"
                  >
                    <div class="sticky top-0 bg-background border-b px-3 py-2 z-10">
                      <div class="relative">
                        <Search class="absolute left-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <input
                          type="text"
                          v-model="notesSearchQuery"
                          placeholder="Search notes..."
                          class="w-full pl-8 pr-3 py-1 text-sm bg-muted/50 border-none rounded-md focus:outline-none focus:ring-1 focus:ring-primary"
                        />
                      </div>
                    </div>
                    <div class="overflow-y-auto max-h-[250px]">
                      <div
                        v-for="note in filteredNotes"
                        :key="note"
                        @click="toggleNote(note)"
                        class="px-4 py-2 hover:bg-muted cursor-pointer flex items-center gap-2"
                        :class="{ 'opacity-50 cursor-not-allowed': selectedNotes.includes(note) }"
                      >
                        <div class="w-4 h-4 border rounded-sm flex items-center justify-center"
                             :class="{ 'bg-primary border-primary': selectedNotes.includes(note) }">
                          <div v-if="selectedNotes.includes(note)" class="w-2 h-2 bg-background rounded-sm"></div>
                        </div>
                        {{ note }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex items-center px-4 w-[300px] border-l border-[#18181B] dark:border-white">
                <Store class="w-6 h-6 text-gray-600 mr-2 shrink-0" />
                <div id="brands-container" class="relative w-[250px]">
                  <div 
                    class="flex items-center h-[40px] cursor-pointer"
                    @click.stop="openBrandsDropdown"
                  >
                    <div class="flex items-center gap-1 overflow-x-auto overflow-y-hidden whitespace-nowrap no-scrollbar pr-2">
                      <div
                        v-for="brand in selectedBrands"
                        :key="brand"
                        class="bg-primary/10 text-xs rounded-full px-2 py-1 flex items-center gap-1 shrink-0"
                      >
                        {{ brand }}
                        <button @click.stop="toggleBrand(brand)" class="hover:text-primary">×</button>
                      </div>
                      <input
                        id="brands-input"
                        readonly
                        :placeholder="selectedBrands.length === 0 ? 'Search brands...' : ''"
                        class="bg-transparent border-none focus:outline-none w-[100px] h-[40px] shrink-0 pointer-events-none"
                      />
                    </div>
                  </div>
                  <!-- Brands Dropdown -->
                  <div
                    id="brands-dropdown"
                    v-if="isBrandsDropdownOpen"
                    class="absolute top-[45px] left-[-48px] w-[300px] max-h-[300px] bg-background rounded-lg shadow-lg border z-50"
                  >
                    <div class="sticky top-0 bg-background border-b px-3 py-2 z-10">
                      <div class="relative">
                        <Search class="absolute left-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <input
                          type="text"
                          v-model="brandsSearchQuery"
                          placeholder="Search brands..."
                          class="w-full pl-8 pr-3 py-1 text-sm bg-muted/50 border-none rounded-md focus:outline-none focus:ring-1 focus:ring-primary"
                        />
                      </div>
                    </div>
                    <div class="overflow-y-auto max-h-[250px]">
                      <div
                        v-for="brand in filteredBrands"
                        :key="brand"
                        @click="toggleBrand(brand)"
                        class="px-4 py-2 hover:bg-muted cursor-pointer flex items-center gap-2"
                        :class="{ 'opacity-50 cursor-not-allowed': selectedBrands.includes(brand) }"
                      >
                        <div class="w-4 h-4 border rounded-sm flex items-center justify-center"
                             :class="{ 'bg-primary border-primary': selectedBrands.includes(brand) }">
                          <div v-if="selectedBrands.includes(brand)" class="w-2 h-2 bg-background rounded-sm"></div>
                        </div>
                        {{ brand }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex items-center border-l border-[#18181B] dark:border-white">
                <button class="px-8 py-4 bg-[#18181B] text-white rounded-r-full hover:bg-[#18181B]/90 transition-colors dark:bg-white dark:text-[#18181B] dark:hover:bg-white/90">
                  Search
                </button>
              </div>
            </div>
            <div class="mt-12 text-center">
              <span class="font-semibold text-2xl text-gray-600 dark:text-gray-200">518.787</span>
              <span class="ml-2 text-xl text-gray-600 dark:text-gray-300">Total perfumes</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Content sections with white background -->
    <div class="w-full bg-background relative z-10">
      <div class="container mx-auto px-4">
        <section class="py-12">
          <div class="mb-12">
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
              <div class="rounded-lg border bg-card text-card-foreground shadow-sm">
                <div class="p-6">
                  <h3 class="text-lg font-semibold">Coming Soon</h3>
                  <p class="text-sm text-muted-foreground">
                    Featured perfumes will be displayed here
                  </p>
                </div>
              </div>
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
          <div class="mb-16">
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
              <div class="rounded-lg border bg-card text-card-foreground shadow-sm">
                <div class="p-6">
                  <h3 class="text-lg font-semibold">Coming Soon</h3>
                  <p class="text-sm text-muted-foreground">
                    Featured perfumes will be displayed here
                  </p>
                </div>
              </div>
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
          <div class="mb-12">
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
              <div class="rounded-lg border bg-card text-card-foreground shadow-sm">
                <div class="p-6">
                  <h3 class="text-lg font-semibold">Coming Soon</h3>
                  <p class="text-sm text-muted-foreground">
                    Featured perfumes will be displayed here
                  </p>
                </div>
              </div>
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
    </div>
  </div>
</template> 

<style scoped>
.background-animation {
  position: absolute;
  top: -64px; /* Adjust this value based on your navbar height */
  left: 0;
  width: 100%;
  height: calc(100% + 64px); /* Adjust this value based on your navbar height */
  background: 
    linear-gradient(135deg, 
      rgba(255, 223, 236, 0.8) 0%,
      rgba(230, 230, 250, 0.9) 50%,
      rgba(255, 192, 203, 0.8) 100%
    );
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

:root.dark .background-animation {
  background: 
    linear-gradient(135deg, 
      rgba(64, 45, 95, 0.9) 0%,
      rgba(44, 44, 84, 0.9) 50%,
      rgba(84, 35, 45, 0.9) 100%
    );
}

.mouse-follower {
  position: fixed;
  width: 1000px;
  height: 1000px;
  background: radial-gradient(
    circle at center,
    rgba(147, 112, 219, 0.35) 0%,
    rgba(230, 230, 250, 0.25) 40%,
    rgba(255, 192, 203, 0.2) 60%,
    transparent 80%
  );
  border-radius: 50%;
  pointer-events: none;
  z-index: 1;
  will-change: transform;
  filter: blur(50px);
  mix-blend-mode: multiply;
}

:root.dark .mouse-follower {
  background: radial-gradient(
    circle at center,
    rgba(74, 56, 110, 0.35) 0%,
    rgba(44, 44, 84, 0.35) 60%,
    rgba(84, 35, 45, 0.2) 60%,
    transparent 80%
  );
}

.sparkle {
  position: absolute;
  width: 6px;
  height: 6px;
  background-color: rgba(192, 169, 240, 0.9);
  border-radius: 50%;
  opacity: 0;
  pointer-events: none;
  box-shadow: 0 0 10px 2px rgba(147, 112, 219, 0.4);
  will-change: transform, opacity;
}

:root.dark .sparkle {
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 10px 2px rgba(255, 255, 255, 0.3);
}

@keyframes sparkleFloat {
  0% {
    transform: translate(0, 0) scale(0);
    opacity: 0;
  }
  20%, 80% {
    opacity: 0.8;
  }
  50% {
    transform: translate(var(--tx), var(--ty)) scale(1.2);
    opacity: 1;
  }
  100% {
    transform: translate(calc(var(--tx) * 2), calc(var(--ty) * 2)) scale(0);
    opacity: 0;
  }
}

.background-animation .sparkle {
  position: absolute;
  animation: sparkleFloat 6s ease-in-out infinite;
}

.background-animation .sparkle:nth-child(1) { --tx: 100px; --ty: -100px; animation-delay: 0s; left: 10%; top: 20%; }
.background-animation .sparkle:nth-child(2) { --tx: -150px; --ty: -50px; animation-delay: 0.5s; left: 30%; top: 40%; }
.background-animation .sparkle:nth-child(3) { --tx: 80px; --ty: 120px; animation-delay: 1s; left: 50%; top: 60%; }
.background-animation .sparkle:nth-child(4) { --tx: -120px; --ty: 80px; animation-delay: 1.5s; left: 70%; top: 20%; }
.background-animation .sparkle:nth-child(5) { --tx: 140px; --ty: -80px; animation-delay: 2s; left: 90%; top: 70%; }
.background-animation .sparkle:nth-child(6) { --tx: -90px; --ty: -130px; animation-delay: 2.5s; left: 20%; top: 80%; }
.background-animation .sparkle:nth-child(7) { --tx: 110px; --ty: 100px; animation-delay: 3s; left: 40%; top: 15%; }
.background-animation .sparkle:nth-child(8) { --tx: -130px; --ty: 90px; animation-delay: 3.5s; left: 60%; top: 85%; }
.background-animation .sparkle:nth-child(9) { --tx: 70px; --ty: -140px; animation-delay: 1.2s; left: 80%; top: 35%; }
.background-animation .sparkle:nth-child(10) { --tx: -100px; --ty: 110px; animation-delay: 2.7s; left: 15%; top: 55%; }
.background-animation .sparkle:nth-child(11) { --tx: 120px; --ty: -90px; animation-delay: 0.8s; left: 35%; top: 75%; }
.background-animation .sparkle:nth-child(12) { --tx: -110px; --ty: 130px; animation-delay: 1.8s; left: 55%; top: 25%; }
.background-animation .sparkle:nth-child(13) { --tx: 95px; --ty: -120px; animation-delay: 2.3s; left: 75%; top: 45%; }
.background-animation .sparkle:nth-child(14) { --tx: -140px; --ty: 70px; animation-delay: 3.2s; left: 25%; top: 65%; }
.background-animation .sparkle:nth-child(15) { --tx: 130px; --ty: -70px; animation-delay: 1.7s; left: 45%; top: 95%; }
.background-animation .sparkle:nth-child(16) { --tx: -80px; --ty: 140px; animation-delay: 2.9s; left: 85%; top: 5%; }
.background-animation .sparkle:nth-child(17) { --tx: 140px; --ty: -140px; animation-delay: 0.3s; left: 5%; top: 40%; }
.background-animation .sparkle:nth-child(18) { --tx: -120px; --ty: 120px; animation-delay: 1.4s; left: 95%; top: 50%; }
.background-animation .sparkle:nth-child(19) { --tx: 110px; --ty: -110px; animation-delay: 2.1s; left: 65%; top: 10%; }
.background-animation .sparkle:nth-child(20) { --tx: -100px; --ty: 100px; animation-delay: 3.7s; left: 15%; top: 90%; }

.mist-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.mist-particle {
  position: absolute;
  background: linear-gradient(135deg,
    rgba(230, 230, 250, 0.2),
    rgba(255, 192, 203, 0.1)
  );
  border-radius: 50%;
  filter: blur(20px);
  opacity: 0;
  animation: mistFloat 20s ease-out infinite;
}

:root.dark .mist-particle {
  background: linear-gradient(135deg,
    rgba(44, 44, 84, 0.2),
    rgba(84, 35, 45, 0.1)
  );
}

@keyframes mistFloat {
  0% {
    opacity: 0;
    transform: translateY(100%) translateX(-5%) scale(1);
  }
  20% {
    opacity: 0.3;
  }
  80% {
    opacity: 0.2;
    transform: translateY(-20%) translateX(5%) scale(1.5);
  }
  100% {
    opacity: 0;
    transform: translateY(-50%) translateX(10%) scale(1.2);
  }
}

.luxury-overlay {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(255, 223, 236, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(230, 230, 250, 0.4) 0%, transparent 50%);
  pointer-events: none;
  mix-blend-mode: soft-light;
  z-index: 2;
}

:root.dark .luxury-overlay {
  background: 
    radial-gradient(circle at 20% 20%, rgba(64, 45, 95, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(84, 35, 45, 0.4) 0%, transparent 50%);
}

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

.no-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.no-scrollbar::-webkit-scrollbar {
  display: none;  /* Chrome, Safari and Opera */
}
</style> 