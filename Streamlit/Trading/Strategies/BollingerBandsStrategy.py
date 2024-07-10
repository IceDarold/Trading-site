from Trading.TradeStrategy import TradeStrategy
from Trading.SimulationSystem import SimulationSystem
import pandas as pd
from datetime import datetime, timedelta 

class BollingerBandsStrategy(TradeStrategy):
    name = "Линии Боллинджера"
    description = "Этот метод торговли работает на основе линий Боллинджера"
    def __init__(self, window, num_of_std):
        if window is None: raise ValueError("You should provide window param!")
        if num_of_std is None: raise ValueError("You should provide num_of_std param!")
        self.window = window
        self.num_of_std = num_of_std
        super().__init__()
    
    def check_signal(self, simulation_system: SimulationSystem, date: datetime):
        try:
            lower_band, upper_band, sma = self.get_bollinger_bands(
                simulation_system.get_data_between_dates(date -  timedelta(minutes=(self.window + 1) * simulation_system.time_frame_in_minutes), date)["Close"],
                self.window, 
                self.num_of_std)
        except ValueError as err:
            print(err)
            return 0, -1
        current_price = simulation_system.get_price_by_date(date=date)
        if current_price.iloc[0] <= lower_band.iloc[-1]:
            return 1, -1
        elif current_price.iloc[0] >= upper_band.iloc[-1]:
            return -1, -1
        else: return 0, -1
        

    def get_bollinger_bands(self, param: pd.Series, window=20, num_of_std=2):
        if len(param) < window: raise ValueError(f"The size of series ({len(param)}) is lower then window ({window})")
        sma: pd.Series = param.rolling(window=window).mean()
        std: pd.Series = param.rolling(window=window).std()
        upper_band = sma + (std * num_of_std)
        lower_band = sma - (std * num_of_std)
        return lower_band, upper_band, sma