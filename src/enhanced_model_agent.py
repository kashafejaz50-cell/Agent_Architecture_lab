"""
Enhanced model-based agent that estimates consumption patterns
Addresses question from page 7
"""

from src.agents import Agent


class EnhancedModelAgent(Agent):

    def __init__(self, learning_rate=0.1):
        self.spent = 0
        self.buy_history = []
        self.price_history = []
        self.stock_history = []

        self.estimated_consumption = 3.5
        self.learning_rate = learning_rate

        self.last_stock = None
        self.last_buy = 0

    def estimate_consumption(self, previous_stock, current_stock, bought):

        if previous_stock is not None:
            actual_consumption = previous_stock + bought - current_stock

            if actual_consumption > 0:
                self.estimated_consumption = (
                    self.estimated_consumption * (1 - self.learning_rate)
                    + actual_consumption * self.learning_rate
                )

        return self.estimated_consumption

    def predict_future_stock(self, current_stock, horizon=5):
        return current_stock - (self.estimated_consumption * horizon)

    def select_action(self, percept):

        price = percept['price']
        current_stock = percept['instock']

        self.price_history.append(price)
        self.stock_history.append(current_stock)

        self.estimate_consumption(
            self.last_stock,
            current_stock,
            self.last_buy
        )

        self.last_stock = current_stock

        predicted_stock = self.predict_future_stock(current_stock, horizon=5)

        if predicted_stock < 10:

            if price < self.get_average_price():
                tobuy = 30
            else:
                tobuy = 15

        elif current_stock < 15:
            tobuy = 10

        elif price < 200 and current_stock < 40:
            tobuy = 5

        else:
            tobuy = 0

        self.last_buy = tobuy
        self.spent += tobuy * price
        self.buy_history.append(tobuy)

        return {'buy': tobuy}

    def get_average_price(self):

        if not self.price_history:
            return 250

        window = min(10, len(self.price_history))
        return sum(self.price_history[-window:]) / window