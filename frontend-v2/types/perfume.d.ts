export interface PerfumeDetails{
    id: number
    category: string
    description: string
    gender: string
    inspiration: string
    local_image_path: string
    longevity: string
    name: string
    country: Country
    family: Family
    type: Type
    concentration: Concentration
    perfumer: Perfumer
    brands: Brand
    occasion: string[]
    release_year: number
    season: string[]
    sillage: string
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

export interface Perfume {
    id: number
    name: string
    local_image_path: string
    brands: Brand
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
    perfume_id: number
    note_id: number
    note_type: 'top' | 'middle' | 'base'
    note: Note
}

export interface Concentration{
    id: number
    name: string
}

export interface MainAccord {
    id: number
    name: string
}
