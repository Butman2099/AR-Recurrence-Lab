import sys, json; sys.path.insert(0,'.')
from rqa_core import *; from style import *
# RQA parameters (v2): standardised prices, m=1, tau=1, eps=0.1
P = {"sp500":dict(W=250,tauv=9),"brent":dict(W=250,tauv=10),"btc":dict(W=100,tauv=5)}
M, TAU, EPS = 1, 1, 0.1
MV = 3   # embedding dimension for 3D phase portraits (visualisation only, delay tauv)
EV = json.load(open("../results/events.json"))
S = {n: load(n) for n in P}            # raw prices
ROLL = {}
import os
for n in P:
    f=f"../results/rqa_{n}.csv"
    if os.path.exists(f): ROLL[n]=pd.read_csv(f, index_col=0, parse_dates=True)
POSN = ["calm","early","late","crash"]
POSLAB = {"calm":"Calm","early":"Early pre-crash","late":"Late pre-crash","crash":"Crash"}
def window(e, k):
    n=e["asset"]; W=P[n]["W"]; end=e["pos"][k]
    return zscore(S[n].values[end-W+1:end+1]), S[n].index[end-W+1], S[n].index[end]
def rp(x): return recmat(x, M, TAU, EPS)[0]
