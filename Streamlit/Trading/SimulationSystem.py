import pandas as pd
from datetime import datetime
from Trading.TradeStrategy import TradeStrategy


class SimulationSystem:
    def __init__(self, real_time_data: pd.DataFrame, initial_balance=1000, commission=0, time_frame_in_minutes=10):
        """
        Params:
            real_time_data: (DataFrame): Data, that uses for making decisions and checking them. Need to contain columns Open, Close, High, Low, 
                                        Volume, Date. Without any if these columns, the ValueError will be arised
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.common_balance = self.balance
        self.shares = 0
        self.commission = commission
        self.time_frame_in_minutes = time_frame_in_minutes
        self.real_time_data = real_time_data
        self.validate_dataframe()
        self.create_history()
    
    def validate_dataframe(self, except_list=[]):
        """
        return:
            Result of validation and the error if it is
        """
        required_columns = [item for item in ["Open", "Close", "High", "Low", "Volume", "Date"] if item not in except_list]
        for column in required_columns:
            if column not in self.real_time_data.columns:
                raise ValueError(f"There is no param {column}")
    
    def get_data_between_dates(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        '''
        Return dataframe with data between two dates (non-inclusive)
        '''
        if len(self.real_time_data) == 0: raise ValueError("self.real_time_data is empty")
        return self.real_time_data[start_date < self.real_time_data['Date']][self.real_time_data['Date'] < end_date]

    def create_history(self):
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

    def get_price_by_date(self, date, param="Close"):
        return self.real_time_data[self.real_time_data["Date"] == date][param]

    def simulate_trading(self, trade_strategy: TradeStrategy) -> dict:
        """
        Params:
            trade_strategy (TradeStrategy): strategy, that uses for making decisions
        Return:
            dict with simulation log data
        """
        for i in range(0, len(self.real_time_data) - 1):
            actual_price_today = self.real_time_data.iloc[i].Close
            signal, amount = trade_strategy.check_signal(self, self.real_time_data.iloc[i].Date)
            print(f"{i} out of {len(self.real_time_data) - 1}", actual_price_today, signal, amount)
            if signal == 1:
                shares_to_buy = min(amount if amount != -1 else self.balance, self.balance) // (actual_price_today * (1 + self.commission))
                self.balance -= shares_to_buy * actual_price_today * (1 + self.commission)
                self.shares += shares_to_buy
                self.history["purchases"]["Date"].append(pd.to_datetime(self.real_time_data.iloc[i].Date))
                self.history["purchases"]["Price"].append(actual_price_today)
                self.history["purchases"]["Amount"].append(shares_to_buy)
            elif signal == -1:
                shares_to_sell = min(self.shares, amount if amount != -1 else self.shares)
                self.balance += shares_to_sell * actual_price_today * (1 - self.commission)
                self.shares -= shares_to_sell
                self.history["sales"]["Date"].append(pd.to_datetime(self.real_time_data.iloc[i].Date))
                self.history["sales"]["Price"].append(actual_price_today)
                self.history["sales"]["Amount"].append(shares_to_sell)

            self.common_balance = self.balance + self.shares * actual_price_today
            self.history["balance_over_time"]["Date"].append(pd.to_datetime(self.real_time_data.iloc[i].Date))
            self.history["balance_over_time"]["Balance"].append(self.common_balance)
        return self.history