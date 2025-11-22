import stock_analyzer as sa
import streamlit as st
import os
files = os.listdir('stockData')
tickers = [f.split('.')[0] for f in files if f.endswith('.csv') and f != 'stock_metadata.csv' and f != 'NIFTY50_all.csv']

st.write('Write the ticker of the company for analyzing')

selectedTicker = st.selectbox('Choose a stock',options=sorted(tickers),index=sorted(tickers).index('ADANIPORTS') if 'ADANIPORTS' in tickers else 0)

stock1 = sa.stock(selectedTicker)

stock1.getVerdict()

displayDf = stock1.df[['Date','Close','Final Signal']]
st.write(displayDf[displayDf['Final Signal'] != 'HOLD'].set_index('Date'))

st.subheader('BackTrader Results: ')
st.write('Final Profit := ',sa.backTrader(selectedTicker).doTrade())

