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
    <aside className="w-64 border-r bg-muted/40 p-4">
      <div className="space-y-6">
        <div>
          <h2 className="mb-4 text-lg font-semibold">状态过滤</h2>
          <div className="space-y-2">
            {(['all', 'pending', 'completed'] as const).map((status) => (
              <div key={status} className="flex items-center space-x-2">
                <Checkbox
                  id={status}
                  checked={statusFilter === status}
                  onCheckedChange={() => setStatusFilter(status)}
                />
                <label
                  htmlFor={status}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                >
                  {status === 'all' ? '全部' : status === 'pending' ? '待完成' : '已完成'}
                </label>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">标签过滤</h2>
            {hasActiveFilters && (
              <Button
                variant="ghost"
                size="sm"
                onClick={clearFilters}
                className="h-8 px-2"
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
          <ScrollArea className="h-[400px]">
            <div className="space-y-2">
              {tags.length === 0 ? (
                <p className="text-sm text-muted-foreground">暂无标签</p>
              ) : (
                tags.map((tag) => (
                  <div
                    key={tag.id}
                    className="flex items-center justify-between rounded-md p-2 hover:bg-accent cursor-pointer"
                    onClick={() => toggleTag(tag.id)}
                  >
                    <div className="flex items-center space-x-2 flex-1">
                      <Checkbox
                        checked={selectedTagIds.includes(tag.id)}
                        onCheckedChange={() => toggleTag(tag.id)}
                      />
                      <TagBadge tag={tag} variant="outline" />
                    </div>
                    {tag.ticket_count !== undefined && (
                      <Badge variant="secondary" className="ml-2">
                        {tag.ticket_count}
                      </Badge>
                    )}
                  </div>
                ))
              )}
            </div>
          </ScrollArea>
        </div>
      </div>
    </aside>
  )
}
