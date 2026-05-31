"""DeepSeek API 批量摘要生成。

将原始采集数据分批次发送给 DeepSeek，获取双语摘要。
"""

import json
import logging

from processor.api_client import call_deepseek, extract_json
from processor.prompts import SYSTEM_PROMPT, BATCH_SUMMARIZE_PROMPT

logger = logging.getLogger(__name__)

# 每批处理条数（控制 token 消耗）
BATCH_SIZE = 15


def batch_summarize(items: list[dict]) -> list[dict]:
    """批量生成中英双语摘要。

    Args:
        items: 过滤后的原始条目列表

    Returns:
        list[dict]: 添加了 title_cn, title_en, summary_cn, summary_en,
                    student_note 字段的条目列表
    """
    if not items:
        return items

    result = []

    for i in range(0, len(items), BATCH_SIZE):
        batch = items[i : i + BATCH_SIZE]
        logger.info(f"Summarizing batch {i // BATCH_SIZE + 1}: {len(batch)} items")

        # 构造输入
        input_data = []
        for idx, item in enumerate(batch):
            input_data.append({
                "index": idx,
                "title": item.get("title", ""),
                "description": item.get("description", "")[:300],
                "source": item.get("source", ""),
            })

        prompt = BATCH_SUMMARIZE_PROMPT.format(
            count=len(input_data),
            items_json=json.dumps(input_data, ensure_ascii=False, indent=2),
        )

        try:
            content = call_deepseek(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )

            ai_results = json.loads(extract_json(content))

            # 合并回原始数据
            for ai_item in ai_results:
                idx = ai_item.get("index", -1)
                if 0 <= idx < len(batch):
                    batch[idx]["title_cn"] = ai_item.get("title_cn", batch[idx].get("title", ""))
                    batch[idx]["title_en"] = ai_item.get("title_en", batch[idx].get("title", ""))
                    batch[idx]["summary_cn"] = ai_item.get("summary_cn", "")
                    batch[idx]["summary_en"] = ai_item.get("summary_en", "")
                    batch[idx]["student_note"] = ai_item.get("student_note")

            logger.info(f"  Batch summarized: {len(ai_results)} responses")

        except json.JSONDecodeError as e:
            logger.error(f"  JSON parse error: {e}")
        except Exception as e:
            logger.error(f"  DeepSeek API error: {e}")

        result.extend(batch)

    return result
