import pandas as pd
    
class stock:
    def __init__(self,ticker):
        self.ticker = ticker
        try:
            self.df = pd.read_csv(f'./stockData/{ticker}.csv',parse_dates=['Date'])
        except FileNotFoundError as e:
            print(f'Error:An Error has occured\n{e}')

    def calculateMA(self):
        self.df['MA50'] = self.df['Close'].rolling(window=50).mean()
        self.df['MA200'] = self.df['Close'].rolling(window=200).mean()
        self.df['MA Signal'] = 'HOLD'

        buyCon = (self.df['MA50'] > self.df['MA200']) & (self.df['MA50'].shift(1) < self.df['MA200'].shift(1))
        sellCon = (self.df['MA50'] < self.df['MA200']) & (self.df['MA50'].shift(1) > self.df['MA200'].shift(1))

        self.df.loc[buyCon, 'MA Signal'] = 'BUY'
        self.df.loc[sellCon, 'MA Signal'] = 'SELL'

    def calculateRSI(self):
        delta = self.df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        self.df['RSI'] = 100 - (100 / (1 + rs))
        self.df['RSI Signal'] = 'HOLD'
        self.df.loc[self.df['RSI'] < 30, 'RSI Signal'] = 'BUY'
        self.df.loc[self.df['RSI'] > 70, 'RSI Signal'] = 'SELL'

    def calculate_macd(self):
        # Calculate the EMAs
        ema_12 = self.df['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = self.df['Close'].ewm(span=26, adjust=False).mean()

        # Calculate the MACD line
        self.df['MACD'] = ema_12 - ema_26

        # Calculate the Signal line
        self.df['MACD_Signal'] = self.df['MACD'].ewm(span=9, adjust=False).mean()

        # Calculate the MACD Histogram
        self.df['MACD_Hist'] = self.df['MACD'] - self.df['MACD_Signal']

        # Generate Signals
        self.df['MACD_Signal_Line'] = 'HOLD'
        buy_condition = (self.df['MACD'] > self.df['MACD_Signal']) & (self.df['MACD'].shift(1) < self.df['MACD_Signal'].shift(1))
        sell_condition = (self.df['MACD'] < self.df['MACD_Signal']) & (self.df['MACD'].shift(1) > self.df['MACD_Signal'].shift(1))

        self.df.loc[buy_condition, 'MACD_Signal_Line'] = 'BUY'
        self.df.loc[sell_condition, 'MACD_Signal_Line'] = 'SELL'
    
    def getVerdict(self):
    # Ensure indicators are computed
        self.calculateMA()
        self.calculateRSI()
        self.calculate_macd()

    # Mapping for signals
        signal_map = {'BUY': 1, 'SELL': -1, 'HOLD': 0}

    # Compute total score in one vectorized step
        self.df['Final_Score'] = (
            self.df['MA Signal'].map(signal_map) +
            self.df['RSI Signal'].map(signal_map) +
            self.df['MACD_Signal_Line'].map(signal_map)
        )

    # Default verdict
        self.df['Final Signal'] = 'HOLD'

    # Apply conditions
        self.df.loc[self.df['Final_Score'] >= 2, 'Final Signal'] = 'BUY'
        self.df.loc[self.df['Final_Score'] <= -2, 'Final Signal'] = 'SELL'

class backTrader(stock):
    def __init__(self, ticker):
        super().__init__(ticker)   # load df
        self.balance = 10000       # starting capital
        self.position = 0          # 0 = no stock, 1 = holding stock
        self.buy_price = 0
        self.equity_curve = []     # track equity over time

    def doTrade(self):
        # Generate signals
        self.getVerdict()

        for idx, row in self.df.iterrows():
            signal = row['Final Signal']
            price = row['Close']

            # BUY CONDITION
            if signal == "BUY" and self.position == 0:
                self.position = 1
                self.buy_price = price
                # print(f"BUY @ {price}")

            # SELL CONDITION
            elif signal == "SELL" and self.position == 1:
                self.position = 0
                profit = price - self.buy_price
                self.balance += profit
                # print(f"SELL @ {price}, Profit = {profit:.2f}")

            # Track equity (if holding, unrealized P/L is shown)
            if self.position == 1:
                current_equity = self.balance + (price - self.buy_price)
            else:
                current_equity = self.balance

            self.equity_curve.append(current_equity)

        return round(self.balance - 10000,2)

