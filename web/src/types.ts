export interface NewsItem {
  title_cn: string
  title_en: string
  summary_cn: string
  summary_en: string
  url: string
  source: string
  source_icon: string
  heat: number
  tags: string[]
  student_note?: string | null
  meta?: string
  published_at?: string
  detail_summary?: string
  key_points?: string[]
}

export interface Section {
  id: string
  title_cn: string
  title_en: string
  icon: string
  items: NewsItem[]
}

export interface DailyData {
  date: string
  generated_at: string
  headlines: NewsItem[]
  sections: Section[]
  must_read?: NewsItem[]
}

/** Section color mapping */
export const SECTION_COLORS: Record<string, string> = {
  github: '#f59e0b',
  vendor: '#6366f1',
  people: '#ec4899',
  news: '#10b981',
  academic: '#8b5cf6',
}

/** Get relative time string (e.g. "2小时前更新") */
export function getRelativeTime(isoString: string): string {
  const now = Date.now()
  const then = new Date(isoString).getTime()
  const diffMin = Math.floor((now - then) / 60000)
  if (diffMin < 1) return '刚刚更新'
  if (diffMin < 60) return `${diffMin}分钟前更新`
  const diffHr = Math.floor(diffMin / 60)
  if (diffHr < 24) return `${diffHr}小时前更新`
  return `${Math.floor(diffHr / 24)}天前更新`
}
