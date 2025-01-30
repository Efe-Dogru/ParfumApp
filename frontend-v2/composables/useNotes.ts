import type { Note, NoteDetails } from '@/types/note'

export const useNotes = () => {
    const client = useSupabaseClient()
    
    const getNotes = async (page: number = 1, itemsPerPage: number = 42, filters: any = {}): Promise<{ data: Note[], count: number }> => {
        const startRow = (page - 1) * itemsPerPage
        const endRow = startRow + itemsPerPage - 1

        let query = client
            .from('notes')
            .select('id, name, image_filename, family_id', { count: 'exact' })
            .range(startRow, endRow)

        if (filters.family_id && filters.family_id !== 'all') {
            query = query.eq('family_id', filters.family_id)
        }

        const { data, error, count } = await query

        if (error) throw error
        return { 
            data: data as Note[], 
            count: count || 0 
        }
    }

    const searchNotes = async (searchQuery: string, filters: any = {}): Promise<{ data: Note[], count: number }> => {
        let query = client
            .from('notes')
            .select('id, name, image_filename, family_id', { count: 'exact' })
            .ilike('name', `%${searchQuery}%`)

        if (filters.family_id && filters.family_id !== 'all') {
            query = query.eq('family_id', filters.family_id)
        }

        const { data, error, count } = await query

        if (error) throw error
        return { 
            data: data as Note[], 
            count: count || 0 
        }
    }

    const getNoteFamilies = async () => {
        const { data, error } = await client
            .from('note_families')
            .select('id, name')
            .order('name')

        if (error) throw error
        return data
    }

    const getNoteDetails = async (id: number) => {
        const { data, error } = await client
            .from('notes')
            .select(`
                id,
                name,
                image_filename,
                description,
                family:family_id(name),
                source,
                cultural_significance,
                moods:note_mood_relations(
                    mood:mood_id(
                        id,
                        name
                    )
                )
            `)
            .eq('id', id)
            .single()

        if (error) throw error
        return data as NoteDetails
    }

    return {
        getNotes,
        searchNotes,
        getNoteFamilies,
        getNoteDetails
    }
} 