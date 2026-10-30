from common import *
from mpl_toolkits.mplot3d.art3d import Line3DCollection
setup()
COLLAB = {"SP08":"S&P 500\n2007–2009","BR08":"Brent\n2008","BT17":"BTC-USD\n2017–2018","SP20":"S&P 500\n2020","BR20":"Brent\n2020","BT20":"BTC-USD\n2020"}
order = ["SP08","BR08","BT17","SP20","BR20","BT20"]
ROWLAB = {"calm":"Calm","early":"Early\npre-crash","late":"Late\npre-crash","crash":"Crash"}
evs = {e["id"]:e for e in EV}
F="../figs/"
# ---- phase portraits: rows = positions, columns = events
fig = plt.figure(figsize=(6.3,4.55))
gs = fig.add_gridspec(4,6, left=0.085, right=0.998, top=0.93, bottom=0.005, wspace=0.0, hspace=0.02)
for c,eid in enumerate(order):
    e=evs[eid]; n=e["asset"]; tau=P[n]["tauv"]
    for r,k in enumerate(POSN):
        x,t0,t1 = window(e,k); Y=embed(x,MV,tau)
        ax = fig.add_subplot(gs[r,c], projection="3d")
        seg = np.stack([Y[:-1],Y[1:]],axis=1)
        ax.add_collection3d(Line3DCollection(seg, colors=SEQ(np.linspace(0,1,len(seg))), linewidths=0.6))
        L=max(2.2, np.abs(Y).max()*1.02); ax.set_xlim(-L,L); ax.set_ylim(-L,L); ax.set_zlim(-L,L)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        for a in (ax.xaxis, ax.yaxis, ax.zaxis):
            a.set_pane_color((0.97,0.97,0.96,1)); a._axinfo["grid"]["color"]=(0.9,0.9,0.9,1); a.line.set_color("#b0afa9"); a.line.set_linewidth(0.4)
        ax.view_init(24,-52); ax.set_box_aspect((1,1,1), zoom=1.25)
        if r==0: ax.set_title(COLLAB[eid], fontsize=6.8, pad=-2)
        if c==0: ax.text2D(-0.08,0.5, ROWLAB[k], transform=ax.transAxes, ha="center", va="center", rotation=90, fontsize=6.8)
fig.savefig(F+"fig3_phase_portraits.png", dpi=300); fig.savefig(F+"fig3_phase_portraits.pdf"); plt.close(fig)
# ---- recurrence plots
fig = plt.figure(figsize=(6.3,4.75))
gs = fig.add_gridspec(4,6, left=0.085, right=0.998, top=0.93, bottom=0.03, wspace=0.10, hspace=0.30)
cm = plt.matplotlib.colors.ListedColormap(["#ffffff","#0d366b"])
for c,eid in enumerate(order):
    e=evs[eid]
    for r,k in enumerate(POSN):
        x,t0,t1 = window(e,k); R=rp(x); N=R.shape[0]; q=rqa(R)
        ax = fig.add_subplot(gs[r,c])
        ax.imshow(R, cmap=cm, origin="lower", interpolation="nearest", extent=(0,N,0,N))
        ax.grid(False); ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(True); sp.set_color("#b0afa9"); sp.set_linewidth(0.4)
        ax.set_xlabel(f"DET = {q['DET']:.2f}", fontsize=5.6, color=INK2, labelpad=1.5)
        if r==0: ax.set_title(COLLAB[eid], fontsize=6.8, pad=3)
        if c==0: ax.set_ylabel(ROWLAB[k], fontsize=6.8, labelpad=3)
fig.savefig(F+"fig4_recurrence_plots.png", dpi=300); fig.savefig(F+"fig4_recurrence_plots.pdf"); plt.close(fig)
print("ok")
