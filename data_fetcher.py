import requests
import json
import time
import re
import random

class GoldFetcher:
    def __init__(self):
        # 新浪财经国际现货黄金（伦敦金）接口
        self.url = "https://hq.sinajs.cn/list=hf_XAU"
        
        # 随机 User-Agent 列表
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        ]
    
    def get_price(self):
        try:
            headers = {
                "User-Agent": random.choice(self.user_agents),
                "Referer": "https://finance.sina.com.cn", # 新浪接口必须带 Referer
                "Accept": "*/*",
                "Connection": "keep-alive"
            }
            
            # 增加随机时间戳防止缓存
            # 新浪接口的URL中如果有参数，应该用逗号分隔，或者直接不加时间戳
            # 为了稳定，我们直接使用原始URL，不加时间戳，因为新浪接口通常不会缓存
            url = self.url
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # 新浪接口返回的是 GBK 编码的 JS 代码
                text = response.content.decode('gbk')
                
                # 解析返回的字符串: var hq_str_hf_XAU="最新价,昨收,开盘,最高,最低,时间,日期,名称,...";
                match = re.search(r'="([^"]+)"', text)
                if match:
                    data_str = match.group(1)
                    if not data_str:
                        return None
                        
                    fields = data_str.split(',')
                    if len(fields) >= 14:
                        current_price = float(fields[0])
                        # 新浪期货接口字段：0最新价, 1?, 2买价, 3卖价, 4最高, 5最低, 6时间, 7昨收, 8开盘, 9持仓, 10?, 11?, 12日期, 13名称
                        prev_close = float(fields[7]) # 昨收盘价
                        
                        # 计算涨跌幅
                        change = current_price - prev_close
                        change_percent = (change / prev_close) * 100 if prev_close > 0 else 0.0
                        
                        return {
                            "name": "伦敦金(XAU)",
                            "price": round(current_price, 2),
                            "change": round(change, 2),
                            "change_percent": round(change_percent, 2),
                            "high": float(fields[4]),
                            "low": float(fields[5]),
                            "time": f"{fields[12]} {fields[6]}" # 日期 + 时间
                        }
                    else:
                        print(f"字段数量不足: {len(fields)}")
                else:
                    print(f"正则匹配失败: {text}")
            else:
                print(f"请求失败，状态码: {response.status_code}")
            return None
        except Exception as e:
            print(f"获取黄金数据失败: {e}")
            return None

    def get_ma20(self):
        """获取20日均价 - 暂不实现，返回当前价格避免报错"""
        # 由于更换了数据源，获取历史K线计算MA20比较复杂，这里暂时返回None
        # 监控脚本中如果获取不到MA20会自动跳过该项报警
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
