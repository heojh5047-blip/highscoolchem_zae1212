# -*- coding: utf-8 -*-
"""고급화학 3-2-2 깁스 자유 에너지와 반응의 자발성 — 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   labs_src.js·extra_src.css를 labs.js·extra.css로 복사하고 meta.json을 쓴다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)
   ΔG–T 그래프는 모두 ΔG° = ΔH° − TΔS° 계산값으로 그린다."""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FOLDER='3-2-2_깁스_자유_에너지와_반응의_자발성'
OUT=BASE+FOLDER+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-2-2_깁스_자유_에너지와_반응의_자발성/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FOLDER), OUT
FIG={}
SYSBG='#FFF4E8'; HOT='#FDE2E4'; COLD='#E3EEFB'; ICE='#D6ECFA'; ICE_S='#7FB3D5'; CU='#C77B4A'; CU_S='#8A4B26'
DASH={'가':None,'나':'12 7','다':'3 6','라':'14 6 3 6'}
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def step(g,body): return f'<g class="step" data-g="{g}">{body}</g>'
def heat(x1,y1,x2,y2,w=3): return A(x1,y1,x2,y2,'equi',w)
def barrow(x,y0,dy,w,col,extra=''):
    hd=min(abs(dy)*.45,w*1.1); sg=-1 if dy<0 else 1; y1=y0+dy; yb=y1-sg*hd
    pts=[(x-w/2,y0),(x-w/2,yb),(x-w*.95,yb),(x,y1),(x+w*.95,yb),(x+w/2,yb),(x+w/2,y0)]
    return P(pts,col,2,fill=col,extra='fill-opacity=".35" '+extra,close=True)
def beaker(x,y,w,h,lvl,fill=WATER):
    return (R(x+2,y+h-lvl,w-4,lvl-2,'none',0,fill)+L(x+2,y+h-lvl,x+w-2,y+h-lvl,WATER_S,1.5)
            +P([(x,y),(x,y+h),(x+w,y+h),(x+w,y)],GLASS,3))

def gline(ax,H,S,t0,t1,col=INK,w=3.5,dash=None,anim=True,dur='1.1'):
    """ΔG°(T) = H − T·S/1000 (H kJ, S J/K) 직선. 축 범위 밖은 잘라 그림"""
    pts=[]
    for i in range(201):
        T_=t0+(t1-t0)*i/200; v=H-T_*S/1000
        if ax.ymin-1e-9<=v<=ax.ymax+1e-9: pts.append((ax.X(T_),ax.Y(v)))
    p=P(pts,col,w,dash=dash,extra='stroke-linecap="round"')
    return an('draw',p,dur=dur) if anim else p
def zero(ax): return L(ax.x0,ax.Y(0),ax.x0+ax.w,ax.Y(0),MUTED,2,'7 5')
def shade(ax,H,S,t0,t1,lab=True,size=18,ly=None):
    """ΔG° < 0인 온도 구간: 0선 아래 띠(field .15) + 「자발적」"""
    xs=[t0+(t1-t0)*i/400 for i in range(401)]; neg=[T_ for T_ in xs if H-T_*S/1000<0]
    if not neg: return ''
    a,b=min(neg),max(neg); y0=ax.Y(0); y1=ax.Y(ax.ymin)
    o=R(ax.X(a),y0,ax.X(b)-ax.X(a),y1-y0,'none',0,FIELD,extra='fill-opacity=".15"')
    if lab: o+=T((ax.X(a)+ax.X(b))/2,ly if ly else y1-12,mix='자발적',size=size,fill=FIELD,weight=700,halo=True)
    return o

# ═════ 1 표지: 석회석 분해의 ΔG°–T ═════
def cover():
    ax=Ax(70,330,300,260,1500,200,xmin=0,ymin=-80)
    s=[ax.frame([0,500,1000,1500],[-50,0,50,100,150,200],T(384,382,mix='$T$ [K]',size=19,anchor='end',fill=MUTED),
                T(64,52,mix='$\\Delta G^\\circ$ [kJ]',size=19,anchor='start',fill=MUTED),size=18)]
    s.append(zero(ax)+shade(ax,178.3,160.6,0,1500,ly=ax.Y(-62)))
    s.append(gline(ax,178.3,160.6,0,1500,dur='1.6'))
    tx=178300/160.6
    s.append(L(ax.X(tx),ax.Y(0),ax.X(tx),ax.Y(-80),MUTED,1.5,'4 4'))
    s.append(an('pop',C(ax.X(tx),ax.Y(0),7,INK,2,'#FFFFFF'),delay='1.4',o=f'{f(ax.X(tx))},{f(ax.Y(0))}'))
    s.append(T(ax.X(tx)-8,ax.Y(0)-14,mix='$1110\\ \\text{K}$',size=19,anchor='end',halo=True))
    s.append(T(ax.X(120),ax.Y(176),mix='$\\ce{CaCO3 -> CaO + CO2}$',size=19,anchor='start',halo=True))
    s.append(T(ax.X(120),ax.Y(150),mix='$\\Delta G^\\circ=\\Delta H^\\circ-T\\Delta S^\\circ$',size=19,anchor='start',halo=True))
    return svg((460,400),440,'석회석 분해 반응의 ΔG°는 온도가 높을수록 작아져 1110 K보다 높은 온도에서 음수가 되어 자발적이다',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 3 화학사: 연표 ═════
def hist():
    s=[]; y=150
    s.append(A(20,y,460,y,'ink',3))
    ev=[(70,'카르노','칼로릭은||보존된다',GRAV),(170,'줄','열과 일의 총량||보존',GRAV),(285,'1850','클라우지우스||첫 논문',INK),(400,'1865','엔트로피||$S$ 정의',FIELD)]
    for i,(x,top,bot,col) in enumerate(ev):
        body=C(x,y,9,col,2.5,'#FFFFFF')+T(x,y-26,mix=top,size=20,weight=700,fill=col)+T(x,y+40,mix=bot,size=19)
        s.append(an('fade',body,delay=f(i*.35),dur='.6'))
    s.append(R(250,240,200,64,FIELD,2,'#F2FAF5',10)+T(350,268,tex='\\Delta S=\\dfrac{q_\\text{가역}}{T}',size=21))
    s.append(L(400,206,380,240,MUTED,1.5))
    s.append(T(30,48,mix='모순: 칼로릭 보존 ↔ 에너지 보존',size=19,anchor='start',fill=MUTED))
    s.append(T(30,80,mix='→ 열은 높은 온도에서 낮은 온도로',size=19,anchor='start',fill=MUTED))
    return svg((480,320),450,'카르노의 칼로릭 보존과 줄의 에너지 보존 사이의 모순을 클라우지우스가 1850년에 해결하고 1865년에 엔트로피를 정의하였다',s)
FIG['HIST']=hist()

# ═════ 4 생각 열기: 계와 주위 ═════
def opening():
    s=[R(10,20,460,320,MUTED,1.5,'#F3F6F9',14)]
    s.append(T(30,52,mix='주위 (매우 큼)',size=20,anchor='start',fill=MUTED,weight=700))
    s.append(R(150,110,180,130,INK,3,SYSBG,10)+T(240,150,mix='계 (반응)',size=21,weight=700))
    s.append(T(240,188,tex='\\Delta H,\\ \\Delta S',size=21)+T(240,222,tex='T',size=21))
    for (x1,y1,x2,y2) in [(146,175,70,175),(334,175,410,175)]:
        s.append(an('draw',heat(x1,y1,x2,y2),dur='.8'))
    s.append(an('fade',T(410,290,mix='$\\Delta S_\\text{주위}=\\ ?$',size=21,anchor='end',fill=RD,weight=700),delay='.6',rep='alt',dur='1.2'))
    s.append(T(70,290,mix='계만 보고 알 수 없을까?',size=19,anchor='start',fill=INK))
    return svg((480,350),440,'반응이 일어나는 계와 매우 큰 주위: 주위의 엔트로피 변화까지 매번 구해야 할까',s)
FIG['OPEN']=opening()

# ═════ 5 ① 블록 화살표: ΔS전체 = ΔS + ΔS주위 ═════
def blocks():
    s=[]; base=250
    s.append(L(20,base,460,base,MUTED,1.5,'5 4'))
    s.append(an('draw',barrow(90,base,-90,40,BF),dur='.6'))
    s.append(an('draw',barrow(220,base,-140,40,RD),dur='.6',delay='.3'))
    s.append(an('draw',barrow(370,base,-210,46,FIELD),dur='.7',delay='.7'))
    s.append(T(155,base-60,mix='+',size=34,weight=700)+T(295,base-60,mix='=',size=34,weight=700))
    s.append(T(90,base+36,tex='\\Delta S',size=21,fill=BF)+T(90,base+66,mix='계',size=19,fill=BF))
    s.append(T(220,base+36,tex='\\Delta S_\\text{주위}',size=21,fill=RD)+T(220,base+66,tex='=-\\Delta H/T',size=19,fill=RD))
    s.append(T(370,base+36,tex='\\Delta S_\\text{전체}',size=21,fill=FIELD)+T(370,base+66,mix='전체',size=19,fill=FIELD))
    return svg((480,330),430,'계의 엔트로피 변화와 주위의 엔트로피 변화(−ΔH/T)를 더하면 전체 엔트로피 변화가 된다',s)
FIG['BLOCK']=blocks()

# ═════ 6 ② 계의 성질만으로 ═════
def sysonly():
    s=[R(10,20,460,300,MUTED,1.5,'#F3F6F9',14,dash='8 6')]
    s.append(an('fade',T(440,52,mix='주위는 따로 계산하지 않는다',size=19,anchor='end',fill=MUTED),dur='.8'))
    s.append(R(40,90,190,170,INK,3,SYSBG,10)+T(135,124,mix='계의 성질',size=20,weight=700))
    s.append(T(135,164,tex='H,\\ S,\\ T',size=22)+T(135,206,tex='G\\equiv H-TS',size=22,fill=FIELD))
    s.append(A(240,175,300,175,'ink',4))
    s.append(R(306,120,150,110,FIELD,2.5,'#F2FAF5',10)+T(381,166,tex='\\Delta G',size=24,weight=700)+T(381,204,mix='자발성 판단',size=19))
    s.append(T(240,296,mix='일정한 온도와 압력',size=19,fill=MUTED))
    return svg((480,330),430,'계의 성질 H, S, T로 깁스 자유 에너지 G를 정의하면 ΔG만으로 자발성을 판단할 수 있다',s)
FIG['SYS']=sysonly()

# ═════ 7 ③ 거울 눈금: ΔS전체 ↔ ΔG ═════
def mirror():
    s=[]; xL,xR,y0=175,365,170; sc=1.1
    for x,lab,col in ((xL,'\\Delta S_\\text{전체}',FIELD),(xR,'\\Delta G',INK)):
        s.append(L(x,40,x,300,MUTED,2)+T(x,30,tex=lab,size=21,fill=col))
        s.append(L(x-8,y0,x+8,y0,MUTED,2))
    s.append(T(xL-16,y0+7,mix='0',size=19,anchor='end')+T(xR+16,y0+7,mix='0',size=19,anchor='start'))
    s.append(L(xL,y0,xR,y0,MUTED,1.5,'5 4'))
    yS=y0-109.8*sc; yG=y0+32.7*sc*3.4
    s.append(an('pop',C(xL,yS,8,FIELD,2,FIELD),o=f'{xL},{f(yS)}'))
    s.append(T(xL-16,yS+7,mix='$+109.8\\ \\text{J/K}$',size=19,anchor='end',fill=FIELD))
    s.append(an('pop',C(xR,yG,8,INK,2,INK),delay='.6',o=f'{xR},{f(yG)}'))
    s.append(T(xR+16,yG+7,mix='$-32.7\\ \\text{kJ}$',size=19,anchor='start'))
    s.append(an('draw',P([(xL+12,yS+6),(270,y0),(xR-12,yG-6)],MUTED,2,dash='5 4'),delay='.2'))
    s.append(T(270,y0-16,tex='\\times(-T)',size=20,fill=MUTED,halo=True))
    s.append(T(xL,322,mix='증가 (자발)',size=19,fill=FIELD)+T(xR,322,mix='감소 (자발)',size=19))
    return svg((480,336),420,'일정한 온도와 압력에서 ΔG = −TΔS전체이므로 전체 엔트로피가 증가하면 깁스 자유 에너지는 감소한다',s)
FIG['MIRROR']=mirror()

# ═════ 9 ④ 그림 Ⅲ-22 새로 그림: G–과정 ═════
def gcurve():
    s=[]; X0,Y0,W,H=70,300,370,240
    s.append(R(X0,Y0-H,W,H,'none',0,'#FFF8E6'))
    s.append(L(X0,Y0,X0+W+10,Y0,MUTED,2)+L(X0,Y0,X0,Y0-H-10,MUTED,2))
    fx=lambda t: Y0-H+12+ (H-60)*(1-((t-0.62)/0.62)**2) if False else None
    def gy(t): return Y0-50-170*((t-0.62)/0.62)**2 if t<0.62 else Y0-50-170*((t-0.62)/0.70)**2
    pts=[(X0+t*W,  Y0-  (50+ (170*((t-0.62)/0.62)**2 if t<0.62 else 120*((t-0.62)/0.38)**2)) ) for t in [i/100 for i in range(101)]]
    s.append(P(pts,EQUI,4))
    xm=X0+0.62*W; ym=Y0-50
    s.append(L(xm,ym,xm,Y0,MUTED,1.5,'5 4')+T(xm,ym-80,mix='평형',size=20,weight=700))
    s.append(L(xm,ym-68,xm,ym-12,MUTED,1.5))
    s.append(an('move',C(xm,ym-11,11,INK,2,PLUS),**{'from':f'{f(X0+0.12*W-xm)},{f(-(170*((0.12-0.62)/0.62)**2))}','dur':'1.8','ease':'out'}))
    s.append(A(X0+0.18*W,Y0-50-170*((0.18-.62)/.62)**2-14,X0+0.36*W,Y0-50-170*((0.36-.62)/.62)**2-14,'field',4))
    s.append(A(X0+0.95*W,Y0-50-120*((0.95-.62)/.38)**2-14,X0+0.80*W,Y0-50-120*((0.80-.62)/.38)**2-14,'field',4))
    s.append(T(X0+0.28*W,Y0-120,mix='자발적',size=20,fill=FIELD,weight=700,anchor='end',halo=True))
    s.append(T(X0+0.92*W,Y0-146,mix='자발적',size=20,fill=FIELD,weight=700,halo=True))
    s.append(T(X0+W,Y0+30,mix='반응 진행',size=19,anchor='end',fill=MUTED))
    s.append(T(X0+6,Y0-H-16,mix='깁스 자유 에너지 $G$',size=19,anchor='start',fill=MUTED))
    return svg((470,340),440,'일정한 온도와 압력에서 계는 깁스 자유 에너지가 감소하는 방향으로 변하여 G가 가장 작은 평형에 이른다',s)
FIG['CURVE']=gcurve()

# ═════ 10 ⑤ 사분면: ΔH, ΔS 부호 ═════
def quad():
    s=[]; cx,cy,w=240,182,190
    cells=[(1,-1,'나','항상 자발적',FIELD,'#E3F4EA'),(-1,-1,'가','낮은 온도에서 자발적',INK,'#EEF2F6'),
           (1,1,'라','높은 온도에서 자발적',INK,'#EEF2F6'),(-1,1,'다','항상 비자발적',PLUS,'#FBE5E8')]
    for i,(sx,sy,k,lab,col,bg) in enumerate(cells):
        x=cx if sx>0 else cx-w; y=cy if sy>0 else cy-140
        body=R(x+4,y+4,w-8,132,col,2,bg,10)+T(x+w/2,y+44,mix=f'({k})',size=20,weight=700,fill=col)+T(x+w/2,y+84,mix=lab.replace(' 자발','||자발') if len(lab)>8 else lab,size=19,fill=col,weight=700)
        s.append(an('pop',body,delay=f(i*.25),o=f'{f(x+w/2)},{f(y+70)}'))
    s.append(A(cx-w-14,cy,cx+w+20,cy,'ink',2.5)+A(cx,cy+150,cx,cy-160,'ink',2.5))
    s.append(T(cx+w+18,cy+30,tex='\\Delta S',size=21,anchor='end')+T(cx+12,cy-150,tex='\\Delta H',size=21,anchor='start'))
    s.append(T(cx+w-6,cy-148,mix='흡열',size=18,anchor='end',fill=MUTED)+T(cx+w-6,cy+176,mix='발열',size=18,anchor='end',fill=MUTED))
    return svg((480,370),440,'ΔH와 ΔS의 부호에 따른 네 경우: 발열·증가는 항상 자발, 발열·감소는 낮은 온도, 흡열·증가는 높은 온도에서 자발, 흡열·감소는 항상 비자발',s)
FIG['QUAD']=quad()

# ═════ 11 ⑥ 얼음과 물의 평형 ═════
def icewater():
    s=[]; x,y,w,h=60,80,220,210
    s.append(beaker(x,y,w,h,150))
    for i,(dx,dy,a) in enumerate([(30,96,10),(96,104,-8),(150,94,14),(60,148,-12),(130,152,6)]):
        s.append(an('move',f'<g transform="rotate({a} {x+dx+20} {y+dy+16})">'+R(x+dx,y+dy,40,32,ICE_S,2,ICE,6)+'</g>',**{'from':f'0,{f(3 if i%2 else -3)}','rep':'alt','dur':f(1.4+i*.2),'ease':'io'}))
    s.append(T(x+w/2,y-30,mix='$0\\ {}^\\circ\\text{C}$, $1\\ \\text{atm}$',size=20))
    s.append(T(310,150,mix='물 $1\\ \\text{mol}$의 $G$',size=19,anchor='start'))
    s.append(T(380,188,mix='$=$',size=24,weight=700))
    s.append(T(310,226,mix='얼음 $1\\ \\text{mol}$의 $G$',size=19,anchor='start'))
    s.append(T(380,276,mix='$\\Delta G=0$ (평형)',size=20,fill=FIELD,weight=700))
    return svg((480,320),440,'0 °C, 1 atm에서 얼음과 물이 공존하는 평형에서는 물 1 mol과 얼음 1 mol의 깁스 자유 에너지가 같다',s)
FIG['ICE']=icewater()

# ═════ 12 ⑦ 직선의 절편과 기울기 (가상의 반응 ΔH° = +60 kJ, ΔS° = +100 J/K) ═════
def gline_generic():
    ax=Ax(80,300,360,250,1000,80,xmin=0,ymin=-40)
    s=[ax.frame([0,200,400,600,800,1000],[-40,-20,0,20,40,60,80],T(452,350,mix='$T$ [K]',size=19,anchor='end',fill=MUTED),
                T(74,32,mix='$\\Delta G^\\circ$ [kJ]',size=19,anchor='start',fill=MUTED),size=18)]
    s.append(zero(ax))
    s.append(L(ax.X(0),ax.Y(60),ax.X(1000),ax.Y(60),RD,2.5,'8 5')+T(ax.X(990),ax.Y(60)-10,tex='\\Delta H^\\circ',size=19,anchor='end',fill=RD,halo=True))
    s.append(gline(ax,60,100,0,1000))
    s.append(an('pop',C(ax.X(0),ax.Y(60),7,INK,2,PLUS),o=f'{f(ax.X(0))},{f(ax.Y(60))}'))
    s.append(step('i1',T(ax.X(30),ax.Y(60)-12,mix='절편 $=\\Delta H^\\circ$',size=19,anchor='start',fill=PLUS,halo=True)))
    # 기울기 삼각형 200→400 K
    x1,x2=200,400; y1,y2=60-x1*0.1,60-x2*0.1
    s.append(step('i2',P([(ax.X(x1),ax.Y(y1)),(ax.X(x2),ax.Y(y1)),(ax.X(x2),ax.Y(y2))],MUTED,2,dash='5 4')
             +T(ax.X(300),ax.Y(y1)-10,mix='$\\Delta T$',size=18,halo=True)+T(ax.X(x2)+8,ax.Y((y1+y2)/2)+6,mix='$\\Delta(\\Delta G^\\circ)$',size=18,anchor='start',halo=True)
             +T(ax.X(160),ax.Y(-28),mix='기울기 $=-\\Delta S^\\circ$',size=19,anchor='start',fill=BF,halo=True)))
    s.append(A(ax.X(700),ax.Y(60)+6,ax.X(700),ax.Y(60-70)-6,'bfield',3))
    s.append(T(ax.X(700)+10,ax.Y(30),mix='$-T\\Delta S^\\circ$',size=19,anchor='start',fill=BF,halo=True))
    s.append(T(ax.X(970),ax.Y(60-97)-12,tex='\\Delta G^\\circ',size=19,anchor='end',halo=True))
    return svg((470,362),450,'ΔG° = ΔH° − TΔS°는 T에 대한 직선으로, 세로축 절편이 ΔH°, 기울기가 −ΔS°이다',s)
FIG['LINE']=gline_generic()

# ═════ 13·14 그림 Ⅲ-23 새로 그림 (실제 반응의 계산값) ═════
CASES={'가':('\\ce{N2 + 3H2 -> 2NH3}',-92.0,-198.9,(-100,150),[-100,0,100]),
       '나':('\\ce{2H2O2(l) -> 2H2O(l) + O2}',-196.1,125.8,(-400,0),[-400,-300,-200,-100,0]),
       '다':('\\ce{3O2 -> 2O3}',285.4,-137.6,(0,500),[0,100,200,300,400,500]),
       '라':('\\ce{CaCO3 -> CaO + CO2}',178.3,160.6,(-100,200),[-100,0,100,200])}
SIGN={'가':'\\Delta H^\\circ&lt;0,\\ \\Delta S^\\circ&lt;0','나':'\\Delta H^\\circ&lt;0,\\ \\Delta S^\\circ&gt;0','다':'\\Delta H^\\circ&gt;0,\\ \\Delta S^\\circ&lt;0','라':'\\Delta H^\\circ&gt;0,\\ \\Delta S^\\circ&gt;0'}
def panel(k,ox):
    eq,H,S,(ymn,ymx),yt=CASES[k]
    ax=Ax(ox+66,330,170,226,1200,ymx,xmin=0,ymin=ymn)
    s=[ax.frame([0,600,1200],yt,T(ox+246,378,mix='$T$ [K]',size=18,anchor='end',fill=MUTED),
                T(ox+60,84,mix='$\\Delta G^\\circ$ [kJ]',size=18,anchor='start',fill=MUTED),size=18)]
    s.append(zero(ax)+shade(ax,H,S,0,1200,size=18))
    s.append(L(ax.X(0),ax.Y(H),ax.X(1200),ax.Y(H),RD,2.5,'7 5'))
    s.append(gline(ax,H,S,0,1200,dash=DASH[k]))
    Tm=900; s.append(A(ax.X(Tm),ax.Y(H),ax.X(Tm),ax.Y(H-Tm*S/1000),'bfield',2.5))
    s.append(T(ox+130,30,mix=f'({k}) ${SIGN[k]}$',size=19,weight=700))
    s.append(T(ox+130,60,tex=eq,size=18))
    tx=H/S*1000 if H*S>0 else None
    if tx and 0<tx<1200:
        s.append(C(ax.X(tx),ax.Y(0),6,INK,2,'#FFFFFF'))
        s.append(T(ax.X(tx),ax.Y(0)-14 if k=='라' else ax.Y(0)+28,mix=f'${tx:.0f}\\ \\text{{K}}$',size=18,halo=True))
    return ''.join(s),ax
def cases(k1,k2):
    s=[]
    for k,ox in ((k1,0),(k2,270)):
        b,ax=panel(k,ox); s.append(b)
    s.append(T(540,404,mix='$\\Delta H^\\circ$ (빨강 점선)   $-T\\Delta S^\\circ$ (보라 화살표)   $\\Delta G^\\circ$ (검정)',size=18,anchor='end',fill=MUTED))
    return svg((540,414),540,f'그림 Ⅲ-23 ({k1})({k2})를 실제 반응의 계산값으로 다시 그린 ΔG°–T 그래프',s)
FIG['CASE_AB']=cases('가','나'); FIG['CASE_CD']=cases('다','라')

# ═════ 15 ⑩ 같은 부호일 때만 가로축과 만난다 (가상의 두 반응) ═════
def tstar():
    ax=Ax(80,300,360,250,1200,80,xmin=0,ymin=-80)
    s=[ax.frame([0,300,600,900,1200],[-80,-40,0,40,80],T(452,350,mix='$T$ [K]',size=19,anchor='end',fill=MUTED),
                T(74,32,mix='$\\Delta G^\\circ$ [kJ]',size=19,anchor='start',fill=MUTED),size=18)]
    s.append(zero(ax))
    s.append(gline(ax,-60,-100,0,1200,dash=DASH['가'])+gline(ax,60,100,0,1200,dash=DASH['라']))
    s.append(an('pop',C(ax.X(600),ax.Y(0),8,INK,2.5,'#FFFFFF'),delay='1',o=f'{f(ax.X(600))},{f(ax.Y(0))}'))
    s.append(T(ax.X(600),ax.Y(-40),mix='$T=\\dfrac{\\Delta H^\\circ}{\\Delta S^\\circ}$',size=19,halo=True))
    s.append(T(ax.X(1180),ax.Y(60)+4,mix='(가)',size=19,anchor='end',weight=700,halo=True)+T(ax.X(60),ax.Y(60)-12,mix='(라)',size=19,anchor='start',weight=700,halo=True))
    s.append(T(ax.X(170),ax.Y(-60)+30,mix='(가) 자발적',size=18,fill=FIELD,weight=700,halo=True))
    s.append(T(ax.X(1000),ax.Y(-40)+40,mix='(라) 자발적',size=18,fill=FIELD,weight=700,halo=True))
    return svg((470,362),450,'ΔH°와 ΔS°의 부호가 같은 두 경우 (가)와 (라)의 직선은 T = ΔH°/ΔS°에서 가로축과 만나 자발성이 바뀐다',s)
FIG['TSTAR']=tstar()

# ═════ 16 예제 Ⅲ-8 브로민 ═════
def br2():
    ax=Ax(80,290,360,240,500,20,xmin=200,ymin=-20)
    s=[ax.frame([200,300,400,500],[-10,0,10,20],T(452,342,mix='$T$ [K]',size=19,anchor='end',fill=MUTED),
                T(74,32,mix='$\\Delta G^\\circ$ [kJ/mol]',size=19,anchor='start',fill=MUTED),size=18)]
    s.append(zero(ax)+shade(ax,31.0,93.0,200,500,ly=ax.Y(-16)))
    s.append(gline(ax,31.0,93.0,200,500))
    tx=31000/93.0
    s.append(step('b4',C(ax.X(tx),ax.Y(0),7,INK,2,PLUS)+T(ax.X(tx)-8,ax.Y(0)-16,mix='$333\\ \\text{K}$ 기준 끓는점',size=18,anchor='end',halo=True)))
    s.append(T(ax.X(250),ax.Y(-16),mix='비자발적',size=18,fill=MUTED,weight=700,halo=True))
    return svg((470,352),430,'브로민 증발의 ΔG°는 333 K에서 0이 되고, 333 K보다 높은 온도에서 음수가 되어 자발적이다',s)
FIG['BR2']=br2()

# ═════ 19·21 탐구 활동 그래프 ═════
def inq(result):
    ax=Ax(86,300,360,240,800,40,xmin=0,ymin=-40)
    s=[ax.frame([0,200,400,600,800],[-40,-20,0,20,40],T(456,352,mix='$T$ [K]',size=19,anchor='end',fill=MUTED),
                T(80,32,mix='$\\Delta G^\\circ$ [kJ/mol]',size=19,anchor='start',fill=MUTED),size=18)]
    s.append(zero(ax))
    if not result:
        s.append(an('pop',C(ax.X(0),ax.Y(40),7,INK,2,PLUS),o=f'{f(ax.X(0))},{f(ax.Y(40))}'))
        s.append(T(ax.X(20),ax.Y(40)+28,mix='절편 $+40$',size=19,anchor='start',fill=PLUS,halo=True))
        s.append(T(ax.X(560),ax.Y(30),mix='기울기 $-100\\ \\text{J/(K}\\cdot\\text{mol)}$',size=19,fill=MUTED,halo=True))
        s.append(T(ax.X(560),ax.Y(30)+30,mix='$=-0.100\\ \\text{kJ/(K}\\cdot\\text{mol)}$',size=19,fill=MUTED,halo=True))
        return svg((470,362),450,'탐구 활동: 세로축 절편 +40 kJ/mol, 기울기 −100 J/(K·mol)인 ΔG° 직선을 그릴 빈 그래프',s)
    s.append(step('p1',shade(ax,40,100,0,800,ly=ax.Y(-30))))
    pts=[(0,40),(200,20),(400,0),(600,-20),(800,-40)]
    for i,(t,v) in enumerate(pts):
        s.append(step('p0',C(ax.X(t),ax.Y(v),6,INK,2,PLUS if t!=400 else '#FFFFFF')))
    s.append(step('p0',gline(ax,40,100,0,800,anim=False)))
    s.append(step('p1',T(ax.X(400)+10,ax.Y(0)-14,mix='$400\\ \\text{K}$',size=19,anchor='start',halo=True)))
    return svg((470,362),450,'탐구 활동 결과: ΔG° = 40 − 0.100T 직선은 400 K에서 0이 되고 400 K보다 높은 온도에서 자발적이다',s)
FIG['INQ0']=inq(False); FIG['INQ1']=inq(True)

# ═════ 23 ⑪ 표준 생성 깁스 자유 에너지 준위 ═════
def gf():
    s=[]; y0=150; sc=0.52
    s.append(L(30,y0,450,y0,INK,3)+T(36,y0+32,mix='가장 안정한 원소: $\\Delta G_\\mathrm{f}^\\circ=0$',size=19,anchor='start'))
    lv=[(90,86.6,'\\ce{NO(g)}','+86.6'),(190,51.3,'\\ce{NO2(g)}','+51.3'),(290,-120.4,'\\ce{H2O2(l)}','-120.4'),(390,-237.1,'\\ce{H2O(l)}','-237.1')]
    for i,(x,v,lab,num) in enumerate(lv):
        y=y0-v*sc if v>0 else y0-v*sc*0.6
        s.append(an('draw',L(x-36,y,x+36,y,INK,3)+L(x,y0,x,y,MUTED,1.5,'4 4'),delay=f(i*.3),dur='.6'))
        s.append(T(x,y-12 if v>0 else y+28,tex=lab,size=19,halo=True))
        s.append(T(x,y+(-38 if v>0 else 52),mix=f'${num}$',size=18,fill=FIELD if v<0 else PLUS))
    s.append(T(450,330,mix='단위: kJ/mol, $25\\ {}^\\circ\\text{C}$',size=18,anchor='end',fill=MUTED))
    return svg((480,340),460,'표준 생성 깁스 자유 에너지: 가장 안정한 원소를 0으로 하여 NO는 +86.6, NO2는 +51.3, 과산화 수소는 −120.4, 물은 −237.1 kJ/mol',s)
FIG['GF']=gf()

# ═════ 25 진로: 물의 전기 분해 ═════
def h2():
    s=[]; x,y,w,h=90,120,300,200
    s.append(beaker(x,y,w,h,150))
    for ex,col,lab,gas,n in ((170,OX,'(+)극','\\ce{O2}',4),(310,RD,'(−)극','\\ce{H2}',8)):
        s.append(R(ex-9,y+30,18,160,col,2,'#E8EDF2',3))
        s.append(L(ex,y+30,ex,70,INK,2.5))
        s.append(T(ex,354,mix=lab,size=20,fill=col,weight=700))
        s.append(T(ex+(-40 if ex<240 else 40),y+100,tex=gas,size=20,fill=col,halo=True))
        rnd=random.Random(ex)
        for i in range(n):
            bx=ex+rnd.uniform(-22,22); by=y+70+rnd.uniform(0,90)
            s.append(an('move',C(bx,by,4+rnd.uniform(0,2.5),WATER_S,1.5,'#FFFFFF'),**{'from':f'0,{f(55+rnd.uniform(0,25))}','rep':'loop','dur':f(1.2+rnd.random()*.8),'ease':'lin'}))
    s.append(L(170,70,205,70,INK,2.5)+L(275,70,310,70,INK,2.5))
    s.append(R(205,50,70,40,INK,2,'#FFFFFF',6)+T(240,77,mix='전원',size=20))
    s.append(T(240,28,tex='\\ce{2H2O(l) -> 2H2(g) + O2(g)}',size=20))
    return svg((480,370),450,'물의 전기 분해: (+)극에서 산소, (−)극에서 수소 기체가 2배의 부피로 발생한다',s)
FIG['H2']=h2()

# ═════ 26 연습 문제 1: 두 구리 덩어리 ═════
def copper():
    s=[]
    s.append(R(40,90,170,130,CU_S,3,'#E9B08C',8)+R(250,90,170,130,CU_S,3,'#F6D9C6',8))
    s.append(T(125,150,mix='금속 2',size=20,weight=700)+T(125,186,tex='T_2',size=21))
    s.append(T(335,150,mix='금속 1',size=20,weight=700)+T(335,186,tex='T_1',size=21))
    s.append(an('draw',heat(150,250,310,250,4),dur='.9'))
    s.append(T(230,282,mix='열 $1\\ \\text{J}$',size=19,fill=EQUI))
    s.append(T(230,60,mix='$T_2&gt;T_1$ 이면?',size=20))
    return svg((460,300),420,'온도가 다른 두 구리 덩어리를 접촉하면 열이 온도가 높은 금속 2에서 온도가 낮은 금속 1로 이동한다',s)
FIG['CU']=copper()

# ═════ 27 연습 문제 2: 두 단계 가역 경로 ═════
def arpath():
    ax=Ax(90,280,330,210,6,300,xmin=0,ymin=290)
    s=[ax.frame([0,1,2,3,4,5,6],[290,295,300],T(436,334,mix='$V$ [L]',size=19,anchor='end',fill=MUTED),
                T(84,52,mix='$T$ [K]',size=19,anchor='start',fill=MUTED),size=19)]
    A0=(ax.X(5),ax.Y(293.2)); B=(ax.X(1),ax.Y(293.2)); Cc=(ax.X(1),ax.Y(298.4))
    s.append(P([A0,Cc],MUTED,2.5,dash='8 6')+T((A0[0]+Cc[0])/2+20,(A0[1]+Cc[1])/2-10,mix='실제(비가역)',size=18,anchor='start',fill=MUTED,halo=True))
    s.append(an('draw',P([A0,B],BF,3.5),dur='.8')+an('draw',P([B,Cc],RD,3.5),dur='.6',delay='.8'))
    s.append(T((A0[0]+B[0])/2,A0[1]+30,mix='1단계 등온 압축',size=18,fill=BF,halo=True))
    s.append(T(B[0]+12,(B[1]+Cc[1])/2+6,mix='2단계 가열',size=18,anchor='start',fill=RD,halo=True))
    for p,lab,dx in ((A0,'$5.00\\ \\text{L},\\ 293.2\\ \\text{K}$',-6),(Cc,'$1.00\\ \\text{L},\\ 298.4\\ \\text{K}$',8)):
        s.append(C(p[0],p[1],6,INK,2,PLUS))
    s.append(T(A0[0],A0[1]-14,mix='$5.00\\ \\text{L},\\ 293.2\\ \\text{K}$',size=18,anchor='middle',halo=True))
    s.append(T(Cc[0]+10,Cc[1]-14,mix='$1.00\\ \\text{L},\\ 298.4\\ \\text{K}$',size=18,anchor='start',halo=True))
    return svg((460,344),440,'엔트로피는 상태 함수이므로 비가역 압축 대신 등온 압축과 일정 부피 가열의 두 가역 단계로 계산한다',s)
FIG['AR']=arpath()

# ═════ 29 연습 문제 4: 산화 철(Ⅲ)의 탄소 환원 ═════
def fe():
    ax=Ax(80,300,360,250,1200,500,xmin=0,ymin=-200)
    s=[ax.frame([0,300,600,900,1200],[-200,0,200,400],T(452,350,mix='$T$ [K]',size=20,anchor='end',fill=MUTED),
                T(74,32,mix='$\\Delta G^\\circ$ [kJ]',size=20,anchor='start',fill=MUTED),size=20)]
    s.append(zero(ax)+step('e3',shade(ax,467.9,558.4,0,1200,size=20,ly=ax.Y(-160))))
    s.append(gline(ax,467.9,558.4,0,1200,dash=DASH['라']))
    tx=467900/558.4
    s.append(step('e3',C(ax.X(tx),ax.Y(0),7,INK,2,PLUS)+T(ax.X(tx)-10,ax.Y(0)-16,mix='$838\\ \\text{K}$',size=20,anchor='end',halo=True)))
    return svg((470,362),415,'산화 철(Ⅲ)의 탄소 환원은 838 K보다 높은 온도에서 ΔG°가 음수가 되어 가능하다',s)
FIG['FE']=fe()

# ═════ 출력 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(out)
for src,dst in (('labs_src.js','labs.js'),('extra_src.css','extra.css')):
    if os.path.exists(os.path.join(HERE,src)): shutil.copy(os.path.join(HERE,src),OUT+dst)
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "깁스 자유 에너지와 반응의 자발성", "file": "3-2-2_깁스_자유_에너지와_반응의_자발성", "header": "Ⅲ-2-2 깁스 자유 에너지와 반응의 자발성 (고등 고급 화학 151–156쪽)"}\n')
print('ok',len(out),'sections',out.count('<section'),'anim',out.count('data-anim'))
