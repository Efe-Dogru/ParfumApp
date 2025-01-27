export const usePerfumes = () => {
    const client = useSupabaseClient()
    
    const getPerfumes = async () => {
        const { data } = await useAsyncData('perfumes', async () => {
            return await client.from('perfumes').select('id, name').limit(5)
        }, {
            transform: result => result.data
        })
        
        return data
    }

    return {
        getPerfumes
    }
} 