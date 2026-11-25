# -*- coding: utf-8 -*-
"""고급화학 2-1-1 그림 도우미 (1-1-1·1-M helpers에서 옮겨 고침)"""
import math, random
INK='#16233D';PLUS='#D7263D';MINUS='#1F6FD1';FIELD='#2E9E6A';EQUI='#E08A2C';BF='#7B4FC8';MUTED='#5B6B7F';GRAV='#8C99A6';OX='#C2410C';RD='#0E7490'
GAS='#F2A65A';GAS_S='#B4561C'   # 대단원 Ⅱ: 종류를 구분하지 않는 기체 분자
GLASS='#7E8B98';WATER='#DDEEF8';WATER_S='#9FC3DD'
def f(v): return ('%.1f'%v).rstrip('0').rstrip('.')
def T(x,y,tex=None,mix=None,size=20,anchor='middle',fill=None,halo=False,weight=None,extra=''):
    a=f'<text class="tex" x="{f(x)}" y="{f(y)}" '
    a+=(f'data-tex="{tex}" ' if tex is not None else f'data-mix="{mix}" ')
    a+=f'data-size="{size}" data-anchor="{anchor}"'
    if fill: a+=f' fill="{fill}"'
    if halo: a+=' data-halo="1"'
    if weight: a+=f' data-weight="{weight}"'
    return a+(' '+extra if extra else '')+'></text>'
def A(x1,y1,x2,y2,col='ink',w=3,d=False,extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}{",d" if d else ""}"{(" "+extra) if extra else ""}></g>'
def L(x1,y1,x2,y2,col=INK,w=2,dash=None,extra=''):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def P(pts,col=INK,w=2.5,fill='none',dash=None,extra='',close=False):
    d='M'+' L'.join(f'{f(x)} {f(y)}' for x,y in pts)+(' Z' if close else '')
    return f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def C(cx,cy,r,col=INK,w=2,fill='none',dash=None,extra=''):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def R(x,y,w,h,col=INK,sw=2,fill='none',rx=0,dash=None,extra=''):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}" stroke="{col}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def gm(x,y,r=10): return C(x,y,r,GAS_S,1.5,GAS)
def wave(x1,y1,x2,y2,col,amp=6,lam=14,w=3):   # 다시 정의(사본에서 잘린 것)
    dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
    pts=[]; n=max(2,int(Ln/2))
    for i in range(n+1):
        s=i/n*Ln; a=amp*math.sin(2*math.pi*s/lam)
        pts.append((x1+ux*s+px*a,y1+uy*s+py*a))
    return P(pts,col,w)
def svg(vb,width,label,body,cls='fig'):
    return f'<svg class="{cls}" viewBox="0 0 {vb[0]} {vb[1]}" style="width:{width}px" aria-label="{label}">'+''.join(body)+'</svg>'
def mol_box(x,y,w,h,n,seed,r=10,arrow=14,anim=True,fast=1.0,pts=None):
    """상자 안 기체 분자 n개 + 속도 화살표. 움직임: 무작위 왕복(그린 모습이 끝 모습)."""
    rnd=random.Random(seed); s=[]
    placed=[] if pts is None else list(pts)
    while pts is None and len(placed)<n:
        px=rnd.uniform(x+r+6,x+w-r-6); py=rnd.uniform(y+r+6,y+h-r-6)
        if all(math.hypot(px-a,py-b)>2.6*r+arrow*0.5 for a,b in placed): placed.append((px,py))
    for i,(px,py) in enumerate(placed):
        th=rnd.uniform(0,2*math.pi); L_=arrow*fast*rnd.uniform(.75,1.25)
        ex,ey=px+(r+L_)*math.cos(th),py+(r+L_)*math.sin(th)
        ex=min(max(ex,x+4),x+w-4); ey=min(max(ey,y+4),y+h-4)
        body=A(px+r*math.cos(th)*.9,py+r*math.sin(th)*.9,ex,ey,'ink',2)+gm(px,py,r)
        if anim:
            dx,dy=-6*math.cos(th)*fast,-6*math.sin(th)*fast
            s.append(f'<g data-anim="move" data-from="{f(dx)},{f(dy)}" data-rep="alt" data-dur="{f(0.9+0.5*rnd.random())}" data-ease="io">{body}</g>')
        else: s.append(body)
    return ''.join(s)
class Ax:
    """그래프 축: x0,y0 = 원점(화면), w,h, xr=(0,xmax), yr=(0,ymax)"""
    def __init__(s,x0,y0,w,h,xmax,ymax,xmin=0,ymin=0):
        s.x0,s.y0,s.w,s.h,s.xmax,s.ymax,s.xmin,s.ymin=x0,y0,w,h,xmax,ymax,xmin,ymin
    def X(s,v): return s.x0+(v-s.xmin)/(s.xmax-s.xmin)*s.w
    def Y(s,v): return s.y0-(v-s.ymin)/(s.ymax-s.ymin)*s.h
    def frame(s,xt,yt,xlab,ylab,xfmt=None,yfmt=None,grid=True,size=18):
        o=[]
        if grid:
            for v in xt[1:]: o.append(L(s.X(v),s.y0,s.X(v),s.y0-s.h,'#E2E7EC',1))
            for v in yt[1:]: o.append(L(s.x0,s.Y(v),s.x0+s.w,s.Y(v),'#E2E7EC',1))
        o.append(L(s.x0,s.y0,s.x0+s.w+8,s.y0,MUTED,2)); o.append(L(s.x0,s.y0,s.x0,s.y0-s.h-8,MUTED,2))
        for v in xt:
            o.append(L(s.X(v),s.y0,s.X(v),s.y0+6,MUTED,1.5)); o.append(T(s.X(v),s.y0+26,tex=(xfmt(v) if xfmt else str(v)),size=size))
        for v in yt:
            o.append(L(s.x0-6,s.Y(v),s.x0,s.Y(v),MUTED,1.5)); o.append(T(s.x0-10,s.Y(v)+6,tex=(yfmt(v) if yfmt else str(v)),size=size,anchor='end'))
        o.append(xlab); o.append(ylab)
        return ''.join(o)
    def curve(s,fn,a,b,n=160,col=INK,w=3,dash=None,extra=''):
        pts=[(s.X(a+(b-a)*i/n),s.Y(min(max(fn(a+(b-a)*i/n),s.ymin),s.ymax*1.02))) for i in range(n+1)]
        return P(pts,col,w,dash=dash,extra=extra)
# 맥스웰 분포 (SI)
Rg=8.314
def mb(v,T,M):  # M kg/mol → f(v) s/m
    a=M/(2*Rg*T)
    return 4*math.pi*(a/math.pi)**1.5*v*v*math.exp(-a*v*v)
def vp(T,M): return math.sqrt(2*Rg*T/M)
def vavg(T,M): return math.sqrt(8*Rg*T/(math.pi*M))
def vrms(T,M): return math.sqrt(3*Rg*T/M)
