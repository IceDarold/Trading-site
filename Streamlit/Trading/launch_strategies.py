from Trading.Strategies.LinearRegressionStrategy import LinearRegressionStrategy, RegressionSettings
from Trading.Strategies.BollingerBandsStrategy import BollingerBandsStrategy
from Trading.Strategies.SMAStrategy import SMAStrategy
from Trading.Strategies.TwoSMAStrategy import TwoSMAStrategy
import streamlit as st
import plotly.graph_objects as go
from Config import config

def launch_bollinger_bands_strategy():
    with st.sidebar:
        with st.expander("Параметры линий Боллинджера"):
            window = st.number_input("Размер окна", min_value=2, value=20)
            num_of_std = st.number_input("Num of std", min_value=1, value=2) 
    return BollingerBandsStrategy(window, num_of_std)

def prepare_linear_regression(start_date, regression: LinearRegressionStrategy):
    with st.sidebar:
        with st.expander("Advanced settings"):
            predicted_param = st.radio("Predicted param", ["Close", "Open", "High", "Low"])
            feature_number = st.number_input("Feature number", min_value=0, value=10)
            is_log = st.toggle("Is log")
    if st.sidebar.button("Show prediction"):
        regressionSettings = RegressionSettings(
                                prediction_data=df, 
                                predicted_param=predicted_param,
                                features_number=feature_number,
                                is_log=is_log,
                                start_date=start_date)
        regression.prepareLinearRegression(regressionSettings)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=regression._X_test["Date"], y=regression._y_predicted, 
                                    mode='lines', line=dict(color=config.visualization.color, width=config.visualization.width),
                                    name="Предсказания модели"))
        fig.add_trace(go.Scatter(x=regression._X_test["Date"], y=regression._y_test, 
                                    mode='lines', line=dict(color=config.visualization.prediction_color, width=config.visualization.width),
                                    name="Реальная цена"))
        st.plotly_chart(fig)
        with st.expander("Show statistics"):
            st.text(f"MAE: {regression._model_accuracy}")
    st.sidebar.divider()


def launch_MA_strategy():
    with st.sidebar:
        with st.expander("Параметры одной скользящей средней"):
            window = st.number_input("Размер окна", min_value=2, value=20)
    return SMAStrategy(window)

def launch_twoMA_strategy():
    with st.sidebar:
        with st.expander("Параметры скользящих средних"):
            window_1 = st.number_input("Размер первого окна", min_value=2, value=12)
            window_2 = st.number_input("Размер второго окна", min_value=2, value=48)
    return TwoSMAStrategy(window_1, window_2)