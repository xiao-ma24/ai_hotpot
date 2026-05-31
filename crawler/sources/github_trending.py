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
