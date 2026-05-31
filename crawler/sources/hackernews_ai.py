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
