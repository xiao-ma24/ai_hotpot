interface HeatBadgeProps {
  heat: number
}

export function HeatBadge({ heat }: HeatBadgeProps) {
  const colorClass =
    heat >= 8 ? 'text-[#f59e0b] bg-[#f59e0b]/10' :
    heat >= 5 ? 'text-[#10b981] bg-[#10b981]/10' :
    'text-gray-500 bg-gray-500/10'

  return (
    <span className={`inline-flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded ${colorClass}`}>
      🔥 {heat.toFixed(1)}
    </span>
  )
}
