import { create } from 'zustand'
import type { Ticket, TicketCreate, TicketUpdate } from '@/types/ticket'
import type { Tag, TagCreate, TagUpdate } from '@/types/tag'
import { ticketsApi, tagsApi } from '@/lib/api'

interface TicketStore {
  // State
  tickets: Ticket[]
  tags: Tag[]
  isLoading: boolean
  error: string | null

  // Filters
  statusFilter: 'all' | 'pending' | 'completed'
  selectedTagIds: number[]
  searchQuery: string

  // Ticket Actions
  fetchTickets: () => Promise<void>
  createTicket: (data: TicketCreate) => Promise<void>
  updateTicket: (id: number, data: TicketUpdate) => Promise<void>
  deleteTicket: (id: number) => Promise<void>
  toggleComplete: (id: number) => Promise<void>

  // Tag Actions
  fetchTags: () => Promise<void>
  createTag: (data: TagCreate) => Promise<void>
  updateTag: (id: number, data: TagUpdate) => Promise<void>
  deleteTag: (id: number) => Promise<void>

  // Filter Actions
  setStatusFilter: (status: 'all' | 'pending' | 'completed') => void
  setSelectedTagIds: (ids: number[]) => void
  setSearchQuery: (query: string) => void
}

export const useTicketStore = create<TicketStore>((set, get) => ({
  // Initial state
  tickets: [],
  tags: [],
  isLoading: false,
  error: null,
  statusFilter: 'all',
  selectedTagIds: [],
  searchQuery: '',

  // Ticket Actions
  fetchTickets: async () => {
    set({ isLoading: true, error: null })
    try {
      const { statusFilter, selectedTagIds, searchQuery } = get()
      const response = await ticketsApi.getAll({
        status: statusFilter === 'all' ? undefined : statusFilter,
        tag_ids: selectedTagIds.length > 0 ? selectedTagIds : undefined,
        search: searchQuery || undefined,
      })
      set({ tickets: response.tickets, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch tickets',
        isLoading: false,
      })
    }
  },

  createTicket: async (data: TicketCreate) => {
    set({ isLoading: true, error: null })
    try {
      await ticketsApi.create(data)
      await get().fetchTickets()
      await get().fetchTags()
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create ticket',
        isLoading: false,
      })
      throw error
    }
  },

  updateTicket: async (id: number, data: TicketUpdate) => {
    set({ isLoading: true, error: null })
    try {
      await ticketsApi.update(id, data)
      await get().fetchTickets()
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update ticket',
        isLoading: false,
      })
      throw error
    }
  },

  deleteTicket: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      await ticketsApi.delete(id)
      await get().fetchTickets()
      await get().fetchTags()
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete ticket',
        isLoading: false,
      })
      throw error
    }
  },

  toggleComplete: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      const ticket = get().tickets.find((t) => t.id === id)
      if (ticket?.status === 'completed') {
        await ticketsApi.uncomplete(id)
      } else {
        await ticketsApi.complete(id)
      }
      await get().fetchTickets()
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to toggle ticket status',
        isLoading: false,
      })
      throw error
    }
  },

  // Tag Actions
  fetchTags: async () => {
    try {
      const tags = await tagsApi.getAll()
      set({ tags })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch tags',
      })
    }
  },

  createTag: async (data: TagCreate) => {
    set({ isLoading: true, error: null })
    try {
      await tagsApi.create(data)
      await get().fetchTags()
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create tag',
        isLoading: false,
      })
      throw error
    }
  },

  updateTag: async (id: number, data: TagUpdate) => {
    set({ isLoading: true, error: null })
    try {
      await tagsApi.update(id, data)
      await get().fetchTags()
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update tag',
        isLoading: false,
      })
      throw error
    }
  },

  deleteTag: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      await tagsApi.delete(id)
      await get().fetchTags()
      await get().fetchTickets()
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete tag',
        isLoading: false,
      })
      throw error
    }
  },

  // Filter Actions
  setStatusFilter: (status: 'all' | 'pending' | 'completed') => {
    set({ statusFilter: status })
    get().fetchTickets()
  },

  setSelectedTagIds: (ids: number[]) => {
    set({ selectedTagIds: ids })
    get().fetchTickets()
  },

  setSearchQuery: (query: string) => {
    set({ searchQuery: query })
    // Debounce will be handled in the component
  },
}))
