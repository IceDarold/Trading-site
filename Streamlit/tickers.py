import pandas as pd
import os


def get_ticker_data(name: str) -> pd.DataFrame:
    if os.path.exists("Data/" + name + ".csv"):
        df = pd.read_csv("Data/" + name + ".csv")
        return df
    else: return None

