<script setup lang="ts">
import { ArrowRight } from 'lucide-vue-next'

interface Props {
  text?: string
  class?: string
}

withDefaults(defineProps<Props>(), {
  text: 'Button'
})
</script>

<template>
  <button
    class="group relative w-52 h-12 cursor-pointer overflow-hidden rounded-full border bg-background text-center font-semibold"
    :class="class"
  >
    <span class="inline-block translate-x-6 transition-all duration-300 group-hover:translate-x-12 group-hover:opacity-0 pr-4">
      {{ text }}
    </span>
    <div class="absolute top-0 z-10 flex h-full w-full translate-x-12 items-center justify-center gap-2 text-primary-foreground opacity-0 transition-all duration-300 group-hover:-translate-x-1 group-hover:opacity-100">
      <span>{{ text }}</span>
      <ArrowRight />
    </div>
    <div class="absolute left-[12%] top-[40%] h-2 w-2 scale-[1] rounded-lg bg-[#834966] transition-all duration-300 group-hover:left-[0%] group-hover:top-[0%] group-hover:h-full group-hover:w-full group-hover:scale-[1.8] group-hover:bg-[#834966]" />
  </button>
</template>
