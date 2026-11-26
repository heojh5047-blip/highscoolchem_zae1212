# -*- coding: utf-8 -*-
"""고급화학 4-M 대단원 Ⅳ 마무리 — 그림 생성. h.py·cellh.py(3-M 사본) + 3-M gen 꼴.
   tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html, extra_src.css → extra.css.  python3 -I gen.py
   ★ 출력 OUT은 이 덱(4-M) 폴더만 — assert로 막음"""
import math, re, sys, os, random, shutil
from math import sqrt, exp, pi, erfc, log, log10
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cellh import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FD='4-M_대단원_Ⅳ_마무리'; OUT=BASE+FD+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-M_대단원_Ⅳ_마무리/', OUT
assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FD) and '/4-M_' in OUT, OUT
FIG={}
HL='#FFE45C'; Rg=8.314
IOD='#9A5B1E'; STARCH='#24306B'; PHE='#E04F8A'; MA='#3D6FE0'; MB='#F2A65A'; MBS='#B4561C'
def G(body,attrs=''): return f'<g {attrs}>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def pop(body,x,y,d=0,dur='.6'): return an('pop',body,o=f'{f(x)},{f(y)}',dur=dur,delay=f'{d:.1f}')
def mvalt(body,dx,dy,dur='1.4',delay='0'): return an('move',body,**{'from':f'{f(dx)},{f(dy)}','rep':'alt','dur':dur,'delay':delay,'ease':'io'})
def draw(body,dur='1',delay='0'): return an('draw',body,dur=dur,delay=delay)
def stp(g,body): return step(g,''.join(body) if isinstance(body,list) else body)
def lt(x,y,s,size=18,anchor='middle',fill=None,weight=None,halo=False): return T(x,y,mix=s,size=size,anchor=anchor,fill=fill,weight=weight,halo=halo)
def dot(x,y,col,r=6,fill=None): return C(x,y,r,col,2,fill or col)
def xlab(ax,s,size=19,dy=50): return lt(ax.x0+ax.w,ax.y0+dy,s,size,'end',fill=MUTED)
def ylab(ax,s,size=19): return lt(ax.x0+8,ax.y0-ax.h-14,s,size,'start',fill=MUTED)
random.seed(49)

# ═══ 검산 (plan.md 2절)
x1=-92220/8.3145*(1/298-1/400); K400=6.8e5*exp(x1)
assert abs(x1+9.49)<0.01 and abs(K400-51.4)<0.1
s2=(1.4e-7/4)**(1/3); assert abs(s2-3.27e-3)<1e-5
Ka5=1.3e-5
assert round(-log10(sqrt(Ka5*0.1)),2)==2.94 and round(-log10(Ka5*4),2)==4.28 and round(-log10(Ka5*1.5),2)==4.71
k6=log(2)/1200; assert abs(log(8)/k6-3600)<1e-6
assert abs(1/(100*0.01)-1.0)<1e-12
assert abs(0.00500*0.01250*176.12*1000-11.0)<0.02 and abs(0.100*7.10e-3*176.12*4*1000-500)<0.5
d_=0.36e-9; sig=pi*d_**2; mu=30*48/78/1000; ubar=sqrt(8*8.314*300/(pi*mu)); NA=6.022e23
Ath=sig*ubar*NA*1000; Aex=3.0e-12*NA/1000; Ea_no=1500*8.314
assert abs(ubar-587)<1 and abs(Ath-1.44e11)<1e9 and abs(Aex/Ath-0.0126)<3e-4 and abs(exp(-Ea_no/(8.314*300))-6.74e-3)<5e-5
assert abs(1.8e9*exp(-12470/(8.314*298))-1.18e7)<1e5 and abs(exp(65600/8.314*(1/300-1/310))-2.34)<0.01

# 적정 곡선 — 전하 수지(정확한 풀이)
def ph_titr(Vb,Va,Ca,Cb,Ka1,Ka2=0.0,Kw=1e-14):
    V=(Va+Vb); C=Ca*Va/V; Na=Cb*Vb/V
    def g(h):
        D=h*h+Ka1*h+Ka1*Ka2; a1=C*Ka1*h/D; a2=C*Ka1*Ka2/D
        return h+Na-Kw/h-a1-2*a2
    lo,hi=-14.5,0.5
    for _ in range(80):
        m=(lo+hi)/2
        if g(10**m)>0: hi=m
        else: lo=m
    return -(lo+hi)/2
assert abs(ph_titr(25,50,0.1,0.1,Ka5)-4.886)<0.01 and abs(ph_titr(50,50,0.1,0.1,Ka5)-8.79)<0.01
Cvc=7.10e-4/0.025
assert abs(ph_titr(7.10,25,Cvc,0.1,10**-4.10,10**-11.6)-7.81)<0.03 and abs((4.10+11.6)/2-7.85)<1e-9
print('K400',round(K400,1),'s',s2,'ubar',round(ubar),'Ath',f'{Ath:.3g}','p',round(Aex/Ath,4))

# ═══ 반응 에너지 도표 도우미 (4-4-1 ED 꼴)
class ED:
    def __init__(s,x0,y0,w,h,Elo,Ehi): s.x0,s.y0,s.w,s.h,s.Elo,s.Ehi=x0,y0,w,h,Elo,Ehi
    def X(s,t): return s.x0+t*s.w
    def Y(s,E): return s.y0-(E-s.Elo)/(s.Ehi-s.Elo)*s.h
    def axes(s,yl='에너지',xl='반응 진행 경로',size=18):
        return A(s.x0,s.y0,s.x0,s.y0-s.h-20,'muted',2)+A(s.x0,s.y0,s.x0+s.w+16,s.y0,'muted',2)+lt(s.x0+10,s.y0-s.h-8,yl,size,'start',fill=MUTED)+lt(s.x0+s.w+14,s.y0+28,xl,size,'end',fill=MUTED)
    def path(s,nodes,n=40):
        P_=[]
        for (t1,e1),(t2,e2) in zip(nodes,nodes[1:]):
            for i in range(n+1 if (t2,e2)==nodes[-1] else n):
                u=i/n; P_.append((s.X(t1+(t2-t1)*u),s.Y(e1+(e2-e1)*(1-math.cos(pi*u))/2)))
        return P_
    def curve(s,nodes,col=INK,w=3.5,dash=None): return P(s.path(nodes),col,w,dash=dash)
    def guide(s,t1,t2,E): return L(s.X(t1),s.Y(E),s.X(t2),s.Y(E),MUTED,1.6,'6 5')
    def up(s,t,E1,E2,col='equi',w=2.5): return A(s.X(t),s.Y(E1),s.X(t),s.Y(E2),col,w)
def fE(E,T_): RT=Rg*T_/1000; return 2/sqrt(pi)*RT**-1.5*sqrt(max(E,0))*exp(-E/RT)

# ═══ 중단원 띠
UN=['1. 화학 평형','2. 산과 염기의 평형','3. 반응 속도식','4. 충돌 모형','5. 메커니즘과 촉매']
for i in range(5):
    o=[]
    for j,u in enumerate(UN):
        if j: o.append('<span class="ac49-ar">→</span>')
        o.append(f'<span class="ac49-u{" ac49-now" if i==j else ""}">{u}</span>')
    FIG[f'TOP{i+1}']='<div class="ac49-top">'+''.join(o)+'</div>'

# ═══ S1 표지
def cover():
    s=[]
    # 평형
    s.append(R(20,60,170,200,MUTED,1.5,'#FFFFFF',12,dash='5 4'))
    s.append(mvalt(A(50,138,160,138,'field',4),10,0,dur='1.2'))
    s.append(mvalt(A(160,172,50,172,'bfield',4),-10,0,dur='1.2',delay='.6'))
    s.append(lt(105,118,'정반응',23,fill=FIELD)+lt(105,212,'역반응',23,fill=BF))
    s.append(T(105,246,tex='K',size=30))
    s.append(lt(105,300,'평형: 어디까지',23,weight=700))
    # 적정 곡선
    ax=Ax(225,240,150,170,60,14)
    s.append(R(210,60,170,200,MUTED,1.5,'#FFFFFF',12,dash='5 4'))
    s.append(L(225,240,380,240,MUTED,2)+L(225,240,225,70,MUTED,2))
    s.append(draw(ax.curve(lambda v:ph_titr(max(v,0.01),50,0.1,0.1,Ka5),0,60,col=INK,w=3),dur='1.4'))
    s.append(dot(ax.X(25),ax.Y(4.886),EQUI,5)+dot(ax.X(50),ax.Y(8.79),PLUS,5))
    s.append(lt(295,300,'산 염기 평형',23,weight=700))
    # 반응 에너지
    s.append(R(400,60,170,200,MUTED,1.5,'#FFFFFF',12,dash='5 4'))
    e=ED(415,240,145,165,-40,110)
    s.append(L(415,240,415,72,MUTED,2)+L(415,240,565,240,MUTED,2))
    s.append(draw(e.curve([(0,20),(.15,20),(.5,100),(.85,-20),(1,-20)],INK,3),dur='1.2'))
    s.append(draw(e.curve([(0,20),(.15,20),(.5,55),(.85,-20),(1,-20)],FIELD,3,dash='7 5'),dur='1.2',delay='.6'))
    s.append(lt(485,300,'반응 속도: 빠르기',23,weight=700))
    return svg((580,330),470,'정반응과 역반응이 맞서는 평형, 약산 적정 곡선, 촉매가 있을 때와 없을 때의 반응 에너지 도표',s)
FIG['COVER']=cover()

# ═══ S6 에너지 분포(작게)
def dist():
    s=[]; ax=Ax(40,180,300,150,30,0.30); Em=10; T1,T2=300,600
    for TT,col,op in ((T2,HL,'.55'),(T1,MINUS,'.22')):
        tail=[(ax.X(Em),ax.Y(0))]+[(ax.X(E),ax.Y(fE(E,TT))) for E in [Em+i*0.25 for i in range(81)]]+[(ax.X(30),ax.Y(0))]
        s.append(P(tail,'none',0,col,extra=f'fill-opacity="{op}"',close=True))
    s.append(L(40,180,350,180,MUTED,2)+L(40,180,40,24,MUTED,2))
    s.append(draw(ax.curve(lambda E:fE(E,T1),0,30,col=MINUS,w=3,n=200),dur='1.2'))
    s.append(draw(ax.curve(lambda E:fE(E,T2),0,30,col=PLUS,w=3,n=200),dur='1.2',delay='.3'))
    s.append(L(ax.X(Em),180,ax.X(Em),30,EQUI,2.5)+lt(ax.X(Em)+6,26,'$E_\\mathrm{a}$',19,'start',fill=EQUI))
    s.append(T(ax.X(1.8),ax.Y(fE(1.3,T1))-6,tex='T_1',size=19,fill=MINUS,anchor='start'))
    s.append(T(ax.X(6.5),ax.Y(fE(6,T2))-10,tex='T_2',size=19,fill=PLUS,anchor='start'))
    s.append(lt(350,204,'분자 운동 에너지',18,'end',fill=MUTED))
    return svg((360,228),340,'온도가 높은 T2에서 활성화 에너지 이상인 분자의 분율(음영)이 더 크다',s)
FIG['DIST']=dist()

# ═══ S7 두 단계 반응 에너지 도표(작게)
def cyc5():
    s=[]; e=ED(60,170,540,140,-40,100)
    s.append(e.axes(size=18))
    N=[(0,0),(.08,0),(.28,85),(.45,30),(.62,55),(.85,-30),(1,-30)]
    s.append(draw(e.curve(N),dur='1.4'))
    s.append(lt(e.X(.28),e.Y(85)-10,'느린 단계 (속도 결정)',18,fill=PLUS,weight=700))
    s.append(lt(e.X(.45),e.Y(30)+28,'반응 중간체',18,fill=EQUI,weight=700))
    s.append(lt(e.X(.62)+10,e.Y(55)-10,'빠른 단계',18,'start',fill=MUTED))
    s.append(dot(e.X(.45),e.Y(30),EQUI,5))
    return svg((700,218),640,'두 단계 반응의 에너지 도표: 첫 단계 꼭대기가 높아 속도 결정 단계이고, 골짜기에 반응 중간체가 있다',s)
FIG['CYCLE5']='<div class="ac49-fig5">'+cyc5()+'</div>'

# ═══ S8 연결 흐름
def flow():
    s=[]; W_,H_=330,74
    def box(x,y,tx,lab,d,dash=None,bg='#FFFFFF',col=INK):
        g=[R(x-W_/2,y-H_/2,W_,H_,col,2,bg,12,dash=dash),T(x,y+2,mix=tx,size=21),T(x,y+28,mix=lab,size=18,fill=MUTED)]
        return pop(''.join(g),x,y,d)
    s.append(box(175,55,'$\\Delta G^\\circ$, $\\Delta G=0$ 평형','Ⅲ-2 자발성',0,dash='6 5',bg='#F7F8FA',col=MUTED))
    s.append(box(555,55,'$K$, $Q$, $\\Delta G^\\circ=-RT\\ln K$','Ⅳ-1 화학 평형',.3))
    s.append(box(935,55,'$K_\\mathrm{a}$, $K_\\mathrm{b}$, pH, 완충','Ⅳ-2 산과 염기의 평형',.6))
    s.append(box(175,255,'반응 속도 $=k[\\ce{A}]^m[\\ce{B}]^n$','Ⅳ-3 반응 속도식',.9))
    s.append(box(555,255,'$k=Ae^{-E_\\mathrm{a}/RT}$','Ⅳ-4 충돌 모형',1.2))
    s.append(box(935,255,'속도 결정 단계, 촉매','Ⅳ-5 메커니즘과 촉매',1.5))
    for i,(a,b,c,d) in enumerate([(340,55,390,55),(720,55,770,55),(340,255,390,255),(720,255,770,255)]):
        s.append(draw(A(a,b,c,d,'ink',3),dur='.4',delay=f'{0.3*i+0.3:.1f}'))
    # 다리
    s.append(pop(R(405,134,300,44,FIELD,2,'#EAF6EF',10)+T(555,163,mix='동적 평형: $v_\\text{정}=v_\\text{역}$',size=20,weight=700),555,156,1.8))
    s.append(draw(A(555,94,555,130,'field',3)+A(555,182,555,216,'field',3),dur='.4',delay='1.9'))
    s.append(pop(R(775,134,320,44,EQUI,2,'#FDF3E6',10)+T(935,163,mix='촉매: $k_\\text{정}$·$k_\\text{역}$ 함께↑ → $K$ 그대로',size=19),935,156,2.1))
    s.append(draw(A(935,216,935,182,'equi',3)+A(935,130,935,94,'equi',3,d=True),dur='.4',delay='2.2'))
    return svg((1110,300),1080,'위 줄은 평형(자발성, 화학 평형, 산 염기 평형), 아래 줄은 속도(반응 속도식, 충돌 모형, 메커니즘과 촉매)이고, 동적 평형과 촉매가 두 줄을 잇는다',s)
FIG['FLOW']=flow()

# ═══ S12 ln K–1/T
def z1():
    s=[]; ax=Ax(70,300,370,250,3.5,16,xmin=2.4,ymin=0)
    s.append(ax.frame([2.4,2.7,3.0,3.3],[0,4,8,12,16],xlab(ax,'$1/T$ [$10^{-3}$ K$^{-1}$]',dy=52),ylab(ax,'$\\ln K$'),xfmt=lambda v:f'{v:.1f}',size=18))
    x298,y298=1/298*1e3,log(6.8e5); x400,y400=1/400*1e3,log(K400); slope=(y298-y400)/(x298-x400)
    s.append(draw(ax.curve(lambda x:y400+slope*(x-x400),2.4,3.45,col=INK,w=3),dur='1.2'))
    s.append(pop(dot(ax.X(x298),ax.Y(y298),INK,7),ax.X(x298),ax.Y(y298),.9))
    s.append(lt(ax.X(x298)-12,ax.Y(y298)+30,'298 K: $6.8\\times10^{5}$',19,'end',halo=True))
    s.append(stp('z1',[dot(ax.X(x400),ax.Y(y400),PLUS,7),lt(ax.X(x400)+12,ax.Y(y400)+28,'400 K: $K\\approx51$',19,'start',fill=PLUS,weight=700,halo=True)]))
    s.append(lt(ax.X(2.45),ax.Y(14.8),'기울기 $=-\\dfrac{\\Delta H^\\circ}{R}&gt;0$',19,'start',halo=True))
    s.append(lt(ax.X(3.45),ax.Y(1.6),'온도↑ → $K$↓ (발열)',19,'end',fill=MUTED))
    return svg((470,370),470,'ln K와 1/T의 직선: 298 K에서 ln K 13.4, 400 K에서 3.9로, 온도가 높아지면 평형 상수가 작아진다',s)
FIG['Z1']=z1()

# ═══ S13 Cu(IO3)2 용해
def z2():
    s=[beaker(60,380,top=40,bot=320),R(62,80,316,238,col='none',sw=0,fill=WATER)]
    for i in range(7): s.append(R(90+38*i,288,32,26,'#4E8A9A',1.5,'#9CCAD6',3))
    s.append(lt(220,346,'$\\ce{Cu(IO3)2(s)}$ — 녹다 남은 고체',19))
    rnd=random.Random(5)
    cu=[(130,140),(285,200)]; io=[(95,215),(200,120),(250,250),(340,130)]
    for (x,y) in cu: s.append(mvalt(C(x,y,15,'#1F5FA8',2,'#7FB2E5'),rnd.choice([-1,1])*7,rnd.choice([-1,1])*5,dur=f'{rnd.uniform(1,1.5):.1f}'))
    for (x,y) in io: s.append(mvalt(C(x,y,11,MBS,2,'#F7D2AE'),rnd.choice([-1,1])*7,rnd.choice([-1,1])*5,dur=f'{rnd.uniform(1,1.5):.1f}'))
    s.append(C(80,372,13,'#1F5FA8',2,'#7FB2E5')+lt(100,379,'$\\ce{Cu^2+}$: $s$',19,'start'))
    s.append(C(250,372,10,MBS,2,'#F7D2AE')+lt(268,379,'$\\ce{IO3-}$: $2s$',19,'start'))
    s.append(lt(220,66,'이온 수 1 : 2',19,fill=MUTED))
    return svg((440,395),420,'아이오딘산 구리(Ⅱ) 고체가 녹아 구리 이온 하나마다 아이오딘산 이온이 둘 생긴다',s)
FIG['Z2']=z2()

# ═══ S14 양성자 이동
def z3():
    s=[]
    s.append(lt(100,70,'$\\ce{H3PO4}$',24)+lt(100,100,'산',19,fill=FIELD,weight=700))
    s.append(lt(320,70,'$\\ce{NH3}$',24)+lt(320,100,'염기',19,fill=BF,weight=700))
    s.append(lt(100,290,'$\\ce{H2PO4-}$',24)+lt(100,320,'짝염기',19,fill=FIELD,weight=700))
    s.append(lt(320,290,'$\\ce{NH4+}$',24)+lt(320,320,'짝산',19,fill=BF,weight=700))
    s.append(L(100,112,100,258,FIELD,2.5,dash='6 5')+L(320,112,320,258,BF,2.5,dash='6 5'))
    s.append(lt(92,190,'짝',19,'end',fill=FIELD)+lt(328,190,'짝',19,'start',fill=BF))
    s.append(A(150,160,270,160,'plus',3))
    hp=C(270,190,15,PLUS,2,'#FBD3D8')+T(270,196,tex='\\ce{H+}',size=18,fill=PLUS)
    s.append(an('move',hp,**{'from':'-120,0','dur':'1.6','rep':'loop','ease':'io'}))
    s.append(lt(210,145,'양성자 이동',18,fill=PLUS))
    s.append(lt(210,30,'1) $\\ce{NH3 + H3PO4 <=> NH4+ + H2PO4-}$',19,fill=MUTED))
    return svg((420,340),400,'인산이 암모니아에 양성자를 주어 인산 이수소 이온과 암모늄 이온이 되고, 각각 짝을 이룬다',s)
FIG['Z3']=z3()

# ═══ S15 완충 막대
def z4():
    s=[]; base=300; k=150
    s.append(L(30,base,500,base,MUTED,2))
    groups=[('처음',1.0,1.0),('$\\ce{H3O+}$ 조금',1.1,0.9),('$\\ce{OH-}$ 조금',0.9,1.1)]
    for i,(lab,a,b) in enumerate(groups):
        x=95+160*i
        for j,(v,col,st) in enumerate(((a,'#C9D3DD','#5B6B7F'),(b,'#BFE3CF',FIELD))):
            bx=x-48+52*j; bar=R(bx,base-v*k,44,v*k,st,2,col,3)
            s.append(an('scale',bar,**{'from':'1,0.2','o':f'{bx+22},{base}','dur':'.8','delay':f'{0.3*i:.1f}'}) if i else bar)
        s.append(lt(x,base+28,lab,19))
    s.append(R(40,24,18,18,'#5B6B7F',2,'#C9D3DD',3)+lt(66,40,'$\\ce{CH3COOH}$',19,'start')+R(250,24,18,18,FIELD,2,'#BFE3CF',3)+lt(276,40,'$\\ce{CH3COO-}$',19,'start'))
    s.append(lt(265,376,'두 성분의 비가 조금만 변한다 → pH 거의 그대로',19,fill=MUTED))
    return svg((520,390),500,'완충 용액에 산을 넣으면 아세트산 이온이 조금 줄고 아세트산이 조금 늘며, 염기를 넣으면 그 반대이다',s)
FIG['Z4']=z4()

# ═══ S16 적정 곡선
def z5():
    s=[]; ax=Ax(70,330,390,280,60,14)
    s.append(f'<rect x="{f(ax.X(5))}" y="{f(ax.Y(14))}" width="{f(ax.X(45)-ax.X(5))}" height="{f(ax.h)}" fill="{FIELD}" fill-opacity=".15"/>')
    s.append(ax.frame([0,10,20,30,40,50,60],[0,2,4,6,8,10,12,14],xlab(ax,'$\\ce{NaOH}$ 부피 [mL]',dy=52),ylab(ax,'pH'),size=18))
    s.append(draw(ax.curve(lambda v:ph_titr(max(v,1e-3),50,0.1,0.1,Ka5),0,60,n=240,col=INK,w=3),dur='1.6'))
    for i,(v,ph,lab) in enumerate([(0,2.94,'2.94'),(10,4.28,'4.28'),(20,4.71,'4.71')]):
        s.append(pop(dot(ax.X(v),ax.Y(ph),INK,6),ax.X(v),ax.Y(ph),1.2+0.2*i))
        s.append(lt(ax.X(v)+(10 if i==0 else 0),ax.Y(ph)-14 if i else ax.Y(ph)+28,lab,19,'start' if i==0 else 'middle',weight=700,halo=True))
    s.append(stp('z5',[dot(ax.X(25),ax.Y(4.886),EQUI,7),lt(ax.X(25)+10,ax.Y(4.886)+28,'pH $=\\mathrm{p}K_\\mathrm{a}=4.89$',18,'start',fill=EQUI,halo=True),
                       dot(ax.X(50),ax.Y(8.79),PLUS,7),lt(ax.X(50)-10,ax.Y(8.79)+6,'당량점 8.79',18,'end',fill=PLUS,halo=True)]))
    s.append(lt(ax.X(25),ax.Y(12.6),'완충 구간',19,fill=FIELD,weight=700))
    return svg((500,400),500,'0.1 M 프로피온산 50 mL를 0.1 M 수산화 나트륨으로 적정한 곡선: 0, 10, 20 mL에서 pH 2.94, 4.28, 4.71, 반당량점 4.89, 당량점 8.79',s)
FIG['Z5']=z5()

# ═══ S17 1차 반감기
def z6():
    s=[]; ax=Ax(80,320,390,260,80,100)
    s.append(ax.frame([0,20,40,60,80],[0,25,50,75,100],xlab(ax,'시간 [min]',dy=50),ylab(ax,'남은 $\\ce{N2O5}$ [%]'),size=18))
    s.append(draw(ax.curve(lambda t:100*0.5**(t/20),0,80,col=INK,w=3.2),dur='1.4'))
    for i,(t,v) in enumerate([(20,50),(40,25),(60,12.5)]):
        g=[L(ax.X(t),ax.Y(0),ax.X(t),ax.Y(v),MUTED,1.6,'6 5'),L(ax.X(0),ax.Y(v),ax.X(t),ax.Y(v),MUTED,1.6,'6 5'),dot(ax.X(t),ax.Y(v),INK,6),
           lt(ax.X(t)+10,ax.Y(v)-12,f'{v:g} %',19,'start',weight=700,halo=True)]
        s.append(pop(''.join(g),ax.X(t),ax.Y(v),1.0+0.4*i))
    s.append(stp('z6',[lt(ax.X(60)-8,ax.Y(4),'60 min',19,'end',fill=PLUS,weight=700,halo=True)]))
    s.append(lt(ax.X(40),ax.Y(88),'반감기 20 min마다 반으로',19,'start',fill=MUTED))
    return svg((500,380),500,'1차 반응: 20분마다 반으로 줄어 20, 40, 60분에 50, 25, 12.5 %가 남는다',s)
FIG['Z6']=z6()

# ═══ S18 2차 반감기
def z7():
    s=[]; ax=Ax(80,320,390,260,400,1.0)
    s.append(ax.frame([0,100,200,300,400],[0,0.25,0.5,0.75,1.0],xlab(ax,'시간 [s]',dy=50),ylab(ax,'$[\\ce{A}]$ [$10^{-2}$ M]'),yfmt=lambda v:f'{v:g}',size=18))
    s.append(draw(ax.curve(lambda t:1/(1+0.01*t),0,400,col=INK,w=3.2),dur='1.4'))
    for i,(t,v) in enumerate([(100,.5),(300,.25)]):
        s.append(pop(L(ax.X(t),ax.Y(0),ax.X(t),ax.Y(v),MUTED,1.6,'6 5')+L(ax.X(0),ax.Y(v),ax.X(t),ax.Y(v),MUTED,1.6,'6 5')+dot(ax.X(t),ax.Y(v),INK,6),ax.X(t),ax.Y(v),1.0+0.4*i))
    s.append(lt(ax.X(100)+8,ax.Y(.5)-14,'100 s: 반',19,'start',weight=700,halo=True))
    s.append(stp('z7',[L(ax.X(100),ax.Y(.1),ax.X(300),ax.Y(.1),PLUS,2)+L(ax.X(100),ax.Y(.1)-8,ax.X(100),ax.Y(.1)+8,PLUS,2)+L(ax.X(300),ax.Y(.1)-8,ax.X(300),ax.Y(.1)+8,PLUS,2),
                       lt(ax.X(200),ax.Y(.1)-10,'다음 반감기 200 s',19,fill=PLUS,weight=700,halo=True)]))
    return svg((500,380),500,'2차 반응: 100초에 반이 되고, 다시 반이 되는 데는 200초가 걸린다',s)
FIG['Z7']=z7()

# ═══ S20 촉매 순환
def arcarrow(cx,cy,r,a0,a1,col,w=3.5):
    n=40; pts=[(cx+r*math.cos(math.radians(a0+(a1-a0)*i/n)),cy+r*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
    (x1,y1),(x2,y2)=pts[-2],pts[-1]; ux,uy=(x2-x1),(y2-y1); Ln=math.hypot(ux,uy); ux,uy=ux/Ln,uy/Ln; px,py=-uy,ux
    head=[(x2+ux*6,y2+uy*6),(x2-ux*12+px*8,y2-uy*12+py*8),(x2-ux*12-px*8,y2-uy*12-py*8)]
    return P(pts[:-1],col,w)+P(head,col,1,fill=col,close=True)
def z9():
    s=[]; cx,cy,r=220,200,105
    s.append(arcarrow(cx,cy,r,200,340,INK)+arcarrow(cx,cy,r,20,160,INK))
    s.append(C(cx-r,cy,34,FIELD,2.5,'#EAF6EF')+T(cx-r,cy+7,tex='\\ce{Br-}',size=21))
    s.append(C(cx+r,cy,34,EQUI,2.5,'#FDF3E6')+T(cx+r,cy+7,tex='\\ce{BrO-}',size=20))
    s.append(lt(cx-r,cy+60,'촉매',19,fill=FIELD,weight=700)+lt(cx+r,cy+60,'중간체',19,fill=EQUI,weight=700))
    s.append(lt(cx,cy-r-34,'1단계 (느림)',19,weight=700))
    s.append(A(cx-40,40,cx-14,cy-r+4,'ink',2.5)+lt(cx-44,34,'$\\ce{H2O2}$',19,'end'))
    s.append(A(cx+14,cy-r+4,cx+40,40,'ink',2.5)+lt(cx+44,34,'$\\ce{H2O}$',19,'start'))
    s.append(lt(cx,cy+r+44,'2단계 (빠름)',19,weight=700))
    s.append(A(cx-40,cy+r+80,cx-14,cy+r-4,'ink',2.5)+lt(cx-44,cy+r+96,'$\\ce{H2O2}$',19,'end'))
    s.append(A(cx+14,cy+r-4,cx+40,cy+r+80,'ink',2.5)+lt(cx+44,cy+r+96,'$\\ce{H2O + O2}$',19,'start'))
    ball=C(cx+r*math.cos(math.radians(90)),cy+r*math.sin(math.radians(90)),8,PLUS,1.5,'#FBD3D8')
    s.append(an('rot',ball,**{'from':'-360','o':f'{cx},{cy}','dur':'4','rep':'loop','ease':'lin'}))
    return svg((440,420),420,'브로민화 이온이 1단계에서 하이포브로민산 이온이 되고 2단계에서 다시 브로민화 이온으로 돌아오는 촉매 순환',s)
FIG['Z9']=z9()

# ═══ S21 촉매 에너지 도표
def z10():
    s=[]; e=ED(70,330,390,270,-80,120)
    s.append(e.axes())
    N=[(0,0),(.12,0),(.45,100),(.82,-60),(1,-60)]
    Nc=[(0,0),(.12,0),(.32,55),(.45,30),(.58,45),(.82,-60),(1,-60)]
    s.append(draw(e.curve(N),dur='1.2'))
    s.append(draw(e.curve(Nc,FIELD,3.2,dash='8 6'),dur='1.2',delay='.6'))
    s.append(e.guide(.12,.5,0)+e.up(.45,0,100)+lt(e.X(.45)+8,e.Y(70),'$E_\\mathrm{a}$',20,'start',fill=EQUI,weight=700,halo=True))
    s.append(e.up(.32,0,55,'field')+lt(e.X(.32)-8,e.Y(28),"$E_\\mathrm{a}'$",20,'end',fill=FIELD,weight=700,halo=True))
    s.append(e.guide(.82,1,0)+A(e.X(.97),e.Y(0),e.X(.97),e.Y(-60),'ink',2.5)+lt(e.X(.95)-8,e.Y(-22),'$\\Delta H$ 같음',19,'end',halo=True))
    s.append(lt(e.X(.62),e.Y(100),'촉매 없음',19,'start')+lt(e.X(.6),e.Y(68),'촉매 있음',19,'start',fill=FIELD,weight=700))
    s.append(lt(e.X(.03),e.Y(0)-12,'반응물',18,'start')+lt(e.X(.99),e.Y(-60)+26,'생성물',18,'end'))
    return svg((500,380),500,'촉매가 있으면 활성화 에너지가 낮은 새 경로로 반응하고, 반응 엔탈피는 같다',s)
FIG['Z10']=z10()

# ═══ S22 식품별 함량 막대
def vc1():
    s=[]; foods=[('빨간 파프리카',128),('키위',93),('브로콜리',89),('딸기',59),('오렌지',53),('토마토',14),('사과',5)]
    X0,k=150,2.75; y0=30
    s.append(L(X0,14,X0,y0+31*len(foods),MUTED,2))
    for i,(nm,v) in enumerate(foods):
        y=y0+31*i; bar=R(X0,y,v*k,24,'#B07A14',1.5,'#F4B63F',3)
        s.append(an('scale',bar,**{'from':'0,1','o':f'{X0},{y}','dur':'.8','delay':f'{0.1*i:.1f}'}))
        s.append(lt(X0-10,y+20,nm,18,'end')+lt(X0+v*k+8,y+20,str(v),18,'start'))
    xw=X0+45*k
    s.append(L(xw,22,xw,y0+31*len(foods)+4,EQUI,2.5,'7 5')+lt(xw+6,18,'WHO 하루 권장량 45 mg',18,'start',fill=EQUI,weight=700))
    s.append(lt(X0+4,y0+31*len(foods)+26,'100 g당 [mg] (어림값)',18,'start',fill=MUTED))
    return svg((560,285),520,'식품 100 g당 바이타민 C 어림값: 빨간 파프리카 128, 키위 93, 브로콜리 89, 딸기 59, 오렌지 53, 토마토 14, 사과 5 mg과 WHO 하루 권장량 45 mg',s)
FIG['VC1']=vc1()

# ═══ S23 아이오딘 적정
def vc2():
    s=[]
    s.append(L(40,20,40,448,INK,4)+L(40,40,128,40,INK,3)+R(20,448,230,10,INK,2,'#C9D2DB'))
    s.append(R(128,24,24,236,GLS,2,'#FFFFFF',4)+R(130,90,20,168,'none',0,IOD,0,extra='fill-opacity=".75"'))
    for i,y in enumerate(range(50,250,30)): s.append(L(128,y,138,y,GLS,1.2))
    s.append(R(124,260,32,10,INK,2,'#C9D2DB',2)+P([(134,270),(146,270),(142,292),(138,292)],GLS,2,'#FFFFFF',close=True))
    drop=C(140,310,5,IOD,1,IOD)
    s.append(an('move',drop,**{'from':'0,-16','dur':'1','rep':'loop','ease':'in'}))
    s.append(lt(162,110,'$\\ce{I2}$ 용액',19,'start')+lt(162,136,'0.00500 M',18,'start',fill=MUTED))
    fl=[(128,330),(128,360),(80,446),(200,446),(152,360),(152,330)]
    s.append(P([(85,432),(195,432),(178,405),(102,405)],'none',0,STARCH,close=True,extra='fill-opacity=".85"'))
    s.append(pop(C(140,418,14,'#3B4A9A',1,'#3B4A9A',extra='fill-opacity=".6"'),140,418,0.6,dur='1'))
    s.append(P(fl,GLS,3))
    s.append(lt(150,482,'주스 + 녹말',18)+lt(150,506,'→ 종말점 청흑색',18,fill=STARCH,weight=700))
    return svg((300,515),270,'뷰렛의 아이오딘 용액을 주스와 녹말이 든 삼각 플라스크에 떨어뜨리면 종말점에서 청흑색이 된다',s)
FIG['VC2']=vc2()

def vc2b():
    s=[]; ax=Ax(46,170,236,140,12,14); Ka1,Ka2=10**-4.10,10**-11.6
    s.append(ax.frame([0,4,8,12],[0,7,14],lt(ax.x0+ax.w,ax.y0+50,'$\\ce{NaOH}$ [mL]',18,'end',fill=MUTED),lt(ax.x0+6,ax.y0-ax.h-12,'pH',18,'start',fill=MUTED),size=18))
    s.append(draw(ax.curve(lambda v:ph_titr(max(v,1e-3),25,Cvc,0.1,Ka1,Ka2),0,12,n=200,col=INK,w=2.8),dur='1.2'))
    s.append(dot(ax.X(3.55),ax.Y(4.10),EQUI,6)+lt(ax.X(3.55)+6,ax.Y(4.10)+24,'4.10',18,'start',fill=EQUI,weight=700))
    s.append(dot(ax.X(7.10),ax.Y(7.81),PLUS,6)+lt(ax.X(7.10)-8,ax.Y(7.81)+4,'7.8',18,'end',fill=PLUS,weight=700))
    return svg((300,232),290,'아스코브산을 수산화 나트륨으로 적정한 곡선: 반당량점 pH 4.10, 당량점 pH 약 7.8',s)
FIG['VC2B']=vc2b()

# ═══ S24 섭취량 쌓은 막대
def vc3():
    s=[]; base=360; k=1.15; xb=150
    s.append(L(70,base,400,base,MUTED,2)+L(70,base,70,40,MUTED,2))
    for v in (100,200): s.append(L(64,base-v*k,400,base-v*k,'#E2E7EC',1)+lt(58,base-v*k+6,str(v),18,'end'))
    s.append(lt(58,base+6,'0',18,'end')+lt(76,30,'섭취량 [mg]',18,'start',fill=MUTED))
    segs=[('주스',88,'#F2A65A'),('브로콜리',45,'#7CC27C'),('파프리카',38,'#E0705E'),('딸기',59,'#F29AB2')]
    y=base; g=[]
    for nm,v,col in segs:
        h=v*k; g.append(R(xb-45,y-h,90,h,INK,1.5,col)); g.append(lt(xb,y-h/2+7,f'{nm} {v}',18)); y-=h
    s.append(an('scale',''.join(g),**{'from':'1,0','o':f'{xb},{base}','dur':'1.2'}))
    s.append(lt(xb,y-12,'230 mg',20,weight=700))
    s.append(R(290,base-45*k,70,45*k,MUTED,1.5,'#C9D3DD')+lt(325,base+26,'WHO 권장량',18)+lt(325,base-45*k-10,'45 mg',19,weight=700))
    s.append(lt(xb,base+26,'나의 하루',18))
    s.append(L(70,base-45*k,400,base-45*k,EQUI,2,'7 5'))
    s.append(A(380,250,380,60,'plus',2.5)+lt(370,90,'상한 2 g은',18,'end',fill=PLUS)+lt(370,114,'이 축의 약 9배 위',18,'end',fill=PLUS))
    return svg((420,400),400,'하루 식단의 바이타민 C 230 mg(주스 88, 브로콜리 45, 파프리카 38, 딸기 59)은 WHO 권장량 45 mg의 약 5배이고 상한 2 g보다 훨씬 적다',s)
FIG['VC3']=vc3()

# ═══ S26 세 충돌
def cl1():
    s=[]
    def Bmol(x,y,react_left=True):
        a=C(x,y,13,MBS,1.8,MB); b=C(x+24,y,13,MBS,1.8,MB)
        hl=C(x if react_left else x+24,y,13,PLUS,2.5,'#F4A3AE')
        return a+b+hl
    caps=[('방향 ○ · 에너지 ○','→ 반응',FIELD),('에너지 부족','→ 튕김',MUTED),('방향 ×','→ 튕김',MUTED)]
    for i,(c1,c2,col) in enumerate(caps):
        x0=170*i; s.append(R(x0+6,6,158,150,MUTED,1.2,'#FFFFFF',10,dash='5 4'))
        bx=x0+96; by=70
        s.append(Bmol(bx,by,react_left=(i!=2)))
        ax_=bx-29 if i!=2 else bx-29
        Aball=C(ax_,by,13,'#1F4FA8',1.8,'#9DB8F0')
        if i==0:
            s.append(an('move',Aball,**{'from':'-40,0','dur':'1.2','rep':'loop','ease':'in'}))
            s.append(A(x0+20,by,x0+44,by,'ink',3)+lt(x0+86,130,'',18))
            s.append(pop(P([(bx-14,by-26),(bx-10,by-14),(bx-2,by-22),(bx-6,by-10)],PLUS,2.5),bx-10,by-18,0.4))
        elif i==1:
            s.append(an('move',Aball,**{'from':'-30,0','dur':'1.2','rep':'alt','ease':'io'}))
            s.append(A(x0+24,by,x0+36,by,'ink',2))
        else:
            s.append(an('move',Aball,**{'from':'-30,0','dur':'1.2','rep':'alt','ease':'io'}))
            s.append(A(x0+20,by,x0+44,by,'ink',3))
        s.append(lt(x0+85,124,c1,18,fill=col if i==0 else INK,weight=700)+lt(x0+85,148,c2,18,fill=col,weight=700))
    s.append(C(20,184,10,'#1F4FA8',1.8,'#9DB8F0')+lt(36,190,'A',18,'start')+C(80,184,10,MBS,1.8,MB)+C(116,184,10,PLUS,2.5,'#F4A3AE')+lt(100,190,'B',18,'start')+lt(134,190,'(빨간 쪽 = 반응하는 자리)',18,'start',fill=MUTED))
    return svg((510,200),500,'세 가지 충돌: 알맞은 방향과 충분한 에너지면 반응하고, 에너지가 부족하거나 방향이 틀리면 튕겨 나간다',s)
FIG['CL1']=cl1()

# ═══ S27 충돌 원기둥
def cl2():
    s=[]; x0,x1,cy,r=80,440,110,52
    s.append(P([(x0,cy-r),(x1,cy-r)],MUTED,1.8,dash='6 5')+P([(x0,cy+r),(x1,cy+r)],MUTED,1.8,dash='6 5'))
    s.append(f'<ellipse cx="{x0}" cy="{cy}" rx="16" ry="{r}" fill="{FIELD}" fill-opacity=".15" stroke="{FIELD}" stroke-width="2"/>')
    s.append(f'<ellipse cx="{x1}" cy="{cy}" rx="16" ry="{r}" fill="none" stroke="{MUTED}" stroke-width="1.8" stroke-dasharray="6 5"/>')
    rnd=random.Random(11)
    for (bx,by) in [(150,90),(230,140),(300,75),(380,128),(200,30),(340,190),(175,196),(410,24)]:
        inside=abs(by-cy)<r-6
        s.append(C(bx,by,11,PLUS if inside else MBS,2.4 if inside else 1.5,MB))
    Ab=C(x1,cy,16,'#1F4FA8',2,'#9DB8F0')
    s.append(an('move',Ab,**{'from':f'{x0-x1},0','dur':'2.4','rep':'loop','ease':'lin'}))
    s.append(A(x1+20,cy,x1+60,cy,'ink',3)+T(x1+44,cy-12,tex='\\bar u',size=20))
    s.append(L(x0,cy,x0,cy-r,INK,2)+T(x0-10,cy-r/2+6,tex='d',size=20,anchor='end'))
    s.append(lt(x0,cy+r+30,'$\\sigma=\\pi d^2$',19,fill=FIELD,weight=700))
    s.append(L(x0,cy+r+50,x1,cy+r+50,MUTED,1.5)+L(x0,cy+r+42,x0,cy+r+58,MUTED,1.5)+L(x1,cy+r+42,x1,cy+r+58,MUTED,1.5))
    s.append(lt((x0+x1)/2,cy+r+76,'1초에 $\\bar u\\times1\\ \\text{s}$ 만큼 — 원기둥 안의 B와 충돌',18))
    return svg((520,250),500,'분자 A가 평균 상대 속력으로 지나가며 쓸고 가는 원기둥(단면적 σ = πd²) 안에 중심이 있는 B 분자와 충돌한다',s)
FIG['CL2']=cl2()

# ═══ S28 ln k–1/T 두 반응
def cl3():
    s=[]; ax=Ax(70,250,330,210,3.6,20,xmin=3.0,ymin=-12)
    s.append(ax.frame([3.0,3.2,3.4,3.6],[-12,-4,4,12,20],xlab(ax,'$1/T$ [$10^{-3}$ K$^{-1}$]',dy=48),ylab(ax,'$\\ln k$'),xfmt=lambda v:f'{v:.1f}',size=18))
    s.append(L(ax.X(3.0),ax.Y(0),ax.X(3.6),ax.Y(0),MUTED,1.2,'4 4'))
    fA=lambda x:log(1.8e9)-1500*x*1e-3; fB=lambda x:log(1.6e8)-65600/8.314*x*1e-3
    s.append(draw(ax.curve(fA,3.0,3.6,col=FIELD,w=3),dur='1'))
    s.append(draw(ax.curve(fB,3.0,3.6,col=PLUS,w=3),dur='1',delay='.4'))
    s.append(lt(ax.X(3.58),ax.Y(fA(3.58))-14,'$\\ce{NO + O3}$ (12.5)',18,'end',fill=FIELD,weight=700,halo=True))
    s.append(lt(ax.X(3.12),ax.Y(fB(3.12))+30,'$\\ce{NH2OH}$ 분해 (65.6)',18,'start',fill=PLUS,weight=700,halo=True))
    s.append(lt(ax.X(3.3),ax.Y(6),'기울기 $-E_\\mathrm{a}/R$',18,halo=True))
    return svg((420,310),420,'두 반응의 ln k와 1/T 직선: 활성화 에너지가 큰 NH2OH 분해는 기울기가 가파르고 k가 훨씬 작다',s)
FIG['CL3']=cl3()

# ═══ 조립
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
assert (OUT+'slides.html').endswith('/4-M_대단원_Ⅳ_마무리/slides.html')
open(OUT+'slides.html','w',encoding='utf-8').write(out)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused)
