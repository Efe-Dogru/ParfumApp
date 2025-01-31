import type { Brand, Concentration, Perfume, PerfumeDetails } from '~/types/perfume'

interface PerfumeTagJoin {
    perfumes: Perfume

}
interface FilterParams {
    gender?: string;
    brand_id?: string;
    concentration_id?: string;
    season?: string;

}

export const usePerfumes = () => {
    const client = useSupabaseClient()

    const getBrands = async () => {
        const { data, error } = await client
            .from('brands')
            .select('id, name')
        if (error) throw error
        return data as Brand[]
    }

    const getConcentrations = async () => {
        const { data, error } = await client
            .from('concentration')
            .select('id, name')
        if (error) throw error
        return data as Concentration[]
    }

    const applyFilters = (query: any, filters: FilterParams) => {
        if (filters.gender && filters.gender !== 'all') {
            query = query.eq('gender', filters.gender)
        }
        if (filters.brand_id && filters.brand_id !== 'all') {
            query = query.eq('brand_id', filters.brand_id)
        }
        if (filters.concentration_id && filters.concentration_id !== 'all') {
            query = query.eq('concentration_id', filters.concentration_id)
        }
        if (filters.season && filters.season !== 'all') {
            query = query.contains('season', [filters.season])
        }
        return query
    }

    const searchPerfume = async (search: string, filters: FilterParams = {}) => {
        let query = client
            .from('perfumes')
            .select('id, name, local_image_path, brands:brand_id(name)')

        // Apply text search if search is provided
        if (search.trim()) {
             query = query.ilike('name', `%${search}%`)
        }

        // Apply filters
        query = applyFilters(query, filters)

        const { data, error } = await query
        if (error) throw error
        return { data }
    }
    
    const getPerfumes = async (page: number = 1, itemsPerPage: number = 42, filters: FilterParams = {}) => {
        const start = (page - 1) * itemsPerPage
        const end = start + itemsPerPage - 1

        let query = client.from('perfumes')
        
        // Apply filters to count query
        let countQuery = applyFilters(
            client.from('perfumes').select('*', { count: 'exact', head: true }),
            filters
        )

        // Apply filters to main query
        query = applyFilters(
            query.select('id, name, local_image_path, brands:brand_id(name)'),
            filters
        )

        const [countResult, { data, error }] = await Promise.all([
            countQuery,
            query.range(start, end)
        ])

        if (error) throw error
        
        return {
            data: data as Perfume[],
            count: countResult.count || 0
        }
    }


    const getPerfumeDetails = async (id: number) => {
        const { data, error } = await client
            .from('perfumes')
            .select(`
                id,
                category,
                description,
                gender,
                inspiration,
                local_image_path,
                longevity,
                name,
                country:country_id(name),
                family:family_id(name),
                type:type_id(name),
                concentration:concentration_id(name),
                perfumer:perfumer_id(name),
                brands:brand_id(name),
                occasion,
                release_year,
                season,
                sillage,
                notes:perfume_notes(
                    note_id,
                    note_type,
                    notes:note_id(
                        name,
                        image_filename
                    )
                ),
                accords:perfume_main_accords(
                    main_accords:accord_id(
                        id,
                        name
                    )
                )
                
            `)
            .eq('id', id)
            .single()

        if (error) throw error
        return data as PerfumeDetails
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
        getPerfumeDetails,
        getTrendingPerfumes,
        getTopRatedPerfumes,
        getMostLovedPerfumes,
        searchPerfume,
        getBrands,
        getConcentrations
    }
}