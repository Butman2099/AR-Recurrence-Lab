import numpy as np, pandas as pd
from numba import njit

def load(n):
    d = pd.read_csv(f"../prices/{n}.csv", index_col=0, parse_dates=True)["Close"].astype(float)
    return d[d>0].sort_index()

def zscore(x):
    x = np.asarray(x, float); return (x - x.mean())/x.std()

def embed(x, m, tau):
    n = len(x) - (m-1)*tau
    return np.column_stack([x[i*tau:i*tau+n] for i in range(m)])

def recmat(x, m, tau, eps):
    Y = embed(x, m, tau)
    D = np.sqrt(((Y[:,None,:]-Y[None,:,:])**2).sum(-1))   # Euclidean
    return (D <= eps).astype(np.uint8), D

@njit(cache=True)
def _rqa(R, lmin, vmin, theiler):
    N = R.shape[0]
    tot = 0
    for i in range(N):
        for j in range(N):
            if abs(i-j) >= theiler and R[i,j]:
                tot += 1
    # diagonal lines (both triangles via symmetry: count upper and double)
    dh = np.zeros(N+1, np.int64)
    for k in range(theiler, N):
        run = 0
        for i in range(N-k):
            if R[i, i+k]:
                run += 1
            else:
                if run>0: dh[run]+=1
                run = 0
        if run>0: dh[run]+=1
    vh = np.zeros(N+1, np.int64)
    for j in range(N):
        run = 0
        for i in range(N):
            if abs(i-j) >= theiler and R[i,j]:
                run += 1
            else:
                if run>0: vh[run]+=1
                run = 0
        if run>0: vh[run]+=1
    return tot, dh, vh

def rqa(R, lmin=2, vmin=2, theiler=1):
    N = R.shape[0]
    tot, dh, vh = _rqa(R, lmin, vmin, theiler)
    dh = dh*2  # symmetric RP: lower triangle mirrors upper
    L = np.arange(len(dh))
    rr = tot/(N*N - (N if theiler>0 else 0))
    if tot == 0:
        return dict(RR=0, DET=np.nan, L=np.nan, ENTR=np.nan, LAM=np.nan, TT=np.nan, Lmax=np.nan)
    dsel = L>=lmin; vsel = L>=vmin
    det = (L[dsel]*dh[dsel]).sum()/tot
    nd = dh[dsel].sum()
    Lm = (L[dsel]*dh[dsel]).sum()/nd if nd else np.nan
    p = dh[dsel]/nd if nd else np.array([])
    p = p[p>0]; ent = -(p*np.log(p)).sum() if len(p) else np.nan
    lam = (L[vsel]*vh[vsel]).sum()/tot
    nv = vh[vsel].sum()
    tt = (L[vsel]*vh[vsel]).sum()/nv if nv else np.nan
    lmax = L[dh>0].max() if (dh>0).any() else np.nan
    return dict(RR=rr, DET=det, L=Lm, ENTR=ent, LAM=lam, TT=tt, Lmax=lmax)

def ami(x, maxlag, bins=16):
    out=[]
    for k in range(maxlag+1):
        a = x[:len(x)-k]; b = x[k:]
        h,_,_ = np.histogram2d(a,b,bins=bins); p = h/h.sum()
        pa = p.sum(1, keepdims=True); pb = p.sum(0, keepdims=True)
        nz = p>0
        out.append((p[nz]*np.log(p[nz]/(pa@pb)[nz])).sum())
    return np.array(out)
