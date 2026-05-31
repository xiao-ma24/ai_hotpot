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
}
