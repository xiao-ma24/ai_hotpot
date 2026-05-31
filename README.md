# 🤖 AI 每日热点 (AI Daily Hotpot)

每天早上 7:40，自动收集全球 AI 热点，生成中英双语简报。
手机打开即看 → [ai-hotpot.vercel.app](https://ai-hotpot.vercel.app)

## 板块
- 🐙 GitHub AI 热门项目
- 🧠 大模型厂商动态
- 👤 AI 科技人物
- 📰 AI 行业新闻
- 📚 学术前沿

## 技术栈
Python 采集 → DeepSeek API 处理 → GitHub Actions 调度 → Vercel 托管 PWA

## 本地运行
```bash
pip install -r requirements.txt
python crawler/fetch_all.py
```
