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
