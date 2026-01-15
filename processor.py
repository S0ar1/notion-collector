"""数据处理模块 - 整理和归纳数据"""

from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


class DataProcessor:
    """数据处理器 - 整理和归纳 Notion 数据"""

    def __init__(self):
        """初始化数据处理器"""
        pass

    def process_daily_logs(self, raw_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        处理 Daily Log 数据，进行整理归纳

        Args:
            raw_logs: 原始 Daily Log 数据

        Returns:
            处理后的数据字典
        """
        result = {
            "summary": self._generate_daily_summary(raw_logs),
            "by_date": self._group_by_date(raw_logs),
            "relationships": self._analyze_relationships(raw_logs),
            "metadata": {
                "total_count": len(raw_logs),
                "date_range": self._get_date_range(raw_logs),
                "generated_at": datetime.now().isoformat(),
            },
        }
        return result

    def process_weekly_logs(self, raw_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        处理 Weekly Log 数据，进行整理归纳

        Args:
            raw_logs: 原始 Weekly Log 数据

        Returns:
            处理后的数据字典
        """
        result = {
            "summaries": self._extract_summaries(raw_logs),
            "tasks": self._extract_tasks(raw_logs),
            "by_week": self._group_by_week(raw_logs),
            "metadata": {
                "total_count": len(raw_logs),
                "date_range": self._get_weekly_date_range(raw_logs),
                "generated_at": datetime.now().isoformat(),
            },
        }
        return result

    def _generate_daily_summary(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成 Daily Log 摘要统计"""
        summary = {
            "total_entries": len(logs),
            "concepts_count": 0,
            "strategies_count": 0,
            "experiments_count": 0,
            "insights_count": 0,
            "codebase_count": 0,
        }

        for log in logs:
            for field in ["concepts", "strategies", "experiments", "insights", "codebase"]:
                if log.get(field):
                    summary[f"{field}_count"] += len(log[field])

        return summary

    def _group_by_date(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """按日期分组 Daily Log"""
        grouped = defaultdict(list)
        for log in logs:
            date = log.get("date", "unknown")
            grouped[date].append(log)

        # 转换为列表并按日期排序
        result = [
            {"date": date, "entries": entries, "count": len(entries)}
            for date, entries in grouped.items()
        ]
        result.sort(key=lambda x: x["date"], reverse=True)
        return result

    def _analyze_relationships(self, logs: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """分析关联关系"""
        relationships = {
            "concepts": set(),
            "strategies": set(),
            "experiments": set(),
            "insights": set(),
            "codebase": set(),
        }

        for log in logs:
            for field in relationships.keys():
                if log.get(field):
                    relationships[field].update(log[field])

        # 转换为列表
        return {k: list(v) for k, v in relationships.items()}

    def _get_date_range(self, logs: List[Dict[str, Any]]) -> Dict[str, str]:
        """获取日期范围"""
        dates = [log.get("date") for log in logs if log.get("date")]
        if not dates:
            return {"start": None, "end": None}
        return {"start": min(dates), "end": max(dates)}

    def _extract_summaries(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """提取周总结"""
        summaries = []
        for log in logs:
            if log.get("last_week_summary"):
                summaries.append({
                    "id": log.get("id"),
                    "date": log.get("date"),
                    "created_time": log.get("created_time"),
                    "summary": log.get("last_week_summary"),
                })
        summaries.sort(key=lambda x: x.get("date", ""), reverse=True)
        return summaries

    def _extract_tasks(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """提取本周任务"""
        tasks = []
        for log in logs:
            if log.get("this_week_tasks"):
                tasks.append({
                    "id": log.get("id"),
                    "date": log.get("date"),
                    "created_time": log.get("created_time"),
                    "tasks": log.get("this_week_tasks"),
                })
        tasks.sort(key=lambda x: x.get("date", ""), reverse=True)
        return tasks

    def _group_by_week(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """按周分组 Weekly Log"""
        # 按创建时间分组
        grouped = defaultdict(list)
        for log in logs:
            # 使用创建时间的年-周作为分组键
            created_time = log.get("created_time", "")
            if created_time:
                try:
                    dt = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
                    week_key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
                    grouped[week_key].append(log)
                except (ValueError, TypeError):
                    grouped["unknown"].append(log)
            else:
                grouped["unknown"].append(log)

        # 转换为列表并按周排序
        result = [
            {"week": week, "entries": entries, "count": len(entries)}
            for week, entries in grouped.items()
        ]
        result.sort(key=lambda x: x["week"], reverse=True)
        return result

    def _get_weekly_date_range(self, logs: List[Dict[str, Any]]) -> Dict[str, str]:
        """获取周日志日期范围"""
        dates = [log.get("created_time") for log in logs if log.get("created_time")]
        if not dates:
            return {"start": None, "end": None}
        return {"start": min(dates), "end": max(dates)}
