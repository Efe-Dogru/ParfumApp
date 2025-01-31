<script setup lang="ts">
import TubelightNavbar from '@/components/ui/navbar.vue'
import FooterSection from '@/components/ui/FooterSection.vue'
import { Home, Search, User, Briefcase, Flower } from 'lucide-vue-next'
import { useRoute } from 'vue-router'

const route = useRoute()
const isIndexPage = computed(() => {
  const isIndex = route.path === '/' || route.path === ''
  return isIndex
})

const navItems = [
  { name: 'Home', url: '/', icon: Home },
  { name: 'Perfumes', url: '/perfumes', icon: Search },
  { name: 'Notes', url: '/notes', icon: Flower },
  { name: 'Feedback', url: '/feedback', icon: Briefcase },
  { name: 'About', url: '/about', icon: User },
]
</script>
<template>
    <div>
      <div :class="{ 'mb-24': !isIndexPage }">
        <TubelightNavbar :items="navItems"/>
      </div>
        <main>
            <slot />
        </main>
      <FooterSection />
    </div>
  </template> 