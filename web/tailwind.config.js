/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#0f0f1a',
        card: '#1a1a2e',
        border: '#2a2a3e',
        accent: '#6366f1',
        heat: {
          high: '#f59e0b',
          mid: '#10b981',
          low: '#6b7280',
        },
      },
    },
  },
  plugins: [],
}
