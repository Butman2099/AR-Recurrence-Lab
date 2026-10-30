import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
COL = {"sp500":"#2a78d6","brent":"#eb6834","btc":"#199e70"}
LS  = {"sp500":"-","brent":"--","btc":"-."}
NAME= {"sp500":"S&P 500","brent":"Brent","btc":"BTC-USD"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SEQ = LinearSegmentedColormap.from_list("seqblue", ["#b7d3f6","#86b6ef","#3987e5","#256abf","#184f95","#0d366b"])
SEQFULL = LinearSegmentedColormap.from_list("seqfull", ["#fcfcfb","#cde2fb","#9ec5f4","#6da7ec","#3987e5","#256abf","#184f95","#0d366b"])
def setup():
    plt.rcParams.update({
        "font.family":"DejaVu Sans","font.size":8,"axes.titlesize":8.5,"axes.labelsize":7.5,
        "xtick.labelsize":7,"ytick.labelsize":7,"legend.fontsize":7,
        "axes.edgecolor":INK2,"axes.linewidth":0.6,"axes.labelcolor":INK,"text.color":INK,
        "xtick.color":INK2,"ytick.color":INK2,"xtick.major.width":0.5,"ytick.major.width":0.5,
        "axes.grid":True,"grid.color":GRID,"grid.linewidth":0.5,"axes.spines.top":False,"axes.spines.right":False,
        "savefig.dpi":300,"figure.dpi":110,"lines.linewidth":1.2,"legend.frameon":False})
