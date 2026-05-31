import { getRelativeTime } from '../types'

interface HeaderProps {
  date: string
  generatedAt?: string
}

export function Header({ date, generatedAt }: HeaderProps) {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const d = new Date(date)
  if (isNaN(d.getTime())) return null
  const weekday = weekdays[d.getDay()]
  const formatted = `${d.getMonth() + 1}月${d.getDate()}日`

  return (
    <header className="bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#5b2c8e] px-4 pt-2 pb-4 safe-top relative overflow-hidden">
      <div className="absolute -top-6 -right-6 w-24 h-24 rounded-full bg-white/[0.04]" />
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-3/4 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />

      <div className="relative flex items-center justify-between">
        <div>
          <div className="flex items-baseline gap-2">
            <h1 className="text-[19px] font-bold tracking-tight">🤖 AI 每日热点</h1>
            <span className="text-[10px] opacity-50">{formatted} · {weekday}</span>
          </div>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-[10px] opacity-45">AI Daily Hotpot</span>
            {generatedAt && (
              <span className="text-[10px] opacity-35">· {getRelativeTime(generatedAt)}</span>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
