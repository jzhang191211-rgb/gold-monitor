import requests
import time
from data_fetcher import GoldFetcher

class AlertManager:
    def __init__(self, serverchan_key):
        self.key = serverchan_key
        self.last_alert_time = 0
        self.alert_interval = 3600  # 相同类型的提醒间隔1小时
        self.gold_fetcher = GoldFetcher()
        
        # 提醒阈值配置
        self.ma_deviation_threshold = 0.05  # 均线偏离阈值 5%

    def send_wechat(self, title, content):
        """发送微信通知"""
        if not self.key:
            print("未配置Server酱Key，跳过发送")
            return
            
        url = f"https://sctapi.ftqq.com/{self.key}.send"
        data = {
            "title": title,
            "desp": content
        }
        try:
            response = requests.post(url, data=data)
            print(f"通知发送结果: {response.text}")
        except Exception as e:
            print(f"发送通知失败: {e}")

    def check_gold_alerts(self, current_price, change_percent):
        """检查黄金相关提醒"""
        current_time = time.time()
        
        # 1. 涨跌幅提醒
        if abs(change_percent) >= 1.0:
            if current_time - self.last_alert_time > self.alert_interval:
                direction = "上涨" if change_percent > 0 else "下跌"
                title = f"⚠️ 黄金{direction}预警: {change_percent}%"
                content = f"当前金价: {current_price}\n涨跌幅: {change_percent}%"
                self.send_wechat(title, content)
                self.last_alert_time = current_time
        
        # 2. 均线偏离提醒
        ma20 = self.gold_fetcher.get_ma20()
        if ma20:
            deviation = (current_price - ma20) / ma20
            if abs(deviation) > self.ma_deviation_threshold:
                # 这里可以设置独立的冷却时间，为简化暂用同一个
                if current_time - self.last_alert_time > self.alert_interval:
                    type_str = "高于" if deviation > 0 else "低于"
                    risk_str = "回调风险" if deviation > 0 else "反弹机会"
                    title = f"⚠️ 均线偏离预警: {deviation*100:.2f}%"
                    content = f"当前金价: {current_price}\n20日均价: {ma20:.2f}\n偏离度: {deviation*100:.2f}% ({type_str})\n提示: 可能存在{risk_str}"
                    self.send_wechat(title, content)
                    self.last_alert_time = current_time
