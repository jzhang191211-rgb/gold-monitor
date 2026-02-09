import requests
import os

class Notifier:
    def __init__(self):
        # 尝试从多个环境变量获取SendKey
        keys_str = os.environ.get("SERVERCHAN_SENDKEY", "")
        if not keys_str:
            keys_str = os.environ.get("SENDKEY", "")
            
        # 如果环境变量未设置，使用硬编码的默认Key
        if not keys_str:
            print("提示: 未检测到环境变量，使用默认硬编码 Key")
            keys_str = "SCT307811T6s55AozLghm2HysoCig4FhiG,SCT308084Tp3AGrj8PWub1z0I16sWiYSb6"
            
        # 支持多个Key用逗号分隔
        self.send_keys = keys_str.split(",")
        # 过滤空字符串
        self.send_keys = [key.strip() for key in self.send_keys if key.strip()]
        
        if not self.send_keys:
            print("警告: 未能获取到任何有效的 SendKey")
        else:
            print(f"成功加载 {len(self.send_keys)} 个 SendKey")

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
