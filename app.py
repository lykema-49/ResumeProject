import stock_analyzer as sa
import streamlit as st
import os
files = os.listdir('stockData')
tickers = [f.split('.')[0] for f in files if f.endswith('.csv') and f != 'stock_metadata.csv' and f != 'NIFTY50_all.csv']

st.write('Write the ticker of the company for analyzing')

selectedTicker = st.selectbox('Choose a stock',options=sorted(tickers),index=sorted(tickers).index('ADANIPORTS') if 'ADANIPORTS' in tickers else 0)

stock1 = sa.stock(selectedTicker)
stock1.calculateMA()
stock1.calculateRSI()
stock1.calculate_macd()
displayDf = stock1.df[['Date','Close','MA50','MA200','MA Signal',"RSI",'RSI Signal','MACD','MACD_Signal','MACD_Signal_Line']]
st.write(displayDf.set_index('Date'))

st.dataframe(displayDf[(displayDf['MA Signal'] != 'HOLD') & (displayDf['RSI Signal'] != 'HOLD') & (displayDf['MACD_Signal_Line'] != 'HOLD')].set_index('Date'))
