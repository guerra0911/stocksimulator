import yfinance as yf
ticker1 = yf.Ticker("DOW")
data = ticker1.history(period="max", interval="1d")  # fetches daily data
last_quote = data['Date'].iloc[-1]
second_last = data['Date'].iloc[-2]
print(last_quote)
print(second_last)
if last_quote >= second_last:
    print(1)
else:
    print(0)

