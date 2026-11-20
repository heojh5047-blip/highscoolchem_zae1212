# -*- coding: utf-8 -*-
"""고급화학 3-2-1 엔트로피 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   labs_src.js·extra_src.css를 labs.js·extra.css로 복사한다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)"""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
OUT=BASE+'3-2-1_엔트로피/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-2-1_엔트로피/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT), OUT
FIG={}
SYSBG='#FFF4E8'; HOT='#FDE2E4'; COLD='#E3EEFB'; ICE='#D6ECFA'; ICE_S='#7FB3D5'
COIN='#F2C94C'; COIN_B='#E6DDC3'; SOLID='#8C99A6'; LIQ='#7FB3D5'
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def step(g,body): return f'<g class="step" data-g="{g}">{body}</g>'
def atom(x,y,r,el,lab=None):
    return f'<g data-atom="{f(x)},{f(y)},{r},{el}'+(f',{lab}' if lab else '')+'"></g>'
def spread(x,y,w,h,n,seed,r=10,gap=2.6):
    rnd=random.Random(seed); pts=[]; t=0
    while len(pts)<n and t<6000:
        t+=1; p=(rnd.uniform(x+r+4,x+w-r-4),rnd.uniform(y+r+4,y+h-r-4))
        if all(math.hypot(p[0]-a,p[1]-b)>gap*r for a,b in pts): pts.append(p)
    return pts
def jiggle(pts,seed,r=10,amp=5):
    rnd=random.Random(seed); s=[]
    for px,py in pts:
        th=rnd.uniform(0,6.283)
        s.append(an('move',gm(px,py,r),**{'from':f'{f(amp*math.cos(th))},{f(amp*math.sin(th))}','rep':'alt','dur':f(0.8+0.5*rnd.random()),'ease':'io'}))
    return ''.join(s)
def barrow(x,y0,dy,w,col,extra=''):
    """두꺼운 블록 화살표: (x,y0)에서 세로로 dy(위 음수)"""
    hd=min(abs(dy)*.45,w*1.1); sg=-1 if dy<0 else 1; y1=y0+dy; yb=y1-sg*hd
    pts=[(x-w/2,y0),(x-w/2,yb),(x-w*.95,yb),(x,y1),(x+w*.95,yb),(x+w/2,yb),(x+w/2,y0)]
    return P(pts,col,2,fill=col,extra='fill-opacity=".35" '+extra,close=True)
def heat(x1,y1,x2,y2,w=3): return A(x1,y1,x2,y2,'equi',w)
def beaker(x,y,w,h,lvl,fill=WATER):
    return (R(x+2,y+h-lvl,w-4,lvl-2,'none',0,fill)+L(x+2,y+h-lvl,x+w-2,y+h-lvl,WATER_S,1.5)
            +P([(x,y),(x,y+h),(x+w,y+h),(x+w,y)],GLASS,3))

# ═════ 1 표지: 칸막이를 열면 기체가 퍼진다 ═════
def cover():
    s=[]; X0,Y0,W,H=40,96,380,250
    s.append(R(X0,Y0,W,H,INK,3,'#FFFFFF',8))
    s.append(L(X0+W/2,Y0,X0+W/2,Y0+70,MUTED,3)+L(X0+W/2,Y0+H-70,X0+W/2,Y0+H,MUTED,3))
    s.append(L(X0+W/2,Y0+70,X0+W/2,Y0+H-70,MUTED,2,'6 6'))
    fin=spread(X0,Y0,W,H,14,7,r=11,gap=3.0); start=spread(X0,Y0,W/2-14,H,14,3,r=11,gap=2.4)
    for (fx,fy),(sx,sy) in zip(fin,start):
        s.append(an('move',gm(fx,fy,11),**{'from':f'{f(sx-fx)},{f(sy-fy)}','dur':'2.4','ease':'soft'}))
    s.append(T(X0+W/4,Y0-18,mix='처음: 왼쪽에만',size=20,fill=MUTED))
    s.append(T(X0+3*W/4,Y0-18,mix='칸막이를 열면',size=20,fill=MUTED))
    s.append(T(230,Y0+H+44,mix='미시 상태의 수 $W$ 증가',size=22,weight=700))
    s.append(T(230,Y0+H+78,mix='$S=k\\ln W$ 증가 → 저절로 퍼진다',size=22,fill=FIELD,weight=700))
    return svg((460,440),430,'칸막이를 열면 왼쪽에 모여 있던 기체 분자가 상자 전체로 퍼진다: 미시 상태의 수가 늘어 엔트로피가 증가한다',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 2 중단원 도입: 드라이아이스와 물 ═════
def mid():
    s=[]; x,y,w,h=120,110,240,200
    s.append(beaker(x,y,w,h,150))
    rnd=random.Random(5)
    for i,(dx,dy) in enumerate([(40,176),(92,184),(150,178),(196,186),(70,190)]):
        s.append(R(x+dx-16,y+dy-12,32,24,'#9AA7B5',1.5,'#F4F7FA',4))
    for i in range(9):
        bx=x+30+rnd.uniform(0,180); by=y+80+rnd.uniform(0,80); r=5+rnd.uniform(0,5)
        s.append(an('move',C(bx,by,r,WATER_S,1.5,'#FFFFFF'),**{'from':f'0,{f(60+rnd.uniform(0,30))}','rep':'loop','dur':f(1.4+rnd.random()*.8),'ease':'lin'}))
    for i,(cx,cy,r) in enumerate([(170,70,26),(205,58,30),(245,66,28),(280,74,22),(225,84,24)]):
        s.append(an('fade',C(cx,cy,r,'none',0,'#DDE3EA',extra='opacity=".85"'),dur='1.6',rep='alt',delay=f(i*.2)))
    s.append(T(240,34,tex='\\ce{CO2(s) -> CO2(g)}',size=22))
    s.append(T(120,96,mix='안개',size=19,fill=MUTED,anchor='end'))
    s.append(T(400,250,mix='드라이||아이스',size=19,fill=MUTED,anchor='start'))
    s.append(L(330,286,392,252,MUTED,1.5))
    return svg((480,330),440,'물에 넣은 드라이아이스에서 이산화 탄소 기포가 생기고 위에 안개가 낀다',s)
FIG['MID']=mid()

# ═════ 4 생각 열기: 얼음 녹음(흡열)과 철의 녹슮(발열) ═════
def opening():
    s=[]
    # (가) 얼음
    s.append(T(20,30,mix='(가) 얼음이 녹는다',size=21,anchor='start',weight=700))
    s.append(R(40,170,200,10,GLASS,2,'#EEF1F4',3))
    s.append(P([(70,170),(70,166),(210,166),(210,170)],WATER_S,1.5,fill=WATER,close=True))
    s.append(an('scale',R(105,96,70,70,ICE_S,2,ICE,6),**{'from':'1.25','o':'140,166','dur':'2.2','ease':'soft'}))
    s.append(heat(30,90,92,118)+heat(250,90,188,118))
    s.append(T(30,80,mix='열 흡수',size=19,anchor='start',fill=EQUI))
    s.append(T(300,96,mix='$\\Delta H&gt;0$',size=21,anchor='start')+T(300,128,mix='그래도 저절로',size=20,anchor='start',fill=FIELD,weight=700))
    s.append(T(300,156,mix='($25\\ {}^\\circ\\text{C}$의 방)',size=19,anchor='start',fill=MUTED))
    # (나) 철
    y=230
    s.append(T(20,y,mix='(나) 철이 녹슨다',size=21,anchor='start',weight=700))
    s.append(R(50,y+50,180,26,INK,2,'#B9C1CA',5)+P([(230,y+50),(256,y+63),(230,y+76)],INK,2,fill='#B9C1CA',close=True))
    for cx,cy,r in [(80,y+60,8),(122,y+68,10),(170,y+58,7),(205,y+67,8)]:
        s.append(an('fade',C(cx,cy,r,'none',0,'#B5541E',extra='opacity=".9"'),dur='1.8',delay=f((cx-80)/120)))
    s.append(heat(140,y+92,110,y+140)+heat(160,y+92,190,y+140))
    s.append(T(150,y+164,mix='열 방출',size=19,fill=EQUI))
    s.append(T(300,y+60,mix='$\\Delta H&lt;0$',size=21,anchor='start')+T(300,y+92,mix='저절로',size=20,anchor='start',fill=FIELD,weight=700))
    return svg((480,420),460,'얼음은 열을 흡수하면서도 저절로 녹고, 철은 열을 방출하면서 저절로 녹슨다',s)
FIG['OPEN']=opening()

# ═════ 5 자발성: 언덕의 공 ═════
def spon():
    s=[]; pts=[(30,90)]
    for i in range(1,61):
        x=30+i*7; y=90+150*(1-math.cos(math.pi*min(i/50,1)))/2; pts.append((x,y))
    s.append(P(pts+[(450,240),(450,290),(30,290)],'none',0,'#E8EDF2',close=True)+P(pts+[(450,240)],INK,3))
    s.append(an('move',C(420,222,18,INK,2,PLUS),**{'from':'-370,-150','dur':'1.8','ease':'in'}))
    s.append(C(52,72,18,MUTED,1.5,'none','4 3'))
    s.append(A(130,92,250,182,'field',4)+T(212,118,mix='저절로',size=21,fill=FIELD,weight=700,anchor='start'))
    s.append(A(330,262,160,170,'muted',3,True))
    s.append(L(232,198,262,228,PLUS,4)+L(262,198,232,228,PLUS,4))
    s.append(T(250,284,mix='저절로 올라가지 않는다',size=20,fill=MUTED))
    return svg((470,300),460,'언덕 위의 공은 저절로 굴러 내려오지만 저절로 다시 올라가지는 않는다',s)
FIG['SPON']=spon()

# ═════ 6 엔트로피: 모여 있음 → 퍼져 있음 ═════
def ent():
    s=[]
    s.append(R(10,40,200,200,INK,2.5,'#FFFFFF',6)+R(270,40,200,200,INK,2.5,'#FFFFFF',6))
    for i in range(3):
        for j in range(3): s.append(gm(32+i*24,62+j*24,10))
    s.append(jiggle(spread(270,40,200,200,9,11,r=10,gap=3.2),4))
    s.append(A(218,140,262,140,'ink',4))
    s.append(T(110,28,mix='모여 있음',size=21,weight=700)+T(370,28,mix='퍼져 있음',size=21,weight=700))
    s.append(T(110,272,mix='낮은 엔트로피',size=20,fill=MUTED)+T(370,272,mix='높은 엔트로피',size=20,fill=FIELD,weight=700))
    s.append(T(240,312,mix='자발적 변화의 방향 →',size=20))
    return svg((480,326),460,'입자가 한쪽에 모여 있는 낮은 엔트로피 상태에서 퍼져 있는 높은 엔트로피 상태로 저절로 변한다',s)
FIG['ENT']=ent()

# ═════ 7 금속의 냉각 (그림 Ⅲ-16을 새로 그림) ═════
def metal():
    s=[]
    def block(x,y,fill,hot):
        o=R(x,y,190,120,INK,2.5,fill,8)
        for i in range(5):
            for j in range(3):
                cx,cy=x+27+i*34,y+28+j*32
                b=C(cx,cy,11,'#6B7785',1.5,'#B9C1CA')
                o+=an('move',b,**{'from':'3,0' if (i+j)%2 else '-3,0','rep':'swing','dur':'.12' if hot else '.5','ease':'sine'}) if hot else b
        return o
    s.append(block(40,40,HOT,True)+T(135,30,mix='뜨거운 금속',size=20,weight=700))
    for (x1,y1,x2,y2) in [(240,70,300,50),(240,110,306,110),(240,150,300,170),(30,110,4,110)]:
        s.append(heat(x1,y1,x2,y2))
    s.append(T(310,116,mix='열이 주위로 퍼짐',size=19,anchor='start',fill=EQUI))
    s.append(block(40,290,COLD,False)+T(135,436,mix='냉각된 금속',size=20,weight=700))
    s.append(A(110,176,110,280,'field',5)+T(98,232,mix='자발적',size=20,anchor='end',fill=FIELD,weight=700))
    s.append(A(170,280,170,176,'muted',3,True)+L(156,216,184,244,PLUS,4)+L(184,216,156,244,PLUS,4))
    s.append(T(196,232,mix='비자발적',size=20,anchor='start',fill=MUTED,weight=700))
    return svg((480,452),440,'뜨거운 금속은 에너지가 주위로 퍼지며 저절로 냉각되지만, 냉각된 금속이 저절로 뜨거워지지는 않는다',s)
FIG['METAL']=metal()

# ═════ 8 열역학 제2법칙: 고립계 = 계 + 주위 ═════
def law2():
    s=[]
    s.append(R(20,40,440,320,INK,3,'#F7F8FA',24)+R(32,52,416,296,MUTED,1.5,'none',18,'7 5'))
    s.append(T(240,30,mix='우주 = 계 + 주위 (고립계)',size=21,weight=700))
    s.append(beaker(170,150,140,150,110,SYSBG))
    s.append(R(172,192,136,106,INK,3,'none',4))
    s.append(T(240,250,mix='계',size=24,weight=700))
    s.append(T(90,110,mix='주위',size=22,fill=MUTED,weight=700))
    for (x1,y1,x2,y2) in [(166,230,96,230),(314,230,384,230),(240,146,240,90)]:
        s.append(an('draw',heat(x1,y1,x2,y2),dur='.9'))
    s.append(T(390,212,mix='열',size=19,fill=EQUI))
    s.append(T(240,334,mix='단열·밀봉 → 물질도 에너지도 드나들지 않음',size=19,fill=MUTED))
    return svg((480,370),460,'단열되고 밀봉된 용기 속 계와 주위를 합한 고립계(우주)',s)
FIG['LAW2']=law2()

# ═════ 9 ΔS = q/T: 같은 열, 다른 온도 ═════
def qt():
    s=[]
    for i,(T_,fill,lab) in enumerate([(300,COLD,'차가운 계 $300\\ \\text{K}$'),(600,HOT,'뜨거운 계 $600\\ \\text{K}$')]):
        x=40+i*230
        s.append(R(x,40,170,90,INK,3,fill,8)+T(x+85,92,mix=lab,size=19))
        s.append(heat(x+85,0+6,x+85,36))
        s.append(T(x+97,24,mix='$q=1000\\ \\text{J}$',size=21,anchor='start',fill=EQUI))
        ds=1000/T_; hgt=ds*48
        s.append(an('scale',R(x+55,330-hgt,60,hgt,FIELD,2,FIELD,3,extra='fill-opacity=".35"'),**{'from':'1,0','o':f'{x+85},330','dur':'1.1'}))
        s.append(T(x+85,320-hgt,tex=f'+{ds:.2f}\\ \\text{{J/K}}',size=20,weight=700))
    s.append(L(20,330,460,330,MUTED,2)+T(20,360,mix='$\\Delta S$ 막대 (높이 ∝ 값)',size=21,anchor='start',fill=MUTED))
    return svg((480,370),410,'같은 열 1000 J이 들어갈 때 300 K의 계는 3.33 J/K, 600 K의 계는 1.67 J/K만큼 엔트로피가 증가한다',s)
FIG['QT']=qt()

# ═════ 10 온도와 엔트로피: ΔS = C ln(T2/T1) ═════
def heatfig():
    C_=75.3; ax=Ax(78,290,360,240,400,25,xmin=290,ymin=0)
    s=[ax.frame([300,325,350,375,400],[0,5,10,15,20,25],T(446,262,mix='$T_2$ [K]',size=19,anchor='end',fill=MUTED),T(84,34,mix='$\\Delta S$ [J/K]',size=19,anchor='start',fill=MUTED))]
    s.append(an('draw',ax.curve(lambda t:C_*math.log(t/298),298,400,120,INK,3),dur='1.4'))
    v=C_*math.log(348/298)
    s.append(step('h1',L(ax.X(348),ax.Y(0),ax.X(348),ax.Y(v),MUTED,1.5,'5 4')+L(ax.X(298),ax.Y(v),ax.X(348),ax.Y(v),MUTED,1.5,'5 4')
             +C(ax.X(348),ax.Y(v),6,INK,2,PLUS)+T(ax.X(348)+12,ax.Y(v)+26,mix='$348\\ \\text{K}$: $+11.7\\ \\text{J/K}$',size=19,anchor='start',halo=True)))
    s.append(T(ax.X(330),ax.Y(21),mix='물 $1\\ \\text{mol}$, $T_1=298\\ \\text{K}$',size=19,halo=True))
    return svg((470,340),440,'물 1 mol을 298 K에서 가열할 때 나중 온도에 따른 엔트로피 변화 곡선',s)
FIG['HEAT']=heatfig()

# ═════ 11 부피와 엔트로피: 등온 가역 팽창 ═════
def volfig():
    s=[]
    def cyl(x,top,label,pts):
        o=P([(x,40),(x,300),(x+170,300),(x+170,40)],INK,3)
        o+=R(x+3,top,164,300-top-2,'none',0,'#FFFFFF')
        o+=R(x+2,top-16,166,16,INK,2,'#C9D2DB',3)
        o+=''.join(gm(px,py,9) for px,py in pts)
        o+=T(x+85,330,mix=label,size=20)
        return o
    p1=spread(43,222,164,76,8,2,r=9,gap=2.4); s.append(cyl(40,220,'$V_1$',p1))
    p2=spread(273,122,164,176,8,9,r=9,gap=3.0)
    s.append(an('move',R(272,104,166,16,INK,2,'#C9D2DB',3),**{'from':'0,100','dur':'1.6','ease':'soft'}))
    s.append(cyl(270,120,'$V_2=2V_1$',[]).replace(R(272,104,166,16,INK,2,'#C9D2DB',3),''))
    s.append(jiggle(p2,6,r=9,amp=4))
    s.append(A(355,96,355,52,'ink',5)+T(368,62,mix='일',size=19,anchor='start',weight=700))
    s.append(heat(250,262,282,262)+heat(462,262,430,262)+T(240,324,mix='열 흡수',size=18,fill=EQUI))
    s.append(A(222,200,256,200,'ink',3))
    s.append(T(245,24,mix='온도 일정',size=20,fill=MUTED))
    return svg((480,345),450,'이상 기체가 온도가 일정하게 열을 흡수하며 부피가 2배로 팽창한다: 분자가 머무를 공간이 넓어진다',s)
FIG['VOL']=volfig()

# ═════ 12 예제 Ⅲ-5 ═════
def ex5():
    s=[]
    s.append(R(10,60,120,120,INK,2.5,'#FFFFFF',6)+R(190,60,240,120,INK,2.5,'#FFFFFF',6))
    s.append(''.join(gm(px,py,8) for px,py in spread(10,60,120,120,7,4,r=8,gap=2.6)))
    s.append(jiggle(spread(190,60,240,120,7,8,r=8,gap=3.2),3,r=8,amp=4))
    s.append(A(138,120,182,120,'ink',3))
    s.append(T(70,44,mix='$22.0\\ \\text{L}$',size=20)+T(310,44,mix='$44.0\\ \\text{L}$',size=20))
    s.append(T(220,212,mix='$\\ce{N2}$ $1.00\\ \\text{mol}$, 등온',size=19,fill=MUTED))
    return svg((440,224),400,'질소 1.00 mol이 22.0 L에서 44.0 L로 등온 팽창한다',s)
FIG['EX5']=ex5()

# ═════ 14 제3법칙: 완전 결정 ═════
def cryst():
    s=[]
    def grid(x,y,hot):
        o=R(x,y,190,190,INK,2.5,COLD if not hot else HOT,8)
        rnd=random.Random(3)
        for i in range(4):
            for j in range(4):
                cx,cy=x+35+i*40,y+35+j*40
                if hot:
                    dx,dy=rnd.uniform(-4,4),rnd.uniform(-4,4)
                    o+=an('move',C(cx+dx,cy+dy,13,'#6B7785',1.5,'#B9C1CA'),**{'from':f'{f(-2*dx)},{f(-2*dy)}','rep':'swing','dur':f(.25+.1*rnd.random()),'ease':'sine'})
                else: o+=C(cx,cy,13,'#6B7785',1.5,'#B9C1CA')
        return o
    s.append(grid(20,50,False)+grid(270,50,True))
    s.append(T(115,36,mix='$0\\ \\text{K}$ 완전 결정',size=20,weight=700)+T(365,36,mix='$T&gt;0\\ \\text{K}$',size=20,weight=700))
    s.append(T(115,272,mix='배열 1가지',size=19,fill=MUTED)+T(115,302,mix='$S=0$',size=22,weight=700))
    s.append(T(365,272,mix='진동 → 배열 여러 가지',size=19,fill=MUTED)+T(365,302,mix='$S&gt;0$',size=22,weight=700,fill=FIELD))
    s.append(A(222,145,262,145,'ink',3)+T(242,132,mix='가열',size=18,fill=MUTED))
    return svg((480,316),460,'0 K의 완전 결정은 배열이 1가지라 엔트로피가 0이고, 온도가 오르면 원자가 진동하여 엔트로피가 0보다 크다',s)
FIG['CRYST']=cryst()

# ═════ 15 볼츠만의 비문 ═════
def stone():
    s=[]
    s.append(P([(90,380),(90,140),(110,90),(150,60),(240,48),(330,60),(370,90),(390,140),(390,380)],'#6B7785',3,fill='#D5DAE0',close=True))
    s.append(R(60,380,360,26,'#6B7785',2.5,'#C3C9D1',4))
    s.append(C(240,150,46,'#6B7785',2,'#C3C9D1')+P([(180,250),(196,206),(240,196),(284,206),(300,250)],'#6B7785',2,fill='#C3C9D1',close=True))
    s.append(T(240,300,mix='볼츠만',size=24,weight=700))
    s.append(an('fade',R(130,318,220,48,INK,2,'#FFFFFF',6),dur='1'))
    s.append(T(240,352,tex='S=k\\ln W',size=28,weight=700))
    s.append(T(240,438,mix='비문에 새겨진 볼츠만 식',size=22,fill=MUTED))
    return svg((480,450),400,'볼츠만의 묘비에 새겨진 엔트로피 식 S = k ln W',s)
FIG['STONE']=stone()

# ═════ 16 동전 모형: 미시 상태 세기 ═════
def coins():
    s=[]; r=17
    def coin(x,y,front):
        return C(x,y,r,'#9C7A1E',2,COIN if front else COIN_B)+T(x,y+6.5,mix='앞' if front else '뒤',size=18)
    def group(x,y,bits):
        o=R(x-r-5,y-r-5,len(bits)*2*r+(len(bits)-1)*4+10,2*r+10,MUTED,1.2,'#FFFFFF',8)
        for i,b in enumerate(bits): o+=coin(x+i*(2*r+4),y,b=='0')
        return o
    rows=[(1,'c1',[(0,)],50)]
    data={1:['0','1'],2:['00','01','10','11'],3:['000','001','010','011','100','101','110','111']}
    ys={1:46,2:126,3:206}
    for N in (1,2,3):
        g=f'c{N}'; o=T(10,ys[N]+7,mix=f'동전 {N}개',size=20,anchor='start',weight=700)
        for k,bits in enumerate(data[N]):
            if N<3: x=130+k*(len(bits)*38+26); y=ys[N]
            else: x=130+(k%4)*124; y=ys[N]+(k//4)*58
            o+=group(x,y,bits)
        wy=ys[N]+7 if N<3 else ys[N]+36
        o+=T(684,wy,mix=f'$W={2**N}$',size=22,anchor='end',weight=700,fill=FIELD)
        s.append(step(g,o))
    return svg((690,300),680,'동전 1개, 2개, 3개의 앞뒤 배열: 미시 상태의 수가 2, 4, 8가지',s)
FIG['COINS']=coins()

# ═════ 17 아보가드로수 동전 ↔ 부피 2배 ═════
def mole():
    s=[]
    s.append(R(30,40,420,170,INK,2.5,'#FFFFFF',6)+L(240,40,240,210,MUTED,2,'6 5'))
    pts=[(80,90),(150,160),(190,80),(300,150),(360,80),(410,170)]
    for i,(x,y) in enumerate(pts):
        s.append(an('move',gm(x,y,14)+T(x,y+6,tex=str(i+1),size=18),**{'from':('6,0' if i%2 else '-6,0'),'rep':'alt','dur':f(.9+.1*i),'ease':'io'}))
    s.append(T(135,32,mix='왼쪽',size=19,fill=MUTED)+T(345,32,mix='오른쪽',size=19,fill=MUTED))
    s.append(T(240,246,mix='분자 하나마다 자리 2가지',size=20,weight=700))
    s.append(T(240,278,mix='→ $N$개이면 $W$가 $2^N$배',size=20))
    s.append(C(150,330,18,'#9C7A1E',2,COIN)+T(150,336.5,mix='앞',size=18)+C(196,330,18,'#9C7A1E',2,COIN_B)+T(196,336.5,mix='뒤',size=18))
    s.append(T(230,337,mix='동전 하나도 2가지',size=19,anchor='start',fill=MUTED))
    return svg((480,360),450,'부피가 2배가 되면 분자 하나마다 왼쪽과 오른쪽 두 자리를 가져 동전의 앞뒤처럼 미시 상태가 2배씩 는다',s)
FIG['MOLE']=mole()

# ═════ 18 예제 Ⅲ-6: CO 분자 4개의 배열 16가지 ═════
def co16():
    s=[]; pw,ph=116,84; r=10
    for k in range(16):
        px=8+(k%4)*(pw+6); py=8+(k//4)*(ph+6)
        s.append(R(px,py,pw,ph,'#B89B2E',1.5,'#FFF8DC',4))
        for m in range(4):
            bit=(k>>(3-m))&1; cx=px+30+(m%2)*56; cy=py+24+(m//2)*36
            c1,c2=(cx-r,cx+r) if bit==0 else (cx+r,cx-r)
            s.append(atom(c1,cy,r,'C','-')+atom(c2,cy,r,'O','-'))
    s.append(step('co1',R(5,5,pw+6,ph+6,PLUS,3.5,'none',6)))
    s.append(atom(150,394,r,'C','-')+T(166,401,mix='C',size=18,anchor='start')+atom(220,394,r,'O','-')+T(236,401,mix='O',size=18,anchor='start'))
    s.append(T(300,401,mix='$W=2^4=16$',size=20,anchor='start',weight=700))
    return svg((500,412),470,'일산화 탄소 분자 4개가 나란히 놓일 때 분자마다 두 방향이 있어 배열이 16가지',s)
FIG['CO16']=co16()

# ═════ 19 실험실 설계 그림 ═════
def plan():
    s=[]; cw=70
    s.append(R(20,30,4*cw,cw,INK,2.5,'#FFFFFF',4))
    for i in range(1,4): s.append(L(20+i*cw,30,20+i*cw,30+cw,'#C9D2DB',1.5))
    s.append(L(20+2*cw,22,20+2*cw,38+cw,PLUS,3,'7 5'))
    for i,(x,y) in enumerate([(40,52),(72,80),(108,50),(140,82)]):
        s.append(gm(x,y,12)+T(x,y+6,tex=str(i+1),size=18))
    s.append(T(20+cw,130,mix='왼쪽 $a=2$칸',size=19)+T(20+3*cw,130,mix='오른쪽 $b=2$칸',size=19))
    s.append(T(20+2*cw,18,mix='칸막이',size=18,fill=PLUS))
    return svg((320,145),320,'왼쪽 2칸에 번호 붙은 입자 4개가 있고 칸막이 너머 오른쪽 2칸이 비어 있다',s)
FIG['PLAN']=plan()

# ═════ 22 상전이에 따른 엔트로피 (그림 Ⅲ-19를 새로 그림) ═════
def phase():
    s=[]; X0,Y0=70,300
    s.append(A(X0,Y0,X0,30,'muted',2)+A(X0,Y0,460,Y0,'muted',2))
    s.append(T(X0+8,44,mix='엔트로피 $S$',size=21,anchor='start',fill=MUTED)+T(458,Y0+44,mix='절대 온도 $T$',size=21,anchor='end',fill=MUTED))
    s.append(T(X0-8,Y0+26,tex='0',size=20,anchor='end'))
    Tf,Tb=190,330
    sol=[(X0+i*(Tf-X0)/40,Y0-60*((i/40)**0.7)) for i in range(41)]
    liq=[(Tf+i*(Tb-Tf)/30,Y0-110-30*(i/30)) for i in range(31)]
    gas=[(Tb+i*(440-Tb)/30,Y0-235-25*(i/30)) for i in range(31)]
    s.append(an('draw',P(sol,INK,3),dur='.8'))
    s.append(an('draw',P([(Tf,Y0-60),(Tf,Y0-110)],INK,3)+P(liq,INK,3),dur='.7',delay='.7'))
    s.append(an('draw',P([(Tb,Y0-140),(Tb,Y0-235)],INK,3)+P(gas,INK,3),dur='.7',delay='1.3'))
    for x,lab in ((Tf,'T_\\mathrm{f}'),(Tb,'T_\\mathrm{b}')):
        s.append(L(x,Y0,x,Y0-60 if x==Tf else Y0-140,MUTED,1.5,'5 4')+T(x,Y0+28,tex=lab,size=21))
    s.append(T(Tf,Y0+52,mix='녹는점',size=20,fill=MUTED)+T(Tb,Y0+52,mix='끓는점',size=20,fill=MUTED))
    s.append(T(130,Y0-70,mix='고체',size=20)+T(258,Y0-150,mix='액체',size=20)+T(390,Y0-272,mix='기체',size=20))
    s.append(T(Tf+10,Y0-80,tex='\\Delta S^\\circ_{\\text{용융}}',size=20,anchor='start',fill=EQUI))
    s.append(T(Tb+10,Y0-184,tex='\\Delta S^\\circ_{\\text{증발}}',size=20,anchor='start',fill=EQUI))
    return svg((480,366),420,'0 K부터 가열할 때 엔트로피는 온도에 따라 늘고 녹는점과 끓는점에서 갑자기 커진다',s)
FIG['PHASE']=phase()

# ═════ 25 표준 몰 엔트로피 막대 ═════
def smbar():
    s=[]; data=[('기체',GAS,[('\\ce{CO2}',213.7),('\\ce{O2}',205.1),('\\ce{N2}',191.6),('\\ce{H2}',130.7)]),
               ('액체',LIQ,[('\\ce{C8H18}',358.0),('\\ce{C2H5OH}',160.7),('\\ce{CH3OH}',127.0),('\\ce{H2O}',69.9)]),
               ('고체',SOLID,[('\\ce{CaCO3}',92.9),('\\ce{NaCl}',72.1),('\\text{흑연}',5.7),('\\text{다이아몬드}',2.4)])]
    X0=150; sc=0.80; y=20
    for gi,(nm,col,items) in enumerate(data):
        s.append(T(8,y+20,mix=nm,size=20,anchor='start',weight=700))
        y+=8
        for lab,v in items:
            y+=30
            s.append(T(X0-8,y+7,tex=lab,size=18,anchor='end'))
            s.append(an('scale',R(X0,y-11,v*sc,22,col,1.5,col,3,extra='fill-opacity=".55"'),**{'from':'0,1','o':f'{X0},{y}','dur':'1','delay':f(gi*.3)}))
            s.append(T(X0+v*sc+8,y+7,tex=f'{v:.1f}',size=18,anchor='start'))
        y+=20
    s.append(L(X0,22,X0,y-12,MUTED,2))
    s.append(T(480,y+8,mix='$S^\\circ_\\mathrm{m}$ [J/(K·mol)]',size=18,anchor='end',fill=MUTED))
    return svg((490,y+18),470,'표 Ⅲ-3의 표준 몰 엔트로피 막대: 기체가 크고, 액체는 분자가 복잡할수록 크며, 고체가 작다',s)
FIG['SMBAR']=smbar()

# ═════ 26 기체 몰수와 ΔS 부호 ═════
def gasn():
    s=[]
    def box(x,y,n,seed,block=False):
        o=R(x,y,130,100,INK,2,'#FFFFFF',6)
        if block: o+=R(x+40,y+66,50,30,'#6B7785',1.5,'#B9C1CA',3)
        o+=''.join(gm(px,py,10) for px,py in spread(x,y,130,62 if block else 100,n,seed,r=10,gap=2.8))
        return o
    s.append(box(10,20,6,1)+A(150,70,200,70,'ink',3)+box(210,20,4,2))
    s.append(T(360,64,mix='기체 몰수 감소',size=19,anchor='start')+T(360,94,mix='$\\Delta S&lt;0$',size=21,anchor='start',weight=700))
    s.append(box(10,150,0,3,True)+A(150,200,200,200,'ink',3)+box(210,150,3,4,True))
    s.append(T(360,194,mix='기체 생성',size=19,anchor='start')+T(360,224,mix='$\\Delta S&gt;0$',size=21,anchor='start',weight=700,fill=FIELD))
    return svg((480,262),450,'기체 분자 수가 줄면 엔트로피가 감소하고, 고체에서 기체가 생기면 엔트로피가 증가한다',s)
FIG['GASN']=gasn()

# ═════ 27 예제 Ⅲ-7: 암모니아 생성 ═════
def nh3():
    s=[]; rN,rH=19,13
    s.append(R(6,30,196,170,INK,2,'#FFFFFF',6)+R(254,30,196,170,INK,2,'#FFFFFF',6))
    def n2(x,y): return atom(x-15,y,rN,'N','-')+atom(x+15,y,rN,'N','-')
    def h2(x,y): return atom(x-10,y,rH,'H','-')+atom(x+10,y,rH,'H','-')
    s.append(n2(60,70)+h2(150,70)+h2(56,150)+h2(150,150))
    def nh(x,y):
        o=''
        for a in (210,330,90): o+=atom(x+26*math.cos(math.radians(a)),y+26*math.sin(math.radians(a)),rH,'H','-')
        return o+atom(x,y,rN,'N','-')
    s.append(an('fade',nh(305,96)+nh(400,140),dur='1.2'))
    s.append(A(208,115,248,115,'ink',3))
    s.append(T(104,22,mix='반응 전: 기체 4 mol',size=19)+T(352,22,mix='반응 후: 기체 2 mol',size=19))
    s.append(atom(130,228,rN,'N','-')+T(156,235,mix='N',size=18,anchor='start')+atom(220,228,rH,'H','-')+T(240,235,mix='H',size=18,anchor='start'))
    s.append(T(300,235,mix='N 2 = 2, H 6 = 6',size=18,anchor='start',fill=MUTED))
    return svg((456,250),440,'질소 1분자와 수소 3분자가 암모니아 2분자가 되어 기체 분자 수가 4에서 2로 줄어든다',s)
FIG['NH3']=nh3()

# ═════ 30 전체 엔트로피 = 계 + 주위 ═════
def total():
    s=[]; base=190
    s.append(L(20,base,460,base,MUTED,2,'5 4')+T(20,base+26,mix='0',size=18,anchor='start',fill=MUTED))
    s.append(an('draw',barrow(100,base,60,46,BF),dur='.8'))
    s.append(an('draw',barrow(240,base,-150,46,RD),dur='.9',delay='.6'))
    s.append(an('draw',barrow(380,base,-90,46,FIELD),dur='.9',delay='1.3'))
    s.append(T(100,base+86,tex='\\Delta S&lt;0',size=20)+T(100,base+112,mix='계',size=19,fill=BF,weight=700))
    s.append(T(240,base-160,tex='\\Delta S_\\text{주위}&gt;0',size=20)+T(240,base+30,mix='주위',size=19,fill=RD,weight=700))
    s.append(T(380,base-100,tex='\\Delta S_\\text{전체}&gt;0',size=20)+T(380,base+30,mix='전체',size=19,fill=FIELD,weight=700))
    s.append(T(170,base-40,tex='+',size=28)+T(310,base-40,tex='=',size=28))
    return svg((480,320),440,'계의 엔트로피가 감소해도 주위의 엔트로피가 더 크게 증가하면 전체 엔트로피는 증가한다',s)
FIG['TOTAL']=total()

# ═════ 31 물이 얼 때 ═════
def freeze():
    s=[]
    s.append(R(10,30,460,330,MUTED,1.5,COLD,14)+T(30,58,mix='주위 $-10\\ {}^\\circ\\text{C}$',size=19,anchor='start',fill=MUTED))
    s.append(beaker(150,110,150,170,120))
    for (x,y,w,h) in [(170,232,40,30),(218,240,34,24),(258,228,30,34),(186,200,30,26),(240,206,36,24)]:
        s.append(an('fade',R(x,y,w,h,ICE_S,2,ICE,4),dur='1.4',delay=f((x-170)/100)))
    for (x1,y1,x2,y2) in [(146,200,90,200),(304,200,360,200)]:
        s.append(heat(x1,y1,x2,y2))
    s.append(T(380,206,mix='열 방출',size=19,anchor='start',fill=EQUI))
    s.append(barrow(70,330,-60,30,RD)+T(108,300,tex='\\Delta S_\\text{주위}',size=18,anchor='start'))
    s.append(barrow(400,270,50,30,BF)+T(430,342,tex='\\Delta S',size=18,anchor='end'))
    s.append(T(225,94,tex='\\ce{H2O(l) -> H2O(s)}',size=19,halo=True))
    return svg((480,370),450,'영하의 주위에서 물이 얼 때 계의 엔트로피는 줄고 방출한 열로 주위의 엔트로피는 는다',s)
FIG['FREEZE']=freeze()

# ═════ 32 주위의 엔트로피 ═════
def surr():
    s=[]
    s.append(R(10,20,460,300,MUTED,1.5,'#F3F6F9',14))
    s.append(T(30,54,mix='주위: 매우 큼, 온도 $T$ 일정',size=22,anchor='start',fill=MUTED))
    s.append(R(170,120,140,110,INK,3,SYSBG,8)+T(240,168,mix='계',size=22,weight=700)+T(240,206,tex='\\Delta H&lt;0',size=22))
    for (x1,y1,x2,y2) in [(164,175,90,175),(316,175,390,175),(240,236,240,290)]:
        s.append(an('draw',heat(x1,y1,x2,y2),dur='.8'))
    s.append(T(408,158,tex='q_\\text{주위}=-\\Delta H',size=22,anchor='end',fill=EQUI))
    s.append(thermo(430,70,140,90))
    return svg((480,330),420,'일정 압력에서 계가 방출한 열은 온도가 일정한 큰 주위로 들어가 주위가 받은 열은 −ΔH이다',s)
def thermo(x,top,bot,lvl,col=PLUS):
    return (R(x-5,top,10,bot-top,INK,1.5,'#FFFFFF',5)+C(x,bot+6,9,INK,1.5,col)+R(x-2.5,lvl,5,bot-lvl+4,'none',0,col))
FIG['SURR']=surr()

# ═════ 33 물이 어는 과정 그래프 ═════
def frzg():
    ax=Ax(80,286,350,230,295,24.0,xmin=255,ymin=20.5)
    s=[ax.frame([255,265,275,285,295],[21,22,23,24],T(446,258,mix='$T$ [K]',size=19,anchor='end',fill=MUTED),T(86,36,mix='[J/(K·mol)]',size=19,anchor='start',fill=MUTED),xfmt=lambda v:str(v),yfmt=lambda v:f'{v:.0f}')]
    s.append(an('draw',ax.curve(lambda t:6010/t,255,295,100,RD,3),dur='1.2'))
    s.append(L(ax.X(255),ax.Y(22.0),ax.X(295),ax.Y(22.0),BF,3,'8 5'))
    s.append(T(ax.X(294),ax.Y(22.0)+26,mix='$-\\Delta S=22.0$',size=18,anchor='end',fill=BF,halo=True))
    s.append(T(ax.X(262),ax.Y(23.4),tex='\\Delta S_\\text{주위}',size=19,anchor='start',fill=RD,halo=True))
    s.append(L(ax.X(273.15),ax.Y(20.5),ax.X(273.15),ax.Y(24),MUTED,1.5,'4 4'))
    s.append(C(ax.X(273.15),ax.Y(22.0),6,INK,2,'#FFFFFF'))
    s.append(T(ax.X(264),ax.Y(20.9),mix='얼음 자발',size=18,fill=FIELD,halo=True))
    s.append(T(ax.X(284),ax.Y(20.9),mix='녹음 자발',size=18,fill=FIELD,halo=True))
    for t,g in ((263.15,'f1'),(283.15,'f3')):
        s.append(step(g,C(ax.X(t),ax.Y(6010/t),6,INK,2,PLUS)))
    s.append(step('f2',T(ax.X(273.15)+8,ax.Y(23.7),mix='평형 $273.15\\ \\text{K}$',size=18,anchor='start',halo=True)))
    return svg((470,340),450,'물이 얼 때 주위의 엔트로피 증가 곡선과 계의 엔트로피 감소 크기 22.0이 273.15 K에서 만난다',s)
FIG['FRZG']=frzg()

# ═════ 34 발열 반응의 자발성 (그림 Ⅲ-20을 새로 그림) ═════
def fig20():
    s=[]; base=210
    def tube(x):
        return (P([(x,base),(x,330),(x+60,330),(x+60,base)],GLASS,3)+R(x+3,base+30,54,98,'none',0,'#E3F1FA')
                +''.join(heat(x+62,base+40+i*30,x+100,base+40+i*30,3) for i in range(3)))
    s.append(L(10,base,470,base,MUTED,1.5,'5 4'))
    s.append(tube(50)+tube(290))
    s.append(T(110,360,mix='(가)',size=20,weight=700)+T(350,360,mix='(나)',size=20,weight=700))
    s.append(an('draw',barrow(62,base,-50,24,BF),dur='.6'))
    s.append(an('draw',barrow(102,base,-110,24,RD),dur='.7',delay='.4'))
    s.append(an('draw',barrow(150,base,-160,28,FIELD),dur='.7',delay='.9'))
    s.append(an('draw',barrow(302,base,60,24,BF),dur='.6'))
    s.append(an('draw',barrow(342,base,-140,24,RD),dur='.7',delay='.4'))
    s.append(an('draw',barrow(390,base,-80,28,FIELD),dur='.7',delay='.9'))
    s.append(T(150,base-172,mix='전체',size=18,fill=FIELD,weight=700)+T(102,base-122,mix='주위',size=18,fill=RD,weight=700)+T(62,base-62,mix='계',size=18,fill=BF,weight=700))
    s.append(T(390,base-92,mix='전체',size=18,fill=FIELD,weight=700)+T(342,base-152,mix='주위',size=18,fill=RD,weight=700)+T(280,base+44,mix='계',size=18,fill=BF,weight=700,anchor='end'))
    s.append(T(158,base+70,mix='열',size=18,fill=EQUI,anchor='start')+T(398,base+70,mix='열',size=18,fill=EQUI,anchor='start'))
    return svg((480,374),430,'발열 반응의 자발성: (가) 계와 주위의 엔트로피가 모두 증가, (나) 계의 엔트로피는 감소하지만 주위의 증가가 더 커서 전체가 증가',s)
FIG['FIG20']=fig20()

# ═════ 36 생명체와 제2법칙 ═════
def life():
    s=[]
    s.append(R(10,20,460,360,MUTED,1.5,'#F3F6F9',14)+T(30,48,mix='주위',size=20,anchor='start',fill=MUTED,weight=700))
    s.append(P([(240-80+80*math.cos(t/40*6.283)*1.0+0,200+70*math.sin(t/40*6.283)) for t in range(41)],FIELD,3,fill='#E8F5EE',close=True))
    s.append(T(240,190,mix='생명체 (계)',size=21,weight=700)+T(240,222,mix='복잡한 분자 합성',size=18,fill=MUTED))
    s.append(A(44,120,150,160,'ink',3)+T(40,104,mix='포도당, $\\ce{O2}$',size=19,anchor='start'))
    s.append(A(330,160,436,120,'ink',3)+T(450,104,mix='$\\ce{CO2}$, $\\ce{H2O}$',size=19,anchor='end'))
    s.append(an('draw',heat(240,272,240,330)+heat(300,262,350,316)+heat(180,262,130,316),dur='.9'))
    s.append(T(240,356,mix='열',size=19,fill=EQUI))
    s.append(T(70,290,tex='\\Delta S&lt;0',size=19,fill=BF)+T(410,290,tex='\\Delta S_\\text{주위}&gt;0',size=19,fill=RD))
    return svg((480,390),450,'생명체는 먹이와 산소를 받아 복잡한 분자를 만들며 열과 이산화 탄소, 물을 주위로 내보낸다',s)
FIG['LIFE']=life()

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
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "엔트로피", "file": "3-2-1_엔트로피", "header": "Ⅲ-2-1 엔트로피 (고등 고급 화학 142–150쪽)"}\n')
print('ok',len(out),'sections',out.count('<section'),'anim',out.count('data-anim'))
