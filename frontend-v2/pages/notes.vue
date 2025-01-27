<script setup lang="ts">
import { useNotes } from '@/composables/useNotes'

const { getNotes } = useNotes()
const notes = await getNotes()
</script>

<template>
    <div>
        <h1>Notes</h1>
    </div>
</template>