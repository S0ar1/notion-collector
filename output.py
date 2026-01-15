"""输出模块 - 将数据输出为 JSON 格式"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from config import Config


class OutputManager:
    """输出管理器 - 处理数据输出"""

    def __init__(self):
        """初始化输出管理器"""
        self.output_dir = Config.OUTPUT_DIR
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_daily_logs(self, data: Dict[str, Any], date: datetime = None) -> str:
        """
        保存 Daily Log 数据为 JSON

        Args:
            data: 处理后的 Daily Log 数据
            date: 数据日期（默认为当前日期）

        Returns:
            输出文件路径
        """
        if date is None:
            date = datetime.now()

        filename = f"daily_{date.strftime('%Y-%m-%d')}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

    def save_weekly_logs(self, data: Dict[str, Any], date: datetime = None) -> str:
        """
        保存 Weekly Log 数据为 JSON

        Args:
            data: 处理后的 Weekly Log 数据
            date: 数据日期（默认为当前日期）

        Returns:
            输出文件路径
        """
        if date is None:
            date = datetime.now()

        filename = f"weekly_{date.strftime('%Y-%m-%d')}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

    def save_combined_report(
        self, daily_data: Dict[str, Any], weekly_data: Dict[str, Any], date: datetime = None
    ) -> str:
        """
        保存综合报告（包含 Daily 和 Weekly 数据）

        Args:
            daily_data: 处理后的 Daily Log 数据
            weekly_data: 处理后的 Weekly Log 数据
            date: 数据日期（默认为当前日期）

        Returns:
            输出文件路径
        """
        if date is None:
            date = datetime.now()

        combined = {
            "daily_logs": daily_data,
            "weekly_logs": weekly_data,
            "report_metadata": {
                "generated_at": date.isoformat(),
                "report_type": "combined",
            },
        }

        filename = f"report_{date.strftime('%Y-%m-%d')}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(combined, f, ensure_ascii=False, indent=2)

        return filepath

    def get_output_files(self) -> list[str]:
        """
        获取输出目录中的所有文件

        Returns:
            文件路径列表
        """
        if not os.path.exists(self.output_dir):
            return []

        files = [
            os.path.join(self.output_dir, f)
            for f in os.listdir(self.output_dir)
            if f.endswith(".json")
        ]
        return sorted(files, reverse=True)
