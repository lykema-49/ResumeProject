# Stock Analysis Dashboard

A Python-based stock analysis tool built with Streamlit that analyzes technical indicators (Moving Averages, RSI, and MACD) to provide investment signals (BUY, SELL, HOLD).

## Features

- **Multiple Technical Indicators**: Analyzes Moving Averages (MA50/MA200), RSI, and MACD
- **Interactive Dashboard**: Streamlit-based web interface for easy stock selection
- **Signal Generation**: BUY/SELL/HOLD signals based on technical analysis
- **Historical Data**: Works with CSV stock data stored locally
- **Filtered Results**: Displays only rows where multiple indicators align

## Project Structure

```
├── app.py                 # Main Streamlit application
├── stock_analyzer.py      # Stock analysis logic and calculations
└── stockData/             # Directory containing stock CSV files
    ├── ADANIPORTS.csv
    ├── stock_metadata.csv
    ├── NIFTY50_all.csv
    └── [other stock files]
```

## Installation

### Prerequisites

- Python 3.8+
- Streamlit
- Pandas

### Setup

1. Install dependencies:
```bash
pip install streamlit pandas
```

2. Prepare your stock data CSV files in the `stockData` folder with columns: `Date`, `Close`

3. Run the app:
```bash
streamlit run app.py
```

## How It Works

### 1. **Moving Averages (MA)**
- Calculates 50-day and 200-day moving averages
- **BUY Signal**: MA50 crosses above MA200
- **SELL Signal**: MA50 crosses below MA200
- **HOLD**: No crossover detected

### 2. **Relative Strength Index (RSI)**
- 14-period RSI calculation
- **BUY Signal**: RSI < 30 (Oversold condition)
- **SELL Signal**: RSI > 70 (Overbought condition)
- **HOLD**: RSI between 30-70

### 3. **MACD (Moving Average Convergence Divergence)**
- 12-day and 26-day EMAs to calculate MACD line
- 9-day EMA as Signal line
- MACD Histogram shows difference between MACD and Signal
- **BUY Signal**: MACD crosses above Signal line
- **SELL Signal**: MACD crosses below Signal line
- **HOLD**: No crossover detected

## Understanding the Code

### stock_analyzer.py

```python
class stock:
    def __init__(self, ticker):
        # Loads CSV data for the given ticker
        self.df = pd.read_csv(f'./stockData/{ticker}.csv', parse_dates=['Date'])
    
    def calculateMA(self):
        # Calculates 50-day and 200-day moving averages
        # Generates BUY/SELL/HOLD signals based on crossovers
    
    def calculateRSI(self):
        # Calculates 14-period RSI
        # Overbought/Oversold signals
    
    def calculate_macd(self):
        # Calculates MACD line, Signal line, and Histogram
        # Generates crossover signals
```

### app.py

- Loads all stock CSV files from `stockData` folder
- Provides dropdown to select a stock
- Calculates all three indicators
- Displays full data table
- Shows filtered table with strong signals (all 3 indicators align)

## CSV Data Format

Your stock data CSV should look like:

```
Date,Close,Volume,High,Low
2024-01-01,150.25,1000000,151.50,149.00
2024-01-02,151.75,1100000,152.25,150.50
...
```

Minimum required column: `Date` and `Close`

## Output

The dashboard displays:

1. **Full Data Table**: All calculated indicators for all dates
2. **Signal Alignment Table**: Only rows where all three indicators give non-HOLD signals

Example output columns:
- `Date`: Trading date
- `Close`: Closing price
- `MA50` / `MA200`: Moving averages
- `MA Signal`: BUY/SELL/HOLD
- `RSI`: RSI value (0-100)
- `RSI Signal`: BUY/SELL/HOLD
- `MACD`: MACD line value
- `MACD_Signal`: Signal line value
- `MACD_Signal_Line`: BUY/SELL/HOLD

## Key Concepts to Learn

### Moving Averages
- **MA50**: Average closing price over 50 days (short-term trend)
- **MA200**: Average closing price over 200 days (long-term trend)
- When short-term MA crosses long-term MA, it signals a trend change

### RSI (Relative Strength Index)
- Measures momentum on a 0-100 scale
- Below 30: Stock is oversold (potential buy)
- Above 70: Stock is overbought (potential sell)
- Helps identify reversal points

### MACD
- MACD Line: Difference between 12-day and 26-day EMAs
- Signal Line: 9-day EMA of the MACD line
- When MACD crosses above Signal: Bullish momentum
- When MACD crosses below Signal: Bearish momentum

## Limitations

- Works only with CSV files in `stockData` folder
- Requires sufficient historical data (at least 200 days for MA200)
- Technical indicators alone aren't guaranteed predictions
- Should be combined with other analysis methods

## Disclaimer

**This tool is for educational and informational purposes only.** It should not be considered financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.

## Next Steps to Enhance Your Project

1. Add more indicators (Bollinger Bands, Stochastic, etc.)
2. Combine indicator signals using voting/weighting system
3. Add backtesting functionality
4. Store analysis results to database
5. Add alerts when signals are generated
6. Create performance metrics for the indicators
7. Add sentiment analysis

## Resources

- [Moving Averages Explained](https://www.investopedia.com/terms/m/movingaverage.asp)
- [RSI Indicator Guide](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Explanation](https://www.investopedia.com/terms/m/macd.asp)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Happy learning! 📈**
