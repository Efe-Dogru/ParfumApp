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
import { Badge } from '@/components/ui/badge'
import { cn } from '@/utils'
import { Check, ChevronsUpDown, X } from 'lucide-vue-next'
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
  modelValue?: string[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string[]): void
}>()

const open = ref(false)
const selectedValues = ref<string[]>(props.modelValue || [])
const search = ref('')

// Filtered items based on search
const filteredItems = computed(() => {
  if (!search.value) return props.items
  return props.items.filter(item => 
    item.label.toLowerCase().includes(search.value.toLowerCase())
  )
})

// Selected items for display
const selectedItems = computed(() => {
  return props.items.filter(item => selectedValues.value.includes(item.value))
})

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  if (newValue !== undefined) {
    selectedValues.value = newValue
  }
})

// Watch for internal value changes
watch(selectedValues, (newValue) => {
  emit('update:modelValue', newValue)
})

// Watch for closing popover
watch(open, (newValue) => {
  if (!newValue) {
    search.value = ''
  }
})

const toggleItem = (value: string) => {
  const index = selectedValues.value.indexOf(value)
  if (index === -1) {
    selectedValues.value.push(value)
  } else {
    selectedValues.value.splice(index, 1)
  }
}

const removeItem = (value: string) => {
  const index = selectedValues.value.indexOf(value)
  if (index !== -1) {
    selectedValues.value.splice(index, 1)
  }
}
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <Button
        role="combobox"
        :aria-expanded="open"
        class="w-full justify-between relative min-h-[40px] bg-primary-800/0 text-white"
      >
        <div class="flex flex-wrap gap-1 items-center">
          <template v-if="selectedValues.length > 0">
            <span class="text-white">
              {{ selectedValues.length }} {{ selectedValues.length === 1 ? 'item' : 'items' }} selected
            </span>
          </template>
          <span v-else class="text-gray-400">
            {{ placeholder || "Select items..." }}
          </span>
        </div>
        <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-full p-0 border border-secondary/30 bg-primary-700">
      <Command class="border-0">
        <div class="px-3 py-2 bg-primary-700">
          <Input
            v-model="search"
            :placeholder="searchPlaceholder || 'Search items...'"
            class="h-9 bg-primary-700 border-0 ring-0 ring-offset-0 focus:ring-0 focus:ring-offset-0 focus-visible:ring-0 focus-visible:ring-offset-0 placeholder:text-gray-400 text-white"
          />
        </div>

        <CommandEmpty class="text-white bg-primary-700 border-0">{{ emptyMessage || "No items found." }}</CommandEmpty>
        <CommandList class="bg-primary-700 border-0">
          <CommandGroup class="bg-primary-700 border-0">
            <CommandItem
              v-for="item in filteredItems"
              :key="item.value"
              :value="item.value"
              class="bg-primary-700 text-white hover:bg-primary-600"
              @select="(ev) => {
                if (typeof ev.detail.value === 'string') {
                  toggleItem(ev.detail.value)
                }
              }"
            >
              <div class="flex items-center">
                {{ item.label }}
                <Check
                  :class="cn(
                    'ml-auto h-4 w-4',
                    selectedValues.includes(item.value) ? 'opacity-100' : 'opacity-0'
                  )"
                />
              </div>
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>

<style scoped>
.popover-content {
  width: var(--radix-popover-trigger-width);
  max-height: var(--radix-popover-content-available-height);
}

:deep(.command) {
  border: none !important;
}

:deep(.command-list) {
  border: none !important;
}

:deep(.command-group) {
  border: none !important;
}

:deep(.input) {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

:deep(.input:focus) {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

:deep(.input:focus-visible) {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}
</style>
