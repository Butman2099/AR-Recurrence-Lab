from common import *
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
setup()
F="../figs/"
rng = {"sp500":("2004-01-01","2021-06-30"),"brent":("2004-01-01","2021-06-30"),"btc":("2015-01-01","2021-06-30")}
fig, axs = plt.subplots(3,1, figsize=(6.3,3.9), gridspec_kw=dict(hspace=0.55))
lightc = {"sp500":"#cde2fb","brent":"#fbd9c9","btc":"#c9ecdc"}
for ax,n in zip(axs,["sp500","brent","btc"]):
    t0,t1=rng[n]; p=S[n][t0:t1]
    ax.plot(p.index,p.values,color=COL[n],lw=0.9)
    ax.set_yscale("log"); ax.set_title(NAME[n], loc="left", fontsize=8.5, fontweight="bold")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v:,.0f}")); ax.yaxis.set_minor_formatter(FuncFormatter(lambda v,_: ""))
    for e in EV:
        if e["asset"]!=n: continue
        c0,c1 = e["windows"]["calm"]
        ax.axvspan(pd.Timestamp(c0),pd.Timestamp(c1), color="#e4e3df", zorder=0, lw=0)
        ax.axvspan(pd.Timestamp(e["peak"]),pd.Timestamp(e["trough"]), color=lightc[n], zorder=0, lw=0)
        ax.plot(pd.Timestamp(e["peak"]), e["peak_px"], marker="v", color=INK, ms=4.5, zorder=3)
        ax.plot(pd.Timestamp(e["trough"]), e["trough_px"], marker="^", color=INK, ms=4.5, zorder=3)
        ax.annotate(e["id"], xy=(pd.Timestamp(e["peak"]), e["peak_px"]), xytext=(0,6), textcoords="offset points", ha="center", fontsize=6.8, fontweight="bold", color=INK)
        ax.annotate("calm", xy=(pd.Timestamp(c0)+(pd.Timestamp(c1)-pd.Timestamp(c0))/2, 0.04), xycoords=("data","axes fraction"), ha="center", fontsize=6, color=INK2)
    ax.set_xlim(pd.Timestamp(t0),pd.Timestamp(t1))
    ax.xaxis.set_major_locator(mdates.YearLocator(2 if n!="btc" else 1)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    lo,hi = ax.get_ylim(); ax.set_ylim(lo, hi*1.6)
    if n=="sp500": ax.set_yticks([1000,2000,4000])
axs[0].set_ylabel("Index points"); axs[1].set_ylabel("USD per barrel"); axs[2].set_ylabel("USD")
for ax in axs: ax.yaxis.set_label_coords(-0.1,0.5)
fig.savefig(F+"fig2_prices_events.png", dpi=300, bbox_inches="tight"); fig.savefig(F+"fig2_prices_events.pdf", bbox_inches="tight")
print("ok")
