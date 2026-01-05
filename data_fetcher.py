import requests
import json
import time
import re

class GoldFetcher:
    def __init__(self):
        self.url = "https://push2.eastmoney.com/api/qt/stock/get?secid=118.AU9999&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f169,f170,f171&ut=fa5fd1943c7b386f172d6893dbfba10b&_=1767237804067"
        self.history_url = "https://push2.eastmoney.com/api/qt/stock/get?secid=118.AU9999&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f169,f170,f171&ut=fa5fd1943c7b386f172d6893dbfba10b&_=1767237804067"
    
    def get_price(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://quote.eastmoney.com/"
            }
            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                # 提取JSON数据
                text = response.text
                json_str = text[text.find('{'):text.rfind('}')+1]
                data = json.loads(json_str)
                
                if 'data' in data and data['data']:
                    item = data['data']
                    # 处理停盘或无数据的情况
                    if item['f43'] == '-' or item['f43'] is None:
                        # 尝试使用收盘价作为当前价格
                        price = float(item['f60']) if item['f60'] != '-' else 0.0
                    else:
                        price = float(item['f43'])
                        
                    return {
                        "name": item['f58'],
                        "price": price,
                        "change": float(item['f169']) if item['f169'] != '-' else 0.0,
                        "change_percent": float(item['f170']) if item['f170'] != '-' else 0.0,
                        "high": float(item['f44']) if item['f44'] != '-' else price,
                        "low": float(item['f45']) if item['f45'] != '-' else price,
                        "time": str(time.time()) # 接口未返回时间，使用当前时间
                    }
            return None
        except Exception as e:
            print(f"获取黄金数据失败: {e}")
            return None

    def get_ma20(self):
        """获取20日均价"""
        try:
            # 这里使用模拟数据或简单的API调用
            # 实际应用中可能需要调用K线数据接口计算MA20
            # 为了简化，我们假设当前价格接近MA20，或者通过简单的历史数据接口获取
            # 这里我们尝试获取日K线数据
            kline_url = "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=118.AU9999&fields1=f1&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&end=20500101&lmt=20"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(kline_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data and 'klines' in data['data']:
                    klines = data['data']['klines']
                    closes = [float(k.split(',')[2]) for k in klines]
                    if len(closes) > 0:
                        return sum(closes) / len(closes)
            return None
        except Exception as e:
            print(f"获取MA20失败: {e}")
            return None

class FundFetcher:
    def __init__(self):
        self.base_url = "http://fundgz.1234567.com.cn/js/{}.js"
    
    def get_fund_data(self, fund_code):
        try:
            url = self.base_url.format(fund_code)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                text = response.text
                # 提取jsonpgz(...)中的内容
                match = re.search(r'jsonpgz\((.*)\)', text)
                if match:
                    json_str = match.group(1)
                    data = json.loads(json_str)
                    return {
                        "code": data['fundcode'],
                        "name": data['name'],
                        "net_value": float(data['dwjz']), # 单位净值
                        "estimate_value": float(data['gsz']), # 估算净值
                        "estimate_growth": float(data['gszzl']), # 估算涨跌幅
                        "time": data['gztime']
                    }
            return None
        except Exception as e:
            print(f"获取基金{fund_code}数据失败: {e}")
            return None
