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

