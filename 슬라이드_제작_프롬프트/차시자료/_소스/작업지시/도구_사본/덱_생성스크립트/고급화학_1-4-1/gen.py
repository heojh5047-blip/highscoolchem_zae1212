# -*- coding: utf-8 -*-
"""고급화학 1-4-1 그림 생성: gen_head.py(OUT=이 덱, lewis 도우미) + lib131.py(1-3-1 3차원·오비탈 도우미 사본) + chem.py(탄소 골격 정규형·좌표)
   → tpl.html의 {{KEY}}를 바꿔 slides.html, labs_tpl.js의 /*@@DATA@@*/를 바꿔 labs.js"""
import math, re, sys, os, json
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/1-4-1_탄소_화합물의_구조식과_탄화수소의_구조/slides.html')
assert OUTLAB.endswith('content/고급화학/1-4-1_탄소_화합물의_구조식과_탄화수소의_구조/labs.js')
exec(open(os.path.join(HERE,'lib131.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,'chem.py'),encoding='utf-8').read())
VAL['Br']=7; RA.update({'Br':32,'Cl':29})
HL='#FFE45C'
def alk(L,br): return build3d(L,br)
def model(cx,cy,L,br,sc=60,k=.8,yaw=0,pitch=-18,anim=None):
    at,bd=alk(L,br); return bs3d(cx,cy,at,bd,sc=sc,yaw=yaw,pitch=pitch,k=k,anim=anim)
def popa(x,y,d): return ('pop',{'o':f'{f(x)},{f(y)}','dur':'.6','delay':f'{d:.1f}'})
# ── 축약 구조식(가지를 위·아래에 쌓음): groups = 주 사슬 묶음 tex, br = [(묶음 번호, 'u'|'d', tex, 강조)]
CW={'C':.72,'H':.76,'B':.68,'r':.40,'l':.28,'O':.78,'N':.75,'=':.95,'#':.95}
def gw(t,size):
    w=0
    for ch in t: w+=(CW.get(ch,.36) if not ch.isdigit() else .38)
    return w*size
def cond(x,y,groups,br=(),size=22,hl=()):
    ws=[gw(g,size) for g in groups]; W=sum(ws); x0=x-W/2; s=[]; cs=[]
    for i,w in enumerate(ws): cs.append(x0+sum(ws[:i])+w/2)
    for i in hl: s.append(f'<rect x="{f(cs[i]-ws[i]/2-3)}" y="{f(y-size*.82)}" width="{f(ws[i]+6)}" height="{f(size*1.12)}" rx="5" fill="{HL}" fill-opacity=".45"/>')
    for (i,ud,t,h) in br:
        cx=cs[i]; yy=y-size*1.75 if ud=='u' else y+size*1.6
        if h: s.append(f'<rect x="{f(cx-gw(t,size)/2-3)}" y="{f(yy-size*.82)}" width="{f(gw(t,size)+6)}" height="{f(size*1.12)}" rx="5" fill="{HL}" fill-opacity=".45"/>')
        s.append(T(cx,yy,tex=f'\\ce{{{t}}}',size=size))
        y1,y2=(y-size*.95,yy+size*.35) if ud=='u' else (y+size*.42,yy-size*.9)
        s.append(L(cx-size*.18,y1,cx-size*.18,y2,INK,2))
    s.append(T(x,y,tex='\\ce{'+''.join(groups)+'}',size=size))
    return ''.join(s)
def skelC(cx,cy,cells,r=14,d=40,col=None):
    """탄소 골격(공 + 결합선, H 생략): cells [(c,r)] 격자, 이웃끼리 결합"""
    s=[]; P_=[(cx+a*d,cy+b*d) for a,b in cells]
    for i,(a,b) in enumerate(cells):
        for j,(c2,d2) in enumerate(cells):
            if j>i and abs(a-c2)+abs(b-d2)==1: s.append(L(*P_[i],*P_[j],'#9AA5B1',7,extra='stroke-linecap="round"'))
    for (x,y) in P_: s.append(atom(x,y,r,'C','-'))
    return ''.join(s)
def cells_canon(cells):
    ed=[(i,j) for i,(a,b) in enumerate(cells) for j,(c,d) in enumerate(cells) if j>i and abs(a-c)+abs(b-d)==1]
    assert len(ed)==len(cells)-1; return canon_edges(len(cells),ed)
def wedge(x1,y1,x2,y2,w=11):
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n,dx/n
    return f'<polygon points="{f(x1)},{f(y1)} {f(x2+px*w/2)},{f(y2+py*w/2)} {f(x2-px*w/2)},{f(y2-py*w/2)}" fill="{INK}"/>'
def hashw(x1,y1,x2,y2,w=12,k=7):
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n,dx/n; s=[]
    for i in range(1,k+1):
        t=i/(k+.4); cx,cy=x1+dx*t,y1+dy*t; hw=w/2*t
        s.append(L(cx-px*hw,cy-py*hw,cx+px*hw,cy+py*hw,INK,2))
    return ''.join(s)
def dimline(x1,y1,x2,y2,lab,off=18,size=19,side=1,lpos=.5):
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n*side,dx/n*side
    a1,b1,a2,b2=x1+px*off,y1+py*off,x2+px*off,y2+py*off
    s=L(a1,b1,a2,b2,MUTED,1.6)
    for (ax,ay,sg) in ((a1,b1,1),(a2,b2,-1)):
        ux,uy=dx/n*sg,dy/n*sg
        s+=P([(ax+ux*9+px*4,ay+uy*9+py*4),(ax,ay),(ax+ux*9-px*4,ay+uy*9-py*4)],MUTED,1.6)
    mx,my=a1+(a2-a1)*lpos+px*(size*.9),b1+(b2-b1)*lpos+py*(size*.9)
    return s+T(mx,my+size*.36,mix=lab,size=size,halo=True)
def arcA(cx,cy,a1,a2,r,lab,lr=None,size=19,col=MUTED):
    s=arc2(cx,cy,a1,a2,r,col); am=math.radians((a1+a2)/2); lr=lr or r+22
    return s+T(cx+math.cos(am)*lr,cy-math.sin(am)*lr+size*.36,tex=lab,size=size,halo=True)
def curved(x1,y1,x2,y2,bend=40,col=INK,w=2.6):
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n,dx/n
    cx,cy=mx+px*bend,my+py*bend
    tx,ty=x2-cx,y2-cy; tn=math.hypot(tx,ty); tx,ty=tx/tn,ty/tn; qx,qy=-ty,tx
    head=P([(x2-tx*11+qx*5.5,y2-ty*11+qy*5.5),(x2,y2),(x2-tx*11-qx*5.5,y2-ty*11-qy*5.5)],col,w,extra='stroke-linecap="round"')
    return f'<path d="M{f(x1)} {f(y1)} Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'+head
def harrow(x1,x2,y,lab=None,size=19,col=INK):
    s=L(x1,y,x2-4,y,col,2.6)+P([(x2-12,y-6),(x2,y),(x2-12,y+6)],col,2.6)
    if lab: s+=T((x1+x2)/2,y-12,mix=lab,size=size)
    return s
def LW(atoms,bonds,S=30,**k): return lewis(atoms,bonds,S=S,showlp=False,**k)
def H_(x,y): return A_('H',x,y)
def Cc(x,y): return A_('C',x,y)
def ring(x,y,d): return (x+d*math.cos(0),y)

# ═══ S1 표지: C5H12 이성질체 3개
def cover():
    s=[]; Ls=[(5,[],270,146,42,0,-18),(4,[2],146,326,36,0,-18),(3,[2,2],408,330,38,28,-26)]
    for i,(Ln,br,x,y,sc,yw,pt) in enumerate(Ls):
        s.append(model(x,y,Ln,br,sc=sc,k=.86,yaw=yw,pitch=pt,anim=popa(x,y,.3+.35*i)))
    s.append(T(270,424,tex='\\ce{C5H12}',size=28,weight=700))
    s.append(T(270,456,mix='구조 이성질체 3가지',size=21,fill=MUTED))
    return svg('0 0 540 540',540,'분자식이 C5H12인 구조 이성질체 3개의 공-막대 모형: 펜테인, 2-메틸뷰테인, 2,2-다이메틸프로페인',s,cls='cover-fig')
FIG['COVER']=cover()

# ═══ S2 사과와 토마토
def intro():
    s=[]
    s.append(f'<ellipse cx="150" cy="252" rx="130" ry="10" fill="{GRAV}" fill-opacity=".25"/>')
    # 사과
    s.append(f'<path d="M80 150 C40 150 38 215 70 240 C85 252 98 246 105 242 C112 246 125 252 140 240 C172 215 170 150 130 150 C118 150 110 156 105 160 C100 156 92 150 80 150 Z" fill="#C8312F" stroke="#8E1F1C" stroke-width="2"/>')
    s.append(L(105,158,110,132,'#6B4A2B',4,extra='stroke-linecap="round"'))
    s.append(f'<path d="M112 140 C124 126 142 128 146 134 C136 144 122 146 112 140 Z" fill="#4E9A3A"/>')
    # 토마토(초록 → 빨강)
    s.append(C(228,214,40,'#4F7F2A',2,fill='#7DB34A'))
    s.append(an('fade',C(228,214,40,'#A8261E',2,fill='#E0452B'),dur='1.6',delay='1.6'))
    s.append(f'<path d="M212 178 L228 186 L244 178 L236 190 L248 194 L228 194 L208 194 L220 190 Z" fill="#3E7A2B"/>')
    # 에틸렌 분자 2개(사과 → 토마토)
    a,b,_=mol('C2H4')
    for i,(x,y) in enumerate(((168,120),(196,82))):
        body=bs3d(x,y,a,b,sc=20,yaw=0,pitch=-10,k=.42,labels=False)
        s.append(an('move',body,**{'from':f'{-58+i*6},{60-i*8}','dur':'1.8','delay':f'{.2+.5*i:.1f}','ease':'out'}))
    s.append(T(240,58,tex='\\ce{C2H4}',size=19))
    s.append(T(105,286,mix='잘 익은 사과',size=19)); s.append(T(232,286,mix='토마토',size=19))
    return svg('0 0 300 300',290,'잘 익은 사과에서 나온 에틸렌 분자가 덜 익은 토마토를 익게 하는 모습',s)
FIG['INTRO']=intro()

# ═══ S4 생각 열기: 모형 상자
def openbox():
    s=[f'<rect x="10" y="10" width="440" height="250" rx="16" fill="#F7F8FA" stroke="{MUTED}" stroke-width="2"/>']
    cs=[(80,80),(170,120),(110,180),(210,200)]
    hs=[(300,50),(360,80),(410,48),(290,125),(350,150),(410,118),(300,195),(370,200),(250,50),(420,180)]
    for i,(x,y) in enumerate(cs): s.append(an('pop',atom(x,y,24,'C'),o=f'{x},{y}',dur='.5',delay=f'{.2+.15*i:.2f}'))
    for (x,y) in hs: s.append(atom(x,y,18,'H'))
    s.append(T(140,252,mix='탄소 4개',size=19,fill=MUTED)); s.append(T(345,252,mix='수소 10개',size=19,fill=MUTED))
    return svg('0 0 460 270',460,'분자 모형 상자: 탄소 공 4개와 수소 공 10개',s)
FIG['OPENBOX']=openbox()

# ═══ S5 그림 Ⅰ-38 선-결합 구조식 5개
def f38():
    s=[]; d=58; S=30
    def put(i,body,nm):
        x=110+i*220
        s.append(an('fade',body,dur='.6',delay=f'{.2+.25*i:.2f}')); s.append(T(x,204,mix=nm,size=20,fill=MUTED))
    x,y=110,85
    put(0,LW([Cc(x,y),H_(x,y-d),H_(x,y+d),H_(x-d,y),H_(x+d,y)],[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],name='메테인'),'메테인')
    x=330; a=[Cc(x-29,y),Cc(x+29,y),H_(x-29,y-d),H_(x-29,y+d),H_(x-29-d,y),H_(x+29,y-d),H_(x+29,y+d),H_(x+29+d,y)]
    put(1,LW(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(1,5,1,'l'),(1,6,1,'l'),(1,7,1,'l')],name='에테인'),'에테인')
    x=550; t=[(x,y-34),(x-36,y+28),(x+36,y+28)]
    a=[Cc(*t[0]),Cc(*t[1]),Cc(*t[2]),H_(t[0][0]-38,t[0][1]-30),H_(t[0][0]+38,t[0][1]-30),H_(t[1][0]-52,t[1][1]-8),H_(t[1][0]-20,t[1][1]+50),H_(t[2][0]+52,t[2][1]-8),H_(t[2][0]+20,t[2][1]+50)]
    put(2,LW(a,[(0,1,1,'l'),(1,2,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(1,5,1,'l'),(1,6,1,'l'),(2,7,1,'l'),(2,8,1,'l')],name='사이클로프로페인'),'사이클로프로페인')
    x=770; a=[Cc(x-30,y),Cc(x+30,y),H_(x-62,y-50),H_(x-62,y+50),H_(x+62,y-50),H_(x+62,y+50)]
    put(3,LW(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],name='에틸렌'),'에틸렌(에텐)')
    x=990; a=[Cc(x-30,y),Cc(x+30,y),H_(x-88,y),H_(x+88,y)]
    put(4,LW(a,[(0,1,3,'l'),(0,2,1,'l'),(1,3,1,'l')],name='아세틸렌'),'아세틸렌(에타인)')
    return svg('0 0 1100 214',1060,'여러 가지 탄소 화합물의 선-결합 구조식: 메테인, 에테인, 사이클로프로페인, 에틸렌, 아세틸렌',s)
FIG['F38']=f38()

# ═══ S6 프로페인 네 표현
def prlew():
    x,y,d=150,75,56
    a=[Cc(x-d,y),Cc(x,y),Cc(x+d,y),H_(x-d,y-d),H_(x-d,y+d),H_(x-2*d,y),H_(x,y-d),H_(x,y+d),H_(x+d,y-d),H_(x+d,y+d),H_(x+2*d,y)]
    b=[(0,1,1,'l'),(1,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(0,5,1,'l'),(1,6,1,'l'),(1,7,1,'l'),(2,8,1,'l'),(2,9,1,'l'),(2,10,1,'l')]
    return svg('0 0 300 150',250,'프로페인의 선-결합 구조식',[LW(a,b,S=26,name='프로페인')])
FIG['PRLEW']=prlew()
FIG['PRBS']=svg('0 0 260 150',250,'프로페인의 공-막대 모형(지그재그)',[model(130,78,3,[],sc=58,k=.72,anim=popa(130,78,.4))])

# ═══ S7 메테인 쐐기 + 공-막대
def ch4w():
    s=[]; cx,cy=150,165; Lb=92
    def pt(a,l=Lb): return (cx+math.cos(math.radians(a))*l,cy-math.sin(math.radians(a))*l)
    hU,hL,hW,hH=pt(90),pt(205),pt(325,86),pt(268,80)
    s.append(L(cx,cy-14,hU[0],hU[1]+16,INK,3)); s.append(L(cx-13,cy+6,hL[0]+15,hL[1]-7,INK,3))
    s.append(wedge(cx+10,cy+7,hW[0]-12,hW[1]-9,13)); s.append(hashw(cx+1,cy+15,hH[0],hH[1]-17,13))
    s.append(T(cx,cy+8,tex='\\mathrm{C}',size=28))
    for (x,y) in (hU,hL,hW,hH): s.append(T(x,y+9,tex='\\mathrm{H}',size=26))
    s.append(arcA(cx,cy,90,205,40,'109.5^\\circ',lr=70))
    s.append(dimline(cx,cy-16,hU[0],hU[1]+18,'0.109 nm',off=26,side=1))
    a,b,_=mol('CH4'); s.append(bs3d(380,160,a,b,sc=70,yaw=28,pitch=-14,k=.9,anim=('rot',{'from':'-40','o':'380,160','dur':'1.4','ease':'out'})))
    return svg('0 0 480 300',470,'메테인의 쐐기 구조식(결합각 109.5도, C–H 0.109 nm)과 공-막대 모형',s)
FIG['CH4W']=ch4w()

# ═══ S8 에테인 쐐기 / sp3–sp3 / 축 방향
def c2h6w():
    s=[]; ya=120; xa,xb=150,270; Lb=78
    def pt(x,a,l=Lb): return (x+math.cos(math.radians(a))*l,ya-math.sin(math.radians(a))*l)
    s.append(L(xa+14,ya-1,xb-14,ya-1,INK,3))
    for x,(pa,wa,ha) in ((xa,(110,215,250)),(xb,(70,325,290))):
        hp,hw,hh=pt(x,pa),pt(x,wa,72),pt(x,ha,70)
        sg=1 if x==xb else -1
        s.append(L(x+sg*4,ya-14,hp[0]-sg*6,hp[1]+15,INK,3))
        s.append(wedge(x+sg*8,ya+8,hw[0]-sg*12,hw[1]-8,12)); s.append(hashw(x+sg*2,ya+15,hh[0]+sg*2,hh[1]-16,12))
        s.append(T(x,ya+8,tex='\\mathrm{C}',size=26))
        for (hx,hy) in (hp,hw,hh): s.append(T(hx,hy+9,tex='\\mathrm{H}',size=24))
    s.append(arcA(xb,ya,0,70,34,'111.2^\\circ',lr=58))
    s.append(dimline(xa,ya,xb,ya,'0.154 nm',off=88,side=1))
    return svg('0 0 420 250',380,'에테인의 쐐기 구조식(H–C–C 111.2도, C–C 0.154 nm)',s)
FIG['C2H6W']=c2h6w()
def c2h6orb():
    s=[]; y=110; xa,xb=140,280
    def side(x,sg):
        g=[]
        for ang in ((140,220,180) if sg<0 else (40,320,0)):
            l0=82 if ang in (180,0) else 88
            t=math.radians(ang); hx,hy=x+math.cos(t)*l0*1.12,y-math.sin(t)*l0*1.12
            g.append(lob(x,y,ang,l0*(.8 if ang in (0,180) else 1),1,lab=False,W=.5)); g.append(sph(hx,hy,22,lab=False)); g.append(dotn(hx,hy,3.5))
            g.append(sigbox(x+(hx-x)*.74,y+(hy-y)*.74,14,14))
        g.append(lob(x,y,0 if sg<0 else 180,62,1,lab=False,W=.5)); g.append(dotn(x,y,5)); g.append(T(x,y+28,tex='\\mathrm{C}',size=19))
        return ''.join(g)
    s.append(side(xa,-1)); s.append(an('move',side(xb,1),**{'from':'60,0','dur':'1.2','ease':'out'}))
    s.append(sigbox(210,y,22,17))
    s.append(T(210,y-38,mix='$sp^3$–$sp^3$ σ 결합',size=19,fill=FIELD,weight=700))
    s.append(T(210,214,mix='C–H: $sp^3$–$1s$ σ 결합 6개',size=19,fill=FIELD))
    return svg('0 0 420 230',400,'에테인의 탄소-탄소 단일 결합: 두 탄소의 sp3 혼성 오비탈이 겹친 시그마 결합과 C–H 시그마 결합',s)
FIG['C2H6ORB']=c2h6orb()
def c2h6end():
    s=[]; cx,cy=110,110
    s.append(C(cx,cy,34,MUTED,2.2,fill='#fff'))
    for a in (30,150,270):
        t=math.radians(a); s.append(L(cx+math.cos(t)*34,cy-math.sin(t)*34,cx+math.cos(t)*74,cy-math.sin(t)*74,GRAV,4,extra='stroke-linecap="round"'))
        s.append(atom(cx+math.cos(t)*86,cy-math.sin(t)*86,15,'H','-'))
    fr=[]
    for a in (90,210,330):
        t=math.radians(a); fr.append(L(cx,cy,cx+math.cos(t)*74,cy-math.sin(t)*74,INK,4,extra='stroke-linecap="round"')); fr.append(atom(cx+math.cos(t)*86,cy-math.sin(t)*86,15,'H','-'))
    fr.append(dotn(cx,cy,6))
    s.append(an('rot',fr,**{'from':'-60','o':f'{cx},{cy}','dur':'1.6','ease':'soft','on':'step'}))
    s.append(T(cx,222,mix='앞 C(검은 선) · 뒤 C(원)',size=19,fill=MUTED))
    return svg('0 0 220 232',200,'C–C 축 방향에서 본 에테인: 앞 탄소의 C–H 결합이 축을 중심으로 돈다',s)
FIG['C2H6END']=c2h6end()

# ═══ S9 에틸렌 평면 구조
def c2h4st():
    s=[]; y=130; xa,xb=150,262
    a=[Cc(xa,y),Cc(xb,y),H_(xa-62,y-98),H_(xa-62,y+98),H_(xb+62,y-98),H_(xb+62,y+98)]
    s.append(lewis(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],S=30,showlp=False,name='에틸렌2'))
    ang=math.degrees(math.atan2(98,62))
    s.append(arcA(xa,y,0,180-ang,30,'121.3^\\circ',lr=58))
    s.append(arcA(xb,y,-ang,ang,30,'117.4^\\circ',lr=64))
    s.append(dimline(xa-10,y-20,xa-56,y-90,'0.1087 nm',off=22,side=-1,lpos=.35))
    s.append(dimline(xa,y,xb,y,'0.134 nm',off=96,side=1))
    return svg('0 0 420 290',360,'에틸렌의 평면 구조: H–C=C 121.3도, H–C–H 117.4도, C–H 0.1087 nm, C=C 0.134 nm',s)
FIG['C2H4ST']=c2h4st()
# ═══ S10 아세틸렌 직선 구조
def c2h2st():
    s=[]; y=70; xa,xb=170,250
    a=[Cc(xa,y),Cc(xb,y),H_(xa-90,y),H_(xb+90,y)]
    s.append(lewis(a,[(0,1,3,'l'),(0,2,1,'l'),(1,3,1,'l')],S=30,showlp=False,name='아세틸렌2'))
    s.append(arc2(xa,y,0,180,30)); s.append(T(xa,y-40,tex='180^\\circ',size=19,halo=True))
    s.append(dimline(xa-90,y,xa,y,'0.106 nm',off=40,side=1))
    s.append(dimline(xa,y,xb,y+0.001,'0.120 nm',off=70,side=1))
    a2,b2,_=mol('C2H2'); s.append(bs3d(210,200,a2,b2,sc=62,yaw=0,pitch=-8,k=.85,anim=popa(210,200,.4)))
    return svg('0 0 420 250',380,'아세틸렌의 직선 구조: 180도, C–H 0.106 nm, C≡C 0.120 nm, 공-막대 모형',s)
FIG['C2H2ST']=c2h2st()
exec(open(os.path.join(HERE,'fig131.py'),encoding='utf-8').read())

# ═══ S11 네 분자 작은 모형
def c2four():
    s=[]
    for k_,nm in enumerate(('C2H6','C2H4','C2H2')):
        a,b,_=mol(nm); x=150+k_*300
        s.append(bs3d(x,62,a,b,sc=50,yaw=18 if nm=='C2H6' else 0,pitch=-20 if nm=='C2H6' else -8,k=.72,anim=popa(x,62,.2+.3*k_)))
    return svg('0 0 900 125',820,'에테인, 에틸렌, 아세틸렌의 공-막대 모형',s)
FIG['C2FOUR']=c2four()

# ═══ S12 탄소 골격 4가지
def divers():
    s=[]; W=300
    panels=[('사슬',[(0,1),(1,0),(2,1),(3,0),(4,1)]),('가지',[(0,1),(1,1),(2,1),(3,1),(1,0)]),('고리',None),('다중 결합·다른 원자',None)]
    for i,(nm,cells) in enumerate(panels):
        x0=i*W; g=[]
        if nm=='사슬':
            pts=[(x0+50+k_*50,95-(k_%2)*32) for k_ in range(5)]
            for p,q in zip(pts,pts[1:]): g.append(L(*p,*q,'#9AA5B1',7,extra='stroke-linecap="round"'))
            for p in pts: g.append(atom(*p,16,'C','-'))
        elif nm=='가지':
            pts=[(x0+60,110),(x0+110,82),(x0+160,110),(x0+210,82),(x0+110,30)]
            for a_,b_ in ((0,1),(1,2),(2,3),(1,4)): g.append(L(*pts[a_],*pts[b_],'#9AA5B1',7,extra='stroke-linecap="round"'))
            for p in pts: g.append(atom(*p,16,'C','-'))
        elif nm=='고리':
            pts=[(x0+150+52*math.cos(math.radians(90+60*k_)),72-52*math.sin(math.radians(90+60*k_))) for k_ in range(6)]
            for k_ in range(6): g.append(L(*pts[k_],*pts[(k_+1)%6],'#9AA5B1',7,extra='stroke-linecap="round"'))
            for p in pts: g.append(atom(*p,16,'C','-'))
        else:
            c=[(x0+40,100),(x0+90,70),(x0+150,70),(x0+210,70)]
            for t in (-5,5): g.append(L(c[0][0],c[0][1]+t,c[1][0],c[1][1]+t,'#9AA5B1',5))
            for t in (-7,0,7): g.append(L(c[2][0],c[2][1]+t,c[3][0],c[3][1]+t,'#9AA5B1',5))
            g.append(L(*c[1],*c[2],'#9AA5B1',7))
            for (ex,ey,el) in ((x0+250,100,'O'),(x0+90,22,'N'),(x0+40,148,'Cl')):
                pass
            g.append(L(*c[3],x0+258,98,'#9AA5B1',7)); g.append(L(*c[1],x0+90,24,'#9AA5B1',7)); g.append(L(*c[0],x0+40,146,'#9AA5B1',7))
            for p in c: g.append(atom(*p,16,'C','-'))
            g.append(atom(x0+258,98,17,'O','-')); g.append(atom(x0+90,24,17,'N','-')); g.append(atom(x0+40,146,19,'Cl','-'))
            g.append(T(x0+282,106,tex='\\mathrm{O}',size=23,anchor='start')); g.append(T(x0+114,32,tex='\\mathrm{N}',size=23,anchor='start')); g.append(T(x0+68,156,tex='\\mathrm{Cl}',size=23,anchor='start'))
        s.append(an('pop',''.join(g),o=f'{x0+150},80',dur='.6',delay=f'{.2+.25*i:.2f}'))
        s.append(T(x0+150,190,mix=nm,size=20,weight=700))
    s.append(T(600,224,mix='검은 공: 탄소 (H는 생략)',size=22,fill=MUTED))
    return svg('0 0 1200 232',1000,'탄소 골격의 여러 모양: 사슬, 가지, 고리, 다중 결합과 다른 원자',s)
FIG['DIVERS']=divers()

# ═══ S14 탄화수소 분류 나무
def classtree():
    s=[]
    def box(x,y,w,h,txt,col=INK,fill='#fff',size=20):
        return f'<rect x="{f(x-w/2)}" y="{f(y-h/2)}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{col}" stroke-width="2"/>'+T(x,y+size*.36-(size*.6 if '||' in txt else 0),mix=txt,size=size)
    s.append(box(500,34,180,50,'탄화수소',fill='#F2FAF5',col=FIELD,size=22))
    s.append(box(250,118,300,62,'포화 탄화수소||2중·3중 결합 없음'))
    s.append(box(750,118,320,62,'불포화 탄화수소||2중·3중 결합 있음'))
    leaves=[(250,'알케인','C–C 단일 결합만','\\mathrm{C}_n\\mathrm{H}_{2n+2}','C2H6','\\ce{C2H6}'),(620,'알켄','C=C 2중 결합','\\mathrm{C}_n\\mathrm{H}_{2n}','C2H4','\\ce{C2H4}'),(880,'알카인','C≡C 3중 결합','\\mathrm{C}_n\\mathrm{H}_{2n-2}','C2H2','\\ce{C2H2}')]
    br=[L(500,59,500,74,MUTED,2),L(250,74,750,74,MUTED,2),L(250,74,250,87,MUTED,2),L(750,74,750,87,MUTED,2),L(250,149,250,170,MUTED,2),L(750,149,750,160,MUTED,2),L(620,160,880,160,MUTED,2),L(620,160,620,170,MUTED,2),L(880,160,880,170,MUTED,2)]
    s.append(an('draw',br,dur='.9'))
    for i,(x,nm,bd,frm,m,tx) in enumerate(leaves):
        s.append(box(x,200,240,62,f'{nm}||{bd}',col=INK,size=22))
        s.append(f'<g class="step" data-g="cf{i}">'+f'<rect x="{x-80}" y="236" width="160" height="38" rx="8" fill="{HL}" fill-opacity=".45"/>'+T(x,262,tex=frm,size=22)+'</g>')
        a,b,_=mol(m); s.append(bs3d(x,318,a,b,sc=34,yaw=18 if m=='C2H6' else 0,pitch=-18 if m=='C2H6' else -8,k=.5,labels=False))
        s.append(T(x,370,tex=tx,size=20))
    return svg('0 0 1000 382',820,'탄화수소의 분류: 포화 탄화수소 알케인, 불포화 탄화수소 알켄과 알카인, 일반식과 예',s)
FIG['CLASS']=classtree()

# ═══ S16 직선-사슬 알케인 끓는점
BP=[-162,-89,-42,-0.5,36,69,98,126,151,174]
def bpgraph():
    s=[]; x0,y0,W,H=80,300,440,260; tmin,tmax=-200,200
    X=lambda n:x0+(n-0.5)*W/10; Y=lambda t:y0-(t-tmin)/(tmax-tmin)*H
    s.append(f'<rect x="{x0}" y="{f(Y(25))}" width="{W}" height="{f(y0-Y(25))}" fill="#E3EEFB" fill-opacity=".8"/>')
    s.append(L(x0,y0,x0+W,y0,MUTED,1.6)); s.append(L(x0,y0,x0,y0-H-6,MUTED,1.6))
    for t in (-200,-100,0,100,200):
        s.append(L(x0-6,Y(t),x0,Y(t),MUTED,1.4)); s.append(T(x0-10,Y(t)+7,mix=str(t),size=18,anchor='end'))
        if t>-200: s.append(L(x0,Y(t),x0+W,Y(t),'#E2E7EC',1))
    for n in range(1,11): s.append(T(X(n),y0+24,mix=str(n),size=18))
    s.append(L(x0,Y(25),x0+W,Y(25),MUTED,1.8,dash='6 5')); s.append(T(x0+W-4,Y(25)-8,mix='25 °C',size=18,anchor='end',fill=MUTED))
    s.append(T(x0+60,y0-14,mix='25 °C에서 기체',size=19,anchor='start',fill=MINUS))
    s.append(T(x0+W-6,Y(25)-36,mix='25 °C에서 액체',size=19,anchor='end'))
    pts=[(X(n+1),Y(t)) for n,t in enumerate(BP)]
    s.append(an('draw',P(pts,INK,2.6),dur='1.6'))
    for (x,y) in pts: s.append(C(x,y,5,INK,1.5,fill=INK))
    s.append(T(X(4)+12,Y(-0.5)+26,mix='뷰테인 −0.5',size=18,anchor='start')); s.append(T(X(5)-10,Y(36)-14,mix='펜테인 36',size=18,anchor='end'))
    s.append(T(x0+W/2,y0+50,mix='탄소 수 $n$',size=19)); s.append(T(x0-58,y0-H-14,mix='끓는점 [°C]',size=19,anchor='start'))
    return svg('0 0 540 360',540,'직선-사슬 알케인의 탄소 수에 따른 끓는점 그래프: 탄소 수 1–4는 25도에서 기체, 5–10은 액체',s)
FIG['BPGRAPH']=bpgraph()

# ═══ S17 그림 Ⅰ-46·47
CONDS={(1,()):(['CH4'],[]),(2,()):(['CH3','CH3'],[]),(3,()):(['CH3','CH2','CH3'],[]),
       (4,()):(['CH3','CH2','CH2','CH3'],[]),(3,(2,)):(['CH3','CH','CH3'],[(1,'u','CH3',True)]),
       (5,()):(['CH3','CH2','CH2','CH2','CH3'],[]),(4,(2,)):(['CH3','CH','CH2','CH3'],[(1,'u','CH3',True)]),
       (3,(2,2)):(['CH3','C','CH3'],[(1,'u','CH3',True),(1,'d','CH3',True)])}
def i46():
    s=[]
    for i,Ln in enumerate((1,2,3)):
        x=105+i*215
        if Ln==1:
            a,b,_=mol('CH4'); body=bs3d(x,74,a,b,sc=44,yaw=28,pitch=-14,k=.66)
        else: body=model(x,74,Ln,[],sc=40,k=.66)
        s.append(an('pop',body,o=f'{x},74',dur='.5',delay=f'{.2+.2*i:.1f}'))
        g,brr=CONDS[(Ln,())]; s.append(cond(x,154,g,brr,size=22))
    return svg('0 0 640 172',560,'메테인, 에테인, 프로페인의 분자 구조식: 공-막대 모형과 축약 구조식',s)
FIG['I46']=i46()
def isorow(Lbs,W,step_g=None,size=21,sc=48,lab=True,yb=104,yc=234):
    s=[]; n=len(Lbs)
    for i,(Ln,br,nm) in enumerate(Lbs):
        x=W/n*(i+.5)
        body=model(x,yb,Ln,list(br),sc=sc,k=.72,anim=popa(x,yb,.2+.3*i))
        g,brr=CONDS[(Ln,tuple(br))]
        part=body+cond(x,yc,g,brr,size=size)+(T(x,yc+64,mix=nm,size=22,fill=MUTED) if lab else '')
        s.append(step(part,f'{step_g}{i}') if step_g else part)
    return s
FIG['I47C4']=svg('0 0 640 318',560,'C4H10의 구조 이성질체: 뷰테인과 2-메틸프로페인',isorow([(4,(),'뷰테인'),(3,(2,),'2-메틸프로페인')],640))
FIG['C5ISO']=svg('0 0 1080 318',1000,'C5H12의 구조 이성질체 3개: 펜테인, 2-메틸뷰테인, 2,2-다이메틸프로페인',isorow([(5,(),'펜테인'),(4,(2,),'2-메틸뷰테인'),(3,(2,2),'2,2-다이메틸프로페인')],1080))

# ═══ S19 같은 분자일까
SAME=[('가',[(0,0),(1,0),(2,0),(3,0),(4,0)]),('나',[(0,0),(1,0),(2,0),(2,1),(3,1)]),('다',[(0,0),(0,1),(0,2),(0,3),(1,1)]),('라',[(0,0),(1,0),(2,0),(3,0),(2,1)])]
cs_=[cells_canon(c) for _,c in SAME]
assert cs_[0]==cs_[1]==canon_edges(*skel(5,[])[:2]) and cs_[2]==cs_[3]==canon_edges(*skel(4,[2])[:2]) and cs_[0]!=cs_[2]
def same4():
    s=[]; xs=[40,290,560,760]; ys=[80,50,22,50]
    for i,(nm,cells) in enumerate(SAME):
        body=skelC(xs[i],ys[i],cells,r=15,d=46)
        if nm=='나':
            fixed=skelC(xs[i],ys[i],cells[:3],r=15,d=46)
            p2=(xs[i]+2*46,ys[i]); mov=L(p2[0],p2[1],p2[0],p2[1]+46,'#9AA5B1',7,extra='stroke-linecap="round"')+L(p2[0],p2[1]+46,p2[0]+46,p2[1]+46,'#9AA5B1',7,extra='stroke-linecap="round"')+atom(p2[0],p2[1]+46,15,'C','-')+atom(p2[0]+46,p2[1]+46,15,'C','-')
            body=fixed+an('rot',mov,**{'from':'-90','o':f'{f(p2[0])},{f(p2[1])}','dur':'1.4','ease':'soft'})
            body=fixed.replace(atom(*p2,15,'C','-'),'')+an('rot',mov,**{'from':'-90','o':f'{f(p2[0])},{f(p2[1])}','dur':'1.4','ease':'soft'})+atom(*p2,15,'C','-')
        s.append(body); s.append(T(xs[i]+ (100 if nm!='다' else 23),205,mix=f'({nm})',size=21,weight=700))
    return svg('0 0 960 220',900,'C5H12 탄소 골격 네 가지 그림: (가) 곧은 사슬, (나) 꺾인 사슬, (다) 세로 사슬에 가지, (라) 가로 사슬에 가지',s)
FIG['SAME4']=same4()

# ═══ S21 이성질체 수 로그 막대
CNT=[1,1,1,2,3,5,9,18,35,75,159,355,802,1858]
src_iso=open(os.path.join(HERE,'iso.py')).read().split('lv=grow')[0]; _g={}; exec(src_iso,_g)
_lv=_g['grow'](14); assert [len(_lv[n]) for n in range(1,15)]==CNT
def logbar():
    s=[]; x0,y0,W,H=74,290,440,250; dec=H/4
    Y=lambda c:y0-math.log10(c)*dec
    s.append(L(x0,y0,x0+W,y0,MUTED,1.6)); s.append(L(x0,y0,x0,y0-H-8,MUTED,1.6))
    for k_,lab in enumerate(('1','10','100','1000','10^4')):
        y=y0-k_*dec; s.append(L(x0-6,y,x0,y,MUTED,1.4)); s.append(T(x0-10,y+7,tex=lab,size=18,anchor='end'))
        if k_: s.append(L(x0,y,x0+W,y,'#E2E7EC',1))
    bw=W/14
    for n,c in enumerate(CNT,1):
        x=x0+(n-1)*bw+4; h=max(3,y0-Y(c))
        attrs=f'fill="{INK}"' if n<=10 else f'fill="#fff" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 3"'
        s.append(an('scale',f'<rect x="{f(x)}" y="{f(y0-h)}" width="{f(bw-8)}" height="{f(h)}" {attrs}/>',**{'from':'1,0','o':f'{f(x+bw/2-4)},{y0}','dur':'.7','delay':f'{.1+.08*n:.2f}'}))
        s.append(T(x+bw/2-4,y0+22,mix=str(n),size=18))
        if n in (4,6,8,10,12,14): s.append(T(x+bw/2-4,y0-h-8,mix=str(c),size=18))
    s.append(T(x0+W/2,y0+48,mix='탄소 수 $n$',size=19)); s.append(T(x0-50,y0-H-18,mix='구조 이성질체 수 (로그 눈금)',size=19,anchor='start'))
    s.append(f'<rect x="{x0+20}" y="{y0-H+6}" width="18" height="14" fill="{INK}"/>'); s.append(T(x0+44,y0-H+19,mix='교과서 자료',size=18,anchor='start'))
    s.append(f'<rect x="{x0+170}" y="{y0-H+6}" width="18" height="14" fill="#fff" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 2"/>'); s.append(T(x0+194,y0-H+19,mix='덱 계산($n$ 11–14)',size=18,anchor='start'))
    return svg('0 0 540 350',520,'알케인의 탄소 수에 따른 구조 이성질체 수 막대그래프(세로 로그 눈금)',s)
FIG['LOGBAR']=logbar()

# ═══ S22 가스레인지 불꽃
def flame():
    s=[]
    s.append(f'<rect x="80" y="40" width="220" height="70" rx="10" fill="#B8C2CC" stroke="{INK}" stroke-width="2"/>'); s.append(L(64,40,316,40,INK,4))
    s.append(f'<rect x="60" y="226" width="260" height="22" rx="6" fill="#5B6B7F"/>'); s.append(f'<rect x="150" y="206" width="80" height="22" rx="4" fill="#3A3F47"/>')
    fl=[]
    for k_ in range(7):
        x=124+k_*22
        fl.append(f'<path d="M{x-9} 206 C{x-12} 182 {x-4} 168 {x} 150 C{x+4} 168 {x+12} 182 {x+9} 206 Z" fill="#3E8ED0" fill-opacity=".75" stroke="#1F6FD1" stroke-width="1.2"/>')
    s.append(an('scale',''.join(fl),**{'from':'1,0.8','o':'190,206','dur':'.5','rep':'swing','ease':'sine'}))
    for x in (110,190,270): s.append(A(x,146,x,118,EQUI,3))
    s.append(T(318,140,mix='열 방출',size=21,anchor='start',fill=EQUI,weight=700))
    s.append(T(200,274,mix='메테인 + 산소 → 이산화 탄소 + 물',size=21,fill=MUTED))
    return svg('0 0 410 285',340,'가스레인지에서 메테인이 연소하며 파란 불꽃과 열을 내는 모습',s)
FIG['FLAME']=flame()

# ═══ S24 에틸렌 모형 + π
def ethpi():
    a,b,_=mol('C2H4'); a=[(e,(x,z,y)) for e,(x,y,z) in a]
    s=[bs3d(200,110,a,b,sc=78,yaw=0,pitch=-14,k=.85,anim=popa(200,110,.3))]
    s.append(sigbox(200,58,70,22,dash='6 5')); s.append(sigbox(200,158,70,22,dash='6 5'))
    s.append(T(290,40,mix='π 결합',size=20,anchor='start',fill=FIELD,weight=700))
    return svg('0 0 400 210',360,'에틸렌의 공-막대 모형과 2중 결합 위아래의 파이 결합',s)
FIG['ETHPI']=ethpi()

# ═══ 시스-트랜스 평면 구조식(교과서 꼴)
def alkene(x,y,subs,S=24,hl=(),dash=False):
    """subs: [왼위, 왼아래, 오위, 오아래] tex. hl: 강조할 자리 번호"""
    s=[]; xa,xb=x-28,x+28; d=54
    for t in (-5,5): s.append(L(xa+12,y+t,xb-12,y+t,INK,2.6))
    s.append(T(xa,y+S*.36,tex='\\mathrm{C}',size=S)); s.append(T(xb,y+S*.36,tex='\\mathrm{C}',size=S))
    pos=[(xa-d*.62,y-d*.85,150),(xa-d*.62,y+d*.85,210),(xb+d*.62,y-d*.85,30),(xb+d*.62,y+d*.85,330)]
    for i,(t,(px,py,ang)) in enumerate(zip(subs,pos)):
        cx,cy=(xa,y) if i<2 else (xb,y); r=math.radians(ang)
        s.append(L(cx+math.cos(r)*13,cy-math.sin(r)*13,px-math.cos(r)*18,py+math.sin(r)*16,INK,2.6))
        w=gw(t,S) if t not in ('H',) else .76*S
        if i in hl: s.append(f'<rect x="{f(px-w/2-4)}" y="{f(py-S*.62)}" width="{f(w+8)}" height="{f(S*1.12)}" rx="5" fill="{HL}" fill-opacity=".45"/>')
        s.append(T(px,py+S*.36,tex=f'\\ce{{{t}}}',size=S))
    if dash: s.append(L(x,y-72,x,y+72,MUTED,1.6,dash='5 4'))
    return ''.join(s)
def cistrans():
    s=[]
    s.append(alkene(150,82,['H3C','H','CH3','H'],hl=(0,2),dash=True)); s.append(T(150,186,mix='시스-2-뷰텐',size=20,weight=700))
    s.append(alkene(410,82,['H3C','H','H','CH3'],hl=(0,3),dash=True)); s.append(T(410,186,mix='트랜스-2-뷰텐',size=20,weight=700))
    s.append(T(150,212,mix='메틸기가 같은 쪽',size=19,fill=MUTED)); s.append(T(410,212,mix='메틸기가 반대쪽',size=19,fill=MUTED))
    return svg('0 0 560 225',540,'시스-2-뷰텐과 트랜스-2-뷰텐의 구조식: 메틸 치환기가 2중 결합을 중심으로 같은 쪽과 반대쪽',s)
FIG['CISTRANS']=cistrans()
def prot():
    s=[]; y=100
    for xa,xb in ((70,150),):
        s.append(lob(xa,y,90,66,1,W=.5,lab=True)); s.append(lob(xa,y,270,66,-1,W=.5,lab=True))
        s.append(lob(xb,y,90,66,1,W=.5,lab=False)); s.append(lob(xb,y,270,66,-1,W=.5,lab=False))
        s.append(L(xa,y,xb,y,INK,3)); s.append(dotn(xa,y,5)); s.append(dotn(xb,y,5))
        s.append(sigbox(110,y-46,52,18,dash='6 5')); s.append(sigbox(110,y+46,52,18,dash='6 5'))
    s.append(T(110,200,mix='나란함 → π 겹침',size=19,fill=FIELD,weight=700))
    s.append(T(230,94,mix='90° 돌리면',size=19)); s.append(harrow(196,266,104))
    xa,xb=300,380
    s.append(lob(xa,y,90,66,1,W=.5,lab=True)); s.append(lob(xa,y,270,66,-1,W=.5,lab=True))
    rotg=lob(xb,y,0,66,1,W=.5,lab=False)+lob(xb,y,180,66,-1,W=.5,lab=False)
    s.append(an('rot',rotg,**{'from':'-90','o':f'{xb},{y}','dur':'1.4','ease':'soft','delay':'.4'}))
    s.append(L(xa,y,xb,y,INK,3)); s.append(dotn(xa,y,5)); s.append(dotn(xb,y,5))
    s.append(T(340,200,mix='수직 → 겹침 없음',size=19,fill=PLUS,weight=700))
    s.append(T(340,226,mix='π 결합이 끊어진다',size=19,fill=PLUS))
    return svg('0 0 460 236',420,'C=C 결합의 p 오비탈: 나란하면 파이 겹침, 한쪽을 90도 돌리면 겹침이 없어 파이 결합이 끊어진다',s)
FIG['PROT']=prot()
# ═══ S26 시스·트랜스 모형 + 쌍극자
def ctbs():
    s=[]
    for i,cis in enumerate((True,False)):
        at,bd,_=butene(cis); x=140+i*280
        s.append(bs3d(x,112,at,bd,sc=52,yaw=0,pitch=-12,k=.78,anim=popa(x,112,.2+.3*i)))
        s.append(T(x,222,mix='시스-2-뷰텐' if cis else '트랜스-2-뷰텐',size=20,weight=700))
    # 시스: 메틸 쪽(δ+) → H 쪽
    x=22; s.append(an('draw',A(x,62,x,160,PLUS,4)+L(x-8,78,x+8,78,PLUS,4),dur='.8',delay='.9'))
    s.append(T(140,250,mix='극성 — 분자의 쌍극자(빨간 화살표)',size=18,fill=PLUS))
    s.append(T(420,250,mix='무극성 — 쌍극자의 합 = 0',size=18,fill=MUTED))
    return svg('0 0 560 262',540,'시스-2-뷰텐(극성, 분자 쌍극자 화살표)과 트랜스-2-뷰텐(무극성) 공-막대 모형',s)
FIG['CTBS']=ctbs()
# ═══ S27 π 전자와 친전자체
def epi():
    s=[]; y=170; xa,xb=170,290
    s.append(lob(xa,y,90,80,1,W=.5,opa=.22,lab=False)); s.append(lob(xa,y,270,80,-1,W=.5,opa=.22,lab=False))
    s.append(lob(xb,y,90,80,1,W=.5,opa=.22,lab=False)); s.append(lob(xb,y,270,80,-1,W=.5,opa=.22,lab=False))
    s.append(sigbox(230,y-56,82,24,dash='6 5')); s.append(sigbox(230,y+56,82,24,dash='6 5'))
    for x,sg in ((xa,-1),(xb,1)):
        for a_ in ((150,210) if sg<0 else (30,330)):
            t=math.radians(a_); hx,hy=x+math.cos(t)*70,y-math.sin(t)*40
            s.append(L(x,y,hx,hy,INK,3)); s.append(atom(hx,hy,15,'H','-'))
    s.append(L(xa,y,xb,y,INK,3.4)); s.append(atom(xa,y,20,'C')); s.append(atom(xb,y,20,'C'))
    e=f'<g data-chg="230,40,18,P"></g>'+T(230,47,tex='\\mathrm{E}^{+}',size=19,fill='#fff')
    s.append(an('move',e,**{'from':'0,-34','dur':'1.4','rep':'alt','ease':'io'}))
    s.append(A(230,62,230,96,PLUS,3)); s.append(T(258,46,mix='친전자체',size=19,anchor='start',fill=PLUS))
    s.append(T(330,112,mix='π 전자',size=19,anchor='start',fill=FIELD,weight=700)); s.append(T(230,280,mix='π 전자는 σ 결합 위아래로 노출',size=19,fill=MUTED))
    return svg('0 0 480 292',440,'에틸렌의 파이 전자는 시그마 결합 위아래로 노출되어 있어 친전자체가 공격하기 쉽다',s)
FIG['EPI']=epi()

# ═══ S28 에틸렌 첨가 반응 두 줄
def add2():
    s=[]
    def row(y,second):
        g=[]
        g.append(T(80,y,tex='\\ce{CH2}',size=24)); g.append(T(168,y,tex='\\ce{CH2}',size=24))
        for t in (-5,5): g.append(L(108,y-8+t,138,y-8+t,INK,2.6))
        g.append(T(214,y,tex='+',size=24))
        X1='\\mathrm{H}' if not second else '\\mathrm{Br}'
        g.append(T(250,y,tex=X1,size=24)); g.append(L(266 if not second else 272,y-8,298,y-8,INK,2.6)); g.append(T(320,y,tex='\\mathrm{Br}',size=24))
        g.append(curved(123,y-24,248,y-30,bend=-34)); g.append(curved(284,y-1,322,y+8,bend=26))
        g.append(harrow(354,410,y-8))
        g.append(P([(436,y-46),(428,y-46),(428,y+20),(436,y+20)],INK,2.2)); g.append(P([(616,y-46),(624,y-46),(624,y+20),(616,y+20)],INK,2.2))
        if not second:
            g.append(T(474,y,tex='\\ce{CH3}',size=22)); g.append(L(500,y-8,524,y-8,INK,2.4)); g.append(T(548,y,tex='\\ce{CH2}',size=22))
            g.append(C(578,y-30,11,PLUS,1.8,fill='#fff')); g.append(T(578,y-24,tex='+',size=17,fill=PLUS,weight=700))
            g.append(T(596,y+8,tex='',size=10))
        else:
            g.append(T(470,y,tex='\\ce{CH2}',size=22)); g.append(L(496,y-8,532,y-8,INK,2.4)); g.append(T(558,y,tex='\\ce{CH2}',size=22))
            g.append(L(474,y-26,500,y-50,INK,2.2)); g.append(L(556,y-26,530,y-50,INK,2.2)); g.append(T(515,y-50,tex='\\mathrm{Br}',size=20))
            g.append(C(588,y-44,11,PLUS,1.8,fill='#fff')); g.append(T(588,y-38,tex='+',size=17,fill=PLUS,weight=700))
        g.append(T(660,y,tex='\\ce{Br-}',size=22))
        g.append(T(526,y+50,mix='양이온 중간체',size=19,fill=MUTED))
        g.append(curved(660,y+14,560 if not second else 470,y+14,bend=-36))
        g.append(harrow(700,760,y-8))
        if not second: g.append(T(900,y,tex='\\ce{CH3-CH2-Br}',size=24)); g.append(T(900,y+44,mix='브로모에테인',size=19,fill=MUTED))
        else: g.append(T(900,y,tex='\\ce{Br-CH2-CH2-Br}',size=24)); g.append(T(900,y+44,mix='1,2-다이브로모에테인',size=19,fill=MUTED))
        return ''.join(g)
    s.append(step(row(78,False),'r1')); s.append(step(row(220,True),'r2'))
    return svg('0 0 1060 290',1060,'에틸렌에 브로민화 수소와 브로민이 첨가되는 두 단계 반응: 양이온 중간체를 거친다. 굽은 화살표는 전자쌍의 이동',s)
FIG['ADD2']=add2()

# ═══ S29 용접 토치 + 아세틸렌 2번 첨가
def torch():
    s=[]
    s.append(f'<path d="M20 150 L150 132 L160 140 L150 148 L20 166 Z" fill="#8C99A6" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="10" y="146" width="60" height="34" rx="6" fill="#5B6B7F"/>')
    fl=f'<path d="M160 140 C200 118 250 128 300 140 C250 152 200 162 160 140 Z" fill="#FFB547" fill-opacity=".85"/><path d="M160 140 C185 132 210 134 232 140 C210 146 185 148 160 140 Z" fill="#FFF4C2"/>'
    s.append(an('scale',fl,**{'from':'0.85,1','o':'160,140','dur':'.4','rep':'swing','ease':'sine'}))
    s.append(f'<rect x="290" y="168" width="80" height="18" fill="#7E8B98"/>')
    sp=''.join(f'<circle cx="{f(300+12*math.cos(math.radians(a)))}" cy="{f(160-14*math.sin(math.radians(a)))}" r="3" fill="#F2A23A"/>' for a in (40,70,100,130))
    s.append(an('move',sp,**{'from':'-6,10','dur':'.6','rep':'loop'}))
    s.append(T(195,214,mix='아세틸렌의 고온 불꽃',size=19,fill=MUTED))
    return svg('0 0 390 226',360,'아세틸렌의 고온 불꽃으로 금속을 용접하는 모습',s)
FIG['TORCH']=torch()
def acadd():
    s=[]; S=24; y=86
    a=[Cc(70,y),Cc(118,y),H_(20,y),H_(168,y)]
    s.append(LW(a,[(0,1,3,'l'),(0,2,1,'l'),(1,3,1,'l')],S=S,name='아세틸렌3'))
    s.append(harrow(196,262,y-4,lab='\\ce{HBr}' and '$\\ce{HBr}$'))
    x=330; a=[Cc(x,y),Cc(x+50,y),H_(x-40,y-30),H_(x-40,y+30),H_(x+90,y-30),A_('Br',x+90,y+34,lp=['r','d','u'])]
    s.append(step(LW(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],S=S,name='브로모에틸렌'),'ac1'))
    s.append(step(T(355,170,mix='브로모에틸렌',size=19,fill=MUTED),'ac1'))
    s.append(step(harrow(470,536,y-4,lab='$\\ce{HBr}$'),'ac2'))
    x=610; d=46; a=[Cc(x,y),Cc(x+d,y),H_(x,y-d),H_(x,y+d),H_(x-d,y),A_('Br',x+d,y-d-6,lp=['u','l','r']),A_('Br',x+d,y+d+6,lp=['d','l','r']),H_(x+2*d,y)]
    s.append(step(LW(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(1,5,1,'l'),(1,6,1,'l'),(1,7,1,'l')],S=S,name='다이브로모'),'ac2'))
    s.append(step(T(632,176,mix='1,1-다이브로모에테인',size=19,fill=MUTED),'ac2'))
    return svg('0 0 740 190',700,'아세틸렌에 브로민화 수소가 두 번 첨가되어 브로모에틸렌을 거쳐 1,1-다이브로모에테인이 된다',s)
FIG['ACADD']=acadd()

# ═══ S35 C4H8 알켄 4가지
def q2fig():
    s=[]; items=[(['H','H','H','CH2CH3'],'1-뷰텐',()),(['H3C','H','CH3','H'],'시스-2-뷰텐',(0,2)),(['H3C','H','H','CH3'],'트랜스-2-뷰텐',(0,3)),(['H','H','CH3','CH3'],'2-메틸프로펜',(2,3))]
    for i,(sb,nm,hl) in enumerate(items):
        x=130+i*250 if i<4 else 0
        s.append(step(alkene(x,80,sb,S=22,hl=hl)+T(x,180,mix=nm,size=19,fill=MUTED),f'q2{i}'))
    return svg('0 0 1000 194',960,'분자식이 C4H8인 사슬 모양 알켄 4가지: 1-뷰텐, 시스-2-뷰텐, 트랜스-2-뷰텐, 2-메틸프로펜',s)
FIG['Q2FIG']=q2fig()
# ═══ S36 C6H14 이성질체 5가지(탄소 골격)
C6=[('헥세인',69,[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0)],6,[]),('2-메틸펜테인',60,[(0,0),(1,0),(2,0),(3,0),(4,0),(1,-1)],5,[2]),('3-메틸펜테인',63,[(0,0),(1,0),(2,0),(3,0),(4,0),(2,-1)],5,[3]),
    ('2,3-다이메틸뷰테인',58,[(0,0),(1,0),(2,0),(3,0),(1,-1),(2,1)],4,[2,3]),('2,2-다이메틸뷰테인',50,[(0,0),(1,0),(2,0),(3,0),(1,-1),(1,1)],4,[2,2])]
assert len({cells_canon(c) for _,_,c,_,_ in C6})==5
for _,_,c,Ln,br in C6: assert cells_canon(c)==canon_edges(*skel(Ln,br)[:2])
def q3fig():
    s=[]
    for i,(nm,bp,cells,_,_) in enumerate(C6):
        x0=40+i*212; w=max(a for a,b in cells)*40
        s.append(step(skelC(x0+(170-w)/2,70,cells,r=13,d=40)+T(x0+85,148,mix=nm,size=19)+T(x0+85,176,mix=f'끓는점 {bp} °C',size=19,fill=MUTED),f'q3{i}'))
    return svg('0 0 1100 190',1060,'C6H14의 구조 이성질체 5가지 탄소 골격과 끓는점',s)
FIG['Q3FIG']=q3fig()

# ═════ 실험실 자료 ═════
NAMES={4:[(4,[],'뷰테인','CH3CH2CH2CH3',-0.5),(3,[2],'2-메틸프로페인','CH3CH(CH3)CH3',-12)],
       5:[(5,[],'펜테인','CH3CH2CH2CH2CH3',36),(4,[2],'2-메틸뷰테인','CH3CH(CH3)CH2CH3',28),(3,[2,2],'2,2-다이메틸프로페인','C(CH3)4',10)],
       6:[(6,[],'헥세인','CH3CH2CH2CH2CH2CH3',69),(5,[2],'2-메틸펜테인','CH3CH(CH3)CH2CH2CH3',60),(5,[3],'3-메틸펜테인','CH3CH2CH(CH3)CH2CH3',63),(4,[2,2],'2,2-다이메틸뷰테인','CH3C(CH3)2CH2CH3',50),(4,[2,3],'2,3-다이메틸뷰테인','CH3CH(CH3)CH(CH3)CH3',58)]}
def r3(v): return [round(c,3) for c in v]
DB={}
for n,lst in NAMES.items():
    for Ln,br,nm,tx,bp in lst:
        at,bd=build3d(Ln,br); key=canon_edges(*skel(Ln,br)[:2])
        DB[key]={'n':n,'name':nm,'tex':'\\ce{'+tx+'}','br':len(br),'bp':bp,'atoms':[[e,r3(p)] for e,p in at],'bonds':[[a,b,o] for a,b,o in bd]}
    assert {k for k,v in DB.items() if v['n']==n}==set(_lv[n].keys())
def side_of(at,bd,a,b):
    adj={}
    for i,j,_ in bd: adj.setdefault(i,[]).append(j); adj.setdefault(j,[]).append(i)
    seen={b}; st=[b]
    while st:
        v=st.pop()
        for w in adj[v]:
            if w!=a and w not in seen: seen.add(w); st.append(w)
    seen.discard(b); return sorted(seen)
BU={}
for key,cis in (('cis',True),('trans',False)):
    at,bd,side=butene(cis); ctr=v_mul(tuple(sum(p[m] for _,p in at) for m in range(3)),1/len(at))
    assert sorted(side)==side_of(at,bd,1,2)
    BU[key]={'atoms':[[e,r3(v_sub(p,ctr))] for e,p in at],'bonds':[[a,b,o] for a,b,o in bd],'side':side,'ax':[1,2]}
at,bd=build3d(4,[]); BU['butane']={'atoms':[[e,r3(p)] for e,p in at],'bonds':[[a,b,o] for a,b,o in bd],'side':side_of(at,bd,1,2),'ax':[1,2]}
data='const DB='+json.dumps(DB,ensure_ascii=False,separators=(',',':'))+';\n    const BU='+json.dumps(BU,ensure_ascii=False,separators=(',',':'))+';'
lt=open(os.path.join(HERE,'labs_tpl.js'),encoding='utf-8').read()
assert '/*@@DATA@@*/' in lt
open(OUTLAB,'w',encoding='utf-8').write(lt.replace('/*@@DATA@@*/',data))

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused)
