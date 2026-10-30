from common import *
import trimesh, json, os
from PIL import Image
OUT=".."
def tube(Y, radius=0.0025, sides=8, cmap=SEQ, size=0.30):
    """Y: (n,3) path -> trimesh tube scaled to a cube of edge `size` metres, vertex colours by time."""
    Y = np.asarray(Y, float)
    c = (Y.max(0)+Y.min(0))/2; span = (Y.max(0)-Y.min(0)).max()
    P = (Y-c)/span*size
    P = P[:, [0,2,1]]          # z-up data -> y-up glTF
    P[:,1] += size/2           # sit on the floor
    n=len(P); T=np.gradient(P,axis=0); T/=np.linalg.norm(T,axis=1,keepdims=True)+1e-12
    a=np.array([0,0,1.0]) if abs(T[0,2])<0.9 else np.array([1.0,0,0])
    N0=np.cross(T[0],a); N0/=np.linalg.norm(N0); Nn=[N0]
    for i in range(1,n):
        v=Nn[-1]-np.dot(Nn[-1],T[i])*T[i]; nv=np.linalg.norm(v)
        Nn.append(v/nv if nv>1e-9 else Nn[-1])
    Nn=np.array(Nn); B=np.cross(T,Nn)
    ang=np.linspace(0,2*np.pi,sides,endpoint=False)
    V=(P[:,None,:]+radius*(np.cos(ang)[None,:,None]*Nn[:,None,:]+np.sin(ang)[None,:,None]*B[:,None,:])).reshape(-1,3)
    F=[]
    for i in range(n-1):
        for k in range(sides):
            a0=i*sides+k; a1=i*sides+(k+1)%sides; b0=a0+sides; b1=a1+sides
            F+= [[a0,b0,a1],[a1,b0,b1]]
    col=(np.array([cmap(t) for t in np.linspace(0,1,n)])*255).astype(np.uint8)
    VC=np.repeat(col,sides,axis=0)
    m=trimesh.Trimesh(V,np.array(F),vertex_colors=VC,process=False)
    return m
def frame(size=0.30, r=0.0008):
    s=size/2; edges=[]
    pts=np.array([[x,y,z] for x in (-s,s) for y in (0,size) for z in (-s,s)])
    meshes=[]
    for i in range(8):
        for j in range(i+1,8):
            d=pts[j]-pts[i]
            if np.isclose(np.abs(d).sum(), size):
                cyl=trimesh.creation.cylinder(radius=r, segment=[pts[i],pts[j]], sections=6)
                cyl.visual.vertex_colors=[176,175,169,255]; meshes.append(cyl)
    return trimesh.util.concatenate(meshes)
def save_glb(meshes, fn):
    sc=trimesh.Scene(meshes); sc.export(fn); return os.path.getsize(fn)
meta={"gallery":[], "scrub":{}, "tunnel":{}, "landscape":{}}
# ---- model systems for the gallery
def lorenz(n=6000, dt=0.01):
    x=np.array([1.,1.,1.]); out=[]
    for i in range(n+1000):
        dx=np.array([10*(x[1]-x[0]), x[0]*(28-x[2])-x[1], x[0]*x[1]-8/3*x[2]]); x=x+dt*dx
        if i>=1000: out.append(x.copy())
    return np.array(out)[::3]
def rossler(n=8000, dt=0.02):
    x=np.array([1.,1.,1.]); out=[]
    for i in range(n+1000):
        dx=np.array([-x[1]-x[2], x[0]+0.2*x[1], 0.2+x[2]*(x[0]-5.7)]); x=x+dt*dx
        if i>=1000: out.append(x.copy())
    return np.array(out)[::4]
rng=np.random.default_rng(7); rw=np.cumsum(rng.standard_normal(250)); rwz=zscore(rw)
models={"lorenz":lorenz(),"rossler":rossler(),"randomwalk":embed(rwz,3,9)}
for k,Y in models.items():
    fn=f"{OUT}/models/{k}.glb"; sz=save_glb([tube(Y, radius=0.0018), frame()], fn)
    meta["gallery"].append(dict(id=k, file=f"models/{k}.glb", bytes=sz))
# ---- event gallery (4 positions)
for e in EV:
    n=e["asset"]; tau=P[n]["tauv"]
    for k in POSN:
        x,t0,t1=window(e,k); Y=embed(x,MV,tau)
        fn=f"{OUT}/models/{e['id']}_{k}.glb"; sz=save_glb([tube(Y), frame()], fn)
        meta["gallery"].append(dict(id=f"{e['id']}_{k}", file=f"models/{e['id']}_{k}.glb", bytes=sz, start=str(t0.date()), end=str(t1.date())))
# ---- scrubber: 16 positions from (peak-1.5W) to trough; GLB + RP png + RQA series
for e in EV:
    n=e["asset"]; tau=P[n]["tauv"]; W=P[n]["W"]; s=S[n]
    i0=max(W-1, e["pos"]["late"]-int(1.5*W)); i1=e["pos"]["crash"]
    ends=np.linspace(i0,i1,16).round().astype(int)
    frames=[]
    for j,end in enumerate(ends):
        x=zscore(s.values[end-W+1:end+1]); Y=embed(x,MV,tau); R=rp(x)
        fn=f"models/{e['id']}_s{j:02d}.glb"; sz=save_glb([tube(Y), frame()], f"{OUT}/{fn}")
        img=np.where(R[::-1]==1, 13, 255).astype(np.uint8); im=Image.fromarray(img).resize((R.shape[0]*2,)*2, Image.NEAREST)
        rpf=f"img/{e['id']}_s{j:02d}.png"; im.save(f"{OUT}/{rpf}", optimize=True)
        frames.append(dict(end=str(s.index[end].date()), start=str(s.index[end-W+1].date()), glb=fn, rp=rpf, bytes=sz))
    r=ROLL[n].loc[s.index[i0]:s.index[i1]]
    px=s.loc[s.index[i0]:s.index[i1]]
    meta["scrub"][e["id"]]=dict(label=e["label"], asset=NAME[n], frames=frames,
        series=dict(dates=[str(d.date()) for d in r.index], DET=[round(v,4) for v in r["DET"]], LAM=[round(v,4) for v in r["LAM"]], RR=[round(v,4) for v in r["RR"]], price=[round(v,2) for v in px.values]),
        peak=e["peak"], trough=e["trough"])
# ---- recurrence tunnel: 12 RP layers, textured planes with alpha
def rp_rgba(R, rgb):
    N=R.shape[0]; a=np.zeros((N,N,4),np.uint8); m=R[::-1]==1
    a[m,:3]=rgb; a[m,3]=235; return Image.fromarray(a,"RGBA")
from matplotlib.colors import to_rgb
for e in EV:
    n=e["asset"]; W=P[n]["W"]; s=S[n]
    i0=e["pos"]["early"]; i1=e["pos"]["crash"]; ends=np.linspace(i0,i1,12).round().astype(int)
    meshes=[]; L=0.24; gap=0.022
    for j,end in enumerate(ends):
        x=zscore(s.values[end-W+1:end+1]); R=rp(x)
        rgb=(np.array(SEQ(j/11)[:3])*255).astype(np.uint8)
        im=rp_rgba(R,rgb)
        quad=trimesh.Trimesh(vertices=[[-L/2,0,0],[L/2,0,0],[L/2,L,0],[-L/2,L,0]], faces=[[0,1,2],[0,2,3]], process=False)
        uv=np.array([[0,0],[1,0],[1,1],[0,1]],float)
        mat=trimesh.visual.material.PBRMaterial(baseColorTexture=im, alphaMode="BLEND", doubleSided=True, metallicFactor=0.0, roughnessFactor=1.0)
        quad.visual=trimesh.visual.TextureVisuals(uv=uv, material=mat)
        quad.apply_translation([0,0,-j*gap+11*gap/2])
        meshes.append(quad)
    fn=f"models/{e['id']}_tunnel.glb"; sz=save_glb(meshes, f"{OUT}/{fn}")
    meta["tunnel"][e["id"]]=dict(file=fn, bytes=sz, ends=[str(s.index[i].date()) for i in ends])
# ---- RQA landscape DET(t, eps) for BTC 2017-2018
d=np.load("../results/btc_det_eps.npz"); G=d["G"][:, ::2]; dates=[str(x) for x in d["dates"][::2]]
ne,nt=G.shape; Lx,Lz,H=0.42,0.16,0.10
xs=np.linspace(-Lx/2,Lx/2,nt); zs=np.linspace(Lz/2,-Lz/2,ne)
V=np.array([[xs[j], 0.003+np.nan_to_num(G[i,j])*H, zs[i]] for i in range(ne) for j in range(nt)])
Fc=[]
for i in range(ne-1):
    for j in range(nt-1):
        a=i*nt+j; b=a+1; c=a+nt; dd=c+1; Fc+=[[a,b,c],[b,dd,c]]
VC=(np.array([SEQFULL(v) for v in np.nan_to_num(G).ravel()])*255).astype(np.uint8)
surf=trimesh.Trimesh(V,np.array(Fc),vertex_colors=VC,process=False)
print('mean normal y', surf.face_normals[:,1].mean())
pk=list(dates).index(min(dates, key=lambda x: abs(pd.Timestamp(x)-pd.Timestamp(EV[4]["peak"]))))
xp=xs[pk]
plane=trimesh.creation.box(extents=[0.002,H*1.15,Lz*1.05]); plane.apply_translation([xp,H*1.15/2,0]); plane.visual.vertex_colors=[235,104,52,200]
base=trimesh.creation.box(extents=[Lx*1.02,0.002,Lz*1.05]); base.apply_translation([0,-0.001,0]); base.visual.vertex_colors=[228,227,223,255]
fn="models/BT17_landscape.glb"; sz=save_glb([surf,plane,base], f"{OUT}/{fn}")
meta["landscape"]=dict(file=fn, bytes=sz, eps=[float(v) for v in d["eps"]], start=str(dates[0]), end=str(dates[-1]))
json.dump(meta, open(f"{OUT}/data/meta.json","w"))
tot=sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(OUT) for f in fs)
print("models:", len(os.listdir(f"{OUT}/models")), "imgs:", len(os.listdir(f"{OUT}/img")), "total MB", tot/1e6)
