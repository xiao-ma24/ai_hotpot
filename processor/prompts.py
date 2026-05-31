"""DeepSeek API Prompt 模板。

所有 AI 处理的核心——提示词质量直接决定简报质量。
"""

# === 系统角色 ===
SYSTEM_PROMPT = """你是一位资深 AI 科技编辑，服务于中国大学生读者。
你的任务是将全球 AI 资讯处理成中英双语深度简报。

核心原则：
1. **准确第一**：不要编造、不要过度解读，基于原文信息提炼
2. **学生友好**：提供学习建议，标注对大学生有帮助的内容
3. **双语自然**：中文摘要面向国内读者，英文摘要面向国际读者，两者独立撰写而非机械翻译
4. **热度客观**：基于实际影响力、讨论度、技术创新度综合评分，而非标题党
5. **格式严格**：必须按指定 JSON 格式输出，不要添加多余文字
"""

# === 批量摘要 Prompt ===
BATCH_SUMMARIZE_PROMPT = """请为以下 {count} 条 AI 资讯生成双语摘要。

## 输入数据
{items_json}

## 输出要求
对每条资讯返回一个 JSON 对象，字段含义：
- `title_cn`: 中文标题（简洁准确，15 字以内，不是原文翻译而是符合中文阅读习惯的标题）
- `title_en`: 英文标题（保留原始英文标题，如原文无英文标题则翻译）
- `summary_cn`: 中文摘要（2-3 句，说清核心内容，面向大学生读者，解释关键术语）
- `summary_en`: 英文摘要（2-3 sentences, clear and concise）
- `student_note`: 学习建议（可选，如果这条资讯对大学生特别有帮助，写 1 句简短的学习建议；否则为 null。例如"推荐阅读，了解 Transformer 架构的最新优化方向"）

## 返回格式
返回一个 JSON 数组，每条资讯对应一个对象：
```json
[
  {{
    "index": 0,
    "title_cn": "...",
    "title_en": "...",
    "summary_cn": "...",
    "summary_en": "...",
    "student_note": "..." or null
  }},
  ...
]
```
注意：
- index 必须与输入顺序一致
- 不要省略任何条目
- student_note 只在确实有帮助时填写，null 表示不需要
- 只返回 JSON 数组，不要有其他文字
"""

# === 分类 & 评分 Prompt ===
CLASSIFY_SCORE_PROMPT = """请为以下 {count} 条已摘要的 AI 资讯进行分类校对和热度评分。

## 输入数据
{items_json}

## 分类规则
每条资讯归入以下板块之一：
- `github`: GitHub 开源项目
- `vendor`: 大模型厂商动态（OpenAI/Anthropic/DeepMind/Meta/DeepSeek/Qwen 等）
- `people`: AI 科技人物（Elon Musk/Sam Altman/Demis Hassabis 等）
- `news`: 行业新闻（TechCrunch/The Verge/机器之心/量子位 等）
- `academic`: 学术前沿（ArXiv 论文/HuggingFace 论文）

## 热度评分 (1-10)
- 9-10 分：行业震动级（GPT-5 发布、万 star 项目、行业并购）
- 7-8 分：重要进展（大厂新功能、千 star 项目、核心人物发声）
- 5-6 分：值得关注（有趣新项目、行业分析、重要论文）
- 3-4 分：一般资讯（常规更新、普通新闻）
- 1-2 分：边角内容

## 标签
每条资讯打 2-4 个标签（中文），如：["模型发布","OpenAI","多模态"]

## 返回格式
```json
[
  {{
    "index": 0,
    "section": "vendor",
    "heat": 8.5,
    "tags": ["模型发布", "OpenAI"]
  }},
  ...
]
```
只返回 JSON 数组，不要有其他文字。
"""

# === 头条筛选 Prompt ===
HEADLINES_PROMPT = """从以下 {count} 条 AI 资讯中，选出 {n} 条作为今日头条。

## 输入数据
{items_json}

## 头条标准
1. 最重要：对 AI 行业有重大影响
2. 最有趣：大学生最想看的内容
3. 覆盖面：尽量覆盖不同板块
4. 新鲜度：优先当日/昨日新内容

## 返回格式
```json
{{
  "headlines": [3, 7, 12, ...]
}}
```
headlines 数组包含入选条目的 index（只返回 index 列表，不是完整对象）。
只返回 JSON 对象，不要有其他文字。
"""
