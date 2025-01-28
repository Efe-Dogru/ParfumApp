import type { Perfume } from '~/types/api'
import type { SupabaseClient } from '@supabase/supabase-js'

interface PerfumeTagJoin {
    perfumes: Perfume
}

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

    const getTrendingPerfumes = async (limit: number = 8) => {
        const { data, error } = await client
            .from('perfume_tags')
            .select('perfumes:perfume_id(id, name, local_image_path, brands:brand_id(name))')
            .eq('tag_id', 1)
            .limit(limit)

        if (error) throw error
        return (data?.map(item => (item as PerfumeTagJoin).perfumes) || []) as Perfume[]
    }

    const getTopRatedPerfumes = async (limit: number = 8) => {
        const { data, error } = await client
            .from('perfume_tags')
            .select('perfumes:perfume_id(id, name, local_image_path, brands:brand_id(name))')
            .eq('tag_id', 2)
            .limit(limit)

        if (error) throw error
        return (data?.map(item => (item as PerfumeTagJoin).perfumes) || []) as Perfume[]
    }

    const getMostLovedPerfumes = async (limit: number = 8) => {
        const { data, error } = await client
            .from('perfume_tags')
            .select('perfumes:perfume_id(id, name, local_image_path, brands:brand_id(name))')
            .eq('tag_id', 3)
            .limit(limit)

        if (error) throw error
        return (data?.map(item => (item as PerfumeTagJoin).perfumes) || []) as Perfume[]
    }

    return {
        getPerfumes,
        getTrendingPerfumes,
        getTopRatedPerfumes,
        getMostLovedPerfumes
    }
}