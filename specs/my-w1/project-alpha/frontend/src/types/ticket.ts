import { Tag } from './tag'

export type TicketStatus = 'pending' | 'completed'

export interface Ticket {
  id: number
  title: string
  description?: string
  status: TicketStatus
  tags: Tag[]
  created_at: string
  updated_at?: string
  completed_at?: string
}

export interface TicketCreate {
  title: string
  description?: string
  tag_ids?: number[]
}

export interface TicketUpdate {
  title?: string
  description?: string
}

export interface TicketListResponse {
  tickets: Ticket[]
  total: number
  limit: number
  offset: number
}
