# Notion Collector

每周日定期拉取 Notion 中指定数据（每日计划及周计划），并做数据整理归纳。

## 功能特性

- 定时拉取 Notion 数据库中的 Daily Log 和 Weekly Log
- 数据整理归纳为 JSON 格式输出
- 支持 GitHub Actions 定时执行（每周日）
- 支持手动触发数据拉取

## 数据库结构

### Daily Log
- Name: 标题
- Date: 日期
- Concepts: 关联概念
- Strategies: 关联策略
- Experiments: 关联实验
- Insights: 关联洞察
- Codebase: 关联代码库

### Weekly Log
- 上周总结: 标题
- 本周任务: 文本内容
- Date: 创建时间

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 为 `.env`
2. 填入 Notion API Token

## 使用

### 手动运行

```bash
python main.py
```

### GitHub Actions 定时运行

Push 到 GitHub 后，每周日 00:00 自动运行。

手动触发：在 GitHub Actions 页面选择 "Run workflow"

## 输出

数据输出到 `output/` 目录，按日期命名：
- `daily_YYYY-MM-DD.json`
- `weekly_YYYY-MM-DD.json`
