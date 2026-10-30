import yfinance as yf, pandas as pd, requests, io, sys
out = sys.argv[1]
for tic, name, start in [("^GSPC","sp500","1990-01-01"),("BTC-USD","btc","2014-09-01")]:
    df = yf.download(tic, start=start, end="2026-10-30", auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    df[["Close"]].dropna().to_csv(f"{out}/{name}.csv")
    print(name, df.index.min(), df.index.max(), len(df))
r = requests.get("https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls", timeout=60)
print("EIA status", r.status_code, len(r.content))
open(f"{out}/RBRTEd.xls","wb").write(r.content)
x = pd.read_excel(io.BytesIO(r.content), sheet_name="Data 1", skiprows=2)
x.columns = ["Date","Close"]
x = x.dropna(); x["Date"]=pd.to_datetime(x["Date"])
x.set_index("Date").to_csv(f"{out}/brent.csv")
print("brent", x.Date.min(), x.Date.max(), len(x))
