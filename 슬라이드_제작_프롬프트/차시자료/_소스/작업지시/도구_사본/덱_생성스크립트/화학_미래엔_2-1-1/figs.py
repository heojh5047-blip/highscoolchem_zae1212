# 2-1-1 그림 도우미: 보어 모형(전자 껍질), 입자 모형, 전기 분해 장치
import math
INK='#16233D'; PLUS='#D7263D'; MINUS='#1F6FD1'; FIELD='#2E9E6A'; EQUI='#E08A2C'; MUTED='#5B6B7F'; GRAV='#8C99A6'
WATER='#DDEEF8'; WATER_E='#9FC3DD'; GLASS='#7E8B98'; ELEC='#5B6B7F'

def f(v):
    s=f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s

def tex(x,y,t,size=20,anchor='middle',fill=None,mix=False,extra=''):
    a='data-mix' if mix else 'data-tex'
    t=t.replace('"','&quot;')
    fl=f' fill="{fill}"' if fill else ''
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {a}="{t}" data-size="{size}" data-anchor="{anchor}"{fl}{extra}></text>'

# ── 보어 모형 ──
ORDER=[90,0,270,180]   # 위, 오른쪽, 아래, 왼쪽 (수학 각도, y는 아래로)
def shell_pos(n, cap, start=0):
    """껍질 위 전자 각도 목록. cap 2: 위·아래. cap 8: 네 자리에 하나씩, 그다음 쌍."""
    if cap==2:
        base=[90,270][:n] if n else []
        return [(a,0) for a in base]
    order=ORDER[start:]+ORDER[:start]
    out=[]
    singles=min(n,4); pairs=n-singles
    for i in range(4):
        a=order[i]
        if i<pairs: out+= [(a,-1),(a,1)]
        elif i<singles: out.append((a,0))
    return out

def bohr(cx,cy,charge,conf,radii=(26,44,62),nr=17,er=5.5,start=None,label=None,lsize=18,
         skip=None,shells_dash=None,el_attr=None,ret_pts=False,pair_deg=13):
    """conf: 껍질별 전자 수. start: 껍질별 시작 자리(ORDER 기준). skip: (껍질, 번호) 그리지 않음."""
    s=''
    for k,n in enumerate(conf):
        dash=' stroke-dasharray="5 4"' if shells_dash and k in shells_dash else ''
        s+=f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{radii[k]}" fill="none" stroke="{MUTED}" stroke-width="1.6"{dash}/>'
    pts=[]
    for k,n in enumerate(conf):
        cap=2 if k==0 else 8
        st=(start[k] if start and k<len(start) else 0)
        for i,(a,p) in enumerate(shell_pos(n,cap,st)):
            ang=math.radians(a+p*pair_deg)
            x=cx+radii[k]*math.cos(ang); y=cy-radii[k]*math.sin(ang)
            pts.append((k,i,x,y))
            if skip and (k,i) in skip: continue
            ea=(el_attr or {}).get((k,i),'')
            s+=f'<circle cx="{f(x)}" cy="{f(y)}" r="{er}" fill="{MINUS}"{ea}/>'
    s+=f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{nr}" fill="#FDE2E4" stroke="{PLUS}" stroke-width="1.8"/>'
    s+=tex(cx,cy+lsize*0.36,f'+{charge}',lsize,fill=PLUS)
    if label: s+=label
    return (s,pts) if ret_pts else s

# ── 입자 모형 ──
def atom(x,y,r,el,lab=None,d=False):
    a=f'{f(x)},{f(y)},{r},{el}'
    if lab is not None or d: a+=','+(lab if lab is not None else el)
    if d: a+=',d'
    return f'<g data-atom="{a}"></g>'

def water(x,y,sc=1.0,lab=True,flip=False):
    R=24*sc; r=18*sc; dx=22*sc; dy=17*sc*(-1 if flip else 1)
    L=None if lab else '-'
    return atom(x-dx,y+dy,r,'H',L)+atom(x+dx,y+dy,r,'H',L)+atom(x,y,R,'O',L)

def h2(x,y,sc=1.0,lab=True):
    L=None if lab else '-'
    return atom(x-13*sc,y,18*sc,'H',L)+atom(x+13*sc,y,18*sc,'H',L)

def o2(x,y,sc=1.0,lab=True):
    L=None if lab else '-'
    return atom(x-17*sc,y,24*sc,'O',L)+atom(x+17*sc,y,24*sc,'O',L)

# ── 물의 전기 분해 장치 ──
def hofmann(ox=0,oy=0,s=1.0,gasL=60,gasR=120,anim=True,bubbles=True,labels=True,flow=True,eArrows=True,
            circuit=True,ticks=True,id_suffix=''):
    """왼쪽 관 = (+)극(산소), 오른쪽 관 = (−)극(수소). 기준 좌표 560×400."""
    X=lambda v: ox+v*s; Y=lambda v: oy+v*s
    xl,xr,w,top,bot,bb=190,370,26,40,250,290
    out=''
    # 몸체(물)
    path=(f'M{f(X(xl-w))} {f(Y(top+w))} A{f(w*s)} {f(w*s)} 0 0 1 {f(X(xl+w))} {f(Y(top+w))} L{f(X(xl+w))} {f(Y(bot))} '
          f'L{f(X(xr-w))} {f(Y(bot))} L{f(X(xr-w))} {f(Y(top+w))} A{f(w*s)} {f(w*s)} 0 0 1 {f(X(xr+w))} {f(Y(top+w))} '
          f'L{f(X(xr+w))} {f(Y(bb))} L{f(X(xl-w))} {f(Y(bb))} Z')
    out+=f'<path d="{path}" fill="{WATER}" stroke="none"/>'
    # 기체(위쪽) — 관 안쪽
    def gas(xc,h,dur):
        p=(f'M{f(X(xc-w+2))} {f(Y(top+w))} A{f((w-2)*s)} {f((w-2)*s)} 0 0 1 {f(X(xc+w-2))} {f(Y(top+w))} '
           f'L{f(X(xc+w-2))} {f(Y(top+2+h))} L{f(X(xc-w+2))} {f(Y(top+2+h))} Z')
        g=f'<path d="{p}" fill="#FFFFFF" stroke="none"/><line x1="{f(X(xc-w+2))}" y1="{f(Y(top+2+h))}" x2="{f(X(xc+w-2))}" y2="{f(Y(top+2+h))}" stroke="{WATER_E}" stroke-width="2"/>'
        if anim:
            return f'<g data-anim="scale" data-from="1,0.05" data-o="{f(X(xc))},{f(Y(top))}" data-dur="{dur}" data-delay=".3" data-ease="out">{g}</g>'
        return g
    out+=gas(xl,gasL,2.4)+gas(xr,gasR,2.4)
    out+=f'<path d="{path}" fill="none" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>'
    if ticks:
        for xc in (xl,xr):
            for k in range(10):
                yy=top+30+k*20
                ln=12 if k%2==0 else 7
                out+=f'<line x1="{f(X(xc+w))}" y1="{f(Y(yy))}" x2="{f(X(xc+w-ln))}" y2="{f(Y(yy))}" stroke="{MUTED}" stroke-width="1.5"/>'
    # 전극
    for xc in (xl,xr):
        out+=f'<rect x="{f(X(xc-5))}" y="{f(Y(195))}" width="{f(10*s)}" height="{f(117*s)}" rx="{f(2*s)}" fill="{ELEC}"/>'
    # 기포
    if bubbles:
        import random
        rnd=random.Random(7)
        for xc,n,gh in ((xl,3,gasL),(xr,5,gasR)):
            y0=188; y1=top+gh+16
            for i in range(n):
                bx=xc+rnd.uniform(-13,13); by=y0-(y0-y1)*i/max(n-1,1)
                rr=rnd.uniform(3,4.5)
                c=f'<circle cx="{f(X(bx))}" cy="{f(Y(by))}" r="{f(rr*s)}" fill="#FFFFFF" stroke="{WATER_E}" stroke-width="1.5"/>'
                if anim:
                    c=f'<g data-anim="move" data-from="0,{f(36*s)}" data-dur="{1.3+0.2*(i%3)}" data-delay="{0.17*i}" data-rep="loop" data-ease="lin">{c}</g>'
                out+=c
    return out

def hofmann_circuit(ox=0,oy=0,s=1.0,ywire=350):
    X=lambda v: ox+v*s; Y=lambda v: oy+v*s
    xl,xr=190,370
    parts=[["wire",[[X(xl),Y(312)],[X(xl),Y(ywire)],[X(272),Y(ywire)]]],
           ["wire",[[X(288),Y(ywire)],[X(xr),Y(ywire)],[X(xr),Y(312)]]],
           ["bat",[X(280),Y(ywire)],{"dir":"h","pos":"left","signs":True}]]
    return parts
