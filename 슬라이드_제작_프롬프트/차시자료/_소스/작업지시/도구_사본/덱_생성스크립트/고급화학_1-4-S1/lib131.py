OX='#C2410C'; LO2='#BFDDF5'
def atom(x,y,r,el,lab=None,d=False):
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+(',d' if d else '')+'"></g>'
def step(body,g=None,extra=''):
    return f'<g class="step"'+(f' data-g="{g}"' if g else '')+(f' {extra}' if extra else '')+'>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def harp(cx,y,h,up,col=INK,w=2.6):
    if up: return P([(cx,y+h-6),(cx,y+6),(cx-6,y+14)],col,w,extra='stroke-linecap="round"')
    return P([(cx,y+6),(cx,y+h-6),(cx+6,y+h-14)],col,w,extra='stroke-linecap="round"')
def ebox(x,y,occ,w=36,h=36,new=(),lab=None,lsize=20,hund=True):
    s=[]
    for i,o in enumerate(occ):
        bx=x+i*w
        fill=f'fill="{EQUI}" fill-opacity=".18"' if (hund and len(o)==1) else 'fill="#fff"'
        s.append(f'<rect x="{f(bx)}" y="{f(y)}" width="{w}" height="{h}" {fill} stroke="{INK}" stroke-width="1.5"/>')
        cx=bx+w/2; xs=[cx] if len(o)==1 else [cx-6,cx+6]
        for j,ch in enumerate(o): s.append(harp(xs[j],y,h,ch=='u',FIELD if (i,ch) in new else INK))
    if lab: s.append(T(x-10,y+h/2+lsize*0.36,tex=lab,size=lsize,anchor='end'))
    return ''.join(s)
def dlev(x,y,occ,LW=34,gap=12,col=INK,line=True):
    n=len(occ); W=n*LW+(n-1)*gap; x0=x-W/2; s=[]
    for i,o in enumerate(occ):
        a=x0+i*(LW+gap)
        if line: s.append(L(a,y,a+LW,y,col,2.6))
        cx=a+LW/2; xs=[cx] if len(o)==1 else [cx-6,cx+6]
        for j,ch in enumerate(o): s.append(harp(xs[j],y-17,34,ch=='u'))
    return ''.join(s)
def an(kind,body,**kw):
    a=f'data-anim="{kind}"'+''.join(f' data-{k.replace("_","-")}="{v}"' for k,v in kw.items())
    return G(body,a)
def arc2(cx,cy,a1,a2,r,col=MUTED,w=2.2):
    pts=[(cx+r*math.cos(math.radians(a1+(a2-a1)*k/24)),cy-r*math.sin(math.radians(a1+(a2-a1)*k/24))) for k in range(25)]
    return P(pts,col,w)

# ═════ 3차원 도우미 ═════
def norm3(v):
    l=math.sqrt(sum(c*c for c in v)); return tuple(c/l for c in v)
def rot3(v,yaw=25,pitch=-16):
    x,y,z=v; a=math.radians(yaw)
    x,z=x*math.cos(a)+z*math.sin(a),-x*math.sin(a)+z*math.cos(a)
    b=math.radians(pitch); y,z=y*math.cos(b)-z*math.sin(b),y*math.sin(b)+z*math.cos(b)
    return (x,y,z)
RT=math.sqrt(8)/3
TET=[(0,1,0)]+[(RT*math.sin(math.radians(p)),-1/3,RT*math.cos(math.radians(p))) for p in (0,120,240)]
def trig(ang):
    """(3,1) 삼각뿔 결합 방향 — 결합각 ang, 비공유 전자쌍은 +y"""
    c=(math.cos(math.radians(ang))+.5)/1.5; al=math.acos(math.sqrt(c))
    return [(math.sin(al)*math.sin(math.radians(p)),-math.cos(al),math.sin(al)*math.cos(math.radians(p))) for p in (0,120,240)]
def bent(ang):
    h=math.radians(ang/2)
    return [(-math.sin(h),-math.cos(h),0),(math.sin(h),-math.cos(h),0)],[norm3((0,.62,.78)),norm3((0,.62,-.78))]
RA={'H':18,'C':24,'N':24,'O':24,'F':24,'B':24,'Be':24}
def bs3d(cx,cy,atoms,bonds,sc=80,yaw=25,pitch=-16,k=1.0,labels=True,arcs=(),lone=(),arc_r=34,arc_size=20,anim=None):
    """atoms: [(el,(x,y,z) Å)], bonds: [(i,j,order)], arcs: [(i,c,j,label,g)], lone: [(c,dir)], k: 원자 반지름 배율"""
    pr=[]
    for el,v in atoms:
        X,Y,Z=rot3(v,yaw,pitch); pr.append((cx+X*sc,cy-Y*sc,Z))
    items=[]
    for (i,j,o) in bonds:
        (x1,y1,z1),(x2,y2,z2)=pr[i],pr[j]; dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy) or 1; px,py=-dy/n,dx/n
        offs={1:[0],2:[-4.5*k,4.5*k],3:[-7*k,0,7*k]}[o]
        sv=''.join(f'<line x1="{f(x1+px*t)}" y1="{f(y1+py*t)}" x2="{f(x2+px*t)}" y2="{f(y2+py*t)}" stroke="{BOND}" stroke-width="{f((7 if o==1 else 5)*k)}" stroke-linecap="round"/>' for t in offs)
        items.append(((z1+z2)/2-0.001,sv))
    for (c,d) in lone:
        X,Y,Z=rot3(norm3(d),yaw,pitch); ll=sc*0.78; ex,ey=X*ll,-Y*ll; pl=math.hypot(ex,ey)
        x0,y0,_=pr[c]; ang=math.degrees(math.atan2(ey,ex)); ccx,ccy=x0+ex*.62,y0+ey*.62
        sv=f'<ellipse cx="{f(ccx)}" cy="{f(ccy)}" rx="{f(max(pl*.62,20*k))}" ry="{f(21*k)}" transform="rotate({f(ang)} {f(ccx)} {f(ccy)})" fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="1.5"/>'
        ux,uy=(ex/pl,ey/pl) if pl>1e-6 else (1,0); tip=.85 if pl>8 else 0; bx,by=x0+ex*tip,y0+ey*tip
        sv+=''.join(f'<circle cx="{f(bx-uy*6*k*s_)}" cy="{f(by+ux*6*k*s_)}" r="{f(3.6*k+.4)}" fill="{INK}"/>' for s_ in (-1,1))
        items.append((Z*.6+pr[c][2],sv))
    for n_,(el,v) in enumerate(atoms):
        x,y,z=pr[n_]; r=RA[el]*k
        items.append((z+0.002,atom(x,y,r,el,None if (labels and r>=17.9) else '-')))
    items.sort(key=lambda t:t[0])
    out=''.join(s for _,s in items)
    if anim: out=an(anim[0],out,**anim[1])
    for (i,c,j,lab,g) in arcs:
        a=norm3(tuple(p-q for p,q in zip(atoms[i][1],atoms[c][1]))); b=norm3(tuple(p-q for p,q in zip(atoms[j][1],atoms[c][1])))
        om=math.acos(max(-1,min(1,sum(p*q for p,q in zip(a,b))))); pts=[]
        for t in [q/24 for q in range(25)]:
            if abs(om-math.pi)<1e-3:
                perp=(0,1,0); v=tuple(a[m]*math.cos(math.pi*t)+perp[m]*math.sin(math.pi*t) for m in range(3))
            else:
                s1=math.sin((1-t)*om)/math.sin(om); s2=math.sin(t*om)/math.sin(om); v=tuple(s1*a[m]+s2*b[m] for m in range(3))
            X,Y,Z=rot3(v,yaw,pitch); pts.append((pr[c][0]+X*arc_r,pr[c][1]-Y*arc_r))
        mid=pts[12]; vx,vy=mid[0]-pr[c][0],mid[1]-pr[c][1]; n=math.hypot(vx,vy) or 1
        lx,ly=pr[c][0]+vx/n*(n+24),pr[c][1]+vy/n*(n+24)
        sv=P(pts,MUTED,2.2)+T(lx,ly+7,tex=lab,size=arc_size,halo=True)
        out+=step(sv,g) if g else sv
    return out
def mol(name):
    """분자 좌표(Å)와 결합"""
    if name=='CH4': return [('C',(0,0,0))]+[('H',tuple(1.09*c for c in d)) for d in TET],[(0,i,1) for i in range(1,5)],[]
    if name=='BH4': return [('B',(0,0,0))]+[('H',tuple(1.19*c for c in d)) for d in TET],[(0,i,1) for i in range(1,5)],[]
    if name=='NH3': return [('N',(0,0,0))]+[('H',tuple(1.01*c for c in d)) for d in trig(107)],[(0,i,1) for i in range(1,4)],[(0,(0,1,0))]
    if name=='NF3': return [('N',(0,0,0))]+[('F',tuple(1.37*c for c in d)) for d in trig(102)],[(0,i,1) for i in range(1,4)],[(0,(0,1,0))]
    if name=='H2O':
        bd,ld=bent(104.5); return [('O',(0,0,0))]+[('H',tuple(0.96*c for c in d)) for d in bd],[(0,1,1),(0,2,1)],[(0,d) for d in ld]
    if name=='BeH2': return [('Be',(0,0,0)),('H',(-1.33,0,0)),('H',(1.33,0,0))],[(0,1,1),(0,2,1)],[]
    if name=='C2H6':
        at=[('C',(-0.77,0,0)),('C',(0.77,0,0))]; bd=[(0,1,1)]
        c_,s_=math.cos(math.radians(111)),math.sin(math.radians(111))
        for p in (90,210,330): at.append(('H',(-0.77-1.09*c_,1.09*s_*math.cos(math.radians(p)),1.09*s_*math.sin(math.radians(p))))); bd.append((0,len(at)-1,1))
        for p in (30,150,270): at.append(('H',(0.77+1.09*c_,1.09*s_*math.cos(math.radians(p)),1.09*s_*math.sin(math.radians(p))))); bd.append((1,len(at)-1,1))
        return at,bd,[]
    if name=='C2H4':
        a=math.radians(58.5); at=[('C',(-0.67,0,0)),('C',(0.67,0,0))]
        for sx in (-1,1):
            for sy in (1,-1): at.append(('H',(sx*(0.67+1.09*math.cos(a)),sy*1.09*math.sin(a),0)))
        return at,[(0,1,2),(0,2,1),(0,3,1),(1,4,1),(1,5,1)],[]
    if name=='C2H2': return [('C',(-0.6,0,0)),('C',(0.6,0,0)),('H',(-1.66,0,0)),('H',(1.66,0,0))],[(0,1,3),(0,2,1),(1,3,1)],[]
    if name=='BF3': return [('B',(0,0,0))]+[('F',(1.31*math.cos(math.radians(a)),1.31*math.sin(math.radians(a)),0)) for a in (90,210,330)],[(0,i,1) for i in range(1,4)],[]
    if name=='CO2': return [('C',(0,0,0)),('O',(-1.16,0,0)),('O',(1.16,0,0))],[(0,1,2),(0,2,2)],[]
    raise ValueError(name)

def lobe3(cx,cy,d,L,sign,W=0.62,yaw=25,pitch=-16,opa=.30,lab=True,lsize=19,dash=None,minL=.42):
    """3차원 방향 d의 엽(눈물방울) — (깊이, svg)"""
    X,Y,Z=rot3(norm3(d),yaw,pitch); k=math.hypot(X,Y); ux,uy=(X/k,-Y/k) if k>1e-6 else (1,0); px,py=-uy,ux
    Ls=L*max(k,minL); pts=[]
    for i in range(61):
        th=math.radians(-90+3*i); rho=Ls*math.cos(th)**2
        a=rho*math.cos(th); b=W*L*math.cos(th)**2*math.sin(th)
        pts.append((cx+ux*a+px*b,cy+uy*a+py*b))
    col=BF if sign>0 else GRAV
    sv=P(pts,col,1.8,fill=col,close=True,dash=dash,extra=f'fill-opacity="{opa}"'+(' stroke-opacity=".55"' if opa<.25 else ''))
    if lab: sv+=T(cx+ux*Ls*0.58,cy+uy*Ls*0.58+lsize*0.36,tex='+' if sign>0 else '-',size=lsize,weight=700)
    return (Z,sv)
def hybrid(cx,cy,d,L,yaw=25,pitch=-16,lab=True,back=True,lsize=19):
    out=[lobe3(cx,cy,d,L,1,yaw=yaw,pitch=pitch,lab=lab,lsize=lsize)]
    if back: out.append(lobe3(cx,cy,tuple(-c for c in d),L*0.36,-1,W=0.9,yaw=yaw,pitch=pitch,lab=False))
    return out
def porb(cx,cy,d,L,yaw=25,pitch=-16,opa=.30,lab=True,lsize=19,W=0.62):
    return [lobe3(cx,cy,d,L,1,W=W,yaw=yaw,pitch=pitch,opa=opa,lab=lab,lsize=lsize),lobe3(cx,cy,tuple(-c for c in d),L,-1,W=W,yaw=yaw,pitch=pitch,opa=opa,lab=lab,lsize=lsize)]
def zjoin(items): return ''.join(s for _,s in sorted(items,key=lambda t:t[0]))
def axes3(cx,cy,A=80,yaw=25,pitch=-16,lsize=19):
    s=[]
    for v,nm in (((1,0,0),'x'),((0,0,1),'z'),((0,1,0),'y')):
        X,Y,Z=rot3(v,yaw,pitch); s.append(L(cx-X*A*.8,cy+Y*A*.8,cx+X*A,cy-Y*A,MUTED,1.3))
        s.append(T(cx+X*(A+14),cy-Y*(A+14)+7,tex=nm,size=lsize,fill=MUTED))
    return ''.join(s)

# ═════ 오비탈 2차원 도우미 (VB·MO 모양) ═════
def sph(cx,cy,r,sign=1,lab=True,lsize=19,opa=.30):
    col=BF if sign>0 else GRAV
    s=C(cx,cy,r,col,1.8,fill=col,extra=f'fill-opacity="{opa}"')
    if lab: s+=T(cx-r*.55,cy-r*.42+lsize*.36,tex='+' if sign>0 else '-',size=lsize,weight=700)
    return s
def ell(cx,cy,rx,ry,sign=1,lab=True,lsize=19,lx=None,ly=None):
    col=BF if sign>0 else GRAV
    s=f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{col}" fill-opacity=".30" stroke="{col}" stroke-width="1.8"/>'
    if lab: s+=T(lx if lx is not None else cx,(ly if ly is not None else cy)+lsize*.36,tex='+' if sign>0 else '-',size=lsize,weight=700)
    return s
def lob(cx,cy,ang,L0,sign,W=0.6,lab=True,lsize=19,opa=.30):
    t=math.radians(ang); ux,uy=math.cos(t),-math.sin(t); px,py=-uy,ux; pts=[]
    for i in range(61):
        th=math.radians(-90+3*i); rho=L0*math.cos(th)**2
        pts.append((cx+ux*rho*math.cos(th)+px*W*L0*math.cos(th)**2*math.sin(th),cy+uy*rho*math.cos(th)+py*W*L0*math.cos(th)**2*math.sin(th)))
    col=BF if sign>0 else GRAV
    s=P(pts,col,1.8,fill=col,close=True,extra=f'fill-opacity="{opa}"')
    if lab: s+=T(cx+ux*L0*.58,cy+uy*L0*.58+lsize*.36,tex='+' if sign>0 else '-',size=lsize,weight=700)
    return s
def dotn(x,y,r=4): return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{INK}"/>'
def spin(x,y,up,col=INK,h=30): return harp(x,y-h/2,h,up,col,2.4)
def sigbox(cx,cy,rx,ry,dash=None):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="none" stroke="{FIELD}" stroke-width="2.6"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'

