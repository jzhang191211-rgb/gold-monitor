import os

# 从环境变量获取Server酱Key，如果没有则使用空字符串
SERVERCHAN_KEY = os.environ.get("SERVERCHAN_KEY", "")

# 黄金持仓配置
GOLD_CONFIG = {
    "holdings": {
        "shares": 20,
        "cost_price": 500.00
    }
}

# 基金持仓配置
FUND_CONFIG = {
    "funds": {
        "000001": {
            "name": "华夏成长混合",
            "shares": 2000,
            "cost_price": 1.50
        }
    }
}

# 提醒配置
ALERT_CONFIG = {
    "gold_change_threshold": 1.0,  # 金价波动提醒阈值 (%)
    "target_price_high": 600,      # 目标高价
    "target_price_low": 400        # 目标低价
}
