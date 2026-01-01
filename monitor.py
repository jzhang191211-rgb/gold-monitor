import time
import schedule
from data_fetcher import GoldFetcher, FundFetcher
from profit_calculator import ProfitCalculator
from notifier import AlertManager
from config import GOLD_CONFIG, FUND_CONFIG, ALERT_CONFIG, SERVERCHAN_KEY

# 默认配置（如果config.py中没有定义）
DEFAULT_CONFIG = {
    "gold": {
        "holdings": {
            "shares": 20,
            "cost_price": 500.00
        }
    },
    "funds": {
        "000001": {
            "name": "华夏成长混合",
            "shares": 2000,
            "cost_price": 1.50
        }
    }
}

# 初始化AlertManager（只需初始化一次）
# SERVERCHAN_KEY 现在可以是一个包含逗号的字符串，例如 "Key1,Key2"
alert_manager = AlertManager(SERVERCHAN_KEY)

def job():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始执行监控任务...")
    
    # 1. 获取数据
    gold_fetcher = GoldFetcher()
    fund_fetcher = FundFetcher()
    
    gold_data = gold_fetcher.get_price()
    if not gold_data:
        print("获取黄金数据失败")
        return

    print(f"当前金价: {gold_data['price']} (涨跌幅: {gold_data['change_percent']}%)")
    
    # 2. 检查提醒
    # 检查金价波动
    alert_manager.check_gold_alerts(gold_data['price'], gold_data['change_percent'])
    
    print("监控任务执行完毕")

if __name__ == "__main__":
    print("黄金与基金监控服务已启动 (Railway版 - 多用户推送)")
    print("正在等待定时任务执行...")
    
    # 立即执行一次
    job()
    
    # 每5分钟执行一次
    schedule.every(5).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
