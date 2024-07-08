import streamlit as st
from Utilities.stock_parser import parse_ticker, ticker_exists
import pandas as pd
import os

def main():
    st.title("Парсер")
    st.text("Здесь можно попарсить данные о котировках")
    ticker = st.text_input("Введите название котировки")
    if st.button("Спарсить"):
        if os.path.exists(f"Data/{ticker}.csv"):
            print("Already exists")
            df = pd.read_csv(f"Data/{ticker}.csv")
        else:
            ticker_exist = ticker_exists(ticker)
            if ticker_exist is True:
                df = parse_ticker(ticker)
            elif ticker_exist is False:
                st.text("Такого тикера в базе мосбиржы нет :(")
                return
            else:
                st.text("Неожиданная ошибка, проверьте ваше подключение к интернету и попробуйте ещё раз")
                return
        with open(f"Data/{ticker}.csv", 'r') as file:
            file_content = file.read()
        st.title(f"Dataframe с данными по ценам {ticker}")
        st.dataframe(df)
        st.download_button("Скачать спарсенные данные", file_content, file_name=f"{ticker}.csv")
main()
