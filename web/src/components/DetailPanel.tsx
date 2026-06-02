import { useEffect } from 'react'
import type { NewsItem } from '../types'
import { HeatBadge } from './HeatBadge'
import { SECTION_COLORS } from '../types'

interface DetailPanelProps {
  item: NewsItem | null
  onClose: () => void
  onOpenOriginal: (url: string) => void
}

export function DetailPanel({ item, onClose, onOpenOriginal }: DetailPanelProps) {
  // Lock body scroll when open
  useEffect(() => {
    if (item) {
      document.body.style.overflow = 'hidden'
      return () => { document.body.style.overflow = '' }
    }
  }, [item])

  if (!item) return null

  const sectionColor = SECTION_COLORS[item.source_icon] || SECTION_COLORS.news

  return (
    <div className="fixed inset-0 z-[60] flex flex-col bg-[#0a0a14]" role="dialog">
      {/* Header */}
      <div className="flex items-center gap-3 px-4 py-3 safe-top border-b border-[#1e1e3a]">
        <button
          onClick={onClose}
          className="tap-target flex items-center justify-center text-gray-400 hover:text-white transition-colors"
        >
          <span className="text-lg">←</span>
        </button>
        <div className="flex-1 min-w-0">
          <div className="text-[11px] text-gray-500">{item.source}</div>
        </div>
        <HeatBadge heat={item.heat} size="md" />
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        <div className="px-4 pt-5 pb-4">
          {/* Title */}
          <h1 className="text-[17px] font-bold text-white leading-[1.6]">
            {item.title_cn}
          </h1>
          {item.title_en && item.title_en !== item.title_cn && (
            <p className="text-[13px] text-gray-500 mt-1 leading-[1.5]">
              {item.title_en}
            </p>
          )}

          {/* Tags */}
          {item.tags.length > 0 && (
            <div className="flex gap-1.5 mt-3 flex-wrap">
              {item.tags.map(tag => (
                <span key={tag} className="text-[10px] px-2 py-0.5 rounded-md bg-[#1e1e3a] text-gray-400">
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Color bar separator */}
          <div className="mt-4 mb-4 h-0.5 w-12 rounded-full" style={{ backgroundColor: sectionColor }} />
        </div>

        {/* Detail Summary */}
        <div className="px-4 pb-4">
          {item.detail_summary ? (
            <>
              <h2 className="text-[13px] font-bold text-gray-300 mb-2">📖 深度摘要</h2>
              <p className="text-[14px] text-gray-300 leading-[1.85]">
                {item.detail_summary}
              </p>
            </>
          ) : (
            <p className="text-[14px] text-gray-300 leading-[1.85]">
              {item.summary_cn}
            </p>
          )}
        </div>

        {/* Key Points */}
        {item.key_points && item.key_points.length > 0 && (
          <div className="px-4 pb-4">
            <h2 className="text-[13px] font-bold text-gray-300 mb-2">📌 关键要点</h2>
            <div className="card p-3.5 space-y-2">
              {item.key_points.map((point, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-[#6366f1] text-xs mt-0.5 shrink-0">•</span>
                  <span className="text-[13px] text-gray-300 leading-[1.6]">{point}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Student Note */}
        {item.student_note && (
          <div className="px-4 pb-4">
            <div className="card p-3.5 bg-[#10b981]/5 border-[#10b981]/10">
              <div className="flex items-start gap-2">
                <span className="shrink-0">💡</span>
                <span className="text-[13px] text-[#10b981] leading-[1.6]">{item.student_note}</span>
              </div>
            </div>
          </div>
        )}

        {/* Original link */}
        <div className="px-4 pb-8">
          <button
            onClick={() => onOpenOriginal(item.url)}
            className="w-full card p-3.5 flex items-center justify-center gap-2 text-[14px] text-[#6366f1] font-medium hover:bg-[#6366f1]/5 transition-colors"
          >
            🔗 阅读原文 →
          </button>
        </div>
      </div>
    </div>
  )
}
