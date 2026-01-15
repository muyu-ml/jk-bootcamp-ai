import { useState } from 'react'
import { Check, ChevronsUpDown, Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { useTicketStore } from '@/store/useTicketStore'
import { TagBadge } from './TagBadge'
import type { Tag } from '@/types/tag'

interface TagSelectorProps {
  selectedTagIds: number[]
  onSelectionChange: (tagIds: number[]) => void
  onCreateTag?: () => void
}

export function TagSelector({ selectedTagIds, onSelectionChange, onCreateTag }: TagSelectorProps) {
  const { tags } = useTicketStore()
  const [open, setOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const filteredTags = tags.filter((tag) =>
    tag.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const selectedTags = tags.filter((tag) => selectedTagIds.includes(tag.id))

  const toggleTag = (tagId: number) => {
    if (selectedTagIds.includes(tagId)) {
      onSelectionChange(selectedTagIds.filter((id) => id !== tagId))
    } else {
      onSelectionChange([...selectedTagIds, tagId])
    }
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between"
        >
          <div className="flex flex-wrap gap-1">
            {selectedTags.length > 0 ? (
              selectedTags.map((tag) => (
                <TagBadge key={tag.id} tag={tag} variant="outline" />
              ))
            ) : (
              <span className="text-muted-foreground">选择标签...</span>
            )}
          </div>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[300px] p-0" align="start">
        <div className="p-2">
          <Input
            placeholder="搜索标签..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="mb-2"
          />
          {onCreateTag && (
            <Button
              variant="ghost"
              size="sm"
              className="w-full justify-start"
              onClick={onCreateTag}
            >
              <Plus className="mr-2 h-4 w-4" />
              创建新标签
            </Button>
          )}
        </div>
        <ScrollArea className="h-[200px]">
          <div className="p-2 space-y-1">
            {filteredTags.length === 0 ? (
              <div className="text-sm text-muted-foreground text-center py-4">
                没有找到标签
              </div>
            ) : (
              filteredTags.map((tag) => (
                <div
                  key={tag.id}
                  className="flex items-center space-x-2 p-2 hover:bg-accent rounded-md cursor-pointer"
                  onClick={() => toggleTag(tag.id)}
                >
                  <Checkbox
                    checked={selectedTagIds.includes(tag.id)}
                    onCheckedChange={() => toggleTag(tag.id)}
                  />
                  <TagBadge tag={tag} variant="outline" />
                  {tag.ticket_count !== undefined && (
                    <span className="text-xs text-muted-foreground ml-auto">
                      {tag.ticket_count}
                    </span>
                  )}
                </div>
              ))
            )}
          </div>
        </ScrollArea>
      </PopoverContent>
    </Popover>
  )
}
