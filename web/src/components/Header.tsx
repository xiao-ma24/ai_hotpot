interface HeaderProps {
  date: string
}

export function Header({ date }: HeaderProps) {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const d = new Date(date)
  const weekday = weekdays[d.getDay()]
  const formatted = `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`

  return (
    <header className="bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#5b2c8e] px-4 pt-3 pb-5 safe-top relative overflow-hidden">
      {/* Decorative background circles */}
      <div className="absolute -top-8 -right-8 w-32 h-32 rounded-full bg-white/5" />
      <div className="absolute -bottom-4 -left-4 w-20 h-20 rounded-full bg-white/5" />

      <div className="relative">
        <div className="text-xs opacity-75">{formatted} · {weekday}</div>
        <h1 className="text-xl font-bold mt-1 tracking-tight">🤖 AI 每日热点</h1>
        <div className="text-xs opacity-60 mt-0.5">AI Daily Hotpot</div>
      </div>
    </header>
  )
}
