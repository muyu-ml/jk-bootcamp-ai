import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'
import { SearchBar } from '@/components/common/SearchBar'

interface HeaderProps {
  onNewTicket: () => void
}

export function Header({ onNewTicket }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-border/40 bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60 transition-all duration-300">
      <div className="container mx-auto flex h-20 items-center justify-between px-6 lg:px-8">
        <div className="flex items-center gap-6">
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">
            Tickets
          </h1>
        </div>
        <div className="flex flex-1 items-center justify-center gap-6 px-8">
          <div className="w-full max-w-lg">
            <SearchBar />
          </div>
        </div>
        <Button 
          onClick={onNewTicket}
          className="h-11 px-6 rounded-full font-medium shadow-sm hover:shadow-md transition-all duration-200 hover:scale-105 active:scale-95"
        >
          <Plus className="mr-2 h-4 w-4" />
          新建
        </Button>
      </div>
    </header>
  )
}
