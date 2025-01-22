<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import InteractiveHoverButton from '../components/ui/InteractiveHoverButton.vue'

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

onMounted(() => {
  interval = setInterval(updateTitle, 4000)
  window.addEventListener('mousemove', updateMousePosition)
  updateFollowerPosition()
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
  window.removeEventListener('mousemove', updateMousePosition)
})
</script>

<template>
  <div class="space-y-8 relative min-h-screen overflow-hidden">
    <div class="background-animation">
      <div 
        class="mouse-follower"
        :style="{
          transform: `translate(${followerX}px, ${followerY}px) translate(-50%, -50%)`
        }"
      >
        <div v-for="n in 12" :key="n" class="sparkle"></div>
      </div>
      <div v-for="n in 20" :key="`bg-sparkle-${n}`" class="sparkle"></div>
      <div class="perfume-bottle"></div>
      <div class="perfume-bottle bottle-2"></div>
      <div class="mist-container">
        <div v-for="n in 20" :key="n" class="mist-particle"></div>
      </div>
      <div class="luxury-overlay"></div>
    </div>
    <div class="relative z-10">
      <section class="py-12 md:py-24">
        <div class="container flex flex-col items-center text-center">
          <h1 class="text-3xl font-bold leading-tight tracking-tighter md:text-5xl lg:text-6xl lg:leading-[1.1] text-center">
            <div class="flex flex-col items-center">
              <span>Discover Your</span>
              <div class="flex items-center gap-3">
                <div class="relative h-[1.2em] w-[200px] overflow-hidden">
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
                </div>
                <span>Fragrance</span>
              </div>
            </div>
          </h1>
          <p class="mt-4 max-w-[700px] text-lg text-muted-foreground">
            Explore our curated collection of perfumes, find your signature scent, and learn about the art of fragrance.
          </p>
          <div class="mt-6 flex flex-wrap justify-center gap-4">
            <div class="relative justify-center">
              <InteractiveHoverButton
                text="Browse Collection"
                @click="navigateTo('/browse')"
              />
              <InteractiveHoverButton
                class="mt-4 ml-8"
                text="Search Perfumes"
                @click="navigateTo('/search')"
              />
            </div>
            <!-- <NuxtLink
              to="/search"
              class="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              Search Perfumes
            </NuxtLink> -->
          </div>
        </div>
      </section>

      <section class="mt-40">
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
</template> 

<style scoped>
.background-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    rgba(230, 230, 250, 1) 0%,
    rgba(255, 192, 203, 0.9) 100%
  );
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

:root.dark .background-animation {
  background: linear-gradient(135deg, 
    rgba(44, 44, 84, 1) 0%,
    rgba(84, 35, 45, 0.9) 100%
  );
}

.luxury-overlay {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(230, 230, 250, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 192, 203, 0.4) 0%, transparent 50%);
  pointer-events: none;
}

:root.dark .luxury-overlay {
  background: 
    radial-gradient(circle at 20% 20%, rgba(44, 44, 84, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(84, 35, 45, 0.4) 0%, transparent 50%);
}

.perfume-bottle {
  position: absolute;
  width: 150px;
  height: 250px;
  bottom: -50px;
  left: 15%;
  opacity: 0.08;
  background: linear-gradient(45deg, rgba(230, 230, 250, 0.3), rgba(255, 192, 203, 0.15));
  clip-path: path('M75 0C85 0 95 10 95 20L95 150C95 160 85 180 75 190C65 180 55 160 55 150L55 20C55 10 65 0 75 0Z M45 150C45 170 75 200 75 200C75 200 105 170 105 150L105 50L45 50L45 150Z');
  transform: scale(1);
  animation: bottleFloat 15s ease-in-out infinite;
}

:root.dark .perfume-bottle {
  background: linear-gradient(45deg, rgba(44, 44, 84, 0.3), rgba(84, 35, 45, 0.15));
}

.bottle-2 {
  left: 75%;
  height: 200px;
  animation-delay: -7.5s;
  opacity: 0.06;
  transform: scale(0.8);
}

@keyframes bottleFloat {
  0%, 100% {
    transform: translateY(0) rotate(-2deg);
  }
  50% {
    transform: translateY(-30px) rotate(2deg);
  }
}

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
</style> 