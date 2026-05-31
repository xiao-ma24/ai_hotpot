import { Swiper, SwiperSlide } from 'swiper/react'
import { Autoplay, Pagination } from 'swiper/modules'
import type { NewsItem } from '../types'
import { HeatBadge } from './HeatBadge'

interface HeadlineCarouselProps {
  headlines: NewsItem[]
  onItemClick: (item: NewsItem) => void
}

export function HeadlineCarousel({ headlines, onItemClick }: HeadlineCarouselProps) {
  if (!headlines.length) return null

  return (
    <div className="px-3 py-4">
      <div className="text-xs font-bold text-[#f59e0b] uppercase tracking-wider mb-2">
        ⭐ 今日头条
      </div>
      <Swiper
        modules={[Autoplay, Pagination]}
        autoplay={{ delay: 5000, disableOnInteraction: false }}
        pagination={{ clickable: true, bulletClass: 'swiper-bullet', bulletActiveClass: 'swiper-bullet-active' }}
        spaceBetween={10}
        slidesPerView={1.05}
        centeredSlides={false}
        className="headline-swiper"
      >
        {headlines.map((item, i) => (
          <SwiperSlide key={i}>
            <button
              onClick={() => onItemClick(item)}
              className="card p-3 w-full text-left block border-l-[3px] border-l-[#f59e0b]"
            >
              <div className="flex items-center gap-2 mb-1">
                <HeatBadge heat={item.heat} />
                <span className="text-xs text-gray-500">{item.source}</span>
              </div>
              <h3 className="text-sm font-bold text-white leading-snug line-clamp-2">
                {item.title_cn}
              </h3>
              <p className="text-xs text-gray-400 mt-1.5 line-clamp-2 leading-relaxed">
                {item.summary_cn}
              </p>
              {item.student_note && (
                <div className="mt-2 text-xs text-[#10b981] bg-[#10b981]/10 rounded-md px-2 py-1">
                  💡 {item.student_note}
                </div>
              )}
            </button>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  )
}
