<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { usePerfumes } from '@/composables/usePerfumes'

const { getPerfumes } = usePerfumes()
const perfumes = await getPerfumes()

console.log(perfumes.value)
</script>

<template>
    <div>
        <h1>Home</h1>
    </div>
</template>