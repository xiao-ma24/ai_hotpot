"""头条筛选。

在所有板块处理完毕后，选出 3-5 条今日头条。
"""

import json
import logging
import os
from openai import OpenAI

from processor.prompts import SYSTEM_PROMPT, HEADLINES_PROMPT

logger = logging.getLogger(__name__)

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"
HEADLINE_COUNT = 5


def select_headlines(items: list[dict], n: int = HEADLINE_COUNT) -> list[dict]:
    """从所有已处理条目中选出头条。

    Args:
        items: 已分类评分的条目列表
        n: 头条数量

    Returns:
        list[dict]: 头条条目（带索引）
    """
    if not items:
        return []

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        logger.error("DEEPSEEK_API_KEY not set")
        sorted_items = sorted(items, key=lambda x: x.get("heat", 0), reverse=True)
        return sorted_items[:n]

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

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

    prompt = HEADLINES_PROMPT.format(
        count=len(input_data),
        n=n,
        items_json=json.dumps(input_data, ensure_ascii=False, indent=2),
    )

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=512,
        )

        content = response.choices[0].message.content or ""
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        result = json.loads(content.strip())
        indices = result.get("headlines", [])

        headlines = []
        for idx in indices:
            if 0 <= idx < len(items):
                headlines.append(items[idx])

        logger.info(f"Headlines selected: {len(headlines)}")
        return headlines

    except Exception as e:
        logger.error(f"Headline selection error: {e}")
        sorted_items = sorted(items, key=lambda x: x.get("heat", 0), reverse=True)
        return sorted_items[:n]
