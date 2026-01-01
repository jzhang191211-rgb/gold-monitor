class ProfitCalculator:
    @staticmethod
    def calculate_gold_profit(holdings, current_price):
        """
        计算黄金收益
        holdings: {"shares": 10, "cost_price": 450}
        current_price: 480
        """
        shares = holdings['shares']
        cost_price = holdings['cost_price']
        
        market_value = shares * current_price
        cost_value = shares * cost_price
        profit = market_value - cost_value
        profit_percent = (profit / cost_value) * 100 if cost_value > 0 else 0
        
        return {
            "market_value": round(market_value, 2),
            "cost_value": round(cost_value, 2),
            "profit": round(profit, 2),
            "profit_percent": round(profit_percent, 2)
        }

    @staticmethod
    def calculate_fund_profit(holdings, current_net_value):
        """
        计算基金收益
        holdings: {"shares": 1000, "cost_price": 1.2}
        current_net_value: 1.25
        """
        shares = holdings['shares']
        cost_price = holdings['cost_price']
        
        market_value = shares * current_net_value
        cost_value = shares * cost_price
        profit = market_value - cost_value
        profit_percent = (profit / cost_value) * 100 if cost_value > 0 else 0
        
        return {
            "market_value": round(market_value, 2),
            "cost_value": round(cost_value, 2),
            "profit": round(profit, 2),
            "profit_percent": round(profit_percent, 2)
        }
