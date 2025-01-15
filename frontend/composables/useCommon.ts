import { ref } from 'vue'
import type { Ref } from 'vue'

export interface Perfume {
  id: number | string
  name: string
  description: string
  brand?: string
  year?: number
  notes?: {
    top: string[]
    heart: string[]
    base: string[]
  }
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