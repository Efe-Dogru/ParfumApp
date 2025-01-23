export function useApi() {
  const { $axios } = useNuxtApp()

  const getPerfumes = (page: number = 1, limit: number = 42) => 
    $axios.get(`/api/v1/perfumes/?skip=${(page - 1) * limit}&limit=${limit}`)
  const getPerfumeById = (id: string) => $axios.get(`/api/v1/perfumes/${id}`)
  
  // Filter options endpoints
  const getTypes = () => $axios.get('/api/v1/types/')
  const getFamilies = () => $axios.get('/api/v1/families/')
  const getConcentrations = () => $axios.get('/api/v1/concentrations/')
  const getPerfumers = () => $axios.get('/api/v1/perfumers/')
  const getCountries = () => $axios.get('/api/v1/countries/')
  const getBrands = () => $axios.get('/api/v1/brands/')
  const getNoteFamilies = () => $axios.get('/api/v1/notes/families/')
  const getNoteMoods = () => $axios.get('/api/v1/notes/moods/')
  
  const searchPerfumes = (params: {
    q?: string,
    type?: string,
    family?: string,
    category?: string,
    concentration?: string,
    gender?: string,
    brand?: string,
    perfumer?: string,
    country?: string,
    page?: number,
    limit?: number
  }) => {
    const { page = 1, limit = 42, ...filters } = params
    const queryParams = new URLSearchParams()
    
    // Add filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, String(value))
    })
    
    // Add pagination
    queryParams.append('skip', String((page - 1) * limit))
    queryParams.append('limit', String(limit))
    
    return $axios.get(`/api/v1/perfumes/search/?${queryParams.toString()}`)
  }
  const searchNotes = (query: string) => $axios.get(`/api/v1/notes/search/?q=${query}&limit=10`)

  const getNotes = (params: {
    page?: number,
    limit?: number,
    family?: string,
    mood?: string
  } = {}) => {
    const { page = 1, limit = 42, ...filters } = params
    const queryParams = new URLSearchParams()
    
    // Add filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, String(value))
    })
    
    // Add pagination
    queryParams.append('skip', String((page - 1) * limit))
    queryParams.append('limit', String(limit))
    
    return $axios.get(`/api/v1/notes/?${queryParams.toString()}`)
  }
  const getNoteById = (id: string) => $axios.get(`/api/v1/notes/${id}`)

  return {
    getPerfumes,
    getPerfumeById,
    searchPerfumes,
    searchNotes,
    getNotes,
    getNoteById,
    getTypes,
    getFamilies,
    getConcentrations,
    getPerfumers,
    getCountries,
    getBrands,
    getNoteFamilies,
    getNoteMoods
  }
} 