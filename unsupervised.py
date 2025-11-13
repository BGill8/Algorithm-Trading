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

end_date = '2025-10-31'
start_date = pd.to_datetime(end_date) - dt.timedelta(days=365*10) #last 10 years
df = yf.download(symbols_list, start=start_date, end=end_date)

df

df['garman-klass_vol'] = ((np.log(df['high'])-np.log(df['low']))**2)/2 - ((2*np.log(2)-1) * (np.log(df['close'])-(np.log(df['open']))**2))