# 3-1-1 그림 도우미
import math, random

INK='#16233D'; MUTED='#5B6B7F'; FIELD='#2E9E6A'; BFIELD='#7B4FC8'; NO2C='#B5562A'
GLASS='#7E8B98'; WATER='#DDEEF8'; WATERL='#9FC3DD'

def f(v):
    s=f"{v:.1f}"
    return s[:-2] if s.endswith('.0') else s

def atom(x,y,r,el,lab='-',d=False):
    s=f'{f(x)},{f(y)},{f(r)},{el}'
    if lab is not None and lab!='': s+=','+lab
    if d: s+=',d'
    return f'<g data-atom="{s}"></g>'

def tex(x,y,t,size=20,anchor='middle',fill=None,mix=True,weight=None,halo=False,cls='',extra=''):
    a=f'<text class="tex{(" "+cls) if cls else ""}" x="{f(x)}" y="{f(y)}" {"data-mix" if mix else "data-tex"}="{t}" data-size="{size}" data-anchor="{anchor}"'
    if weight: a+=f' data-weight="{weight}"'
    if halo: a+=' data-halo="1"'
    if fill: a+=f' fill="{fill}"'
    if extra: a+=' '+extra
    return a+'></text>'

def arw(x1,y1,x2,y2,col='ink',w=3,dash=False,extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}{",d" if dash else ""}"{(" "+extra) if extra else ""}></g>'

def no2(x,y,r=12,th=-90,lab=False):
    """N at (x,y); O's toward direction th(deg) ±67."""
    d=1.35*r; out=''
    for s in (-67,67):
        a=math.radians(th+s)
        out+=atom(x+d*math.cos(a),y+d*math.sin(a),r,'O','' if lab else '-')
    out+=atom(x,y,r,'N','' if lab else '-')
    return out

def n2o4(x,y,r=12,th=0,lab=False):
    """axis direction th; N–N centered at (x,y)."""
    dNN=1.45*r; d=1.35*r; out=''; ns=''
    for side in (-1,1):
        ax=math.radians(th); nx=x+side*dNN/2*math.cos(ax); ny=y+side*dNN/2*math.sin(ax)
        base=th if side==1 else th+180
        for s in (-62,62):
            a=math.radians(base+s)
            out+=atom(nx+d*math.cos(a),ny+d*math.sin(a),r,'O','' if lab else '-')
        ns+=atom(nx,ny,r,'N','' if lab else '-')
    return out+ns

def h2o(x,y,rO=12,rH=8,th=90,lab=False,d=None):
    d=d or 1.05*rO; out=''
    for s in (-52.25,52.25):
        a=math.radians(th+s)
        out+=atom(x+d*math.cos(a),y+d*math.sin(a),rH,'H','' if lab else '-')
    return out+atom(x,y,rO,'O','' if lab else '-')

def place(n,box,mind,seed=1,avoid=()):
    x0,y0,x1,y1=box; rnd=random.Random(seed); pts=[]
    tries=0
    while len(pts)<n and tries<20000:
        tries+=1
        p=(rnd.uniform(x0,x1),rnd.uniform(y0,y1))
        if all(math.hypot(p[0]-q[0],p[1]-q[1])>=mind for q in pts+list(avoid)): pts.append(p)
    assert len(pts)==n, (n,len(pts))
    return pts

def hexagon(x,y,r=9,fill='#F3E9C6',stroke='#B59A4A'):
    pts=' '.join(f'{f(x+r*math.cos(math.radians(60*i+30)))},{f(y+r*math.sin(math.radians(60*i+30)))}' for i in range(6))
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'

def eqarrows(x,y,L,gap=7,lab_top=None,lab_bot=None,size=19,w=3):
    """가역 화살표: 위 → (field), 아래 ← (bfield), 반쪽 화살촉."""
    hx=11; hy=7
    top=f'<path d="M{f(x)} {f(y-gap)} H{f(x+L)} l{-hx} {-hy}" fill="none" stroke="{FIELD}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    bot=f'<path d="M{f(x+L)} {f(y+gap)} H{f(x)} l{hx} {hy}" fill="none" stroke="{BFIELD}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    s=top+bot
    if lab_top: s+=tex(x+L/2,y-gap-10,lab_top,size,fill=FIELD,weight=700)
    if lab_bot: s+=tex(x+L/2,y+gap+size+8,lab_bot,size,fill=BFIELD,weight=700)
    return s

def jar(x,y,w,h,tint=None,op=0,stop=True):
    """밀폐 용기: 둥근 사각 + 마개. (x,y)=왼쪽 위."""
    s=''
    if tint: s+=f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="18" fill="{tint}" fill-opacity="{op}"/>'
    s+=f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="18" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    if stop: s+=f'<rect x="{f(x+w/2-26)}" y="{f(y-14)}" width="52" height="20" rx="4" fill="#C9B79C" stroke="#8C7A5E" stroke-width="2"/>'
    return s

def curve_pts(fn,x0,x1,n=60):
    return [(x0+(x1-x0)*i/n, fn(i/n)) for i in range(n+1)]

def path(pts):
    return 'M'+' L'.join(f'{f(a)} {f(b)}' for a,b in pts)
