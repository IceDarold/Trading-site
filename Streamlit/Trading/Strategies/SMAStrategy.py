from datetime import datetime
from Trading.TradeStrategy import TradeStrategy
import pandas as pd
from datetime import timedelta
from Trading.SimulationSystem import SimulationSystem

class SMAStrategy(TradeStrategy):
    name = "Одна скользящая средняя"
    description = "Этот метод торговли работает на основе пересечений цены и скользящей средней"
    def __init__(self, window):
        if window is None: raise ValueError("You should provide window param!")
        self.window = window
        super().__init__()
    
    def check_signal(self, simulation_system: SimulationSystem, date: datetime):
        try:
            sma = self.get_sma(simulation_system.get_data_between_dates(date - timedelta(minutes=(self.window + 1) * simulation_system.time_frame_in_minutes), date).Close, 
                                                            self.window)
        except ValueError as err:
            print(err)
            return 0, -1
        current_price = simulation_system.get_price_by_date(date=date).iloc[0]
        previous_price = simulation_system.get_price_by_date(date=date - timedelta(minutes=simulation_system.time_frame_in_minutes))
        if len(previous_price) == 0: return 0, -1
        print(len(previous_price))
        if previous_price is None:
            return 0, -1
        if current_price < sma.iloc[-1] and previous_price.iloc[0] >= sma.iloc[-1]:
            return 1, -1
        elif current_price > sma.iloc[-1] and previous_price.iloc[0] <= sma.iloc[-1]:
            return -1, -1
        else: return 0, -1
    
    def get_sma(self, param: pd.Series, window=20):
        if len(param) < window: raise ValueError(f"The size of series ({len(param)}) is lower then window ({window})")
        sma: pd.Series = param.rolling(window=window).mean()
        return sma