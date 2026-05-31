"""DeepSeek API 批量摘要生成。

将原始采集数据分批次发送给 DeepSeek，获取双语摘要。
"""

import json
import logging
import os
from openai import OpenAI

from processor.prompts import SYSTEM_PROMPT, BATCH_SUMMARIZE_PROMPT

logger = logging.getLogger(__name__)

# DeepSeek API 配置 (OpenAI 兼容接口)
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 每批处理条数（控制 token 消耗）
BATCH_SIZE = 15

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if not api_key:
            raise RuntimeError("DEEPSEEK_API_KEY environment variable not set")
        _client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
    return _client


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

    client = _get_client()
    result = []

    for i in range(0, len(items), BATCH_SIZE):
        batch = items[i : i + BATCH_SIZE]
        logger.info(f"Summarizing batch {i // BATCH_SIZE + 1}: {len(batch)} items")

        # 构造输入（只传必要字段给 AI）
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
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=4096,
            )

            content = response.choices[0].message.content or ""
            # 提取 JSON（处理可能的 markdown 包裹）
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            ai_results = json.loads(content.strip())

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
            logger.error(f"  JSON parse error in batch: {e}")
            logger.debug(f"  Raw content: {content[:200]}")
        except Exception as e:
            logger.error(f"  DeepSeek API error in batch: {e}")

        result.extend(batch)

    return result
