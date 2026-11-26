# -*- coding: utf-8 -*-
"""고급화학 4-4-1 충돌 모형과 활성화 에너지 — 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   labs_src.js → labs.js(ac441diag), extra_src.css → extra.css, meta.json도 쓴다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)
   에너지 분포 곡선은 맥스웰–볼츠만 에너지 분포 f(E)=2/√π·(RT)^(-3/2)·√E·e^(-E/RT), 아레니우스 그래프는 k=Ae^(-Ea/RT) 계산값(calc.py와 같은 값).
   반응 에너지 도표 곡선은 반응물–활성화 착물–(중간체–활성화 착물)–생성물 에너지를 코사인 보간으로 이은 것."""
import math, random, re, sys, os, shutil
from math import log, exp, sqrt, pi, erfc
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FD='4-4-1_충돌_모형과_활성화_에너지'
OUT=BASE+FD+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-4-1_충돌_모형과_활성화_에너지/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FD), OUT
FIG={}
HL='#FFE45C'; Rg=8.314; RA=22   # C·N·O 원자 반지름(덱 전체)
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def stp(body,g=None): return f'<g class="step"'+(f' data-g="{g}"' if g else '')+f'>{body}</g>'
def atom(x,y,el,r=RA,lab=None):
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def lt(x,y,s,size=18,anchor='middle',fill=None,weight=None,halo=False): return T(x,y,mix=s,size=size,anchor=anchor,fill=fill,weight=weight,halo=halo)
def ylab(ax,s,size=18): return lt(ax.x0-6,ax.y0-ax.h-16,s,size,'start')
def xlab(ax,s,size=18,dy=48): return lt(ax.x0+ax.w/2,ax.y0+dy,s,size)
def pts(fn,ax,a,b,n=200): return [(ax.X(a+(b-a)*i/n),ax.Y(fn(a+(b-a)*i/n))) for i in range(n+1)]
def dot(x,y,col,r=6,fill=None): return C(x,y,r,col,2,fill or col)
def bond(x1,y1,x2,y2,dash=None): return L(x1,y1,x2,y2,'#9AA5B1',7,dash,extra='stroke-linecap="round"')
# 맥스웰–볼츠만 에너지 분포 (E, RT: kJ/mol)
def fE(E,T): RT=Rg*T/1000; return 2/sqrt(pi)*RT**-1.5*sqrt(max(E,0))*exp(-E/RT)
def frac(Ea,T): x=Ea*1000/(Rg*T); return erfc(sqrt(x))+2*sqrt(x/pi)*exp(-x)

# ═════ 반응 에너지 도표 도우미 ═════
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

def cover():
    w=540; e=ED(60,330,390,270,-260,170); s=[]; N=one(0,132,-226)
    s.append(e.axes())
    s.append(an('draw',e.curve(N,INK,4),dur='1.6'))
    s.append(e.guide(.16,.62,0)+e.guide(.47,.98,-226)+e.guide(.3,.62,132))
    s.append(an('draw',e.up(.36,0,132),delay='1.2',dur='.6')+lt(e.X(.36)-8,e.Y(66),'$E_\\mathrm{a}$',20,'end',fill=EQUI,halo=True))
    s.append(an('draw',A(e.X(.92),e.Y(0),e.X(.92),e.Y(-226),'ink',2.5),delay='1.5',dur='.6')+lt(e.X(.92)-8,e.Y(-110),'$\\Delta H$',20,'end',halo=True))
    s.append(lt(e.X(.08),e.Y(0)-14,'$\\ce{NO2 + CO}$',19)+lt(e.X(.86),e.Y(-226)-14,'$\\ce{NO + CO2}$',19,'end'))
    s.append(lt(e.X(.47),e.Y(132)-16,'활성화 착물',19,fill=MUTED))
    return svg((w,380),w,'표지: 이산화 질소와 일산화 탄소 반응의 반응 에너지 도표(활성화 에너지와 반응 엔탈피)',s,cls='fig cover-fig')
FIG['COVER']=cover()

def hill():
    w=560; s=[]; base=230
    hx=lambda x: base-150*exp(-((x-300)/95)**2)
    pts_=[(x,hx(x)) for x in range(20,561,5)]
    s.append(P(pts_+[(560,base+20),(20,base+20)],'none',0,'#E6F2EA',close=True)+P(pts_,FIELD,3.5))
    def bike(x,y):
        o=C(x-20,y-12,12,INK,2.5)+C(x+20,y-12,12,INK,2.5)+P([(x-20,y-12),(x-4,y-34),(x+14,y-34),(x+20,y-12)],INK,2.5)
        o+=L(x-4,y-34,x+2,y-52,PLUS,5)+C(x+4,y-62,8,PLUS,2,PLUS)
        return o
    x=245; y=hx(x)
    ang=math.degrees(math.atan2(hx(x+1)-hx(x-1),2))
    s.append(f'<g data-anim="move" data-from="-150,72" data-dur="2.2" data-ease="out"><g transform="rotate({ang:.1f} {x} {y})">'+bike(x,y)+'</g></g>')
    s.append(L(300,hx(300),300,base,EQUI,1.5,'5 4')+A(470,base,470,hx(300),'equi',2.5)+L(300,hx(300),480,hx(300),MUTED,1.4,'5 4'))
    s.append(lt(462,(base+hx(300))/2,'넘어야 할||높이',18,'end',fill=EQUI,halo=True))
    s.append(lt(300,hx(300)-14,'언덕 꼭대기',18,fill=MUTED))
    return svg((w,262),w,'자전거가 언덕을 넘으려면 꼭대기까지 오를 에너지가 필요함',s)
FIG['HILL']=hill()

def think():
    w=520; s=[]; sc=19
    def fruit(x,y,col):
        return C(x,y,17,col,2,col if col!='#8A6D3B' else '#B08C55')+P([(x,y-17),(x+3,y-27)],'#5B3A1A',2.5)+P([(x+3,y-24),(x+14,y-30),(x+8,y-21)],FIELD,1.5,'#7CC08F',close=True)
    rows=[(70,'실온 $20\\ {}^\\circ\\text{C}$',5,PLUS),(170,'냉장고 $0\\ {}^\\circ\\text{C}$',20,MINUS)]
    for y,lab,d,col in rows:
        s.append(lt(10,y-30,lab,19,'start',fill=col,weight=700))
        s.append(an('draw',L(60,y,60+d*sc,y,col,18),dur=f'{0.3+d*0.06:.1f}'))
        s.append(fruit(30,y,'#E04B3A')+lt(60+d*sc+10,y+7,f'{d}일',19,'start',fill=col))
    s.append(L(60,205,60+20*sc,205,MUTED,1.5))
    for d in (0,5,10,15,20): s.append(L(60+d*sc,205,60+d*sc,211,MUTED,1.5)+lt(60+d*sc,232,str(d),18,fill=MUTED))
    s.append(lt(60+20*sc,256,'같은 정도로 썩기까지 걸린 날 [일]',18,'end',fill=MUTED))
    return svg((w,266),w,'흠집 난 과일이 같은 정도로 썩기까지: 20 °C에서 5일, 0 °C에서 20일',s)
FIG['THINK']=think()

def link():
    w=440; s=[]; N2=0.02802
    ax=Ax(40,200,370,165,1400,0.0024)
    s.append(L(40,200,420,200,MUTED,2)+L(40,200,40,25,MUTED,2))
    s.append(an('draw',ax.curve(lambda v:mb(v,300,N2),0,1400,col=MINUS,w=3.5),dur='1.2'))
    s.append(an('draw',ax.curve(lambda v:mb(v,600,N2),0,1400,col=PLUS,w=3.5),dur='1.2',delay='.4'))
    s.append(T(ax.X(vp(300,N2))+12,ax.Y(mb(vp(300,N2),300,N2))+4,tex='T_1',size=20,fill=MINUS,anchor='start'))
    s.append(T(ax.X(vp(600,N2))+30,ax.Y(mb(vp(600,N2),600,N2))+4,tex='T_2',size=20,fill=PLUS,anchor='start'))
    s.append(lt(420,226,'속력 $v$',18,'end',fill=MUTED)+lt(48,22,'분자 수 비율',18,'start',fill=MUTED))
    return svg((w,236),w,'질소의 속력 분포(계산): 300 K와 600 K, 온도가 높으면 빠른 분자가 많아짐',s)
FIG['LINK']=link()

def zfp():
    w=1060; s=[]
    # Z: 충돌
    s.append(R(10,10,320,190,MUTED,2,'#F7F8FA',12)+lt(170,44,'$Z$ 충돌 빈도',20,weight=700))
    s.append(an('move',C(95,120,24,GAS_S,2,GAS)+A(122,120,150,120,'ink',2.5),**{'from':'-40,0','dur':'1.2','rep':'alt','ease':'io'}))
    s.append(an('move',C(245,120,24,GAS_S,2,GAS)+A(218,120,190,120,'ink',2.5),**{'from':'40,0','dur':'1.2','rep':'alt','ease':'io'}))
    s.append(lt(170,184,'1초에 몇 번 부딪치나',18,fill=MUTED))
    # f: 에너지
    s.append(R(370,10,320,190,MUTED,2,'#F7F8FA',12)+lt(530,44,'$f$ 에너지 조건',20,weight=700))
    ax=Ax(400,160,260,95,30,0.17)
    tail=[(ax.X(10),ax.Y(0))]+[(ax.X(E),ax.Y(fE(E,600))) for E in [10+i*0.5 for i in range(41)]]+[(ax.X(30),ax.Y(0))]
    s.append(P(tail,'none',0,HL,extra='fill-opacity=".55"',close=True)+L(400,160,665,160,MUTED,2)+ax.curve(lambda E:fE(E,600),0,30,col=INK,w=3))
    s.append(L(ax.X(10),160,ax.X(10),72,EQUI,2.5)+lt(ax.X(10)+6,86,'$E_\\mathrm{a}$',19,'start',fill=EQUI))
    s.append(lt(530,184,'$E_\\mathrm{a}$ 이상일 확률',18,fill=MUTED))
    # p: 방향
    s.append(R(730,10,320,190,MUTED,2,'#F7F8FA',12)+lt(890,44,'$p$ 방향 조건',20,weight=700))
    s.append(C(800,92,18,FIELD,2,'#E6F2EA')+C(836,92,10,FIELD,2,FIELD)+C(892,92,18,FIELD,2,'#E6F2EA')+lt(950,99,'반응 ○',19,'start',fill=FIELD))
    s.append(C(800,140,18,PLUS,2,'#FDE2E4')+C(764,140,10,PLUS,2,PLUS)+C(892,140,18,PLUS,2,'#FDE2E4')+lt(950,147,'반응 ×',19,'start',fill=PLUS))
    s.append(lt(890,184,'알맞은 방향일 확률',18,fill=MUTED))
    return svg((w,210),w,'속도 상수를 이루는 세 요인: 충돌 빈도 Z, 에너지 조건 f, 방향 조건 p',s)
FIG['ZFP']=zfp()

def no2(x,y,rot,pre='',dash=False):
    """NO2: N 중심, O 두 개(∠ONO 134°). rot = 첫 O의 방향(도)."""
    o=[]; d=40
    ang=[rot,rot+134]
    for a in ang: o.append(bond(x,y,x+d*math.cos(math.radians(a)),y-d*math.sin(math.radians(a))))
    o.append(atom(x,y,'N'))
    for a in ang: o.append(atom(x+d*math.cos(math.radians(a)),y-d*math.sin(math.radians(a)),'O'))
    return ''.join(o)
def co(x,y,flip=False):
    c,ox=(x,x+40) if not flip else (x+40,x)
    return bond(x,y,x+40,y)+bond(x,y-7,x+40,y-7)+bond(x,y+7,x+40,y+7)+atom(c,y,'C')+atom(ox,y,'O')
def orient():
    w=600; s=[]
    rows=[(70,'효과적 충돌','반응이 일어난다',FIELD),(200,'비효과적 충돌','N 원자가 C 원자와 충돌',PLUS),(330,'비효과적 충돌','O 원자가 O 원자와 충돌',PLUS)]
    for i,(y,t1,t2,col) in enumerate(rows):
        if i==0: m=no2(120,y,0); c_=co(204,y)   # O(→) 끝 x=160+22, C at 204
        elif i==1: m=no2(130,y,180-67); c_=co(176,y)   # N이 오른쪽을 향함: O 두 개는 왼쪽(113°, 247°)
        else: m=no2(120,y,0); c_=co(204,y,True)  # O가 CO의 O와
        s.append(an('move',m,**{'from':'-50,0','dur':'1.1','delay':f'{i*.3:.1f}','ease':'out'}))
        s.append(an('move',c_,**{'from':'50,0','dur':'1.1','delay':f'{i*.3:.1f}','ease':'out'}))
        cx=182 if i!=1 else 154
        star=P([(cx+16*math.cos(math.radians(k*36-90))*(1 if k%2==0 else .45),y+16*math.sin(math.radians(k*36-90))*(1 if k%2==0 else .45)) for k in range(10)],EQUI,2,HL,close=True)
        if i==0: s.append(an('pop',star,o=f'{cx},{y}',delay='1.1'))
        s.append(lt(330,y-6,t1,20,'start',fill=col,weight=700)+lt(330,y+24,t2,19,'start',fill=MUTED))
    s.append(L(20,135,580,135,'#E2E7EC',1.5)+L(20,265,580,265,'#E2E7EC',1.5))
    return svg((w,390),w,'이산화 질소와 일산화 탄소의 충돌 방향: O 원자가 C 원자와 부딪칠 때만 효과적',s)
FIG['ORIENT']=orient()

def conc():
    w=1000; s=[]; rnd=random.Random(5)
    boxes=[(20,2,2),(350,4,2),(680,4,4)]
    for bx,na,nb in boxes:
        s.append(R(bx,10,300,190,INK,2.5,'#FFFFFF',8))
        P_=[]
        while len(P_)<na+nb:
            px,py=rnd.uniform(bx+30,bx+270),rnd.uniform(40,170)
            if all(math.hypot(px-a,py-b)>58 for a,b in P_): P_.append((px,py))
        for j,(px,py) in enumerate(P_):
            isA=j<na; col=PLUS if isA else MINUS
            body=C(px,py,19,col,2.5,'#FDE2E4' if isA else '#E3EEFB')+lt(px,py+7,'A' if isA else 'B',19,fill=col,weight=700)
            s.append(an('move',body,**{'from':f'{rnd.choice((-6,6))},{rnd.choice((-5,5))}','rep':'alt','dur':f'{1.0+rnd.random()*.5:.1f}','ease':'io'}))
        s.append(lt(bx+150,236,f'A {na}개 · B {nb}개',19))
        s.append(stp(lt(bx+150,266,f'A–B 충돌 쌍 {na*nb}가지',19,fill=FIELD,weight=700),'cc'))
    return svg((w,280),w,'부피가 같은 세 용기: A와 B의 수가 늘면 A–B 충돌 쌍의 수가 4, 8, 16으로 늘어남',s)
FIG['CONC']=conc()

def q01():
    w=560; s=[]
    opts=[(60,'ㄱ',no2(100,60,180-67),co(146,60)),(178,'ㄴ',no2(90,178,0),co(174,178)),(300,'ㄷ',no2(90,300,0),co(174,300,True))]
    for y,lab,m,c_ in opts: s.append(lt(20,y+7,lab,22,'start',weight=700)+m+c_)
    s.append(stp(R(12,116,520,100,FIELD,3,'none',10)+lt(470,186,'유효',20,'end',fill=FIELD,weight=700),'q1'))
    return svg((w,350),w,'이산화 질소와 일산화 탄소가 충돌하는 세 가지 방향 ㄱ, ㄴ, ㄷ',s)
FIG['Q01']=q01()

def ed30():
    w=640; e=ED(70,350,500,290,-320,175); s=[]; N=one(0,132,-226)
    s.append(e.axes())
    s.append(an('draw',e.curve(N),dur='1.6'))
    s.append(lt(e.X(.08),e.Y(0)+28,'$\\ce{NO2 + CO}$',19)+lt(e.X(.08),e.Y(0)+54,'반응물',18,fill=MUTED))
    s.append(lt(e.X(.84),e.Y(-226)+28,'$\\ce{NO + CO2}$',19)+lt(e.X(.84),e.Y(-226)+54,'생성물',18,fill=MUTED))
    s.append(lt(e.X(.47),e.Y(132)-48,'활성화 착물',19,fill=MUTED)+lt(e.X(.47),e.Y(132)-18,'$[\\ce{ON}\\cdots\\ce{O}\\cdots\\ce{CO}]^\\ddagger$',19))
    s.append(stp(e.guide(.16,.47,0)+e.guide(.3,.47,132)+e.up(.3,0,132)+lt(e.X(.3)-8,e.Y(66)-6,'$E_{\\mathrm{a},f}=$||$132\\ \\text{kJ/mol}$',19,'end',fill=EQUI,halo=True),'e1'))
    s.append(stp(e.guide(.47,.75,132)+e.up(.72,-226,132)+lt(e.X(.72)+8,e.Y(60),'$E_{\\mathrm{a},r}=358$||$\\text{kJ/mol}$',19,'start',fill=EQUI,halo=True),'e2'))
    s.append(stp(e.guide(.47,1,0)+A(e.X(.97),e.Y(0),e.X(.97),e.Y(-226),'ink',2.5)+lt(e.X(.97)-8,e.Y(-150),'$\\Delta H=-226$||$\\text{kJ/mol}$',19,'end',halo=True),'e3'))
    return svg((w,410),w,'그림 Ⅳ-30처럼 NO2와 CO 반응의 반응 에너지 도표: 정반응 활성화 에너지 132, 역반응 358, 반응열 −226 kJ/mol',s)
FIG['ED30']=ed30()

def tsmol():
    w=1080; s=[]
    # 반응물
    s.append(no2(80,120,0)+co(160,120))
    s.append(lt(150,210,'$\\ce{NO2 + CO}$',20)+lt(150,238,'반응물',18,fill=MUTED))
    s.append(A(290,120,340,120,'ink',3))
    # 활성화 착물: O–N···O···C≡O (N–O 하나는 끊어지는 중, O–C는 생기는 중)
    x=440; y=120
    s.append(bond(x,y,x+40*math.cos(math.radians(134)),y-40*math.sin(math.radians(134))))
    s.append(L(x,y,x+66,y,EQUI,5,'6 6')+L(x+66,y,x+132,y,EQUI,5,'6 6'))
    s.append(bond(x+132,y,x+172,y)+bond(x+132,y-7,x+172,y-7)+bond(x+132,y+7,x+172,y+7))
    s.append(atom(x,y,'N')+atom(x+40*math.cos(math.radians(134)),y-40*math.sin(math.radians(134)),'O')+atom(x+66,y,'O')+atom(x+132,y,'C')+atom(x+172,y,'O'))
    s.append(an('fade',R(x-60,40,300,140,EQUI,2,'none',14,'8 6'),dur='1.2',rep='alt'))
    s.append(lt(x+86,214,'$[\\ce{ON}\\cdots\\ce{O}\\cdots\\ce{CO}]^\\ddagger$',20)+lt(x+86,242,'활성화 착물(전이 상태)',18,fill=MUTED))
    s.append(lt(x+40,72,'끊어지는 중',18,fill=EQUI,halo=True)+lt(x+99,172,'생기는 중',18,fill=EQUI,halo=True))
    s.append(A(700,120,750,120,'ink',3))
    # 생성물 NO + CO2
    s.append(bond(800,120,840,120)+bond(800,113,840,113)+atom(800,120,'N')+atom(840,120,'O'))
    s.append(bond(900,120,940,120)+bond(940,120,980,120)+atom(900,120,'O')+atom(940,120,'C')+atom(980,120,'O'))
    s.append(lt(890,210,'$\\ce{NO + CO2}$',20)+lt(890,238,'생성물',18,fill=MUTED))
    return svg((w,250),w,'반응물 NO2 + CO가 활성화 착물을 거쳐 NO + CO2가 되는 결합 변화(점선: 끊어지거나 생기는 중인 결합)',s)
FIG['TSMOL']=tsmol()

def eascale():
    w=1060; s=[]; X=lambda E:60+E*3.0; y=140
    s.append(R(X(40),y-24,X(300)-X(40),48,'none',0,FIELD,extra='fill-opacity=".15"'))
    s.append(A(50,y,X(330),y,'muted',2.5))
    for E in range(0,321,40): s.append(L(X(E),y-8,X(E),y+8,MUTED,1.6)+lt(X(E),y+36,str(E),18,fill=MUTED))
    s.append(lt(X(330),y+150,'활성화 에너지 [kJ/mol]',18,'end',fill=MUTED))
    s.append(lt((X(40)+X(300))/2,y+116,'초록 띠 = 대부분의 반응: 40–300 kJ/mol (10–75 kcal/mol)',19,fill=FIELD,weight=700))
    s.append(L(X(80),y-96,X(80),y+30,EQUI,3,'7 5')+lt(X(80)-8,y-104,'← 상온 이하에서도 일어남',18,'end',fill=EQUI)+lt(X(80)+8,y-104,'상온 이상에서 일어남 →',18,'start',fill=EQUI))
    for E,lab,up in ((19,'$\\ce{O3 + O}$ 19',False),(46,'과일이 썩는 반응 46',True),(132,'$\\ce{NO2 + CO}$ 132',False),(166,'$\\ce{H2 + I2}$ 166',True)):
        s.append(an('pop',dot(X(E),y,INK,7),o=f'{f(X(E))},{y}',delay=f'{E/200:.2f}'))
        s.append(L(X(E),y+(10 if not up else -10),X(E),y+(52 if not up else -46),INK,1.5)+lt(X(E),y+(74 if not up else -54),lab,18,fill=INK,halo=True))
    return svg((w,300),w,'활성화 에너지의 크기: 대부분 40–300 kJ/mol, 80 kJ/mol보다 작으면 상온 이하에서도 반응',s)
FIG['EASCALE']=eascale()

def q03():
    w=560; e=ED(80,330,430,280,0,260); s=[]; N=one(50,230,130)
    s.append(A(80,330,80,26,'muted',2)+A(80,330,532,330,'muted',2))
    for E in (0,50,100,150,200,250):
        s.append(L(74,e.Y(E),80,e.Y(E),MUTED,1.5)+lt(68,e.Y(E)+6,str(E),18,'end',fill=MUTED)+(L(80,e.Y(E),510,e.Y(E),'#E2E7EC',1) if E else ''))
    s.append(lt(90,22,'에너지 [kJ/mol]',18,'start')+lt(530,360,'반응 진행 경로',18,'end'))
    s.append(an('draw',e.curve(N),dur='1.4'))
    s.append(lt(e.X(.08),e.Y(50)-12,'반응물',18)+lt(e.X(.93),e.Y(130)-12,'생성물',18))
    s.append(stp(e.up(.3,50,230)+lt(e.X(.3)-8,e.Y(140),'180',19,'end',fill=EQUI,halo=True),'q3a'))
    s.append(stp(A(e.X(.9),e.Y(50),e.X(.9),e.Y(130),'ink',2.5)+L(e.X(.16),e.Y(50),e.X(.92),e.Y(50),MUTED,1.5,'5 4')+lt(e.X(.9)-8,e.Y(90)+6,'+80',19,'end',halo=True),'q3b'))
    s.append(stp(e.up(.7,130,230)+lt(e.X(.7)+8,e.Y(180),'100',19,'start',fill=EQUI,halo=True),'q3c'))
    return svg((w,370),w,'어떤 반응의 반응 에너지 도표: 반응물 50, 활성화 착물 230, 생성물 130 kJ/mol',s)
FIG['Q03']=q03()

EaM=50.0
def tempk():
    w=520; s=[]; ts=[0,10,20,30,40]; ks=[exp(EaM*1000/Rg*(1/273.15-1/(t+273.15))) for t in ts]
    ax=Ax(70,280,400,230,45,ks[-1]*1.15,xmin=-5)
    s.append(L(70,280,480,280,MUTED,2)+L(70,280,70,40,MUTED,2))
    for y in (0,5,10,15): s.append(L(64,ax.Y(y),70,ax.Y(y),MUTED,1.5)+lt(58,ax.Y(y)+6,str(y),18,'end',fill=MUTED)+(L(70,ax.Y(y),470,ax.Y(y),'#E2E7EC',1) if y else ''))
    for i,(t,k) in enumerate(zip(ts,ks)):
        x=ax.X(t)
        s.append(an('scale',R(x-26,ax.Y(k),52,ax.Y(0)-ax.Y(k),PLUS,2,'#FDE2E4',3),**{'from':'1,0','o':f'{f(x)},280','delay':f'{i*.15:.2f}','dur':'.7'}))
        s.append(lt(x,302,f'{t}',18)+lt(x,ax.Y(k)-10,f'{k:.1f}',18,fill=PLUS))
        if i: s.append(lt((ax.X(ts[i-1])+x)/2,ax.Y(k)-36,f'×{ks[i]/ks[i-1]:.1f}',18,fill=MUTED))
    s.append(lt(480,334,'온도 [°C]',18,'end')+lt(76,24,'속도 상수 (0 °C를 1로)',18,'start'))
    return svg((w,344),w,'활성화 에너지 50 kJ/mol인 반응의 속도 상수(계산): 10 °C마다 약 2배',s)
FIG['TEMPK']=tempk()

def arr():
    w=480; s=[]; Ts=[273+i for i in range(0,101)]; kr=lambda T:exp(EaM*1000/Rg*(1/273.15-1/T))
    ax=Ax(70,280,380,240,373,kr(373)*1.08,xmin=273)
    s.append(ax.frame((273,298,323,348,373),(100,200,300),ylab(ax,'$k$ (273 K를 1로)'),xlab(ax,'$T$ [K]',dy=50),yfmt=lambda v:str(v)))
    s.append(an('draw',P([(ax.X(T),ax.Y(kr(T))) for T in Ts],PLUS,3.5),dur='1.4'))
    s.append(lt(ax.X(280),ax.Y(300),'$E_\\mathrm{a}=50\\ \\text{kJ/mol}$',18,'start',fill=MUTED,halo=True))
    return svg((w,346),w,'아레니우스 식으로 계산한 속도 상수–절대 온도 그래프: 지수 함수로 증가',s)
FIG['ARR']=arr()

# N2O5 분해 아레니우스 모형: Ea 103 kJ/mol, 45 °C에서 t1/2 = 24 min (4-3-1과 같음)
EaN=103e3; k45=log(2)/(24*60); lnAN=log(k45)+EaN/(Rg*318.15)
NT=[25,35,45,55,65]; NX=[1/(t+273.15) for t in NT]; NY=[lnAN-EaN/Rg*x for x in NX]
def arrln():
    w=460; s=[]; ax=Ax(70,262,350,215,0.0036,34,ymin=-14)
    s.append(ax.frame((0,0.001,0.002,0.003),(-10,0,10,20,30),ylab(ax,'$\\ln k$'),xlab(ax,'$\\dfrac{1}{T}$ [$\\text{K}^{-1}$]',dy=56),xfmt=lambda v:'0' if v==0 else f'{v:.3f}',yfmt=lambda v:str(v)))
    s.append(L(ax.x0,ax.Y(0),ax.x0+ax.w,ax.Y(0),MUTED,1.5))
    s.append(an('draw',L(ax.X(0),ax.Y(lnAN),ax.X(0.0036),ax.Y(lnAN-EaN/Rg*0.0036),INK,3.5),dur='1.2'))
    for x,y in zip(NX,NY): s.append(dot(ax.X(x),ax.Y(y),PLUS,5))
    s.append(an('pop',dot(ax.X(0),ax.Y(lnAN),EQUI,7),o=f'{f(ax.X(0))},{f(ax.Y(lnAN))}',delay='1.1')+lt(ax.X(0)+16,ax.Y(lnAN)+26,'$y$절편 $=\\ln A$',19,'start',fill=EQUI,halo=True))
    s.append(lt(ax.X(0.0019),ax.Y(lnAN-EaN/Rg*0.0019)-14,'기울기 $=-\\dfrac{E_\\mathrm{a}}{R}$',19,'start',halo=True))
    return svg((w,346),w,'오산화 이질소 분해의 ln k–1/T 그래프(계산): 직선, y절편 ln A, 기울기 −Ea/R',s)
FIG['ARRLN']=arrln()

def arrzoom():
    w=540; s=[]; ax=Ax(80,280,380,220,0.00345,-4.8,xmin=0.00290,ymin=-11)
    s.append(ax.frame((0.0029,0.0031,0.0033),(-10,-8,-6),ylab(ax,'$\\ln k$'),xlab(ax,'$\\dfrac{1}{T}$ [$\\text{K}^{-1}$]',dy=56),xfmt=lambda v:f'{v:.4f}',yfmt=lambda v:str(v)))
    s.append(an('draw',L(ax.X(0.00293),ax.Y(lnAN-EaN/Rg*0.00293),ax.X(0.00338),ax.Y(lnAN-EaN/Rg*0.00338),INK,3),dur='1'))
    for i,(x,y,t) in enumerate(zip(NX,NY,NT)):
        s.append(an('pop',dot(ax.X(x),ax.Y(y),PLUS,6),o=f'{f(ax.X(x))},{f(ax.Y(y))}',delay=f'{i*.12:.2f}'))
        if t==25: s.append(lt(ax.X(x)+(12 if t==25 else -12),ax.Y(y)+(-10 if t==25 else 26),f'{t} °C',18,'start' if t==25 else 'end',fill=MUTED))
    x1,y1,x2,y2=NX[4],NY[4],NX[0],NY[0]
    s.append(stp(L(ax.X(x1),ax.Y(y1),ax.X(x2),ax.Y(y1),EQUI,2.5,'6 4')+L(ax.X(x2),ax.Y(y1),ax.X(x2),ax.Y(y2),EQUI,2.5,'6 4')
        +lt((ax.X(x1)+ax.X(x2))/2,ax.Y(y1)-10,'$\\Delta\\tfrac{1}{T}=3.97\\times10^{-4}$',18,fill=EQUI,halo=True)
        +lt(ax.X(x2)+8,(ax.Y(y1)+ax.Y(y2))/2,'$\\Delta\\ln k$||$=-4.92$',18,'start',fill=EQUI,halo=True),'sl'))
    return svg((w,350),w,'25–65 °C 자료 다섯 점의 ln k–1/T 그래프와 기울기 삼각형',s)
FIG['ARRZOOM']=arrzoom()

def arr2():
    w=520; s=[]; ax=Ax(80,300,380,240,0.00340,3.4,xmin=0.00290,ymin=-0.4)
    s.append(ax.frame((0.0029,0.0031,0.0033),(0,1,2,3),ylab(ax,'$\\ln\\dfrac{k}{k_{298\\,\\mathrm{K}}}$'),xlab(ax,'$\\dfrac{1}{T}$ [$\\text{K}^{-1}$]',dy=56),xfmt=lambda v:f'{v:.4f}',yfmt=lambda v:str(v)))
    for E,col,dash,lab,yy in ((10,MINUS,'9 6','$E_\\mathrm{a}=10\\ \\text{kJ/mol}$',0),(60,PLUS,None,'$E_\\mathrm{a}=60\\ \\text{kJ/mol}$',1)):
        g=lambda x,E=E:E*1000/Rg*(1/298-x)
        s.append(an('draw',L(ax.X(0.00292),ax.Y(g(0.00292)),ax.X(0.00338),ax.Y(g(0.00338)),col,3.5,dash),dur='1.1'))
        for T in (298,308): s.append(dot(ax.X(1/T),ax.Y(g(1/T)),col,5))
        s.append(lt(ax.X(0.00300 if yy else 0.00294)+(14 if yy else 0),ax.Y(g(0.00300 if yy else 0.00294))+(4 if yy else -14),lab,18,'start',fill=col,halo=True))
    return svg((w,370),w,'활성화 에너지 10과 60 kJ/mol 반응의 ln k–1/T 직선(계산): 기울기가 클수록 온도 의존성이 큼',s)
FIG['ARR2']=arr2()

Em=10.0; T1m,T2m=300,600
def mbe(w=560,small=False):
    s=[]; ax=Ax(70,300,w-120,240,30,0.30)
    s.append(L(70,300,w-40,300,MUTED,2)+L(70,300,70,40,MUTED,2))
    for TT,col,op in ((T2m,HL,'.55'),(T1m,MINUS,'.22')):
        tail=[(ax.X(Em),ax.Y(0))]+[(ax.X(E),ax.Y(fE(E,TT))) for E in [Em+i*0.25 for i in range(81)]]+[(ax.X(30),ax.Y(0))]
        s.append(P(tail,'none',0,col,extra=f'fill-opacity="{op}"',close=True))
    s.append(an('draw',ax.curve(lambda E:fE(E,T1m),0,30,col=MINUS,w=3.5,n=240),dur='1.3'))
    s.append(an('draw',ax.curve(lambda E:fE(E,T2m),0,30,col=PLUS,w=3.5,n=240),dur='1.3',delay='.3'))
    s.append(L(ax.X(Em),300,ax.X(Em),60,EQUI,3)+lt(ax.X(Em),320,'$E_\\mathrm{a}$',19,fill=EQUI))
    s.append(T(ax.X(1.6),ax.Y(fE(1.2,T1m))-10,tex='T_1',size=20,fill=MINUS,anchor='start'))
    s.append(T(ax.X(6),ax.Y(fE(6,T2m))-12,tex='T_2',size=20,fill=PLUS,anchor='start'))
    s.append(lt(w-60,90,'$T_2&gt;T_1$',19,'end'))
    s.append(lt(w-40,330,'분자 운동 에너지',18,'end',fill=MUTED)+lt(78,36,'분자 분율',18,'start',fill=MUTED))
    if not small:
        s.append(stp(lt(ax.X(16),ax.Y(0.075),f'$T_2$: $E_\\mathrm{{a}}$ 이상 {frac(Em,T2m)*100:.0f} %',19,'start',fill=PLUS,halo=True)+lt(ax.X(16),ax.Y(0.075)+28,f'$T_1$: $E_\\mathrm{{a}}$ 이상 {frac(Em,T1m)*100:.1f} %',19,'start',fill=MINUS,halo=True),'mb'))
    return svg((w,340),w,'반응 온도에 따른 분자 운동 에너지 분포(계산 모형: Ea 10 kJ/mol, 300 K와 600 K), Ea 이상 부분 음영',s)
FIG['MBE']=mbe()
FIG['MBE_S']=mbe(480,True)

def factors():
    w=520; s=[]; vals=[('$Z$',sqrt(308/298),INK),('$f$',exp(50e3/Rg*(1/298-1/308)),EQUI),('$p$',1.0,MUTED),('$k$',sqrt(308/298)*exp(50e3/Rg*(1/298-1/308)),PLUS)]
    ax=Ax(70,270,420,230,4,2.4)
    s.append(L(70,270,500,270,MUTED,2)+L(70,270,70,30,MUTED,2))
    for v in (1,2): s.append(L(64,ax.Y(v),70,ax.Y(v),MUTED,1.5)+lt(58,ax.Y(v)+6,f'{v}',18,'end',fill=MUTED)+L(70,ax.Y(v),500,ax.Y(v),'#E2E7EC',1))
    s.append(L(70,ax.Y(1),500,ax.Y(1),MUTED,1.5,'6 5'))
    for i,(lab,v,col) in enumerate(vals):
        x=ax.X(i+0.5)
        s.append(an('scale',R(x-34,ax.Y(v),68,ax.Y(0)-ax.Y(v),col,2,'#FFFFFF' if col==MUTED else col,3,extra='fill-opacity=".3"' if col!=MUTED else ''),**{'from':'1,0','o':f'{f(x)},270','delay':f'{i*.2:.1f}','dur':'.7'}))
        s.append(lt(x,296,lab,20)+lt(x,ax.Y(v)-10,f'×{v:.2f}',19,fill=col if col!=MUTED else INK,weight=700))
    s.append(lt(76,22,'25 °C → 35 °C에서 몇 배?',18,'start'))
    return svg((w,310),w,'25 °C에서 35 °C로 올릴 때 Z, f, p, k가 커지는 배수(계산, Ea 50 kJ/mol)',s)
FIG['FACTORS']=factors()

def mini(x0,y0,nodes,Elo,Ehi,labs,w=300,h=200,title=''):
    e=ED(x0,y0,w,h,Elo,Ehi); s=[e.axes(size=17) if False else A(x0,y0,x0,y0-h-14,'muted',2)+A(x0,y0,x0+w+12,y0,'muted',2)]
    s.append(an('draw',e.curve(nodes,INK,3),dur='1.3'))
    s.append(lt(x0+w/2,y0+34,title,19,weight=700))
    for t,E,lab,anc,dy in labs: s.append(lt(e.X(t),e.Y(E)+dy,lab,18,anc,halo=True))
    return ''.join(s),e
def exr():
    w=1080; s=[]
    a,e=mini(40,250,one(0,132,-226),-290,170,[(.02,0,'$\\ce{NO2 + CO}$','start',24),(.98,-226,'$\\ce{NO + CO2}$','end',24)],title='(가) 한 단계 · 발열')
    s.append(a+e.up(.3,0,132)+lt(e.X(.3)-6,e.Y(60),'132',18,'end',fill=EQUI,halo=True)+A(e.X(.95),e.Y(0),e.X(.95),e.Y(-226),'ink',2)+lt(e.X(.95)-6,e.Y(-120),'−226',18,'end',halo=True)+e.guide(.47,.97,0))
    b,e=mini(400,250,one(0,19,-392),-470,60,[(.02,0,'$\\ce{O3 + O}$','start',24),(.98,-392,'$\\ce{2O2}$','end',24)],title='(나) 활성화 에너지 작음 · 발열')
    s.append(b+e.up(.3,0,19)+lt(e.X(.3)+6,e.Y(10)-14,'19',18,'start',fill=EQUI,halo=True)+A(e.X(.95),e.Y(0),e.X(.95),e.Y(-392),'ink',2)+lt(e.X(.95)-6,e.Y(-200),'−392',18,'end',halo=True)+e.guide(.47,.97,0))
    N4=[(0,0),(.08,0),(.28,90),(.5,30),(.7,60),(.9,-50),(1,-50)]
    c,e=mini(760,250,N4,-80,130,[(.02,0,'반응물','start',-12),(.5,30,'중간체','middle',30),(.98,-50,'생성물','end',-12)],title='(다) 두 단계 · 중간체 · 발열')
    s.append(c+e.up(.2,0,90)+lt(e.X(.2)-6,e.Y(45),'90',18,'end',fill=EQUI,halo=True)+e.guide(.08,.3,0)+e.up(.62,30,60)+lt(e.X(.62)+6,e.Y(45)+6,'30',18,'start',fill=EQUI,halo=True)+e.guide(.5,.66,30))
    s.append(lt(60,24,'에너지 [kJ/mol]',17+1,'start',fill=MUTED)+lt(420,24,'에너지 [kJ/mol]',18,'start',fill=MUTED)+lt(780,24,'에너지 [kJ/mol]',18,'start',fill=MUTED))
    return svg((w,300),w,'모둠 결과 예시: 세 반응의 반응 에너지 도표 (가) NO2+CO, (나) O3+O, (다) 중간체가 있는 두 단계 반응(가상)',s)
FIG['EXR']=exr()

def pr2():
    w=600; e=ED(70,320,460,260,-500,70); s=[]; N=one(0,19,-392)
    s.append(e.axes())
    s.append(an('draw',e.curve(N),dur='1.4'))
    s.append(lt(e.X(.14),e.Y(0)+28,'$\\ce{O3(g) + O(g)}$',19)+lt(e.X(.84),e.Y(-392)+28,'$\\ce{2O2(g)}$',19))
    s.append(lt(e.X(.47)+10,e.Y(19)-16,'$[\\ce{O=O}\\cdots\\ce{O}\\cdots\\ce{O}]^\\ddagger$',19,'start'))
    s.append(e.guide(.16,.47,0)+e.up(.3,0,19)+lt(e.X(.3)-8,e.Y(10)-14,'$E_{\\mathrm{a},f}=19$',18,'end',fill=EQUI,halo=True))
    s.append(e.guide(.47,.75,19)+e.up(.72,-392,19)+lt(e.X(.72)+8,e.Y(-80),'$E_{\\mathrm{a},r}$||$=411$',19,'start',fill=EQUI,halo=True))
    s.append(e.guide(.47,1,0)+A(e.X(.97),e.Y(0),e.X(.97),e.Y(-392),'ink',2.5)+lt(e.X(.97)-8,e.Y(-290),'$\\Delta H$||$=-392$',19,'end',halo=True))
    s.append(lt(e.X(1)+12,e.Y(-500)+56,'(단위: kJ/mol)',18,'end',fill=MUTED))
    return svg((w,384),w,'오존 분해 반응 O3 + O → 2O2의 반응 에너지 도표: Ea,f 19, ΔH −392, Ea,r 411 kJ/mol',s)
FIG['PR2']=pr2()

# ═════ 조립 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
keys=re.findall(r'\{\{(\w+)\}\}',tpl)
for k in keys:
    if k not in FIG: sys.exit('no fig '+k)
html=re.sub(r'\{\{(\w+)\}\}',lambda m:FIG[m.group(1)],tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(html)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
shutil.copy(os.path.join(HERE,'labs_src.js'),OUT+'labs.js')
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "충돌 모형과 활성화 에너지", "file": "4-4-1_충돌_모형과_활성화_에너지", "header": "Ⅳ-4-1 충돌 모형과 활성화 에너지 (고등 고급 화학 242–248쪽)"}\n')
print('ok',len(html),'sections',html.count('<section'),'anim',html.count('data-anim'))
if set(FIG)-set(keys): print('unused figs',set(FIG)-set(keys))
