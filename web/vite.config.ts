import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: false,
      workbox: {
        globPatterns: ['**/*.{js,css,html,json,png,svg,ico}'],
        runtimeCaching: [
          {
            urlPattern: /\/data\/daily\.json$/,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'daily-data',
              expiration: { maxEntries: 7, maxAgeSeconds: 86400 },
            },
          },
        ],
      },
    }),
  ],
})
