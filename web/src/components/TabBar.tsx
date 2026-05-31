import { SECTION_COLORS } from '../types'

const TABS = [
  { id: 'all', label: '全部', icon: '🔥', color: '#f59e0b' },
  { id: 'github', label: 'GitHub', icon: '🐙', color: SECTION_COLORS.github },
  { id: 'vendor', label: '厂商', icon: '🧠', color: SECTION_COLORS.vendor },
  { id: 'people', label: '人物', icon: '👤', color: SECTION_COLORS.people },
  { id: 'news', label: '新闻', icon: '📰', color: SECTION_COLORS.news },
  { id: 'academic', label: '学术', icon: '📚', color: SECTION_COLORS.academic },
]

interface TabBarProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

export function TabBar({ activeTab, onTabChange }: TabBarProps) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[#0a0a14]/95 backdrop-blur-xl border-t border-[#1e1e3a] safe-bottom z-50">
      <div className="flex justify-around items-center max-w-lg mx-auto">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex flex-col items-center py-1.5 px-1.5 tap-target transition-all duration-200 relative ${
              activeTab === tab.id
                ? 'text-white scale-105'
                : 'text-gray-600 hover:text-gray-400'
            }`}
          >
            {/* Active indicator dot */}
            {activeTab === tab.id && (
              <span
                className="absolute -top-0.5 w-5 h-0.5 rounded-full"
                style={{ backgroundColor: tab.color }}
              />
            )}
            <span className="text-base leading-none">{tab.icon}</span>
            <span className="text-[9px] font-medium mt-1 leading-none">{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}
