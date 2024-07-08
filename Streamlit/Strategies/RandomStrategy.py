from Strategies.TradeStrategy import TradeStrategy, SimulationSystem
import random

class RandomStrategy(TradeStrategy):
    def __init__(self, prices):
        super().__init__(
            name = "Случайная торговля", 
            description = "В этом методе торговли решения о покупке и продаже происходят абсолютно случайно",
            prices = prices)
    
    def buy(self, simulation_system, date):
        if random.random() < 0.5:
            return True, 1000
        else:
            return False, 1000

    def sell(self, simulation_system, date):
        if random.random() < 0.5:
            return True, 1000
        else:
            return False, 1000
    
    def start_trade(self, initial_balance, commission):
        super().start_trade(initial_balance, commission)
    
