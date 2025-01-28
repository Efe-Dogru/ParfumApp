<script setup lang="ts">
import ComboBox from '@/components/ui/custom/ComboBox.vue'
const items = [
  { value: '1', label: 'Item 1' },
  { value: '2', label: 'Item 2' },
  { value: '3', label: 'Item 3' },
]
</script>

<template>
    <ComboBox :items="items" />
</template>