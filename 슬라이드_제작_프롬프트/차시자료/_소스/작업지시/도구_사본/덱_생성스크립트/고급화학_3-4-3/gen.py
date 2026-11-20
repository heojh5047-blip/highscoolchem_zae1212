# -*- coding: utf-8 -*-
"""고급화학 3-4-3 실용 전지 — 그림 생성. tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   extra_src.css → extra.css, meta.json.  python3 -I gen.py  (출력 OUT — 이 덱 폴더만, assert로 막음)."""
import math, re, sys, os, shutil, json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cellh import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FD='3-4-3_실용_전지'; OUT=BASE+FD+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-4-3_실용_전지/', OUT
assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FD), OUT
FIG={}
CAN='#B7C0C9'; GRAPH='#2B2F35'; PASTE='#7A5C4E'; PB='#8E99A6'; PBO2='#5A3A2A'; ACID='#EEF6FB'; SEPF='#FFF4E8'
def flow(d,speed=32): return f'<path d="{d}" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="{speed}"/>'
def lead_line(x1,y1,x2,y2): return L(x1,y1,x2,y2,MUTED,1.5)

# 1 표지 — 1차·2차·연료 전지
def cover():
    s=[]
    # 알칼리 전지(1차)
    s.append(R(100,156,56,190,INK,3,CAN,10)+R(116,142,24,14,INK,2,CAN,3)+R(108,168,40,166,MUTED,0,'#E6E9ED',6))
    s.append(T(128,200,mix='+',size=24,weight=700)+T(128,320,mix='−',size=26,weight=700)+T(128,262,mix='1.55 V',size=19,weight=700))
    # 리튬-이온 파우치(2차) + 방전/충전
    s.append(R(205,150,74,150,INK,3,'#E9E4F3',8)+P([(250,175),(232,228),(248,228),(236,276),(262,214),(246,214),(258,175)],EQUI,2,'#FFE45C',close=True))
    s.append(an('draw',f'<path d="M206 316 Q242 350 278 316" fill="none" stroke="{FIELD}" stroke-width="3"/>'+A(270,322,280,312,'field',3),dur='1'))
    s.append(an('draw',f'<path d="M278 136 Q242 102 206 136" fill="none" stroke="{BF}" stroke-width="3"/>'+A(214,130,204,140,'bfield',3),dur='1',delay='.6'))
    s.append(T(242,96,mix='충전',size=19,fill=BF,weight=700)+T(242,368,mix='방전',size=19,fill=FIELD,weight=700))
    # 연료 전지
    s.append(R(318,180,14,120,INK,2,'#B8BEC6',2)+R(332,180,26,120,FIELD,1.5,'#E8F5EE')+R(358,180,14,120,INK,2,'#B8BEC6',2))
    s.append(an('move',A(325,130,325,172,'minus',3),**{'from':'0,-14','dur':'1.2','rep':'loop','ease':'lin'}))
    s.append(an('move',A(365,130,365,172,'plus',3),**{'from':'0,-14','dur':'1.2','rep':'loop','ease':'lin','delay':'.4'}))
    s.append(T(318,122,tex=r'\ce{H2}',size=19,fill=MINUS,anchor='end')+T(372,122,tex=r'\ce{O2}',size=19,fill=PLUS,anchor='start'))
    s.append(A(365,306,365,336,'muted',3)+T(372,334,tex=r'\ce{H2O}',size=19,anchor='start'))
    s.append(T(128,404,mix='1차 전지',size=20,weight=700)+T(242,404,mix='2차 전지',size=20,weight=700)+T(345,404,mix='연료 전지',size=20,weight=700))
    return svg((480,480),500,'일회용 알칼리 전지, 방전과 충전을 되풀이하는 리튬-이온 전지, 수소와 산소를 공급받는 연료 전지',s,'fig cover-fig')
FIG['COVER']=cover()
FIG['REVIEW']=cellsvg('다니엘 전지: 아연 전극이 산화 전극, 구리 전극이 환원 전극이고 염다리 이온이 전하 균형을 유지한다',width=460,
    ions=(r'\ce{SO4^2-}',r'\ce{Na+}'),reading='1.10 V')

# 4 생각 열기 — 기기와 전지
def devices():
    s=[]
    cells=[(80,'리모컨','알칼리 전지'),(260,'손목시계','은 단추 전지'),(440,'스마트폰','리튬-이온 전지')]
    def remote(x,y): return R(x-16,y,32,76,INK,2.5,'#FFFFFF',8)+C(x,y+16,5,PLUS,0,PLUS)+''.join(C(x-7+14*(i%2),y+34+14*(i//2),4,MUTED,0,MUTED) for i in range(4))
    def watch(x,y): return R(x-12,y,24,16,MUTED,2,'#E6E9ED',3)+R(x-12,y+60,24,16,MUTED,2,'#E6E9ED',3)+C(x,y+38,26,INK,2.5,'#FFFFFF')+L(x,y+38,x,y+22,INK,2.5)+L(x,y+38,x+12,y+44,INK,2)
    def phone(x,y): return R(x-22,y,44,76,INK,2.5,'#FFFFFF',8)+R(x-16,y+8,32,54,MUTED,1.5,'#E3EEFB',3)+C(x,y+69,3,MUTED,0,MUTED)
    def car(x,y,h2=False):
        o=P([(x-60,y+56),(x-52,y+28),(x-26,y+12),(x+22,y+12),(x+44,y+30),(x+60,y+34),(x+60,y+56)],INK,2.5,'#FFFFFF',close=True)+C(x-34,y+58,12,INK,2.5,'#B7C0C9')+C(x+36,y+58,12,INK,2.5,'#B7C0C9')
        if h2: o+=R(x-14,y+22,30,20,FIELD,1.5,'#E8F5EE',4)+T(x+1,y+38,tex=r'\ce{H2}',size=19,fill=FIELD)
        else: o+=R(x-16,y+30,30,18,INK,1.5,'#E6E9ED',2)
        return o
    icons=[remote(80,26),watch(260,24),phone(440,26),car(160,180),car(360,180,True)]
    names=[(80,128,'리모컨'),(260,128,'손목시계'),(440,128,'스마트폰'),(160,282,'자동차 시동'),(360,282,'수소 자동차')]
    types=[(80,156,'알칼리 전지'),(260,156,'은 단추 전지'),(440,156,'리튬-이온 전지'),(160,310,'납-산 전지'),(360,310,'수소 연료 전지')]
    for i,ic in enumerate(icons):
        cx=names[i][0]; s.append(an('pop',ic,dur='.5',delay=f(.15*i),o=f'{cx},{60 if i<3 else 214}'))
    for x,y,t in names: s.append(T(x,y,mix=t,size=19))
    s.append(step('g1',''.join(T(x,y,mix=t,size=19,weight=700,fill=OX) for x,y,t in types)))
    return svg((520,324),500,'리모컨, 손목시계, 스마트폰, 자동차, 수소 자동차에 쓰이는 전지',s)
FIG['DEVICES']=devices()

# 5 분류 그림
def classes():
    s=[]
    def box(x,y,w,t,col=INK,fill='#FFFFFF'): return R(x,y,w,40,col,2,fill,8)+T(x+w/2,y+27,mix=t,size=19)
    # 1차
    s.append(T(10,26,mix='1차 전지',size=20,weight=700,anchor='start'))
    s.append(box(10,40,110,'반응물')+box(220,40,110,'생성물'))
    s.append(an('draw',A(126,60,214,60,'field',3),dur='.8')+T(170,50,mix='방전',size=18,fill=FIELD,halo=True))
    s.append(T(380,68,mix='✕ 끝',size=19,fill=PLUS,weight=700))
    # 2차
    s.append(T(10,146,mix='2차 전지',size=20,weight=700,anchor='start'))
    s.append(box(10,160,110,'반응물')+box(220,160,110,'생성물'))
    s.append(an('draw',A(126,172,214,172,'field',3),dur='.8',delay='.3')+T(170,160,mix='방전',size=18,fill=FIELD,halo=True))
    s.append(an('draw',A(214,190,126,190,'bfield',3),dur='.8',delay='.6')+T(170,218,mix='충전',size=18,fill=BF,halo=True))
    s.append(T(392,188,mix='반복',size=19,fill=FIELD,weight=700))
    # 연료
    s.append(T(10,270,mix='연료 전지',size=20,weight=700,anchor='start'))
    s.append(box(150,286,110,'전지',INK,'#E8F5EE'))
    s.append(an('draw',A(30,306,144,306,'minus',3),dur='.8',delay='.9')+T(30,296,mix='연료·산화제',size=18,anchor='start',halo=True))
    s.append(an('draw',A(266,306,380,306,'muted',3),dur='.8',delay='1.1')+T(380,296,mix='생성물',size=18,anchor='end',halo=True))
    s.append(T(205,356,mix='공급하는 한 계속 전기를 만든다',size=18,fill=FIELD))
    return svg((420,366),420,'1차 전지는 방전으로 끝나고, 2차 전지는 방전과 충전을 되풀이하며, 연료 전지는 연료와 산화제를 공급받는 한 계속 작동한다',s)
FIG['CLASS']=classes()

# 6 알칼리 전지 구조 (그림 Ⅲ-28을 새로 그림)
def alk():
    s=[]
    s.append(circ([["wire",[[170,40],[170,22],[40,22],[40,202]]],["bulb",[40,220],{"r":16,"on":True}],["wire",[[40,238],[40,412],[170,412],[170,398]]]]))
    s.append(flow('M170 398 V412 H40 V238 M40 202 V22 H170 V40',30))
    s.append(A(58,340,58,280,'minus',3)+T(66,318,tex='e^-',size=19,fill=MINUS,anchor='start'))
    s.append(R(90,60,160,322,INK,3,CAN,14))                      # 철통
    s.append(R(150,40,40,22,INK,2,CAN,4))                        # (+)극 버튼
    s.append(R(100,382,140,16,INK,2,'#8C99A6',4))                # (−)극 캡
    s.append(R(100,72,140,302,OX,2,MET['Zn'][0],6))              # 아연(산화 전극)
    s.append(R(112,84,116,278,EQUI,2,SEPF,4,dash='6 4'))         # 흡착제/격리판
    s.append(R(119,90,102,266,'none',0,PASTE,3))                 # MnO2 반죽
    s.append(R(161,52,18,290,RD,2,GRAPH,3))                      # 흑연 봉
    x=272
    labs=[(50,'(+)극 버튼',None,(190,51)),(100,'철통',None,(250,100)),(150,'$\\ce{KOH}$ 반죽에 있는 $\\ce{MnO2}$',None,(212,150)),
          (210,'$\\ce{Zn}$(산화 전극)',OX,(238,210)),(262,'흑연 봉(환원 전극)',RD,(178,262)),(314,'흡착제/격리판',EQUI,(226,314)),(392,'(−)극 캡',None,(240,390))]
    for y,t,c,(px,py) in labs:
        s.append(lead_line(x-4,y-6,px,py)+T(x,y,mix=t,size=19,anchor='start',fill=c,weight=(700 if c else None)))
    return svg((490,428),460,'알칼리 전지 단면: 철통 안에 아연(산화 전극), 격리판, 수산화 칼륨 반죽 속 이산화 망가니즈, 가운데 흑연 봉(환원 전극)이 있고 전자는 (−)극 캡에서 바깥 도선을 지나 (+)극 버튼으로 흐른다',s)
FIG['ALK']=alk()

# 7 OH- 순환
def alkion():
    s=[R(20,70,380,180,'#9FC3DD',1.5,ACID,8)]
    s.append(R(30,80,90,160,OX,2,MET['Zn'][0],6)+R(300,80,90,160,RD,2,PASTE,6))
    s.append(R(200,76,16,168,EQUI,2,SEPF,3,dash='5 4'))
    s.append(circ([["wire",[[75,80],[75,40],[345,40],[345,80]]]]))
    s.append(flow('M75 80 V40 H345 V80'))
    s.append(A(160,20,260,20,'minus',3)+T(150,27,tex='e^-',size=19,fill=MINUS,anchor='end'))
    for i,y in enumerate((106,146,186,226)):
        s.append(an('move',chg(150,y,10,'-'),**{'from':'130,0','dur':'2','rep':'loop','ease':'lin','delay':f(.5*i)}))
    s.append(T(75,166,tex=r'\ce{Zn}',size=20)+T(345,166,tex=r'\ce{MnO2}',size=20,fill='#FFFFFF'))
    s.append(T(208,62,mix='격리판',size=18,fill=EQUI,weight=700))
    s.append(T(75,276,mix='$\\ce{OH-}$ 2개 쓰임',size=19,fill=OX)+T(345,276,mix='$\\ce{OH-}$ 2개 생김',size=19,fill=RD))
    s.append(T(208,306,mix='← $\\ce{OH-}$ 이동',size=19,fill=MINUS,weight=700))
    s.append(T(75,334,mix='(−) 산화 전극',size=19,weight=700,fill=OX)+T(345,334,mix='(+) 환원 전극',size=19,weight=700,fill=RD))
    return svg((420,346),400,'알칼리 전지에서 환원 전극이 만든 수산화 이온이 격리판을 지나 산화 전극으로 가서 쓰이므로 전체 반응에는 수산화 이온이 남지 않는다',s)
FIG['ALKION']=alkion()

# 8 은 단추 전지 + 전위 눈금
def button():
    s=[]
    s.append(R(30,140,300,130,INK,2.5,CAN,14))                 # 환원 전극 캔 (+)
    s.append(R(42,200,276,58,'none',0,'#5E5A57',6))            # Ag2O 펠릿
    s.append(R(42,186,276,14,EQUI,2,SEPF,2,dash='5 4'))        # 격리판
    s.append(R(54,128,252,58,OX,1.5,MET['Zn'][0],4))           # Zn 젤
    s.append(R(54,112,252,18,INK,2,'#8C99A6',4))               # 산화 전극 캡 (−)
    s.append(R(40,112,14,74,INK,1.5,GRAPH,2)+R(306,112,14,74,INK,1.5,GRAPH,2))   # 개스킷
    s.append(T(180,166,mix='$\\ce{KOH}$ 젤 속 $\\ce{Zn}$',size=19))
    s.append(T(180,236,mix='흑연 속 $\\ce{Ag2O}$ 펠릿',size=19,fill='#FFFFFF'))
    s.append(lead_line(48,92,47,112)+T(20,86,mix='개스킷',size=18,anchor='start'))
    s.append(T(200,90,mix='산화 전극 캡 (−)극',size=19,fill=OX,weight=700))
    s.append(lead_line(330,193,350,193)+T(354,199,mix='격리판',size=18,anchor='start',fill=EQUI))
    s.append(T(180,298,mix='환원 전극 캔 (+)극',size=19,fill=RD,weight=700))
    # 전위 눈금(가로)
    def X(E): return 50+(E+1.5)/2.1*380
    y=400
    s.append(L(X(-1.5),y,X(0.6),y,INK,2.5)+T(X(0.6)+6,y+6,tex=r'E^\circ\ [\text{V}]',size=18,anchor='start'))
    for E,lab,c in ((-1.260,r'\ce{ZnO}/\ce{Zn}',OX),(0.342,r'\ce{Ag2O}/\ce{Ag}',RD),(0.0,'0',MUTED)):
        s.append(L(X(E),y-8,X(E),y+8,c,3)+T(X(E),y+32,mix=(f'{E:+.3f}' if E else '0.00'),size=18))
        if E: s.append(T(X(E),y-46,tex=lab,size=19,fill=c))
    s.append(an('scale',L(X(-1.260),y-22,X(0.342),y-22,EQUI,4),**{'from':'0,1','o':f'{f(X(-1.260))},{y-22}','dur':'1.2'}))
    s.append(T((X(-1.260)+X(0.342))/2,y-30,mix='$E^\\circ_\\text{전지}=1.602$ V',size=19,fill=EQUI,weight=700,halo=True))
    return svg((520,446),500,'은 단추 전지 단면: 위쪽 산화 전극 캡 아래에 아연 젤, 격리판, 산화 은 펠릿과 환원 전극 캔이 있고, 두 반쪽 반응의 표준 환원 전위 차가 1.602 V이다',s)
FIG['BUTTON']=button()

# 9 방전과 충전 — 자유 에너지 도표
def rech():
    s=[L(50,300,50,40,MUTED,2)+T(50,30,tex='G',size=20)]
    s.append(L(130,80,370,80,INK,3)+L(130,270,370,270,INK,3))
    s.append(T(250,66,mix='반응물 — 충전된 상태',size=19,weight=700)+T(250,300,mix='생성물 — 방전된 상태',size=19,weight=700))
    s.append(an('draw',A(210,86,210,264,'field',4),dur='1'))
    s.append(an('draw',A(290,264,290,86,'bfield',4),dur='1',delay='.8'))
    s.append(T(196,166,mix='방전||$\\Delta G&lt;0$',size=19,fill=FIELD,weight=700,anchor='end'))
    s.append(T(196,222,mix='전기 에너지||발생',size=18,fill=FIELD,anchor='end'))
    s.append(T(304,166,mix='충전||$\\Delta G&gt;0$',size=19,fill=BF,weight=700,anchor='start'))
    s.append(T(304,222,mix='전기 에너지||공급',size=18,fill=BF,anchor='start'))
    return svg((440,316),420,'2차 전지는 자유 에너지가 낮아지는 방전으로 전기 에너지를 내고, 바깥에서 전기 에너지를 공급하는 충전으로 반응물을 다시 만든다',s)
FIG['RECH']=rech()

# 10·11 납-산 전지
def lead(mode='dis'):
    s=[]
    dis=(mode=='dis')
    if dis: parts=[["wire",[[165,90],[165,50],[232,50]]],["bulb",[250,50],{"r":18,"on":True}],["wire",[[268,50],[365,50],[365,90]]]]
    else: parts=[["wire",[[165,90],[165,50],[242,50]]],["bat",[250,50],{"dir":"h","pos":"right","signs":True}],["wire",[[258,50],[365,50],[365,90]]]]
    s.append(circ(parts))
    s.append(beaker(60,440,120,330)+sol(60,440,'w',150,328).replace('#DDEEF8',ACID))
    s.append(R(150,90,30,210,INK,2,PB,3)+R(350,90,30,210,INK,2,PBO2,3))
    if dis:
        dots=''.join(C(184,y,4,MUTED,1,'#F4F4F4')+C(346,y,4,MUTED,1,'#F4F4F4') for y in range(170,300,18))
        s.append(an('fade',dots,dur='1.2',delay='.4'))
        s.append(flow('M165 90 V50 H232 M268 50 H365 V90'))
        s.append(A(190,26,236,26,'minus',3)+A(268,26,314,26,'minus',3)+T(184,33,tex='e^-',size=20,fill=MINUS,anchor='end'))
        s.append(T(250,104,mix='2.1 V',size=20,weight=700,halo=True))
    else:
        s.append(flow('M365 90 V50 H258 M242 50 H165 V90'))
        s.append(A(314,26,268,26,'minus',3)+A(236,26,190,26,'minus',3)+T(320,33,tex='e^-',size=20,fill=MINUS,anchor='start'))
        s.append(T(250,104,mix='충전기',size=19,weight=700,halo=True))
    s.append(T(140,118,tex=r'\ce{Pb}',size=21,anchor='end')+T(390,118,tex=r'\ce{PbO2}',size=21,anchor='start'))
    s.append(T(265,250,tex=r'\ce{H2SO4(aq)}',size=19))
    if dis: s.append(T(265,224,mix='$\\ce{PbSO4}$ 덮임',size=18,fill=MUTED))
    a1,a2=(('산화 전극',OX),('환원 전극',RD)) if dis else (('환원 전극',RD),('산화 전극',OX))
    s.append(T(165,354,mix='(−)극',size=20,weight=700)+T(165,380,mix=a1[0],size=19,weight=700,fill=a1[1]))
    s.append(T(365,354,mix='(+)극',size=20,weight=700)+T(365,380,mix=a2[0],size=19,weight=700,fill=a2[1]))
    lab=lab0=('납-산 전지 방전: 납판이 산화 전극, 이산화 납판이 환원 전극이고 두 전극 표면이 황산납으로 덮인다' if dis else
         '납-산 전지 충전: 충전기가 전자를 납 전극 쪽으로 밀어 넣어 (−)극 쪽 전극이 환원 전극, (+)극 쪽 전극이 산화 전극이 된다')
    return svg((500,392),470 if dis else 440,lab,s)
FIG['LEAD']=lead('dis'); FIG['LEADC']=lead('chg')

# 12 리튬-이온 전지
def li():
    s=[R(170,100,200,200,'#9FC3DD',1,'#F4F8FC')]
    s.append(R(40,100,130,200,INK,2.5,'#E8EAED',6))
    for y in range(120,300,28): s.append(L(50,y,160,y,INK,2.5))
    for x,y in ((78,134),(132,190),(92,246)): s.append(chg(x,y,9,'+'))
    s.append(R(370,100,130,200,INK,2.5,'#E9E4F3',6))
    for i in range(4):
        for j in range(5): s.append(C(392+i*28,120+j*40,6,'#6B5B95',0,'#6B5B95',extra='opacity=".55"'))
    for x,y in ((406,140),(462,220)): s.append(chg(x,y,9,'+'))
    s.append(R(262,96,16,208,EQUI,2,SEPF,3,dash='5 4'))
    s.append(circ([["wire",[[105,100],[105,50],[252,50]]],["bulb",[270,50],{"r":18,"on":True}],["wire",[[288,50],[435,50],[435,100]]]]))
    s.append(flow('M105 100 V50 H252 M288 50 H435 V100'))
    s.append(A(130,26,190,26,'minus',3)+A(350,26,410,26,'minus',3)+T(124,33,tex='e^-',size=20,fill=MINUS,anchor='end'))
    for i,y in enumerate((140,190,240)):
        s.append(an('move',chg(330,y,10,'+'),**{'from':'-140,0','dur':'2.2','rep':'loop','ease':'lin','delay':f(.7*i)}))
    s.append(T(270,318,mix='분리막',size=18,fill=EQUI,weight=700))
    s.append(T(222,284,mix='전해질',size=18,fill=MUTED))
    s.append(T(105,326,mix='흑연 층 사이 $\\ce{Li}$',size=19)+T(435,326,tex=r'\ce{LiMn2O4}',size=19))
    s.append(T(330,90,mix='$\\ce{Li+}$ →',size=19,fill=PLUS,weight=700))
    s.append(T(105,354,mix='(−)극 산화 전극',size=19,weight=700,fill=OX)+T(435,354,mix='(+)극 환원 전극',size=19,weight=700,fill=RD))
    return svg((540,366),500,'리튬-이온 전지 방전: 흑연 층 사이의 리튬이 리튬 이온으로 빠져나와 전해질과 분리막을 지나 망가니즈 산화물로 들어가고, 전자는 바깥 도선으로 같은 쪽으로 흐른다',s)
FIG['LI']=li()

# 13 망가니즈 산화수
def oxn():
    s=[]; x=120
    def Y(v): return 300-(v-3.0)*240
    s.append(L(x,Y(3.0)+10,x,Y(4.0)-16,MUTED,2.5)+T(x,Y(4.0)-26,mix='$\\ce{Mn}$의 산화수',size=20,fill=MUTED))
    for v in (3.0,3.5,4.0): s.append(L(x-8,Y(v),x+8,Y(v),MUTED,2)+T(x-14,Y(v)+6,mix=f'+{v:.1f}',size=19,anchor='end'))
    g=C(x,Y(3.5),7,RD,0,RD)+T(x+20,Y(3.5)+6,mix='$\\ce{LiMn2O4}$: $+3.5$',size=19,anchor='start')
    g+=C(x,Y(3.75),7,MUTED,0,MUTED)+T(x+20,Y(3.75)+6,mix='$\\mathrm{Li}_{1-x}\\mathrm{Mn_2O_4}$: $3.5+\\dfrac{x}{2}$',size=19,anchor='start')
    g3=A(x+226,Y(3.75)-4,x+226,Y(3.5)+4,'rd',4)+T(x+238,Y(3.62)+7,mix='방전 = 환원',size=20,fill=RD,weight=700,anchor='start')
    g+=T(x+20,Y(4.0)+6,mix='($x=1$이면 $+4$)',size=20,anchor='start',fill=MUTED)
    s.append(step('g2',g)); s.append(step('g3',g3))
    return svg((480,320),420,'망가니즈의 산화수 수직선: 방전하면 3.5+x/2에서 3.5로 낮아져 망가니즈가 환원된다',s)
FIG['OXN']=oxn()

# 14 전자 1 mol당 최대 일
CMP=[('알칼리 전지',1.55),('은 단추 전지',1.602),('납-산 전지',2.1),('리튬-이온 전지',3.7),('수소 연료 전지',1.2)]
def ecomp():
    s=[]; x0=150; W=200; F=96485
    s.append(T(10,24,mix='전자 1 mol당 최대 일 $FE$ [kJ]',size=20,anchor='start',weight=700))
    for i,(n,E) in enumerate(CMP):
        y=46+i*50; w=F*E/1000/400*W
        s.append(T(x0-10,y+27,mix=n,size=20,anchor='end'))
        s.append(an('scale',R(x0,y+6,w,28,FIELD,1.5,FIELD,3,extra='fill-opacity=".45"'),**{'from':'0,1','o':f'{x0},{y+20}','dur':'.8','delay':f(.12*i)}))
        s.append(T(x0+w+8,y+28,mix=f'{F*E/1000:.0f}',size=20,anchor='start'))
    s.append(L(x0,40,x0,300,MUTED,2))
    return svg((420,306),420,'전자 1 mol당 최대 전기적 일은 리튬-이온 전지가 357 kJ로 가장 크고 수소 연료 전지가 116 kJ로 가장 작다',s)
FIG['ECOMP']=ecomp()

# 15 전기 자동차·드론
def evdr():
    s=[]
    s.append(P([(20,150),(34,104),(90,80),(200,80),(250,110),(290,118),(290,150)],INK,3,'#FFFFFF',close=True))
    s.append(C(80,154,22,INK,3,'#B7C0C9')+C(240,154,22,INK,3,'#B7C0C9'))
    for i in range(6): s.append(an('pop',R(70+i*26,128,22,14,FIELD,1.5,'#BFE5CF',2),dur='.4',delay=f(.1*i),o=f'{81+i*26},135'))
    s.append(T(155,206,mix='전기 자동차 — 바닥의 배터리 팩',size=18))
    cx,cy=400,110
    s.append(L(cx-46,cy-36,cx+46,cy+36,INK,4)+L(cx-46,cy+36,cx+46,cy-36,INK,4))
    for dx,dy in ((-46,-36),(46,-36),(-46,36),(46,36)): s.append(f'<ellipse cx="{cx+dx}" cy="{cy+dy}" rx="26" ry="7" fill="#E3EEFB" stroke="{MUTED}" stroke-width="2"/>')
    s.append(R(cx-20,cy-12,40,24,FIELD,2,'#BFE5CF',4))
    s.append(T(400,206,mix='드론 — 가벼운 배터리',size=18))
    return svg((480,220),460,'바닥에 배터리 팩을 깐 전기 자동차와 가운데 배터리를 단 드론',s)
FIG['EVDR']=evdr()

# 17 수소 연료 전지 (그림 Ⅲ-30을 새로 그림)
def fuel():
    s=[]
    s.append(R(110,110,60,220,MINUS,1.5,'#E3EEFB',4)+R(350,110,60,220,PLUS,1.5,'#FDECEE',4))
    s.append(R(190,110,140,220,FIELD,1.5,'#E8F5EE'))
    s.append(R(170,110,20,220,INK,2,'#B8BEC6',2)+R(330,110,20,220,INK,2,'#B8BEC6',2))
    s.append(circ([["wire",[[180,110],[180,50],[242,50]]],["bulb",[260,50],{"r":18,"on":True}],["wire",[[278,50],[340,50],[340,110]]]]))
    s.append(flow('M180 110 V50 H242 M278 50 H340 V110'))
    s.append(A(196,26,230,26,'minus',3)+A(290,26,324,26,'minus',3)+T(190,33,tex='e^-',size=20,fill=MINUS,anchor='end'))
    s.append(an('move',A(140,60,140,104,'minus',4),**{'from':'0,-16','dur':'1.2','rep':'loop','ease':'lin'}))
    s.append(an('move',A(380,60,380,104,'plus',4),**{'from':'0,-16','dur':'1.2','rep':'loop','ease':'lin','delay':'.4'}))
    s.append(T(130,52,tex=r'\ce{H2}(g)',size=20,fill=MINUS,anchor='end')+T(390,52,tex=r'\ce{O2}(g)',size=20,fill=PLUS,anchor='start'))
    s.append(A(380,336,380,372,'muted',4)+T(392,368,tex=r'\ce{H2O}(l)',size=20,anchor='start'))
    s.append(T(260,140,mix='전해질',size=19,weight=700)+T(260,166,mix='(고분자 막)',size=18))
    for i,y in enumerate((206,250,294)):
        s.append(an('move',chg(290,y,11,'P')+T(290,y+7,tex=r'\ce{H+}',size=18,fill='#FFFFFF'),**{'from':'-70,0','dur':'1.8','rep':'loop','ease':'lin','delay':f(.6*i)}))
    s.append(T(140,226,mix='산화||전극',size=19,weight=700,fill=OX)+T(380,226,mix='환원||전극',size=19,weight=700,fill=RD))
    s.append(T(150,360,mix='(−)극',size=19,weight=700)+T(300,360,mix='(+)극',size=19,weight=700))
    s.append(lead_line(186,330,226,374)+lead_line(334,330,294,374)+T(260,392,mix='흑연 표면의 $\\ce{Pt}$ 촉매',size=18))
    return svg((500,402),480,'수소 연료 전지: 산화 전극으로 들어온 수소가 전자와 양성자를 내놓고, 양성자는 고분자 막을 지나고 전자는 바깥 도선을 지나 환원 전극에서 산소와 만나 물이 된다',s)
FIG['FUEL']=fuel()

# 18 입자 그림: 2H2 + O2 -> 2H2O (원자 수 보존)
def fuelp():
    s=[R(10,20,190,170,MUTED,1.5,'#FFFFFF',10)+R(260,20,190,170,MUTED,1.5,'#FFFFFF',10)]
    def h2(x,y): return L(x-15,y,x+15,y,'#9AA5B1',7)+atom(x-15,y,18,'H')+atom(x+15,y,18,'H')
    def o2(x,y): return L(x-19,y,x+19,y,'#9AA5B1',7)+atom(x-19,y,24,'O')+atom(x+19,y,24,'O')
    def wat(x,y): return L(x,y,x-26,y+20,'#9AA5B1',7)+L(x,y,x+26,y+20,'#9AA5B1',7)+atom(x-26,y+20,18,'H')+atom(x+26,y+20,18,'H')+atom(x,y,24,'O')
    s.append(h2(60,64)+h2(150,64)+o2(105,138))
    s.append(an('draw',A(208,105,252,105,'ink',3),dur='.6'))
    s.append(an('pop',wat(310,74),dur='.5',delay='.6',o='310,84')+an('pop',wat(400,124),dur='.5',delay='.8',o='400,134'))
    s.append(T(105,218,mix='H 4개, O 2개',size=19)+T(355,218,mix='H 4개, O 2개',size=19))
    return svg((460,230),440,'수소 분자 2개와 산소 분자 1개가 물 분자 2개가 되어도 수소 원자 4개, 산소 원자 2개는 그대로이다',s)
FIG['FUELP']=fuelp()

# 19 연료 전지 효율 막대
def eff():
    s=[]; x0=150; y0=290; k=240/571.6
    hg=474.2*k; hh=571.6*k
    s.append(L(60,y0,330,y0,MUTED,2))
    s.append(an('scale',R(x0,y0-hg,90,hg,FIELD,2,FIELD,0,extra='fill-opacity=".45"'),**{'from':'1,0','o':f'{x0},{y0}','dur':'1'}))
    s.append(an('scale',R(x0,y0-hh,90,hh-hg,EQUI,2,EQUI,0,extra='fill-opacity=".45"'),**{'from':'1,0','o':f'{x0},{f(y0-hg)}','dur':'.6','delay':'1'}))
    s.append(T(x0+45,y0-hg/2,mix='83 %',size=21,weight=700))
    s.append(T(x0+104,y0-hg/2-4,mix='전기적 일 최대||$-\\Delta G^\\circ=474.2$ kJ',size=18,anchor='start',fill=FIELD,weight=700))
    s.append(T(x0+104,y0-hg-(hh-hg)/2+6,mix='열 $97.4$ kJ',size=18,anchor='start',fill=EQUI,weight=700))
    s.append(L(x0-14,y0,x0-14,y0-hh,MUTED,1.5)+L(x0-20,y0-hh,x0-8,y0-hh,MUTED,1.5)+T(x0-20,y0-hh/2,mix='$-\\Delta H^\\circ$||$571.6$ kJ',size=18,anchor='end'))
    s.append(T(195,y0+26,mix='$\\ce{2H2 + O2 -&gt; 2H2O(l)}$',size=18))
    return svg((420,326),400,'수소 연료 전지 반응의 엔탈피 571.6 kJ 가운데 최대 474.2 kJ(83 %)를 전기적 일로 꺼낼 수 있고 나머지 97.4 kJ는 열로 나간다',s)
FIG['EFF']=eff()

# 20 닫힌계와 열린계
def open_():
    s=[]
    s.append(R(20,60,170,120,INK,3,'#FFF4E8',10)+T(105,108,mix='반응물 → 생성물',size=19)+T(105,140,mix='(안에 담김)',size=18,fill=MUTED))
    s.append(T(105,36,mix='전기 화학 전지 — 닫힌계',size=19,weight=700))
    s.append(an('draw',A(105,184,105,236,'ink',4),dur='.6')+T(118,226,mix='전기 에너지',size=18,anchor='start'))
    s.append(R(270,60,170,120,INK,3,'#FFF4E8',10)+T(355,126,mix='연료 전지',size=19))
    s.append(T(355,36,mix='연료 전지 — 열린계',size=19,weight=700))
    s.append(an('move',A(230,90,266,90,'minus',4),**{'from':'-14,0','dur':'1','rep':'loop','ease':'lin'})+T(226,96,tex=r'\ce{H2}',size=18,fill=MINUS,anchor='end'))
    s.append(an('move',A(230,150,266,150,'plus',4),**{'from':'-14,0','dur':'1','rep':'loop','ease':'lin','delay':'.3'})+T(226,156,tex=r'\ce{O2}',size=18,fill=PLUS,anchor='end'))
    s.append(an('move',A(444,120,480,120,'muted',4),**{'from':'-14,0','dur':'1','rep':'loop','ease':'lin','delay':'.6'})+T(462,108,tex=r'\ce{H2O}',size=18))
    s.append(an('draw',A(355,184,355,236,'ink',4),dur='.6')+T(368,226,mix='전기 에너지',size=18,anchor='start'))
    return svg((500,250),470,'전기 화학 전지는 반응물을 안에 담은 닫힌계이고, 연료 전지는 수소와 산소가 들어오고 물이 나가는 열린계이다',s)
FIG['OPEN']=open_()

# 21 수소 가치 사슬
def chain():
    s=[]
    nodes=[(90,'생산','개질·수전해'),(260,'저장·운송','압축·액화·운반체'),(430,'활용','수소 연료 전지')]
    for i,(x,t,u) in enumerate(nodes):
        s.append(R(x-72,30,144,74,INK,2.5,'#E8F5EE' if i==2 else '#FFFFFF',12)+T(x,60,mix=t,size=20,weight=700)+T(x,88,mix=u,size=18))
        if i<2: s.append(A(x+74,67,x+96,67,'ink',3))
    bars=[(90,'$\\ce{CO2}$ 배출·비용'),(260,'큰 부피·안전'),(430,'백금 값·막 수명')]
    for i,(x,t) in enumerate(bars):
        s.append(L(x,104,x,140,PLUS,2,'4 3'))
        s.append(an('pop',R(x-80,140,160,44,PLUS,2,'#FDECEE',10)+T(x,169,mix=t,size=18,fill=PLUS,weight=700),dur='.5',delay=f(.25*i),o=f'{x},162'))
    s.append(T(260,214,mix='걸림돌',size=18,fill=PLUS))
    return svg((520,224),500,'수소 생산, 저장과 운송, 연료 전지 활용의 세 단계와 각 단계의 걸림돌',s)
FIG['CHAIN']=chain()

# 연습 문제 그림
FIG['EX1']=cellsvg('다니엘 전지에서 염다리의 질산 이온은 아연 쪽으로, 칼륨 이온은 구리 쪽으로 이동해 두 용액의 전하 균형을 맞춘다',width=510,
    ions=(r'\ce{NO3-}',r'\ce{K+}'))
def ladder(pairs,lo,hi,label,dim):
    s=[]; x=130
    def Y(E): return 270-(E-lo)/(hi-lo)*230
    s.append(L(x,Y(lo)+10,x,Y(hi)-10,INK,2.5)+T(x,Y(hi)-22,tex=r'E^\circ\ [\text{V}]',size=18))
    for E,t,c in pairs: s.append(L(x-9,Y(E),x+9,Y(E),c,3)+T(x-16,Y(E)+6,mix=f'{E:+.3f}' if abs(E)>1e-9 else '0.00',size=19,anchor='end')+T(x+18,Y(E)+6,tex=t,size=19,anchor='start',fill=c))
    a,b=dim
    s.append(an('scale',L(x+150,Y(a),x+150,Y(b),EQUI,4),**{'from':'1,0','o':f'{x+150},{f(Y(b))}','dur':'1'}))
    s.append(L(x+140,Y(a),x+160,Y(a),EQUI,2.5)+L(x+140,Y(b),x+160,Y(b),EQUI,2.5))
    s.append(step('g9',T(x+150,Y(b)+30,mix=label,size=19,fill=EQUI,weight=700,halo=True)))
    return s,Y
s,Y=ladder([(1.229,r'\ce{O2}/\ce{H2O}',RD),(1.077,r'\ce{Br2}/\ce{Br-}',OX)],0.95,1.32,'$0.152$ V',(1.229,1.077))
FIG['EX2']=svg((340,320),330,'산소와 브로민 반쪽 반응의 표준 환원 전위 눈금: 차이는 0.152 V',s)
s,Y=ladder([(0.799,r'\ce{Ag+}/\ce{Ag}',RD),(-0.402,r'\ce{Cd^2+}/\ce{Cd}',OX)],-0.6,1.0,'$1.201$ V',(0.799,-0.402))
FIG['EX3']=svg((340,320),330,'은과 카드뮴 반쪽 반응의 표준 환원 전위 눈금: 차이는 1.201 V',s)
def tri():
    s=[]; A_=(190,50); B=(60,250); Cc=(320,250)
    s.append(P([A_,B,Cc],MUTED,2,'none',close=True))
    for (x,y),t in ((A_,r'\Delta G^\circ'),(B,'K'),(Cc,r'E^\circ')):
        s.append(C(x,y,30,INK,2.5,'#FFFFFF')+T(x,y+8,tex=t,size=22))
    s.append(T(104,138,mix='$-RT\\ln K$',size=18,anchor='end',halo=True)+T(276,138,mix='$-nFE^\\circ$',size=18,anchor='start',halo=True))
    s.append(T(190,290,mix='$E^\\circ=\\dfrac{0.0592}{n}\\log K$',size=18,halo=True))
    return svg((380,320),340,'표준 자유 에너지 변화, 평형 상수, 표준 전지 전위의 관계 삼각형',s)
FIG['EX5']=tri()

# ═════ 출력 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
o=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(o)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "실용 전지", "file": "3-4-3_실용_전지", "header": "Ⅲ-4-3 실용 전지 (고등 고급 화학 175–180쪽)"}\n')
print('ok',len(o),'sections',o.count('<section'),'anim',o.count('data-anim'))
