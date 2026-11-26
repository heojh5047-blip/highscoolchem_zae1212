# -*- coding: utf-8 -*-
"""고급화학 4-1-1 화학 평형 — 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   labs_src.js·extra_src.css를 labs.js·extra.css로 복사하고 meta.json을 쓴다.
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)
   농도–시간·G 곡선·ln K–1/T·수득률 그래프는 모두 calc.py와 같은 식의 계산값으로 그린다."""
import math, random, re, sys, os, shutil
from math import exp, log, sqrt
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FOLDER='4-1-1_화학_평형'
OUT=BASE+FOLDER+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-1-1_화학_평형/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FOLDER), OUT
FIG={}
HL='#FFE45C'; NO2C='#A4421A'; FESCN='#B3122E'
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def step(g,body): return f'<g class="step" data-g="{g}">{body}</g>'
def atom(x,y,r,el,lab='-'): return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el},{lab}"></g>'
def n2(x,y,rN): d=rN*.62; return atom(x-d,y,rN,'N')+atom(x+d,y,rN,'N')
def h2(x,y,rH): d=rH*.62; return atom(x-d,y,rH,'H')+atom(x+d,y,rH,'H')
def nh3(x,y,rN,rH):
    o=''
    for a in (90,210,330):
        if a!=90: continue
    hs=[(x,y-rN*.95),(x-rN*.85,y+rN*.55),(x+rN*.85,y+rN*.55)]
    o+=atom(*hs[0],rH,'H'); o+=atom(x,y,rN,'N'); o+=atom(*hs[1],rH,'H')+atom(*hs[2],rH,'H')
    return o
def mol(kind,x,y,s=1.0):
    rN,rH=10*s,7*s
    return {'N2':n2,'H2':h2}[kind](x,y,rN if kind=='N2' else rH) if kind!='NH3' else nh3(x,y,rN,rH)
def eqarrow(x,y,w,col1=FIELD,col2=BF,sw=3):
    """⇌ 두 반쪽 화살표 (위: 정반응 →, 아래: 역반응 ←)"""
    h=7
    return (P([(x,y-5),(x+w,y-5),(x+w-14,y-5-h)],col1,sw)+P([(x+w,y+5),(x,y+5),(x+14,y+5+h)],col2,sw))
def eqlabel(x,y,s=20): return T(x,y,tex='\\ce{<=>}',size=s)
def shadeeq(ax,t0,t1,lab='평형',ly=None,size=18):
    o=R(ax.X(t0),ax.Y(ax.ymax),ax.X(t1)-ax.X(t0),ax.Y(ax.ymin)-ax.Y(ax.ymax),'none',0,HL,extra='fill-opacity=".25"')
    o+=L(ax.X(t0),ax.Y(ax.ymin),ax.X(t0),ax.Y(ax.ymax),MUTED,1.5,'5 4')
    if lab: o+=T((ax.X(t0)+ax.X(t1))/2,ly if ly else ax.Y(ax.ymax)+22,mix=lab,size=size,fill=MUTED,weight=700)
    return o
def placed(n,x0,y0,w,h,dmin,seed,avoid=()):
    rnd=random.Random(seed); pts=[]; tries=0
    while len(pts)<n:
        tries+=1; assert tries<200000,'place fail'
        p=(rnd.uniform(x0,x0+w),rnd.uniform(y0,y0+h))
        if all(math.hypot(p[0]-a,p[1]-b)>dmin for a,b in list(pts)+list(avoid)): pts.append(p)
    return pts

# ═════ 계산: 암모니아 합성 농도–시간 (질량 작용 모형) ═════
K500=0.0602
def nh3_run(N0,H0,A0,kf=1.0,tmax=4.0,n=4000):
    kr=kf/K500; x=0.0; out=[(0,N0,H0,A0)]; dt=tmax/n
    for i in range(n):
        def d(x): return kf*(N0-x)*(H0-3*x)**3-kr*(A0+2*x)**2
        k1=d(x); k2=d(x+dt*k1/2); k3=d(x+dt*k2/2); k4=d(x+dt*k3); x+=dt*(k1+2*k2+2*k3+k4)/6
        out.append(((i+1)*dt,N0-x,H0-3*x,A0+2*x))
    return out
RUN1=nh3_run(1.0,1.0,0.0)
def teq(run,tol=0.002):
    last=run[-1]
    for r in run:
        if all(abs(r[j]-last[j])<tol for j in (1,2,3)): return r[0]
def conc_plot(ax,run,tmax,anim=True,w=3.5):
    o=''; cols=((1,INK,None),(2,INK,'10 6'),(3,FIELD,None))
    for i,(j,col,dash) in enumerate(cols):
        pts=[(ax.X(r[0]),ax.Y(r[j])) for r in run if r[0]<=tmax+1e-9][::10]
        p=P(pts,col,w,dash=dash,extra='stroke-linecap="round"')
        o+=an('draw',p,dur='1.4',delay=f(0.2*i)) if anim and not dash else p
    return o

# ═════ 1 표지 ═════
def cover():
    s=[]
    # 반응물 묶음과 생성물 묶음, 가운데 ⇌
    for (x,y) in ((60,70),(118,112)): s.append(mol('N2',x,y,1.3))
    for (x,y) in ((52,138),(110,52),(150,150),(40,96)): pass
    hs=[(150,74),(62,150),(118,30),(28,64),(160,118),(95,160)]
    for i,(x,y) in enumerate(hs): s.append(mol('H2',x,y,1.3))
    s.append(T(96,206,tex='\\ce{N2 + 3H2}',size=22))
    s.append(eqarrow(196,100,70,sw=3.5))
    s.append(an('move',eqarrow(196,100,70,sw=0),**{'from':'0,0'}))
    pr=[(330,70),(392,110),(330,146),(398,40)]
    for (x,y) in pr: s.append(an('move',mol('NH3',x,y,1.3),**{'from':'0,-6','rep':'alt','dur':'1.1','ease':'io'}))
    s.append(T(362,206,tex='\\ce{2NH3}',size=22))
    # 아래 작은 농도–시간
    ax=Ax(60,390,360,140,4,1.0)
    s.append(L(ax.x0,ax.y0,ax.x0+ax.w+8,ax.y0,MUTED,2)+L(ax.x0,ax.y0,ax.x0,ax.y0-ax.h-8,MUTED,2))
    te=teq(RUN1)
    s.append(shadeeq(ax,te,4,lab='평형',ly=ax.Y(0.45)))
    s.append(conc_plot(ax,RUN1,4))
    s.append(T(ax.x0+ax.w+4,ax.y0+26,mix='시간',size=19,anchor='end',fill=MUTED))
    s.append(T(ax.x0-6,ax.y0-ax.h-14,mix='몰농도',size=19,anchor='start',fill=MUTED))
    last=RUN1[-1]
    s.append(T(ax.X(4)-6,ax.Y(last[1])-8,tex='\\ce{N2}',size=19,anchor='end',halo=True))
    s.append(T(ax.X(4)-6,ax.Y(last[2])+24,tex='\\ce{H2}',size=19,anchor='end',halo=True))
    s.append(T(ax.X(4)-6,ax.Y(last[3])-8,tex='\\ce{NH3}',size=19,anchor='end',fill=FIELD,halo=True))
    return svg((460,430),440,'질소와 수소가 암모니아와 동적 평형을 이루고, 농도가 시간이 지나 일정해지는 그래프',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 2 대단원 도입: 열역학과 반응 속도 ═════
def unit():
    s=[]
    s.append(R(170,8,220,52,INK,2.5,'#FFFFFF',12)+T(280,42,mix='화학 반응',size=22,weight=700))
    s.append(A(230,60,130,104,'muted',2.5)+A(330,60,430,104,'muted',2.5))
    s.append(R(10,108,250,108,FIELD,2.5,'#F2FAF5',12))
    s.append(T(135,138,mix='열역학 $\\Delta G^\\circ$',size=20,weight=700))
    s.append(T(135,168,mix='반응의 방향·평형의 위치',size=19))
    s.append(T(135,198,mix='→ 1 화학 평형, 2 산 염기 평형',size=18,fill=MUTED))
    s.append(R(300,108,250,108,BF,2.5,'#F5F1FC',12))
    s.append(T(425,138,mix='반응 속도',size=20,weight=700))
    s.append(T(425,168,mix='실험으로만 결정',size=19))
    s.append(T(425,198,mix='→ 3·4·5 속도식·메커니즘',size=18,fill=MUTED))
    return svg((560,224),520,'화학 반응을 열역학(방향과 평형의 위치)과 반응 속도(실험으로 결정) 두 관점에서 본다',s)
FIG['UNIT']=unit()

# ═════ 3 중단원 도입: 석회암 동굴 ═════
def cave():
    s=[]
    s.append(R(0,0,380,250,'none',0,'#EFE8DD',14))
    s.append(P([(0,0),(380,0),(380,34),(0,34)],'none',0,'#C9B79C',close=True))
    for x,l in ((40,70),(90,110),(150,60),(215,95),(285,120),(340,64)):
        s.append(P([(x-16,34),(x+16,34),(x,34+l)],'#9E8A6C',2,'#D8C9AE',close=True))
    s.append(P([(0,250),(380,250),(380,226),(0,226)],'none',0,'#C9B79C',close=True))
    for x,l in ((90,70),(215,52),(285,40)):
        s.append(P([(x-22,226),(x+22,226),(x,226-l)],'#9E8A6C',2,'#D8C9AE',close=True))
    for x,l,dl in ((90,110,'0'),(215,95,'.6'),(285,120,'1.1')):
        s.append(an('move',C(x,34+l+10,4.5,'#6FA6CF',1.5,WATER),**{'from':'0,-10','rep':'loop','dur':'1.6','delay':dl,'ease':'in'}))
    s.append(T(150,276,mix='종유석(위) · 석순(아래)',size=19,fill=MUTED))
    return svg((380,290),360,'석회암 동굴의 종유석과 석순, 천장에서 떨어지는 물방울',s)
FIG['MID']=cave()

# ═════ 5 생각 열기: NO2 관 ═════
def tubes():
    s=[]
    for i,(bx,bath,lab,fin,word) in enumerate(((20,COLD,'얼음물','#E9C9A8','옅어짐'),(250,HOT if False else '#FDE2E4','뜨거운 물',NO2C,'진해짐'))):
        s.append(R(bx,110,200,150,'none',0,bath)+L(bx,110,bx+200,110,WATER_S,1.5)+P([(bx,70),(bx,260),(bx+200,260),(bx+200,70)],GLASS,3))
        tx=bx+80
        s.append(R(tx,30,40,200,GLASS,2.5,'#C9875C',20))   # 처음 색(같음)
        s.append(an('fade',R(tx+2,32,36,196,'none',0,fin,18),dur='2.2',delay='.4'))
        s.append(R(tx,30,40,200,GLASS,2.5,'none',20))
        s.append(T(bx+100,290,mix=lab,size=20,weight=700))
        s.append(T(bx+160,190,mix=word,size=19,anchor='start',fill=MUTED,halo=True))
    s.append(T(130,22,mix='',size=18))
    return svg((470,300),450,'이산화 질소를 봉한 유리관을 얼음물에 넣으면 색이 옅어지고 뜨거운 물에 넣으면 진해진다',s)
COLD='#E3EEFB'
FIG['TUBES']=tubes()

# ═════ 7 가역 반응과 비가역 반응 ═════
def rev():
    s=[]
    s.append(R(10,10,420,160,INK,2.5,'#FFFFFF',10)+T(20,38,mix='가역 — 밀폐 용기',size=19,anchor='start',weight=700))
    for (x,y),k in zip(((50,80),(110,130),(70,140),(150,80)),('N2','H2','H2','H2')):
        s.append(an('move',mol(k,x,y,1.0),**{'from':'4,-3','rep':'alt','dur':'1.0','ease':'io'}))
    s.append(eqarrow(190,100,60,sw=3))
    s.append(T(220,80,mix='정반응',size=18,fill=FIELD)+T(220,134,mix='역반응',size=18,fill=BF))
    for (x,y) in ((300,80),(370,120),(320,140)):
        s.append(an('move',mol('NH3',x,y,1.0),**{'from':'-3,4','rep':'alt','dur':'1.1','ease':'io'}))
    s.append(R(10,190,420,120,INK,2.5,'#FFFFFF',10)+T(20,218,mix='비가역 — 연소',size=19,anchor='start',weight=700))
    s.append(T(220,262,tex='\\ce{CH4 + 2O2 -> CO2 + 2H2O}',size=21))
    s.append(T(220,296,mix='역반응이 거의 일어나지 않는다',size=18,fill=MUTED))
    return svg((440,320),430,'밀폐 용기 속 질소·수소·암모니아의 가역 반응과 메테인 연소의 비가역 반응',s)
FIG['REV']=rev()

# ═════ 8 그림 Ⅳ-1 농도–시간 ═════
def fig1():
    ax=Ax(80,330,400,270,4,1.0)
    s=[ax.frame([0,1,2,3,4],[0,0.2,0.4,0.6,0.8,1.0],T(484,380,mix='시간',size=19,anchor='end',fill=MUTED),
                T(74,40,mix='몰농도 [M]',size=19,anchor='start',fill=MUTED),xfmt=lambda v:'',yfmt=lambda v:('%.1f'%v),size=18)]
    te=teq(RUN1)
    s.append(step('f1',shadeeq(ax,te,4,lab='평형',ly=ax.Y(0.5))))
    s.append(conc_plot(ax,RUN1,4))
    last=RUN1[-1]
    s.append(T(ax.X(3.0),ax.Y(last[1])-12,tex='\\ce{N2}\\ (\\text{반응물})',size=19,halo=True))
    s.append(T(ax.X(3.0),ax.Y(last[2])+30,tex='\\ce{H2}\\ (\\text{반응물})',size=19,halo=True))
    s.append(T(ax.X(3.0),ax.Y(last[3])-12,tex='\\ce{NH3}\\ (\\text{생성물})',size=19,fill=FIELD,halo=True))
    for j in (1,2,3): s.append(step('f1',C(ax.X(4),ax.Y(last[j]),5,INK,1.5,'#FFFFFF')))
    return svg((520,390),520,'암모니아 합성 반응에서 질소와 수소의 농도는 줄고 암모니아는 늘다가 평형에서 일정해진다',s)
FIG['FIG1']=fig1()

# ═════ 9 반응 속도로 본 평형 A ⇌ B ═════
def rate():
    kf,kr=0.30,0.10; Ae=kr/(kf+kr)
    Af=lambda t: Ae+(1-Ae)*exp(-(kf+kr)*t)
    s=[]
    a1=Ax(80,180,380,140,12,1.0); a2=Ax(80,400,380,140,12,0.30)
    s.append(a1.frame([0,4,8,12],[0,0.5,1.0],'',T(74,30,mix='농도 [M]',size=18,anchor='start',fill=MUTED),xfmt=lambda v:'',yfmt=lambda v:('%.1f'%v),size=18))
    s.append(a2.frame([0,4,8,12],[0,0.1,0.2,0.3],T(464,440,mix='시간',size=18,anchor='end',fill=MUTED),T(74,250,mix='반응 속도',size=18,anchor='start',fill=MUTED),xfmt=lambda v:'',yfmt=lambda v:('%.1f'%v),size=18))
    te=11.5/1.0
    te=-log(0.01/(1-Ae))/(kf+kr)
    for ax in (a1,a2): s.append(shadeeq(ax,te,12,lab=None))
    s.append(T(a1.X((te+12)/2),a1.Y(0.62),mix='평형',size=18,fill=MUTED,weight=700))
    s.append(an('draw',a1.curve(Af,0,12,col=INK,w=3.5),dur='1.4'))
    s.append(an('draw',a1.curve(lambda t:1-Af(t),0,12,col=FIELD,w=3.5),dur='1.4'))
    s.append(an('draw',a2.curve(lambda t:kf*Af(t),0,12,col=FIELD,w=3.5),dur='1.4',delay='.3'))
    s.append(an('draw',a2.curve(lambda t:kr*(1-Af(t)),0,12,col=BF,w=3.5,dash='9 6'),dur='1.4',delay='.3'))
    s.append(T(a1.X(1.0),a1.Y(Af(1.0))-10,tex='[\\ce{A}]',size=19,anchor='start',halo=True))
    s.append(T(a1.X(1.0),a1.Y(1-Af(1.0))+26,tex='[\\ce{B}]',size=19,anchor='start',fill=FIELD,halo=True))
    s.append(T(a2.X(0.7),a2.Y(kf*Af(0.7))-4,tex='v_\\text{정}',size=20,anchor='start',fill=FIELD,halo=True))
    s.append(T(a2.X(0.7),a2.Y(kr*(1-Af(0.7)))-6,tex='v_\\text{역}',size=20,anchor='start',fill=BF,halo=True))
    s.append(T(a2.X(12)-4,a2.Y(kf*Ae)-12,tex='v_\\text{정}=v_\\text{역}',size=19,anchor='end',halo=True))
    return svg((480,450),470,'A가 B로 되는 가역 반응에서 농도와 정반응·역반응 속도의 시간 변화, 두 속도가 같아지면 평형',s)
FIG['RATE']=rate()

# ═════ 12 표 Ⅳ-1 막대 ═════
def exp3():
    data=(('Ⅰ',(0.921,0.763,0.157)),('Ⅱ',(0.399,1.197,0.203)),('Ⅲ',(2.59,2.77,1.82)))
    ax=Ax(70,300,320,250,3,3.0)
    s=[ax.frame([],[0,1,2,3],T(0,0,mix='',size=18),T(64,32,mix='평형 농도 [M]',size=18,anchor='start',fill=MUTED),yfmt=lambda v:str(v),size=18)]
    fills=((INK,'.85'),(INK,'.3'),(FIELD,'.85'))
    for gi,(lab,vals) in enumerate(data):
        x0=ax.x0+16+gi*104
        for j,v in enumerate(vals):
            x=x0+j*26; y=ax.Y(v); col,op=fills[j]
            s.append(an('scale',R(x,y,22,ax.y0-y,col,1.5,col,0,extra=f'fill-opacity="{op}"'),**{'from':'1,0','o':f'{x+11},{ax.y0}','dur':'.9','delay':f(0.15*gi)}))
        s.append(T(x0+37,ax.y0+26,mix=f'실험 {lab}',size=18))
    lg=[('\\ce{N2}',INK,'.85'),('\\ce{H2}',INK,'.3'),('\\ce{NH3}',FIELD,'.85')]
    for j,(t,col,op) in enumerate(lg):
        s.append(R(98+j*86,46,18,18,col,1.5,col,0,extra=f'fill-opacity="{op}"')+T(122+j*86,62,tex=t,size=18,anchor='start'))
    s.append(T(230,352,mix='세 실험 모두 $K=6.02\\times10^{-2}$',size=19,weight=700))
    return svg((400,366),390,'표 IV-1 세 실험의 평형 농도는 서로 다르지만 평형 상수는 같다',s)
FIG['EXP3']=exp3()

# ═════ 16 Q와 K ═════
def qk():
    s=[]; y=150
    s.append(L(20,y,420,y,INK,3)+P([(408,y-8),(422,y),(408,y+8)],INK,3))
    s.append(T(420,y+34,mix='$Q$',size=20,anchor='end'))
    kx=220
    s.append(L(kx,y-40,kx,y+40,EQUI,4)+T(kx,y-50,mix='$K$ (평형)',size=20,weight=700,fill=EQUI))
    s.append(an('move',C(80,y,9,INK,2,'#FFFFFF')+T(80,y+36,mix='$Q&lt;K$',size=19),**{'from':'0,0'}))
    s.append(A(95,y-26,200,y-26,'field',4)+T(148,y-38,mix='정반응',size=19,fill=FIELD,weight=700))
    s.append(C(360,y,9,INK,2,'#FFFFFF')+T(360,y+36,mix='$Q&gt;K$',size=19))
    s.append(A(345,y-26,240,y-26,'bfield',4)+T(292,y-38,mix='역반응',size=19,fill=BF,weight=700))
    s.append(an('move',C(kx,y,7,INK,2,FIELD),**{'from':'-140,0','dur':'1.6','ease':'out','rep':'loop'}))
    s.append(an('move',C(kx,y,7,INK,2,BF),**{'from':'140,0','dur':'1.6','ease':'out','rep':'loop'}))
    s.append(T(kx,y+90,mix='어느 쪽에서 출발해도 $Q\\to K$',size=19,fill=MUTED))
    return svg((440,316),430,'Q가 K보다 작으면 정반응, 크면 역반응이 진행해 Q가 K와 같아진다',s)
FIG['QK']=qk()

# ═════ 20 실험실 설계: 시험관 5개 ═════
EPS=4700; KT=lambda t:200*exp((-25000/8.314)*(1/298.15-1/(t+273.15)))
def xeq(K,F,S):
    a=K; b=-(K*(F+S)+1); c=K*F*S; return (-b-sqrt(b*b-4*a*c))/(2*a)
def red(A):
    a=min(1,A/0.75); return f'rgb({round(250-(250-179)*a)},{round(238-(238-18)*a)},{round(214-(214-46)*a)})'
def labset():
    s=[]
    for n in range(1,6):
        x=20+(n-1)*78; A=EPS*xeq(200,1e-3,2e-4*n)
        s.append(P([(x,30),(x,150),(x+20,170),(x+40,150),(x+40,30)],GLASS,2.5,red(A)))
        s.append(an('fade',R(x+2,60,36,88,'none',0,red(A)),dur='1',delay=f(0.2*n)))
        s.append(P([(x,30),(x,150),(x+20,170),(x+40,150),(x+40,30)],GLASS,2.5))
        s.append(T(x+20,198,mix=f'{n}',size=20,weight=700))
    s.append(T(200,226,mix='$\\ce{KSCN}$ $1.00\\to5.00\\ \\text{mL}$ — 붉은색이 진해진다',size=18,fill=MUTED))
    return svg((400,236),390,'KSCN 부피가 1.00 mL에서 5.00 mL로 늘수록 붉은색이 진해지는 시험관 다섯 개',s)
FIG['LABSET']=labset()

# ═════ 22 실험실 결과 그래프 ═════
def labres():
    slope=EPS*xeq(200,0.100,1e-5)/1e-5
    rows={}
    for t in (25,40):
        rows[t]=[]
        for n in range(1,6):
            F,S=1e-3,2e-4*n; x=xeq(KT(t),F,S); xm=EPS*x/slope
            rows[t].append((n,xm/((F-xm)*(S-xm)),xm/((F-xm)+(S-xm))))
    s=[]
    a1=Ax(70,160,300,120,5.5,300,xmin=0.5); a2=Ax(70,350,300,120,5.5,0.10,xmin=0.5)
    s.append(a1.frame([1,2,3,4,5],[0,100,200,300],'',T(64,30,mix='$K$',size=19,anchor='start',fill=MUTED),xfmt=lambda v:'',size=18))
    s.append(a2.frame([1,2,3,4,5],[0,0.05,0.10],T(376,392,mix='용액',size=18,anchor='end',fill=MUTED),T(64,222,mix='다른 비',size=19,anchor='start',fill=MUTED),yfmt=lambda v:('0' if v==0 else '%.2f'%v),size=18))
    for t,col in ((25,INK),(40,PLUS)):
        ps=[(a1.X(n),a1.Y(k)) for n,k,r in rows[t]]
        s.append(P(ps,col,1.5,dash='5 4'))
        for i,(x,y) in enumerate(ps): s.append(an('pop',C(x,y,6,col,2,'#FFFFFF' if t==25 else PLUS),o=f'{f(x)},{f(y)}',dur='.5',delay=f(0.12*i)))
    s.append(T(a1.X(5.4),a1.Y(213)-14,mix='25 °C',size=18,anchor='end',halo=True))
    s.append(T(a1.X(5.4),a1.Y(131)+28,mix='40 °C',size=18,anchor='end',fill=PLUS,halo=True))
    ps=[(a2.X(n),a2.Y(r)) for n,k,r in rows[25]]
    s.append(an('draw',P(ps,MUTED,2.5),dur='1'))
    for x,y in ps: s.append(C(x,y,5,MUTED,2,'#FFFFFF'))
    return svg((400,400),390,'25도에서 다섯 용액의 평형 상수는 거의 같고 40도에서는 더 작으며, 다른 꼴의 농도 비는 용액마다 커진다',s)
FIG['LABRES']=labres()

# ═════ 23 그림 Ⅳ-2 G 곡선 ═════
def gcurve():
    Gf=lambda x:(1-x)*log(max(1e-9,(1-x)*2))+x*(-log(3)+log(max(1e-9,x*2)))
    ax=Ax(80,320,420,260,1.0,0.8,ymin=-0.8)
    s=[ax.frame([0,0.25,0.5,0.75,1.0],[],T(500,374,mix='반응한 $\\ce{A}$의 몰분율',size=19,anchor='end',fill=MUTED),
                T(74,40,mix='$G$',size=21,anchor='start',fill=MUTED),xfmt=lambda v:('0' if v==0 else ('1.0' if v==1 else str(v))),size=18)]
    s.append(L(ax.X(0.75),ax.y0,ax.X(0.75),ax.Y(0.8),MUTED,1.5,'5 4'))
    s.append(an('draw',ax.curve(Gf,0.0005,0.9995,n=400,col=INK,w=3.5),dur='1.4'))
    s.append(an('pop',C(ax.X(0.75),ax.Y(Gf(0.75)),8,INK,2,EQUI),o=f'{f(ax.X(0.75))},{f(ax.Y(Gf(0.75)))}',delay='1.3'))
    s.append(T(ax.X(0.75),ax.Y(0.62),mix='평형에||도달한 지점',size=19,weight=700,halo=True))
    s.append(A(ax.X(0.10),ax.Y(Gf(0.10))-22,ax.X(0.50),ax.Y(Gf(0.50))-22,'field',4))
    s.append(T(ax.X(0.08),ax.Y(Gf(0.08))-40,mix='(가) $\\ce{A}$에서 시작',size=19,anchor='start',fill=FIELD,halo=True))
    s.append(A(ax.X(0.985),ax.Y(Gf(0.985))-18,ax.X(0.83),ax.Y(Gf(0.83))-20,'bfield',4))
    s.append(T(ax.X(1.0),ax.Y(Gf(0.99))-44,mix='(나) $\\ce{B}$에서 시작',size=19,anchor='end',fill=BF,halo=True))
    s.append(T(ax.X(0.75)-14,ax.Y(Gf(0.75))-14,mix='$G$ 최소',size=19,anchor='end',fill=EQUI,halo=True))
    return svg((540,384),540,'A가 B로 되는 반응에서 깁스 자유 에너지는 A의 75퍼센트가 반응한 곳에서 가장 작고, 어느 쪽에서 시작해도 그곳에 도달한다',s)
FIG['GCURVE']=gcurve()

# ═════ 24 ΔG°와 K (298 K) ═════
def dgk():
    RT=8.314*298/1000; lg=lambda G:-G/(2.302585*RT)
    ax=Ax(90,300,280,240,20,4,xmin=-20,ymin=-4)
    s=[ax.frame([-20,-10,0,10,20],[-3,0,3],T(374,350,mix='$\\Delta G^\\circ$ [kJ]',size=19,anchor='end',fill=MUTED),
                T(84,34,mix='$K$ (로그 눈금, 298 K)',size=19,anchor='start',fill=MUTED),yfmt=lambda v:f'10^{{{int(v)}}}',size=18,grid=True)]
    s.append(L(ax.x0,ax.Y(0),ax.x0+ax.w,ax.Y(0),MUTED,1.5,'5 4'))
    s.append(an('draw',ax.curve(lg,-20,20,col=INK,w=3.5),dur='1.2'))
    s.append(an('pop',C(ax.X(0),ax.Y(0),7,INK,2,EQUI),o=f'{f(ax.X(0))},{f(ax.Y(0))}',delay='1'))
    s.append(T(ax.X(0)+12,ax.Y(0)+26,mix='$K=1$',size=19,anchor='start',halo=True))
    s.append(T(ax.X(-10),ax.Y(3.3),mix='$K&gt;1$',size=19,fill=FIELD,weight=700,halo=True))
    s.append(T(ax.X(10),ax.Y(-3.0),mix='$K&lt;1$',size=19,fill=BF,weight=700,halo=True))
    return svg((400,360),380,'298 K에서 표준 깁스 자유 에너지 변화가 음수이면 K가 1보다 크고 양수이면 1보다 작다',s)
FIG['DGK']=dgk()

# ═════ 27 그림 Ⅳ-3 분압 ═════
def conc():
    P0=(0.78,2.30,0.45); P1=(0.687,3.021,0.636); tau=0.55
    def pv(j,t):
        if t<3: return P0[j]
        start=P0[j]+(1.0 if j==1 else 0)
        return P1[j]+(start-P1[j])*exp(-(t-3)/tau)
    ax=Ax(90,330,440,280,9,4.0)
    s=[ax.frame([],[0,1,2,3,4],T(530,358,mix='시간',size=19,anchor='end',fill=MUTED),
                T(84,32,mix='부분 압력 [atm]',size=19,anchor='start',fill=MUTED),yfmt=lambda v:'%.1f'%v,size=18)]
    s.append(R(ax.X(0),ax.Y(4),ax.X(3)-ax.X(0),ax.h,'none',0,HL,extra='fill-opacity=".25"'))
    s.append(R(ax.X(6),ax.Y(4),ax.X(9)-ax.X(6),ax.h,'none',0,HL,extra='fill-opacity=".25"'))
    s.append(T(ax.X(1.5),ax.Y(3.75),mix='처음 평형',size=18,fill=MUTED,weight=700)+T(ax.X(7.5),ax.Y(3.75),mix='나중 평형',size=18,fill=MUTED,weight=700))
    for j,col,dash in ((0,INK,None),(1,INK,'10 6'),(2,FIELD,None)):
        pts=[(ax.X(t),ax.Y(pv(j,t))) for t in [i*0.02 for i in range(0,150)]]
        if j==1: pts.append((ax.X(3),ax.Y(P0[1]+1.0)))
        pts+=[(ax.X(t),ax.Y(pv(j,t))) for t in [3+i*0.02 for i in range(0,301)]]
        s.append(an('draw',P(pts,col,3.5,dash=dash,extra='stroke-linecap="round"'),dur='1.6'))
    s.append(A(ax.X(3)+40,ax.Y(3.9),ax.X(3)+6,ax.Y(3.42),'ink',2))
    s.append(T(ax.X(3)+44,ax.Y(3.88)+6,mix='$\\ce{H2}$ 1 atm 추가',size=18,anchor='start',halo=True))
    s.append(T(ax.X(1.5),ax.Y(P0[1])-12,tex='P_{\\ce{H2}}',size=19,halo=True))
    s.append(T(ax.X(1.5),ax.Y(P0[0])-12,tex='P_{\\ce{N2}}',size=19,halo=True))
    s.append(T(ax.X(1.5),ax.Y(P0[2])+28,tex='P_{\\ce{NH3}}',size=19,fill=FIELD,halo=True))
    for j in range(3): s.append(T(ax.X(9)-2,ax.Y(P1[j])+(-10 if j!=2 else 26),mix='%.2f'%P1[j],size=18,anchor='end',halo=True,fill=FIELD if j==2 else None))
    return svg((560,372),560,'평형인 암모니아 합성 반응에 수소 1 atm을 더 넣으면 수소와 질소의 부분 압력은 줄고 암모니아는 늘어 새 평형이 된다',s)
FIG['CONC']=conc()

# ═════ 28 그림 Ⅳ-4 압력 ═════
def pres():
    s=[]; W_=290; X0=(10,400,790); BOT=318; FT=64; HT=190
    A_=dict(N2=7,H2=13,NH3=8); C_=dict(N2=6,H2=10,NH3=10)
    def cyl(x,top,mols,seed,anim_piston=False):
        o=P([(x,FT-26),(x,BOT),(x+W_,BOT),(x+W_,FT-26)],INK,3)
        pist=R(x+3,top-14,W_-6,14,INK,2,'#C9D2DB')+L(x+W_/2,top-14,x+W_/2,top-40,INK,4)
        o+=an('move',pist,**{'from':f'0,{f(FT-top)}','dur':'1.4','ease':'out'}) if anim_piston else pist
        h=BOT-top; kinds=[k for k,nn in mols.items() for _ in range(nn)]
        random.Random(seed).shuffle(kinds)
        pts=placed(len(kinds),x+16,top+14,W_-32,h-28,24 if h<150 else 32,seed)
        body=''.join(mol(k,px,py,0.7) for k,(px,py) in zip(kinds,pts))
        return o, body
    o,b=cyl(X0[0],FT,A_,11); s.append(o+an('move',b,**{'from':'3,-3','rep':'alt','dur':'1.2','ease':'io'}))
    o,b=cyl(X0[1],HT,A_,12,True); s.append(o+b)
    o,b=cyl(X0[2],HT,C_,23); s.append(o+an('fade',b,dur='1',delay='1.4'))
    s.append(A(X0[0]+W_+14,200,X0[1]-14,200,'ink',3)+T((X0[0]+W_+X0[1])/2,186,mix='압축',size=18,fill=MUTED))
    s.append(A(X0[1]+W_+14,200,X0[2]-14,200,'field',3)+T((X0[1]+W_+X0[2])/2,186,mix='정반응',size=18,fill=FIELD,weight=700))
    for x,lab,cnt in ((X0[0],'(가) 평형','$\\ce{N2}$ 7, $\\ce{H2}$ 13, $\\ce{NH3}$ 8 (28개)'),(X0[1],'(나) 압력을 증가시킴','부피 $\\tfrac12$, 분자 수 그대로'),(X0[2],'(다) 새로운 평형','$\\ce{N2}$ 6, $\\ce{H2}$ 10, $\\ce{NH3}$ 10 (26개)')):
        s.append(T(x+W_/2,BOT+27,mix=lab,size=19,weight=700)+T(x+W_/2,BOT+53,mix=cnt,size=18,fill=MUTED))
    lx=820
    for i,(k,t) in enumerate((('N2','\\ce{N2}'),('H2','\\ce{H2}'),('NH3','\\ce{NH3}'))):
        s.append(mol(k,lx+i*100,22,0.8)+T(lx+i*100+20,29,tex=t,size=19,anchor='start'))
    return svg((1090,378),1090,'질소·수소·암모니아 평형 혼합물(가)의 부피를 절반으로 줄이면(나) 분자 수가 줄어드는 정반응 쪽으로 이동해 새로운 평형(다)이 된다',s)
FIG['PRES']=pres()

# ═════ 29 표 Ⅳ-3 막대 (로그 눈금) ═════
def temp():
    data=((500,90),(600,3),(700,0.3),(800,0.04))
    ax=Ax(80,320,280,230,4,2,xmin=0,ymin=-2)
    s=[ax.frame([],[-2,-1,0,1,2],T(0,0,mix='',size=18),T(74,32,mix='$K$ (로그 눈금)',size=19,anchor='start',fill=MUTED),yfmt=lambda v:f'10^{{{int(v)}}}',size=18)]
    for i,(Tk,Kv) in enumerate(data):
        x=ax.x0+22+i*66; y=ax.Y(math.log10(Kv)); yb=ax.Y(-2)
        s.append(an('scale',R(x,y,40,yb-y,INK,1.5,INK,0,extra='fill-opacity=".6"'),**{'from':'1,0','o':f'{x+20},{yb}','dur':'.9','delay':f(0.15*i)}))
        s.append(T(x+20,y-10,mix=f'{Kv:g}',size=18,halo=True)+T(x+20,ax.y0+26,mix=f'{Tk}',size=18))
    s.append(T(ax.x0+ax.w,ax.y0+52,mix='온도 [K]',size=19,anchor='end',fill=MUTED))
    s.append(A(ax.x0+150,62,ax.x0+282,62,'muted',2.5)+T(ax.x0+216,50,mix='온도 ↑ → $K$ ↓',size=19,halo=True))
    return svg((380,380),370,'표 IV-3 암모니아 합성의 평형 상수는 온도가 500 K에서 800 K로 높아질수록 90에서 0.04로 작아진다',s)
FIG['TEMP']=temp()

# ═════ 30 그림 Ⅳ-5 수득률 ═════
def Kp_T(Tc): T_=Tc+273.15; return exp(-(-92000+T_*198.9)/(8.314*T_))
def yld(Tc,P_):
    K=Kp_T(Tc); lo,hi=0,0.9999
    for _ in range(80):
        m=(lo+hi)/2; nt=4-2*m; yA=2*m/nt; yN=(1-m)/nt; yH=3*(1-m)/nt
        Q=(yA*P_)**2/((yN*P_)*(yH*P_)**3); (lo,hi)=(m,hi) if Q<K else (lo,m)
    return 100*lo
def haber():
    ax=Ax(80,300,400,250,550,100,xmin=350,ymin=0)
    s=[ax.frame([350,400,450,500,550],[0,20,40,60,80,100],T(480,350,mix='온도 [°C]',size=19,anchor='end',fill=MUTED),
                T(74,32,mix='암모니아 수득률 [%]',size=19,anchor='start',fill=MUTED),yfmt=lambda v:('' if v==0 else str(v)),size=18)]
    LY={}
    s.append(R(ax.X(400),ax.Y(100),ax.X(530)-ax.X(400),ax.h,'none',0,HL,extra='fill-opacity=".25"'))
    s.append(T(ax.X(465),ax.Y(92),mix='실제 공정 400–530 °C',size=18,fill=MUTED,weight=700))
    for i,(P_,dash,op) in enumerate(((100,'3 5',1),(200,'10 6',1),(300,None,1),(400,None,1))):
        p=ax.curve(lambda t:yld(t,P_),350,550,n=60,col=INK if P_!=400 else FIELD,w=3,dash=dash)
        s.append(an('draw',p,dur='1.2',delay=f(0.2*i)) if not dash else p)
        LY[P_]=ax.Y(yld(550,P_))+6
    ys=sorted(LY.items(),key=lambda kv:kv[1])
    for i in range(1,len(ys)):
        if ys[i][1]-ys[i-1][1]<21: ys[i]=(ys[i][0],ys[i-1][1]+21)
    for P_,yv in ys: s.append(T(ax.X(550)+6,yv,mix=f'{P_} atm',size=18,anchor='start',fill=FIELD if P_==400 else None))
    s.append(T(280,382,mix='계산값: 이상 기체, $\\ce{N2}:\\ce{H2}=1:3$, $\\Delta H^\\circ$·$\\Delta S^\\circ$ 일정',size=18,fill=MUTED))
    return svg((560,392),560,'암모니아 수득률은 온도가 낮을수록, 전체 압력이 높을수록 크다(계산값)',s)
FIG['HABER']=haber()

# ═════ 32·33 달걀 껍질 평형 사슬 ═════
EGGEQ=['\\ce{CO2(g) <=> CO2(aq)}','\\ce{CO2(aq) + H2O(l) <=> H2CO3(aq)}','\\ce{H2CO3(aq) <=> H+(aq) + HCO3^-(aq)}','\\ce{HCO3^-(aq) <=> H+(aq) + CO3^2-(aq)}','\\ce{Ca^2+(aq) + CO3^2-(aq) <=> CaCO3(s)}']
def egg(shift):
    s=[]
    s.append(R(10,6,440,40,MUTED,1.5,'#F7F8FA',8)+T(230,34,mix=('더위 → 과호흡 → 혈액의 $\\ce{CO2}$ 감소' if shift else '닭의 날숨으로 $\\ce{CO2(g)}$가 빠져나간다'),size=19))
    for i,e in enumerate(EGGEQ):
        y=86+i*64
        box=R(30,y-30,400,48,INK if i==4 else MUTED,2 if i==4 else 1.5,'#FFF8EF' if i==4 else '#FFFFFF',10)+T(230,y+2,tex=e,size=19)
        s.append(box)
        if i<4: s.append(L(230,y+18,230,y+34,MUTED,2))
        if shift:
            s.append(step(f'e{2 if i<4 else 3}',A(470,y-6,438,y-6,'bfield',4)))
    if shift: s.append(step('e3',T(450,y+46,mix='껍질의 탄산 칼슘 감소',size=19,anchor='end',fill=BF,weight=700)))
    else: s.append(T(230,y+46,mix='달걀 껍질 (탄산 칼슘)',size=19,fill=MUTED))
    return svg((480,400),470 if shift else 450,'날숨의 이산화 탄소와 달걀 껍질의 탄산 칼슘을 잇는 평형 다섯 개'+(', 이산화 탄소가 줄면 모두 역반응 쪽으로 이동' if shift else ''),s)
FIG['EGG']=egg(False); FIG['EGG2']=egg(True)

# ═════ 34 그림 Ⅳ-6 ln K–1/T ═════
def vant():
    sl=92000/8.314/1000; ic=-198.9/8.314
    ax=Ax(80,330,380,290,2.4,4,xmin=0,ymin=-32)
    s=[ax.frame([0,0.6,1.2,1.8,2.4],[-32,-24,-16,-8,0],T(470,380,mix='$\\tfrac{1}{T}\\times10^{3}$ [1/K]',size=19,anchor='end',fill=MUTED),
                T(74,32,mix='$\\ln K$',size=20,anchor='start',fill=MUTED),xfmt=lambda v:('0' if v==0 else '%.1f'%v),size=18)]
    s.append(L(ax.x0,ax.Y(0),ax.x0+ax.w,ax.Y(0),MUTED,1.5,'5 4'))
    s.append(an('draw',ax.curve(lambda x:sl*x+ic,0,2.4,col=INK,w=3.5),dur='1.4'))
    for i,Tk in enumerate((833,714,625,556,476)):
        x=1000/Tk; y=sl*x+ic
        s.append(an('pop',C(ax.X(x),ax.Y(y),6,PLUS,1.5,PLUS),o=f'{f(ax.X(x))},{f(ax.Y(y))}',delay=f(1.2+0.12*i)))
    s.append(an('pop',C(ax.X(0),ax.Y(ic),7,INK,2,EQUI),o=f'{f(ax.X(0))},{f(ax.Y(ic))}',delay='1.3'))
    s.append(T(ax.X(0.15),ax.Y(-27.5),mix='절편 $=\\dfrac{\\Delta S^\\circ}{R}=-23.9$',size=19,anchor='start',halo=True))
    x1,x2=1.2,1.8
    s.append(L(ax.X(x1),ax.Y(sl*x1+ic),ax.X(x2),ax.Y(sl*x1+ic),MUTED,2,'5 4')+L(ax.X(x2),ax.Y(sl*x1+ic),ax.X(x2),ax.Y(sl*x2+ic),MUTED,2,'5 4'))
    s.append(T(ax.X(1.5),ax.Y(sl*x1+ic)+36,mix='기울기 $=-\\dfrac{\\Delta H^\\circ}{R}$',size=19,halo=True))
    s.append(T(ax.X(0.08),ax.Y(-3.5),mix='계산값: $\\Delta H^\\circ=-92\\ \\text{kJ}$,||$\\Delta S^\\circ=-198.9\\ \\text{J/K}$',size=18,anchor='start',fill=MUTED))
    return svg((480,392),470,'암모니아 합성에서 ln K와 1/T는 기울기가 −ΔH°/R, 절편이 ΔS°/R인 직선이다',s)
FIG['VANT']=vant()

# ═════ 출력 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT+'slides.html','w',encoding='utf-8').write(out)
for src,dst in (('labs_src.js','labs.js'),('extra_src.css','extra.css')):
    if os.path.exists(os.path.join(HERE,src)): shutil.copy(os.path.join(HERE,src),OUT+dst)
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "화학 평형", "file": "4-1-1_화학_평형", "header": "Ⅳ-1-1 화학 평형 (고등 고급 화학 190–199쪽)"}\n')
print('ok',len(out),'sections',out.count('<section'),'anim',out.count('data-anim'))
