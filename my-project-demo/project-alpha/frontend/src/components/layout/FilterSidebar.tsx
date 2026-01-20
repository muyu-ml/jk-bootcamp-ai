import { useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'
import { X } from 'lucide-react'
import { useTicketStore } from '@/store/useTicketStore'
import { TagBadge } from '@/components/tags/TagBadge'
import { cn } from '@/lib/utils'

export function FilterSidebar() {
  const {
    statusFilter,
    selectedTagIds,
    tags,
    setStatusFilter,
    setSelectedTagIds,
    fetchTags,
  } = useTicketStore()

  useEffect(() => {
    fetchTags()
  }, [fetchTags])

  const toggleTag = (tagId: number) => {
    if (selectedTagIds.includes(tagId)) {
      setSelectedTagIds(selectedTagIds.filter((id) => id !== tagId))
    } else {
      setSelectedTagIds([...selectedTagIds, tagId])
    }
  }

  const clearFilters = () => {
    setStatusFilter('all')
    setSelectedTagIds([])
  }

  const hasActiveFilters = statusFilter !== 'all' || selectedTagIds.length > 0

  return (
    <aside className="w-72 border-r border-border/50 bg-muted/20 p-6">
      <div className="space-y-8">
        <div>
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            状态
          </h2>
          <div className="space-y-1.5">
            {(['all', 'pending', 'completed'] as const).map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={cn(
                  "w-full flex items-center space-x-3 rounded-xl px-4 py-3 text-left transition-all duration-200",
                  "hover:bg-accent/50 active:scale-[0.98]",
                  statusFilter === status && "bg-accent font-medium"
                )}
              >
                <Checkbox
                  id={status}
                  checked={statusFilter === status}
                  onCheckedChange={() => setStatusFilter(status)}
                  className="pointer-events-none"
                />
                <label
                  htmlFor={status}
                  className="text-sm font-medium leading-none cursor-pointer flex-1"
                >
                  {status === 'all' ? '全部' : status === 'pending' ? '待完成' : '已完成'}
                </label>
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
              标签
            </h2>
            {hasActiveFilters && (
              <Button
                variant="ghost"
                size="sm"
                onClick={clearFilters}
                className="h-8 w-8 rounded-lg p-0 hover:bg-accent/50"
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
          <ScrollArea className="h-[500px] -mx-2 px-2">
            <div className="space-y-1.5">
              {tags.length === 0 ? (
                <p className="text-sm text-muted-foreground px-4 py-8 text-center">暂无标签</p>
              ) : (
                tags.map((tag) => (
                  <button
                    key={tag.id}
                    onClick={() => toggleTag(tag.id)}
                    className={cn(
                      "w-full flex items-center justify-between rounded-xl px-4 py-3 transition-all duration-200",
                      "hover:bg-accent/50 active:scale-[0.98]",
                      selectedTagIds.includes(tag.id) && "bg-accent/30"
                    )}
                  >
                    <div className="flex items-center space-x-3 flex-1 min-w-0">
                      <Checkbox
                        checked={selectedTagIds.includes(tag.id)}
                        onCheckedChange={() => toggleTag(tag.id)}
                        className="pointer-events-none shrink-0"
                      />
                      <div className="min-w-0 flex-1">
                        <TagBadge tag={tag} variant="outline" />
                      </div>
                    </div>
                    {tag.ticket_count !== undefined && (
                      <Badge 
                        variant="secondary" 
                        className="ml-3 shrink-0 h-6 px-2 rounded-full text-xs font-medium"
                      >
                        {tag.ticket_count}
                      </Badge>
                    )}
                  </button>
                ))
              )}
            </div>
          </ScrollArea>
        </div>
      </div>
    </aside>
  )
}
