# -*- coding: utf-8 -*-
"""고급화학 3-3-1 산화수 개념과 산화제와 환원제 — 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   extra_src.css를 extra.css로 복사하고 meta.json을 쓴다(실험실 없음 → labs.js 없음).
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음). 반응식·산화수 검산은 calc.py."""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FOLDER='3-3-1_산화수_개념과_산화제와_환원제'
OUT=BASE+FOLDER+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-3-1_산화수_개념과_산화제와_환원제/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FOLDER), OUT
FIG={}
ZN_R=30   # 금속 원자 Zn 반지름(덱 약속)
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def step(g,body): return f'<g class="step" data-g="{g}">{body}</g>'
def atom(x,y,r,el,lab=None): return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def elec(x,y,lab=True,r=9):
    return C(x,y,r,MINUS,1.5,'#DCE9FA')+(T(x,y+6,tex='e^-',size=18,fill=MINUS) if lab else '')
def dot(x,y): return f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="{INK}"/>'
def sym(x,y,s,S=40,fill=None): return T(x,y+0.36*S,tex=f'\\mathrm{{{s}}}',size=S,fill=fill)
def pair(x,y,side,S=40):
    dx,dy=0.70*S,0.75*S; h=0.18*S
    if side=='t': return dot(x-h,y-dy)+dot(x+h,y-dy)
    if side=='b': return dot(x-h,y+dy)+dot(x+h,y+dy)
    if side=='l': return dot(x-dx,y-h)+dot(x-dx,y+h)
    if side=='r': return dot(x+dx,y-h)+dot(x+dx,y+h)
def bondpair(x1,y1,x2,y2,off=0):
    """두 원자 사이 공유 전자쌍(결합 방향에 수직으로 두 점)"""
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); px,py=-dy/Ln,dx/Ln
    mx+=px*off; my+=py*off; ux,uy=dx/Ln*7,dy/Ln*7
    return dot(mx-ux,my-uy)+dot(mx+ux,my+uy)
def oxl(x,y,v,col=INK,size=20): return T(x,y,tex=v,size=size,fill=col,weight=700)
def box(x,y,w,h,col,fill,txt=None,size=20,rx=10,dash=None):
    return R(x,y,w,h,col,2,fill,rx,dash)+(T(x+w/2,y+h/2+7,mix=txt,size=size) if txt else '')

# ═════ 1 표지: 아연과 산의 반응 — 전자 이동과 산화수 ═════
def cover():
    """표지: 가장자리가 둥글게 흐려지므로(엔진 cover-fig 마스크) 모두 중심 (240,240) 반지름 185 안에 둔다"""
    s=[]
    s.append(atom(125,225,ZN_R,'Zn'))
    s.append(T(125,286,mix='$\\ce{Zn}$ 원자 (0)',size=19))
    s.append(atom(350,215,24,'O')+atom(320,187,18,'H','-')+atom(380,187,18,'H','-')+atom(350,253,18,'H','-'))
    s.append(T(350,300,mix='$\\ce{H3O+}$의 H (+1)',size=19))
    s.append(A(160,222,318,214,'minus',3))
    for i,ex in enumerate((205,262)):
        s.append(an('move',elec(ex,203),**{'from':'-50,3','dur':'1.4','delay':f(i*.5),'rep':'loop','ease':'io'}))
    s.append(T(238,170,mix='전자 $2$개 이동',size=20,fill=MINUS,halo=True))
    s.append(R(125,318,230,80,MUTED,1.5,'#FFFFFF',12))
    s.append(T(240,350,mix='$\\ce{Zn}$ $0\\rightarrow+2$ 산화',size=20,fill=OX,weight=700))
    s.append(T(240,384,mix='$\\ce{H}$ $+1\\rightarrow0$ 환원',size=20,fill=RD,weight=700))
    return svg((480,480),500,'아연 원자가 전자 두 개를 하이드로늄 이온의 수소에 주어 아연의 산화수는 0에서 +2로 늘고 수소의 산화수는 +1에서 0으로 준다',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 2 중단원 도입: 녹·광합성·배터리 ═════
def intro():
    s=[]
    # 녹슨 철판
    s.append(R(20,60,130,90,'#6B7480',2,'#B7C0C9',8))
    rnd=random.Random(3)
    for i in range(9):
        x=rnd.uniform(35,135); y=rnd.uniform(72,138); r=rnd.uniform(6,13)
        s.append(an('fade',C(x,y,r,'#8A3B12',1,'#B8561F',extra='opacity=".85"'),delay=f(i*.15),dur='.5'))
    s.append(T(85,184,mix='철의 녹',size=20,weight=700))
    s.append(T(85,212,mix='$\\ce{Fe2O3}$ 생성',size=18))
    # 잎과 산소 기포
    s.append(P([(205,150),(225,80),(290,60),(300,120),(255,155)],'#2E7D4F',2.5,fill='#7CC48F',close=True)+L(210,148,288,72,'#2E7D4F',2))
    for i,(bx,by) in enumerate(((300,52),(318,72),(310,34))):
        s.append(an('move',C(bx,by,6,'#9FC3DD',1.5,'#FFFFFF'),**{'from':'0,30','rep':'loop','dur':f(1.4+i*.3),'ease':'lin'}))
    s.append(T(255,184,mix='광합성',size=20,weight=700))
    s.append(T(255,212,mix='$\\ce{O2}$ 발생',size=18))
    # 배터리
    s.append(R(370,72,110,64,INK,3,'#FFFFFF',8)+R(480,92,10,24,INK,2,INK,2))
    for i in range(4): s.append(an('fade',R(378+i*25,80,20,48,FIELD,0,FIELD,3),delay=f(.3+i*.3),dur='.4'))
    s.append(T(425,184,mix='배터리',size=20,weight=700))
    s.append(T(425,212,mix='충전·방전',size=18))
    s.append(R(30,240,440,64,OX,2,'#FFF3EC',12))
    s.append(T(250,280,mix='공통점: 전자를 주고받는 산화 환원 반응',weight=700,size=20,halo=False))
    return svg((500,320),480,'철의 녹, 광합성의 산소 발생, 배터리 충전은 모두 산화 환원 반응이다',s)
FIG['INTRO']=intro()

# ═════ 4 생각 열기: 산화의 정의가 넓어진 과정 ═════
def history():
    s=[]
    rows=[('산소','산소를 얻으면 산화','$\\ce{2Mg + O2 -> 2MgO}$'),('전자','전자를 잃으면 산화','$\\ce{2Na + Cl2 -> 2NaCl}$'),('산화수','산화수가 늘면 산화','공유 결합 물질에도')]
    for i,(k,d,e) in enumerate(rows):
        y=20+i*104
        body=R(20,y,120,76,OX,2.5,'#FFF3EC',12)+T(80,y+46,mix=k,size=22,weight=700,fill=OX)+T(160,y+32,mix=d,size=20,anchor='start')+T(160,y+64,mix=e,size=19,anchor='start',fill=MUTED)
        s.append(an('fade',body,delay=f(i*.5),dur='.6'))
        if i<2: s.append(an('draw',A(80,y+80,80,y+102,'ink',2.5),delay=f(i*.5+.4),dur='.3'))
    return svg((460,330),440,'산화의 정의는 산소를 얻는 것에서 전자를 잃는 것, 산화수가 증가하는 것으로 넓어졌다',s)
FIG['HIST']=history()

# ═════ 5 ① 전자의 이동: 나트륨과 염소 ═════
def transfer():
    s=[]
    y=110
    s.append(atom(80,y,32,'Na')+atom(300,y,29,'Cl'))
    s.append(an('move',elec(190,y-4),**{'from':'-80,0','dur':'1.6','rep':'loop','ease':'io'}))
    s.append(A(118,y+26,260,y+26,'minus',3))
    s.append(T(80,y+62,mix='$\\ce{Na}$ 원자',size=19)+T(300,y+62,mix='$\\ce{Cl}$ 원자',size=19))
    s.append(T(190,40,mix='전자 이동',size=20,fill=MINUS,weight=700))
    s.append(A(190,200,190,236,'ink',3))
    y2=290
    s.append(an('pop',atom(110,y2,19,'Na','-')+T(110,y2-30,tex='\\ce{Na+}',size=21),o='110,290',delay='.2'))
    s.append(an('pop',atom(270,y2,32,'Cl','\\mathrm{Cl}^{-}'),o='270,290',delay='.4'))
    s.append(T(190,y2+6,mix='인력',size=19,fill=MUTED))
    s.append(T(110,y2+52,mix='전자 잃음',size=19,fill=OX,weight=700)+T(270,y2+56,mix='전자 얻음',size=19,fill=RD,weight=700))
    s.append(T(400,150,mix='잃은 전자 수||$=$||얻은 전자 수',size=20,anchor='middle',fill=INK))
    return svg((480,370),440,'나트륨 원자가 전자를 잃어 나트륨 이온이 되고 염소 원자가 그 전자를 얻어 염화 이온이 되어 이온 결합을 형성한다',s)
FIG['TR']=transfer()

# ═════ 6 ② 산화수의 정의: 물 분자 ═════
def water(x0,mode):
    """mode 'real' 공유, 'ox' 공유 전자쌍을 O가 모두 차지(루이스 구조 H:O:H 꼴)"""
    s=[]; S=34; O=(x0+110,130); H1=(x0+34,130); H2=(x0+186,130)
    s.append(sym(*O,'O',S)+sym(*H1,'H',S)+sym(*H2,'H',S))
    s.append(pair(O[0],O[1],'t',S)+pair(O[0],O[1],'b',S))
    if mode=='real':
        s.append(bondpair(*O,*H1)+bondpair(*O,*H2))
    else:
        s.append(dot(O[0]-35,O[1])+dot(O[0]-23,O[1])+dot(O[0]+23,O[1])+dot(O[0]+35,O[1]))
        s.append(an('pop',f'<ellipse cx="{f(O[0])}" cy="{f(O[1])}" rx="50" ry="40" fill="{RD}" fill-opacity=".10" stroke="{RD}" stroke-width="2" stroke-dasharray="6 4"/>',o=f'{f(O[0])},{f(O[1])}'))
        s.append(oxl(O[0],O[1]-50,'-2',RD,22)+oxl(H1[0],H1[1]-34,'+1',OX,22)+oxl(H2[0],H2[1]-34,'+1',OX,22))
    return ''.join(s)
def oxdef():
    s=[]
    s.append(water(0,'real')+water(250,'ox'))
    s.append(A(222,130,262,130,'ink',3))
    s.append(T(110,222,mix='실제 루이스 구조||공유 전자쌍을 함께 가짐',size=18)+T(360,222,mix='산화수의 가정||O가 공유 전자를 모두 차지',size=18))
    s.append(T(240,300,mix='O: 원자가 전자 6, 가진 전자 8 → $-2$ &nbsp; H: 1, 0 → $+1$',size=18,fill=MUTED))
    return svg((480,316),470,'물 분자에서 전기음성도가 큰 산소가 공유 전자쌍을 모두 차지한다고 가정하면 산소의 산화수는 −2, 수소는 +1이다',s)
FIG['OXDEF']=oxdef()

# ═════ 7 ③ 형식 전하와 산화수: 일산화 탄소 ═════
def co(y,mode):
    s=[]; S=36; Cx,Ox=110,250
    s.append(sym(Cx,y,'C',S)+sym(Ox,y,'O',S))
    s.append(dot(Cx-0.70*S,y-0.18*S)+dot(Cx-0.70*S,y+0.18*S)+dot(Ox+0.70*S,y-0.18*S)+dot(Ox+0.70*S,y+0.18*S))
    mx=(Cx+Ox)/2
    for dy in (-14,0,14): s.append(dot(mx-7,y+dy)+dot(mx+7,y+dy))
    if mode=='fc':
        s.append(L(mx,y-36,mx,y+36,EQUI,2.5,'6 4'))
        s.append(oxl(Cx,y-34,'-1',MINUS,22)+oxl(Ox,y-34,'+1',PLUS,22))
        s.append(T(380,y-6,mix='결합 전자를||반씩 나눔',size=19,anchor='middle'))
    else:
        s.append(an('pop',R(mx-20,y-34,Ox+0.70*S+14-(mx-20),68,RD,2,RD,14,'6 4',extra='fill-opacity=".10"'),o=f'{f(Ox)},{f(y)}'))
        s.append(oxl(Cx,y-34,'+2',OX,22)+oxl(Ox,y-44,'-2',RD,22))
        s.append(T(380,y-6,mix='결합 전자를||O가 모두 가짐',size=19,anchor='middle'))
    return ''.join(s)
def fcfig():
    s=[T(20,34,mix='형식 전하',size=20,anchor='start',weight=700)]
    s.append(co(100,'fc'))
    s.append(L(20,160,460,160,'#E2E7EC',2))
    s.append(T(20,200,mix='산화수',size=20,anchor='start',weight=700))
    s.append(co(268,'ox'))
    return svg((470,320),470,'일산화 탄소에서 형식 전하는 탄소 −1, 산소 +1이지만 산화수는 탄소 +2, 산소 −2이다',s)
FIG['FC']=fcfig()

# ═════ 8 확인 01: 암모늄 이온 ═════
def nh4():
    s=[]; S=38; N=(200,170)
    Hs=[(200,72),(200,268),(102,170),(298,170)]
    s.append(sym(*N,'N',S))
    for hx,hy in Hs: s.append(sym(hx,hy,'H',S)+bondpair(*N,hx,hy))
    s.append(P([(78,62),(66,62),(66,282),(78,282)],INK,3)+P([(322,62),(334,62),(334,282),(322,282)],INK,3))
    s.append(T(352,72,tex='+',size=30))
    return svg((400,320),330,'암모늄 이온의 루이스 구조: 질소 둘레에 수소 네 개가 공유 전자쌍으로 결합하고 전체 전하는 +1이다',s)
FIG['NH4']=nh4()

# ═════ 9 ④ 산화수 수직선 ═════
def ladder():
    s=[]; x=120; y0=320; dy=60
    s.append(L(x,y0+20,x,y0-4*dy-24,MUTED,2.5))
    for i,v in enumerate((-2,-1,0,1,2)):
        y=y0-i*dy; s.append(L(x-8,y,x+8,y,MUTED,2)+T(x-18,y+7,tex=('+' if v>0 else '')+str(v),size=20,anchor='end'))
    s.append(T(x,y0-4*dy-36,mix='산화수',size=19,fill=MUTED))
    s.append(an('draw',A(x+34,y0-2*dy,x+34,y0-3*dy,'ox',4),dur='.6'))
    s.append(T(x+92,y0-2.5*dy+7,mix='$\\ce{H}$ $0\\rightarrow+1$ 산화',size=19,anchor='start',fill=OX,weight=700))
    s.append(an('draw',A(x+70,y0-4*dy,x+70,y0-2*dy,'rd',4),dur='.8',delay='.6'))
    s.append(T(x+92,y0-3.6*dy+7,mix='$\\ce{Cu}$ $+2\\rightarrow0$ 환원',size=19,anchor='start',fill=RD,weight=700))
    s.append(T(x+40,y0-0.2*dy,mix='증가 = 전자 잃음||감소 = 전자 얻음',size=19,anchor='start',fill=MUTED))
    return svg((420,366),380,'산화수 수직선에서 수소는 0에서 +1로 올라가 산화되고 구리는 +2에서 0으로 내려가 환원된다',s)
FIG['LAD']=ladder()

# ═════ 14 연결: 전하 저울 ═════
def scale(cx,y,tilt,lab_l,lab_r,cap,col):
    s=[]; w=150; a=math.radians(tilt); dx,dy=w*math.cos(a),w*math.sin(a)
    s.append(P([(cx-16,y+70),(cx,y+6),(cx+16,y+70)],MUTED,2.5,fill='#E8EDF2',close=True))
    s.append(L(cx-dx,y+dy,cx+dx,y-dy,INK,4))
    for sg,lab in ((-1,lab_l),(1,lab_r)):
        px,py=cx+sg*dx,y-sg*dy
        s.append(L(px,py,px,py+26,MUTED,1.5)+R(px-46,py+26,92,34,col,2,'#FFFFFF',8)+T(px,py+50,mix=lab,size=19))
    s.append(T(cx,y+100,mix=cap,size=19,weight=700,fill=col))
    return ''.join(s)
def balance():
    s=[]
    s.append(T(240,30,tex='\\ce{Cu(s) + Ag+(aq) -> Cu^2+(aq) + Ag(s)}',size=20))
    s.append(scale(240,80,-9,'전하 $+1$','전하 $+2$','계수 전: 전하가 맞지 않음',PLUS))
    s.append(step('b2',T(240,240,tex='\\ce{Cu(s) + 2Ag+(aq) -> Cu^2+(aq) + 2Ag(s)}',size=20)))
    s.append(step('b2',an('rot',scale(240,282,0,'전하 $+2$','전하 $+2$','계수 후: 원자 수·전하 모두 맞음',FIELD),**{'o':'240,282','from':'-9','dur':'.9','on':'step'})))
    return svg((480,420),460,'구리와 은 이온의 반응은 원자 수가 맞아도 전하가 +1과 +2로 다르므로, 은 이온과 은의 계수를 2로 맞추어야 전하 균형도 이룬다',s)
FIG['BAL']=balance()

# ═════ 15 ⑧ 반쪽 반응법: 두 반쪽 카드 ═════
def half():
    s=[]
    s.append(R(20,20,440,96,OX,2.5,'#FFF3EC',12)+T(40,52,mix='산화 반쪽 반응',size=19,anchor='start',fill=OX,weight=700))
    s.append(T(240,94,tex='\\ce{Zn(s) -> Zn^2+(aq) + 2e-}',size=21))
    s.append(R(20,214,440,120,RD,2.5,'#ECF6F8',12)+T(40,246,mix='환원 반쪽 반응 (× 2)',size=19,anchor='start',fill=RD,weight=700))
    s.append(T(240,284,tex='\\ce{H3O+(aq) + e- -> 1/2 H2(g) + H2O(l)}',size=20))
    s.append(step('h2',T(240,320,tex='\\ce{2H3O+(aq) + 2e- -> H2(g) + 2H2O(l)}',size=20)))
    for i,dx in enumerate((-40,40)):
        s.append(an('move',elec(240+dx,166),**{'from':'0,-58','dur':'1.3','delay':f(i*.25),'rep':'loop','ease':'io'}))
    s.append(A(240,118,240,208,'minus',3))
    s.append(T(300,172,mix='전자 $2$개 이동',size=19,anchor='start',fill=MINUS))
    return svg((480,350),460,'산화 반쪽 반응에서 아연이 내놓은 전자 두 개를 환원 반쪽 반응의 하이드로늄 이온 두 개가 받는다',s)
FIG['HALF']=half()

# ═════ 16 ⑨ 산화수법: 산화수 변화 괄호 ═════
def oxmethod():
    s=[]; y=150
    xs={'Mn':70,'Fe':205,'Mn2':330,'Fe3':445}
    s.append(T(70,y,tex='\\ce{MnO4-}',size=26)+T(140,y,tex='+',size=26)+T(205,y,tex='\\ce{Fe^2+}',size=26)
             +T(268,y,tex='\\ce{->}',size=26)+T(330,y,tex='\\ce{Mn^2+}',size=26)+T(388,y,tex='+',size=26)+T(445,y,tex='\\ce{Fe^3+}',size=26))
    s.append(oxl(58,y-38,'+7',INK,20)+oxl(197,y+44,'+2',INK,20)+oxl(320,y-38,'+2',INK,20)+oxl(437,y+44,'+3',INK,20))
    # 위 괄호: Mn
    s.append(an('draw',P([(58,y-60),(58,y-84),(320,y-84),(320,y-60)],RD,3),dur='.7'))
    s.append(T(189,y-94,mix='$\\ce{Mn}$ : $-5$ (전자 5개 얻음, 환원)',size=19,fill=RD,weight=700,halo=True))
    s.append(an('draw',P([(197,y+66),(197,y+90),(437,y+90),(437,y+66)],OX,3),dur='.7',delay='.6'))
    s.append(T(317,y+122,mix='$\\ce{Fe}$ : $+1$ (전자 1개 잃음, 산화)',size=19,fill=OX,weight=700,halo=True))
    s.append(step('m3',T(250,y+172,mix='$-5\\times1$ 과 $+1\\times5$ → $\\ce{Fe}$의 계수 $5$',size=20,weight=700)))
    return svg((500,340),490,'과망가니즈산 이온의 망가니즈 산화수는 +7에서 +2로 5만큼 줄고 철은 +2에서 +3으로 1만큼 늘므로 철의 계수를 5로 맞춘다',s)
FIG['OXM']=oxmethod()

# ═════ 17 ⑩ 산화제와 환원제 ═════
def agents():
    s=[]
    s.append(R(20,60,170,120,OX,3,'#FFF3EC',14)+T(105,104,mix='환원제',size=24,weight=700,fill=OX)+T(105,138,mix='전자를 잃음||(산화됨)',size=19))
    s.append(R(290,60,170,120,RD,3,'#ECF6F8',14)+T(375,104,mix='산화제',size=24,weight=700,fill=RD)+T(375,138,mix='전자를 얻음||(환원됨)',size=19))
    s.append(A(196,110,284,110,'minus',4))
    for i in range(2): s.append(an('move',elec(240,88,False,8),**{'from':'-36,0','dur':'1.2','delay':f(i*.6),'rep':'loop','ease':'lin'}))
    s.append(T(240,148,tex='e^-',size=20,fill=MINUS))
    s.append(T(105,226,mix='상대를 환원시킴',size=20,fill=OX,weight=700)+T(375,226,mix='상대를 산화시킴',size=20,fill=RD,weight=700))
    s.append(T(105,262,mix='산화수 증가',size=19,fill=MUTED)+T(375,262,mix='산화수 감소',size=19,fill=MUTED))
    return svg((480,282),460,'환원제는 전자를 잃어 산화되면서 상대를 환원시키고, 산화제는 전자를 얻어 환원되면서 상대를 산화시킨다',s)
FIG['AG']=agents()

# ═════ 18 ⑪ 아연과 산: 비커 ═════
def znacid():
    s=[]; x,y,w,h=110,70,240,220
    s.append(R(x+2,y+60,w-4,h-62,'none',0,'#E9F3FB')+L(x+2,y+60,x+w-2,y+60,WATER_S,1.5))
    s.append(R(x+92,y-10,56,190,'#6B7480',2.5,'#AEB7C1',4))
    s.append(P([(x,y),(x,y+h),(x+w,y+h),(x+w,y)],GLASS,3))
    rnd=random.Random(7)
    for i in range(9):
        bx=x+92+rnd.choice((-12,68))+rnd.uniform(-6,6); by=y+100+rnd.uniform(0,70)
        s.append(an('move',C(bx,by,4+rnd.uniform(0,3),'#9FC3DD',1.5,'#FFFFFF'),**{'from':f'0,{f(40+rnd.uniform(0,20))}','rep':'loop','dur':f(1.1+rnd.random()*.8),'ease':'lin'}))
    s.append(T(x+120,y-22,mix='아연판',size=21)+T(x+w+12,y+130,mix='$\\ce{H2}$ 기포',size=21,anchor='start'))
    s.append(T(x+w/2,y+h+34,mix='묽은 산 ($\\ce{H3O+}$)',size=21))
    return svg((460,330),400,'묽은 산에 넣은 아연판 표면에서 수소 기체 기포가 생긴다',s)
FIG['ZN']=znacid()

# ═════ 19 ⑫ 세기: 산화수 사다리 (Mn, O) ═════
def strength():
    s=[]
    def lad(x,el,items,vmin,vmax,top,bot):
        o=[]; y0=330; k=280/(vmax-vmin); Y=lambda v:y0-(v-vmin)*k
        o.append(L(x,Y(vmin)+8,x,Y(vmax)-8,MUTED,2.5))
        for v,lab in items:
            o.append(C(x,Y(v),6,INK,2,'#FFFFFF')+T(x-14,Y(v)+7,tex=('+' if v>0 else '')+str(v),size=19,anchor='end')+T(x+16,Y(v)+7,mix=lab,size=20,anchor='start'))
        o.append(T(x,24,mix=f'$\\ce{{{el}}}$의 산화수',size=19,fill=MUTED))
        return ''.join(o)
    s.append(lad(60,'Mn',[(7,'$\\ce{MnO4-}$'),(4,'$\\ce{MnO2}$'),(2,'$\\ce{Mn^2+}$'),(0,'$\\ce{Mn}$')],0,7,'',''))
    s.append(lad(300,'O',[(0,'$\\ce{O2}$'),(-1,'$\\ce{H2O2}$'),(-2,'$\\ce{H2O}$')],-2,0,'',''))
    s.append(an('draw',L(200,70,200,320,MUTED,3,'8 6'),dur='.8'))
    s.append(T(212,110,mix='강한||산화제',size=19,anchor='start',fill=RD,weight=700))
    s.append(T(212,280,mix='강한||환원제',size=19,anchor='start',fill=OX,weight=700))
    s.append(an('pop',R(386,165,92,34,BF,2,'#F3EEFB',8)+T(432,188,mix='둘 다',size=19,fill=BF,weight=700),o='432,182',delay='.6'))
    return svg((490,350),470,'같은 원소를 포함하는 화학종 가운데 산화수가 큰 과망가니즈산 이온이 강한 산화제이고, 중간 산화수의 과산화 수소는 산화제도 환원제도 될 수 있다',s)
FIG['STR']=strength()

# ═════ 21 예제 Ⅲ-9 (2): 전자 수 맞추기 막대 ═════
def ebar():
    s=[]; x0=30; u=40
    s.append(T(20,36,mix='환원 반쪽 $\\times2$ : 얻은 전자',size=19,anchor='start',fill=RD))
    for i in range(2): s.append(an('fade',R(x0+i*5*u,48,5*u-4,40,RD,2,'#ECF6F8',6)+T(x0+i*5*u+2.5*u,75,tex='5e^-',size=19),delay=f(i*.3),dur='.4'))
    s.append(T(20,132,mix='산화 반쪽 $\\times5$ : 잃은 전자',size=19,anchor='start',fill=OX))
    for i in range(5): s.append(an('fade',R(x0+i*2*u,144,2*u-4,40,OX,2,'#FFF3EC',6)+T(x0+i*2*u+u,171,tex='2e^-',size=19),delay=f(.6+i*.2),dur='.4'))
    s.append(T(230,226,mix='$2\\times5=5\\times2=10$ 개',size=21,weight=700))
    return svg((460,244),440,'환원 반쪽 반응 두 번이 얻는 전자 10개와 산화 반쪽 반응 다섯 번이 잃는 전자 10개가 같다',s)
FIG['EBAR']=ebar()

# ═════ 24 탐구 활동: 응용 분야 지도 ═════
def web():
    s=[]; cx,cy=240,180
    s.append(R(cx-92,cy-30,184,60,OX,3,'#FFF3EC',30)+T(cx,cy+8,mix='산화 환원 반응',size=21,weight=700,fill=OX))
    items=[('에너지',0),('금속 제련',60),('부식과 방지',120),('생명 현상',180),('분석·측정',240),('표백·소독',300)]
    for i,(lab,deg) in enumerate(items):
        a=math.radians(deg-90); x=cx+200*math.cos(a); y=cy+128*math.sin(a)
        s.append(L(cx+92*math.cos(a)*.95,cy+30*math.sin(a)*1.0,x-52*math.cos(a),y-18*math.sin(a),MUTED,1.5,'5 4'))
        s.append(an('pop',R(x-62,y-20,124,40,MUTED,2,'#FFFFFF',20)+T(x,y+7,mix=lab,size=19),o=f'{f(x)},{f(y)}',delay=f(.2+i*.2)))
    return svg((480,360),450,'산화 환원 반응의 응용 분야: 에너지, 금속 제련, 부식과 방지, 생명 현상, 분석과 측정, 표백과 소독',s)
FIG['WEB']=web()

# ═════ 29 연습 문제 3: 알칼리 전지 단면 ═════
def alk():
    s=[]; x,y,w,h=130,40,200,300
    s.append(R(x,y+16,w,h-16,'#6B7480',3,'#D9DEE4',14))
    s.append(R(x+70,y,60,18,'#6B7480',2.5,'#B7C0C9',4))
    s.append(R(x+14,y+30,w-28,h-44,'#3B3B3B',2,'#5A5A5A',8))       # MnO2 (검은 가루)
    s.append(R(x+40,y+48,w-80,h-82,'#9FA7B0',2,'#F1F3F5',6))       # 분리막
    rnd=random.Random(11)
    for i in range(40):
        s.append(C(x+52+rnd.uniform(0,w-104),y+62+rnd.uniform(0,h-110),3.2,'#7E8B98',1,'#C9D0D8'))
    s.append(L(x+w/2,y+70,x+w/2,y+h-40,'#8C6D3F',4))
    s.append(T(x+w+16,y+12,mix='(+)극',size=19,anchor='start',fill=INK,weight=700)+T(x+w+16,y+h+6,mix='(−)극',size=19,anchor='start',fill=INK,weight=700))
    s.append(L(x+w-14,y+90,x+w+14,y+90,MUTED,1.5)+T(x+w+18,y+97,mix='$\\ce{MnO2}$ (환원)',size=19,anchor='start',fill=RD))
    s.append(L(x+w/2+30,y+170,x+w+14,y+170,MUTED,1.5)+T(x+w+18,y+177,mix='$\\ce{Zn}$ 가루 (산화)',size=19,anchor='start',fill=OX))
    s.append(L(x+40,y+240,x-14,y+240,MUTED,1.5)+T(x-18,y+247,mix='분리막',size=19,anchor='end'))
    s.append(L(x+18,y+120,x-14,y+120,MUTED,1.5)+T(x-18,y+127,mix='전해질||$\\ce{KOH}$',size=19,anchor='end'))
    return svg((470,360),400,'알칼리 전지 단면: 가운데 아연 가루가 산화되고 바깥쪽 이산화 망가니즈가 환원된다',s)
FIG['ALK']=alk()

# ═════ 출력 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(out)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "산화수 개념과 산화제와 환원제", "file": "3-3-1_산화수_개념과_산화제와_환원제", "header": "Ⅲ-3-1 산화수 개념과 산화제와 환원제 (고등 고급 화학 158–163쪽)"}\n')
print('ok',len(out),'sections',out.count('<section'),'anim',out.count('data-anim'))
