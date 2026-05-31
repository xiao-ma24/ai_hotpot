"""GitHub AI 热门项目采集。

使用 GitHub Search API（官方接口）获取 AI 相关热门仓库。
相比 Trending 页面，Search API 国内访问更稳定，且无需认证即可使用（60 次/小时）。
"""

import logging
from datetime import datetime, timedelta, timezone

import requests

logger = logging.getLogger(__name__)

# GitHub Search API（无需认证，60 次/小时，每天一次绰绰有余）
GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

# AI 主题搜索词
AI_TOPICS = [
    "artificial-intelligence", "machine-learning", "deep-learning",
    "llm", "nlp", "computer-vision", "generative-ai", "transformer",
    "langchain", "llama", "diffusion", "rag", "agent",
]

# 关键词（配合文本搜索）
AI_KEYWORDS = [
    "ai", "llm", "gpt", "nlp", "cv", "agent", "transformer",
    "deep-learning", "machine-learning", "neural", "diffusion",
    "rag", "embedding", "langchain", "llama", "mistral",
    "chatgpt", "openai", "claude", "stable-diffusion",
    "deepseek", "qwen", "whisper", "tts", "ocr",
]


def fetch_github_trending() -> list[dict]:
    """使用 GitHub Search API 获取近期 AI 热门仓库。

    策略：
    1. 搜索 AI 主题标签，按 stars 排序
    2. 搜索最近创建的高星 AI 项目
    3. 合并去重，按 star 增速排序

    Returns:
        list[dict]: 项目列表，字段: title, description, url, stars, language,
                    stars_today, forks
    """
    items = []
    seen = set()
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    last_week = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "ai-daily-hotpot/1.0",
    }

    # 策略 1: 一次性搜索多个 AI 主题（合并为一次 API 调用）
    try:
        # 用 OR 连接多个主题，一次查询覆盖所有
        topic_query = "+".join(f"topic:{t}" for t in AI_TOPICS[:5])
        params = {
            "q": f"{topic_query}+stars:>50",
            "sort": "stars",
            "order": "desc",
            "per_page": 30,
        }
        resp = requests.get(GITHUB_SEARCH_URL, params=params, headers=headers, timeout=15)
        if resp.status_code == 403:
            logger.warning("GitHub API rate limit exceeded (wait for reset)")
        else:
            resp.raise_for_status()
            data = resp.json()

            for repo in data.get("items", []):
                url = repo.get("html_url", "")
                if url in seen:
                    continue
                seen.add(url)
                items.append(_parse_repo(repo))

            logger.debug(f"  Topic search: {len(items)} repos so far")

    except Exception as e:
        logger.warning(f"GitHub topic search failed: {e}")

    # 策略 2: 搜索最近一周创建的高星 AI 项目（关键词匹配）
    try:
        params = {
            "q": f"ai+machine-learning+stars:>100+created:>={last_week}",
            "sort": "stars",
            "order": "desc",
            "per_page": 20,
        }
        resp = requests.get(GITHUB_SEARCH_URL, params=params, headers=headers, timeout=15)
        if resp.status_code == 403:
            logger.warning("GitHub API rate limit exceeded (wait for reset)")
        else:
            resp.raise_for_status()
            data = resp.json()

            for repo in data.get("items", []):
                url = repo.get("html_url", "")
                if url in seen:
                    continue
                seen.add(url)

                # 关键词二次筛选
                if not _is_ai_project(repo):
                    continue

                items.append(_parse_repo(repo))

    except Exception as e:
        logger.warning(f"GitHub keyword search failed: {e}")

    # 按 stars 排序
    items.sort(key=lambda x: x.get("stars", 0), reverse=True)
    logger.info(f"GitHub: {len(items)} AI-related repos found")
    return items


def _parse_repo(repo: dict) -> dict:
    """将 GitHub API 返回的仓库转为标准格式。"""
    return {
        "title": repo.get("full_name", repo.get("name", "")),
        "description": (repo.get("description") or "")[:500],
        "url": repo.get("html_url", ""),
        "stars": repo.get("stargazers_count", 0),
        "language": repo.get("language") or "",
        "stars_today": 0,  # Search API 不提供日增量
        "forks": repo.get("forks_count", 0),
        "source": "GitHub Trending",
        "published_at": repo.get("created_at", ""),
    }


def _is_ai_project(repo: dict) -> bool:
    """检查仓库是否与 AI 相关。"""
    name = repo.get("full_name", repo.get("name", "")).lower()
    description = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    language = (repo.get("language") or "").lower()

    # 检查 topics（最可靠）
    ai_topics_lower = [t.lower() for t in AI_TOPICS]
    if any(at in t for t in topics for at in ai_topics_lower):
        return True

    # 检查关键词
    text = f"{name} {description} {language}"
    return any(kw in text for kw in AI_KEYWORDS)


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
