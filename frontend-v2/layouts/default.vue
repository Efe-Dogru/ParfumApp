<script setup lang="ts">
import TubelightNavbar from '@/components/ui/navbar.vue'
import FooterSection from '@/components/ui/FooterSection.vue'
import { Home, Search, User, Briefcase } from 'lucide-vue-next'
const navItems = [
  { name: 'Home', url: '/', icon: Home },
  { name: 'Perfumes', url: '/perfumes', icon: Search },
  { name: 'Notes', url: '/notes', icon: User },
  { name: 'Feedback', url: '/feedback', icon: Briefcase },
  { name: 'About', url: '/about', icon: User },
]
</script>
<template>
    <div>
      <div class="mb-24">
        <TubelightNavbar :items="navItems"/>
      </div>
        <main>
            <slot />
        </main>
      <FooterSection />
    </div>
  </template> 