from statsmodels.regression.rolling import RollingOLS
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import datetime as dt
import yfinance as yf
import pandas_ta
import warnings
import requests
warnings.filterwarnings("ignore")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# Use requests to fetch the page content with the header
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url, headers=headers)


sp500 = pd.read_html(response.text)[0]
sp500['Symbol'] = sp500['Symbol'].str.replace('.','-')

symbols_list = sp500['Symbol'].unique().tolist()
symbols_list