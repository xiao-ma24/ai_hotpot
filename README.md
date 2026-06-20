# 🍲 AI Daily Hotpot · AI 每日热点

> 每天清晨，自动采集全球 AI 热点，经 DeepSeek 总结成中英双语简报，推送到你手机上。

> A serverless daily AI news pipeline — crawl → summarize → deploy, fully automated with GitHub Actions.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/React-18-61DAFB.svg" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6.svg" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-5-646CFF.svg" alt="Vite">
  <img src="https://img.shields.io/badge/DeepSeek-API-4D6BFE.svg" alt="DeepSeek">
  <img src="https://img.shields.io/badge/Vercel-PWA-000.svg" alt="Vercel">
</p>

📱 手机打开即看 → **[ai-hotpot.vercel.app](https://ai-hotpot.vercel.app)**

---

## ✨ 这是什么

一个**无服务器、全自动**的 AI 每日简报系统：每天定时从 5 个数据源采集全球 AI 动态，用 DeepSeek 大模型做分类、打分、摘要与中英双语翻译，生成结构化 JSON 后由前端渲染，Vercel 自动构建发布为 PWA（可离线、可装到手机桌面）。

整条链路**零人工干预、零服务器成本**——GitHub Actions 跑采集与处理，Vercel 跑前端托管。

---

## 🔄 数据流

```
┌─────────────── 采集层 (Crawler) ───────────────┐
│  arxiv_papers · github_trending · hackernews_ai │
│            rss_feeds · tech_news               │
└───────────────────────┬─────────────────────────┘
                        ▼
┌─────────────── 处理层 (Processor) ─────────────┐
│  DeepSeek API: 分类 → 打分 → 摘要 → 中英双语    │
│  → must_read 精选 → headlines 头条              │
└───────────────────────┬─────────────────────────┘
                        ▼
            web/public/data/daily.json
                        ▼
┌─────────────── 调度与部署 ─────────────────────┐
│  GitHub Actions (cron) → commit daily.json     │
│  → Vercel Deploy Hook → 自动构建发布 PWA        │
└─────────────────────────────────────────────────┘
```

---

## 📋 内容板块

- 🐙 **GitHub AI 热门** — Trending AI repositories
- 🧠 **大模型厂商动态** — OpenAI / Anthropic / DeepMind / Meta / DeepSeek / Qwen 等
- 👤 **AI 科技人物** — Musk / Altman / Hassabis / LeCun / Karpathy / Sutskever
- 📰 **AI 行业新闻** — Hacker News / TechCrunch / The Verge / VentureBeat / 机器之心 / 量子位
- 📚 **学术前沿** — ArXiv cs.AI/cs.CL/cs.CV、HuggingFace Daily Papers

---

## 🛠️ 技术栈

| 层 | 技术 |
|---|---|
| 采集 (Crawling) | Python · requests · feedparser · arxiv · BeautifulSoup |
| AI 处理 (Processing) | DeepSeek API（OpenAI 兼容）：分类 / 打分 / 摘要 / 中英翻译 |
| 调度 (Scheduling) | GitHub Actions（cron 定时，触发 Vercel Deploy Hook） |
| 前端 (Frontend) | React 18 · TypeScript · Vite · TailwindCSS · Swiper |
| 部署 (Hosting) | Vercel · vite-plugin-pwa（离线支持、可安装到桌面） |

---

## 📁 项目结构

```
├── crawler/
│   ├── fetch_all.py          # 采集入口
│   ├── filter_rank.py        # 去重 / 排序
│   └── sources/              # 5 个数据源
│       ├── arxiv_papers.py
│       ├── github_trending.py
│       ├── hackernews_ai.py
│       ├── rss_feeds.py
│       └── tech_news.py
├── processor/
│   ├── api_client.py         # DeepSeek 调用封装
│   ├── classify_score.py     # 分类 + 热度打分
│   ├── summarize.py          # 摘要
│   ├── headlines.py          # 头条提取
│   ├── must_read.py          # 必读精选
│   ├── generate_json.py      # 生成 daily.json
│   └── prompts.py            # Prompt 模板
├── web/                      # React + TS + Vite 前端
│   ├── src/components/       # NewsItem / DetailPanel / HeatBadge ...
│   └── public/data/daily.json # 自动生成的数据
├── .github/workflows/daily-fetch.yml  # 定时采集 + 触发部署
└── vercel.json
```

---

## 🚀 本地运行

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 配置 DeepSeek API Key（绝不要写进代码或提交到 Git）
cp .env.example .env
# 在 .env 中填入 DEEPSEEK_API_KEY=sk-xxxx

# 3. 采集并处理（生成 web/public/data/daily.json）
python crawler/fetch_all.py

# 4. 启动前端
cd web && npm install && npm run dev
```

打开 http://localhost:5173

---

## ⏰ 自动化机制

GitHub Actions 按 cron 每日定时执行：采集 → DeepSeek 处理 → 提交 `daily.json` → 触发 Vercel Deploy Hook，前端自动重新构建发布。北京时间清晨完成更新，手机打开 PWA 即可看到当日简报。

---

## 📌 项目说明

个人独立开发的全栈项目，覆盖**采集 → AI 处理 → 自动化部署 → PWA 前端**完整链路。设计目标是用最低成本（零服务器）维持一个可持续运营的 AI 资讯产品。

📄 MIT License
