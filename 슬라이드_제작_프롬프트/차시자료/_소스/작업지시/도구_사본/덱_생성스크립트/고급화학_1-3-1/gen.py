# -*- coding: utf-8 -*-
"""고급화학 1-3-1 그림 생성: gen_head.py(1-2-2 사본: lewis·bracket 도우미, OUT=이 덱) + 이 파일의 그림 → tpl.html의 {{KEY}}를 바꿔 slides.html"""
import math, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/1-3-1_원자가_결합_분자_오비탈과_혼성_오비탈/slides.html')
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

# ═════ MO 도표 ═════
ORD_O=[('s2s',1,'b'),('s2s*',1,'a'),('s2p',1,'b'),('p2p',2,'b'),('p2p*',2,'a'),('s2p*',1,'a')]
ORD_N=[('s2s',1,'b'),('s2s*',1,'a'),('p2p',2,'b'),('s2p',1,'b'),('p2p*',2,'a'),('s2p*',1,'a')]
MOTEX={'s2s':'\\sigma_{2s}','s2s*':'\\sigma^*_{2s}','s2p':'\\sigma_{2p}','p2p':'\\pi_{2p}','p2p*':'\\pi^*_{2p}','s2p*':'\\sigma^*_{2p}'}
def mofill(order,n):
    occ={}; left=n
    for nm,deg,_ in order:
        if deg==1: k=min(2,left); occ[nm]=['ud'[:k] if k==2 else ('u' if k==1 else '')]; left-=k
        else:
            k=min(4,left); o=['','']
            for i in range(k): o[i%2]+= 'u' if i<2 else 'd'
            occ[nm]=o; left-=k
    assert left==0
    return occ
def bo(order,occ):
    b=sum(sum(len(x) for x in occ[nm]) for nm,_,t in order if t=='b'); a=sum(sum(len(x) for x in occ[nm]) for nm,_,t in order if t=='a')
    up=sum(1 for nm,_,_ in order for x in occ[nm] if len(x)==1)
    return b,a,(b-a)/2,up
def modiag(x0,y0,el,molname,nval,order,expect,W=470,size=20,step_e=None,showE=True):
    """2주기 동핵 2원자 MO 도표. expect=(결합 차수, 홀전자) 자동 검산"""
    occ=mofill(order,nval); b,a,bord,up=bo(order,occ)
    if (bord,up)!=expect: sys.exit(f'[{molname}] 결합 차수 {bord}, 홀전자 {up} ≠ {expect}')
    ao={'B':('ud','u'),'N':('ud','uuu'),'O':('ud','uudu')}[el]
    xl,xm,xr=x0+110,x0+W/2+10,x0+W-70
    Y={'2s':y0+330,'2p':y0+150}
    ys={'s2s':y0+372,'s2s*':y0+290}
    if order is ORD_O: ys.update({'s2p':y0+222,'p2p':y0+186,'p2p*':y0+108,'s2p*':y0+60})
    else: ys.update({'p2p':y0+214,'s2p':y0+180,'p2p*':y0+108,'s2p*':y0+60})
    s=[]
    def aoline(x,which,o):
        if which=='2s': return dlev(x,Y['2s'],[o[0]])
        p=o[1]; arr=['','','']
        for i,ch in enumerate(p): arr[i%3]+=( 'u' if i<3 else 'd')
        return dlev(x,Y['2p'],arr,LW=30,gap=8)
    # 연결 점선
    for nm,deg,t in order:
        src='2s' if '2s' in nm else '2p'
        hw=(34 if deg==1 else 46+12)/2 if True else 0
        hwm=17 if deg==1 else 40
        hwa=17 if src=='2s' else 53
        s.append(L(xl+hwa,Y[src],xm-hwm,ys[nm],MUTED,1.4,dash='4 4'))
        s.append(L(xr-hwa,Y[src],xm+hwm,ys[nm],MUTED,1.4,dash='4 4'))
    s.append(aoline(xl,'2s',ao)); s.append(aoline(xl,'2p',ao)); s.append(aoline(xr,'2s',ao)); s.append(aoline(xr,'2p',ao))
    s.append(T(xl-24,Y['2s']+7,tex='2s',size=size,anchor='end')); s.append(T(xl-58,Y['2p']+7,tex='2p',size=size,anchor='end'))
    s.append(T(xr+24,Y['2s']+7,tex='2s',size=size,anchor='start')); s.append(T(xr+58,Y['2p']+7,tex='2p',size=size,anchor='start'))
    ev=[]
    for nm,deg,t in order:
        if deg==1: ln=dlev(xm,ys[nm],[''])
        else: ln=dlev(xm,ys[nm],['',''],LW=34,gap=12)
        s.append(ln)
        o=occ[nm]
        e=dlev(xm,ys[nm],o,LW=34,gap=12,line=False)
        ev.append(e)
        lx=xm+(30 if deg==1 else 52)
        s.append(T(lx,ys[nm]+7,tex=MOTEX[nm],size=size,anchor='start',fill=FIELD if t=='b' else OX,halo=True))
    s.append(step(ev,step_e) if step_e else an('fade',ev,dur='.8',delay='.4'))
    yb=y0+412
    s.append(T(xl,yb+6,tex='\\mathrm{'+el+'}',size=size+2)); s.append(T(xr,yb+6,tex='\\mathrm{'+el+'}',size=size+2)); s.append(T(xm,yb+6,tex=f'\\ce{{{molname}}}',size=size+2))
    if showE:
        s.append(A(x0+12,y0+392,x0+12,y0+40,'ink',2.6)); s.append(T(x0+26,y0+52,tex='E',size=size+2,anchor='start'))
    return ''.join(s)

# ═══ S1 표지: 메테인의 sp³ 혼성 오비탈과 H 1s
def cover():
    s=['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    cx,cy=270,268; yaw,pitch=28,-14
    items=[]
    for i,d in enumerate(TET):
        L0=150
        z,lb=lobe3(cx,cy,d,L0,1,yaw=yaw,pitch=pitch,lab=False)
        X,Y,Z=rot3(d,yaw,pitch); hx,hy=cx+X*L0*0.98,cy-Y*L0*0.98
        h=C(hx,hy,34,BF,1.8,fill=BF,extra='fill-opacity=".22"')+dotn(hx,hy,5)
        items.append((Z,f'<g data-anim="pop" data-o="{f(cx)},{f(cy)}" data-dur=".7" data-delay="{.2+.35*i:.2f}">{lb}{h}</g>'))
    s.append(zjoin(items)); s.append(dotn(cx,cy,6))
    return svg('0 0 540 540',540,'메테인: 탄소의 sp3 혼성 오비탈 4개가 정사면체 꼭짓점을 향하고, 끝마다 수소의 1s 오비탈이 겹친다',s,cls='cover-fig')
FIG['COVER']=cover()

# ═══ S2 중단원 도입: 엽록소 중심(포르피린 고리)
def porph():
    s=[]; sc=31; cx,cy=150,150; at=[]; bd=[]
    def add(el,x,y): at.append((el,x,y)); return len(at)-1
    mg=add('Mg',0,0); ns=[]; alph={}
    for k in range(4):
        a=math.radians(90*k+45); ux,uy=math.cos(a),math.sin(a)
        n=add('N',2.05*ux,2.05*uy); ns.append(n); bd.append((mg,n,'d'))
        rc=(3.224*ux,3.224*uy); R=1.174; vs=[n]
        base=math.atan2(-uy,-ux)
        for j in (1,2,3,4):
            t=base+math.radians(72*j); vs.append(add('C',rc[0]+R*math.cos(t),rc[1]+R*math.sin(t)))
        for j in range(5): bd.append((vs[j],vs[(j+1)%5],'s'))
        alph[k]=(vs[1],vs[4])
    for k in range(4):
        a=math.radians(90*k+90); m=add('C',3.42*math.cos(a),3.42*math.sin(a))
        bd.append((alph[k][0],m,'s')); bd.append((alph[(k+1)%4][1],m,'s'))
    P2=lambda i:(cx+at[i][1]*sc,cy-at[i][2]*sc)
    for i,j,t in bd:
        (x1,y1),(x2,y2)=P2(i),P2(j)
        s.append(L(x1,y1,x2,y2,BOND,5 if t=='s' else 3,dash='4 4' if t=='d' else None,extra='stroke-linecap="round"'))
    for i,(el,x,y) in enumerate(at):
        X,Y=P2(i); s.append(atom(X,Y,{'Mg':15,'N':11,'C':9}[el],el,'-'))
    nC=sum(1 for a in at if a[0]=='C'); nN=sum(1 for a in at if a[0]=='N')
    assert (nC,nN)==(20,4)
    # 범례
    ly=318
    for k,(el,lab,r) in enumerate((('C','C',9),('N','N',11),('Mg','Mg',13))):
        x=40+k*92; s.append(atom(x,ly,r,el,'-')); s.append(T(x+18,ly+7,tex='\\mathrm{'+lab+'}',size=19,anchor='start'))
    out=an('fade','' .join(s),dur='1.2')
    return svg('0 0 300 340',300,'엽록소 분자의 중심 부분: 마그네슘 이온을 질소 원자 4개가 둘러싼 고리 모양 골격 (수소 원자 생략)',[out])
FIG['PORPH']=porph()

# ═══ S4 생각 열기: CH4 루이스 구조 + 공-막대
def openfig():
    S=34; x0,y0=110,120; R=58
    at=[A_('C',x0,y0)]+[A_('H',x0+dx,y0+dy) for dx,dy in ((0,-R),(R,0),(0,R),(-R,0))]
    lw=lewis(at,[(0,i,1,'d') for i in range(1,5)],S=S,name='CH4')
    s=[lw,T(110,250,mix='루이스 구조',size=20)]
    a,b,_=mol('CH4')
    s.append(bs3d(380,128,a,b,sc=78,yaw=28,pitch=-14,arcs=[(1,0,2,'109.5^\\circ',None)],arc_r=36))
    s.append(T(380,250,mix='실제 모양 (공-막대 모형)',size=20))
    s.append(A(205,120,262,120,'ink',2.6))
    s.append(T(234,104,mix='?',size=24,weight=700))
    return svg('0 0 500 265',500,'메테인의 루이스 구조와 공-막대 모형: 루이스 구조는 평면에 그리지만 실제 결합각은 109.5도',s)
FIG['OPEN']=openfig()

# ═══ S5 편재 전자 모형 → 오비탈
def locfig():
    s=[]
    S=40
    at=[A_('H',90,95),A_('H',170,95)]
    s.append(lewis(at,[(0,1,1,'d')],S=S,name='H2dot'))
    s.append(f'<rect x="113" y="74" width="34" height="40" rx="8" fill="{FIELD}" fill-opacity=".18" stroke="{FIELD}" stroke-width="1.5"/>')
    s.append(T(130,170,mix='(가) 전자쌍이 두 원자 사이 한곳에',size=19))
    s.append(T(130,196,mix='— 편재 전자 모형',size=19,fill=MUTED))
    g=[]
    for x in (370,450):
        for r,o in ((58,.08),(44,.10),(30,.14)): g.append(C(x,95,r,MINUS,0,fill=MINUS,extra=f'fill-opacity="{o}" stroke-width="0"'))
    g.append(f'<ellipse cx="410" cy="95" rx="30" ry="26" fill="{MINUS}" fill-opacity=".16"/>')
    g.append(nuc(370,95,8)); g.append(nuc(450,95,8))
    s.append(an('scale',g,**{'from':'.6','o':'410,95','dur':'1.1'}))
    s.append(T(410,170,mix='(나) 전자구름이 두 원자에 퍼져 있다',size=19))
    s.append(T(410,196,mix='— 오비탈에서 발견될 확률',size=19,fill=MUTED))
    return svg('0 0 560 210',560,'루이스 구조의 점 전자쌍과 전자구름 그림 비교',s)
FIG['LOC']=locfig()

# ═══ S6 원자가 결합 파동 함수: 전자 1, 2가 바뀜
def vbfig():
    s=[]
    for k,(x0,lab) in enumerate(((20,'\\psi_\\mathrm{A}(1)\\,\\psi_\\mathrm{B}(2)'),(300,'\\psi_\\mathrm{A}(2)\\,\\psi_\\mathrm{B}(1)'))):
        xa,xb,y=x0+70,x0+190,80
        for x,nm in ((xa,'A'),(xb,'B')):
            s.append(C(x,y,46,MINUS,1.2,fill=MINUS,extra='fill-opacity=".10"')); s.append(nuc(x,y,9))
            s.append(T(x,y+72,tex='\\mathrm{H_'+nm+'}',size=20))
        e1,e2=(xa-26,xb+26) if k==0 else (xb+26,xa-26)
        s.append(ele(e1,y-26,9)); s.append(T(e1,y-44,tex='1',size=19))
        s.append(ele(e2,y-26,9)); s.append(T(e2,y-44,tex='2',size=19))
        s.append(T((xa+xb)/2,y+108,tex=lab,size=21))
    s.append(P([(258,58),(280,40),(302,58)],MINUS,2.4))
    s.append(A(296,54,302,60,'minus',2.4))
    s.append(T(280,30,mix='바뀜',size=19,fill=MINUS))
    return svg('0 0 560 200',560,'수소 원자 A, B와 전자 1, 2: 전자가 서로 바뀐 경우도 같은 확률로 생각한다',s)
FIG['VB']=vbfig()

# ═══ S7 H2 σ 결합
def h2sig():
    s=[]; r=44
    s.append(T(280,24,mix='원자 오비탈',size=20,fill=MUTED))
    for x,nm,up in ((170,'H_A(1s)',True),(390,'H_B(1s)',False)):
        s.append(sph(x,92,r)); s.append(dotn(x,92)); s.append(spin(x+18,92,up))
        s.append(T(x,160,tex='\\mathrm{'+nm.split('(')[0].replace('_A','_A').replace('_B','_B')+'}('+'1s)',size=20))
    s.append(A(280,176,280,206,'ink',2.6))
    g=[an('move',sph(244,272,r,lab=True)+dotn(244,272),**{'from':'-60,0','dur':'1.2','ease':'out'}),
       an('move',sph(316,272,r,lab=False)+dotn(316,272),**{'from':'60,0','dur':'1.2','ease':'out'})]
    s+=g
    s.append(sigbox(280,272,22,34)); s.append(spin(274,272,True)); s.append(spin(286,272,False))
    s.append(T(400,250,mix='σ 결합',size=21,anchor='start',fill=FIELD,weight=700)); s.append(L(302,262,396,246,FIELD,1.6))
    s.append(T(280,348,tex='\\ce{H2}',size=22))
    s.append(T(470,330,mix='보라: 위상 (+)',size=19,fill=MUTED))
    return svg('0 0 560 360',560,'수소 원자 두 개의 1s 오비탈이 겹쳐 시그마 결합을 만든다. 두 전자의 스핀은 반대',s)
FIG['H2SIG']=h2sig()

# ═══ S8 HF σ 결합 + 축 방향에서 본 모양
def hfsig():
    s=[]
    s.append(sph(120,80,40)); s.append(dotn(120,80)); s.append(spin(136,80,True))
    s.append(T(120,150,tex='\\mathrm{H}(1s)',size=20))
    s.append(lob(320,80,180,74,1)); s.append(lob(320,80,0,74,-1)); s.append(dotn(320,80)); s.append(spin(298,58,False))
    s.append(T(320,150,tex='\\mathrm{F}(2p_z)',size=20))
    s.append(A(220,170,220,198,'ink',2.6))
    hx,fx,y=150,250,262
    g=an('move',sph(hx,y,40,lab=False)+dotn(hx,y),**{'from':'-50,0','dur':'1.2','ease':'out'})
    s.append(lob(fx,y,180,74,1,lab=False)); s.append(lob(fx,y,0,74,-1)); s.append(dotn(fx,y)); s.append(g)
    s.append(sigbox(200,y,36,30)); s.append(spin(194,y,True)); s.append(spin(206,y,False))
    s.append(T(200,330,mix='HF의 σ 결합',size=20))
    # 축 방향에서 본 모양
    s.append(L(340,y,420,y,MUTED,1.4,dash='5 4')); s.append(A(394,y-34,418,y-34,'muted',2))
    s.append(C(470,y,30,FIELD,2.6,fill=FIELD,extra='fill-opacity=".12"'))
    s.append(T(470,y+62,mix='축 방향에서 보면||원 (원통 대칭)',size=19))
    return svg('0 0 540 360',540,'수소의 1s와 플루오린의 2pz 오비탈이 핵 사이 축을 따라 겹친 시그마 결합. 축 방향에서 보면 원 모양',s)
FIG['HFSIG']=hfsig()

# ═══ S9 N2: σ (pz–pz) / π (px–px)
def n2pi():
    s=[]
    # (가) σ
    xa,xb,y=90,210,120
    s.append(lob(xa,y,180,62,-1)); s.append(lob(xb,y,0,62,-1))
    s.append(lob(xa,y,0,62,1,lab=False)); s.append(lob(xb,y,180,62,1,lab=False))
    s.append(T(150,y+7,tex='+',size=19,weight=700))
    s.append(dotn(xa,y)); s.append(dotn(xb,y)); s.append(sigbox(150,y,28,24))
    s.append(T(150,208,mix='(가) $2p_z$–$2p_z$ σ 결합',size=20))
    # (나) π
    xa,xb,y=370,450,120
    g=[]
    for x,dx in ((xa,'-40,0'),(xb,'40,0')):
        g.append(an('move',lob(x,y,90,66,1,W=.66,lab=(x==xa))+lob(x,y,270,66,-1,W=.66,lab=(x==xa))+dotn(x,y),**{'from':dx,'dur':'1.2','ease':'out'}))
    s+=g
    s.append(L(310,y,520,y,MUTED,1.6,dash='6 5')); s.append(T(524,y+6,mix='마디면',size=19,anchor='start',fill=MUTED))
    s.append(sigbox(410,y-46,30,26,dash='6 5')); s.append(sigbox(410,y+46,30,26,dash='6 5'))
    s.append(P([(444,y-46),(470,y-46),(470,y+46),(444,y+46)],FIELD,2,dash='6 5'))
    s.append(T(476,y-58,mix='π 결합 1개',size=20,anchor='start',fill=FIELD,weight=700))
    s.append(T(410,208,mix='(나) $2p_x$–$2p_x$ π 결합',size=20))
    return svg('0 0 600 225',600,'질소 분자: 2pz끼리 마주 겹친 시그마 결합과, 2px끼리 나란히 겹친 파이 결합. 위아래 두 덩어리가 합쳐 파이 결합 하나',s)
FIG['N2PI']=n2pi()

# ═══ S10 결합 에너지 막대
def bebar():
    s=[]; x0,y0=70,240; sc=0.22
    s.append(L(x0,y0,x0,20,MUTED,1.6)); s.append(L(x0,y0,470,y0,MUTED,1.6))
    for v in (0,200,400,600,800):
        y=y0-v*sc; s.append(L(x0-6,y,x0,y,MUTED,1.4)); s.append(T(x0-10,y+6,tex=str(v),size=18,anchor='end'))
    s.append(T(14,22,mix='결합 에너지 (kJ/mol)',size=19,anchor='start'))
    for i,(lab,v) in enumerate((('C{-}C',348),('C{=}C',612),('C{\\equiv}C',837))):
        x=130+i*120; h=v*sc
        s.append(an('scale',f'<rect x="{x-30}" y="{f(y0-h)}" width="60" height="{f(h)}" fill="{INK}"/>',**{'from':'1,0','o':f'{x},{y0}','dur':'1','delay':f'{.2+.3*i:.1f}'}))
        s.append(T(x,y0-h+28,tex=str(v),size=20,fill='#fff')); s.append(T(x,y0+26,tex='\\mathrm{'+lab+'}',size=20))
    y2=y0-696*sc; s.append(L(214,y2,290,y2,MUTED,2,dash='6 5')); s.append(T(208,y2+6,mix='2 × 348 = 696',size=19,anchor='end',fill=MUTED))
    return svg('0 0 480 280',480,'탄소-탄소 결합 에너지 막대그래프: 단일 348, 이중 612, 삼중 837 kJ/mol, 단일의 두 배 696 점선',s)
FIG['BEBAR']=bebar()

# ═══ S11 액체 산소와 자석 + O2 루이스 구조
def o2mag():
    s=[]
    g='#AAB4BF'
    s.append(P([(60,60),(60,200),(100,240),(220,240),(260,200),(260,60),(220,60),(220,190),(200,206),(120,206),(100,190),(100,60)],INK,2,fill=g,close=True))
    s.append(f'<rect x="60" y="40" width="40" height="22" fill="#fff" stroke="{INK}" stroke-width="2"/>'); s.append(f'<rect x="220" y="40" width="40" height="22" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    s.append(T(80,58,mix='N',size=19,weight=700)); s.append(T(240,58,mix='S',size=19,weight=700))
    s.append(f'<path d="M100 66 Q160 84 220 66 L220 96 Q160 112 100 96 Z" fill="{LO2}" stroke="#7FB3DD" stroke-width="1.5"/>')
    s.append(an('move',f'<ellipse cx="160" cy="30" rx="6" ry="9" fill="{LO2}" stroke="#7FB3DD" stroke-width="1.5"/>',**{'from':'0,-24','dur':'1.4','rep':'loop'}))
    s.append(T(160,280,mix='액체 산소가 두 극 사이에 달라붙는다',size=19))
    S=36; x1,x2,y=380,470,130
    at=[A_('O',x1,y,lp=[135,225]),A_('O',x2,y,lp=[45,315])]
    s.append(lewis(at,[(0,1,2,'l')],S=S,name='O2'))
    s.append(T(425,200,mix='모든 전자가 짝을 지음',size=19)); s.append(T(425,226,mix='→ 홀전자 0 (예측)',size=19,fill=MUTED))
    return svg('0 0 560 300',560,'자석의 N극과 S극 사이에 액체 산소가 달라붙은 모습과 산소 분자의 루이스 구조',s)
FIG['O2MAG']=o2mag()

# ═══ S12 H2 MO 모양 + 준위
def h2mo():
    s=[]
    # 반결합성 (위)
    y=70
    s.append(sph(60,y,30)); s.append(T(100,y+7,mix='−',size=22,weight=700)); s.append(sph(140,y,30));
    s.append(T(60,y+52,tex='1s_\\mathrm{A}',size=19)); s.append(T(140,y+52,tex='1s_\\mathrm{B}',size=19))
    s.append(A(184,y,224,y,'ink',2.4))
    g=[ell(262,y,30,28,1),ell(330,y,30,28,-1),L(296,y-38,296,y+38,MUTED,1.6,dash='5 4'),dotn(270,y),dotn(322,y)]
    s.append(an('pop',g,o=f'296,{y}',dur='.8',delay='.3'))
    s.append(T(296,y+56,mix='반결합성 MO $\\sigma^*$',size=19,fill=OX))
    # 결합성 (아래)
    y=200
    s.append(sph(60,y,30)); s.append(T(100,y+7,mix='+',size=22,weight=700)); s.append(sph(140,y,30))
    s.append(T(60,y+52,tex='1s_\\mathrm{A}',size=19)); s.append(T(140,y+52,tex='1s_\\mathrm{B}',size=19))
    s.append(A(184,y,224,y,'ink',2.4))
    g=[ell(296,y,64,32,1),dotn(270,y),dotn(322,y)]
    s.append(an('pop',g,o=f'296,{y}',dur='.8',delay='.8'))
    s.append(T(296,y+56,mix='결합성 MO $\\sigma$',size=19,fill=FIELD))
    # 준위 도표
    x0=400; xl,xm,xr=x0+40,x0+120,x0+200; ya,yb,ys=150,236,64
    s.append(A(x0-8,270,x0-8,30,'ink',2.4)); s.append(T(x0+4,40,tex='E',size=21,anchor='start'))
    for (xa,xb) in ((xl+17,xm-17),(xr-17,xm+17)):
        s.append(L(xa,ya,xb,yb,MUTED,1.4,dash='4 4')); s.append(L(xa,ya,xb,ys,MUTED,1.4,dash='4 4'))
    s.append(dlev(xl,ya,['u'])); s.append(dlev(xr,ya,['u'])); s.append(dlev(xm,ys,[''])); s.append(dlev(xm,yb,['']))
    s.append(an('fade',dlev(xm,yb,['ud'],line=False),dur='.8',delay='1.2'))
    s.append(T(xl,ya+30,tex='\\mathrm{H}\\,1s',size=19)); s.append(T(xr,ya+30,tex='\\mathrm{H}\\,1s',size=19))
    s.append(T(xm+24,ys+7,tex='\\sigma^*_{1s}',size=20,anchor='start',fill=OX)); s.append(T(xm+24,yb+7,tex='\\sigma_{1s}',size=20,anchor='start',fill=FIELD))
    return svg('0 0 640 290',600,'수소 분자의 분자 오비탈: 1s 두 개를 더하면 결합성 시그마, 빼면 반결합성 시그마 별. 두 전자는 결합성에 들어간다',s)
FIG['H2MO']=h2mo()

# ═══ S13 2p 겹침 모양 (σ2p, σ*2p, π2p, π*2p)
def p2mo():
    s=[]
    def row(y,kind):
        if kind in ('s','s*'):
            sgB=1 if kind=='s' else -1
            s.append(lob(40,y,180,34,-1,W=.7,lsize=18)); s.append(lob(40,y,0,34,1,W=.7,lsize=18))
            s.append(T(92,y+7,mix='+' if kind=='s' else '−',size=21,weight=700))
            s.append(lob(144,y,180,34,sgB,W=.7,lsize=18)); s.append(lob(144,y,0,34,-sgB,W=.7,lsize=18))
            s.append(A(192,y,224,y,'ink',2.2))
            if kind=='s':
                g=[lob(250,y,180,30,-1,W=.7,lsize=18),ell(306,y,38,22,1,lsize=18),lob(362,y,0,30,-1,W=.7,lsize=18)]
            else:
                g=[lob(262,y,180,30,-1,W=.7,lsize=18),lob(262,y,0,26,1,W=.75,lsize=18),L(306,y-30,306,y+30,MUTED,1.5,dash='4 4'),lob(350,y,180,26,-1,W=.75,lsize=18),lob(350,y,0,30,1,W=.7,lsize=18)]
            s.append(an('fade',g,dur='.7',delay='.3' if kind=='s' else '.6'))
            nm=('\\sigma_{2p}','결합성',FIELD) if kind=='s' else ('\\sigma^*_{2p}','반결합성',OX)
        else:
            sgB=1 if kind=='p' else -1
            for x,sg in ((50,1),(134,sgB)):
                s.append(lob(x,y,90,32,sg,W=.75,lsize=18)); s.append(lob(x,y,270,32,-sg,W=.75,lsize=18))
            s.append(T(92,y+7,mix='+' if kind=='p' else '−',size=21,weight=700))
            s.append(A(192,y,224,y,'ink',2.2))
            if kind=='p':
                g=[ell(306,y-24,44,17,1,lsize=18),ell(306,y+24,44,17,-1,lsize=18),L(250,y,362,y,MUTED,1.5,dash='4 4')]
            else:
                g=[lob(284,y,90,30,1,W=.7,lsize=18),lob(284,y,270,30,-1,W=.7,lsize=18),lob(328,y,90,30,-1,W=.7,lsize=18),lob(328,y,270,30,1,W=.7,lsize=18),L(306,y-34,306,y+34,MUTED,1.5,dash='4 4')]
            s.append(an('fade',g,dur='.7',delay='.9' if kind=='p' else '1.2'))
            nm=('\\pi_{2p}','결합성',FIELD) if kind=='p' else ('\\pi^*_{2p}','반결합성',OX)
        s.append(T(400,y+7,tex=nm[0],size=21,anchor='start',fill=nm[2])); s.append(T(460,y+7,mix=nm[1],size=19,anchor='start',fill=nm[2]))
    row(50,'s'); row(130,'s*'); row(225,'p'); row(320,'p*')
    s.append(T(92,90,tex='2p_z\\ \\ 2p_z',size=18)); s.append(T(92,280,tex='2p_y\\ \\ 2p_y',size=18))
    return svg('0 0 560 360',560,'2p 오비탈 두 개가 겹쳐 생기는 분자 오비탈: 축 방향은 시그마 2p와 시그마 별, 옆으로는 파이 2p와 파이 별',s)
FIG['P2MO']=p2mo()

# ═══ S14 B2, O2 MO 도표
def b2o2():
    s=[modiag(0,0,'B','B2',6,ORD_N,(1,2),W=480,step_e='e1',size=22),modiag(560,0,'O','O2',12,ORD_O,(2,2),W=480,step_e='e2',size=22)]
    return svg('0 0 1060 430',820,'붕소 분자와 산소 분자의 분자 오비탈 에너지 준위와 전자 배치: 둘 다 홀전자 2개',s)
FIG['B2O2']=b2o2()
def n2o2():
    s=[modiag(0,0,'N','N2',10,ORD_N,(3,0),W=470,step_e='n1',size=25),modiag(540,0,'O','O2',12,ORD_O,(2,2),W=470,step_e='n1',size=25)]
    return svg('0 0 1040 440',740,'질소 분자와 산소 분자의 분자 오비탈 에너지 준위와 전자 배치',s)
FIG['N2O2']=n2o2()

# ═══ S15 탄소의 전자 재배치
def rearr():
    s=[]
    s.append(ebox(80,40,['u','u',''],lab='2p')); s.append(ebox(80,150,['ud'],lab='2s'))
    s.append(T(134,220,tex='\\mathrm{C}:[\\mathrm{He}]2s^22p_x^12p_y^1',size=20))
    s.append(A(222,110,282,110,'ink',2.6)); s.append(T(252,96,mix='재배치',size=19))
    s.append(ebox(330,40,['u','u',''],lab='2p')); s.append(ebox(330,150,['u'],lab='2s'))
    s.append(an('move',harp(420,40,36,True,FIELD),**{'from':'-72,110','dur':'1.2','delay':'.4','ease':'io'}))
    s.append(T(384,220,tex='\\mathrm{C}:[\\mathrm{He}]2s^12p_x^12p_y^12p_z^1',size=20))
    return svg('0 0 520 236',520,'탄소 원자의 전자 재배치: 2s 전자 하나가 빈 2pz 오비탈로 옮겨 홀전자 4개',s)
FIG['REARR']=rearr()
def p90():
    s=[axes3(110,110,78)]
    items=[]
    for d in ((1,0,0),(0,1,0),(0,0,1)): items+=porb(110,110,d,62,lab=False,W=.5)
    s.append(zjoin(items)); s.append(dotn(110,110))
    s.append(T(110,226,mix='2p 오비탈끼리 90°',size=19))
    return svg('0 0 220 236',220,'세 2p 오비탈은 서로 90도',s)
FIG['P90']=p90()

# ═══ S16 sp³ 혼성: 에너지 상자 + 오비탈
def sp3e(kind='sp3'):
    s=[]
    n={'sp3':4,'sp2':3,'sp':2}[kind]; frac={'sp3':.75,'sp2':2/3,'sp':.5}[kind]
    y2s,y2p=170,40; yh=y2s-(y2s-y2p)*frac
    s.append(ebox(70,y2p,['u','u','u'],lab='2p')); s.append(ebox(70,y2s,['u'],lab='2s'))
    s.append(A(196,yh+18,252,yh+18,'ink',2.6)); s.append(T(224,yh+4,mix='혼성화',size=19))
    hx=280; lab={'sp3':'sp^3','sp2':'sp^2','sp':'sp'}[kind]
    s.append(an('fade',ebox(hx,yh,['u']*n,lab=None),dur='.8',delay='.5'))
    s.append(T(hx+n*18,yh+62,tex=lab+'\\ '+str(n)+'\\text{개}',size=20))
    if n<4:
        s.append(ebox(hx+n*36+18,y2p,['u']*(4-n)))
        s.append(T(hx+n*36+18+(4-n)*18,y2p-12,mix='혼성하지 않은 $2p$',size=19))
    s.append(A(22,y2s+50,22,14,'muted',2)); s.append(T(30,24,mix='에너지',size=19,anchor='start',fill=MUTED))
    return svg('0 0 520 236',520,f'2s와 2p 오비탈이 섞여 {lab} 혼성 오비탈을 만드는 에너지 상자 그림',s)
FIG['SP3E']=sp3e('sp3'); FIG['SP2E']=sp3e('sp2'); FIG['SPE']=sp3e('sp').replace('width:520px','width:480px',1)
def sp3orb():
    s=[]; cx,cy=150,150; yaw,pitch=28,-14
    items=[]
    for i,d in enumerate(TET):
        for z,sv in hybrid(cx,cy,d,108,yaw,pitch):
            items.append((z,f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.3+.3*i:.1f}">{sv}</g>'))
    s.append(zjoin(items)); s.append(dotn(cx,cy,5))
    s.append(T(150,292,mix='4개의 같은 $sp^3$ — 정사면체 배열',size=19))
    return svg('0 0 300 305',300,'탄소의 sp3 혼성 오비탈 4개가 정사면체 꼭짓점을 향한다',s)
FIG['SP3ORB']=sp3orb()
def onehyb():
    s=[]; cx,cy=110,60
    s.append(lob(cx,cy,0,150,1,W=.6)); s.append(lob(cx,cy,180,52,-1,W=.95)); s.append(dotn(cx,cy))
    s.append(T(178,22,mix='더 멀리 넓게',size=19,anchor='start')); s.append(T(80,112,mix='더 가까이 좁게',size=19))
    return svg('0 0 320 125',320,'sp3 혼성 오비탈 하나: 한쪽 엽은 크고 멀리, 반대쪽 엽은 작고 가깝게',s)
FIG['ONEHYB']=onehyb()

# ═══ S17 메테인 σ 결합
def ch4sig():
    s=[]; cx,cy=230,200; yaw,pitch=28,-14; L0=118
    items=[]
    for i,d in enumerate(TET):
        z,lb=lobe3(cx,cy,d,L0,1,yaw=yaw,pitch=pitch,lab=(i==0))
        X,Y,Z=rot3(d,yaw,pitch); hx,hy=cx+X*L0*1.02,cy-Y*L0*1.02
        h=an('move',sph(hx,hy,32,lab=False)+dotn(hx,hy,4),**{'from':f'{f(X*60)},{f(-Y*60)}','dur':'1.1','delay':f'{.3+.25*i:.2f}','ease':'out'})
        ox,oy=cx+X*L0*0.78,cy-Y*L0*0.78
        items.append((Z,lb+h+sigbox(ox,oy,24,24)))
    s.append(zjoin(items)); s.append(dotn(cx,cy,5))
    a,b=TET[0],TET[1]
    pts=[]
    om=math.acos(sum(p*q for p,q in zip(a,b)))
    for t in [q/20 for q in range(21)]:
        s1=math.sin((1-t)*om)/math.sin(om); s2=math.sin(t*om)/math.sin(om); v=tuple(s1*a[m]+s2*b[m] for m in range(3))
        X,Y,Z=rot3(v,yaw,pitch); pts.append((cx+X*46,cy-Y*46))
    s.append(P(pts,MUTED,2.2)); mx,my=pts[10]; s.append(T(mx+38,my+2,tex='109.5^\\circ',size=20,halo=True))
    s.append(T(cx,388,mix='C의 $sp^3$ + H의 $1s$ → σ 결합 4개',size=20))
    return svg('0 0 460 400',460,'메테인: 탄소 sp3 혼성 오비탈 4개와 수소 1s 오비탈 4개가 겹친 시그마 결합 4개, 결합각 109.5도',s)
FIG['CH4SIG']=ch4sig()

# ═══ S18 CH4·NH3·H2O
def three():
    s=[]
    for k,(nm,lab,ar) in enumerate((('CH4','109.5^\\circ',(1,0,2)),('NH3','107^\\circ',(1,0,2)),('H2O','104.5^\\circ',(1,0,2)))):
        a,b,lp=mol(nm); x=95+k*175
        s.append(bs3d(x,112,a,b,sc=66,yaw=28,pitch=-14,k=.85,lone=lp,arcs=[(ar[0],ar[1],ar[2],lab,None)],arc_r=30,arc_size=19,
                      anim=('pop',{'o':f'{x},112','dur':'.6','delay':f'{.2+.3*k:.1f}'})))
        s.append(T(x,222,tex=f'\\ce{{{nm}}}',size=21)); s.append(T(x,248,mix=['비공유 0','비공유 1','비공유 2'][k],size=19,fill=MUTED))
    return svg('0 0 530 260',530,'메테인, 암모니아, 물의 공-막대 모형과 결합각 109.5, 107, 104.5도. 비공유 전자쌍 로브',s)
FIG['THREE']=three()

# ═══ S19 sp² 오비탈
def sp2orb():
    s=[]; cx,cy=150,150; yaw,pitch=20,-24
    pl=[]
    for v in ((1.25,0,1.25),(1.25,0,-1.25),(-1.25,0,-1.25),(-1.25,0,1.25)):
        X,Y,Z=rot3(v,yaw,pitch); pl.append((cx+X*105,cy-Y*105))
    dirs=[(math.cos(math.radians(a)),0,math.sin(math.radians(a))) for a in (90,210,330)]
    items=[]
    for i,d in enumerate(dirs):
        for z,sv in hybrid(cx,cy,d,104,yaw,pitch): items.append((z,f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.3+.3*i:.1f}">{sv}</g>'))
    for z,sv in porb(cx,cy,(0,1,0),84,yaw,pitch,opa=.15,W=.55): items.append((z,sv))
    s.append(P(pl,MUTED,1.4,dash='5 4',close=True))
    s.append(zjoin(items)); s.append(dotn(cx,cy,5))
    s.append(T(268,40,mix='혼성하지 않은 $2p$',size=19,anchor='end'))
    s.append(T(150,298,mix='삼각 평면 배열, 120°',size=19))
    return svg('0 0 300 310',300,'sp2 혼성 오비탈 3개는 한 평면에서 120도, 혼성하지 않은 p 오비탈은 평면에 수직',s)
FIG['SP2ORB']=sp2orb()

# ═══ S20 에텐 σ·π
def ethene():
    s=[]; y=150; xa,xb=200,330
    # σ 골격
    for x,sg in ((xa,-1),(xb,1)):
        for ang in (120,240) if sg<0 else (60,300):
            t=math.radians(ang); hx,hy=x+math.cos(t)*104,y-math.sin(t)*104*0.62
            s.append(lob(x,y,math.degrees(math.atan2(-(hy-y),hx-x)),86,1,lab=False,W=.5))
            s.append(sph(hx,hy,26,lab=False)); s.append(dotn(hx,hy,4))
            mx,my=x+(hx-x)*.72,y+(hy-y)*.72; s.append(sigbox(mx,my,17,17))
    s.append(lob(xa,y,0,74,1,lab=False,W=.5)); s.append(lob(xb,y,180,74,1,lab=False,W=.5)); s.append(sigbox(265,y,20,18))
    # π
    g=[]
    for x in (xa,xb):
        g.append(lob(x,y,90,80,1,W=.5,opa=.22,lab=(x==xa))); g.append(lob(x,y,270,80,-1,W=.5,opa=.22,lab=(x==xa)))
    s.append(an('fade',g,dur='.9',delay='.4'))
    s.append(sigbox(265,y-58,66,22,dash='6 5')); s.append(sigbox(265,y+58,66,22,dash='6 5'))
    s.append(dotn(xa,y,5)); s.append(dotn(xb,y,5))
    s.append(T(265,y-96,mix='π 결합 (p–p)',size=20,fill=FIELD,weight=700))
    s.append(T(265,y+122,mix='σ 결합 (sp²–sp², sp²–1s)',size=20,fill=FIELD))
    s.append(T(xa,y+30,tex='\\mathrm{C}',size=19)); s.append(T(xb,y+30,tex='\\mathrm{C}',size=19))
    return svg('0 0 540 290',540,'에틸렌: 탄소 sp2 혼성 오비탈이 만든 시그마 결합 골격과, 혼성하지 않은 p 오비탈이 위아래로 겹친 파이 결합',s)
FIG['ETHENE']=ethene()

# ═══ S21 sp 오비탈 + 에타인
def sporb():
    s=[]; cx,cy=130,130; yaw,pitch=24,-18
    items=[]
    for i,d in enumerate(((1,0,0),(-1,0,0))):
        for z,sv in hybrid(cx,cy,d,100,yaw,pitch): items.append((z,f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.3+.3*i:.1f}">{sv}</g>'))
    for d in ((0,1,0),(0,0,1)):
        for z,sv in porb(cx,cy,d,70,yaw,pitch,opa=.15,W=.55,lab=False): items.append((z,sv))
    s.append(zjoin(items)); s.append(dotn(cx,cy,5))
    s.append(T(130,262,mix='선형 배열, 180°',size=19))
    return svg('0 0 260 275',220,'sp 혼성 오비탈 2개는 180도 반대 방향, 혼성하지 않은 p 오비탈 2개는 수직',s)
FIG['SPORB']=sporb()
def ethyne():
    s=[]; y=120; xa,xb=170,280; yaw,pitch=24,-18
    for x,sg in ((xa,180),(xb,0)):
        hx=x+(-1 if sg==180 else 1)*96
        s.append(lob(x,y,sg,78,1,lab=False,W=.5)); s.append(sph(hx,y,24,lab=False)); s.append(dotn(hx,y,4)); s.append(sigbox(x+(hx-x)*.72,y,16,16))
    s.append(lob(xa,y,0,62,1,lab=False,W=.5)); s.append(lob(xb,y,180,62,1,lab=False,W=.5)); s.append(sigbox(225,y,18,16))
    g=[]
    for x in (xa,xb):
        for z,sv in porb(x,y,(0,1,0),66,yaw,pitch,opa=.2,W=.5,lab=(x==xa)): g.append((z,sv))
        for z,sv in porb(x,y,(0,0,1),66,yaw,pitch,opa=.2,W=.5,lab=False): g.append((z,sv))
    s.append(an('fade',zjoin(g),dur='.9',delay='.4'))
    s.append(sigbox(225,y-52,58,18,dash='6 5')); s.append(sigbox(225,y+52,58,18,dash='6 5'))
    s.append(dotn(xa,y,5)); s.append(dotn(xb,y,5))
    s.append(T(300,y-66,mix='π 결합 2개',size=20,anchor='start',fill=FIELD,weight=700))
    s.append(T(225,y+112,mix='σ 결합 3개 (sp–sp, sp–1s)',size=20,fill=FIELD))
    return svg('0 0 450 250',450,'아세틸렌: 시그마 결합 3개와 서로 수직인 파이 결합 2개',s)
FIG['ETHYNE']=ethyne()

# ═══ S22 에테인·에텐·에타인 작은 모형
def c2three():
    s=[]
    for k,nm in enumerate(('C2H6','C2H4','C2H2')):
        a,b,_=mol(nm); x=150+k*300
        s.append(bs3d(x,70,a,b,sc=52,yaw=18 if nm=='C2H6' else 0,pitch=-20 if nm=='C2H6' else -8,k=.72,
                      anim=('pop',{'o':f'{x},70','dur':'.6','delay':f'{.2+.3*k:.1f}'})))
    return svg('0 0 900 140',900,'에테인, 에틸렌, 아세틸렌의 공-막대 모형',s)
FIG['C2THREE']=c2three()

# ═══ S24 NMR 스펙트럼
def nmr():
    s=[]; x0,x1,yb=40,500,200
    s.append(L(x0,yb,x1,yb,INK,2))
    s.append(T(x1-4,yb+30,mix='흡수 위치',size=19,anchor='end',fill=MUTED))
    def peak(xc,h,w=9):
        return [(xc+t,yb-h*math.exp(-(t/w)**2)) for t in range(-36,37,2)]
    pts=[(x0,yb)]+peak(200,70)+peak(330,150)+[(x1,yb)]
    s.append(an('draw',P(pts,INK,2.4),dur='1.4'))
    # 적분 곡선 (높이 비 1 : 3)
    base=yb-6; u=28
    st=[(x0+10,base),(180,base),(220,base-u),(310,base-u),(350,base-4*u),(x1-10,base-4*u)]
    s.append(an('draw',P(st,FIELD,2.2,dash='6 4'),dur='1.4',delay='.6'))
    s.append(dim(232,base,base-u,'1',size=19)); s.append(dim(362,base-u,base-4*u,'3',size=19))
    s.append(T(200,yb-82,mix='피크 1',size=19)); s.append(T(330,yb-162,mix='피크 2',size=19))
    return svg('0 0 520 236',520,'수소 NMR 스펙트럼: 흡수 피크 2개, 적분 곡선 높이 비 1 대 3',s)
def dim(x,y1,y2,lab,col=EQUI,size=20):
    s=L(x,y1,x,y2,col,2)+L(x-6,y1,x+6,y1,col,2)+L(x-6,y2,x+6,y2,col,2)
    return s+T(x+10,(y1+y2)/2+7,tex=lab,size=size,anchor='start',fill=col)
FIG['NMR']=nmr()

# ═══ S25 예제 Ⅰ-4 CH4
def ex4():
    a,b,_=mol('CH4')
    return svg('0 0 300 250',300,'메테인 공-막대 모형, 결합각 109.5도',[bs3d(150,120,a,b,sc=82,yaw=28,pitch=-14,arcs=[(1,0,2,'109.5^\\circ',None)],arc_r=38,anim=('pop',{'o':'150,120','dur':'.7'})),T(150,240,mix='정사면체',size=20)])
FIG['EX4']=ex4()

# ═══ S28 폴링 연표
def pauling():
    s=[]; y=70; xs=[60,200,340,480,620]
    s.append(L(30,y,660,y,INK,2.4))
    ev=[('1928','혼성 오비탈'),('1932','전기음성도'),('1933','벤젠의 공명'),('1954','노벨 화학상'),('1962','노벨 평화상')]
    for i,(x,(yr,tx)) in enumerate(zip(xs,ev)):
        s.append(an('pop',C(x,y,10,FIELD if i<3 else EQUI,2.4,fill='#fff'),o=f'{x},{y}',dur='.5',delay=f'{.2+.25*i:.2f}'))
        s.append(T(x,y-24,mix=yr,size=21,weight=700)); s.append(T(x,y+42,mix=tx,size=19))
    return svg('0 0 690 130',690,'폴링 연표: 1928 혼성 오비탈, 1932 전기음성도, 1933 벤젠의 공명, 1954 노벨 화학상, 1962 노벨 평화상',s)
FIG['PAULING']=pauling()

# ═══ S29 퍼플루오로데칼린
def c10f18():
    s=[]; sl=58; cx,cy=230,175
    h=sl*math.sqrt(3)/2
    L_=[(cx-h,cy) ,(cx+h,cy)]
    ring=lambda c0:[(c0[0]+sl*math.cos(math.radians(90+60*k)),c0[1]-sl*math.sin(math.radians(90+60*k))) for k in range(6)]
    r1,r2=ring(L_[0]),ring(L_[1])
    # 공유 꼭짓점: r1의 k=5(오른쪽 위, -30°)… 좌표로 합침
    verts=[];
    def vid(p):
        for i,q in enumerate(verts):
            if math.hypot(p[0]-q[0],p[1]-q[1])<1: return i
        verts.append(p); return len(verts)-1
    edges=set()
    for r in (r1,r2):
        ids=[vid(p) for p in r]
        for k in range(6): edges.add(tuple(sorted((ids[k],ids[(k+1)%6]))))
    assert len(verts)==10 and len(edges)==11
    for i,j in edges: s.append(L(*verts[i],*verts[j],INK,2.6,extra='stroke-linecap="round"'))
    nF=0
    deg={i:sum(1 for e in edges if i in e) for i in range(10)}
    for i,(x,y) in enumerate(verts):
        if deg[i]==3:
            u=(0,-1) if y<cy else (0,1); dirs=[u]
        else:
            c0=L_[0] if math.hypot(x-L_[0][0],y-L_[0][1])<sl+1 else L_[1]
            ux,uy=x-c0[0],y-c0[1]; n=math.hypot(ux,uy); ux,uy=ux/n,uy/n
            dirs=[]
            for da in (-34,34):
                t=math.atan2(uy,ux)+math.radians(da); dirs.append((math.cos(t),math.sin(t)))
        for ux,uy in dirs:
            s.append(L(x+ux*6,y+uy*6,x+ux*30,y+uy*30,INK,2))
            s.append(T(x+ux*44,y+uy*44+7,tex='\\mathrm{F}',size=20,fill='#4E8A2E')); nF+=1
    assert nF==18
    s.append(T(cx,cy+170,tex='\\ce{C10F18}',size=22))
    return svg('0 0 460 360',460,'퍼플루오로데칼린 C10F18의 골격 구조: 육각형 고리 두 개가 붙어 있고 탄소마다 플루오린이 붙어 있다',s)
FIG['C10F18']=c10f18()

# ═══ S33 결과 막대그래프
def resbar():
    s=[]; x0,yb=70,250; sc=2.0; base=90
    s.append(L(x0,yb,500,yb,MUTED,1.6)); s.append(L(x0,yb,x0,20,MUTED,1.6))
    for v in (90,120,150,180):
        y=yb-(v-base)*sc; s.append(L(x0-6,y,x0,y,MUTED,1.4)); s.append(T(x0-10,y+6,tex=str(v),size=18,anchor='end'))
        if v>90: s.append(L(x0,y,500,y,'#E2E7EC',1))
    s.append(T(16,22,mix='결합각 (°)',size=19,anchor='start'))
    data=[('CH4',109.5,109.5),('NH3',109.5,107),('H2O',109.5,104.5),('C2H4',120,117),('C2H2',180,180)]
    for i,(nm,pv,mv) in enumerate(data):
        x=110+i*80
        s.append(f'<rect x="{x}" y="{f(yb-(pv-base)*sc)}" width="26" height="{f((pv-base)*sc)}" fill="#fff" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 3"/>')
        s.append(an('scale',f'<rect x="{x+28}" y="{f(yb-(mv-base)*sc)}" width="26" height="{f((mv-base)*sc)}" fill="{INK}"/>',**{'from':'1,0','o':f'{x+41},{yb}','dur':'.9','delay':f'{.2+.2*i:.1f}'}))
        s.append(T(x+27,yb+28,tex=f'\\ce{{{nm}}}',size=19))
    s.append(f'<rect x="300" y="30" width="20" height="16" fill="#fff" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 3"/>'); s.append(T(326,45,mix='혼성 예측',size=19,anchor='start'))
    s.append(f'<rect x="410" y="30" width="20" height="16" fill="{INK}"/>'); s.append(T(436,45,mix='측정',size=19,anchor='start'))
    return svg('0 0 520 290',520,'혼성 예측 결합각과 측정 결합각 비교 막대그래프',s)
FIG['RESBAR']=resbar()

# ═══ S34 연습 문제 1 작은 모형 4개
def q1figs():
    s=[]
    for k,(nm,lab) in enumerate((('NF3','\\ce{NF3}'),('BH4','\\ce{BH4-}'),('BeH2','\\ce{BeH2}'),('CH4','\\ce{CH4}'))):
        a,b,lp=mol(nm); x=105+k*210
        body=bs3d(x,80,a,b,sc=56 if nm!='BeH2' else 60,yaw=28,pitch=-14,k=.86,lone=lp)
        s.append(step(body+T(x,176,tex=lab,size=21),f'q{k+1}'))
    return svg('0 0 840 190',840,'삼플루오린화 질소, 수소화 붕소 이온, 수소화 베릴륨, 메테인의 공-막대 모형',s)
FIG['Q1FIGS']=q1figs()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'))
