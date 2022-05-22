
export interface Anime {
    id: number;
    type: string;
    createdAt: string;
    updatedAt: string;
    canonicalTitle: string;
    synopsis: string;
    description: string;
    attributes: {
        posterImage: {
            original: string;
        }
    }

}