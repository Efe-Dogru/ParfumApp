export const useNotes = () => {
    const client = useSupabaseClient()
    
    const getNotes = async () => {
        const { data } = await useAsyncData('notes', async () => {
            return await client.from('notes').select('id, name').limit(5)
        }, {
            transform: result => result.data
        })
        
        return data
    }

    return {
        getNotes
    }
} 