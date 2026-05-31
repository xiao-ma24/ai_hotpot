import type { Section, NewsItem as INewsItem } from '../types'
import { NewsItem } from './NewsItem'

interface SectionCardProps {
  section: Section
  onItemClick: (item: INewsItem) => void
  showCount?: number
}

export function SectionCard({ section, onItemClick, showCount = 5 }: SectionCardProps) {
  if (!section.items.length) return null

  const visibleItems = section.items.slice(0, showCount)

  return (
    <div className="px-3 mb-5">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-base">{section.icon}</span>
        <h2 className="text-sm font-bold text-white">{section.title_cn}</h2>
        <span className="text-xs text-gray-500">{section.title_en}</span>
      </div>

      {visibleItems.map((item, i) => (
        <NewsItem key={i} item={item} onClick={onItemClick} />
      ))}

      {section.items.length > showCount && (
        <button className="w-full text-xs text-gray-500 py-2 text-center card">
          查看全部 {section.items.length} 条 →
        </button>
      )}
    </div>
  )
}
