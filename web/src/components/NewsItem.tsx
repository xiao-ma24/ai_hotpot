import type { NewsItem as INewsItem } from '../types'
import { HeatBadge } from './HeatBadge'
import { SECTION_COLORS } from '../types'

interface NewsItemProps {
  item: INewsItem
  onClick: (item: INewsItem) => void
  sectionId?: string
  isRead?: boolean
  isMustRead?: boolean
}

export function NewsItem({ item, onClick, sectionId, isRead, isMustRead }: NewsItemProps) {
  const borderColor = sectionId ? SECTION_COLORS[sectionId] : undefined

  return (
    <button
      onClick={() => onClick(item)}
      className={`card p-3.5 w-full text-left block mb-2.5 border-l-[3px] transition-all duration-200 ${
        isRead ? 'opacity-55' : ''
      }`}
      style={borderColor ? { borderLeftColor: borderColor } : undefined}
    >
      {/* Title row with badges */}
      <div className="flex items-start gap-2">
        {isMustRead && (
          <span className="shrink-0 text-xs mt-0.5">⭐</span>
        )}
        <h4 className={`text-[15px] font-semibold leading-[1.7] line-clamp-2 flex-1 ${
          isRead ? 'text-gray-500' : 'text-white'
        }`}>
          {item.title_cn}
        </h4>
        {isRead && (
          <span className="read-check mt-0.5">✓</span>
        )}
      </div>

      {item.title_en && item.title_en !== item.title_cn && (
        <p className="text-[12px] text-gray-600 mt-0.5 line-clamp-1 leading-[1.6]">
          {item.title_en}
        </p>
      )}

      {/* Summary */}
      {item.summary_cn && (
        <p className="text-[13px] article-summary mt-1.5 line-clamp-2">
          {item.summary_cn}
        </p>
      )}

      {/* Meta row */}
      <div className="flex items-center gap-2 mt-2.5 flex-wrap">
        <HeatBadge heat={item.heat} />
        <span className="text-[11px] text-gray-600">{item.source}</span>
        {item.meta && (
          <span className="text-[11px] text-gray-600 truncate">{item.meta}</span>
        )}
      </div>

      {/* Tags */}
      {item.tags.length > 0 && (
        <div className="flex gap-1.5 mt-2 flex-wrap">
          {item.tags.slice(0, 3).map(tag => (
            <span key={tag}
              className="text-[11px] px-2 py-1 rounded-md bg-[#1e1e3a] text-gray-400 border border-[#2a2a4a]"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Student note */}
      {item.student_note && (
        <div className="mt-2.5 text-[12px] text-[#10b981] bg-[#10b981]/5 rounded-lg px-2.5 py-1.5 flex items-start gap-1.5 border border-[#10b981]/10">
          <span className="shrink-0">💡</span>
          <span className="leading-[1.6]">{item.student_note}</span>
        </div>
      )}
    </button>
  )
}
