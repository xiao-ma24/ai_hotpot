import { useState, useCallback } from 'react'
import { useDailyData } from './hooks/useDailyData'
import { Header } from './components/Header'
import { HeadlineCarousel } from './components/HeadlineCarousel'
import { SectionCard } from './components/SectionCard'
import { TabBar } from './components/TabBar'
import type { NewsItem } from './types'

export default function App() {
  const { data, loading, error } = useDailyData()
  const [activeTab, setActiveTab] = useState('all')

  const handleItemClick = useCallback((item: NewsItem) => {
    if (item.url) {
      // Use location.href for better PWA standalone behavior on Android
      window.location.href = item.url
    }
  }, [])

  const filteredSections =
    activeTab === 'all'
      ? data.sections
      : data.sections.filter(s => s.id === activeTab)

  return (
    <div className="min-h-screen pb-20 max-w-lg mx-auto">
      <Header date={data.date} />

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-500">
          <div className="text-3xl mb-3 animate-pulse">🤖</div>
          <p className="text-sm">正在加载今日热点...</p>
        </div>
      ) : error && !data.sections.length ? (
        <div className="flex flex-col items-center justify-center py-20 px-4 text-gray-500">
          <div className="text-3xl mb-3">📡</div>
          <p className="text-sm text-center">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 text-sm text-[#6366f1] bg-[#6366f1]/10 px-4 py-2 rounded-lg tap-target"
          >
            点击重试
          </button>
        </div>
      ) : (
        <>
          {activeTab === 'all' && data.headlines.length > 0 && (
            <HeadlineCarousel
              headlines={data.headlines}
              onItemClick={handleItemClick}
            />
          )}

          {filteredSections.map(section => (
            <SectionCard
              key={section.id}
              section={section}
              onItemClick={handleItemClick}
              showCount={activeTab === 'all' ? 5 : 15}
            />
          ))}

          {filteredSections.length === 0 && activeTab !== 'all' && (
            <div className="text-center py-20 text-gray-500 text-sm">
              该板块暂无今日资讯
            </div>
          )}

          <div className="text-center text-[10px] text-gray-600 py-6">
            AI 每日热点 · {data.date} · 由 DeepSeek 提供摘要
          </div>
        </>
      )}

      <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  )
}
