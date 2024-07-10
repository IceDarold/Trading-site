import pandas as pd
import os


def get_ticker_data(name: str) -> pd.DataFrame:
    if os.path.exists("Data/" + name + ".csv"):
        df = pd.read_csv("Data/" + name + ".csv")
        try:
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
            df = df.dropna(subset=['Close'])
        except ValueError:
            df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
            df = df.dropna(subset=['Close'])
        return df
    else: return None

