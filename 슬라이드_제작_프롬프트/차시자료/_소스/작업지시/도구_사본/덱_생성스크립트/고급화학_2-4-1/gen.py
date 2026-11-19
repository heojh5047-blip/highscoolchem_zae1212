# -*- coding: utf-8 -*-
"""고급화학 2-4-1(a/b) 그림 생성: tpl_a.html, tpl_b.html의 {{KEY}}를 SVG로 바꿔 각 덱 slides.html을 만든다.
   labs_src.js·extra_src.css를 두 덱에 labs.js·extra.css로 복사한다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 두 폴더만, assert로 막음)"""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
DECK='2-4-1_용액의_농도와_용해도_묽은_용액의_성질'
OUT={'a':BASE+DECK+'a/','b':BASE+DECK+'b/'}
for k,v in OUT.items():
    assert v==BASE+'2-4-1_용액의_농도와_용해도_묽은_용액의_성질'+k+'/', v
FIG={}
CU='#3E8ED0'; SOLUTE='#F2B035'; LASER='#E53935'; AGC='#E3B23C'
def cu(c): # 농도 → 파랑 진하기
    a=min(1,c/0.5); r=int(232-(232-62)*a); g=int(242-(242-142)*a); b=int(250-(250-208)*a); return f'#{r:02X}{g:02X}{b:02X}'
def ion(x,y,s,r=9):
    col=PLUS if s=='+' else MINUS
    k=r*.5; o=C(x,y,r,col,2,'#FFFFFF')+L(x-k,y,x+k,y,col,2.2)
    if s=='+': o+=L(x,y-k,x,y+k,col,2.2)
    return o
def wdot(x,y,r=6): return C(x,y,r,GRAV,1.2,'#E4E8EC')
def beaker(x,y,w,h,fill=WATER,level=.7,stroke=GLASS,extra=''):
    lv=y+h*(1-level)
    return (R(x,lv,w,y+h-lv,'none',0,fill)+P([(x-4,y-6),(x,y),(x,y+h),(x+w,y+h),(x+w,y),(x+w+4,y-6)],stroke,2.5)
            +L(x,lv,x+w,lv,WATER_S if fill==WATER else stroke,1.5))
def vflask(cx,by,r=46,neck=110,fill=None,mark=True,lvl=None):
    """부피 플라스크: 둥근 바닥(중심 cx,by), 목 위쪽 끝 by-r-neck. lvl: 액면 y(없으면 표선)"""
    top=by-r-neck; mk=top+32; nw=9
    s=[]
    if fill:
        ly=lvl if lvl else mk
        s.append(f'<path d="M{cx-nw} {ly} L{cx-nw} {by-r+6} A{r} {r} 0 1 0 {cx+nw} {by-r+6} L{cx+nw} {ly} Z" fill="{fill}" stroke="none"/>')
    s.append(f'<path d="M{cx-nw} {top} L{cx-nw} {by-r+6} A{r} {r} 0 1 0 {cx+nw} {by-r+6} L{cx+nw} {top}" fill="none" stroke="{GLASS}" stroke-width="2.5"/>')
    s.append(R(cx-nw-3,top-12,2*nw+6,12,INK,1.5,'#C9D2DB',2))
    if mark: s.append(L(cx-nw-4,mk,cx+nw+4,mk,INK,2))
    return ''.join(s)
def grid(ax,xs,ys,col='#E2E7EC'):
    return ''.join(L(ax.X(v),ax.y0,ax.X(v),ax.y0-ax.h,col,1) for v in xs[1:])+''.join(L(ax.x0,ax.Y(v),ax.x0+ax.w,ax.Y(v),col,1) for v in ys[1:])
def eps(l): return 12.0*math.exp(-((1e7/l-12500)**2)/(2*2400**2))
def obs(A): return -math.log10(10**(-A)+0.002)
def pw(t): return 10**(8.07131-1730.63/(233.426+t))*0.133322
def wl_rgb(l):
    if l<440: r,g,b=(440-l)/60,0,1
    elif l<490: r,g,b=0,(l-440)/50,1
    elif l<510: r,g,b=0,1,(510-l)/20
    elif l<580: r,g,b=(l-510)/70,1,0
    elif l<645: r,g,b=1,(645-l)/65,0
    else: r,g,b=1,0,0
    k=1 if l<700 else max(.35,1-(l-700)/300)
    return '#%02X%02X%02X'%(int(255*r*k),int(255*g*k),int(255*b*k))

# ═════════ a ═════════
def cover_a():
    s=[vflask(150,300,62,130,cu(.35))]
    s.append(f'<g data-anim="move" data-from="0,-60" data-dur="1.4" data-ease="out">'+R(268,40,12,190,GLASS,2.2,'#FFFFFF',4)+R(270,150,8,78,'none',0,cu(.5))+P([(270,230),(274,262),(278,230)],GLASS,2)+R(264,20,20,26,INK,1.5,'#C9D2DB',3)+'</g>')
    ax=Ax(70,500,330,100,0.55,1.5)
    s.append(L(70,500,410,500,MUTED,2)+L(70,500,70,390,MUTED,2))
    pts=[(c,c*2.63) for c in (0.1,0.2,0.3,0.4,0.5)]
    s.append('<g data-anim="draw" data-dur="1.4">'+P([(ax.X(0),ax.Y(0)),(ax.X(0.55),ax.Y(0.55*2.63))],FIELD,3)+'</g>')
    for i,(c,a) in enumerate(pts): s.append(f'<g data-anim="pop" data-o="{f(ax.X(c))},{f(ax.Y(a))}" data-delay="{f(.15*i)}">'+C(ax.X(c),ax.Y(a),6,INK,2,cu(c))+'</g>')
    s.append(T(405,526,mix='농도',size=19,anchor='end',fill=MUTED)+T(80,394,mix='흡광도',size=19,anchor='start',fill=MUTED))
    return svg((440,540),400,'부피 플라스크와 피펫, 흡광도–농도 직선',s,'fig cover-fig')
FIG['COVER_A']=cover_a()

def sea():
    rnd=random.Random(4); s=[R(10,10,520,200,INK,2.5,'#EAF4FB',8)]
    pts=[]
    while len(pts)<46:
        p=(rnd.uniform(26,514),rnd.uniform(26,194))
        if all(math.hypot(p[0]-a,p[1]-b)>24 for a,b in pts): pts.append(p)
    for i,(x,y) in enumerate(pts):
        if i<4: s.append(f'<g data-anim="move" data-from="{rnd.choice((-8,8))},{rnd.choice((-6,6))}" data-rep="alt" data-dur="{f(1+rnd.random()*.6)}">'+ion(x,y,'+' if i%2==0 else '-')+'</g>')
        else: s.append(wdot(x,y,7))
    s.append(wdot(40,236,7)+T(54,242,mix='물 분자(용매)',size=19,anchor='start'))
    s.append(ion(230,236,'+')+ion(254,236,'-')+T(272,242,mix='$\\ce{Na+}$, $\\ce{Cl-}$(용질)',size=19,anchor='start'))
    s.append(T(530,242,mix='크기 비례 아님',size=18,anchor='end',fill=MUTED))
    return svg((540,256),520,'바닷물 속 물 분자와 나트륨 이온·염화 이온',s)
FIG['SEA']=sea()

def saline():
    s=[P([(60,30),(200,30),(210,60),(210,230),(180,260),(80,260),(50,230),(50,60)],GLASS,2.5,'#F4F9FD',close=True)]
    s.append('<g data-anim="scale" data-from="1,0.2" data-o="130,258">'+P([(54,90),(206,90),(206,228),(178,256),(82,256),(54,228)],'none',0,'#E2EEF8',close=True)+'</g>')
    s.append(L(130,260,130,300,GLASS,4)+R(118,20,24,12,INK,1.5,'#C9D2DB',2))
    s.append(T(130,140,mix='생리 식염수',size=20,weight=700)+T(130,172,mix='$\\ce{NaCl}$ 0.9 %',size=20))
    return svg((260,310),220,'생리 식염수 수액 주머니',s)
FIG['SALINE']=saline()

def tools():
    s=[]
    # 눈금실린더
    x=40; s.append(R(x,40,36,220,GLASS,2.2,'none')+R(x+2,120,32,138,'none',0,WATER)+P([(x-14,262),(x+50,262)],GLASS,4))
    for i in range(10): s.append(L(x,60+i*20,x+(14 if i%5==0 else 8),60+i*20,MUTED,1.2))
    # 뷰렛
    x=170; s.append(R(x,30,18,200,GLASS,2.2,'none')+R(x+2,70,14,158,'none',0,WATER)+P([(x,230),(x+6,246),(x+12,246),(x+18,230)],GLASS,2)+R(x-6,236,30,8,INK,1.5,'#C9D2DB',2)+L(x+9,246,x+9,268,GLASS,2.5))
    for i in range(9): s.append(L(x,40+i*22,x+8,40+i*22,MUTED,1.2))
    s.append(T(x+30,48,tex='0',size=18,anchor='start'))
    # 부피 피펫
    x=300; s.append(L(x,24,x,110,GLASS,5)+'<ellipse cx="300" cy="150" rx="16" ry="40" fill="none" stroke="#7E8B98" stroke-width="2.5"/>'+L(x,190,x,262,GLASS,5)+L(x-9,70,x+9,70,INK,2))
    # 부피 플라스크
    s.append(vflask(430,224,40,120,WATER))
    for i,(lx,t1,t2) in enumerate(((58,'눈금실린더','Tc'),(179,'뷰렛','Td'),(300,'부피 피펫','Td'),(430,'부피 플라스크','Tc'))):
        s.append(f'<g data-anim="pop" data-o="{lx},296" data-delay="{f(.15*i)}">'+T(lx,300,mix=t1,size=20,weight=700)+T(lx,328,mix=t2,size=19,fill=PLUS if t2=='Td' else MINUS)+'</g>')
    s.append(T(318,74,mix='표선',size=18,anchor='start',fill=MUTED)+T(448,106,mix='표선',size=18,anchor='start',fill=MUTED))
    return svg((500,340),500,'눈금실린더, 뷰렛, 부피 피펫, 부피 플라스크',s)
FIG['TOOLS']=tools()

def menis():
    s=[]
    for j,(x0,hg,lab) in enumerate(((40,False,'물'),(300,True,'수은'))):
        s.append(R(x0,30,60,230,GLASS,2.2,'none'))
        for i in range(11):
            yy=50+i*20; s.append(L(x0,yy,x0+(22 if i%5==0 else 12),yy,MUTED,1.3))
        s.append(T(x0-8,56,tex='20',size=18,anchor='end')+T(x0-8,156,tex='15',size=18,anchor='end')+T(x0-8,256,tex='10',size=18,anchor='end'))
        y=150
        if not hg:
            s.append(f'<path d="M{x0+2} 258 L{x0+2} {y-10} Q{x0+30} {y+12} {x0+58} {y-10} L{x0+58} 258 Z" fill="{WATER}" stroke="{WATER_S}" stroke-width="1.5"/>')
            yr=y+1
        else:
            s.append(f'<path d="M{x0+2} 258 L{x0+2} {y+10} Q{x0+30} {y-12} {x0+58} {y+10} L{x0+58} 258 Z" fill="#AEB6BF" stroke="#5B6B7F" stroke-width="1.5"/>')
            yr=y-1
        # 눈
        ex=x0+150
        s.append(f'<g data-anim="move" data-from="0,-40" data-dur="1.2" data-delay="{f(.3*j)}">'+L(x0+30,yr,ex-14,yr,PLUS,2,'6 4')+f'<path d="M{ex-14} {yr} Q{ex} {yr-16} {ex+16} {yr} Q{ex} {yr+16} {ex-14} {yr} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>'+C(ex+2,yr,5,INK,0,INK)+'</g>')
        s.append(T(x0+30,296,mix=lab,size=21,weight=700))
        s.append(T(x0+150,yr+46,mix=('오목한 아래 끝' if not hg else '볼록한 위 끝'),size=18,fill=PLUS))
    return svg((520,310),500,'물과 수은의 메니스커스를 눈높이에서 읽기',s)
FIG['MENIS']=menis()

def molar():
    s=[vflask(110,250,62,120,cu(.3))]
    rnd=random.Random(2)
    for i in range(7):
        a=rnd.uniform(0,2*math.pi); rr=rnd.uniform(0,40); s.append(C(110+rr*math.cos(a),250+rr*math.sin(a),5,PLUS,0,PLUS))
    s.append(T(128,106,mix='← 표선: 용액 1 L',size=19,anchor='start',fill=MUTED)+T(140,340,mix='용질 $n$ mol을 녹여 용액 1 L',size=19))
    return svg((300,350),280,'부피 플라스크에 만든 용액 1 L',s)
FIG['MOLAR']=molar()

def molal():
    s=[beaker(40,60,180,170,WATER,.75)]
    s.append(T(130,218,mix='용매 1 kg',size=20,weight=700))
    s.append('<g data-anim="move" data-from="0,-70" data-dur="1.2" data-ease="out">')
    for i in range(6): s.append(C(90+i*16,110+(i%2)*10,5,PLUS,0,PLUS))
    s.append('</g>')
    s.append(T(130,40,mix='+ 용질 $n$ mol',size=19,fill=PLUS))
    s.append(T(130,270,mix='부피가 아니라 질량 기준',size=19,fill=MUTED))
    return svg((260,284),240,'용매 1 kg에 용질을 녹인 용액',s)
FIG['MOLAL']=molal()

def etoh():
    s=[R(60,30,90,230,GLASS,2.5,'none')]
    s.append('<g data-anim="scale" data-from="1,0" data-o="105,258" data-dur="1.2">'+R(62,58,86,200,'none',0,WATER)+'</g>')
    s.append('<g data-anim="scale" data-from="1,0" data-o="105,258" data-dur="1.2" data-delay=".4">'+R(62,218,86,40,'none',0,'#BFE3CC')+'</g>')
    s.append(L(150,58,176,58,MUTED,1.5)+T(182,64,mix='100 mL(용액)',size=19,anchor='start'))
    s.append(L(150,218,176,218,MUTED,1.5)+T(182,224,mix='에탄올 20 mL',size=19,anchor='start',fill=FIELD))
    s.append(T(150,292,mix='20 vol% 에탄올 수용액',size=19,fill=MUTED))
    s.append(T(150,316,mix='(실제로는 고르게 섞인다)',size=18,fill=MUTED))
    return svg((320,326),300,'100 mL 용액 속 에탄올 20 mL',s)
FIG['ETOH']=etoh()

def prep(k):
    s=[]
    if k==1:
        s.append(R(20,150,120,20,INK,2,'#E6EAEE',3)+R(40,130,80,20,INK,1.5,'#FFFFFF')+T(80,146,tex='12.49',size=20))
        s.append(beaker(150,70,90,100,WATER,.55))
        s.append(f'<g data-anim="move" data-from="-50,-20" data-dur="1.2">'+P([(180,40),(205,28),(212,44)],INK,2,'#C9D2DB',close=True)+C(203,62,4,CU,0,CU)+C(198,72,4,CU,0,CU)+'</g>')
    elif k==2:
        s.append(vflask(170,170,40,90,cu(.2),lvl=150))
        s.append(P([(140,30),(200,30),(176,58),(176,80),(164,80),(164,58)],GLASS,2,close=True))
        s.append(f'<g data-anim="rot" data-from="-20" data-o="80,70">'+beaker(40,40,70,60,cu(.45),.5)+'</g>')
    elif k==3:
        s.append(f'<g data-anim="rot" data-from="10" data-o="130,140" data-rep="damp" data-dur="1.6">'+vflask(130,170,40,100,cu(.3),lvl=88)+'</g>')
    else:
        s.append(vflask(110,170,40,100,cu(.3)))
        s.append(P([(180,40),(230,40),(236,110),(174,110)],GLASS,2.2,'#F4F9FD',close=True)+P([(205,40),(205,24),(150,24),(130,46)],GLASS,3))
        s.append(f'<g data-anim="move" data-from="0,-14" data-rep="loop" data-dur="1">'+C(122,54,3.5,WATER_S,0,WATER_S)+'</g>')
        s.append(L(60,62,98,62,PLUS,2,'5 4')+T(56,68,mix='표선',size=18,anchor='end',fill=PLUS))
    return svg((260,216),240,f'고체 용질의 용액 제조 {k}단계',s)
for k in (1,2,3,4): FIG[f'PREP{k}']=prep(k)

def dilute():
    s=[beaker(20,90,110,120,cu(.5),.7)]
    s.append(T(75,236,mix='저장 용액 5.0 M',size=19))
    s.append(f'<g data-anim="move" data-from="-120,0" data-dur="1.4" data-ease="io">'+R(196,20,10,150,GLASS,2,'#FFFFFF',3)+R(198,110,6,58,'none',0,cu(.5))+P([(196,170),(201,192),(206,170)],GLASS,2)+'</g>')
    s.append(A(150,120,186,120,'ink',2.5)+T(168,108,mix='피펫',size=18))
    s.append(vflask(330,210,60,100,cu(.08)))
    s.append(T(315,300,mix='증류수로 표선까지 → 1 L',size=19))
    for i,(x,y) in enumerate(((45,170),(65,190),(90,165),(110,195),(100,180))): s.append(C(x,y,4,PLUS,0,PLUS))
    for (x,y) in ((300,205),(330,230),(355,200),(320,180),(345,245)): s.append(C(x,y,4,PLUS,0,PLUS))
    s.append(T(330,40,mix='용질 입자 수(몰수) 같음',size=19,fill=PLUS))
    return svg((430,310),400,'저장 용액을 피펫으로 덜어 부피 플라스크에서 희석',s)
FIG['DILUTE']=dilute()

def spec():
    s=[]
    s.append(R(10,90,70,60,INK,2,'#FFF6D6',6)+T(45,126,mix='광원',size=19))
    s.append(f'<g data-anim="draw" data-dur="1">'+L(80,120,150,120,'#C9B458',6)+'</g>')
    s.append(P([(150,80),(190,120),(150,160)],INK,2,'#E8EEF5',close=True)+T(165,186,mix='회절발',size=18))
    rb=['#7B2CBF','#1F6FD1','#2E9E6A','#E8C547','#E08A2C','#D7263D']
    for i,c in enumerate(rb): s.append(L(180,120,250,70+i*20,c,3))
    s.append(R(250,60,10,110,INK,0,INK)+R(250,156,10,14,'none',0,'#FFFFFF')+T(255,200,mix='슬릿',size=18))
    s.append(R(250,60,10,96,INK,0,INK))
    s.append(f'<g data-anim="dash" data-speed="40" data-flow="1">'+L(260,163,450,163,'#E53935',2,'8 8')+'</g>')
    s.append(L(260,163,330,163,'#E53935',6)+R(330,120,50,80,GLASS,2.5,cu(.4),3)+L(380,163,440,163,'#E53935',3))
    s.append(T(355,226,mix='큐벳(용액)',size=18))
    s.append(R(440,130,70,66,INK,2,'#E6EAEE',6)+T(475,168,mix='검출기',size=18))
    s.append(T(300,148,tex='I_0',size=20)+T(410,148,tex='I',size=20))
    s.append(L(330,214,380,214,MUTED,1.5)+T(355,252,mix='$b$ = 1 cm',size=18,fill=MUTED))
    return svg((520,262),520,'분광 광도계의 구조: 광원, 회절발, 슬릿, 큐벳, 검출기',s)
FIG['SPEC']=spec()

def wheel():
    cols=[('빨강','#D7263D'),('주황','#E8792B'),('노랑','#E8C547'),('초록','#2E9E6A'),('파랑','#1F6FD1'),('보라','#7B2CBF')]
    s=[]; cx,cy,r=130,128,88
    for i,(n,c) in enumerate(cols):
        a1=math.radians(-90+i*60-30); a2=math.radians(-90+i*60+30)
        s.append(f'<path d="M{cx} {cy} L{f(cx+r*math.cos(a1))} {f(cy+r*math.sin(a1))} A{r} {r} 0 0 1 {f(cx+r*math.cos(a2))} {f(cy+r*math.sin(a2))} Z" fill="{c}" fill-opacity=".85" stroke="#FFFFFF" stroke-width="2"/>')
        am=math.radians(-90+i*60); s.append(T(cx+(r+24)*math.cos(am),cy+(r+24)*math.sin(am)+7,mix=n,size=18))
    s.append(C(cx,cy,30,'#FFFFFF',0,'#FFFFFF'))
    s.append(f'<g data-anim="rot" data-from="-180" data-o="{cx},{cy}" data-dur="1.4">'+A(cx+52*math.cos(math.radians(150)),cy+52*math.sin(math.radians(150)),cx+52*math.cos(math.radians(-30)),cy+52*math.sin(math.radians(-30)),'ink',3)+A(cx+52*math.cos(math.radians(-30)),cy+52*math.sin(math.radians(-30)),cx+52*math.cos(math.radians(150)),cy+52*math.sin(math.radians(150)),'ink',3)+'</g>')
    s.append(T(130,274,mix='마주 보는 색 = 보색',size=18,fill=MUTED))
    return svg((260,284),240,'색상환: 마주 보는 색이 보색',s)
FIG['WHEEL']=wheel()

def spectrum():
    s=[]; ax=Ax(70,230,400,190,900,3.0,xmin=400)
    s.append(grid(ax,[400,500,600,700,800,900],[0,1,2,3]))
    s.append(ax.frame([400,500,600,700,800,900],[1,2,3],'','',grid=False)+T(ax.x0-10,ax.y0-2,tex='0',size=18,anchor='end'))
    s.append(L(ax.X(400),ax.Y(2),ax.X(900),ax.Y(2),MUTED,1.5,'6 4')+T(ax.X(410),ax.Y(2)-8,mix='측정 한계에 가까움',size=18,anchor='start',fill=MUTED))
    for c,col,lab in ((0.5,CU,'0.5 M'),(0.1,FIELD,'0.1 M')):
        s.append('<g data-anim="draw" data-dur="1.4">'+ax.curve(lambda l:obs(c*eps(l)),400,900,col=col,w=3)+'</g>')
    s.append(T(ax.X(760),ax.Y(2.7)-8,mix='0.5 M',size=18,fill=CU)+T(ax.X(820),ax.Y(1.12)-12,mix='0.1 M',size=18,fill=FIELD))
    s.append(T(470,286,mix='파장 (nm)',size=19,anchor='end',fill=MUTED)+T(80,26,mix='흡광도',size=19,anchor='start',fill=MUTED))
    return svg((490,296),470,'황산 구리 수용액의 파장별 흡광도',s)
FIG['SPECTRUM']=spectrum()

def cal(lam,col,k=None):
    s=[]; ax=Ax(70,220,300,180,0.55,3.0)
    s.append(grid(ax,[0,0.1,0.2,0.3,0.4,0.5],[0,1,2,3]))
    s.append(ax.frame([0,0.1,0.2,0.3,0.4,0.5],[1,2,3],'','',xfmt=lambda v:('0' if v==0 else f'{v:.1f}'),grid=False))
    pts=[(c,obs(c*eps(lam))) for c in (0.1,0.2,0.3,0.4,0.5)]
    if k: s.append('<g data-anim="draw" data-dur="1.2">'+P([(ax.X(0),ax.Y(0)),(ax.X(0.55),ax.Y(0.55*k))],FIELD,3)+'</g>')
    else: s.append(L(ax.X(0),ax.Y(0),ax.X(0.25),ax.Y(0.25*eps(lam)),MUTED,2,'6 4')+T(ax.X(0.27),ax.Y(2.95),mix='비례라면',size=18,anchor='start',fill=MUTED))
    for i,(c,a) in enumerate(pts): s.append(f'<g data-anim="pop" data-o="{f(ax.X(c))},{f(ax.Y(a))}" data-delay="{f(.12*i)}">'+C(ax.X(c),ax.Y(a),6,col,2.5,'#FFFFFF')+'</g>')
    if k:
        a=obs(0.26*eps(lam)); s.append(f'<g class="step" data-g="unk">'+L(ax.X(0),ax.Y(a),ax.X(0.26),ax.Y(a),PLUS,1.8,'5 4')+L(ax.X(0.26),ax.Y(a),ax.X(0.26),ax.Y(0),PLUS,1.8,'5 4')+f'<path d="M{f(ax.X(.26))} {f(ax.Y(a)-8)} l8 8 l-8 8 l-8 -8 Z" fill="{PLUS}"/>'+T(ax.X(0.26)+10,ax.Y(a)-12,mix='미지 0.69',size=18,anchor='start',fill=PLUS,halo=True)+'</g>')
    s.append(T(370,276,mix='농도 (M)',size=19,anchor='end',fill=MUTED)+T(80,22,mix=f'흡광도 ({lam} nm)',size=19,anchor='start',fill=col))
    return svg((390,286),380,f'{lam} nm에서 흡광도와 농도',s)
FIG['CAL600']=cal(600,FIELD,2.63); FIG['CAL800']=cal(800,EQUI)

# ═════════ b ═════════
def crystal(x0,y0,n=5,m=3,step=26,anim=False):
    s=[]
    for i in range(n):
        for j in range(m):
            s.append(ion(x0+i*step,y0+j*step,'+' if (i+j)%2==0 else '-',10))
    return ''.join(s)
def cover_b():
    s=[R(30,30,360,250,INK,3,'#EAF4FB',10)]
    s.append(crystal(120,200,7,3))
    s.append(f'<g data-anim="move" data-from="-40,60" data-dur="1.6" data-rep="loop">'+ion(150,110,'+',10)+'</g>')
    s.append(f'<g data-anim="move" data-from="40,60" data-dur="1.6" data-rep="loop" data-delay=".8">'+ion(290,90,'-',10)+'</g>')
    rnd=random.Random(3)
    for i in range(16): s.append(wdot(rnd.uniform(50,370),rnd.uniform(50,170),6))
    ax=Ax(60,520,330,170,110,110,xmin=60)
    s.append(L(60,520,400,520,MUTED,2)+L(60,520,60,340,MUTED,2)+L(60,ax.Y(101.3),395,ax.Y(101.3),MUTED,1.5,'5 4'))
    s.append('<g data-anim="draw" data-dur="1.4">'+ax.curve(lambda t:pw(t),60,100.5,col=MINUS,w=3.5)+'</g>')
    s.append('<g data-anim="draw" data-dur="1.4" data-delay=".4">'+ax.curve(lambda t:pw(t-6)*0.94,66,106,col=EQUI,w=3.5,dash='8 5')+'</g>')
    s.append(T(395,546,mix='온도',size=19,anchor='end',fill=MUTED)+T(70,336,mix='증기압',size=19,anchor='start',fill=MUTED))
    s.append(T(244,404,mix='물',size=19,fill=MINUS,anchor='end')+T(330,470,mix='용액',size=19,fill=EQUI))
    return svg((430,560),400,'소금 결정이 물에 녹는 모습과 물·용액의 증기압 곡선',s,'fig cover-fig')
FIG['COVER_B']=cover_b()

def sols():
    s=[]
    items=(('설탕물','고체 용질',WATER,'#FFFFFF'),('에탄올 수용액','액체 용질',WATER,None),('탄산수','기체 용질',WATER,'gas'),('물 + 식용유','섞이지 않음',WATER,'oil'))
    for i,(n,k,fill,typ) in enumerate(items):
        x=20+i*150
        s.append(beaker(x,60,100,120,fill,.75))
        if typ=='gas':
            for j,(dx,dy) in enumerate(((30,140),(60,120),(45,100),(75,150))):
                s.append(f'<g data-anim="move" data-from="0,30" data-rep="loop" data-dur="{f(1.2+.2*j)}">'+C(x+dx,60+dy-40,4,GLASS,1.2,'#FFFFFF')+'</g>')
        if typ=='oil': s.append(R(x,90,100,22,'none',0,'#F3D27A')+L(x,112,x+100,112,'#C9A43A',1.5))
        s.append(T(x+50,214,mix=n,size=19,weight=700)+T(x+50,240,mix=k,size=18,fill=MUTED))
    return svg((610,250),600,'설탕물, 에탄올 수용액, 탄산수, 물과 식용유',s)
FIG['SOLS']=sols()

def dyn(k):
    s=[R(10,10,220,170,INK,2,'#EAF4FB',6)]
    s.append(crystal(48,128,7,2,24))
    rnd=random.Random(10+k); nfree=(2,6,8)[k-1]
    for i in range(nfree):
        x=rnd.uniform(30,210); y=rnd.uniform(28,96)
        s.append(ion(x,y,'+' if i%2==0 else '-',9))
    if k>=1: s.append(f'<g data-anim="move" data-from="0,26" data-dur="1.2" data-rep="loop">'+A(84,110,84,70,'field',3)+'</g>')
    if k>=2: s.append(f'<g data-anim="move" data-from="0,-26" data-dur="1.2" data-rep="loop" data-delay=".6">'+A(170,62,170,104,'bfield',3 if k==3 else 2)+'</g>')
    return svg((240,190),220,f'소금의 용해와 석출 {k}단계',s)
for k in (1,2,3): FIG[f'DYN{k}']=dyn(k)

def soda():
    s=[P([(70,20),(150,20),(150,40),(170,70),(170,250),(50,250),(50,70),(70,40)],GLASS,2.5,'none',close=True)]
    s.append(P([(52,110),(168,110),(168,248),(52,248)],'none',0,WATER,close=True))
    rnd=random.Random(6)
    for i in range(10):
        x=rnd.uniform(62,158); y=rnd.uniform(124,240)
        s.append(f'<g data-anim="move" data-from="0,{f(rnd.uniform(20,50))}" data-rep="loop" data-dur="{f(1.2+rnd.random())}">'+C(x,y,4,GLASS,1.2,'#FFFFFF')+'</g>')
    for i in range(5): s.append(C(rnd.uniform(70,150),rnd.uniform(50,100),6,GAS_S,1.5,GAS))
    s.append(T(110,280,mix='$\\ce{CO2(g) <=> CO2(aq)}$',size=19))
    s.append(C(196,70,6,GAS_S,1.5,GAS)+T(206,78,mix='$\\ce{CO2}$',size=21,anchor='start'))
    return svg((250,292),220,'탄산수: 물에 녹은 이산화 탄소와 위쪽 기체',s)
FIG['SODA']=soda()

def crack():
    s=[]
    s.append('<path d="M40 60 L130 60 L130 150 L70 150 L40 120 Z" fill="#F4F6F8" stroke="#16233D" stroke-width="2.5"/>')
    s.append(A(150,105,200,105,'ink',3)+T(175,88,mix='며칠 뒤',size=18))
    s.append('<g class="step" data-g="cr">'+R(220,60,90,90,INK,2.5,'#F4F6F8')+T(265,178,mix='모양이 바뀐다',size=18,fill=FIELD)+'</g>')
    s.append(T(85,178,mix='깨진 결정',size=18))
    return svg((330,190),320,'포화 용액 속 깨진 소금 결정',s)
FIG['CRACK']=crack()

def dhsol():
    s=[]
    def blk(x,y,col,n=3,m=2,gap=24,loose=False,seed=1):
        rnd=random.Random(seed); o=[]
        for i in range(n):
            for j in range(m):
                dx=rnd.uniform(-6,6) if loose else 0; dy=rnd.uniform(-6,6) if loose else 0
                o.append(C(x+i*gap*(1.6 if loose else 1)+dx,y+j*gap*(1.6 if loose else 1)+dy,10,col,0,col))
        return ''.join(o)
    s.append(blk(40,50,MINUS)+T(64,124,mix='용질',size=19))
    s.append(A(110,62,176,62,'minus',3)+T(143,48,mix='팽창 $\\Delta H_1$',size=18))
    s.append(f'<g data-anim="move" data-from="-110,0" data-dur="1.2">'+blk(196,40,MINUS,loose=True,seed=2)+'</g>'+T(240,124,mix='팽창된 용질',size=19))
    s.append(blk(40,190,PLUS,4,2)+T(76,264,mix='용매',size=19))
    s.append(A(134,202,176,202,'plus',3)+T(155,166,mix='팽창 $\\Delta H_2$',size=18))
    s.append(f'<g data-anim="move" data-from="-110,0" data-dur="1.2" data-delay=".3">'+blk(196,180,PLUS,4,2,loose=True,seed=3)+'</g>'+T(260,264,mix='팽창된 용매',size=19))
    s.append(P([(330,80),(370,140),(330,210)],INK,2.5)+A(370,140,440,140,'bfield',3)+T(372,174,mix='혼합 $\\Delta H_3$',size=18,anchor='start'))
    rnd=random.Random(7); pts=[]
    while len(pts)<14:
        p=(rnd.uniform(470,580),rnd.uniform(70,220))
        if all(math.hypot(p[0]-a,p[1]-b)>24 for a,b in pts): pts.append(p)
    s.append(f'<g data-anim="fade" data-delay="1.2">'+''.join(C(x,y,10,MINUS if i<5 else PLUS,0,MINUS if i<5 else PLUS) for i,(x,y) in enumerate(pts))+'</g>')
    s.append(T(525,264,mix='용액',size=19))
    return svg((600,280),590,'용액 형성의 세 단계: 용질 팽창, 용매 팽창, 혼합',s)
FIG['DHSOL']=dhsol()

def dhlev(exo):
    s=[L(40,250,40,30,MUTED,2)+T(20,30,mix='$H$',size=20,anchor='start',fill=MUTED)]
    y0=180; ytop=60; ysol=230 if exo else 150
    s.append(L(60,y0,200,y0,INK,2.5,'6 4')+T(130,y0+24,mix='용매 + 용질',size=18))
    s.append(L(110,ytop,250,ytop,INK,2.5)+T(180,ytop-10,mix='팽창된 용매·용질',size=18))
    s.append(L(220,ysol,330,ysol,INK,2.5)+T(275,ysol+(24 if exo else -10),mix='용액',size=18))
    s.append(A(130,y0,130,ytop+4,'ink',2.5)+T(124,128,mix='$\\Delta H_1+\\Delta H_2$',size=18,anchor='end'))
    s.append(A(250,ytop,250,ysol-4,'ink',2.5)+T(258,(ytop+ysol)/2,mix='$\\Delta H_3$',size=18,anchor='start'))
    s.append(f'<g class="step" data-g="dh{int(exo)}">'+A(200,y0,200,ysol-(4 if exo else -4),'ink',3.5)+T(206 if not exo else 190,ysol+(30 if exo else 28),mix='$\\Delta H_\\text{용해}$',size=18,anchor='middle',fill=INK,halo=True)+'</g>')
    s.append(T(185,286 if exo else 286,mix='(가) 발열 용해' if exo else '(나) 흡열 용해',size=19,weight=700))
    return svg((350,296),330,'용해 과정의 엔탈피 변화 '+('발열' if exo else '흡열'),s)
FIG['DHEXO']=dhlev(True); FIG['DHENDO']=dhlev(False)

def iodine():
    s=[]
    for j,(lab,top,bot) in enumerate((('흔들기 전','#FBFBFB',WATER),('흔든 뒤','#B98AD8',WATER))):
        x=40+j*170
        s.append(f'<path d="M{x} 20 L{x} 200 A30 30 0 0 0 {x+60} 200 L{x+60} 20" fill="none" stroke="{GLASS}" stroke-width="2.5"/>')
        g=f'<g data-anim="fade" data-dur="1.4" data-delay=".5">' if j==1 else '<g>'
        s.append(g+R(x+2,60,56,60,'none',0,top)+'</g>')
        s.append(f'<path d="M{x+2} 120 L{x+2} 200 A28 28 0 0 0 {x+58} 200 L{x+58} 120 Z" fill="{bot if j else "#E9D2A6"}"/>')
        s.append(T(x+30,262,mix=lab,size=19,weight=700))
    s.append(T(260,84,mix='헥세인',size=18,anchor='start')+T(260,176,mix='물',size=18,anchor='start'))
    return svg((330,272),300,'아이오딘을 녹인 물과 헥세인을 흔들기 전과 뒤',s)
FIG['IODINE']=iodine()

def micelle():
    s=[]
    # 비누 분자 하나
    pts=[(30+i*18,60+(8 if i%2 else 0)) for i in range(10)]
    s.append(P(pts,INK,3)+ion(222,64,'-',12)+ion(250,40,'+',9))
    s.append(T(110,30,mix='무극성 꼬리',size=18)+T(226,100,mix='이온 머리',size=18)+T(266,46,mix='$\\ce{Na+}$',size=18,anchor='start'))
    cx,cy=430,150
    s.append(f'<g data-anim="scale" data-from=".3" data-o="{cx},{cy}" data-dur="1.2">'+C(cx,cy,40,'#C9A43A',0,'#F3D27A')+'</g>')
    s.append(T(cx,cy+6,mix='기름때',size=18))
    s.append(f'<g data-anim="rot" data-from="-30" data-o="{cx},{cy}" data-dur="1.6">')
    for k in range(14):
        a=2*math.pi*k/14; x1,y1=cx+44*math.cos(a),cy+44*math.sin(a); x2,y2=cx+92*math.cos(a),cy+92*math.sin(a)
        s.append(L(x1,y1,x2,y2,INK,2.5)+C(cx+102*math.cos(a),cy+102*math.sin(a),9,MINUS,2,'#FFFFFF'))
    s.append('</g>')
    s.append(T(cx,282,mix='마이셀(꼬리는 안쪽, 머리는 물 쪽)',size=18,fill=MUTED))
    return svg((560,292),540,'비누 분자와 기름때를 둘러싼 마이셀',s)
FIG['MICELLE']=micelle()

def solcurve():
    s=[]; ax=Ax(64,230,240,190,80,180)
    xt=[0,20,40,60,80]; yt=[0,60,120,180]
    s.append(grid(ax,xt,yt)+ax.frame(xt,yt,'','',grid=False))
    K=[(0,13.3),(20,31.6),(40,63.9),(60,110),(80,169)]; N=[(0,35.7),(20,36.0),(40,36.6),(60,37.3),(80,38.4)]
    s.append('<g data-anim="draw" data-dur="1.4">'+P([(ax.X(t),ax.Y(v)) for t,v in K],BF,3)+'</g>'+P([(ax.X(t),ax.Y(v)) for t,v in N],RD,3,dash='8 5'))
    s.append(T(ax.X(62),ax.Y(150),mix='$\\ce{KNO3}$',size=19,fill=BF,anchor='end')+T(ax.X(70),ax.Y(37)-12,mix='$\\ce{NaCl}$',size=19,fill=RD))
    s.append(T(310,286,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)+T(74,24,mix='용해도 (g/물 100 g)',size=19,anchor='start',fill=MUTED))
    ox=360; ax2=Ax(ox+50,230,220,190,40,16)
    s.append(grid(ax2,[0,10,20,30,40],[0,4,8,12,16])+ax2.frame([0,10,20,30,40],[0,4,8,12,16],'','',grid=False))
    O=[(0,14.6),(10,11.3),(20,9.1),(30,7.6),(40,6.4)]
    s.append('<g data-anim="draw" data-dur="1.4" data-delay=".3">'+P([(ax2.X(t),ax2.Y(v)) for t,v in O],MINUS,3)+'</g>')
    s.append(T(ax2.X(40),ax2.Y(14.5),mix='산소(공기와 평형)',size=18,fill=MINUS,anchor='end'))
    s.append(T(ox+275,286,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)+T(ox+60,24,mix='용해도 (mg/L)',size=19,anchor='start',fill=MUTED))
    return svg((650,296),640,'온도에 따른 질산 칼륨·염화 나트륨과 산소의 용해도',s)
FIG['SOLCURVE']=solcurve()

def sizeband():
    s=[L(40,60,600,60,MUTED,3)]
    for x,lab in ((60,'참용액'),(320,'콜로이드'),(540,'현탁액')):
        s.append(T(x if x!=320 else 320,40,mix=lab,size=20,weight=700,anchor='middle'))
    s.append(R(200,52,240,16,'none',0,'#FFE45C',extra='fill-opacity=".6"'))
    for x,lab in ((200,'1 nm'),(440,'1 μm')): s.append(L(x,50,x,72,INK,2)+T(x,98,mix=lab,size=19))
    s.append(T(320,124,mix='입자 지름 (로그 눈금, 대략)',size=18,fill=MUTED))
    return svg((640,134),600,'참용액, 콜로이드, 현탁액의 입자 크기',s)
FIG['SIZEBAND']=sizeband()

def tyndall():
    s=[]
    s.append(R(10,96,60,28,INK,2,'#E6EAEE',4)+T(40,150,mix='레이저',size=18))
    s.append(L(70,110,560,110,LASER,2,'3 6'))
    for j,(x,fill,lab,vis) in enumerate(((110,'#E5F1FA','황산 구리 수용액(참용액)',False),(340,'#F6E6A8','은 나노 콜로이드',True))):
        s.append(beaker(x,40,160,130,fill,.85))
        if vis: s.append(f'<g data-anim="draw" data-dur="1">'+L(x+2,110,x+158,110,LASER,7,extra='stroke-opacity=".75"')+'</g>')
        s.append(T(x+80,206,mix=lab,size=18)+T(x+80,232,mix=('빛의 길이 안 보임' if not vis else '빛의 길이 보임(틴들)'),size=18,fill=(MUTED if not vis else PLUS)))
    return svg((580,244),560,'레이저 빛을 참용액과 콜로이드에 비춘 모습',s)
FIG['TYNDALL']=tyndall()

def brown():
    s=[C(110,110,96,INK,2.5,'#FFFBEA')]
    rnd=random.Random(12)
    for i in range(9):
        x=rnd.uniform(50,170); y=rnd.uniform(50,170)
        s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-14,14))},{f(rnd.uniform(-14,14))}" data-rep="alt" data-dur="{f(.6+rnd.random()*.5)}" data-ease="lin">'+C(x,y,5,'#8A6A1E',0,'#8A6A1E')+'</g>')
    s.append(T(110,236,mix='브라운 운동(현미경)',size=18))
    return svg((220,246),200,'콜로이드 입자의 불규칙한 브라운 운동',s)
FIG['BROWN']=brown()

def ag(k):
    s=[]
    if k==1:
        s.append(R(20,110,200,70,'none',0,'#E3EEFB')+L(20,110,220,110,MINUS,1.5)+beaker(70,60,100,110,WATER,.6))
        for x,y in ((40,140),(200,150),(36,170),(205,124)): s.append(R(x-7,y-7,14,14,'#9FC3DD',1.5,'#FFFFFF',3))
        s.append(T(120,214,mix='$\\ce{NaBH4}$ 0.002 M 30 mL',size=18)+T(120,238,mix='얼음물 중탕, 20분 교반',size=18,fill=MUTED))
    elif k==2:
        s.append(beaker(70,60,100,110,AGC,.6))
        s.append(R(112,0,14,40,GLASS,2,'#FFFFFF',3)+P([(112,40),(119,52),(126,40)],GLASS,2))
        s.append(f'<g data-anim="move" data-from="0,-30" data-rep="loop" data-dur="1">'+C(119,70,4,'#C9D2DB',0,'#C9D2DB')+'</g>')
        s.append(T(120,214,mix='$\\ce{AgNO3}$ 0.001 M 2 mL를',size=18)+T(120,238,mix='한 방울씩 → 노란 콜로이드',size=18,fill=MUTED))
    else:
        for i,col in enumerate((AGC,'#D9A24A','#7C7466')):
            x=30+i*62; s.append(R(x,90,50,50,GLASS,2,col,6))
            s.append(T(x+25,164,mix=('0','2','6')[i]+' 방울',size=18))
        s.append(T(120,214,mix='홈판에 나누어 1.5 M $\\ce{NaCl}$',size=18)+T(120,238,mix='→ 색 변화, 틴들 다시 확인',size=18,fill=MUTED))
    return svg((240,248),220,f'은 나노 콜로이드 실험 {k}단계',s)
for k in (1,2,3): FIG[f'AG{k}']=ag(k)

def vplmol():
    s=[]
    for j,(x0,lab) in enumerate(((10,'순수한 물'),(300,'용액'))):
        s.append(R(x0,10,260,210,INK,2.5,'#FFFFFF',6)+R(x0+2,100,256,118,'none',0,'#EAF4FB'))
        rnd=random.Random(20+j)
        for row in range(4):
            for i in range(9):
                x=x0+22+i*27+(12 if row%2 else 0); y=114+row*27
                if x>x0+246: continue
                sol=(j==1 and (row*9+i)%5==2)
                s.append(C(x,y,9,EQUI,1.5,'#FBD9A8') if sol else wdot(x,y,9))
        n=4 if j==0 else 2
        for k in range(n):
            x=x0+40+k*(180/(n)); s.append(f'<g data-anim="move" data-from="0,40" data-rep="loop" data-dur="1.6" data-delay="{f(.3*k)}">'+A(x,96,x,50,'field',3)+'</g>')
        for k in range(2):
            x=x0+180+k*40; s.append(A(x,40,x,88,'bfield',2.5))
        s.append(T(x0+130,248,mix=lab,size=20,weight=700))
    s.append(wdot(40,280,8)+T(54,286,mix='물 분자',size=18,anchor='start')+C(150,280,8,EQUI,1.5,'#FBD9A8')+T(164,286,mix='비휘발성 용질',size=18,anchor='start'))
    s.append(A(320,280,320,262,'field',2.5)+T(332,286,mix='증발',size=18,anchor='start',fill=FIELD)+A(400,262,400,280,'bfield',2.5)+T(412,286,mix='응축',size=18,anchor='start',fill=BF))
    return svg((570,296),560,'순수한 물과 용액 표면의 증발과 응축',s)
FIG['VPLMOL']=vplmol()

def raoult():
    s=[]; ax=Ax(70,230,320,190,1,1)
    xt=[0,.25,.5,.75,1]
    s.append(R(70,40,320,190,'none',0,'#FFF8E5')+grid(ax,xt,[0,.25,.5,.75,1],'#EAD9A8'))
    s.append(L(70,230,400,230,MUTED,2)+L(70,230,70,32,MUTED,2))
    for v in xt: s.append(L(ax.X(v),230,ax.X(v),236,MUTED,1.5)+T(ax.X(v),256,tex=('0' if v==0 else ('1' if v==1 else f'{v:g}')),size=18))
    s.append('<g data-anim="draw" data-dur="1.4">'+L(ax.X(0),ax.Y(0),ax.X(1),ax.Y(1),EQUI,4)+'</g>')
    s.append(L(64,ax.Y(1),70,ax.Y(1),MUTED,2)+T(ax.X(1)-16,ax.Y(1)+4,mix='$P_\\text{순수 용매}$',size=18,anchor='end',halo=True))
    for k,v in enumerate(xt):
        x0=ax.X(v)-15; y0=268; n=round(v*9)
        for c in range(9):
            col=PLUS if c<n else SOLUTE
            s.append(R(x0+(c%3)*10,y0+(c//3)*10,10,10,'#FFFFFF',1,col))
    s.append(T(390,330,mix='용매의 몰분율 $X_\\text{용매}$',size=19,anchor='end',fill=MUTED)+T(16,26,mix='증기 압력',size=19,anchor='start',fill=MUTED))
    return svg((420,340),400,'라울 법칙: 용매의 증기 압력은 용매의 몰분율에 비례',s)
FIG['RAOULT']=raoult()

def bpe():
    s=[]; ax=Ax(70,250,330,220,10,10)
    s.append(L(70,250,410,250,MUTED,2)+L(70,250,70,22,MUTED,2))
    f1=lambda x:0.09*x*x+0.4*x; f2=lambda x:0.09*(x-1.3)**2+0.4*(x-1.3)
    s.append('<g data-anim="draw" data-dur="1.3">'+ax.curve(f1,0,9.4,col=MINUS,w=3.5)+'</g>')
    s.append('<g data-anim="draw" data-dur="1.3" data-delay=".3">'+ax.curve(f2,1.3,10,col=PLUS,w=3.5,dash='9 5')+'</g>')
    y1=6.0; xb=(-0.4+math.sqrt(0.16+4*0.09*y1))/(0.18); xb2=xb+1.3
    s.append(L(70,ax.Y(y1),410,ax.Y(y1),MUTED,1.5,'6 4')+T(64,ax.Y(y1)+6,tex='1',size=18,anchor='end'))
    s.append(L(ax.X(xb),ax.Y(y1),ax.X(xb),250,MUTED,1.5,'4 4')+L(ax.X(xb2),ax.Y(y1),ax.X(xb2),250,MUTED,1.5,'4 4'))
    s.append(T(ax.X(xb),274,tex='T_\\mathrm{b}',size=19)+T(ax.X(xb2)+6,274,tex="T_\\mathrm{b}'",size=19))
    s.append(f'<g class="step" data-g="bpe1">'+A(ax.X(xb)-2,ax.Y(y1)-26,ax.X(xb2)+2,ax.Y(y1)-26,'ink',2.5)+T((ax.X(xb)+ax.X(xb2))/2,ax.Y(y1)-36,tex='\\Delta T_\\mathrm{b}',size=19,halo=True)+'</g>')
    yb=f2(xb)
    s.append(f'<g class="step" data-g="bpe2">'+A(ax.X(xb),ax.Y(y1)+2,ax.X(xb),ax.Y(yb)-2,'equi',2.5)+T(ax.X(xb)-10,(ax.Y(y1)+ax.Y(yb))/2+6,tex='\\Delta P',size=19,anchor='end',fill=EQUI,halo=True)+'</g>')
    s.append(T(150,ax.Y(f1(3.2))-12,mix='순수한 용매',size=18,fill=MINUS,anchor='end')+T(ax.X(6.5)+10,ax.Y(f2(6.5))+20,mix='용액 속 용매',size=18,fill=PLUS,anchor='start'))
    s.append(T(405,300,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)+T(16,18,mix='증기압 (atm)',size=19,anchor='start',fill=MUTED)+T(90,50,mix='크기 비례 아님',size=18,anchor='start',fill=MUTED))
    return svg((420,308),420,'순수한 용매와 용액의 증기압 곡선과 끓는점 오름',s)
FIG['BPE']=bpe()

def partic():
    s=[R(10,10,200,130,INK,2,'#FFFFFF',6),R(240,10,200,130,INK,2,'#FFFFFF',6)]
    rnd=random.Random(4)
    for x,y in ((60,50),(150,90),(100,110)): s.append(C(x,y,11,EQUI,1.5,'#FBD9A8'))
    for (x,y) in ((290,50),(380,90),(330,110)):
        s.append(f'<g data-anim="move" data-from="10,0" data-dur="1">'+ion(x,y,'+',10)+'</g>'+f'<g data-anim="move" data-from="-10,0" data-dur="1">'+ion(x+26,y,'-',10)+'</g>')
    s.append(T(110,170,mix='설탕 0.15 m: 입자 0.15 m',size=18)+T(340,170,mix='$\\ce{NaCl}$ 0.15 m:||입자 약 0.30 m',size=18))
    return svg((450,206),440,'설탕과 염화 나트륨 수용액 속 용질 입자 수',s)
FIG['PARTIC']=partic()

def app():
    s=[R(10,60,300,110,GLASS,2,'#FDE2E4',8)]
    s.append(R(50,96,180,36,GLASS,2.2,'#FFFFFF',3)+R(52,98,40,32,'none',0,WATER))
    for x,y in ((60,110),(80,120),(70,104)): s.append(C(x,y,3.5,EQUI,0,EQUI))
    s.append(R(220,92,10,44,INK,1.5,'#C9D2DB')+L(230,114,300,114,INK,4))
    rnd=random.Random(5)
    for i in range(8):
        s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-10,10))},{f(rnd.uniform(-6,6))}" data-rep="alt" data-dur="{f(.8+rnd.random()*.6)}">'+C(rnd.uniform(100,210),rnd.uniform(102,126),3.5,GRAV,1,'#E4E8EC')+'</g>')
    s.append(P([(50,114),(30,114),(30,30),(380,30),(380,40)],MUTED,3))
    s.append(C(380,82,40,INK,2.5,'#FFFFFF')+L(380,82,404,64,PLUS,3)+T(380,112,mix='kPa',size=18,fill=MUTED))
    s.append(L(270,40,270,150,GLASS,4)+C(270,152,6,PLUS,0,PLUS)+T(276,58,mix='온도계',size=18,anchor='start'))
    s.append(T(160,196,mix='물중탕(20–80 °C)',size=18)+T(140,90,mix='용액',size=18,fill=MINUS))
    return svg((440,206),420,'물중탕 속 주사기와 압력계로 용액의 증기 압력 측정',s)
FIG['APP']=app()

VT=[20,30,40,50,60,70,80]
def xs(i,m=0.15): return i*m/(i*m+55.51)
def vplres():
    s=[]; ax=Ax(64,220,300,190,85,50,xmin=15)
    s.append(grid(ax,VT,[0,10,20,30,40,50])+ax.frame(VT,[0,10,20,30,40,50],'','',grid=False))
    for i,col,dash in ((0,MINUS,None),(1,FIELD,None),(1.9,PLUS,'7 4')):
        g=lambda t,i=i:pw(t)*(1-xs(i))
        s.append(f'<g data-anim="draw" data-dur="1.3">'+P([(ax.X(t),ax.Y(g(t))) for t in VT],col,2.5,dash=dash)+'</g>')
    s.append(T(ax.X(62),ax.Y(40),mix='세 곡선이 거의 겹친다',size=18,fill=MUTED,anchor='end'))
    s.append(T(364,276,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)+T(74,22,mix='증기 압력 (kPa)',size=19,anchor='start',fill=MUTED))
    ox=400; ax2=Ax(ox+60,220,200,190,85,0.3,xmin=15)
    s.append(grid(ax2,VT,[0,.1,.2,.3])+ax2.frame([20,40,60,80],[0,.1,.2,.3],'','',yfmt=lambda v:('0' if v==0 else f'{v:.1f}'),grid=False))
    for i,col,lab in ((1,FIELD,'설탕'),(1.9,PLUS,'$\\ce{NaCl}$')):
        pts=[(ax2.X(t),ax2.Y(pw(t)*xs(i))) for t in VT]
        s.append(f'<g data-anim="draw" data-dur="1.3" data-delay=".3">'+P(pts,col,3)+'</g>'+T(pts[-1][0]-6,pts[-1][1]-12,mix=lab,size=18,fill=col,anchor='end'))
    s.append(T(ox+265,276,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)+T(ox+70,22,mix='$\\Delta P$ (kPa)',size=19,anchor='start',fill=MUTED))
    return svg((680,286),660,'물·설탕 수용액·염화 나트륨 수용액의 증기 압력과 증기 압력 내림',s)
FIG['VPLRES']=vplres()

def q4cyc():
    s=[L(60,60,200,60,INK,2.5)+T(130,46,mix='$\\ce{Na+(g) + Cl-(g)}$',size=18)]
    s.append(L(20,200,150,200,INK,2.5)+T(70,226,mix='$\\ce{NaCl(s)}$',size=18))
    s.append(L(150,190,290,190,INK,2.5)+T(232,216,mix='$\\ce{Na+(aq) + Cl-(aq)}$',size=18))
    s.append(A(70,198,70,64,'plus',3)+T(64,130,mix='786',size=18,anchor='end',fill=PLUS))
    s.append(A(200,64,200,186,'minus',3)+T(206,130,mix='−783',size=18,anchor='start',fill=MINUS))
    s.append(f'<g class="step" data-g="q4">'+A(150,200,150,192,'ink',2)+T(160,176,mix='+3',size=18,anchor='start')+'</g>')
    s.append(T(150,262,mix='(kJ/mol, 크기 비례 아님)',size=18,fill=MUTED))
    return svg((340,272),310,'염화 나트륨 용해의 엔탈피 순환',s)
FIG['Q4CYC']=q4cyc()

def q5line():
    s=[]; ax=Ax(70,230,300,190,1,600)
    s.append(grid(ax,[0,.2,.4,.6,.8,1],[0,200,400,600])+ax.frame([0,.2,.4,.6,.8,1],[0,200,400,600],'','',xfmt=lambda v:('0' if v==0 else ('1' if v==1 else f'{v:.1f}')),grid=False))
    s.append(L(ax.X(0),ax.Y(0),ax.X(1),ax.Y(515),FIELD,2.5)+L(ax.X(0),ax.Y(332),ax.X(1),ax.Y(0),EQUI,2.5)+'<g data-anim="draw" data-dur="1.3">'+L(ax.X(0),ax.Y(332),ax.X(1),ax.Y(515),INK,3)+'</g>')
    s.append(f'<g class="step" data-g="q5">'+L(ax.X(.6),ax.Y(0),ax.X(.6),ax.Y(442),PLUS,1.8,'5 4')+C(ax.X(.6),ax.Y(442),6,PLUS,0,PLUS)+T(ax.X(.6)-8,ax.Y(442)-12,mix='442',size=18,fill=PLUS,anchor='end',halo=True)+'</g>')
    s.append(T(ax.X(.95),ax.Y(515)-12,mix='$P_{\\ce{CS2}}$',size=18,fill=FIELD,anchor='end')+T(ax.X(.62),ax.Y(175),mix='$P_\\text{아세톤}$',size=18,fill=EQUI,anchor='start')+T(ax.X(.18),ax.Y(445),mix='$P_\\text{전체}$',size=18,anchor='middle'))
    s.append(T(370,286,mix='$X_{\\ce{CS2}}$',size=19,anchor='end',fill=MUTED)+T(80,22,mix='증기압 (mmHg)',size=19,anchor='start',fill=MUTED))
    return svg((390,296),380,'이황화 탄소–아세톤 혼합 용액의 부분 압력과 전체 증기압(이상 용액)',s)
FIG['Q5LINE']=q5line()

# ═════════ 출력 ═════════
for d in 'ab':
    tpl=open(os.path.join(HERE,f'tpl_{d}.html'),encoding='utf-8').read()
    def rep(m):
        k=m.group(1)
        if k not in FIG: sys.exit('no fig '+k)
        return FIG[k]
    out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
    open(OUT[d]+'slides.html','w',encoding='utf-8').write(out)
    for src,dst in (('labs_src.js','labs.js'),('extra_src.css','extra.css')):
        if os.path.exists(os.path.join(HERE,src)): shutil.copy(os.path.join(HERE,src),OUT[d]+dst)
    print('ok',d,len(out))
