export interface Perfume {
    id: number
    name: string
    local_image_path: string
    brands: Brand
}

export interface PerfumeDetails extends Perfume {
    category: string
    description: string
    gender: string
    inspiration: string
    longevity: string
    country: Country
    family: Family
    type: Type
    concentration: Concentration
    perfumer: Perfumer
    occasion: string[]
    release_year: number
    season: string[]
    sillage: string
    notes: {
        note_id: number
        note_type: 'top' | 'middle' | 'base'
        notes: {
            id: number
            name: string
            image_filename: string
        }
    }[]
    accords: {
        main_accords: {
            id: number
            name: string
        }
    }[]
}

export interface Country {
    id: number
    name: string
}

export interface Family {
    id: number
    name: string
}

export interface Type {
    id: number
    name: string
}


export interface Brand {
    id: number
    name: string
}

export interface Perfumer {
    id: number
    name: string
}

export interface PerfumeNote {
    note_id: number
    note_type: 'top' | 'middle' | 'base'
    notes: {
        id: number
        name: string
        image_filename?: string
    }
}

export interface Concentration{
    id: number
    name: string
}

export interface MainAccord {
    id: number
    name: string
}
