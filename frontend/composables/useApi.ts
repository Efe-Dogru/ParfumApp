export function useApi() {
  const { $axios } = useNuxtApp()

  const getPerfumes = (page: number = 1, limit: number = 42) => 
    $axios.get(`/api/v1/perfumes/?skip=${(page - 1) * limit}&limit=${limit}`)
  const getPerfumeById = (id: string) => $axios.get(`/api/v1/perfumes/${id}`)
  const searchPerfumes = (query: string) => $axios.get(`/api/v1/perfumes/?search=${query}&limit=10`)

  return {
    getPerfumes,
    getPerfumeById,
    searchPerfumes,
  }
} 