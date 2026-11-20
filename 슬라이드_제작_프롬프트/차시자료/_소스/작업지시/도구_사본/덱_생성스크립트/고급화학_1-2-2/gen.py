# -*- coding: utf-8 -*-
"""고급화학 1-2-2 그림 생성: gen_head.py(1-2-1 사본: lewis·bracket 도우미, OUT=이 덱) + 이 파일의 그림 → tpl.html의 {{KEY}}를 바꿔 slides.html"""
import math, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert '1-2-2_이온_결합_금속_결합과_전이_금속의_결합/slides.html' in OUT
def wave(x1,y1,x2,y2,col,amp=6,lam=14,w=3):
    dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
    pts=[(x1+ux*t+px*amp*math.sin(2*math.pi*t/lam),y1+uy*t+py*amp*math.sin(2*math.pi*t/lam)) for t in [i*Ln/80 for i in range(81)]]
    return P(pts,col,w)
def atom(x,y,r,el,lab=None,d=False):
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+(',d' if d else '')+'"></g>'
def chg(x,y,r,s): return f'<g data-chg="{f(x)},{f(y)},{r},{s}"></g>'
def step(body,g=None,extra=''):
    return f'<g class="step"'+(f' data-g="{g}"' if g else '')+(f' {extra}' if extra else '')+'>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def harp(cx,y,h,up,col=INK,w=2.6):
    if up: return P([(cx,y+h-6),(cx,y+6),(cx-6,y+14)],col,w,extra='stroke-linecap="round"')
    return P([(cx,y+6),(cx,y+h-6),(cx+6,y+h-14)],col,w,extra='stroke-linecap="round"')
def ebox(x,y,occ,w=30,h=30,hund=True):
    s=[]
    for i,o in enumerate(occ):
        bx=x+i*w
        fill=f'fill="{EQUI}" fill-opacity=".18"' if (hund and len(o)==1) else 'fill="#fff"'
        s.append(f'<rect x="{f(bx)}" y="{f(y)}" width="{w}" height="{h}" {fill} stroke="{INK}" stroke-width="1.5"/>')
        cx=bx+w/2; xs=[cx] if len(o)==1 else [cx-5,cx+5]
        for j,ch in enumerate(o): s.append(harp(xs[j],y,h,ch=='u',w=2.2))
    return ''.join(s)
def dlev(x,y,occ,LW=34,gap=12,new=()):
    """준위선 여러 개(가로로) + 전자 반화살표. occ: 선마다 '', 'u', 'ud'. 가운데 x 기준"""
    n=len(occ); W=n*LW+(n-1)*gap; x0=x-W/2; s=[]
    for i,o in enumerate(occ):
        a=x0+i*(LW+gap); s.append(L(a,y,a+LW,y,INK,2.6))
        cx=a+LW/2; xs=[cx] if len(o)==1 else [cx-6,cx+6]
        for j,ch in enumerate(o):
            s.append(harp(xs[j],y-17,34,ch=='u',FIELD if (i,j) in new else INK))
    return ''.join(s)
def dim(x,y1,y2,lab,col=EQUI,size=20,side='r'):
    s=L(x,y1,x,y2,col,2)+L(x-6,y1,x+6,y1,col,2)+L(x-6,y2,x+6,y2,col,2)
    s+=T(x+(10 if side=='r' else -10),(y1+y2)/2+7,tex=lab,size=size,anchor='start' if side=='r' else 'end',fill=col)
    return s
def cfd(cx,yt,ye,tocc,eocc,dlab=True,new=(),newe=(),labs=True,size=20,dx=None):
    s=[dlev(cx,ye,eocc,new=newe),dlev(cx,yt,tocc,new=new)]
    if labs:
        s.append(T(cx+92,ye+7,tex='e_g',size=size,anchor='start'))
        s.append(T(cx+92,yt+7,tex='t_{2g}',size=size,anchor='start'))
    if dlab: s.append(dim(cx-(dx if dx else 96),ye,yt,'\\Delta_\\mathrm{o}',side='l'))
    return ''.join(s)
def band(x,y,w,h,filled,lab=None,lsize=19,dots=True):
    if filled:
        s=f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="4" fill="{MINUS}" fill-opacity=".30" stroke="{MINUS}" stroke-width="1.5"/>'
        if dots:
            for i in range(int(w//22)):
                for j in range(max(1,int(h//24))):
                    s+=f'<circle cx="{f(x+11+i*22)}" cy="{f(y+12+j*24)}" r="3.6" fill="{MINUS}"/>'
    else:
        s=f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="4" fill="#F4F6F8" stroke="{MUTED}" stroke-width="1.5"/>'
    if lab: s+=T(x+w/2,y+h/2+7,mix=lab,size=lsize)
    return s

# ═══ S1 표지
def cover():
    s=['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    # NaCl 3D 조각
    g=[]; ox,oy,a=270,150,58
    pts=[]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                X=ox+(i-1)*a-(k-1)*a*0.45; Y=oy+(j-1)*a+(k-1)*a*0.32
                pts.append((-k,j,i,X,Y,(i+j+k)%2==0))
    for (i,j,k) in [(0,0,0)]: pass
    # 격자선
    for p in pts:
        _,j,i,X,Y,_n=p
    pts.sort(key=lambda t:(t[0],t[2]))
    for p in pts:
        _,_,_,X,Y,na=p
        g.append(atom(X,Y,11 if na else 19,'Na' if na else 'Cl','-'))
    s.append(an('pop',g,o=f'{ox},{oy}',dur='.8',delay='.2'))
    # 금속
    g=[f'<rect x="60" y="300" width="200" height="150" rx="18" fill="{MINUS}" fill-opacity=".12"/>']
    for i in range(3):
        for j in range(3): g.append(chg(100+i*60,330+j*45,15,'+'))
    e=[]
    for (x,y) in ((130,350),(190,395),(75,410),(160,440),(245,330),(220,420),(100,370)):
        e.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{MINUS}"/>')
    g.append(f'<g data-anim="move" data-from="10,-6" data-rep="alt" data-dur="1.6">{"".join(e)}</g>')
    s.append(''.join(g))
    s.append(T(160,480,mix='금속 결합',size=20,weight=700))
    # 착이온
    g=[]; cx,cy=405,375
    g.append(f'<circle cx="{cx}" cy="{cy}" r="88" fill="#8E4FC2" fill-opacity=".14"/>')
    V=[(0,-62),(0,62),(-62,0),(62,0),(-30,22),(30,-22)]
    for vx,vy in V: g.append(L(cx,cy,cx+vx,cy+vy,BOND,6,extra='stroke-linecap="round"'))
    for vx,vy in V: g.append(atom(cx+vx,cy+vy,15,'O','-'))
    g.append(atom(cx,cy,24,'X','\\mathrm{M}'))
    s.append(an('pop',g,o=f'{cx},{cy}',dur='.7',delay='.9'))
    s.append(T(405,490,mix='착이온',size=20,weight=700))
    s.append(T(270,262,mix='이온 결정',size=20,weight=700))
    return svg('0 0 540 540',540,'위: 나트륨 이온과 염화 이온이 번갈아 쌓인 이온 결정 조각, 왼쪽 아래: 금속 양이온과 자유 전자, 오른쪽 아래: 중심 금속 둘레에 리간드 여섯 개가 결합한 착이온',s,cls='cover-fig',extra='data-audit="skip"')
FIG['COVER']=cover()

# ═══ S3 생각 열기: 소금과 구리
def hammer(x,y,ang):
    return (f'<g data-anim="rot" data-from="-35" data-o="{x+70},{y+70}" data-dur=".7" data-delay=".3" data-ease="in">'
            f'<g transform="rotate({ang} {x+70} {y+70})"><rect x="{x+64}" y="{y-10}" width="12" height="86" rx="4" fill="#B07A45" stroke="{INK}" stroke-width="1.5"/>'
            f'<rect x="{x+40}" y="{y-34}" width="60" height="28" rx="5" fill="#8C99A6" stroke="{INK}" stroke-width="1.5"/></g></g>')
def openfig():
    s=[]
    # (가) 소금
    x=20
    s.append(T(x,24,mix='(가) 소금(염화 나트륨) 결정',size=20,anchor='start',weight=700))
    s.append(P([(x+40,170),(x+120,170),(x+150,145),(x+70,145)],INK,1.6,fill='#F4F6F8',close=True))
    s.append(P([(x+40,170),(x+120,170),(x+120,230),(x+40,230)],INK,1.6,fill='#FFFFFF',close=True))
    s.append(P([(x+120,170),(x+150,145),(x+150,205),(x+120,230)],INK,1.6,fill='#E6EBF0',close=True))
    s.append(hammer(x+30,60,-20))
    s.append(A(x+180,190,x+230,190,'ink',3))
    sh=[[(0,0),(26,-6),(30,18),(6,22)],[(0,0),(22,4),(16,26),(-4,18)],[(0,0),(30,0),(24,20)],[(0,0),(18,-10),(28,10),(10,18)],[(0,0),(14,2),(10,16)]]
    for k,(dx,dy) in enumerate([(250,165),(290,185),(262,205),(305,150),(325,205)]):
        s.append(P([(x+dx+a,dy+b) for a,b in sh[k]],INK,1.5,fill='#F4F6F8',close=True))
    s.append(T(x+290,255,mix='조각으로 부서진다',size=19))
    # (나) 구리
    x=380
    s.append(T(x,24,mix='(나) 구리 덩어리',size=20,anchor='start',weight=700))
    s.append(f'<rect x="{x+40}" y="185" width="90" height="45" rx="6" fill="#C8803A" stroke="{INK}" stroke-width="1.5"/>')
    s.append(hammer(x+20,80,-20))
    s.append(A(x+170,205,x+220,205,'ink',3))
    s.append(f'<rect x="{x+230}" y="212" width="150" height="18" rx="5" fill="#C8803A" stroke="{INK}" stroke-width="1.5"/>')
    s.append(T(x+305,255,mix='얇게 펴진다',size=19))
    return svg('0 0 780 268',780,'소금 결정을 망치로 치면 여러 조각으로 부서지고, 구리 덩어리를 망치로 치면 얇게 펴진다',s)
FIG['OPEN']=openfig()

# ═══ S4 퍼센트 이온성 그래프
def ionpct():
    s=[]; X0,Y0,W,H=70,350,440,300
    X=lambda v:X0+v/4*W; Y=lambda p:Y0-p/100*H
    for v in range(5):
        s.append(L(X(v),Y0,X(v),Y0+6,INK,1.5)); s.append(T(X(v),Y0+26,tex=str(v),size=19))
    for p in (0,25,50,75,100):
        s.append(L(X0-6,Y(p),X0,Y(p),INK,1.5)); s.append(T(X0-10,Y(p)+7,tex=str(p),size=19,anchor='end'))
        if p: s.append(L(X0,Y(p),X0+W,Y(p),'#E6EBF0',1))
    s.append(A(X0,Y0,X0+W+16,Y0,'ink',2)); s.append(A(X0,Y0,X0,Y0-H-20,'ink',2))
    s.append(T(X0+W/2,Y0+52,mix='전기음성도 차이, $\\Delta\\chi$',size=20))
    s.append(T(X0+8,Y0-H-6,mix='이온성 (%)',size=20,anchor='start'))
    cur=[]
    for i in range(0,81):
        v=i*0.045; p=100/(1+math.exp(-2.3*(v-1.75)))
        cur.append((X(v),Y(p)))
    s.append(an('draw',P(cur,PLUS,3),dur='1.4',delay='.3'))
    D={'H':2.20,'Li':0.98,'K':0.82,'Cs':0.79,'F':3.98,'Cl':3.16,'Br':2.96,'I':2.66}
    pts=[('HI','H','I',5,'r'),('HBr','H','Br',11,'r'),('HCl','H','Cl',18,'r'),('HF','H','F',43,'r'),('LiI','Li','I',59,'l'),('LiBr','Li','Br',63,'l'),
         ('KI','K','I',73,'l'),('LiCl','Li','Cl',74,'r'),('KBr','K','Br',78,'u'),('CsCl','Cs','Cl',70,'d'),('KCl','K','Cl',83,'u'),('LiF','Li','F',96,'u'),('KF','K','F',88,'r'),('CsF','Cs','F',72,'d')]
    for nm,a,b,p,pos in pts:
        v=abs(D[a]-D[b]); x,y=X(v),Y(p)
        col=MINUS if a!='H' else FIELD
        s.append(C(x,y,5.5,col,2,fill='#fff'))
        off={'HI':(12,10),'HBr':(12,16),'HCl':(-12,-4),'HF':(12,6),'LiI':(-12,4),'KCl':(-10,-10),'LiF':(-10,-8),'CsF':(10,22)}
        if nm in off:
            dx,dy=off[nm]; s.append(T(x+dx,y+dy,tex='\\mathrm{'+nm+'}',size=19,anchor='start' if dx>0 else 'end',fill=col,halo=True))
    s.append(C(X0+250,Y0-60,5.5,FIELD,2,fill='#fff')); s.append(T(X0+262,Y0-53,mix='수소 할로젠화물',size=19,anchor='start',fill=FIELD))
    s.append(C(X0+250,Y0-30,5.5,MINUS,2,fill='#fff')); s.append(T(X0+262,Y0-23,mix='알칼리 금속 할로젠화물',size=19,anchor='start',fill=MINUS))
    return svg('0 0 540 420',540,'전기음성도 차이가 커질수록 결합의 이온성이 S자 모양으로 커진다. 수소 할로젠화물은 아래쪽, 알칼리 금속 할로젠화물은 위쪽에 있다',s)
FIG['IONPCT']=ionpct()

# ═══ S5 CO2 쌍극자
def dip(x1,x2,y,col=INK,w=3):
    # x1 → x2 화살표 + 꼬리 막대(D24)
    t=x1+(x2-x1)*0.15
    return A(x1,y,x2,y,'ink',w)+L(t,y-7,t,y+7,INK,w)
def co2dip():
    s=[]; y=110; xs=[110,250,390]
    for k in (-1,1): s.append(L(xs[0]+6,y+5*k,xs[2]-6,y+5*k,BOND,6,extra='stroke-linecap="round"'))
    s.append(atom(xs[0],y,26,'O')); s.append(atom(xs[1],y,26,'C')); s.append(atom(xs[2],y,26,'O'))
    s.append(T(xs[0],y-40,tex='\\delta^-',size=22,fill=MINUS)); s.append(T(xs[1],y-40,tex='\\delta^+',size=22,fill=PLUS)); s.append(T(xs[2],y-40,tex='\\delta^-',size=22,fill=MINUS))
    s.append(an('fade',[dip(230,130,y+58),dip(270,370,y+58)],dur='.8',delay='.4'))
    s.append(step([T(250,y+100,mix='두 쌍극자 모멘트가 상쇄 → 합 = 0',size=20,fill=PLUS,weight=700)],g='c1'))
    return svg('0 0 500 230',500,'직선형 이산화 탄소: 가운데 C는 부분 양전하, 양쪽 O는 부분 음전하, 두 결합 쌍극자 화살표가 반대 방향이라 합이 0',s)
FIG['CO2DIP']=co2dip()

# ═══ S6 전자 이동
def etrans():
    s=[]; y=70; S=40
    s.append(lewis([A_('Na',70,y,rad=['r'],oct=None)],[],S=S,check=False))
    s.append(T(150,y+12,tex='+',size=32))
    s.append(lewis([A_('Cl',230,y,lp=['u','r','d'],rad=['l'],oct=None)],[],S=S,check=False))
    # 전자 이동 굽은 화살표 (Na 점 → Cl 빈자리)
    s.append(f'<path d="M 104 {y-12} Q 150 {y-62} 196 {y-12}" fill="none" stroke="{MINUS}" stroke-width="2.6"/>')
    s.append(P([(186,y-24),(197,y-11),(200,y-27)],MINUS,2.6,extra='stroke-linecap="round"'))
    s.append(T(150,y-50,tex='e^-',size=20,fill=MINUS))
    s.append(A(320,y,390,y,'ink',3))
    g=[T(470,y+14,tex='\\mathrm{Na}^{+}',size=S,fill=PLUS)]
    g.append(lewis([A_('Cl',640,y,lp=['u','r','d','l'],oct=None)],[],S=S,check=False,elcol=MINUS))
    g.append(bracket(598,y-36,684,y+36,'-',24))
    s.append(an('fade',g,dur='.8',delay='.8'))
    s.append(T(70,y+66,mix='금속 원자',size=19,fill=MUTED)); s.append(T(230,y+66,mix='비금속 원자',size=19,fill=MUTED))
    s.append(T(470,y+66,mix='양이온 (Ne 배치)',size=19,fill=PLUS)); s.append(T(640,y+66,mix='음이온 (Ar 배치)',size=19,fill=MINUS))
    return svg('0 0 740 150',740,'나트륨 원자의 원자가 전자 하나가 염소 원자로 옮겨 가 나트륨 이온과 염화 이온이 된다',s)
FIG['ETRANS']=etrans()

# ═══ S7 NaCl 결정
def nacl(cx=190,cy=180,a=92,rna=13,rcl=22,lab=True):
    s=[]; pts=[]
    def pr(i,j,k): return cx+(i-1)*a-(k-1)*a*0.42, cy-(j-1)*a+(k-1)*a*0.30
    for (i1,j1,k1,i2,j2,k2) in [(0,0,0,2,0,0),(0,2,0,2,2,0),(0,0,2,2,0,2),(0,2,2,2,2,2),(0,0,0,0,2,0),(2,0,0,2,2,0),(0,0,2,0,2,2),(2,0,2,2,2,2),(0,0,0,0,0,2),(2,0,0,2,0,2),(0,2,0,0,2,2),(2,2,0,2,2,2)]:
        x1,y1=pr(i1,j1,k1); x2,y2=pr(i2,j2,k2); s.append(L(x1,y1,x2,y2,MUTED,1.4,dash='4 4'))
    for k in (2,1,0):
        for j in range(3):
            for i in range(3):
                x,y=pr(i,j,k); na=(i+j+k)%2==1
                pts.append(atom(x,y,rna if na else rcl,'Na' if na else 'Cl','-'))
    s.append(an('pop',pts,o=f'{cx},{cy}',dur='.8',delay='.2'))
    if lab:
        s.append(atom(110,372,rna,'Na','-')); s.append(T(130,379,tex='\\ce{Na+}',size=20,anchor='start'))
        s.append(atom(230,372,rcl,'Cl','-')); s.append(T(260,379,tex='\\ce{Cl-}',size=20,anchor='start'))
    return s
FIG['NACL']=svg('0 0 400 400',400,'염화 나트륨 결정: 나트륨 이온과 염화 이온이 세 방향으로 번갈아 쌓여 있다',nacl())

# ═══ S9 본-하버 엔탈피 도표
def bhdiag():
    s=[]; Y=lambda E:40+(720-E)*0.3106
    s.append(A(40,470,40,20,'ink',2)); s.append(T(52,30,mix='$H$ (kJ)',size=19,anchor='start'))
    lv=[(0,120,300),(109,120,300),(604,120,340),(681,300,520),(353,330,520),(-570,120,520)]
    for E,x1,x2 in lv: s.append(L(x1,Y(E),x2,Y(E),INK,2.6))
    s.append(T(308,Y(0)+7,tex='\\ce{Na(s) + 1/2F2(g)}',size=19,anchor='start'))
    s.append(T(308,Y(109)+7,tex='\\ce{Na(g) + 1/2F2(g)}',size=19,anchor='start'))
    s.append(T(372,Y(604)+9,tex='\\ce{Na+(g) + 1/2F2(g)}',size=19,anchor='start'))
    s.append(T(420,Y(681)-10,tex='\\ce{Na+(g) + F(g)}',size=19))
    s.append(T(425,Y(353)+26,tex='\\ce{Na+(g) + F-(g)}',size=19))
    s.append(T(528,Y(-570)+7,tex='\\ce{NaF(s)}',size=19,anchor='start'))
    def arr(x,E1,E2,txt,g,w=3,lx=None,ly=None):
        y1,y2=Y(E1),Y(E2)
        return step([A(x,y1,x,y2,'ink',w),T(lx if lx else x+10,ly if ly else (y1+y2)/2+7,mix=txt,size=19,anchor='start',weight=700 if w>3 else None)],g=g)
    s.append(arr(140,0,109,'109 승화','h1'))
    s.append(arr(140,109,604,'495||이온화 에너지','h2'))
    s.append(arr(320,604,681,'77','h3',lx=328,ly=Y(640)+12))
    s.append(arr(370,681,353,'−328||전자 친화도','h4'))
    s.append(arr(510,353,-570,'−923||격자||에너지','h5',w=4))
    s.append(step([A(90,Y(0),90,Y(-570),'field',3,d=True),T(100,Y(-290)+7,mix='−570||전체 에너지 변화',size=19,anchor='start',fill=FIELD,weight=700)],g='h6'))
    return svg('0 0 640 470',640,'NaF 생성의 엔탈피 도표: 승화 109, 이온화 495, 해리 77만큼 올라가고, 전자 친화도 328, 격자 에너지 923만큼 내려가 전체 −570 kJ/mol',s)
FIG['BHDIAG']=bhdiag()

# ═══ S10 이온화 막대
def ionbar():
    s=[]; k=0.2; y0=130; Y=lambda E:y0-E*k
    s.append(L(30,y0,530,y0,INK,2)); s.append(T(34,y0-8,tex='0',size=19,anchor='start'))
    def bar(x,E,lab,val,g=None,fill='#E6EBF0',bold=False):
        y=Y(E); top,h=min(y,y0),abs(y-y0)
        b=[f'<rect x="{x}" y="{f(top)}" width="90" height="{f(h)}" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>',
           T(x+45,(top-10) if E>0 else (top+h+26),mix=val,size=20,weight=700),T(x+45,(y0+26) if E>0 else (y0-10),mix=lab,size=19)]
        return step(b,g=g) if g else ''.join(b)
    s.append(bar(70,495,'이온화','+495'))
    s.append(bar(190,-328,'전자 친화도','−328'))
    s.append(bar(310,167,'합','+167','b1',fill='#FDE2E4'))
    s.append(bar(430,-923,'격자 에너지','−923','b2',fill='#E3EEFB'))
    return svg('0 0 560 362',560,'막대: 이온화 +495, 전자 친화도 −328, 둘의 합 +167(흡열), 격자 에너지 −923(큰 발열)',s)
FIG['IONBAR']=ionbar()

# ═══ S11 마델룽: 결정의 한 층
def madel():
    s=[]; cx,cy,a=170,130,86
    for i in (-1,0,1):
        for j in (-1,0,1):
            if (i,j)==(0,0): continue
            x,y=cx+i*a,cy+j*a
            if (i+j)%2: s.append(L(cx,cy,x,y,FIELD,3))
            else: s.append(L(cx,cy,x,y,PLUS,2.4,dash='6 5'))
    for i in (-1,0,1):
        for j in (-1,0,1):
            x,y=cx+i*a,cy+j*a; na=(i+j)%2==0
            s.append(atom(x,y,26 if na else 32,'Na' if na else 'Cl','\\mathrm{Na}^{+}' if na else '\\mathrm{Cl}^{-}'))
    s.append(T(cx,cy+a+62,mix='실선 인력: 이웃 음이온 (입체 6개)',size=19,fill=FIELD))
    s.append(T(cx,cy+a+88,mix='점선 반발: 다음 양이온 (입체 12개)',size=19,fill=PLUS))
    return svg('0 0 340 320',340,'결정의 한 층: 가운데 나트륨 이온은 이웃한 염화 이온과 인력(실선), 대각선의 나트륨 이온과 반발(점선)',s)
FIG['MADEL']=madel()

# ═══ S12 격자 에너지 그래프
def latg():
    s=[]; X0,Y0,W,H=80,330,360,290
    X=lambda v:X0+v/20*W; Y=lambda E:Y0-E/4000*H
    for v in (0,5,10,15,20):
        s.append(L(X(v),Y0,X(v),Y0+6,INK,1.5)); s.append(T(X(v),Y0+26,tex=str(v),size=19))
    for E in (0,1000,2000,3000,4000):
        s.append(L(X0-6,Y(E),X0,Y(E),INK,1.5)); s.append(T(X0-10,Y(E)+7,tex=str(E),size=19,anchor='end'))
    s.append(A(X0,Y0,X0+W+16,Y0,'ink',2)); s.append(A(X0,Y0,X0,Y0-H-18,'ink',2))
    s.append(T(X0+W/2,Y0+68,mix='$\\dfrac{Z^+Z^-}{r_0}$ ($10^{-3}\\ \\text{pm}^{-1}$)',size=19))
    s.append(T(X0+8,Y0-H-4,mix='격자 에너지 (kJ/mol)',size=19,anchor='start'))
    s.append(L(X(0),Y(0),X(19.5),Y(19.5*205),MUTED,1.6,dash='6 5'))
    d=[('NaI',3.10,704),('NaBr',3.36,747),('NaCl',3.55,787),('NaF',4.33,923),('MgO',19.05,3791)]
    g=[]
    for nm,v,E in d: g.append(C(X(v),Y(E),6,PLUS,2.2,fill='#fff'))
    s.append(''.join(g))
    s.append(T(X(19.05)-12,Y(3791)+6,tex='\\mathrm{MgO}',size=19,anchor='end'))
    s.append(T(X(4.6)+8,Y(1150),mix='NaF, NaCl,||NaBr, NaI',size=19,anchor='start'))
    return svg('0 0 470 420',450,'격자 에너지는 전하의 곱을 이온 사이 거리로 나눈 값에 거의 비례한다. 나트륨 할로젠화물은 아래 왼쪽에 모이고 산화 마그네슘은 오른쪽 위에 있다',s)
FIG['LATG']=latg()

# ═══ S13 에너지 띠 형성
def bands():
    s=[]; cy=210
    s.append(A(36,350,36,60,'ink',2.4)); s.append(T(50,72,tex='E',size=22,anchor='start'))
    s.append(T(285,24,mix='상호 작용하는 원자 오비탈의 수',size=19))
    cols=[(110,2,44),(200,4,70),(290,16,92)]
    for k,(x,n,sp) in enumerate(cols):
        g=[]
        for i in range(n):
            y=cy-sp+ (2*sp)*(i/(n-1)) if n>1 else cy
            gapy=8 if n>2 else 0
            y=y-gapy if i<n/2 else y+gapy
            g.append(L(x-28,y,x+28,y,INK,2.4 if n<16 else 1.8))
        g.append(T(x,58,tex=str(n),size=19))
        s.append(an('fade',g,dur='.6',delay=f'{.2+.4*k:.1f}'))
    g=[f'<rect x="372" y="104" width="70" height="98" fill="#F4F6F8" stroke="{MUTED}" stroke-width="1.5"/>',
       f'<rect x="372" y="218" width="70" height="98" fill="{MINUS}" fill-opacity=".30" stroke="{MINUS}" stroke-width="1.5"/>',
       T(407,58,tex='6.02\\times10^{23}',size=19)]
    s.append(an('fade',g,dur='.6',delay='1.4'))
    s.append(T(452,146,mix='반결합성 띠||(전도띠)',size=19,anchor='start'))
    s.append(T(452,260,mix='결합성 띠||(원자가띠)',size=19,anchor='start'))
    s.append(T(110,345,mix='준위 2개',size=19,fill=MUTED)); s.append(T(290,345,mix='준위가 촘촘',size=19,fill=MUTED)); s.append(T(407,345,mix='연속된 띠',size=19,fill=MUTED))
    return svg('0 0 580 360',580,'상호 작용하는 원자 오비탈 수가 2, 4, 16개로 늘수록 분자 오비탈 준위가 촘촘해지고, 6.02×10^23개이면 아래 결합성 띠와 위 반결합성 띠가 연속된 띠를 이룬다',s)
FIG['BANDS']=bands()

# ═══ S14 띠와 전도성
def bandcond():
    s=[]
    s.append(A(36,330,36,40,'ink',2.4)); s.append(T(50,52,tex='E',size=22,anchor='start'))
    s.append(band(80,70,300,100,False)); s.append(band(80,180,300,120,True))
    s.append(T(392,124,mix='전도띠',size=20,anchor='start')); s.append(T(392,248,mix='원자가띠',size=20,anchor='start'))
    s.append(A(150,190,150,150,'ink',2.6)); s.append(T(392,182,mix='작은 에너지로 들뜸',size=19,anchor='start'))
    g=[f'<circle cx="{x}" cy="134" r="5" fill="{MINUS}"/>' for x in (130,210,290)]
    g.append(A(120,112,330,112,'minus',2.4))
    s.append(f'<g data-anim="move" data-from="-50,0" data-dur="1.6" data-rep="loop" data-ease="lin">{"".join(g)}</g>')
    s.append(T(230,94,mix='자유롭게 이동하는 전자',size=19,fill=MINUS))
    return svg('0 0 580 330',520,'금속의 에너지 띠: 전자로 채워진 원자가띠 바로 위에 빈 전도띠가 있고, 작은 에너지로 들뜬 전자가 전도띠에서 자유롭게 이동한다',s)
FIG['BANDCOND']=bandcond()

# ═══ S15 금속과 이온 결정에 힘을 가할 때
def malle():
    s=[]; a=40
    def metal(x0,y0,shift=0,anim=False):
        g=[f'<rect x="{x0-24}" y="{y0-24}" width="{5*a+8}" height="{3*a+8}" rx="14" fill="{MINUS}" fill-opacity=".12"/>']
        top=[chg(x0+i*a+shift,y0,14,'+') for i in range(5)]
        rest=[chg(x0+i*a,y0+j*a,14,'+') for j in (1,2) for i in range(5)]
        e=''.join(f'<circle cx="{x0+dx}" cy="{y0+dy}" r="3.6" fill="{MINUS}"/>' for dx,dy in ((20,20),(100,20),(60,60),(140,62),(-2,40),(170,30),(30,85),(120,96)))
        tg=''.join(top)
        if anim: tg=f'<g data-anim="move" data-from="{-shift},0" data-dur="1.2" data-delay=".5">{tg}</g>'
        return ''.join(rest)+tg+e
    def ionic(x0,y0,shift=0,anim=False,rep=False):
        top=[chg(x0+i*a+shift,y0,15,'+' if i%2==0 else '-') for i in range(5)]
        rest=[chg(x0+i*a,y0+j*a,15,'+' if (i+j)%2==0 else '-') for j in (1,2) for i in range(5)]
        tg=''.join(top)
        if anim: tg=f'<g data-anim="move" data-from="{-shift},0" data-dur="1.2" data-delay=".5">{tg}</g>'
        out=''.join(rest)+tg
        if rep:
            out+=step([P([(x0-22,y0+20),(x0+5*a-10,y0+22)],PLUS,2.4,dash='7 5')]+[T(x0+80+a,y0-26,mix='같은 전하끼리 반발 → 쪼개짐',size=19,fill=PLUS,weight=700)],g='m1')
        return out
    s.append(T(20,24,mix='(가) 금속',size=20,anchor='start',weight=700))
    s.append(metal(40,70)); s.append(A(250,110,290,110,'ink',3)); s.append(T(270,94,mix='힘',size=19))
    s.append(metal(320,70,shift=a,anim=True))
    s.append(T(390,200,mix='층이 밀려도 자유 전자가 결합을 유지',size=19,fill=MINUS))
    X=540
    s.append(T(X+10,24,mix='(나) 이온 결정',size=20,anchor='start',weight=700))
    s.append(ionic(X+30,70)); s.append(A(X+230,110,X+270,110,'ink',3)); s.append(T(X+250,94,mix='힘',size=19))
    s.append(ionic(X+300,70,shift=a,anim=True,rep=True))
    return svg('0 0 1080 216',1080,'금속: 양이온 층이 한 칸 밀려도 자유 전자 속에서 결합이 유지된다. 이온 결정: 층이 한 칸 밀리면 같은 전하의 이온이 위아래로 마주쳐 반발하여 쪼개진다',s)
FIG['MALLE']=malle()

# ═══ S16 도체·반도체·부도체
def bands3():
    s=[]
    s.append(A(26,330,26,30,'ink',2.4)); s.append(T(38,44,tex='E',size=22,anchor='start'))
    cols=[(60,'도체(금속)',172,178),(250,'반도체',140,190),(440,'부도체(유리)',100,250)]
    for k,(x,nm,ub,lt) in enumerate(cols):
        g=[band(x,60,140,ub-60,False),band(x,lt,140,300-lt,True,dots=False),T(x+70,330,mix=nm,size=20,weight=700)]
        if lt-ub>20: g.append(dim(x+160,ub,lt,'',size=19))
        s.append(''.join(g))
    s.append(T(130,124,mix='전도띠',size=19)); s.append(T(130,246,mix='원자가띠',size=19))
    s.append(T(608,182,mix='큰 간격',size=19,anchor='start',fill=EQUI)); s.append(T(418,160,mix='작은||간격',size=19,anchor='start',fill=EQUI))
    return svg('0 0 680 350',680,'세 가지 에너지 띠: 도체는 두 띠가 거의 붙어 있고, 반도체는 작은 간격, 부도체는 큰 간격으로 떨어져 있다',s)
FIG['BANDS3']=bands3()

# ═══ S17 n형·p형
def nptype():
    s=[]
    for k,(x,nm) in enumerate([(30,'n형 반도체'),(310,'p형 반도체')]):
        s.append(T(x+125,24,mix=nm,size=20,weight=700))
        s.append(band(x,40,250,70,False)); s.append(band(x,180,250,70,True))
        s.append(T(x+125,82,mix='전도띠',size=19)); s.append(T(x+125,236,mix='원자가띠',size=19,fill=INK,halo=True))
        if k==0:
            s.append(L(x+20,128,x+230,128,MUTED,2,dash='6 5'))
            s.append('<g data-anim="move" data-from="0,22" data-dur="1" data-delay=".6">'+''.join(f'<circle cx="{xx}" cy="106" r="5" fill="{MINUS}"/>' for xx in (x+60,x+125,x+190))+'</g>')
            for xx in (x+60,x+125,x+190): s.append(A(xx,124,xx,112,'minus',2))
            s.append(T(x+125,152,mix='여분 전자 → 전도띠로 들뜸',size=19,fill=MINUS))
        else:
            s.append(L(x+20,162,x+230,162,MUTED,2,dash='6 5'))
            s.append('<g data-anim="move" data-from="0,-22" data-dur="1" data-delay=".6">'+''.join(f'<circle cx="{xx}" cy="194" r="7" fill="#fff" stroke="{PLUS}" stroke-width="2.4"/>' for xx in (x+60,x+125,x+190))+'</g>')
            s.append(T(x+125,150,mix='원자가띠에 생긴 구멍',size=19,fill=PLUS))
    # 격자 조각
    for k,(cx,el,lab) in enumerate([(155,'P','여분 전자'),(435,'B','구멍')]):
        cy=340
        for dx,dy in ((-70,0),(70,0),(0,-56),(0,56)):
            s.append(L(cx,cy,cx+dx,cy+dy,BOND,6,extra='stroke-linecap="round"'))
        for dx,dy in ((-70,0),(70,0),(0,-56),(0,56)): s.append(atom(cx+dx,cy+dy,20,'Si'))
        s.append(atom(cx,cy,22,el))
        if el=='P':
            s.append(f'<circle cx="{cx+34}" cy="{cy-26}" r="5" fill="{MINUS}"/>'); s.append(T(cx+46,cy-34,mix=lab,size=19,anchor='start',fill=MINUS))
        else:
            s.append(C(cx+35,cy+18,7,PLUS,2.4,fill='#fff')); s.append(T(cx+48,cy+48,mix=lab,size=19,anchor='start',fill=PLUS))
    return svg('0 0 590 410',590,'n형: 전도띠 바로 아래 여분 전자가 전도띠로 들뜬다(규소 사이 인). p형: 원자가띠에 양전하의 구멍이 생긴다(규소 사이 붕소)',s)
FIG['NPTYPE']=nptype()

# ═══ S19 보석과 안료
def gems():
    s=[]
    def gem(cx,cy,col):
        pts=[(cx-50,cy-20),(cx-28,cy-44),(cx+28,cy-44),(cx+50,cy-20),(cx,cy+50)]
        g=P(pts,INK,1.6,fill=col,close=True)
        g+=P([(cx-50,cy-20),(cx+50,cy-20)],'#fff',1.4,extra='stroke-opacity=".7"')
        g+=P([(cx-28,cy-44),(cx-14,cy-20),(cx,cy+50),(cx+14,cy-20),(cx+28,cy-44)],'#fff',1.2,extra='stroke-opacity=".6"')
        return g
    s.append(gem(90,110,'#C8102E')); s.append(T(90,200,mix='루비',size=20,weight=700))
    s.append(gem(250,110,'#1F4FB8')); s.append(T(250,200,mix='사파이어',size=20,weight=700))
    s.append(f'<rect x="360" y="62" width="110" height="100" rx="12" fill="#0B2E59" stroke="{INK}" stroke-width="1.5"/>')
    s.append(P([(380,150),(420,92),(445,120)],'#2B5B95',4,extra='stroke-linecap="round"'))
    s.append(T(415,200,mix='프러시안블루',size=20,weight=700))
    s.append(T(250,246,mix='색의 원인: 미량의 전이 금속 이온',size=19,fill=MUTED))
    return svg('0 0 500 260',500,'붉은 루비, 푸른 사파이어, 짙은 파란색 안료 프러시안블루',s)
FIG['GEMS']=gems()

# ═══ S20 표 Ⅰ-4
def tmtab():
    s=[]; rows=[(21,'Sc','ud','u    ','4s^2 3d^1',1),(22,'Ti','ud','uu   ','4s^2 3d^2',2),(23,'V','ud','uuu  ','4s^2 3d^3',3),(24,'Cr','u','uuuuu','4s^1 3d^5',6),
        (25,'Mn','ud','uuuuu','4s^2 3d^5',5),(26,'Fe','ud','Duuuu','4s^2 3d^6',4),(27,'Co','ud','DDuuu','4s^2 3d^7',3),(28,'Ni','ud','DDDuu','4s^2 3d^8',2),(29,'Cu','u','DDDDD','4s^1 3d^{10}',1),(30,'Zn','ud','DDDDD','4s^2 3d^{10}',0)]
    y0=50; rh=40
    hdr=[(30,'번호'),(88,'원소'),(150,'4s'),(254,'3d'),(440,'전체 전자 배치'),(590,'홀전자')]
    for x,t in hdr: s.append(T(x,30,mix=t if t not in ('4s','3d') else None,tex=t if t in ('4s','3d') else None,size=19,weight=700) if t not in ('4s','3d') else T(x,30,tex=t,size=19))
    s.append(L(4,40,620,40,INK,1.5))
    for r,(z,el,s4,d3,cfg,un) in enumerate(rows):
        y=y0+r*rh
        if el in ('Cr','Cu'): s.append(f'<rect x="4" y="{y-4}" width="616" height="{rh}" fill="#FFF1B8"/>')
        s.append(T(30,y+24,tex=str(z),size=19)); s.append(T(88,y+24,tex='\\mathrm{'+el+'}',size=20))
        s.append(ebox(135,y,[s4],30,30))
        occ=[{'u':'u','D':'ud',' ':''}[c] for c in d3]
        s.append(ebox(179,y,occ,30,30))
        s.append(T(440,y+24,tex='[\\mathrm{Ar}]\\,'+cfg,size=19)); s.append(T(590,y+24,tex=str(un),size=20,weight=700 if el in ('Cr','Cu') else None))
    return svg('0 0 630 450',630,'첫 주기 전이 금속 스칸듐부터 아연까지의 4s와 3d 오비탈 전자 배치와 홀전자 수. 크로뮴과 구리는 4s 전자가 1개',s)
FIG['TMTAB']=tmtab()

# ═══ S21 K4[Fe(CN)6]
OCT=[(0,-1,0),(0,1,0),(-1,0,0),(1,0,0),(0,0,1),(0,0,-1)]
def oproj(v,R): return (v[0]*R - v[2]*R*0.42, v[1]*R + v[2]*R*0.30)
def octa(cx,cy,R,lig,rl=15,center='\\mathrm{Fe}',rc=24,cn=False,lab=None):
    s=[]; order=sorted(range(6),key=lambda i:-OCT[i][2])
    for i in order:
        dx,dy=oproj(OCT[i],R)
        s.append(L(cx,cy,cx+dx,cy+dy,BOND,6,extra='stroke-linecap="round"'))
    back=[i for i in order if OCT[i][2]<0]; front=[i for i in order if OCT[i][2]>=0]
    def lg(i):
        dx,dy=oproj(OCT[i],R); out=''
        if cn:
            ex,ey=oproj(OCT[i],R*1.55)
            out+=L(cx+dx,cy+dy,cx+ex,cy+ey,BOND,6,extra='stroke-linecap="round"')
            out+=atom(cx+ex,cy+ey,rl,'N','-')
        out+=atom(cx+dx,cy+dy,rl,lig,lab if lab else '-')
        return out
    for i in back: s.append(lg(i))
    s.append(atom(cx,cy,rc,'X',center))
    for i in front: s.append(lg(i))
    return ''.join(s)
def fecn():
    s=[octa(170,170,78,'C',rl=14,cn=True)]
    s.append(bracket(30,30,310,312,'4-',24))
    g=[]
    for k,(x,y) in enumerate([(380,70),(380,140),(380,210),(380,280)]):
        g.append(chg(x,y,17,'+')); g.append(T(x+24,y+7,tex='\\ce{K+}',size=19,anchor='start'))
    s.append(an('pop',g,o='390,175',dur='.6',delay='.6'))
    s.append(T(170,350,mix='착이온 $\\ce{[Fe(CN)6]^4-}$',size=19)); s.append(T(395,350,mix='상대 이온',size=19))
    s.append(atom(40,385,12,'C','-')); s.append(T(58,391,tex='\\mathrm{C}',size=19,anchor='start'))
    s.append(atom(110,385,12,'N','-')); s.append(T(128,391,tex='\\mathrm{N}',size=19,anchor='start'))
    s.append(T(170,391,mix='C가 Fe에 배위',size=19,anchor='start',fill=MUTED))
    return svg('0 0 440 405',440,'팔면체 착이온 헥사사이아노철 이온: 가운데 Fe에 CN 여섯 개가 C 쪽으로 결합하고, 바깥에 칼륨 이온 넷이 상대 이온으로 있다',s)
FIG['FECN']=fecn()

# ═══ S22 배위수와 구조
def geom():
    s=[]; W=250
    def ball(cx,cy,vecs,R):
        out=''
        vs=sorted(vecs,key=lambda v:v[2])
        for v in vs:
            dx,dy=oproj(v,R); out+=L(cx,cy,cx+dx,cy+dy,BOND,6,extra='stroke-linecap="round"')
        for v in [v for v in vs if v[2]<0]:
            dx,dy=oproj(v,R); out+=atom(cx+dx,cy+dy,14,'N','-')
        out+=atom(cx,cy,26,'X','\\mathrm{M}')
        for v in [v for v in vs if v[2]>=0]:
            dx,dy=oproj(v,R); out+=atom(cx+dx,cy+dy,14,'N','-')
        return out
    t=1/math.sqrt(3)
    sets=[('선형','2','\\ce{[Ag(NH3)2]+}',[(1,0,0),(-1,0,0)]),
          ('사면체형','4','\\ce{[Zn(NH3)4]^2+}',[(t,-t,t),(-t,-t,-t),(-t,t,t),(t,t,-t)]),
          ('평면사각형','4','\\ce{[Pt(NH3)2Cl2]}',[(1,0,0),(-1,0,0),(0,0,1),(0,0,-1)]),
          ('팔면체형','6','\\ce{[Co(NH3)6]^3+}',OCT)]
    for k,(nm,n,ex,vecs) in enumerate(sets):
        cx=W*k+125
        s.append(an('pop',ball(cx,95,vecs,70),o=f'{cx},95',dur='.6',delay=f'{.2+.3*k:.1f}'))
        s.append(T(cx,196,mix=f'배위수 {n} · {nm}',size=20,weight=700))
        s.append(T(cx,226,tex=ex,size=19))
    return svg('0 0 1000 240',1000,'배위수 2 선형, 배위수 4 사면체형과 평면사각형, 배위수 6 팔면체형의 공-막대 모형',s)
FIG['GEOM']=geom()

# ═══ S23 en, EDTA
def lig():
    s=[]
    # en 고리
    M=(120,190)
    s.append(T(120,28,mix='en (두 자리)',size=20,weight=700))
    pos={'C1':(85,70),'C2':(155,70),'N1':(55,130),'N2':(185,130)}
    s.append(L(105,70,135,70,INK,2.4)); s.append(L(77,82,62,116,INK,2.4)); s.append(L(163,82,178,116,INK,2.4))
    s.append(T(85,78,tex='\\ce{H2C}',size=20,anchor='end')); s.append(T(155,78,tex='\\ce{CH2}',size=20,anchor='start'))
    s.append(T(55,138,tex='\\ce{H2N}',size=20,anchor='end')); s.append(T(185,138,tex='\\ce{NH2}',size=20,anchor='start'))
    for (x,y) in ((40,140),(200,140)): s.append(f'<ellipse cx="{x}" cy="{y}" rx="22" ry="16" fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="1.5"/>')
    s.append(A(46,154,104,182,'ink',2.4)); s.append(A(194,154,136,182,'ink',2.4))
    s.append(atom(120,200,25,'X','\\mathrm{M}'))
    # EDTA 모식
    cx,cy=340,170
    s.append(T(cx,28,mix='EDTA (여러 자리)',size=20,weight=700))
    don=[('N',-46,-58),('N',46,-58),('O',-80,6),('O',80,6),('O',-44,70),('O',44,70)]
    pts=[(cx+dx,cy+dy) for _,dx,dy in don]
    path=f'M {f(pts[2][0])} {f(pts[2][1])} Q {f(cx-100)} {f(cy-50)} {f(pts[0][0])} {f(pts[0][1])} Q {f(cx)} {f(cy-100)} {f(pts[1][0])} {f(pts[1][1])} Q {f(cx+100)} {f(cy-50)} {f(pts[3][0])} {f(pts[3][1])}'
    s.append(f'<path d="{path}" fill="none" stroke="{MUTED}" stroke-width="2.4"/>')
    s.append(f'<path d="M {f(pts[0][0])} {f(pts[0][1])} Q {f(cx-110)} {f(cy+40)} {f(pts[4][0])} {f(pts[4][1])}" fill="none" stroke="{MUTED}" stroke-width="2.4"/>')
    s.append(f'<path d="M {f(pts[1][0])} {f(pts[1][1])} Q {f(cx+110)} {f(cy+40)} {f(pts[5][0])} {f(pts[5][1])}" fill="none" stroke="{MUTED}" stroke-width="2.4"/>')
    for (el,dx,dy) in don: s.append(L(cx,cy,cx+dx*0.72,cy+dy*0.72,EQUI,2.4,dash='5 4'))
    for (el,dx,dy) in don: s.append(atom(cx+dx,cy+dy,19,el))
    s.append(atom(cx,cy,25,'X','\\mathrm{M}'))
    s.append(T(cx,270,mix='N 2개, O 4개가 M을 둘러쌈',size=19,fill=MUTED))
    return svg('0 0 460 290',460,'en은 두 N 원자의 비공유 전자쌍으로 금속 M과 두 군데 결합하고, EDTA는 N 두 개와 O 네 개, 모두 여섯 원자로 M을 둘러싸 결합한다',s)
FIG['LIG']=lig()

# ═══ S24 d 오비탈 방향
def lobe2(cx,cy,ang,L0,sign,W=0.55,lsize=18,lab=True):
    t=math.radians(ang); ux,uy=math.cos(t),-math.sin(t); px,py=-uy,ux; pts=[]
    for i in range(61):
        th=math.radians(-90+3*i); rho=L0*math.cos(th)**2
        a=rho*math.cos(th); b=W*L0*math.cos(th)**2*math.sin(th)
        pts.append((cx+ux*a+px*b,cy+uy*a+py*b))
    col=BF if sign>0 else GRAV
    out=P(pts,col,1.8,fill=col,close=True,extra='fill-opacity=".30"')
    if lab: out+=T(cx+ux*L0*0.55,cy+uy*L0*0.55+lsize*0.36,tex='+' if sign>0 else '-',size=lsize,weight=700)
    return out
def dlobe():
    s=[]
    for k,(cx,nm,angs,cap) in enumerate([(105,'d_{x^2-y^2}',[(0,1),(180,1),(90,-1),(270,-1)],'리간드를 향함'),(315,'d_{xy}',[(45,1),(225,1),(135,-1),(315,-1)],'리간드 사이를 향함')]):
        cy=135
        s.append(L(cx-95,cy,cx+95,cy,MUTED,1.4)); s.append(L(cx,cy+95,cx,cy-95,MUTED,1.4))
        s.append(T(cx+98,cy+20,tex='x',size=19,fill=MUTED)); s.append(T(cx+14,cy-86,tex='y',size=19,fill=MUTED,anchor='start'))
        for a,sg in angs: s.append(lobe2(cx,cy,a,74,sg))
        for dx,dy in ((84,0),(-84,0),(0,84),(0,-84)): s.append(chg(cx+dx,cy+dy,11,'-'))
        s.append(T(cx,262,tex=nm,size=22)); s.append(T(cx,290,mix=cap,size=19,fill=MUTED))
    s.append(chg(30,316,9,'-')); s.append(T(46,322,mix='리간드(음의 점전하)',size=19,anchor='start'))
    return svg('0 0 430 330',430,'위에서 본 두 d 오비탈: dx2-y2의 엽은 x, y축 위 리간드 점전하를 향하고, dxy의 엽은 리간드 사이를 향한다',s)
FIG['DLOBE']=dlobe()
def cfsplit():
    s=[]
    s.append(A(20,210,20,14,'ink',2.4)); s.append(T(32,26,tex='E',size=22,anchor='start'))
    s.append(dlev(140,120,['','','','',''],LW=26,gap=8))
    s.append(T(140,150,mix='금속 이온의 3d',size=19))
    for xx,yy in ((222,120),(222,120)): pass
    s.append(L(222,120,318,46,MUTED,1.4,dash='5 4')); s.append(L(222,120,318,180,MUTED,1.4,dash='5 4'))
    s.append(f'<g data-anim="move" data-from="0,60" data-dur="1" data-delay=".4">{dlev(372,46,["",""])}</g>')
    s.append(f'<g data-anim="move" data-from="0,-50" data-dur="1" data-delay=".4">{dlev(372,180,["","",""])}</g>')
    s.append(T(450,53,tex='e_g',size=21,anchor='start')); s.append(T(450,187,tex='t_{2g}',size=21,anchor='start'))
    s.append(dim(512,46,180,'\\Delta_\\mathrm{o}'))
    return svg('0 0 580 210',580,'팔면체 착물에서 다섯 개의 3d 오비탈이 위의 eg 두 개와 아래의 t2g 세 개로 갈라지고, 그 차이가 Δo이다',s)
FIG['CFSPLIT']=cfsplit()

# ═══ S25 Ti 착이온의 색
def ticol():
    s=[]
    s.append(T(110,24,mix='바닥상태',size=19,weight=700)); s.append(T(400,24,mix='들뜬상태',size=19,weight=700))
    s.append(step([dlev(110,60,['','']),dlev(110,170,['u','','']),T(185,177,tex='t_{2g}',size=19,anchor='start'),T(185,67,tex='e_g',size=19,anchor='start')],g='t1'))
    g=[dlev(400,60,['u','']),dlev(400,170,['','','']),T(475,177,tex='t_{2g}',size=19,anchor='start'),T(475,67,tex='e_g',size=19,anchor='start'),
       wave(215,115,300,115,'#9DBB1E',amp=6,lam=14,w=3),A(300,115,320,115,'#9DBB1E',3),T(262,100,tex='h\\nu',size=20),dim(530,60,170,'\\Delta_\\mathrm{o}')]
    s.append(step(g,g='t2'))
    # 색상환
    cx,cy,R=200,292,62
    cols=['#E53935','#FB8C00','#FDD835','#43A047','#1E88E5','#8E24AA']
    names=['빨강','주황','노랑','초록','파랑','보라']
    w=[]
    for i,c in enumerate(cols):
        a1=math.radians(90-60*i-30); a2=math.radians(90-60*i+30)
        x1,y1=cx+R*math.cos(a1),cy-R*math.sin(a1); x2,y2=cx+R*math.cos(a2),cy-R*math.sin(a2)
        w.append(f'<path d="M {cx} {cy} L {f(x1)} {f(y1)} A {R} {R} 0 0 0 {f(x2)} {f(y2)} Z" fill="{c}" stroke="#fff" stroke-width="2"/>')
    ay=math.radians(90-150); ax_,ay_=cx+(R+4)*math.cos(ay),cy-(R+4)*math.sin(ay)
    w.append(A(ax_+28*math.cos(ay),ay_-28*math.sin(ay),ax_,ay_,'ink',2.4))
    w.append(T(ax_+30*math.cos(ay)+6,ay_-30*math.sin(ay)+18,mix='흡수: 황록색',size=19,anchor='start'))
    w.append(L(cx+(R-10)*math.cos(ay),cy-(R-10)*math.sin(ay),cx-(R-10)*math.cos(ay),cy+(R-10)*math.sin(ay),INK,1.8,dash='5 4'))
    w.append(T(cx-R-8,cy-44,mix='보색: 보라색',size=19,anchor='end'))
    # 비커
    bx=440
    w.append(f'<path d="M {bx-50} 270 L {bx-50} 380 Q {bx-50} 392 {bx-38} 392 L {bx+38} 392 Q {bx+50} 392 {bx+50} 380 L {bx+50} 270" fill="none" stroke="#7E8B98" stroke-width="2.4"/>')
    w.append(f'<rect x="{bx-48}" y="300" width="96" height="90" rx="8" fill="#8E4FC2" fill-opacity=".55"/>')
    w.append(T(bx,258,tex='\\ce{[Ti(H2O)6]^3+}',size=19))
    s.append(step(w,g='t3'))
    return svg('0 0 590 410',560,'바닥상태 t2g에 있던 전자 하나가 황록색 빛의 광자를 흡수해 eg로 들뜬다. 색상환에서 황록색의 반대편인 보라색이 용액의 색이다',s)
FIG['TICOL']=ticol()

# ═══ S26 분광학적 계열
def series():
    s=[f'<defs><linearGradient id="grad-ac122-26" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#16233D" stop-opacity=".85"/><stop offset="1" stop-color="#16233D" stop-opacity=".08"/></linearGradient></defs>']
    s.append('<rect x="40" y="58" width="920" height="16" rx="8" fill="url(#grad-ac122-26)"/>')
    L_=['\\ce{CO},\\ \\ce{CN-}','\\mathrm{en}','\\ce{NH3}','\\ce{H2O}','\\ce{OH-}','\\ce{F-}','\\ce{Cl-}','\\ce{Br-}','\\ce{I-}']
    xs=[95,205,300,395,490,585,680,775,870]
    for i,(x,t) in enumerate(zip(xs,L_)):
        s.append(T(x,40,tex=t,size=21))
        if i<len(xs)-1: s.append(T((x+xs[i+1])/2+(14 if i==0 else 0),40,tex='>',size=21,fill=MUTED))
    s.append(T(40,102,mix='$\\Delta_\\mathrm{o}$ 큼 · 강한 장',weight=700,size=20,anchor='start'))
    s.append(T(960,102,mix='$\\Delta_\\mathrm{o}$ 작음 · 약한 장',weight=700,size=20,anchor='end'))
    return svg('0 0 1000 116',1000,'분광학적 계열: CO, CN− > en > NH3 > H2O > OH− > F− > Cl− > Br− > I−, 왼쪽일수록 Δo가 큰 강한 장',s)
FIG['SERIES']=series()
def d4():
    s=[]
    s.append(step([T(110,22,mix='(가) 강한 장',size=19,weight=700),dlev(110,52,['','']),dlev(110,150,['ud','u','u'],new={(0,1)}),dim(14,52,150,'',size=19),T(110,196,tex='t_{2g}^{4}',size=21),T(205,196,mix='저스핀',size=19,fill=MUTED)],g='s1'))
    s.append(step([T(345,22,mix='(나) 약한 장',size=19,weight=700),dlev(345,96,['u',''],new={(0,0)}),dlev(345,150,['u','u','u']),dim(249,96,150,'',size=19),T(345,196,tex='t_{2g}^{3}e_g^{1}',size=21),T(440,196,mix='고스핀',size=19,fill=MUTED,anchor='start')],g='s2'))
    return svg('0 0 500 210',500,'d4 배치 두 가지: 강한 장에서는 넷째 전자가 t2g에서 짝을 지어 t2g4, 약한 장에서는 eg로 들어가 t2g3 eg1',s)
FIG['D4']=d4()

# ═══ S27 Co(III)
def coiii():
    s=[]
    s.append(T(150,26,tex='\\ce{[Co(NH3)6]^3+}',size=21)); s.append(T(450,26,tex='\\ce{[CoF6]^3-}',size=21))
    s.append(dlev(150,70,['',''])); s.append(dlev(150,240,['ud','ud','ud'])); s.append(dim(54,70,240,'\\Delta_\\mathrm{o}',side='l'))
    s.append(dlev(450,160,['u','u'])); s.append(dlev(450,240,['ud','u','u'])); s.append(dim(354,160,240,'\\Delta_\\mathrm{o}',side='l'))
    for x in (150,450):
        s.append(T(x+92,(70 if x==150 else 160)+7,tex='e_g',size=19,anchor='start')); s.append(T(x+92,247,tex='t_{2g}',size=19,anchor='start'))
    s.append(T(150,290,mix='큰 $\\Delta_\\mathrm{o}$ → 저스핀, 홀전자 0',size=19)); s.append(T(450,290,mix='작은 $\\Delta_\\mathrm{o}$ → 고스핀, 홀전자 4',size=19))
    return svg('0 0 600 305',600,'헥사암민코발트(Ⅲ) 이온은 갈라짐이 커서 t2g에 전자 여섯이 모두 짝을 짓고, 헥사플루오로코발트(Ⅲ) 이온은 갈라짐이 작아 t2g 넷, eg 둘로 홀전자 넷',s)
FIG['COIII']=coiii()
def pair(lab1,lab2,t1,e1,t2,e2,y1e,y2e,cap1,cap2,label):
    s=[]
    s.append(T(110,26,tex=lab1,size=20)); s.append(T(330,26,tex=lab2,size=20))
    s.append(dlev(110,y1e,e1,LW=28,gap=9)); s.append(dlev(110,220,t1,LW=28,gap=9)); s.append(dim(40,y1e,220,'',size=19))
    s.append(dlev(330,y2e,e2,LW=28,gap=9)); s.append(dlev(330,220,t2,LW=28,gap=9)); s.append(dim(260,y2e,220,'',size=19))
    s.append(T(110,262,mix=cap1,size=19)); s.append(T(330,262,mix=cap2,size=19))
    return svg('0 0 430 276',430,label,s)
FIG['FEEX']=pair('\\ce{[FeCl6]^3-}','\\ce{[Fe(CN)6]^3-}',['u','u','u'],['u','u'],['ud','ud','u'],['',''],150,60,'고스핀 $t_{2g}^3e_g^2$','저스핀 $t_{2g}^5$','염화 이온 착이온은 갈라짐이 작아 t2g 셋, eg 둘에 하나씩(홀전자 5), 사이안화 이온 착이온은 갈라짐이 커서 t2g에 다섯(홀전자 1)')
FIG['FE5']=pair('\\ce{[Fe(CN)6]^4-}','\\ce{[Fe(H2O)6]^2+}',['ud','ud','ud'],['',''],['ud','u','u'],['u','u'],60,150,'저스핀 $t_{2g}^6$ · 홀전자 0','고스핀 $t_{2g}^4e_g^2$ · 홀전자 4','사이안화 착이온은 t2g에 전자 여섯이 모두 짝, 물 착이온은 t2g 넷, eg 둘로 홀전자 넷')

# ═══ S29 시스플라틴
def cispt():
    s=[]
    for k,(cx,nm,cl) in enumerate([(105,'시스 (시스플라틴)',[(1,0),(0,1)]),(315,'트랜스',[(1,0),(-1,0)])]):
        cy=120; R=66; v=[(1,0),(-1,0),(0,1),(0,-1)]
        for dx,dy in v: s.append(L(cx,cy,cx+dx*R,cy+dy*R,BOND,6,extra='stroke-linecap="round"'))
        for dx,dy in v:
            if (dx,dy) in cl: s.append(atom(cx+dx*R,cy+dy*R,22,'Cl'))
            else:
                s.append(atom(cx+dx*R,cy+dy*R,18,'N','-'))
                s.append(T(cx+dx*R+(0 if dx==0 else dx*8),cy+dy*R+(-26 if dy<=0 and dx==0 else (40 if dy>0 else 7)) if dx==0 else cy+dy*R-24,tex='\\ce{NH3}',size=19))
        s.append(atom(cx,cy,24,'X','\\mathrm{Pt}'))
        s.append(T(cx,250,mix=nm,size=19,weight=700 if k==0 else None))
    s.append(T(210,282,mix='Pt에 $\\ce{NH3}$ 2개, $\\ce{Cl-}$ 2개 — 평면사각형',size=19,fill=MUTED))
    return svg('0 0 420 296',420,'평면사각형 백금 착화합물: 시스 이성질체는 두 염소가 이웃하고, 트랜스 이성질체는 두 염소가 마주 본다',s)
FIG['CISPT']=cispt()
def dna():
    s=[]
    for x in (60,240):
        s.append(f'<path d="M {x} 20 Q {x+40 if x==60 else x-40} 150 {x} 280" fill="none" stroke="{MUTED}" stroke-width="4"/>')
    for k,y in enumerate((50,95,205,250)):
        s.append(L(66 if True else 0,y,234,y,'#C9D3DD',6,extra='stroke-linecap="round"'))
    for y in (130,170):
        s.append(f'<rect x="88" y="{y-16}" width="54" height="32" rx="6" fill="#E9F6EF" stroke="{FIELD}" stroke-width="1.8"/>')
        s.append(T(115,y+7,tex='\\mathrm{G}',size=20))
        s.append(L(142,y,190,150,INK,2.4))
    s.append(atom(205,150,27,'X','\\mathrm{Pt}'))
    s.append(T(150,302,mix='이웃한 두 구아닌(G)의 N과 결합',size=19,fill=MUTED))
    return svg('0 0 300 315',300,'DNA 두 가닥 사이에서 백금이 이웃한 두 구아닌 염기와 결합해 DNA를 구부리는 모식도',s)
FIG['DNA']=dna()

# ═══ S31 I3-
def i3():
    at=[A_('I',70,76,lp=['u','l','d']),A_('I',180,76,lp=[90,240,300],oct=10,fc=-1,fcp='ur'),A_('I',290,76,lp=['u','r','d'])]
    s=[lewis(at,[(0,1,1,'l'),(1,2,1,'l')],S=36,name='I3',num=['0',None,'0'])]
    s.append(bracket(22,30,338,122,'-',22))
    return svg('0 0 380 136',380,'삼아이오딘화 이온: I–I–I, 가운데 I에 비공유 전자쌍 셋과 형식 전하 −1, 양 끝 I에 비공유 전자쌍 셋과 형식 전하 0',s)
FIG['I3']=i3()
def bfclf():
    s=[]
    cx,cy,S=110,110,32
    pos=[(cx,cy-80),(cx-70,cy+40),(cx+70,cy+40)]
    at=[A_('B',cx,cy,oct=6)]
    for (x,y),l in zip(pos,[[90,0,180],[210,120,300],[330,60,240]]): at.append(A_('F',x,y,lp=l))
    s.append(lewis(at,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')],S=S,name='BF3'))
    s.append(T(cx,236,mix='$\\ce{BF3}$: B 둘레 6개',size=19))
    cx=370
    at=[A_('Cl',cx,cy,lp=[30,-30],oct=10),A_('F',cx-80,cy,lp=['u','l','d']),A_('F',cx,cy-78,lp=['u','l','r']),A_('F',cx,cy+78,lp=['l','r','d'])]
    s.append(lewis(at,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')],S=S,name='ClF3'))
    s.append(T(cx,236,mix='$\\ce{ClF3}$: Cl 둘레 10개',size=19))
    return svg('0 0 480 250',480,'삼플루오린화 붕소는 B 둘레 전자 6개, 삼플루오린화 염소는 Cl 둘레 전자 10개',s)
FIG['BFCLF']=bfclf()
def no3():
    s=[]; S=30
    def lps(bd,n):
        o=bd+180
        return [o] if n==1 else ([o-60,o+60] if n==2 else [o,o-90,o+90])
    for k in range(3):
        x0=110+k*300; y0=100; R=60
        ang=[90,210,330]
        at=[A_('N',x0,y0,fc=1,fcp='d')]
        bds=[]
        for i,a in enumerate(ang):
            ox,oy=x0+R*math.cos(math.radians(a)),y0-R*math.sin(math.radians(a))
            dbl=(i==k)
            fp={90:'ur',210:'dl',330:'dr'}[a]
            at.append(A_('O',ox,oy,lp=lps(a+180,2 if dbl else 3),fc=0 if dbl else -1,fcp=fp))
            bds.append((0,i+1,2 if dbl else 1,'l'))
        s.append(lewis(at,bds,S=S,name=f'NO3_{k}'))
        s.append(bracket(x0-96,22,x0+96,160,'-',20))
        if k<2: s.append(rarrow(x0+124,x0+176,100))
    return svg('0 0 920 170',920,'질산 이온의 세 공명 구조: 2중 결합의 위치만 다르고, N은 형식 전하 +1, 단일 결합한 O 둘은 −1',s)
FIG['NO3']=no3()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='))
