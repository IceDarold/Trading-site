import streamlit as st
from utilities import get_tickers
from func.ticker_page import show
from Strategies.RandomStrategy import RandomStrategy
from Strategies.LinearRegressionStrategy import LinearRegressionStrategy
from Strategies.TradeStrategy import TradeStrategy
from tickers import get_ticker_data
import streamlit as st
import plotly.graph_objects as go
from Config import config
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def pluralize(value, forms):
    """
    Функция для подбора правильного склонения слова.
    forms - это список из трех форм слова: для 1, для 2-4, для 5-0.
    """
    if value % 10 == 1 and value % 100 != 11:
        form = forms[0]
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        form = forms[1]
    else:
        form = forms[2]
    return f"{value} {form}"

def calculate_date_difference(date1_str, date2_str):
    # Преобразование строк в объекты datetime
    date_format = "%d-%m-%Y"
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)

    # Вычисление разницы между датами
    diff = relativedelta(date2, date1)

    # Формирование строки результата
    result = []
    if diff.years != 0:
        result.append(pluralize(diff.years, ["год", "года", "лет"]))
    if diff.months != 0:
        result.append(pluralize(diff.months, ["месяц", "месяца", "месяцев"]))
    if diff.days != 0:
        result.append(pluralize(diff.days, ["день", "дня", "дней"]))
    if len(result) > 1:
        return ", ".join(result[:-1]) + " и " + result[-1]
    elif len(result) == 1:
        return result[0]
    else:
        return "0 дней"

def draw():
    trade_strategies = [RandomStrategy(None), Li]
    strategy_l = ["None"]
    for strategy_item in trade_strategies:
        strategy_l.append(strategy_item.name)
    tickers_list = ["None"]
    tickers_list.extend(get_tickers())
    st.sidebar.page_link("main_menu.py", label="В меню")
    # Боковая панель для параметров
    st.sidebar.title("Параметры графика")
    ticker = st.sidebar.selectbox("Выберите котировку:", tickers_list, index=1)
    trade_strategy = st.sidebar.selectbox("Стратегия торговли", strategy_l, index=1)
    if trade_strategy != "None":
        strategy = TradeStrategy.get_instance_by_name(trade_strategy)
        st.sidebar.caption(strategy.description)
        st.sidebar.divider()
    
    commission = st.sidebar.slider("Коммиссия (в %)", 0.0, 5.0, step=0.01, value=0.0)
    initial_balance = st.sidebar.number_input("Начальный баланс", min_value=0, max_value=1000000, value=1000)
    df = get_ticker_data(ticker)
    if df is None:
        st.subheader("Для отображения информации выберите котировку с меню слева")
    else:
        st.title(f"График акций {ticker}")
        sc = go.Figure(data=go.Scatter(x=df["Date"], y=df["Close"], mode='lines', line=dict(color=config.visualization.color, width=config.visualization.width)))
        st.plotly_chart(sc)
    # Кнопка для начала торговли
    if st.sidebar.button("Start trade", key="Trade button", disabled=(ticker == 'None' or trade_strategy == 'None' or initial_balance == 0)):
        strategy.prices = pd.DataFrame({
            "Date": df["Date"],
            "Close": df["Close"]
        })
        strategy.start_trade(initial_balance, commission)
        history = strategy.simulation_system.history
        st.title(f"График вашего баланса")
        sc = go.Figure(data=go.Scatter(x=history["balance_over_time"]["Date"], y=history["balance_over_time"]["Balance"], mode='lines'))
        st.plotly_chart(sc)
        st.text(f'Всего проведено сделок по покупке {len(history["purchases"]["Date"])} штук')
        st.text(f'Всего проведено сделок по продаже {len(history["sales"]["Date"])} штук')
        st.text(f'Всего проведено сделок {len(history["purchases"]["Date"]) + len(history["sales"]["Date"])} штук')
        end_balance = history["balance_over_time"]["Balance"][-1]
        date_diff = calculate_date_difference(history["balance_over_time"]["Date"][0], history["balance_over_time"]["Date"][-1])
        start_phrase = "Общая прибыль за" if end_balance - initial_balance > 0 else "Общий убыток за"
        end_phrase = "составила" if end_balance - initial_balance > 0 else "составил"
        st.text(f'{start_phrase} {date_diff} {end_phrase} {round(abs(end_balance - initial_balance), 2)} рублей или {round(abs(end_balance / initial_balance - 1    ) * 100, 2)}%')

draw()