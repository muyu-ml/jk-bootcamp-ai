import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { TicketCard } from '@/components/tickets/TicketCard'
import type { Ticket } from '@/types/ticket'

const mockTicket: Ticket = {
  id: 1,
  title: 'Test Ticket',
  description: 'Test Description',
  status: 'pending',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  completed_at: null,
  tags: [],
}

describe('TicketCard', () => {
  it('renders ticket title and description', () => {
    const onEdit = vi.fn()
    const onDelete = vi.fn()
    const onToggleComplete = vi.fn()

    render(
      <TicketCard
        ticket={mockTicket}
        onEdit={onEdit}
        onDelete={onDelete}
        onToggleComplete={onToggleComplete}
      />
    )

    expect(screen.getByText('Test Ticket')).toBeInTheDocument()
    expect(screen.getByText('Test Description')).toBeInTheDocument()
  })

  it('renders completed ticket with strikethrough', () => {
    const completedTicket: Ticket = {
      ...mockTicket,
      status: 'completed',
      completed_at: '2024-01-02T00:00:00Z',
    }

    const onEdit = vi.fn()
    const onDelete = vi.fn()
    const onToggleComplete = vi.fn()

    render(
      <TicketCard
        ticket={completedTicket}
        onEdit={onEdit}
        onDelete={onDelete}
        onToggleComplete={onToggleComplete}
      />
    )

    const title = screen.getByText('Test Ticket')
    expect(title).toHaveClass('line-through')
  })

  it('calls onToggleComplete when check button is clicked', async () => {
    const user = userEvent.setup()
    const onEdit = vi.fn()
    const onDelete = vi.fn()
    const onToggleComplete = vi.fn()

    render(
      <TicketCard
        ticket={mockTicket}
        onEdit={onEdit}
        onDelete={onDelete}
        onToggleComplete={onToggleComplete}
      />
    )

    const checkButton = screen.getByRole('button', { name: /complete/i })
    await user.click(checkButton)

    expect(onToggleComplete).toHaveBeenCalledWith(1)
  })

  it('calls onEdit when edit button is clicked', async () => {
    const user = userEvent.setup()
    const onEdit = vi.fn()
    const onDelete = vi.fn()
    const onToggleComplete = vi.fn()

    render(
      <TicketCard
        ticket={mockTicket}
        onEdit={onEdit}
        onDelete={onDelete}
        onToggleComplete={onToggleComplete}
      />
    )

    const editButton = screen.getByRole('button', { name: /编辑/i })
    await user.click(editButton)

    expect(onEdit).toHaveBeenCalledWith(mockTicket)
  })

  it('calls onDelete when delete button is clicked', async () => {
    const user = userEvent.setup()
    const onEdit = vi.fn()
    const onDelete = vi.fn()
    const onToggleComplete = vi.fn()

    render(
      <TicketCard
        ticket={mockTicket}
        onEdit={onEdit}
        onDelete={onDelete}
        onToggleComplete={onToggleComplete}
      />
    )

    const deleteButton = screen.getByRole('button', { name: /删除/i })
    await user.click(deleteButton)

    expect(onDelete).toHaveBeenCalledWith(1)
  })

  it('displays tags when present', () => {
    const ticketWithTags: Ticket = {
      ...mockTicket,
      tags: [
        { id: 1, name: 'Tag 1', color: '#FF0000', created_at: '2024-01-01T00:00:00Z', ticket_count: 1 },
        { id: 2, name: 'Tag 2', color: '#00FF00', created_at: '2024-01-01T00:00:00Z', ticket_count: 1 },
      ],
    }

    const onEdit = vi.fn()
    const onDelete = vi.fn()
    const onToggleComplete = vi.fn()

    render(
      <TicketCard
        ticket={ticketWithTags}
        onEdit={onEdit}
        onDelete={onDelete}
        onToggleComplete={onToggleComplete}
      />
    )

    expect(screen.getByText('Tag 1')).toBeInTheDocument()
    expect(screen.getByText('Tag 2')).toBeInTheDocument()
  })
})
