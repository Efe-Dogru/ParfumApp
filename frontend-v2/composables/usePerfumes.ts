import type { Perfume } from '~/types/api'

export const usePerfumes = () => {
    const client = useSupabaseClient()
    
    const getPerfumes = async (page: number = 1, itemsPerPage: number = 42) => {
        const start = (page - 1) * itemsPerPage
        const end = start + itemsPerPage - 1

        const countQuery = await client
            .from('perfumes')
            .select('*', { count: 'exact', head: true })

        const { data, error } = await client
            .from('perfumes')
            .select('id, name, local_image_path, brands:brand_id(name)')
            .range(start, end)

        if (error) throw error
        
        return {
            data: data as Perfume[],
            count: countQuery.count || 0
        }
    }

    const getPerfume = async (id: number) => {
        const { data, error } = await client
            .from('perfumes')
            .select(`
                *,
                brands:brand_id(*)
            `)
            .eq('id', id)
            .single()

        if (error) throw error
        return data as Perfume
    }

    return {
        getPerfumes,
        getPerfume
    }
}