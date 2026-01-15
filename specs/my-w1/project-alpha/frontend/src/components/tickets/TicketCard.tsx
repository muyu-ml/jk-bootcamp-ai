import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Check, Edit, Trash2 } from 'lucide-react'
import { TagBadge } from '@/components/tags/TagBadge'
import type { Ticket } from '@/types/ticket'
import { cn } from '@/lib/utils'
import { format } from 'date-fns'

interface TicketCardProps {
  ticket: Ticket
  onEdit: (ticket: Ticket) => void
  onDelete: (ticketId: number) => void
  onToggleComplete: (ticketId: number) => void
}

export function TicketCard({ ticket, onEdit, onDelete, onToggleComplete }: TicketCardProps) {
  const isCompleted = ticket.status === 'completed'

  return (
    <Card className={cn('transition-all hover:shadow-md', isCompleted && 'opacity-75')}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className={cn('text-lg font-semibold', isCompleted && 'line-through text-muted-foreground')}>
              {ticket.title}
            </h3>
            {ticket.description && (
              <p className="mt-2 text-sm text-muted-foreground line-clamp-2">
                {ticket.description}
              </p>
            )}
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onToggleComplete(ticket.id)}
            className={cn(
              'shrink-0',
              isCompleted && 'text-green-600 hover:text-green-700'
            )}
          >
            <Check className={cn('h-5 w-5', isCompleted && 'fill-current')} />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {ticket.tags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {ticket.tags.map((tag) => (
              <TagBadge key={tag.id} tag={tag} variant="outline" />
            ))}
          </div>
        )}
        <div className="mt-4 text-xs text-muted-foreground">
          <div>创建时间: {format(new Date(ticket.created_at), 'yyyy-MM-dd HH:mm')}</div>
          {ticket.completed_at && (
            <div>完成时间: {format(new Date(ticket.completed_at), 'yyyy-MM-dd HH:mm')}</div>
          )}
        </div>
      </CardContent>
      <CardFooter className="flex justify-end gap-2">
        <Button variant="outline" size="sm" onClick={() => onEdit(ticket)}>
          <Edit className="mr-2 h-4 w-4" />
          编辑
        </Button>
        <Button variant="destructive" size="sm" onClick={() => onDelete(ticket.id)}>
          <Trash2 className="mr-2 h-4 w-4" />
          删除
        </Button>
      </CardFooter>
    </Card>
  )
}
