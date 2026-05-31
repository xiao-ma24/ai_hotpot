# 🤖 AI 每日热点 (AI Daily Hotpot)

> Your daily dose of global AI news — curated, summarized, bilingual.
> 每天早上 7:40，自动收集全球 AI 热点，生成中英双语简报。

手机打开即看 · Open on your phone → [ai-hotpot.vercel.app](https://ai-hotpot.vercel.app)

---

## 📋 内容板块 (Content Sections)

- 🐙 **GitHub AI 热门** — Trending AI repositories
- 🧠 **大模型厂商动态** — LLM vendor updates (OpenAI, Anthropic, DeepMind, Meta, DeepSeek, Qwen, etc.)
- 👤 **AI 科技人物** — Key figure news (Musk, Altman, Hassabis, LeCun, Karpathy, Sutskever)
- 📰 **AI 行业新闻** — Industry news (Hacker News, TechCrunch, The Verge, VentureBeat, 机器之心, 量子位)
- 📚 **学术前沿** — Academic frontier (ArXiv cs.AI/cs.CL/cs.CV, HuggingFace Daily Papers)

---

## 🛠️ 技术栈 (Tech Stack)

| Layer | Technology |
|-------|-----------|
| 采集 (Crawling) | Python: requests, feedparser, arxiv, BeautifulSoup |
| AI 处理 (Processing) | DeepSeek API (OpenAI-compatible) |
| 调度 (Scheduling) | GitHub Actions (daily 7:00 AM Beijing Time) |
| 前端 (Frontend) | React 18 + TypeScript + Vite + TailwindCSS |
| 托管 (Hosting) | Vercel (PWA with offline support) |

---

## 🚀 本地运行 (Local Development)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Set DeepSeek API key
export DEEPSEEK_API_KEY="sk-xxxx"

# 3. Run crawler (generates web/public/data/daily.json)
python crawler/fetch_all.py

# 4. Start frontend dev server
cd web && npm install && npm run dev
```

Open http://localhost:5173 on your phone or browser.

---

## 📄 License

MIT
