<script setup lang="ts">
import { useApi } from '~/composables/useApi'
import type { Perfume, PerfumeNote } from '~/composables/useCommon'
import { 
  Home, 
  Search, 
  Droplets, 
  Wind, 
  Clock, 
  Calendar, 
  User2, 
  Flower2, 
  Sparkles, 
  Flame,
  Heart,
  Sun,
  CloudSun,
  CloudRain,
  Snowflake,
  MapPin,
  GlassWater,
  Zap,
  Info,
  SunSnow
} from 'lucide-vue-next'

const route = useRoute()
const { getPerfumeById } = useApi()

const perfume = ref<Perfume | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const getAccordClass = (accordName: string) => {
  const classes = {
    // Woody & Earthy tones
    woody: 'bg-amber-200 dark:bg-amber-800 text-amber-900 dark:text-amber-100',
    earthy: 'bg-stone-200 dark:bg-stone-800 text-stone-900 dark:text-stone-100',
    sandalwood: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-900 dark:text-yellow-100',
    cedarwood: 'bg-orange-100 dark:bg-orange-900 text-orange-900 dark:text-orange-100',
    vetiver: 'bg-lime-200 dark:bg-lime-800 text-lime-900 dark:text-lime-100',
    patchouli: 'bg-emerald-100 dark:bg-emerald-900 text-emerald-900 dark:text-emerald-100',
    oud: 'bg-rose-950 dark:bg-rose-900 text-rose-100 dark:text-rose-100',

    // Fresh & Citrus
    citrus: 'bg-yellow-300 dark:bg-yellow-700 text-yellow-900 dark:text-yellow-100',
    fresh: 'bg-sky-100 dark:bg-sky-900 text-sky-900 dark:text-sky-100',
    'fresh spicy': 'bg-teal-200 dark:bg-teal-800 text-teal-900 dark:text-teal-100',
    clean: 'bg-cyan-100 dark:bg-cyan-900 text-cyan-900 dark:text-cyan-100',
    marine: 'bg-blue-200 dark:bg-blue-800 text-blue-900 dark:text-blue-100',
    aquatic: 'bg-sky-200 dark:bg-sky-800 text-sky-900 dark:text-sky-100',
    mint: 'bg-green-200 dark:bg-green-800 text-green-900 dark:text-green-100',
    green: 'bg-lime-300 dark:bg-lime-700 text-lime-900 dark:text-lime-100',
    herbal: 'bg-emerald-200 dark:bg-emerald-800 text-emerald-900 dark:text-emerald-100',
    
    // Floral & Sweet
    floral: 'bg-fuchsia-200 dark:bg-fuchsia-800 text-fuchsia-900 dark:text-fuchsia-100',
    rose: 'bg-rose-200 dark:bg-rose-800 text-rose-900 dark:text-rose-100',
    jasmine: 'bg-pink-100 dark:bg-pink-900 text-pink-900 dark:text-pink-100',
    neroli: 'bg-orange-200 dark:bg-orange-800 text-orange-900 dark:text-orange-100',
    iris: 'bg-violet-200 dark:bg-violet-800 text-violet-900 dark:text-violet-100',
    tuberose: 'bg-pink-300 dark:bg-pink-700 text-pink-900 dark:text-pink-100',
    sweet: 'bg-purple-200 dark:bg-purple-800 text-purple-900 dark:text-purple-100',
    vanilla: 'bg-amber-100 dark:bg-amber-900 text-amber-900 dark:text-amber-100',
    honey: 'bg-yellow-200 dark:bg-yellow-800 text-yellow-900 dark:text-yellow-100',
    'tonka bean': 'bg-amber-300 dark:bg-amber-700 text-amber-900 dark:text-amber-100',
    almond: 'bg-orange-50 dark:bg-orange-950 text-orange-900 dark:text-orange-100',
    nutty: 'bg-amber-200 dark:bg-amber-800 text-amber-900 dark:text-amber-100',
    fruity: 'bg-rose-100 dark:bg-rose-900 text-rose-900 dark:text-rose-100',

    // Spicy & Warm
    spicy: 'bg-red-300 dark:bg-red-700 text-red-900 dark:text-red-100',
    'warm spicy': 'bg-orange-300 dark:bg-orange-700 text-orange-900 dark:text-orange-100',
    'oriental spicy': 'bg-red-200 dark:bg-red-800 text-red-900 dark:text-red-100',
    cardamom: 'bg-lime-100 dark:bg-lime-900 text-lime-900 dark:text-lime-100',
    ginger: 'bg-yellow-400 dark:bg-yellow-600 text-yellow-900 dark:text-yellow-100',
    saffron: 'bg-orange-400 dark:bg-orange-600 text-orange-900 dark:text-orange-100',

    // Aromatic
    aromatic: 'bg-indigo-200 dark:bg-indigo-800 text-indigo-900 dark:text-indigo-100',
    lavender: 'bg-violet-300 dark:bg-violet-700 text-violet-900 dark:text-violet-100',
    tobacco: 'bg-amber-400 dark:bg-amber-600 text-amber-900 dark:text-amber-100',
    coffee: 'bg-stone-400 dark:bg-stone-600 text-stone-900 dark:text-stone-100',
    rum: 'bg-amber-500 dark:bg-amber-500 text-amber-950 dark:text-amber-50',

    // Misc
    leather: 'bg-stone-300 dark:bg-stone-700 text-stone-900 dark:text-stone-100',
    powdery: 'bg-slate-200 dark:bg-slate-800 text-slate-900 dark:text-slate-100',
    musky: 'bg-neutral-200 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100',
    musk: 'bg-neutral-300 dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100',
    amber: 'bg-amber-200 dark:bg-amber-800 text-amber-900 dark:text-amber-100',
    metallic: 'bg-zinc-300 dark:bg-zinc-700 text-zinc-900 dark:text-zinc-100',
    rubber: 'bg-neutral-400 dark:bg-neutral-600 text-neutral-900 dark:text-neutral-100',
    smoky: 'bg-stone-500 dark:bg-stone-500 text-stone-950 dark:text-stone-50',
    aldehydic: 'bg-cyan-200 dark:bg-cyan-800 text-cyan-900 dark:text-cyan-100',
    aldehydes: 'bg-cyan-200 dark:bg-cyan-800 text-cyan-900 dark:text-cyan-100',
    solar: 'bg-amber-100 dark:bg-amber-900 text-amber-900 dark:text-amber-100',
    kulfi: 'bg-neutral-100 dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100',
  }

  // Convert accord name to lowercase for matching
  const key = accordName.toLowerCase() as keyof typeof classes
  return classes[key] || 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100' // default styling
}

// Helper function to filter notes by type
const filterNotesByType = (notes: PerfumeNote[] | undefined, type: 'top' | 'middle' | 'base') => {
  return notes?.filter(n => n.note_type === type) || []
}

onMounted(async () => {
  try {
    const response = await getPerfumeById(route.params.id as string)
    perfume.value = response.data
  } catch (err) {
    error.value = 'Failed to load perfume details'
    console.error('Error fetching perfume:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-background">
    <div class="container mx-auto px-4 py-12">
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>

      <div v-else-if="error" class="flex justify-center items-center py-8">
        <div class="text-red-500">{{ error }}</div>
      </div>


      <div v-else-if="perfume" class="">
        <!-- Breadcrumb -->
        <div class="mb-8 flex items-center space-x-2 text-sm text-muted-foreground">
          <NuxtLink to="/" class="hover:text-primary transition-colors inline-flex items-center gap-1">
            <Home class="w-4 h-4" />
            Home
          </NuxtLink>
          <span>/</span>
          <NuxtLink to="/browse" class="hover:text-primary transition-colors inline-flex items-center gap-1">
            <Search class="w-4 h-4" />
            Browse
          </NuxtLink>
          <span>/</span>
          <span class="text-foreground">{{ perfume?.name }}</span>
        </div>
        
        <!-- Header Section -->
        <div class="mb-8">
          <p class="text-sm uppercase tracking-wider text-muted-foreground mb-2">{{ perfume.brand?.name }}</p>
          <h1 class="text-4xl font-light mb-2">{{ perfume.name }}</h1>
          <p v-if="perfume.perfumer" class="text-sm text-muted-foreground">
            By {{ perfume.perfumer }}
          </p>
        </div>

        <div class="grid gap-16 lg:grid-cols-12">
          <!-- Left Column - Image -->
          <div class="lg:col-span-5">
            <div class="aspect-square">
              <img 
                :src="`http://127.0.0.1:8000/static/${perfume.local_image_path?.replace('\\', '/')}`"
                :alt="perfume.name"
                class="w-full h-full object-cover rounded-lg"
              />
            </div>
          </div>

          <!-- Right Column - Content -->
          <div class="lg:col-span-7 space-y-12">
            <!-- Main Accords -->
            <div v-if="perfume.main_accords?.length">
              <h2 class="text-sm uppercase tracking-wider mb-6">Main Accords</h2>
              <div class="flex flex-wrap gap-3">
                <span 
                  v-for="(accord, index) in perfume.main_accords" 
                  :key="index"
                  class="px-4 py-2 text-sm rounded-full transition-all"
                  :class="getAccordClass(String(accord))"
                >
                  {{ String(accord).charAt(0).toUpperCase() + String(accord).slice(1) }}
                </span>
              </div>
            </div>

            <!-- Notes Pyramid -->
            <div class="space-y-8">
              <div v-if="filterNotesByType(perfume?.perfume_notes, 'top').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Sparkles class="w-4 h-4" />
                  Top Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfume?.perfume_notes, 'top')" 
                    :key="note.note"
                    class="flex flex-col items-center group"
                  >
                    <div class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all">
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground group-hover:scale-110 transition-transform">
                        <img 
                          v-if="note.image_filename"
                          :src="`http://127.0.0.1:8000/static/notes_images/${note.image_filename}`"
                          :alt="note.note"
                          class="w-full h-full object-cover"
                        />
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                      </div>
                    </div>
                    <span class="text-sm">{{ note.note.charAt(0).toUpperCase() + note.note.slice(1) }}</span>
                  </div>
                </div>
              </div>

              <div v-if="filterNotesByType(perfume?.perfume_notes, 'middle').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Heart class="w-4 h-4" />
                  Middle Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfume?.perfume_notes, 'middle')" 
                    :key="note.note"
                    class="flex flex-col items-center group"
                  >
                    <div class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all">
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground group-hover:scale-110 transition-transform">
                        <img 
                          v-if="note.image_filename"
                          :src="`http://127.0.0.1:8000/static/notes_images/${note.image_filename}`"
                          :alt="note.note"
                          class="w-full h-full object-cover"
                        />
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                      </div>
                    </div>
                    <span class="text-sm">{{ note.note.charAt(0).toUpperCase() + note.note.slice(1) }}</span>
                  </div>
                </div>
              </div>

              <div v-if="filterNotesByType(perfume?.perfume_notes, 'base').length">
                <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Flame class="w-4 h-4" />
                  Base Notes
                </h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
                  <div 
                    v-for="note in filterNotesByType(perfume?.perfume_notes, 'base')" 
                    :key="note.note"
                    class="flex flex-col items-center group"
                  >
                    <div class="w-16 h-16 rounded-full bg-muted mb-2 overflow-hidden group-hover:scale-110 transition-all">
                      <div class="w-full h-full flex items-center justify-center text-muted-foreground group-hover:scale-110 transition-transform">
                        <img 
                          v-if="note.image_filename"
                          :src="`http://127.0.0.1:8000/static/notes_images/${note.image_filename}`"
                          :alt="note.note"
                          class="w-full h-full object-cover"
                        />
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                      </div>
                    </div>
                    <span class="text-sm">{{ note.note.charAt(0).toUpperCase() + note.note.slice(1) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Description & Inspiration -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 border-t border-border pt-8 mt-12">
          <div v-if="perfume.description" class="prose prose-sm max-w-none">
            <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
              <Info class="w-4 h-4" />
              Description
            </h2>
            <p class="text-muted-foreground leading-relaxed">{{ perfume.description }}</p>
          </div>
          <div v-if="perfume.inspiration" class="prose prose-sm max-w-none border-l border-border pl-6">
            <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
              <Flower2 class="w-4 h-4" />
              Inspiration
            </h2>
            <p class="text-muted-foreground leading-relaxed">{{ perfume.inspiration }}</p>
          </div>
        </div>

        <!-- Details & Best For -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 border-t border-border pt-8 mt-8">
          <div>
            <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
              <Info class="w-4 h-4" />
              Details
            </h2>
            <div class="grid grid-cols-2 gap-y-6 gap-x-12">
              <div v-if="perfume.type">

                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Droplets class="w-3 h-3" />
                  Type
                </p>
                <p>{{ perfume.type }}</p>
              </div>
              <div v-if="perfume.gender">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <User2 class="w-3 h-3" />
                  Gender
                </p>
                <p>{{ perfume.gender.charAt(0).toUpperCase() + perfume.gender.slice(1) }}</p>
              </div>
              <div v-if="perfume.family">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Flower2 class="w-3 h-3" />
                  Family
                </p>
                <p>{{ perfume.family }}</p>
              </div>
              <div v-if="perfume.concentration">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <GlassWater class="w-3 h-3" />
                  Concentration
                </p>
                <p>{{ perfume.concentration}}</p>
              </div>
              <div v-if="perfume.release_year">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Calendar class="w-3 h-3" />
                  Release Year
                </p>
                <p>{{ perfume.release_year }}</p>
              </div>
              <div v-if="perfume.longevity">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Clock class="w-3 h-3" />
                  Longevity
                </p>
                <p>{{ perfume.longevity.charAt(0).toUpperCase() + perfume.longevity.slice(1) }}</p>
              </div>
              <div v-if="perfume.sillage">
                <p class="text-xs uppercase text-muted-foreground mb-1 flex items-center gap-1">
                  <Wind class="w-3 h-3" />
                  Sillage
                </p>
                <p>{{ perfume.sillage.charAt(0).toUpperCase() + perfume.sillage.slice(1) }}</p>
              </div>
            </div>
          </div>

          <div>
            <h2 class="text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
              <MapPin class="w-4 h-4" />
              Best For
            </h2>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="occasion in perfume.occasion" 
                :key="occasion"
                class="px-3 py-1 text-sm border border-border rounded-sm inline-flex items-center gap-1"
              >
                {{ occasion.charAt(0).toUpperCase() + occasion.slice(1) }}
              </span>
            </div>
            <h2 class="text-sm uppercase tracking-wider mt-8 mb-4 flex items-center gap-2">
              <SunSnow class="w-4 h-4" />
              Ideal Seasons
            </h2>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="season in perfume.season" 
                :key="season"
                class="px-3 py-1 text-sm border border-border rounded-sm inline-flex items-center gap-1"
              >
                <component 
                  :is="season.toLowerCase() === 'summer' ? Sun : 
                       season.toLowerCase() === 'spring' ? CloudSun :
                       season.toLowerCase() === 'fall' ? CloudRain :
                       Snowflake" 
                  class="w-3 h-3"
                />
                {{ season.charAt(0).toUpperCase() + season.slice(1) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add any additional custom styles here */
</style> 