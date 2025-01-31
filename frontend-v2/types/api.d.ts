export interface Perfume {
    id: number
    brand_id: number
    name: string
    category: string
    concentration_id: number
    local_image_path: string
    gender: string
    type_id: number
    family_id: number
    release_year: number
    country_id: number
    description: string
    longevity: string
    sillage: string
    occasion: string[]
    season: string[]
    perfumer_id: number
    inspiration: string
    brands: Brand
    perfume_notes?: PerfumeNote[]
}

export interface Brand {
    id: number
    name: string
}

export interface Note {
    id: number
    name: string
    image_filename: string | null
    description: string | null
    family_id: number | null
    source: string | null
    cultural_significance: string | null
    normalized_name: string | null
}

export interface PerfumeNote {
    perfume_id: number
    note_id: number
    note_type: 'top' | 'middle' | 'base'
    note: Note
}

export interface Concentration{
    id: number
    name: string
}

export interface AnimateLogoCloudProps {
    logos: Array<{
        name: string;
        path: string;
    }>;
    title?: string;
    class?: string;
}