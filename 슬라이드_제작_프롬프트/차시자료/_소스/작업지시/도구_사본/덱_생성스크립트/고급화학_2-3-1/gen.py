# -*- coding: utf-8 -*-
"""고급화학 2-3-1 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   labs_src.js·extra_src.css를 덱 폴더에 labs.js·extra.css로 복사한다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)"""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
sys.path.insert(0,os.path.join(os.path.dirname(HERE),'고급화학_2-2-1'))
from h import *          # 그림 도우미(2-2-1 h.py: T, A, L, P, C, R, svg, Ax …)
from cells import *      # 결정 좌표·투영(이 덱)
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
OUT=BASE+'2-3-1_고체_결정의_종류와_특성/'
assert OUT.endswith('/고급화학/2-3-1_고체_결정의_종류와_특성/'), OUT
FIG={}
YAW,PITCH=28,18          # 실험실 처음 각도와 같음
POS={'꼭짓점':('#4F86C6','#2F5F98'),'면 중심':('#E8A33D','#A8701A'),'체심':('#C0504D','#86302E'),'내부':('#C0504D','#86302E'),'모서리':('#7AA95C','#4F7A36')}
MET=('#9AA9BA','#5C6F82')
ION={'Cl':('#4CAF50','#2E7D32'),'Na':('#8E5BD0','#5E3A96'),'Cs':('#7A4FC0','#4E2F8A'),'Zn':('#8FA3B8','#5C6F82'),'S':('#E8C547','#A88A1E'),'Ti':('#B8BEC6','#6E7883'),'O':('#E5533D','#A8321F'),'C':('#3A3F47','#1C1F24')}
def ball(x,y,r,col,extra='',ghost=False):
    f_,s_=col
    if ghost: return f'<g opacity=".45"{(" "+extra) if extra else ""}>'+C(x,y,r,s_,1.6,f_,'4 3')+'</g>'
    return f'<g{(" "+extra) if extra else ""}>'+C(x,y,r,s_,1.6,f_)+f'<ellipse cx="{f(x-.33*r)}" cy="{f(y-.36*r)}" rx="{f(.32*r)}" ry="{f(.22*r)}" fill="#fff" opacity=".55"/></g>'
def cell3d(key,ox,oy,S,rad,colmode='pos',yaw=YAW,pitch=PITCH,coord=False,coord_step=None,pop=False,extra_atoms=None,hide_cell=False):
    """단위세포 그림. rad: 종류별 표시 반지름(모서리 1 기준). colmode 'pos'(자리 색)|'ion'(이온 색)|'met'(한 색).
       coord=True → CENTER 원자 둘레 테 + 이웃 연결선(field), 칸 밖 이웃은 흐린 점선 공."""
    if key=='hcp': V,E,F=hex_frame(); ctr=(0,0,CH/2)
    else:
        cz=CUBIC.get(key,{}).get('c',1.0); V,E,F=cube_frame(cz); ctr=(.5,.5,cz/2)
    pr=lambda p: rot(p,yaw,pitch,ctr)
    sc=lambda p: (ox+pr(p)[0]*S, oy-pr(p)[2]*S)
    hid=edge_hidden(E,F,yaw,pitch); items=[]
    if not hide_cell:
        for (i,j),hh in zip(E,hid):
            (x1,y1),(x2,y2)=sc(V[i]),sc(V[j]); dep=(pr(V[i])[1]+pr(V[j])[1])/2
            items.append((100+dep+(0.6 if hh else 0),L(x1,y1,x2,y2,MUTED if hh else INK,1.5 if hh else 2,'5 4' if hh else None)))
    atoms=[(p,t,pl) for p,t,w,pl in cell_atoms(key)] if key in CUBIC or key=='hcp' else []
    if extra_atoms: atoms+=extra_atoms
    ghosts=[]; cen=None
    if coord:
        cp,ct=CENTER[key]; d,nb=neighbors(key,cp,ct); cen=cp
        inset=lambda p:any(math.dist(p,q)<1e-6 for q,_,_ in atoms)
        for p,t in nb:
            if not inset(p): ghosts.append((p,t))
        lines=[]
        for p,t in nb:
            (x1,y1),(x2,y2)=sc(cp),sc(p)
            lines.append(((pr(cp)[1]+pr(p)[1])/2,L(x1,y1,x2,y2,FIELD,3.5,extra='stroke-linecap="round"')))
        if coord_step: items+=[(dp,f'<g class="step" data-g="{coord_step}">{s}</g>') for dp,s in lines]
        else: items+=lines
    k=0; order=sorted(range(len(atoms)),key=lambda i:-pr(atoms[i][0])[1])
    for p,t,pl in atoms:
        x,y=sc(p); r=rad.get(t,.12)*S
        col=POS.get(pl,MET) if colmode=='pos' else ION.get(t,MET) if colmode=='ion' else MET
        ex=''
        if pop: ex=f'data-anim="pop" data-dur=".5" data-delay="{f(0.08*order.index(atoms.index((p,t,pl))))}"'
        s=ball(x,y,r,col,ex)
        if coord and math.dist(p,cen)<1e-6:
            s+=C(x,y,r+5,FIELD,3.5) if not coord_step else f'<g class="step" data-g="{coord_step}">'+C(x,y,r+5,FIELD,3.5)+'</g>'
        items.append((pr(p)[1],s))
    for p,t in ghosts:
        x,y=sc(p); r=rad.get(t,.12)*S
        col=MET if colmode!='ion' else ION.get(t,MET)
        g=ball(x,y,r,col,ghost=True)
        items.append((pr(p)[1],g if not coord_step else f'<g class="step" data-g="{coord_step}">{g}</g>'))
    items.sort(key=lambda it:-it[0])
    return ''.join(s for _,s in items),sc
def leg_pos(x,y,keys,size=18,gap=120):
    s=[]
    for i,k in enumerate(keys):
        s.append(ball(x+i*gap,y,9,POS[k])+T(x+i*gap+16,y+6,mix=k,size=size,anchor='start'))
    return ''.join(s)
def leg_ion(x,y,ions,size=20,gap=110,r=10):
    s=[]
    for i,(t,tex) in enumerate(ions):
        s.append(ball(x+i*gap,y,r,ION[t])+T(x+i*gap+r+6,y+7,tex=tex,size=size,anchor='start'))
    return ''.join(s)
RM={'M':.13}

# ═════════ 1. 표지 ═════════
def cover():
    rad={'Cl':.17,'Na':.09}
    body,_=cell3d('nacl',230,200,205,rad,'ion',pop=True)
    s=[body,leg_ion(130,418,[('Na','\\ce{Na+}'),('Cl','\\ce{Cl-}')],size=22,gap=130,r=12)]
    return svg((460,440),430,'염화 나트륨 결정의 단위세포',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════════ 2. 중단원 도입: 눈 결정 ═════════
def snow():
    cx,cy=170,170; s=[]
    arm=[]
    for k in range(6):
        a=math.radians(60*k-90); ux,uy=math.cos(a),math.sin(a)
        arm.append(L(cx+ux*18,cy+uy*18,cx+ux*140,cy+uy*140,'#4F86C6',7,extra='stroke-linecap="round"'))
        for t,ln in ((60,36),(95,28),(122,16)):
            bx,by=cx+ux*t,cy+uy*t
            for sg in (-1,1):
                b=a+sg*math.radians(60)
                arm.append(L(bx,by,bx+math.cos(b)*ln,by+math.sin(b)*ln,'#4F86C6',5,extra='stroke-linecap="round"'))
    hexa=[(cx+20*math.cos(math.radians(60*k)),cy+20*math.sin(math.radians(60*k))) for k in range(6)]
    s.append(f'<g data-anim="rot" data-from="-30" data-o="{cx},{cy}" data-dur="2.4" data-ease="out">'+''.join(arm)+P(hexa,'#2F5F98',4,'#DDEEF8',close=True)+'</g>')
    s.append(T(cx,cy+178,mix='눈 결정 — 육각형 대칭',size=19,fill=MUTED))
    return svg((340,360),300,'눈 결정의 육각형 대칭',s)
FIG['SNOW']=snow()

# ═════════ 4. 생각 열기: 소금 알갱이 ═════════
def salt():
    s=[]
    # 소금 알갱이(정육면체)
    V,E,F=cube_frame(); hid=edge_hidden(E,F,YAW,PITCH)
    sc=lambda p:(110+rot(p,YAW,PITCH,(.5,.5,.5))[0]*120,170-rot(p,YAW,PITCH,(.5,.5,.5))[2]*120)
    faces=[(n,sv) for n,sv in F if rot(n,YAW,PITCH,(0,0,0))[1]<0]
    shade={0:'#F4F7FB',1:'#E6ECF3',2:'#D7DFE9'}
    for i,(n,sv) in enumerate(faces):
        pts=[sc(V[j]) for j in sv]
        cx_=sum(p[0] for p in pts)/4; cy_=sum(p[1] for p in pts)/4
        pts.sort(key=lambda p:math.atan2(p[1]-cy_,p[0]-cx_))
        s.append(P(pts,'#8C99A6',2,shade[i%3],close=True))
    s.append(T(110,272,mix='소금 알갱이(돋보기)',size=19,fill=MUTED))
    # 확대 원
    s.append(L(160,130,300,80,MUTED,1.5,'5 4')); s.append(L(160,200,300,250,MUTED,1.5,'5 4'))
    s.append(C(400,165,105,INK,2.5,'#FFFFFF'))
    g=[]
    for i in range(-4,5):
        for j in range(-4,5):
            x,y=400+i*26,165+j*26
            if math.hypot(x-400,y-165)>92: continue
            if (i+j)%2==0: g.append(C(x,y,12,'#2E7D32',1.4,'#4CAF50'))
            else: g.append(C(x,y,7,'#5E3A96',1.4,'#8E5BD0'))
    s.append('<g data-anim="pop" data-dur=".8" data-o="400,165">'+''.join(g)+'</g>')
    s.append(leg_ion(320,300,[('Na','\\ce{Na+}'),('Cl','\\ce{Cl-}')],size=20,gap=110,r=9))
    return svg((520,320),500,'소금 알갱이와 그 속의 이온 배열',s)
FIG['SALT']=salt()

# ═════════ 5. 결정성·비결정성 ═════════
def crys():
    s=[]; rnd=random.Random(7)
    def net(x0,y0,ordered):
        pts=[]
        for j in range(5):
            for i in range(6):
                x=x0+i*36+(18 if j%2 else 0); y=y0+j*31
                if not ordered: x+=rnd.uniform(-11,11); y+=rnd.uniform(-10,10)
                pts.append((x,y))
        o=[]
        for a in range(len(pts)):
            for b in range(a+1,len(pts)):
                d=math.dist(pts[a],pts[b])
                if d<(40 if ordered else 44): o.append(L(*pts[a],*pts[b],'#9AA5B1',3))
        for k,(x,y) in enumerate(pts):
            o.append(f'<g data-anim="move" data-from="{rnd.choice((-2,2))},{rnd.choice((-2,2))}" data-rep="swing" data-dur="{f(.3+.2*rnd.random())}">'+C(x,y,9,'#5C6F82',1.5,'#9AA9BA')+'</g>')
        return ''.join(o)
    s.append(net(30,40,True)); s.append(net(290,40,False))
    s.append(T(130,215,mix='결정성 고체',size=21,weight=700)); s.append(T(130,240,mix='(예: 수정, 소금)',size=19,fill=MUTED))
    s.append(T(390,215,mix='비결정성 고체',size=21,weight=700)); s.append(T(390,240,mix='(예: 유리, 플라스틱)',size=19,fill=MUTED))
    return svg((520,255),500,'결정성 고체와 비결정성 고체의 입자 배열',s)
FIG['CRYS']=crys()

# ═════════ 6. 결정의 종류 아이콘 ═════════
def icon(kind):
    s=[]
    if kind=='ion':
        for i in range(4):
            for j in range(3):
                sg='+' if (i+j)%2 else '-'
                s.append(f'<g data-chg="{20+i*30},{18+j*30},{11 if sg=="+" else 13},{sg}"></g>')
    elif kind=='met':
        s.append(R(4,3,112,90,'none',0,'#E3EEFB',8))
        for i in range(4):
            for j in range(3): s.append(f'<g data-chg="{20+i*27},{18+j*28},11,+"></g>')
        rnd=random.Random(3)
        for k in range(9): s.append(C(rnd.uniform(12,108),rnd.uniform(10,86),3.5,MINUS,0,MINUS))
    elif kind=='cov':
        pts=[(16+i*28+(14 if j%2 else 0),16+j*26) for j in range(4) for i in range(4)]
        for a in range(len(pts)):
            for b in range(a+1,len(pts)):
                if math.dist(pts[a],pts[b])<30: s.append(L(*pts[a],*pts[b],'#9AA5B1',3))
        for x,y in pts: s.append(C(x,y,7,'#1C1F24',1,'#3A3F47'))
    else:
        for i in range(3):
            for j in range(2):
                x,y=22+i*38,26+j*44; s.append(L(x-8,y,x+8,y,'#9AA5B1',4)); s.append(C(x-9,y,8,'#A8321F',1.2,'#E5533D')); s.append(C(x+9,y,8,'#A8321F',1.2,'#E5533D'))
        for i in range(2): s.append(L(42+i*38,26,42+i*38+0.1,70,MUTED,2,'4 4'))
        s.append(L(31,26,51,26,MUTED,2,'4 4')); s.append(L(69,70,89,70,MUTED,2,'4 4'))
    return svg((120,96),110,{'ion':'이온 결정','met':'금속 결정','cov':'공유 결정','mol':'분자 결정'}[kind]+' 모형',s,'fig ac231-ico')
for k in ('ion','met','cov','mol'): FIG['ICO_'+k.upper()]=icon(k)

# ═════════ 7. X선 회절 실험 ═════════
def xrd():
    s=[]
    s.append(R(20,95,120,70,INK,2.5,'#F1F3F5',8)); s.append(T(80,190,mix='X선관',size=20))
    s.append(A(36,112,104,112,'minus',2.5)); s.append(T(70,148,mix='전자 빔',size=18,fill=MINUS))
    s.append(R(205,60,14,70,INK,0,'#5B6B7F')); s.append(R(205,140,14,70,INK,0,'#5B6B7F')); s.append(T(212,232,mix='납 스크린',size=19))
    s.append(f'<g data-anim="draw" data-dur=".8">'+L(140,135,320,135,PLUS,4)+'</g>'); s.append(T(170,122,mix='X선',size=19,fill=PLUS))
    # 결정
    s.append(f'<g data-anim="rot" data-from="-40" data-o="335,135" data-dur="1.6" data-rep="alt">'+P([(335,108),(362,135),(335,162),(308,135)],'#2F5F98',2.5,'#C9DDF2',close=True)+'</g>')
    s.append(T(335,192,mix='결정',size=19))
    # 필름
    s.append(f'<path d="M520 30 Q560 135 520 240" fill="none" stroke="{INK}" stroke-width="6"/>'); s.append(T(520,268,mix='사진 필름',size=19))
    spots=[(-90,50),(-55,40),(-25,32),(0,26),(25,32),(55,40),(90,50)]
    for i,(dy,dx) in enumerate(spots):
        y=135+dy; xf=520+40*(1-((y-135)/105)**2)-2
        if dy!=0: s.append(f'<g data-anim="draw" data-dur=".6" data-delay="{f(.6+.08*i)}">'+L(362,135,xf,y,PLUS,1.8,'6 4')+'</g>')
        s.append(f'<g data-anim="pop" data-dur=".4" data-delay="{f(1.0+.08*i)}">'+C(xf,y,6 if dy else 8,INK,0,INK)+'</g>')
    s.append(L(362,135,556,135,PLUS,2))
    return svg((600,285),560,'X선 회절 실험 장치',s)
FIG['XRD']=xrd()

# ═════════ 8. 브래그 법칙 ═════════
def bragg():
    s=[]; th=math.radians(30); d=110; y1=150; y2=y1+d; px=300
    for yy in (y1,y2,y2+d*0.0):
        pass
    for yy in (y1,y2):
        s.append(L(40,yy,540,yy,MUTED,1.5,'3 4'))
        for i in range(-5,6): s.append(C(px+i*50,yy,14,'#5C6F82',1.5,'#9AA9BA'))
    u=(math.cos(th),math.sin(th)); v=(math.cos(th),-math.sin(th)); a=d*math.sin(th)
    P1=(px,y1); Q=(px,y2)
    M=(Q[0]-a*u[0],Q[1]-a*u[1]); N=(Q[0]+a*v[0],Q[1]+a*v[1])
    Lr=230
    # 입사·반사 광선
    s.append(A(P1[0]-Lr*u[0],P1[1]-Lr*u[1],P1[0]-6*u[0],P1[1]-6*u[1],'plus',3))
    s.append(A(P1[0],P1[1],P1[0]+Lr*0.85*v[0],P1[1]+Lr*0.85*v[1],'plus',3))
    s.append(A(Q[0]-(Lr+a)*u[0],Q[1]-(Lr+a)*u[1],Q[0]-6*u[0],Q[1]-6*u[1],'plus',3))
    s.append(A(Q[0],Q[1],Q[0]+(Lr*0.85+a+40)*v[0],Q[1]+(Lr*0.85+a+40)*v[1],'plus',3))
    s.append(T(P1[0]-Lr*u[0]+12,P1[1]-Lr*u[1]-8,mix='X선',size=20,fill=PLUS,anchor='start'))
    # 파면(점선) PM, PN
    s.append(L(*P1,*M,MUTED,2,'5 4')); s.append(L(*P1,*N,MUTED,2,'5 4'))
    # 경로 차이 a, a
    s.append(f'<g class="step" data-g="b1">'+L(*M,*Q,EQUI,6,extra='stroke-linecap="round"')+L(*Q,*N,EQUI,6,extra='stroke-linecap="round"')+T((M[0]+Q[0])/2-14,(M[1]+Q[1])/2+6,tex='a',size=24,fill=EQUI,anchor='end',halo=True)+T((Q[0]+N[0])/2+14,(Q[1]+N[1])/2+6,tex='a',size=24,fill=EQUI,anchor='start',halo=True)+'</g>')
    # d 치수
    s.append(L(560,y1,560,y2,INK,1.5)); s.append(L(552,y1,568,y1,INK,1.5)); s.append(L(552,y2,568,y2,INK,1.5)); s.append(T(574,(y1+y2)/2+8,tex='d',size=24,anchor='start'))
    s.append(L(px,y1,px,y2,MUTED,1.5,'2 3'))
    # θ 호
    r=46; s.append(P([(P1[0]-r*math.cos(t_),P1[1]-r*math.sin(t_)) for t_ in [th*i/12 for i in range(13)]],INK,1.8))
    s.append(T(P1[0]-r-24,P1[1]-6,tex='\\theta',size=22))
    s.append(T(px+80,(y1+y2)/2+30,tex='\\theta',size=20,fill=MUTED))
    s.append(T(48,y2+28,mix='원자 면',size=18,fill=MUTED,anchor='start'))
    return svg((620,300),580,'결정 층에 의한 X선의 회절과 경로 차이',s)
FIG['BRAGG']=bragg()

# ═════════ 9. 다이아몬드·흑연 ═════════
def diag():
    s=[]
    # 다이아몬드: 면심 입방 + 사면체 자리 4
    cand=[p for p,t in cubic_sites('fcc')]; cand+= [(x+.25,y+.25,z+.25) for x,y,z in cand]
    c0=(.25,.25,.25); at=[p for p in cand if math.dist(p,c0)<.72]
    ctr=c0; S=190; ox,oy=140,150
    pr=lambda p:rot(p,YAW,PITCH,ctr); sc=lambda p:(ox+pr(p)[0]*S,oy-pr(p)[2]*S)
    items=[]
    for i in range(len(at)):
        for j in range(i+1,len(at)):
            if abs(math.dist(at[i],at[j])-math.sqrt(3)/4)<1e-6:
                items.append(((pr(at[i])[1]+pr(at[j])[1])/2,L(*sc(at[i]),*sc(at[j]),'#9AA5B1',6,extra='stroke-linecap="round"')))
    for p in at: items.append((pr(p)[1],ball(*sc(p),11,ION['C'])))
    items.sort(key=lambda it:-it[0]); s.append('<g data-anim="pop" data-dur=".9" data-o="140,150">'+''.join(x for _,x in items)+'</g>')
    s.append(T(140,300,mix='다이아몬드',size=21,weight=700)); s.append(T(140,324,mix='원자마다 공유 결합 4개(입체 그물)',size=18,fill=MUTED))
    # 흑연: 벌집 층 3장
    def honey():
        pts=[]
        for i in range(-3,4):
            for j in range(-3,4):
                for b in ((0,0),(.5,.5/math.sqrt(3))):
                    x=i+j*.5+b[0]; y=j*math.sqrt(3)/2+b[1]
                    if math.hypot(x,y)<1.8: pts.append((x*.95,y*.95))
        return pts
    hp=honey(); items=[]; S2=62; ox2,oy2=440,150
    for k,z in enumerate((-1.55,0,1.55)):
        off=(0,0) if k%2==0 else (.55,0)
        P3=[(x+off[0],y+off[1],z) for x,y in hp]
        pr2=lambda p:rot(p,20,22,(0,0,0)); sc2=lambda p:(ox2+pr2(p)[0]*S2,oy2-pr2(p)[2]*S2)
        for i in range(len(P3)):
            for j in range(i+1,len(P3)):
                if abs(math.dist(P3[i],P3[j])-.95/math.sqrt(3))<1e-3:
                    items.append(((pr2(P3[i])[1]+pr2(P3[j])[1])/2,L(*sc2(P3[i]),*sc2(P3[j]),'#9AA5B1',4)))
        for p in P3: items.append((pr2(p)[1],ball(*sc2(p),5.5,ION['C'])))
    items.sort(key=lambda it:-it[0]); s.append(''.join(x for _,x in items))
    s.append(A(578,132,578,80,'muted',2,True)); s.append(A(578,80,578,132,'muted',2,True))
    s.append(T(588,100,mix='약한||결합력',size=18,fill=MUTED,anchor='start'))
    s.append(T(440,300,mix='흑연',size=21,weight=700)); s.append(T(440,324,mix='판 안: 공유 결합 · 판 사이: 약한 힘',size=18,fill=MUTED))
    return svg((640,340),600,'다이아몬드와 흑연의 구조',s)
FIG['DIAG']=diag()

# ═════════ 10. 녹는점 막대 ═════════
def mpbar():
    data=[('철',1538,'met'),('구리',1085,'met'),('염화||나트륨',801,'ion'),('질산||칼륨',334,'ion'),('나프탈렌',80,'mol'),('얼음',0,'mol')]
    col={'met':('#8FA3B8','금속 결정'),'ion':('#8E5BD0','이온 결정'),'mol':('#5FA8D3','분자 결정')}
    ax=Ax(80,300,440,250,6,1600); s=[]
    for v in (0,400,800,1200,1600):
        s.append(L(80,ax.Y(v),520,ax.Y(v),'#E2E7EC',1)); s.append(T(70,ax.Y(v)+6,mix=str(v),size=18,anchor='end'))
    s.append(L(80,300,524,300,MUTED,2)); s.append(L(80,300,80,40,MUTED,2))
    for i,(n,v,k) in enumerate(data):
        x=100+i*70; h=max(3,300-ax.Y(v))
        s.append(f'<g data-anim="scale" data-from="1,0" data-o="{x+22},300" data-dur=".9" data-delay="{f(.1*i)}">'+R(x,300-h,44,h,'none',0,col[k][0],3)+'</g>')
        s.append(T(x+22,300-h-8,mix=str(v),size=18))
        s.append(T(x+22,324,mix=n,size=18))
    s.append(T(90,30,mix='녹는점 (°C)',size=19,anchor='start',fill=MUTED))
    for i,k in enumerate(('met','ion','mol')):
        s.append(R(200+i*105,16,18,18,'none',0,col[k][0],3)); s.append(T(224+i*105,32,mix=col[k][1],size=18,anchor='start'))
    return svg((540,375),500,'결정의 종류에 따른 녹는점',s)
FIG['MPBAR']=mpbar()

# ═════════ 11. 결정격자와 단위세포 ═════════
def latt():
    s=[]; S=82; ox,oy=170,175; ctr=(1,1,1)
    pr=lambda p:rot(p,YAW,PITCH,ctr); sc=lambda p:(ox+pr(p)[0]*S,oy-pr(p)[2]*S)
    items=[]
    import itertools as it
    pts=list(it.product(range(3),repeat=3))
    for p in pts:
        for q in pts:
            if p<q and sum(abs(a-b) for a,b in zip(p,q))==1:
                incell=all(c<=1 for c in p+q)
                items.append(((pr(p)[1]+pr(q)[1])/2-(0.01 if incell else 0),L(*sc(p),*sc(q),INK if incell else '#B7C1CC',3 if incell else 1.5)))
    for p in pts: items.append((pr(p)[1],C(*sc(p),7,'#2F5F98',1.2,'#4F86C6')))
    items.sort(key=lambda t:-t[0]); s.append(''.join(x for _,x in items))
    s.append(T(170,350,mix='결정격자',size=20,weight=700))
    # 단위세포 한 개
    V,E,F=cube_frame(); hid=edge_hidden(E,F,YAW,PITCH); S2=130; ox2,oy2=460,180
    sc2=lambda p:(ox2+rot(p,YAW,PITCH,(.5,.5,.5))[0]*S2,oy2-rot(p,YAW,PITCH,(.5,.5,.5))[2]*S2)
    g=[]
    for (i,j),hh in zip(E,hid): g.append(L(*sc2(V[i]),*sc2(V[j]),MUTED if hh else INK,1.5 if hh else 3,'5 4' if hh else None))
    for p in V: g.append(C(*sc2(p),7,'#2F5F98',1.2,'#4F86C6'))
    s.append('<g data-anim="move" data-from="-120,0" data-dur="1.2" data-ease="out">'+''.join(g)+'</g>')
    a0,a1,a2=sc2((0,0,0)),sc2((1,0,0)),sc2((0,0,1))
    s.append(T((a0[0]+a1[0])/2,(a0[1]+a1[1])/2+30,tex='a',size=22)); s.append(T(a0[0]-16,(a0[1]+a2[1])/2+6,tex='a',size=22,anchor='end'))
    b1=sc2((1,1,0)); s.append(T((a1[0]+b1[0])/2+16,(a1[1]+b1[1])/2+24,tex='a',size=22))
    s.append(T(a0[0]+26,a0[1]-12,mix='90°',size=18,fill=MUTED,anchor='start'))
    s.append(T(460,350,mix='단위세포(입방 정계)',size=20,weight=700))
    s.append(A(300,180,360,180,'muted',2.5))
    return svg((600,365),560,'결정격자와 단위세포',s)
FIG['LATT']=latt()

# ═════════ 12. 입방 정계 3가지 ═════════
def cub3(coord=False):
    s=[]; names=[('sc','단순 입방'),('bcc','체심 입방'),('fcc','면심 입방')]
    for i,(k,n) in enumerate(names):
        b,_=cell3d(k,130+i*250,140,112,RM,'pos' if not coord else 'met',pop=not coord,coord=coord,coord_step=(f'c{i}' if coord else None))
        s.append(b); s.append(T(130+i*250,262,mix=n,size=21,weight=700))
    if not coord: s.append(leg_pos(120,302,['꼭짓점','체심','면 중심'],gap=150)+T(560,308,mix='색은 위치 구분 — 같은 원자',size=18,fill=MUTED,anchor='start'))
    return svg((760,320 if not coord else 285),740,'입방 정계의 세 가지 단위세포'+(' 배위수' if coord else ''),s)
FIG['CUB3']=cub3()
def coord3():
    s=[]; names=[('sc','단순 입방','6'),('bcc','체심 입방','8'),('fcc','면심 입방','12')]
    for i,(k,n,cn) in enumerate(names):
        oy=180 if k!='fcc' else 190
        b,_=cell3d(k,140+i*235,oy,112 if k!='fcc' else 104,RM,'met',coord=True,coord_step=f'c{i}')
        s.append(b); s.append(T(140+i*235,320,mix=n,size=21,weight=700))
        s.append(f'<g class="step" data-g="c{i}">'+T(140+i*235,348,mix=f'배위수 {cn}',size=21,fill=FIELD,weight=700)+'</g>')
    return svg((800,375),740,'세 단위세포에서 가운데 원자의 배위수',s)
FIG['COORD3']=coord3()

# ═════════ 13. 꼭짓점 공유 ═════════
def share():
    s=[]; S=92; ox,oy=200,170; ctr=(1,1,1)
    pr=lambda p:rot(p,YAW,PITCH,ctr); sc=lambda p:(ox+pr(p)[0]*S,oy-pr(p)[2]*S)
    import itertools as it
    pts=list(it.product(range(3),repeat=3)); items=[]
    for p in pts:
        for q in pts:
            if p<q and sum(abs(a-b) for a,b in zip(p,q))==1:
                items.append(((pr(p)[1]+pr(q)[1])/2,L(*sc(p),*sc(q),'#8C99A6',2)))
    items.append((pr((1,1,1))[1]-0.01,f'<g data-anim="pop" data-dur=".8" data-o="{f(sc((1,1,1))[0])},{f(sc((1,1,1))[1])}">'+ball(*sc((1,1,1)),26,POS['꼭짓점'])+'</g>'))
    items.sort(key=lambda t:-t[0]); s.append(''.join(x for _,x in items))
    s.append(T(200,350,mix='꼭짓점 원자 하나를 단위세포 8개가 나눔',size=19,fill=MUTED))
    return svg((400,365),380,'꼭짓점 원자를 여덟 단위세포가 나누어 가짐',s)
FIG['SHARE']=share()

# ═════════ 15. a와 r ═════════
def ar3():
    s=[]; defs=['<defs>']
    def sq(x0,y0,w,h,idn):
        defs.append(f'<clipPath id="clip-ac231-15{idn}"><rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}"/></clipPath>')
        return f'clip-path="url(#clip-ac231-15{idn})"'
    A_=150
    # 단순 입방
    x0,y0=30,60; r=A_/2; cp=sq(x0,y0,A_,A_,'a')
    for cx,cy in ((x0,y0),(x0+A_,y0),(x0,y0+A_),(x0+A_,y0+A_)):
        s.append(f'<g {cp}>'+C(cx,cy,r,'#2F5F98',1.8,'#4F86C6')+'</g>')
    s.append(R(x0,y0,A_,A_,INK,2.5)); s.append(T(x0+A_/2,y0+A_+32,tex='a=2r',size=22)); s.append(T(x0+A_/2,y0-16,tex='a',size=22))
    c45=r/math.sqrt(2); s.append(L(x0+A_,y0+A_,x0+A_-c45,y0+A_-c45,INK,2)); s.append(T(x0+A_-c45/2-8,y0+A_-c45/2-4,tex='r',size=20,anchor='end',halo=True))
    s.append(T(x0+A_/2,y0+A_+64,mix='단순 입방: 모서리',size=19,fill=MUTED))
    # 체심 입방: 대각면 a × √2a
    x1,y1=250,60; W=A_*math.sqrt(2)*0.82; H=A_*0.82; r=math.sqrt(W*W+H*H)/4; cp=sq(x1,y1,W,H,'b')
    for cx,cy in ((x1,y1),(x1+W,y1),(x1,y1+H),(x1+W,y1+H),(x1+W/2,y1+H/2)):
        s.append(f'<g {cp}>'+C(cx,cy,r,'#2F5F98' if (cx,cy)!=(x1+W/2,y1+H/2) else '#86302E',1.8,'#4F86C6' if (cx,cy)!=(x1+W/2,y1+H/2) else '#C0504D')+'</g>')
    s.append(R(x1,y1,W,H,INK,2.5)); s.append(L(x1,y1+H,x1+W,y1,INK,2.5,'7 5'))
    s.append(T(x1+W/2+14,y1+H/2-14,tex='b',size=22,anchor='start',halo=True)); s.append(T(x1-12,y1+H/2+8,tex='a',size=22,anchor='end'))
    s.append(T(x1+W/2,y1+H+26,tex='\\sqrt{2}a',size=20,fill=MUTED)); s.append(T(x1+W/2,y0+A_+32,tex='b=\\sqrt{3}a=4r',size=21)); s.append(T(x1+W/2,y0+A_+64,mix='체심 입방: 몸 대각선 b',size=19,fill=MUTED))
    # 면심 입방: 면
    x2,y2=500,60; r=A_*math.sqrt(2)/4; cp=sq(x2,y2,A_,A_,'c')
    for cx,cy in ((x2,y2),(x2+A_,y2),(x2,y2+A_),(x2+A_,y2+A_),(x2+A_/2,y2+A_/2)):
        fc,sc_=('#4F86C6','#2F5F98') if (cx,cy)!=(x2+A_/2,y2+A_/2) else ('#E8A33D','#A8701A')
        s.append(f'<g {cp}>'+C(cx,cy,r,sc_,1.8,fc)+'</g>')
    s.append(R(x2,y2,A_,A_,INK,2.5)); s.append(L(x2,y2+A_,x2+A_,y2,INK,2.5,'7 5'))
    s.append(T(x2+A_/2+16,y2+A_/2+30,tex='f',size=22,anchor='start',halo=True)); s.append(T(x2+A_/2,y2-16,tex='a',size=22))
    s.append(T(x2+A_/2,y2+A_+32,tex='f=\\sqrt{2}a=4r',size=21)); s.append(T(x2+A_/2,y2+A_+64,mix='면심 입방: 면 대각선 f',size=19,fill=MUTED))
    defs.append('</defs>')
    return svg((680,290),660,'단위세포 모서리와 원자 반지름의 관계',[''.join(defs)]+s)
FIG['AR3']=ar3()

# ═════════ 18. 조밀 쌓임과 육방 밀집 ═════════
def hcp():
    s=[]; rr=17; dx=2*rr
    def layer(x0,y0,kind,n=4,anim=None):
        o=[]; col={'A':('#9AA9BA','#5C6F82'),'B':('#E8A33D','#A8701A'),'C':('#C0504D','#86302E')}[kind]
        off={'A':(0,0),'B':(rr,rr/math.sqrt(3)),'C':(2*rr,2*rr/math.sqrt(3))}[kind]
        for j in range(3):
            for i in range(n):
                x=x0+i*dx+(rr if j%2 else 0)+off[0]; y=y0+j*rr*math.sqrt(3)+off[1]
                o.append(ball(x,y,rr if kind=='A' else rr*.92,col))
        return ''.join(o) if not anim else f'<g data-anim="move" data-from="0,-60" data-dur=".9" data-delay="{anim}" data-ease="out">'+''.join(o)+'</g>'
    s.append(layer(40,60,'A')+layer(40,60,'B',3,'.2')); s.append(T(105,200,mix='A 위에 B',size=19,fill=MUTED))
    s.append(T(105,232,mix='셋째 층: A(ABAB…)',size=19,weight=700)); s.append(T(105,258,mix='→ 육방 밀집',size=19,fill=FIELD,weight=700))
    s.append(T(105,288,mix='셋째 층: C(ABCABC…)',size=19,weight=700)); s.append(T(105,314,mix='→ 입방 밀집(면심 입방)',size=19,fill=FIELD,weight=700))
    # 육방 밀집 단위세포
    b,_=cell3d('hcp',390,165,74,{'M':.17},'pos',yaw=12,pitch=16)
    s.append(b); s.append(T(390,318,mix='육방 밀집 구조의 단위세포',size=19,weight=700))
    s.append(leg_pos(240,346,['꼭짓점','면 중심','내부'],gap=120))
    return svg((560,362),520,'조밀 쌓임과 육방 밀집 구조',s)
FIG['HCP']=hcp()

# ═════════ 19·20 탐구: 공 모형(면심 입방 14개) ═════════
def fcc_balls(S=120,ox=110,oy=120,rf=.3536,anim=False):
    b,_=cell3d('fcc',ox,oy,S,{'M':rf},'met',hide_cell=True,pop=anim)
    return b
FIG['FCC14']=svg((220,220),200,'면심 입방 구조의 공 모형(원자 14개)',[fcc_balls(92,110,110,.3536,True)])

# ═════════ 22. 틈새 자리 ═════════
def holes():
    s=[]; S=150
    # 사면체: 정육면체 꼭짓점 4개
    tet=[(0,0,0),(1,1,0),(1,0,1),(0,1,1)]; ctr=(.5,.5,.5)
    pr=lambda p:rot(p,YAW,PITCH,ctr); sc=lambda p,ox=140,oy=150:(ox+pr(p)[0]*S,oy-pr(p)[2]*S)
    V,E,F=cube_frame(); hid=edge_hidden(E,F,YAW,PITCH); items=[]
    for (i,j),hh in zip(E,hid): items.append((5,L(*sc(V[i]),*sc(V[j]),'#B7C1CC',1.5,'4 4')))
    for p in tet:
        items.append(((pr(p)[1]+pr(ctr)[1])/2,L(*sc(p),*sc(ctr),FIELD,3)))
        items.append((pr(p)[1],ball(*sc(p),34,ION['Cl'])))
    items.append((pr(ctr)[1],'<g data-anim="move" data-from="0,-90" data-dur="1.1" data-delay=".3" data-ease="out">'+ball(*sc(ctr),14,ION['Na'])+'</g>'))
    items.sort(key=lambda t:-t[0]); s.append(''.join(x for _,x in items))
    s.append(T(140,322,mix='사면체 자리 (배위수 4)',size=20,weight=700))
    # 팔면체: ±x ±y ±z
    octa=[(.5,.5,0),(.5,.5,1),(0,.5,.5),(1,.5,.5),(.5,0,.5),(.5,1,.5)]; items=[]
    sc2=lambda p:sc(p,430,150)
    for p in octa:
        items.append(((pr(p)[1]+pr(ctr)[1])/2,L(*sc2(p),*sc2(ctr),FIELD,3)))
        items.append((pr(p)[1],ball(*sc2(p),30,ION['Cl'])))
    items.append((pr(ctr)[1],'<g data-anim="move" data-from="0,-90" data-dur="1.1" data-delay=".6" data-ease="out">'+ball(*sc2(ctr),16,ION['Na'])+'</g>'))
    items.sort(key=lambda t:-t[0]); s.append(''.join(x for _,x in items))
    s.append(T(430,322,mix='팔면체 자리 (배위수 6)',size=20,weight=700))
    s.append(ball(170,356,13,ION['Cl'])+T(190,362,mix='큰 음이온',size=19,anchor='start')+ball(330,356,8,ION['Na'])+T(346,362,mix='작은 양이온',size=19,anchor='start'))
    return svg((580,375),540,'음이온 사이의 사면체 자리와 팔면체 자리',s)
FIG['HOLES']=holes()

# ═════════ 23. 반지름 비 수직선 ═════════
def ratio():
    s=[]; x0,x1=40,600; X=lambda v:x0+(v-0.2)/(1.0-0.2)*(x1-x0); y=110
    zones=[(0.225,0.414,'#E3EEFB','배위수 4','사면체'),(0.414,0.732,'#E7F5EC','배위수 6','팔면체'),(0.732,1.0,'#FBEFE3','배위수 8','입방체')]
    for a,b,c,t1,t2 in zones:
        s.append(R(X(a),y-40,X(b)-X(a),40,'none',0,c)); s.append(T((X(a)+X(b))/2,y-50,mix=t1,size=19,weight=700)); s.append(T((X(a)+X(b))/2,y-14,mix=t2,size=18,fill=MUTED))
    s.append(L(x0,y,x1+8,y,INK,2.5))
    for v in (0.225,0.414,0.732,1.0):
        s.append(L(X(v),y-6,X(v),y+6,INK,2)); s.append(T(X(v),y+28,mix=('%.3f'%v).rstrip('0') if v<1 else '1',size=18))
    s.append(T(x0,y+62,tex='r^+/r^-',size=20,anchor='start'))
    for i,(v,tex) in enumerate(((0.402,'\\ce{ZnS}'),(0.536,'\\ce{NaCl}'),(0.923,'\\ce{CsCl}'))):
        s.append(f'<g class="step" data-g="r{i}">'+A(X(v),y+96,X(v),y+42,'plus',2.5)+T(X(v),y+120,tex=tex,size=21)+T(X(v),y+144,mix='%.2f'%v,size=18,fill=PLUS)+'</g>')
    return svg((640,260),600,'반지름 비와 배위수',s)
FIG['RATIO']=ratio()

# ═════════ 24–26 이온 결정 ═════════
def ionic(key,rad,ions,extra_leg=''):
    b,_=cell3d(key,190,170,188,rad,'ion',coord=True,coord_step='cn',pop=True)
    return svg((380,370),430,{'zns':'황화 아연','nacl':'염화 나트륨','cscl':'염화 세슘'}[key]+' 결정의 단위세포',[b,leg_ion(95,352,ions,size=21,gap=120,r=11)])
FIG['ZNS']=ionic('zns',{'S':.11,'Zn':.075},[('Zn','\\ce{Zn^2+}'),('S','\\ce{S^2-}')])
FIG['NACL']=ionic('nacl',{'Cl':.15,'Na':.08},[('Na','\\ce{Na+}'),('Cl','\\ce{Cl-}')])
FIG['CSCL']=ionic('cscl',{'Cl':.155,'Cs':.145},[('Cs','\\ce{Cs+}'),('Cl','\\ce{Cl-}')])

# ═════════ 27. 이온 결정의 깨짐 ═════════
def cleave():
    s=[]; d=40
    def rows(x0,y0,shift,top_anim=False,lift=0):
        o=[]; top=[]
        for j in range(3):
            for i in range(6):
                sg='+' if (i+j)%2 else '-'
                x=x0+i*d+(shift if j==0 else 0); y=y0+j*d-(lift if j==0 else 0)
                e=f'<g data-chg="{f(x)},{y},{13 if sg=="+" else 16},{sg}"></g>'
                (top if j==0 else o).append(e)
        tt=''.join(top)
        if top_anim: tt=f'<g data-anim="move" data-from="{-shift},{lift}" data-dur="1.2" data-delay=".4" data-ease="io">'+tt+'</g>'
        return ''.join(o)+tt
    s.append(rows(40,70,0)); s.append(A(10,70,32,70,'ink',3)); s.append(T(150,190,mix='(가) 힘을 가하기 전',size=19,weight=700))
    s.append(T(150,30,mix='반대 전하끼리 마주 봄 → 인력',size=18,fill=MUTED))
    s.append(rows(340,70,d,True,14))
    for i in range(5):
        x=340+d+i*d
        s.append(f'<g class="step" data-g="rep">'+A(x,77,x,63,'plus',2.5)+A(x,80,x,94,'plus',2.5)+'</g>')
    s.append(f'<g class="step" data-g="rep">'+T(470,30,mix='같은 전하끼리 마주 봄 → 반발',size=18,fill=PLUS,weight=700)+'</g>')
    s.append(T(470,190,mix='(나) 한 층이 밀린 뒤',size=19,weight=700))
    s.append(A(300,70,330,70,'ink',3)); s.append(T(316,56,mix='힘',size=18))
    return svg((640,205),600,'힘을 받아 이온 층이 밀릴 때 같은 전하가 마주 보아 깨지는 모습',s)
FIG['CLEAVE']=cleave()

# ═════════ 28. 장치(용융 전기 전도성) ═════════
def app():
    s=[]
    s.append(P([(150,140),(160,240),(260,240),(270,140)],GLASS,3,'#F7F8FA'))
    s.append(P([(154,180),(160,236),(260,236),(266,180)],'none',0,'#F5E6C8',close=True)); s.append(T(210,214,tex='\\ce{KNO3}',size=20))
    for x in (185,235): s.append(R(x-6,92,12,130,INK,1.5,'#3A3F47',2))
    s.append(T(150,86,mix='전극',size=18,anchor='end',fill=MUTED))
    s.append(L(185,92,185,50,INK,2.5)); s.append(L(235,92,235,50,INK,2.5))
    s.append(L(185,50,300,50,INK,2.5)); s.append(L(235,50,235,50,INK,2.5)); s.append(L(235,70,235,70,INK,2.5))
    # 전지·전구 (위쪽 회로)
    s.append(L(185,50,185,30,INK,2.5)); s.append(L(185,30,330,30,INK,2.5)); s.append(L(235,50,235,64,INK,0))
    s.append(L(235,92,235,64,INK,2.5)); s.append(L(235,64,420,64,INK,2.5)); s.append(L(420,64,420,30,INK,2.5))
    s.append(L(330,18,330,42,INK,3)); s.append(L(342,24,342,36,INK,5)); s.append(L(342,30,380,30,INK,2.5))
    s.append(T(300,22,mix='전원',size=18,anchor='end'))
    s.append(C(400,30,14,INK,2.5,'#FFF4B8')); s.append(L(380,30,386,30,INK,2.5)); s.append(L(414,30,420,30,INK,2.5)); s.append(T(420,104,mix='전구||(또는 전류계)',size=18,fill=MUTED,anchor='end'))
    s.append(L(392,22,408,38,INK,1.5)); s.append(L(392,38,408,22,INK,1.5))
    # 삼발이·버너
    s.append(L(140,246,280,246,INK,3)); s.append(L(150,246,135,300,INK,3)); s.append(L(270,246,285,300,INK,3))
    s.append(f'<g data-anim="scale" data-from="1,.6" data-o="210,300" data-rep="alt" data-dur=".5">'+f'<path d="M195 300 Q200 268 210 252 Q220 268 225 300 Z" fill="#F2A65A" stroke="#C2410C" stroke-width="2"/>'+'</g>')
    s.append(R(190,300,40,24,INK,2,'#C9D3DD',3)); s.append(T(300,300,mix='가열',size=18,fill=OX,anchor='start'))
    s.append(T(300,180,mix='도가니',size=18,anchor='start',fill=MUTED))
    return svg((440,335),420,'질산 칼륨을 녹이며 전기 전도성을 확인하는 장치',s)
FIG['APP']=app()

# ═════════ 31. 플라즈마 ═════════
def plasma():
    s=[]; rnd=random.Random(12)
    labs=['고체','액체','기체','플라즈마']
    for k in range(4):
        x0=10+k*150; s.append(R(x0,20,120,120,INK,2.5,'#FFFFFF',8)); s.append(T(x0+60,168,mix=labs[k],size=20,weight=700))
        if k<3: s.append(A(x0+124,80,x0+146,80,'equi',3))
        if k==0:
            for i in range(4):
                for j in range(4): s.append(f'<g data-anim="move" data-from="{rnd.choice((-2,2))},0" data-rep="swing" data-dur=".25">'+C(x0+24+i*24,44+j*24,10,'#5C6F82',1.2,'#9AA9BA')+'</g>')
        elif k==1:
            pts=[]
            while len(pts)<12:
                x,y=rnd.uniform(x0+14,x0+106),rnd.uniform(52,128)
                if all(math.dist((x,y),q)>21 for q in pts): pts.append((x,y))
            for x,y in pts: s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-5,5))},{f(rnd.uniform(-4,4))}" data-rep="alt" data-dur="{f(.7+.4*rnd.random())}">'+C(x,y,10,'#5C6F82',1.2,'#9AA9BA')+'</g>')
        elif k==2:
            for i in range(5):
                x,y=rnd.uniform(x0+20,x0+100),rnd.uniform(36,124); s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-14,14))},{f(rnd.uniform(-12,12))}" data-rep="alt" data-dur="{f(.6+.4*rnd.random())}">'+C(x,y,10,'#5C6F82',1.2,'#9AA9BA')+'</g>')
        else:
            for i in range(4):
                x,y=rnd.uniform(x0+22,x0+98),rnd.uniform(38,122); s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-14,14))},{f(rnd.uniform(-12,12))}" data-rep="alt" data-dur="{f(.6+.4*rnd.random())}"><g data-chg="{f(x)},{f(y)},11,+"></g></g>')
            for i in range(4):
                x,y=rnd.uniform(x0+16,x0+104),rnd.uniform(32,128); s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-22,22))},{f(rnd.uniform(-18,18))}" data-rep="alt" data-dur="{f(.4+.3*rnd.random())}">'+C(x,y,4.5,MINUS,0,MINUS)+'</g>')
    s.append(T(305,200,mix='에너지를 더 받을수록 →',size=18,fill=EQUI))
    s.append(T(600,200,mix='양이온 + 전자(전체 중성)',size=18,fill=MUTED,anchor='end'))
    return svg((620,212),600,'고체·액체·기체·플라즈마의 입자 모형',s)
FIG['PLASMA']=plasma()

# ═════════ 35·36 연습 문제 그림 ═════════
def holes_fcc():
    s=[]; S=180; ox,oy=150,165
    b,sc=cell3d('fcc',ox,oy,S,{'M':.09},'met')
    s.append(b)
    import itertools as it
    tet=[p for p in it.product((.25,.75),repeat=3)]
    octs=[(.5,.5,.5)]+[p for p in it.product((0,.5,1),repeat=3) if sum(1 for c in p if c==.5)==1]
    s.append('<g class="step" data-g="t">'+''.join(C(*sc(p),8,'#1F6FD1',2,'#E3EEFB') for p in tet)+'</g>')
    s.append('<g class="step" data-g="o">'+''.join(P([(sc(p)[0],sc(p)[1]-9),(sc(p)[0]+9,sc(p)[1]),(sc(p)[0],sc(p)[1]+9),(sc(p)[0]-9,sc(p)[1])],PLUS,2,'#FDE2E4',close=True) for p in octs)+'</g>')
    s.append('<g class="step" data-g="t">'+C(30,345,8,'#1F6FD1',2,'#E3EEFB')+T(44,351,mix='사면체 자리',size=19,anchor='start')+'</g>')
    s.append('<g class="step" data-g="o">'+P([(170,336),(179,345),(170,354),(161,345)],PLUS,2,'#FDE2E4',close=True)+T(186,351,mix='팔면체 자리',size=19,anchor='start')+'</g>')
    return svg((300,365),290,'면심 입방 단위세포 속 사면체 자리와 팔면체 자리',s)
FIG['Q4FIG']=svg((220,220),200,'면심 입방 구조로 쌓인 원자 14개',[fcc_balls(92,110,110,.3536)])
FIG['Q4HOLE']=holes_fcc()
def rutile():
    S=210; ox,oy=170,160
    key='tio2'; cz=CUBIC[key]['c']
    at=[(p,t,pl) for p,t,w,pl in cell_atoms(key)]
    b,sc=cell3d(key,ox,oy,S,{'Ti':.075,'O':.06},'ion')
    # Ti–O 결합(가까운 6개)
    bonds=[]
    for p,t,_ in at:
        if t!='Ti': continue
        for q,u,_ in at:
            if u=='O' and math.dist(p,q)<0.62: bonds.append(L(*sc(p),*sc(q),'#9AA5B1',4))
    return svg((340,330),300,'타이타늄 산화물(루틸)의 단위세포',[''.join(bonds),b,leg_ion(70,312,[('Ti','\\mathrm{Ti}'),('O','\\mathrm{O}')],size=20,gap=110,r=10)])
FIG['RUTILE']=rutile()
FIG['BRAGG_SM']=FIG['BRAGG'].replace('style="width:580px"','style="width:440px"')

# ═════════ 쓰기 ═════════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
miss=[]
def rep(m):
    k=m.group(1)
    if k not in FIG: miss.append(k); return m.group(0)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
assert not miss, miss
os.makedirs(OUT,exist_ok=True)
open(OUT+'slides.html','w',encoding='utf-8').write(out)
for src,dst in (('labs_src.js','labs.js'),('extra_src.css','extra.css')):
    if os.path.exists(os.path.join(HERE,src)): shutil.copy(os.path.join(HERE,src),OUT+dst)
print('ok',len(out),'slides',out.count('<section'))
