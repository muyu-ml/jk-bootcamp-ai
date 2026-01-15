import { Badge } from '@/components/ui/badge'
import { X } from 'lucide-react'
import type { Tag } from '@/types/tag'
import { cn } from '@/lib/utils'

interface TagBadgeProps {
  tag: Tag
  onRemove?: () => void
  variant?: 'default' | 'outline'
  className?: string
}

export function TagBadge({ tag, onRemove, variant = 'default', className }: TagBadgeProps) {
  return (
    <Badge
      variant={variant}
      className={cn('flex items-center gap-1', className)}
      style={
        variant === 'outline'
          ? { borderColor: tag.color, color: tag.color }
          : { backgroundColor: tag.color, borderColor: tag.color, color: '#fff' }
      }
    >
      <span className="text-xs font-medium">{tag.name}</span>
      {onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation()
            onRemove()
          }}
          className="ml-1 rounded-full hover:bg-black/20"
        >
          <X className="h-3 w-3" />
        </button>
      )}
    </Badge>
  )
}
