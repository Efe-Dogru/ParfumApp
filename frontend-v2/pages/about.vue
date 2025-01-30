<script setup lang="ts">
import { Button } from '~/components/ui/button'
import { Heart, Users, Target, ArrowRight, Sparkles, Droplet, Leaf, Crown, Beaker, Award, Glasses, Star } from 'lucide-vue-next'
import FeatureSection from '~/components/ui/feature-section/FeatureSection.vue'

const achievements = [
  { number: '50K+', label: 'Active Users' },
  { number: '10K+', label: 'Fragrances' },
  { number: '4.9', label: 'App Rating', icon: Star },
  { number: '100+', label: 'Expert Reviews' }
]

const testimonials = [
  {
    quote: "Parfum App has revolutionized how I discover and experience fragrances. It's an indispensable tool for any perfume enthusiast.",
    author: "Emma Thompson",
    role: "Certified Perfumer"
  },
  {
    quote: "The most comprehensive and user-friendly fragrance platform I've ever used. The note discovery feature is simply brilliant.",
    author: "Michael Chen",
    role: "Fragrance Blogger"
  }
]

const sections = [
  {
    badge: 'Mission',
    title: 'Our Purpose',
    description: 'Parfum App was built for fragrance lovers, by fragrance lovers. Our mission is to help you explore the world of scents, discover new perfumes, and understand the art of perfumery.',
    features: [
      {
        title: 'Extensive Collection',
        description: 'Discover a vast collection of fragrances, from timeless classics to contemporary favorites, with over 10,000 unique scents.',
        icon: Beaker,
        span: true,
        link: '/perfumes'
      },
      {
        title: 'Note Discovery',
        description: 'Explore the intricate world of fragrance notes through our interactive visualization and comprehensive note database.',
        icon: Leaf,
        span: false,
        link: '/notes'
      },
      {
        title: 'Expert Curation',
        description: 'Experience handpicked collections and personalized recommendations from industry experts and perfume connoisseurs.',
        icon: Crown,
        span: false,
        link: '/notes'
      }
    ]
  },
  {
    badge: 'Story',
    title: 'Our Journey',
    description: 'From a simple idea to a thriving community, our journey has been driven by passion, innovation, and the love for exceptional fragrances.',
    features: [
      {
        title: 'Community First',
        description: 'Join over 50,000 fragrance enthusiasts sharing reviews, experiences, and discoveries. Your next signature scent awaits!',
        icon: Heart,
        span: true
      },
      {
        title: 'Expert Team',
        description: 'Led by certified perfumers, developers, and designers united by their passion for creating the ultimate fragrance platform.',
        icon: Users,
        span: false
      },
      {
        title: 'Innovation & Growth',
        description: 'Continuously evolving with AI-powered recommendations, virtual testing, and collaborations with top perfume houses.',
        icon: Sparkles,
        span: true
      }
    ]
  },
  {
    badge: 'Vision',
    title: 'Looking Forward',
    description: 'We\'re on a mission to revolutionize how people discover, experience, and share their passion for fragrances.',
    features: [
      {
        title: 'Global Reach',
        description: 'Expanding our database to include rare and niche fragrances from around the world, making them accessible to everyone.',
        icon: Glasses,
        span: false
      },
      {
        title: 'Industry Recognition',
        description: 'Proud recipient of multiple awards for innovation in the fragrance industry and community engagement.',
        icon: Award,
        span: true
      }
    ]
  }
]
</script>

<template>
  <div>
    <!-- Breadcrumb -->
    <!-- <nav class="container mx-auto px-4 py-4 text-sm text-muted-foreground">
      <NuxtLink to="/" class="hover:text-primary transition-colors">Home</NuxtLink>
      <span class="mx-2">/</span>
      <span class="text-foreground">About</span>
    </nav> -->

    <div class="container mx-auto px-4 py-12">
      <!-- Hero Section with Background -->
      <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary/10 via-primary/5 to-background p-8 md:p-12 mb-16">
        <div class="relative text-center">
          <h1 class="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            About Parfum App
          </h1>
          <p class="text-xl md:text-2xl text-muted-foreground/90 max-w-2xl mx-auto mb-8">
            Your ultimate destination for exploring the enchanting world of fragrances
          </p>
          
          <!-- Achievement Stats -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto mt-12">
            <div v-for="achievement in achievements" :key="achievement.label" 
                 class="bg-background/80 backdrop-blur-sm p-4 rounded-lg border border-border/50">
              <div class="flex items-center justify-center gap-1">
                <span class="text-3xl font-bold text-primary">{{ achievement.number }}</span>
                <component v-if="achievement.icon" :is="achievement.icon" class="w-5 h-5 text-primary" />
              </div>
              <div class="text-sm text-muted-foreground mt-1">{{ achievement.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Dynamic Sections -->
      <FeatureSection
        v-for="(section, index) in sections"
        :key="index"
        :badge="section.badge"
        :title="section.title"
        :description="section.description"
        :features="section.features"
        :variant="index % 2 === 1 ? 'highlight' : 'default'"
      />

      <!-- Testimonials -->
      <div class="grid md:grid-cols-2 gap-8 mt-16 mb-16">
        <div v-for="(testimonial, index) in testimonials" :key="index"
             class="bg-muted/30 p-8 rounded-xl border border-border/50 relative">
          <div class="absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2">
            <div class="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
              <Heart class="w-6 h-6 text-primary" />
            </div>
          </div>
          <p class="text-lg italic text-muted-foreground/90 mb-4">
            "{{ testimonial.quote }}"
          </p>
          <div>
            <div class="font-semibold">{{ testimonial.author }}</div>
            <div class="text-sm text-muted-foreground">{{ testimonial.role }}</div>
          </div>
        </div>
      </div>

      <!-- Enhanced Call to Action -->
      <div class="bg-gradient-to-br from-primary/10 to-primary/5 rounded-xl p-12 text-center mt-8 backdrop-blur-sm border border-primary/20">
        <h3 class="text-3xl font-bold mb-4 text-primary">Start Your Fragrance Journey</h3>
        <p class="text-muted-foreground/90 mb-8 text-lg max-w-xl mx-auto">
          Join our global community of fragrance enthusiasts and discover your next signature scent.
          Experience the art of perfumery like never before!
        </p>
        <NuxtLink to="/perfumes">
          <Button class="gap-2 text-lg px-8 py-6 bg-primary hover:bg-primary/90 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-primary/20">
            Explore Perfumes
            <ArrowRight class="w-5 h-5" />
          </Button>
        </NuxtLink>
        <p class="text-sm text-muted-foreground mt-4">
          Join 50,000+ fragrance enthusiasts today!
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1400px;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>