export interface Tag {
  id: number
  name: string
  color: string
  created_at: string
  ticket_count?: number
}

export interface TagCreate {
  name: string
  color?: string
}

export interface TagUpdate {
  name?: string
  color?: string
}

// Tags API returns Tag[] directly, not wrapped
