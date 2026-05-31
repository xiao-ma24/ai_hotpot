const TABS = [
  { id: 'all', label: '全部', icon: '🔥' },
  { id: 'github', label: 'GitHub', icon: '🐙' },
  { id: 'vendor', label: '厂商', icon: '🧠' },
  { id: 'people', label: '人物', icon: '👤' },
  { id: 'news', label: '新闻', icon: '📰' },
  { id: 'academic', label: '学术', icon: '📚' },
]

interface TabBarProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

export function TabBar({ activeTab, onTabChange }: TabBarProps) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[#0f0f1a]/95 backdrop-blur-lg border-t border-[#2a2a3e] safe-bottom z-50">
      <div className="flex justify-around items-center max-w-lg mx-auto">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex flex-col items-center py-1.5 px-2 tap-target transition-colors ${
              activeTab === tab.id
                ? 'text-[#6366f1]'
                : 'text-gray-500'
            }`}
          >
            <span className="text-lg">{tab.icon}</span>
            <span className="text-[9px] font-medium mt-0.5">{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}
