from common import *
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, MaxNLocator
setup()
F="../figs/"
MEAS = ["RR","DET","LAM","TT","ENTR"]
PRICE_LAB = {"sp500":"S&P 500, points","brent":"Brent, USD/bbl","btc":"BTC-USD, USD"}
ev = {e["id"]:e for e in EV}
def multi_axes(ax, assets, offset=0.075):
    """host axis for the first asset, twinx axes with offset spines for the others"""
    axes=[ax]
    for i,n in enumerate(assets[1:]):
        t=ax.twinx(); axes.append(t)
        t.spines["right"].set_visible(True)
        if i>=1: t.spines["right"].set_position(("axes", 1+offset*i))
        t.grid(False)
    for a,n in zip(axes,assets):
        side = "left" if a is ax else "right"
        a.spines[side].set_color(COL[n]); a.spines[side].set_linewidth(0.9)
        a.tick_params(axis="y", colors=COL[n], labelsize=5.8, width=0.6, length=2.5, pad=1.5)
        a.yaxis.set_major_locator(MaxNLocator(3))
    return axes
def stack(assets, t0, t1, marks, fname, figsize=(6.3,5.1)):
    nrow=1+len(MEAS)
    fig, axs = plt.subplots(nrow,1, figsize=figsize, sharex=True, gridspec_kw=dict(height_ratios=[1.35]+[1]*len(MEAS), hspace=0.16))
    handles=[]
    for r,ax in enumerate(axs):
        A = multi_axes(ax, assets)
        for a,n in zip(A,assets):
            if r==0:
                p=S[n][t0:t1]; h,=a.plot(p.index,p.values,color=COL[n],ls=LS[n],lw=1.1,label=NAME[n]); handles.append(h)
                a.yaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v:,.0f}"))
            else:
                rr=ROLL[n][t0:t1]; a.plot(rr.index, rr[MEAS[r-1]].values, color=COL[n], ls=LS[n], lw=0.95)
        ax.set_ylabel("Price" if r==0 else MEAS[r-1], color=INK)
        ax.yaxis.set_label_coords(-0.085,0.5)
        for (d,lab,col,ls) in marks: ax.axvline(pd.Timestamp(d), color=col, ls=ls, lw=0.75, zorder=0)
    fig.legend(handles=handles, loc="lower center", ncol=len(assets), handlelength=2.6, fontsize=7, bbox_to_anchor=(0.5,0.0), frameon=False)
    x0,x1 = mdates.date2num(pd.Timestamp(t0)), mdates.date2num(pd.Timestamp(t1)); placed=[]
    for k,(d,lab,col,ls) in enumerate(marks):
        fx=(mdates.date2num(pd.Timestamp(d))-x0)/(x1-x0); lvl=0
        while any(abs(fx-p)<0.028 and l==lvl for p,l in placed): lvl+=1
        placed.append((fx,lvl))
        axs[0].text(fx,1.03+0.11*lvl,str(k+1),transform=axs[0].transAxes,ha="center",va="bottom",fontsize=6.5,bbox=dict(boxstyle="circle,pad=0.18",fc="white",ec=col,lw=0.8))
    axs[-1].xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,7])); axs[-1].xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y"))
    axs[-1].set_xlim(pd.Timestamp(t0), pd.Timestamp(t1))
    fig.savefig(fname+".png", dpi=300, bbox_inches="tight"); fig.savefig(fname+".pdf", bbox_inches="tight"); plt.close(fig)
marks5=[(ev["SP08"]["peak"],"",COL["sp500"],":"),(ev["BR08"]["peak"],"",COL["brent"],":"),("2008-09-15","",INK2,"--"),(ev["BR08"]["trough"],"",COL["brent"],"-."),(ev["SP08"]["trough"],"",COL["sp500"],"-.")]
stack(["sp500","brent"],"2006-01-01","2010-01-01",marks5,F+"fig5_rqa_2008")
marks6=[(ev["BR20"]["peak"],"",COL["brent"],":"),(ev["BT20"]["peak"],"",COL["btc"],":"),(ev["SP20"]["peak"],"",COL["sp500"],":"),("2020-03-11","",INK2,"--"),(ev["BR20"]["trough"],"",COL["brent"],"-.")]
stack(["sp500","brent","btc"],"2019-01-01","2020-12-31",marks6,F+"fig6_rqa_2020")
# ---------- Fig 7: BTC 2017-2018 (a) RQA stack, (b) DET(t, eps) -- separate files for subfigures
n="btc"; t0,t1="2017-01-01","2018-12-31"; s=S[n]
d=np.load("../results/btc_det_eps.npz"); G=d["G"]; dates=pd.to_datetime(d["dates"]); epsg=d["eps"]
e=ev["BT17"]; marks7=[(e["peak"],COL[n],":"),(e["trough"],COL[n],"-.")]
fig,axs=plt.subplots(6,1,figsize=(6.3,4.3),sharex=True,gridspec_kw=dict(height_ratios=[1.3,0.8,0.8,0.8,0.8,0.8],hspace=0.14))
p_=s[t0:t1]; axs[0].plot(p_.index,p_.values,color=COL[n],lw=1.1); axs[0].set_ylabel("Price, USD")
axs[0].yaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v:,.0f}"))
r=ROLL[n][t0:t1]
for i,c in enumerate(MEAS): axs[i+1].plot(r.index,r[c].values,color=COL[n],lw=1.0); axs[i+1].set_ylabel(c)
for (dd,col,ls) in marks7:
    for ax in axs: ax.axvline(pd.Timestamp(dd),color=col,ls=ls,lw=0.8,zorder=0)
for k,(dd,col,ls) in enumerate(marks7):
    axs[0].annotate(str(k+1),xy=(pd.Timestamp(dd),1.03),xycoords=("data","axes fraction"),ha="center",va="bottom",fontsize=6.5,bbox=dict(boxstyle="circle,pad=0.18",fc="white",ec=col,lw=0.8))
axs[-1].xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10])); axs[-1].xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y")); axs[-1].set_xlim(pd.Timestamp(t0),pd.Timestamp(t1))
for ax in axs: ax.yaxis.set_label_coords(-0.095,0.5)
fig.savefig(F+"fig7a_btc_rqa.png",dpi=300,bbox_inches="tight"); fig.savefig(F+"fig7a_btc_rqa.pdf",bbox_inches="tight"); plt.close(fig)
fig,axh=plt.subplots(1,1,figsize=(6.3,2.1)); X=mdates.date2num(dates)
im=axh.pcolormesh(X,epsg,G,cmap=SEQFULL,vmin=0,vmax=1,shading="nearest",rasterized=True)
axh.axhline(EPS,color="white",lw=0.8,ls="--"); axh.text(X[5],EPS+0.01,"ε = 0.1",color="white",fontsize=6.5,va="bottom")
for (dd,col,ls) in marks7: axh.axvline(pd.Timestamp(dd),color=INK,ls=ls,lw=0.8)
axh.set_ylabel("Threshold ε"); axh.grid(False); axh.yaxis.set_label_coords(-0.095,0.5)
axh.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10])); axh.xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y")); axh.set_xlim(pd.Timestamp(t0),pd.Timestamp(t1))
cb=fig.colorbar(im,ax=axh,orientation="horizontal",fraction=0.08,pad=0.30,aspect=45,shrink=0.5); cb.set_label("DET",labelpad=1); cb.outline.set_linewidth(0.4); cb.ax.tick_params(labelsize=6)
fig.savefig(F+"fig7b_btc_det_eps.png",dpi=300,bbox_inches="tight"); fig.savefig(F+"fig7b_btc_det_eps.pdf",bbox_inches="tight"); plt.close(fig)
print("ok")
