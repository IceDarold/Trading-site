from TradeStrategy import TradeStrategy
import pandas as pd
import numpy as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error
from datetime import timedelta


class NotPreparedError(Exception):
    def __init__(self):
        super().__init__("You can not run regression without prepareLinrearRegression() function. Call it first of all and only after call other functions")

class RegressionSettings:
    def __init__(self, prediction_data, predicted_param="Close", test_sample_size=0.1, random_state=42, features_number=10, is_log=True):
        """
        Args:
            prediction_data (DataFrame): The data, that uses for prediction of predicted_param with predicted_param itself for checking. 
            Needs to contain columns Open, Close, High, Low, Volume, Date. Without any if these columns, the ValueError will be arised
        """
        if predicted_param not in ["Close", "Open", "High", "Low"]: raise ValueError(f"Param {predicted_param} can not be predicted")
        self.feature_number = features_number
        self.is_log = is_log
        self.random_state = random_state
        self.test_sample_size = test_sample_size
        self.random_state = random_state

class LinearRegressionStrategy(TradeStrategy):
    def __init__(self):
        self.regression_settings = None
        self._trained_data = None
        self._prepared = False
        super().__init__(
            name = "Линейная регрессия",
            description = "Этот метод торговли работает на основе предсказаний будущих ценых с помощью линейной регрессии",
            prices = pd.concat([X_test["Date"], y_test])
        )
    
    def prepareLinearRegression(self, regressionSettings: RegressionSettings):
        self.validate_dataframe(regressionSettings.prediction_data)
        X_train, X_test, y_train, y_test = train_test_split(self.regression_settings.prediction_data, self.regression_settings.prediction_data["Close"], 
                                                            test_size=self.regression_settings.test_sample_size, random_state=self.regression_settings.random_state,
                                                            shuffle=False)
        self._model, self._model_accuracy, self._X_test, self._y_predicted, self._y_test = self.train_model(pd.concat([X_train, y_train], axis=1))
        self._trained_data = pd.concat([X_train, y_train])
        self._prepared = True
    
    def validate_dataframe(df, except_list=[]):
        """
        return:
            Result of validation and the error if it is
        """
        required_columns = [item for item in ["Open", "Close", "High", "Low", "Volume", "Date"] if item not in except_list]
        for column in required_columns:
            if column not in df.columns:
                raise f"There is no param {column}"


    def _generate_features_days_ago(self, df):
        for i in range(1, self.features_number + 1):
            if self.is_log:
                df[f"Y{i}Low"] = np.log(df["Low"].shift(i) / df["Open"].shift(i))
                df[f"Y{i}High"] = np.log(df["High"].shift(i) / df["Open"].shift(i))
                df[f"Y{i}Close"] = np.log(df["Close"].shift(i) / df["Open"].shift(i))
            else:
                df[f"Y{i}Low"] = df["Low"].shift(i)
                df[f"Y{i}High"] = df["High"].shift(i)
                df[f"Y{i}Close"] = df["Close"].shift(i)
    
    def _convert_df(self, df) -> pd.DataFrame:
        new_df = df.copy()
        # Преобразование колонок в datetime формат
        new_df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        # Преобразование даты в числовой формат
        new_df["YVolume"] = df["Volume"].shift(1)
        new_df["YClose"] = df["Close"].shift(1)
        new_df = self._generate_features_days_ago(new_df)

        if self.is_log:
            new_df["YLow"] = np.log(df["Low"].shift(1) / df["Open"])
            new_df["YHigh"] = np.log(df["High"].shift(1) / df["Open"])
            new_df["log_lable"] =  np.log(df["Close"] / df["YClose"])
        else:
            new_df["YLow"] = df["Low"].shift(1)
            new_df["YHigh"] = df["High"].shift(1)
            new_df["log_lable"] =  df["Close"]
        new_df = new_df.drop(['Date', "Close", "Low", "High", "Volume", "YClose"], axis=1)
        return new_df
            
    def _fill(self, df, feature):
        return df[feature].fillna(df[feature].mean())

    def train_model(self, X_train, test_size=0.1):
        if not self._prepared: raise NotPreparedError()
        train_df = self._convert_df(X_train)
        X_tr, X_te, y_train, y_test = train_test_split(train_df, train_df["log_lable"], test_size=test_size, random_state=42,
                                                            shuffle=False)
        X_train = X_tr.drop(["log_lable"], axis=1)
        numeric_features = X_train.columns
        print(numeric_features)
        numeric_transformer = Pipeline(steps=[
            ("imputes", SimpleImputer(strategy="mean"))
        ])
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features)
            ]
        )
        model = Pipeline(steps=[
           ("preprocessor", preprocessor),
           ("regressor", LinearRegression())
        ])
        model.fit(X_train, y_train)
        X_test = X_te.drop(["log_lable"], axis=1)
        y_test_predict = model.predict(X_test)
        accuracy = mean_absolute_error(y_test_predict, y_test)
        return model, accuracy, X_te, y_test_predict, y_test
    
    def get_prediction(self, model, data, prepared=False):
        if not self._prepared:
            raise NotPreparedError()
        self.validate_dataframe(data, ["Close"])
        if not prepared:
            data = data[["Open", "High", "Low", "Volume", "Date"]]
            self._convert_df(data)
        return pd.concat([model.predict(data), data["Date"]])

    def buy(self, simulation_system, date):
        predicted_df = self.get_prediction(self._model, simulation_system.actual_prices[simulation_system.actual_prices["Date"] == date])#Make sure about equality
        predicted_price_today = predicted_df.iloc(1)["Close"]
        actual_price_yestersay = simulation_system.get_price_by_date(date - timedelta(days=1))
        # predicted_price_today = actual_price_yesterday * np.exp(get_prediction(model, X_test.iloc[i]))

        # Решение о покупке или продаже
        if predicted_price_today > actual_price_yestersay and simulation_system.balance > 0:
            return True, simulation_system.balance
        return False,

    def sell(self, simulation_system, date):
        predicted_df = self.get_prediction(self._model, simulation_system.actual_prices[simulation_system.actual_prices["Date"] == date])#Make sure about equality
        predicted_price_today = predicted_df.iloc(1)["Close"]
        actual_price_yestersay = simulation_system.get_price_by_date(date - timedelta(days=1))
        # predicted_price_today = actual_price_yesterday * np.exp(get_prediction(model, X_test.iloc[i]))

        # Решение о покупке или продаже
        if predicted_price_today < actual_price_yestersay and simulation_system.shares > 0:
            return True, simulation_system.shares
        return False,
