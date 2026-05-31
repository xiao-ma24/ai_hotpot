# AI 每日热点 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建每天自动收集全球 AI 热点、DeepSeek API 生成双语简报、手机 PWA 查看的完整系统

**Architecture:** Python 采集层（10+ 数据源并行抓取 → 规则过滤）→ DeepSeek API 处理层（摘要/分类/评分/头条）→ 生成 daily.json → Vercel 托管 React PWA 前端 → 用户手机查看

**Tech Stack:** Python 3.11+, feedparser, requests, arxiv, openai (DeepSeek compatible); React 18 + TypeScript + Vite + Tailwind CSS + Swiper.js; GitHub Actions + Vercel

---

## File Map

```
ai-hotpot/
├── .github/workflows/daily-fetch.yml        # GitHub Actions 定时触发
├── .gitignore
├── requirements.txt                          # Python 依赖
├── README.md
├── crawler/
│   ├── fetch_all.py                          # 编排入口
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── github_trending.py                # GitHub Trending 采集
│   │   ├── rss_feeds.py                      # 统一 RSS 采集 (OpenAI/Anthropic/DeepMind/Meta/DeepSeek/Qwen)
│   │   ├── hackernews_ai.py                  # Hacker News AI 帖子
│   │   ├── arxiv_papers.py                   # ArXiv + HuggingFace 论文
│   │   └── tech_news.py                      # 行业新闻 (TC/VB/Verge/机器之心/量子位) + AI人物
│   └── filter_rank.py                        # 去重/过滤/预排序
├── processor/
│   ├── __init__.py
│   ├── prompts.py                            # DeepSeek Prompt 模板 (核心)
│   ├── summarize.py                          # 批量摘要生成
│   ├── classify_score.py                     # 分类校对 + 热度评分
│   ├── headlines.py                          # 头条筛选
│   └── generate_json.py                      # 生成 daily.json
└── web/
    ├── index.html
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── public/
    │   ├── manifest.json
    │   ├── sw.js
    │   └── icons/
    │       └── icon-192.png                  # PWA 图标 (占位)
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── types.ts
        ├── hooks/
        │   └── useDailyData.ts
        ├── components/
        │   ├── Header.tsx
        │   ├── HeadlineCarousel.tsx
        │   ├── SectionCard.tsx
        │   ├── NewsItem.tsx
        │   ├── TabBar.tsx
        │   └── HeatBadge.tsx
        └── styles/
            └── index.css
```

---

### Task 1: 项目初始化与基础配置

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `README.md`

- [ ] **Step 1: 创建 .gitignore**

```bash
cd D:/ai_hotpot && git init
```

Write `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Node
node_modules/
dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Superpowers
.superpowers/

# Env
.env
.env.local

# Data output (generated daily)
web/public/data/daily.json
```

- [ ] **Step 2: 创建 requirements.txt**

```txt
requests>=2.31.0
feedparser>=6.0.11
beautifulsoup4>=4.12.3
lxml>=5.1.0
arxiv>=2.1.3
openai>=1.30.0
```

- [ ] **Step 3: 创建 README.md**

```markdown
# 🤖 AI 每日热点 (AI Daily Hotpot)

每天早上 7:40，自动收集全球 AI 热点，生成中英双语简报。
手机打开即看 → [ai-hotpot.vercel.app](https://ai-hotpot.vercel.app)

## 板块
- 🐙 GitHub AI 热门项目
- 🧠 大模型厂商动态
- 👤 AI 科技人物
- 📰 AI 行业新闻
- 📚 学术前沿

## 技术栈
Python 采集 → DeepSeek API 处理 → GitHub Actions 调度 → Vercel 托管 PWA

## 本地运行
```bash
pip install -r requirements.txt
python crawler/fetch_all.py
```
```

- [ ] **Step 4: 创建目录结构**

```bash
mkdir -p D:/ai_hotpot/.github/workflows
mkdir -p D:/ai_hotpot/crawler/sources
mkdir -p D:/ai_hotpot/processor
mkdir -p D:/ai_hotpot/web/public/icons
mkdir -p D:/ai_hotpot/web/src/components
mkdir -p D:/ai_hotpot/web/src/hooks
mkdir -p D:/ai_hotpot/web/src/styles
touch D:/ai_hotpot/crawler/__init__.py
touch D:/ai_hotpot/crawler/sources/__init__.py
touch D:/ai_hotpot/processor/__init__.py
```

- [ ] **Step 5: 安装 Python 依赖**

```bash
cd D:/ai_hotpot && pip install -r requirements.txt
```

- [ ] **Step 6: Commit**

```bash
git add .gitignore requirements.txt README.md
git commit -m "chore: project initialization"
```

---

### Task 2: GitHub Actions 定时工作流

**Files:**
- Create: `.github/workflows/daily-fetch.yml`

- [ ] **Step 1: 创建 daily-fetch.yml**

```yaml
name: Daily AI Fetch

on:
  schedule:
    # UTC 23:00 = 北京时间 7:00
    - cron: '0 23 * * *'
  workflow_dispatch:  # 手动触发

jobs:
  fetch-and-build:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Fetch all sources
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: python crawler/fetch_all.py

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install frontend deps
        run: |
          cd web
          npm ci

      - name: Build frontend
        run: |
          cd web
          npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./web

      - name: Commit daily.json (backup)
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add web/public/data/daily.json
          git diff --staged --quiet || git commit -m "data: daily update $(date +%Y-%m-%d)"
          git push || true
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/daily-fetch.yml
git commit -m "feat: add GitHub Actions daily workflow"
```

---

### Task 3: 采集层 — GitHub Trending

**Files:**
- Create: `crawler/sources/github_trending.py`

- [ ] **Step 1: 编写 github_trending.py**

```python
"""GitHub Trending AI 项目采集。

使用非官方 API 获取 trending 数据，筛选 AI/ML 相关项目。
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# 非官方 GitHub Trending API (RSSHub 镜像)
TRENDING_URL = "https://gh-trending-api.herokuapp.com/repositories"
# 备用: RSSHub 路由
TRENDING_RSS_URL = "https://rsshub.app/github/trending/daily"


def fetch_github_trending(language: str = "") -> list[dict]:
    """抓取 GitHub Trending 日榜。

    Returns:
        list[dict]: 原始项目列表，字段: title, description, url, stars, language,
                    stars_today, forks
    """
    items = []
    seen = set()

    # 循环获取多页以便覆盖更多项目
    for lang in [language] if language else ["", "python", "javascript", "typescript"]:
        try:
            params = {"since": "daily", "spoken_language_code": ""}
            if lang:
                params["language"] = lang

            resp = requests.get(TRENDING_URL, params=params, timeout=15)
            resp.raise_for_status()
            repos = resp.json()

            for repo in repos:
                url = repo.get("url") or repo.get("html_url", "")
                if url in seen:
                    continue
                seen.add(url)

                description = repo.get("description") or ""
                # AI/ML 关键词匹配
                if not _is_ai_related(
                    repo.get("name", ""),
                    description,
                    repo.get("language") or lang,
                ):
                    continue

                items.append({
                    "title": repo.get("name", ""),
                    "description": description[:500],
                    "url": url,
                    "stars": repo.get("stars") or repo.get("stargazers_count", 0),
                    "language": repo.get("language") or lang,
                    "stars_today": repo.get("currentPeriodStars")
                                   or repo.get("stars_since", 0),
                    "forks": repo.get("forks", 0),
                    "source": "GitHub Trending",
                })

        except Exception as e:
            logger.warning(f"GitHub Trending fetch failed for lang={lang!r}: {e}")
            continue

    # 按今日 star 排序
    items.sort(key=lambda x: x.get("stars_today", 0), reverse=True)
    logger.info(f"GitHub: {len(items)} AI-related repos found")
    return items


def _is_ai_related(name: str, description: str, language: str) -> bool:
    """检查项目是否与 AI 相关。"""
    text = f"{name} {description} {language}".lower()
    keywords = [
        "ai", "ml", "llm", "gpt", "nlp", "cv", "agent",
        "transformer", "deep-learning", "machine-learning",
        "neural", "diffusion", "rag", "embedding", "langchain",
        "llama", "mistral", "chatgpt", "openai", "claude",
        "stable-diffusion", "whisper", "tts", "ocr",
        "deepseek", "qwen",
    ]
    return any(kw in text for kw in keywords)
```

- [ ] **Step 2: 自测采集逻辑**

```bash
cd D:/ai_hotpot && python -c "
from crawler.sources.github_trending import fetch_github_trending
items = fetch_github_trending()
print(f'Found {len(items)} repos')
for item in items[:5]:
    print(f'  {item[\"title\"]} ⭐{item[\"stars\"]} +{item[\"stars_today\"]}')
"
```

Expected: 输出 0-20 个 AI 相关 repo（取决于当日 trending）

- [ ] **Step 3: Commit**

```bash
git add crawler/sources/github_trending.py crawler/sources/__init__.py crawler/__init__.py
git commit -m "feat: add GitHub Trending crawler"
```

---

### Task 4: 采集层 — RSS 源（厂商博客）

**Files:**
- Create: `crawler/sources/rss_feeds.py`

- [ ] **Step 1: 编写 rss_feeds.py**

```python
"""RSS 源采集：大模型厂商博客。

统一采集 OpenAI、Anthropic、DeepMind、Meta AI、DeepSeek、Qwen 的 RSS/Atom。
"""

import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Optional

import feedparser
import requests

logger = logging.getLogger(__name__)

# RSS 源配置
RSS_SOURCES = [
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "icon": "openai",
    },
    {
        "name": "Anthropic Blog",
        "url": "https://www.anthropic.com/blog/rss.xml",
        "icon": "anthropic",
    },
    {
        "name": "Google DeepMind",
        "url": "https://blog.google/technology/ai/rss/",
        "icon": "deepmind",
    },
    {
        "name": "Meta AI Blog",
        "url": "https://ai.meta.com/blog/feed/",
        "icon": "meta",
    },
    {
        "name": "DeepSeek",
        "url": "https://api-docs.deepseek.com/news/rss.xml",
        "icon": "deepseek",
    },
    # 备用: 国产厂商通常没有 RSS，通过网页抓取或新闻 API 覆盖
]


def fetch_rss_feeds(sources: list[dict] | None = None) -> list[dict]:
    """抓取所有 RSS 源的最新文章。

    Args:
        sources: 自定义源列表，默认使用 RSS_SOURCES

    Returns:
        list[dict]: 文章列表，字段: title, description, url, source,
                    source_icon, published_at
    """
    if sources is None:
        sources = RSS_SOURCES

    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)

    for src in sources:
        try:
            feed = feedparser.parse(src["url"])
            if feed.bozo and not feed.entries:
                logger.warning(f"RSS parse warning for {src['name']}: {feed.bozo_exception}")
                continue

            for entry in feed.entries[:10]:  # 每个源最多取 10 条
                # 解析发布时间
                published = _parse_date(entry)
                if published and published < cutoff:
                    continue

                items.append({
                    "title": entry.get("title", "").strip(),
                    "description": _clean_html(entry.get("summary") or entry.get("description", "")),
                    "url": entry.get("link", ""),
                    "source": src["name"],
                    "source_icon": src["icon"],
                    "published_at": published.isoformat() if published else "",
                })

        except Exception as e:
            logger.warning(f"RSS fetch failed for {src['name']}: {e}")
            continue

    logger.info(f"RSS: {len(items)} articles from {len(sources)} sources")
    return items


def _parse_date(entry) -> Optional[datetime]:
    """从 feed entry 解析发布时间。"""
    for attr in ("published_parsed", "updated_parsed"):
        tp = getattr(entry, attr, None)
        if tp:
            try:
                from time import mktime
                return datetime.fromtimestamp(mktime(tp), tz=timezone.utc)
            except Exception:
                pass

    for attr in ("published", "updated"):
        raw = getattr(entry, attr, None)
        if raw:
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(raw)
            except Exception:
                pass

    return None


def _clean_html(text: str, max_len: int = 500) -> str:
    """去除 HTML 标签并截断。"""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    if len(clean) > max_len:
        clean = clean[:max_len] + "..."
    return clean
```

- [ ] **Step 2: 自测 RSS 采集**

```bash
cd D:/ai_hotpot && python -c "
from crawler.sources.rss_feeds import fetch_rss_feeds
items = fetch_rss_feeds()
print(f'Found {len(items)} articles')
for item in items[:5]:
    print(f'  [{item[\"source\"]}] {item[\"title\"][:60]}')
"
```

Expected: 输出 0-30 篇文章

- [ ] **Step 3: Commit**

```bash
git add crawler/sources/rss_feeds.py
git commit -m "feat: add RSS feeds crawler for vendor blogs"
```

---

### Task 5: 采集层 — Hacker News AI 帖子

**Files:**
- Create: `crawler/sources/hackernews_ai.py`

- [ ] **Step 1: 编写 hackernews_ai.py**

```python
"""Hacker News AI 相关热门帖子采集。

使用官方 Firebase API，筛选标题含 AI/ML/LLM/GPT 关键词且 points > 50 的帖子。
"""

import logging
import requests
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HN_NEW_STORIES = "https://hacker-news.firebaseio.com/v0/newstories.json"

AI_KEYWORDS = [
    "ai", "artificial intelligence", "llm", "gpt", "nlp", "cv",
    "transformer", "deep learning", "machine learning", "neural",
    "diffusion", "rag", "embedding", "langchain", "llama",
    "mistral", "chatgpt", "openai", "claude", "stable diffusion",
    "anthropic", "deepseek", "qwen", "gemini", "copilot",
    "fine-tun", "token", "inference", "gpu", "tpu",
    "reinforcement learning", "rlhf", "multimodal",
]


def fetch_hackernews_ai(min_points: int = 50, max_items: int = 100) -> list[dict]:
    """获取 Hacker News 上 AI 相关的高分帖子。

    Args:
        min_points: 最低分数阈值
        max_items: 最多检查的帖子数

    Returns:
        list[dict]: 帖子列表，字段: title, description, url, source,
                    source_icon, points, comments, published_at
    """
    try:
        resp = requests.get(HN_TOP_STORIES, timeout=10)
        resp.raise_for_status()
        story_ids = resp.json()[:max_items]
    except Exception as e:
        logger.error(f"Failed to fetch HN top stories: {e}")
        return []

    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)

    for sid in story_ids:
        try:
            resp = requests.get(HN_ITEM.format(sid), timeout=8)
            resp.raise_for_status()
            story = resp.json()

            if not story:
                continue

            title = story.get("title", "")
            points = story.get("score", 0)
            url = story.get("url") or f"https://news.ycombinator.com/item?id={sid}"

            # 关键词和分数筛选
            if not _is_ai_title(title.lower()):
                continue
            if points < min_points:
                continue

            pub_time = datetime.fromtimestamp(story.get("time", 0), tz=timezone.utc)
            if pub_time < cutoff:
                continue

            items.append({
                "title": title,
                "description": story.get("text", "")[:500] if story.get("text") else "",
                "url": url,
                "source": "Hacker News",
                "source_icon": "hackernews",
                "points": points,
                "comments": story.get("descendants", 0),
                "published_at": pub_time.isoformat(),
            })

        except Exception as e:
            logger.warning(f"Failed to fetch HN item {sid}: {e}")
            continue

    items.sort(key=lambda x: x.get("points", 0), reverse=True)
    logger.info(f"HN: {len(items)} AI-related posts with points > {min_points}")
    return items


def _is_ai_title(title: str) -> bool:
    """检查标题是否与 AI 相关。"""
    return any(kw in title for kw in AI_KEYWORDS)
```

- [ ] **Step 2: 自测 HN 采集**

```bash
cd D:/ai_hotpot && python -c "
from crawler.sources.hackernews_ai import fetch_hackernews_ai
items = fetch_hackernews_ai(min_points=30, max_items=80)
print(f'Found {len(items)} posts')
for item in items[:5]:
    print(f'  [{item[\"points\"]}pts] {item[\"title\"][:60]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add crawler/sources/hackernews_ai.py
git commit -m "feat: add Hacker News AI crawler"
```

---

### Task 6: 采集层 — ArXiv + HuggingFace 论文

**Files:**
- Create: `crawler/sources/arxiv_papers.py`

- [ ] **Step 1: 编写 arxiv_papers.py**

```python
"""学术前沿采集：ArXiv 论文 + HuggingFace Daily Papers。"""

import logging
import requests
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

ARXIV_CATEGORIES = ["cs.AI", "cs.CL", "cs.CV"]
HF_DAILY_PAPERS = "https://huggingface.co/api/daily_papers"


def fetch_arxiv_papers(max_results: int = 30) -> list[dict]:
    """抓取 ArXiv 最新 AI 相关论文。

    Returns:
        list[dict]: 论文列表，字段: title, description (abstract), url, source,
                    source_icon, authors, published_at
    """
    import arxiv

    items = []
    today = datetime.now(timezone.utc).date()

    for cat in ARXIV_CATEGORIES:
        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=f"cat:{cat}",
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
            )
            for result in client.results(search):
                pub_date = result.published.date()
                # 只取最近 2 天
                if (today - pub_date).days > 2:
                    continue

                items.append({
                    "title": result.title,
                    "description": result.summary[:500].replace("\n", " "),
                    "url": result.entry_id,
                    "source": f"ArXiv {cat}",
                    "source_icon": "arxiv",
                    "authors": [a.name for a in result.authors[:5]],
                    "published_at": result.published.isoformat(),
                })

        except Exception as e:
            logger.warning(f"ArXiv fetch failed for {cat}: {e}")
            continue

    logger.info(f"ArXiv: {len(items)} papers")
    return items


def fetch_huggingface_papers() -> list[dict]:
    """抓取 HuggingFace Daily Papers。

    Returns:
        list[dict]: 论文列表，字段: title, description, url, source,
                    source_icon, upvotes, published_at
    """
    try:
        resp = requests.get(HF_DAILY_PAPERS, timeout=15)
        resp.raise_for_status()
        papers = resp.json()
    except Exception as e:
        logger.warning(f"HuggingFace Daily Papers fetch failed: {e}")
        return []

    items = []
    for paper in papers[:20]:
        # paper 结构: {title, paper: {summary, id}, upvotes, ...}
        paper_data = paper.get("paper", {})
        items.append({
            "title": paper_data.get("title", paper.get("title", "")),
            "description": (paper_data.get("summary", "") or "")[:500],
            "url": f"https://huggingface.co/papers/{paper_data.get('id', '')}",
            "source": "HuggingFace Daily Papers",
            "source_icon": "huggingface",
            "upvotes": paper.get("upvotes", 0),
            "published_at": paper.get("publishedAt", ""),
        })

    logger.info(f"HuggingFace: {len(items)} papers")
    return items


def fetch_all_academic() -> list[dict]:
    """统一采集学术板块所有数据。"""
    results = []
    results.extend(fetch_arxiv_papers())
    results.extend(fetch_huggingface_papers())
    return results
```

- [ ] **Step 2: 自测学术采集**

```bash
cd D:/ai_hotpot && python -c "
from crawler.sources.arxiv_papers import fetch_all_academic
items = fetch_all_academic()
print(f'Found {len(items)} papers')
for item in items[:5]:
    print(f'  [{item[\"source\"]}] {item[\"title\"][:60]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add crawler/sources/arxiv_papers.py
git commit -m "feat: add ArXiv & HuggingFace papers crawler"
```

---

### Task 7: 采集层 — 行业新闻 + AI 人物

**Files:**
- Create: `crawler/sources/tech_news.py`

- [ ] **Step 1: 编写 tech_news.py**

```python
"""行业新闻 & AI 科技人物动态采集。

涵盖:
- 英文: TechCrunch AI, The Verge AI, VentureBeat AI
- 中文: 机器之心, 量子位
- 人物: Elon Musk, Sam Altman, Demis Hassabis, Yann LeCun, Andrej Karpathy 等
"""

import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Optional

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# === RSS 源 ===
NEWS_RSS = [
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "icon": "techcrunch",
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "icon": "verge",
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "icon": "venturebeat",
    },
    {
        "name": "机器之心",
        "url": "https://rsshub.app/jiqizhixin/latest",
        "icon": "jiqizhixin",
    },
    {
        "name": "量子位",
        "url": "https://rsshub.app/liangzhiwei/latest",
        "icon": "liangzhiwei",
    },
]

# === AI 人物新闻追踪 (通过 Google News RSS 间接获取) ===
AI_FIGURES = [
    {"name": "Elon Musk", "query": "Elon+Musk+xAI+AI", "icon": "musk"},
    {"name": "Sam Altman", "query": "Sam+Altman+OpenAI", "icon": "altman"},
    {"name": "Demis Hassabis", "query": "Demis+Hassabis+DeepMind", "icon": "hassabis"},
    {"name": "Yann LeCun", "query": "Yann+LeCun+AI", "icon": "lecun"},
    {"name": "Andrej Karpathy", "query": "Andrej+Karpathy+AI", "icon": "karpathy"},
    {"name": "Ilya Sutskever", "query": "Ilya+Sutskever+AI", "icon": "sutskever"},
]

AI_FIGURE_NEWS_URL = "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en"


def fetch_tech_news() -> list[dict]:
    """采集行业新闻 RSS。"""
    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)

    for src in NEWS_RSS:
        try:
            feed = feedparser.parse(src["url"])
            if feed.bozo and not feed.entries:
                logger.warning(f"News RSS parse warning for {src['name']}")
                continue

            for entry in feed.entries[:15]:
                pub_time = _parse_entry_date(entry)
                if pub_time and pub_time < cutoff:
                    continue

                items.append({
                    "title": entry.get("title", "").strip(),
                    "description": _clean_html_text(
                        entry.get("summary") or entry.get("description", "")
                    )[:500],
                    "url": entry.get("link", ""),
                    "source": src["name"],
                    "source_icon": src["icon"],
                    "published_at": pub_time.isoformat() if pub_time else "",
                })

        except Exception as e:
            logger.warning(f"News fetch failed for {src['name']}: {e}")
            continue

    logger.info(f"Tech news: {len(items)} articles")
    return items


def fetch_ai_figures_news() -> list[dict]:
    """通过 Google News RSS 采集 AI 科技人物相关新闻。"""
    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)

    for figure in AI_FIGURES:
        try:
            url = AI_FIGURE_NEWS_URL.format(figure["query"])
            feed = feedparser.parse(url)
            if not feed.entries:
                continue

            for entry in feed.entries[:8]:
                pub_time = _parse_entry_date(entry)
                if pub_time and pub_time < cutoff:
                    continue

                # 提取标题和来源
                title = entry.get("title", "")
                # Google News 标题格式: "title - source"
                if " - " in title:
                    news_title, news_source = title.rsplit(" - ", 1)
                else:
                    news_title, news_source = title, ""

                items.append({
                    "title": news_title.strip(),
                    "description": _clean_html_text(
                        entry.get("summary") or ""
                    )[:500],
                    "url": entry.get("link", ""),
                    "source": f"{figure['name']} · {news_source}" if news_source else figure["name"],
                    "source_icon": figure["icon"],
                    "published_at": pub_time.isoformat() if pub_time else "",
                    "figure": figure["name"],
                })

        except Exception as e:
            logger.warning(f"Figure news failed for {figure['name']}: {e}")
            continue

    logger.info(f"AI figures: {len(items)} news items")
    return items


def fetch_all_news() -> list[dict]:
    """统一采集新闻 + 人物板块。"""
    results = []
    results.extend(fetch_tech_news())
    results.extend(fetch_ai_figures_news())
    return results


def _parse_entry_date(entry) -> Optional[datetime]:
    """解析 RSS entry 的发布时间。"""
    for attr in ("published_parsed", "updated_parsed"):
        tp = getattr(entry, attr, None)
        if tp:
            try:
                from time import mktime
                return datetime.fromtimestamp(mktime(tp), tz=timezone.utc)
            except Exception:
                pass
    return None


def _clean_html_text(text: str) -> str:
    """去除 HTML 标签和多余空白。"""
    clean = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", clean).strip()
```

- [ ] **Step 2: 自测新闻采集**

```bash
cd D:/ai_hotpot && python -c "
from crawler.sources.tech_news import fetch_all_news
items = fetch_all_news()
print(f'Found {len(items)} news items')
for item in items[:5]:
    print(f'  [{item[\"source\"]}] {item[\"title\"][:60]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add crawler/sources/tech_news.py
git commit -m "feat: add tech news & AI figures crawler"
```

---

### Task 8: 采集层 — 过滤与预排序

**Files:**
- Create: `crawler/filter_rank.py`

- [ ] **Step 1: 编写 filter_rank.py**

```python
"""原始数据去重、规则过滤、预排序。

在 DeepSeek API 处理之前，先用规则大幅削减数据量 (200-500 → 50-100 条)。
"""

import re
import logging
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

# 板块分类关键词
SECTION_KEYWORDS = {
    "github": ["github", "repo", "repository", "star"],
    "vendor": ["openai", "anthropic", "deepmind", "meta", "deepseek",
               "qwen", "google", "kimi", "model", "api", "release",
               "发布", "模型", "降价", "价格"],
    "people": ["elon", "musk", "xai", "altman", "hassabis", "lecun",
               "karpathy", "sutskever", "马斯克", "奥特曼"],
    "news": ["techcrunch", "verge", "venturebeat", "机器之心", "量子位",
             "hacker news", "hn", "报道", "融资", "policy", "regulat"],
    "academic": ["arxiv", "huggingface", "paper", "论文", "research"],
}


def filter_and_rank(raw_items: list[dict]) -> list[dict]:
    """去重、过滤、预分类、预排序。

    Args:
        raw_items: 各数据源采集的原始条目

    Returns:
        list[dict]: 过滤后带 section 字段的条目列表
    """
    if not raw_items:
        return []

    # 1. 按 URL 去重
    seen_urls = set()
    deduped = []
    for item in raw_items:
        url = item.get("url", "").strip().lower()
        if not url:
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        deduped.append(item)

    logger.info(f"Dedup: {len(raw_items)} → {len(deduped)}")

    # 2. 相似标题去重
    unique = _dedup_by_title(deduped)

    # 3. 时间过滤（最近 48 小时）
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)
    recent = []
    for item in unique:
        pub_str = item.get("published_at", "")
        if pub_str:
            try:
                pub_time = datetime.fromisoformat(pub_str)
                if pub_time < cutoff:
                    continue
            except (ValueError, TypeError):
                pass
        recent.append(item)

    logger.info(f"Time filter: {len(unique)} → {len(recent)}")

    # 4. 预分类 (给 DeepSeek 提供初始分类参考)
    for item in recent:
        item["_section_hint"] = _guess_section(item)

    # 5. 预排序 (按热度/时间)
    recent.sort(key=_sort_key, reverse=True)

    # 6. 截断到 100 条 (DeepSeek token 限制)
    final = recent[:100]
    logger.info(f"Final filtered: {len(final)} items")

    return final


def _dedup_by_title(items: list[dict], threshold: float = 0.8) -> list[dict]:
    """基于标题相似度去重。"""
    keep = []
    keep_titles = []

    for item in items:
        title = item.get("title", "").lower().strip()
        if not title:
            keep.append(item)
            keep_titles.append(title)
            continue

        is_dup = False
        for existing in keep_titles[-20:]:  # 只比较最近 20 条
            if _title_similarity(title, existing) > threshold:
                is_dup = True
                break

        if not is_dup:
            keep.append(item)
            keep_titles.append(title)

    return keep


def _title_similarity(a: str, b: str) -> float:
    """标题相似度（归一化后比较）。"""
    def normalize(s):
        s = s.lower().strip()
        s = re.sub(r"[^a-z0-9一-鿿]", " ", s)
        return re.sub(r"\s+", " ", s).strip()

    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def _guess_section(item: dict) -> str:
    """根据来源和内容猜测所属板块。"""
    source = (item.get("source") or "").lower()
    title = (item.get("title") or "").lower()
    text = source + " " + title

    scores = {}
    for section, keywords in SECTION_KEYWORDS.items():
        scores[section] = sum(1 for kw in keywords if kw in text)

    if max(scores.values()) == 0:
        return "news"  # 默认归入新闻

    return max(scores, key=scores.get)


def _sort_key(item: dict) -> float:
    """综合排序键。"""
    score = 0.0

    # 时间越新分越高
    pub_str = item.get("published_at", "")
    if pub_str:
        try:
            pub_time = datetime.fromisoformat(pub_str)
            age_hours = (datetime.now(timezone.utc) - pub_time).total_seconds() / 3600
            score += max(0, 10 - age_hours)  # 最近 10 小时内满分
        except (ValueError, TypeError):
            pass

    # 有热度信息加分
    score += (item.get("points") or item.get("stars_today") or item.get("upvotes") or 0) / 100

    return score
```

- [ ] **Step 2: 自测过滤逻辑**

```bash
cd D:/ai_hotpot && python -c "
from crawler.filter_rank import filter_and_rank
# 构造测试数据
test_data = [
    {'title': 'GPT-5 released', 'url': 'http://a.com', 'source': 'OpenAI', 'published_at': '2026-05-31T00:00:00+00:00', 'points': 500},
    {'title': 'GPT-5 Released!!!', 'url': 'http://a.com', 'source': 'Other', 'published_at': '2026-05-31T00:00:00+00:00', 'points': 100},
    {'title': 'Old news', 'url': 'http://b.com', 'source': 'X', 'published_at': '2026-05-01T00:00:00+00:00'},
]
result = filter_and_rank(test_data)
print(f'Filtered: {len(result)} items')
for item in result:
    print(f'  [{item[\"_section_hint\"]}] {item[\"title\"]}')
"
```

- [ ] **Step 3: Commit**

```bash
git add crawler/filter_rank.py
git commit -m "feat: add filter, dedup, and pre-rank logic"
```

---

### Task 9: 采集层 — 编排入口

**Files:**
- Create: `crawler/fetch_all.py`

- [ ] **Step 1: 编写 fetch_all.py**

```python
"""每日采集编排入口。

被 GitHub Actions 调用，协调所有数据源的采集、过滤、AI 处理、JSON 生成。
"""

import json
import logging
import sys
import os
from pathlib import Path

# 确保项目根在 path 中
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crawler.sources.github_trending import fetch_github_trending
from crawler.sources.rss_feeds import fetch_rss_feeds
from crawler.sources.hackernews_ai import fetch_hackernews_ai
from crawler.sources.arxiv_papers import fetch_all_academic
from crawler.sources.tech_news import fetch_all_news
from crawler.filter_rank import filter_and_rank
from processor.summarize import batch_summarize
from processor.classify_score import classify_and_score
from processor.headlines import select_headlines
from processor.generate_json import generate_daily_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("fetch_all")


def main():
    logger.info("===== AI Daily Hotpot: Fetch Start =====")

    # Step 1: 并行采集 (串行调用，单个失败不影响整体)
    logger.info("--- Phase 1: Crawling ---")
    all_items = []

    crawlers = [
        ("GitHub Trending", fetch_github_trending),
        ("RSS Feeds", fetch_rss_feeds),
        ("Hacker News", lambda: fetch_hackernews_ai(min_points=50)),
        ("Academic", fetch_all_academic),
        ("News & Figures", fetch_all_news),
    ]

    for name, fn in crawlers:
        try:
            items = fn()
            logger.info(f"  {name}: {len(items)} items")
            all_items.extend(items)
        except Exception as e:
            logger.error(f"  {name}: FAILED - {e}")

    logger.info(f"Total raw items: {len(all_items)}")

    # Step 2: 过滤预排序
    logger.info("--- Phase 2: Filtering ---")
    filtered = filter_and_rank(all_items)
    logger.info(f"Filtered: {len(filtered)} items")

    if not filtered:
        logger.error("No items after filtering. Aborting.")
        # 尝试加载昨日数据兜底
        _fallback_to_yesterday()
        return

    # Step 3: DeepSeek 摘要
    logger.info("--- Phase 3: AI Summarization ---")
    summarized = batch_summarize(filtered)
    logger.info(f"Summarized: {len(summarized)} items")

    # Step 4: 分类评分
    logger.info("--- Phase 4: Classification & Scoring ---")
    classified = classify_and_score(summarized)

    # Step 5: 头条筛选
    logger.info("--- Phase 5: Headlines ---")
    headlines = select_headlines(classified)
    logger.info(f"Headlines: {len(headlines)} selected")

    # Step 6: 生成 JSON
    logger.info("--- Phase 6: Generate daily.json ---")
    daily_json = generate_daily_json(classified, headlines)

    # Step 7: 写入文件
    output_path = Path(__file__).resolve().parent.parent / "web" / "public" / "data" / "daily.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(daily_json, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Written to {output_path}")

    logger.info("===== AI Daily Hotpot: Fetch Complete =====")


def _fallback_to_yesterday():
    """如果今日采集完全失败，复制昨日数据。"""
    logger.warning("Using yesterday's data as fallback...")
    # 什么都不做 — 前端会显示缓存的上次数据


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add crawler/fetch_all.py
git commit -m "feat: add crawler orchestration entry point"
```

---

### Task 10: AI 处理层 — DeepSeek Prompt 模板（核心）

**Files:**
- Create: `processor/prompts.py`

- [ ] **Step 1: 编写 prompts.py**

```python
"""DeepSeek API Prompt 模板。

所有 AI 处理的核心——提示词质量直接决定简报质量。
"""

# === 系统角色 ===
SYSTEM_PROMPT = """你是一位资深 AI 科技编辑，服务于中国大学生读者。
你的任务是将全球 AI 资讯处理成中英双语深度简报。

核心原则：
1. **准确第一**：不要编造、不要过度解读，基于原文信息提炼
2. **学生友好**：提供学习建议，标注对大学生有帮助的内容
3. **双语自然**：中文摘要面向国内读者，英文摘要面向国际读者，两者独立撰写而非机械翻译
4. **热度客观**：基于实际影响力、讨论度、技术创新度综合评分，而非标题党
5. **格式严格**：必须按指定 JSON 格式输出，不要添加多余文字
"""

# === 批量摘要 Prompt ===
BATCH_SUMMARIZE_PROMPT = """请为以下 {count} 条 AI 资讯生成双语摘要。

## 输入数据
{items_json}

## 输出要求
对每条资讯返回一个 JSON 对象，字段含义：
- `title_cn`: 中文标题（简洁准确，15 字以内，不是原文翻译而是符合中文阅读习惯的标题）
- `title_en`: 英文标题（保留原始英文标题，如原文无英文标题则翻译）
- `summary_cn`: 中文摘要（2-3 句，说清核心内容，面向大学生读者，解释关键术语）
- `summary_en`: 英文摘要（2-3 sentences, clear and concise）
- `student_note`: 学习建议（可选，如果这条资讯对大学生特别有帮助，写 1 句简短的学习建议；否则为 null。例如"推荐阅读，了解 Transformer 架构的最新优化方向"）

## 返回格式
返回一个 JSON 数组，每条资讯对应一个对象：
```json
[
  {{
    "index": 0,
    "title_cn": "...",
    "title_en": "...",
    "summary_cn": "...",
    "summary_en": "...",
    "student_note": "..." or null
  }},
  ...
]
```
注意：
- index 必须与输入顺序一致
- 不要省略任何条目
- student_note 只在确实有帮助时填写，null 表示不需要
- 只返回 JSON 数组，不要有其他文字
"""

# === 分类 & 评分 Prompt ===
CLASSIFY_SCORE_PROMPT = """请为以下 {count} 条已摘要的 AI 资讯进行分类校对和热度评分。

## 输入数据
{items_json}

## 分类规则
每条资讯归入以下板块之一：
- `github`: GitHub 开源项目
- `vendor`: 大模型厂商动态（OpenAI/Anthropic/DeepMind/Meta/DeepSeek/Qwen 等）
- `people`: AI 科技人物（Elon Musk/Sam Altman/Demis Hassabis 等）
- `news`: 行业新闻（TechCrunch/The Verge/机器之心/量子位 等）
- `academic`: 学术前沿（ArXiv 论文/HuggingFace 论文）

## 热度评分 (1-10)
- 9-10 分：行业震动级（GPT-5 发布、万 star 项目、行业并购）
- 7-8 分：重要进展（大厂新功能、千 star 项目、核心人物发声）
- 5-6 分：值得关注（有趣新项目、行业分析、重要论文）
- 3-4 分：一般资讯（常规更新、普通新闻）
- 1-2 分：边角内容

## 标签
每条资讯打 2-4 个标签（中文），如：["模型发布","OpenAI","多模态"]

## 返回格式
```json
[
  {{
    "index": 0,
    "section": "vendor",
    "heat": 8.5,
    "tags": ["模型发布", "OpenAI"]
  }},
  ...
]
```
只返回 JSON 数组，不要有其他文字。
"""

# === 头条筛选 Prompt ===
HEADLINES_PROMPT = """从以下 {count} 条 AI 资讯中，选出 {n} 条作为今日头条。

## 输入数据
{items_json}

## 头条标准
1. 最重要：对 AI 行业有重大影响
2. 最有趣：大学生最想看的内容
3. 覆盖面：尽量覆盖不同板块
4. 新鲜度：优先当日/昨日新内容

## 返回格式
```json
{{
  "headlines": [3, 7, 12, ...]
}}
```
headlines 数组包含入选条目的 index（只返回 index 列表，不是完整对象）。
只返回 JSON 对象，不要有其他文字。
"""
```

- [ ] **Step 2: Commit**

```bash
git add processor/prompts.py processor/__init__.py
git commit -m "feat: add DeepSeek prompt templates"
```

---

### Task 11: AI 处理层 — 摘要生成

**Files:**
- Create: `processor/summarize.py`

- [ ] **Step 1: 编写 summarize.py**

```python
"""DeepSeek API 批量摘要生成。

将原始采集数据分批次发送给 DeepSeek，获取双语摘要。
"""

import json
import logging
import os
from openai import OpenAI

from processor.prompts import SYSTEM_PROMPT, BATCH_SUMMARIZE_PROMPT

logger = logging.getLogger(__name__)

# DeepSeek API 配置 (OpenAI 兼容接口)
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 每批处理条数（控制 token 消耗）
BATCH_SIZE = 15

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if not api_key:
            raise RuntimeError("DEEPSEEK_API_KEY environment variable not set")
        _client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
    return _client


def batch_summarize(items: list[dict]) -> list[dict]:
    """批量生成中英双语摘要。

    Args:
        items: 过滤后的原始条目列表

    Returns:
        list[dict]: 添加了 title_cn, title_en, summary_cn, summary_en,
                    student_note 字段的条目列表
    """
    if not items:
        return items

    client = _get_client()
    result = []

    for i in range(0, len(items), BATCH_SIZE):
        batch = items[i : i + BATCH_SIZE]
        logger.info(f"Summarizing batch {i // BATCH_SIZE + 1}: {len(batch)} items")

        # 构造输入（只传必要字段给 AI）
        input_data = []
        for idx, item in enumerate(batch):
            input_data.append({
                "index": idx,
                "title": item.get("title", ""),
                "description": item.get("description", "")[:300],
                "source": item.get("source", ""),
            })

        prompt = BATCH_SUMMARIZE_PROMPT.format(
            count=len(input_data),
            items_json=json.dumps(input_data, ensure_ascii=False, indent=2),
        )

        try:
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=4096,
            )

            content = response.choices[0].message.content or ""
            # 提取 JSON（处理可能的 markdown 包裹）
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            ai_results = json.loads(content.strip())

            # 合并回原始数据
            for ai_item in ai_results:
                idx = ai_item.get("index", -1)
                if 0 <= idx < len(batch):
                    batch[idx]["title_cn"] = ai_item.get("title_cn", batch[idx].get("title", ""))
                    batch[idx]["title_en"] = ai_item.get("title_en", batch[idx].get("title", ""))
                    batch[idx]["summary_cn"] = ai_item.get("summary_cn", "")
                    batch[idx]["summary_en"] = ai_item.get("summary_en", "")
                    batch[idx]["student_note"] = ai_item.get("student_note")

            logger.info(f"  Batch summarized: {len(ai_results)} responses")

        except json.JSONDecodeError as e:
            logger.error(f"  JSON parse error in batch: {e}")
            logger.debug(f"  Raw content: {content[:200]}")
            # 该批次保留原始数据，跳过 AI 处理
        except Exception as e:
            logger.error(f"  DeepSeek API error in batch: {e}")
            # 该批次保留原始数据，继续处理下一批

        result.extend(batch)

    return result
```

- [ ] **Step 2: 自测（需要设置 API key）**

```bash
cd D:/ai_hotpot && python -c "
# 注意：需要先设置 DEEPSEEK_API_KEY 环境变量
import os
if not os.environ.get('DEEPSEEK_API_KEY'):
    print('SKIP: Set DEEPSEEK_API_KEY to test')
    exit(0)

from processor.summarize import batch_summarize
test_items = [
    {'title': 'GPT-5 Released: A New Era of Multimodal AI',
     'description': 'OpenAI announced GPT-5 with breakthrough multimodal capabilities.',
     'source': 'OpenAI Blog'},
]
result = batch_summarize(test_items)
for item in result:
    print(f'CN: {item.get(\"title_cn\", \"N/A\")}')
    print(f'EN: {item.get(\"title_en\", \"N/A\")}')
    print(f'Summary CN: {item.get(\"summary_cn\", \"N/A\")}')
"
```

- [ ] **Step 3: Commit**

```bash
git add processor/summarize.py
git commit -m "feat: add DeepSeek batch summarization"
```

---

### Task 12: AI 处理层 — 分类评分 + 头条筛选

**Files:**
- Create: `processor/classify_score.py`
- Create: `processor/headlines.py`

- [ ] **Step 1: 编写 classify_score.py**

```python
"""DeepSeek API 分类校对与热度评分。"""

import json
import logging
from openai import OpenAI
import os

from processor.prompts import SYSTEM_PROMPT, CLASSIFY_SCORE_PROMPT

logger = logging.getLogger(__name__)

BATCH_SIZE = 20
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"


def classify_and_score(items: list[dict]) -> list[dict]:
    """为每条资讯分类 + 热度评分 + 打标签。

    Args:
        items: 已有摘要的条目列表

    Returns:
        list[dict]: 添加了 section, heat, tags 字段的条目列表
    """
    if not items:
        return items

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        logger.error("DEEPSEEK_API_KEY not set")
        return items

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    for i in range(0, len(items), BATCH_SIZE):
        batch = items[i : i + BATCH_SIZE]
        logger.info(f"Classifying batch {i // BATCH_SIZE + 1}: {len(batch)} items")

        input_data = []
        for idx, item in enumerate(batch):
            input_data.append({
                "index": idx,
                "title_cn": item.get("title_cn", item.get("title", "")),
                "summary_cn": item.get("summary_cn", ""),
                "source": item.get("source", ""),
                "source_icon": item.get("source_icon", ""),
                "_section_hint": item.get("_section_hint", "news"),
            })

        prompt = CLASSIFY_SCORE_PROMPT.format(
            count=len(input_data),
            items_json=json.dumps(input_data, ensure_ascii=False, indent=2),
        )

        try:
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2048,
            )

            content = response.choices[0].message.content or ""
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            ai_results = json.loads(content.strip())

            for ai_item in ai_results:
                idx = ai_item.get("index", -1)
                if 0 <= idx < len(batch):
                    batch[idx]["section"] = ai_item.get("section", batch[idx].get("_section_hint", "news"))
                    batch[idx]["heat"] = float(ai_item.get("heat", 5.0))
                    batch[idx]["tags"] = ai_item.get("tags", [])

            # 清理内部字段
            for item in batch:
                item.pop("_section_hint", None)

        except Exception as e:
            logger.error(f"  Classification error: {e}")
            # 该批次保留默认分类
            for item in batch:
                item.pop("_section_hint", None)

    return items
```

- [ ] **Step 2: 编写 headlines.py**

```python
"""头条筛选。

在所有板块处理完毕后，选出 3-5 条今日头条。
"""

import json
import logging
import os
from openai import OpenAI

from processor.prompts import SYSTEM_PROMPT, HEADLINES_PROMPT

logger = logging.getLogger(__name__)

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"
HEADLINE_COUNT = 5


def select_headlines(items: list[dict], n: int = HEADLINE_COUNT) -> list[dict]:
    """从所有已处理条目中选出头条。

    Args:
        items: 已分类评分的条目列表
        n: 头条数量

    Returns:
        list[dict]: 头条条目（带索引）
    """
    if not items:
        return []

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        logger.error("DEEPSEEK_API_KEY not set")
        # 兜底：取热度最高的 n 条
        sorted_items = sorted(items, key=lambda x: x.get("heat", 0), reverse=True)
        return sorted_items[:n]

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    input_data = []
    for idx, item in enumerate(items):
        input_data.append({
            "index": idx,
            "title_cn": item.get("title_cn", item.get("title", "")),
            "summary_cn": item.get("summary_cn", ""),
            "heat": item.get("heat", 5.0),
            "section": item.get("section", "news"),
            "source": item.get("source", ""),
        })

    prompt = HEADLINES_PROMPT.format(
        count=len(input_data),
        n=n,
        items_json=json.dumps(input_data, ensure_ascii=False, indent=2),
    )

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=512,
        )

        content = response.choices[0].message.content or ""
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        result = json.loads(content.strip())
        indices = result.get("headlines", [])

        headlines = []
        for idx in indices:
            if 0 <= idx < len(items):
                headlines.append(items[idx])

        logger.info(f"Headlines selected: {len(headlines)}")
        return headlines

    except Exception as e:
        logger.error(f"Headline selection error: {e}")
        # 兜底
        sorted_items = sorted(items, key=lambda x: x.get("heat", 0), reverse=True)
        return sorted_items[:n]
```

- [ ] **Step 3: Commit**

```bash
git add processor/classify_score.py processor/headlines.py
git commit -m "feat: add classification, scoring, and headline selection"
```

---

### Task 13: AI 处理层 — JSON 生成

**Files:**
- Create: `processor/generate_json.py`

- [ ] **Step 1: 编写 generate_json.py**

```python
"""生成最终的 daily.json 文件。"""

from datetime import datetime, timezone, timedelta


def generate_daily_json(items: list[dict], headlines: list[dict]) -> dict:
    """将处理完的条目组织成 daily.json 结构。

    Args:
        items: 已处理的所有条目（带 title_cn, summary_cn, heat, section 等）
        headlines: 头条条目

    Returns:
        dict: daily.json 完整结构
    """
    # 北京时间
    beijing_tz = timezone(timedelta(hours=8))
    now_beijing = datetime.now(beijing_tz)

    # 板块配置
    section_config = {
        "github": {
            "title_cn": "GitHub AI 热门",
            "title_en": "GitHub AI Trending",
            "icon": "🐙",
        },
        "vendor": {
            "title_cn": "大模型厂商动态",
            "title_en": "LLM Vendors Updates",
            "icon": "🧠",
        },
        "people": {
            "title_cn": "AI 科技人物",
            "title_en": "AI Key Figures",
            "icon": "👤",
        },
        "news": {
            "title_cn": "AI 行业新闻",
            "title_en": "AI Industry News",
            "icon": "📰",
        },
        "academic": {
            "title_cn": "学术前沿",
            "title_en": "Academic Frontier",
            "icon": "📚",
        },
    }

    # 构建 sections
    sections_map = {}
    for item in items:
        section_id = item.get("section", "news")
        if section_id not in sections_map:
            sections_map[section_id] = []
        sections_map[section_id].append(_to_output_item(item))

    # 每个板块按热度排序，取前 15 条
    sections = []
    for sec_id in ["github", "vendor", "people", "news", "academic"]:
        sec_items = sections_map.get(sec_id, [])
        sec_items.sort(key=lambda x: x.get("heat", 0), reverse=True)
        sec_items = sec_items[:15]

        config = section_config.get(sec_id, section_config["news"])
        sections.append({
            "id": sec_id,
            "title_cn": config["title_cn"],
            "title_en": config["title_en"],
            "icon": config["icon"],
            "items": sec_items,
        })

    # 构建头条
    headline_items = [_to_output_item(h, is_headline=True) for h in headlines]

    return {
        "date": now_beijing.strftime("%Y-%m-%d"),
        "generated_at": now_beijing.isoformat(),
        "headlines": headline_items,
        "sections": sections,
    }


def _to_output_item(item: dict, is_headline: bool = False) -> dict:
    """将内部条目转为 daily.json 中的标准条目格式。"""
    out = {
        "title_cn": item.get("title_cn", item.get("title", "")),
        "title_en": item.get("title_en", item.get("title", "")),
        "summary_cn": item.get("summary_cn", item.get("description", "")),
        "summary_en": item.get("summary_en", item.get("description", "")),
        "url": item.get("url", ""),
        "source": item.get("source", ""),
        "source_icon": item.get("source_icon", "link"),
        "heat": item.get("heat", 5.0),
        "tags": item.get("tags", []),
        "student_note": item.get("student_note"),
        "published_at": item.get("published_at", ""),
    }

    # 附加元数据（不同来源有不同元数据）
    meta_parts = []
    if item.get("stars"):
        meta_parts.append(f"⭐ {_format_number(item['stars'])}")
    if item.get("language"):
        meta_parts.append(item["language"])
    if item.get("stars_today"):
        meta_parts.append(f"+{_format_number(item['stars_today'])} today")
    if item.get("points"):
        meta_parts.append(f"▲ {item['points']}")
    if item.get("comments"):
        meta_parts.append(f"💬 {item['comments']}")
    if item.get("upvotes"):
        meta_parts.append(f"👍 {item['upvotes']}")
    if item.get("authors"):
        meta_parts.append(", ".join(item["authors"][:3]))

    if meta_parts:
        out["meta"] = " · ".join(meta_parts)

    return out


def _format_number(n: int) -> str:
    """格式化数字（1.2k, 3.4M 等）。"""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)
```

- [ ] **Step 2: 自测 JSON 生成**

```bash
cd D:/ai_hotpot && python -c "
import json
from processor.generate_json import generate_daily_json

test_items = [
    {
        'title': 'GPT-5 Released',
        'title_cn': 'OpenAI 发布 GPT-5',
        'title_en': 'OpenAI Releases GPT-5',
        'summary_cn': 'OpenAI 发布了 GPT-5 预览版...',
        'summary_en': 'OpenAI released GPT-5 preview...',
        'url': 'https://openai.com/blog/gpt-5',
        'source': 'OpenAI Blog',
        'source_icon': 'openai',
        'heat': 9.8,
        'tags': ['模型发布', 'OpenAI'],
        'student_note': '推荐了解多模态架构',
        'section': 'vendor',
        'published_at': '2026-05-31T00:00:00+00:00',
    },
    {
        'title': 'mini-deepseek',
        'title_cn': '在手机本地运行 DeepSeek',
        'title_en': 'Run DeepSeek Locally on Mobile',
        'summary_cn': '该项目实现了手机端本地运行...',
        'summary_en': 'This project implements...',
        'url': 'https://github.com/x/mini-deepseek',
        'source': 'GitHub Trending',
        'source_icon': 'github',
        'heat': 8.5,
        'tags': ['开源', '移动端'],
        'student_note': '了解模型量化',
        'section': 'github',
        'published_at': '2026-05-31T00:00:00+00:00',
        'stars': 12300,
        'language': 'Python',
        'stars_today': 2100,
    },
]

headlines = [test_items[0]]
result = generate_daily_json(test_items, headlines)
print(json.dumps(result, ensure_ascii=False, indent=2))
"
```

- [ ] **Step 3: Commit**

```bash
git add processor/generate_json.py
git commit -m "feat: add daily.json generation"
```

---

### Task 14: 前端 — Vite + React + Tailwind 脚手架

**Files:**
- Create: `web/package.json`
- Create: `web/index.html`
- Create: `web/vite.config.ts`
- Create: `web/tailwind.config.js`
- Create: `web/postcss.config.js`
- Create: `web/tsconfig.json`
- Create: `web/src/main.tsx`
- Create: `web/src/types.ts`
- Create: `web/src/styles/index.css`

- [ ] **Step 1: 创建 package.json**

```bash
cd D:/ai_hotpot/web
```

Write `web/package.json`:

```json
{
  "name": "ai-daily-hotpot",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "swiper": "^11.1.4"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "typescript": "^5.5.2",
    "vite": "^5.3.1",
    "vite-plugin-pwa": "^0.20.0"
  }
}
```

- [ ] **Step 2: 创建配置文件**

Write `web/index.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <meta name="theme-color" content="#0f0f1a" />
    <meta name="description" content="AI 每日热点 - 全球 AI 资讯中英双语简报" />
    <link rel="manifest" href="/manifest.json" />
    <link rel="icon" href="/icons/icon-192.png" />
    <title>🤖 AI 每日热点</title>
  </head>
  <body class="bg-[#0f0f1a] text-white">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Write `web/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: false, // 使用 public/manifest.json
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
```

Write `web/tailwind.config.js`:

```javascript
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
```

Write `web/postcss.config.js`:

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

Write `web/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
```

- [ ] **Step 3: 创建 types.ts**

Write `web/src/types.ts`:

```typescript
export interface NewsItem {
  title_cn: string
  title_en: string
  summary_cn: string
  summary_en: string
  url: string
  source: string
  source_icon: string
  heat: number
  tags: string[]
  student_note?: string | null
  meta?: string
  published_at?: string
}

export interface Section {
  id: string
  title_cn: string
  title_en: string
  icon: string
  items: NewsItem[]
}

export interface DailyData {
  date: string
  generated_at: string
  headlines: NewsItem[]
  sections: Section[]
}
```

- [ ] **Step 4: 创建样式入口**

Write `web/src/styles/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import 'swiper/css';

@layer base {
  html {
    -webkit-tap-highlight-color: transparent;
    -webkit-font-smoothing: antialiased;
  }

  body {
    @apply bg-[#0f0f1a] text-white overscroll-none;
  }
}

@layer components {
  .card {
    @apply bg-[#1a1a2e] rounded-xl border border-[#2a2a3e] transition-colors;
  }

  .card:active {
    @apply border-[#3a3a5e] bg-[#222240];
  }

  .tap-target {
    @apply min-h-[44px] min-w-[44px];
  }
}

/* Swiper 轮播样式 */
.headline-swiper {
  padding-bottom: 20px !important;
}

.swiper-bullet {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #3a3a5e;
  margin: 0 3px;
  transition: all 0.2s;
}

.swiper-bullet-active {
  background: #f59e0b;
  width: 16px;
  border-radius: 3px;
}

/* 移动端安全区域 */
.safe-top {
  padding-top: max(12px, env(safe-area-inset-top));
}

.safe-bottom {
  padding-bottom: max(4px, env(safe-area-inset-bottom));
}
```

- [ ] **Step 5: 安装依赖**

```bash
cd D:/ai_hotpot/web && npm install
```

- [ ] **Step 6: Commit**

```bash
git add web/package.json web/package-lock.json web/index.html web/vite.config.ts web/tailwind.config.js web/postcss.config.js web/tsconfig.json web/src/types.ts web/src/styles/index.css web/src/main.tsx
git commit -m "feat: scaffold Vite + React + Tailwind frontend"
```

---

### Task 15: 前端 — 数据加载 Hook

**Files:**
- Create: `web/src/hooks/useDailyData.ts`

- [ ] **Step 1: 编写 useDailyData.ts**

```typescript
import { useState, useEffect } from 'react'
import type { DailyData } from '../types'

/** 当天 sample 数据，用于开发和兜底 */
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
        // 尝试加载今日数据，带 cache-busting
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
          // 尝试从缓存加载
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
```

- [ ] **Step 2: Commit**

```bash
git add web/src/hooks/useDailyData.ts
git commit -m "feat: add daily data loading hook with cache fallback"
```

---

### Task 16: 前端 — Header + HeadlineCarousel

**Files:**
- Create: `web/src/components/Header.tsx`
- Create: `web/src/components/HeadlineCarousel.tsx`

- [ ] **Step 1: 编写 Header.tsx**

```typescript
interface HeaderProps {
  date: string
}

export function Header({ date }: HeaderProps) {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const d = new Date(date)
  const weekday = weekdays[d.getDay()]
  const formatted = `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`

  return (
    <header className="bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#5b2c8e] px-4 pt-3 pb-5 safe-top">
      <div className="text-xs opacity-75">{formatted} · {weekday}</div>
      <h1 className="text-xl font-bold mt-1 tracking-tight">🤖 AI 每日热点</h1>
      <div className="text-xs opacity-60 mt-0.5">AI Daily Hotpot</div>
    </header>
  )
}
```

- [ ] **Step 2: 编写 HeadlineCarousel.tsx**

```typescript
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
```

- [ ] **Step 3: Commit**

```bash
git add web/src/components/Header.tsx web/src/components/HeadlineCarousel.tsx
git commit -m "feat: add Header and HeadlineCarousel components"
```

---

### Task 17: 前端 — NewsItem + HeatBadge

**Files:**
- Create: `web/src/components/NewsItem.tsx`
- Create: `web/src/components/HeatBadge.tsx`

- [ ] **Step 1: 编写 HeatBadge.tsx**

```typescript
interface HeatBadgeProps {
  heat: number
}

export function HeatBadge({ heat }: HeatBadgeProps) {
  const colorClass =
    heat >= 8 ? 'text-[#f59e0b] bg-[#f59e0b]/10' :
    heat >= 5 ? 'text-[#10b981] bg-[#10b981]/10' :
    'text-gray-500 bg-gray-500/10'

  return (
    <span className={`inline-flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded ${colorClass}`}>
      🔥 {heat.toFixed(1)}
    </span>
  )
}
```

- [ ] **Step 2: 编写 NewsItem.tsx**

```typescript
import type { NewsItem as INewsItem } from '../types'
import { HeatBadge } from './HeatBadge'

interface NewsItemProps {
  item: INewsItem
  onClick: (item: INewsItem) => void
}

export function NewsItem({ item, onClick }: NewsItemProps) {
  return (
    <button
      onClick={() => onClick(item)}
      className="card p-3 w-full text-left block mb-2"
    >
      {/* 标题行 */}
      <div className="flex items-start gap-2">
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-white leading-snug line-clamp-2">
            {item.title_cn}
          </h4>
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">
            {item.title_en}
          </p>
        </div>
      </div>

      {/* 摘要 */}
      <p className="text-xs text-gray-400 mt-1.5 leading-relaxed line-clamp-2">
        {item.summary_cn}
      </p>

      {/* 底部信息 */}
      <div className="flex items-center gap-2 mt-2 flex-wrap">
        <HeatBadge heat={item.heat} />
        <span className="text-[10px] text-gray-600">{item.source}</span>
        {item.meta && (
          <span className="text-[10px] text-gray-600">{item.meta}</span>
        )}
      </div>

      {/* 标签 */}
      {item.tags.length > 0 && (
        <div className="flex gap-1 mt-1.5 flex-wrap">
          {item.tags.slice(0, 3).map(tag => (
            <span key={tag} className="text-[9px] px-1.5 py-0.5 rounded-full bg-[#2a2a3e] text-gray-400">
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* 学习建议 */}
      {item.student_note && (
        <div className="mt-1.5 text-[10px] text-[#10b981] bg-[#10b981]/5 rounded-md px-2 py-1">
          💡 {item.student_note}
        </div>
      )}
    </button>
  )
}
```

- [ ] **Step 3: Commit**

```bash
git add web/src/components/NewsItem.tsx web/src/components/HeatBadge.tsx
git commit -m "feat: add NewsItem and HeatBadge components"
```

---

### Task 18: 前端 — SectionCard + TabBar

**Files:**
- Create: `web/src/components/SectionCard.tsx`
- Create: `web/src/components/TabBar.tsx`

- [ ] **Step 1: 编写 SectionCard.tsx**

```typescript
import type { Section, NewsItem as INewsItem } from '../types'
import { NewsItem } from './NewsItem'

interface SectionCardProps {
  section: Section
  onItemClick: (item: INewsItem) => void
  showCount?: number
}

export function SectionCard({ section, onItemClick, showCount = 5 }: SectionCardProps) {
  if (!section.items.length) return null

  const visibleItems = section.items.slice(0, showCount)

  return (
    <div className="px-3 mb-5">
      {/* 板块标题 */}
      <div className="flex items-center gap-2 mb-2">
        <span className="text-base">{section.icon}</span>
        <h2 className="text-sm font-bold text-white">{section.title_cn}</h2>
        <span className="text-xs text-gray-500">{section.title_en}</span>
      </div>

      {/* 条目列表 */}
      {visibleItems.map((item, i) => (
        <NewsItem key={i} item={item} onClick={onItemClick} />
      ))}

      {/* 更多 */}
      {section.items.length > showCount && (
        <button className="w-full text-xs text-gray-500 py-2 text-center card">
          查看全部 {section.items.length} 条 →
        </button>
      )}
    </div>
  )
}
```

- [ ] **Step 2: 编写 TabBar.tsx**

```typescript
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
```

- [ ] **Step 3: Commit**

```bash
git add web/src/components/SectionCard.tsx web/src/components/TabBar.tsx
git commit -m "feat: add SectionCard and TabBar components"
```

---

### Task 19: 前端 — App.tsx + main.tsx

**Files:**
- Create: `web/src/App.tsx`
- Modify: `web/src/main.tsx`

- [ ] **Step 1: 编写 App.tsx**

```typescript
import { useState, useCallback } from 'react'
import { useDailyData } from './hooks/useDailyData'
import { Header } from './components/Header'
import { HeadlineCarousel } from './components/HeadlineCarousel'
import { SectionCard } from './components/SectionCard'
import { TabBar } from './components/TabBar'
import type { NewsItem } from './types'

export default function App() {
  const { data, loading, error } = useDailyData()
  const [activeTab, setActiveTab] = useState('all')

  const handleItemClick = useCallback((item: NewsItem) => {
    if (item.url) {
      window.open(item.url, '_blank', 'noopener,noreferrer')
    }
  }, [])

  const filteredSections =
    activeTab === 'all'
      ? data.sections
      : data.sections.filter(s => s.id === activeTab)

  return (
    <div className="min-h-screen pb-20 max-w-lg mx-auto">
      <Header date={data.date} />

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-500">
          <div className="text-3xl mb-3 animate-pulse">🤖</div>
          <p className="text-sm">加载中...</p>
        </div>
      ) : error && !data.sections.length ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-500">
          <div className="text-3xl mb-3">📡</div>
          <p className="text-sm">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 text-xs text-[#6366f1]"
          >
            点击重试
          </button>
        </div>
      ) : (
        <>
          {activeTab === 'all' && data.headlines.length > 0 && (
            <HeadlineCarousel
              headlines={data.headlines}
              onItemClick={handleItemClick}
            />
          )}

          {filteredSections.map(section => (
            <SectionCard
              key={section.id}
              section={section}
              onItemClick={handleItemClick}
              showCount={activeTab === 'all' ? 5 : 15}
            />
          ))}

          {filteredSections.length === 0 && (
            <div className="text-center py-20 text-gray-500 text-sm">
              该板块暂无今日资讯
            </div>
          )}

          <div className="text-center text-[10px] text-gray-600 py-6">
            AI 每日热点 · {data.date} · 由 DeepSeek 提供摘要
          </div>
        </>
      )}

      <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  )
}
```

- [ ] **Step 2: 编写 main.tsx**

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

- [ ] **Step 3: Commit**

```bash
git add web/src/App.tsx web/src/main.tsx
git commit -m "feat: add main App layout with tab navigation"
```

---

### Task 20: 前端 — PWA 配置 + Service Worker

**Files:**
- Create: `web/public/manifest.json`
- Create: `web/public/sw.js`
- Create: `web/public/icons/icon-192.png` (占位)

- [ ] **Step 1: 编写 manifest.json**

```json
{
  "name": "AI 每日热点",
  "short_name": "AI热点",
  "description": "每日 AI 热点中英双语简报",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0f0f1a",
  "theme_color": "#667eea",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

- [ ] **Step 2: 编写 sw.js**

```javascript
// Service Worker for AI Daily Hotpot
const CACHE_NAME = 'ai-hotpot-v1'
const DATA_CACHE = 'daily-data'

// 安装时不预缓存（数据是动态的）
self.addEventListener('install', () => {
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== DATA_CACHE).map(k => caches.delete(k)))
    )
  )
  self.clients.claim()
})

// 网络优先策略（数据文件）
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // daily.json: Network First
  if (url.pathname.endsWith('/data/daily.json')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          const clone = response.clone()
          caches.open(DATA_CACHE).then(cache => cache.put(request, clone))
          return response
        })
        .catch(() => caches.match(request))
    )
    return
  }

  // 其他资源: Cache First
  event.respondWith(
    caches.match(request).then(cached => cached || fetch(request))
  )
})
```

- [ ] **Step 3: 生成占位图标**

```bash
# 创建一个简单的 SVG 转 PNG 占位图标
cd D:/ai_hotpot/web/public/icons
# 使用 Python 生成简单的 192x192 PNG 图标（纯色方块）
python -c "
import struct, zlib

def create_png(width, height, color=(102, 126, 234)):
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    header = b'\\x89PNG\\r\\n\\x1a\\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))

    raw = b''
    for y in range(height):
        raw += b'\\x00'  # filter none
        for x in range(width):
            raw += bytes(color)

    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')

    return header + ihdr + idat + iend

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    with open(name, 'wb') as f:
        f.write(create_png(size, size))
    print(f'Created {name} ({size}x{size})')
"
```

- [ ] **Step 4: Commit**

```bash
git add web/public/manifest.json web/public/sw.js web/public/icons/icon-192.png web/public/icons/icon-512.png
git commit -m "feat: add PWA manifest and service worker"
```

---

### Task 21: Vercel 部署配置 + 集成测试

**Files:**
- Create: `web/vercel.json`
- Create: `web/public/data/.gitkeep`

- [ ] **Step 1: 创建 vercel.json**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

- [ ] **Step 2: 创建 data 目录占位**

```bash
mkdir -p D:/ai_hotpot/web/public/data
touch D:/ai_hotpot/web/public/data/.gitkeep
```

Write `web/public/data/.gitkeep`:
```
# daily.json 由 GitHub Actions 每天自动生成
# 此文件仅用于确保目录被 git 跟踪
```

- [ ] **Step 3: 创建 sample daily.json 用于本地开发**

Write `web/public/data/daily.json` (开发用示例):

```json
{
  "date": "2026-05-31",
  "generated_at": "2026-05-31T07:00:00+08:00",
  "headlines": [
    {
      "title_cn": "欢迎使用 AI 每日热点",
      "title_en": "Welcome to AI Daily Hotpot",
      "summary_cn": "这是开发环境的示例数据。正式数据由 GitHub Actions 每天 7:00 自动生成。",
      "summary_en": "This is sample data for development. Real data is generated daily at 7:00 AM by GitHub Actions.",
      "url": "https://github.com",
      "source": "Dev Sample",
      "source_icon": "link",
      "heat": 9.0,
      "tags": ["示例"],
      "student_note": null
    }
  ],
  "sections": [
    {
      "id": "github",
      "title_cn": "GitHub AI 热门",
      "title_en": "GitHub AI Trending",
      "icon": "🐙",
      "items": []
    },
    {
      "id": "vendor",
      "title_cn": "大模型厂商动态",
      "title_en": "LLM Vendors Updates",
      "icon": "🧠",
      "items": []
    },
    {
      "id": "people",
      "title_cn": "AI 科技人物",
      "title_en": "AI Key Figures",
      "icon": "👤",
      "items": []
    },
    {
      "id": "news",
      "title_cn": "AI 行业新闻",
      "title_en": "AI Industry News",
      "icon": "📰",
      "items": []
    },
    {
      "id": "academic",
      "title_cn": "学术前沿",
      "title_en": "Academic Frontier",
      "icon": "📚",
      "items": []
    }
  ]
}
```

- [ ] **Step 4: 本地构建测试**

```bash
cd D:/ai_hotpot/web && npm run build
```

Expected: 构建成功，输出到 `web/dist/`

- [ ] **Step 5: 本地预览测试**

```bash
cd D:/ai_hotpot/web && npm run preview
```

打开 http://localhost:4173 验证：
- 页面正常渲染
- Header 显示日期和标题
- Tab 切换正常
- 卡片布局正常
- 暗色主题生效

- [ ] **Step 6: Commit**

```bash
git add web/vercel.json web/public/data/.gitkeep web/public/data/daily.json
git commit -m "feat: add Vercel config, sample data, and local dev setup"
```

---

### Task 22: 集成验证 & GitHub 推送

- [ ] **Step 1: 完整端到端测试（模拟 GitHub Actions 环境）**

```bash
cd D:/ai_hotpot

# 1. 采集测试（离线模式，不需要 DeepSeek Key）
python -c "
from crawler.sources.github_trending import fetch_github_trending
from crawler.sources.rss_feeds import fetch_rss_feeds
from crawler.sources.hackernews_ai import fetch_hackernews_ai
from crawler.filter_rank import filter_and_rank

# 测试各采集器能正常运行
items = []
items.extend(fetch_github_trending())
items.extend(fetch_rss_feeds())
items.extend(fetch_hackernews_ai(min_points=30, max_items=50))
print(f'Total collected: {len(items)}')

filtered = filter_and_rank(items)
print(f'After filter: {len(filtered)}')
print('✅ Crawler pipeline OK')
"

# 2. JSON 生成测试
python -c "
from processor.generate_json import generate_daily_json
import json

# 使用测试数据
test_items = [{
    'title': 'Test',
    'title_cn': '测试标题',
    'title_en': 'Test Title',
    'summary_cn': '测试摘要',
    'summary_en': 'Test summary',
    'url': 'https://example.com',
    'source': 'Test',
    'source_icon': 'test',
    'heat': 5.0,
    'tags': ['test'],
    'section': 'news',
    'published_at': '2026-05-31T00:00:00+00:00',
}]
result = generate_daily_json(test_items, test_items)
print(json.dumps(result, ensure_ascii=False, indent=2)[:200])
print('✅ JSON generation OK')
"

# 3. 前端构建测试
cd web && npm run build
echo '✅ Frontend build OK'
```

- [ ] **Step 2: 创建 GitHub 仓库并推送**

```bash
cd D:/ai_hotpot
git add -A
git status
```

检查遗漏文件后：

```bash
git commit -m "chore: complete project structure and all modules"
```

创建 GitHub 仓库（手动或通过 CLI）：
```bash
# 在 GitHub 上创建仓库 ai-hotpot 后:
git remote add origin https://github.com/YOUR_USERNAME/ai-hotpot.git
git branch -M main
git push -u origin main
```

- [ ] **Step 3: 配置 GitHub Secrets**

在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加：
- `DEEPSEEK_API_KEY`：DeepSeek API 密钥
- `VERCEL_TOKEN`：Vercel 个人令牌
- `VERCEL_ORG_ID`：Vercel 组织 ID
- `VERCEL_PROJECT_ID`：Vercel 项目 ID

- [ ] **Step 4: Vercel 项目创建**

```bash
# 安装 Vercel CLI
npm i -g vercel

# 在 web 目录下初始化 Vercel 项目
cd D:/ai_hotpot/web && vercel link
# 记下输出的 org ID 和 project ID，填入 GitHub Secrets
```

- [ ] **Step 5: 手动触发首次运行验证**

在 GitHub Actions → Daily AI Fetch → Run workflow

验证：
1. Actions 日志无报错
2. `web/public/data/daily.json` 被更新
3. Vercel 部署成功
4. 手机打开 Vercel URL，PWA 正常显示

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: final integration and deployment setup"
git push
```

---

## 附录 A: 环境变量清单

| 变量名 | 用途 | 配置位置 |
|--------|------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | GitHub Secrets |
| `VERCEL_TOKEN` | Vercel 部署令牌 | GitHub Secrets |
| `VERCEL_ORG_ID` | Vercel 组织 ID | GitHub Secrets |
| `VERCEL_PROJECT_ID` | Vercel 项目 ID | GitHub Secrets |

## 附录 B: 本地开发快速启动

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 设置 DeepSeek API Key
export DEEPSEEK_API_KEY="sk-xxxx"

# 3. 运行完整采集（会在 web/public/data/ 生成 daily.json）
python crawler/fetch_all.py

# 4. 启动前端开发服务器
cd web && npm run dev

# 5. 手机预览：确保手机和电脑在同一网络
# 浏览器打开 http://<电脑IP>:5173
```

## 附录 C: Swiper 轮播样式覆盖

在 `web/src/styles/index.css` 末尾添加：

```css
/* Swiper 轮播样式 */
.headline-swiper {
  padding-bottom: 20px !important;
}

.swiper-bullet {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #3a3a5e;
  margin: 0 3px;
  transition: all 0.2s;
}

.swiper-bullet-active {
  background: #f59e0b;
  width: 16px;
  border-radius: 3px;
}

/* 移动端安全区域 */
.safe-top {
  padding-top: max(12px, env(safe-area-inset-top));
}

.safe-bottom {
  padding-bottom: max(4px, env(safe-area-inset-bottom));
}
```
