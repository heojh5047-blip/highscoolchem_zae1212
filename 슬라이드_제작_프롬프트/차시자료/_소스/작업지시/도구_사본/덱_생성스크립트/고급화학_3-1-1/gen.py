# -*- coding: utf-8 -*-
"""고급화학 3-1-1 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   labs_src.js·extra_src.css를 labs.js·extra.css로 복사한다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)"""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
OUT=BASE+'3-1-1_화학_반응과_에너지/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-1-1_화학_반응과_에너지/', OUT
FIG={}
PIS='#C9D2DB'; HOT='#FDE2E4'; COLD='#E3EEFB'; SAND='#C9A66B'; FLAME='#F2A93B'
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
def cyl(x,top,w,bot,py,fill='#FFFFFF',n=8,seed=1,pt=14,rod=0,anim=True,r=8):
    """실린더 벽(위가 열림) + 기체(py+pt ~ bot) + 피스톤(py ~ py+pt)"""
    s=[R(x+3,py+pt,w-6,bot-py-pt,'none',0,fill)]
    s.append(gas(x+3,py+pt,w-6,bot-py-pt,n,seed,r,anim))
    p=R(x+3,py,w-6,pt,INK,2,PIS,2)
    if rod: p=R(x+w/2-6,py-rod,12,rod,INK,1.5,PIS)+p
    s.append(p)
    s.append(P([(x,top),(x,bot),(x+w,bot),(x+w,top)],INK,3))
    return ''.join(s)
def piston_only(x,w,py,pt=14,rod=0):
    p=R(x+3,py,w-6,pt,INK,2,PIS,2)
    if rod: p=R(x+w/2-6,py-rod,12,rod,INK,1.5,PIS)+p
    return p
def flame(cx,by,s=1.0):
    return (f'<path d="M{f(cx)} {f(by-34*s)} C{f(cx+16*s)} {f(by-16*s)} {f(cx+14*s)} {f(by)} {f(cx)} {f(by)} C{f(cx-14*s)} {f(by)} {f(cx-16*s)} {f(by-16*s)} {f(cx)} {f(by-34*s)} Z" fill="{FLAME}" stroke="{OX}" stroke-width="1.5"/>'
            +f'<path d="M{f(cx)} {f(by-18*s)} C{f(cx+7*s)} {f(by-9*s)} {f(cx+6*s)} {f(by)} {f(cx)} {f(by)} C{f(cx-6*s)} {f(by)} {f(cx-7*s)} {f(by-9*s)} {f(cx)} {f(by-18*s)} Z" fill="#FFE45C"/>')
def thermo(x,top,bot,lvl,col=PLUS):
    return (R(x-5,top,10,bot-top,INK,1.5,'#FFFFFF',5)+C(x,bot+6,9,INK,1.5,col)+R(x-2.5,lvl,5,bot-lvl+4,'none',0,col))
def hdim(x1,x2,y,lab,col=MUTED,size=19,dy=-8):
    return (L(x1,y-7,x1,y+7,col,1.5)+L(x2,y-7,x2,y+7,col,1.5)+A(x1+2,y,x2-2,y,'muted',1.5)+A(x2-2,y,x1+2,y,'muted',1.5)+T((x1+x2)/2,y+dy,mix=lab,size=size,fill=col,halo=True))
def vdim(x,y1,y2,lab,col=MUTED,size=19,dx=10,anchor='start'):
    return (L(x-7,y1,x+7,y1,col,1.5)+L(x-7,y2,x+7,y2,col,1.5)+A(x,y1+2,x,y2-2,'muted',1.5)+A(x,y2-2,x,y1+2,'muted',1.5)+T(x+dx,(y1+y2)/2+7,mix=lab,size=size,anchor=anchor,fill=col))

# ═════ 1 표지 ═════
def cover():
    s=[]
    s.append(T(230,40,tex='\\Delta U=q+w',size=34))
    s.append(an('move',cyl(120,90,220,420,190,'#FFF4E8',10,3,anim=True),**{'from':'0,40','dur':'1.6','ease':'out'}))
    for x in (165,230,295): s.append(A(x,104,x,176,'ink',3))
    s.append(T(355,140,tex='P_\\text{외부}',size=24,anchor='start'))
    s.append(A(395,250,395,170,'ink',5)+T(405,224,mix='일 $w$',size=22,anchor='start'))
    s.append(flame(230,488,1.0)+an('fade',A(230,450,230,428,'equi',5)+A(196,452,206,428,'equi',4)+A(264,452,254,428,'equi',4),dur='1.2',rep='loop')+T(290,470,mix='열 $q$',size=22,anchor='start',fill=EQUI))
    return svg((460,500),430,'피스톤 실린더 속 기체: 열 q를 흡수하고 외부 압력을 거슬러 팽창하며 일 w를 한다',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 2 대단원 도입: 에너지 흐름 ═════
def eflow():
    s=[R(150,14,240,64,INK,2.5,'#FFF4E8',12)+T(270,42,mix='화학 반응',size=22,weight=700)+T(270,68,mix='(화학 결합의 에너지)',size=20,fill=MUTED)]
    xs=(80,270,460); labs=(('열','제련: 쇳물'),('일','엔진: 피스톤'),('전기 에너지','전기 자동차·전지'))
    for i,(x,(a,b)) in enumerate(zip(xs,labs)):
        s.append(an('fade',A(270+(x-270)*.12,82,x,150,'ink',3),delay=f(.25*i),dur='.8'))
        s.append(R(x-82,156,164,108,MUTED,2,'#FFFFFF',10))
        s.append(T(x,250,mix=a,size=21,weight=700)+T(x,290,mix=b,size=20,fill=MUTED))
    s.append(flame(80,236,1.1))
    s.append(R(242,218,56,10,INK,1.5,PIS)+R(244,228,52,4,'none',0,'none')+P([(236,180),(236,240),(304,240),(304,180)],INK,2.5)+A(270,212,270,170,'ink',3))
    s.append(R(430,196,52,34,INK,2,'#FFFFFF',4)+R(482,206,7,14,INK,1.5,INK)+T(446,220,tex='-',size=20)+T(466,220,tex='+',size=20))
    s.append(an('fade',L(440,196,452,176,'#E3B23C',3)+L(452,176,446,176,'#E3B23C',3)+L(446,176,458,158,'#E3B23C',3),dur='.6',rep='loop'))
    return svg((540,300),470,'화학 반응의 에너지가 열, 일, 전기 에너지로 바뀌어 쓰인다',s)
FIG['EFLOW']=eflow()

# ═════ 3 중단원 도입: 메테인 연소 에너지 도표 ═════
def mid():
    s=[A(50,300,50,30,'muted',2)+T(62,40,mix='엔탈피 $H$',size=19,anchor='start',fill=MUTED)+L(50,300,470,300,MUTED,2)+T(468,326,mix='반응 경로',size=19,anchor='end',fill=MUTED)]
    s.append(L(70,90,230,90,INK,3)+T(150,76,tex='\\ce{CH4(g) + 2O2(g)}',size=21))
    s.append(L(300,250,470,250,INK,3)+T(385,236,tex='\\ce{CO2(g) + 2H2O(l)}',size=21))
    s.append(L(230,90,262,90,MUTED,1.5,'5 4')+L(262,250,300,250,MUTED,1.5,'5 4'))
    s.append(an('draw',A(262,94,262,246,'ink',3),dur='1.2'))
    s.append(T(274,160,tex='\\Delta H^\\circ=-890\\ \\text{kJ}',size=21,anchor='start'))
    s.append(an('fade',A(150,140,150,200,'equi',4),dur='1',rep='loop')+T(140,226,mix='주위로 열 방출',size=19,fill=EQUI,anchor='middle'))
    return svg((490,336),440,'메테인 연소의 에너지 도표: 반응물보다 생성물의 엔탈피가 890 kJ 낮다',s)
FIG['MID']=mid()

# ═════ 5 생각 열기: 엔진 ═════
def engine():
    s=[R(130,36,12,30,INK,1.5,PIS)+L(136,66,136,78,INK,2)]
    s.append(R(83,70,106,90,'none',0,'#FFF1D6'))
    s.append(an('pop',f'<path d="M136 86 L146 104 L166 98 L152 114 L170 128 L148 126 L140 146 L132 126 L110 130 L124 114 L106 100 L128 104 Z" fill="#FFE45C" stroke="{OX}" stroke-width="2"/>',o='136,114',dur='.8',rep='loop'))
    s.append(an('move',piston_only(80,112,160,16,110),**{'from':'0,-46','dur':'1.4','ease':'out'}))
    s.append(P([(80,60),(80,300),(192,300),(192,60),(80,60)],INK,3))
    s.append(A(230,190,230,262,'ink',5)+T(242,230,mix='기체가 피스톤을||미는 일',size=19,anchor='start'))
    for y in (86,126): s.append(an('fade',A(76,y,26,y,'equi',4),dur='1',rep='loop'))
    s.append(T(50,166,mix='열',size=21,fill=EQUI,anchor='middle'))
    s.append(T(136,24,mix='점화 플러그',size=19,fill=MUTED))
    s.append(T(136,110,mix='',size=19) if False else '')
    return svg((380,316),330,'엔진 실린더: 연소한 기체가 열을 내놓고 피스톤을 밀어 일을 한다',s)
FIG['ENGINE']=engine()

# ═════ 7 계와 주위 ═════
def system():
    s=[R(14,14,492,300,MUTED,2,'none',12,'8 6')+T(26,40,mix='우주 = 계 + 주위',size=19,anchor='start',fill=MUTED)]
    s.append(R(70,110,380,180,'none',0,WATER)+P([(64,92),(70,104),(70,290),(450,290),(450,104),(456,92)],GLASS,3)+L(70,110,450,110,WATER_S,1.5))
    s.append(R(242,84,36,170,'none',0,'none'))
    s.append(f'<path d="M242 60 L242 236 A18 18 0 0 0 278 236 L278 60" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2.5"/>')
    s.append(f'<path d="M244 150 L244 236 A16 16 0 0 0 276 236 L276 150 Z" fill="#F7D8A8"/>')
    s.append(L(244,150,276,150,'#C8954A',1.5))
    for (x1,y1,x2,y2,d) in ((228,200,170,200,0),(170,230,228,230,.3),(292,200,350,200,.15),(350,230,292,230,.45)):
        s.append(an('fade',A(x1,y1,x2,y2,'equi',3),delay=f(d),dur='.9',rep='loop'))
    s.append(T(260,286,mix='',size=19) if False else '')
    s.append(T(330,72,mix='계: 반응 용액',size=21,anchor='start',weight=700)+L(282,170,326,80,MUTED,1.5))
    s.append(T(110,272,mix='주위: 수조의 물',size=21,anchor='start',weight=700))
    s.append(T(400,180,mix='에너지',size=19,fill=EQUI,anchor='middle'))
    return svg((520,328),500,'시험관 속 반응 용액(계)과 수조(주위) 사이의 에너지 출입',s)
FIG['SYS']=system()

# ═════ 8 계의 종류 ═════
def kind(k):
    s=[]
    if k==0:
        s.append(beaker(100,80,100,110,WATER,.6))
        for i,x in enumerate((125,150,175)): s.append(an('move',C(x,60,6,GRAV,1.2,'#E4E8EC'),**{'from':'0,30','dur':f(1.4+.2*i),'rep':'loop'}))
        s.append(A(150,52,150,22,'grav',2.5)+T(178,28,mix='물질',size=19,anchor='start',fill=MUTED))
    elif k==1:
        s.append(f'<path d="M135 62 L135 104 L100 186 L200 186 L165 104 L165 62" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'+f'<path d="M116 148 L184 148 L200 186 L100 186 Z" fill="{WATER}"/>'+R(129,46,42,20,INK,1.5,'#8C6B4A',3))
    else:
        s.append(R(104,52,92,140,INK,2.5,'#F3F5F8',14)+R(116,64,68,116,MUTED,1.5,WATER,8,'5 3')+R(126,36,48,18,INK,2,'#8C99A6',4))
    if k<2:
        s.append(an('fade',A(92,140,48,140,'equi',4)+A(48,166,92,166,'equi',4),dur='1',rep='loop')+T(42,124,mix='에너지',size=19,fill=EQUI,anchor='start'))
    else:
        for x,y in ((60,120),(240,120)): s.append(L(x-12,y-12,x+12,y+12,PLUS,3)+L(x-12,y+12,x+12,y-12,PLUS,3))
    return svg((290,210),270,['열린계','닫힌계','고립계'][k],s)
def beaker(x,y,w,h,fill=WATER,level=.7,stroke=GLASS):
    lv=y+h*(1-level)
    return (R(x,lv,w,y+h-lv,'none',0,fill)+P([(x-4,y-6),(x,y),(x,y+h),(x+w,y+h),(x+w,y),(x+w+4,y-6)],stroke,2.5)+L(x,lv,x+w,lv,WATER_S,1.5))
for i in range(3): FIG['KIND%d'%i]=kind(i)

# ═════ 9 발열·흡열 ═════
def exo():
    s=[f'<path d="M110 120 L250 120 L228 214 L132 214 Z" fill="#8C99A6" stroke="{INK}" stroke-width="2.5"/>',f'<path d="M118 132 L242 132 L238 150 L122 150 Z" fill="#FF8A3D"/>']
    rnd=random.Random(5)
    for i in range(9):
        a=math.radians(rnd.uniform(205,335)); L_=rnd.uniform(30,60); x0,y0=180+rnd.uniform(-30,30),120
        s.append(an('move',L(x0,y0,x0+L_*math.cos(a),y0+L_*math.sin(a),'#F2B035',3),**{'from':f'{f(-8*math.cos(a))},{f(-8*math.sin(a))}','dur':f(.5+.3*rnd.random()),'rep':'loop'}))
    for (x1,y1,x2,y2) in ((96,170,40,170),(264,170,320,170)): s.append(an('fade',A(x1,y1,x2,y2,'equi',4),dur='1',rep='loop'))
    s.append(T(180,248,mix='열 방출',size=20,fill=EQUI,weight=700))
    return svg((360,262),330,'테르밋 반응: 녹은 철과 불꽃, 주위로 열을 방출',s)
def endo():
    s=[R(60,200,240,18,INK,2,'#C8A27A',3)]
    s.append(f'<ellipse cx="180" cy="200" rx="58" ry="7" fill="#DDEFFF" stroke="#8FB8E0" stroke-width="2"/>')
    s.append(beaker(128,96,104,104,'#F4F6F8',.55))
    for x,y in ((140,186),(162,180),(190,184),(214,178),(176,166)): s.append(C(x,y,7,'#9AA5B1',1.2,'#FFFFFF'))
    for i,(x1,y1,x2,y2) in enumerate(((40,140,116,140),(320,140,244,140),(180,40,180,84))): s.append(an('fade',A(x1,y1,x2,y2,'equi',4),delay=f(.2*i),dur='1',rep='loop'))
    s.append(T(180,250,mix='주위에서 열 흡수 → 물이 얼어붙음',size=19,fill=EQUI,weight=700))
    return svg((360,262),330,'흡열 반응: 비커 바닥과 나무판 사이의 물이 언다',s)
FIG['EXO']=exo(); FIG['ENDO']=endo()

# ═════ 10 예측: 냉찜질 팩 ═════
def pack():
    s=[R(40,150,340,70,'none',0,'#F6D5BD')+T(210,196,mix='손(주위)',size=20)]
    s.append(R(120,74,180,70,INK,2.5,'#E3EEFB',18)+T(210,116,mix='냉찜질 팩(계)',size=20,weight=700))
    for i,x in enumerate((150,210,270)): s.append(an('fade',A(x,170,x,150,'equi',4),delay=f(.2*i),dur='1',rep='loop'))
    s.append(T(120,168,mix='열',size=20,fill=EQUI,anchor='end',weight=700))
    s.append(f'<g class="step" data-g="pk">'+T(210,40,mix='$\\ce{NH4NO3}$ 용해(흡열)',size=20,fill=MUTED)+'</g>')
    return svg((420,232),400,'냉찜질 팩과 손 사이의 열 이동',s)
FIG['PACK']=pack()

# ═════ 11 컵 열량계 ═════
def cup():
    s=[]
    s.append(f'<path d="M80 110 L280 110 L262 330 L98 330 Z" fill="#F3F5F8" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<path d="M100 120 L260 120 L246 318 L114 318 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<path d="M106 196 L254 196 L246 318 L114 318 Z" fill="#F7D8A8"/>')
    s.append(R(74,96,212,16,INK,2,'#E6EBF0',4))
    s.append(thermo(220,30,284,200))
    s.append(P([(150,40),(150,296),(130,296),(170,296)],MUTED,3))
    s.append(an('move',C(160,250,4,INK,1,'#FFFFFF')+C(130,270,3,INK,1,'#FFFFFF'),**{'from':'0,30','dur':'1.4','rep':'loop'}))
    s.append(T(236,46,mix='온도계',size=19,anchor='start')+T(140,54,mix='젓개',size=19,anchor='end'))
    s.append(T(290,150,mix='폴리스타이렌||컵(2겹)',size=19,anchor='start'))
    s.append(T(180,356,mix='반응 혼합물',size=19))
    return svg((390,366),330,'폴리스타이렌 컵 열량계: 2겹 컵, 뚜껑, 온도계, 젓개, 반응 혼합물',s)
FIG['CUP']=cup()

# ═════ 12 통열량계 ═════
def bomb():
    s=[R(40,90,320,250,INK,3,'#F3F5F8',10)+R(56,104,288,222,'none',0,WATER)]
    s.append(R(150,170,100,120,INK,3,'#B7C0CA',12)+R(168,250,64,24,INK,1.5,'#FFFFFF',3)+R(180,240,40,12,INK,1.5,'#3A3F47',2))
    s.append(L(176,170,176,60,INK,2)+L(224,170,224,60,INK,2)+C(176,56,5,INK,2,'#FFFFFF')+C(224,56,5,INK,2,'#FFFFFF'))
    s.append(an('pop',C(200,236,9,OX,1.5,'#FFE45C'),o='200,236',dur='.8',rep='loop'))
    s.append(L(176,200,192,236,INK,1.5)+L(224,200,208,236,INK,1.5))
    s.append(thermo(300,40,300,170))
    s.append(P([(72,50),(72,300),(60,300),(84,300)],MUTED,3))
    s.append(P([(150,186),(128,186),(128,60)],INK,2)+T(128,48,mix='산소 주입구',size=19,anchor='middle'))
    s.append(T(212,40,mix='점화 단자',size=19)+T(318,62,mix='온도계',size=19,anchor='start')+T(56,40,mix='젓개',size=19,anchor='middle'))
    s.append(T(110,318,mix='물',size=20,anchor='middle')+T(150,164,mix='통(강철)',size=19,anchor='end')+T(146,280,mix='시료',size=19,anchor='end')+T(260,210,mix='가압된 산소',size=19,anchor='start'))
    return svg((400,350),360,'통열량계: 단열 용기 속 물에 잠긴 강철 통, 시료, 점화 단자, 온도계, 젓개',s)
FIG['BOMB']=bomb()

# ═════ 13 확인 문제 01: 온도-시간 ═════
def ttg():
    ax=Ax(70,220,290,170,10,27.0,ymin=23.5)
    s=[ax.frame([0,2,4,6,8,10],[24,25,26,27],T(360,272,mix='시간 (분)',size=18,anchor='end',fill=MUTED),T(76,20,mix='온도 (°C)',size=18,anchor='start',fill=MUTED),size=18)]
    fn=lambda t:24.00 if t<3 else 24.00+2.50*(1-math.exp(-(t-3)*1.4))
    s.append(an('draw',ax.curve(fn,0,10,200,INK,3),dur='1.6'))
    s.append(L(ax.X(3),ax.Y(24),ax.X(10),ax.Y(24),MUTED,1.5,'5 4')+L(ax.X(7.5),ax.Y(26.5),ax.X(10),ax.Y(26.5),MUTED,1.5,'5 4'))
    s.append(vdim(ax.X(9.2),ax.Y(26.5),ax.Y(24),'$\\Delta T=2.50\\ {}^\\circ\\text{C}$',dx=-12,anchor='end'))
    s.append(L(ax.X(3),ax.Y(24),ax.X(3),ax.Y(25.3),OX,1.5,'4 3')+T(ax.X(3)-4,ax.Y(25.1),mix='점화',size=18,anchor='end',fill=OX))
    return svg((380,282),360,'통열량계의 온도-시간 그래프: 점화 뒤 2.50 °C 오름',s)
FIG['TT']=ttg()

# ═════ 14 에너지 = 일을 할 수 있는 능력 ═════
def capacity():
    s=[]
    for i,(x,fill,py,lab) in enumerate(((60,COLD,170,'차가운 기체'),(300,HOT,110,'뜨거운 기체'))):
        body=cyl(x,40,150,280,py,fill,6 if i==0 else 6,11+i,rod=26,anim=True)
        wt=R(x+45,py-26-40,60,40,INK,2,'#8C99A6',4)+T(x+75,py-26-14,mix='추',size=19,fill='#FFFFFF')
        s.append(body+an('move',wt,**{'from':f'0,{f(150-py+10)}','dur':'1.4','ease':'out'}))
        s.append(T(x+75,310,mix=lab,size=20,weight=700))
    s.append(L(220,240-110-76,440,240-110-76,MUTED,1.5,'5 4'))
    s.append(T(470,40,mix='더 높이 들어 올림',size=19,anchor='end',fill=MUTED))
    return svg((480,322),440,'같은 양의 기체라도 뜨거운 기체가 추를 더 높이 들어 올린다',s)
FIG['CAP']=capacity()

# ═════ 15 내부 에너지의 구성 ═════
def uparts():
    s=[R(70,190,150,110,INK,2,'#FCE9D4')+R(70,110,150,80,INK,2,'#E5F2EA')+R(70,70,150,40,INK,2,'#E8E1F6')]
    s.append(L(70,70,70,40,INK,2,'6 4')+L(220,70,220,40,INK,2,'6 4')+T(145,52,mix='?',size=24,fill=MUTED))
    s.append(T(145,252,mix='분자의||운동 에너지',size=19)+T(145,156,mix='분자 사이의||위치 에너지',size=19)+T(145,96,mix='화학 결합',size=19))
    s.append(T(145,326,mix='내부 에너지 $U$',size=21,weight=700))
    s.append(L(270,200,380,200,INK,3)+T(390,206,tex='U_\\text{처음}',size=21,anchor='start'))
    s.append(L(270,110,380,110,INK,3)+T(390,116,tex='U_\\text{나중}',size=21,anchor='start'))
    s.append(an('draw',A(325,196,325,114,'ink',3),dur='1'))
    s.append(T(335,160,tex='\\Delta U',size=22,anchor='start'))
    s.append(T(325,250,mix='측정할 수 있는 것',size=19,fill=MUTED))
    return svg((460,340),420,'내부 에너지를 이루는 에너지와, 측정할 수 있는 내부 에너지 변화',s)
FIG['UPARTS']=uparts()

# ═════ 16·24 부호 그림 ═════
def sbox(kind):
    s=[]
    col='ink' if kind=='w' else 'equi'; c2=INK if kind=='w' else EQUI
    for i,(x,inn) in enumerate(((20,True),(280,False))):
        s.append(R(x+60,60,130,110,INK,3,'#FFF4E8',10)+T(x+125,124,mix='계',size=24,weight=700))
        a=A(x+4,115,x+56,115,col,6) if inn else A(x+194,115,x+246,115,col,6)
        s.append(an('move',a,**{'from':'-14,0' if inn else '-14,0','dur':'1.2','rep':'loop'}))
        if kind=='w': lab=('일을 받음','$w>0$') if inn else ('일을 함','$w<0$')
        else: lab=('열 흡수','$q=+10\\ \\text{J}$') if inn else ('열 방출','$q=-10\\ \\text{J}$')
        s.append(T(x+125,30,mix=lab[0]+' '+lab[1],size=20,fill=c2,weight=700))
        s.append(T(x+125,204,mix='$U$ 증가' if inn else '$U$ 감소',size=20))
    s.append(T(260,234,mix='주위',size=19,fill=MUTED)) if False else None
    return svg((540,222),520,'계로 들어가는 에너지는 +, 계에서 나가는 에너지는 −',s)
FIG['WSIGN']=sbox('w'); FIG['QSIGN']=sbox('q')

# ═════ 17 팽창 일·비팽창 일 ═════
def wt0():
    s=[an('move',cyl(80,20,120,190,70,'#FFF4E8',5,21,rod=0),**{'from':'0,40','dur':'1.4','ease':'out'})]
    s.append(A(230,110,230,50,'ink',4)+T(240,92,mix='일',size=22,anchor='start'))
    return svg((290,200),240,'팽창 일: 기체가 피스톤을 밀어낸다',s)
def wt1():
    s=['<svg x="0" y="0">'] if False else []
    s.append(R(30,110,60,40,INK,2,'#FFFFFF',4)+R(90,122,8,16,INK,1.5,INK)+T(48,138,tex='-',size=20)+T(72,138,tex='+',size=20))
    s.append(P([(60,110),(60,80),(160,80),(160,96)],INK,2)+P([(60,150),(60,170),(160,170),(160,152)],INK,2))
    s.append(C(160,124,26,INK,2.5,'#FFFFFF')+T(160,132,tex='\\mathrm{M}',size=22))
    s.append(L(186,124,230,124,INK,2)+C(236,124,8,INK,2,PIS)+L(244,124,244,60,INK,1.5))
    s.append(an('move',L(244,60,244,96,INK,1.5)+R(226,96,36,30,INK,2,'#8C99A6',3),**{'from':'0,40','dur':'1.4','ease':'out'}))
    s.append(an('dash',P([(64,80),(156,80)],MINUS,2,dash='6 6',extra='data-flow="1"'),speed='30'))
    return svg((290,200),240,'전기적 일: 전지의 전류로 전동기가 추를 들어 올린다',s)
def wt2():
    s=[R(30,30,90,124,INK,2.5,'#FCE3DA',30)+T(75,112,mix='근육',size=22)]
    s.append(L(120,70,200,70,INK,2)+C(206,70,8,INK,2,PIS)+L(214,70,214,100,INK,1.5))
    s.append(an('move',R(196,100,36,30,INK,2,'#8C99A6',3),**{'from':'0,40','dur':'1.4','ease':'out'}))
    s.append(T(75,186,mix='물질 대사',size=21,fill=MUTED))
    return svg((290,200),240,'역학적 일: 근육(물질 대사)이 추를 들어 올린다',s)
FIG['WT0']=wt0(); FIG['WT1']=wt1(); FIG['WT2']=wt2()

# ═════ 18 팽창 일 유도 (그림 Ⅲ-7) ═════
def pistonfig():
    s=[]
    # (가)
    x=60; s.append(cyl(x,60,150,320,200,'#FFF4E8',7,31))
    s.append(R(x+3,186,16,12,INK,1.5,MUTED)+R(x+131,186,16,12,INK,1.5,MUTED))
    for xx in (x+40,x+75,x+110): s.append(A(xx,130,xx,192,'ink',3))
    s.append(T(x+75,118,tex='P_\\text{외부}',size=21)+T(x+75,350,mix='(가)',size=20)+T(x-10,192,mix='고정 장치',size=19,anchor='end') if False else T(x+75,118,tex='P_\\text{외부}',size=21)+T(x+75,350,mix='(가)',size=20))
    s.append(L(x+11,198,x+11,240,MUTED,1.5)+T(x+20,258,mix='고정 장치',size=19,anchor='start',fill=MUTED) if False else '')
    # (나)
    x=330
    s.append(R(x+3,214,144,106,'none',0,'#FFF4E8'))
    s.append(R(x+3,120,144,94,'none',0,'#E5F2EA')+L(x+3,214,x+147,214,MUTED,1.5,'6 4'))
    s.append(gas(x+3,120,144,200,7,32))
    s.append(an('move',piston_only(x,150,106,14)+''.join(A(xx,40,xx,98,'ink',3) for xx in (x+40,x+75,x+110))+T(x+75,30,tex='P_\\text{외부}',size=21),**{'from':'0,94','dur':'1.6','ease':'out'}))
    s.append(P([(x,60),(x,320),(x+150,320),(x+150,60)],INK,3))
    s.append(R(x+3,200,16,12,MUTED,1.5,'none',0,'4 3')+R(x+131,200,16,12,MUTED,1.5,'none',0,'4 3'))
    s.append(vdim(x+175,120,214,'$d$'))
    s.append(T(x+75,172,tex='\\Delta V=Ad',size=21,halo=True))
    s.append(hdim(x+3,x+147,262,'넓이 $A$',dy=-8))
    s.append(T(x+75,350,mix='(나)',size=20))
    s.append(T(210,120,mix='',size=19) if False else '')
    s.append(T(285,196,mix='고정 장치',size=19,anchor='middle',fill=MUTED)+L(250,192,212,192,MUTED,1.5)+L(320,198,334,204,MUTED,1.5))
    return svg((560,362),540,'(가) 고정 장치로 멈춘 피스톤 (나) 고정 장치를 풀면 기체가 외부 압력을 거슬러 거리 d만큼 팽창',s)
FIG['PISTON']=pistonfig()

# ═════ 19 P–V 넓이: 팽창·압축 ═════
def pvr(exp):
    ax=Ax(56,200,200,150,10,3)
    s=[ax.frame([0,5,10],[0,1,2,3],T(266,250,mix='$V$ [L]',size=18,anchor='end',fill=MUTED),T(62,30,mix='$P$ [atm]',size=18,anchor='start',fill=MUTED),size=18)]
    v1,v2=(3,8) if exp else (8,3); p=1.5
    s.append(an('fade',R(ax.X(min(v1,v2)),ax.Y(p),ax.X(max(v1,v2))-ax.X(min(v1,v2)),ax.Y(0)-ax.Y(p),'none',0,BF,extra='fill-opacity=".15"'),dur='1'))
    s.append(L(ax.X(v1),ax.Y(p),ax.X(v2),ax.Y(p),BF,3))
    s.append(an('draw',A(ax.X(v1),ax.Y(p)-14,ax.X(v2),ax.Y(p)-14,'bfield',3),dur='1'))
    s.append(T((ax.X(v1)+ax.X(v2))/2,ax.Y(p)+44,mix='넓이 $=|w|$',size=19))
    s.append(T(ax.X(5.5),ax.Y(p)-24,tex='P_\\text{외부}',size=19,fill=BF))
    s.append(T(150,278,mix=('팽창: $\\Delta V>0$, $w<0$' if exp else '압축: $\\Delta V<0$, $w>0$'),size=20,weight=700))
    return svg((290,290),290,'일정한 외부 압력에서 '+('팽창' if exp else '압축')+'할 때 P–V 그래프 아래 넓이',s)
FIG['PVE']=pvr(True); FIG['PVC']=pvr(False)

# ═════ 21 심화: 가역 과정(모래알) ═════
def rev():
    s=[cyl(110,40,180,320,170,'#FFF4E8',7,41)]
    rnd=random.Random(8); grains=[]
    for i in range(46):
        gx=rnd.uniform(120,280); hh=40*(1-abs(gx-200)/85)
        gy=170-rnd.uniform(3,max(4,hh)); grains.append((gx,gy))
    for gx,gy in grains: s.append(C(gx,gy,4,'#8C6B3E',1,SAND))
    s.append(an('move',C(300,112,4.5,'#8C6B3E',1,SAND),**{'from':'-90,30','dur':'1.4','ease':'out','rep':'loop'}))
    s.append(A(300,104,330,80,'ink',2)+T(336,74,mix='한 알씩 덜어 냄',size=19,anchor='start'))
    s.append(T(200,350,mix='매 순간 $P_\\text{외부}=P$',size=20,weight=700))
    s.append(T(300,240,mix='기체 압력 $P$',size=19,anchor='start') if False else '')
    return svg((470,362),420,'피스톤 위 모래알을 한 알씩 덜어 내면 외부 압력이 아주 조금씩 줄어 기체가 거의 평형을 유지하며 팽창한다',s)
FIG['REV']=rev()

# ═════ 22 심화: 등온 가역 팽창 넓이 ═════
nRT=0.08206*292
def iso():
    ax=Ax(66,280,400,230,24,4)
    s=[ax.frame([0,4,8,12,16,20,24],[0,1,2,3,4],T(476,334,mix='부피 $V$ [L]',size=18,anchor='end',fill=MUTED),T(72,34,mix='압력 $P$ [atm]',size=18,anchor='start',fill=MUTED),size=18)]
    pts=[(ax.X(8+12*i/80),ax.Y(nRT/(8+12*i/80))) for i in range(81)]
    s.append(an('fade',P([(ax.X(8),ax.Y(0))]+pts+[(ax.X(20),ax.Y(0))],'none',0,FIELD,extra='fill-opacity=".2"',close=True),dur='1.2'))
    s.append(an('draw',ax.curve(lambda v:nRT/v,6,24,160,INK,3),dur='1.4'))
    st=[]
    for i in range(6):
        va=8+2*i; st.append(R(ax.X(va),ax.Y(nRT/(va+2)),ax.X(va+2)-ax.X(va),ax.Y(0)-ax.Y(nRT/(va+2)),MUTED,1.5,'none',0,'4 3'))
    s.append('<g class="step" data-g="st">'+''.join(st)+T(ax.X(14),ax.Y(0.55),mix='작은 직사각형의 합',size=19,halo=True)+'</g>')
    s.append(L(ax.X(8),ax.Y(nRT/8),ax.X(8),ax.Y(0),MUTED,1.5,'5 4')+L(ax.X(20),ax.Y(nRT/20),ax.X(20),ax.Y(0),MUTED,1.5,'5 4'))
    s.append(T(ax.X(8),ax.Y(0)-8,tex='V_\\text{처음}',size=18,halo=True)+T(ax.X(20),ax.Y(0)-8,tex='V_\\text{나중}',size=18,halo=True))
    s.append(T(ax.X(14),ax.Y(1.45),mix='넓이 = 계가 한 일의 크기',size=19,halo=True))
    s.append(T(ax.X(8.6),ax.Y(3.55),mix='등온선 $P=\\dfrac{nRT}{V}$',size=19,anchor='start'))
    return svg((490,344),480,'등온 가역 팽창: 등온선 아래 V처음에서 V나중까지의 넓이가 계가 한 일의 크기',s)
FIG['ISO']=iso()

# ═════ 23 열과 온도 ═════
def heatt():
    s=[]
    for i,(x,w,h,lab) in enumerate(((60,80,90,'물 1 L'),(250,170,150,'물 10 L'))):
        s.append(beaker(x,220-h,w,h,'#FDE2E4',.8,GLASS)); s.append(thermo(x+w/2,40,190,80))
        s.append(T(x+w/2,252,mix=lab+', 80 °C',size=19))
    s.append(T(220,282,mix='내놓을 수 있는 열: 10 L 쪽이 약 10배',size=19,fill=EQUI,weight=700))
    return svg((460,292),430,'온도가 같은 물 1 L와 10 L: 온도는 같아도 내놓을 수 있는 열은 다르다',s)
FIG['HEATT']=heatt()

# ═════ 25 ΔU = q + w ═════
def first():
    s=[an('move',cyl(110,40,180,300,120,'#FDE2E4',9,51,rod=0),**{'from':'0,40','dur':'1.6','ease':'out'})]
    s.append(flame(200,350,0.9)+an('fade',A(200,326,200,306,'equi',5),dur='1',rep='loop')+T(230,336,mix='열 $q$ 흡수',size=20,anchor='start',fill=EQUI))
    s.append(A(330,160,330,90,'ink',5)+T(342,124,mix='일 $w$',size=20,anchor='start')+T(342,150,mix='(계가 함)',size=19,anchor='start',fill=MUTED))
    s.append(T(200,210,tex='\\Delta U',size=26,halo=True))
    return svg((440,362),380,'계가 열을 흡수하고 팽창하며 일을 하는 피스톤',s)
FIG['FIRST']=first()

# ═════ 26 고립계 ═════
def isol():
    s=[R(20,20,440,250,INK,6,'#F3F5F8',16)+R(34,34,412,222,MUTED,1.5,'#FFFFFF',10,'6 4')]
    s.append(T(240,62,mix='고립계 (물질 × 에너지 ×)',size=19,fill=MUTED))
    s.append(C(150,160,62,INK,3,'#FFF4E8')+T(150,168,mix='계',size=22,weight=700))
    s.append(T(350,168,mix='주위',size=22,weight=700))
    s.append(an('fade',A(216,140,290,140,'equi',4),dur='1',rep='loop')+T(253,128,mix='$q$',size=19,fill=EQUI))
    s.append(an('fade',A(290,184,216,184,'ink',4),delay='.4',dur='1',rep='loop')+T(253,214,mix='$w$',size=19))
    s.append(T(240,296,tex='\\Delta U_\\text{계}+\\Delta U_\\text{주위}=0',size=22))
    return svg((480,310),440,'고립계 안의 계와 주위가 열과 일을 주고받아도 전체 내부 에너지는 일정',s)
FIG['ISOL']=isol()

# ═════ 31 상태 함수: 산의 고도 ═════
def mount():
    s=[f'<path d="M20 250 L110 170 L160 200 L230 80 L300 160 L330 140 L400 250 Z" fill="#E5F2EA" stroke="{INK}" stroke-width="2"/>']
    s.append(an('draw',P([(70,232),(120,200),(180,160),(240,120),(285,110)],INK,3),dur='1.4'))
    s.append(an('draw',P([(70,232),(150,236),(250,232),(330,190),(285,110)],INK,3,dash='7 5'),dur='1.8'))
    s.append(C(70,232,7,INK,2,PLUS)+T(58,224,tex='\\mathrm{A}',size=21,anchor='end')+C(285,110,7,INK,2,PLUS)+T(285,96,tex='\\mathrm{B}',size=21))
    s.append(L(300,110,440,110,MUTED,1.5,'5 4')+L(80,232,440,232,MUTED,1.5,'5 4')+vdim(430,110,232,'$h$',dx=-10,anchor='end'))
    s.append(T(220,286,mix='(가) 산의 고도',size=20))
    x0=500
    s.append(A(x0,250,x0,40,'muted',2)+T(x0+8,50,mix='내부 에너지',size=19,anchor='start',fill=MUTED))
    s.append(L(x0+20,220,x0+90,220,INK,3)+T(x0+55,246,tex='\\mathrm{A}',size=21)+L(x0+180,90,x0+250,90,INK,3)+T(x0+215,76,tex='\\mathrm{B}',size=21))
    s.append(an('draw',P([(x0+90,220),(x0+120,120),(x0+150,60),(x0+180,90)],FIELD,3),dur='1.2')+T(x0+110,70,mix='화학적 변화',size=18,fill=FIELD,anchor='end'))
    s.append(an('draw',P([(x0+90,220),(x0+135,200),(x0+165,150),(x0+180,90)],BF,3,dash='7 5'),dur='1.4')+T(x0+172,196,mix='물리적 변화',size=18,fill=BF,anchor='start'))
    s.append(A(x0+262,218,x0+262,94,'ink',3)+T(x0+272,162,tex='\\Delta U',size=21,anchor='start'))
    s.append(T(x0+150,286,mix='(나) 상태 함수인 내부 에너지',size=20))
    return svg((820,300),760,'(가) 어느 길로 올라도 고도 변화는 같다 (나) 어느 경로를 거쳐도 내부 에너지 변화는 같다',s)
FIG['MOUNT']=mount()

# ═════ 32–34 두 경로 ═════
def paths(sh=None,width=480):
    ax=Ax(66,280,400,230,24,4)
    s=[ax.frame([0,4,8,12,16,20,24],[0,1,2,3,4],T(476,334,mix='부피 $V$ [L]',size=18,anchor='end',fill=MUTED),T(72,34,mix='압력 $P$ [atm]',size=18,anchor='start',fill=MUTED),size=18)]
    if sh=='A':
        pts=[(ax.X(8+12*i/80),ax.Y(nRT/(8+12*i/80))) for i in range(81)]
        s.append(an('fade',P([(ax.X(8),ax.Y(0))]+pts+[(ax.X(20),ax.Y(0))],'none',0,FIELD,extra='fill-opacity=".2"',close=True),dur='1.2'))
        s.append(T(ax.X(11.8),ax.Y(.45),mix='$|w|=2.22\\ \\text{kJ}$',size=19,halo=True))
    if sh=='B':
        s.append(an('fade',R(ax.X(8),ax.Y(1.20),ax.X(20)-ax.X(8),ax.Y(0)-ax.Y(1.2),'none',0,BF,extra='fill-opacity=".15"'),dur='1.2'))
        s.append(T(ax.X(11.8),ax.Y(.5),mix='$|w|=1.46\\ \\text{kJ}$',size=19,halo=True))
    s.append(an('draw',ax.curve(lambda v:nRT/v,8,20,120,INK,3),dur='1.4'))
    s.append(A(ax.X(12.6),ax.Y(nRT/12.6),ax.X(13.4),ax.Y(nRT/13.4),'ink',3))
    s.append(an('draw',P([(ax.X(8),ax.Y(3.0)),(ax.X(8),ax.Y(1.2)),(ax.X(20),ax.Y(1.2))],BF,3,dash='8 5'),dur='1.6'))
    s.append(A(ax.X(8),ax.Y(2.2),ax.X(8),ax.Y(1.95),'bfield',3)+A(ax.X(15.5),ax.Y(1.2),ax.X(16.3),ax.Y(1.2),'bfield',3))
    s.append(C(ax.X(8),ax.Y(3.0),6,INK,2,PLUS)+C(ax.X(20),ax.Y(1.2),6,INK,2,PLUS))
    s.append(T(ax.X(8)+10,ax.Y(3.0)-10,mix='처음 (8.00 L, 3.00 atm)',size=18,anchor='start'))
    s.append(T(ax.X(23.9),ax.Y(1.2)-46,mix='나중||(20.00 L, 1.20 atm)',size=18,anchor='end',halo=True))
    s.append(T(ax.X(11.4),ax.Y(nRT/11.4)-14,mix='경로 A',size=19,anchor='start',weight=700))
    s.append(T(ax.X(8)-8,ax.Y(2.1),mix='경로 B||1단계',size=18,anchor='end',fill=BF,weight=700)+T(ax.X(11.6),ax.Y(1.2)-10,mix='2단계',size=18,fill=BF,weight=700,halo=True))
    return svg((490,344),width,'이상 기체 1.00 mol의 두 경로: A 등온 가역 팽창, B 일정 부피 냉각 뒤 일정 압력 가열 팽창',s)
FIG['PATHS']=paths(); FIG['PATHA']=paths('A',440); FIG['PATHB']=paths('B',440)

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
print('ok',len(out))
