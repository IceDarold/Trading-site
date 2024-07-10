from datetime import datetime
from Trading.TradeStrategy import TradeStrategy
import pandas as pd
from datetime import timedelta
from Trading.SimulationSystem import SimulationSystem

class TwoSMAStrategy(TradeStrategy):
    name = "Скользящие средние"
    description = "Этот метод торговли работает на основе скользящих средних"
    def __init__(self, window_1, window_2):
        if window_1 is None: raise ValueError("You should provide window_1 param!")
        if window_2 is None: raise ValueError("You should provide window_2 param!")
        self.window_1 = window_1
        self.window_2 = window_2
        super().__init__()
    
    def check_signal(self, simulation_system: SimulationSystem, date: datetime):
        try:
            sma_1, sma_2 = self.get_sma(simulation_system.get_data_between_dates(date - timedelta(minutes=(self.window_2 + 2) * simulation_system.time_frame_in_minutes), date).Close, 
                                                            self.window_1, 
                                                            self.window_2)
        except ValueError as err:
            print(err)
            return 0, -1
        if sma_1.iloc[-1] < sma_2.iloc[-1] and sma_1.iloc[-2] >= sma_2.iloc[-2]:
            return 1, -1
        elif sma_1.iloc[-1] > sma_2.iloc[-1] and sma_1.iloc[-2] <= sma_2.iloc[-2]:
            return -1, -1
        else: return 0, -1
    
    def get_sma(self, param: pd.Series, window_1=12, window_2=48):
        if len(param) < window_2: raise ValueError(f"The size of series ({len(param)}) is lower then window ({window_2})")
        sma_1: pd.Series = param.rolling(window=window_1).mean()
        sma_2: pd.Series = param.rolling(window=window_2).mean()
        return sma_1, sma_2