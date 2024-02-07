import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import time
import warnings

# Ignore FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

start_date = '2023-01-01'
end_date = "2023-10-31"

# Record the time at the start of the program
start_time = time.time()

# Fetching the S&P 500 components
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]

# Extracting the tickers
tickers = df['Symbol'].tolist()
# Remove problematic tickers
tickers_to_remove = ['BRK.B', 'BF.B']
tickers = [ticker for ticker in tickers if ticker not in tickers_to_remove]

# Creating an empty DataFrame
hist_all = pd.DataFrame()
meta_all = pd.DataFrame()
actions_all = pd.DataFrame()
shares_all = pd.DataFrame()
inc_stmt_all = pd.DataFrame()
bal_sheet_all = pd.DataFrame()
cf_stmt_all = pd.DataFrame()
maj_hold_all = pd.DataFrame()
inst_hold_all = pd.DataFrame()
mut_hold_all = pd.DataFrame()

# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:ferrari11@localhost:5432/GUERRA')

# Downloading data for all tickers
download_start_time = time.time()

for i, ticker in enumerate(tickers, start=1):
    stock = yf.Ticker(ticker)

    # History
    hist = yf.download(ticker, start=start_date, end=end_date)
    if hist.empty:
        print(f"No history data for {ticker}, skipping...")
        continue
    hist['ticker'] = ticker
    hist.reset_index(inplace=True)
    hist_all = pd.concat([hist_all, hist])

    # MetaData
    prereq = stock.history(period="1y")
    meta = stock.history_metadata
    if meta is None:
        print(f"No metadata for {ticker}, skipping...")
        continue
    meta_df = pd.json_normalize(meta)
    meta_df['ticker'] = ticker
    meta_all = pd.concat([meta_all, meta_df])

    # Actions (Dividends & Splits)
    actions = stock.actions
    if actions.empty:
        print(f"No actions data for {ticker}, skipping...")
        continue
    actions['ticker'] = ticker  
    actions.reset_index(inplace=True)  
    actions_all = pd.concat([actions_all, actions])

    # Shares
    shares = stock.get_shares_full(start=start_date, end=end_date)
    if shares.empty:
        print(f"No shares data for {ticker}, skipping...")
        continue
    shares = shares.to_frame(name='Shares') 
    shares['ticker'] = ticker  
    shares.reset_index(inplace=True) 
    shares_all = pd.concat([shares_all, shares])

    # Income Statement
    inc_stmt = stock.income_stmt
    if inc_stmt.empty:
        print(f"No income statement data for {ticker}, skipping...")
        continue
    inc_stmt['ticker'] = ticker
    inc_stmt.reset_index(inplace=True)
    inc_stmt = inc_stmt.melt(id_vars=['index', 'ticker'], var_name='Date', value_name='Value')  # Reshape the DataFrame
    inc_stmt_all = pd.concat([inc_stmt_all, inc_stmt])

    # Balance Sheet
    bal_sheet = stock.balance_sheet
    if bal_sheet.empty:
        print(f"No balance sheet data for {ticker}, skipping...")
        continue
    bal_sheet['ticker'] = ticker
    bal_sheet.reset_index(inplace=True)
    bal_sheet = bal_sheet.melt(id_vars=['index', 'ticker'], var_name='Date', value_name='Value')  # Reshape the DataFrame
    bal_sheet_all = pd.concat([bal_sheet_all, bal_sheet])

    # Cash Flow Statement
    cf_stmt = stock.cash_flow
    if cf_stmt.empty:
        print(f"No cash flow statement data for {ticker}, skipping...")
        continue
    cf_stmt['ticker'] = ticker
    cf_stmt.reset_index(inplace=True)
    cf_stmt = cf_stmt.melt(id_vars=['index', 'ticker'], var_name='Date', value_name='Value')  # Reshape the DataFrame
    cf_stmt_all = pd.concat([cf_stmt_all, cf_stmt])

    # Major Holders
    try:
        maj_hold = stock.major_holders
        if maj_hold is None:
            print(f"No major holders data for {ticker}, skipping...")
            continue
        maj_hold['ticker'] = ticker
        maj_hold.reset_index(inplace=True)
        maj_hold_all = pd.concat([maj_hold_all, maj_hold])
    except ValueError:
        print(f"Skipping major holders data for {ticker} due to ValueError")
        continue

    # Institutional Holders
    try:
        inst_hold = stock.institutional_holders
        if inst_hold is None:
            print(f"No institutional holders data for {ticker}, skipping...")
            continue
        inst_hold['ticker'] = ticker
        inst_hold.reset_index(inplace=True)
        inst_hold_all = pd.concat([inst_hold_all, inst_hold])
    except ValueError:
        print(f"Skipping major holders data for {ticker} due to ValueError")
        continue

    # Mutual Fund Holders
    try:
        mut_hold = stock.mutualfund_holders
        if mut_hold is None:
            print(f"No mutual fund holders data for {ticker}, skipping...")
            continue
        mut_hold['ticker'] = ticker
        mut_hold.reset_index(inplace=True)
        mut_hold_all = pd.concat([mut_hold_all, mut_hold])
    except ValueError:
        print(f"Skipping major holders data for {ticker} due to ValueError")
        continue

    # Print the iteration number
    print(f"Completed: {i} out of {len(tickers)}")

download_end_time = time.time()
download_time = download_end_time - download_start_time
download_minutes, download_seconds = divmod(download_end_time - download_start_time, 60)

# Storing the data in the PostgreSQL database
storing_start_time = time.time()

hist_all.to_sql('History', engine, if_exists='append')
meta_all.to_sql('Metadata', engine, if_exists='append')
actions_all.to_sql('Actions', engine, if_exists='append')
shares_all.to_sql('Shares', engine, if_exists='append')
inc_stmt_all.to_sql('IncStmt', engine, if_exists='append')
bal_sheet_all.to_sql('BalSheet', engine, if_exists='append')
cf_stmt_all.to_sql('CashFlowStmt', engine, if_exists='append')
maj_hold_all.to_sql('MajorHolders', engine, if_exists='append')
inst_hold_all.to_sql('InstitutionalHolders', engine, if_exists='append')
mut_hold_all.to_sql('MutualFundHolders', engine, if_exists='append')

storing_end_time = time.time()
storing_minutes, storing_seconds = divmod(storing_end_time - storing_start_time, 60)

# Close the connection
engine.dispose()

end_minutes, end_seconds = divmod(time.time() - start_time, 60)

print(f"Download Time: {download_minutes:.0f} minutes {download_seconds:.2f} seconds \n")
print(f"Total Storing Time: {storing_minutes:.0f} minutes {storing_seconds:.2f} seconds \n")
print(f"Total Time: {end_minutes:.0f} minutes {end_seconds:.2f} seconds \n")