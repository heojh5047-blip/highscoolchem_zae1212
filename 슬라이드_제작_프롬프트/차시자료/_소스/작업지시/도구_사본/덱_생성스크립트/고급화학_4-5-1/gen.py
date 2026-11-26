# -*- coding: utf-8 -*-
"""고급화학 4-5-1 반응 메커니즘과 촉매 — 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   labs_src.js → labs.js(ac451cat), extra_src.css → extra.css, meta.json도 쓴다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)
   반응 에너지 도표는 4-4-1과 같은 도우미(코사인 보간), 기체 부피–시간 곡선은 실험실과 같은 1차 반응 모형(calc.py)."""
import math, random, re, sys, os, shutil
from math import log, exp, sqrt, pi
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FD='4-5-1_반응_메커니즘과_촉매'
OUT=BASE+FD+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-5-1_반응_메커니즘과_촉매/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FD), OUT
FIG={}
HL='#FFE45C'; Rg=8.314; RA=22; RH=14   # C·N·O 반지름 22(4-4-1과 같음), H 14
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def stp(body,g=None): return f'<g class="step"'+(f' data-g="{g}"' if g else '')+f'>{body}</g>'
def atom(x,y,el,r=None,lab=None):
    r=r or (RH if el=='H' else RA)
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def lt(x,y,s,size=18,anchor='middle',fill=None,weight=None,halo=False): return T(x,y,mix=s,size=size,anchor=anchor,fill=fill,weight=weight,halo=halo)
def dot(x,y,col,r=6,fill=None): return C(x,y,r,col,2,fill or col)
def bond(x1,y1,x2,y2,dash=None,w=7): return L(x1,y1,x2,y2,'#9AA5B1',w,dash,extra='stroke-linecap="round"')
def pol(x,y,d,ang): return x+d*math.cos(math.radians(ang)), y-d*math.sin(math.radians(ang))

# ═════ 반응 에너지 도표 도우미 (4-4-1과 같음) ═════
class ED:
    def __init__(s,x0,y0,w,h,Elo,Ehi): s.x0,s.y0,s.w,s.h,s.Elo,s.Ehi=x0,y0,w,h,Elo,Ehi
    def X(s,t): return s.x0+t*s.w
    def Y(s,E): return s.y0-(E-s.Elo)/(s.Ehi-s.Elo)*s.h
    def axes(s,yl='에너지',xl='반응 진행 경로',size=18):
        o=A(s.x0,s.y0,s.x0,s.y0-s.h-24,'muted',2)+A(s.x0,s.y0,s.x0+s.w+22,s.y0,'muted',2)
        o+=lt(s.x0+10,s.y0-s.h-8,yl,size,'start')+lt(s.x0+s.w+18,s.y0+30,xl,size,'end')
        return o
    def path(s,nodes,n=40):
        P_=[]
        for (t1,e1),(t2,e2) in zip(nodes,nodes[1:]):
            for i in range(n+1 if (t2,e2)==nodes[-1] else n):
                u=i/n; P_.append((s.X(t1+(t2-t1)*u),s.Y(e1+(e2-e1)*(1-math.cos(pi*u))/2)))
        return P_
    def curve(s,nodes,col=INK,w=3.5,dash=None): return P(s.path(nodes),col,w,dash=dash)
    def guide(s,t1,t2,E): return L(s.X(t1),s.Y(E),s.X(t2),s.Y(E),MUTED,1.6,'6 5')
    def up(s,t,E1,E2,col='equi',w=2.5): return A(s.X(t),s.Y(E1),s.X(t),s.Y(E2),col,w)
def one(Er,Ets,Ep,a=.16,b=.47,c=.8): return [(0,Er),(a,Er),(b,Ets),(c,Ep),(1,Ep)]
def two(Er,T1,I,T2,Ep): return [(0,Er),(.1,Er),(.3,T1),(.48,I),(.64,T2),(.85,Ep),(1,Ep)]
CAT='6 5'   # 촉매 경로 = field 점선(공통 약속 4절)

# 과산화 수소 분해 모형(calc.py와 같음): 촉매 없음 76(교과서), I⁻ 57, MnO2 50, 카탈레이스 23 kJ/mol (H2O2 1 mol당), ΔH −95
H2O2_U=one(0,76,-95)
H2O2_C=[(0,0),(.1,0),(.3,57),(.47,22),(.62,45),(.84,-95),(1,-95)]

def cover():
    w=540; e=ED(60,330,400,270,-140,100); s=[]
    s.append(e.axes())
    s.append(an('draw',e.curve(H2O2_U,INK,4),dur='1.5'))
    s.append(an('draw',e.curve(H2O2_C,FIELD,4,CAT),dur='1.5',delay='.6'))
    s.append(e.guide(.1,.5,0)+e.guide(.18,.5,76)+e.guide(.84,1,-95))
    s.append(an('draw',e.up(.2,0,76),delay='1.4',dur='.5')+lt(e.X(.2)-8,e.Y(38),'$E_\\mathrm{a}$',20,'end',fill=EQUI,halo=True))
    s.append(lt(e.X(.47)+16,e.Y(76)-12,'촉매 없음',19,'start')+lt(e.X(.66),e.Y(45)+40,'촉매',19,'start',fill=FIELD,weight=700))
    s.append(lt(e.X(.06),e.Y(0)-14,'반응물',18)+lt(e.X(.95),e.Y(-95)-14,'생성물',18,'end'))
    return svg((w,380),w,'표지: 촉매가 있을 때와 없을 때의 반응 에너지 도표 — 촉매는 활성화 에너지가 낮은 새 경로를 연다',s,cls='fig cover-fig')
FIG['COVER']=cover()

def zeo():
    w=520; s=[]; a=34; h3=a*sqrt(3)
    nodes=set(); edges=[]
    for i in range(-1,8):
        for j in range(-1,4):
            cx=40+i*1.5*a; cy=40+j*h3+(h3/2 if i%2 else 0)
            pts=[(cx+a*math.cos(math.radians(60*k)),cy+a*math.sin(math.radians(60*k))) for k in range(6)]
            for k in range(6):
                p1=(round(pts[k][0],1),round(pts[k][1],1)); p2=(round(pts[(k+1)%6][0],1),round(pts[(k+1)%6][1],1))
                if all(10<=v[0]<=w-10 and 10<=v[1]<=250 for v in (p1,p2)):
                    edges.append((p1,p2)); nodes.add(p1); nodes.add(p2)
    for p1,p2 in edges: s.append(L(p1[0],p1[1],p2[0],p2[1],MUTED,4))
    for x,y in nodes: s.append(C(x,y,7,'#7E8B98',2,'#C9CED6'))
    s.append(C(40+3*1.5*a,40+1*h3+h3/2,a*0.62,EQUI,2.5,'none','5 4'))
    gx,gy=40+3*1.5*a,40+1*h3+h3/2
    s.append(an('move',gm(gx,gy,9),**{'from':'140,-60','dur':'1.8','ease':'out'}))
    s.append(lt(10,282,'주황 점선 원: 세공(미세한 구멍) — 분자가 드나들며 반응',18,'start',fill=EQUI))
    s.append(lt(w-10,306,'제올라이트 골격(모식도)',18,'end',fill=MUTED))
    return svg((w,314),w,'제올라이트의 다공성 골격 모식도: 규칙적인 미세한 구멍으로 분자가 드나들며 흡착·반응한다',s)
FIG['ZEO']=zeo()

def tube(x,top,bot,wid,liq,foam=0):
    o=P([(x-wid/2,top),(x-wid/2,bot-wid/2)],GLASS,3)+P([(x+wid/2,top),(x+wid/2,bot-wid/2)],GLASS,3)
    o+=f'<path d="M{f(x-wid/2)} {f(bot-wid/2)} A{f(wid/2)} {f(wid/2)} 0 0 0 {f(x+wid/2)} {f(bot-wid/2)}" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    o+=f'<path d="M{f(x-wid/2+2)} {f(liq)} L{f(x-wid/2+2)} {f(bot-wid/2)} A{f(wid/2-2)} {f(wid/2-2)} 0 0 0 {f(x+wid/2-2)} {f(bot-wid/2)} L{f(x+wid/2-2)} {f(liq)} Z" fill="{WATER}" stroke="none"/>'
    return o
def yeast():
    w=520; s=[]; rnd=random.Random(3)
    for x,lab,n,foam in ((140,'과산화 수소수',3,0),(380,'과산화 수소수 + 효모',16,1)):
        s.append(tube(x,40,250,70,150))
        if foam:
            for k in range(14):
                bx=x+rnd.uniform(-26,26); by=rnd.uniform(70,148)
                s.append(C(bx,by,rnd.uniform(5,10),WATER_S,1.5,'#FFFFFF'))
            s.append(R(x-24,225,48,16,'#8A6D3B',1.5,'#C9A46A',4))
        for k in range(n):
            bx=x+rnd.uniform(-24,24); by=rnd.uniform(160,230); r=rnd.uniform(3,6)
            s.append(an('move',C(bx,by,r,WATER_S,1.5,'#FFFFFF'),**{'from':f'0,{rnd.randint(40,70)}','dur':f'{1.2+rnd.random():.1f}','rep':'loop','ease':'in'}))
        s.append(lt(x,282,lab,19))
    s.append(lt(380,30,'거품(산소) 많이',18,fill=FIELD,weight=700)+lt(140,30,'거품 거의 없음',18,fill=MUTED))
    return svg((w,292),w,'같은 양의 과산화 수소수: 효모를 넣은 쪽에서만 산소 거품이 많이 생긴다',s)
FIG['YEAST']=yeast()

def review():
    w=480; e=ED(50,230,380,190,-80,130); s=[]
    s.append(A(50,230,50,26,'muted',2)+A(50,230,446,230,'muted',2)+lt(60,22,'에너지',18,'start')+lt(446,258,'반응 진행 경로',18,'end'))
    N=[(0,0),(.08,0),(.28,90),(.5,30),(.7,60),(.9,-50),(1,-50)]
    s.append(an('draw',e.curve(N),dur='1.4'))
    s.append(lt(e.X(.28),e.Y(90)-10,'‡',20,fill=MUTED)+lt(e.X(.7),e.Y(60)-10,'‡',20,fill=MUTED))
    s.append(dot(e.X(.5),e.Y(30),EQUI)+lt(e.X(.5),e.Y(30)+30,'중간체',18,fill=EQUI,halo=True))
    s.append(lt(e.X(.05),e.Y(0)-12,'반응물',18,'start')+lt(e.X(.98),e.Y(-50)-12,'생성물',18,'end'))
    return svg((w,268),w,'4-4-1 탐구 활동 (다): 봉우리 두 개와 골짜기(중간체)가 있는 두 단계 반응의 에너지 도표',s)
FIG['REVIEW']=review()

def no2m(x,y,rot):
    o=[]; d=40
    for a in (rot,rot+134): o.append(bond(x,y,*pol(x,y,d,a)))
    o.append(atom(x,y,'N'))
    for a in (rot,rot+134): o.append(atom(*pol(x,y,d,a),'O'))
    return ''.join(o)
def no3m(x,y,rot=90,hl=False):
    o=[]; d=42
    for a in (rot,rot+120,rot+240): o.append(bond(x,y,*pol(x,y,d,a)))
    o.append(atom(x,y,'N'))
    for a in (rot,rot+120,rot+240): o.append(atom(*pol(x,y,d,a),'O'))
    if hl: o.append(C(x,y,d+RA+8,EQUI,2.5,'none','6 4'))
    return ''.join(o)
def nom(x,y): return bond(x,y-4,x+40,y-4)+bond(x,y+4,x+40,y+4)+atom(x,y,'N')+atom(x+40,y,'O')
def o2m(x,y): return bond(x,y-4,x+40,y-4)+bond(x,y+4,x+40,y+4)+atom(x,y,'O')+atom(x+40,y,'O')
def o3m(x,y):
    a=pol(x,y,40,150); b=pol(x,y,40,30)
    return bond(x,y,*a)+bond(x,y,*b)+atom(*a,'O')+atom(x,y,'O')+atom(*b,'O')
def com(x,y,flip=False):
    c,ox=(x,x+40) if not flip else (x+40,x)
    return bond(x,y,x+40,y)+bond(x,y-7,x+40,y-7)+bond(x,y+7,x+40,y+7)+atom(c,y,'C')+atom(ox,y,'O')
def co2m(x,y): return bond(x,y,x+80,y,w=7)+atom(x,y,'O')+atom(x+40,y,'C')+atom(x+80,y,'O')
def n2o5(x,y):
    nl=pol(x,y,44,210); nr=pol(x,y,44,330); o=[bond(x,y,*nl),bond(x,y,*nr)]
    ol=[pol(*nl,40,150),pol(*nl,40,270)]; orr=[pol(*nr,40,30),pol(*nr,40,270)]
    for p in ol: o.append(bond(*nl,*p))
    for p in orr: o.append(bond(*nr,*p))
    o.append(atom(x,y,'O')+atom(*nl,'N')+atom(*nr,'N')+''.join(atom(*p,'O') for p in ol+orr))
    return ''.join(o)
def unibi():
    w=1080; s=[]
    s.append(R(6,6,520,236,MUTED,2,'#F7F8FA',14)+R(554,6,520,236,MUTED,2,'#F7F8FA',14))
    s.append(lt(266,40,'1분자 반응: 한 분자가 쪼개진다',20,weight=700)+lt(814,40,'2분자 반응: 두 분자가 충돌한다',20,weight=700))
    s.append(n2o5(110,120)+A(200,130,250,130,'ink',3))
    s.append(an('move',no2m(320,140,20),**{'from':'-50,0','dur':'1.2','delay':'.3','ease':'out'}))
    s.append(an('move',no3m(440,140,90),**{'from':'-90,0','dur':'1.2','delay':'.3','ease':'out'}))
    s.append(lt(110,218,'$\\ce{N2O5}$',19)+lt(380,218,'$\\ce{NO2 + NO3}$',19))
    s.append(an('move',nom(600,130),**{'from':'-36,0','dur':'1','rep':'alt','ease':'io'}))
    s.append(an('move',o3m(735,140),**{'from':'36,0','dur':'1','rep':'alt','ease':'io'}))
    s.append(A(790,130,830,130,'ink',3))
    s.append(no2m(890,140,20)+o2m(980,130))
    s.append(lt(680,218,'$\\ce{NO + O3}$',19)+lt(940,218,'$\\ce{NO2 + O2}$',19))
    return svg((w,248),w,'1분자 반응(N2O5 한 분자가 NO2와 NO3로 쪼개짐)과 2분자 반응(NO와 O3가 충돌하여 NO2와 O2 생성)',s)
FIG['UNIBI']=unibi()

def molec():
    w=520; s=[]
    def ball(x,y,lab,col): return C(x,y,22,col,2.5,'#FDE2E4' if col==PLUS else ('#E3EEFB' if col==MINUS else '#F2F2F2'))+lt(x,y+7,lab,19,fill=col,weight=700)
    rows=[(60,'1분자',[ (120,60,'A',PLUS)],[]),
          (160,'2분자',[(100,160,'A',PLUS),(180,160,'B',MINUS)],[(130,160,150,160)]),
          (260,'3분자',[(90,260,'A',PLUS),(170,240,'B',MINUS),(150,300,'C',INK)],[])]
    for y,lab,balls,_ in rows:
        s.append(lt(14,y+7,lab,19,'start',weight=700))
        for bx,by,bl,col in balls: s.append(ball(bx+40,by,bl,col))
    s.append(lt(260,67,'저절로 분해·자리 바꿈',18,'start',fill=MUTED))
    s.append(lt(260,167,'가장 흔함',18,'start',fill=FIELD,weight=700))
    s.append(lt(260,262,'셋이 동시에, 알맞은 방향과',18,'start',fill=PLUS)+lt(260,290,'에너지로 만날 확률 → 매우 낮음',18,'start',fill=PLUS))
    s.append(an('move',ball(140,160,'A',PLUS),**{'from':'-30,0','dur':'1','rep':'alt','ease':'io'}) if False else '')
    return svg((w,320),w,'분자도: 1분자, 2분자, 3분자 반응 — 3분자 반응은 매우 드물다',s)
FIG['MOLEC']=molec()

def bottle():
    w=1000; s=[]; y=110
    s.append(P([(20,y-60),(330,y-60),(400,y-22),(600,y-22),(670,y-60),(980,y-60)],MUTED,3))
    s.append(P([(20,y+60),(330,y+60),(400,y+22),(600,y+22),(670,y+60),(980,y+60)],MUTED,3))
    s.append(R(400,y-22,200,44,'none',0,HL,extra='fill-opacity=".45"'))
    rnd=random.Random(2)
    def car(x,yy,col): return R(x-18,yy-10,36,20,col,2,'#FFFFFF',5)
    for k in range(9):
        x=40+k*32; yy=y+rnd.choice((-30,0,30))
        s.append(an('move',car(x,yy,MINUS),**{'from':'-30,0','dur':'1.4','rep':'loop','ease':'lin'}))
    for k in range(3):
        s.append(an('move',car(430+k*70,y,PLUS),**{'from':'-70,0','dur':'2.4','rep':'loop','ease':'lin'}))
    for k in range(3):
        s.append(an('move',car(720+k*100,y+rnd.choice((-30,30)),FIELD),**{'from':'-60,0','dur':'1.2','rep':'loop','ease':'lin'}))
    s.append(lt(175,y+96,'1단계: 넓은 길(빠름)',19,fill=MINUS)+lt(500,y+96,'2단계: 좁은 다리(가장 느림)',19,fill=PLUS,weight=700)+lt(825,y+96,'3단계: 넓은 길(빠름)',19,fill=FIELD))
    s.append(lt(500,y+130,'1분에 지나가는 차의 수는 좁은 다리가 정한다 = 속도 결정 단계',19,fill=INK))
    return svg((w,250),w,'넓은 길–좁은 다리–넓은 길: 가장 좁은 곳이 전체 흐름을 정하는 것처럼 가장 느린 단계가 전체 반응 속도를 정한다',s)
FIG['BOTTLE']=bottle()

def mech1():
    w=1080; s=[]
    # 1단계: NO2 + NO2 → NO3 + NO (O 원자 하나가 옮겨 감)
    y=80
    s.append(lt(20,y+8,'1단계',20,'start',weight=700)+lt(20,y+36,'느림',19,'start',fill=PLUS,weight=700))
    s.append(no2m(120,y+10,-23)+lt(200,y+18,'+',24)+no2m(285,y+10,200))
    s.append(C(*pol(285,y+10,40,200),RA+6,EQUI,2.5,'none','5 4'))
    s.append(A(370,y+6,440,y+6,'ink',3)+lt(405,y-8,'$k_1$',19))
    s.append(an('move',no3m(530,y+10,90,True),**{'from':'-40,0','dur':'1','ease':'out'}))
    s.append(lt(620,y+18,'+',24)+nom(660,y+4))
    s.append(lt(900,y+16,'$\\ce{NO3}$: 중간체',19,'start',fill=EQUI,weight=700))
    y=220
    s.append(lt(20,y+8,'2단계',20,'start',weight=700)+lt(20,y+36,'빠름',19,'start',fill=FIELD,weight=700))
    s.append(no3m(165,y+6,90,True)+lt(250,y+14,'+',24)+com(282,y+6))
    s.append(C(*pol(165,y+6,42,330),RA+6,EQUI,2.5,'none','5 4'))
    s.append(A(370,y+6,440,y+6,'ink',3)+lt(405,y-8,'$k_2$',19))
    s.append(no2m(510,y+16,20)+lt(590,y+14,'+',24))
    s.append(an('move',co2m(630,y+6),**{'from':'-40,0','dur':'1','delay':'.4','ease':'out'}))
    s.append(lt(900,y+14,'O 원자가 C로',19,'start',fill=MUTED))
    s.append(L(14,150,1066,150,'#E2E7EC',1.5))
    return svg((w,292),w,'NO2와 CO 반응의 두 단계 메커니즘: 1단계 NO2 두 분자 사이 O 원자 이동으로 NO3 생성(느림), 2단계 NO3가 CO에 O 원자를 주어 CO2 생성(빠름)',s)
FIG['MECH1']=mech1()

def ed2():
    w=620; e=ED(80,350,470,290,-270,175); s=[]; N=two(0,132,96,116,-226)
    s.append(e.axes())
    s.append(an('draw',e.curve(N),dur='1.6'))
    s.append(lt(e.X(.04),e.Y(0)+28,'$\\ce{2NO2 + CO}$',19,'start'))
    s.append(lt(e.X(.48),e.Y(96)+34,'$\\ce{NO3 + NO + CO}$',18,halo=True))
    s.append(dot(e.X(.48),e.Y(96),EQUI,7))
    s.append(lt(e.X(1),e.Y(-226)+28,'$\\ce{NO2 + NO + CO2}$',19,'end'))
    s.append(lt(e.X(.3),e.Y(132)-12,'‡',22,fill=MUTED)+lt(e.X(.64),e.Y(116)-12,'‡',22,fill=MUTED))
    s.append(stp(lt(e.X(.3),e.Y(132)-40,'활성화 착물 1',18,fill=MUTED)+lt(e.X(.48),e.Y(96)+60,'중간체(골짜기)',18,fill=EQUI,weight=700,halo=True),'i1'))
    s.append(stp(e.guide(.1,.3,0)+e.up(.17,0,132)+lt(e.X(.17)-8,e.Y(66),'$E_\\mathrm{a1}$',19,'end',fill=EQUI,halo=True)+e.guide(.5,.68,96)+e.up(.6,96,116)+lt(e.X(.6)+10,e.Y(78),'$E_\\mathrm{a2}$',18,'start',fill=EQUI,halo=True),'i2'))
    s.append(lt(e.X(0)+4,e.Y(-270)+30,'(단위: kJ/mol, 모형)',18,'start',fill=MUTED))
    return svg((w,410),w,'NO2와 CO 반응의 두 단계 반응 에너지 도표: 1단계 봉우리가 가장 높고 골짜기에 중간체 NO3',s)
FIG['ED2']=ed2()

def ed3():
    w=500; e=ED(60,270,400,220,-130,110); s=[]
    N=[(0,0),(.08,0),(.22,22),(.36,8),(.6,80),(.86,-114),(1,-114)]
    s.append(A(60,270,60,26,'muted',2)+A(60,270,480,270,'muted',2)+lt(70,22,'에너지',18,'start')+lt(480,298,'반응 진행 경로',18,'end'))
    s.append(an('draw',e.curve(N),dur='1.4'))
    s.append(dot(e.X(.36),e.Y(8),EQUI,6)+lt(e.X(.36),e.Y(8)+30,'$\\ce{NO3}$',18,fill=EQUI,halo=True))
    s.append(lt(e.X(.2),e.Y(22)-14,'1단계: 빠른 평형',18,fill=MUTED,halo=True)+lt(e.X(.6),e.Y(80)-14,'2단계: 느림',18,fill=PLUS,weight=700,halo=True))
    s.append(lt(e.X(.04),e.Y(0)+28,'$\\ce{2NO + O2}$',18,'start')+lt(e.X(.98),e.Y(-114)-14,'$\\ce{2NO2}$',18,'end'))
    return svg((w,306),w,'2NO + O2 반응: 1단계가 빠르게 평형을 이루고 2단계(높은 봉우리)가 속도 결정 단계(모식도)',s)
FIG['ED3']=ed3()

def consec():
    w=480; s=[]; ax=Ax(60,250,380,200,4,1.0); k1,k2=1.0,3.0
    s.append(L(60,250,450,250,MUTED,2)+L(60,250,60,40,MUTED,2)+lt(450,280,'시간 $t$',18,'end')+lt(66,34,'농도',18,'start'))
    s.append(an('draw',ax.curve(lambda t:exp(-k1*t),0,4,col=INK,w=3.5),dur='1.2'))
    s.append(an('draw',ax.curve(lambda t:k1/(k2-k1)*(exp(-k1*t)-exp(-k2*t)),0,4,col=EQUI,w=3.5),dur='1.2',delay='.3'))
    s.append(an('draw',ax.curve(lambda t:1-exp(-k1*t)-k1/(k2-k1)*(exp(-k1*t)-exp(-k2*t)),0,4,col=FIELD,w=3.5),dur='1.2',delay='.6'))
    s.append(lt(ax.X(.5)+6,ax.Y(exp(-.5))-12,'반응물',18,'start',fill=INK,halo=True)+lt(ax.X(1.5),ax.Y(.24)-6,'중간체: 잠깐 생겼다 사라짐',18,'start',fill=EQUI,weight=700,halo=True)+lt(ax.X(3.6),ax.Y(.93)-14,'생성물',18,'end',fill=FIELD,halo=True))
    return svg((w,290),w,'두 단계 반응에서 반응물·중간체·생성물의 농도 변화(계산): 중간체는 잠깐 생겼다가 사라진다',s)
FIG['CONSEC']=consec()

def sn1():
    w=460; e=ED(50,240,380,190,-40,120); s=[]
    N=[(0,0),(.08,0),(.3,100),(.5,60),(.66,75),(.88,-20),(1,-20)]
    s.append(A(50,240,50,30,'muted',2)+A(50,240,440,240,'muted',2)+lt(60,26,'에너지',18,'start')+lt(440,266,'반응 진행 경로',18,'end'))
    s.append(an('draw',e.curve(N),dur='1.3'))
    s.append(dot(e.X(.5),e.Y(60),EQUI,6)+lt(e.X(.5),e.Y(60)+30,'탄소 양이온',18,fill=EQUI,weight=700,halo=True))
    s.append(lt(e.X(.3),e.Y(100)-12,'속도 결정 단계',18,fill=PLUS,halo=True))
    return svg((w,276),w,'SN1 반응 에너지 도표(모식도): 첫 봉우리가 가장 높은 속도 결정 단계, 골짜기에 탄소 양이온 중간체',s)
FIG['SN1']=sn1()

def passfig():
    w=560; s=[]
    hx=lambda x: 230-170*exp(-((x-280)/80)**2)-0*x
    pts_=[(x,hx(x)) for x in range(20,541,5)]
    s.append(P(pts_+[(540,250),(20,250)],'none',0,'#EEF1F4',close=True)+P(pts_,MUTED,3))
    lo=lambda x: 230-95*exp(-((x-280)/95)**2)
    s.append(an('draw',P([(x,lo(x)) for x in range(20,541,5)],FIELD,4,dash=CAT),dur='1.4'))
    s.append(an('draw',P(pts_,INK,4),dur='1.4'))
    s.append(lt(280,48,'높은 고개(원래 경로)',18,fill=INK,halo=True)+lt(280,lo(280)-14,'낮은 고개: 촉매가 연 새 경로',18,fill=FIELD,weight=700,halo=True))
    s.append(lt(40,270,'출발(반응물)',18,'start')+lt(520,270,'도착(생성물)',18,'end'))
    return svg((w,282),w,'촉매는 높은 고개 대신 낮은 고개로 가는 새 길(반응 경로)을 연다 — 출발점과 도착점은 그대로',s)
FIG['PASS']=passfig()

def cycle(spA,spB,in1,out1,in2,out2,lab1,lab2,w=520):
    s=[]; cx,cy,r=w/2,164,80
    s.append(f'<path d="M{f(cx-r)} {f(cy)} A{r} {r} 0 0 1 {f(cx+r)} {f(cy)}" fill="none" stroke="{FIELD}" stroke-width="4"/>')
    s.append(f'<path d="M{f(cx+r)} {f(cy)} A{r} {r} 0 0 1 {f(cx-r)} {f(cy)}" fill="none" stroke="{FIELD}" stroke-width="4"/>')
    s.append(A(cx+6,cy-r,cx+22,cy-r+1,'field',4)+A(cx-6,cy+r,cx-22,cy+r-1,'field',4))
    s.append(R(cx-r-54,cy-22,108,44,FIELD,2.5,'#E6F2EA',22)+lt(cx-r,cy+7,spA,20,weight=700))
    s.append(R(cx+r-54,cy-22,108,44,EQUI,2.5,'#FDF1E2',22)+lt(cx+r,cy+7,spB,20,weight=700))
    s.append(A(cx-40,cy-r-56,cx-14,cy-r-6,'ink',2.5)+lt(cx-44,cy-r-62,in1,19,'end'))
    if out1: s.append(A(cx+14,cy-r-6,cx+40,cy-r-56,'ink',2.5)+lt(cx+44,cy-r-62,out1,19,'start'))
    s.append(A(cx+40,cy+r+56,cx+14,cy+r+6,'ink',2.5)+lt(cx+44,cy+r+74,in2,19,'start'))
    s.append(A(cx-14,cy+r+6,cx-40,cy+r+56,'ink',2.5)+lt(cx-44,cy+r+74,out2,19,'end'))
    s.append(lt(cx,cy-r+30,lab1,18,fill=MUTED)+lt(cx,cy+r-18,lab2,18,fill=MUTED))
    s.append(an('spin',C(cx+r*math.cos(math.radians(40)),cy-r*math.sin(math.radians(40)),7,FIELD,2,FIELD),o=f'{f(cx)},{cy}',speed='60'))
    return s
def cyc1():
    w=520; s=cycle('$\\ce{I-}$','$\\ce{IO-}$','$\\ce{H2O2}$','$\\ce{H2O}$','$\\ce{H2O2}$','$\\ce{H2O + O2}$','1단계','2단계',w)
    return svg((w,332),w,'아이오딘화 이온 촉매의 순환: I⁻가 1단계에서 소모되어 IO⁻가 되고 2단계에서 다시 I⁻로 돌아온다',s)
FIG['CYC1']=cyc1()
def cyc2():
    w=520; s=cycle('$\\ce{2NO}$','$\\ce{2NO2}$','$\\ce{O2}$','','$\\ce{2SO2}$','$\\ce{2SO3}$','1단계','2단계 ×2',w)
    return svg((w,330),w,'일산화 질소 촉매의 순환: NO가 1단계에서 NO2가 되고, 2단계에서 SO2를 산화하며 다시 NO가 된다',s)
FIG['CYC2']=cyc2()

def ed33():
    w=640; e=ED(70,350,500,290,-140,105); s=[]
    s.append(e.axes())
    s.append(an('draw',e.curve(H2O2_U,INK,3.5),dur='1.5'))
    s.append(an('draw',e.curve(H2O2_C,FIELD,3.5,CAT),dur='1.5',delay='.5'))
    s.append(lt(e.X(.47)-10,e.Y(76)-14,'촉매 없음',19,'end')+lt(e.X(.47),e.Y(22)+32,'중간체',18,fill=EQUI,halo=True)+dot(e.X(.47),e.Y(22),EQUI,6))
    s.append(lt(e.X(.66),e.Y(45)-14,'촉매',19,'start',fill=FIELD,weight=700,halo=True))
    s.append(lt(e.X(.06),e.Y(0)-14,'반응물',18)+lt(e.X(.8),e.Y(-95)+28,'생성물',18,'end'))
    s.append(stp(e.guide(.08,.5,0)+e.guide(.16,.47,76)+e.up(.16,0,76)+lt(e.X(.16)-8,e.Y(40),'$76$',19,'end',fill=EQUI,halo=True)
                 +e.guide(.24,.32,57)+e.up(.24,0,57,'field')+lt(e.X(.24)+8,e.Y(28),'$57$',19,'start',fill=FIELD,halo=True),'a1'))
    s.append(stp(e.guide(.47,.9,76)+e.guide(.62,.96,45)+e.guide(.3,.4,57)+L(e.X(.3),e.Y(57),e.X(.96),e.Y(57),MUTED,1.4,'4 5')+e.up(.89,-95,76)+e.up(.95,-95,57,'field')
                 +lt(e.X(.89)-8,e.Y(-30),'$171$',19,'end',fill=EQUI,halo=True)+lt(e.X(.95)+8,e.Y(-30),'$152$',19,'start',fill=FIELD,halo=True)+lt(e.X(.92),e.Y(76)-12,'역반응',18,fill=MUTED),'a2'))
    s.append(stp(A(e.X(1.04),e.Y(0),e.X(1.04),e.Y(-95),'ink',2.5)+e.guide(.5,1.06,0)+lt(e.X(1.04)+6,e.Y(-40),'$\\Delta H$',19,'start',halo=True),'a3'))
    s.append(lt(e.X(0)+4,e.Y(-140)+30,'(단위: kJ/mol, $\\ce{H2O2}$ 1 mol당)',18,'start',fill=MUTED))
    return svg((w,410),w,'그림 Ⅳ-33처럼 촉매 유무에 따른 반응 에너지 도표: 과산화 수소 분해, 촉매가 정반응과 역반응의 활성화 에너지를 같은 크기만큼 낮추고 ΔH는 그대로',s)
FIG['ED33']=ed33()

def negcat():
    w=480; e=ED(50,250,390,200,-110,140); s=[]
    s.append(A(50,250,50,26,'muted',2)+A(50,250,460,250,'muted',2)+lt(60,22,'에너지',18,'start')+lt(460,278,'반응 진행 경로',18,'end'))
    s.append(an('draw',e.curve(one(0,110,-80),PLUS,3.5,'10 6'),dur='1.3',delay='.6'))
    s.append(an('draw',e.curve(one(0,76,-80),INK,3.5),dur='1.3'))
    s.append(an('draw',e.curve(one(0,45,-80),FIELD,3.5,CAT),dur='1.3',delay='.3'))
    s.append(lt(e.X(.47)+10,e.Y(110)-8,'부촉매',18,'start',fill=PLUS,weight=700)+lt(e.X(.55)+6,e.Y(76)-6,'촉매 없음',18,'start',halo=True)+lt(e.X(.6)+4,e.Y(40)+6,'정촉매',18,'start',fill=FIELD,weight=700,halo=True))
    return svg((w,288),w,'정촉매는 활성화 에너지를 낮추고 부촉매는 활성화 에너지가 높은 경로로 반응을 느리게 한다(모식도)',s)
FIG['NEG']=negcat()

def surface(x0,y0,n,r=16):
    return ''.join(C(x0+r+2*r*i,y0,r,'#7E8B98',2,'#C9CED6') for i in range(n))
def phase():
    w=1080; s=[]; rnd=random.Random(7)
    titles=[('균일 촉매','반응물과 같은 상태'),('불균일 촉매','반응물과 다른 상태'),('효소(생체촉매)','두 성격을 함께')]
    for i,(t1,t2) in enumerate(titles):
        x=i*360+6; s.append(R(x,6,348,284,MUTED,2,'#F7F8FA',14)+lt(x+174,38,t1,20,weight=700)+lt(x+174,64,t2,18,fill=MUTED))
    # 균일: 기체 속 NO (field 테), SO2·O2
    pts=[]
    while len(pts)<10:
        px,py=rnd.uniform(40,320),rnd.uniform(90,220)
        if all(math.hypot(px-a,py-b)>42 for a,b in pts): pts.append((px,py))
    for j,(px,py) in enumerate(pts):
        isc=j<3
        s.append(an('move',C(px,py,13,FIELD if isc else GAS_S,2.5 if isc else 1.5,'#E6F2EA' if isc else GAS),**{'from':f'{rnd.choice((-6,6))},{rnd.choice((-5,5))}','rep':'alt','dur':f'{1+rnd.random()*.5:.1f}','ease':'io'}))
    s.append(lt(180,276,'모두 기체: 촉매 $\\ce{NO(g)}$(초록 테)',18))
    # 불균일: Pt 표면
    s.append(surface(378,230,10)+lt(540,276,'고체 촉매 $\\ce{Pt(s)}$ 표면',18,fill=MUTED))
    for j in range(5):
        px=400+j*62; py=130 if j%2 else 160
        s.append(an('move',C(px,py+(48 if j in (1,3) else 0),11,GAS_S,1.5,GAS),**{'from':'0,-50','dur':'1.4','delay':f'{j*.2:.1f}','ease':'out'}))
    s.append(lt(540,105,'기체 분자가 표면에 흡착',18,fill=MUTED))
    # 효소
    ex=900
    s.append(f'<path d="M{ex-110} 230 L{ex-110} 140 Q{ex-110} 100 {ex-70} 100 L{ex-26} 100 L{ex-26} 136 L{ex+26} 136 L{ex+26} 100 L{ex+70} 100 Q{ex+110} 100 {ex+110} 140 L{ex+110} 230 Z" fill="#E6F2EA" stroke="{FIELD}" stroke-width="3"/>')
    s.append(an('move',R(ex-24,104,48,30,EQUI,2.5,HL,6),**{'from':'0,-56','dur':'1.4','ease':'out'}))
    s.append(lt(ex,276,'활성 자리에 기질이 꼭 맞음',18,fill=FIELD))
    return svg((w,296),w,'균일 촉매(모두 기체), 불균일 촉매(고체 백금 표면에 기체 흡착), 효소(활성 자리에 기질 결합) 비교',s)
FIG['PHASE']=phase()

def ethylene(x,y,sc=1.0):
    d=38*sc; o=[bond(x,y-4,x+d,y-4,w=6),bond(x,y+4,x+d,y+4,w=6)]
    hs=[pol(x,y,30,150),pol(x,y,30,210),pol(x+d,y,30,30),pol(x+d,y,30,-30)]
    for i,h in enumerate(hs): o.append(bond(x if i<2 else x+d,y,*h,w=5))
    o.append(atom(x,y,'C',18,'-')+atom(x+d,y,'C',18,'-')+''.join(atom(*h,'H',11,'-') for h in hs))
    return ''.join(o)
def ethane(x,y):
    d=40; o=[bond(x,y,x+d,y,w=6)]; hs=[]
    for a in (90,180,270): hs.append(((x,y),pol(x,y,30,a)))
    for a in (90,0,270): hs.append(((x+d,y),pol(x+d,y,30,a)))
    for (c,h) in hs: o.append(bond(*c,*h,w=5))
    o.append(atom(x,y,'C',18,'-')+atom(x+d,y,'C',18,'-')+''.join(atom(*h,'H',11,'-') for c,h in hs))
    return ''.join(o)
def hyd():
    w=1080; s=[]; pw=264
    caps=['1단계: $\\ce{H2}$ 물리적 흡착','2단계: H–H 끊어짐(속도 결정)','3단계: C–H 하나 생성','4단계: 에테인 이탈']
    for i in range(4):
        x=i*(pw+8)+4
        s.append(R(x,4,pw,240,MUTED,1.5,'#FBFCFD',12)+surface(x+4,212,8))
        s.append(lt(x+pw/2,270,caps[i],18,fill=PLUS if i==1 else INK,weight=700 if i==1 else None))
    # 1
    x=4; s.append(an('move',bond(x+90,186,x+120,186,w=5)+atom(x+90,186,'H',11,'-')+atom(x+120,186,'H',11,'-'),**{'from':'0,-90','dur':'1.2','ease':'out'}))
    s.append(ethylene(x+150,70))
    # 2
    x=4+(pw+8); s.append(an('move',atom(x+70,190,'H',11,'-'),**{'from':'30,0','dur':'1','delay':'.3','ease':'out'})+an('move',atom(x+150,190,'H',11,'-'),**{'from':'-50,0','dur':'1','delay':'.3','ease':'out'}))
    s.append(ethylene(x+110,80))
    # 3
    x=4+2*(pw+8)
    s.append(atom(x+190,190,'H',11,'-'))
    s.append(an('move',ethylene(x+60,150),**{'from':'0,-70','dur':'1.2','ease':'out'}))
    s.append(L(x+128,150,x+140,176,EQUI,4,'5 4')+atom(x+140,184,'H',11,'-'))
    # 4
    x=4+3*(pw+8)
    s.append(an('move',ethane(x+110,90),**{'from':'0,80','dur':'1.4','ease':'out'}))
    s.append(A(x+130,150,x+130,124,'ink',2.5))
    s.append(lt(1074,298,'흰 공: H · 검은 공: C · 회색 공: 금속 촉매($\\ce{Pt}$, $\\ce{Ni}$) 원자',18,'end',fill=MUTED))
    return svg((w,304),w,'그림 Ⅳ-34처럼 에틸렌의 불균일 촉매 수소화 4단계: 수소 흡착, H–H 결합 끊어짐(속도 결정 단계), C–H 결합 생성, 에테인 이탈',s)
FIG['HYD']=hyd()

def conv():
    w=1000; s=[]
    s.append(R(20,90,180,80,MUTED,3,'#EEF1F4',8)+R(800,90,180,80,MUTED,3,'#EEF1F4',8))
    s.append(P([(200,90),(280,40),(720,40),(800,90)],MUTED,3)+P([(200,170),(280,220),(720,220),(800,170)],MUTED,3))
    for i in range(16):
        x=300+i*26; s.append(L(x,46,x,214,'#9AA5B1',3))
    for j in range(6):
        y=60+j*28; s.append(L(286,y,714,y,'#9AA5B1',2))
    s.append(R(296,46,184,168,'none',0,'#B48EDB',extra='fill-opacity=".22"')+R(520,46,190,168,'none',0,'#9FC3DD',extra='fill-opacity=".3"'))
    s.append(lt(388,248,'$\\ce{Rh}$: $\\ce{NO}$ → $\\ce{N2}$ (환원)',18)+lt(615,248,'$\\ce{Pt}$/$\\ce{Pd}$: $\\ce{CO}$ → $\\ce{CO2}$ (산화)',18))
    for k,(lab,y) in enumerate((('$\\ce{NO}$',112),('$\\ce{CO}$',152))):
        s.append(an('move',C(70+k*60,y-8,13,GAS_S,1.5,GAS),**{'from':'-40,0','dur':'1.4','rep':'loop','ease':'lin'}))
    s.append(lt(110,70,'배기가스 $\\ce{NO}$, $\\ce{CO}$',18)+lt(890,70,'$\\ce{N2}$, $\\ce{CO2}$',18))
    for k in range(2): s.append(an('move',C(850+k*60,124+k*20,13,FIELD,1.5,'#E6F2EA'),**{'from':'-40,0','dur':'1.4','rep':'loop','ease':'lin'}))
    s.append(A(10,130,40,130,'ink',3)+A(960,130,995,130,'ink',3))
    s.append(lt(500,30,'벌집 모양 담체 표면에 금속 촉매',18,fill=MUTED))
    return svg((w,262),w,'자동차 촉매 전환기 모식도: 벌집 모양 표면의 Rh가 NO를 N2로, Pt/Pd가 CO를 CO2로 바꾼다',s)
FIG['CONV']=conv()

def enz():
    w=1080; s=[]
    def E(x,y,notch=True):
        return (f'<path d="M{x-90} {y+70} L{x-90} {y} Q{x-90} {y-40} {x-50} {y-40} L{x-24} {y-40} L{x-24} {y-6} L{x+24} {y-6} L{x+24} {y-40} L{x+50} {y-40} Q{x+90} {y-40} {x+90} {y} L{x+90} {y+70} Z" fill="#E6F2EA" stroke="{FIELD}" stroke-width="3"/>')
    def Sb(x,y): return R(x-22,y-18,44,34,EQUI,2.5,HL,6)
    def Ph(x,y): return R(x-22,y-18,20,34,EQUI,2.5,'#FFF6C2',4)+R(x+2,y-18,20,34,EQUI,2.5,'#FFF6C2',4)
    y=140
    s.append(E(120,y)+lt(120,y+50,'E 효소',19,weight=700)+lt(250,y+10,'+',26)+Sb(320,y-12)+lt(320,y+50,'S 기질',19,weight=700))
    s.append(A(380,y,450,y,'ink',3))
    s.append(E(560,y)+an('move',Sb(560,y-23),**{'from':'-60,-50','dur':'1.2','ease':'out'})+lt(560,y+50,'ES 효소-기질 복합체',19,weight=700))
    s.append(lt(560,y-80,'활성 자리',18,fill=FIELD)+A(560,y-70,560,y-46,'field',2))
    s.append(A(670,y,740,y,'ink',3))
    s.append(E(850,y)+lt(850,y+50,'E 효소',19,weight=700)+lt(965,y+10,'+',26))
    s.append(an('move',Ph(1030,y-12),**{'from':'-170,-12','dur':'1.2','delay':'1','ease':'out'})+lt(1030,y+50,'P 생성물',19,weight=700))
    s.append(lt(415,y-16,'느림',18,fill=PLUS,weight=700)+lt(705,y-16,'빠름',18,fill=FIELD))
    return svg((w,214),w,'효소 촉매 반응: 효소 E의 활성 자리에 기질 S가 꼭 맞게 결합해 ES를 만들고, 생성물 P를 내놓으며 효소는 그대로 남는다',s)
FIG['ENZ']=enz()

def app():
    w=540; s=[]
    s.append(R(10,170,200,120,RD,2,'#E3F2F6',10)+lt(110,284,'물중탕(온도 조절)',18,fill=RD))
    s.append(P([(80,60),(80,120),(40,230),(180,230),(140,120),(140,60)],GLASS,3))
    s.append(P([(58,180),(162,180),(176,226),(44,226)],'none',0,WATER,close=True))
    s.append(R(90,214,40,10,'#5B4636',1,'#3A2E25',3))
    s.append(R(74,48,72,16,INK,2,'#7E8B98',3))
    rnd=random.Random(4)
    for k in range(6):
        bx=rnd.uniform(70,150); s.append(an('move',C(bx,205,4,WATER_S,1.5,'#FFFFFF'),**{'from':'0,20','dur':f'{.8+rnd.random()*.6:.1f}','rep':'loop','ease':'in'}))
    s.append(P([(110,48),(110,26),(260,26),(260,96)],INK,3))
    s.append(R(250,96,270,52,GLASS,3,'#F7F8FA',8))
    for k in range(6): s.append(L(280+k*40,148,280+k*40,158,MUTED,1.5)+lt(280+k*40,178,str(k*20),18,fill=MUTED))
    s.append(an('move',R(262,100,10,44,INK,2,'#7E8B98',2)+L(272,122,520,122,INK,4),**{'from':'-120,0','dur':'2.4','ease':'out'}) if False else '')
    s.append(an('move',R(380,100,10,44,INK,2,'#7E8B98',2)+L(390,122,530,122,INK,4),**{'from':'-110,0','dur':'2.4','ease':'out'}))
    s.append(lt(385,82,'기체 주사기 [mL]',18,fill=MUTED))
    s.append(lt(230,214,'과산화 수소수 5 mL',18,'start')+lt(230,238,'+ 촉매(바닥)',18,'start',fill='#5B4636'))
    return svg((w,296),w,'과산화 수소 촉매 분해 장치: 삼각 플라스크(물중탕) → 기체 주사기로 산소 부피를 시간마다 읽는다',s)
FIG['APP']=app()

# 실험실과 같은 1차 반응 모형
EA={'none':76,'KI':57,'MnO2':50,'cat':23}; K25={'none':2.0e-7,'KI':0.010,'MnO2':0.025,'cat':0.050}
def kk(c,t):
    T=t+273.15; v=K25[c]*exp(-EA[c]*1000/Rg*(1/T-1/298.15))
    if c=='cat': v*=(1/(1+exp((t-45)/3)))/(1/(1+exp((25-45)/3)))
    return v
def Vmax(p): return p*10/34.01*0.005/2*24.5*1000
SERIES=[('cat','카탈레이스(감자)',RD,None),('MnO2','$\\ce{MnO2}$',INK,None),('KI','$\\ce{KI}$',BF,None),('none','촉매 없음',MUTED,'7 5')]
def res(w=560):
    s=[]; ax=Ax(70,270,420,220,180,60)
    s.append(ax.frame((0,30,60,90,120,150,180),(0,20,40,60),lt(ax.x0-6,ax.y0-ax.h-18,'$V_{\\ce{O2}}$ [mL]',18,'start'),lt(ax.x0+ax.w,ax.y0+50,'$t$ [s]',18,'end')))
    for i,(c,lab,col,dash) in enumerate(SERIES):
        k=kk(c,25); fn=lambda t,k=k:Vmax(3)*(1-exp(-k*t))
        s.append(an('draw',ax.curve(fn,0,180,col=col,w=3.5,dash=dash),dur='1.4',delay=f'{i*.25:.2f}'))
    s.append(lt(ax.X(14),ax.Y(50),'카탈레이스',18,'start',fill=RD,halo=True)+lt(ax.X(48),ax.Y(41),'$\\ce{MnO2}$',18,'start',fill=INK,halo=True)+lt(ax.X(100),ax.Y(30),'$\\ce{KI}$',18,'start',fill=BF,halo=True)+lt(ax.X(178),ax.Y(0)-12,'촉매 없음',18,'end',fill=MUTED,halo=True))
    s.append(L(ax.X(0),ax.Y(Vmax(3)),ax.X(180),ax.Y(Vmax(3)),MUTED,1.4,'4 4')+lt(ax.X(180)+4,ax.Y(Vmax(3))+6,'54',18,'start',fill=MUTED))
    return svg((w,330),w,'25 °C, 3 % 과산화 수소수 5 mL의 산소 부피–시간 곡선(계산 모형): 촉매마다 빠르기는 다르지만 최종 부피 54 mL는 같다',s)
FIG['RES']=res()

def pr3():
    w=520; e=ED(60,300,400,250,-170,150); s=[]
    s.append(A(60,300,60,30,'muted',2)+A(60,300,480,300,'muted',2)+lt(70,26,'에너지',18,'start')+lt(480,328,'반응 진행 경로',18,'end'))
    s.append(an('draw',e.curve(one(0,130,-137)),dur='1.4'))
    Nc=[(0,0),(.1,0),(.22,35),(.32,15),(.44,50),(.56,10),(.68,30),(.84,-137),(1,-137)]
    s.append(an('draw',e.curve(Nc,FIELD,3.5,CAT),dur='1.4',delay='.4'))
    s.append(lt(e.X(.47)+12,e.Y(130)-6,'촉매 없음: $E_\\mathrm{a}$ 매우 큼',18,'start',halo=True)+lt(e.X(.5),e.Y(50)-18,'$\\ce{Pt}$ 촉매: 여러 단계',18,'start',fill=FIELD,weight=700,halo=True))
    s.append(lt(e.X(.04),e.Y(0)+28,'$\\ce{C2H4 + H2}$',18,'start')+lt(e.X(.98),e.Y(-137)+28,'$\\ce{C2H6}$',18,'end'))
    s.append(A(e.X(.9),e.Y(0),e.X(.9),e.Y(-137),'ink',2.5)+e.guide(.6,1,0)+lt(e.X(.9)+8,e.Y(-60),'경로와',18,'start',halo=True)+lt(e.X(.9)+8,e.Y(-60)+24,'무관',18,'start',halo=True))
    return svg((w,336),w,'에틸렌 수소화의 반응 에너지 도표(모식도): 촉매가 없으면 활성화 에너지가 매우 크고, Pt 촉매는 낮은 여러 단계 경로를 연다. 반응물과 생성물의 차이는 경로와 무관',s)
FIG['PR3']=pr3()

# ═════ 조립 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
keys=re.findall(r'\{\{(\w+)\}\}',tpl)
for k in keys:
    if k not in FIG: sys.exit('no fig '+k)
html=re.sub(r'\{\{(\w+)\}\}',lambda m:FIG[m.group(1)],tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(html)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
shutil.copy(os.path.join(HERE,'labs_src.js'),OUT+'labs.js')
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "반응 메커니즘과 촉매", "file": "4-5-1_반응_메커니즘과_촉매", "header": "Ⅳ-5-1 반응 메커니즘과 촉매 (고등 고급 화학 249–258쪽)"}\n')
print('ok',len(html),'sections',html.count('<section'),'anim',html.count('data-anim'))
if set(FIG)-set(keys): print('unused figs',set(FIG)-set(keys))
