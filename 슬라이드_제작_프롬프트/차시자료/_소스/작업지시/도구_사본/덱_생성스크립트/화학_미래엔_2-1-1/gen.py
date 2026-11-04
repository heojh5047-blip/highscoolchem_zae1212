# slides.tpl.html 의 @@이름@@ 자리에 계산한 SVG 조각을 넣어 slides.html을 만든다.
import os, sys, json, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *
HERE=os.path.dirname(os.path.abspath(__file__))
OUT='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학_미래엔/2-1-1_화학_결합의_전기적_성질/slides.html'
F={}

def circ(parts,stroke=3,ls=22):
    return json.dumps({"parts":parts,"stroke":stroke,"labelSize":ls},ensure_ascii=False).replace("'","&#39;")

# ── S1 표지: 전기 분해 장치 ──
def cover():
    s=0.92; ox=270-280*s; oy=40
    body=hofmann(ox,oy,s,gasL=62,gasR=124)
    lab=(tex(ox+150*s,oy+105*s,'\\ce{O2}',24,'end')+tex(ox+410*s,oy+135*s,'\\ce{H2}',24,'start')
         +tex(ox+150*s,oy+305*s,'(+)극',20,'end',mix=True)+tex(ox+410*s,oy+305*s,'(−)극',20,'start',mix=True))
    return f'<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>{body}{lab}', circ(hofmann_circuit(ox,oy,s),3)

# ── S7 장치 (설명용, 라벨 많음) ──
def apparatus7():
    body=hofmann(0,0,1,gasL=60,gasR=120)
    flow=(f'<path d="M190 330 L190 350 L272 350" fill="none" stroke="{MINUS}" stroke-width="3" stroke-dasharray="4 10" data-anim="dash" data-speed="-30" data-flow="1"/>'
          f'<path d="M288 350 L370 350 L370 330" fill="none" stroke="{MINUS}" stroke-width="3" stroke-dasharray="4 10" data-anim="dash" data-speed="-30" data-flow="1"/>')
    arr=('<g data-arw="206,334,252,334,minus,3"></g><g data-arw="308,334,354,334,minus,3"></g>'
         +tex(229,326,'e^-',20,fill=MINUS)+tex(331,326,'e^-',20,fill=MINUS))
    lab=(tex(156,80,'산소 $\\ce{O2}$',21,'end',mix=True)+tex(404,110,'수소 $\\ce{H2}$',21,'start',mix=True)
         +tex(156,306,'(+)극',21,'end',mix=True,fill=PLUS)+tex(404,306,'(−)극',21,'start',mix=True,fill=MINUS)
         +tex(280,394,'전원(9 V 건전지)',19,mix=True,fill=MUTED)
         +tex(280,212,'황산 나트륨||수용액',19,mix=True,fill=MUTED))
    return body+flow+arr+lab, circ(hofmann_circuit(0,0,1),3)

# ── S9 과정 그림 (작게) ──
def proc(k):
    s=0.5; ox=10; oy=6
    if k==1:
        body=hofmann(ox,oy,s,gasL=0,gasR=0,anim=False,bubbles=False)
        return body, None
    if k==2:
        body=hofmann(ox,oy,s,gasL=0,gasR=0,anim=False,bubbles=False)
        return body, circ(hofmann_circuit(ox,oy,s),2.5)
    if k==3:
        body=hofmann(ox,oy,s,gasL=60,gasR=120,anim=True,bubbles=False)
        return body, circ(hofmann_circuit(ox,oy,s),2.5)
    # 4: 시험관 기체 확인
    o=(f'<rect x="58" y="40" width="44" height="120" rx="20" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2.5"/>'
       f'<rect x="56" y="140" width="48" height="10" fill="#FFFFFF" stroke="none"/>'
       f'<path d="M80 172 q-10 -14 0 -30 q10 16 0 30z" fill="#F2A33A" stroke="#C2410C" stroke-width="1.5"/>'
       f'<line x1="80" y1="172" x2="80" y2="196" stroke="#8B5A2B" stroke-width="4" stroke-linecap="round"/>'
       + tex(80,30,'\\ce{H2}',18) +
       f'<rect x="198" y="40" width="44" height="120" rx="20" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2.5"/>'
       f'<path d="M220 172 q-6 -8 0 -16 q6 8 0 16z" fill="#F2A33A" stroke="#C2410C" stroke-width="1.2"/>'
       f'<line x1="220" y1="172" x2="220" y2="196" stroke="#8B5A2B" stroke-width="3" stroke-linecap="round"/>'
       + tex(220,30,'\\ce{O2}',18))
    return o, None

# ── S13 입자 모형: 2H2O → 2H2 + O2 (원자 수 보존, 생성물 원자가 반응물 자리에서 옮겨 옴) ──
def particles13():
    sc=0.9
    W=[(70,70),(70,160)]          # 물 분자 중심
    P_H=[(250,62),(250,128)]      # 수소 분자
    P_O=(250,196)                 # 산소 분자
    s=''
    for (x,y) in W: s+=water(x,y,sc,lab=False)
    s+='<g data-arw="125,118,178,118,ink,3"></g>'
    # 생성물: 각 원자를 반응물 자리에서 옮겨 온다
    Hsrc=[(W[0][0]-22*sc,W[0][1]+17*sc),(W[0][0]+22*sc,W[0][1]+17*sc),(W[1][0]-22*sc,W[1][1]+17*sc),(W[1][0]+22*sc,W[1][1]+17*sc)]
    Hdst=[(P_H[0][0]-13*sc,P_H[0][1]),(P_H[0][0]+13*sc,P_H[0][1]),(P_H[1][0]-13*sc,P_H[1][1]),(P_H[1][0]+13*sc,P_H[1][1])]
    Osrc=[W[0],W[1]]; Odst=[(P_O[0]-17*sc,P_O[1]),(P_O[0]+17*sc,P_O[1])]
    for i,((sx,sy),(dx,dy)) in enumerate(zip(Hsrc,Hdst)):
        s+=f'<g data-anim="move" data-from="{f(sx-dx)},{f(sy-dy)}" data-dur="1.4" data-delay=".2" data-ease="io" data-on="step">{atom(dx,dy,18*sc,"H","-")}</g>'
    for (sx,sy),(dx,dy) in zip(Osrc,Odst):
        s+=f'<g data-anim="move" data-from="{f(sx-dx)},{f(sy-dy)}" data-dur="1.4" data-delay=".2" data-ease="io" data-on="step">{atom(dx,dy,24*sc,"O","-")}</g>'
    s+=tex(70,242,'물 분자 2개',20,mix=True,fill=MUTED)+tex(250,242,'수소 2 + 산소 1',20,mix=True,fill=MUTED)
    return s

def mini13():
    s=0.46; ox=10; oy=4
    return hofmann(ox,oy,s,gasL=60,gasR=120,anim=False,bubbles=True), circ(hofmann_circuit(ox,oy,s),2.4)

# ── S14 전자 4개 → H2 2개, O2 1개 ──
def electrons14():
    s=''
    s+=tex(16,40,'(−)극',20,'start',mix=True,fill=MINUS)
    for i in range(4): s+=f'<g data-chg="{110+i*30},34,10,-"></g>'
    s+='<g data-arw="222,34,280,34,ink,3"></g>'
    s+=h2(330,34)+h2(410,34)
    s+=tex(155,82,'전자 4개를 얻으면',18,mix=True,fill=MUTED)+tex(370,82,'수소 분자 2개',18,mix=True,fill=MUTED)
    s+=tex(16,146,'(+)극',20,'start',mix=True,fill=PLUS)
    s+=o2(150,140)
    s+='<g data-arw="222,140,280,140,ink,3"></g>'
    for i in range(4): s+=f'<g data-chg="{325+i*30},140,10,-"></g>'
    s+=tex(150,188,'산소 분자 1개가 생기면',18,mix=True,fill=MUTED)+tex(370,188,'전자 4개를 내놓음',18,mix=True,fill=MUTED)
    return s

# ── S16 / S28 액체 염화 나트륨 전기 분해 장치 ──
def molten(lab_l='(+)극', lab_r='(−)극', pos='left', anim=True, names=True):
    s=''
    # 도가니
    s+=f'<path d="M150 150 L170 300 L390 300 L410 150" fill="#FCE9D2" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>'
    s+=f'<line x1="154" y1="180" x2="406" y2="180" stroke="#E7B98A" stroke-width="2"/>'
    # 불꽃
    for x in (230,280,330):
        s+=f'<path d="M{x} 352 q-16 -22 0 -44 q16 22 0 44z" fill="#F2A33A" stroke="#C2410C" stroke-width="1.5"/>'
    s+=f'<rect x="200" y="352" width="160" height="10" rx="3" fill="{GRAV}"/>'
    # 전극
    for x in (220,340):
        s+=f'<rect x="{x-7}" y="70" width="14" height="190" rx="3" fill="#3A3F47"/>'
    # 나트륨 방울((−)쪽), 염소 기포((+)쪽)
    na_x = 340 if pos=='left' else 220
    cl_x = 220 if pos=='left' else 340
    for i,(dx,dy) in enumerate([(-16,250),(14,232),(-14,212)]):
        s+=f'<circle cx="{na_x+dx}" cy="{dy}" r="7" fill="#C9CED6" stroke="#7E8B98" stroke-width="1.5"/>'
    for i,(dx,dy) in enumerate([(-15,240),(15,214),(-13,192)]):
        c=f'<circle cx="{cl_x+dx}" cy="{dy}" r="6.5" fill="#E4EEA0" stroke="#9BAA2E" stroke-width="1.5"/>'
        if anim: c=f'<g data-anim="move" data-from="0,30" data-dur="1.4" data-delay="{0.3*i}" data-rep="loop" data-ease="lin">{c}</g>'
        s+=c
    # 염소 기체(위로)
    s+=f'<path d="M{cl_x-22} 140 q8 -14 0 -26 q-8 -12 4 -24" fill="none" stroke="#B5C23A" stroke-width="2.5" stroke-dasharray="5 4"/>'
    if names:
        s+=tex(cl_x-14 if pos=='left' else cl_x+14, 150,'염소 $\\ce{Cl2}$',20,'end' if pos=='left' else 'start',mix=True,fill='#6B7A10')
        s+=tex(na_x+30 if pos=='left' else na_x-30, 230,'나트륨 $\\ce{Na}$',20,'start' if pos=='left' else 'end',mix=True)
    s+=tex(280,284,'액체 $\\ce{NaCl}$',20,mix=True,fill=MUTED)
    s+=tex(204 if True else 0,102,lab_l,21,'end',mix=True,fill=PLUS if '+' in lab_l else (MINUS if '−' in lab_l else INK))
    s+=tex(356,102,lab_r,21,'start',mix=True,fill=MINUS if '−' in lab_r else (PLUS if '+' in lab_r else INK))
    parts=[["wire",[[220,70],[220,36],[272 if pos=='left' else 272,36]]],["wire",[[288,36],[340,36],[340,70]]],
           ["bat",[280,36],{"dir":"h","pos":pos,"signs":True}]]
    return s, circ(parts,3)

# ── S17 이온 이동 ──
def ions17():
    s=f'<rect x="20" y="20" width="520" height="230" rx="10" fill="#FCE9D2" stroke="#E7B98A" stroke-width="2"/>'
    s+=f'<rect x="30" y="34" width="22" height="202" rx="3" fill="#3A3F47"/><rect x="508" y="34" width="22" height="202" rx="3" fill="#3A3F47"/>'
    s+='<g data-pm="+,16,41:70 41:120 41:170 41:220,plus"></g><g data-pm="-,16,519:70 519:120 519:170 519:220,minus"></g>'
    rnd=random.Random(3)
    na=[(170,70),(250,160),(330,90),(400,200),(200,205)]
    cl=[(130,150),(290,215),(360,55),(445,125),(225,110)]
    gna=''; gcl=''
    for (x,y) in na:
        gna+=atom(x,y,19,'Na','-')+tex(x,y+7,'+',20,fill='#FFFFFF')
        gna+=f'<g data-arw="{x+24},{y},{x+60},{y},plus,2.5"></g>'
    for (x,y) in cl:
        gcl+=atom(x,y,32,'Cl','-')+tex(x,y+7,'−',22,mix=True,fill='#FFFFFF')
        gcl+=f'<g data-arw="{x-36},{y},{x-72},{y},minus,2.5"></g>'
    s+=f'<g data-anim="move" data-from="-40,0" data-dur="1.8" data-delay=".3" data-ease="out">{gna}</g>'
    s+=f'<g data-anim="move" data-from="40,0" data-dur="1.8" data-delay=".3" data-ease="out">{gcl}</g>'
    s+=tex(60,276,'(+)극',21,'middle',mix=True,fill=PLUS)+tex(500,276,'(−)극',21,'middle',mix=True,fill=MINUS)
    # 범례
    s+=atom(205,268,12,'Na','-')+tex(222,275,'$\\ce{Na+}$',20,'start',mix=True)+atom(315,268,14,'Cl','-')+tex(334,275,'$\\ce{Cl-}$',20,'start',mix=True)
    return s

# ── S18 고체·액체·수용액 ──
def lattice(x0,y0,nx,ny,d,rna=19,rcl=32,cls=''):
    s=''
    for j in range(ny):
        for i in range(nx):
            x=x0+i*d; y=y0+j*d
            if (i+j)%2==0: s+=atom(x,y,rcl,'Cl','-')
            else: s+=atom(x,y,rna,'Na','-')
    return s

def solid18():
    s=lattice(55,45,5,3,48,13,22)
    return f'<g data-anim="move" data-from="1.5,0" data-dur=".18" data-rep="swing">{s}</g>'

def liquid18():
    pts=[(50,50,'Cl'),(120,40,'Na'),(200,62,'Cl'),(250,140,'Na'),(90,128,'Na'),(160,150,'Cl'),(230,40,'Na'),(40,150,'Cl'),(150,95,'Na'),(250,85,'Cl')]
    s=''
    for i,(x,y,e) in enumerate(pts):
        a=atom(x,y,22 if e=='Cl' else 13,e,'-')
        dx,dy=[(8,-6),(-7,8),(6,7),(-8,-5),(7,5)][i%5]
        s+=f'<g data-anim="move" data-from="{dx},{dy}" data-dur="{1.0+0.15*(i%4)}" data-rep="alt" data-ease="io">{a}</g>'
    return s

def aq18():
    rnd=random.Random(11)
    s=''
    ions=[(70,60,'Na'),(200,70,'Cl'),(120,140,'Cl'),(240,145,'Na')]
    for (x,y,e) in ions:
        R=34 if e=='Cl' else 28
        for k in range(5 if e=='Cl' else 4):
            a=math.radians(k*360/(5 if e=='Cl' else 4)+rnd.uniform(-10,10))
            wx=x+R*math.cos(a); wy=y+R*math.sin(a)
            # 물 분자: Na+ 쪽으로는 O, Cl- 쪽으로는 H
            if e=='Na':
                s+=atom(wx+8*math.cos(a)-4*math.sin(a),wy+8*math.sin(a)+4*math.cos(a),7,'H','-')+atom(wx+8*math.cos(a)+4*math.sin(a),wy+8*math.sin(a)-4*math.cos(a),7,'H','-')+atom(wx,wy,10,'O','-')
            else:
                s+=atom(wx+4,wy,10,'O','-')+atom(wx-6*math.cos(a),wy-6*math.sin(a),7,'H','-')
        s+=atom(x,y,22 if e=='Cl' else 13,e,'-')
    return s

# ── S20 18족 ──
def noble20():
    s=bohr(90,110,2,[2],radii=(26,44,62))+tex(90,215,'$\\ce{He}$ (2)',20,mix=True)
    s+=bohr(280,110,10,[2,8],radii=(26,44,62))+tex(280,215,'$\\ce{Ne}$ (2, 8)',20,mix=True)
    s+=bohr(480,110,18,[2,8,8],radii=(26,44,62))+tex(480,215,'$\\ce{Ar}$ (2, 8, 8)',20,mix=True)
    return s

# ── S21 이온 형성 ──
def ions21():
    s=''
    # Na → Na+
    s+=bohr(85,90,11,[2,8,1],start=[0,0,1])
    s+='<g data-arw="170,90,240,90,ink,3"></g>'+tex(205,78,'전자 1개||잃음',18,mix=True,fill=MINUS)
    s+=bohr(330,90,11,[2,8])
    s+=f'<path d="M262 30 q-8 0 -8 8 v104 q0 8 8 8" fill="none" stroke="{INK}" stroke-width="2.5"/><path d="M398 30 q8 0 8 8 v104 q0 8 -8 8" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    s+=tex(414,46,'+',24,'start',fill=PLUS)
    s+=tex(85,178,'$\\ce{Na}$ (2, 8, 1)',20,mix=True)+tex(330,178,'$\\ce{Na+}$ (2, 8)',20,mix=True)
    s+=tex(500,98,'$\\ce{Ne}$와 같은||전자 배치',19,mix=True,fill=MUTED)
    # Cl → Cl-
    y=290
    s+=bohr(85,y,17,[2,8,7])
    s+='<g data-arw="170,290,240,290,ink,3"></g>'+tex(205,278,'전자 1개||얻음',18,mix=True,fill=MINUS)
    s2,pts=bohr(330,y,17,[2,8,8],ret_pts=True)
    s+=s2
    s+=f'<path d="M262 {y-74} q-8 0 -8 8 v132 q0 8 8 8" fill="none" stroke="{INK}" stroke-width="2.5"/><path d="M398 {y-74} q8 0 8 8 v132 q0 8 -8 8" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    s+=tex(414,y-56,'−',24,'start',mix=True,fill=MINUS)
    # 얻은 전자 강조(왼쪽 쌍 중 하나)
    k,i,x,yy=[p for p in pts if p[0]==2][-1]
    s+=f'<circle cx="{f(x)}" cy="{f(yy)}" r="10" fill="none" stroke="{EQUI}" stroke-width="2"/>'
    s+=tex(85,y+90,'$\\ce{Cl}$ (2, 8, 7)',20,mix=True)+tex(330,y+90,'$\\ce{Cl-}$ (2, 8, 8)',20,mix=True)
    s+=tex(500,y+8,'$\\ce{Ar}$과 같은||전자 배치',19,mix=True,fill=MUTED)
    return s

# ── S22 단계 카드 ──
def card22_1():
    R=(16,28,40)
    a,pa=bohr(70,85,11,[2,8,1],radii=R,nr=14,er=4.5,lsize=16,start=[0,0,1],skip={(2,0)},ret_pts=True)
    b,pb=bohr(230,85,17,[2,8,8],radii=R,nr=14,er=4.5,lsize=16,skip=None,ret_pts=True)
    # 이동한 전자: Cl 셋째 껍질 마지막(왼쪽 쌍) 위치에 있음 → Na 오른쪽 자리에서 옮겨 옴
    src=[p for p in pa if p[0]==2][0]; dst=[p for p in pb if p[0]==2][-1]
    # b에서 그 전자를 빼고 따로 그림
    b,_=bohr(230,85,17,[2,8,8],radii=R,nr=14,er=4.5,lsize=16,skip={(2,dst[1])},ret_pts=True)
    e=f'<g data-anim="move" data-from="{f(src[2]-dst[2])},{f(src[3]-dst[3])}" data-dur="1.4" data-delay=".5" data-ease="io"><circle cx="{f(dst[2])}" cy="{f(dst[3])}" r="4.5" fill="{MINUS}"/></g>'
    lab=tex(70,160,'\\ce{Na}',19)+tex(230,160,'\\ce{Cl}',19)
    arc=f'<path d="M112 70 Q150 40 186 76" fill="none" stroke="{MINUS}" stroke-width="2" stroke-dasharray="4 4"/>'
    return a+b+arc+e+lab

def card22_2():
    s=atom(85,85,19,'Na','\\mathrm{Na}^{+}')+atom(215,85,32,'Cl','\\mathrm{Cl}^{-}')
    s+=tex(85,150,'양이온',18,mix=True,fill=PLUS)+tex(215,150,'음이온',18,mix=True,fill=MINUS)
    return s

def card22_3():
    s=lattice(46,40,5,3,52,16,27)
    return f'<g data-anim="move" data-from="0,-14" data-dur="1.2" data-delay=".3" data-ease="out" data-on="step">{s}</g>'

# ── S24 H2 형성 ──
def h2_24():
    r=30
    a=bohr(70,80,1,[1],radii=(r,),nr=14,er=5.5,lsize=16,start=[1])
    b=bohr(220,80,1,[1],radii=(r,),nr=14,er=5.5,lsize=16)
    # 오른쪽 원자의 전자를 왼쪽 자리에
    b=(f'<circle cx="220" cy="80" r="{r}" fill="none" stroke="{MUTED}" stroke-width="1.6"/>'
       f'<circle cx="{220-r}" cy="80" r="5.5" fill="{MINUS}"/><circle cx="220" cy="80" r="14" fill="#FDE2E4" stroke="{PLUS}" stroke-width="1.8"/>'+tex(220,85.8,'+1',16,fill=PLUS))
    left=f'<g data-anim="move" data-from="-30,0" data-dur="1.2" data-delay=".2" data-ease="out">{a}</g>'
    right=f'<g data-anim="move" data-from="30,0" data-dur="1.2" data-delay=".2" data-ease="out">{b}</g>'
    s=left+right+tex(145,86,'+',26)
    s+='<g data-arw="270,80,320,80,ink,3"></g>'
    # H2: 두 껍질 겹침, 전자쌍 가운데
    cx1,cx2=385,425
    s+=f'<ellipse cx="405" cy="80" rx="12" ry="22" fill="{FIELD}" fill-opacity=".18" stroke="{FIELD}" stroke-width="1.5"/>'
    for cx in (cx1,cx2):
        s+=f'<circle cx="{cx}" cy="80" r="{r}" fill="none" stroke="{MUTED}" stroke-width="1.6"/>'
    s+=f'<circle cx="405" cy="70" r="5.5" fill="{MINUS}"/><circle cx="405" cy="90" r="5.5" fill="{MINUS}"/>'
    for cx in (cx1,cx2):
        s+=f'<circle cx="{cx}" cy="80" r="14" fill="#FDE2E4" stroke="{PLUS}" stroke-width="1.8"/>'+tex(cx-(10 if cx==cx1 else -10),85.8,'+1',16,fill=PLUS)
    s+=tex(70,145,'\\ce{H}',20)+tex(220,145,'\\ce{H}',20)+tex(405,145,'\\ce{H2}',20)
    s+=tex(405,22,'공유 전자쌍',18,mix=True,fill=FIELD)
    return s

# ── S25 H2O 보어 모형 ──
def h2o25():
    cx,cy=150,80; rO=(22,44); rH=26
    s=f'<circle cx="{cx}" cy="{cy}" r="{rO[0]}" fill="none" stroke="{MUTED}" stroke-width="1.6"/><circle cx="{cx}" cy="{cy}" r="{rO[1]}" fill="none" stroke="{MUTED}" stroke-width="1.6"/>'
    # 첫 껍질 전자 2
    s+=f'<circle cx="{cx}" cy="{cy-rO[0]}" r="5" fill="{MINUS}"/><circle cx="{cx}" cy="{cy+rO[0]}" r="5" fill="{MINUS}"/>'
    hs=[]
    for ang in (218,322):
        a=math.radians(ang); d=rO[1]+rH-20
        hx=cx+d*math.cos(a); hy=cy-d*math.sin(a); hs.append((hx,hy,a))
    for hx,hy,a in hs:
        s+=f'<circle cx="{f(hx)}" cy="{f(hy)}" r="{rH}" fill="none" stroke="{MUTED}" stroke-width="1.6"/>'
        m=(rO[1]+ (rO[1]+rH-20-rH))/2   # 겹친 렌즈 가운데
        px=cx+m*math.cos(a); py=cy-m*math.sin(a); nx=-math.sin(a); ny=-math.cos(a)
        s+=f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="9" ry="17" transform="rotate({f(-math.degrees(a)+90)} {f(px)} {f(py)})" fill="{FIELD}" fill-opacity=".18" stroke="{FIELD}" stroke-width="1.5"/>'
        for sgn in (-1,1):
            s+=f'<circle cx="{f(px+nx*7*sgn)}" cy="{f(py+ny*7*sgn)}" r="5" fill="{MINUS}"/>'
    # 나머지 O 전자 4 (위쪽 두 쌍)
    for ang in (125,55):
        for p in (-12,12):
            a=math.radians(ang+p); s+=f'<circle cx="{f(cx+rO[1]*math.cos(a))}" cy="{f(cy-rO[1]*math.sin(a))}" r="5" fill="{MINUS}"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="14" fill="#FDE2E4" stroke="{PLUS}" stroke-width="1.8"/>'+tex(cx,cy+5.8,'+8',16,fill=PLUS)
    for hx,hy,a in hs:
        s+=f'<circle cx="{f(hx)}" cy="{f(hy)}" r="12" fill="#FDE2E4" stroke="{PLUS}" stroke-width="1.8"/>'+tex(hx,hy+5.8,'+1',16,fill=PLUS)
    s+=tex(cx,190,'$\\ce{H2O}$ — 공유 전자쌍 2개',19,mix=True)
    return s

# ── S3 중단원 도입: 소금 결정과 물 분자 ──
def intro3():
    s=water(80,70,1.0,lab=False)+water(60,150,1.0,lab=False,flip=True)
    s+=tex(80,222,'물($\\ce{H2O}$)',19,mix=True)+tex(80,246,'공유 결합',19,mix=True,fill=MUTED)
    s+=lattice(200,60,4,3,48,15,26)
    s+=tex(272,222,'염화 나트륨($\\ce{NaCl}$)',19,mix=True)+tex(272,246,'이온 결합',19,mix=True,fill=MUTED)
    # 석영: Si 사이에 O가 다리를 놓는 그물
    q=''; pts=[(420,60),(500,60),(420,140),(500,140)]
    bonds=[((420,60),(500,60)),((420,140),(500,140)),((420,60),(420,140)),((500,60),(500,140))]
    for (x1,y1),(x2,y2) in bonds:
        q+=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#9AA5B1" stroke-width="5"/>'
    for (x,y) in pts:
        for dx,dy in ((-34,0),(0,-34)) if (x,y)==(420,60) else ((34,0),) if (x,y)==(500,60) else ((0,34),):
            q+=f'<line x1="{x}" y1="{y}" x2="{x+dx}" y2="{y+dy}" stroke="#9AA5B1" stroke-width="5"/>'
    for (x1,y1),(x2,y2) in bonds: q+=atom((x1+x2)/2,(y1+y2)/2,16,'O','-')
    for (x,y) in pts: q+=atom(x,y,25,'Si')
    s+=q+tex(460,222,'석영($\\ce{SiO2}$)',19,mix=True)+tex(460,246,'공유 결합 그물',19,mix=True,fill=MUTED)
    return s

# ── S6 원자 = 원자핵 + 전자 ──
def atom6():
    s=bohr(110,110,1,[1],radii=(36,),nr=16,er=6,lsize=17,start=[0])
    s=bohr(110,110,1,[1],radii=(40,),nr=16,er=6,lsize=17)
    s+=bohr(330,110,8,[2,6],radii=(30,58),nr=17,er=6,lsize=18)
    s+=tex(110,195,'수소 원자',19,mix=True)+tex(330,195,'산소 원자',19,mix=True)
    s+=f'<line x1="347" y1="110" x2="430" y2="40" stroke="{MUTED}" stroke-width="1.5"/>'+tex(434,38,'원자핵 (+)',19,'start',mix=True,fill=PLUS)
    s+=f'<line x1="388" y1="118" x2="432" y2="150" stroke="{MUTED}" stroke-width="1.5"/>'+tex(434,160,'전자 (−)',19,'start',mix=True,fill=MINUS)
    return s


# ── S5 비유: 조각을 잇는 접착제 ↔ 원자를 잇는 화학 결합 ──
def anal5():
    s=''
    cols=['#9FC3DD','#F2C230','#E8792B','#6FBF8E']
    for i,(x,y,w,h) in enumerate([(20,60,60,40),(84,52,50,56),(138,64,56,36)]):
        s+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{cols[i]}" stroke="{GLASS}" stroke-width="2"/>'
    for x in (82,136):
        s+=f'<rect x="{x-3}" y="66" width="6" height="28" rx="2" fill="{EQUI}"/>'
    s+=tex(105,150,'재료 + 접착제',19,mix=True,fill=MUTED)
    s+=tex(215,90,'↔',30,mix=True,fill=MUTED)
    s+=water(320,66,1.5,lab=False)
    s+=tex(320,150,'원자 + ?',19,mix=True,fill=MUTED)
    return s

# ── S9 빨대 장치 ──
def straw():
    s=f'<rect x="40" y="110" width="220" height="150" rx="14" fill="#FFFFFF" stroke="{GLASS}" stroke-width="3"/>'
    s+=f'<rect x="43" y="170" width="214" height="87" rx="11" fill="{WATER}"/>'
    for x,gh,lab,col in ((110,30,'(+)극',PLUS),(190,60,'(−)극',MINUS)):
        s+=f'<rect x="{x-11}" y="30" width="22" height="200" fill="{WATER}" stroke="{GLASS}" stroke-width="2"/>'
        s+=f'<rect x="{x-9}" y="32" width="18" height="{gh}" fill="#FFFFFF"/>'
        s+=f'<rect x="{x-13}" y="22" width="26" height="12" rx="3" fill="{MUTED}"/>'
        s+=f'<line x1="{x-24}" y1="214" x2="{x+4}" y2="214" stroke="{ELEC}" stroke-width="3"/><circle cx="{x-26}" cy="214" r="4" fill="{ELEC}"/>'
        s+=tex(x,292 if False else 250,lab,18,mix=True,fill=col)
    # 도선 → 건전지(위쪽 오른쪽)
    s+=f'<path d="M84 214 L64 214 L64 280" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    s+=f'<path d="M164 214 L150 214 L150 240 L236 240 L236 280" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    s+=f'<rect x="44" y="278" width="212" height="20" rx="4" fill="#3A3F47"/>'
    s+=tex(64,294,'+',18,fill='#FFFFFF')+tex(236,294,'−',18,mix=True,fill='#FFFFFF')+tex(150,294,'9 V 건전지',16,mix=True,fill='#FFFFFF')
    s+=tex(150,96,'빨대',18,mix=True,fill=MUTED)
    return s

# ── S20 알루미늄 제련 모식도 ──
def al20():
    s=f'<path d="M60 90 L76 220 L324 220 L340 90" fill="#FCE9D2" stroke="{GLASS}" stroke-width="3"/>'
    s+=f'<rect x="80" y="196" width="240" height="20" fill="#C9CED6" stroke="#8A919C" stroke-width="1.5"/>'
    for x in (110,290):
        s+=f'<rect x="{x-12}" y="40" width="24" height="120" rx="3" fill="#3A3F47"/>'
    s+=tex(200,150,'녹인 $\\ce{Al2O3}$',19,mix=True,fill=MUTED)
    s+=tex(200,246,'(−)극 쪽에 알루미늄이 모인다',18,mix=True,fill=MINUS)
    s+=tex(110,30,'(+)극',19,mix=True,fill=PLUS)+tex(290,30,'(+)극',19,mix=True,fill=PLUS)
    s+=tex(352,206,'$\\ce{Al}$',19,'start',mix=True)
    return s

if __name__=='__main__':
    tpl=open(os.path.join(HERE,'slides.tpl.html'),encoding='utf-8').read()
    c,cc=cover(); F['COVER']=c; F['COVER_C']=cc
    a,ac=apparatus7(); F['APP7']=a; F['APP7_C']=ac
    for k in (1,2,3,4):
        b,bc=proc(k); F[f'P{k}']=b; F[f'P{k}_C']=bc or ''
    F['PART13']=particles13(); m,mc=mini13(); F['MINI13']=m; F['MINI13_C']=mc
    F['E14']=electrons14()
    m,mc=molten(); F['MOLT']=m; F['MOLT_C']=mc
    m,mc=molten('(가)','(나)',pos='right',anim=False,names=False); F['MOLT28']=m; F['MOLT28_C']=mc
    F['ION17']=ions17(); F['SOL18']=solid18(); F['LIQ18']=liquid18(); F['AQ18']=aq18()
    F['NOB20']=noble20(); F['ION21']=ions21()
    F['C221']=card22_1(); F['C222']=card22_2(); F['C223']=card22_3()
    F['H224']=h2_24(); F['H2O25']=h2o25(); F['INT3']=intro3(); F['ANAL5']=anal5(); F['STRAW']=straw(); F['AL20']=al20(); F['ATOM6']=atom6()
    out=tpl
    for k,v in F.items(): out=out.replace(f'@@{k}@@',v)
    import re
    left=re.findall(r'@@[A-Z0-9_]+@@',out)
    if left: print('남은 자리', left)
    open(OUT,'w',encoding='utf-8').write(out)
    print('ok', len(out))
