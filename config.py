"""配置模块 - 读取环境变量和配置"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置类"""

    # Notion 配置
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    DAILY_LOG_DATABASE_ID = os.getenv("NOTION_DAILY_LOG_DATABASE_ID")
    WEEKLY_LOG_DATABASE_ID = os.getenv("NOTION_WEEKLY_LOG_DATABASE_ID")

    # 输出配置
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

    @classmethod
    def validate(cls) -> bool:
        """验证必需的配置项是否存在"""
        required = [
            ("NOTION_TOKEN", cls.NOTION_TOKEN),
            ("NOTION_DAILY_LOG_DATABASE_ID", cls.DAILY_LOG_DATABASE_ID),
            ("NOTION_WEEKLY_LOG_DATABASE_ID", cls.WEEKLY_LOG_DATABASE_ID),
        ]
        missing = [name for name, value in required if not value]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        return True
