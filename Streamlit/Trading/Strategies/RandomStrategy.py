from datetime import datetime
from Trading.TradeStrategy import TradeStrategy
import random

class RandomStrategy(TradeStrategy):
    name = "Случайная торговля"
    description = "В этом методе торговли решения о покупке и продаже происходят абсолютно случайно"
    def __init__(self):
        super().__init__()
    
    def check_signal(self, simulation_system, date: datetime):
        if random.random() < 0.5:
            return 1, -1
        else:
            return -1, -1
    
    def start_trade(self, initial_balance, commission):
        super().start_trade(initial_balance, commission)
    
