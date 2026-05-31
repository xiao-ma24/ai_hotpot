"""DeepSeek API 分类校对与热度评分。"""

import json
import logging

from processor.api_client import call_deepseek, extract_json
from processor.prompts import SYSTEM_PROMPT, CLASSIFY_SCORE_PROMPT

logger = logging.getLogger(__name__)

BATCH_SIZE = 10


def classify_and_score(items: list[dict]) -> list[dict]:
    """为每条资讯分类 + 热度评分 + 打标签。

    Args:
        items: 已有摘要的条目列表

    Returns:
        list[dict]: 添加了 section, heat, tags 字段的条目列表
    """
    if not items:
        return items

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
            content = call_deepseek(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2048,
            )

            ai_results = json.loads(extract_json(content))

            for ai_item in ai_results:
                idx = ai_item.get("index", -1)
                if 0 <= idx < len(batch):
                    batch[idx]["section"] = ai_item.get("section", batch[idx].get("_section_hint", "news"))
                    batch[idx]["heat"] = float(ai_item.get("heat", 5.0))
                    batch[idx]["tags"] = ai_item.get("tags", [])

            for item in batch:
                item.pop("_section_hint", None)

        except Exception as e:
            logger.error(f"  Classification error: {e}")
            for item in batch:
                item.pop("_section_hint", None)

    return items
