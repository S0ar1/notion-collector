"""Notion 客户端模块 - 封装 Notion API 调用"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from config import Config


class NotionCollector:
    """Notion 数据收集器"""

    def __init__(self):
        """初始化 Notion 客户端"""
        Config.validate()
        self.token = Config.NOTION_TOKEN
        self.daily_db_id = Config.DAILY_LOG_DATABASE_ID.replace("-", "")
        self.weekly_db_id = Config.WEEKLY_LOG_DATABASE_ID.replace("-", "")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def _query_database(self, database_id: str) -> List[Dict[str, Any]]:
        """
        查询数据库（获取所有数据）

        Args:
            database_id: 数据库 ID（不含连字符）

        Returns:
            数据库条目列表
        """
        results = []
        has_more = True
        start_cursor = None

        while has_more:
            body = {}
            if start_cursor:
                body["start_cursor"] = start_cursor

            response = requests.post(
                f"{self.base_url}/databases/{database_id}/query",
                headers=self.headers,
                json=body,
            )
            response.raise_for_status()
            data = response.json()

            results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")

        return results

    def get_daily_logs(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        获取过去 N 天的 Daily Log

        Args:
            days: 获取过去几天的数据

        Returns:
            Daily Log 条目列表
        """
        results = self._query_database(self.daily_db_id)

        # 解析并过滤数据
        parsed_logs = []
        cutoff_date = datetime.now() - timedelta(days=days)

        for item in results:
            parsed = self._parse_daily_log(item)
            if parsed:
                # 检查日期是否在范围内
                if parsed.get("date"):
                    try:
                        item_date = datetime.fromisoformat(parsed["date"].replace("Z", "+00:00"))
                        if item_date >= cutoff_date:
                            parsed_logs.append(parsed)
                    except (ValueError, TypeError):
                        # 如果日期解析失败，仍然包含该条目
                        parsed_logs.append(parsed)
                else:
                    parsed_logs.append(parsed)

        # 按日期排序
        parsed_logs.sort(key=lambda x: x.get("date", ""), reverse=True)
        return parsed_logs

    def get_weekly_logs(self, weeks: int = 4) -> List[Dict[str, Any]]:
        """
        获取过去 N 周的 Weekly Log

        Args:
            weeks: 获取过去几周的数据

        Returns:
            Weekly Log 条目列表
        """
        results = self._query_database(self.weekly_db_id)

        # 解析并过滤数据
        parsed_logs = []
        cutoff_date = datetime.now() - timedelta(weeks=weeks)

        for item in results:
            parsed = self._parse_weekly_log(item)
            if parsed:
                # 检查日期是否在范围内
                if parsed.get("created_time"):
                    try:
                        item_date = datetime.fromisoformat(parsed["created_time"].replace("Z", "+00:00"))
                        if item_date >= cutoff_date:
                            parsed_logs.append(parsed)
                    except (ValueError, TypeError):
                        parsed_logs.append(parsed)
                else:
                    parsed_logs.append(parsed)

        # 按创建时间排序
        parsed_logs.sort(key=lambda x: x.get("created_time", ""), reverse=True)
        return parsed_logs

    def _parse_daily_log(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析 Daily Log 条目

        Args:
            item: Notion API 返回的条目

        Returns:
            解析后的数据字典
        """
        properties = item.get("properties", {})
        result = {
            "id": item.get("id"),
            "url": item.get("url"),
            "created_time": item.get("created_time"),
            "last_edited_time": item.get("last_edited_time"),
        }

        # 解析名称 (title, 中文名称)
        name_prop = properties.get("名称", {})
        if not name_prop:
            name_prop = properties.get("Name", {})
        if name_prop.get("type") == "title":
            title_data = name_prop.get("title", [])
            if title_data:
                result["name"] = title_data[0].get("plain_text", "")

        # 解析 Logdate (date)
        date_prop = properties.get("Logdate", {})
        if not date_prop:
            date_prop = properties.get("Date", {})
        if date_prop.get("type") == "date":
            date_data = date_prop.get("date", {})
            if date_data:
                result["date"] = date_data.get("start")

        # 解析 Week Task (rollup)
        week_task_prop = properties.get("Week Task", {})
        if week_task_prop and week_task_prop.get("type") == "rollup":
            rollup_data = week_task_prop.get("rollup", {})
            if rollup_data:
                rollup_prop = rollup_data.get("array")
                if rollup_prop and rollup_prop.get("type") == "text":
                    result["week_task"] = rollup_prop.get("plain_text", "")

        # 解析 Weekly Log (relation)
        relation_prop = properties.get("Weekly Log", {})
        if relation_prop and relation_prop.get("type") == "relation":
            relations = relation_prop.get("relation", [])
            result["weekly_log_ids"] = [r.get("id") for r in relations]

        return result if result.get("name") else None

    def _parse_weekly_log(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析 Weekly Log 条目

        Args:
            item: Notion API 返回的条目

        Returns:
            解析后的数据字典
        """
        properties = item.get("properties", {})
        result = {
            "id": item.get("id"),
            "url": item.get("url"),
            "created_time": item.get("created_time"),
            "last_edited_time": item.get("last_edited_time"),
        }

        # 解析上周总结 (title)
        summary_prop = properties.get("上周总结", {})
        if summary_prop.get("type") == "title":
            title_data = summary_prop.get("title", [])
            if title_data:
                result["last_week_summary"] = title_data[0].get("plain_text", "")

        # 解析本周任务 (text)
        task_prop = properties.get("本周任务", {})
        if task_prop.get("type") == "text":
            text_data = task_prop.get("text", [])
            if text_data:
                result["this_week_tasks"] = text_data[0].get("plain_text", "")

        # 解析 Date (created_time)
        date_prop = properties.get("Date", {})
        if date_prop.get("type") == "created_time":
            result["date"] = date_prop.get("created_time", item.get("created_time"))

        return result if result.get("last_week_summary") or result.get("this_week_tasks") else None
