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
