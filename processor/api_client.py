"""DeepSeek API 客户端。

自动选择底层 HTTP 后端：
1. 优先 OpenAI SDK (httpx)
2. SSL 失败时回退到 curl（Windows Python SSL 兼容）
"""

import json
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-flash"


def get_api_key() -> str:
    """获取 API Key（必须通过环境变量 DEEPSEEK_API_KEY 设置）。"""
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "DEEPSEEK_API_KEY 环境变量未设置。\n"
            "请在终端执行: export DEEPSEEK_API_KEY=sk-xxxx\n"
            "或在 GitHub Actions 中配置 DEEPSEEK_API_KEY secret。"
        )
    return api_key


def call_deepseek(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 4096,
    model: str | None = None,
) -> str:
    """调用 DeepSeek Chat API。

    Args:
        messages: OpenAI 格式的消息列表
        temperature: 创意度
        max_tokens: 最大输出 token
        model: 模型名（默认 DEEPSEEK_MODEL）

    Returns:
        模型回复的文本内容
    """
    if model is None:
        model = DEEPSEEK_MODEL

    api_key = get_api_key()

    # 方法 1: OpenAI SDK
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.debug(f"OpenAI SDK failed (trying curl): {e}")

    # 方法 2: curl 回退（Windows Python SSL 兼容）
    try:
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }, ensure_ascii=False)
        cmd = [
            "curl", "-s", "-m", "120",
            f"{DEEPSEEK_BASE_URL}/v1/chat/completions",
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {api_key}",
            "-d", payload,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=125)
        if result.returncode != 0:
            raise RuntimeError(f"curl exit {result.returncode}: {result.stderr[:200]}")
        data = json.loads(result.stdout)
        if "error" in data:
            raise RuntimeError(f"API error: {data['error']}")
        return data["choices"][0]["message"]["content"] or ""
    except Exception as e:
        raise RuntimeError(f"DeepSeek API call failed: {e}")


def extract_json(content: str) -> str:
    """从可能包含 markdown 包裹的文本中提取 JSON。"""
    content = content.strip()
    if "```json" in content:
        return content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        return content.split("```")[1].split("```")[0].strip()
    return content
