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
