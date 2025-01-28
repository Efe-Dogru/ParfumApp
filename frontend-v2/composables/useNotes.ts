import type { Note, PerfumeNote } from '~/types/api'

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

    const getPerfumeNotes = async (perfumeId: number): Promise<PerfumeNote[]> => {
        const { data: perfumeNotes, error } = await client
            .from('perfume_notes')
            .select(`
                perfume_id,
                note_id,
                note_type,
                note:notes (
                    id,
                    name,
                    image_filename,
                    description,
                    family_id,
                    source,
                    cultural_significance,
                    normalized_name
                )
            `)
            .eq('perfume_id', perfumeId)
            .order('note_type')

        if (error) {
            console.error('Error fetching perfume notes:', error)
            return []
        }

        return perfumeNotes as PerfumeNote[]
    }

    return {
        getNotes,
        getPerfumeNotes
    }
} 