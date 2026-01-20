import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { TagSelector } from '@/components/tags/TagSelector'
import type { Ticket, TicketCreate, TicketUpdate } from '@/types/ticket'

interface TicketFormProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: TicketCreate | TicketUpdate) => Promise<void>
  ticket?: Ticket
  onCreateTag?: () => void
}

export function TicketForm({ open, onOpenChange, onSubmit, ticket, onCreateTag }: TicketFormProps) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (ticket) {
      setTitle(ticket.title)
      setDescription(ticket.description || '')
      setSelectedTagIds(ticket.tags.map((tag) => tag.id))
    } else {
      setTitle('')
      setDescription('')
      setSelectedTagIds([])
    }
  }, [ticket, open])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return

    setIsSubmitting(true)
    try {
      await onSubmit({
        title,
        description: description || undefined,
        ...(ticket ? {} : { tag_ids: selectedTagIds }),
      })
      onOpenChange(false)
    } catch (error) {
      console.error('Failed to submit ticket:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>{ticket ? '编辑 Ticket' : '创建 Ticket'}</DialogTitle>
          <DialogDescription>
            {ticket ? '更新 ticket 信息' : '填写 ticket 信息以创建新的 ticket'}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="title">标题 *</Label>
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="输入 ticket 标题"
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">描述</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="输入 ticket 描述（可选）"
                rows={4}
              />
            </div>
            <div className="grid gap-2">
              <Label>标签</Label>
              <TagSelector
                selectedTagIds={selectedTagIds}
                onSelectionChange={setSelectedTagIds}
                onCreateTag={onCreateTag}
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              取消
            </Button>
            <Button type="submit" disabled={isSubmitting || !title.trim()}>
              {isSubmitting ? '提交中...' : ticket ? '更新' : '创建'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
