import yfinance as yf
ticker1 = yf.Ticker("DOW")
data = ticker1.history()
last_quote = data['Close'].iloc[-1]
second_last = data['Close'].iloc[-2]
print(last_quote)
print(second_last)
if last_quote >= second_last:
    print(1)
else:
    print(0)

