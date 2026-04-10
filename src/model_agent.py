"""
Model-based agent that maintains internal state and estimates trends
Based on TP_agent from page 5
"""

from src.agents import Agent


class ModelBasedPaperAgent(Agent):

    def __init__(self):
        self.spent = 0
        self.buy_history = []
        self.avg_price = None
        self.last_price = None
        self.instock = None
        self.price_history = []

    def select_action(self, percept):

        self.last_price = percept['price']
        self.instock = percept['instock']

        # Exponential smoothing (α = 0.05)
        if self.avg_price is None:
            self.avg_price = self.last_price
        else:
            self.avg_price = self.avg_price + (
                self.last_price - self.avg_price
            ) * 0.05

        self.price_history.append(self.last_price)

        # Decision logic
        if self.last_price < 0.9 * self.avg_price and self.instock < 60:
            tobuy = 48
        elif self.instock < 12:
            tobuy = 12
        else:
            tobuy = 0

        self.spent += tobuy * self.last_price
        self.buy_history.append(tobuy)

        return {'buy': tobuy}

    def get_statistics(self):
        return {
            'avg_price': self.avg_price,
            'total_spent': self.spent,
            'total_bought': sum(self.buy_history),
            'num_purchases': len([b for b in self.buy_history if b > 0])
        }