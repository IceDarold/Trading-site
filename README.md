# MOEX Stock Price Prediction

This project is focused on creating a model to predict stock prices for companies listed on the Moscow Exchange (MOEX). It includes data collection, processing, analysis, and machine learning model building to forecast future stock prices. This project can serve as a tool for market analysis and investment decision-making support.

## Features

- **Data Collection:** The project automatically downloads historical stock price data from the Moscow Exchange.
- **Data Preprocessing:** Cleans and transforms data to improve model quality.
- **Model Building:** Utilizes a machine learning model trained on historical data to forecast stock prices.
- **Result Analysis:** Visualizes prediction results and model accuracy metrics.
- **Forecasting:** Predicts future stock prices based on the trained model.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IceDarold/moex-stock-prediction.git
   cd moex-stock-prediction
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Obtain API keys to access data (e.g., Alpha Vantage or Yahoo Finance) and specify them in the configuration file.

## Usage

### Steps to Run

1. **Data Collection:** Run `data_collection.py` to gather historical data.
   ```bash
   python data_collection.py
   ```

2. **Model Training:** Run `train_model.py` to train the model on the collected data.
   ```bash
   python train_model.py
   ```

3. **Forecasting:** Run `predict.py` to predict prices for selected stocks.
   ```bash
   python predict.py --ticker SBER
   ```

### Configuration

All script parameters, such as stock list, forecast period, and other settings, can be specified in the `config.json` file.

## Project Structure

- `data_collection.py` - script for collecting historical data.
- `train_model.py` - script for training the model.
- `predict.py` - script for forecasting prices.
- `config.json` - project configuration file.
- `requirements.txt` - dependency file.

## Technologies

- **Programming Language:** Python
- **Libraries:** 
  - `Pandas` for data manipulation
  - `Scikit-Learn` or `TensorFlow` for machine learning model creation
  - `Matplotlib`, `Seaborn` for data visualization
- **Data Sources:** API for price data retrieval (e.g., Alpha Vantage)

## Future Plans

- Support for more stocks.
- Addition of an interface for data visualization and analysis.
- Model improvements and new prediction methods.

## Contributing

If you have suggestions or would like to contribute, please open a Pull Request or create an Issue.

---
