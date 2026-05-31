import { useState, useEffect, useCallback } from 'react'
import type { DailyData } from '../types'

const EMPTY_DATA: DailyData = {
  date: new Date().toISOString().slice(0, 10),
  generated_at: new Date().toISOString(),
  headlines: [],
  sections: [],
}

export function useDailyData() {
  const [data, setData] = useState<DailyData>(EMPTY_DATA)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true)
    else setLoading(true)

    try {
      const timestamp = Date.now()
      const resp = await fetch(`/data/daily.json?t=${timestamp}`)
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const json: DailyData = await resp.json()
      setData(json)
      setError(null)
    } catch (e) {
      // Try cache fallback
      try {
        const cache = await caches.open('daily-data')
        const cached = await cache.match('/data/daily.json')
        if (cached) {
          const json: DailyData = await cached.json()
          setData(json)
          setError('正在显示缓存数据 — 联网后自动更新')
        } else {
          setError('无法加载数据，请检查网络后重试')
        }
      } catch {
        setError('无法加载数据，请检查网络后重试')
      }
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }, [])

  useEffect(() => {
    let cancelled = false
    if (!cancelled) load()
    return () => { cancelled = true }
  }, [load])

  return { data, loading, refreshing, error, refresh: () => load(true) }
}
