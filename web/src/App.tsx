import { useState, useCallback, useEffect, useRef } from 'react'
import { useDailyData } from './hooks/useDailyData'
import { Header } from './components/Header'
import { HeadlineCarousel } from './components/HeadlineCarousel'
import { SectionCard } from './components/SectionCard'
import { TabBar } from './components/TabBar'
import { DetailPanel } from './components/DetailPanel'
import { NewsItem } from './components/NewsItem'
import type { NewsItem as INewsItem } from './types'
import { SECTION_COLORS } from './types'

function SkeletonLoader() {
  return (
    <div className="px-3 pt-4 animate-pulse">
      <div className="skeleton h-3 w-16 rounded mb-3" />
      <div className="skeleton h-32 w-full rounded-[14px] mb-4" />
      {[1, 2, 3].map(i => (
        <div key={i} className="mb-4">
          <div className="skeleton h-3 w-24 rounded mb-2" />
          <div className="skeleton h-24 w-full rounded-[14px] mb-2" />
          <div className="skeleton h-24 w-full rounded-[14px]" />
        </div>
      ))}
    </div>
  )
}

export default function App() {
  const { data, loading, refreshing, error, refresh } = useDailyData()
  const [activeTab, setActiveTab] = useState('all')
  const [ptrY, setPtrY] = useState(0)
  const [ptrState, setPtrState] = useState<'idle' | 'pulling' | 'refreshing'>('idle')
  const [readUrls, setReadUrls] = useState<Set<string>>(new Set())
  const [showBackTop, setShowBackTop] = useState(false)
  const [detailItem, setDetailItem] = useState<INewsItem | null>(null)
  const contentRef = useRef<HTMLDivElement>(null)

  // Gather must_read URLs for quick lookup
  const mustReadUrls = new Set(data.must_read?.map(m => m.url) || [])

  // Track scroll position for back-to-top button
  useEffect(() => {
    const onScroll = () => setShowBackTop(window.scrollY > 400)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // Scroll to top when tab changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [activeTab])

  const handleItemClick = useCallback((item: INewsItem) => {
    if (!item.url) return
    setReadUrls(prev => new Set(prev).add(item.url))
    // Must-read items open detail panel instead of jumping out
    if (mustReadUrls.has(item.url)) {
      setDetailItem(item)
    } else {
      window.location.href = item.url
    }
  }, [mustReadUrls])

  const handleBackToTop = useCallback(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [])

  const handleRefresh = useCallback(async () => {
    setPtrState('refreshing')
    await refresh()
    setPtrState('idle')
    setPtrY(0)
  }, [refresh])

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    if (window.scrollY === 0) {
      setPtrY(e.touches[0].clientY)
    }
  }, [])

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (ptrY > 0 && ptrState !== 'refreshing') {
      const delta = e.touches[0].clientY - ptrY
      if (delta > 30) setPtrState('pulling')
      if (delta > 80) {
        setPtrState('refreshing')
        handleRefresh()
      }
    }
  }, [ptrY, ptrState, handleRefresh])

  const handleTouchEnd = useCallback(() => {
    if (ptrState === 'pulling') setPtrState('idle')
    setPtrY(0)
  }, [ptrState])

  const filteredSections =
    activeTab === 'all'
      ? data.sections
      : data.sections.filter(s => s.id === activeTab)

  const totalItems = data.sections.reduce((sum, s) => sum + s.items.length, 0)
  const sectionsWithContent = data.sections.filter(s => s.items.length > 0).length

  return (
    <div
      className="min-h-screen pb-20 max-w-lg mx-auto"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      ref={contentRef}
    >
      <Header date={data.date} generatedAt={data.generated_at} />

      {loading ? (
        <SkeletonLoader />
      ) : error && totalItems === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 px-4 text-gray-500">
          <div className="text-4xl mb-4">📡</div>
          <p className="text-sm text-center mb-1">{error}</p>
          <p className="text-[11px] text-gray-600 text-center mb-4">请检查网络连接后重试</p>
          <button
            onClick={() => refresh()}
            className="text-sm text-white bg-[#6366f1] px-5 py-2.5 rounded-xl font-medium tap-target"
          >
            重新加载
          </button>
        </div>
      ) : (
        <>
          {ptrState !== 'idle' && (
            <div className={`ptr-indicator ${ptrState}`}>
              {ptrState === 'refreshing' ? '更新中...' : '下拉刷新'}
            </div>
          )}

          {activeTab === 'all' && totalItems > 0 && (
            <div className="px-3 pt-1 pb-0.5">
              <div className="card px-4 py-2.5 flex items-center justify-between text-[11px]">
                <span className="text-gray-400">
                  今日收录 <span className="text-white font-bold">{totalItems}</span> 条资讯
                </span>
                <span className="text-gray-600">
                  {sectionsWithContent}/5 板块有更新
                </span>
              </div>
            </div>
          )}

          {activeTab === 'all' && data.headlines.length > 0 && (
            <HeadlineCarousel
              headlines={data.headlines}
              onItemClick={handleItemClick}
              readUrls={readUrls}
            />
          )}

          {/* Must-Read Section */}
          {activeTab === 'all' && data.must_read && data.must_read.length > 0 && (
            <div className="px-3 mb-4">
              <div className="flex items-center gap-2 mb-2.5">
                <span className="w-1 h-4 rounded-full shrink-0" style={{ backgroundColor: '#f59e0b' }} />
                <span className="text-base">⭐</span>
                <h2 className="text-[13px] font-bold text-white">必读精选</h2>
                <span className="text-[10px] text-gray-600">Must Read</span>
                <span className="text-[10px] text-gray-700 ml-auto">{data.must_read.length}篇</span>
              </div>
              {data.must_read.map((item, i) => (
                <NewsItem
                  key={i}
                  item={item}
                  onClick={handleItemClick}
                  isRead={readUrls.has(item.url)}
                  isMustRead
                />
              ))}
            </div>
          )}

          <div className={activeTab !== 'all' ? 'pt-3' : ''}>
            {filteredSections.map(section => (
              <SectionCard
                key={section.id}
                section={section}
                onItemClick={handleItemClick}
                showCount={activeTab === 'all' ? 5 : 15}
                readUrls={readUrls}
              />
            ))}
          </div>

          {filteredSections.length === 0 && activeTab !== 'all' && (
            <div className="text-center py-24 text-gray-500">
              <div className="text-2xl mb-3">📭</div>
              <p className="text-sm">该板块暂无今日资讯</p>
              <p className="text-[11px] text-gray-600 mt-1">换个板块看看吧</p>
            </div>
          )}

          <div className="text-center text-[10px] text-gray-700 py-6 px-4">
            AI 每日热点 · 由 DeepSeek 提供智能摘要 · {data.date}
          </div>
        </>
      )}

      {/* Back to top button */}
      {showBackTop && (
        <button
          onClick={handleBackToTop}
          className="back-to-top tap-target"
          aria-label="回到顶部"
        >
          ↑
        </button>
      )}

      <TabBar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Detail Panel for must-read articles */}
      <DetailPanel
        item={detailItem}
        onClose={() => setDetailItem(null)}
        onOpenOriginal={(url) => { window.location.href = url }}
      />
    </div>
  )
}
