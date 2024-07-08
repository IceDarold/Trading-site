from tickers import get_ticker_data
import streamlit as st
import plotly.graph_objects as go
from Config import config

def show_stock(stock_name):
    df = get_ticker_data(stock_name)
    if df is None:
        st.subheader("Для отображения информации выберите котировку с меню слева")
        return
    st.title(f"График акций {stock_name}")
    sc = go.Figure(data=go.Scatter(x=df["Date"], y=df["Close"], mode='lines', line=dict(color=config.visualization.color, width=config.visualization.width)))
    st.plotly_chart(sc)