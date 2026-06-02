import { useState } from 'react'
import type { Section, NewsItem as INewsItem } from '../types'
import { NewsItem } from './NewsItem'
import { SECTION_COLORS } from '../types'

interface SectionCardProps {
  section: Section
  onItemClick: (item: INewsItem) => void
  showCount?: number
  readUrls?: Set<string>
}

export function SectionCard({ section, onItemClick, showCount = 5, readUrls }: SectionCardProps) {
  const [expanded, setExpanded] = useState(false)

  if (!section.items.length) {
    // Show graceful empty state
    return (
      <div className="px-3 mb-4">
        <div className="flex items-center gap-2 mb-2 opacity-40">
          <span className="text-base">{section.icon}</span>
          <h2 className="text-sm font-bold text-white">{section.title_cn}</h2>
        </div>
        <div className="card p-4 text-center text-[11px] text-gray-600">
          今日暂无{section.title_cn}资讯
        </div>
      </div>
    )
  }

  const color = SECTION_COLORS[section.id] || SECTION_COLORS.news
  const visibleItems = expanded ? section.items : section.items.slice(0, showCount)

  return (
    <div className="px-3 mb-4">
      {/* Section header with color bar */}
      <div className="flex items-center gap-2 mb-2.5">
        <span className="w-1 h-4 rounded-full shrink-0" style={{ backgroundColor: color }} />
        <span className="text-base">{section.icon}</span>
        <h2 className="text-[13px] font-bold text-white">{section.title_cn}</h2>
        <span className="text-[10px] text-gray-600">{section.title_en}</span>
        <span className="text-[10px] text-gray-700 ml-auto">{section.items.length}条</span>
      </div>

      {visibleItems.map((item, i) => (
        <NewsItem key={i} item={item} onClick={onItemClick} sectionId={section.id} isRead={readUrls?.has(item.url)} />
      ))}

      {section.items.length > showCount && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full text-[11px] text-gray-400 py-2.5 text-center card hover:text-white transition-colors"
        >
          {expanded
            ? `收起 — 仅显示前${showCount}条`
            : `查看全部 ${section.items.length} 条 →`}
        </button>
      )}
    </div>
  )
}
