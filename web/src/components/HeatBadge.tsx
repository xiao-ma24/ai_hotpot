interface HeatBadgeProps {
  heat: number
  size?: 'sm' | 'md'
}

export function HeatBadge({ heat, size = 'sm' }: HeatBadgeProps) {
  const isHot = heat >= 8
  const isWarm = heat >= 5

  const sizeClass = size === 'md'
    ? 'text-[11px] px-2 py-0.5'
    : 'text-[10px] px-1.5 py-0.5'

  const colorClass = isHot
    ? 'text-[#f59e0b] bg-[#f59e0b]/12 border-[#f59e0b]/20'
    : isWarm
    ? 'text-[#10b981] bg-[#10b981]/10 border-[#10b981]/15'
    : 'text-gray-500 bg-gray-500/8 border-gray-500/10'

  return (
    <span className={`inline-flex items-center gap-1 font-bold rounded-md border ${sizeClass} ${colorClass}`}>
      <span className="text-[9px]">🔥</span>
      {heat.toFixed(1)}
    </span>
  )
}
