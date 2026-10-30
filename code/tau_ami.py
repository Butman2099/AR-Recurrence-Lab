import sys; sys.path.insert(0,'.')
from rqa_core import *
W = {"sp500":250,"brent":250,"btc":100}
for n in W:
    s = load(n); w = W[n]; fm=[]
    for t in range(w, len(s), 50):
        x = zscore(s.values[t-w:t]); a = ami(x, w//4, bins=8)
        d = np.diff(a); f = np.argmax(d>0) if (d>0).any() else -1
        if f>0: fm.append(f)
    print(n, "AMI first-min median", np.median(fm))
