import { useState, useEffect } from 'react'
import { Header } from '@/components/layout/Header'
import { FilterSidebar } from '@/components/layout/FilterSidebar'
import { TicketList } from '@/components/tickets/TicketList'
import { TicketForm } from '@/components/tickets/TicketForm'
import { TagForm } from '@/components/tags/TagForm'
import { ConfirmDialog } from '@/components/common/ConfirmDialog'
import { Toaster } from '@/components/ui/toaster'
import { useToast } from '@/components/ui/use-toast'
import { useTicketStore } from '@/store/useTicketStore'
import type { Ticket, TicketCreate, TicketUpdate } from '@/types/ticket'
import type { TagCreate, TagUpdate } from '@/types/tag'

function App() {
  const { toast } = useToast()
  const {
    createTicket,
    updateTicket,
    deleteTicket,
    toggleComplete,
    createTag,
    updateTag,
    deleteTag,
    fetchTags,
  } = useTicketStore()

  const [ticketFormOpen, setTicketFormOpen] = useState(false)
  const [tagFormOpen, setTagFormOpen] = useState(false)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [selectedTicket, setSelectedTicket] = useState<Ticket | undefined>()
  const [selectedTag, setSelectedTag] = useState<any | undefined>()
  const [deleteTarget, setDeleteTarget] = useState<{ type: 'ticket' | 'tag'; id: number } | null>(null)

  useEffect(() => {
    fetchTags()
  }, [fetchTags])

  const handleNewTicket = () => {
    setSelectedTicket(undefined)
    setTicketFormOpen(true)
  }

  const handleEditTicket = (ticket: Ticket) => {
    setSelectedTicket(ticket)
    setTicketFormOpen(true)
  }

  const handleSubmitTicket = async (data: TicketCreate | TicketUpdate) => {
    try {
      if (selectedTicket) {
        await updateTicket(selectedTicket.id, data)
        toast({
          title: '成功',
          description: 'Ticket 已更新',
        })
      } else {
        await createTicket(data as TicketCreate)
        toast({
          title: '成功',
          description: 'Ticket 已创建',
        })
      }
      setTicketFormOpen(false)
      setSelectedTicket(undefined)
    } catch (error) {
      toast({
        title: '错误',
        description: error instanceof Error ? error.message : '操作失败',
        variant: 'destructive',
      })
      throw error
    }
  }

  const handleDeleteTicket = (ticketId: number) => {
    setDeleteTarget({ type: 'ticket', id: ticketId })
    setDeleteDialogOpen(true)
  }

  const handleToggleComplete = async (ticketId: number) => {
    try {
      await toggleComplete(ticketId)
      toast({
        title: '成功',
        description: 'Ticket 状态已更新',
      })
    } catch (error) {
      toast({
        title: '错误',
        description: error instanceof Error ? error.message : '操作失败',
        variant: 'destructive',
      })
    }
  }

  const handleConfirmDelete = async () => {
    if (!deleteTarget) return

    try {
      if (deleteTarget.type === 'ticket') {
        await deleteTicket(deleteTarget.id)
        toast({
          title: '成功',
          description: 'Ticket 已删除',
        })
      } else {
        await deleteTag(deleteTarget.id)
        toast({
          title: '成功',
          description: '标签已删除',
        })
      }
      setDeleteDialogOpen(false)
      setDeleteTarget(null)
    } catch (error) {
      toast({
        title: '错误',
        description: error instanceof Error ? error.message : '删除失败',
        variant: 'destructive',
      })
    }
  }

  const handleNewTag = () => {
    setSelectedTag(undefined)
    setTagFormOpen(true)
  }

  const handleSubmitTag = async (data: TagCreate | TagUpdate) => {
    try {
      if (selectedTag) {
        await updateTag(selectedTag.id, data)
        toast({
          title: '成功',
          description: '标签已更新',
        })
      } else {
        await createTag(data as TagCreate)
        toast({
          title: '成功',
          description: '标签已创建',
        })
      }
      setTagFormOpen(false)
      setSelectedTag(undefined)
    } catch (error) {
      toast({
        title: '错误',
        description: error instanceof Error ? error.message : '操作失败',
        variant: 'destructive',
      })
      throw error
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Header onNewTicket={handleNewTicket} />
      <div className="flex">
        <FilterSidebar />
        <main className="flex-1 p-8 lg:p-12">
          <div className="max-w-7xl mx-auto">
            <TicketList
              onEdit={handleEditTicket}
              onDelete={handleDeleteTicket}
              onToggleComplete={handleToggleComplete}
            />
          </div>
        </main>
      </div>

      <TicketForm
        open={ticketFormOpen}
        onOpenChange={setTicketFormOpen}
        onSubmit={handleSubmitTicket}
        ticket={selectedTicket}
        onCreateTag={handleNewTag}
      />

      <TagForm
        open={tagFormOpen}
        onOpenChange={setTagFormOpen}
        onSubmit={handleSubmitTag}
        tag={selectedTag}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        onConfirm={handleConfirmDelete}
        title={deleteTarget?.type === 'ticket' ? '删除 Ticket' : '删除标签'}
        description={
          deleteTarget?.type === 'ticket'
            ? '确定要删除这个 ticket 吗？此操作无法撤销。'
            : '确定要删除这个标签吗？此操作无法撤销。'
        }
        confirmText="删除"
        cancelText="取消"
        variant="destructive"
      />

      <Toaster />
    </div>
  )
}

export default App
