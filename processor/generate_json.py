"""生成最终的 daily.json 文件。"""

from datetime import datetime, timezone, timedelta


def generate_daily_json(items: list[dict], headlines: list[dict], must_read: list[dict] | None = None) -> dict:
    """将处理完的条目组织成 daily.json 结构。

    Args:
        items: 已处理的所有条目（带 title_cn, summary_cn, heat, section 等）
        headlines: 头条条目

    Returns:
        dict: daily.json 完整结构
    """
    # 北京时间
    beijing_tz = timezone(timedelta(hours=8))
    now_beijing = datetime.now(beijing_tz)

    # 板块配置
    section_config = {
        "github": {
            "title_cn": "GitHub AI 热门",
            "title_en": "GitHub AI Trending",
            "icon": "🐙",
        },
        "vendor": {
            "title_cn": "大模型厂商动态",
            "title_en": "LLM Vendors Updates",
            "icon": "🧠",
        },
        "people": {
            "title_cn": "AI 科技人物",
            "title_en": "AI Key Figures",
            "icon": "👤",
        },
        "news": {
            "title_cn": "AI 行业新闻",
            "title_en": "AI Industry News",
            "icon": "📰",
        },
        "academic": {
            "title_cn": "学术前沿",
            "title_en": "Academic Frontier",
            "icon": "📚",
        },
    }

    # 构建 sections
    sections_map = {}
    for item in items:
        section_id = item.get("section", "news")
        if section_id not in sections_map:
            sections_map[section_id] = []
        sections_map[section_id].append(_to_output_item(item))

    # 每个板块按热度排序，取前 15 条
    sections = []
    for sec_id in ["github", "vendor", "people", "news", "academic"]:
        sec_items = sections_map.get(sec_id, [])
        sec_items.sort(key=lambda x: x.get("heat", 0), reverse=True)
        sec_items = sec_items[:15]

        config = section_config.get(sec_id, section_config["news"])
        sections.append({
            "id": sec_id,
            "title_cn": config["title_cn"],
            "title_en": config["title_en"],
            "icon": config["icon"],
            "items": sec_items,
        })

    # 构建头条
    headline_items = [_to_output_item(h, is_headline=True) for h in headlines]

    # 构建必读
    must_read_items = []
    if must_read:
        for item in must_read:
            out = _to_output_item(item)
            out["detail_summary"] = item.get("detail_summary", "")
            out["key_points"] = item.get("key_points", [])
            must_read_items.append(out)

    return {
        "date": now_beijing.strftime("%Y-%m-%d"),
        "generated_at": now_beijing.isoformat(),
        "headlines": headline_items,
        "sections": sections,
        "must_read": must_read_items,
    }


def _to_output_item(item: dict, is_headline: bool = False) -> dict:
    """将内部条目转为 daily.json 中的标准条目格式。"""
    out = {
        "title_cn": item.get("title_cn", item.get("title", "")),
        "title_en": item.get("title_en", item.get("title", "")),
        "summary_cn": item.get("summary_cn", item.get("description", "")),
        "summary_en": item.get("summary_en", item.get("description", "")),
        "url": item.get("url", ""),
        "source": item.get("source", ""),
        "source_icon": item.get("source_icon", "link"),
        "heat": item.get("heat", 5.0),
        "tags": item.get("tags", []),
        "student_note": item.get("student_note"),
        "published_at": item.get("published_at", ""),
    }

    # 附加元数据（不同来源有不同元数据）
    meta_parts = []
    if item.get("stars"):
        meta_parts.append(f"⭐ {_format_number(item['stars'])}")
    if item.get("language"):
        meta_parts.append(item["language"])
    if item.get("stars_today"):
        meta_parts.append(f"+{_format_number(item['stars_today'])} today")
    if item.get("points"):
        meta_parts.append(f"▲ {item['points']}")
    if item.get("comments"):
        meta_parts.append(f"💬 {item['comments']}")
    if item.get("upvotes"):
        meta_parts.append(f"👍 {item['upvotes']}")
    if item.get("authors"):
        meta_parts.append(", ".join(item["authors"][:3]))

    if meta_parts:
        out["meta"] = " · ".join(meta_parts)

    return out


def _format_number(n: int) -> str:
    """格式化数字（1.2k, 3.4M 等）。"""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)
