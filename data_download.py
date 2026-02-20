import yfinance as yf

data = yf.download("BTC-USD", start= "2020-01-01")
data.to_csv("btc_data.csv")
print("Downloaded data.")
