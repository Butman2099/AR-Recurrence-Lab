from common import *
for n,p in P.items():
    s=S[n].values; W=p["W"]; rows=[]
    for t in range(W, len(s)+1):
        q=rqa(rp(zscore(s[t-W:t]))); q["date"]=S[n].index[t-1]; rows.append(q)
    df=pd.DataFrame(rows).set_index("date"); df.to_csv(f"../results/rqa_{n}.csv"); print(n,len(df), "median RR %.3f DET %.2f LAM %.2f TT %.2f ENTR %.2f"%tuple(df[c].median() for c in ["RR","DET","LAM","TT","ENTR"]))
# window values
out=[]
for e in EV:
    d={k:rqa(rp(window(e,k)[0])) for k in POSN}
    out.append(dict(id=e["id"], vals={k:{m:float(v) for m,v in d[k].items()} for k in POSN}))
json.dump(out, open("../results/window_rqa.json","w"), indent=1)
# DET(t,eps) for BTC 2017-2018
n="btc"; W=P[n]["W"]; s=S[n]; idx=np.where((s.index>="2017-01-01")&(s.index<="2018-12-31"))[0]
epsg=np.round(np.arange(0.02,0.401,0.02),2); G=np.zeros((len(epsg),len(idx)))
for j,t in enumerate(idx):
    x=zscore(s.values[t-W+1:t+1]); D=np.abs(x[:,None]-x[None,:])
    for i,e in enumerate(epsg): G[i,j]=rqa((D<=e).astype(np.uint8))["DET"]
np.savez("../results/btc_det_eps.npz", G=G, eps=epsg, dates=s.index[idx].values.astype("datetime64[D]").astype(str))
print("done")
