import pandas as pd
from datetime import datetime

class TradeStrategy:
    def check_signal(self, simulation_system, date: datetime):
        '''
        In first returning param return 1 if there is a buy signal, -1 if there is a sell signal, and 0 if there is no signals
        Params:
            date (datetime): date of purchase
        '''
        return -1, -1

    def __init__(self):
        pass