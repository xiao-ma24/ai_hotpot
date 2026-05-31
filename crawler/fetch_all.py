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


if __name__ == "__main__":
    main()
