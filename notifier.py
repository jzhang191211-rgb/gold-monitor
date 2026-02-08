import requests
import os

class Notifier:
    def __init__(self):
        # 从环境变量获取SendKey，支持多个Key用逗号分隔
        self.send_keys = os.environ.get("SERVERCHAN_SENDKEY", "").split(",")
        # 过滤空字符串
        self.send_keys = [key.strip() for key in self.send_keys if key.strip()]
        
        if not self.send_keys:
            print("警告: 未设置 SERVERCHAN_SENDKEY 环境变量")

    def send(self, title, content):
        if not self.send_keys:
            print("未配置SendKey，无法发送通知")
            return
            
        for key in self.send_keys:
            try:
                url = f"https://sctapi.ftqq.com/{key}.send"
                data = {
                    "title": title,
                    "desp": content
                }
                response = requests.post(url, data=data)
                result = response.json()
                if result.get("code") == 0:
                    print(f"通知发送成功 (Key: {key[:5]}...)")
                else:
                    print(f"通知发送失败 (Key: {key[:5]}...): {result.get('message')}")
            except Exception as e:
                print(f"发送通知时发生异常 (Key: {key[:5]}...): {e}")
