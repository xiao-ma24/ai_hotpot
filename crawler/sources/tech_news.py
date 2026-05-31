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
