# -*- coding: utf-8 -*-
"""고급화학 1-M 그림 생성: gen_head.py(1-4-2 사본, OUT=이 덱 — assert) + helpers.py → tpl.html의 {{KEY}}를 바꿔 slides.html (실험실 없음)"""
import math, re, sys, os
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/1-M_대단원_Ⅰ_마무리/slides.html'), OUT
HL='#FFE45C'; GR='#8C99A6'
CW={'C':.72,'H':.76,'B':.68,'r':.40,'l':.28,'O':.78,'N':.75,'S':.62,'=':.95,'#':.95,'(':.34,')':.34,'-':.5}
def gw(t,size): return sum((CW.get(ch,.36) if not ch.isdigit() else .38) for ch in t)*size
def wave(x1,y1,x2,y2,col,amp=6,lam=14,w=3):
    dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
    pts=[(x1+ux*t+px*amp*math.sin(2*math.pi*t/lam),y1+uy*t+py*amp*math.sin(2*math.pi*t/lam)) for t in [i*Ln/80 for i in range(81)]]
    return P(pts,col,w)
def step(body,g=None):
    return '<g class="step"'+(f' data-g="{g}"' if g else '')+'>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def atom(x,y,r,el,lab=None):
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def bond(x1,y1,x2,y2,n=1,w=6):
    if n==1: return L(x1,y1,x2,y2,BOND,w,extra='stroke-linecap="round"')
    dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); px,py=-dy/Ln*4.5,dx/Ln*4.5
    return ''.join(L(x1+s*px,y1+s*py,x2+s*px,y2+s*py,BOND,w-1.5,extra='stroke-linecap="round"') for s in (-1,1))
def swing(body,dx,dy,dur='.5',delay='0'):
    return an('move',body,**{'from':f'{f(dx)},{f(dy)}','rep':'swing','dur':dur,'delay':delay,'ease':'sine'})
def rotsw(body,deg,ox,oy,dur='.6'):
    return an('rot',body,**{'from':f'{deg}','o':f'{f(ox)},{f(oy)}','rep':'swing','dur':dur,'ease':'sine'})
def popg(body,x,y,d): return an('pop',body,o=f'{f(x)},{f(y)}',dur='.6',delay=f'{d:.1f}')
def harp(cx,y,h,up,col=INK,w=2.6):
    if up: return P([(cx,y+h-6),(cx,y+6),(cx-6,y+14)],col,w,extra='stroke-linecap="round"')
    return P([(cx,y+6),(cx,y+h-6),(cx+6,y+h-14)],col,w,extra='stroke-linecap="round"')
def dlev(x,y,occ,LW=34,gap=12,new=()):
    n=len(occ); W=n*LW+(n-1)*gap; x0=x-W/2; s=[]
    for i,o in enumerate(occ):
        a=x0+i*(LW+gap); s.append(L(a,y,a+LW,y,INK,2.6))
        cx=a+LW/2; xs=[cx] if len(o)==1 else [cx-6,cx+6]
        for j,ch in enumerate(o): s.append(harp(xs[j],y-17,34,ch=='u',FIELD if (i,j) in new else INK))
    return ''.join(s)
def dim(x,y1,y2,lab,col=EQUI,size=20,side='l'):
    s=L(x,y1,x,y2,col,2)+L(x-6,y1,x+6,y1,col,2)+L(x-6,y2,x+6,y2,col,2)
    if lab: s+=T(x+(10 if side=='r' else -10),(y1+y2)/2+7,tex=lab,size=size,anchor='start' if side=='r' else 'end',fill=col)
    return s
def lob(cx,cy,ang,L0,sign,W=0.6,lab=True,lsize=19,opa=.30):
    t=math.radians(ang); ux,uy=math.cos(t),-math.sin(t); px,py=-uy,ux; pts=[]
    for i in range(61):
        th=math.radians(-90+3*i); rho=L0*math.cos(th)**2
        pts.append((cx+ux*rho*math.cos(th)+px*W*L0*math.cos(th)**2*math.sin(th),cy+uy*rho*math.cos(th)+py*W*L0*math.cos(th)**2*math.sin(th)))
    col=BF if sign>0 else GRAV
    s=P(pts,col,1.8,fill=col,close=True,extra=f'fill-opacity="{opa}"')
    if lab: s+=T(cx+ux*L0*.58,cy+uy*L0*.58+lsize*.36,tex='+' if sign>0 else '-',size=lsize,weight=700)
    return s
def fcount(txt):
    c=Counter()
    def add(s,k):
        for m in re.finditer(r'\(([^()]*)\)(\d*)|([A-Z][a-z]?)(\d*)',s):
            if m.group(1) is not None: add(m.group(1),k*int(m.group(2) or 1))
            else: c[m.group(3)]+=k*int(m.group(4) or 1)
    add(txt,1); return c
def chk(txt,want,name):
    if +fcount(txt)!=+fcount(want): sys.exit(f'[{name}] {dict(fcount(txt))} != {want}')

# ── H2O·CO2 공-막대 (O 반지름 rO, H rH)
def h2o(cx,cy,r=48,rO=20,rH=15,bend=None):
    a=math.radians(52.25); hl=(cx-r*math.sin(a),cy+r*math.cos(a)); hr=(cx+r*math.sin(a),cy+r*math.cos(a))
    return hl,hr
def co2(cx,cy,d=58,rO=20,rC=20):
    return (cx-d,cy),(cx,cy),(cx+d,cy)

# ═══ S1 표지
def cover():
    s=[]
    o1,c,o2=co2(270,150,70,24,24)
    s.append(bond(*o1,*c,2,7)+bond(*c,*o2,2,7))
    s.append(swing(atom(*o1,24,'O'),6,0)+swing(atom(*c,24,'C'),-8,0)+swing(atom(*o2,24,'O'),6,0))
    s.append(T(270,215,tex='\\ce{CO2}',size=26,weight=700))
    O=(270,310); hl,hr=h2o(*O,62)
    s.append(rotsw(bond(*O,*hl)+atom(*hl,18,'H'),-9,*O)+rotsw(bond(*O,*hr)+atom(*hr,18,'H'),9,*O))
    s.append(atom(*O,24,'O'))
    s.append(T(270,415,tex='\\ce{H2O}',size=26,weight=700))
    s.append(an('draw',wave(40,290,150,170,INK,7,16,3),dur='1.2')+A(140,181,165,154,'ink',3))
    s.append(T(64,330,mix='적외선',size=21,anchor='start'))
    return svg('0 0 540 500',520,'선형 이산화 탄소와 굽은 물 분자가 떨리며, 적외선이 분자로 들어온다',s,cls='cover-fig')
FIG['COVER']=cover()

# ═══ S7 연결: 네 칸
def chain():
    s=[]; cy=110
    # ① 원자 오비탈
    p1=[C(80,cy,30,MINUS,1.5,fill=MINUS,extra='fill-opacity=".18"'),T(80,cy+60,tex='1s',size=20),
        lob(175,cy,90,52,1,lsize=18),lob(175,cy,270,52,-1,lsize=18),C(175,cy,3,INK,1,fill=INK),T(215,cy+8,tex='2p',size=20,anchor='start'),
        T(130,228,mix='① 원자 오비탈',size=21,weight=700)]
    s.append(popg(p1,130,cy,0.2))
    # ② 겹침
    p2=[C(375,70,24,MINUS,1.5,fill=MINUS,extra='fill-opacity=".18"'),C(405,70,24,MINUS,1.5,fill=MINUS,extra='fill-opacity=".18"'),
        f'<ellipse cx="390" cy="70" rx="44" ry="30" fill="none" stroke="{FIELD}" stroke-width="2.4"/>',T(455,77,tex='\\sigma',size=22,anchor='start'),
        lob(368,155,90,38,1,lab=False),lob(368,155,270,38,-1,lab=False),lob(412,155,90,38,1,lab=False),lob(412,155,270,38,-1,lab=False),
        f'<rect x="346" y="112" width="88" height="34" rx="12" fill="none" stroke="{FIELD}" stroke-width="2.4" stroke-dasharray="6 4"/>',
        T(455,160,tex='\\pi',size=22,anchor='start'),T(400,228,mix='② 겹침 → 결합',size=21,weight=700)]
    s.append(popg(p2,400,cy,0.8))
    # ③ 혼성
    def star(cx,angs,lab,ang):
        o=[L(cx,cy-8,cx+34*math.cos(math.radians(a)),cy-8-34*math.sin(math.radians(a)),INK,3,extra='stroke-linecap="round"') for a in angs]
        o.append(C(cx,cy-8,4,INK,1,fill=INK)); o.append(T(cx,cy+52,tex=lab,size=20)); o.append(T(cx,cy+78,mix=ang,size=19,fill=MUTED))
        return ''.join(o)
    p3=[star(605,[90,210,330,270],'sp^3','109.5°'),star(685,[90,210,330],'sp^2','120°'),star(765,[0,180],'sp','180°'),
        T(685,228,mix='③ 혼성 오비탈',size=21,weight=700)]
    s.append(popg(p3,685,cy,1.4))
    # ④ 분자 모양
    p4=[T(960,62,tex='\\ce{CH4}',size=22),T(960,86,mix='정사면체',size=19,fill=MUTED),
        T(960,124,tex='\\ce{H2C=CH2}',size=22),T(960,148,mix='평면',size=19,fill=MUTED),
        T(960,186,tex='\\ce{HC#CH}',size=22),T(960,210,mix='직선',size=19,fill=MUTED),
        T(960,246,mix='④ 분자 모양',size=21,weight=700)]
    s.append(popg(p4,960,cy,2.0))
    for x1,x2 in ((250,330),(500,565),(815,880)): s.append(A(x1,cy,x2,cy,'muted',3))
    return svg('0 0 1100 258',1060,'원자 오비탈이 겹쳐 시그마·파이 결합을 만들고, 혼성 오비탈의 방향이 메테인·에틸렌·아세틸렌의 모양을 정한다',s)
FIG['CHAIN']=chain()

# ═══ S10 에너지 준위
def hlev():
    s=[]; Y=lambda n: 60 if n==0 else 60+330/n**2
    s.append(A(36,400,36,40,'ink',2.4)); s.append(T(26,30,mix='에너지',size=19,anchor='start'))
    for n in (1,2,3):
        s.append(L(70,Y(n),290,Y(n),INK,2.4)); s.append(T(300,Y(n)+7,tex=f'n={n}',size=19,anchor='start'))
    s.append(L(70,Y(0),290,Y(0),MUTED,2,dash='7 5')); s.append(T(300,Y(0)+7,tex='n=\\infty',size=19,anchor='start'))
    s.append(T(180,Y(0)-12,tex='E=0',size=19,fill=MUTED))
    s.append(T(180,Y(1)+32,tex='E_1=-2.178\\times10^{-18}\\ \\text{J}',size=19))
    s.append(A(150,Y(1)-4,150,Y(0)+4,'ink',3))
    s.append(T(162,250,mix='흡수||$\\Delta E=2.178\\times10^{-18}\\ \\text{J}$',size=19,anchor='start'))
    s.append(an('move',ele(228,Y(0)-28)+T(244,Y(0)-22,tex='e^-',size=19,anchor='start',fill=MINUS),**{'from':'0,346','dur':'1.4','ease':'out'}))
    return svg('0 0 400 440',350,'수소 원자의 에너지 준위 n=1부터 무한대까지, 전자가 n=1에서 무한대로 옮겨 가며 2.178×10^-18 J를 흡수한다',s)
FIG['HLEV']=hlev()

# ═══ S11 알렌 루이스 구조
def allene():
    s=[]
    at=[A_('C',150,140),A_('C',280,140),A_('C',410,140),A_('H',80,72),A_('H',80,208),A_('H',480,72),A_('H',480,208)]
    bd=[(0,1,2,'l'),(1,2,2,'l'),(0,3,1,'l'),(0,4,1,'l'),(2,5,1,'l'),(2,6,1,'l')]
    s.append(lewis(at,bd,S=34,name='알렌'))
    fc=[(150,196),(280,196),(410,196),(46,80),(46,216),(514,80),(514,216)]
    s.append('<span></span>' if False else '')
    s.append(step([T(x,y,mix='0',size=21,fill=PLUS,weight=700) for x,y in fc],'fa'))
    s.append(step([T(150,96,tex='sp^2',size=23,fill=FIELD,weight=700),T(280,96,tex='sp',size=23,fill=FIELD,weight=700),T(410,96,tex='sp^2',size=23,fill=FIELD,weight=700)],'hy'))
    s.append(T(280,262,mix='알렌 $\\ce{H2C=C=CH2}$',size=21,fill=MUTED))
    return svg('0 0 560 285',540,'알렌의 루이스 구조식 H2C=C=CH2, 모든 원자의 형식 전하 0, 탄소 혼성 sp2, sp, sp2',s)
FIG['ALLENE']=allene()

# ═══ S12 알렌의 두 π 결합
def allpi():
    s=[]; y=190; X=(140,280,420)
    piA=[lob(X[0],y,90,72,1),lob(X[0],y,270,72,-1),lob(X[1],y,90,72,1),lob(X[1],y,270,72,-1),
         f'<rect x="{X[0]-36}" y="{y-80}" width="{X[1]-X[0]+72}" height="46" rx="18" fill="none" stroke="{FIELD}" stroke-width="2.4" stroke-dasharray="7 5"/>',
         f'<rect x="{X[0]-36}" y="{y+34}" width="{X[1]-X[0]+72}" height="46" rx="18" fill="none" stroke="{FIELD}" stroke-width="2.4" stroke-dasharray="7 5"/>',
         T(210,y-96,mix='π 결합 ① 위아래 ($p_y$)',size=19,fill=FIELD,weight=700)]
    s.append(popg(piA,210,y,0.2))
    def head(x):
        return (C(x+11,y-11,25,GRAV,1.8,fill=GRAV,extra='fill-opacity=".30"')+C(x-6,y+6,25,BF,1.8,fill=BF,extra='fill-opacity=".30"')
                +T(x+26,y-24,tex='-',size=18,weight=700)+T(x-20,y+28,tex='+',size=18,weight=700))
    piB=[head(X[1]),head(X[2]),f'<ellipse cx="{(X[1]+X[2])/2}" cy="{y}" rx="112" ry="46" fill="none" stroke="{FIELD}" stroke-width="2.4" stroke-dasharray="7 5"/>',
         T(330,y+122,mix='π 결합 ② 앞뒤 ($p_z$, 지면에 수직)',size=19,fill=FIELD,weight=700)]
    s.append(popg(piB,350,y,0.9))
    for a,b in ((0,1),(1,2)): s.append(L(X[a]+14,y,X[b]-14,y,INK,3))
    # 왼쪽 H: 앞(쐐기)·뒤(점선 쐐기), 오른쪽 H: 지면
    x0=X[0]-14
    s.append(f'<polygon points="{x0},{y+2} {x0-46},{y+30} {x0-40},{y+38}" fill="{INK}"/>')
    for k in range(1,8):
        t=k/8; cx_=x0+(-44)*t; cy_=y-2+(-30)*t; hw=1+5*t
        s.append(L(cx_-hw*.55,cy_-hw*.83,cx_+hw*.55,cy_+hw*.83,INK,2))
    s.append(T(x0-60,y+56,tex='\\mathrm{H}',size=24)); s.append(T(x0-56,y-30,tex='\\mathrm{H}',size=24))
    for sg in (-1,1):
        hx,hy=X[2]+62*math.cos(math.radians(60)),y+sg*62*math.sin(math.radians(60))
        s.append(L(X[2]+8,y+sg*14,hx-7,hy-sg*10,INK,3)); s.append(T(hx+6,hy+9+sg*4,tex='\\mathrm{H}',size=24))
    for i,x in enumerate(X): s.append(T(x,y+8,tex='\\mathrm{C}',size=24,halo=True))
    s.append(T(X[0],y+96,tex='\\mathrm{C}_1',size=19,fill=MUTED)); s.append(T(X[1],y+96,tex='\\mathrm{C}_2',size=19,fill=MUTED)); s.append(T(X[2],y+96,tex='\\mathrm{C}_3',size=19,fill=MUTED))
    return svg('0 0 560 340',540,'알렌의 첫째 파이 결합은 위아래, 둘째 파이 결합은 지면 앞뒤로 서로 수직이며, 왼쪽 수소 둘은 앞뒤, 오른쪽 수소 둘은 지면에 있다',s)
FIG['ALLPI']=allpi()

# ═══ S13 Co(III) 두 착이온
def co3():
    s=[]
    s.append(T(150,26,tex='\\ce{[Co(CN)6]^3-}',size=21)); s.append(dlev(150,70,['',''])); s.append(dlev(150,230,['ud','ud','ud']))
    s.append(dim(54,70,230,'\\Delta_\\mathrm{o}')); s.append(T(242,77,tex='e_g',size=19,anchor='start')); s.append(T(242,237,tex='t_{2g}',size=19,anchor='start'))
    g=[T(420,26,tex='\\ce{[Co(NH3)6]^3+}',size=21),dlev(420,110,['','']),dlev(420,230,['ud','ud','ud']),dim(324,110,230,'\\Delta_\\mathrm{o}'),
       T(512,117,tex='e_g',size=19,anchor='start'),T(512,237,tex='t_{2g}',size=19,anchor='start'),
       f'<rect x="372" y="268" width="26" height="22" rx="4" fill="#3D6FE0"/>',T(404,286,mix='파랑 흡수',size=19,anchor='start'),
       f'<rect x="372" y="298" width="26" height="22" rx="4" fill="#F2B35A" stroke="{MUTED}"/>',T(404,316,mix='노란 주황색',size=19,anchor='start')]
    s.append(step(g,'n3'))
    s.append(f'<rect x="102" y="268" width="26" height="22" rx="4" fill="#7B3FC4"/>'); s.append(T(134,286,mix='보라 흡수',size=19,anchor='start'))
    s.append(f'<rect x="102" y="298" width="26" height="22" rx="4" fill="#F7EBA6" stroke="{MUTED}"/>'); s.append(T(134,316,mix='연한 노란색',size=19,anchor='start'))
    return svg('0 0 560 330',540,'사이안화 착이온은 갈라짐이 커서 보라를 흡수해 연한 노란색, 암민 착이온은 갈라짐이 약간 작아 파랑을 흡수해 노란 주황색, 둘 다 t2g6',s)
FIG['CO3']=co3()

# ═══ S14 Co(II) → Co(III)
def co4():
    s=[]
    s.append(T(200,26,tex='\\ce{[Co(CN)6]^4-}',size=21)); s.append(dlev(200,80,['u',''],new={(0,0)})); s.append(dlev(200,220,['ud','ud','ud']))
    s.append(dim(104,80,220,'\\Delta_\\mathrm{o}')); s.append(T(292,87,tex='e_g',size=19,anchor='start')); s.append(T(292,227,tex='t_{2g}',size=19,anchor='start'))
    s.append(f'<rect x="157" y="58" width="40" height="44" rx="6" fill="{EQUI}" fill-opacity=".18"/>')
    s.append(T(200,272,mix='$t_{2g}^6e_g^1$ · 홀전자 1 · 상자성',size=20))
    s.append(A(400,150,580,150,'ink',3)); s.append(T(490,186,mix='산화',size=20,weight=700))
    s.append(an('move',ele(490,112)+T(506,118,tex='e^-',size=19,anchor='start',fill=MINUS),**{'from':'-310,-32','dur':'1.4','ease':'out'}))
    s.append(T(780,26,tex='\\ce{[Co(CN)6]^3-}',size=21)); s.append(dlev(780,80,['',''])); s.append(dlev(780,220,['ud','ud','ud']))
    s.append(dim(684,80,220,'\\Delta_\\mathrm{o}')); s.append(T(872,87,tex='e_g',size=19,anchor='start')); s.append(T(872,227,tex='t_{2g}',size=19,anchor='start'))
    s.append(T(780,272,mix='$t_{2g}^6$ · 홀전자 0 · 반자성',size=20))
    return svg('0 0 1000 290',900,'코발트(Ⅱ) 사이안화 착이온 t2g6 eg1에서 eg 전자 하나가 빠져나가 코발트(Ⅲ) 착이온 t2g6이 된다',s)
FIG['CO4']=co4()

# ═══ S15 기하 이성질체
def alkene(cx,cy,ul,dl,ur,dr,hl,name,want,g):
    chk(ul+dl+ur+dr+'C2',want,name)
    s=[]; ca,cb=(cx-38,cy),(cx+38,cy)
    s.append(L(ca[0]+14,cy-4,cb[0]-14,cy-4,INK,2.6)+L(ca[0]+14,cy+4,cb[0]-14,cy+4,INK,2.6))
    s.append(T(ca[0],cy+8,tex='\\mathrm{C}',size=24)+T(cb[0],cy+8,tex='\\mathrm{C}',size=24))
    for (x,y),sgx,sgy,grp in ((ca,-1,-1,ul),(ca,-1,1,dl),(cb,1,-1,ur),(cb,1,1,dr)):
        ex,ey=x+sgx*34,y+sgy*56
        s.append(L(x+sgx*10,y+sgy*16,ex-sgx*4,ey-sgy*8,INK,2.6))
        anc='middle' if grp=='H' else ('end' if sgx<0 else 'start')
        lx=ex if grp=='H' else ex+sgx*(-14)
        lx=ex+sgx*2 if grp=='H' else (ex+14 if sgx<0 else ex-14)
        ly=ey+(-4 if sgy<0 else 26)
        wd=gw(grp,22)
        if grp in hl:
            bx=lx-wd if anc=='end' else (lx if anc=='start' else lx-wd/2)
            s.insert(0,f'<rect x="{f(bx-5)}" y="{f(ly-21)}" width="{f(wd+10)}" height="29" rx="6" fill="{HL}" fill-opacity=".45"/>')
        s.append(T(lx,ly,tex='\\ce{'+grp+'}',size=22,anchor=anc))
    s.append(T(cx,cy+108,mix=name,size=19,fill=MUTED))
    return step(s,g)
def iso():
    s=[]
    s.append(alkene(140,110,'CH3','H','Br','H',('CH3','Br'),'시스-1-브로모프로펜','C3H5Br','i1'))
    s.append(alkene(405,110,'CH3','H','H','Br',('CH3','Br'),'트랜스-1-브로모프로펜','C3H5Br','i2'))
    s.append(alkene(675,110,'Br','H','CH2CH3','H',('Br','CH2CH3'),'시스-1-브로모-1-뷰텐','C4H7Br','i3'))
    s.append(alkene(945,110,'Br','H','H','CH2CH3',('Br','CH2CH3'),'트랜스-1-브로모-1-뷰텐','C4H7Br','i4'))
    s.append(L(540,20,540,230,MUTED,1.5,dash='5 5'))
    return svg('0 0 1100 240',1040,'1-브로모프로펜과 1-브로모-1-뷰텐의 시스·트랜스 이성질체 네 구조',s)
FIG['ISO']=iso()

# ═══ S17 치환 반응
def part(x,y,left,right,hl=None,size=24,fill=None):
    s=[T(x,y,tex='\\ce{'+left+'}',size=size,anchor='end'),T(x,y,tex='\\ce{'+right+'}',size=size,anchor='start',fill=fill)]
    if hl:
        wd=gw(right.lstrip('-'),size); x0=x+(gw('-',size) if right.startswith('-') else 0)
        s.insert(0,f'<rect x="{f(x0-4)}" y="{f(y-24)}" width="{f(wd+8)}" height="32" rx="6" fill="{HL}" fill-opacity=".45"/>')
    return ''.join(s)
def rx12():
    s=[]; y1,y2=60,170
    chk('(CH3)3CBr'+'OH','(CH3)3COH'+'Br','7-1'); chk('CH3CH2CH2Br'+'SCH2CH3','CH3CH2CH2SCH2CH3'+'Br','7-2')
    s.append(T(10,y1,mix='1)',size=21,anchor='start',weight=700))
    s.append(part(190,y1,'(CH3)3C','-Br')); s.append(T(178,y1-30,tex='\\delta^+',size=19,fill=PLUS,weight=700)); s.append(T(224,y1-30,tex='\\delta^-',size=19,fill=MINUS,weight=700))
    s.append(T(300,y1,tex='+\\ \\ce{^{-}OH}',size=24)); s.append(T(300,y1+30,mix='친핵체',size=19,fill=MINUS))
    s.append(A(360,y1-8,450,y1-8,'ink',2.6))
    s.append(step([part(600,y1,'(CH3)3C-','OH',hl=True),T(680,y1,tex='+\\ \\ce{Br-}',size=24,anchor='start'),T(600,y1+32,mix='2-메틸-2-프로판올',size=19,fill=MUTED)],'r1'))
    s.append(T(10,y2,mix='2)',size=21,anchor='start',weight=700))
    s.append(part(230,y2,'CH3CH2CH2','-Br')); s.append(T(216,y2-30,tex='\\delta^+',size=19,fill=PLUS,weight=700)); s.append(T(264,y2-30,tex='\\delta^-',size=19,fill=MINUS,weight=700))
    s.append(T(390,y2,tex='+\\ \\ce{^{-}SCH2CH3}',size=24)); s.append(T(390,y2+30,mix='친핵체',size=19,fill=MINUS))
    s.append(A(480,y2-8,560,y2-8,'ink',2.6))
    s.append(step([part(745,y2,'CH3CH2CH2-','SCH2CH3',hl=True),T(895,y2,tex='+\\ \\ce{Br-}',size=24,anchor='start'),T(800,y2+32,mix='에틸 프로필 설파이드',size=19,fill=MUTED)],'r2'))
    return svg('0 0 1080 220',1040,'친핵체 수산화 이온과 에테인싸이올레이트 이온이 브로민이 붙은 탄소를 공격해 브로민화 이온이 떨어져 나가는 치환 반응',s)
FIG['RX12']=rx12()

# ═══ S18 첨가 반응
def rx34():
    s=[]; y1,y2=56,176
    chk('(CH3)2CCH2'+'HBr','(CH3)3CBr','7-3'); chk('CH3CCH'+'Br4','CH3CBr2CHBr2','7-4')
    s.append(T(10,y1,mix='3)',size=21,anchor='start',weight=700))
    s.append(T(160,y1,tex='\\ce{(CH3)2C=CH2 + HBr}',size=24))
    s.append(A(300,y1-8,370,y1-8,'ink',2.6)); s.append(T(335,y1-22,tex='\\ce{H+}',size=19))
    s.append(step([T(470,y1,tex='\\ce{(CH3)3C+}',size=24,fill=EQUI),T(470,y1+32,mix='탄소 양이온 중간체',size=19,fill=MUTED)],'a1'))
    s.append(step([A(560,y1-8,640,y1-8,'ink',2.6),T(600,y1-22,tex='\\ce{Br-}',size=19),
                   part(790,y1,'(CH3)3C','-Br',hl=True),T(790,y1+32,mix='2-브로모-2-메틸프로페인',size=19,fill=MUTED)],'a2'))
    s.append(T(10,y2,mix='4)',size=21,anchor='start',weight=700))
    s.append(T(120,y2,tex='\\ce{CH3-C#C-H}',size=24))
    s.append(A(215,y2-8,295,y2-8,'ink',2.6)); s.append(T(255,y2-22,tex='\\ce{Br2}',size=19))
    s.append(step([T(440,y2,tex='\\ce{CH3-CBr=CHBr}',size=24),T(440,y2+32,mix='첫째 첨가',size=19,fill=MUTED)],'b1'))
    s.append(step([A(585,y2-8,665,y2-8,'ink',2.6),T(625,y2-22,tex='\\ce{Br2}',size=19),
                   T(840,y2,tex='\\ce{CH3-CBr2-CHBr2}',size=24),T(840,y2+32,mix='1,1,2,2-테트라브로모프로페인',size=19,fill=MUTED)],'b2'))
    return svg('0 0 1080 225',1040,'2-메틸프로펜에 브로민화 수소가 탄소 양이온 중간체를 거쳐 첨가되고, 프로파인에 브로민이 두 번 첨가된다',s)
FIG['RX34']=rx34()

# ═══ S19 세 가지 운동
def h2om(cx,cy,r=44,rO=20,rH=15,lab=True):
    hl,hr=h2o(cx,cy,r)
    rO,rH=(24,19) if lab else (rO,rH)
    return bond(cx,cy,*hl,1,5)+bond(cx,cy,*hr,1,5)+atom(*hl,rH,'H')+atom(*hr,rH,'H')+atom(cx,cy,rO,'O')
def motion():
    s=[]
    s.append(an('move',h2om(170,70)+A(225,82,285,82,'ink',2.6),**{'from':'-40,0','rep':'alt','dur':'1.4'}))
    s.append(T(180,170,mix='병진 운동 — 분자 전체가 이동',size=20))
    s.append(an('spin',h2om(550,86),o='550,86',speed='70'))
    s.append(P([(486,40),(470,60),(470,112)],MUTED,2,dash='5 4')+A(470,100,478,126,'muted',2))
    s.append(T(550,170,mix='회전 운동 — 축을 중심으로 회전',size=20))
    O=(920,66); hl,hr=h2o(*O,52)
    s.append(rotsw(bond(*O,*hl,1,5)+atom(*hl,19,'H'),-12,*O)+rotsw(bond(*O,*hr,1,5)+atom(*hr,19,'H'),12,*O)+atom(*O,24,'O'))
    s.append(T(920,170,mix='진동 운동 — 결합 길이·결합각 변화',size=20))
    return svg('0 0 1100 186',1060,'물 분자의 병진 운동, 회전 운동, 진동 운동',s)
FIG['MOTION']=motion()

# ═══ S20 루이스 구조와 모양
def shape():
    s=[]
    O=(180,70); a=math.radians(52.25); hl=(O[0]-72*math.sin(a),O[1]+72*math.cos(a)); hr=(O[0]+72*math.sin(a),O[1]+72*math.cos(a))
    s.append(lewis([A_('O',*O,lp=[60,120]),A_('H',*hl),A_('H',*hr)],[(0,1,1,'l'),(0,2,1,'l')],S=32,name='H2O'))
    s.append(P([(O[0]-18*math.sin(a)*1.7,O[1]+18*math.cos(a)*1.7+6),(O[0],O[1]+40),(O[0]+18*math.sin(a)*1.7,O[1]+18*math.cos(a)*1.7+6)],MUTED,2))
    s.append(T(O[0],O[1]+72,mix='104.5°',size=19,fill=MUTED))
    s.append(T(180,200,mix='$\\ce{H2O}$ · $sp^3$ · 굽은형',size=21,weight=700))
    at=[A_('O',560,90,lp=[135,225]),A_('C',680,90),A_('O',800,90,lp=[45,315])]
    s.append(lewis(at,[(0,1,2,'l'),(1,2,2,'l')],S=32,name='CO2'))
    s.append(L(530,40,830,40,MUTED,1.5,dash='5 4')); s.append(T(680,30,mix='180°',size=19,fill=MUTED))
    s.append(T(680,200,mix='$\\ce{CO2}$ · $sp$ · 직선형',size=21,weight=700))
    return svg('0 0 1000 220',900,'물의 루이스 구조: 산소에 비공유 전자쌍 2개, 결합각 104.5도의 굽은형. 이산화 탄소: O=C=O, 180도 직선형',s)
FIG['SHAPE']=shape()

# ═══ S21 H2O 진동 3가지
def h2ov():
    s=[]; a=math.radians(52.25); bl=(-math.sin(a),math.cos(a)); br=(math.sin(a),math.cos(a))
    def mode(cx,cy,vl,vr,vo,name,nu):
        hl=(cx+54*bl[0],cy+54*bl[1]); hr=(cx+54*br[0],cy+54*br[1]); k=24
        g=[bond(cx,cy,*hl,1,5)+bond(cx,cy,*hr,1,5)]
        g.append(swing(atom(*hl,19,'H')+A(hl[0]+vl[0]*21,hl[1]+vl[1]*21,hl[0]+vl[0]*(21+k),hl[1]+vl[1]*(21+k),'ink',2.4),-vl[0]*5,-vl[1]*5))
        g.append(swing(atom(*hr,19,'H')+A(hr[0]+vr[0]*21,hr[1]+vr[1]*21,hr[0]+vr[0]*(21+k),hr[1]+vr[1]*(21+k),'ink',2.4),-vr[0]*5,-vr[1]*5))
        g.append(swing(atom(cx,cy,24,'O')+A(cx+vo[0]*26,cy+vo[1]*26,cx+vo[0]*44,cy+vo[1]*44,'ink',2.4),-vo[0]*2,-vo[1]*2))
        g.append(T(cx,cy+140,mix=name,size=20,weight=700)); g.append(T(cx,cy+166,tex=nu+'\\ \\text{cm}^{-1}',size=19,fill=MUTED))
        return ''.join(g)
    s.append(mode(100,70,bl,br,(0,-1),'대칭 신축','3657'))
    tl=(math.cos(a),math.sin(a)); tr=(-math.cos(a),math.sin(a))
    s.append(mode(300,70,tl,tr,(0,-1),'굽힘','1595'))
    s.append(mode(500,70,bl,(-br[0],-br[1]),(1,0),'비대칭 신축','3756'))
    return svg('0 0 600 250',580,'물 분자의 진동 세 가지: 대칭 신축 3657, 굽힘 1595, 비대칭 신축 3756 cm-1, 원자마다 움직이는 방향 화살표',s)
FIG['H2OV']=h2ov()

# ═══ S22 CO2 진동 4가지
def co2v():
    s=[]
    def mode(cx,vO1,vC,vO2,name,nu,ir,oop=False):
        y=78; o1,c,o2=co2(cx,y,60)
        g=[bond(*o1,*c,2,6)+bond(*c,*o2,2,6)]
        for (x,yy),v in ((o1,vO1),(c,vC),(o2,vO2)):
            if oop:
                sym=[C(x,yy-34,9,INK,2,fill='#fff')+(C(x,yy-34,2.6,INK,1,fill=INK) if v>0 else L(x-6,yy-40,x+6,yy-28,INK,2)+L(x-6,yy-28,x+6,yy-40,INK,2))]
                g.append(swing(atom(x,yy,20,'O' if (x,yy)!=c else 'C'),0,v*-3)+''.join(sym))
            elif v is None: g.append(atom(x,yy,20,'O' if (x,yy)!=c else 'C'))
            else:
                ux,uy=v; g.append(swing(atom(x,yy,20,'O' if (x,yy)!=c else 'C')+A(x+ux*22,yy+uy*22,x+ux*46,yy+uy*46,'ink',2.4),-ux*5,-uy*5))
        g.append(T(cx,y+88,mix=name,size=20,weight=700)); g.append(T(cx,y+114,tex=nu+'\\ \\text{cm}^{-1}',size=19,fill=MUTED))
        g.append(T(cx,y+140,mix=ir,size=19,fill=FIELD if ir.startswith('적외선 흡수') else MUTED))
        return ''.join(g)
    s.append(mode(140,(-1,0),None,(1,0),'대칭 신축','1333','흡수 없음'))
    s.append(mode(410,(0,-1),(0,1),(0,-1),'굽힘 (지면 안)','667','적외선 흡수'))
    s.append(mode(690,1,-1,1,'굽힘 (지면 앞뒤)','667','적외선 흡수',oop=True))
    s.append(mode(960,(1,0),(-1,0),(1,0),'비대칭 신축','2349','적외선 흡수'))
    s.append(T(1090,22,mix='⊙ 앞으로 · ⊗ 뒤로',size=19,fill=MUTED,anchor='end'))
    return svg('0 0 1100 236',1060,'이산화 탄소의 진동 네 가지: 대칭 신축 1333(적외선 흡수 없음), 굽힘 두 가지 667, 비대칭 신축 2349 cm-1',s)
FIG['CO2V']=co2v()

# ═══ S23 진동 에너지 막대
def ebar():
    hc=6.626e-34*3.00e8; NA=6.02e23
    rows=[('\\ce{H2O}','대칭 신축',3657,INK),('\\ce{H2O}','굽힘',1595,INK),('\\ce{H2O}','비대칭 신축',3756,INK),
          ('\\ce{CO2}','대칭 신축',1333,GR),('\\ce{CO2}','굽힘 ×2',667,GR),('\\ce{CO2}','비대칭 신축',2349,GR)]
    x0=210; sc=6.4; s=[]; DY=46
    for i,(m,n,nu,col) in enumerate(rows):
        E=hc*nu*100*NA/1000; y=40+i*DY
        s.append(T(10,y+22,tex=m,size=20,anchor='start')); s.append(T(72,y+22,mix=n,size=19,anchor='start'))
        s.append(an('scale',f'<rect x="{x0}" y="{y}" width="{f(E*sc)}" height="28" rx="3" fill="{col}" fill-opacity=".85"/>',**{'from':'0,1','o':f'{x0},{y+15}','dur':'.9','delay':f'{.15*i:.2f}'}))
        s.append(T(x0+E*sc+8,y+22,mix=f'{E:.1f}',size=19,anchor='start'))
    yb=40+6*DY+6
    s.append(L(x0,30,x0,yb,INK,2)); s.append(L(x0,yb,x0+50*sc,yb,INK,2))
    for t in range(0,51,10): s.append(L(x0+t*sc,yb,x0+t*sc,yb+6,INK,2)+T(x0+t*sc,yb+26,mix=str(t),size=19))
    s.append(T(x0+25*sc,yb+52,mix='진동 에너지 한 단계 (kJ/mol)',size=19))
    xr=x0+2.48*sc; s.append(L(xr,30,xr,yb,EQUI,2,dash='5 4')); s.append(T(xr+4,24,mix='$RT$ = 2.48 (25 °C)',size=19,fill=EQUI,anchor='start'))
    return svg('0 0 560 390',490,'진동 에너지 한 단계: 물 대칭 신축 43.8, 굽힘 19.1, 비대칭 신축 44.9, 이산화 탄소 대칭 신축 16.0, 굽힘 8.0, 비대칭 신축 28.1 kJ/mol, RT 2.48',s)
FIG['EBAR']=ebar()

# ═══ S24 지구 복사와 흡수 띠
def irspec():
    s=[]; X=lambda l: 60+(l-2)*(470/28); yb=300; top=60
    def B(l):
        l=l*1e-6; return 1/(l**5*(math.exp(6.626e-34*3e8/(l*1.381e-23*288))-1))
    mx=max(B(2+i*0.05) for i in range(561))
    for lo,hi,lab,ly in ((2.5,2.9,'$\\ce{H2O}$',1),(4.1,4.5,'$\\ce{CO2}$',0),(5.5,7.0,'$\\ce{H2O}$',1),(13.5,16.5,'$\\ce{CO2}$',0)):
        s.append(an('fade',f'<rect x="{f(X(lo))}" y="{top}" width="{f(X(hi)-X(lo))}" height="{yb-top}" fill="{MINUS}" fill-opacity=".18"/>'+T((X(lo)+X(hi))/2,top-10-ly*26,mix=lab,size=19),dur='1',delay='.6'))
    pts=[(X(2+i*0.1),yb-(yb-top-20)*B(2+i*0.1)/mx) for i in range(281)]
    s.append(an('draw',P(pts,PLUS,3),dur='1.4'))
    s.append(T(X(19),150,mix='지표(288 K)가||내보내는 적외선',size=19,fill=PLUS,anchor='start'))
    s.append(L(60,yb,535,yb,INK,2)); s.append(L(60,yb,60,top-10,INK,2))
    for t in (5,10,15,20,25,30): s.append(L(X(t),yb,X(t),yb+6,INK,2)+T(X(t),yb+26,mix=str(t),size=19))
    s.append(T(300,yb+54,mix='파장 (μm)',size=19))
    s.append(T(48,180,mix='복사 세기',size=19,anchor='middle',extra='transform="rotate(-90 48 180)"'))
    s.append(T(X(15),yb-12,mix='굽힘',size=19,fill=MINUS,halo=True)); s.append(T(X(6.3)+4,yb-12,mix='굽힘',size=19,fill=MINUS,halo=True))
    return svg('0 0 560 380',540,'지표가 내보내는 적외선 세기는 약 10 마이크로미터에서 가장 크고, 물은 2.7과 6.3, 이산화 탄소는 4.3과 15 마이크로미터 부근을 흡수한다',s)
FIG['IRSPEC']=irspec()

# ═══ S25 온실 효과 그림
def green():
    s=[]
    s.append(f'<rect x="10" y="236" width="420" height="44" rx="6" fill="#D9CBB0"/>'); s.append(T(400,266,mix='지표',size=19,anchor='end'))
    s.append(C(48,46,24,EQUI,2,fill=EQUI,extra='fill-opacity=".5"'))
    s.append(A(70,70,150,230,'equi',3)); s.append(A(100,58,190,230,'equi',3)); s.append(T(96,128,mix='햇빛',size=19,anchor='end'))
    s.append(an('draw',wave(230,232,262,128,INK,6,14,2.6),dur='1')+A(258,140,264,122,'ink',2.6)); s.append(T(270,214,mix='적외선',size=19,anchor='start'))
    o1,c,o2=co2(300,96,30)
    s.append(popg(bond(*o1,*c,2,5)+bond(*c,*o2,2,5)+atom(*o1,12,'O','-')+atom(*c,12,'C','-')+atom(*o2,12,'O','-'),300,96,1.0))
    s.append(popg(h2om(390,150,28,12,9,False).replace(',O"',',O,-"').replace(',H"',',H,-"'),390,160,1.2))
    s.append(an('draw',wave(305,120,330,222,INK,5,12,2.2),dur='.9',delay='1.6')+A(328,212,331,228,'ink',2.2))
    s.append(an('draw',wave(320,80,380,24,INK,5,12,2.2),dur='.9',delay='1.6')+A(372,32,384,20,'ink',2.2))
    s.append(T(345,232,mix='다시 내보냄',size=19,anchor='start',halo=True))
    s.append(T(300,52,tex='\\ce{CO2}',size=19,anchor='end')); s.append(T(425,128,tex='\\ce{H2O}',size=19,anchor='end'))
    return svg('0 0 440 290',430,'햇빛이 지표를 데우고 지표가 적외선을 내보내면 이산화 탄소와 물 분자가 흡수해 일부를 지표 쪽으로 다시 내보낸다',s)
FIG['GREEN']=green()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused)
