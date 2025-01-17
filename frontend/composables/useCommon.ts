import { ref } from 'vue'
import type { Ref } from 'vue'

interface Note {
  id: number
  name: string
}

interface MainAccord {
  id: number
  name: string
}

interface Occasion {
  id: number
  name: string
}

interface Season {
  id: number
  name: string
}

export interface Perfume {
  id: number
  name: string
  description: string
  brand?: string
  price?: number
  type?: string
  gender?: string
  family?: string
  release_year?: number
  concentration?: string
  longevity?: string
  sillage?: string
  image_url?: string
  perfumer?: string
  inspiration?: string
  top_notes?: Note[]
  middle_notes?: Note[]
  base_notes?: Note[]
  main_accords?: MainAccord[]
  occasions?: Occasion[]
  seasons?: Season[]
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

export const usePerfumes = () => {
  const perfumes: Ref<Perfume[]> = ref([])
  const { isLoading, error, setLoading, setError } = useCommon()

  const fetchPerfumes = async () => {
    setLoading(true)
    setError(null)
    try {
      // TODO: Replace with actual API call
      perfumes.value = [
        { id: 1, name: 'Sample Perfume 1', description: 'A delightful fragrance' },
        { id: 2, name: 'Sample Perfume 2', description: 'An enchanting scent' },
        { id: 3, name: 'Sample Perfume 3', description: 'A mysterious aroma' },
      ]
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to fetch perfumes')
    } finally {
      setLoading(false)
    }
  }

  return {
    perfumes,
    isLoading,
    error,
    fetchPerfumes
  }
} 