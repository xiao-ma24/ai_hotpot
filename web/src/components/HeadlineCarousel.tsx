import { Swiper, SwiperSlide } from 'swiper/react'
import { Autoplay, Pagination } from 'swiper/modules'
import type { NewsItem } from '../types'
import { HeatBadge } from './HeatBadge'
import { SECTION_COLORS } from '../types'

interface HeadlineCarouselProps {
  headlines: NewsItem[]
  onItemClick: (item: NewsItem) => void
}

export function HeadlineCarousel({ headlines, onItemClick }: HeadlineCarouselProps) {
  if (!headlines.length) return null

  return (
    <div className="px-3 pt-2 pb-1">
      <div className="flex items-center gap-2 mb-2">
        <span className="w-1 h-4 rounded-full bg-[#f59e0b]" />
        <span className="text-[11px] font-bold text-[#f59e0b] uppercase tracking-widest">
          今日头条
        </span>
        <span className="text-[10px] text-gray-600 ml-auto">
          共{headlines.length}条 · 自动轮播
        </span>
      </div>

      <Swiper
        modules={[Autoplay, Pagination]}
        autoplay={{ delay: 3500, disableOnInteraction: false }}
        pagination={{ clickable: true, bulletClass: 'swiper-bullet', bulletActiveClass: 'swiper-bullet-active' }}
        spaceBetween={10}
        slidesPerView={1.08}
        centeredSlides={false}
        className="headline-swiper"
      >
        {headlines.map((item, i) => {
          const sectionColor = SECTION_COLORS[item.source_icon] || SECTION_COLORS.news
          return (
            <SwiperSlide key={i} className="!h-auto">
              <button
                onClick={() => onItemClick(item)}
                className="card p-3.5 w-full text-left block border-l-[3px] relative overflow-hidden min-h-[170px] flex flex-col"
                style={{ borderLeftColor: sectionColor }}
              >
                <div className="absolute inset-0 opacity-[0.03]"
                  style={{ background: `linear-gradient(135deg, ${sectionColor}, transparent 70%)` }} />

                <div className="relative flex-1 flex flex-col">
                  <div className="flex items-center gap-2 mb-1.5">
                    <HeatBadge heat={item.heat} />
                    <span className="text-[10px] text-gray-500">{item.source}</span>
                    {item.meta && (
                      <span className="text-[10px] text-gray-600 truncate">{item.meta}</span>
                    )}
                  </div>
                  <h3 className="text-[15px] font-bold text-white leading-snug line-clamp-2">
                    {item.title_cn}
                  </h3>
                  <p className="text-[11px] text-gray-400 mt-1.5 leading-relaxed line-clamp-2 flex-1">
                    {item.summary_cn}
                  </p>
                  {item.student_note ? (
                    <div className="mt-2 text-[11px] text-[#10b981] bg-[#10b981]/8 rounded-lg px-2.5 py-1.5 flex items-start gap-1.5">
                      <span className="shrink-0">💡</span>
                      <span>{item.student_note}</span>
                    </div>
                  ) : (
                    <div className="mt-2 h-2" />
                  )}
                </div>
              </button>
            </SwiperSlide>
          )
        })}
      </Swiper>
    </div>
  )
}
