# -*- coding: utf-8 -*-
"""고급화학 3-5-1 전기 분해와 전해 전지 — 그림 생성. tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   extra_src.css → extra.css, meta.json.  python3 -I gen.py  (출력 OUT — 이 덱 폴더만, assert로 막음)."""
import math, re, sys, os, shutil, json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cellh import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FD='3-5-1_전기_분해와_전해_전지'; OUT=BASE+FD+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-5-1_전기_분해와_전해_전지/', OUT
assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FD), OUT
FIG={}
MET['Au']=('#F0D27A','#B8962E'); MET['Fe']=('#B7C0C9','#7E8B98')
CU_DEP='#B0703C'; CL2='#D9E36A'; CL2S='#8F9A2E'; MOLT='#F3E1BE'
def flow(d,speed=32): return f'<path d="{d}" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="{speed}"/>'
def bubbles(x,y0,y1,n,col='#FFFFFF',st=MUTED,r=6,delay=0):
    """x 위치에서 y1(아래) → y0(위)로 올라가는 기포 n개(그린 모습 = 끝 모습)"""
    o=[]
    for i in range(n):
        yy=y0+(y1-y0)*i/max(1,n-1)*0.85; xx=x+(4 if i%2 else -4)
        o.append(an('move',C(xx,yy,r,st,1.5,col),**{'from':f'0,{f(min(60,y1-yy+10))}','dur':'1.6','rep':'loop','ease':'lin','delay':f(delay+.3*i)}))
    return ''.join(o)

# ── 한 비커 전해 전지 (viewBox 460×400): 왼쪽 전극(150) = 전원 (−)극 = 환원 전극, 오른쪽(310) = (+)극 = 산화 전극
def ebox(label,Lm='Pt',Rm='Pt',solc='#DDEEF8',solo=1,Ltex=r'\ce{Pt}',Rtex=r'\ce{Pt}',soltex='',cat=None,ani=None,
         Lprod='',Rprod='',poles=True,width=460,ph=200,Lcustom=None,extra='',polestep=None,tint=None):
    s=[]
    s.append(circ([["wire",[[150,100],[150,52],[222,52]]],["bat",[230,52],{"dir":"h","pos":"right","signs":True}],["wire",[[238,52],[310,52],[310,100]]]]))
    s.append(beaker(50,410,top=140,bot=330))
    s.append(f'<rect x="52" y="170" width="356" height="158" fill="{solc}" fill-opacity="{solo}"/>')
    if tint:
        s.append(f'<rect x="52" y="170" width="178" height="158" fill="{tint[0]}" fill-opacity="{tint[1]}"/><rect x="230" y="170" width="178" height="158" fill="{tint[2]}" fill-opacity="{tint[3]}"/>')
    s.append(Lcustom if Lcustom else plate(150,Lm,top=100,h=ph)); s.append(plate(310,Rm,top=100,h=ph))
    s.append(flow('M310 100 V52 H238 M222 52 H150 V100'))
    s.append(A(300,24,250,24,'minus',3)+T(306,31,tex='e^-',size=20,fill=MINUS,anchor='start'))
    s.append(A(210,24,160,24,'minus',3)+T(154,31,tex='e^-',size=20,fill=MINUS,anchor='end'))
    s.append(T(230,92,mix='전원',size=18,fill=MUTED))
    if Ltex: s.append(T(130,126,tex=Ltex,size=20,anchor='end'))
    if Rtex: s.append(T(330,126,tex=Rtex,size=20,anchor='start'))
    if soltex: s.append(T(230,318,mix=soltex,size=19,halo=True))
    if cat:
        s.append(an('move',chg(182,200,10,'+'),**{'from':'96,0','dur':'1.8','rep':'loop','ease':'lin'}))
        s.append(T(232,222,mix=f'← ${cat}$',size=19,fill=PLUS,halo=True))
    if ani:
        s.append(an('move',chg(278,252,10,'-'),**{'from':'-96,0','dur':'1.8','rep':'loop','ease':'lin','delay':'.9'}))
        s.append(T(230,276,mix=f'${ani}$ →',size=19,fill=MINUS,halo=True))
    s.append(Lprod+Rprod+extra)
    if poles:
        pl=T(150,358,mix='(−)극',size=21,weight=700)+T(150,384,mix='환원 전극',size=20,weight=700,fill=RD)+T(310,358,mix='(+)극',size=21,weight=700)+T(310,384,mix='산화 전극',size=20,weight=700,fill=OX)
        s.append(step(polestep,pl) if polestep else pl)
    return svg((460,400),width,label,s)

# 물의 전기 분해 — 거꾸로 세운 관 2개(그림 Ⅲ-31 새로 그림), viewBox 460×420
def water(width=460,cover=False):
    s=[]
    s.append(circ([["wire",[[150,322],[150,372],[222,372]]],["bat",[230,372],{"dir":"h","pos":"right","signs":True}],["wire",[[238,372],[310,372],[310,322]]]]))
    s.append(beaker(50,410,top=150,bot=330)); s.append(f'<rect x="52" y="186" width="356" height="142" fill="{WATER}"/>')
    for cx,gh,lab in ((150,150,r'\ce{H2}'),(310,75,r'\ce{O2}')):
        s.append(f'<rect x="{cx-26}" y="40" width="52" height="270" fill="{WATER}"/>')
        s.append(an('scale',f'<rect x="{cx-26}" y="40" width="52" height="{gh}" fill="#FFFFFF"/>',**{'from':'1,0','o':f'{cx},40','dur':'2'}))
        s.append(f'<path d="M{cx-26} 310 V52 Q{cx-26} 38 {cx} 38 Q{cx+26} 38 {cx+26} 52 V310" fill="none" stroke="{GLS}" stroke-width="3"/>')
        s.append(T(cx,40+gh/2+8,tex=lab,size=22,weight=700))
        s.append(R(cx-6,240,12,90,INK,1.5,MET['Pt'][0],2))
        s.append(bubbles(cx+12,200,236,3,delay=(0 if cx<200 else .5)))
    s.append(flow('M310 322 V372 H238 M222 372 H150 V322'))
    s.append(A(296,398,256,398,'minus',3)+T(302,405,tex='e^-',size=19,fill=MINUS,anchor='start'))
    s.append(A(204,398,164,398,'minus',3))
    s.append(T(230,352,mix='물 + 전해질',size=18,fill=MUTED) if cover else T(230,300,mix='물 + 전해질',size=18,fill=MUTED,halo=True))
    s.append(T(108,124,mix='2',size=26,weight=700,fill=EQUI)+T(352,86,mix='1',size=26,weight=700,fill=EQUI))
    if not cover:
        s.append(T(140,352,mix='(−)극 환원 전극',size=18,fill=RD,weight=700,anchor='end')+T(320,352,mix='(+)극 산화 전극',size=18,fill=OX,weight=700,anchor='start'))
        s.append(T(230,100,mix='부피비',size=19,fill=EQUI,weight=700))
    return svg((460,420),width,'물의 전기 분해: 전원의 (−)극에 연결된 환원 전극 쪽 관에 수소가, (+)극에 연결된 산화 전극 쪽 관에 산소가 2 대 1의 부피비로 모인다',s,'fig cover-fig' if cover else 'fig')
FIG['COVER']=water(500,cover=True)
FIG['WATER']=water()

# 중단원 도입 — 알루미늄 전기 분해 제련(모식도)
def smelt(width=480):
    s=[]
    s.append(R(30,120,420,190,INK,3,'#8E99A6',10))                 # 강철 통
    s.append(R(44,132,392,166,'none',0,MET['C'][0],6))             # 탄소 내벽(환원 전극)
    s.append(R(58,150,364,96,'none',0,'#F2C58A'))                   # 녹은 빙정석 + Al2O3
    s.append(R(58,246,364,38,'none',0,'#D5DCE3'))                   # 녹은 Al
    s.append(R(100,26,280,12,INK,2,'#B0835A',3))                    # 버스바
    for x in (130,290):
        s.append(R(x+28,38,8,40,INK,1.5,'#B0835A',1)+R(x,78,64,130,INK,2,MET['C'][0],4))
        s.append(bubbles(x+76,150,200,3,'#FFFFFF',MUTED,5,delay=(0 if x<200 else .6)))
    s.append(T(240,190,mix='녹은 빙정석 + $\\ce{Al2O3}$',size=19,halo=True))
    s.append(T(240,272,mix='녹은 $\\ce{Al}$',size=19,weight=700))
    s.append(T(240,330,mix='탄소 내벽 — 환원 전극 (−)극',size=19,fill=RD,weight=700))
    s.append(T(240,20,mix='탄소 전극 — 산화 전극 (+)극',size=19,fill=OX,weight=700))
    s.append(T(470,108,tex=r'\ce{CO2}',size=19,anchor='end',fill=MUTED)+L(400,140,440,114,MUTED,1.5))
    return svg((480,340),width,'알루미늄 제련 전해조: 녹은 빙정석에 산화 알루미늄을 녹이고 탄소 전극으로 전기 분해하면 바닥에 녹은 알루미늄이 모이고 탄소 전극에서 이산화 탄소가 생긴다',s)
FIG['SMELT']=smelt()
FIG['SMELT2']=smelt(460)

# 생각 열기 — 다니엘 전지(3-4-1)
FIG['REVIEW']=cellsvg('다니엘 전지: 아연 전극이 산화 전극, 구리 전극이 환원 전극이고 전압계는 1.1 볼트를 가리킨다',width=500,
    ions=(r'\ce{SO4^2-}',r'\ce{Na+}'),reading='1.1 V')

# 물 전기 분해와 pH 변화
def waterion():
    lp=bubbles(170,184,250,3)
    rp=bubbles(290,184,250,3,delay=.5)
    ex=T(186,164,tex=r'\ce{H2}',size=20,weight=700,anchor='start')+T(274,164,tex=r'\ce{O2}',size=20,weight=700,anchor='end')
    ex+=T(140,302,mix='염기성 $\\ce{OH-}$',size=19,fill=MINUS,weight=700)+T(320,302,mix='산성 $\\ce{H+}$',size=19,fill=PLUS,weight=700)
    return ebox('물의 전기 분해: 환원 전극 쪽은 수산화 이온이 생겨 염기성(지시약 파란색), 산화 전극 쪽은 수소 이온이 생겨 산성(노란색)이 된다',
        ph=160,extra=ex,Lprod=lp,Rprod=rp,tint=('#3E8ED0',.22,'#FFE45C',.40))
FIG['WATERION']=waterion()

# ③ 자유 에너지 도표
def energy():
    s=[]
    s.append(A(30,300,30,30,'ink',2.5)+T(42,40,tex='G',size=22,anchor='start'))
    s.append(L(60,80,230,80,INK,4)+L(230,80,430,80,MUTED,1.5,'5 5'))
    s.append(L(230,250,410,250,INK,4)+L(60,250,230,250,MUTED,1.5,'5 5'))
    s.append(T(145,66,mix='$\\ce{Zn + Cu^2+}$',size=20)+T(320,282,mix='$\\ce{Zn^2+ + Cu}$',size=20))
    s.append(an('draw',A(200,86,200,244,'field',4),dur='.9'))
    s.append(T(188,150,mix='자발 (화학 전지)',size=19,fill=FIELD,weight=700,anchor='end')+T(188,178,mix='$\\Delta G^\\circ=-212.3$ kJ',size=19,fill=FIELD,anchor='end'))
    s.append(an('draw',A(260,244,260,86,'bfield',4),dur='.9',delay='.9'))
    s.append(T(272,150,mix='비자발 (전해 전지)',size=19,fill=BF,weight=700,anchor='start')+T(272,178,mix='$+212.3$ kJ 공급',size=19,fill=BF,anchor='start'))
    s.append(T(230,316,mix='반응 경로',size=18,fill=MUTED))
    return svg((450,330),450,'다니엘 전지 반응은 깁스 자유 에너지가 212.3 킬로줄 줄어드는 자발 반응이고, 역반응은 그만큼 전기 에너지를 공급해야 일어난다',s)
FIG['ENERGY']=energy()

# ④ 다니엘 전지의 역반응 (전원 연결)
def reverse():
    o=[]
    o.append(circ([["wire",[[124,90],[124,50],[272,50]]],["bat",[280,50],{"dir":"h","pos":"right","signs":True}],["wire",[[288,50],[424,50],[424,90]]]]))
    o+= [beaker(40,230),beaker(330,520),sol(40,230,'w'),sol(330,520,'cu')]
    o.append(bridge()); o.append(T(280,142,mix='염다리',size=20,fill=MUTED))
    o.append(plate(124,'Zn')); o.append(plate(424,'Cu'))
    o.append(flow('M424 90 V50 H288 M272 50 H124 V90',36))
    o.append(A(232,26,160,26,'minus',3)+A(400,26,328,26,'minus',3)+T(152,34,tex='e^-',size=21,fill=MINUS,anchor='end')+T(408,34,tex='e^-',size=21,fill=MINUS,anchor='start'))
    o.append(T(280,92,mix='1.1 V보다 큰 전압',size=19,weight=700,halo=True))
    o.append(T(104,112,tex=r'\ce{Zn}',size=22,anchor='end')+T(446,112,tex=r'\ce{Cu}',size=22,anchor='start'))
    o.append(T(135,288,tex=r'\ce{ZnSO4(aq)}',size=20)+T(425,288,tex=r'\ce{CuSO4(aq)}',size=20))
    o.append(an('move',chg(346,112,9,'-'),**{'from':'-60,0','dur':'1.6','rep':'loop','ease':'lin'}))
    o.append(an('move',chg(214,112,9,'+'),**{'from':'60,0','dur':'1.6','rep':'loop','ease':'lin','delay':'.8'}))
    o.append(T(280,170,mix='$\\ce{SO4^2-}$ →',size=20,fill=MINUS,halo=True)+T(280,206,mix='← $\\ce{Na+}$',size=20,fill=PLUS,halo=True))
    o.append(T(135,326,mix='(−)극',size=21,weight=700)+T(135,353,mix='환원 전극',size=20,weight=700,fill=RD))
    o.append(T(425,326,mix='(+)극',size=21,weight=700)+T(425,353,mix='산화 전극',size=20,weight=700,fill=OX))
    return svg((560,370),500,'다니엘 전지에 1.1 볼트보다 큰 전원을 반대로 걸면 구리 전극이 산화 전극이 되어 녹고 아연 전극이 환원 전극이 되어 아연이 석출된다',o)
FIG['REVERSE']=reverse()

# ⑤ 화학 전지와 전해 전지 비교 (작은 그림 두 칸)
def compare():
    s=[]
    for ox0,kind in ((0,'g'),(250,'e')):
        x1,x2=ox0+50,ox0+170
        s.append(R(ox0+20,110,180,90,GLS,2.5,WATER,6))
        s.append(R(x1-8,80,16,100,INK,1.5,'#C9D3DD',2)+R(x2-8,80,16,100,INK,1.5,'#C9D3DD',2))
        if kind=='g':
            s.append(circ([["wire",[[x1,80],[x1,48],[ox0+96,48]]],["bulb",[ox0+110,48],{"r":14,"on":True}],["wire",[[ox0+124,48],[x2,48],[x2,80]]]]))
            s.append(flow(f'M{x1} 80 V48 H{ox0+96} M{ox0+124} 48 H{x2} V80'))
            s.append(T(ox0+110,24,mix='화학 전지',size=20,weight=700,fill=FIELD))
            labs=((x1,'(−)극','산화',OX),(x2,'(+)극','환원',RD))
        else:
            s.append(circ([["wire",[[x1,80],[x1,48],[ox0+102,48]]],["bat",[ox0+110,48],{"dir":"h","pos":"right","signs":True}],["wire",[[ox0+118,48],[x2,48],[x2,80]]]]))
            s.append(flow(f'M{x2} 80 V48 H{ox0+118} M{ox0+102} 48 H{x1} V80'))
            s.append(T(ox0+110,24,mix='전해 전지',size=20,weight=700,fill=BF))
            labs=((x1,'(−)극','환원',RD),(x2,'(+)극','산화',OX))
        for x,p,r,c in labs: s.append(T(x,228,mix=p,size=19,weight=700)+T(x,254,mix=r,size=19,weight=700,fill=c))
    return svg((460,264),460,'화학 전지는 산화 전극이 (−)극이고, 전해 전지는 전원의 (+)극에 연결된 산화 전극이 (+)극이다',s)
FIG['COMPARE']=compare()

# 확인 01 — 물 분해와 연료 전지
def wfuel():
    s=[]
    s.append(A(30,280,30,30,'ink',2.5)+T(42,40,tex='G',size=22,anchor='start'))
    s.append(L(60,250,190,250,INK,4)+T(125,280,tex=r'\ce{2H2O(l)}',size=20))
    s.append(L(250,70,390,70,INK,4)+T(320,56,tex=r'\ce{2H2(g) + O2(g)}',size=20))
    s.append(L(190,250,390,250,MUTED,1.5,'5 5')+L(60,70,250,70,MUTED,1.5,'5 5'))
    s.append(an('draw',A(150,244,150,76,'bfield',4),dur='.9'))
    s.append(T(162,150,mix='전기 분해',size=19,fill=BF,weight=700,anchor='start')+T(162,176,mix='$+474.2$ kJ',size=19,fill=BF,anchor='start'))
    s.append(an('draw',A(290,76,290,244,'field',4),dur='.9',delay='.9'))
    s.append(T(302,150,mix='연료 전지',size=19,fill=FIELD,weight=700,anchor='start')+T(302,176,mix='$-474.2$ kJ',size=19,fill=FIELD,anchor='start'))
    return svg((420,300),420,'물의 전기 분해는 깁스 자유 에너지가 474.2 킬로줄 늘어나는 비자발 반응이고, 그 역반응이 수소 연료 전지 반응이다',s)
FIG['WFUEL']=wfuel()

# ⑥ 녹은 NaCl
def molten():
    na=''.join(an('pop',C(170,y,7,'#7E8B98',1.5,'#E6E9ED'),dur='.5',delay=f(.4*i),o=f'170,{y}') for i,y in enumerate((292,268,244)))
    cl=bubbles(290,184,250,3,CL2,CL2S)
    ex=T(128,232,tex=r'\ce{Na(l)}',size=20,weight=700,anchor='end')+T(332,200,tex=r'\ce{Cl2(g)}',size=20,weight=700,anchor='start')
    return ebox('녹은 염화 나트륨의 전기 분해: 나트륨 이온은 환원 전극으로 가서 나트륨이 되고, 염화 이온은 산화 전극으로 가서 염소 기체가 된다',
        Lm='C',Rm='C',Ltex=r'\text{흑연}',Rtex=r'\text{흑연}',solc=MOLT,soltex='녹은 $\\ce{NaCl}$ (약 $801\\ {}^\\circ\\text{C}$)',cat=r'\ce{Na+}',ani=r'\ce{Cl-}',Lprod=na,Rprod=cl,extra=ex)
FIG['MOLTEN']=molten()

# ⑦ 생성물 예측 — 표준 환원 전위 눈금
def ladder2():
    s=[]; x=230
    def Y(E): return 40+(1.5-E)/4.3*290
    s.append(L(x,Y(1.5)-6,x,Y(-2.8)+6,INK,2.5)+T(x,20,tex=r'E^\circ\ [\text{V}]',size=19))
    for E,t,lab in ((0.34,r'\ce{Cu^2+}/\ce{Cu}','+0.34'),(-0.83,r'\ce{H2O}/\ce{H2}','-0.83'),(-2.70,r'\ce{Na+}/\ce{Na}','-2.70')):
        s.append(L(x-10,Y(E),x,Y(E),RD,3)+T(x-16,Y(E)+7,mix=f'${t}$ ${lab}$',size=19,anchor='end',fill=RD))
    for E,t,lab,yl in ((1.36,r'\ce{Cl2}/\ce{Cl-}','+1.36',44),(1.23,r'\ce{O2}/\ce{H2O}','+1.23',80)):
        s.append(L(x,Y(E),x+10,Y(E),OX,3)+L(x+10,Y(E),x+18,yl-6,OX,1.5)+T(x+22,yl,mix=f'${t}$ ${lab}$',size=19,anchor='start',fill=OX))
    s.append(T(x+22,140,mix='$\\ce{SO4^2-}$, $\\ce{NO3-}$은',size=19,anchor='start',fill=MUTED)+T(x+22,166,mix='산화되지 않는다',size=19,anchor='start',fill=MUTED))
    s.append(an('draw',A(40,300,40,90,'rd',3),dur='.8')+T(20,376,mix='위쪽일수록 먼저 환원',size=19,fill=RD,weight=700,anchor='start'))
    s.append(an('draw',A(430,200,430,300,'ox',3),dur='.8',delay='.4')+T(444,400,mix='아래쪽일수록 먼저 산화',size=19,fill=OX,weight=700,anchor='end'))
    s.append(step('g1',R(x-200,Y(-0.83)-17,190,30,RD,2.5,'none',8)))
    s.append(step('g2',R(x+14,20,200,32,OX,2.5,'none',8)))
    return svg((460,410),460,'표준 환원 전위 눈금: 환원 전극에서는 위쪽에 있는 화학종이, 산화 전극에서는 아래쪽에 있는 화학종이 먼저 반응한다',s)
FIG['LADDER']=ladder2()

# 수용액(구리) — 확인 03
def cuso4():
    dep=an('fade',R(134,170,32,130,'none',0,CU_DEP,3,extra='fill-opacity=".85"'),dur='1.5')
    ob=bubbles(290,184,250,3,delay=.4)
    ex=T(186,164,tex=r'\ce{Cu}',size=20,weight=700,anchor='start',fill=CU_DEP)+T(274,164,tex=r'\ce{O2}',size=20,weight=700,anchor='end')
    return ebox('백금 전극으로 황산 구리(Ⅱ) 수용액을 전기 분해하면 환원 전극에 구리가 석출되고 산화 전극에서 산소가 발생한다',
        solc='#3E8ED0',solo=.30,soltex='$\\ce{CuSO4(aq)}$',cat=r'\ce{Cu^2+}',ani=r'\ce{SO4^2-}',Lprod=dep,Rprod=ob,extra=ex)
FIG['CUSO4']=cuso4()

# 연습 문제 2 — CuCl2 (극 이름은 단계)
def cucl2():
    dep=an('fade',R(134,170,32,130,'none',0,CU_DEP,3,extra='fill-opacity=".85"'),dur='1.5')
    cb=bubbles(290,184,250,3,CL2,CL2S,delay=.4)
    ex=T(186,164,tex=r'\ce{Cu}',size=20,weight=700,anchor='start',fill=CU_DEP)+T(274,164,tex=r'\ce{Cl2}',size=20,weight=700,anchor='end')
    return ebox('염화 구리(Ⅱ) 수용액의 전기 분해: 전원의 (−)극에 연결된 전극이 환원 전극, (+)극에 연결된 전극이 산화 전극이다',
        solc='#3E8ED0',solo=.22,soltex='$\\ce{CuCl2(aq)}$',cat=r'\ce{Cu^2+}',ani=r'\ce{Cl-}',Lprod=dep,Rprod=cb,extra=ex,polestep='g1')
FIG['CUCL2']=cucl2()

# 연습 문제 3 — 묽은 산
def acid():
    hb=bubbles(170,184,250,4); ob=bubbles(290,184,250,2,delay=.5)
    ex=T(186,164,tex=r'\ce{H2}',size=20,weight=700,anchor='start')+T(274,164,tex=r'\ce{O2}',size=20,weight=700,anchor='end')
    return ebox('묽은 산 수용액의 전기 분해: 수소 이온이 환원 전극에서 수소가 되고 산화 전극에서는 물이 산화되어 산소가 발생한다',
        soltex='묽은 $\\ce{H2SO4(aq)}$',cat=r'\ce{H+}',ani=r'\ce{SO4^2-}',Lprod=hb,Rprod=ob,extra=ex)
FIG['ACID']=acid()

# ⑨ 은 도금
def spoon(lab=True):
    sp=R(145,100,10,140,INK,1.5,'#B7C0C9',3)+f'<ellipse cx="150" cy="270" rx="20" ry="36" fill="#B7C0C9" stroke="{INK}" stroke-width="1.5"/>'
    sp+=an('fade',f'<ellipse cx="150" cy="270" rx="22" ry="38" fill="none" stroke="#EEF1F4" stroke-width="5"/>',dur='1.5')
    ex=(T(92,226,mix='도금할',size=19,weight=700)+T(92,250,mix='숟가락',size=19,weight=700)) if lab else ''
    return ebox('은 도금: 도금할 숟가락을 환원 전극에, 은판을 산화 전극에 연결하면 은판의 은이 녹아 나와 숟가락 표면에 은이 석출된다',
        Rm='Ag',Ltex='',Rtex=r'\ce{Ag}',solc='#EEF1F4',soltex='',cat=r'\ce{Ag+}',Lcustom=sp,extra=T(310,318,tex=r'\ce{AgNO3(aq)}',size=19,halo=True)+ex)
FIG['PLATE']=spoon()
FIG['PLATE2']=spoon()

# 예제 Ⅲ-13 — 금 도금
def gold():
    dep=an('fade',R(134,170,32,130,'none',0,MET['Au'][0],3),dur='1.5')
    return ebox('금 도금: 환원 전극에서 금 이온이 전자 3개를 얻어 금으로 석출된다',
        Lm='Cu',Rm='Au',Ltex=r'\text{물체}',Rtex=r'\ce{Au}',solc='#F7EBC0',soltex='$\\ce{Au^3+}$ 수용액',cat=r'\ce{Au^3+}',Lprod=dep)
FIG['GOLD']=gold()

# 탐구 28 — 도금의 예
def plicons():
    s=[]
    def faucet(x,y): return P([(x-40,y+20),(x+10,y+20),(x+10,y+60),(x-6,y+60),(x-6,y+36),(x-40,y+36)],INK,2.5,'#DDE1E6',close=True)+R(x-12,y,24,20,INK,2,'#DDE1E6',3)+R(x-30,y-8,60,10,INK,2,'#DDE1E6',4)
    def roof(x,y): return ''.join(P([(x-56+i*28,y+60),(x-42+i*28,y+20),(x-28+i*28,y+60)],INK,2,'#C9D3DD',close=True) for i in range(4))
    def can(x,y): return f'<ellipse cx="{x}" cy="{y+6}" rx="30" ry="8" fill="#E6E9ED" stroke="{INK}" stroke-width="2"/>'+R(x-30,y+6,60,56,INK,2,'#E6E9ED')+f'<ellipse cx="{x}" cy="{y+62}" rx="30" ry="8" fill="#E6E9ED" stroke="{INK}" stroke-width="2"/>'+R(x-30,y+22,60,20,'none',0,'#E8F5EE')
    def chip(x,y): return R(x-30,y+10,60,44,INK,2,'#2B2F35',4)+''.join(R(x-26+i*14,y+54,8,16,'#B8962E',1,MET['Au'][0],1) for i in range(4))
    cells=[(110,30,faucet,'수도꼭지','크로뮴'),(350,30,roof,'함석 지붕','아연'),(110,190,can,'통조림 캔','주석'),(350,190,chip,'전자 부품 단자','금')]
    for i,(x,y,fn,nm,mt) in enumerate(cells):
        s.append(an('pop',fn(x,y),dur='.5',delay=f(.2*i),o=f'{x},{y+35}'))
        s.append(T(x,y+102,mix=nm,size=19)+T(x,y+128,mix=f'{mt} 도금',size=19,weight=700,fill=EQUI))
    return svg((460,340),460,'도금의 예: 수도꼭지의 크로뮴 도금, 함석 지붕의 아연 도금, 통조림 캔의 주석 도금, 전자 부품 단자의 금 도금',s)
FIG['PLICON']=plicons()

# ⑩ 양적 관계 흐름
def chain():
    s=[]; boxes=['전류 $I$·시간 $t$','전하량 $Q$ [C]','전자 $n_{e^-}$ [mol]','생성물 [mol]','질량·부피']
    ops=['$Q=It$','$\\div F$','계수비','$\\times M$']
    for i,t in enumerate(boxes):
        x=10+i*200; col=EQUI if i in (1,2) else INK
        s.append(an('pop',R(x,20,160,64,col,2.5,'#FFFFFF' if i not in (1,2) else '#FFF4E8',12)+T(x+80,60,mix=t,size=20,weight=700),dur='.45',delay=f(.25*i),o=f'{x+80},52'))
        if i<4: s.append(A(x+164,52,x+196,52,'muted',3)+T(x+180,112,mix=ops[i],size=19,fill=MUTED))
    return svg((1000,124),1000,'전류와 시간으로 전하량을 구하고, 패러데이 상수로 나누어 전자의 몰수를 구한 뒤, 반쪽 반응의 계수비로 생성물의 몰수와 질량을 구한다',s)
FIG['CHAIN']=chain()

# 탐구 29 — 1 t당 전하량 막대
def qbar():
    s=[]; data=[('Al',10.73),('Mg',7.94),('Na',4.20),('Cu',3.04),(r'Cl2',2.72)]
    x0=90; k=270/11
    for i,(nm,v) in enumerate(data):
        y=30+i*50
        s.append(T(x0-12,y+24,tex=r'\ce{'+nm+'}',size=20,anchor='end'))
        s.append(an('scale',R(x0,y,v*k,30,'none',0,BF if i==0 else '#B9A6E0',4),**{'from':'0,1','o':f'{x0},{y+15}','dur':'1','delay':f(.15*i)}))
        s.append(T(x0+v*k+8,y+23,mix=f'{v:.2f}',size=19,anchor='start'))
    s.append(L(x0,22,x0,282,MUTED,2))
    s.append(T(210,312,mix='1 t당 전하량 [$\\times10^{9}$ C]',size=19,fill=MUTED))
    return svg((420,324),420,'원료 1톤을 얻는 데 필요한 전하량: 알루미늄이 가장 크고 마그네슘, 나트륨, 구리, 염소 순이다',s)
FIG['QBAR']=qbar()

# 연습 문제 1 — Cu/Sn 눈금
def ladder1():
    s=[]; x=150
    def Y(E): return 270-(E+0.4)/0.9*220
    s.append(L(x,Y(-0.4)+10,x,Y(0.5)-10,INK,2.5)+T(x,Y(0.5)-22,tex=r'E^\circ\ [\text{V}]',size=19))
    for E,t,c in ((0.34,r'\ce{Cu^2+}/\ce{Cu}',RD),(-0.14,r'\ce{Sn^2+}/\ce{Sn}',OX)):
        s.append(L(x-9,Y(E),x+9,Y(E),c,3)+T(x-16,Y(E)+6,mix=f'{E:+.2f}',size=19,anchor='end')+T(x+18,Y(E)+6,tex=t,size=19,anchor='start',fill=c))
    s.append(an('scale',L(x+150,Y(0.34),x+150,Y(-0.14),EQUI,4),**{'from':'1,0','o':f'{x+150},{f(Y(-0.14))}','dur':'1'}))
    s.append(L(x+140,Y(0.34),x+160,Y(0.34),EQUI,2.5)+L(x+140,Y(-0.14),x+160,Y(-0.14),EQUI,2.5))
    s.append(step('g9',T(x+150,Y(-0.14)+34,mix='$0.48$ V',size=19,fill=EQUI,weight=700,halo=True)))
    return svg((360,300),360,'구리와 주석의 표준 환원 전위 눈금: 구리 쪽이 0.48 볼트 높다',s)
FIG['EX1']=ladder1()

# ═════ 출력 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
o=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(o)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "전기 분해와 전해 전지", "file": "3-5-1_전기_분해와_전해_전지", "header": "Ⅲ-5-1 전기 분해와 전해 전지 (고등 고급 화학 181–185쪽)"}\n')
print('ok',len(o),'sections',o.count('<section'),'anim',o.count('data-anim'))
