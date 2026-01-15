import { useState, useEffect } from 'react'
import { Input } from '@/components/ui/input'
import { Search } from 'lucide-react'
import { useTicketStore } from '@/store/useTicketStore'

interface SearchBarProps {
  placeholder?: string
  debounceMs?: number
}

export function SearchBar({ placeholder = '搜索 tickets...', debounceMs = 300 }: SearchBarProps) {
  const { searchQuery, setSearchQuery, fetchTickets } = useTicketStore()
  const [localQuery, setLocalQuery] = useState(searchQuery)

  useEffect(() => {
    const timer = setTimeout(() => {
      if (localQuery !== searchQuery) {
        setSearchQuery(localQuery)
        fetchTickets()
      }
    }, debounceMs)

    return () => clearTimeout(timer)
  }, [localQuery, debounceMs, searchQuery, setSearchQuery, fetchTickets])

  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <Input
        type="text"
        placeholder={placeholder}
        value={localQuery}
        onChange={(e) => setLocalQuery(e.target.value)}
        className="pl-10"
      />
    </div>
  )
}
