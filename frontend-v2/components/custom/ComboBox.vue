<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import { Input } from '@/components/ui/input'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { cn } from '@/utils'
import { Check, ChevronsUpDown } from 'lucide-vue-next'
import { ref, watch, computed } from 'vue'

interface Item {
  value: string
  label: string
}

const props = defineProps<{
  items: Item[]
  placeholder?: string
  searchPlaceholder?: string
  emptyMessage?: string
  modelValue?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const open = ref(false)
const value = ref(props.modelValue || '')
const search = ref('')

// Filtered items based on search
const filteredItems = computed(() => {
  if (!search.value) return props.items
  return props.items.filter(item => 
    item.label.toLowerCase().includes(search.value.toLowerCase())
  )
})

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  if (newValue !== undefined) {
    value.value = newValue
  }
})

// Watch for internal value changes
watch(value, (newValue) => {
  emit('update:modelValue', newValue)
})

// Reset search when closing popover
watch(open, (newValue) => {
  if (!newValue) {
    search.value = ''
  }
})
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        class="w-[200px] justify-between"
      >
        {{ value
          ? items.find((item) => item.value === value)?.label
          : placeholder || "Select..." }}
        <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[200px] p-0">
      <Command>
        <div class="px-3 py-2">
          <Input
            v-model="search"
            :placeholder="searchPlaceholder || 'Search...'"
            class="h-9"
          />
        </div>
        <CommandEmpty>{{ emptyMessage || "No items found." }}</CommandEmpty>
        <CommandList>
          <CommandGroup>
            <CommandItem
              v-for="item in filteredItems"
              :key="item.value"
              :value="item.value"
              @select="(ev) => {
                if (typeof ev.detail.value === 'string') {
                  value = ev.detail.value
                }
                open = false
              }"
            >
              {{ item.label }}
              <Check
                :class="cn(
                  'ml-auto h-4 w-4',
                  value === item.value ? 'opacity-100' : 'opacity-0',
                )"
              />
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template> 