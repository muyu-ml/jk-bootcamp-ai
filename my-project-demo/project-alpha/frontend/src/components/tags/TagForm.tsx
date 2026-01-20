import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import type { Tag, TagCreate, TagUpdate } from '@/types/tag'

interface TagFormProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: TagCreate | TagUpdate) => Promise<void>
  tag?: Tag
}

export function TagForm({ open, onOpenChange, onSubmit, tag }: TagFormProps) {
  const [name, setName] = useState('')
  const [color, setColor] = useState('#3b82f6')
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (tag) {
      setName(tag.name)
      setColor(tag.color)
    } else {
      setName('')
      setColor('#3b82f6')
    }
  }, [tag, open])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return

    setIsSubmitting(true)
    try {
      if (tag) {
        await onSubmit({ name, color })
      } else {
        await onSubmit({ name, color })
      }
      onOpenChange(false)
    } catch (error) {
      console.error('Failed to submit tag:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{tag ? '编辑标签' : '创建标签'}</DialogTitle>
          <DialogDescription>
            {tag ? '更新标签信息' : '填写标签信息以创建新标签'}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="name">名称 *</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="输入标签名称"
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="color">颜色</Label>
              <div className="flex items-center gap-2">
                <Input
                  id="color"
                  type="color"
                  value={color}
                  onChange={(e) => setColor(e.target.value)}
                  className="h-10 w-20"
                />
                <Input
                  type="text"
                  value={color}
                  onChange={(e) => setColor(e.target.value)}
                  placeholder="#3b82f6"
                  pattern="^#[0-9A-Fa-f]{6}$"
                />
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              取消
            </Button>
            <Button type="submit" disabled={isSubmitting || !name.trim()}>
              {isSubmitting ? '提交中...' : tag ? '更新' : '创建'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
