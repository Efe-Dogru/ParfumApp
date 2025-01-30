export interface Note {
    id: number
    name: string
    image_filename: string
}

interface NoteMood {
    id: number
    name: string
}

interface NoteMoodRelation {
    mood: NoteMood
}

export interface NoteDetails extends Note {
    family: NoteFamily
    description: string | null
    source: string | null
    cultural_significance: string | null
    normalized_name: string | null
    mood: string | null
    moods: NoteMoodRelation[]
}

export interface NoteFamily {
    id: number
    name: string
}
