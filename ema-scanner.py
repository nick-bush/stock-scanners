#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:52:01 2021

@author: nick
"""

import yfinance as yf
from yahoo_fin import stock_info as si

tickers = si.tickers_sp500()
tickers = [item.replace(".", "-") for item in tickers]

hourly_data = yf.download(tickers, period="5d", interval='60m')

# Print the data
print(hourly_data.tail())
