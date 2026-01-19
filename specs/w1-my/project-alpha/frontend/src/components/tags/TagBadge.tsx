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
      className={cn(
        'flex items-center gap-1.5 transition-all duration-200',
        variant === 'outline' && 'hover:shadow-sm',
        className
      )}
      style={
        variant === 'outline'
          ? { 
              borderColor: tag.color + '40', 
              color: tag.color,
              backgroundColor: tag.color + '10'
            }
          : { 
              backgroundColor: tag.color, 
              borderColor: tag.color, 
              color: '#fff' 
            }
      }
    >
      <span className="text-xs font-medium leading-none">{tag.name}</span>
      {onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation()
            onRemove()
          }}
          className="ml-0.5 rounded-full p-0.5 hover:bg-black/20 transition-colors duration-200 active:scale-95"
        >
          <X className="h-3 w-3" />
        </button>
      )}
    </Badge>
  )
}
