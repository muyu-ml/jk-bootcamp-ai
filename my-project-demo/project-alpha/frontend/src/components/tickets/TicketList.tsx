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
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 animate-fade-in">
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="p-6">
            <Skeleton className="h-6 w-3/4 mb-4 rounded-lg" />
            <Skeleton className="h-4 w-full mb-2 rounded-lg" />
            <Skeleton className="h-4 w-2/3 rounded-lg" />
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-center animate-fade-in">
        <div className="rounded-full bg-destructive/10 p-4 mb-6">
          <AlertCircle className="h-8 w-8 text-destructive" />
        </div>
        <h3 className="text-xl font-semibold mb-2">加载失败</h3>
        <p className="text-sm text-muted-foreground max-w-md">{error}</p>
      </div>
    )
  }

  if (tickets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-center animate-fade-in">
        <div className="rounded-full bg-muted p-6 mb-6">
          <svg 
            className="h-12 w-12 text-muted-foreground" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={1.5} 
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
            />
          </svg>
        </div>
        <h3 className="text-xl font-semibold mb-2">暂无 tickets</h3>
        <p className="text-sm text-muted-foreground">创建你的第一个 ticket 开始使用</p>
      </div>
    )
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 animate-fade-in">
      {tickets.map((ticket, index) => (
        <div 
          key={ticket.id}
          className="animate-slide-up"
          style={{ animationDelay: `${index * 0.05}s` }}
        >
          <TicketCard
            ticket={ticket}
            onEdit={onEdit}
            onDelete={onDelete}
            onToggleComplete={onToggleComplete}
          />
        </div>
      ))}
    </div>
  )
}
