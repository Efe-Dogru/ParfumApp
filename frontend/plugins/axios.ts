import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  
  const api = axios.create({
    baseURL: config.public.apiBase,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // Add request interceptor to handle errors
  api.interceptors.request.use(
    (config) => {
      return config
    },
    (error) => {
      console.error('API Request Error:', error)
      return Promise.reject(error)
    }
  )

  // Add response interceptor for better error handling
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      console.error('API Response Error:', error)
      return Promise.reject(error)
    }
  )

  return {
    provide: {
      axios: api
    }
  }
}) 