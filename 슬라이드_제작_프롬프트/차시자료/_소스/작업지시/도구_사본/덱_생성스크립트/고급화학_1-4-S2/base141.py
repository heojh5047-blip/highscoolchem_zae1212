HL='#FFE45C'
def alk(L,br): return build3d(L,br)
def model(cx,cy,L,br,sc=60,k=.8,yaw=0,pitch=-18,anim=None):
    at,bd=alk(L,br); return bs3d(cx,cy,at,bd,sc=sc,yaw=yaw,pitch=pitch,k=k,anim=anim)
def popa(x,y,d): return ('pop',{'o':f'{f(x)},{f(y)}','dur':'.6','delay':f'{d:.1f}'})
# ── 축약 구조식(가지를 위·아래에 쌓음): groups = 주 사슬 묶음 tex, br = [(묶음 번호, 'u'|'d', tex, 강조)]
CW={'C':.72,'H':.76,'B':.68,'r':.40,'l':.28,'O':.78,'N':.75,'=':.95,'#':.95}
def gw(t,size):
    w=0
    for ch in t: w+=(CW.get(ch,.36) if not ch.isdigit() else .38)
    return w*size
def cond(x,y,groups,br=(),size=22,hl=()):
    ws=[gw(g,size) for g in groups]; W=sum(ws); x0=x-W/2; s=[]; cs=[]
    for i,w in enumerate(ws): cs.append(x0+sum(ws[:i])+w/2)
    for i in hl: s.append(f'<rect x="{f(cs[i]-ws[i]/2-3)}" y="{f(y-size*.82)}" width="{f(ws[i]+6)}" height="{f(size*1.12)}" rx="5" fill="{HL}" fill-opacity=".45"/>')
    for (i,ud,t,h) in br:
        cx=cs[i]; yy=y-size*1.75 if ud=='u' else y+size*1.6
        if h: s.append(f'<rect x="{f(cx-gw(t,size)/2-3)}" y="{f(yy-size*.82)}" width="{f(gw(t,size)+6)}" height="{f(size*1.12)}" rx="5" fill="{HL}" fill-opacity=".45"/>')
        s.append(T(cx,yy,tex=f'\\ce{{{t}}}',size=size))
        y1,y2=(y-size*.95,yy+size*.35) if ud=='u' else (y+size*.42,yy-size*.9)
        s.append(L(cx-size*.18,y1,cx-size*.18,y2,INK,2))
    s.append(T(x,y,tex='\\ce{'+''.join(groups)+'}',size=size))
    return ''.join(s)
def skelC(cx,cy,cells,r=14,d=40,col=None):
    """탄소 골격(공 + 결합선, H 생략): cells [(c,r)] 격자, 이웃끼리 결합"""
    s=[]; P_=[(cx+a*d,cy+b*d) for a,b in cells]
    for i,(a,b) in enumerate(cells):
        for j,(c2,d2) in enumerate(cells):
            if j>i and abs(a-c2)+abs(b-d2)==1: s.append(L(*P_[i],*P_[j],'#9AA5B1',7,extra='stroke-linecap="round"'))
    for (x,y) in P_: s.append(atom(x,y,r,'C','-'))
    return ''.join(s)
def cells_canon(cells):
    ed=[(i,j) for i,(a,b) in enumerate(cells) for j,(c,d) in enumerate(cells) if j>i and abs(a-c)+abs(b-d)==1]
    assert len(ed)==len(cells)-1; return canon_edges(len(cells),ed)
def wedge(x1,y1,x2,y2,w=11):
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n,dx/n
    return f'<polygon points="{f(x1)},{f(y1)} {f(x2+px*w/2)},{f(y2+py*w/2)} {f(x2-px*w/2)},{f(y2-py*w/2)}" fill="{INK}"/>'
def hashw(x1,y1,x2,y2,w=12,k=7):
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n,dx/n; s=[]
    for i in range(1,k+1):
        t=i/(k+.4); cx,cy=x1+dx*t,y1+dy*t; hw=w/2*t
        s.append(L(cx-px*hw,cy-py*hw,cx+px*hw,cy+py*hw,INK,2))
    return ''.join(s)
def dimline(x1,y1,x2,y2,lab,off=18,size=19,side=1,lpos=.5):
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n*side,dx/n*side
    a1,b1,a2,b2=x1+px*off,y1+py*off,x2+px*off,y2+py*off
    s=L(a1,b1,a2,b2,MUTED,1.6)
    for (ax,ay,sg) in ((a1,b1,1),(a2,b2,-1)):
        ux,uy=dx/n*sg,dy/n*sg
        s+=P([(ax+ux*9+px*4,ay+uy*9+py*4),(ax,ay),(ax+ux*9-px*4,ay+uy*9-py*4)],MUTED,1.6)
    mx,my=a1+(a2-a1)*lpos+px*(size*.9),b1+(b2-b1)*lpos+py*(size*.9)
    return s+T(mx,my+size*.36,mix=lab,size=size,halo=True)
def arcA(cx,cy,a1,a2,r,lab,lr=None,size=19,col=MUTED):
    s=arc2(cx,cy,a1,a2,r,col); am=math.radians((a1+a2)/2); lr=lr or r+22
    return s+T(cx+math.cos(am)*lr,cy-math.sin(am)*lr+size*.36,tex=lab,size=size,halo=True)
def curved(x1,y1,x2,y2,bend=40,col=INK,w=2.6):
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n,dx/n
    cx,cy=mx+px*bend,my+py*bend
    tx,ty=x2-cx,y2-cy; tn=math.hypot(tx,ty); tx,ty=tx/tn,ty/tn; qx,qy=-ty,tx
    head=P([(x2-tx*11+qx*5.5,y2-ty*11+qy*5.5),(x2,y2),(x2-tx*11-qx*5.5,y2-ty*11-qy*5.5)],col,w,extra='stroke-linecap="round"')
    return f'<path d="M{f(x1)} {f(y1)} Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'+head
def harrow(x1,x2,y,lab=None,size=19,col=INK):
    s=L(x1,y,x2-4,y,col,2.6)+P([(x2-12,y-6),(x2,y),(x2-12,y+6)],col,2.6)
    if lab: s+=T((x1+x2)/2,y-12,mix=lab,size=size)
    return s
def LW(atoms,bonds,S=30,**k): return lewis(atoms,bonds,S=S,showlp=False,**k)
def H_(x,y): return A_('H',x,y)
def Cc(x,y): return A_('C',x,y)
def ring(x,y,d): return (x+d*math.cos(0),y)
