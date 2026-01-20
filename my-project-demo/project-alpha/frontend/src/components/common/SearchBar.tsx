import { useState, useEffect } from 'react'
import { Input } from '@/components/ui/input'
import { Search } from 'lucide-react'
import { useTicketStore } from '@/store/useTicketStore'
import { cn } from '@/lib/utils'

interface SearchBarProps {
  placeholder?: string
  debounceMs?: number
}

export function SearchBar({ placeholder = '搜索 tickets...', debounceMs = 300 }: SearchBarProps) {
  const { searchQuery, setSearchQuery, fetchTickets } = useTicketStore()
  const [localQuery, setLocalQuery] = useState(searchQuery)
  const [isFocused, setIsFocused] = useState(false)

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
    <div className="relative w-full">
      <Search className={cn(
        "absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground transition-colors duration-200",
        isFocused && "text-foreground"
      )} />
      <Input
        type="text"
        placeholder={placeholder}
        value={localQuery}
        onChange={(e) => setLocalQuery(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        className={cn(
          "h-11 w-full rounded-full border-border/50 bg-muted/30 pl-11 pr-4 text-sm",
          "transition-all duration-200",
          "placeholder:text-muted-foreground/60",
          "focus:bg-background focus:border-border focus:shadow-md focus:ring-2 focus:ring-primary/20",
          "hover:bg-muted/50"
        )}
      />
    </div>
  )
}
