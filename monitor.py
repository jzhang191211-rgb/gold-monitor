import time
import datetime
import os
from data_fetcher import GoldFetcher
from notifier import Notifier

# 配置
CHECK_INTERVAL = 60  # 检查间隔（秒）
PRICE_CHANGE_THRESHOLD = 1.0  # 价格波动阈值（%）
SECONDARY_CHANGE_THRESHOLD = 0.5 # 二次报警阈值（%）：在已报警基础上，价格再次波动多少才触发新报警
MA20_DEVIATION_THRESHOLD = 5.0  # 均线偏离阈值（%）

def main():
    print("启动黄金监控服务...")
    
    # 初始化
    gold_fetcher = GoldFetcher()
    notifier = Notifier()
    
    # 记录上一次通知时的价格，用于计算波动
    last_notify_price = 0
    last_notify_time = 0
    
    # 记录上一次获取的数据时间戳，用于判断数据是否更新
    last_data_timestamp = None
    
    while True:
        try:
            # 获取当前时间
            now = datetime.datetime.now()
            
            # 周末休市检测 (周六=5, 周日=6)
            # 上海黄金交易所周末休市，周五夜盘结束后直到周一早盘
            # 简单处理：如果是周六或周日，直接跳过监控
            if now.weekday() >= 5:
                print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 周末休市期间，暂停监控")
                time.sleep(3600) # 休市期间每小时检查一次时间即可
                continue
            
            # 获取黄金数据
            gold_data = gold_fetcher.get_price()
            
            if gold_data:
                # 数据更新检测
                # 接口返回的数据中通常包含时间戳或时间字符串，这里我们假设gold_data['time']是数据时间
                # 如果数据时间没有变化，说明市场没有新数据（可能是休市或暂停交易），不应重复报警
                current_data_timestamp = gold_data.get('time')
                
                # 如果是第一次获取，或者数据时间戳发生了变化，才进行处理
                if last_data_timestamp is None or current_data_timestamp != last_data_timestamp:
                    last_data_timestamp = current_data_timestamp
                    
                    current_price = gold_data['price']
                    change_percent = gold_data['change_percent']
                    
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 当前金价: {current_price}, 涨跌幅: {change_percent}%")
                    
                    # 1. 涨跌幅报警
                    # 逻辑优化：
                    # 1. 基础条件：涨跌幅绝对值 >= 1%
                    # 2. 触发条件（满足其一即可）：
                    #    a. 首次报警（last_notify_price 为 0）
                    #    b. 价格相比上次报警时的价格，波动幅度超过 0.5% (SECONDARY_CHANGE_THRESHOLD)
                    #    c. 距离上次报警超过 4 小时（作为兜底，避免长时间不提醒）
                    
                    if abs(change_percent) >= PRICE_CHANGE_THRESHOLD:
                        should_notify = False
                        reason = ""
                        
                        if last_notify_price == 0:
                            should_notify = True
                            reason = "首次触发阈值"
                        else:
                            # 计算相比上次通知时的价格变化幅度
                            price_diff_percent = abs((current_price - last_notify_price) / last_notify_price * 100)
                            
                            if price_diff_percent >= SECONDARY_CHANGE_THRESHOLD:
                                should_notify = True
                                reason = f"价格再次波动 {price_diff_percent:.2f}%"
                            elif time.time() - last_notify_time > 14400: # 4小时兜底
                                should_notify = True
                                reason = "距离上次通知已过4小时"
                        
                        if should_notify:
                            title = f"黄金价格波动提醒: {change_percent}%"
                            content = f"当前金价: {current_price}\n涨跌幅: {change_percent}%\n触发原因: {reason}\n时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
                            notifier.send(title, content)
                            last_notify_price = current_price
                            last_notify_time = time.time()
                            print(f"已发送涨跌幅通知 ({reason})")
                        else:
                            print(f"满足阈值但未达二次波动条件 (上次: {last_notify_price}, 当前: {current_price})")
                else:
                    # 数据未更新，跳过
                    pass
                
                # 2. 均线偏离报警
                # 每天只检查一次，例如在收盘后或特定时间
                # 这里简化为每隔一段时间检查一次
                if now.minute == 0 and now.second < 10: # 每小时整点检查
                    ma20 = gold_fetcher.get_ma20()
                    if ma20:
                        deviation = (current_price - ma20) / ma20 * 100
                        if abs(deviation) >= MA20_DEVIATION_THRESHOLD:
                            title = f"黄金价格偏离20日均线提醒: {deviation:.2f}%"
                            content = f"当前金价: {current_price}\n20日均线: {ma20:.2f}\n偏离度: {deviation:.2f}%\n时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
                            notifier.send(title, content)
                            print("已发送均线偏离通知")
            
            else:
                print("获取金价失败")
                
        except Exception as e:
            print(f"监控循环发生错误: {e}")
            
        # 等待下一次检查
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
