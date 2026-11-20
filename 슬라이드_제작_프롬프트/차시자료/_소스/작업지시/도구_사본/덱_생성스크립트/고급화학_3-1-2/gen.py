# -*- coding: utf-8 -*-
"""고급화학 3-1-2 엔탈피 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   엔탈피 도표는 kJ → px 비율 하나(EN 클래스)로 그려 계산값과 비율이 맞는다(비율은 실행할 때 출력).
   labs_src.js·extra_src.css를 labs.js·extra.css로 복사한다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)"""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
OUT=BASE+'3-1-2_엔탈피/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-1-2_엔탈피/', OUT
assert os.path.isdir(OUT), OUT
FIG={}; SCALES={}
PIS='#C9D2DB'; FLAME='#F2A93B'; SYSBG='#FFF4E8'
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def gas(x,y,w,h,n,seed,r=8,anim=True):
    rnd=random.Random(seed); pts=[]; s=[]; tries=0
    while len(pts)<n and tries<4000:
        tries+=1; p=(rnd.uniform(x+r+5,x+w-r-5),rnd.uniform(y+r+5,y+h-r-5))
        if all(math.hypot(p[0]-a,p[1]-b)>2.8*r for a,b in pts): pts.append(p)
    for px,py in pts:
        b=gm(px,py,r)
        if anim:
            th=rnd.uniform(0,6.283); s.append(an('move',b,**{'from':f'{f(5*math.cos(th))},{f(5*math.sin(th))}','rep':'alt','dur':f(0.8+0.5*rnd.random()),'ease':'io'}))
        else: s.append(b)
    return ''.join(s)
def flame(cx,by,s=1.0):
    return (f'<path d="M{f(cx)} {f(by-34*s)} C{f(cx+16*s)} {f(by-16*s)} {f(cx+14*s)} {f(by)} {f(cx)} {f(by)} C{f(cx-14*s)} {f(by)} {f(cx-16*s)} {f(by-16*s)} {f(cx)} {f(by-34*s)} Z" fill="{FLAME}" stroke="{OX}" stroke-width="1.5"/>'
            +f'<path d="M{f(cx)} {f(by-18*s)} C{f(cx+7*s)} {f(by-9*s)} {f(cx+6*s)} {f(by)} {f(cx)} {f(by)} C{f(cx-6*s)} {f(by)} {f(cx-7*s)} {f(by-9*s)} {f(cx)} {f(by-18*s)} Z" fill="#FFE45C"/>')
def thermo(x,top,bot,lvl,col=PLUS):
    return (R(x-5,top,10,bot-top,INK,1.5,'#FFFFFF',5)+C(x,bot+6,9,INK,1.5,col)+R(x-2.5,lvl,5,bot-lvl+4,'none',0,col))
def vdim(x,y1,y2,lab,col=MUTED,size=19,dx=10,anchor='start'):
    return (L(x-7,y1,x+7,y1,col,1.5)+L(x-7,y2,x+7,y2,col,1.5)+A(x,y1+2,x,y2-2,'muted',1.5)+A(x,y2-2,x,y1+2,'muted',1.5)+T(x+dx,(y1+y2)/2+7,mix=lab,size=size,anchor=anchor,fill=col))
def atom(x,y,r,el,lab=None):
    return f'<g data-atom="{f(x)},{f(y)},{r},{el}'+(f',{lab}' if lab else '')+'"></g>'

class EN:
    """엔탈피 도표: Y(v) = y0 − s·v (v kJ, 위로 증가)"""
    def __init__(s,y0,sc,key):
        s.y0,s.s=y0,sc; SCALES[key]=sc
    def Y(s,v): return s.y0-s.s*v
    def lev(s,x1,x2,v,tex=None,mix=None,size=20,dy=-10,anchor='middle',lx=None,col=INK):
        y=s.Y(v); o=L(x1,y,x2,y,col,3)
        if tex or mix: o+=T(lx if lx is not None else (x1+x2)/2,y+dy,tex=tex,mix=mix,size=size,anchor=anchor,halo=True)
        return o
    def arr(s,x,v1,v2,col='ink',w=3,gap=3):
        y1,y2=s.Y(v1),s.Y(v2); d=gap if y2>y1 else -gap
        return A(x,y1+d,x,y2-d,col,w)
def haxis(x,ytop,ybot,lab='엔탈피 $H$',dx=10):
    return A(x,ybot,x,ytop,'muted',2)+T(x+dx,ytop+12,mix=lab,size=19,anchor='start',fill=MUTED)

# ═════ 1 표지: 헤스 법칙 도표 ═════
def cover():
    e=EN(342,1.20,'표지'); s=[]
    s.append(e.lev(100,240,0,tex='\\ce{N2(g) + 2O2(g)}',dy=30,lx=170))
    s.append(L(240,e.Y(0),372,e.Y(0),MUTED,1.5,'5 4'))
    s.append(e.lev(130,300,180,tex='\\ce{2NO(g) + O2(g)}',lx=215))
    s.append(e.lev(270,380,68,tex='\\ce{2NO2(g)}',dy=-12,lx=330))
    s.append(an('draw',e.arr(165,0,180,'field',4),dur='1.0'))
    s.append(T(157,e.Y(100),tex='+180',size=22,anchor='end',fill=FIELD))
    s.append(an('draw',e.arr(285,180,68,'bfield',4),dur='1.0',delay='.9'))
    s.append(T(277,e.Y(130),tex='-112',size=22,anchor='end',fill=BF))
    s.append(an('draw',e.arr(355,0,68,'ink',4),dur='.9',delay='1.8'))
    s.append(T(347,e.Y(30)+8,tex='+68',size=22,anchor='end',halo=True))
    return svg((460,460),430,'헤스 법칙: 질소가 두 단계(+180 kJ, −112 kJ)를 거쳐도 한 단계(+68 kJ)로 반응해도 엔탈피 변화는 같다',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 3 진로: 에너지 전환 ═════
def career():
    s=[]
    # 공장 굴뚝
    s.append(R(20,120,120,90,INK,2,'#E6EBF0',4)+R(40,60,22,62,INK,2,'#C9D2DB')+R(90,76,22,46,INK,2,'#C9D2DB'))
    s.append(an('move',C(52,44,12,MUTED,1.5,'#EEF1F4')+C(70,30,15,MUTED,1.5,'#EEF1F4'),**{'from':'-6,14','dur':'2','rep':'loop'}))
    s.append(T(80,240,mix='화석 연료',size=20,weight=700)+T(80,266,mix='$\\ce{CO2}$ 배출, 고갈',size=19,fill=MUTED))
    s.append(A(160,160,226,160,'ink',4))
    # 태양
    s.append(C(282,74,24,EQUI,2,'#FFE7B8'))
    for i in range(8):
        a=i*math.pi/4; s.append(L(282+31*math.cos(a),74+31*math.sin(a),282+42*math.cos(a),74+42*math.sin(a),EQUI,3))
    # 풍력
    s.append(L(372,150,372,72,INK,3))
    s.append(an('spin',''.join(P([(372,72),(372+34*math.cos(a),72+34*math.sin(a))],INK,4) for a in (-math.pi/2,math.pi/6,5*math.pi/6)),o='372,72',speed='60'))
    s.append(C(372,72,4,INK,1,INK))
    # 수소
    s.append(atom(300,180,18,'H')+atom(326,180,18,'H'))
    s.append(T(326,240,mix='신재생·청정에너지',size=20,weight=700)+T(326,266,mix='태양·풍력·수소',size=19,fill=MUTED))
    return svg((440,280),420,'화석 연료 중심에서 태양, 풍력, 수소 같은 신재생·청정에너지로',s)
FIG['CAREER']=career()

# ═════ 4 생각 열기: 단단한 통 / 열린 용기 ═════
def cyl(x,top,w,bot,py,fill='#FFFFFF',n=8,seed=1,pt=14,anim=True,r=8):
    s=[R(x+3,py+pt,w-6,bot-py-pt,'none',0,fill)]
    s.append(gas(x+3,py+pt,w-6,bot-py-pt,n,seed,r,anim))
    s.append(R(x+3,py,w-6,pt,INK,2,PIS,2))
    s.append(P([(x,top),(x,bot),(x+w,bot),(x+w,top)],INK,3))
    return ''.join(s)
def openfig():
    s=[]
    # (가) 단단한 통
    s.append(R(40,90,170,170,INK,5,SYSBG,14)+gas(46,96,158,158,9,7))
    s.append(T(125,22,mix='(가) 단단한 통',size=21,weight=700))
    s.append(T(125,300,tex='\\Delta V=0\\ \\rightarrow\\ w=0',size=21))
    s.append(T(125,334,tex='\\Delta U=q_V',size=22))
    s.append(an('fade',A(214,175,262,175,'equi',4),dur='1',rep='loop')+T(238,160,mix='열',size=19,fill=EQUI))
    # (나) 열린 용기
    x=330; s.append(an('move',cyl(x,70,170,260,124,SYSBG,9,11),**{'from':'0,26','dur':'1.6','ease':'out'}))
    for xx in (365,415,465): s.append(A(xx,64,xx,110,'ink',3))
    s.append(T(415,54,mix='대기압 약 $1\\ \\text{atm}$',size=19))
    s.append(L(x+3,150,x+167,150,MUTED,1.5,'5 4')+T(x+176,156,mix='처음',size=18,anchor='start',fill=MUTED))
    s.append(A(x+190,140,x+190,104,'ink',4)+T(x+180,192,mix='대기를||밀어냄',size=18,anchor='start'))
    s.append(T(x+85,300,tex='\\Delta V>0\\ \\rightarrow\\ w<0',size=21))
    s.append(T(x+85,334,mix='열 $q$ ≠ $\\Delta U$',size=22))
    s.append(T(x+85,22,mix='(나) 열린 용기(압력 일정)',size=21,weight=700))
    return svg((570,350),560,'(가) 부피가 변하지 않는 단단한 통에서는 일이 없다 (나) 압력이 일정한 열린 용기에서는 기체가 대기를 밀어내며 일을 한다',s)
FIG['OPEN']=openfig()

# ═════ 5 엔탈피 정의: 상자 ═════
def hdef():
    s=[]
    boxes=[(20,'H','엔탈피',PLUS),(200,'U','내부 에너지',INK),(334,'P','압력',INK),(450,'V','부피',INK)]
    for i,(x,t,lab,col) in enumerate(boxes):
        b=R(x,30,96,84,col,3,'#FFFFFF' if t!='H' else '#FDECEE',12)+T(x+48,88,tex=t,size=40,fill=col)+T(x+48,146,mix=lab,size=20)
        s.append(an('pop',b,o=f'{x+48},72',dur='.5',delay=f'{0.25*i:.2f}'))
    s.append(T(158,88,tex='\\equiv',size=38)+T(313,88,tex='+',size=38))
    s.append(T(373,200,mix='셋 다 상태 함수 → $H$도 상태 함수',size=20,fill=FIELD,weight=700))
    s.append(P([(216,158),(216,166),(540,166),(540,158)],FIELD,2))
    return svg((570,214),540,'엔탈피 H는 내부 에너지 U에 압력 P와 부피 V의 곱을 더한 것으로, U, P, V가 상태 함수이므로 H도 상태 함수이다',s)
FIG['HDEF']=hdef()

# ═════ 7 두 열량계 (3-1-1 그림을 줄여 고침) ═════
def cup(w=300):
    s=[]
    s.append(f'<path d="M80 110 L280 110 L262 330 L98 330 Z" fill="#F3F5F8" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<path d="M100 120 L260 120 L246 318 L114 318 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<path d="M106 196 L254 196 L246 318 L114 318 Z" fill="#F7D8A8"/>')
    s.append(R(74,96,212,16,INK,2,'#E6EBF0',4))
    s.append(thermo(220,30,284,200))
    s.append(P([(150,40),(150,296),(130,296),(170,296)],MUTED,3))
    s.append(an('move',C(160,250,4,INK,1,'#FFFFFF')+C(130,270,3,INK,1,'#FFFFFF'),**{'from':'0,30','dur':'1.4','rep':'loop'}))
    s.append(T(236,46,mix='온도계',size=25,anchor='start')+T(140,54,mix='젓개',size=25,anchor='end'))
    s.append(T(180,92,mix='뚜껑',size=25,halo=True))
    s.append(T(180,376,mix='대기압에서 반응',size=25))
    return svg((400,392),w,'컵 열량계: 2겹 폴리스타이렌 컵과 뚜껑, 온도계, 젓개 — 대기압(압력 일정)에서 반응',s)
def bomb(w=320):
    s=[R(40,90,320,250,INK,3,'#F3F5F8',10)+R(56,104,288,222,'none',0,WATER)]
    s.append(R(150,170,100,120,INK,3,'#B7C0CA',12)+R(168,250,64,24,INK,1.5,'#FFFFFF',3)+R(180,240,40,12,INK,1.5,'#3A3F47',2))
    s.append(L(176,170,176,60,INK,2)+L(224,170,224,60,INK,2)+C(176,56,5,INK,2,'#FFFFFF')+C(224,56,5,INK,2,'#FFFFFF'))
    s.append(an('pop',C(200,236,9,OX,1.5,'#FFE45C'),o='200,236',dur='.8',rep='loop'))
    s.append(L(176,200,192,236,INK,1.5)+L(224,200,208,236,INK,1.5))
    s.append(thermo(300,40,300,170))
    s.append(T(200,34,mix='점화 단자',size=25)+T(312,62,mix='온도계',size=25,anchor='start'))
    s.append(T(100,318,mix='물',size=25)+T(146,160,mix='강철 통',size=25,anchor='end'))
    s.append(T(200,376,mix='부피 일정',size=25))
    return svg((420,392),w,'통열량계: 물에 잠긴 단단한 강철 통 속에서 시료가 연소한다 — 부피 일정',s)
FIG['CUP2']=cup(290); FIG['BOMB2']=bomb(300)
FIG['BOMB3']=bomb(330)

# ═════ 8 발열·흡열: 같은 비율 두 도표 ═════
def sign():
    sc=0.80; s=[haxis(24,26,350)]
    e1=EN(96,sc,'S8 발열·흡열')
    s.append(e1.lev(60,240,0,tex='\\ce{Zn(s) + I2(s)}'))
    s.append(e1.lev(60,240,-208,tex='\\ce{ZnI2(s)}',dy=30))
    s.append(an('draw',e1.arr(160,0,-208,'ink',4),dur='1.1'))
    s.append(T(172,e1.Y(-104)+8,tex='-208\\ \\text{kJ}',size=21,anchor='start',halo=True))
    s.append(an('fade',A(150,e1.Y(-130),90,e1.Y(-130),'equi',4),dur='1',rep='loop')+T(118,e1.Y(-130)-14,mix='열 방출',size=19,fill=EQUI))
    s.append(T(150,378,mix='발열: $\\Delta H&lt;0$',size=21,weight=700))
    e2=EN(300,sc,'S8 발열·흡열')
    s.append(e2.lev(360,560,0,tex='\\ce{N2(g) + O2(g)}',dy=30))
    s.append(e2.lev(360,560,180,tex='\\ce{2NO(g)}'))
    s.append(an('draw',e2.arr(460,0,180,'ink',4),dur='1.1',delay='.6'))
    s.append(T(472,e2.Y(90)+8,tex='+180\\ \\text{kJ}',size=21,anchor='start',halo=True))
    s.append(an('fade',A(392,e2.Y(60),450,e2.Y(60),'equi',4),dur='1',rep='loop')+T(420,e2.Y(60)-14,mix='열 흡수',size=19,fill=EQUI))
    s.append(T(460,378,mix='흡열: $\\Delta H&gt;0$',size=21,weight=700))
    return svg((600,392),560,'같은 비율의 엔탈피 도표: 아이오딘화 아연 생성은 208 kJ 발열, 일산화 질소 생성은 180 kJ 흡열',s)
FIG['SIGN']=sign()

# ═════ 9 예제 Ⅲ-3: 에너지 출입 ═════
def ex3():
    s=[R(130,60,170,150,INK,4,SYSBG,14)+T(215,150,mix='계',size=24,weight=700)]
    s.append(an('fade',A(215,56,215,8,'equi',5),dur='1',rep='loop')+T(228,30,mix='열 $50\\ \\text{kJ}$ 방출',size=20,anchor='start',fill=EQUI))
    s.append(A(304,135,380,135,'ink',6)+T(342,118,mix='일 $20\\ \\text{kJ}$',size=20)+T(342,162,mix='(팽창)',size=19,fill=MUTED))
    s.append(T(215,246,tex='q=-50\\ \\text{kJ},\\ \\ w=-20\\ \\text{kJ}',size=21))
    return svg((430,262),400,'계가 열 50 kJ을 방출하고 팽창 일 20 kJ을 한다',s)
FIG['EX3']=ex3()

# ═════ 12 그림 Ⅲ-11 메테인 연소 ═════
def ch4st():
    e=EN(70,0.30,'S12 그림 Ⅲ-11'); s=[haxis(26,30,370)]
    s.append(e.lev(60,420,0,tex='\\ce{CH4(g) + 2O2(g)}',lx=240))
    s.append(e.lev(60,290,-802,tex='\\ce{CO2(g) + 2H2O(g)}',lx=190))
    s.append(e.lev(60,420,-890,tex='\\ce{CO2(g) + 2H2O(l)}',dy=30,lx=240))
    s.append(an('draw',e.arr(84,0,-802,'ink',4),dur='1.1'))
    s.append(T(96,e.Y(-400),tex='-802\\ \\text{kJ}',size=21,anchor='start',halo=True))
    s.append(an('draw',e.arr(390,0,-890,'ink',4),dur='1.2',delay='.4'))
    s.append(T(380,e.Y(-445),tex='-890\\ \\text{kJ}',size=21,anchor='end',halo=True))
    s.append(L(290,e.Y(-802),336,e.Y(-802),MUTED,1.5,'5 4'))
    s.append(an('draw',e.arr(316,-802,-890,'equi',3,2),dur='.6',delay='1.4'))
    s.append(T(328,e.Y(-846)+7,tex='-88\\ \\text{kJ}',size=20,anchor='start',fill=EQUI,halo=True))
    return svg((520,380),470,'메테인 연소의 엔탈피 변화: 수증기가 생기면 −802 kJ, 물이 생기면 −890 kJ, 차이 88 kJ',s)
FIG['CH4ST']=ch4st()

# ═════ 16 예제 Ⅲ-4 흑연·다이아몬드 ═════
def diam():
    e=EN(96,0.70,'S16 예제 Ⅲ-4'); s=[haxis(26,24,396)]
    s.append(e.lev(44,184,2,tex='\\mathrm{C}_\\text{다이아몬드}(s)+\\ce{O2(g)}',dy=-12,lx=112))
    s.append(e.lev(214,364,0,tex='\\mathrm{C}_\\text{흑연}(s)+\\ce{O2(g)}',dy=-12,lx=302))
    s.append(e.lev(44,364,-394,tex='\\ce{CO2(g)}',dy=30))
    s.append(an('draw',e.arr(110,2,-394,'bfield',4),dur='1.1'))
    s.append(T(122,e.Y(-190),tex='-396\\ \\text{kJ}',size=21,anchor='start',fill=BF,halo=True))
    s.append(an('draw',e.arr(300,0,-394,'field',4),dur='1.1',delay='.4'))
    s.append(T(312,e.Y(-250),tex='-394\\ \\text{kJ}',size=21,anchor='start',fill=FIELD,halo=True))
    cx,cy,r=448,196,58; z=40
    s.append(C(200,e.Y(1),14,MUTED,1.5,'none','3 3')+L(213,e.Y(1)+5,cx-r+3,cy-12,MUTED,1.5,'3 3'))
    yd,yg=cy-z*0.7*1,cy+z*0.7*1
    s.append(C(cx,cy,r,MUTED,2,'#FFFFFF'))
    s.append(L(cx-44,yd,cx-4,yd,INK,3)+L(cx+4,yg,cx+44,yg,INK,3)+L(cx-4,yd,cx+44,yd,MUTED,1.5,'4 3'))
    s.append(an('draw',A(cx+24,yg-3,cx+24,yd+3,'ink',3),dur='.6',delay='1.4'))
    s.append(T(cx,cy+r+24,tex='+2\\ \\text{kJ}',size=21,weight=700)+T(cx,cy-r-10,mix='확대 ×40',size=18,fill=MUTED))
    return svg((520,410),480,'흑연과 다이아몬드의 연소 엔탈피 도표: 다이아몬드가 흑연보다 2 kJ 높다(확대 원)',s)
FIG['DIAM']=diam()

# ═════ 18 표 Ⅲ-2 표준 생성 엔탈피 막대 ═════
def bars():
    data=[('\\ce{NO2(g)}',34),('\\ce{NH3(g)}',-46),('\\ce{CH3OH(l)}',-239),('\\ce{C8H18(l)}',-250),('\\ce{H2O(l)}',-286),('\\ce{CO2(g)}',-394),('\\ce{Fe2O3(s)}',-826),('\\ce{Al2O3(s)}',-1676)]
    sc=0.25; SCALES['S18 표 Ⅲ-2 막대']=sc; x0=660; s=[]
    top=46; hh=38
    s.append(T(x0,30,mix='원소 = 0',size=22,fill=MUTED))
    for i,(tex,v) in enumerate(data):
        y=top+i*hh; x1=x0+min(v,0)*sc; w=abs(v)*sc
        col=PLUS if v>0 else MINUS
        s.append(T(150,y+24,tex=tex,size=22,anchor='end'))
        s.append(an('scale',R(x1,y+6,w,24,'none',0,col,0,extra='fill-opacity=".75"'),**{'from':'0,1','o':f'{x0},{y+18}','dur':'1','delay':f'{0.1*i:.1f}'}))
        lab=('+' if v>0 else '−')+str(abs(v))
        if v>0: s.append(T(x0+w+8,y+25,mix=lab,size=20,anchor='start',fill=PLUS,weight=700))
        else: s.append(T(x1-8,y+25,mix=lab,size=20,anchor='end',weight=700))
    s.append(L(x0,top-6,x0,top+8*hh+4,INK,2.5))
    s.append(T(400,top+8*hh+36,mix='$\\Delta H_\\mathrm{f}^\\circ$ (kJ/mol, 25 °C)',size=21,fill=MUTED))
    return svg((740,402),640,'표 Ⅲ-2 25 °C 표준 생성 엔탈피 막대그래프: 이산화 질소만 양수, 산화 알루미늄이 가장 작다',s)
FIG['BARS']=bars()

# ═════ 20 그림 Ⅲ-13 메테인 연소 경로(원자 모형) ═════
def ch4(x,y): return ''.join(atom(x+dx,y+dy,18,'H') for dx,dy in ((-30,-22),(30,-22),(-30,22),(30,22)))+atom(x,y,24,'C')
def o2(x,y): return atom(x-19,y,24,'O')+atom(x+19,y,24,'O')
def h2(x,y): return atom(x-13,y,18,'H')+atom(x+13,y,18,'H')
def co2(x,y): return atom(x-40,y,24,'O')+atom(x+40,y,24,'O')+atom(x,y,24,'C')
def h2o(x,y): return atom(x-26,y+18,18,'H')+atom(x+26,y+18,18,'H')+atom(x,y,24,'O')
def path():
    s=[]
    cols=((30,'반응물','#EFE9F6'),(410,'원소','#FFF4D6'),(790,'생성물','#EEF3DF'))
    for x,lab,bg in cols: s.append(R(x,40,240,290,'none',0,bg,12)+T(x+120,28,mix=lab,size=21,weight=700))
    s.append(ch4(150,110)+o2(150,240)+o2(150,300))
    el=atom(530,82,24,'C')+h2(500,150)+h2(560,150)+o2(530,240)+o2(530,300)
    s.append(an('move',el,**{'from':'-40,0','dur':'1.0','delay':'.2','ease':'out'}))
    pr=co2(910,110)+h2o(868,246)+h2o(956,246)
    s.append(an('move',pr,**{'from':'-40,0','dur':'1.0','delay':'1.0','ease':'out'}))
    # 화살표
    s.append(A(272,96,398,80,'ink',3)+A(272,124,398,150,'ink',3)+A(272,270,398,270,'ink',3))
    s.append(A(660,82,778,104,'ink',3)+A(660,150,778,236,'ink',3)+A(660,250,778,124,'ink',3)+A(660,282,778,252,'ink',3))
    s.append(T(335,358,mix='1단계',size=19,fill=MUTED)+T(720,362,mix='2단계',size=19,fill=MUTED))
    s.append(T(335,118,mix='(가)',size=20,weight=700,halo=True)+T(335,258,mix='(나)',size=20,weight=700,halo=True))
    s.append(T(720,74,mix='(다)',size=20,weight=700,halo=True)+T(720,300,mix='(라)',size=20,weight=700,halo=True))
    s.append('<g class="step" data-g="p1">'+T(335,190,tex='\\Delta H^\\circ_{(\\text{가})}=+75\\ \\text{kJ}',size=19,halo=True)+'</g>')
    s.append('<g class="step" data-g="p2">'+T(335,302,tex='\\Delta H^\\circ_{(\\text{나})}=0\\ \\text{kJ}',size=19,halo=True)+'</g>')
    s.append('<g class="step" data-g="p3">'+T(720,44,tex='\\Delta H^\\circ_{(\\text{다})}=-394\\ \\text{kJ}',size=19,halo=True)+'</g>')
    s.append('<g class="step" data-g="p4">'+T(720,332,tex='\\Delta H^\\circ_{(\\text{라})}=-572\\ \\text{kJ}',size=19,halo=True)+'</g>')
    return svg((1060,372),1060,'그림 Ⅲ-13 메테인 연소의 반응 경로: 반응물을 표준 상태 원소로 분해한 뒤 원소로부터 생성물을 만든다',s)
FIG['PATH']=path()

# ═════ 21 단계의 합 비율 도표 ═════
def pathd():
    e=EN(56,0.34,'S21 경로 도표'); s=[haxis(24,22,392)]
    s.append(e.lev(160,470,0,tex='\\mathrm{C}_\\text{흑연}+\\ce{2H2 + 2O2}\\ (\\text{원소})',dy=-12,lx=330))
    s.append(e.lev(40,200,-75,tex='\\ce{CH4 + 2O2}',dy=30,lx=110))
    s.append(e.lev(250,470,-394,tex='\\ce{CO2 + 2H2 + O2}',dy=-12,lx=380))
    s.append(e.lev(40,470,-966,tex='\\ce{CO2 + 2H2O(l)}',dy=30,lx=290))
    s.append(an('draw',e.arr(190,-75,0,'field',3,2),dur='.6'))
    s.append(T(182,e.Y(-37)+8,tex='+75',size=19,anchor='end',fill=FIELD))
    s.append(an('draw',e.arr(300,0,-394,'bfield',3),dur='.9',delay='.5'))
    s.append(T(310,e.Y(-200),tex='-394',size=19,anchor='start',fill=BF))
    s.append(an('draw',e.arr(430,-394,-966,'bfield',3),dur='1',delay='1.2'))
    s.append(T(422,e.Y(-680),tex='-572',size=19,anchor='end',fill=BF))
    s.append(an('draw',e.arr(80,-75,-966,'ink',4),dur='1.1',delay='2'))
    s.append(T(92,e.Y(-560),tex='\\Delta H^\\circ=-891\\ \\text{kJ}',size=21,anchor='start',halo=True,weight=700))
    return svg((490,430),470,'메테인 연소의 엔탈피 도표: 원소를 거치는 경로의 합이 −891 kJ',s)
FIG['PATHD']=pathd()

# ═════ 24 헤스 법칙 원자 모형 ═════
def no(x,y): return atom(x-17,y,24,'N')+atom(x+17,y,24,'O')
def no2(x,y): return atom(x-34,y+14,24,'O')+atom(x+34,y+14,24,'O')+atom(x,y-4,24,'N')
def n2(x,y): return atom(x-17,y,24,'N')+atom(x+17,y,24,'N')
def hessatoms():
    s=[]
    s.append(n2(60,70)+o2(165,70)+o2(270,70))
    s.append(A(326,70,372,70,'field',4))
    s.append(an('move',no(420,70)+no(510,70)+o2(610,70),**{'from':'-30,0','dur':'.9','delay':'.2','ease':'out'}))
    s.append(A(666,70,712,70,'bfield',4))
    s.append(an('move',no2(790,68)+no2(920,68),**{'from':'-30,0','dur':'.9','delay':'.9','ease':'out'}))
    s.append(T(165,128,tex='\\ce{N2 + 2O2}',size=20)+T(515,128,tex='\\ce{2NO + O2}',size=20)+T(855,128,tex='\\ce{2NO2}',size=20))
    return svg((990,140),960,'원자 수 보존: 질소 분자와 산소 분자 둘이 일산화 질소 둘과 산소를 거쳐 이산화 질소 둘이 된다',s)
FIG['HESSAT']=hessatoms()

# ═════ 25 그림 Ⅲ-14 헤스 법칙의 원리 ═════
def hess2():
    e=EN(330,1.30,'S25 그림 Ⅲ-14'); s=[haxis(24,30,350,'$H$ (kJ)')]
    s.append(e.lev(90,230,0,tex='\\ce{N2(g), 2O2(g)}',dy=30,lx=160))
    s.append(e.lev(110,270,180,tex='\\ce{O2(g), 2NO(g)}',lx=190))
    s.append(e.lev(220,360,68,tex='\\ce{2NO2(g)}',lx=300,dy=-12))
    s.append(L(230,e.Y(0),290,e.Y(0),MUTED,1.5,'5 4'))
    s.append(an('draw',e.arr(150,0,180,'field',4),dur='1'))
    s.append(T(142,e.Y(95),tex='\\Delta H_2=+180',size=20,anchor='end',fill=FIELD,halo=True))
    s.append(an('draw',e.arr(250,180,68,'bfield',4),dur='.9',delay='.8'))
    s.append(T(260,e.Y(140),tex='\\Delta H_3=-112',size=20,anchor='start',fill=BF))
    s.append(an('draw',e.arr(280,0,68,'ink',4),dur='.7',delay='1.6'))
    s.append(T(290,e.Y(30)+6,tex='\\Delta H_1',size=20,anchor='start'))
    s.append(T(190,22,mix='2단계 반응',size=21,weight=700,fill=MUTED))
    x=470
    s.append(e.lev(x,x+190,0,tex='\\ce{N2(g), 2O2(g)}',dy=30))
    s.append(e.lev(x,x+190,68,tex='\\ce{2NO2(g)}'))
    s.append(an('draw',e.arr(x+50,0,68,'ink',4),dur='.8',delay='2.2'))
    s.append(T(x+62,e.Y(34)+8,tex='\\Delta H_1=+68\\ \\text{kJ}',size=20,anchor='start',halo=True))
    s.append(T(x+95,e.Y(180)+20,mix='1단계 반응',size=21,weight=700,fill=MUTED))
    s.append(f'<g class="step" data-g="h1">'+T(x+95,e.Y(130),tex='=\\Delta H_2+\\Delta H_3',size=20)+T(x+95,e.Y(130)+30,tex='=180-112\\ \\text{(kJ)}',size=20)+'</g>')
    return svg((680,370),640,'그림 Ⅲ-14 헤스 법칙의 원리: 2단계 반응의 엔탈피 변화 합 +180 − 112와 1단계 반응의 +68 kJ이 같다',s)
FIG['HESS2']=hess2()

# ═════ 27 결합 엔탈피 경로 ═════
def bond():
    e=EN(292,0.075,'S27 결합 엔탈피'); s=[haxis(24,22,384)]
    s.append(e.lev(60,470,2648,tex='\\ce{C(g) + 4H(g) + 4O(g)}\\ (\\text{기체 원자})',lx=265))
    s.append(e.lev(40,250,0,tex='\\ce{CH4(g) + 2O2(g)}',dy=-12,lx=130))
    s.append(e.lev(220,470,-818,tex='\\ce{CO2(g) + 2H2O(g)}',dy=30,lx=345))
    s.append(L(250,e.Y(0),300,e.Y(0),MUTED,1.5,'5 4'))
    s.append(an('draw',e.arr(110,0,2648,'equi',4),dur='1.1'))
    s.append(T(122,e.Y(1500),mix='결합 끊기||$+2648\\ \\text{kJ}$',size=19,anchor='start',fill=EQUI))
    s.append(an('draw',e.arr(420,2648,-818,'minus',4),dur='1.2',delay='.9'))
    s.append(T(410,e.Y(1200),mix='결합 만들기||$-3466\\ \\text{kJ}$',size=19,anchor='end',fill=MINUS))
    s.append(an('draw',e.arr(280,0,-818,'ink',4),dur='.7',delay='2'))
    s.append(T(268,e.Y(-420)+8,tex='-818',size=20,anchor='end',weight=700,halo=True))
    return svg((490,398),470,'결합 엔탈피 경로: 반응물의 결합을 모두 끊어 기체 원자로 만든 뒤 생성물의 결합을 만든다',s)
FIG['BOND']=bond()

# ═════ 29 화학사 연표 ═════
def hist():
    s=[L(30,70,660,70,INK,2.4)]
    pts=[(90,'1783','얼음 열량계','라부아지에·라플라스',EQUI),(360,'1840','헤스 법칙 발표','반응열 체계적 측정',FIELD),(600,'오늘','열화학 반응식','표준 생성 엔탈피 표',INK)]
    for i,(x,y,a,b,col) in enumerate(pts):
        s.append(an('pop',C(x,70,11,col,2.6,'#FFFFFF'),o=f'{x},70',dur='.5',delay=f'{0.3*i:.1f}'))
        s.append(T(x,46,mix=y,size=21,weight=700)+T(x,108,mix=a,size=20)+T(x,136,mix=b,size=19,fill=MUTED))
    return svg((690,150),690,'열화학 연표: 1783 얼음 열량계, 1840 헤스 법칙',s)
FIG['HIST']=hist()

# ═════ 30 디지털 탐구 장치 ═════
def labset():
    s=[]
    s.append(f'<path d="M60 120 L240 120 L224 320 L76 320 Z" fill="#F3F5F8" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<path d="M78 130 L222 130 L210 308 L90 308 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<path d="M84 200 L216 200 L210 308 L90 308 Z" fill="{WATER}"/>')
    s.append(R(52,106,196,16,INK,2,'#E6EBF0',4))
    s.append(L(180,60,180,284,INK,4)+C(180,288,6,INK,1.5,INK))
    s.append(P([(180,60),(180,40),(300,40),(300,90)],INK,2))
    s.append(R(280,90,150,100,INK,2.5,'#FFFFFF',8))
    s.append(an('draw',P([(292,176),(316,176),(330,130),(346,120),(370,124),(418,132)],PLUS,3),dur='1.6',rep='loop'))
    s.append(T(355,214,mix='데이터 수집 장치',size=19))
    s.append(T(124,60,mix='온도 센서',size=19,anchor='middle'))
    s.append(T(150,352,mix='스타이로폼 컵 2겹 + 뚜껑',size=19))
    return svg((440,366),400,'디지털 탐구 장치: 뚜껑 덮은 2겹 스타이로폼 컵 열량계에 온도 센서를 꽂고 데이터 수집 장치로 기록',s)
FIG['LABSET']=labset()

# ═════ 31 보정 그래프 (실험실과 같은 모형, 실험 ③·뚜껑 덮음) ═════
def corr():
    T0=22.0; dT=0.0500*100.3*1000/(102*4.18)*0.98; tau=8; k=0.010
    fn=lambda t: T0 if t<30 else T0+dT*(1-math.exp(-(t-30)/tau))-k*(t-30)
    ax=Ax(64,250,380,210,180,36,ymin=20)
    s=[ax.frame([0,30,60,90,120,150,180],[20,24,28,32,36],T(452,300,mix='$t$ [s]',size=19,anchor='end',fill=MUTED),T(70,22,mix='$T$ [°C]',size=19,anchor='start',fill=MUTED),size=18)]
    s.append(an('draw',ax.curve(fn,0,180,240,PLUS,3),dur='1.6'))
    mx=max(fn(t/10) for t in range(1800)); tm=max(range(1800),key=lambda t:fn(t/10))/10
    s.append(f'<g class="step" data-g="c1">'+L(ax.X(30),ax.Y(T0+dT),ax.X(180),ax.Y(T0+dT-k*150),MUTED,2,'6 4')+C(ax.X(30),ax.Y(T0+dT),5,INK,1.5,FIELD)
             +T(ax.X(30)+10,ax.Y(T0+dT)-12,mix='보정한 최고 온도',size=18,anchor='start',fill=FIELD,weight=700)+'</g>')
    s.append(C(ax.X(tm),ax.Y(mx),5,INK,1.5,PLUS)+T(ax.X(tm)+8,ax.Y(mx)+26,mix='측정 최고 온도',size=18,anchor='start',fill=PLUS))
    s.append(L(ax.X(30),ax.Y(20),ax.X(30),ax.Y(23.6),OX,1.5,'4 3')+T(ax.X(30)+6,ax.Y(21.2),mix='혼합',size=18,anchor='start',fill=OX))
    return svg((470,310),440,'온도–시간 그래프: 냉각 구간을 혼합 시점까지 연장해 최고 온도를 보정한다',s),round(mx,2),round(T0+dT,2)
FIG['CORR'],_mx,_cr=corr(); print('보정 그래프 측정 최고',_mx,'보정',_cr)

# ═════ 36 연습 문제 3: 등온 가역 압축 ═════
def pv3():
    nRT=2.00*0.08206*300; V1=nRT/2.00; V2=V1/2
    ax=Ax(70,250,360,200,28,5)
    s=[ax.frame([0,7,14,21,28],[0,1,2,3,4,5],T(446,300,mix='$V$ [L]',size=19,anchor='end',fill=MUTED),T(76,30,mix='$P$ [atm]',size=19,anchor='start',fill=MUTED),size=18)]
    pts=[(ax.X(V2+(V1-V2)*i/80),ax.Y(nRT/(V2+(V1-V2)*i/80))) for i in range(81)]
    s.append(an('fade',P([(ax.X(V2),ax.Y(0))]+pts+[(ax.X(V1),ax.Y(0))],'none',0,FIELD,extra='fill-opacity=".2"',close=True),dur='1'))
    s.append(an('draw',ax.curve(lambda v:nRT/v,V2,V1,100,INK,3),dur='1.2'))
    s.append(A(ax.X(19),ax.Y(nRT/19),ax.X(17.6),ax.Y(nRT/17.6),'ink',3))
    s.append(C(ax.X(V1),ax.Y(2.0),6,INK,2,PLUS)+C(ax.X(V2),ax.Y(4.0),6,INK,2,PLUS))
    s.append(T(ax.X(V1)+4,ax.Y(2.0)+28,mix='처음 (24.6 L, 2.00 atm)',size=18,anchor='end',halo=True))
    s.append(T(ax.X(V2)+10,ax.Y(4.0)-8,mix='나중 (12.3 L, 4.00 atm)',size=18,anchor='start',halo=True))
    s.append(T(ax.X(18.4),ax.Y(0.6),mix='$w&gt;0$ (압축)',size=19,halo=True))
    return svg((460,310),430,'이산화 탄소 2.00 mol, 300 K 등온 가역 압축: 24.6 L에서 12.3 L로, 곡선 아래 넓이가 받은 일',s)
FIG['PV3']=pv3()

# ═════ 37 연습 문제 4: PCl5 ═════
def pcl():
    e=EN(52,0.55,'S37 연습 4'); s=[haxis(24,20,330)]
    s.append(e.lev(40,450,0,tex='\\ce{P(s) + 5/2Cl2(g)}\\ (\\text{원소})',lx=245))
    s.append(e.lev(150,450,-319.7,tex='\\ce{PCl3(l) + Cl2(g)}',lx=330,dy=-12))
    s.append(e.lev(40,450,-443.7,tex='\\ce{PCl5(s)}',dy=30,lx=245))
    s.append(an('draw',e.arr(200,0,-319.7,'field',4),dur='1'))
    s.append(T(212,e.Y(-160),tex='-319.7\\ \\text{kJ}',size=20,anchor='start',fill=FIELD,halo=True))
    s.append(an('draw',e.arr(400,-319.7,-443.7,'bfield',4),dur='.7',delay='.9'))
    s.append(T(390,e.Y(-382)+8,tex='-124\\ \\text{kJ}',size=20,anchor='end',fill=BF,halo=True))
    s.append(an('draw',e.arr(90,0,-443.7,'ink',4),dur='.9',delay='1.6'))
    s.append(f'<g class="step" data-g="pc">'+T(102,e.Y(-210),tex='-443.7\\ \\text{kJ}',size=20,anchor='start',weight=700,halo=True)+'</g>')
    return svg((470,336),440,'오염화 인의 표준 생성 엔탈피 도표: −319.7 kJ와 −124 kJ의 합',s)
FIG['PCL']=pcl()

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
print('scales px/kJ',SCALES); print('ok',len(out),'sections',out.count('<section'))
