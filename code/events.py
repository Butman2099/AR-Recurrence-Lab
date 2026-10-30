"""Identify the six crash events (peak, trough, calm window, window positions) -> ../results/events.json"""
import sys, json; sys.path.insert(0, '.')
from rqa_core import *
W = {"sp500": 250, "brent": 250, "btc": 100}
EVENTS = [  # id, asset, search interval for the peak, label, origin
    ("SP08", "sp500", "2007-01-01", "2008-01-31", "Global financial crisis", "endogenous"),
    ("SP20", "sp500", "2020-01-01", "2020-03-01", "COVID-19 crash", "exogenous"),
    ("BR08", "brent", "2008-01-01", "2008-12-31", "Oil price collapse 2008", "mixed"),
    ("BR20", "brent", "2019-12-01", "2020-02-28", "COVID-19 oil crash", "exogenous"),
    ("BT17", "btc", "2017-10-01", "2018-01-15", "Bitcoin bubble burst", "endogenous"),
    ("BT20", "btc", "2020-01-15", "2020-03-05", "COVID-19 crash", "exogenous"),
]
cat = []
for eid, n, a, b, lab, orig in EVENTS:
    px = load(n); s = np.log(px); w = W[n]
    pk = px[a:b].idxmax(); ipk = px.index.get_loc(pk)
    seg = px.iloc[ipk:ipk + int(1.5 * w) + 1]; tr = seg.idxmin(); itr = px.index.get_loc(tr)  # trough within 1.5W after the peak
    r = s.diff(); best = None
    for e in range(max(w, ipk - 3 * w), ipk - w + 1):  # calm window: lowest volatility, ending in [t_p-3W, t_p-W]
        sd = r.iloc[e - w + 1:e + 1].std()
        if best is None or sd < best[0]: best = (sd, e)
    pos = {"calm": best[1], "early": ipk - w // 2, "late": ipk, "crash": itr}
    win = {k: (str(px.index[e - w + 1].date()), str(px.index[e].date())) for k, e in pos.items()}
    cat.append(dict(id=eid, asset=n, label=lab, origin=orig, peak=str(pk.date()), peak_px=float(px[pk]),
                    trough=str(tr.date()), trough_px=float(px[tr]), dd=float(px[tr] / px[pk] - 1), dur_obs=int(itr - ipk),
                    windows=win, pos={k: int(e) for k, e in pos.items()}))
    print(eid, pk.date(), tr.date(), f"{(px[tr] / px[pk] - 1) * 100:.1f}%")
json.dump(cat, open("../results/events.json", "w"), indent=1)
