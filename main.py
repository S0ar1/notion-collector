"""主程序 - Notion Collector 入口点"""

import sys
from datetime import datetime
from notion_client import APIResponseError

from config import Config
from notion_client import NotionCollector
from processor import DataProcessor
from output import OutputManager


def main():
    """主函数"""
    try:
        print(f"[{datetime.now().isoformat()}] Notion Collector 开始运行...")

        # 初始化组件
        collector = NotionCollector()
        processor = DataProcessor()
        output_manager = OutputManager()

        # 拉取数据
        print("正在拉取 Daily Log 数据...")
        daily_logs = collector.get_daily_logs(days=7)
        print(f"已获取 {len(daily_logs)} 条 Daily Log")

        print("正在拉取 Weekly Log 数据...")
        weekly_logs = collector.get_weekly_logs(weeks=4)
        print(f"已获取 {len(weekly_logs)} 条 Weekly Log")

        # 处理数据
        print("正在处理数据...")
        daily_processed = processor.process_daily_logs(daily_logs)
        weekly_processed = processor.process_weekly_logs(weekly_logs)

        # 输出数据
        print("正在保存数据...")
        current_time = datetime.now()

        daily_file = output_manager.save_daily_logs(daily_processed, current_time)
        print(f"Daily Log 已保存到: {daily_file}")

        weekly_file = output_manager.save_weekly_logs(weekly_processed, current_time)
        print(f"Weekly Log 已保存到: {weekly_file}")

        combined_file = output_manager.save_combined_report(daily_processed, weekly_processed, current_time)
        print(f"综合报告已保存到: {combined_file}")

        print(f"[{datetime.now().isoformat()}] 数据收集完成！")
        return 0

    except ValueError as e:
        print(f"配置错误: {e}", file=sys.stderr)
        print("请检查 .env 文件中的配置是否正确。")
        return 1

    except APIResponseError as e:
        print(f"Notion API 错误: {e}", file=sys.stderr)
        print(f"错误详情: {e.body}")
        return 1

    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
