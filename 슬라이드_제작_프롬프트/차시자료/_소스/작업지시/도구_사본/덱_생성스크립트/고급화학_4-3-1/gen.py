# -*- coding: utf-8 -*-
"""고급화학 4-3-1 반응 속도의 표현과 반응 속도식 (a/b) — 그림 생성: tpl_a.html·tpl_b.html의 {{KEY}}를 SVG로 바꿔 두 덱의 slides.html을 만든다.
   labs_src.js → b 덱 labs.js(ac431ord), extra_src.css → 두 덱 extra.css, meta.json을 쓴다.
   python3 -I gen.py   (출력 경로 OUT_A/OUT_B — 이 덱 두 폴더만, assert로 막음)
   농도–시간·ln[A]–t·1/[A]–t 그래프는 모두 적분 속도식 계산값(calc.py와 같은 값)."""
import math, random, re, sys, os, shutil
from math import log, exp
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FA='4-3-1_반응_속도의_표현과_반응_속도식a'; FB='4-3-1_반응_속도의_표현과_반응_속도식b'
OUT_A=BASE+FA+'/'; OUT_B=BASE+FB+'/'
assert OUT_A=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-3-1_반응_속도의_표현과_반응_속도식a/', OUT_A
assert OUT_B=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-3-1_반응_속도의_표현과_반응_속도식b/', OUT_B
for o,fd in ((OUT_A,FA),(OUT_B,FB)):
    os.makedirs(o,exist_ok=True); assert os.path.isdir(o) and o.rstrip('/').endswith(fd), o
FIG={}
HL='#FFE45C'; CVV='#6A2C91'
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def stp(body,g=None): return f'<g class="step"'+(f' data-g="{g}"' if g else '')+f'>{body}</g>'
def atom(x,y,r,el,lab='-'):
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def lt(x,y,s,size=18,anchor='middle',fill=None,weight=None,halo=False): return T(x,y,mix=s,size=size,anchor=anchor,fill=fill,weight=weight,halo=halo)
def ylab(ax,s,size=18): return lt(ax.x0-6,ax.y0-ax.h-16,s,size,'start')
def xlab(ax,s,size=18): return lt(ax.x0+ax.w/2,ax.y0+48,s,size)
def pts(fn,ax,a,b,n=200): return [(ax.X(a+(b-a)*i/n),ax.Y(fn(a+(b-a)*i/n))) for i in range(n+1)]
def dot(x,y,col,r=6,fill=None): return C(x,y,r,col,2,fill or col)
def sq(x,y,col,s=6): return R(x-s,y-s,2*s,2*s,col,2,col)
def tri(x,y,col,s=7): return P([(x,y-s),(x+s,y+s*.8),(x-s,y+s*.8)],col,2,col,close=True)
def lsq(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sxx=sum((x-mx)**2 for x in xs); sxy=sum((x-mx)*(y-my) for x,y in zip(xs,ys)); syy=sum((y-my)**2 for y in ys)
    b=sxy/sxx; return b,my-b*mx,sxy*sxy/(sxx*syy)
def tf(v,d=2): return f'{v:.{d}f}'

# ═════ 공통 모형 ═════
K23=0.30; A23=0.160
N5=lambda t:A23*exp(-K23*t); NO2=lambda t:2*(A23-N5(t)); O2=lambda t:(A23-N5(t))/2
k28=log(2)/24; F28=lambda t:0.0600*exp(-k28*t)

def fig23(w=560,big=True,tang=False,pt=True,label='그림 Ⅳ-23 계산 모형'):
    ax=Ax(70,300,w-110,250,12,0.32); s=[]
    yt=(0,0.08,0.16,0.24,0.32)
    s.append(ax.frame((0,2,4,6,8,10,12),yt,ylab(ax,'몰농도 [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.2f}'))
    s.append(an('draw',P(pts(N5,ax,0,12),INK,3),dur='1.4'))
    s.append(an('draw',P(pts(NO2,ax,0,12),FIELD,3),dur='1.4'))
    s.append(an('draw',P(pts(O2,ax,0,12),FIELD,3,dash='9 6'),dur='1.4'))
    if pt:
        for t in (2,4,6,8,10,12):
            s.append(dot(ax.X(t),ax.Y(NO2(t)),FIELD,5)+sq(ax.X(t),ax.Y(O2(t)),FIELD,5)+tri(ax.X(t),ax.Y(N5(t)),INK,6))
    s.append(lt(ax.X(7.6),ax.Y(0.30)-4,'$[\\ce{NO2}]$',19,fill=FIELD,halo=True))
    s.append(lt(ax.X(10.4),ax.Y(0.076)-16,'$[\\ce{O2}]$',19,fill=FIELD,halo=True))
    s.append(lt(ax.X(2.9),ax.Y(0.055)+30,'$[\\ce{N2O5}]$',19,halo=True))
    return svg((w,356),w,'오산화 이질소 분해 반응에서 시간에 따른 N2O5, NO2, O2의 몰농도 변화(계산값)',s)

# ═════ a ═════
def cover_a():
    w=520; ax=Ax(60,300,410,250,12,0.32); s=[]
    s.append(ax.frame((0,4,8,12),(0,0.08,0.16,0.24),ylab(ax,'몰농도 [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.2f}'))
    s.append(an('draw',P(pts(N5,ax,0,12),INK,3.5),dur='1.6'))
    s.append(an('draw',P(pts(NO2,ax,0,12),FIELD,3.5),dur='1.6'))
    s.append(an('draw',P(pts(O2,ax,0,12),FIELD,3,dash='9 6'),dur='1.6'))
    t0=4; m=2*K23*N5(t0); x1,x2=1.2,7.4
    s.append(an('draw',L(ax.X(x1),ax.Y(NO2(t0)+m*(x1-t0)),ax.X(x2),ax.Y(NO2(t0)+m*(x2-t0)),PLUS,3),delay='1.4',dur='.8'))
    s.append(an('pop',dot(ax.X(t0),ax.Y(NO2(t0)),PLUS,7),delay='1.5',o=f'{f(ax.X(t0))},{f(ax.Y(NO2(t0)))}'))
    s.append(lt(ax.X(7.4),ax.Y(NO2(7.4))+30,'접선의 기울기','18',fill=PLUS))
    s.append(lt(ax.X(10.6),ax.Y(0.305)-12,'$\\ce{NO2}$',19,fill=FIELD))
    s.append(lt(ax.X(10.6),ax.Y(0.078)-14,'$\\ce{O2}$',19,fill=FIELD))
    s.append(lt(ax.X(1.6),ax.Y(0.11),'$\\ce{N2O5}$',19,anchor='start'))
    return svg((w,376),w,'표지: 오산화 이질소 분해의 몰농도–시간 계산 곡선과 4분에서 그은 접선',s,cls='fig cover-fig')
FIG['COVER_A']=cover_a()

def intro():
    s=[]; rnd=random.Random(7)
    def flask(x,y,mols,lab,sub):
        o=P([(x-40,y),(x-40,y+50),(x-95,y+160),(x+95,y+160),(x+40,y+50),(x+40,y)],GLASS,3)
        o+=mols+lt(x,y+192,lab,19,weight=700)+lt(x,y-12,sub,18,fill=MUTED)
        return o
    def h2(x,y,a=0): c,sn=math.cos(math.radians(a)),math.sin(math.radians(a)); return atom(x-6*c,y-6*sn,7,'H')+atom(x+6*c,y+6*sn,7,'H')
    def o2(x,y,a=0): c,sn=math.cos(math.radians(a)),math.sin(math.radians(a)); return atom(x-9*c,y-9*sn,10,'O')+atom(x+9*c,y+9*sn,10,'O')
    def h2o(x,y,a=0):
        o=''
        for d in (-52,52):
            t=math.radians(a+90+d); o+=atom(x+13*math.cos(t),y+13*math.sin(t),7,'H')
        return o+atom(x,y,10,'O')
    L1=[(-45,115,'h',20),(0,95,'h',-30),(45,120,'h',60),(-20,140,'h',0),(25,145,'o',10),(-55,145,'o',-40)]
    m=''.join(an('move',(h2 if k=='h' else o2)(130+dx,40+dy,a),**{'from':f'{rnd.choice((-5,5))},{rnd.choice((-4,4))}','rep':'alt','dur':f'{1.1+rnd.random()*.6:.1f}','ease':'io'}) for dx,dy,k,a in L1)
    s.append(flask(130,40,m,'몇 년이 지나도 그대로','$\\ce{2H2 + O2}$ 혼합 기체'))
    L2=[(-40,120,0),(0,100,40),(40,125,-30),(-10,145,180)]
    m2=''.join(an('pop',h2o(390+dx,40+dy,a),delay=f'{.3+i*.15:.2f}',o=f'{390+dx},{40+dy}') for i,(dx,dy,a) in enumerate(L2))
    star=P([(390+18*math.cos(math.radians(i*36))*(1 if i%2==0 else .45),118+18*math.sin(math.radians(i*36))*(1 if i%2==0 else .45)) for i in range(10)],EQUI,2,'#FFE45C',close=True)
    s.append(flask(390,40,an('pop',star,o='390,118',dur='.5')+m2,'불꽃 → 순식간에 반응','스파크를 만나면'))
    s.append(A(235,130,285,130,'ink',3))
    s.append(lt(130,262,'원자 수: H 8, O 4',18,fill=MUTED)+lt(390,262,'H 8, O 4 ($\\ce{4H2O}$)',18,fill=MUTED))
    return svg((520,275),500,'같은 수소와 산소 혼합 기체가 그대로 있을 때와 스파크로 순식간에 물이 될 때(원자 수 보존)',s)
FIG['INTRO']=intro()

def think_a():
    w=560; ax=Ax(70,300,450,250,10,1.0); s=[]
    s.append(ax.frame((0,2,4,6,8,10),(0,0.5,1.0),ylab(ax,'반응물의 몰농도 [M]'),xlab(ax,'시간 [s]'),yfmt=lambda v:'0' if v==0 else f'{v:.1f}'))
    fa=lambda t:exp(-0.5*t); fb=lambda t:exp(-0.12*t)
    s.append(an('draw',P(pts(fa,ax,0,10),INK,3.5),dur='1.4'))
    s.append(an('draw',P(pts(fb,ax,0,10),INK,3,dash='10 6'),dur='1.4'))
    s.append(lt(ax.X(3.0),ax.Y(fa(3))+28,'(가)',20,weight=700)+lt(ax.X(8),ax.Y(fb(8))-14,'(나)',20,weight=700))
    for fn,col,dx in ((fa,PLUS,0),(fb,MINUS,0.15)):
        x=ax.X(2+dx); s.append(stp(L(x,ax.Y(1),x,ax.Y(fn(2)),col,4)+lt(x+8,ax.Y((1+fn(2))/2)+6,f'{1-fn(2):.2f} M',18,'start',fill=col,halo=True),'thA'))
    s.append(L(ax.X(2),ax.y0,ax.X(2),ax.Y(1.0),MUTED,1.5,'5 5'))
    return svg((w,356),w,'반응 (가)와 (나)의 반응물 몰농도–시간 그래프: 처음 2초 동안 줄어든 농도 비교',s)
FIG['THINK_A']=think_a()

def link():
    w=500; ax=Ax(60,280,400,220,10,0.45); s=[]
    kf,kr=0.4,0.2; Aeq=kr/(kf+kr); Af=lambda t:Aeq+(1-Aeq)*exp(-(kf+kr)*t)
    vf=lambda t:kf*Af(t); vr=lambda t:kr*(1-Af(t))
    s.append(R(ax.X(6),ax.Y(0.45),ax.X(10)-ax.X(6),ax.h,'none',0,HL,extra='fill-opacity=".25"'))
    s.append(ax.frame((0,2,4,6,8,10),(0,0.2,0.4),ylab(ax,'반응 속도'),xlab(ax,'시간'),xfmt=lambda v:'',yfmt=lambda v:''))
    s.append(an('draw',P(pts(vf,ax,0,10),FIELD,3.5),dur='1.4'))
    s.append(an('draw',P(pts(vr,ax,0,10),BF,3,dash='9 6'),dur='1.4'))
    s.append(lt(ax.X(1.2),ax.Y(vf(1.2))-14,'정반응 속도',19,'start',fill=FIELD)+lt(ax.X(1.4),ax.Y(vr(1.4))+30,'역반응 속도',19,'start',fill=BF))
    s.append(lt(ax.X(8),ax.Y(0.38),'평형',20,weight=700))
    return svg((w,336),w,'평형에 이르는 동안 정반응 속도는 줄고 역반응 속도는 늘어 같아진다',s)
FIG['LINK']=link()

def ratedef():
    w=480; ax=Ax(60,280,380,220,10,1.0); s=[]
    fa=lambda t:exp(-0.25*t); fb=lambda t:1-exp(-0.25*t)
    s.append(ax.frame((0,2,4,6,8,10),(0,0.5,1.0),ylab(ax,'몰농도 [M]'),xlab(ax,'시간 [s]'),yfmt=lambda v:'0' if v==0 else f'{v:.1f}'))
    s.append(an('draw',P(pts(fa,ax,0,10),INK,3.5),dur='1.2')+an('draw',P(pts(fb,ax,0,10),FIELD,3.5),dur='1.2'))
    t1,t2=2,6
    for fn,col,side in ((fa,INK,1),(fb,FIELD,-1)):
        x1,y1,x2,y2=ax.X(t1),ax.Y(fn(t1)),ax.X(t2),ax.Y(fn(t2))
        s.append(stp(L(x1,y1,x2,y1,MUTED,2,'5 4')+L(x2,y1,x2,y2,col,3)+dot(x1,y1,col,5)+dot(x2,y2,col,5)+lt(x2+8,(y1+y2)/2+6,'$\\Delta[\\ce{%s}]$'%('A' if col==INK else 'B'),19,'start',fill=col,halo=True),'rd'))
    s.append(stp(lt((ax.X(t1)+ax.X(t2))/2,ax.Y(fa(t1))-10,'$\\Delta t$',19,halo=True),'rd'))
    s.append(lt(ax.X(9),ax.Y(fa(9))-12,'반응물 A',18,fill=INK)+lt(ax.X(9),ax.Y(fb(9))+30,'생성물 B',18,fill=FIELD))
    return svg((w,336),w,'반응물 A의 농도 감소와 생성물 B의 농도 증가, 같은 시간 간격의 농도 변화',s)
FIG['RATEDEF']=ratedef()
FIG['FIG23']=fig23()

def n2o5(x,y):
    P_=[(-24,4,'N'),(24,4,'N'),(0,-6,'O'),(-40,-10,'O'),(-32,24,'O'),(40,-10,'O'),(32,24,'O')]
    return ''.join(atom(x+dx,y+dy,10,e) for dx,dy,e in P_)
def no2(x,y): return atom(x-17,y+10,10,'O')+atom(x+17,y+10,10,'O')+atom(x,y,10,'N')
def o2m(x,y): return atom(x-9,y,10,'O')+atom(x+9,y,10,'O')
def coef():
    s=[]; w=500
    s.append(R(10,20,150,170,MUTED,2,'#F7F8FA',10)+R(230,20,260,170,MUTED,2,'#F7F8FA',10))
    s.append(n2o5(85,70)+n2o5(85,140))
    s.append(A(170,105,220,105,'ink',3))
    prods=[(280,60),(360,60),(280,140),(360,140)]
    s.append(''.join(an('move',no2(x,y),**{'from':f'{f(85-x)},{f((70 if y<100 else 140)-y)}','dur':'1.2','ease':'out','delay':'.3'}) for x,y in prods))
    s.append(an('move',o2m(440,100),**{'from':'-355,0','dur':'1.2','ease':'out','delay':'.3'}))
    s.append(lt(85,210,'$\\ce{2N2O5}$',20)+lt(320,210,'$\\ce{4NO2}$',20)+lt(440,210,'$\\ce{O2}$',20))
    s.append(lt(250,238,'N 4 = 4, O 10 = 8 + 2',18,fill=MUTED))
    # 막대: 같은 시간에 변한 몰수
    y0=380; sc=26
    for i,(lab,v,col) in enumerate((('$\\ce{N2O5}$ 감소',2,INK),('$\\ce{NO2}$ 생성',4,FIELD),('$\\ce{O2}$ 생성',1,FIELD))):
        x=150+i*120
        s.append(an('scale',R(x-25,y0-v*sc,50,v*sc,col,2,col,3,extra='fill-opacity=".35"'),**{'from':'1,0','o':f'{x},{y0}','delay':f'{.4+i*.15:.2f}'}))
        s.append(lt(x,y0-v*sc-10,f'{v}',20,weight=700)+lt(x,y0+26,lab,18))
    s.append(L(90,y0,470,y0,MUTED,2))
    s.append(lt(20,y0-100,'같은 시간에||변한 몰수',18,'start',fill=MUTED))
    return svg((w,420),w,'오산화 이질소 2개가 이산화 질소 4개와 산소 1개로 분해(원자 수 보존)하고, 같은 시간에 변한 몰수는 2:4:1',s)
FIG['COEF']=coef()

def tangent():
    w=580; ax=Ax(70,300,470,250,12,0.32); s=[]
    s.append(ax.frame((0,2,4,6,8,10,12),(0,0.08,0.16,0.24,0.32),ylab(ax,'$[\\ce{NO2}]$ [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.2f}'))
    s.append(P(pts(NO2,ax,0,12),FIELD,3.5))
    t0=4
    for i,dt in enumerate((6,3,1.5)):
        x1,y1,x2,y2=ax.X(t0),ax.Y(NO2(t0)),ax.X(t0+dt),ax.Y(NO2(t0+dt))
        s.append(stp(L(x1,y1,x2,y2,MUTED,2.2,'7 5')+dot(x2,y2,MUTED,4.5)+(lt(x2+4,y2+28,f'$\\Delta t={dt:g}$',18,'start',fill=MUTED,halo=True) if i==0 else ''),f'sec{i}'))
    # Δt=6 삼각형
    x1,y1,x2,y2=ax.X(t0),ax.Y(NO2(t0)),ax.X(t0+6),ax.Y(NO2(t0+6))
    s.append(stp(L(x1,y1,x2,y1,MUTED,1.5,'3 4')+L(x2,y1,x2,y2,MUTED,1.5,'3 4'),'sec0'))
    m=2*K23*N5(t0); a1,a2=1.4,7.0
    s.append(stp(an('draw',L(ax.X(a1),ax.Y(NO2(t0)+m*(a1-t0)),ax.X(a2),ax.Y(NO2(t0)+m*(a2-t0)),PLUS,3.5),dur='.8',on='step')+lt(ax.X(0.3),ax.Y(0.29),'접선의 기울기 $\\dfrac{d[\\ce{NO2}]}{dt}$',19,'start',fill=PLUS,halo=True),'tan'))
    s.append(dot(ax.X(t0),ax.Y(NO2(t0)),PLUS,6))
    s.append(lt(ax.X(t0)+4,ax.Y(NO2(t0))+34,'$t$',19,halo=True)+lt(ax.X(12),ax.Y(0.05),'할선: $\\Delta t=6,\\ 3,\\ 1.5$ min',18,'end',fill=MUTED))
    return svg((w,356),w,'이산화 질소의 몰농도 곡선에서 4분부터 시간 간격을 줄인 할선들이 4분의 접선에 가까워짐',s)
FIG['TANGENT']=tangent()

def init():
    w=520; ax=Ax(70,300,410,250,12,0.32); s=[]
    s.append(ax.frame((0,4,8,12),(0,0.08,0.16,0.24,0.32),ylab(ax,'$[\\ce{NO2}]$ [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.2f}'))
    s.append(P(pts(NO2,ax,0,12),FIELD,3.5))
    for t0,col,a1,a2,lab in ((0,PLUS,0,2.6,'초기 반응 속도'),(4,MUTED,2,6.6,''),(8,MUTED,5.5,11,'')):
        m=2*K23*N5(t0)
        s.append(an('draw',L(ax.X(a1),ax.Y(NO2(t0)+m*(a1-t0)),ax.X(a2),ax.Y(NO2(t0)+m*(a2-t0)),col,3 if col==PLUS else 2.4,None if col==PLUS else '8 5'),dur='.7',delay=f'{.3+t0*.08:.2f}'))
        s.append(dot(ax.X(t0),ax.Y(NO2(t0)),col,5.5))
        s.append(lt(ax.X(t0)+(26 if t0 else 34),ax.Y(NO2(t0))+(30 if t0 else -10),f'{m:.3f}',18,'start' if t0 else 'start',fill=col,halo=True))
    s.append(lt(ax.X(2.7),ax.Y(0.27),'초기 반응 속도','19',fill=PLUS,halo=True))
    s.append(lt(ax.X(12),ax.Y(0.04),'접선 기울기 (M/min)',18,'end',fill=MUTED))
    return svg((w,356),w,'이산화 질소 생성 곡선의 0분, 4분, 8분 접선: 기울기가 0.096, 0.029, 0.009 M/min으로 줄어듦',s)
FIG['INIT']=init()

def q02():
    w=440; ax=Ax(70,250,330,200,12,0.32); s=[]
    s.append(ax.frame((0,4,8,12),(0,0.16,0.32),ylab(ax,'$[\\ce{NO2}]$ [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.2f}'))
    s.append(P(pts(NO2,ax,0,12),FIELD,3.5))
    s.append(L(ax.X(4),ax.y0,ax.X(4),ax.Y(NO2(4)),MUTED,1.5,'5 4')+L(ax.x0,ax.Y(NO2(4)),ax.X(4),ax.Y(NO2(4)),MUTED,1.5,'5 4'))
    s.append(dot(ax.X(4),ax.Y(NO2(4)),PLUS,5.5)+lt(ax.x0+6,ax.Y(NO2(4))-8,'0.224',18,'start',fill=MUTED,halo=True))
    return svg((w,306),w,'이산화 질소 몰농도 곡선과 4분의 값 0.224 M',s)
FIG['Q02']=q02()

def surf():
    s=[]; w=500
    def cube(x,y,a,col='#B9C2CC'):
        d=a*.45
        top=P([(x,y),(x+a,y),(x+a+d,y-d),(x+d,y-d)],INK,1.5,'#DDE3E9',close=True)
        side=P([(x+a,y),(x+a+d,y-d),(x+a+d,y+a-d),(x+a,y+a)],INK,1.5,'#9AA5B1',close=True)
        front=R(x,y,a,a,INK,1.5,col)
        return top+side+front
    s.append(cube(40,80,110)+lt(120,240,'덩어리 1개',19,weight=700)+lt(120,268,'겉넓이 $6a^2$',19))
    s.append(A(200,140,245,140,'ink',3)+lt(222,124,'자름',18,fill=MUTED))
    sm=''
    for j in range(2):
        for i in range(2):
            for k in range(2):
                sm+=cube(280+i*72+k*26,70+j*72-k*26,52)
    s.append(an('pop',sm,o='370,140',dur='.9'))
    s.append(lt(390,240,'작은 조각 8개',19,weight=700)+lt(390,268,'겉넓이 $12a^2$ (2배)',19))
    s.append(lt(120,310,'쇠못, 분필 덩어리',18,fill=MUTED)+lt(390,310,'철 가루, 분필 가루',18,fill=MUTED))
    return svg((w,325),w,'한 변 a인 정육면체를 8조각으로 자르면 겉넓이가 2배가 된다',s)
FIG['SURF']=surf()

def ex4():
    s=[]; w=420; y0=200; sc=280
    for i,(lab,v,col) in enumerate((('$\\ce{H2}$ 감소',0.48,INK),('$\\ce{O2}$ 감소',0.24,INK),('$\\ce{H2O}$ 증가',0.48,FIELD))):
        x=90+i*120
        s.append(an('scale',R(x-30,y0-v*sc,60,v*sc,col,2,col,3,extra='fill-opacity=".35"'),**{'from':'1,0','o':f'{x},{y0}','delay':f'{.2+i*.15:.2f}'}))
        s.append(lt(x,y0-v*sc-10,f'{v:.2f}',20,weight=700)+lt(x,y0+28,lab,18))
    s.append(L(30,y0,400,y0,MUTED,2))
    s.append(lt(210,y0+60,'단위 $\\text{mol/(L}\\cdot\\text{s)}$, 계수비 2 : 1 : 2',18,fill=MUTED))
    return svg((w,275),w,'수소 감소 0.48, 산소 감소 0.24, 수증기 증가 0.48 mol/(L·s) 막대',s)
FIG['EX4']=ex4()

def conc():
    s=[]; w=540; rnd=random.Random(11)
    def box(x,n,lab):
        o=R(x,20,230,210,INK,3,'#FAFBFC',8); placed=[]
        while len(placed)<2*n:
            px,py=rnd.uniform(x+20,x+210),rnd.uniform(40,210)
            if all(math.hypot(px-a,py-b)>30 for a,b in placed): placed.append((px,py))
        for i,(px,py) in enumerate(placed):
            body=C(px,py,11,PLUS if i%2==0 else MINUS,2,'#F8D3D8' if i%2==0 else '#D3E3F8')
            o+=an('move',body,**{'from':f'{rnd.choice((-6,6))},{rnd.choice((-5,5))}','rep':'alt','dur':f'{0.9+rnd.random()*.5:.1f}','ease':'io'})
        return o+lt(x+115,262,lab,19,weight=700)
    s.append(box(15,4,'농도 작음')+box(295,8,'농도 2배'))
    s.append(C(30,295,10,PLUS,2,'#F8D3D8')+lt(48,301,'반응물 A',18,'start')+C(190,295,10,MINUS,2,'#D3E3F8')+lt(208,301,'반응물 B',18,'start'))
    s.append(lt(525,301,'부피는 같다',18,'end',fill=MUTED))
    return svg((w,315),w,'같은 부피에 반응물 분자가 4쌍일 때와 8쌍일 때: 농도가 크면 단위 부피 속 분자 수가 많다',s)
FIG['CONC']=conc()

def order():
    w=540; ax=Ax(70,300,430,250,2,4.2); s=[]
    s.append(ax.frame((0,1,2),(0,1,2,4),ylab(ax,'반응 속도 ($k=1$)'),xlab(ax,'$[\\ce{A}]$'),xfmt=lambda v:str(v),yfmt=lambda v:str(v)))
    s.append(an('draw',P(pts(lambda c:1,ax,0,2),INK,3,dash='4 5'),dur='1')+an('draw',P(pts(lambda c:c,ax,0,2),INK,3,dash='12 6'),dur='1')+an('draw',P(pts(lambda c:c*c,ax,0,2.05),FIELD,3.5),dur='1'))
    s.append(lt(ax.X(1.92),ax.Y(1)-10,'0차',19,'end')+lt(ax.X(1.94),ax.Y(1.94)-16,'1차',19,'end')+lt(ax.X(1.6),ax.Y(2.56)-12,'2차',19,'end',fill=FIELD))
    for v,col in ((1,INK),(2,INK),(4,FIELD)):
        s.append(an('pop',dot(ax.X(2),ax.Y(v),col,6),o=f'{f(ax.X(2))},{f(ax.Y(v))}',delay='1'))
    s.append(L(ax.X(1),ax.y0,ax.X(1),ax.Y(1),MUTED,1.5,'5 4')+L(ax.X(2),ax.y0,ax.X(2),ax.Y(4),MUTED,1.5,'5 4'))
    s.append(lt(ax.X(2)+12,ax.Y(4)+6,'×4',19,'start',fill=FIELD,weight=700)+lt(ax.X(2)+12,ax.Y(2)+6,'×2',19,'start',weight=700)+lt(ax.X(2)+12,ax.Y(1)+6,'×1',19,'start',weight=700))
    return svg((w,356),w,'반응물 농도에 따른 0차, 1차, 2차 반응의 반응 속도: 농도 2배에서 1배, 2배, 4배',s)
FIG['ORDER']=order()

def steps10():
    s=[]; w=330; y0=300; sc=8.5
    for i,(v,lab) in enumerate(((3.20,'실험 1'),(6.40,'실험 2'),(25.6,'실험 3'))):
        x=60+i*100
        s.append(an('scale',R(x-28,y0-v*sc,56,v*sc,FIELD,2,FIELD,3,extra='fill-opacity=".35"'),**{'from':'1,0','o':f'{x},{y0}','delay':f'{.2+i*.2:.1f}'}))
        s.append(lt(x,y0-v*sc-10,f'{v:.2f}' if v<10 else f'{v:.1f}',19,weight=700)+lt(x,y0+26,lab,18))
    s.append(L(20,y0,320,y0,MUTED,2))
    s.append(lt(160,y0-112,'×2',20,fill=PLUS,weight=700)+lt(196,y0-170,'×4',20,fill=PLUS,weight=700,anchor='end'))
    s.append(lt(160,y0-88,'$[\\ce{O2}]$×2',18,fill=MUTED)+lt(226,y0-146,'$[\\ce{NO}]$×2',18,fill=MUTED,anchor='end'))
    s.append(lt(165,y0+56,'초기 반응 속도 ($10^{-3}\\ \\text{mol/(L}\\cdot\\text{s)}$)',18,fill=MUTED))
    return svg((w,370),w,'표 Ⅳ-10의 초기 반응 속도 막대: 실험 1에서 2로 2배, 2에서 3으로 4배',s)
FIG['STEPS10']=steps10()

# ═════ b ═════
def mini3(x0,y0,data,lin,w=150,h=100,cols=True,labels=True,size=18):
    """data: (ts, cs) → 세 그래프. lin: 직선인 칸 번호(0,1,2)"""
    ts,cs=data; o=''
    trans=(lambda c:c, lambda c:log(c), lambda c:1/c)
    for j in range(3):
        ys=[trans[j](c) for c in cs]; lo,hi=min(ys),max(ys); pad=(hi-lo)*.08
        X=lambda t:x0+j*(w+30)+(t-ts[0])/(ts[-1]-ts[0])*w; Y=lambda v:y0-(v-lo+pad)/(hi-lo+2*pad)*h
        o+=L(x0+j*(w+30),y0,x0+j*(w+30)+w+6,y0,MUTED,1.5)+L(x0+j*(w+30),y0,x0+j*(w+30),y0-h-6,MUTED,1.5)
        good=(j==lin)
        o+=P([(X(t),Y(v)) for t,v in zip(ts,ys)],FIELD if good else INK,4 if good else 2.2)
    return o
def cover_b():
    s=[]; w=540
    ts=[i*5 for i in range(21)]
    s.append(an('draw',mini3(40,250,(ts,[0.06*exp(-0.0289*t) for t in ts]),1,w=135,h=170),dur='1.4'))
    for j,lab in enumerate(('$[\\ce{A}]$','$\\ln[\\ce{A}]$','$\\dfrac{1}{[\\ce{A}]}$')):
        s.append(lt(40+j*165+68,300,lab,20))
    s.append(lt(40+165+68,70,'직선!',20,fill=FIELD,weight=700))
    s.append(lt(270,26,'1차 반응 자료를 세 가지로 그리면',18,fill=MUTED))
    return svg((w,330),w,'표지: 1차 반응 자료의 [A]–t, ln[A]–t, 1/[A]–t 그래프 중 ln[A]–t만 직선',s,cls='fig cover-fig')
FIG['COVER_B']=cover_b()

def think_b():
    w=560; ax=Ax(80,300,440,250,100,0.0600); s=[]
    s.append(ax.frame((0,24,48,72,96),(0,0.015,0.030,0.045,0.060),ylab(ax,'$[\\ce{N2O5}]$ [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.3f}'))
    s.append(an('draw',P(pts(F28,ax,0,100),INK,3.5),dur='1.4'))
    s.append(L(ax.X(24),ax.y0,ax.X(24),ax.Y(0.03),MUTED,1.8,'6 5')+L(ax.x0,ax.Y(0.03),ax.X(24),ax.Y(0.03),MUTED,1.8,'6 5'))
    s.append(dot(ax.X(24),ax.Y(0.03),INK,5.5)+lt(ax.X(24)+10,ax.Y(0.03)-12,'24분',19,'start',weight=700,halo=True))
    s.append(L(ax.x0,ax.Y(0.015),ax.X(100),ax.Y(0.015),MUTED,1.5,'3 5'))
    s.append(lt(ax.X(70),ax.Y(0.015)-12,'0.0150 M까지는?',19,fill=PLUS,halo=True))
    return svg((w,356),w,'45 °C에서 N2O5 몰농도 곡선: 0.0600 M에서 0.0300 M까지 24분',s)
FIG['THINK_B']=think_b()

def first():
    s=[]; w=420; y0=230; sc=190
    for i in range(5):
        v=0.5**i; x=50+i*80
        s.append(an('scale',R(x-24,y0-v*sc,48,v*sc,INK,2,'#C9D2DB',3),**{'from':'1,0','o':f'{x},{y0}','delay':f'{.2+i*.18:.2f}'}))
        s.append(lt(x,y0+26,f'{i*24}',18))
        if i: s.append(lt(x-40,y0-0.5**(i-1)*sc*0.72-6,'×½',19,fill=PLUS,weight=700))
    s.append(L(20,y0,410,y0,MUTED,2)+lt(400,y0+52,'시간 [min]',18,'end'))
    s.append(lt(20,22,'남은 $\\ce{N2O5}$ (24분마다)',18,'start',fill=MUTED))
    return svg((w,295),w,'1차 반응에서 같은 시간 24분마다 남은 양이 같은 비율(절반)로 줄어듦',s)
FIG['FIRST']=first()

def fig25():
    s=[]; w=620
    a1=Ax(70,280,220,220,100,0.0600); a2=Ax(380,280,210,220,100,-2.0,ymin=-6.0)
    s.append(a1.frame((0,50,100),(0,0.03,0.06),ylab(a1,'$[\\ce{N2O5}]$ [M]'),xlab(a1,'$t$ [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.2f}'))
    s.append(an('draw',P(pts(F28,a1,0,100),INK,3.2),dur='1.2'))
    s.append(a2.frame((0,50,100),(-6,-4,-2),ylab(a2,'$\\ln[\\ce{N2O5}]$'),xlab(a2,'$t$ [min]'),yfmt=lambda v:str(int(v))))
    s.append(an('draw',P(pts(lambda t:log(F28(t)),a2,0,100),FIELD,4.5),dur='1.2',delay='.4'))
    for t in range(0,101,12): s.append(dot(a2.X(t),a2.Y(log(F28(t))),FIELD,4.5))
    # 기울기 삼각형 20→80
    xA,xB=20,80; yA,yB=log(F28(xA)),log(F28(xB))
    s.append(stp(L(a2.X(xA),a2.Y(yA),a2.X(xB),a2.Y(yA),MUTED,1.8,'5 4')+L(a2.X(xB),a2.Y(yA),a2.X(xB),a2.Y(yB),MUTED,1.8,'5 4')+lt(a2.X(50),a2.Y(yA)-10,'60 min',18,halo=True)+lt(a2.X(xB)+6,a2.Y((yA+yB)/2)+30,f'{yB-yA:.2f}',18,'start',halo=True)+lt(a2.X(50),a2.Y(-5.6),'기울기 $=-0.0289$',19,fill=FIELD,halo=True)))
    s.append(lt(a2.x0+8,a2.Y(log(0.06))-10,'$\\ln0.0600=-2.81$',18,'start',halo=True))
    s.append(A(300,170,355,170,'ink',3)+lt(327,154,'ln',18,fill=MUTED))
    return svg((w,346),w,'45 °C N2O5 분해: [N2O5]–t 곡선과 ln[N2O5]–t 직선(기울기 −0.0289/min, 절편 −2.81)',s)
FIG['FIG25']=fig25()

def fig26():
    s=[]; w=500; k2,A0=0.25,0.0500
    Af=lambda t:1/(k2*t+1/A0)
    a2=Ax(70,300,390,250,200,75)
    s.append(a2.frame((0,50,100,150,200),(0,20,40,60),ylab(a2,'$\\dfrac{1}{[\\ce{A}]}$ [$\\text{M}^{-1}$]'),xlab(a2,'$t$ [s]'),yfmt=lambda v:str(v)))
    s.append(an('draw',P(pts(lambda t:1/Af(t),a2,0,200),FIELD,4.5),dur='1.2'))
    for t in range(0,201,25): s.append(dot(a2.X(t),a2.Y(1/Af(t)),FIELD,4.5))
    s.append(lt(a2.X(100),a2.Y(58),'기울기 $=k$',20,fill=FIELD,halo=True)+lt(a2.X(8),a2.Y(20)+30,'$y$절편 $=\\dfrac{1}{[\\ce{A}]_0}=20$',19,'start',halo=True))
    s.append(lt(a2.X(200),a2.Y(14),'$k=0.25\\ \\text{L/(mol}\\cdot\\text{s)}$',18,'end',fill=MUTED))
    return svg((w,356),w,'2차 반응의 1/[A]–t 직선(기울기 k, 절편 1/[A]0), 계산값',s)
FIG['FIG26']=fig26()

def fig27():
    s=[]; w=520; k0,A0=1.0e-5,4.0e-3
    ax=Ax(80,250,390,200,400,4.0)
    s.append(ax.frame((0,100,200,300,400),(0,1,2,3,4),ylab(ax,'$[\\ce{NH3}]$ [$10^{-3}$ M]'),xlab(ax,'$t$ [s]'),yfmt=lambda v:str(v)))
    s.append(an('draw',P(pts(lambda t:max(A0-k0*t,0)*1e3,ax,0,400),FIELD,4.5),dur='1.2'))
    s.append(lt(ax.X(230),ax.Y(2.6),'기울기 $=-k$',20,fill=FIELD,halo=True))
    # W 표면
    y=470; o=''
    for i in range(9): o+=atom(70+i*45,y,20,'W','-')
    s.append(R(40,y-6,440,40,'none',0,'#E7EAEE')+o)
    mols=''
    for i in range(9):
        x=70+i*45
        mols+=atom(x-9,y-36,7,'H')+atom(x+9,y-36,7,'H')+atom(x,y-46,7,'H')+atom(x,y-34,10,'N')
    s.append(an('pop',mols,o=f'250,{y-30}',dur='.8'))
    gas=''
    for x,yy in ((120,370),(260,355),(400,368)):
        gas+=an('move',atom(x-9,yy+2,7,'H')+atom(x+9,yy+2,7,'H')+atom(x,yy-12,7,'H')+atom(x,yy,10,'N'),**{'from':'6,-6','rep':'alt','dur':'1.2','ease':'io'})
    s.append(gas+lt(40,402,'기다리는 $\\ce{NH3}$',18,'start',fill=MUTED)+lt(260,y+48,'$\\ce{W}$ 표면의 자리가 모두 차 있다',18,fill=MUTED))
    return svg((w,530),w,'0차 반응: [NH3]–t 직선과 텅스텐 표면 자리가 모두 암모니아로 찬 모습',s)
FIG['FIG27']=fig27()

def judge():
    s=[]; w=660
    ts=[i*20 for i in range(21)]
    rows=(('0차',[4.0e-3-1.0e-5*t*0.95 for t in ts],0),('1차',[0.06*exp(-3*t/400) for t in ts],1),('2차',[1/(0.25*t*2+20) for t in ts],2))
    for j,lab in enumerate(('$[\\ce{A}]$–$t$','$\\ln[\\ce{A}]$–$t$','$\\dfrac{1}{[\\ce{A}]}$–$t$')):
        s.append(lt(150+j*180,30,lab,19,weight=700))
    for i,(lab,cs,lin) in enumerate(rows):
        y0=150+i*130
        s.append(an('draw',mini3(80,y0,(ts,cs),lin,w=140,h=88),dur='1',delay=f'{i*.25:.2f}'))
        s.append(lt(40,y0-38,lab,20,weight=700,fill=FIELD))
        s.append(R(80+lin*170-8,y0-100,166,108,FIELD,2.5,'none',8,'6 4'))
    return svg((w,420),w,'0차, 1차, 2차 반응 자료를 [A]–t, ln[A]–t, 1/[A]–t로 그리면 각각 한 그래프만 직선',s)
FIG['JUDGE']=judge()

def hl1bar():
    w=480; ax=Ax(80,290,370,240,72,0.0600); s=[]
    s.append(ax.frame((0,24,48,72),(0,0.015,0.030,0.045,0.060),ylab(ax,'$[\\ce{N2O5}]$ [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.3f}'))
    s.append(an('draw',P(pts(F28,ax,0,72),INK,3.5),dur='1.2'))
    s.append(an('draw',P(pts(lambda t:0.03*exp(-k28*t),ax,0,72),INK,3,dash='10 6'),dur='1.2',delay='.3'))
    s.append(L(ax.X(24),ax.y0,ax.X(24),ax.Y(0.0315),MUTED,1.8,'6 5'))
    s.append(dot(ax.X(24),ax.Y(0.03),INK,5)+dot(ax.X(24),ax.Y(0.015),INK,5))
    s.append(lt(ax.X(26),ax.Y(0.03)-10,'0.0600 → 0.0300',18,'start',halo=True)+lt(ax.X(26),ax.Y(0.015)+28,'0.0300 → 0.0150',18,'start',halo=True))
    s.append(lt(ax.X(50),ax.Y(0.052),'두 경우 모두 $t_{1/2}=24$분',19,fill=PLUS,weight=700,halo=True))
    return svg((w,350),w,'초기 농도 0.0600 M과 0.0300 M인 1차 반응: 두 경우 모두 반감기 24분',s)
FIG['HL1BAR']=hl1bar()

def fig28():
    w=620; ax=Ax(80,300,500,250,96,0.0600); s=[]
    s.append(ax.frame((0,24,48,72,96),(0,0.0075,0.0150,0.0300,0.0600),ylab(ax,'$[\\ce{N2O5}]$ [M]'),xlab(ax,'시간 [min]'),yfmt=lambda v:'0' if v==0 else f'{v:.4f}',grid=False))
    s.append(an('draw',P(pts(F28,ax,0,96),INK,3.5),dur='1.4'))
    for i,t in enumerate((24,48,72)):
        v=F28(t)
        s.append(stp(L(ax.X(t),ax.y0,ax.X(t),ax.Y(v),MUTED,1.8,'6 5')+L(ax.x0,ax.Y(v),ax.X(t),ax.Y(v),MUTED,1.8,'6 5')+dot(ax.X(t),ax.Y(v),INK,5)+
                 lt((ax.X(t)+ax.X(t-24))/2,ax.y0-12,'$t_{1/2}$',19,fill=PLUS,halo=True)+lt(ax.X(t)+8,ax.Y(v)-12,['첫 번째','두 번째','세 번째'][i]+' 반감기',18,'start',halo=True),f'h{i}'))
    return svg((w,356),w,'45 °C N2O5 분해: 24, 48, 72분마다 농도가 0.0300, 0.0150, 0.0075 M으로 반씩 줄어듦',s)
FIG['FIG28']=fig28()

def hl20():
    s=[]; w=620
    k2,A0=0.10,0.100; F2=lambda t:1/(k2*t+1/A0)
    a1=Ax(70,180,500,130,800,0.100)
    s.append(a1.frame((0,100,300,700,800),(0,0.05,0.10),ylab(a1,'2차 $[\\ce{A}]$ [M]'),xlab(a1,'$t$ [s]'),yfmt=lambda v:'0' if v==0 else f'{v:.2f}',grid=False))
    s.append(an('draw',P(pts(F2,a1,0,800),INK,3.2),dur='1.2'))
    for t,lab in ((100,'100 s'),(300,'200 s'),(700,'400 s')):
        s.append(L(a1.X(t),a1.y0,a1.X(t),a1.Y(F2(t)),MUTED,1.6,'5 4')+dot(a1.X(t),a1.Y(F2(t)),INK,4.5))
    for (t1,t2,lab) in ((0,100,'100 s'),(100,300,'200 s'),(300,700,'400 s')):
        s.append(stp(lt((a1.X(t1)+a1.X(t2))/2,a1.Y(0.012),lab,18,fill=PLUS,halo=True),'h2'))
    s.append(lt(a1.X(800),a1.Y(0.08),'점점 길어짐',19,'end',fill=PLUS,weight=700))
    k0,B0=1.0e-5,4.0e-3; F0=lambda t:max(B0-k0*t,0)*1e3
    a2=Ax(70,420,500,130,400,4.0)
    s.append(a2.frame((0,200,300,350,400),(0,2,4),ylab(a2,'0차 $[\\ce{A}]$ [$10^{-3}$ M]'),xlab(a2,'$t$ [s]'),yfmt=lambda v:str(v),grid=False))
    s.append(an('draw',P(pts(F0,a2,0,400),INK,3.2),dur='1.2',delay='.3'))
    for t in (200,300,350): s.append(L(a2.X(t),a2.y0,a2.X(t),a2.Y(F0(t)),MUTED,1.6,'5 4')+dot(a2.X(t),a2.Y(F0(t)),INK,4.5))
    for (t1,t2,lab) in ((0,200,'200 s'),(200,300,'100 s'),(300,350,'50')):
        s.append(stp(lt((a2.X(t1)+a2.X(t2))/2,a2.Y(0.45),lab,18,fill=MINUS,halo=True),'h0'))
    s.append(lt(a2.X(400),a2.Y(3.4),'점점 짧아짐',19,'end',fill=MINUS,weight=700))
    return svg((w,480),w,'2차 반응은 반감기가 100, 200, 400 s로 길어지고 0차 반응은 200, 100, 50 s로 짧아짐',s)
FIG['HL20']=hl20()

def cvset():
    s=[]; w=420
    s.append(R(10,60,70,60,INK,2,'#FFF3C4',8)+lt(45,145,'광원',18))
    s.append(an('dash',L(80,90,140,90,'#F2C230',4,'8 6'),speed='40',extra='data-flow="1"') if False else '')
    s.append(L(80,90,150,90,'#E0A800',4))
    s.append(R(150,70,26,40,INK,2,'#7FC97F',3)+lt(163,145,'590 nm',18))
    s.append(L(176,90,215,90,'#7FC97F',4))
    s.append(R(215,45,60,95,INK,2.5,'#FFFFFF',4)+an('fade',R(218,60,54,77,'none',0,CVV,2,extra='fill-opacity=".75"'),dur='2.4',rep='alt'))
    s.append(lt(245,165,'큐벳',18))
    s.append(L(275,90,315,90,'#B79CD0',4))
    s.append(R(315,60,80,60,INK,2,'#E7EAEE',8)+lt(355,96,'센서',18)+lt(355,145,'데이터 수집',18))
    s.append(lt(210,205,'$\\ce{CV+}$ (보라) + $\\ce{OH-}$ → $\\ce{CVOH}$ (무색)',18))
    s.append(lt(210,235,'흡광도 $A$ ∝ $[\\ce{CV+}]$',18,fill=MUTED))
    return svg((w,250),w,'광원, 590 nm 필터, 크리스털 바이올렛 큐벳, 센서로 이루어진 흡광도 측정 장치',s)
FIG['CVSET']=cvset()

def cvres():
    s=[]; w=620; kp=0.010
    ts=[i*15 for i in range(41) if 0.80*exp(-kp*i*15)>=0.02]; As=[0.80*exp(-kp*t) for t in ts]
    labs=('$A$–$t$','$\\ln A$–$t$','$\\dfrac{1}{A}$–$t$'); r2=[lsq(ts,[fn(a) for a in As])[2] for fn in (lambda a:a,log,lambda a:1/a)]
    s.append(an('draw',mini3(40,200,(ts,As),1,w=160,h=150),dur='1.3'))
    for j in range(3):
        s.append(lt(40+j*190+80,240,labs[j],20)+lt(40+j*190+80,272,f'$R^2={r2[j]:.3f}$',18,fill=FIELD if j==1 else INK))
    s.append(lt(40+190+80,30,'직선 → 1차',19,fill=FIELD,weight=700))
    return svg((w,290),w,'크리스털 바이올렛 예시 자료의 A–t, ln A–t, 1/A–t 그래프와 결정 계수',s)
FIG['CVRES']=cvres()

def radio():
    w=500; ax=Ax(70,280,390,230,23000,1.0); s=[]
    s.append(ax.frame((0,5730,11460,17190,22920),(0,0.25,0.5,1.0),ylab(ax,'남은 $\\ce{^{14}C}$ 비율'),xlab(ax,'시간 [년]'),xfmt=lambda v:str(v),yfmt=lambda v:{0:'0',0.25:'1/4',0.5:'1/2',1.0:'1'}[v],grid=False,size=17 if False else 18))
    s.append(an('draw',P(pts(lambda t:0.5**(t/5730),ax,0,23000),INK,3.5),dur='1.4'))
    for i in range(1,4):
        t=5730*i; v=0.5**i
        s.append(L(ax.X(t),ax.y0,ax.X(t),ax.Y(v),MUTED,1.6,'5 4')+dot(ax.X(t),ax.Y(v),INK,5))
    s.append(lt(ax.X(5730)+8,ax.Y(0.5)-10,'$t_{1/2}=5730$년',19,'start',fill=PLUS,halo=True))
    return svg((w,346),w,'탄소-14의 붕괴: 5730년마다 남은 비율이 1/2, 1/4, 1/8로 줄어듦',s)
FIG['RADIO']=radio()

def ex5():
    w=470; t5=[0,50,100,150,200,300,400,500]; c5=[8.00e-3,6.58e-3,5.59e-3,4.85e-3,4.29e-3,3.48e-3,2.93e-3,2.53e-3]
    b,a,r2=lsq(t5,[1/c for c in c5])
    ax=Ax(70,330,370,280,500,400); s=[]
    s.append(ax.frame((0,100,200,300,400,500),(0,100,200,300,400),ylab(ax,'$\\dfrac{1}{[\\ce{NO2}]}$ [$\\text{M}^{-1}$]'),xlab(ax,'$t$ [s]'),yfmt=lambda v:str(v)))
    s.append(an('draw',L(ax.X(0),ax.Y(a),ax.X(500),ax.Y(a+b*500),FIELD,3.5),dur='1',delay='.6'))
    for i,(t,c) in enumerate(zip(t5,c5)): s.append(an('pop',dot(ax.X(t),ax.Y(1/c),INK,5.5),o=f'{f(ax.X(t))},{f(ax.Y(1/c))}',delay=f'{i*.07:.2f}'))
    s.append(lt(ax.X(330),ax.Y(110),f'기울기 $={b:.3f}$',19,fill=FIELD,halo=True)+lt(ax.X(330),ax.Y(110)+28,f'$R^2={r2:.3f}$',18,fill=FIELD,halo=True))
    return svg((w,386),w,'연습 문제 5 자료의 1/[NO2]–t 그래프: 직선, 기울기 0.541',s)
FIG['EX5']=ex5()

# ═════ 조립 ═════
def build(tplname,out,meta):
    tpl=open(os.path.join(HERE,tplname),encoding='utf-8').read()
    keys=re.findall(r'\{\{(\w+)\}\}',tpl)
    for k in keys:
        if k not in FIG: sys.exit('no fig '+k)
    html=re.sub(r'\{\{(\w+)\}\}',lambda m:FIG[m.group(1)],tpl)
    open(out+'slides.html','w',encoding='utf-8').write(html)
    shutil.copy(os.path.join(HERE,'extra_src.css'),out+'extra.css')
    open(out+'meta.json','w',encoding='utf-8').write(meta+'\n')
    print('ok',out[-30:],len(html),'sections',html.count('<section'),'anim',html.count('data-anim'))
    return set(keys)
used=build('tpl_a.html',OUT_A,'{"title": "반응 속도의 표현과 반응 속도식 (1) 반응 속도와 반응 속도식", "file": "4-3-1_반응_속도의_표현과_반응_속도식a", "header": "Ⅳ-3-1 반응 속도의 표현과 반응 속도식 (고등 고급 화학 230–241쪽)"}')
used|=build('tpl_b.html',OUT_B,'{"title": "반응 속도의 표현과 반응 속도식 (2) 적분 속도식과 반감기", "file": "4-3-1_반응_속도의_표현과_반응_속도식b", "header": "Ⅳ-3-1 반응 속도의 표현과 반응 속도식 (고등 고급 화학 230–241쪽)"}')
if set(FIG)-used: print('unused figs',set(FIG)-used)
src=open(os.path.join(HERE,'labs_src.js'),encoding='utf-8').read()
open(OUT_B+'labs.js','w',encoding='utf-8').write(src)
if os.path.exists(OUT_A+'labs.js'): os.remove(OUT_A+'labs.js')
print('labs ok')
