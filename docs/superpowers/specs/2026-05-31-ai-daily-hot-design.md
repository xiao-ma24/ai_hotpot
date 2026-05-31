# 每日 AI 热点聚合 — 设计方案

**日期**: 2026-05-31
**状态**: 已批准
**版本**: v2.0

---

## 一、项目目标

每天自动收集全球 AI 相关热点（GitHub 热门项目、大模型厂商动态、科技人物动态、行业新闻、学术前沿），通过 DeepSeek API 生成中英双语深度简报，生成静态 JSON，通过 PWA 网页在手机上查看。零服务器成本，全自动运行。

**用户**：中国大学生，每天早上 7:40 打开手机即可查看当日 AI 热点。

---

## 二、数据源 & 板块设计

### 板块 1：🐙 GitHub AI 热门
- **来源**：GitHub Trending（日榜/周榜）
- **筛选**：标签含 AI/ML/LLM/NLP/CV/Agent，star 日增长 > 100 或周增长 > 500
- **内容**：项目名、描述、star 数、语言、链接、README 摘要

### 板块 2：🧠 大模型厂商动态
- **来源**：
  - OpenAI 官方博客 RSS、Anthropic 官方博客、Google DeepMind 博客
  - Meta AI 博客、DeepSeek 官方公告、阿里 Qwen 团队动态
  - 小米/Kimi 等国产厂商
- **筛选**：最近 2 天发布，模型发布/价格变更/重大更新优先
- **内容**：标题、摘要、来源、日期、链接

### 板块 3：👤 AI 科技人物
- **来源**：
  - Elon Musk / xAI（Nitter RSS + 新闻聚合）
  - Sam Altman、Demis Hassabis、Yann LeCun、Andrej Karpathy、Ilya Sutskever
- **筛选**：与 AI 直接相关的发言/公告
- **内容**：人物名、发言摘要（需 AI 提炼核心观点）、来源、日期、链接

### 板块 4：📰 AI 行业新闻
- **来源**：
  - Hacker News（title 含 AI/LLM/GPT，points > 50）
  - TechCrunch AI RSS、The Verge AI / VentureBeat AI RSS
  - 国内：机器之心 RSS、量子位 RSS
- **筛选**：最近 1-2 天，非重复
- **内容**：标题、摘要、来源、日期、链接

### 板块 5：📚 学术前沿
- **来源**：
  - ArXiv cs.AI / cs.CL / cs.CV 当日新提交
  - Hugging Face Daily Papers
- **筛选**：当日/昨日高关注度
- **内容**：标题、作者、摘要、链接

---

## 三、技术架构

```
📁 ai-hotpot/
├── .github/workflows/
│   └── daily-fetch.yml              # UTC 23:00 (= 北京时间 7:00) 触发
├── crawler/                          # 采集脚本（每个数据源独立）
│   ├── fetch_all.py                  # 编排入口
│   ├── sources/
│   │   ├── github_trending.py
│   │   ├── openai_blog.py
│   │   ├── anthropic_blog.py
│   │   ├── deepmind_blog.py
│   │   ├── meta_ai.py
│   │   ├── deepseek.py
│   │   ├── qwen.py
│   │   ├── ai_people.py              # 科技人物动态
│   │   ├── hackernews_ai.py
│   │   ├── tech_news.py              # TC/VB/The Verge/机器之心/量子位
│   │   └── arxiv.py
│   ├── filter_rank.py                # 去重 / 规则过滤 / 预排序
│   └── deepseek_process.py           # DeepSeek API 处理
├── processor/                        # AI 处理层
│   ├── prompts.py                    # DeepSeek Prompt 模板（核心）
│   ├── summarize.py                  # 批量摘要生成
│   ├── classify_score.py             # 分类校对 + 热度评分
│   ├── headlines.py                  # 头条筛选
│   └── generate_json.py              # 生成 daily.json
├── web/                              # PWA 前端
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Header.tsx            # 顶部日期 + 标题
│   │   │   ├── HeadlineCarousel.tsx  # 头条轮播
│   │   │   ├── SectionCard.tsx       # 板块卡片
│   │   │   ├── NewsItem.tsx          # 单条资讯
│   │   │   ├── TabBar.tsx            # 底部 Tab 导航
│   │   │   └── HeatBadge.tsx         # 热度标签
│   │   ├── hooks/
│   │   │   └── useDailyData.ts       # 数据加载 Hook
│   │   └── styles/
│   │       └── index.css
│   ├── public/
│   │   ├── manifest.json
│   │   ├── sw.js                     # Service Worker
│   │   └── data/
│   │       └── daily.json            # 每日数据（Actions 自动更新）
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-05-31-ai-daily-hot-design.md
└── README.md
```

---

## 四、调度流程

```
北京时间 7:00 (UTC 23:00)
    │
    ▼
GitHub Actions 触发 daily-fetch.yml
    │
    ├── (1) 并行抓取 10+ 数据源                     ~60s
    │
    ├── (2) 合并 / 去重 / 规则过滤 / 关键词筛选       ~10s
    │        原始 200-500 条 → 过滤后 50-100 条
    │
    ├── (3) DeepSeek API 智能处理                   ~120s
    │        · 中英双语摘要
    │        · 分类校对 + 二级标签
    │        · 热度评分 (1-10)
    │        · 头条筛选 (3-5 条)
    │        · 学习建议标注
    │
    ├── (4) 生成 web/public/data/daily.json          ~5s
    │
    ├── (5) 触发 Vercel 自动部署                     ~60s
    │
    └── ✅ 7:40 前就绪，用户打开手机即看
```

### 时间轴
| 时间 (北京时间) | 动作 |
|------|------|
| 7:00 | GitHub Actions 触发 |
| 7:01 | 并行抓取完成 |
| 7:02 | 规则过滤完成 |
| 7:04 | DeepSeek 处理完成 |
| 7:05 | daily.json 生成 |
| 7:06 | Vercel 部署开始 |
| 7:40 前 | 简报就绪 |

**每次失败自动重试 1 次；仍失败则保留昨日数据兜底。**

---

## 五、数据格式

### daily.json

```json
{
  "date": "2026-05-31",
  "generated_at": "2026-05-31T07:00:00+08:00",
  "headlines": [
    {
      "title_cn": "OpenAI 发布 GPT-5 预览版",
      "title_en": "OpenAI Releases GPT-5 Preview",
      "summary_cn": "OpenAI 今日发布 GPT-5 预览版，在多模态推理和代码生成方面取得重大突破。新模型支持更长上下文窗口，并在多个基准测试中刷新纪录。",
      "summary_en": "OpenAI released GPT-5 preview today, making breakthroughs in multimodal reasoning and code generation...",
      "heat": 9.8,
      "tags": ["模型发布", "OpenAI", "GPT-5"],
      "url": "https://openai.com/blog/gpt-5-preview",
      "source": "OpenAI Blog",
      "source_icon": "openai",
      "student_note": "推荐阅读，了解前沿多模态架构和推理优化技术"
    }
  ],
  "sections": [
    {
      "id": "github",
      "title_cn": "GitHub AI 热门",
      "title_en": "GitHub AI Trending",
      "icon": "🐙",
      "items": [
        {
          "title_cn": "mini-deepseek — 在手机本地运行的小型 DeepSeek 模型",
          "title_en": "mini-deepseek: Run DeepSeek Locally on Mobile",
          "summary_cn": "该项目实现了在手机端本地运行量化版 DeepSeek 模型，推理速度达到实用水平。",
          "summary_en": "This project implements a quantized DeepSeek model that runs locally on mobile devices with practical inference speed.",
          "url": "https://github.com/xxx/mini-deepseek",
          "source": "GitHub Trending",
          "source_icon": "github",
          "meta": "⭐ 12,300 · Python · +2.1k today",
          "heat": 8.5,
          "tags": ["开源", "移动端", "模型量化"],
          "student_note": "适合了解模型量化和移动端部署"
        }
      ]
    }
  ]
}
```

---

## 六、前端设计

### 页面结构
- **顶部 Header**：日期 + "AI 每日热点" 标题 + 英文副标题
- **头条轮播**：3-5 条最重要资讯，自动轮播，点击跳转
- **板块卡片**：按 5 个板块分区，每区显示 Top 条目
- **底部 Tab Bar**：全部 / GitHub / 厂商 / 人物 / 新闻
- **条目标题 + 摘要 + 标签 + 热度标识 + 外链**

### 设计原则
- 🌙 暗色默认（早上看护眼）
- 📱 响应式，移动优先
- 👆 大点击区域，手指友好
- ⚡ 静态加载，即开即看
- 🏷️ 颜色标签区分来源和热度
- 💾 PWA 离线缓存

### PWA 特性
- 添加到主屏幕 → 全屏体验
- Service Worker 缓存今日数据
- 打开即最新（网络优先，离线回退缓存）

### 技术选型
- React + TypeScript
- Tailwind CSS
- Vite 构建
- Swiper.js（头条轮播）

---

## 七、DeepSeek API 使用策略

### Prompt 设计要点
- **批量处理**：一次 API 调用处理多条资讯，减少请求次数
- **结构化输出**：要求 JSON 格式返回，精确匹配 daily.json schema
- **角色设定**：作为资深 AI 编辑，面向大学生读者
- **双语要求**：中文摘要面向国内读者，英文摘要保留原文信息

### 处理批次
- 分板块依次处理，每个板块独立 Prompt
- 头条筛选在所有板块处理完后单独调用
- 每批 10-20 条，避免 token 超限

### 成本估算
| 阶段 | 输入 Tokens | 输出 Tokens | 成本 |
|------|------------|------------|------|
| 摘要生成 (~80条) | ~24K | ~16K | ¥0.05 |
| 分类+评分+头条 | ~10K | ~5K | ¥0.01 |
| **每日总计** | **~34K** | **~21K** | **≈ ¥0.06** |
| **每月总计** | | | **≈ ¥1.8** |

---

## 八、部署方案

| 组件 | 平台 | 成本 |
|------|------|------|
| 定时任务 + 采集 + AI 处理 | GitHub Actions | ¥0（公开仓库 2000 分钟/月） |
| 前端托管 | Vercel | ¥0（100GB 带宽） |
| AI 摘要 | DeepSeek API | ≈ ¥1.8/月 |
| 数据源 | 免费 RSS/API | ¥0 |
| **总计** | | **≈ ¥1.8/月** |

---

## 九、风险 & 应对

| 风险 | 应对 |
|------|------|
| GitHub Actions IP 被 ban | 优先用 RSS/API，少用网页爬虫；必要时加延迟和 UA 伪装 |
| 数据源变更/失效 | 每个数据源独立脚本，单点故障不影响全局 |
| 抓取失败 | Actions 失败自动重试 1 次，保留昨日数据兜底 |
| DeepSeek API 超时/限流 | 分批次调用，单次失败仅影响该板块，不阻塞全局 |
| GitHub Trending 无官方 API | 使用第三方 mirror API 或 RSS 桥接 |
| Vercel 部署失败 | GitHub Actions 直接输出到 Pages 作为备份 |

---

## 十、边界定义

**v1 不做**：
- 用户系统 / 收藏 / 评论（纯浏览）
- 历史搜索 / 历史归档
- 实时推送通知
- X（Twitter）直接 API 接入（通过新闻/博客间接跟踪）

**v1 做**：
- 稳定的每日自动抓取 + AI 摘要
- 5 个板块的双语深度简报
- 头条轮播 + 热度评分
- 手机友好的 PWA 浏览体验
- 零运维、零服务器成本

**v2 可扩展**：
- 历史归档（保留过去 7 天数据）
- 关键词搜索
- 推送通知（Web Push API）
- 用户偏好定制板块
