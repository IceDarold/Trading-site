import pandas as pd

class TradeStrategy:
    _instances = []
    def __init__(self, name, description, prices):
        self.name = name
        self.description = description
        TradeStrategy._instances.append(self)
        self.prices = prices

    @classmethod
    def get_instance_by_name(self, name):
        for instance in TradeStrategy._instances:
            if instance.name == name:
                return instance
    def buy(self, simulation_system, date):
        pass

    def sell(self, simulation_system, date):
        pass

    def start_trade(self, initial_balance, commission):
        self.simulation_system = SimulationSystem(buy_function=self.buy, sell_function=self.sell, initial_balance=initial_balance, commission=commission)
        self.simulation_system.simulate_trading(self.prices)

class Deal:
    def __init__(self):
        self.open_price = None
        self.close_price = None
        self.open_commission = None
        self.close_commission = None
        self.profit = 0
        self.profit_with_commission = 0

    def open(self, price, commission):
        self.open_price = price
        self.open_commission = commission

    def close(self, price, close_commission):
        if not self.open:
            return
        self.close_price = price
        self.close_commission = close_commission
        self.profit = self.close_price - self.open_price
        self.profit_with_commission = self.profit - self.open_price * (1 + self.open_commission) - self.close_price * (
                    1 + self.close_commission)


class SimulationSystem:
    def __init__(self, buy_function, sell_function, initial_balance=1000, commission=0):
        """
        Params:
            buy_function (function): function, which gives a buy signal. It takes ref to SimulationSystem and date of required prediction
            sell_function (function): function, which gives a sell signal. It takes ref to SimulationSystem and date of required prediction
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.common_balance = self.balance
        self.shares = 0
        self.buy_function = buy_function
        self.sell_function = sell_function
        self.commission = commission
        self.actual_prices = pd.DataFrame()
        self.clear_history()

    def clear_history(self):
        self.history = {
            "purchases": {
                "Date": [],
                "Price": [],
                "Amount": []
            },
            "sales": {
                "Date": [],
                "Price": [],
                "Amount": []
            },
            "balance_over_time": {
                "Date": [],
                "Balance": []
            }
        }

    def real_trade(self):
        pass

    def get_price_by_date(self, date):
        return self.actual_prices[self.actual_prices["Date"] == date]["Close"]

    def simulate_trading(self, actual_prices: pd.DataFrame):
        """
        Params
            actual_prices (pd.DataFrame): real prices, which our model need to predict
        """
        self.actual_prices = actual_prices
        for i in range(0, len(actual_prices.Close) - 1):
            actual_price_today = actual_prices.Close[i]
            buy_data = self.buy_function(self, actual_prices.Date[i])
            if buy_data[0]:
                shares_to_buy = min(buy_data[1], self.balance) // (actual_price_today * (1 + self.commission))
                self.balance -= shares_to_buy * actual_price_today * (1 + self.commission)
                self.shares += shares_to_buy
                self.history["purchases"]["Date"].append(actual_prices.Date[i])
                self.history["purchases"]["Price"].append(actual_price_today)
                self.history["purchases"]["Amount"].append(shares_to_buy)
            sell_data = self.sell_function(self, actual_prices.Date[i])
            if sell_data[0]:
                shares_to_sell = min(self.shares, sell_data[1])
                self.balance += shares_to_sell * actual_price_today * (1 - self.commission)
                self.shares -= shares_to_sell
                self.history["sales"]["Date"].append(actual_prices.Date[i])
                self.history["sales"]["Price"].append(actual_price_today)
                self.history["sales"]["Amount"].append(shares_to_sell)

            self.common_balance = self.balance + self.shares * actual_price_today
            self.history["balance_over_time"]["Date"].append(actual_prices.Date[i])
            self.history["balance_over_time"]["Balance"].append(self.common_balance)