import { ref } from 'vue'
import type { Ref } from 'vue'

interface Brand {
  id: number
  name: string
}

interface Type {
  id: number
  name: string
}

interface Family {
  id: number
  name: string
}

interface Concentration {
  id: number
  name: string
}

interface Country {
  id: number
  name: string
}

interface Perfumer {
  id: number
  name: string
}

export interface Note {
  id: number
  name: string
  image_filename?: string
  description?: string
  family?: string
  source?: string
  cultural_significance?: string
  mood?: string
}

interface MainAccord {
  id: string
  name: string
}

export interface Perfume {
  // Fields in the same order as backend model
  id: number
  name: string
  brand_id: number
  concentration: string
  local_image_path?: string
  gender?: string
  year?: string // ???
  category: string,

  type_id: number
  family_id: number

  release_year?: number
  country_id: number
  description?: string
  longevity?: string
  sillage?: string
  occasion?: string[]
  season?: string[]
  perfumer_id: number
  inspiration?: string
  istrend?: any
  assets?: string[]

  // Relationships (same order as backend)
  brand?: Brand
  type?: Type
  family?: Family
  country?: Country
  perfumer?: Perfumer
  top_notes?: Note[]
  middle_notes?: Note[]
  base_notes?: Note[]
  main_accords?: MainAccord[]
}

export const useCommon = () => {
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  return {
    isLoading,
    error,
    setLoading,
    setError
  }
}


