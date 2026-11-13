# 4-4a/4-4b 그림 도우미 (좌표 계산). 템플릿의 ⟪식⟫을 이 모듈 이름공간에서 eval 한다.
import math, random
INK='#16233D'; PLUS='#D7263D'; MINUS='#1F6FD1'; FIELD='#2E9E6A'; EQUI='#E08A2C'; EQT='#B8661A'
MUTED='#5B6B7F'; BF='#7B4FC8'; GAS='#6C8EBF'
A_F='#F2A65A'; A_S='#B86A1F'; B_F='#8FD19E'; B_S='#2E7D4F'

def f(E,T):
    if E<=0: return 0.0
    return 2/math.sqrt(math.pi)*T**-1.5*math.sqrt(E)*math.exp(-E/T)

def _pt(X0,Y0,W,H,E,v,Emax,fmax):
    return X0+E/Emax*W, Y0-v/fmax*H

def dist(X0,Y0,W,H,T,Emax=7,fmax=0.52,n=120):
    d=[]
    for i in range(n+1):
        E=Emax*i/n; x,y=_pt(X0,Y0,W,H,E,f(E,T),Emax,fmax)
        d.append(('M' if i==0 else 'L')+f'{x:.1f} {y:.1f}')
    return ' '.join(d)

def tail(X0,Y0,W,H,T,Ea,Emax=7,fmax=0.52,n=60):
    x0,_=_pt(X0,Y0,W,H,Ea,0,Emax,fmax)
    d=[f'M{x0:.1f} {Y0:.1f}']
    for i in range(n+1):
        E=Ea+(Emax-Ea)*i/n; x,y=_pt(X0,Y0,W,H,E,f(E,T),Emax,fmax); d.append(f'L{x:.1f} {y:.1f}')
    x1,_=_pt(X0,Y0,W,H,Emax,0,Emax,fmax); d.append(f'L{x1:.1f} {Y0:.1f} Z')
    return ' '.join(d)

def fy(X0,Y0,W,H,T,E,Emax=7,fmax=0.52):
    return _pt(X0,Y0,W,H,E,f(E,T),Emax,fmax)

def ex(X0,W,E,Emax=7): return X0+E/Emax*W

def axes(X0,Y0,W,H,col=MUTED,sw=2):
    return (f'<line x1="{X0}" y1="{Y0}" x2="{X0+W+8}" y2="{Y0}" stroke="{col}" stroke-width="{sw}"/>'
            f'<polygon points="{X0+W+16},{Y0} {X0+W+6},{Y0-5} {X0+W+6},{Y0+5}" fill="{col}"/>'
            f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y0-H-8}" stroke="{col}" stroke-width="{sw}"/>'
            f'<polygon points="{X0},{Y0-H-16} {X0-5},{Y0-H-6} {X0+5},{Y0-H-6}" fill="{col}"/>')

def ediag(x0,x1,xp,x2,x3,yR,yT,yP):
    a=.55*(xp-x1); b=.55*(x2-xp)
    return (f'M{x0} {yR} L{x1} {yR} C{x1+a:.1f} {yR} {xp-a:.1f} {yT} {xp} {yT} '
            f'C{xp+b:.1f} {yT} {x2-b:.1f} {yP} {x2} {yP} L{x3} {yP}')

def dimv(x,y1,y2,col=EQUI,sw=2.5,extra=''):
    # y1 위, y2 아래, 양 끝 화살촉
    return (f'<g{extra}><line x1="{x}" y1="{y1+3}" x2="{x}" y2="{y2-3}" stroke="{col}" stroke-width="{sw}"/>'
            f'<polygon points="{x},{y1} {x-5},{y1+10} {x+5},{y1+10}" fill="{col}"/>'
            f'<polygon points="{x},{y2} {x-5},{y2-10} {x+5},{y2-10}" fill="{col}"/></g>')

def arrv(x,y1,y2,col=INK,sw=2.5):
    # y1 → y2 한쪽 화살표
    s=1 if y2>y1 else -1
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-s*9}" stroke="{col}" stroke-width="{sw}"/>'
            f'<polygon points="{x},{y2} {x-5},{y2-s*11} {x+5},{y2-s*11}" fill="{col}"/>')

def T(x,y,mix,size=22,anchor='start',fill=INK,extra=''):
    a='' if anchor=='start' else f' data-anchor="{anchor}"'
    return f'<text class="tex" x="{x}" y="{y}" data-mix="{mix}" data-size="{size}"{a} fill="{fill}"{extra}></text>'

def pts(seed,n,x0,y0,x1,y1,r,gap=4,avoid=()):
    rnd=random.Random(seed); out=[]; tries=0
    while len(out)<n and tries<20000:
        tries+=1
        x=rnd.uniform(x0+r,x1-r); y=rnd.uniform(y0+r,y1-r)
        if all((x-a)**2+(y-b)**2>(2*r+gap)**2 for a,b in out+list(avoid)):
            out.append((x,y))
    return out

def ab(x,y,kind,r=16,extra=''):
    fl,st=(A_F,A_S) if kind=='A' else (B_F,B_S)
    return (f'<g{extra}><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fl}" stroke="{st}" stroke-width="2"/>'
            f'<text class="tex" x="{x:.1f}" y="{y+6.5:.1f}" data-tex="\\mathrm{{{kind}}}" data-size="18" data-anchor="middle" fill="{INK}"></text></g>')

def gas(x,y,r=7,fill=GAS):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="#3F5F8F" stroke-width="1.2"/>'

def cube(x,y,s,c=('#E3D3B2','#CBB68C','#B39D72'),sw=1.5):
    # (x,y) = 앞 아래 꼭짓점, s = 한 변. 등각 투영
    dx=s*0.866; dy=s*0.5
    top=f'{x},{y-s} {x+dx},{y-s-dy} {x},{y-s-2*dy} {x-dx},{y-s-dy}'
    left=f'{x},{y} {x},{y-s} {x-dx},{y-s-dy} {x-dx},{y-dy}'
    right=f'{x},{y} {x},{y-s} {x+dx},{y-s-dy} {x+dx},{y-dy}'
    st='#7A6A4A'
    return (f'<polygon points="{left}" fill="{c[1]}" stroke="{st}" stroke-width="{sw}"/>'
            f'<polygon points="{right}" fill="{c[2]}" stroke="{st}" stroke-width="{sw}"/>'
            f'<polygon points="{top}" fill="{c[0]}" stroke="{st}" stroke-width="{sw}"/>')

def frac(T,Ea,Emax=12,n=4000):
    s=0; h=(Emax-Ea)/n
    for i in range(n): s+=f(Ea+(i+.5)*h,T)*h
    return s
