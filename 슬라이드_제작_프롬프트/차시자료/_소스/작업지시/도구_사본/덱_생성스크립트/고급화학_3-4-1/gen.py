# -*- coding: utf-8 -*-
"""고급화학 3-4-1 화학 전지의 개요와 전지 전위 — a/b 두 덱 그림 생성.
   tpl_a.html, tpl_b.html의 {{KEY}}를 SVG로 바꿔 각 덱 폴더의 slides.html을 만든다.
   extra_src.css → extra.css(두 덱), labs_src.js → a의 labs.js, meta.json(두 덱).
   python3 -I gen.py   (출력 경로 OUT_A, OUT_B — 이 덱 두 폴더만, assert로 막음). 검산은 calc.py."""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FA='3-4-1_화학_전지의_개요와_전지_전위a'; FB='3-4-1_화학_전지의_개요와_전지_전위b'
OUT_A=BASE+FA+'/'; OUT_B=BASE+FB+'/'
assert OUT_A=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-4-1_화학_전지의_개요와_전지_전위a/', OUT_A
assert OUT_B=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-4-1_화학_전지의_개요와_전지_전위b/', OUT_B
for o,fd in ((OUT_A,FA),(OUT_B,FB)):
    os.makedirs(o,exist_ok=True); assert os.path.isdir(o) and o.rstrip('/').endswith(fd), o
FIG={}
M_R=30   # 금속 원자 Zn·Cu 반지름(덱 약속, 3-3-1 Zn 30 이어받음), 이온 Zn2+·Cu2+ 22
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def step(g,body): return f'<g class="step" data-g="{g}">{body}</g>'
def atom(x,y,r,el,lab=None): return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def chg(x,y,r,s): return f'<g data-chg="{f(x)},{f(y)},{f(r)},{s}"></g>'
def elec(x,y,lab=True,r=9):
    return C(x,y,r,MINUS,1.5,'#DCE9FA')+(T(x,y+6,tex='e^-',size=18,fill=MINUS) if lab else '')
def circ(parts):
    import json
    return "<g data-circuit='"+json.dumps({"parts":parts,"stroke":3})+"'></g>"
MET={'Zn':('#C9D3DD','#7E8B98'),'Cu':('#E6C29C','#B0835A'),'Ni':('#B9BDB4','#7A7F74'),'Ag':('#DDE1E6','#8C99A6'),
     'Mg':('#EEF1F4','#9AA5B1'),'Co':('#A7B3C2','#6B7A8C'),'C':('#4A4F57','#2B2F35'),'Pt':('#B8BEC6','#7E8B98')}
SOLC={'w':('#DDEEF8',1),'cu':('#3E8ED0',.32),'cu2':('#3E8ED0',.14),'cu3':('#3E8ED0',.06),'mn':('#A24FB5',.35),'i':('#C9A46A',.35),'co':('#D98C9B',.3),'cr':('#E08A2C',.35)}
GLS='#7E8B98'
def beaker(x0,x1,top=120,bot=300):
    return (f'<path d="M{x0-6} {top} H{x0} V{bot-10} Q{x0} {bot} {x0+10} {bot} H{x1-10} Q{x1} {bot} {x1} {bot-10} V{top} H{x1+6}" '
            f'fill="none" stroke="{GLS}" stroke-width="3" stroke-linejoin="round"/>')
def sol(x0,x1,kind,top=160,bot=298):
    c,o=SOLC[kind]; return f'<rect x="{x0+2}" y="{top}" width="{x1-x0-4}" height="{bot-top}" fill="{c}" fill-opacity="{o}"/>'
def plate(cx,m,top=90,h=180,w=None):
    fl,st=MET[m]; w=w or (22 if m=='C' else 18 if m=='Pt' else 28)
    return R(cx-w/2,top,w,h,st,2,fl,3)
def bridge(x1=190,x2=370,top=112,bot=250,w=24,kind='tube'):
    d=f'M{x1} {bot} V{top} H{x2} V{bot}'
    if kind=='tube': return f'<path d="{d}" fill="none" stroke="#B9A98A" stroke-width="{w}"/><path d="{d}" fill="none" stroke="#F6F0E0" stroke-width="{w-6}"/>'
    return ''
def cell(Lm='Zn',Rm='Cu',Ltex=r'\ce{Zn}',Rtex=r'\ce{Cu}',Lsol=r'\ce{ZnSO4(aq)}',Rsol=r'\ce{CuSO4(aq)}',Lk='w',Rk='cu',
         e='r',poles=True,br=True,ions=None,ion_anim=True,flow=True,meter='V',reading=None,extra='',elab=True,blab=True):
    """viewBox 560×370: L 비커 40–230(전극 124), R 비커 330–520(전극 424). e='r' → 전자 L→R(L이 (−)극).
       ions=(음이온 tex, 양이온 tex) 염다리 이온 이동(음이온 → 산화 전극 쪽)."""
    o=[]
    mp=[["wire",[[124,90],[124,50],[262,50]]],["wire",[[298,50],[424,50],[424,90]]],["meter",[280,50],meter,{"r":18}]]
    o.append(circ(mp))
    o+= [beaker(40,230),beaker(330,520),sol(40,230,Lk),sol(330,520,Rk)]
    if br:
        o.append(bridge())
        if blab: o.append(T(280,142,mix='염다리',size=20,fill=MUTED))
    o.append(plate(124,Lm)); o.append(plate(424,Rm))
    if flow and e:
        dd='M124 90 V50 H262 M298 50 H424 V90' if e=='r' else 'M424 90 V50 H298 M262 50 H124 V90'
        o.append(f'<path d="{dd}" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="36"/>')
    if elab and e:
        if e=='r': o.append(A(160,26,232,26,'minus',3)+A(328,26,400,26,'minus',3))
        else: o.append(A(232,26,160,26,'minus',3)+A(400,26,328,26,'minus',3))
        o.append(T(152,34,tex='e^-',size=21,fill=MINUS,anchor='end')+T(408,34,tex='e^-',size=21,fill=MINUS,anchor='start'))
    if reading: o.append(T(280,92,mix=reading,size=20,weight=700,halo=True))
    o.append(T(104,112,tex=Ltex,size=22,anchor='end')); o.append(T(446,112,tex=Rtex,size=22,anchor='start'))
    o.append(T(135,288,tex=Lsol,size=20)); o.append(T(425,288,tex=Rsol,size=20))
    if br and ions:
        an_,ca_=ions; sL,sR=(1,-1) if e=='r' else (-1,1)
        # 음이온은 산화 전극(전자가 나가는 쪽) 쪽으로, 양이온은 환원 전극 쪽으로
        ax_end= 214 if e=='r' else 346; cx_end= 346 if e=='r' else 214
        ab=chg(ax_end,112,9,'-'); cb=chg(cx_end,112,9,'+')
        if ion_anim:
            o.append(an('move',ab,**{'from':f'{f(60*sL)},0','dur':'1.6','rep':'loop','ease':'lin'}))
            o.append(an('move',cb,**{'from':f'{f(60*sR)},0','dur':'1.6','rep':'loop','ease':'lin','delay':'.8'}))
        else: o.append(ab+cb)
        ya,yc=(170,206)
        if e=='r':
            o.append(T(280,ya,mix=f'← ${an_}$',size=20,fill=MINUS,halo=True)); o.append(T(280,yc,mix=f'${ca_}$ →',size=20,fill=PLUS,halo=True))
        else:
            o.append(T(280,ya,mix=f'${an_}$ →',size=20,fill=MINUS,halo=True)); o.append(T(280,yc,mix=f'← ${ca_}$',size=20,fill=PLUS,halo=True))
    if poles and e:
        neg,pos=(135,425) if e=='r' else (425,135)
        o.append(T(neg,326,mix='(−)극',size=21,weight=700)+T(neg,353,mix='산화 전극',size=20,weight=700,fill=OX))
        o.append(T(pos,326,mix='(+)극',size=21,weight=700)+T(pos,353,mix='환원 전극',size=20,weight=700,fill=RD))
    o.append(extra)
    return ''.join(o)
def cellsvg(label,width=560,vb=(560,370),**k): return svg(vb,width,label,[cell(**k)])

# ═════════════════════ a 덱 ═════════════════════
# 1 표지 — 작은 다니엘 전지 (중심 240,240 반지름 185 안)
def cover():
    s=[]
    s.append(L(150,170,150,110,INK,3)+L(150,110,214,110,INK,3)+L(266,110,330,110,INK,3)+L(330,110,330,170,INK,3))
    s.append(C(240,110,26,INK,3,'#FFFFFF')+T(240,119,mix='V',size=24,weight=700))
    s.append(f'<path d="M150 170 V110 H214 M266 110 H330 V170" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 14" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="30"/>')
    s.append(A(160,80,206,80,'minus',3)+A(274,80,320,80,'minus',3)+T(240,86,tex='e^-',size=20,fill=MINUS))
    s.append(beaker(95,210,190,350)+beaker(270,385,190,350)+sol(95,210,'w',220,348)+sol(270,385,'cu',220,348))
    s.append(bridge(185,295,178,300,20))
    s.append(plate(150,'Zn',160,150,24)+plate(330,'Cu',160,150,24))
    s.append(an('move',chg(205,178,8,'-'),**{'from':'60,0','dur':'1.6','rep':'loop','ease':'lin'}))
    s.append(an('move',chg(275,178,8,'+'),**{'from':'-60,0','dur':'1.6','rep':'loop','ease':'lin','delay':'.8'}))
    s.append(T(128,214,tex=r'\ce{Zn}',size=22,anchor='end')+T(352,214,tex=r'\ce{Cu}',size=22,anchor='start'))
    s.append(T(150,388,mix='(−) 산화',size=20,weight=700,fill=OX)+T(330,388,mix='(+) 환원',size=20,weight=700,fill=RD))
    return svg((480,480),500,'아연 전극과 구리 전극을 염다리와 전압계로 이은 다니엘 전지에서 전자가 도선을 따라 아연에서 구리로 흐른다',s,'fig cover-fig')
FIG['COVER']=cover()

# 2 중단원 도입 — 배터리가 쓰이는 곳
def intro():
    s=[]
    # 스마트폰
    s.append(R(30,40,80,140,INK,3,'#FFFFFF',12)+R(42,58,56,96,MUTED,1.5,'#E3EEFB',4)+C(70,166,5,MUTED,1.5))
    s.append(T(70,212,mix='휴대 전화',size=19))
    # 손목시계
    s.append(R(178,46,24,34,MUTED,2,'#E6E9ED',4)+R(178,140,24,34,MUTED,2,'#E6E9ED',4)+C(190,110,36,INK,3,'#FFFFFF')+L(190,110,190,86,INK,3)+L(190,110,208,118,INK,2.5))
    s.append(T(190,212,mix='손목시계',size=19))
    # 연료 전지 자동차
    s.append(P([(270,150),(282,108),(318,92),(380,92),(410,118),(440,124),(440,150)],INK,3,'#FFFFFF',close=True)+C(300,152,16,INK,3,'#B7C0C9')+C(410,152,16,INK,3,'#B7C0C9'))
    s.append(R(326,106,40,24,FIELD,2,'#E8F5EE',4)+T(346,124,tex=r'\ce{H2}',size=18,fill=FIELD))
    s.append(T(355,212,mix='연료 전지 자동차',size=19))
    # 에너지 전환 상자
    s.append(R(40,246,400,70,OX,2,'#FFF3EC',12))
    s.append(T(240,276,mix='화학 에너지 → 전기 에너지',size=21,weight=700))
    s.append(T(240,303,mix='산화 환원 반응이 전자를 한 방향으로 흐르게 한다',size=19))
    for i,(x,y) in enumerate(((70,104),(190,110),(346,118))):
        s.append(an('pop',C(x,y-44 if i!=2 else y-40,6,EQUI,0,EQUI),**{'dur':'.5','delay':f(.3*i),'o':f'{f(x)},{f(y-44 if i!=2 else y-40)}'}))
    return svg((480,330),480,'휴대 전화, 손목시계, 연료 전지 자동차는 모두 화학 에너지를 전기 에너지로 바꾸는 화학 전지로 작동한다',s)
FIG['INTRO']=intro()

# 4 생각 열기 — 레몬 전지
def lemon():
    s=[]
    s.append(f'<ellipse cx="230" cy="250" rx="150" ry="95" fill="#F7E36B" stroke="#C9A900" stroke-width="3"/>')
    s.append(f'<ellipse cx="200" cy="225" rx="60" ry="22" fill="#FFF6B8" opacity=".7"/>')
    s.append(R(150,150,20,120,MET['Zn'][1],2,MET['Zn'][0],3)+R(290,150,20,120,MET['Cu'][1],2,MET['Cu'][0],3))
    s.append(circ([["wire",[[160,150],[160,70],[212,70]]],["wire",[[248,70],[300,70],[300,150]]]]))
    # LED
    s.append(an('fade',C(230,70,30,'#FFE45C',0,'#FFE45C',extra='opacity=".55"'),**{'dur':'.8','rep':'alt'}))
    s.append(C(230,70,18,PLUS,2.5,'#FFD3D8')+L(222,88,222,104,INK,2)+L(238,88,238,104,INK,2))
    s.append(T(230,30,mix='LED',size=19,weight=700))
    s.append(T(128,168,tex=r'\ce{Zn}',size=20,anchor='end')+T(332,168,tex=r'\ce{Cu}',size=20,anchor='start'))
    s.append(T(230,372,mix='레몬즙(전해질) · 여러 개를 이어 씀',size=19))
    return svg((460,390),430,'레몬에 아연판과 구리판을 꽂고 도선으로 LED에 이으면 불이 켜진다',s)
FIG['LEMON']=lemon()

# 5 연결 — 한 비커에서 아연판 + 황산 구리(II): 전자가 직접 이동
def mix():
    s=[beaker(60,330,90,330),sol(60,330,'cu',130,328)]
    s.append(R(170,60,36,230,MET['Zn'][1],2,MET['Zn'][0],3))
    # 구리 석출
    rnd=random.Random(5)
    for i in range(9):
        y=150+i*16+rnd.uniform(-3,3)
        s.append(an('fade',C(208+rnd.uniform(0,6),y,6,'#9C5A2B',1,'#C47A44'),**{'dur':'.4','delay':f(.6+i*.12)}))
    # 확대 원
    s.append(C(330,200,78,MUTED,1.5,'#FFFFFF',dash='5 4'))
    s.append(L(218,200,252,200,MUTED,1.5,'4 4'))
    s.append(atom(298,200,M_R,'Zn','\\mathrm{Zn}'))
    s.append(atom(368,186,24,'Cu','\\mathrm{Cu}^{2+}'))
    s.append(an('move',elec(338,234,False,6)+elec(352,240,False,6),**{'from':'-26,-4','dur':'1.2','rep':'loop'}))
    s.append(T(330,312,mix='전자가 직접 이동',size=19,fill=MINUS,halo=True))
    # 온도계
    s.append(R(96,40,16,230,MUTED,2,'#FFFFFF',8)+C(104,282,13,PLUS,2,'#FFD3D8'))
    s.append(an('scale',R(100,150,8,130,PLUS,0,PLUS,3),**{'from':'1,.6','o':'104,280','dur':'1.6'}))
    s.append(T(104,28,mix='온도 ↑',size=19,fill=PLUS,weight=700))
    s.append(T(200,354,tex=r'\ce{CuSO4(aq)}',size=18))
    return svg((420,370),420,'아연판을 황산 구리(II) 수용액에 넣으면 아연에서 구리 이온으로 전자가 직접 옮겨 가 구리가 석출되고 온도가 올라간다',s)
FIG['MIX']=mix()

# 6 전기 화학 전지의 두 종류
def two():
    s=[]
    # 갈바니
    s.append(R(10,10,250,250,FIELD,2,'#F2FAF5',12)+T(135,44,mix='갈바니 전지',size=21,weight=700))
    s.append(R(65,110,140,90,INK,2.5,'#FFFFFF',8)+T(135,150,mix='자발적',size=19,weight=700)+T(135,176,mix='산화 환원 반응',size=19))
    s.append(A(135,106,135,72,'field',3)+T(135,66,mix='전기 에너지 발생',size=19,fill=FIELD,weight=700,halo=True))
    s.append(T(135,232,mix='$\\Delta G&lt;0$ · 볼타·다니엘 전지',size=19))
    # 전해
    s.append(R(280,10,250,250,BF,2,'#F5F1FC',12)+T(405,44,mix='전해 전지',size=21,weight=700))
    s.append(R(335,110,140,90,INK,2.5,'#FFFFFF',8)+T(405,150,mix='비자발적',size=19,weight=700)+T(405,176,mix='산화 환원 반응',size=19))
    s.append(A(405,72,405,106,'bfield',3)+T(405,66,mix='전기 에너지 공급',size=19,fill=BF,weight=700,halo=True))
    s.append(T(405,232,mix='$\\Delta G&gt;0$ · 전기 분해',size=19))
    return svg((540,270),540,'갈바니 전지는 자발적 산화 환원 반응으로 전기 에너지를 만들고, 전해 전지는 전기 에너지를 공급해 비자발적 반응을 일으킨다',s)
FIG['TWO']=two()

# 7 두 반쪽 반응을 나누면 — 한 방향 전자 흐름
FIG['SPLIT']=cellsvg('산화 반쪽 반응과 환원 반쪽 반응을 두 용기로 나누고 도선으로 이으면 전자가 산화 전극에서 환원 전극으로 한 방향으로 흐른다',
    meter='G',br=True,ions=None,blab=True)

# 8 볼타 전지 (볼타 더미)
def volta():
    s=[]
    y=330
    for i in range(4):
        s.append(R(110,y-20,160,20,MET['Cu'][1],2,MET['Cu'][0],3))   # 구리판(아래)
        s.append(R(114,y-34,152,14,'#9FC3DD',1.5,'#DDEEF8',3))        # 소금물 적신 골판지
        s.append(R(110,y-54,160,20,MET['Zn'][1],2,MET['Zn'][0],3))   # 아연판(위)
        y-=60
    s.append(circ([["wire",[[270,100],[330,100],[330,180]]],["bulb",[330,200],{"r":18,"on":True}],["wire",[[330,220],[330,320],[270,320]]]]))
    s.append(f'<path d="M270 100 H330 V180 M330 220 V320 H270" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="30"/>')
    s.append(A(350,120,350,170,'minus',3)+T(368,152,tex='e^-',size=19,fill=MINUS,anchor='start'))
    s.append(L(110,86,70,70,MUTED,1.5)+T(66,66,mix='아연판',size=19,anchor='end'))
    s.append(L(114,114,70,124,MUTED,1.5)+T(66,128,mix='소금물||골판지',size=19,anchor='end'))
    s.append(L(110,140,70,180,MUTED,1.5)+T(66,186,mix='구리판',size=19,anchor='end'))
    s.append(T(190,32,mix='맨 위 아연 · 맨 아래 구리',size=19,weight=700))
    return svg((420,350),400,'아연판, 소금물에 적신 골판지, 구리판을 차례로 쌓은 볼타 더미를 도선으로 이으면 전류가 흐른다',s)
FIG['VOLTA']=volta()

# 9 다니엘 전지 구성 (그림 Ⅲ-25 (가) 새로 그림)
FIG['DANIELL']=cellsvg('황산 아연 용액의 아연 전극과 황산 구리(II) 용액의 구리 전극을 도선과 염다리로 이은 다니엘 전지',
    ions=(r'\ce{SO4^2-}',r'\ce{Na+}'))

# 10 전극 표면(미시) + 작동 뒤 전극
def surf():
    s=[]
    for k,(x0,tit,col) in enumerate(((10,'산화 전극 표면',OX),(290,'환원 전극 표면',RD))):
        s.append(R(x0,10,260,290,col,2,'#FFFFFF',12)+T(x0+130,40,mix=tit,size=20,weight=700,fill=col))
    # 아연 표면: 금속 격자 왼쪽, 용액 오른쪽
    s.append(R(22,56,92,190,MET['Zn'][1],1.5,'#E9EDF1',6))
    for i in range(3):
        for j in range(2): s.append(atom(44+j*46,90+i*58,M_R-8,'Zn','-'))
    s.append(an('move',atom(196,140,26,'Zn','\\mathrm{Zn}^{2+}'),**{'from':'-106,6','dur':'1.4','ease':'out'}))
    s.append(an('fade',elec(68,232,True,9),**{'dur':'.4','delay':'.8'}))
    s.append(an('fade',elec(96,232,True,9),**{'dur':'.4','delay':'.9'}))
    s.append(T(196,196,mix='용액으로',size=19,halo=True))
    s.append(T(140,284,mix='전자 $2$개는 전극에 남음',size=19,fill=MINUS,halo=True))
    # 구리 표면
    s.append(R(446,56,92,190,MET['Cu'][1],1.5,'#F6E7D6',6))
    for i in range(3):
        for j in range(2):
            if (i,j)!=(0,0): s.append(atom(470+j*46,90+i*58,M_R-8,'Cu','-'))
    s.append(an('move',atom(470,90,M_R-8,'Cu','-'),**{'from':'-120,40','dur':'1.4','ease':'out','delay':'.4'}))
    s.append(atom(352,190,22,'Cu','\\mathrm{Cu}^{2+}','d') if False else '')
    s.append(an('fade',elec(470,232,True,9),**{'dur':'.4','delay':'.0'}))
    s.append(an('fade',elec(498,232,True,9),**{'dur':'.4','delay':'.1'}))
    s.append(T(372,120,mix='$\\ce{Cu^2+}$이||전자 $2$개 받아',size=19,halo=True))
    s.append(T(372,196,mix='구리 원자로||석출',size=19,halo=True))
    return svg((560,310),560,'산화 전극 표면에서는 아연 원자가 전자 두 개를 남기고 아연 이온으로 녹아 나가고, 환원 전극 표면에서는 구리 이온이 전자 두 개를 받아 구리 원자로 석출된다',s)
FIG['SURF']=surf()
def after():
    s=[]
    s.append(T(110,26,mix='작동 전',size=19,weight=700)+T(330,26,mix='작동 뒤',size=19,weight=700))
    s.append(plate(80,'Zn',40,150,28)+plate(140,'Cu',40,150,28))
    s.append(R(286,40,28,150,MET['Zn'][1],2,MET['Zn'][0],3,extra='') .replace('width="28"','width="28"'))
    # 작동 뒤: 아연은 아래쪽이 가늘어짐, 구리는 두꺼워짐
    s[-1]=P([(286,40),(314,40),(314,110),(306,190),(294,190),(286,110)],MET['Zn'][1],2,MET['Zn'][0],close=True)
    s.append(an('fade',P([(346,40),(374,40),(374,108),(382,190),(338,190),(346,108)],'#9C5A2B',2,'#C47A44',close=True),**{'dur':'1.2'}))
    s.append(T(80,218,tex=r'\ce{Zn}',size=19)+T(140,218,tex=r'\ce{Cu}',size=19)+T(296,216,mix='$\\ce{Zn}$ 줄어듦',size=19,fill=OX)+T(372,244,mix='$\\ce{Cu}$ 늘어남',size=19,fill=RD))
    s.append(A(196,110,250,110,'muted',3))
    return svg((440,258),440,'전지가 작동한 뒤 산화 전극의 아연은 줄어들고 환원 전극의 구리는 늘어난다',s)
FIG['AFTER']=after()

# 11 전자와 이온의 이동 (염다리 이온 강조)
FIG['MOVE']=cellsvg('전자는 도선을 따라 아연에서 구리로, 염다리의 음이온은 산화 전극 쪽으로, 양이온은 환원 전극 쪽으로 이동한다',vb=(560,400),
    ions=(r'\ce{SO4^2-}',r'\ce{Na+}'),blab=False,
    extra=step('m1',R(166,96,228,32,PLUS,2.5,'none',10,'6 5')+L(280,128,280,150,PLUS,1.5,'4 3')+T(280,390,mix='염다리 속에서는 이온만 이동 — 전자는 지나가지 않는다',size=20,fill=PLUS,weight=700)))

# 12 반쪽 전지 구조
def halfcell():
    s=[]
    for k,(x0,m,tex,soltex,kind,nm,col,sgn,lab) in enumerate(((20,'Zn',r'\ce{Zn}',r'\ce{Zn^2+(aq)}','w','산화 전극(anode)',OX,'(−)','전자 방출'),(290,'Cu',r'\ce{Cu}',r'\ce{Cu^2+(aq)}','cu','환원 전극(cathode)',RD,'(+)','전자 받음'))):
        s.append(beaker(x0+20,x0+230,90,280)+sol(x0+20,x0+230,kind,130,278)+plate(x0+125,m,60,180,30))
        s.append(T(x0+125,40,mix=nm,size=20,weight=700,fill=col))
        s.append(T(x0+170,92,tex=tex,size=20,anchor='start'))
        s.append(T(x0+125,264,tex=soltex,size=19,halo=True))
        s.append(T(x0+125,316,mix=f'{sgn}극 · {lab}',size=19,weight=700))
    s.append(an('pop',C(145,160,22,MINUS,2,'#DCE9FA')+T(145,167,tex='-',size=22,fill=MINUS),**{'dur':'.6','o':'145,160'}))
    s.append(an('pop',C(415,160,22,PLUS,2,'#FFE4E7')+T(415,167,tex='+',size=22,fill=PLUS),**{'dur':'.6','delay':'.3','o':'415,160'}))
    s.append(L(64,200,24,200,MUTED,1.5)+T(22,190,mix='전해질',size=18,anchor='start') if False else '')
    return svg((540,330),540,'반쪽 전지는 전해질 용액과 전극으로 이루어지며, 산화 전극은 전자가 남아 음의 전하를, 환원 전극은 양의 전하를 띤다',s)
FIG['HALF']=halfcell()

# 14 전지 표기법
def notation():
    s=[]
    parts=[(62,r'\ce{Zn(s)}'),(120,'|'),(200,r'\ce{Zn^2+(aq)}'),(290,r'\|'),(380,r'\ce{Cu^2+(aq)}'),(460,'|'),(518,r'\ce{Cu(s)}')]
    for x,t in parts: s.append(T(x,90,tex=t,size=28))
    s.append(P([(40,110),(40,122),(260,122),(260,110)],OX,2.5)+T(150,148,mix='산화 반쪽 전지 (왼쪽)',size=19,fill=OX,weight=700))
    s.append(P([(320,110),(320,122),(540,122),(540,110)],RD,2.5)+T(430,148,mix='환원 반쪽 전지 (오른쪽)',size=19,fill=RD,weight=700))
    s.append(L(120,40,120,58,MUTED,1.5)+T(120,30,mix='상 경계',size=18,fill=MUTED)+L(460,40,460,58,MUTED,1.5)+T(460,30,mix='상 경계',size=18,fill=MUTED))
    s.append(step('n1',L(290,170,290,190,MUTED,1.5)+T(290,212,mix='이중 선 = 염다리',size=19,weight=700)))
    s.append(step('n2',A(80,240,500,240,'minus',3.5)+T(290,270,mix='전자의 흐름: 왼쪽 → 오른쪽',size=19,fill=MINUS,weight=700)))
    return svg((580,284),580,'전지 표기: 산화 반쪽 전지를 왼쪽, 환원 반쪽 전지를 오른쪽에 쓰고 상 경계는 세로선, 염다리는 이중 선으로 나타낸다',s)
FIG['NOTE']=notation()

# 15 염다리가 없으면 / 있으면
def imbal(stage):
    o=[beaker(40,230),beaker(330,520),sol(40,230,'w'),sol(330,520,'cu'),plate(124,'Zn'),plate(424,'Cu')]
    o.append(circ([["wire",[[124,90],[124,50],[262,50]]],["wire",[[298,50],[424,50],[424,90]]],["meter",[280,50],"V",{"r":18}]]))
    if stage==0:
        for i,(x,y) in enumerate(((70,200),(170,230),(90,260),(190,190),(160,268))):
            o.append(an('pop',chg(x,y,11,'+'),**{'dur':'.5','delay':f(.15*i),'o':f'{f(x)},{f(y)}'}))
        for i,(x,y) in enumerate(((370,200),(470,230),(390,262),(490,190),(460,268))):
            o.append(an('pop',chg(x,y,11,'-'),**{'dur':'.5','delay':f(.15*i),'o':f'{f(x)},{f(y)}'}))
        o.append(T(135,176,mix='양전하 쌓임',size=19,weight=700,fill=PLUS,halo=True)+T(425,176,mix='음전하 쌓임',size=19,weight=700,fill=MINUS,halo=True))
        o.append(T(280,92,mix='? V',size=20,weight=700,halo=True))
        o.append(T(280,340,mix='염다리 없음 — 두 용액에 전하가 쌓인다',size=20,weight=700))
    else:
        o.append(bridge())
        o.append(an('move',chg(214,112,10,'-'),**{'from':'70,0','dur':'1.5','rep':'loop','ease':'lin'}))
        o.append(an('move',chg(346,112,10,'+'),**{'from':'-70,0','dur':'1.5','rep':'loop','ease':'lin','delay':'.75'}))
        o.append(T(280,170,mix='← 음이온',size=19,fill=MINUS,halo=True)+T(280,206,mix='양이온 →',size=19,fill=PLUS,halo=True))
        o.append(f'<path d="M124 90 V50 H262 M298 50 H424 V90" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="36"/>')
        o.append(T(280,92,mix='1.10 V',size=20,weight=700,halo=True))
        o.append(T(280,340,mix='염다리가 전하 균형 유지 → 작동이 계속된다',size=20,weight=700))
    return svg((560,356),540,'염다리가 없으면 산화 전극 쪽 용액에 양전하, 환원 전극 쪽 용액에 음전하가 쌓여 전지가 멈추고, 염다리가 있으면 이온이 이동해 전하 균형이 유지된다' if stage==0 else '염다리의 음이온은 산화 전극 쪽, 양이온은 환원 전극 쪽으로 이동해 전하 균형을 유지한다',o)
FIG['IMB0']=imbal(0).replace('<text class="tex"','<text class="tex" data-overlap="ok"'); FIG['IMB1']=imbal(1).replace('<text class="tex"','<text class="tex" data-overlap="ok"')

# 16 염다리 종류
def btypes():
    s=[]
    # U자관 젤
    s.append(T(90,28,mix='U자형 유리관',size=19,weight=700))
    d='M50 170 V70 H130 V170'
    s.append(f'<path d="{d}" fill="none" stroke="{GLS}" stroke-width="26"/><path d="{d}" fill="none" stroke="#F6F0E0" stroke-width="20"/>')
    s.append(C(50,176,10,GLS,2,'#FFFFFF')+C(130,176,10,GLS,2,'#FFFFFF'))
    s.append(T(90,214,mix='고농도 이온 젤||(한천 + $\\ce{KNO3}$)',size=18))
    # 다공성 원반
    s.append(T(280,28,mix='다공성 원반',size=19,weight=700))
    s.append(R(220,60,50,120,GLS,2.5,'#DDEEF8',4)+R(290,60,50,120,GLS,2.5,'#3E8ED0',4,extra='fill-opacity=".3"'))
    s.append(R(268,90,24,60,'#8C7A5B',2,'#D9CBA8',3))
    for i in range(6): s.append(C(276+(i%2)*8,98+i*9,2.2,'#8C7A5B',0,'#8C7A5B'))
    s.append(T(280,214,mix='작은 구멍으로||이온만 통과',size=18))
    # 거름종이 띠
    s.append(T(462,28,mix='거름종이 띠',size=19,weight=700))
    s.append(P([(410,170),(410,80),(514,80),(514,170)],'#C8B98F',7)+P([(410,170),(410,80),(514,80),(514,170)],'#F3EBD3',3))
    s.append(T(462,214,mix='$\\ce{KNO3}$ 용액에||적셔 씀(수업 실험)',size=18))
    return svg((560,250),560,'염다리의 여러 형태: 이온 젤을 채운 U자형 유리관, 다공성 원반, 질산 칼륨 용액에 적신 거름종이 띠',s)
FIG['BTYPE']=btypes()

# 17 비활성 전극 (그림 Ⅲ-26 새로 그림)
FIG['INERT']=cellsvg('흑연 전극 두 개를 쓴 전지: 왼쪽에서는 아이오딘화 이온이 산화되어 아이오딘이 되고, 오른쪽에서는 과망가니즈산 이온이 환원된다',
    Lm='C',Rm='C',Ltex=r'\ce{C}',Rtex=r'\ce{C}',Lsol=r'\ce{I-}, \ce{I2}',Rsol=r'\ce{MnO4-}, \ce{H+}, \ce{Mn^2+}',Lk='i',Rk='mn',
    ions=(r'\ce{NO3-}',r'\ce{K+}'))

# 18·19 예제 Ⅲ-10
FIG['EX10A']=cellsvg('아연 전극과 백금 전극을 쓴 전지: 아연이 산화되고 코발트(III) 이온이 코발트(II) 이온으로 환원된다',width=500,
    Rm='Pt',Rtex=r'\ce{Pt}',Lsol=r'\ce{Zn^2+(aq)}',Rsol=r'\ce{Co^3+}, \ce{Co^2+}',Rk='co',poles=True,ions=None,blab=True)
FIG['EX10B']=cellsvg('니켈 전극과 은 전극을 쓴 전지: 니켈이 산화되고 은 이온이 환원된다',width=500,
    Lm='Ni',Ltex=r'\ce{Ni}',Rm='Ag',Rtex=r'\ce{Ag}',Lsol=r'\ce{Ni^2+(aq)}',Rsol=r'\ce{Ag+(aq)}',Rk='w',poles=True,ions=None)

# 20 확인 02 — 마그네슘과 수소 이온 (기체 전극)
def mgh():
    ex=(R(404,76,40,200,'#FFFFFF',2,'#FFFFFF',18,extra='fill-opacity=".35" stroke="#7E8B98"')+A(470,96,438,108,'ink',2.5)+T(474,92,tex=r'\ce{H2}(g)',size=21,anchor='start')
        +an('move',C(416,240,5,'#7FA8C9',2,'#FFFFFF')+C(432,218,4,'#7FA8C9',2,'#FFFFFF'),**{'from':'0,30','dur':'1.8','rep':'loop'}))
    return svg((560,370),500,'마그네슘 전극과 수소 기체를 넣는 백금 전극으로 만든 전지',[cell(Lm='Mg',Ltex=r'\ce{Mg}',Rm='Pt',Rtex='',Lsol=r'\ce{Mg^2+(aq)}',Rsol=r'\ce{H+(aq)}',Rk='w',ions=None,poles=False,elab=False,flow=False,extra=ex)])
FIG['MGH']=mgh()

# 22 탐구 과정 카드
def proc():
    s=[]
    W=262
    tit=['① 전극 닦기','② 반쪽 전지','③ 염다리 걸치기','④ 전압 재기']
    for i in range(4):
        x0=i*(W+8)
        s.append(R(x0+4,4,W,200,MUTED,1.5,'#FFFFFF',12)+T(x0+W/2+4,32,mix=tit[i],size=19,weight=700))
    # 1 사포
    s.append(R(60,60,30,120,MET['Zn'][1],2,MET['Zn'][0],3)+R(160,60,30,120,MET['Cu'][1],2,MET['Cu'][0],3))
    s.append(an('move',R(52,100,46,26,'#8C7A5B',1.5,'#D9CBA8',4),**{'from':'0,-30','dur':'.6','rep':'alt','ease':'io'}))
    s.append(T(136,196,mix='산화막 제거',size=18))
    # 2 비커
    x=270; s.append(beaker(x+30,x+110,70,180)+sol(x+30,x+110,'w',110,178)+beaker(x+150,x+230,70,180)+sol(x+150,x+230,'cu',110,178))
    s.append(T(x+70,160,tex=r'\ce{ZnSO4}',size=18)+T(x+190,160,tex=r'\ce{CuSO4}',size=18)+T(x+132,196,mix='1.0 M씩',size=18))
    # 3 염다리
    x=540; s.append(beaker(x+30,x+110,90,180)+sol(x+30,x+110,'w',120,178)+beaker(x+150,x+230,90,180)+sol(x+150,x+230,'cu',120,178))
    s.append(an('move',P([(x+90,170),(x+90,74),(x+170,74),(x+170,170)],'#C8B98F',7)+P([(x+90,170),(x+90,74),(x+170,74),(x+170,170)],'#F3EBD3',3),**{'from':'0,-24','dur':'.9','ease':'out'}))
    s.append(T(x+132,196,mix='조건을 바꾸며',size=18))
    # 4 전압계
    x=810; s.append(R(x+60,56,150,92,INK,2.5,'#FFFFFF',10)+R(x+76,70,118,40,MUTED,1.5,'#E8F5EE',4)+T(x+135,99,mix='1.08 V',size=21,weight=700,fill=FIELD))
    s.append(T(x+95,138,mix='(−)',size=18,weight=700)+T(x+176,138,mix='(+)',size=18,weight=700))
    s.append(T(x+135,196,mix='30초 뒤 기록',size=18))
    return svg((1080,210),1080,'탐구 과정: 금속판을 사포로 닦고, 두 반쪽 전지를 만들고, 염다리를 걸친 뒤 전압계로 전압을 잰다',s)
FIG['PROC']=proc()

# 24 결과 예시 막대
RES=[('없음','—',0.00,0.0),('거름종이','증류수',0.68,0.0),('거름종이','0.1 M',1.10,1.6),('거름종이','1.0 M',1.10,6.8),('면실','1.0 M',1.10,2.1),('한천 젤','포화',1.10,10.1)]   # 실험실 PRE 시험 값
def result():
    s=[]; x0,y0,H=70,250,190
    s.append(L(x0,y0,520,y0,MUTED,2)+L(x0,y0,x0,40,MUTED,2))
    for v in (0,5,10):
        y=y0-v/12*H; s.append(L(x0-6,y,x0,y,MUTED,2)+T(x0-10,y+6,mix=str(v),size=18,anchor='end'))
    s.append(T(x0+6,30,mix='전류 (부하 100 Ω) [mA]',size=18,anchor='start',fill=MUTED))
    for i,(m,c,v,I) in enumerate(RES):
        x=x0+20+i*74; h=I/12*H
        if h>0: s.append(an('scale',R(x,y0-h,46,h,FIELD,1.5,FIELD,3,extra='fill-opacity=".55"'),**{'from':'1,0','o':f'{f(x+23)},{y0}','dur':'.8','delay':f(.1*i)}))
        s.append(T(x+23,y0-h-8,mix=f'{I:.1f}',size=18))
        s.append(T(x+23,y0+24,mix=m,size=18)+T(x+23,y0+46,mix=c,size=18))
    return svg((540,310),540,'염다리 조건별 전류 예시: 염다리가 없거나 증류수이면 전류가 거의 없고, 이온 농도가 클수록 전류가 크다',s)
FIG['RESULT']=result()

# 25 알칼리 전지의 분리막
def sep():
    s=[]; x,y,w,h=150,40,170,270
    s.append(R(x,y,w,h,INK,3,'#E6E9ED',14)+R(x+w/2-14,y-16,28,16,INK,2,'#B7C0C9',3))
    s.append(R(x+10,y+10,w-20,h-20,RD,0,'#2B2F35',10,extra='fill-opacity=".8"'))
    s.append(R(x+38,y+30,w-76,h-60,EQUI,3,'#FFF4E8',8,'7 5'))
    s.append(R(x+48,y+40,w-96,h-80,OX,0,'#C9D3DD',6))
    s.append(L(x+w/2,y+6,x+w/2,y+h-50,INK,3))
    for i in range(5):
        yy=y+70+i*36
        s.append(an('move',chg(x+46,yy,7,'-'),**{'from':'-22,0','dur':'1.4','rep':'loop','delay':f(.2*i),'ease':'lin'}))
    s.append(L(x+w+10,y+70,x+w-14,y+70,MUTED,1.5)+T(x+w+14,y+77,mix='$\\ce{MnO2}$ (환원 전극 쪽)',size=19,anchor='start',fill=RD))
    s.append(L(x+w+10,y+150,x+w-40,y+150,EQUI,2)+T(x+w+14,y+157,mix='분리막 — 염다리 역할',size=19,anchor='start',fill=EQUI,weight=700))
    s.append(L(x+w+10,y+230,x+w/2+20,y+230,MUTED,1.5)+T(x+w+14,y+237,mix='$\\ce{Zn}$ 가루 (산화 전극 쪽)',size=19,anchor='start',fill=OX))
    s.append(L(x-10,y+120,x+20,y+120,MUTED,1.5)+T(x-14,y+127,mix='$\\ce{KOH}$ 전해질',size=19,anchor='end'))
    s.append(T(x-14,y+180,mix='$\\ce{OH-}$ 이동',size=19,anchor='end',fill=MINUS))
    return svg((540,330),520,'알칼리 전지 단면: 아연 가루와 이산화 망가니즈 사이의 분리막이 전극은 떼어 놓고 수산화 이온만 지나가게 하여 염다리 역할을 한다',s)
FIG['SEP']=sep()

# 26 화학사 — 다공성 단지 다니엘 전지
def hist():
    s=[]
    s.append(R(60,60,250,250,MET['Cu'][1],5,'#3E8ED0',16,extra='fill-opacity=".28"'))
    s.append(R(130,90,110,200,'#8C7A5B',3,'#F3EDE0',12,'5 4'))
    s.append(R(170,40,30,230,MET['Zn'][1],2,MET['Zn'][0],3))
    s.append(circ([["wire",[[185,40],[185,20],[360,20],[360,90]]],["bulb",[360,110],{"r":18,"on":True}],["wire",[[360,130],[360,180],[310,180]]]]))
    s.append(L(240,250,340,270,MUTED,1.5)+T(344,276,mix='다공성 단지||(이온 통로)',size=19,anchor='start'))
    s.append(L(200,80,340,60,MUTED,1.5)+T(344,62,mix='아연 막대',size=19,anchor='start') if False else '')
    s.append(L(96,280,40,330,MUTED,1.5)+T(36,350,mix='구리 용기 + 황산 구리(Ⅱ)',size=19,anchor='start'))
    s.append(T(214,170,tex=r'\ce{Zn}',size=20,anchor='start',halo=True))
    return svg((500,370),460,'다공성 단지 안에 아연 막대를 넣고 황산 구리(II) 용액이 든 구리 용기에 담근 개량된 다니엘 전지',s)
FIG['HIST']=hist()

# ═════════════════════ b 덱 ═════════════════════
def coverb():
    s=[]
    x=160; s.append(L(x,96,x,400,INK,3))
    pts=[(1.23,r'\ce{O2}/\ce{H2O}'),(0.34,r'\ce{Cu^2+}/\ce{Cu}'),(0.0,r'\ce{H+}/\ce{H2}'),(-0.76,r'\ce{Zn^2+}/\ce{Zn}')]
    def Y(E): return 250-E*110
    for E,t in pts:
        y=Y(E); s.append(L(x-10,y,x+10,y,INK,3)+T(x-16,y+7,mix=f'{E:+.2f}' if E else '0.00',size=20,anchor='end')+T(x+22,y+7,tex=t,size=20,anchor='start'))
    s.append(f'<line x1="{x}" y1="{Y(0)}" x2="340" y2="{Y(0)}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    s.append(T(x,84,tex=r'E^\circ\ [\text{V}]',size=20))
    s.append(an('scale',L(330,Y(0.34),330,Y(-0.76),EQUI,4),**{'from':'1,0','o':f'330,{f(Y(-0.76))}','dur':'1.2'}))
    s.append(L(316,Y(0.34),344,Y(0.34),EQUI,3)+L(316,Y(-0.76),344,Y(-0.76),EQUI,3))
    s.append(T(352,Y(-0.2),mix='$E^\\circ_\\text{전지}$||$=1.10$ V',size=21,anchor='start',weight=700,fill=EQUI))
    return svg((480,480),500,'표준 환원 전위 눈금 위의 구리와 아연 반쪽 반응: 두 값의 차가 다니엘 전지의 표준 전지 전위 1.10 V이다',s,'fig cover-fig')
FIG['COVERB']=coverb()
FIG['REVIEW']=cellsvg('다니엘 전지: 아연 전극이 산화 전극, 구리 전극이 환원 전극이며 염다리 이온이 전하 균형을 유지한다',width=470,
    ions=(r'\ce{SO4^2-}',r'\ce{Na+}'))

# 4 표 Ⅲ-9 막대
T9=[('알칼리 전지',1.5),('납축전지 전지 하나',2.1),('수은 전지',1.3),('리튬 이온 전지',3.7),('전기뱀장어 세포 하나',0.15),('오징어 신경 세포막',0.070)]
def t9():
    s=[]; x0=230; W=260
    for i,(n,v) in enumerate(T9):
        y=26+i*46; w=v/3.7*W
        s.append(T(x0-12,y+22,mix=n,size=19,anchor='end'))
        s.append(an('scale',R(x0,y+4,max(w,3),26,EQUI,1.5,EQUI,3,extra='fill-opacity=".55"'),**{'from':'0,1','o':f'{x0},{y+17}','dur':'.8','delay':f(.1*i)}))
        s.append(T(x0+max(w,3)+8,y+24,mix=('0.070' if v==0.070 else f'{v:g}')+' V',size=19,anchor='start'))
    return svg((560,300),540,'여러 전지의 전압 비교: 리튬 이온 전지 3.7 V가 가장 크고 오징어 신경 세포막 0.070 V가 가장 작다',s)
FIG['T9']=t9()

# 5 전위차와 전자 이동 (비유)
def pot():
    s=[]
    s.append(R(20,40,120,240,MINUS,2,'#EAF2FC',10)+T(80,30,mix='(−)극',size=20,weight=700))
    s.append(R(400,40,120,240,PLUS,2,'#FDECEE',10)+T(460,30,mix='(+)극',size=20,weight=700))
    s.append(T(80,170,mix='낮은 전위',size=19)+T(460,170,mix='높은 전위',size=19))
    s.append(L(140,120,400,120,INK,3))
    s.append(an('move',elec(370,120),**{'from':'-210,0','dur':'2','rep':'loop','ease':'lin'}))
    s.append(A(170,90,370,90,'minus',3)+T(270,78,mix='전자는 양의 전위 쪽으로',size=19,fill=MINUS,halo=True))
    s.append(L(80,300,460,300,MUTED,1.5)+L(80,292,80,308,MUTED,1.5)+L(460,292,460,308,MUTED,1.5)+T(270,330,mix='전위차 = 전지 전위 $E_\\text{전지}$ (자발적이면 $+$)',size=19,halo=True))
    s.append(T(270,200,mix='전자가 이동하며||일을 한다',size=19,halo=True))
    return svg((540,344),520,'전자는 낮은 전위의 (−)극에서 높은 전위의 (+)극으로 이동하며 일을 하고, 두 극의 전위차가 전지 전위이다',s)
FIG['POT']=pot()

# 8 높이 비유: 기준이 필요
def sea():
    s=[]
    s.append(f'<path d="M20 250 L90 120 L140 170 L200 60 L270 250 Z" fill="#DDE7D3" stroke="#6B8F5A" stroke-width="2"/>')
    s.append(R(10,250,300,50,'#9FC3DD',1.5,'#DDEEF8'))
    s.append(L(10,250,320,250,MUTED,2,'6 5')+T(160,284,mix='해수면 = 0 m (기준)',size=19,fill=INK))
    s.append(L(200,60,200,250,EQUI,2.5)+T(260,140,mix='높이',size=20,anchor='start',fill=EQUI,weight=700)+L(204,150,256,140,EQUI,1.5))
    s.append(R(340,40,190,240,MUTED,1.5,'#FFFFFF',12)+T(435,70,mix='전위도 기준이 필요',size=19,weight=700))
    s.append(L(360,190,510,190,MUTED,2,'6 5')+T(435,182,mix='표준 수소 전극 = 0.00 V',size=18,fill=MUTED))
    s.append(L(380,120,500,120,INK,2.5)+T(440,112,mix='$\\ce{Cu^2+}$/$\\ce{Cu}$ $+0.34$',size=18))
    s.append(L(380,250,500,250,INK,2.5)+T(440,242,mix='$\\ce{Zn^2+}$/$\\ce{Zn}$ $-0.76$',size=18))
    return svg((540,310),540,'산의 높이를 해수면 기준으로 재듯, 반쪽 전지의 전위는 표준 수소 전극을 0 V 기준으로 잰 상댓값이다',s)
FIG['SEA']=sea()

# 9 표준 수소 전극
def she():
    s=[beaker(60,300,120,330),sol(60,300,'w',160,328)]
    s.append(R(150,70,60,230,GLS,2.5,'#FFFFFF',22,extra='fill-opacity=".4"'))
    s.append(L(180,20,180,270,INK,3)+R(162,240,36,50,MET['Pt'][1],2,MET['Pt'][0],2))
    s.append(A(60,90,148,100,'ink',3)+T(56,82,tex=r'\ce{H2}(g)\ 1\ \text{atm}',size=19,anchor='start'))
    s.append(an('move',C(170,232,5,'#7FA8C9',2,'#FFFFFF')+C(192,222,4,'#7FA8C9',2,'#FFFFFF')+C(182,206,4.5,'#7FA8C9',2,'#FFFFFF'),**{'from':'0,40','dur':'1.6','rep':'loop'}))
    s.append(L(198,270,330,280,MUTED,1.5)+T(334,286,mix='백금 전극',size=19,anchor='start'))
    s.append(L(270,300,330,320,MUTED,1.5)+T(334,326,mix='$1\\ \\text{M}$ $\\ce{H3O+}(aq)$',size=19,anchor='start'))
    s.append(R(314,80,246,100,INK,2,'#FFFFFF',10)+T(437,118,tex=r'\ce{2H+(aq) + 2e- -> H2(g)}',size=19)+T(437,158,tex=r'E^\circ_\text{기준}=0.00\ \text{V}',size=20))
    return svg((570,350),520,'표준 수소 전극: 1 M 하이드로늄 이온 용액에 담근 백금 전극에 1 atm 수소 기체를 불어 넣는다',s)
FIG['SHE']=she()

# 10 표준 환원 전위 재기 — 구리, 아연
def sheX(m,E,lab):
    ex=(R(104,76,40,200,'#FFFFFF',2,'#FFFFFF',18,extra='fill-opacity=".35" stroke="#7E8B98"')+A(40,96,100,104,'ink',2.5)+T(36,88,tex=r'\ce{H2}',size=21,anchor='start')
        +an('move',C(116,240,5,'#7FA8C9',2,'#FFFFFF')+C(132,218,4,'#7FA8C9',2,'#FFFFFF'),**{'from':'0,30','dur':'1.8','rep':'loop'}))
    if m=='Cu':
        return cell(Lm='Pt',Ltex='',Rm='Cu',Rtex=r'\ce{Cu}',Lsol=r'1\ \text{M}\ \ce{H3O+}',Rsol=r'1\ \text{M}\ \ce{Cu^2+}',Lk='w',Rk='cu',e='r',ions=None,reading='0.34 V',extra=ex,poles=True)
    return cell(Lm='Pt',Ltex='',Rm='Zn',Rtex=r'\ce{Zn}',Lsol=r'1\ \text{M}\ \ce{H3O+}',Rsol=r'1\ \text{M}\ \ce{Zn^2+}',Lk='w',Rk='w',e='l',ions=None,reading='0.76 V',extra=ex,poles=True)
FIG['SHECU']=svg((560,370),470,'표준 수소 전극을 왼쪽, 구리 반쪽 전지를 오른쪽에 이으면 전자가 수소 전극에서 구리 쪽으로 흐르고 전압은 0.34 V이다',[sheX('Cu',0.34,'')])
FIG['SHEZN']=svg((560,370),470,'표준 수소 전극과 아연 반쪽 전지를 이으면 전자는 아연에서 수소 전극 쪽으로 흐르고 전압은 0.76 V이다 — 아연이 산화 전극이 된다',[sheX('Zn',-0.76,'')])

# 11–12 전위 사다리
TAB=[(2.87,r'\ce{F2}/\ce{F-}'),(1.23,r'\ce{O2}/\ce{H2O}'),(0.40,r'\ce{O2}/\ce{OH-}'),(0.34,r'\ce{Cu^2+}/\ce{Cu}'),(0.0,r'\ce{H+}/\ce{H2}'),(-0.28,r'\ce{Co^2+}/\ce{Co}'),(-0.76,r'\ce{Zn^2+}/\ce{Zn}'),(-2.37,r'\ce{Mg^2+}/\ce{Mg}'),(-2.70,r'\ce{Na+}/\ce{Na}')]
def ladder(items,Emax,Emin,H=300,x=150,diff=None,w=520,arrows=True,title=True,label='',hl=()):
    s=[]; top=40
    def Y(E): return top+(Emax-E)/(Emax-Emin)*H
    s.append(L(x,top-10,x,top+H+10,INK,3))
    if title: s.append(T(x,22,tex=r'E^\circ\ [\text{V}]',size=19))
    ys=[Y(E) for E,_ in items]; ly=ys[:]
    for _ in range(60):
        for i in range(1,len(ly)):
            if ly[i]-ly[i-1]<25: d=(25-(ly[i]-ly[i-1]))/2; ly[i]+=d; ly[i-1]-=d
    for (E,t),y,yl in zip(items,ys,ly):
        col=EQUI if t in hl else INK
        s.append(L(x-10,y,x+10,y,col,3))
        if abs(yl-y)>2: s.append(L(x-12,y,x-24,yl,MUTED,1.2)+L(x+12,y,x+20,yl,MUTED,1.2))
        s.append(T(x-28,yl+7,mix=('%+.2f'%E if E else '0.00') if abs(E*100-round(E*100))<1e-6 else ('%+.3f'%E),size=19,anchor='end')+T(x+24,yl+7,tex=t,size=19,anchor='start',fill=col if t in hl else None))
    if arrows:
        s.append(A(w-60,Y(Emin)-10,w-60,Y(Emax)+10,'rd',3)+T(w-70,Y(Emax)+4,mix='환원되기 쉬움||(강한 산화제)',size=18,anchor='end',fill=RD))
        s.append(T(w-70,Y(Emin)-30,mix='산화되기 쉬움||(강한 환원제)',size=18,anchor='end',fill=OX))
    if diff:
        Eh,El,lab=diff; xx=x+200
        s.append(an('scale',L(xx,Y(Eh),xx,Y(El),EQUI,4),**{'from':'1,0','o':f'{xx},{f(Y(El))}','dur':'1.2','on':'step'}) if False else
                 step('d1',L(xx,Y(Eh),xx,Y(El),EQUI,4)+L(xx-14,Y(Eh),xx+14,Y(Eh),EQUI,3)+L(xx-14,Y(El),xx+14,Y(El),EQUI,3)+T(xx+20,(Y(Eh)+Y(El))/2+7,mix=lab,size=20,anchor='start',weight=700,fill=EQUI,halo=True)))
    return svg((w,H+80),w,label or '표준 환원 전위 눈금',s)
FIG['LAD']=ladder(TAB,2.87,-2.70,H=330,x=120,w=520,label='표 Ⅲ-10의 표준 환원 전위를 세로 눈금에 놓으면 위쪽일수록 환원되기 쉽고 아래쪽일수록 산화되기 쉽다')
FIG['LADDAN']=ladder([(0.34,r'\ce{Cu^2+}/\ce{Cu}'),(0.0,r'\ce{H+}/\ce{H2}'),(-0.76,r'\ce{Zn^2+}/\ce{Zn}')],0.6,-1.0,H=260,x=120,w=460,arrows=False,
    diff=(0.34,-0.76,'$1.10$ V'),label='구리와 아연의 표준 환원 전위 차 1.10 V가 다니엘 전지의 표준 전지 전위이다')
FIG['LADEX']=ladder([(0.771,r'\ce{Fe^3+}/\ce{Fe^2+}'),(0.536,r'\ce{I3-}/\ce{I-}'),(0.0,r'\ce{H+}/\ce{H2}')],0.9,-0.1,H=250,x=120,w=460,arrows=False,
    diff=(0.771,0.536,'$0.235$ V'),label='철 이온과 삼아이오딘화 이온의 표준 환원 전위 차 0.235 V')

# 16 ΔG와 E 부호
def dge():
    s=[]
    rows=[('$\\Delta G&lt;0$','$E_\\text{전지}&gt;0$','자발적',FIELD),('$\\Delta G=0$','$E_\\text{전지}=0$','평형',MUTED),('$\\Delta G&gt;0$','$E_\\text{전지}&lt;0$','비자발적',PLUS)]
    s.append(T(110,26,mix='Ⅲ-2 깁스 자유 에너지',size=19,weight=700)+T(400,26,mix='Ⅲ-4 전지 전위',size=19,weight=700))
    for i,(a,b,c,col) in enumerate(rows):
        y=50+i*78
        s.append(R(20,y,180,56,col,2,'#FFFFFF',10)+T(110,y+36,mix=a,size=22))
        s.append(R(310,y,180,56,col,2,'#FFFFFF',10)+T(400,y+36,mix=b,size=22))
        s.append(an('draw',P([(204,y+28),(306,y+28)],col,2.5,dash='6 4'),**{'dur':'.6','delay':f(.25*i)}))
        s.append(T(255,y+20,mix=c,size=18,fill=col,weight=700,halo=True))
    return svg((510,290),500,'깁스 자유 에너지 변화가 음수이면 전지 전위는 양수로 자발적이고, 0이면 평형, 양수이면 전지 전위가 음수로 비자발적이다',s)
FIG['DGE']=dge()

# 17 전하량 = nF
def nf():
    s=[]
    s.append(R(20,40,150,190,MINUS,2,'#EAF2FC',10)+T(95,30,mix='(−)극',size=19,weight=700))
    s.append(R(370,40,150,190,PLUS,2,'#FDECEE',10)+T(445,30,mix='(+)극',size=19,weight=700))
    for i in range(3):
        s.append(an('move',elec(300+i*26,110+(i%2)*24),**{'from':'-170,0','dur':'1.8','rep':'loop','delay':f(.3*i),'ease':'lin'}))
    s.append(L(170,135,370,135,INK,3))
    s.append(T(270,190,mix='전자 $n$ mol 이동',size=19,fill=MINUS,weight=700,halo=True))
    s.append(R(60,250,420,80,INK,2,'#FFFFFF',10)+T(270,282,mix='전하량 $=nF$ &nbsp;(1 mol 전자의 전하량 $F$)',size=19)+T(270,314,mix='일 $=$ 전위차 $\\times$ 전하량 $=E_\\text{전지}\\times nF$',size=19))
    return svg((540,340),520,'전자 n몰이 전위차 E를 지나며 옮긴 전하량은 nF이고, 전기가 한 일은 E와 nF의 곱이다',s)
FIG['NF']=nf()

# 19 ΔG°–K–E° 삼각형
def tri():
    s=[]
    P1,P2,P3=(300,50),(90,300),(510,300)
    s.append(P([P1,P2,P3],MUTED,2,close=True,fill='#FAFBFC'))
    for (x,y),t in ((P1,r'\Delta G^\circ'),(P2,r'K'),(P3,r'E^\circ_\text{전지}')):
        s.append(C(x,y,38,INK,2.5,'#FFFFFF')+T(x,y+8,tex=t,size=24))
    s.append(T(182,168,mix='$\\Delta G^\\circ=-RT\\ln K$',size=21,anchor='end',halo=True))
    s.append(T(418,168,mix='$\\Delta G^\\circ=-nFE^\\circ_\\text{전지}$',size=21,anchor='start',halo=True))
    s.append(T(300,346,mix='$E^\\circ_\\text{전지}=\\dfrac{RT}{nF}\\ln K$',size=21,halo=True))
    s.append(step('t1',T(300,220,mix='$E^\\circ_\\text{전지}&gt;0$||⇔ $\\Delta G^\\circ&lt;0$ ⇔ $K&gt;1$',size=19,weight=700,fill=FIELD)))
    return svg((600,380),520,'표준 자유 에너지 변화, 평형 상수, 표준 전지 전위는 세 식으로 서로 이어진다',s)
FIG['TRI']=tri()

# 22 E–log Q 그래프 (심화)
def nern():
    s=[]; x0,y0,W,H=80,300,400,250
    # 다니엘 전지 n=2: E = 1.10 - 0.0296 logQ, logQ -10..40 ; E 0..1.4
    def X(lq): return x0+(lq+10)/50*W
    def Y(E): return y0-E/1.4*H
    s.append(L(x0,y0,x0+W+10,y0,MUTED,2)+L(x0,y0+5,x0,y0-H-10,MUTED,2))
    for lq in (-10,0,10,20,30,40): s.append(L(X(lq),y0,X(lq),y0+6,MUTED,2)+T(X(lq),y0+28,mix=str(lq),size=18))
    for E in (0,0.5,1.0): s.append(L(x0-6,Y(E),x0,Y(E),MUTED,2)+T(x0-10,Y(E)+6,mix=f'{E:.1f}',size=18,anchor='end'))
    s.append(T(x0+W,y0+56,mix='$\\log Q$',size=19,anchor='end')+T(x0+8,y0-H-14,mix='$E_\\text{전지}$ [V]',size=19,anchor='start'))
    lqK=1.10/0.0296
    s.append(an('draw',L(X(-10),Y(1.10+0.296),X(lqK),Y(0),INK,3.5),**{'dur':'1.4'}))
    s.append(L(X(0),Y(1.10),X(0),y0,MUTED,1.5,'5 4')+C(X(0),Y(1.10),6,PLUS,0,PLUS)+T(X(0)+10,Y(1.10)-8,mix='$Q=1$: $E=E^\\circ=1.10$ V',size=18,anchor='start',halo=True))
    s.append(C(X(lqK),Y(0),7,FIELD,0,FIELD)+T(X(lqK)-6,Y(0)-14,mix='$Q=K$: $E=0$',size=18,anchor='end',fill=FIELD,weight=700,halo=True))
    s.append(step('g1',A(X(6),Y(0.80),X(24),Y(0.30),'ox',3)+T(X(16),Y(0.70)-4,mix='방전 →||$Q$ 증가',size=18,fill=OX,anchor='start',halo=True)))
    return svg((520,380),520,'다니엘 전지의 전지 전위는 log Q가 커질수록 직선으로 작아지고, Q가 K가 되면 0이 된다',s)
FIG['NERN']=nern()

# 24 농도와 전지 전위 (a 실험실 결과 다시 보기)
CONC=[(1.0,1.10,1.10),(0.10,1.07,1.07),(0.010,1.04,1.04),(0.0010,1.01,1.01)]   # (농도, 이론, 실험실 측정값)
def conc():
    s=[]; x0,y0,W,H=80,270,340,210
    def X(lc): return x0+(lc+3.4)/3.8*W
    def Y(E): return y0-(E-0.95)/0.2*H
    s.append(L(x0,y0,x0+W+10,y0,MUTED,2)+L(x0,y0,x0,y0-H-10,MUTED,2))
    for lc in (-3,-2,-1,0): s.append(L(X(lc),y0,X(lc),y0+6,MUTED,2)+T(X(lc),y0+28,mix=str(lc),size=18))
    for E in (1.00,1.05,1.10): s.append(L(x0-6,Y(E),x0,Y(E),MUTED,2)+T(x0-10,Y(E)+6,mix=f'{E:.2f}',size=18,anchor='end'))
    s.append(T(x0+W,y0+56,mix='$\\log[\\ce{Cu^2+}]$',size=19,anchor='end')+T(x0+8,y0-H-14,mix='$E_\\text{전지}$ [V]',size=19,anchor='start'))
    s.append(L(X(-3.2),Y(1.10-0.0296*3.2),X(0.2),Y(1.10+0.0296*0.2),INK,2.5))
    for i,(c,Eth,Em) in enumerate(CONC):
        lc=math.log10(c); s.append(an('pop',C(X(lc),Y(Em),7,FIELD,0,FIELD),**{'dur':'.4','delay':f(.15*i),'o':f'{f(X(lc))},{f(Y(Em))}'}))
    s.append(T(X(-1.6),Y(1.085),mix='기울기 $\\approx\\dfrac{0.0592}{2}=0.0296$',size=18,halo=True))
    return svg((460,340),440,'구리 이온 농도를 10배씩 줄이면 다니엘 전지의 전위가 약 0.03 V씩 작아진다',s)
FIG['CONC']=conc()

# 25 농도차 전지
FIG['CCELL']=cellsvg('같은 구리 전극을 묽은 용액과 진한 용액에 담근 농도차 전지: 묽은 쪽 구리가 산화되고 진한 쪽 구리 이온이 환원된다',width=500,
    Lm='Cu',Ltex=r'\ce{Cu}',Lsol=r'0.010\ \text{M}\ \ce{Cu^2+}',Rsol=r'1.0\ \text{M}\ \ce{Cu^2+}',Lk='cu3',Rk='cu',ions=(r'\ce{NO3-}',r'\ce{K+}'),reading='0.059 V')

# ═════ 출력 ═════
def build(tplname,out,meta):
    tpl=open(os.path.join(HERE,tplname),encoding='utf-8').read()
    def rep(m):
        k=m.group(1)
        if k not in FIG: sys.exit('no fig '+k)
        return FIG[k]
    o=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
    open(out+'slides.html','w',encoding='utf-8').write(o)
    shutil.copy(os.path.join(HERE,'extra_src.css'),out+'extra.css')
    open(out+'meta.json','w',encoding='utf-8').write(meta+'\n')
    print('ok',out[-40:],len(o),'sections',o.count('<section'),'anim',o.count('data-anim'))
build('tpl_a.html',OUT_A,'{"title": "화학 전지의 개요와 전지 전위 (1) 화학 전지의 개요", "file": "3-4-1_화학_전지의_개요와_전지_전위a", "header": "Ⅲ-4-1 화학 전지의 개요와 전지 전위 (고등 고급 화학 164–175쪽)"}')
shutil.copy(os.path.join(HERE,'labs_src.js'),OUT_A+'labs.js')
build('tpl_b.html',OUT_B,'{"title": "화학 전지의 개요와 전지 전위 (2) 전지 전위", "file": "3-4-1_화학_전지의_개요와_전지_전위b", "header": "Ⅲ-4-1 화학 전지의 개요와 전지 전위 (고등 고급 화학 164–175쪽)"}')
