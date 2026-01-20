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
    <Card className={cn(
      'group transition-all duration-300 hover:shadow-lg hover:-translate-y-1',
      isCompleted && 'opacity-60'
    )}>
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-start gap-3">
              <button
                onClick={() => onToggleComplete(ticket.id)}
                className={cn(
                  "mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition-all duration-200",
                  "hover:scale-110 active:scale-95",
                  isCompleted 
                    ? "border-primary bg-primary text-primary-foreground" 
                    : "border-border hover:border-primary/50"
                )}
              >
                {isCompleted && <Check className="h-3.5 w-3.5" />}
              </button>
              <div className="flex-1 min-w-0">
                <h3 className={cn(
                  'text-lg font-semibold leading-tight tracking-tight mb-2',
                  isCompleted && 'line-through text-muted-foreground'
                )}>
                  {ticket.title}
                </h3>
                {ticket.description && (
                  <p className={cn(
                    "text-sm leading-relaxed line-clamp-3",
                    isCompleted ? "text-muted-foreground/70" : "text-muted-foreground"
                  )}>
                    {ticket.description}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        {ticket.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {ticket.tags.map((tag) => (
              <TagBadge key={tag.id} tag={tag} variant="outline" />
            ))}
          </div>
        )}
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <span className="font-medium">
            {format(new Date(ticket.created_at), 'MMM d, yyyy')}
          </span>
          {ticket.completed_at && (
            <span className="text-primary">
              {format(new Date(ticket.completed_at), 'MMM d, yyyy')}
            </span>
          )}
        </div>
      </CardContent>
      <CardFooter className="flex justify-end gap-2 pt-4 border-t border-border/50">
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={() => onEdit(ticket)}
          className="h-9 rounded-lg hover:bg-accent/50"
        >
          <Edit className="mr-2 h-4 w-4" />
          编辑
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={() => onDelete(ticket.id)}
          className="h-9 rounded-lg text-destructive hover:bg-destructive/10 hover:text-destructive"
        >
          <Trash2 className="mr-2 h-4 w-4" />
          删除
        </Button>
      </CardFooter>
    </Card>
  )
}
