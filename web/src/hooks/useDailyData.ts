import { useState, useEffect } from 'react'
import type { DailyData } from '../types'

const SAMPLE_DATA: DailyData = {
  date: new Date().toISOString().slice(0, 10),
  generated_at: new Date().toISOString(),
  headlines: [],
  sections: [],
}

export function useDailyData() {
  const [data, setData] = useState<DailyData>(SAMPLE_DATA)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        const timestamp = Date.now()
        const resp = await fetch(`/data/daily.json?t=${timestamp}`)
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
        const json: DailyData = await resp.json()
        if (!cancelled) {
          setData(json)
          setError(null)
        }
      } catch (e) {
        if (!cancelled) {
          try {
            const cache = await caches.open('daily-data')
            const cached = await cache.match('/data/daily.json')
            if (cached) {
              const json: DailyData = await cached.json()
              setData(json)
              setError('Showing cached data — refresh when online')
            } else {
              setError('Unable to load daily data')
            }
          } catch {
            setError('Unable to load daily data')
          }
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    load()
    return () => { cancelled = true }
  }, [])

  return { data, loading, error }
}
