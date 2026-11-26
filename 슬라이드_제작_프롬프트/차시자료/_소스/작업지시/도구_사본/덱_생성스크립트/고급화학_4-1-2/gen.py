# -*- coding: utf-8 -*-
"""고급화학 4-1-2 상평형과 용해도 평형 — 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   extra_src.css를 extra.css로 복사하고 meta.json을 쓴다(실험실 없음 → labs.js 없음).
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)
   상평형 그림·증기압·기체 용해도는 calc.py의 물성식(IAPWS·Span–Wagner·헨리 상수) 계산값으로 그린다."""
import math, random, re, sys, os, shutil
from math import exp, log, log10, sqrt
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
from calc import *
from h import R
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FOLDER='4-1-2_상평형과_용해도_평형'
OUT=BASE+FOLDER+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-1-2_상평형과_용해도_평형/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FOLDER), OUT
FIG={}
HL='#FFE45C'
SOLID_F='#D3DCE8'; LIQ_F='#DDEEF8'; GAS_F='#F7F9FB'
CAT_F='#F8D3D8'; AN_F='#D3E3F8'; AGCL='#F4F6F8'; AGCRO='#B5432F'; PBI2='#E8C21E'
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def mv(body,frm,**k): k['from']=frm; return an('move',body,**k)
def step(g,body): return f'<g class="step" data-g="{g}">{body}</g>'
def stp(body): return f'<g class="step">{body}</g>'
def atom(x,y,r,el,lab='-'): return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el},{lab}"></g>'
def ion(x,y,r,sign,lab=None,size=18):
    o=C(x,y,r,PLUS if sign>0 else MINUS,2,CAT_F if sign>0 else AN_F)
    if lab: o+=T(x,y+6,tex=lab,size=size)
    else: o+=T(x,y+7,mix=('+' if sign>0 else '−'),size=20,weight=700,fill=PLUS if sign>0 else MINUS)
    return o
def water(cx,cy,ang,s=1.0):
    """물 분자: O 중심 (cx,cy), 두 H의 이등분선 방향 ang(도) — H는 그 방향 ±52°"""
    o=''; d=13*s
    for da in (-52.25,52.25):
        a=math.radians(ang+da); o+=atom(cx+d*math.cos(a),cy+d*math.sin(a),8*s,'H')
    return atom(cx,cy,12*s,'O')+o
def lg(v): return log10(v)
def smooth(pts,n=12):
    """Catmull–Rom 보간 (그림 Ⅳ-13 문헌값 점 잇기)"""
    out=[]; P_=[pts[0]]+pts+[pts[-1]]
    for i in range(1,len(P_)-2):
        p0,p1,p2,p3=P_[i-1],P_[i],P_[i+1],P_[i+2]
        for k in range(n):
            t=k/n; t2=t*t; t3=t2*t
            out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t2+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t3) for j in (0,1)))
    out.append(pts[-1]); return out
def yt_log(v): return '10^{%d}'%v if v not in (0,1) else ('1' if v==0 else '10')

# ═════ 상평형 그림 곡선 (계산) ═════
W_TT=273.16; W_TC=647.096
def water_curves():
    sub=[(T-273.15,h2o_sub(T)) for T in [233.15+i*(W_TT-233.15)/80 for i in range(81)]]
    vap=[(T-273.15,h2o_vap(T)) for T in [W_TT+i*(W_TC-W_TT)/200 for i in range(201)]]
    Ps=[10**(lg(h2o_sub(W_TT))+i*(3-lg(h2o_sub(W_TT)))/80) for i in range(81)]
    melt=[(h2o_melt_T(P)-273.15,P) for P in Ps]
    return sub,vap,melt
C_TT=CO2_Tt; C_TC=304.1282
def co2_curves():
    sub=[(T-273.15,co2_sub(T)) for T in [173.15+i*(C_TT-173.15)/80 for i in range(81)]]
    vap=[(T-273.15,co2_vap(T)) for T in [C_TT+i*(C_TC-C_TT)/120 for i in range(121)]]
    melt=[]
    T=C_TT
    while True:
        P=co2_melt(T); melt.append((T-273.15,P))
        if P>=1000: break
        T+=0.1
    return sub,vap,melt
def phase(ax,sub,vap,melt,ymin,ymax,anim=True,lw=3.2):
    """ax: x=°C, y=log10 atm. 영역 칠 + 경계선"""
    X=lambda p:(ax.X(p[0]),ax.Y(lg(p[1])))
    top=ax.Y(ymax); bot=ax.Y(ymin); left=ax.X(ax.xmin); right=ax.X(ax.xmax)
    subc=[p for p in sub if lg(p[1])>=ymin]
    s=[R(left,top,right-left,bot-top,'none',0,GAS_F)]
    # 고체 영역: 왼쪽 위 ~ 융해 곡선 ~ 승화 곡선
    sol=[(left,top)]+[X(p) for p in reversed(melt)]+[X(p) for p in reversed(subc)]+[(X(subc[0])[0],bot),(left,bot)]
    s.append(P(sol,'none',0,SOLID_F,close=True))
    liq=[X(melt[-1])]+[X(p) for p in reversed(melt)][1:]+[X(p) for p in vap]+[(X(vap[-1])[0],top)] if False else \
        [X(p) for p in melt]+[(X(melt[-1])[0],top),(right,top)]+[(right,X(vap[-1])[1])]+[X(p) for p in reversed(vap)]
    s.append(P(liq,'none',0,LIQ_F,close=True))
    curves=[P([X(p) for p in subc],INK,lw),P([X(p) for p in vap],INK,lw),P([X(p) for p in melt],INK,lw)]
    if anim:
        for i,c in enumerate(curves): s.append(an('draw',c,dur='1.0',delay=f(0.3+0.5*i)))
    else: s+=curves
    return ''.join(s)
def logframe(ax,xt,ydec,xlab,ylab,size=18,xfmt=None):
    return ax.frame(xt,list(ydec),xlab,ylab,xfmt=xfmt,yfmt=lambda v:yt_log(v),size=size)

# ═════ 1 표지 ═════
def cover():
    s=[]
    ax=Ax(60,230,340,190,400,3,xmin=-60,ymin=-4)
    sub,vap,melt=water_curves()
    s.append(phase(ax,sub,vap,melt,-4,3,anim=True,lw=3))
    s.append(L(ax.x0,ax.y0,ax.x0+ax.w+6,ax.y0,MUTED,2)+L(ax.x0,ax.y0,ax.x0,ax.y0-ax.h-6,MUTED,2))
    s.append(T(ax.x0+ax.w,ax.y0+26,mix='온도',size=19,anchor='end',fill=MUTED)+T(ax.x0+4,ax.y0-ax.h-12,mix='압력',size=19,anchor='start',fill=MUTED))
    tp=(ax.X(0.01),ax.Y(lg(0.00604))); cp=(ax.X(373.95),ax.Y(lg(217.7)))
    s.append(an('pop',C(*tp,7,INK,2,EQUI),o=f'{f(tp[0])},{f(tp[1])}',delay='1.8')+an('pop',C(*cp,7,INK,2,PLUS),o=f'{f(cp[0])},{f(cp[1])}',delay='2.0'))
    s.append(T(ax.X(-38),ax.Y(1.6),mix='고체',size=19,weight=700)+T(ax.X(150),ax.Y(1.2),mix='액체',size=19,weight=700)+T(ax.X(240),ax.Y(-2.6),mix='기체',size=19,weight=700))
    # 아래: 포화 용액 비커 (용해 ⇌ 석출)
    bx,by,bw,bh=120,270,220,150
    s.append(R(bx,by+30,bw,bh-30,'none',0,WATER))
    s.append(P([(bx,by),(bx,by+bh),(bx+bw,by+bh),(bx+bw,by)],GLASS,3))
    rnd=random.Random(7)
    for i in range(9):
        x=bx+20+i*21; y=by+bh-12-(i%2)*10
        s.append(R(x-8,y-8,16,16,INK,1.5,AGCL,3))
    for i,(x,y,sg) in enumerate(((150,330,1),(205,322,-1),(262,338,1),(305,318,-1),(180,360,-1),(285,362,1))):
        s.append(mv(C(x,y,9,PLUS if sg>0 else MINUS,2,CAT_F if sg>0 else AN_F),f'{rnd.choice((-4,4))},{rnd.choice((-4,4))}',rep='alt',dur=f(1.0+0.15*i),ease='io'))
    s.append(A(bx+bw+24,by+bh-20,bx+bw+24,by+60,'field',3)+A(bx+bw+44,by+60,bx+bw+44,by+bh-20,'bfield',3))
    s.append(T(bx+bw+36,by+46,tex='\\ce{&lt;=&gt;}',size=20))
    s.append(T(bx-10,by+96,mix='용해',size=19,anchor='end',fill=FIELD,weight=700)+T(bx-10,by+124,mix='석출',size=19,anchor='end',fill=BF,weight=700))
    return svg((460,440),440,'물의 상평형 그림과, 고체가 남은 포화 용액에서 용해와 석출이 함께 일어나는 모습',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 2 그림 Ⅳ-7 ln K–1/T ═════
def lnk():
    s=[]; ax=Ax(130,330,360,280,10,10)
    s.append(L(ax.x0,ax.y0,ax.x0+ax.w+10,ax.y0,MUTED,2)+L(ax.x0,ax.y0,ax.x0,ax.y0-ax.h-10,MUTED,2))
    s.append(T(ax.x0+ax.w+6,ax.y0+28,mix='$\\dfrac{1}{T}$',size=20,anchor='end',fill=MUTED)+T(ax.x0-8,ax.y0-ax.h-18,mix='$\\ln K$',size=20,anchor='start',fill=MUTED))
    s.append(an('draw',L(ax.X(0.5),ax.Y(1.5),ax.X(9.5),ax.Y(8.5),INK,4),dur='1.1'))
    s.append(an('draw',L(ax.X(0.5),ax.Y(8.5),ax.X(9.5),ax.Y(1.5),INK,4,'12 7'),dur='1.1',delay='.5'))
    s.append(T(ax.X(9.6),ax.Y(8.6)-12,mix='발열 ($\\Delta H^\\circ&lt;0$)',size=19,anchor='end',weight=700,halo=True))
    s.append(T(ax.X(9.6),ax.Y(1.4)+30,mix='흡열 ($\\Delta H^\\circ&gt;0$)',size=19,anchor='end',weight=700,halo=True))
    s.append(A(ax.X(7.5),ax.y0+44,ax.X(2.5),ax.y0+44,'plus',3)+T(ax.X(5),ax.y0+70,mix='$T$ 증가',size=19,fill=PLUS,weight=700))
    s.append(A(ax.x0-34,ax.Y(2),ax.x0-34,ax.Y(8),'field',3)+T(ax.x0-44,ax.Y(5),mix='생성물||증가',size=18,anchor='end',fill=FIELD))
    return svg((520,420),520,'발열 반응은 1/T가 커질수록 ln K가 커지는 직선, 흡열 반응은 작아지는 직선',s)
FIG['LNK']=lnk()

# ═════ 4 생각 열기: 주사기 ═════
def syringe():
    s=[]; y0,y1=120,200
    s.append(R(20,y0,340,y1-y0,GLASS,3,'#FFFFFF',4))
    s.append(R(22,y0+2,110,y1-y0-4,'none',0,WATER))
    s.append(R(4,y0+28,16,24,INK,2,'#9AA5B1',3)+T(4,y0-10,mix='막음',size=18,anchor='start',fill=MUTED))
    pl=R(130,y0+3,14,y1-y0-6,INK,2,'#5B6B7F',2)+R(144,155,250,10,INK,2,'#C9D2DB',2)+R(394,130,14,60,INK,2,'#C9D2DB',3)
    s.append(mv(pl,'-100,0',dur='1.4',delay='.3',ease='out'))
    for i,(x,y,r) in enumerate(((50,182,6),(80,170,5),(105,186,7),(64,150,4),(95,140,5),(40,135,4))):
        s.append(an('pop',C(x,y,r,WATER_S,2,'#FFFFFF'),o=f'{x},{y}',delay=f(1.3+0.18*i),rep='loop',dur='1.2'))
    s.append(A(300,236,420,236,'ink',3)+T(360,266,mix='당긴다',size=19,weight=700))
    s.append(T(77,y1+34,mix='40 °C 물',size=19,weight=700))
    s.append(T(230,y0-16,mix='물 위의 압력 ↓',size=19,fill=MINUS,weight=700))
    s.append(R(20,290,440,48,MUTED,1.5,'#F7F9FB',8)+T(240,322,mix='물 위 압력 &lt; 증기 압력(40 °C: 0.073 atm) → 끓음',size=19))
    return svg((470,350),480,'끝을 막은 주사기의 피스톤을 당기면 미지근한 물에서 거품이 생기며 끓는다',s)
FIG['SYRINGE']=syringe()

# ═════ 6 세 상태와 상전이 ═════
def states():
    s=[]
    box={'g':(170,10),'s':(20,230),'l':(320,230)}; w,h=150,120
    for k,(x,y) in box.items(): s.append(R(x,y,w,h,INK,2.5,{'g':GAS_F,'s':SOLID_F,'l':LIQ_F}[k],12))
    # 고체: 격자 + 제자리 진동
    for i in range(4):
        for j in range(3):
            s.append(an('move',gm(40+i*36,252+j*34,11),**{'from':'1.5,0','rep':'swing','dur':'.25'}))
    # 액체
    rnd=random.Random(3)
    pts=[(338,330),(366,322),(394,330),(422,322),(450,330),(352,298),(380,292),(408,300),(436,294),(372,264),(420,268)]
    for i,(x,y) in enumerate(pts): s.append(mv(gm(x,y,11),f'{rnd.choice((-3,3))},{rnd.choice((-2,2))}',rep='alt',dur=f(.7+.05*i),ease='io'))
    # 기체
    s.append(mol_box(170,10,w,h,4,11,r=11,arrow=12))
    s.append(T(245,154,mix='기체',size=20,weight=700)+T(95,374,mix='고체',size=20,weight=700)+T(395,374,mix='액체',size=20,weight=700))
    def pair(x1,y1,x2,y2,l1,l2,lx,ly,anc):
        dx,dy=x2-x1,y2-y1; L_=math.hypot(dx,dy); nx,ny=-dy/L_*7,dx/L_*7
        o=A(x1+nx,y1+ny,x2+nx,y2+ny,'field',3)+A(x2-nx,y2-ny,x1-nx,y1-ny,'bfield',3)
        o+=T(lx,ly,mix=l1,size=19,fill=FIELD,weight=700,anchor=anc)+T(lx,ly+24,mix=l2,size=19,fill=BF,weight=700,anchor=anc)
        return o
    s.append(pair(175,290,315,290,'융해 →','← 응고',245,214,'middle'))
    s.append(pair(110,226,180,140,'승화','승화',112,170,'end'))
    s.append(pair(400,226,330,140,'기화','응축',398,170,'start'))
    s.append(T(245,404,mix='상평형: 두 화살표의 속도가 같고 $\\Delta G=0$',size=19,fill=MUTED))
    return svg((490,416),490,'고체, 액체, 기체 사이의 상전이와 두 방향의 화살표',s)
FIG['STATES']=states()

# ═════ 7 그림 Ⅳ-8 증발과 응축 ═════
def evap():
    s=[]; x0,y0,w,h=14,40,170,300
    s.append(R(x0,y0,w,h,GLASS,3,'#FFFFFF',10)+R(x0-6,y0-12,w+12,14,INK,2,'#9AA5B1',4))
    s.append(R(x0+3,y0+h-90,w-6,87,'none',0,WATER,6))
    rnd=random.Random(5)
    for i in range(7):
        x=rnd.uniform(x0+20,x0+w-20); y=rnd.uniform(y0+30,y0+h-120)
        s.append(mv(gm(x,y,8),f'{rnd.choice((-5,5))},{rnd.choice((-5,5))}',rep='alt',dur=f(.8+.1*i),ease='io'))
    for i in range(10):
        s.append(gm(x0+18+(i%5)*33,y0+h-60+(i//5)*30,8))
    s.append(A(x0+50,y0+h-100,x0+50,y0+h-160,'field',3)+A(x0+120,y0+h-160,x0+120,y0+h-100,'bfield',3))
    s.append(T(x0+50,y0+h-166,mix='증발',size=18,fill=FIELD,weight=700))
    s.append(T(x0+136,y0+h-166,mix='응축',size=18,fill=BF,weight=700))
    # 그래프: 속도–시간
    ax=Ax(250,330,270,250,5,1.2)
    s.append(L(ax.x0,ax.y0,ax.x0+ax.w+8,ax.y0,MUTED,2)+L(ax.x0,ax.y0,ax.x0,ax.y0-ax.h-8,MUTED,2))
    s.append(T(ax.x0+ax.w+6,ax.y0+26,mix='시간',size=19,anchor='end',fill=MUTED)+T(ax.x0-4,ax.y0-ax.h-16,mix='속도',size=19,anchor='start',fill=MUTED))
    te=3.0
    s.append(step('ev',R(ax.X(te),ax.Y(1.2),ax.X(5)-ax.X(te),ax.h,'none',0,HL,extra='fill-opacity=".25"')+L(ax.X(te),ax.y0,ax.X(te),ax.Y(1.2),MUTED,1.5,'5 4')+T(ax.X(4.0),ax.Y(1.12),mix='평형',size=18,fill=MUTED,weight=700)))
    s.append(an('draw',ax.curve(lambda t:1.0,0,5,col=FIELD,w=3.5),dur='1.0'))
    s.append(an('draw',ax.curve(lambda t:1-exp(-1.5*t),0,5,col=BF,w=3.5,dash='9 6'),dur='1.4',delay='.4'))
    s.append(T(ax.X(0.3),ax.Y(1.0)-12,mix='증발 속도',size=18,anchor='start',fill=FIELD,weight=700))
    s.append(T(ax.X(1.1),ax.Y(0.5),mix='응축 속도',size=18,anchor='start',fill=BF,weight=700,halo=True))
    return svg((540,370),540,'닫힌 용기에서 증발 속도는 일정하고 응축 속도는 커져 같아지면 평형',s)
FIG['EVAP']=evap()

# ═════ 8 ln P–1/T (물, 계산값) ═════
def cc():
    s=[]; ax=Ax(80,330,360,280,3.5,0.5,xmin=2.6,ymin=-4)
    s.append(ax.frame([2.6,2.8,3.0,3.2,3.4],[-4,-3,-2,-1,0],T(450,380,mix='$\\tfrac{1}{T}\\times10^{3}$ [1/K]',size=19,anchor='end',fill=MUTED),
                      T(74,36,mix='$\\ln P$ ($P$ [atm])',size=19,anchor='start',fill=MUTED),xfmt=lambda v:'%.1f'%v,size=18))
    sl=-40700/8.314/1000; b=log(1.0)-sl*1000/373.15
    s.append(an('draw',ax.curve(lambda x:sl*x+b,2.62,3.48,col=INK,w=3),dur='1.2'))
    for i,tc in enumerate((20,40,60,80,100)):
        x=1000/(tc+273.15); y=log(h2o_vap(tc+273.15))
        s.append(an('pop',C(ax.X(x),ax.Y(y),6,PLUS,1.5,PLUS),o=f'{f(ax.X(x))},{f(ax.Y(y))}',delay=f(1.0+0.12*i)))
        s.append(T(ax.X(x)+(10 if tc>20 else -10),ax.Y(y)-10,mix=f'{tc} °C',size=18,anchor='start' if tc>20 else 'end',fill=MUTED,halo=True))
    s.append(T(ax.X(2.65),ax.Y(-3.3),mix='기울기 $=-\\dfrac{\\Delta H_\\text{증발}^\\circ}{R}$',size=19,anchor='start',halo=True))
    s.append(T(ax.X(2.65),ax.Y(-3.85),mix='점: 물의 실제 증기 압력',size=18,anchor='start',fill=MUTED))
    return svg((460,392),460,'물의 ln P와 1/T는 기울기가 −ΔH증발/R인 직선이다',s)
FIG['CC']=cc()

# ═════ 10 융해 곡선의 기울기 (물·CO2) ═════
def slope():
    s=[]
    # 물
    a1=Ax(70,340,170,240,1,1000,xmin=-10,ymin=0)
    s.append(a1.frame([-10,-5,0],[0,500,1000],T(250,390,mix='$t$ [°C]',size=18,anchor='end',fill=MUTED),T(30,74,mix='$P$ [atm]',size=18,anchor='start',fill=MUTED),size=17))
    pts=[(h2o_melt_T(P)-273.15,P) for P in [1+i*10 for i in range(101)]]
    s.append(P([(a1.X(-10),a1.Y(0)),(a1.X(-10),a1.Y(1000))]+[(a1.X(t),a1.Y(p)) for t,p in reversed(pts)]+[(a1.X(pts[0][0]),a1.Y(0))],'none',0,SOLID_F,close=True,extra='fill-opacity=".8"'))
    s.append(an('draw',P([(a1.X(t),a1.Y(p)) for t,p in pts],INK,3.5),dur='1.2'))
    s.append(T(a1.X(-7.5),a1.Y(120),mix='얼음',size=19,weight=700)+T(a1.X(-1.2),a1.Y(880),mix='물',size=19,weight=700))
    s.append(T(155,24,mix='물: 기울기 음수',size=19,weight=700))
    s.append(step('sl',A(a1.X(-5),a1.Y(30),a1.X(-5),a1.Y(760),'minus',3)+T(a1.X(-9.6),a1.Y(800),mix='압력↑ → 녹음',size=18,anchor='start',fill=MINUS,weight=700,halo=True)))
    # CO2
    a2=Ax(345,340,170,240,-30,1000,xmin=-60,ymin=0)
    s.append(a2.frame([-60,-45,-30],[0,500,1000],T(525,390,mix='$t$ [°C]',size=18,anchor='end',fill=MUTED),T(305,74,mix='$P$ [atm]',size=18,anchor='start',fill=MUTED),size=17))
    _,_,m2=co2_curves()
    m2=[(t,p) for t,p in m2 if p<=1000]
    s.append(P([(a2.X(-60),a2.Y(0)),(a2.X(-60),a2.Y(1000))]+[(a2.X(t),a2.Y(p)) for t,p in reversed(m2)]+[(a2.X(m2[0][0]),a2.Y(0))],'none',0,SOLID_F,close=True,extra='fill-opacity=".8"'))
    s.append(an('draw',P([(a2.X(t),a2.Y(p)) for t,p in m2],INK,3.5),dur='1.2',delay='.4'))
    s.append(T(a2.X(-52),a2.Y(780),mix='고체',size=19,weight=700)+T(a2.X(-38),a2.Y(220),mix='액체',size=19,weight=700))
    s.append(T(430,24,mix='$\\ce{CO2}$: 기울기 양수',size=19,weight=700))
    s.append(T(275,424,mix='계산값: 물은 1000 atm에서 −8.9 °C, $\\ce{CO2}$는 −37 °C에서 녹는다',size=17,fill=MUTED))
    return svg((540,436),540,'물의 융해 곡선은 압력이 커질수록 녹는점이 낮아지고, 이산화 탄소는 높아진다',s)
FIG['SLOPE']=slope()

# ═════ 11 그림 Ⅳ-9 물의 상평형 그림 ═════
def water_fig(paths=False):
    s=[]
    if paths: ax=Ax(80,350,450,310,140,3,xmin=-60,ymin=-4)
    else: ax=Ax(80,350,460,310,400,3,xmin=-60,ymin=-4)
    sub,vap,melt=water_curves()
    vap2=vap if not paths else [p for p in vap if p[0]<=140]
    s.append(phase(ax,sub,vap2,melt,-4,3,anim=not paths))
    xt=[-60,0,100,200,300,400] if not paths else [-60,-40,-20,0,20,40,60,80,100,120,140]
    s.append(logframe(ax,xt if not paths else [-40,0,40,80,120],range(-4,4),T(ax.x0+ax.w+6,ax.y0+48,mix='온도 [°C]',size=19,anchor='end',fill=MUTED),
                      T(ax.x0-10,ax.y0-ax.h-20,mix='압력 [atm] (로그 눈금)',size=19,anchor='start',fill=MUTED),size=17))
    s.append(L(ax.x0,ax.Y(0),ax.x0+ax.w,ax.Y(0),MUTED,1.5,'6 4'))
    tp=(ax.X(0.01),ax.Y(lg(0.00604)))
    if not paths:
        cp=(ax.X(373.95),ax.Y(lg(217.7)))
        s.append(an('pop',C(*tp,8,INK,2,EQUI),o=f'{f(tp[0])},{f(tp[1])}',delay='1.9')+an('pop',C(*cp,8,INK,2,PLUS),o=f'{f(cp[0])},{f(cp[1])}',delay='2.1'))
        s.append(T(tp[0]+14,tp[1]+30,mix='삼중점 ($T_3$ 0.01 °C, $P_3$ 0.0060 atm)',size=18,anchor='start',halo=True,weight=700))
        s.append(T(cp[0]-8,cp[1]-18,mix='임계점 ($T_\\mathrm{c}$ 374 °C, $P_\\mathrm{c}$ 218 atm)',size=18,anchor='end',halo=True,weight=700))
        for t,lab in ((0,'$T_\\mathrm{m}$'),(100,'$T_\\mathrm{b}$')):
            s.append(C(ax.X(t),ax.Y(0),5,INK,1.5,'#FFFFFF')+T(ax.X(t)+(-8 if t==0 else 8),ax.Y(0)-10,mix=lab,size=18,anchor='end' if t==0 else 'start',halo=True))
        s.append(T(ax.x0+ax.w-4,ax.Y(0)-8,mix='1 atm',size=17,anchor='end',fill=MUTED))
        s.append(T(ax.X(-34),ax.Y(1.5),mix='고체',size=21,weight=700)+T(ax.X(130),ax.Y(1.6),mix='액체',size=21,weight=700)+T(ax.X(250),ax.Y(-2.2),mix='기체',size=21,weight=700))
        s.append(T(ax.X(-58),ax.Y(-3.75),mix='승화 곡선',size=17,anchor='start',fill=MUTED)+T(ax.X(205),ax.Y(0.9),mix='증발(기화) 곡선',size=17,anchor='start',fill=MUTED,halo=True))
        s.append(T(ax.X(6),ax.Y(2.6),mix='융해 곡선',size=17,anchor='start',fill=MUTED,halo=True))
        return svg((560,420),580,'물의 상평형 그림: 실제 값으로 그린 승화·융해·증발 곡선, 삼중점과 임계점',s)
    # 세 경로
    s.append(an('pop',C(*tp,7,INK,2,EQUI),o=f'{f(tp[0])},{f(tp[1])}'))
    s.append(T(ax.X(-38),ax.Y(1.9),mix='고체',size=20,weight=700)+T(ax.X(70),ax.Y(1.9),mix='액체',size=20,weight=700)+T(ax.X(100),ax.Y(-1.6),mix='기체',size=20,weight=700))
    s.append(T(ax.X(30),ax.Y(0)+24,mix='1 atm',size=17,anchor='middle',fill=MUTED))
    ya=ax.Y(0); s.append(an('draw',L(ax.X(-20),ya,ax.X(120),ya,PLUS,4),dur='1.2',delay='.2')+A(ax.X(112),ya,ax.X(124),ya,'plus',4))
    s.append(T(ax.X(-20),ya+28,mix='ⓐ',size=20,fill=PLUS,weight=700))
    yb=ax.Y(-3); s.append(an('draw',L(ax.X(-40),yb,ax.X(40),yb,MINUS,4),dur='1.0',delay='.6')+A(ax.X(32),yb,ax.X(44),yb,'minus',4))
    s.append(T(ax.X(-46),yb+6,mix='ⓑ',size=20,fill=MINUS,weight=700,anchor='end'))
    s.append(T(ax.X(44)+6,yb+6,mix='0.001 atm',size=17,anchor='start',fill=MUTED))
    xc=ax.X(-5); s.append(an('draw',L(xc,ax.Y(0),xc,ax.Y(2.85),FIELD,4),dur='1.0',delay='1.0')+A(xc,ax.Y(2.7),xc,ax.Y(2.95),'field',4))
    s.append(T(xc-8,ax.Y(0.6),mix='ⓒ',size=20,fill=FIELD,weight=700,anchor='end'))
    s.append(step('p1',C(ax.X(0),ya,7,INK,2,HL)+C(ax.X(100),ya,7,INK,2,HL)+T(ax.X(0)+4,ya-12,mix='융해',size=18,anchor='start',halo=True,weight=700)+T(ax.X(100),ya-12,mix='기화',size=18,halo=True,weight=700)))
    tb=-20.0
    s.append(step('p2',C(ax.X(tb),yb,7,INK,2,HL)+T(ax.X(tb),yb-14,mix='승화',size=18,halo=True,weight=700)))
    s.append(step('p3',C(xc,ax.Y(lg(600)),7,INK,2,HL)+T(xc-10,ax.Y(lg(600))+6,mix='약 600 atm',size=18,anchor='end',halo=True,weight=700)))
    return svg((560,420),560,'물의 상평형 그림 위 세 경로: 1 atm 가열, 0.001 atm 가열, −5 °C 가압',s)
FIG['WATER']=water_fig()
FIG['PATHS']=water_fig(True)

# ═════ 12 그림 Ⅳ-10 CO2 ═════
def co2_fig():
    s=[]; ax=Ax(80,350,460,310,60,3,xmin=-100,ymin=-1)
    sub,vap,melt=co2_curves()
    s.append(phase(ax,sub,vap,melt,-1,3))
    s.append(logframe(ax,[-100,-80,-60,-40,-20,0,20,40,60],range(-1,4),T(ax.x0+ax.w+6,ax.y0+48,mix='온도 [°C]',size=19,anchor='end',fill=MUTED),
                      T(ax.x0-10,ax.y0-ax.h-20,mix='압력 [atm] (로그 눈금)',size=19,anchor='start',fill=MUTED),size=17))
    s.append(L(ax.x0,ax.Y(0),ax.x0+ax.w,ax.Y(0),MUTED,1.5,'6 4')+T(ax.x0+ax.w-4,ax.Y(0)-8,mix='1 atm',size=17,anchor='end',fill=MUTED))
    tp=(ax.X(-56.6),ax.Y(lg(5.11))); cp=(ax.X(30.98),ax.Y(lg(72.8)))
    s.append(an('pop',C(*tp,8,INK,2,EQUI),o=f'{f(tp[0])},{f(tp[1])}',delay='1.9')+an('pop',C(*cp,8,INK,2,PLUS),o=f'{f(cp[0])},{f(cp[1])}',delay='2.1'))
    s.append(T(tp[0]+12,tp[1]+26,mix='삼중점 (−56.6 °C, 5.1 atm)',size=18,anchor='start',halo=True,weight=700))
    s.append(T(cp[0]+4,cp[1]-18,mix='임계점 (31 °C, 72.8 atm)',size=18,anchor='middle',halo=True,weight=700))
    sp=(ax.X(-78.5),ax.Y(0))
    s.append(step('c1',C(*sp,7,INK,2,HL)+T(sp[0]-10,sp[1]+28,mix='−78 °C 승화',size=18,anchor='middle',halo=True,weight=700)))
    s.append(T(ax.X(-85),ax.Y(1.8),mix='고체',size=21,weight=700)+T(ax.X(-12),ax.Y(1.75),mix='액체',size=21,weight=700)+T(ax.X(10),ax.Y(-0.5),mix='기체',size=21,weight=700))
    return svg((560,420),580,'이산화 탄소의 상평형 그림: 삼중점 압력이 1 atm보다 커서 1 atm에서는 승화한다',s)
FIG['CO2']=co2_fig()

# ═════ 15 그림 Ⅳ-11 CsCl 용해 ═════
def cscl():
    s=[R(0,0,540,420,'none',0,WATER,14)]
    # 결정 덩어리
    for i in range(4):
        for j in range(6):
            sg=1 if (i+j)%2==0 else -1
            if (i,j) in ((3,1),(3,2)): continue
            s.append(ion(30+i*40,50+j*40,18,sg))
    s.append(T(90,320+40,mix='$\\ce{CsCl}$ 결정',size=19,weight=700))
    # 떨어져 나오는 이온 (원래 자리 (3,1)·(3,2) → 물 쪽)
    def hyd(cx,cy,sg,dfrom,dl):
        o=''
        n=6; R_=44 if sg>0 else 46
        for k in range(n):
            a=2*math.pi*k/n+0.3
            wx,wy=cx+R_*math.cos(a),cy+R_*math.sin(a)
            if sg>0: o+=water(wx,wy,math.degrees(a))          # O가 양이온 쪽 (H는 바깥)
            else:
                # H 하나가 음이온을 향함: 이등분선이 안쪽에서 52° 돌아간 방향
                o+=water(wx,wy,math.degrees(a)+180-52.25)
        o+=ion(cx,cy,18,sg,'\\ce{Cs+}' if sg>0 else '\\ce{Cl-}',17)
        return mv(o,dfrom,dur='1.6',delay=dl,ease='out')
    s.append(hyd(300,110,1,'-150,4','.2'))
    s.append(hyd(400,250,-1,'-250,-130','.8'))
    s.append(T(300,186,mix='양이온',size=19,weight=700,fill=PLUS)+T(400,326,mix='음이온',size=19,weight=700,fill=MINUS))
    # δ 라벨 예시
    s.append(T(470,60,mix='$\\delta^-$: O',size=18,anchor='middle',fill=MINUS)+T(470,84,mix='$\\delta^+$: H',size=18,anchor='middle',fill=PLUS))
    s.append(atom(250,380,12,'O')+atom(250+13*math.cos(math.radians(-52)),380+13*math.sin(math.radians(-52)),8,'H')+atom(250+13*math.cos(math.radians(52)),380+13*math.sin(math.radians(52)),8,'H'))
    s.append(T(272,388,mix='물 분자 (O 빨강, H 흰색)',size=17,anchor='start',fill=MUTED))
    return svg((540,420),540,'염화 세슘 결정에서 떨어져 나온 양이온과 음이온을 물 분자가 둘러싸 수화한다',s)
FIG['CSCL']=cscl()

# ═════ 16 AgCl 포화 용액 ═════
def kspfig():
    s=[]; bx,by,bw,bh=40,30,300,300
    s.append(R(bx,by+40,bw,bh-40,'none',0,WATER))
    s.append(P([(bx,by),(bx,by+bh),(bx+bw,by+bh),(bx+bw,by)],GLASS,3))
    for i in range(12):
        x=bx+18+i*23; y=by+bh-14-(i%3)*9
        s.append(R(x-9,y-9,18,18,INK,1.5,AGCL,3))
    rnd=random.Random(2)
    pts=[(90,110,1),(150,150,-1),(220,100,1),(280,160,-1),(110,200,-1),(250,215,1),(190,240,1),(300,110,-1)]
    for i,(x,y,sg) in enumerate(pts):
        s.append(mv(ion(x,y,15,sg),f'{rnd.choice((-5,5))},{rnd.choice((-4,4))}',rep='alt',dur=f(.9+.12*i),ease='io'))
    s.append(A(bx+bw+28,by+bh-30,bx+bw+28,by+120,'field',3.5)+A(bx+bw+52,by+120,bx+bw+52,by+bh-30,'bfield',3.5))
    s.append(T(bx+bw+40,by+108,tex='\\ce{&lt;=&gt;}',size=20))
    s.append(T(bx+bw+22,by+bh+2,mix='용해',size=18,fill=FIELD,weight=700,anchor='end')+T(bx+bw+58,by+bh+2,mix='석출',size=18,fill=BF,weight=700,anchor='start'))
    s.append(ion(70,372,15,1)+T(92,379,tex='\\ce{Ag+}',size=19,anchor='start')+ion(170,372,15,-1)+T(192,379,tex='\\ce{Cl-}',size=19,anchor='start'))
    s.append(R(250,362,20,20,INK,1.5,AGCL,3)+T(278,379,mix='고체 $\\ce{AgCl}$',size=19,anchor='start'))
    return svg((440,400),420,'고체 염화 은이 남아 있는 포화 용액에서 용해와 석출이 같은 속도로 일어난다',s)
FIG['KSPFIG']=kspfig()

# ═════ 19 Ksp와 s 비교 (로그 막대) ═════
def compare():
    s=[]
    def panel(x0,title,vals,ymin,ymax,yt,delay):
        ax=Ax(x0,310,190,240,1,ymax,ymin=ymin)
        o=[L(ax.x0,ax.y0,ax.x0+ax.w,ax.y0,MUTED,2),L(ax.x0,ax.y0,ax.x0,ax.y0-ax.h-6,MUTED,2)]
        for v in yt: o.append(L(ax.x0-6,ax.Y(v),ax.x0,ax.Y(v),MUTED,1.5)+T(ax.x0-10,ax.Y(v)+6,tex='10^{%d}'%v,size=17,anchor='end'))
        o.append(T(ax.x0+ax.w/2,30,mix=title,size=19,weight=700))
        for i,(lab,v,col) in enumerate(vals):
            x=ax.x0+20+i*95; y=ax.Y(lg(v))
            o.append(an('scale',R(x,y,50,ax.y0-y,INK,1.5,col),**{'from':'1,0','o':f'{x+25},{ax.y0}','dur':'.9','delay':f(delay+0.2*i)}))
            o.append(T(x+25,ax.y0+26+(24 if i else 0),tex=lab,size=18))
        return ''.join(o)
    s.append(panel(70,'$K_\\mathrm{sp}$',[('\\ce{AgCl}',1.6e-10,AGCL),('\\ce{Ag2CrO4}',2.7e-12,AGCRO)],-13,-9,[-13,-12,-11,-10,-9],0.1))
    s.append(panel(320,'몰 용해도 $s$ [M]',[('\\ce{AgCl}',1.26e-5,AGCL),('\\ce{Ag2CrO4}',8.8e-5,AGCRO)],-6,-3.5,[-6,-5,-4],0.7))
    s.append(T(165,392,mix='$\\ce{AgCl}$이 크다',size=18,fill=MUTED)+T(415,392,mix='$\\ce{Ag2CrO4}$가 크다',size=18,fill=MUTED))
    s.append(step('cm',R(300,404,236,34,EQUI,2,'#FFF8EF',8)+T(418,428,mix='약 7배 더 잘 녹는다',size=18,fill=EQUI,weight=700)))
    return svg((540,446),520,'Ksp는 염화 은이 크지만 몰 용해도는 크로뮴산 은이 더 크다(로그 눈금 막대)',s)
FIG['COMPARE']=compare()

# ═════ 20 이온곱과 침전 (로그 수직선) ═════
def precip():
    s=[]; y=110; x0,x1=40,440; lo,hi=-12,-8
    X=lambda v:x0+(v-lo)/(hi-lo)*(x1-x0)
    s.append(R(X(lg(1.6e-10)),y-50,x1-X(lg(1.6e-10)),100,'none',0,'#FDE7EA')+R(x0,y-50,X(lg(1.6e-10))-x0,100,'none',0,'#EAF2FC'))
    s.append(L(x0,y,x1+10,y,INK,3)+P([(x1,y-8),(x1+14,y),(x1,y+8)],INK,3))
    for v in range(lo,hi+1): s.append(L(X(v),y-6,X(v),y+6,INK,2)+T(X(v),y+32,tex='10^{%d}'%v,size=17))
    kx=X(lg(1.6e-10)); s.append(L(kx,y-56,kx,y+50,EQUI,4)+T(kx,y-64,mix='$K_\\mathrm{sp}=1.6\\times10^{-10}$',size=18,weight=700,fill=EQUI))
    s.append(T((x0+kx)/2,y-28,mix='불포화',size=18,fill=MINUS,weight=700)+T((kx+x1)/2,y-28,mix='과포화 → 침전',size=18,fill=PLUS,weight=700))
    s.append(T(x1+16,y-12,mix='$Q$',size=19,anchor='start'))
    def beaker(cx,ppt):
        o=R(cx-50,190,100,30,'none',0,WATER)+R(cx-50,222,100,58,'none',0,WATER)
        o+=P([(cx-50,175),(cx-50,280),(cx+50,280),(cx+50,175)],GLASS,3)
        if ppt:
            for i in range(9): o+=C(cx-38+i*9.5,272-(i%2)*4,4.5,MUTED,1,AGCL)
            for i in range(10): o+=C(cx-40+(i*23)%80,200+(i*17)%60,3,MUTED,1,AGCL)
        return o
    x1p=X(lg(2.5e-9)); x2p=X(lg(2.5e-11))
    s.append(step('c1',C(x1p,y,9,INK,2,PLUS)+T(x1p,y+60,mix='$2.5\\times10^{-9}$',size=18,weight=700)+beaker(330,True)+T(330,306,mix='흰색 $\\ce{AgCl}$ 침전',size=18)))
    s.append(step('c2',C(x2p,y,9,INK,2,'#FFFFFF')+T(x2p,y+60,mix='$2.5\\times10^{-11}$',size=18,weight=700)+beaker(130,False)+T(130,306,mix='맑다',size=18)))
    return svg((480,320),470,'이온곱 Q가 Ksp보다 크면 침전이 생기고 작으면 생기지 않는다',s)
FIG['PRECIP']=precip()

# ═════ 22 공통 이온 효과 ═════
def common():
    s=[]; ax=Ax(90,330,300,270,1,-4,ymin=-10)
    s.append(L(ax.x0,ax.y0,ax.x0+ax.w,ax.y0,MUTED,2)+L(ax.x0,ax.y0,ax.x0,ax.y0-ax.h-6,MUTED,2))
    for v in range(-10,-3): s.append(L(ax.x0-6,ax.Y(v),ax.x0,ax.Y(v),MUTED,1.5)+T(ax.x0-10,ax.Y(v)+6,tex='10^{%d}'%v,size=17,anchor='end'))
    s.append(T(ax.x0-6,ax.y0-ax.h-18,mix='$\\ce{AgCl}$의 몰 용해도 [M]',size=18,anchor='start',fill=MUTED))
    for i,(lab,v,dl) in enumerate((('순수한 물',1.26e-5,'.1'),('0.10 M $\\ce{NaCl}$',1.6e-9,'.6'))):
        x=ax.x0+50+i*130; yv=ax.Y(lg(v))
        s.append(an('scale',R(x,yv,80,ax.y0-yv,INK,1.5,AN_F if i else '#FFFFFF'),**{'from':'1,0','o':f'{x+40},{ax.y0}','dur':'.9','delay':dl}))
        s.append(T(x+40,ax.y0+26,mix=lab,size=18)+T(x+40,yv-10,mix=('$1.26\\times10^{-5}$' if i==0 else '$1.6\\times10^{-9}$'),size=18,weight=700))
    s.append(step('ci',A(ax.x0+175,ax.Y(-5.2),ax.x0+222,ax.Y(-8.4),'bfield',3)+T(ax.x0+250,ax.Y(-6.6),mix='약 8000배 ↓',size=19,anchor='start',fill=BF,weight=700)))
    return svg((460,380),440,'염화 나트륨 용액에서 염화 은의 몰 용해도가 순수한 물보다 약 8000배 작다',s)
FIG['COMMON']=common()

# ═════ 24 그림 Ⅳ-12 기체 용해도–온도 ═════
def gast():
    s=[]; ax=Ax(80,330,400,280,30,2.5)
    s.append(ax.frame([0,10,20,30],[0,0.5,1.0,1.5,2.0,2.5],T(490,380,mix='온도 [°C]',size=19,anchor='end',fill=MUTED),
                      T(74,36,mix='용해도 [$10^{-3}$ mol/L] (1 atm)',size=19,anchor='start',fill=MUTED),yfmt=lambda v:'%.1f'%v,size=18))
    sty={'CH4':('8 5',2.8),'O2':(None,4),'CO':('12 6',2.8),'N2':('4 4',2.8),'He':(None,2.5)}
    for i,g in enumerate(('CH4','O2','CO','N2','He')):
        d,w=sty[g]
        s.append(an('draw',ax.curve(lambda t:kh(g,t)*1e3,0,30,col=INK,w=w,dash=d),dur='1.2',delay=f(0.15*i)))
    lab={'CH4':('\\text{메테인}',0.5,8,-12,'start'),'O2':('\\text{산소}',3,None,28,'start'),'CO':('\\text{일산화 탄소}',29.5,None,-12,'end'),'N2':('\\text{질소}',29.5,None,-12,'end'),'He':('\\text{헬륨}',29.5,None,-12,'end')}
    for g,(t,x,_,dy,anc) in lab.items():
        s.append(T(ax.X(x),ax.Y(kh(g,x)*1e3)+dy,tex=t,size=18,anchor=anc,halo=True))
    s.append(T(ax.X(1),ax.Y(0.2),mix='계산값: 25 °C 헨리 상수와 온도 의존성',size=17,anchor='start',fill=MUTED))
    return svg((500,392),520,'메테인, 산소, 일산화 탄소, 질소, 헬륨 모두 온도가 높을수록 물에 덜 녹는다',s)
FIG['GAST']=gast()

# ═════ 25 그림 Ⅳ-13 고체 용해도–온도 ═════
def solt():
    s=[]
    a1=Ax(70,330,300,280,100,1000)
    s.append(a1.frame([0,20,40,60,80,100],[0,200,400,600,800,1000],T(370,380,mix='온도 [°C]',size=18,anchor='end',fill=MUTED),
                      T(10,30,mix='용해도 [g/100 g 물]',size=18,anchor='start',fill=MUTED),size=16))
    for i,(k,lab,x,dy) in enumerate((('AgNO3','\\ce{AgNO3}',78,-6),('KNO3','\\ce{KNO3}',92,30),('KI','\\ce{KI}',55,-14))):
        pts=smooth(SOL[k]); s.append(an('draw',P([(a1.X(t),a1.Y(v)) for t,v in pts],INK,3.2),dur='1.2',delay=f(0.2*i)))
        yv=[v for t,v in pts if t>=x][0]
        s.append(T(a1.X(x)-6,a1.Y(yv)+dy,tex=lab,size=18,anchor='end',halo=True))
    s.append(R(a1.x0,a1.Y(50),a1.w,a1.y0-a1.Y(50),EQUI,2,'none',4,'5 4'))
    a2=Ax(440,330,180,280,100,50)
    s.append(a2.frame([0,50,100],[0,10,20,30,40,50],T(630,380,mix='온도 [°C]',size=18,anchor='end',fill=MUTED),T(636,24,mix='(아래 확대)',size=18,anchor='end',fill=EQUI),size=16))
    s.append(R(a2.x0-4,a2.y0-a2.h-4,a2.w+12,a2.h+8,EQUI,2,'none',6,'5 4'))
    for i,(k,dash) in enumerate((('NaCl',None),('Li2CO3',None),('Na2SO4.10H2O',None),('Na2SO4','9 5'))):
        pts=smooth(SOL[k]); s.append(an('draw',P([(a2.X(t),a2.Y(v)) for t,v in pts],INK,3,dash=dash),dur='1.0',delay=f(0.6+0.2*i)))
    s.append(T(a2.X(98),a2.Y(39.2)+26,tex='\\ce{NaCl}',size=17,anchor='end',halo=True))
    s.append(T(a2.X(98),a2.Y(0.7)-10,tex='\\ce{Li2CO3}',size=17,anchor='end',halo=True))
    s.append(T(a2.X(18),a2.Y(17),tex='\\ce{Na2SO4.10H2O}',size=16,anchor='start',halo=True))
    s.append(T(a2.X(98),a2.Y(42.5)-12,tex='\\ce{Na2SO4}',size=17,anchor='end',halo=True))
    pt=(a2.X(32.4),a2.Y(49.7)); s.append(an('pop',C(*pt,6,INK,1.5,EQUI),o=f'{f(pt[0])},{f(pt[1])}',delay='1.8'))
    s.append(T(pt[0],pt[1]-12,mix='32 °C',size=17,fill=EQUI,weight=700,halo=True))
    s.append(T(345,414,mix='문헌값을 이은 곡선',size=16,fill=MUTED))
    return svg((640,420),640,'질산 은, 질산 칼륨, 아이오딘화 칼륨은 온도가 높을수록 잘 녹고, 탄산 리튬은 덜 녹으며, 황산 나트륨 십수화물은 32도에서 꺾인다',s)
FIG['SOLT']=solt()

# ═════ 26 헨리 법칙 입자 그림과 그림 Ⅳ-14 ═════
def henrybox():
    s=[]
    for k,(x0,ng,nd,lab) in enumerate(((10,6,3,'(가) 부분 압력 $P$'),(240,12,6,'(나) 부분 압력 $2P$'))):
        w,h=210,240
        s.append(R(x0,10,w,h,GLASS,3,'#FFFFFF',8)+R(x0+3,140,w-6,107,'none',0,WATER,4))
        rnd=random.Random(20+k); pts=[]
        while len(pts)<ng:
            p=(rnd.uniform(x0+22,x0+w-22),rnd.uniform(32,118))
            if all(math.hypot(p[0]-a,p[1]-b)>27 for a,b in pts): pts.append(p)
        for i,(x,y) in enumerate(pts): s.append(mv(gm(x,y,9),f'{rnd.choice((-5,5))},{rnd.choice((-4,4))}',rep='alt',dur=f(.7+.06*i),ease='io'))
        dp=[]
        while len(dp)<nd:
            p=(rnd.uniform(x0+22,x0+w-22),rnd.uniform(160,232))
            if all(math.hypot(p[0]-a,p[1]-b)>27 for a,b in dp): dp.append(p)
        for x,y in dp: s.append(gm(x,y,9))
        s.append(T(x0+w/2,276,mix=lab,size=19,weight=700))
        s.append(T(x0+w/2,300,mix=f'녹은 분자 {nd}개',size=18,fill=MUTED))
    return svg((460,310),450,'기체의 부분 압력이 2배이면 녹은 기체 분자도 2배이다',s)
FIG['HENRYBOX']=henrybox()
def henry():
    s=[]; ax=Ax(90,250,330,210,1,1.5)
    s.append(ax.frame([0,0.5,1],[0,0.5,1.0,1.5],T(440,296,mix='부분 압력 [atm]',size=18,anchor='end',fill=MUTED),
                      T(10,26,mix='몰 용해도 [$10^{-3}$ mol/L]',size=18,anchor='start',fill=MUTED),yfmt=lambda v:'%.1f'%v,size=17))
    for i,(g,lab) in enumerate((('O2','산소'),('N2','질소'),('He','헬륨'))):
        k=KH[g]*1e3
        s.append(an('draw',L(ax.X(0),ax.Y(0),ax.X(1),ax.Y(k),INK,3.5,None if g!='N2' else '10 6'),dur='1.0',delay=f(0.25*i)))
        s.append(T(ax.X(1)+8,ax.Y(k)+6,mix=lab,size=18,anchor='start'))
    return svg((480,300),480,'산소, 질소, 헬륨의 몰 용해도는 부분 압력에 정비례한다',s)
FIG['HENRY']=henry()

# ═════ 29 잠수 깊이와 질소 용해도 ═════
def dive():
    s=[]; top,bot=40,340
    s.append(R(10,top-6,150,bot-top+20,'none',0,'#CFE3F2',8)+L(10,top-6,160,top-6,MINUS,3))
    Y=lambda d:top+d/30*(bot-top)
    for d in (0,10,20,30):
        s.append(L(10,Y(d),24,Y(d),INK,2)+T(30,Y(d)+6,mix=f'{d} m',size=18,anchor='start'))
        s.append(T(150,Y(d)+6,mix=f'{d//10+1} atm',size=18,anchor='end',weight=700))
    s.append(T(85,top-18,mix='수심 · 압력',size=18,fill=MUTED))
    # 막대: s_N2
    ax=Ax(200,0,280,0,2.2,1)
    s.append(L(200,top-14,200,bot+14,MUTED,2))
    for i,d in enumerate((0,10,20,30)):
        v=6.1e-4*0.78*(d/10+1)*1e3; y=Y(d)
        s.append(an('scale',R(200,y-14,ax.X(v)-200,28,INK,1.5,GAS),**{'from':'0,1','o':f'200,{f(y)}','dur':'.8','delay':f(0.2*i)}))
        s.append(T(ax.X(v)+8,y+7,mix='%.2f'%v,size=18,anchor='start'))
    s.append(T(340,top-18,mix='녹는 $\\ce{N2}$ [$10^{-3}$ M]',size=18,fill=MUTED))
    # 상승 화살표와 기포
    s.append(A(470,bot-10,470,top+60,'ink',3)+T(470,top+40,mix='천천히',size=18,weight=700))
    for i,(x,y,r) in enumerate(((450,200,5),(492,160,4),(455,120,6))):
        s.append(mv(C(x,y,r,WATER_S,2,'#FFFFFF'),'0,40',rep='loop',dur='2',delay=f(0.5*i),ease='lin'))
    s.append(T(250,bot+50,mix='계산값: $s=k_\\mathrm{H}P_{\\ce{N2}}$, $P_{\\ce{N2}}=0.78P$',size=17,fill=MUTED))
    return svg((520,400),500,'수심 30 m까지 내려가면 압력이 4 atm이 되어 녹는 질소도 4배가 된다',s)
FIG['DIVE']=dive()

# ═════ 34 연습 문제 3: 분자 수 (원자 보존) ═════
def ex3():
    s=[]; rN=10; rO=10; rH=7
    def nh3(x,y):
        return atom(x,y-rN*.95,rH,'H')+atom(x,y,rN,'N')+atom(x-rN*.85,y+rN*.6,rH,'H')+atom(x+rN*.85,y+rN*.6,rH,'H')
    def di(x,y,el,r): return atom(x-r*.62,y,r,el)+atom(x+r*.62,y,r,el)
    def h2o(x,y): return atom(x-rO*.85,y+rO*.55,rH,'H')+atom(x+rO*.85,y+rO*.55,rH,'H')+atom(x,y,rO,'O')
    s.append(R(10,10,170,170,INK,2,'#FFFFFF',10)+R(240,10,170,170,INK,2,'#FFFFFF',10))
    for i,(x,y) in enumerate(((50,50),(130,46),(54,130),(138,128))): s.append(mv(nh3(x,y),'3,-2',rep='alt',dur=f(.9+.1*i),ease='io'))
    for i,(x,y) in enumerate(((95,88),(96,152),(150,90))): s.append(mv(di(x,y,'O',rO),'-3,2',rep='alt',dur=f(1.0+.1*i),ease='io'))
    for i,(x,y) in enumerate(((290,45),(370,150))): s.append(mv(di(x,y,'N',rN),'3,2',rep='alt',dur=f(1.0+.1*i),ease='io'))
    for i,(x,y) in enumerate(((345,45),(275,100),(330,100),(385,95),(280,152),(325,150))): s.append(mv(h2o(x,y),'-2,3',rep='alt',dur=f(.9+.08*i),ease='io'))
    s.append(T(210,100,tex='\\ce{&lt;=&gt;}',size=22))
    s.append(T(95,210,mix='기체 분자 7개',size=19,weight=700)+T(325,210,mix='기체 분자 8개',size=19,weight=700))
    s.append(atom(40,245,rN,'N')+T(56,252,mix='N',size=18,anchor='start')+atom(110,245,rO,'O')+T(126,252,mix='O',size=18,anchor='start')+atom(180,245,rH,'H')+T(194,252,mix='H',size=18,anchor='start'))
    s.append(T(320,252,mix='원자 수 보존',size=18,anchor='middle',fill=MUTED)+T(320,278,mix='N 4 · H 12 · O 6',size=18,anchor='middle',fill=MUTED))
    return svg((420,290),420,'암모니아 4분자와 산소 3분자가 질소 2분자와 물 6분자로: 기체 분자 수가 7에서 8로 는다',s)
FIG['EX3']=ex3()

# ═════ 출력 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(out)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "상평형과 용해도 평형", "file": "4-1-2_상평형과_용해도_평형", "header": "Ⅳ-1-2 상평형과 용해도 평형 (고등 고급 화학 200–208쪽)"}\n')
print('ok',len(out),'sections',out.count('<section'),'anim',out.count('data-anim'))
