<script setup lang="ts">
import { Heart, Users, Target, ArrowRight, Sparkles, Droplet, Leaf, Crown, Star } from 'lucide-vue-next'
import { Badge } from '~/components/ui/badge'
import { computed } from 'vue'

interface Feature {
  title: string
  description: string
  icon: any
  span: boolean
  link?: string
}

interface Props {
  badge?: string
  title: string
  description: string
  features: Feature[]
  variant?: 'default' | 'highlight'
}

const props = defineProps<Props>()

const sectionClasses = computed(() => {
  return {
    '': props.variant === 'highlight'
  }
})
</script>

<template>
  <div class="w-full py-12 transition-all duration-500 ease-in-out rounded-lg" :class="sectionClasses">
    <div class="container mx-auto px-4">
      <div class="flex flex-col gap-12">
        <div class="flex gap-6 flex-col items-start animate-fade-in">
          <div v-if="badge">
            <Badge class="text-sm px-4 py-1.5 font-medium">{{ badge }}</Badge>
          </div>
          <div class="flex gap-6 flex-col">
            <h2 class="text-4xl md:text-6xl tracking-tight max-w-xl font-bold text-left relative">
              {{ title }}
              <span class="absolute -bottom-3 left-0 w-24 h-1.5 bg-primary rounded-full"></span>
            </h2>
            <p class="text-xl max-w-xl lg:max-w-2xl leading-relaxed tracking-tight text-muted-foreground/90 text-left">
              {{ description }}
            </p>
          </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="(feature, index) in features"
            :key="index"
            :style="{ animationDelay: `${index * 100}ms` }"
            class="animate-fade-in-up"
            :class="[
              'relative bg-gradient-to-br from-background to-muted/50 rounded-xl p-8 flex justify-between flex-col group',
              'transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-primary/5',
              'border border-border/50 hover:border-primary/20',
              feature.span ? 'h-full lg:col-span-2 aspect-square lg:aspect-auto' : 'aspect-square'
            ]"
          >
            <div class="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl"></div>
            <div class="flex justify-between items-start relative">
              <component 
                :is="feature.icon" 
                class="w-12 h-12 stroke-[1.5] text-primary transition-all duration-300 group-hover:scale-110 group-hover:rotate-3" 
              />
              <NuxtLink 
                v-if="feature.link"
                :to="feature.link"
                class="text-primary hover:text-primary/80 transition-all flex items-center gap-1.5 text-sm font-medium group/link"
              >
                Learn more
                <ArrowRight class="w-4 h-4 transition-transform duration-300 group-hover/link:translate-x-1" />
              </NuxtLink>
            </div>
            <div class="flex flex-col mt-8 relative">
              <h3 class="text-2xl font-semibold tracking-tight mb-3">{{ feature.title }}</h3>
              <p class="text-muted-foreground/90 text-lg leading-relaxed">
                {{ feature.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1400px;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out forwards;
}

.animate-fade-in-up {
  animation: fade-in-up 0.5s ease-out forwards;
  opacity: 0;
}
</style> 