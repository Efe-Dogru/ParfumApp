<!-- components/NavBar.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import type { LucideIcon } from 'lucide-vue-next'

interface NavItem {
  name: string
  url: string
  icon: LucideIcon
}

interface Props {
  items: NavItem[]
  className?: string
}

const props = defineProps<Props>()
const route = useRoute()

// Compute active tab based on current route
const activeTab = computed(() => {
  const currentPath = route.path
  const activeItem = props.items.find(item => item.url === currentPath)
  return activeItem ? activeItem.name : props.items[0].name
})

const isMobile = ref(false)

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div
    :class="[
      'fixed sm:top-0 left-1/2 -translate-x-1/2 z-50 mb-6 sm:pt-6',
      className
    ]"
  >
    <div class="flex items-center gap-3 bg-background/5 border border-border backdrop-blur-lg rounded-full shadow-lg p-3">
      <NuxtLink
        v-for="item in items"
        :key="item.name"
        :to="item.url"
        :class="[
          'relative cursor-pointer text-sm font-semibold px-6 py-2 rounded-full transition-all duration-300',
          'text-foreground/80 hover:text-primary',
          { 'bg-muted text-primary': activeTab === item.name }
        ]"
      >
        <span class="hidden md:inline">{{ item.name }}</span>
        <span class="md:hidden">
          <component :is="item.icon" :size="18" :stroke-width="2.5" />
        </span>
        
        <!-- Remove transition wrapper and simplify the active indicator -->
        <div
          v-show="activeTab === item.name"
          class="absolute inset-0 w-full bg-primary/5 rounded-full -z-10 transition-opacity duration-300"
        >
          <div class="absolute -top-2 left-1/2 -translate-x-1/2 w-8 h-1 bg-primary rounded-t-full transition-all duration-300">
            <div class="absolute w-12 h-6 bg-primary/20 rounded-full blur-md -top-2 -left-2" />
            <div class="absolute w-8 h-6 bg-primary/20 rounded-full blur-md -top-1" />
            <div class="absolute w-4 h-4 bg-primary/20 rounded-full blur-sm top-0 left-2" />
          </div>
        </div>
      </NuxtLink>

      <!-- Add slot for additional content like search bar -->
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.router-link-active {
  @apply text-primary;
}
</style>