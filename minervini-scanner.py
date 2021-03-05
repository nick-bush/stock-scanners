#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 15:01:20 2021

@author: neo
"""

from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time
yf.pdr_override()

#get s&p 500 tickers and format
tickers = si.tickers_sp500()
tickers = [item.replace(".", "-") for item in tickers]
#S&P ticker
index_name = '^GSPC'
#start date - one year ago
start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = datetime.date.today()
#relevant values for each ticker
exportList = pd.DataFrame(columns =['Stock','RS_Rating','50 MA','150 MA', '200 MA','52 Week Low','52 Week high'])
#performance relative to index
returns_multiples=[]

#read index data with pdr
index_df = pdr.get_data_yahoo(index_name,start_date,end_date)
index_df['Percent Change'] = index_df['Adj Close'].pct_change()
index_return = (index_df['Percent Change'] + 1).cumprod()[-1]

#top 30% of stocks relative to index
for ticker in tickers:
    #get data for each ticker
    df = pdr.get_data_yahoo(ticker,start_date,end_date)
    df.to_csv(f'{ticker}.csv')
    
    #calculate returns relative to market
    df['Percent Change'] = df['Adj Close'].pct_change()
    stock_return = (df['Percent Change'] + 1).cumprod()[-1]
    returns_multiple = round((stock_return / index_return),2)
    returns_multiples.extend([returns_multiple])
    print(f'Ticker: {ticker}; Returns Multiple against {index_name}: {returns_multiple}\n')
    #prevents errors due to spamming yahoo
    time.sleep(1)
    
    rs_df = pd.DataFrame(list(zip(tickers, returns_multiples)), columns = ['Ticker','Returns_multiple'])
    rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True)*100
    rs_df=rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.7)]
    
    
    
    


 