<script setup lang="ts">
import { Button } from '@/components/ui/button'
const client = useSupabaseClient()

const { data } = await useAsyncData('perfumes', async () => {
    return await client.from('perfumes').select('id, name').limit(5)
})
console.log(data.value)

</script>

<template>
    
</template>