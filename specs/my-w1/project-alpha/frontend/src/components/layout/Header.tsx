import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'
import { SearchBar } from '@/components/common/SearchBar'

interface HeaderProps {
  onNewTicket: () => void
}

export function Header({ onNewTicket }: HeaderProps) {
  return (
    <header className="sticky top-0 z-10 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold">Ticket 管理系统</h1>
        </div>
        <div className="flex flex-1 items-center gap-4 px-4">
          <div className="w-full max-w-md">
            <SearchBar />
          </div>
        </div>
        <Button onClick={onNewTicket}>
          <Plus className="mr-2 h-4 w-4" />
          新建 Ticket
        </Button>
      </div>
    </header>
  )
}
