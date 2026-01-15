import { useEffect } from 'react'
import { TicketCard } from './TicketCard'
import { Skeleton } from '@/components/ui/skeleton'
import { Card } from '@/components/ui/card'
import { useTicketStore } from '@/store/useTicketStore'
import { AlertCircle } from 'lucide-react'

interface TicketListProps {
  onEdit: (ticket: any) => void
  onDelete: (ticketId: number) => void
  onToggleComplete: (ticketId: number) => void
}

export function TicketList({ onEdit, onDelete, onToggleComplete }: TicketListProps) {
  const { tickets, isLoading, error, fetchTickets } = useTicketStore()

  useEffect(() => {
    fetchTickets()
  }, [fetchTickets])

  if (isLoading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="p-6">
            <Skeleton className="h-6 w-3/4 mb-4" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-2/3" />
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <AlertCircle className="h-12 w-12 text-destructive mb-4" />
        <h3 className="text-lg font-semibold mb-2">加载失败</h3>
        <p className="text-sm text-muted-foreground">{error}</p>
      </div>
    )
  }

  if (tickets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <p className="text-lg font-semibold mb-2">暂无 tickets</p>
        <p className="text-sm text-muted-foreground">创建你的第一个 ticket 开始使用</p>
      </div>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {tickets.map((ticket) => (
        <TicketCard
          key={ticket.id}
          ticket={ticket}
          onEdit={onEdit}
          onDelete={onDelete}
          onToggleComplete={onToggleComplete}
        />
      ))}
    </div>
  )
}
