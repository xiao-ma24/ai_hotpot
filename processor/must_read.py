"""必读文章筛选 + 详细摘要生成。

从已分类评分的所有条目中：
1. 筛选 10 篇必读
2. 为必读文章生成详细摘要和关键要点
"""

import json
import logging

from processor.api_client import call_deepseek, extract_json
from processor.prompts import SYSTEM_PROMPT, MUST_READ_SELECT_PROMPT, MUST_READ_DETAIL_PROMPT

logger = logging.getLogger(__name__)

MUST_READ_COUNT = 10


def select_and_detail(items: list[dict], n: int = MUST_READ_COUNT) -> list[dict]:
    """筛选必读文章并生成详细摘要。

    Args:
        items: 已分类评分的所有条目
        n: 必读数量

    Returns:
        list[dict]: 必读条目（含 detail_summary 和 key_points）
    """
    if not items:
        return []

    # Step 1: 筛选必读
    indices = _select_must_read(items, n)
    if not indices:
        logger.warning("Must-read selection failed, using top by heat")
        sorted_items = sorted(items, key=lambda x: x.get("heat", 0), reverse=True)
        indices = list(range(min(n, len(sorted_items))))

    must_read_items = [items[i] for i in indices if 0 <= i < len(items)]
    logger.info(f"Must-read: {len(must_read_items)} articles selected")

    # Step 2: 生成详细摘要
    detailed = _generate_details(must_read_items)
    logger.info(f"Must-read details: {len(detailed)} generated")

    return detailed


def _select_must_read(items: list[dict], n: int) -> list[int]:
    """调用 DeepSeek 筛选必读文章。"""
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

    prompt = MUST_READ_SELECT_PROMPT.format(
        count=len(input_data),
        n=n,
        items_json=json.dumps(input_data, ensure_ascii=False, indent=2),
    )

    try:
        content = call_deepseek(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=512,
        )
        result = json.loads(extract_json(content))
        return result.get("must_read_indices", [])
    except Exception as e:
        logger.error(f"Must-read selection failed: {e}")
        return []


def _generate_details(items: list[dict]) -> list[dict]:
    """调用 DeepSeek 为必读文章生成详细摘要。"""
    if not items:
        return items

    input_data = []
    for idx, item in enumerate(items):
        input_data.append({
            "index": idx,
            "title_cn": item.get("title_cn", item.get("title", "")),
            "summary_cn": item.get("summary_cn", ""),
            "source": item.get("source", ""),
            "heat": item.get("heat", 5.0),
            "section": item.get("section", "news"),
            "tags": item.get("tags", []),
        })

    prompt = MUST_READ_DETAIL_PROMPT.format(
        count=len(input_data),
        items_json=json.dumps(input_data, ensure_ascii=False, indent=2),
    )

    try:
        content = call_deepseek(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        results = json.loads(extract_json(content))

        for r in results:
            idx = r.get("index", -1)
            if 0 <= idx < len(items):
                items[idx]["detail_summary"] = r.get("detail_summary", "")
                items[idx]["key_points"] = r.get("key_points", [])

    except Exception as e:
        logger.error(f"Detail generation failed: {e}")

    return items
