import type { NewsItem as INewsItem } from '../types'
import { HeatBadge } from './HeatBadge'

interface NewsItemProps {
  item: INewsItem
  onClick: (item: INewsItem) => void
}

export function NewsItem({ item, onClick }: NewsItemProps) {
  return (
    <button
      onClick={() => onClick(item)}
      className="card p-3 w-full text-left block mb-2"
    >
      <div className="flex items-start gap-2">
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-white leading-snug line-clamp-2">
            {item.title_cn}
          </h4>
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">
            {item.title_en}
          </p>
        </div>
      </div>

      <p className="text-xs text-gray-400 mt-1.5 leading-relaxed line-clamp-2">
        {item.summary_cn}
      </p>

      <div className="flex items-center gap-2 mt-2 flex-wrap">
        <HeatBadge heat={item.heat} />
        <span className="text-[10px] text-gray-600">{item.source}</span>
        {item.meta && (
          <span className="text-[10px] text-gray-600">{item.meta}</span>
        )}
      </div>

      {item.tags.length > 0 && (
        <div className="flex gap-1 mt-1.5 flex-wrap">
          {item.tags.slice(0, 3).map(tag => (
            <span key={tag} className="text-[9px] px-1.5 py-0.5 rounded-full bg-[#2a2a3e] text-gray-400">
              {tag}
            </span>
          ))}
        </div>
      )}

      {item.student_note && (
        <div className="mt-1.5 text-[10px] text-[#10b981] bg-[#10b981]/5 rounded-md px-2 py-1">
          💡 {item.student_note}
        </div>
      )}
    </button>
  )
}
