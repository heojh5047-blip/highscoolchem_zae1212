# -*- coding: utf-8 -*-
"""고급화학 2-M 그림 생성: gen_head.py(1-M 사본, OUT=이 덱 — assert) + helpers.py → tpl.html의 {{KEY}}를 바꿔 slides.html (실험실 없음)"""
import math, re, sys, os, random
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/2-M_대단원_Ⅱ_마무리/slides.html'), OUT
GAS='#F2A65A'; GAS_E='#B4561C'; U8='#8FA3B8'; U8_E='#5C6F82'; MET='#9AA9BA'; MET_E='#5C6F82'
LR='#E8322B'; LG='#2EAA4A'; LB='#3D6FE0'
def pt(x,y,r=10,fill=GAS,st=GAS_E,w=1.8): return C(x,y,r,st,w,fill=fill)
def step(body,g=None):
    return '<g class="step"'+(f' data-g="{g}"' if g else '')+'>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def pop(body,x,y,d=0,dur='.6'): return an('pop',body,o=f'{f(x)},{f(y)}',dur=dur,delay=f'{d:.1f}')
def mvalt(body,dx,dy,dur='1.4',delay='0'): return an('move',body,**{'from':f'{f(dx)},{f(dy)}','rep':'alt','dur':dur,'delay':delay,'ease':'io'})
def swing(body,dx,dy,dur='.35',delay='0'): return an('move',body,**{'from':f'{f(dx)},{f(dy)}','rep':'swing','dur':dur,'delay':delay,'ease':'sine'})
def pink(c,cmax=0.25):
    a=max(0,min(1,c/cmax)); c0=(0xFB,0xE3,0xEC); c1=(0xC2,0x18,0x5B)
    return '#%02X%02X%02X'%tuple(int(round(c0[i]+(c1[i]-c0[i])*a)) for i in range(3))
def axes(X0,Y0,W,H,xr,yr,xt,yt,fx=str,fy=str,size=18):
    X=lambda v: X0+(v-xr[0])/(xr[1]-xr[0])*W; Y=lambda v: Y0-(v-yr[0])/(yr[1]-yr[0])*H
    s=[]
    for v in xt: s.append(L(X(v),Y0,X(v),Y0-H,'#E2E7EC',1)); s.append(T(X(v),Y0+24,mix=fx(v),size=size))
    for v in yt: s.append(L(X0,Y(v),X0+W,Y(v),'#E2E7EC',1)); s.append(T(X0-8,Y(v)+6,mix=fy(v),size=size,anchor='end'))
    s.append(A(X0,Y0,X0+W+14,Y0,'muted',2)); s.append(A(X0,Y0,X0,Y0-H-14,'muted',2))
    return s,X,Y
def mn(v): return ('−' if v<0 else '')+('%g'%abs(v))
random.seed(29)

# ═══ 계산 (STEAM 예시값 — plan.md 검산 8–10)
EPS_EFF={'R':0.07,'G':3.99,'B':2.40}; I0={'R':760,'G':820,'B':640}
def mixA(keys,c=0.15):
    num=sum(I0[k]*10**(-EPS_EFF[k]*c) for k in keys); den=sum(I0[k] for k in keys); return -math.log10(num/den)
BAR=[('빨강',['R'],LR),('초록',['G'],LG),('파랑',['B'],LB),('빨+초',['R','G'],'#E8C547'),('초+파',['G','B'],'#21B5C9'),('빨+파',['R','B'],'#C2398B'),('흰빛',['R','G','B'],'#FFFFFF')]
BARV=[(n,round(mixA(k),2),col) for n,k,col in BAR]
STD=[(0.05,521),(0.10,324),(0.15,208),(0.20,128),(0.25,83)]; UNK=272; I00=820
STDA=[(c,-math.log10(i/I00)) for c,i in STD]
SLOPE=sum(c*a for c,a in STDA)/sum(c*c for c,a in STDA)
mA=sum(a for c,a in STDA)/len(STDA); R2=1-sum((a-SLOPE*c)**2 for c,a in STDA)/sum((a-mA)**2 for c,a in STDA)
AUNK=-math.log10(UNK/I00); CUNK=AUNK/round(SLOPE,2)
print('bars',BARV); print('stdA',[(c,round(a,3)) for c,a in STDA],'slope',round(SLOPE,3),'R2',round(R2,4),'Aunk',round(AUNK,3),'cunk',round(CUNK,3))
assert abs(round(SLOPE,2)-4.00)<1e-9 and abs(round(AUNK,3)-0.479)<1e-9 and abs(round(CUNK,3)-0.120)<1e-9
# 종합 문제 검산
assert round(78.5/0.105/1.04)==719
MU5=235.044+6*18.998; MU8=238.051+6*18.998; assert abs(math.sqrt(MU8/MU5)-1.004)<5e-4
LNP=-35200/8.314*(1/285.15-1/337.75); assert abs(LNP+2.31)<0.005
assert round(5.00/0.512,2)==9.77 and round(9.77*62.07)==606

# ═══ S1 표지
def box_gas(x,y,w,h,n=7,anim=True):
    s=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>']
    P0=[(0.18,0.25),(0.62,0.18),(0.85,0.55),(0.35,0.62),(0.12,0.82),(0.6,0.84),(0.5,0.42)][:n]
    for i,(u,v) in enumerate(P0):
        px,py=x+u*w,y+v*h; dx,dy=random.choice([-1,1])*random.uniform(8,14),random.choice([-1,1])*random.uniform(6,12)
        s.append(mvalt(pt(px,py,9),dx,dy,dur=f'{random.uniform(1.1,1.7):.1f}') if anim else pt(px,py,9))
    return s
def box_liq(x,y,w,h,anim=True):
    s=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>']
    k=0
    for j in range(4):
        for i in range(6):
            px=x+12+i*(w-24)/5.3+(9 if j%2 else 0)+random.uniform(-3,3); py=y+h-13-j*20+random.uniform(-2,2)
            if px>x+w-11: continue
            if j==3 and i%2: continue
            b=pt(px,py,9); k+=1
            s.append(mvalt(b,random.uniform(-4,4),random.uniform(-3,3),dur=f'{random.uniform(.6,1.0):.1f}') if anim else b)
    return s
def box_sol(x,y,w,h,anim=True):
    s=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>']
    pos=[]
    for j in range(4):
        for i in range(6):
            px=x+14+i*(w-28)/5+(8 if j%2 else 0); py=y+h-14-j*21
            if px>x+w-12: continue
            pos.append((px,py))
    sol={3,9,14}
    for k,(px,py) in enumerate(pos):
        if k in sol: continue
        s.append(C(px,py,8,'#6F9FC4',1.6,fill='#CFE3F2'))
    for k in sorted(sol):
        px,py=pos[k]; b=C(px,py,11,'#8E1546',1.8,fill='#E46A9A')
        s.append(pop(b,px,py,0.4+0.2*len(s)%3) if anim else b)
    return s
def box_sol_grid(x,y,w,h,anim=True):
    s=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>']
    nx,ny=6,5; dx=(w-28)/(nx-1); dy=(h-26)/(ny-1)
    for j in range(ny):
        for i in range(nx):
            b=pt(x+14+i*dx,y+13+j*dy,9.5,fill=GAS,st=GAS_E)
            s.append(swing(b,random.choice([-2.2,2.2]),0,dur=f'{random.uniform(.25,.4):.2f}') if anim else b)
    return s
def cover():
    s=[]
    s+=box_gas(20,10,150,120); s+=box_liq(200,10,150,120); s+=box_sol_grid(380,10,150,120)
    for x,t in ((95,'기체'),(275,'액체'),(455,'고체')): s.append(T(x,162,mix=t,size=22))
    # 간이 분광 광도계
    y=300
    s.append(f'<rect x="20" y="215" width="510" height="170" rx="12" fill="#F4F6F8" stroke="#3A3F47" stroke-width="2.5"/>')
    s.append(T(36,242,mix='빛 차단 상자',size=21,anchor='start',fill=MUTED))
    s.append(P([(52,y-22),(52,y+22),(80,y+22),(80,y-8)],INK,2)+f'<path d="M52 {y-8} A14 14 0 0 1 80 {y-8}" fill="{LG}" fill-opacity=".35" stroke="{INK}" stroke-width="2"/>')
    s.append(an('draw',L(86,y,250,y,LG,12,extra='stroke-linecap="round" stroke-opacity=".85"'),dur='.8'))
    s.append(f'<rect x="250" y="{y-48}" width="54" height="96" rx="4" fill="#E9A5BF" stroke="#7E8B98" stroke-width="2.5"/>')
    s.append(an('draw',L(304,y,440,y,LG,4,extra='stroke-linecap="round" stroke-opacity=".85"'),dur='.6',delay='.8'))
    s.append(f'<rect x="440" y="{y-26}" width="60" height="52" rx="6" fill="#E6EAEE" stroke="{INK}" stroke-width="2"/>')
    s.append(T(66,y+52,mix='LED',size=21)); s.append(T(277,y+76,mix='용액',size=21)); s.append(T(470,y+52,mix='광센서',size=21))
    s.append(T(168,y-16,tex='I_0',size=24)); s.append(T(372,y-16,tex='I',size=24))
    return svg('0 0 550 400',420,'기체·액체·고체 입자 상자와, 초록 빛이 분홍 용액을 지나며 약해져 광센서에 닿는 간이 분광 광도계',s)
FIG['COVER']=cover()

# ═══ S7 상태 네 칸
def states():
    s=[]; Y=62; W=230; H=170
    xs=[20,300,580,860]
    s+=box_gas(xs[0],Y,W,H); s+=box_liq(xs[1],Y,W,H); s+=box_sol_grid(xs[2],Y,W,H); s+=box_sol(xs[3],Y,W,H)
    s.append(A(30,30,800,30,'ink',3)); s.append(T(415,22,mix='입자 사이 힘의 효과 ↑ · 운동 에너지의 효과 ↓',size=19,halo=True))
    names=[('기체','이상 기체·실제 기체, $Z$'),('액체','증기압·끓는점·표면 장력'),('고체','단위세포·배위수'),('용액','농도·총괄성·흡광도')]
    for x,(a,b) in zip(xs,names):
        s.append(T(x+W/2,Y+H+30,mix=a,size=21,weight=700)); s.append(T(x+W/2,Y+H+58,mix=b,size=19,fill=MUTED))
    s.append(C(xs[3]+30,24,9,'#6F9FC4',1.6,fill='#CFE3F2')); s.append(T(xs[3]+44,30,mix='용매',size=18,anchor='start'))
    s.append(C(xs[3]+120,24,11,'#8E1546',1.8,fill='#E46A9A')); s.append(T(xs[3]+136,30,mix='용질',size=18,anchor='start'))
    return svg('0 0 1100 300',1100,'기체는 흩어져 빠르게 움직이고, 액체는 촘촘하게 자리를 바꾸며, 고체는 규칙적으로 배열해 제자리에서 진동하고, 용액은 용매 입자 사이에 용질 입자가 섞여 있다',s)
FIG['STATES']=states()

# ═══ S11 단위 인자 사슬
def chain1():
    s=[]; y=70
    cards=[(150,'설탕 78.5 g'),(500,'음료 ? g'),(850,'음료 ? mL')]
    for k,(x,t) in enumerate(cards):
        b=f'<rect x="{x-110}" y="{y-34}" width="220" height="68" rx="12" fill="#F2FAF5" stroke="{FIELD}" stroke-width="2"/>'+T(x,y+9,mix=t,size=25,weight=700)
        s.append(pop(b,x,y,0.3*k))
    s.append(A(265,y,385,y,'ink',3)); s.append(T(325,y-44,mix='질량 백분율 10.5 %',size=23))
    s.append(A(615,y,735,y,'ink',3)); s.append(T(675,y-44,mix='밀도 1.04 g/mL',size=23))
    return svg('0 0 1000 110',820,'설탕 질량에서 질량 백분율로 음료 질량을, 밀도로 음료 부피를 구하는 순서',s)
FIG['CHAIN1']=chain1()

# ═══ S12 분출
def effuse():
    s=[]
    s.append(f'<rect x="20" y="30" width="230" height="200" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>')
    s.append(L(250,118,250,142,'#FFFFFF',5))
    s.append(T(330,80,mix='진공',size=20,fill=MUTED)); s.append(T(262,175,mix='작은 구멍',size=18,anchor='start'))
    s.append(A(262,158,252,140,'muted',2))
    pts=[(50,60,1),(110,55,0),(185,70,1),(220,110,0),(70,120,0),(140,110,1),(200,165,1),(60,190,1),(120,200,0),(175,210,0),(95,160,1),(225,200,1)]
    for i,(x,y,k) in enumerate(pts):
        b=pt(x,y,10,GAS,GAS_E) if k else pt(x,y,10,U8,U8_E)
        s.append(mvalt(b,random.choice([-1,1])*random.uniform(6,11),random.choice([-1,1])*random.uniform(5,9),dur=f'{random.uniform(1.0,1.6):.1f}'))
    s.append(an('move',pt(330,128,10,GAS,GAS_E),**{'from':'-90,0','dur':'1.4','ease':'out'}))
    s.append(an('move',pt(296,138,10,U8,U8_E),**{'from':'-56,0','dur':'1.4','delay':'.3','ease':'out'}))
    s.append(A(345,128,395,128,'ink',2.4))
    s.append(pt(36,268,10,GAS,GAS_E)); s.append(T(54,275,mix='$\\ce{^{235}UF6}$ 349.032',size=19,anchor='start'))
    s.append(pt(236,268,10,U8,U8_E)); s.append(T(254,275,mix='$\\ce{^{238}UF6}$ 352.039',size=19,anchor='start'))
    return svg('0 0 420 295',410,'두 종류의 육플루오린화 우라늄 분자가 섞인 용기에서 작은 구멍으로 분자가 진공 쪽으로 빠져나간다',s)
FIG['EFFUSE']=effuse()

# ═══ S13 ln P – 1/T
def claus():
    X0,Y0,W,H=78,318,320,272
    s,X,Y=axes(X0,Y0,W,H,(2.9,3.6),(-2.6,0.4),[2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6],[-2.5,-2,-1.5,-1,-0.5,0],fx=lambda v:'%.1f'%v,fy=mn)
    s.append(T(X0+W,Y0+52,mix='$1/T$ [$10^{-3}\\ \\text{K}^{-1}$]',size=19,anchor='end',fill=MUTED))
    s.append(T(X0+6,26,mix='$\\ln P$ ($P$: atm)',size=19,anchor='start',fill=MUTED))
    lnP=lambda x: -35200/8.314*(x*1e-3-1/337.75)
    pts=[(X(x),Y(lnP(x))) for x in [2.9+0.7*i/40 for i in range(41)] if -2.6<=lnP(x)<=0.4]
    s.append(an('draw',P(pts,INK,3),dur='1.2'))
    x1,x2=1e3/337.75,1e3/285.15
    s.append(C(X(x1),Y(0),6,INK,2,fill=INK)); s.append(T(X(x1)+10,Y(0)-12,mix='64.6 °C, 1 atm',size=18,anchor='start',halo=True))
    s.append(T(X(3.22),Y(lnP(3.22))-16,mix='기울기 $=-\\dfrac{\\Delta H^\\circ_\\text{vap}}{R}$',size=19,anchor='start',halo=True))
    g=[L(X(x2),Y(lnP(x2)),X(x2),Y0,EQUI,2,dash='6 4'),L(X0,Y(lnP(x2)),X(x2),Y(lnP(x2)),EQUI,2,dash='6 4'),
       C(X(x2),Y(lnP(x2)),6,EQUI,2,fill=EQUI),T(X0+8,Y(lnP(x2))-10,mix='12.0 °C, $\\ln P_2=-2.31$',size=18,anchor='start',halo=True)]
    s.append(step(g,'c2'))
    return svg('0 0 420 380',420,'메탄올의 ln P와 1/T 직선: 정상 끓는점 64.6도에서 ln P는 0이고, 12.0도에서 ln P는 −2.31이다',s)
FIG['CLAUS']=claus()

# ═══ S14 체심 입방 단위세포
YAW,PIT=math.radians(28),math.radians(18)
def proj(p,cx,cy,S):
    X,Yd,Z=p[0]-.5,p[1]-.5,p[2]-.5
    x1=X*math.cos(YAW)-Yd*math.sin(YAW); y1=X*math.sin(YAW)+Yd*math.cos(YAW)
    up=Z*math.cos(PIT)+y1*math.sin(PIT); dep=y1*math.cos(PIT)-Z*math.sin(PIT)
    return cx+S*x1, cy-S*up, dep
def bcc():
    s=[]; cx,cy,S=215,205,230
    V=[(i,j,k) for i in (0,1) for j in (0,1) for k in (0,1)]
    Pj={v:proj(v,cx,cy,S) for v in V}
    hid=max(V,key=lambda v:Pj[v][2])
    E=[(a,b) for a in V for b in V if a<b and sum(abs(a[t]-b[t]) for t in range(3))==1]
    for a,b in E:
        back=hid in (a,b)
        s.append(L(Pj[a][0],Pj[a][1],Pj[b][0],Pj[b][1],MUTED if back else INK,1.6 if back else 2.2,dash='6 5' if back else None))
    atoms=[(v,16) for v in V]+[((.5,.5,.5),24)]
    for v,r in sorted(atoms,key=lambda t:-proj(t[0],cx,cy,S)[2]):
        x,y,_=proj(v,cx,cy,S); s.append(C(x,y,r,MET_E,1.8,fill=MET))
    best=max([(0,0),(0,1),(1,0),(1,1)],key=lambda ij: math.hypot(Pj[(ij[0],ij[1],1)][0]-Pj[(1-ij[0],1-ij[1],0)][0],Pj[(ij[0],ij[1],1)][1]-Pj[(1-ij[0],1-ij[1],0)][1]))
    i0,j0=best; p0=Pj[(i0,j0,1)]; p1=Pj[(1-i0,1-j0,0)]; q=Pj[(i0,j0,0)]
    s.append(an('draw',L(p0[0],p0[1],p1[0],p1[1],PLUS,4.5,extra='stroke-linecap="round"'),dur='1',delay='.2'))
    s.append(an('draw',L(q[0],q[1],p1[0],p1[1],FIELD,4.5,extra='stroke-linecap="round"'),dur='.8',delay='1.2'))
    s.append(an('draw',L(q[0],q[1],p0[0],p0[1],INK,4.5,extra='stroke-linecap="round"'),dur='.6',delay='2'))
    m=lambda a,b,t=.5:(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
    la=m(p0,p1,.64); s.append(T(la[0]+14,la[1]-12,tex='a',size=24,fill=PLUS,halo=True,weight=700))
    lb=m(q,p1,.62); s.append(T(lb[0]+4,lb[1]+28,tex='b',size=24,fill=FIELD,halo=True,weight=700))
    ll=m(q,p0); s.append(T(ll[0]-16,ll[1]+8,tex='l',size=24,anchor='end',halo=True,weight=700))
    return svg('0 0 430 400',390,'체심 입방 단위세포: 몸 대각선 a, 바닥면 대각선 b, 모서리 l이 직각삼각형을 이룬다',s)
FIG['BCC']=bcc()

# ═══ S15 몸 대각선을 품은 단면
def bccsec():
    s=[]; l=210.0; b=l*math.sqrt(2); r=math.sqrt(3)*l/4
    x0,y0=95,70; x1,y1=x0+b,y0+l
    s.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(b)}" height="{f(l)}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>')
    def quarter(cx,cy,sx,sy,d):
        ex1=(cx+sx*r,cy); ex2=(cx,cy+sy*r); sweep=1 if sx*sy>0 else 0
        pth=f'<path d="M{f(cx)} {f(cy)} L{f(ex1[0])} {f(ex1[1])} A{f(r)} {f(r)} 0 0 {sweep} {f(ex2[0])} {f(ex2[1])} Z" fill="{MET}" stroke="{MET_E}" stroke-width="1.8"/>'
        return pop(pth,cx,cy,d)
    s.append(quarter(x0,y0,1,1,0)); s.append(quarter(x1,y1,-1,-1,.4)); s.append(quarter(x1,y0,-1,1,.6)); s.append(quarter(x0,y1,1,-1,.6))
    mx,my=(x0+x1)/2,(y0+y1)/2
    s.append(pop(C(mx,my,r,MET_E,1.8,fill=MET),mx,my,.2))
    s.append(an('draw',L(x0,y0,x1,y1,PLUS,4,extra='stroke-linecap="round"'),dur='1',delay='.9'))
    D=math.hypot(b,l); ux,uy=b/D,l/D
    for t in (r,3*r):
        px,py=x0+ux*t,y0+uy*t; s.append(L(px-uy*9,py+ux*9,px+uy*9,py-ux*9,PLUS,3))
    for t,lab in ((r/2,'r'),(2*r,'2r'),(3.5*r,'r')):
        px,py=x0+ux*t,y0+uy*t; s.append(T(px+uy*22,py-ux*22+7,tex=lab,size=20,fill=PLUS,halo=True,weight=700))
    s.append(T(mx+70,my+60,tex='a=4r',size=22,fill=PLUS,halo=True,weight=700))
    s.append(L(x0-26,y0,x0-26,y1,INK,2)); s.append(L(x0-32,y0,x0-20,y0,INK,2)); s.append(L(x0-32,y1,x0-20,y1,INK,2))
    s.append(T(x0-34,my+8,tex='l',size=22,anchor='end',weight=700))
    s.append(L(x0,y1+26,x1,y1+26,FIELD,2)); s.append(L(x0,y1+20,x0,y1+32,FIELD,2)); s.append(L(x1,y1+20,x1,y1+32,FIELD,2))
    s.append(T(mx,y1+56,tex='b=\\sqrt{2}\\,l',size=22,fill=FIELD,weight=700))
    s.append(T(mx,y0-22,mix='몸 대각선을 품은 단면 (크기 비례)',size=19,fill=MUTED))
    return svg('0 0 500 370',490,'몸 대각선을 품은 직사각형 단면에서 꼭짓점 원자, 체심 원자, 꼭짓점 원자가 대각선을 따라 맞닿아 a는 4r이다',s)
FIG['BCCSEC']=bccsec()

# ═══ S16 끓는점 오름
def bpe():
    X0,Y0,W,H=80,300,310,250
    s,X,Y=axes(X0,Y0,W,H,(94,110),(0.75,1.15),[94,98,102,106,110],[0.8,0.9,1.0,1.1],fx=lambda v:str(v),fy=lambda v:'%.1f'%v)
    s.append(T(X0+W,Y0+52,mix='온도 [°C]',size=19,anchor='end',fill=MUTED)); s.append(T(X0+6,28,mix='증기압 [atm]',size=19,anchor='start',fill=MUTED))
    Pw=lambda t: math.exp(-40700/8.314*(1/(t+273.15)-1/373.15)); k=1/Pw(105)
    tt=[94+16*i/60 for i in range(61)]
    s.append(L(X0,Y(1.0),X0+W,Y(1.0),MUTED,2,dash='7 5')); s.append(T(X0+W-4,Y(1.0)-8,mix='1 atm',size=18,anchor='end',fill=MUTED))
    s.append(an('draw',P([(X(t),Y(Pw(t))) for t in tt if 0.75<=Pw(t)<=1.15],INK,3),dur='1'))
    s.append(an('draw',P([(X(t),Y(k*Pw(t))) for t in tt if 0.75<=k*Pw(t)<=1.15],MINUS,3,dash='9 6'),dur='1',delay='.5'))
    s.append(L(X(100),Y(1.0),X(100),Y0,MUTED,1.6,dash='4 4')); s.append(L(X(105),Y(1.0),X(105),Y0,MUTED,1.6,dash='4 4'))
    s.append(T(X(98.6),Y(1.05),mix='순수한 물',size=19,anchor='end',halo=True)); s.append(T(X(107.2),Y(0.94),mix='용액',size=19,anchor='start',fill=MINUS,halo=True))
    yy=Y(0.82); s.append(an('scale',A(X(100),yy,X(105),yy,'equi',2.6),**{'from':'0,1','o':f'{f(X(100))},{f(yy)}','delay':'1.4','dur':'.6'}))
    s.append(T(X(102.5),yy-12,mix='$\\Delta T_\\mathrm{b}=5.0\\ {}^\\circ\\text{C}$',size=19,fill=EQUI,halo=True))
    return svg('0 0 420 360',410,'끓는점 근처의 증기압 곡선: 순수한 물은 100도에서, 용액은 105도에서 증기압이 1 atm이 되어 끓는점이 5.0도 오른다',s)
FIG['BPE']=bpe()

# ═══ S17 빛줄기
def beam():
    s=[]; y=80
    s.append(P([(18,y-22),(18,y+22),(46,y+22),(46,y-8)],INK,2)+f'<path d="M18 {y-8} A14 14 0 0 1 46 {y-8}" fill="{LG}" fill-opacity=".35" stroke="{INK}" stroke-width="2"/>')
    s.append(an('draw',L(52,y,200,y,LG,14,extra='stroke-linecap="round" stroke-opacity=".85"'),dur='.8'))
    s.append(f'<rect x="200" y="{y-50}" width="64" height="100" rx="4" fill="#E9A5BF" stroke="#7E8B98" stroke-width="2.5"/>')
    s.append(an('draw',L(264,y,380,y,LG,5,extra='stroke-linecap="round" stroke-opacity=".85"'),dur='.6',delay='.8'))
    s.append(f'<rect x="380" y="{y-26}" width="64" height="52" rx="6" fill="#E6EAEE" stroke="{INK}" stroke-width="2"/>')
    s.append(T(126,y-20,tex='I_0',size=22)); s.append(T(322,y-16,tex='I',size=22))
    s.append(L(200,y+62,264,y+62,EQUI,2)); s.append(L(200,y+56,200,y+68,EQUI,2)); s.append(L(264,y+56,264,y+68,EQUI,2))
    s.append(T(232,y+90,tex='b',size=21,fill=EQUI))
    s.append(T(32,y+50,mix='LED',size=18)); s.append(T(232,y+24,tex='c',size=21,halo=True)); s.append(T(412,y+50,mix='광센서',size=18))
    s.append(T(126,y+34,mix='단색광',size=18,fill=MUTED))
    return svg('0 0 470 185',430,'단색광 세기 I0가 두께 b, 농도 c인 용액을 지나며 I로 약해져 광센서에 닿는다',s)
FIG['BEAM']=beam()

# ═══ S18 시험관
def tubes():
    s=[]; cs=[0.05,0.10,0.15,0.20,0.25,None]; x0=50; dx=70; top=70; h=200
    s.append(f'<ellipse cx="230" cy="26" rx="26" ry="13" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>'); s.append(C(230,26,6,INK,1,fill=INK))
    s.append(T(268,32,mix='눈으로 비교',size=18,anchor='start',fill=MUTED))
    for i,c in enumerate(cs):
        x=x0+i*dx; col=pink(0.12 if c is None else c)
        b=(f'<path d="M{x-17} {top} L{x-17} {top+h-17} A17 17 0 0 0 {x+17} {top+h-17} L{x+17} {top} Z" fill="#FFFFFF" stroke="#7E8B98" stroke-width="2.4"/>'
           +f'<path d="M{x-15} {top+50} L{x-15} {top+h-17} A15 15 0 0 0 {x+15} {top+h-17} L{x+15} {top+50} Z" fill="{col}"/>')
        s.append(pop(b,x,top+h,0.15*i))
        s.append(T(x,top+h+30,mix=('?' if c is None else '%.2f'%c),size=20,weight=700 if c is None else None))
    s.append(T(x0+2*dx,top+h+58,mix='표준 용액 농도 [M]',size=18,fill=MUTED)); s.append(T(x0+5*dx,top+h+58,mix='미지',size=18,fill=EQUI))
    return svg('0 0 460 340',450,'진하기가 다른 염화 코발트 표준 용액 다섯 개와 농도를 모르는 용액 한 개를 눈으로 비교한다',s)
FIG['TUBES']=tubes()

# ═══ S19 회로 블록도
def circuit():
    s=[]
    s.append(f'<rect x="20" y="170" width="760" height="46" rx="6" fill="#F4EFE6" stroke="#B9A8A0" stroke-width="2"/>')
    for i in range(37):
        for j in range(2): s.append(C(36+i*20.4,184+j*18,2.2,'#B9A8A0',0,fill='#B9A8A0'))
    s.append(T(400,244,mix='브레드 보드',size=18,fill=MUTED))
    s.append(f'<rect x="120" y="36" width="430" height="128" rx="8" fill="#EEF0F3" stroke="#3A3F47" stroke-width="3"/>')
    s.append(T(335,28,mix='빛 차단 상자',size=18,fill=MUTED))
    y=100
    s.append(P([(150,y-22),(150,y+22),(178,y+22),(178,y-8)],INK,2)+f'<path d="M150 {y-8} A14 14 0 0 1 178 {y-8}" fill="{LG}" fill-opacity=".35" stroke="{INK}" stroke-width="2"/>')
    for k,col in enumerate((LR,LG,LB)): s.append(C(158+6*k,y+4,3.2,col,0,fill=col))
    s.append(T(164,y+52,mix='RGB LED',size=18))
    s.append(an('draw',L(184,y,300,y,LG,10,extra='stroke-linecap="round" stroke-opacity=".85"'),dur='.7'))
    s.append(f'<rect x="300" y="{y-40}" width="46" height="80" rx="3" fill="#E9A5BF" stroke="#7E8B98" stroke-width="2.4"/>'); s.append(T(323,y+60,mix='큐벳',size=18))
    s.append(an('draw',L(346,y,460,y,LG,4,extra='stroke-linecap="round" stroke-opacity=".85"'),dur='.5',delay='.7'))
    s.append(f'<rect x="460" y="{y-22}" width="50" height="44" rx="5" fill="#E6EAEE" stroke="{INK}" stroke-width="2"/>'); s.append(T(485,y+52,mix='광센서',size=18))
    for k in range(3):
        x=50+k*22; s.append(P([(x,170),(x,150)]+[(x+(5 if i%2==0 else -5),150-4-i*6) for i in range(5)]+[(x,116),(x,108),(150,108-0*k)],INK,1.8))
    s.append(T(72,98,mix='저항',size=18))
    s.append(f'<rect x="600" y="70" width="120" height="70" rx="4" fill="#2B2F36" stroke="{INK}" stroke-width="2"/>')
    for i in range(6): s.append(L(610+i*20,140,610+i*20,152,INK,2)); s.append(L(610+i*20,58,610+i*20,70,INK,2))
    s.append(T(660,112,mix='IC 회로',size=19,fill='#FFFFFF'))
    s.append(an('draw',P([(510,96),(570,96),(570,90),(600,90)],FIELD,2.6),dur='.6',delay='1.2'))
    s.append(T(556,82,mix='전압',size=18,fill=FIELD,halo=True))
    s.append(P([(620,152),(620,166)],INK,1.8)); s.append(P([(116,166),(620,166)],INK,1.8,dash='5 4')); s.append(P([(116,166),(116,108),(150,108)],INK,1.8,dash='5 4'))
    s.append(an('draw',P([(720,105),(820,105)],FIELD,2.6),dur='.5',delay='1.8')); s.append(T(770,92,mix='숫자',size=18,fill=FIELD,halo=True))
    s.append(f'<rect x="830" y="44" width="200" height="124" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="2.4"/>')
    s.append(P([(810,180),(1050,180),(1036,168),(824,168)],INK,2.2,fill='#E6EAEE',close=True))
    s.append(L(850,150,1010,150,MUTED,1.5)); s.append(L(850,150,850,60,MUTED,1.5))
    s.append(an('draw',L(850,150,1000,72,FIELD,2.6),dur='.6',delay='2.3'))
    for i,(u,v) in enumerate(((880,135),(915,117),(950,99),(985,80))): s.append(C(u,v,4,INK,1,fill=INK))
    s.append(T(930,206,mix='컴퓨터(엑셀)',size=18))
    return svg('0 0 1060 250',1000,'브레드 보드 위 빛 차단 상자 안에 RGB LED, 큐벳, 광센서가 일렬로 있고, 광센서 전압을 IC 회로가 숫자로 바꾸어 컴퓨터로 보낸다',s)
FIG['CIRCUIT']=circuit()

# ═══ S20 흡수 스펙트럼 + 막대
def spec():
    X0,Y0,W,H=66,280,370,220
    s,X,Y=axes(X0,Y0,W,H,(400,700),(0,5),[400,450,500,550,600,650,700],[1,2,3,4,5])
    s.append(T(X0+W,Y0+48,mix='파장 $\\lambda$ [nm]',size=19,anchor='end',fill=MUTED)); s.append(T(X0+4,26,mix='몰 흡광계수 $\\varepsilon$',size=19,anchor='start',fill=MUTED))
    for lam,col,nm in ((470,LB,'파랑'),(525,LG,'초록'),(630,LR,'빨강')):
        pts=[(X(l),Y(4.6*math.exp(-(l-lam)**2/(2*12**2)))) for l in range(lam-36,lam+37,2)]
        s.append(P(pts+[(X(lam+36),Y0),(X(lam-36),Y0)],col,1,fill=col,close=True,extra='fill-opacity=".22" stroke-opacity=".5"'))
        s.append(T(X(lam),Y(4.6)-10,mix=nm,size=18,fill=col,halo=True))
    eps=lambda l: 4.8*math.exp(-(l-510)**2/(2*40**2))
    s.append(an('draw',P([(X(l),Y(eps(l))) for l in range(400,701,5)],INK,3),dur='1.2'))
    s.append(T(X(560),Y(4.2),mix='염화 코발트(Ⅱ)||수용액',size=18,anchor='start',halo=True))
    return svg('0 0 460 345',460,'염화 코발트 수용액의 흡수는 510 nm 부근에서 가장 크고, 초록 LED 빛 띠와 가장 많이 겹친다',s)
FIG['SPEC']=spec()
def bars():
    X0,Y0,W,H=60,270,390,220
    s,X,Y=axes(X0,Y0,W,H,(0,7),(0,0.8),[],[0,0.2,0.4,0.6,0.8],fy=lambda v:'%.1f'%v)
    s.append(T(X0+4,26,mix='흡광도 $A$ (0.15 M)',size=19,anchor='start',fill=MUTED))
    for i,(nm,v,col) in enumerate(BARV):
        x=X(i+0.5); bw=36; b=f'<rect x="{f(x-bw/2)}" y="{f(Y(v))}" width="{bw}" height="{f(Y0-Y(v))}" fill="{col}" stroke="{INK}" stroke-width="1.4"/>'
        s.append(an('scale',b,**{'from':'1,0','o':f'{f(x)},{Y0}','dur':'.7','delay':f'{0.12*i:.2f}'}))
        s.append(T(x,Y(v)-8,mix='%.2f'%v,size=18)); s.append(T(x,Y0+24,mix=nm,size=18))
    return svg('0 0 460 330',460,'0.15 M 용액에서 빛 조합별 흡광도: 초록 빛 하나가 0.60으로 가장 크고, 빛을 섞으면 흡광도가 작아진다',s)
FIG['BARS']=bars()

# ═══ S21 색상환
def wheel():
    s=[]; cx,cy,R1,R0=200,190,150,64
    cols=[('빨강',LR),('주황','#F28C28'),('노랑','#E8C21B'),('초록',LG),('파랑',LB),('보라','#7B3FC4')]
    for i,(nm,col) in enumerate(cols):
        a0=math.radians(-90+60*i-30); a1=math.radians(-90+60*i+30)
        p=lambda r,a:(cx+r*math.cos(a),cy+r*math.sin(a))
        o0,o1,i1,i0=p(R1,a0),p(R1,a1),p(R0,a1),p(R0,a0)
        s.append(f'<path d="M{f(o0[0])} {f(o0[1])} A{R1} {R1} 0 0 1 {f(o1[0])} {f(o1[1])} L{f(i1[0])} {f(i1[1])} A{R0} {R0} 0 0 0 {f(i0[0])} {f(i0[1])} Z" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>')
        m=p((R1+R0)/2,math.radians(-90+60*i)); s.append(T(m[0],m[1]+7,mix=nm,size=19,fill='#FFFFFF' if nm not in ('노랑',) else INK,weight=700))
    g=A(cx+0,cy+R0-6,cx+0,cy-R0+6,'ink',3)+A(cx+0,cy-R0+6,cx+0,cy+R0-6,'ink',3)
    s.append(an('pop',g,o=f'{cx},{cy}',dur='.6',delay='.4')); s.append(T(cx+10,cy+7,mix='보색',size=19,anchor='start',halo=True))
    s.append(T(cx,cy+R1+34,mix='초록을 흡수 → 분홍(빨강 쪽)으로 보임',size=19))
    return svg('0 0 400 390',390,'빨강·주황·노랑·초록·파랑·보라 색상환에서 마주 보는 색이 보색이며, 초록을 흡수한 용액은 빨강 쪽 분홍으로 보인다',s)
FIG['WHEEL']=wheel()

# ═══ S22 측정 표 (HTML)
def data():
    r=['<table class="tight ac29-dat"><tr><th>시료</th><th>센서 값 $I$</th><th>$T=I/I_0$</th><th>$A=-\\log T$</th></tr>',
       f'<tr><td>증류수</td><td>{I00} $(I_0)$</td><td>1.000</td><td>0</td></tr>']
    for (c,i),(_,a) in zip(STD,STDA):
        r.append(f'<tr><td>{c:.2f} M</td><td>{i}</td><td><span class="step" data-g="d1">{i/I00:.3f}</span></td><td><span class="step" data-g="d1">{a:.3f}</span></td></tr>')
    r.append(f'<tr><td>미지</td><td>{UNK}</td><td><span class="step" data-g="d1">{UNK/I00:.3f}</span></td><td><span class="step" data-g="d1">{AUNK:.3f}</span></td></tr></table>')
    return ''.join(r)
FIG['DATA']=data()

# ═══ S23 표준 검증 곡선
def curve():
    X0,Y0,W,H=78,330,440,284
    s,X,Y=axes(X0,Y0,W,H,(0,0.30),(0,1.2),[0,0.05,0.10,0.15,0.20,0.25,0.30],[0,0.2,0.4,0.6,0.8,1.0,1.2],fx=lambda v:'%.2f'%v if v else '0',fy=lambda v:'%.1f'%v if v else '0')
    s.append(T(X0+W,Y0+52,mix='농도 $c$ [M]',size=19,anchor='end',fill=MUTED)); s.append(T(X0+6,26,mix='흡광도 $A$',size=19,anchor='start',fill=MUTED))
    s.append(an('draw',L(X(0),Y(0),X(0.29),Y(SLOPE*0.29),FIELD,3),dur='1',delay='.8'))
    for k,(c,a) in enumerate(STDA): s.append(pop(C(X(c),Y(a),7,INK,2,fill=INK),X(c),Y(a),0.12*k))
    s.append(T(X(0.17),Y(SLOPE*0.25)-6,mix=f'$y={SLOPE:.2f}x$, $R^2={R2:.4f}$',size=19,anchor='end',fill=FIELD,halo=True))
    g=[L(X0,Y(AUNK),X(CUNK),Y(AUNK),EQUI,2.2,dash='7 5'),L(X(CUNK),Y(AUNK),X(CUNK),Y0,EQUI,2.2,dash='7 5'),C(X(CUNK),Y(AUNK),7,EQUI,2,fill='#FFFFFF'),
       T(X0+8,Y(AUNK)-10,mix='미지 0.479',size=18,anchor='start',fill=EQUI,halo=True),T(X(CUNK)+8,Y0-12,mix=f'{CUNK:.3f} M',size=18,anchor='start',fill=EQUI,halo=True)]
    s.append(step(g,'u1'))
    return svg('0 0 560 390',550,'염화 코발트 표준 용액 다섯 개의 흡광도가 원점을 지나는 직선 위에 있고, 미지 용액 흡광도 0.479는 0.120 M에 해당한다',s)
FIG['CURVE']=curve()

# ═══ S24 흡광도–시간
def fade():
    X0,Y0,W,H=44,118,226,96
    s=[A(X0,Y0,X0+W+10,Y0,'muted',2),A(X0,Y0,X0,Y0-H-10,'muted',2)]
    s.append(T(X0+W+8,Y0+24,mix='시간',size=18,anchor='end',fill=MUTED)); s.append(T(X0+6,14,mix='흡광도',size=18,anchor='start',fill=MUTED))
    s.append(an('draw',P([(X0+W*t/40,Y0-H*0.92*math.exp(-3*t/40)) for t in range(41)],INK,3),dur='1.2'))
    return svg('0 0 290 158',270,'색이 옅어지는 반응에서 흡광도가 시간에 따라 줄어드는 곡선',s)
FIG['FADE']=fade()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused)
