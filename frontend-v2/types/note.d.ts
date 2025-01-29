export interface Note {
    id: number
    name: string
    image_filename: string
}

export interface NoteDetails extends Note {
    family: NoteFamily
    description: string | null
    source: string | null
    cultural_significance: string | null
    normalized_name: string | null
    mood: string | null
}
