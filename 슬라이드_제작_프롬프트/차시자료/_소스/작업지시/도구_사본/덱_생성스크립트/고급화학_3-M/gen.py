# -*- coding: utf-8 -*-
"""고급화학 3-M 대단원 Ⅲ 마무리 — 그림 생성. h.py·cellh.py(3-5-1 사본) + 2-M gen 꼴.
   tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html, extra_src.css → extra.css.  python3 -I gen.py
   ★ 출력 OUT은 이 덱(3-M) 폴더만 — assert로 막음"""
import math, re, sys, os, random, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cellh import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FD='3-M_대단원_Ⅲ_마무리'; OUT=BASE+FD+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/3-M_대단원_Ⅲ_마무리/', OUT
assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FD) and '/3-M_' in OUT, OUT
FIG={}
MET['Pb']=('#A9B0BA','#6E7783'); MET['Fe']=('#B7C0C9','#7E8B98'); MET['Al']=('#E3E7EC','#9AA5B1')
RUB='#7A5C3E'; SYS_BG='#FFF4E8'; PHE='#E04F8A'
def G(body,attrs=''): return f'<g {attrs}>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def pop(body,x,y,d=0,dur='.6'): return an('pop',body,o=f'{f(x)},{f(y)}',dur=dur,delay=f'{d:.1f}')
def mvalt(body,dx,dy,dur='1.4',delay='0'): return an('move',body,**{'from':f'{f(dx)},{f(dy)}','rep':'alt','dur':dur,'delay':delay,'ease':'io'})
def draw(body,dur='1',delay='0'): return an('draw',body,dur=dur,delay=delay)
def stp(g,body): return step(g,''.join(body) if isinstance(body,list) else body)
random.seed(39)

# ═══ 검산 (plan.md 2절)
dV=math.pi*1.5**2*20/1000; W1=2.00*dV*101.325
assert abs(dV-0.1414)<5e-4 and abs(W1-28.65)<0.01
assert abs(60*-393.51+25937-2326.4)<0.01
n4=4.95*1.67/(0.08206*323); dS4=n4*8.314*math.log(7.33/1.67)
assert abs(n4-0.312)<5e-4 and abs(dS4-3.84)<5e-3
assert abs(-90-298*-0.220+24.44)<1e-6 and round(90/0.220)==409
E10=0.02-0.0592/2*math.log10(0.10/0.40); assert abs(E10-0.0378)<1e-4
assert abs((0.34-0.80)+0.46)<1e-9 and abs(1.36+0.13-1.49)<1e-9
EP={'Mg':-2.37,'Zn':-0.76,'Fe':-0.44,'Pb':-0.13,'Cu':0.34,'Ag':0.80}
COMBO=[('Zn','Cu'),('Fe','Cu'),('Pb','Ag'),('Zn','Ag'),('Mg','Cu'),('Mg','Ag')]
CV={(a,b):round(EP[b]-EP[a],2) for a,b in COMBO}
assert CV[('Zn','Cu')]==1.10 and CV[('Mg','Ag')]==3.17 and CV[('Pb','Ag')]==0.93
print('w1',round(W1,2),'n',round(n4,4),'dS',round(dS4,3),'E10',round(E10,4),CV)

# ═══ 공통 그림 조각
def gas(x,y,r=9): return C(x,y,r,GAS_S,1.5,GAS)
def chains(x0,y0,w,h,n=4,seed=1,stretched=False,col=RUB):
    """고무 사슬 n개 + 교차 결합(빨간 점). stretched=True면 나란히 펴진 사슬"""
    rnd=random.Random(seed); s=[]; P_=[]
    if stretched:
        for k in range(n):
            yy=y0+h*(k+0.5)/n; ph=rnd.uniform(0,6)
            pts=[(x0+w*i/60,yy+2.2*math.sin(ph+i*0.9)) for i in range(61)]
            P_.append(pts)
        links=[(k,i) for k in range(n-1) for i in (12,34,52) if (k+i)%2==0 or k==1]
    else:
        for k in range(n):
            px,py=x0+w*rnd.uniform(.2,.8),y0+h*rnd.uniform(.2,.8); th=rnd.uniform(0,6.28); pts=[(px,py)]
            for i in range(60):
                th+=rnd.uniform(-.75,.75); nx,ny=px+5.2*math.cos(th),py+5.2*math.sin(th)
                if not (x0+6<nx<x0+w-6): th=math.pi-th; nx=px+5.2*math.cos(th)
                if not (y0+6<ny<y0+h-6): th=-th; ny=py+5.2*math.sin(th)
                px,py=nx,ny; pts.append((px,py))
            P_.append(pts)
        links=[]
    for k,pts in enumerate(P_): s.append(P(pts,col,3,extra='stroke-linecap="round"'))
    if stretched:
        for k,i in links:
            (ax,ay),(bx,by)=P_[k][i],P_[k+1][i]; s.append(L(ax,ay,bx,by,PLUS,2.2)); s.append(C(ax,ay,3.6,PLUS,1,PLUS)+C(bx,by,3.6,PLUS,1,PLUS))
    else:
        cnt=0
        for k in range(n):
            for j in range(k+1,n):
                best=None
                for i in range(5,56,3):
                    for m in range(5,56,3):
                        d=math.dist(P_[k][i],P_[j][m])
                        if 6<d<16 and (best is None or d<best[0]): best=(d,i,m)
                if best and cnt<4:
                    (ax,ay),(bx,by)=P_[k][best[1]],P_[j][best[2]]
                    s.append(L(ax,ay,bx,by,PLUS,2.2)+C(ax,ay,3.6,PLUS,1,PLUS)+C(bx,by,3.6,PLUS,1,PLUS)); cnt+=1
    return ''.join(s)
def piston(x0,y0,w,h,py,gasn=6,anim=True,seed=3,pis=True):
    """세로 실린더(위가 열림) x0..x0+w, 바닥 y0+h, 피스톤 윗면 py"""
    rnd=random.Random(seed); s=[R(x0+3,py+14,w-6,y0+h-py-17,col='none',sw=0,fill=SYS_BG)]
    s.append(P([(x0,y0),(x0,y0+h),(x0+w,y0+h),(x0+w,y0)],INK,3))
    for i in range(gasn):
        gx=rnd.uniform(x0+16,x0+w-16); gy=rnd.uniform(py+30,y0+h-14)
        s.append(mvalt(gas(gx,gy),rnd.choice([-1,1])*8,rnd.choice([-1,1])*6,dur=f'{rnd.uniform(1,1.6):.1f}') if anim else gas(gx,gy))
    if pis: s.append(R(x0+3,py,w-6,14,INK,2,'#C9D2DB',2)); s.append(L(x0+w/2,py,x0+w/2,py-40,INK,4))
    return ''.join(s)

# ═══ S1 표지
def cover():
    s=[]
    s.append(piston(30,60,130,200,130,pis=False))
    s.append(an('move',G([R(33,130,124,14,INK,2,'#C9D2DB',2),L(95,130,95,90,INK,4)]),**{'from':'0,30','rep':'alt','dur':'1.8','ease':'io'}))
    s.append(A(70,300,120,300,'equi',3)+T(95,330,mix='열과 일',size=20))
    s.append(R(210,70,150,120,MUTED,1.5,'#FFFFFF',10,dash='5 4')); s.append(chains(212,72,146,116,4,seed=5))
    s.append(A(285,200,285,232,'ink',3))
    s.append(an('move',chains(190,240,190,56,4,seed=6,stretched=True),**{'from':'-14,0','rep':'alt','dur':'1.6','ease':'io'}))
    s.append(T(285,330,mix='고무줄의 엔트로피',size=20))
    # 전자 이동
    s.append(R(430,150,22,110,MET['Zn'][1],2,MET['Zn'][0],3)+R(530,150,22,110,MET['Cu'][1],2,MET['Cu'][0],3))
    s.append(P([(441,150),(441,90),(541,90),(541,150)],INK,3))
    s.append(f'<path d="M441 150 V90 H541 V150" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="36"/>')
    s.append(T(491,80,tex='e^-',size=21,fill=MINUS)+T(441,284,tex='\\ce{Zn}',size=20)+T(541,284,tex='\\ce{Cu}',size=20))
    s.append(T(491,330,mix='전자의 이동',size=20))
    return svg((580,350),560,'피스톤 속 기체의 열과 일, 엉킨 고무 사슬과 늘인 사슬, 아연에서 구리로 이동하는 전자',s)
FIG['COVER']=cover()

# ═══ S5 전자 이동(작게)
def eltr():
    s=[C(70,60,30,MET['Zn'][1],2,MET['Zn'][0]),T(70,67,tex='\\ce{Zn}',size=20),
       C(330,60,22,MET['Cu'][1],2,MET['Cu'][0]),T(330,66,tex='\\ce{Cu^2+}',size=18)]
    s.append(A(110,60,296,60,'muted',2.5))
    for i,dx in enumerate((150,200)):
        s.append(an('move',elec(dx,48,lab=True),**{'from':'-40,0','rep':'loop','dur':'1.6','ease':'lin','delay':f'{0.5*i:.1f}'}))
    s.append(T(70,118,mix='산화: 전자 잃음',size=19,fill=OX)+T(330,118,mix='환원: 전자 얻음',size=19,fill=RD))
    return svg((420,130),400,'아연 원자가 전자 2개를 구리 이온에 주어 아연은 산화되고 구리 이온은 환원된다',s)
FIG['ELTR']=eltr()

# ═══ S7 물의 전기 분해
def bub(x,y0,y1,n,r=6,delay=0):
    o=[]
    for i in range(n):
        yy=y0+(y1-y0)*i/max(1,n-1)*0.85; xx=x+(5 if i%2 else -5)
        o.append(an('move',C(xx,yy,r,MUTED,1.5,'#FFFFFF'),**{'from':f'0,{f(min(60,y1-yy+10))}','dur':'1.6','rep':'loop','ease':'lin','delay':f(delay+.3*i)}))
    return ''.join(o)
def elec_fig():
    s=[circ([["wire",[[120,100],[120,52],[192,52]]],["bat",[200,52],{"dir":"h","pos":"right","signs":True}],["wire",[[208,52],[280,52],[280,100]]]])]
    s.append(beaker(40,360,top=130,bot=300)); s.append(R(42,160,316,138,col='none',sw=0,fill=WATER))
    s.append(plate(120,'Pt',top=100,h=170)); s.append(plate(280,'Pt',top=100,h=170))
    s.append(bub(120,170,262,6)); s.append(bub(280,190,262,3,delay=.2))
    s.append(T(120,330,mix='(−)극 $\\ce{H2}$',size=20,weight=700,fill=RD)+T(280,330,mix='(+)극 $\\ce{O2}$',size=20,weight=700,fill=OX))
    s.append(T(200,362,mix='부피비 2 : 1',size=21,fill=MUTED))
    return svg((400,375),330,'물의 전기 분해: 전원의 (−)극에 연결된 전극에서 수소, (+)극에서 산소 기포가 2대 1로 생긴다',s)
FIG['ELEC']=elec_fig()

# ═══ S8 연결 흐름
def flow():
    s=[]; W_,H_=320,74
    boxes=[(170,60,'$\\Delta U=q+w$','Ⅲ-1 열과 일'),(550,60,'$\\Delta H=q_P$, 헤스 법칙','Ⅲ-1 엔탈피'),(930,60,'$\\Delta S_\\text{전체}=\\Delta S+\\Delta S_\\text{주위}$','Ⅲ-2 엔트로피'),
           (930,210,'$\\Delta G=\\Delta H-T\\Delta S$','Ⅲ-2 자발성'),(550,210,'$\\Delta G^\\circ=-nFE^\\circ_\\text{전지}$','Ⅲ-3·4 산화 환원·전지')]
    for i,(x,y,tx,lab) in enumerate(boxes):
        g=[R(x-W_/2,y-H_/2,W_,H_,INK,2,'#FFFFFF',12),T(x,y+2,mix=tx,size=22),T(x,y+28,mix=lab,size=18,fill=MUTED)]
        s.append(pop(''.join(g),x,y,0.35*i))
    arr=[(330,60,390,60),(710,60,770,60),(930,97,930,173),(770,210,710,210)]
    for i,(a,b,c,d) in enumerate(arr): s.append(draw(A(a,b,c,d,'ink',3),dur='.4',delay=f'{0.35*i+0.25:.2f}'))
    # 갈래
    s.append(draw(A(390,210,300,170,'field',3)+A(390,210,300,262,'plus',3),dur='.5',delay='1.6'))
    s.append(pop(R(40,140,260,60,FIELD,2,'#EAF6EF',10)+T(170,166,mix='화학 전지',size=21,weight=700)+T(170,190,mix='$\\Delta G&lt;0$, $E&gt;0$ 자발',size=18),170,170,1.8))
    s.append(pop(R(40,232,260,60,PLUS,2,'#FDECEE',10)+T(170,258,mix='전해 전지 (Ⅲ-5)',size=21,weight=700)+T(170,282,mix='$\\Delta G&gt;0$ — 외부 전기 에너지',size=18),170,262,2.0))
    return svg((1110,300),1080,'열과 일, 엔탈피, 엔트로피, 깁스 자유 에너지, 전지 전위로 이어지는 대단원 Ⅲ의 흐름과 화학 전지·전해 전지의 갈래',s)
FIG['FLOW']=flow()

# ═══ S12 펌프
def pump():
    s=[]; x0,x1,y0,y1=60,370,60,140
    s.append(R(x0,y0,x1-x0,y1-y0,col='none',sw=0,fill=SYS_BG))
    s.append(P([(x1,y0),(x0,y0),(x0,y1),(x1,y1)],INK,3)); s.append(P([(x0,94),(34,94)],INK,3)+P([(x0,106),(34,106)],INK,3))
    s.append(L(340,y0+3,340,y1-3,MUTED,2,dash='6 5')); s.append(T(340,y0-10,mix='처음',size=20,fill=MUTED))
    for i,(gx,gy) in enumerate([(90,82),(130,118),(170,86),(200,122),(105,108),(185,104)]):
        s.append(mvalt(gas(gx,gy),random.choice([-1,1])*6,random.choice([-1,1])*5,dur=f'{1.1+0.1*i:.1f}'))
    pis=[R(220,y0+3,16,y1-y0-6,INK,2,'#C9D2DB',2),L(236,100,400,100,INK,5),R(400,72,14,56,INK,2,'#C9D2DB',3),A(470,100,420,100,'ink',4)]
    s.append(an('move',''.join(pis),**{'from':'120,0','dur':'1.6','ease':'io'}))
    s.append(T(565,46,mix='$P_\\text{외부}=2.00\\ \\text{atm}$',size=21,anchor='end'))
    s.append(L(228,y1+30,340,y1+30,MUTED,1.5)+L(228,y1+22,228,y1+38,MUTED,1.5)+L(340,y1+22,340,y1+38,MUTED,1.5))
    s.append(T(284,y1+58,mix='20 cm',size=21))
    s.append(L(40,y0,40,y1,MUTED,1.5)+L(34,y0,46,y0,MUTED,1.5)+L(34,y1,46,y1,MUTED,1.5)+T(20,y1+58,mix='지름 3.0 cm',size=21,anchor='start'))
    s.append(T(130,y0-10,mix='계: 펌프 안 공기',size=20,fill=MUTED))
    return svg((570,215),560,'자전거 펌프의 피스톤을 2.00 atm 외부 압력으로 20 cm 밀어 안의 공기를 압축한다',s)
FIG['PUMP']=pump()

# ═══ S13 엔탈피 도표
def hdiag():
    s=[]; Y=lambda H: 100-H*(300/25937)
    s.append(A(40,410,40,20,'muted',2)); s.append(T(50,26,mix='엔탈피 $H$',size=20,anchor='start',fill=MUTED))
    s.append(L(60,Y(2326),300,Y(2326),INK,3)); s.append(L(300,Y(0),560,Y(0),INK,3)); s.append(L(60,Y(-23610.6),560,Y(-23610.6),INK,3))
    s.append(L(300,Y(2326),560,Y(2326),MUTED,1.5,dash='5 4'))
    s.append(T(62,Y(2326)-10,mix='$\\ce{C60(s) + 60O2(g)}$',size=20,anchor='start')+T(302,Y(0)+28,mix='$\\ce{60C(s)}$(흑연) + $\\ce{60O2(g)}$',size=20,anchor='start')+T(310,Y(-23610.6)+30,mix='$\\ce{60CO2(g)}$',size=20))
    s.append(draw(A(130,Y(2326)+2,130,Y(-23610.6)-2,'ink',3),delay='.2')); s.append(T(140,230,mix='연소 $-25937$ kJ',size=20,anchor='start',halo=True))
    s.append(draw(A(550,Y(0)+40,550,Y(-23610.6)-2,'ink',3),delay='.6')); s.append(T(540,250,mix='$60\\times(-393.51)$',size=20,anchor='end',halo=True)+T(540,278,mix='$=-23610.6$ kJ',size=20,anchor='end',halo=True))
    s.append(stp('h1',[A(520,Y(0)-2,520,Y(2326)+1,'plus',3),T(510,Y(2326)-10,mix='$\\Delta H_\\mathrm{f}^\\circ=+2326$ kJ',size=20,anchor='end',fill=PLUS,halo=True)]))
    return svg((580,440),520,'엔탈피 도표: C60과 산소가 흑연과 산소보다 2326 kJ 높고, 연소하면 25937 kJ 낮은 이산화 탄소가 된다',s)
FIG['HDIAG']=hdiag()

# ═══ S14 세 비교
def ent3():
    s=[]
    # 1) I2, Br2
    s.append(T(10,30,mix='1)',size=20,anchor='start',weight=700))
    s.append(mvalt(C(90,40,20,'#5E3A8C',2,'#B79AD6')+C(126,40,20,'#5E3A8C',2,'#B79AD6')+T(108,47,tex='\\ce{I2}',size=19),6,-4))
    s.append(mvalt(C(270,40,15,'#8E3B2E',2,'#E3A091')+C(297,40,15,'#8E3B2E',2,'#E3A091')+T(283,46,tex='\\ce{Br2}',size=18),-6,4,dur='1.2'))
    s.append(T(108,84,mix='$\\ce{I2}$ 증기 ($M=254$)',size=18)+T(283,84,mix='$\\ce{Br2}$ 증기 ($M=160$)',size=18))
    # 2) 사이클로펜테인 / 1-펜텐
    y=150; s.append(T(10,y-20,mix='2)',size=20,anchor='start',weight=700))
    pent=[(105+32*math.cos(math.radians(-90+72*i)),y+4+32*math.sin(math.radians(-90+72*i))) for i in range(5)]
    s.append(P(pent,INK,2.8,close=True)); s.append(T(105,y+62,mix='사이클로펜테인',size=18))
    zz=[(225,y+16),(250,y-10),(278,y+16),(306,y-10),(334,y+16)]
    s.append(an('rot',P(zz,INK,2.8),**{'from':'8','o':'280,150','rep':'alt','dur':'1.4','ease':'io'}))
    (ax_,ay_),(bx_,by_)=zz[0],zz[1]; ux,uy=(bx_-ax_)/math.dist(zz[0],zz[1]),(by_-ay_)/math.dist(zz[0],zz[1]); px,py=uy,-ux
    px,py=-px,-py
    s.append(L(ax_+6*px+4*ux,ay_+6*py+4*uy,bx_+6*px-4*ux,by_+6*py-4*uy,INK,2.4))
    s.append(T(280,y+62,mix='1-펜텐 (사슬)',size=18))
    # 3) 에틸렌 / 폴리에틸렌
    y=275; s.append(T(10,y-36,mix='3)',size=20,anchor='start',weight=700))
    rnd=random.Random(7)
    for i in range(6):
        cx,cy=50+ (i%3)*48+rnd.uniform(-6,6), y-18+(i//3)*34
        m=C(cx-7,cy,7,INK,1.5,'#8C99A6')+C(cx+7,cy,7,INK,1.5,'#8C99A6')
        s.append(mvalt(m,rnd.choice([-1,1])*7,rnd.choice([-1,1])*5,dur=f'{rnd.uniform(1,1.6):.1f}'))
    s.append(T(100,y+42,mix='에틸렌 (기체)',size=18))
    poly=[(225+11*i,y+(-8 if i%2 else 8)-6) for i in range(15)]
    s.append(P(poly,INK,2.6)); s.append(T(300,y+42,mix='폴리에틸렌 (고체)',size=18))
    return svg((400,330),380,'아이오딘과 브로민 분자, 고리 모양 사이클로펜테인과 사슬 모양 1-펜텐, 많은 에틸렌 분자와 긴 폴리에틸렌 사슬 하나',s)
FIG['ENT3']=ent3()

# ═══ S15 두 경로
def paths():
    s=[]
    s.append(T(10,24,mix='1) 등온 가역 팽창',size=21,anchor='start',weight=700))
    s.append(piston(60,60,120,150,110,gasn=5,seed=11,pis=False))
    s.append(an('move',R(63,110,114,14,INK,2,'#C9D2DB',2)+L(120,110,120,70,INK,4),**{'from':'0,60','dur':'2','ease':'io'}))
    for i,yy in enumerate((140,175)):
        s.append(an('move',A(250,yy,186,yy,'equi',3),**{'from':'16,0','rep':'alt','dur':'1.2','delay':f'{.3*i:.1f}','ease':'io'}))
    s.append(T(200,232,mix='열 흡수 $q=T\\Delta S$',size=21,fill=EQUI,anchor='start')); s.append(T(130,232,mix='323 K',size=20,fill=MUTED))
    s.append(T(10,280,mix='2) 등온 비가역 자유 팽창 (진공으로)',size=21,anchor='start',weight=700))
    s.append(R(40,300,150,110,INK,3,SYS_BG,10)+R(230,300,150,110,INK,3,'#FFFFFF',10)+R(190,345,40,20,INK,2,'#E9EDF1'))
    rnd=random.Random(12)
    for i in range(8):
        tx,ty=rnd.uniform(60,360),rnd.uniform(318,394)
        if 186<tx<234: tx+=60
        fx=-(tx-110) if tx>200 else 0
        s.append(an('move',gas(tx,ty),**{'from':f'{f(fx)},0','dur':'1.6','delay':f'{.1*i:.1f}','ease':'io'}))
    s.append(T(305,436,mix='진공이던 쪽',size=20,fill=MUTED)+T(115,436,mix='처음 기체',size=20,fill=MUTED))
    s.append(T(210,464,mix='$w=0$, $q=0$ (주위 변화 없음)',size=21))
    return svg((420,480),400,'경로 1: 피스톤이 천천히 올라가며 주위에서 열을 흡수하는 등온 가역 팽창. 경로 2: 진공 쪽으로 기체가 퍼지는 자유 팽창',s)
FIG['PATHS']=paths()

# ═══ S16 ΔG°–T
def gt():
    ax=Ax(80,300,420,250,600,60,ymin=-100); s=[]
    s.append(f'<rect x="{f(ax.X(0))}" y="{f(ax.Y(0))}" width="{f(ax.X(409.1)-ax.X(0))}" height="{f(ax.Y(-100)-ax.Y(0))}" fill="{FIELD}" fill-opacity=".15"/>')
    s.append(ax.frame([0,200,400,600],[-100,-50,0,50],T(500,362,mix='온도 $T$ [K]',size=23,anchor='end',fill=MUTED),T(88,26,mix='$\\Delta G^\\circ$ [kJ]',size=23,anchor='start',fill=MUTED),
                      yfmt=lambda v: ('-' if v<0 else '')+str(abs(v)),size=23))
    s.append(L(ax.X(0),ax.Y(0),ax.X(600),ax.Y(0),MUTED,1.8,dash='6 5'))
    s.append(draw(ax.curve(lambda t:-90+0.220*t,0,600,col=INK,w=3.2),dur='1.2'))
    s.append(pop(C(ax.X(298),ax.Y(-24.44),7,INK,2,INK),ax.X(298),ax.Y(-24.44),1.0)); s.append(T(ax.X(298)+12,ax.Y(-24.44)+30,mix='298 K, −24.4',size=23,anchor='start',halo=True))
    s.append(stp('t1',[C(ax.X(409.1),ax.Y(0),7,PLUS,2,'#FFFFFF'),T(ax.X(409.1)-8,ax.Y(0)-14,mix='409 K',size=23,fill=PLUS,anchor='end',halo=True)]))
    s.append(T(ax.X(150),ax.Y(-80),mix='자발적',size=23,fill=FIELD,weight=700))
    s.append(T(ax.X(595),ax.Y(-75),mix='$\\Delta G^\\circ=-90+0.220T$',size=23,anchor='end',halo=True))
    return svg((540,380),430,'메탄올 합성 반응의 표준 자유 에너지 변화는 온도에 따라 직선으로 커지고 409 K에서 0이 된다. 그보다 낮은 온도에서 자발적',s)
FIG['GT']=gt()

# ═══ S18 Pb–Ag 전지 (전자·이온 이동은 단계 공개)
def cell7():
    o=[cell(Lm='Pb',Rm='Ag',Ltex=r'\ce{Pb}',Rtex=r'\ce{Ag}',Lsol=r'\ce{Pb(NO3)2(aq)}',Rsol=r'\ce{AgNO3(aq)}',Lk='w',Rk='w',
            e='r',poles=False,br=True,ions=None,flow=False,elab=False,blab=True)]
    g=[f'<path d="M124 90 V50 H262 M298 50 H424 V90" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="36"/>',
       A(160,26,232,26,'minus',3),A(328,26,400,26,'minus',3),T(152,34,tex='e^-',size=21,fill=MINUS,anchor='end'),T(408,34,tex='e^-',size=21,fill=MINUS,anchor='start')]
    ab=chg(214,112,9,'-'); cb=chg(346,112,9,'+')
    g.append(an('move',ab,**{'from':'60,0','dur':'1.6','rep':'loop','ease':'lin'})); g.append(an('move',cb,**{'from':'-60,0','dur':'1.6','rep':'loop','ease':'lin','delay':'.8'}))
    g.append(T(280,170,mix='← $\\ce{NO3-}$',size=20,fill=MINUS,halo=True)+T(280,206,mix='$\\ce{K+}$ →',size=20,fill=PLUS,halo=True))
    g.append(T(135,326,mix='(−)극',size=21,weight=700)+T(135,353,mix='산화 전극',size=20,weight=700,fill=OX))
    g.append(T(425,326,mix='(+)극',size=21,weight=700)+T(425,353,mix='환원 전극',size=20,weight=700,fill=RD))
    o.append(step('c7',''.join(g)))
    return svg((560,370),520,'납 반쪽 전지와 은 반쪽 전지를 KNO3 염다리로 이은 전지: 전자는 납에서 은으로, 질산 이온은 납 쪽, 칼륨 이온은 은 쪽으로 이동',o)
FIG['CELL7']=cell7()

# ═══ S19 전지 표기 읽기
def note8():
    s=[T(160,60,tex='\\ce{Mg(s)}\\,|\\,\\ce{Mg^2+(aq)}',size=26),T(300,60,tex='\\|',size=28),T(440,60,tex='\\ce{Sc^3+(aq)}\\,|\\,\\ce{Sc(s)}',size=26)]
    s.append(draw(P([(60,84),(60,96),(260,96),(260,84)],OX,2.5),dur='.5')+T(160,124,mix='산화 반쪽 전지 (산화 전극)',size=19,fill=OX,weight=700))
    s.append(draw(P([(340,84),(340,96),(540,96),(540,84)],RD,2.5),dur='.5',delay='.4')+T(440,124,mix='환원 반쪽 전지 (환원 전극)',size=19,fill=RD,weight=700))
    s.append(T(300,22,mix='염다리',size=18,fill=MUTED))
    s.append(an('move',G([elec(240,160,True),A(262,160,330,160,'minus',3)]),**{'from':'-50,0','rep':'loop','dur':'1.8','ease':'lin'}))
    s.append(T(300,196,mix='전자: 왼쪽 → 오른쪽',size=18,fill=MINUS))
    return svg((600,210),560,'전지 표기에서 왼쪽은 산화 반쪽 전지, 겹세로줄은 염다리, 오른쪽은 환원 반쪽 전지이며 전자는 왼쪽에서 오른쪽으로 이동한다',s)
FIG['NOTE8']=note8()

# ═══ S20 전위 사다리
def ladder9():
    s=[]; Y=lambda E: 400-(E+0.3)*(360/1.8); X0=170
    s.append(A(X0,420,X0,22,'muted',2)); s.append(T(X0-10,26,mix='$E^\\circ$ [V]',size=20,anchor='end',fill=MUTED))
    items=[('\\ce{Cl2}/\\ce{Cl-}',1.36),('\\ce{Ag+}/\\ce{Ag}',0.80),('\\ce{Cu^2+}/\\ce{Cu}',0.34),('\\ce{H+}/\\ce{H2}',0.00),('\\ce{Pb^2+}/\\ce{Pb}',-0.13)]
    for t,E in items:
        y=Y(E); s.append(L(X0-8,y,X0+60,y,INK,2.5)); s.append(T(X0-14,y+7,mix=f'${t}$',size=20,anchor='end')); s.append(T(X0+66,y+7,mix=('%+.2f'%E).replace('+0.00','0.00'),size=20,anchor='start'))
    s.append(draw(A(280,Y(-0.13)-3,280,Y(1.36)+3,'field',3.5),delay='.3')); s.append(T(292,Y(1.12),mix='2) $+1.49$ V',size=21,anchor='start',fill=FIELD,weight=700,halo=True))
    s.append(T(292,Y(1.12)+26,mix='자발적',size=20,anchor='start',fill=FIELD))
    s.append(draw(A(440,Y(0.80)+3,440,Y(0.34)-3,'plus',3.5,d=True),delay='.8')); s.append(T(428,Y(0.62),mix='1) $-0.46$ V',size=21,anchor='end',fill=PLUS,weight=700,halo=True))
    s.append(T(428,Y(0.62)+26,mix='비자발적',size=20,anchor='end',fill=PLUS))
    s.append(T(280,Y(-0.13)+34,mix='화살표: 산화 전극 → 환원 전극',size=19,fill=MUTED))
    return svg((470,450),440,'표준 환원 전위 사다리: 납에서 염소로 가는 반응은 +1.49 V로 자발적, 은에서 구리 이온으로 가는 반응은 −0.46 V로 비자발적',s)
FIG['LAD9']=ladder9()

# ═══ S21 막대
def bar10():
    s=[]; Y0=230; k=4000
    s.append(A(60,Y0,360,Y0,'muted',2)+A(60,Y0,60,20,'muted',2)); s.append(T(70,26,mix='전지 전위 [V]',size=18,anchor='start',fill=MUTED))
    for v in (0.01,0.02,0.03,0.04): s.append(L(56,Y0-v*k,360,Y0-v*k,'#E2E7EC',1)+T(52,Y0-v*k+6,mix='%.2f'%v,size=17,anchor='end'))
    for i,(nm,v,col) in enumerate([('$E^\\circ_\\text{전지}$ (표준)',0.020,MUTED),('$E_\\text{전지}$ (처음)',0.0378,FIELD)]):
        x=140+150*i; b=R(x-36,Y0-v*k,72,v*k,INK,1.5,col)
        s.append(an('scale',b,**{'from':'1,0','o':f'{x},{Y0}','dur':'.8','delay':f'{0.4*i:.1f}'}))
        s.append(T(x,Y0-v*k-10,mix='%.3f V'%v,size=18,weight=700)+T(x,Y0+26,mix=nm,size=18))
    return svg((380,270),360,'표준 전지 전위 0.020 V보다 처음 전지 전위 0.038 V가 더 크다',s)
FIG['BAR10']=bar10()

# ═══ S22 고무 사슬
def rubber():
    s=[R(20,40,200,190,MUTED,1.5,'#FFFFFF',12,dash='5 4'),R(330,80,330,110,MUTED,1.5,'#FFFFFF',12,dash='5 4')]
    s.append(an('move',chains(22,42,196,186,4,seed=21),**{'from':'0,3','rep':'swing','dur':'.5','ease':'sine'}))
    s.append(an('move',chains(334,84,322,102,4,seed=22,stretched=True),**{'from':'-30,0','dur':'1.4','ease':'io'}))
    s.append(A(236,112,316,112,'ink',3.5)+T(276,100,mix='늘이기',size=19,weight=700))
    s.append(A(316,160,236,160,'field',3)+T(276,190,mix='놓으면 저절로',size=18,fill=FIELD))
    s.append(T(120,262,mix='엉킨 사슬 (교차 결합 ●)',size=18)+T(495,222,mix='나란히 펴진 사슬',size=18))
    s.append(stp('r1',[T(120,292,mix='따뜻해짐 ← 늘일 때 열 방출',size=18,fill=EQUI),T(495,252,mix='배열 가짓수 $W$ 감소',size=18,fill=MINUS)]))
    return svg((680,305),620,'교차 결합으로 묶인 엉킨 고무 사슬을 늘이면 나란히 펴지고, 놓으면 저절로 다시 엉킨다',s)
FIG['RUB']=rubber()

# ═══ S23 추 매단 고무줄 + 가열
def dryer():
    s=[L(100,30,100,360,INK,4),L(100,30,230,30,INK,4),R(50,360,150,12,INK,2,'#C9D2DB')]
    s.append(L(210,240,210,300,MUTED,1.5,dash='5 4')+R(185,300,50,40,MUTED,1.5,'none',4,dash='5 4')+T(243,330,mix='처음',size=20,fill=MUTED,anchor='start'))
    band=P([(204,32),(204,200),(216,200),(216,32)],RUB,3,close=True)
    s.append(an('scale',band,**{'from':'1,1.3','o':'210,32','dur':'1.6','delay':'.4','ease':'io'}))
    s.append(an('move',R(185,200,50,40,INK,2,'#8C99A6',4)+T(210,228,mix='추',size=20,fill='#FFFFFF',weight=700),**{'from':'0,50','dur':'1.6','delay':'.4','ease':'io'}))
    s.append(R(290,110,80,46,INK,2,'#F3D9B1',8)+R(362,125,32,16,INK,2,'#F3D9B1',3)+R(310,156,22,50,INK,2,'#F3D9B1',4))
    for i,yy in enumerate((112,133,154)):
        s.append(an('move',wave(282,yy,240,yy,EQUI,4,12,2.5),**{'from':'10,0','rep':'alt','dur':'.8','delay':f'{.2*i:.1f}','ease':'io'}))
    s.append(T(330,236,mix='가열',size=21,fill=EQUI,weight=700))
    s.append(A(262,300,262,250,'field',3)+T(272,282,mix='줄어듦',size=20,fill=FIELD,anchor='start'))
    return svg((400,380),360,'추를 매단 고무줄을 헤어드라이어로 가열하면 고무줄이 줄어 추가 올라간다',s)
FIG['DRYER']=dryer()

# ═══ S25 다니엘 전지
FIG['DAN']=svg((560,370),480,'아연과 구리 반쪽 전지를 염다리로 이은 다니엘 전지, 전압 1.10 V',[cell(ions=(r'\ce{NO3-}',r'\ce{K+}'),reading='1.10 V')])

# ═══ S26 금속 사다리
def ladder26():
    s=[]; Y=lambda E: 410-(E+2.6)*(380/3.6); X0=180
    s.append(A(X0,430,X0,20,'muted',2)); s.append(T(X0-10,24,mix='$E^\\circ$ [V]',size=20,anchor='end',fill=MUTED))
    for m,E in sorted(EP.items(),key=lambda t:-t[1]):
        y=Y(E); fl,st=MET[m]
        s.append(L(X0-8,y,X0+60,y,INK,2.5)+C(X0-30,y,11,st,1.5,fl)); s.append(T(X0-50,y+7,mix=f'$\\ce{{{m}}}$',size=21,anchor='end')); s.append(T(X0+66,y+7,mix=('%+.2f'%E),size=20,anchor='start'))
    s.append(draw(A(320,Y(-2.37)-3,320,Y(0.80)+3,'field',4),dur='1',delay='.3')); s.append(T(332,Y(-1.9),mix='$\\ce{Mg}$–$\\ce{Ag}$',size=21,anchor='start',fill=FIELD,weight=700,halo=True)+T(332,Y(-1.9)+28,mix='3.17 V',size=21,anchor='start',fill=FIELD,weight=700))
    s.append(draw(A(470,Y(-0.76)-3,470,Y(0.34)+3,'ink',3),dur='.6',delay='1')); s.append(T(505,Y(0.55),mix='$\\ce{Zn}$–$\\ce{Cu}$ 1.10 V',size=20,anchor='end',halo=True))
    return svg((520,440),470,'금속 여섯 가지의 표준 환원 전위 사다리: 가장 멀리 떨어진 마그네슘과 은의 조합이 3.17 V로 가장 크다',s)
FIG['LAD26']=ladder26()

def art():
    s=[circ([["wire",[[242,40],[120,40],[120,150]]],["bat",[250,40],{"dir":"h","pos":"right","signs":True}],["wire",[[258,40],[312,40]]],["bat",[320,40],{"dir":"h","pos":"right","signs":True}],["wire",[[328,40],[480,40],[480,236]]]])]
    s.append(T(285,84,mix='다니엘 전지 2개 직렬 (약 2.2 V)',size=20,fill=MUTED))
    s.append(P([(40,300),(150,232),(550,232),(440,300)],INK,2,fill=MET['Al'][0],close=True))
    s.append(P([(70,292),(162,240),(520,240),(428,292)],'#C9D3DD',1.5,fill='#FBFAF5',close=True))
    line=[(330,270),(290,258),(250,268),(210,256),(172,264)]
    s.append(draw(P(line,PHE,6,extra='stroke-linecap="round"'),dur='1.4',delay='.3'))
    s.append(L(120,150,163,250,'#4A4F57',16,extra='stroke-linecap="round"')+P([(157,246),(172,264),(171,240)],INK,1.5,fill='#4A4F57',close=True))
    s.append(T(132,130,mix='흑연 펜: (−)극',size=20,fill=RD,anchor='start'))
    s.append(T(330,222,mix='$\\ce{OH-}$ 생김 → 붉은 선',size=20,fill=PHE,anchor='start'))
    s.append(T(20,326,mix='$\\ce{Na2SO4}$ + 페놀프탈레인 종이',size=20,anchor='start',fill=MUTED))
    s.append(T(552,326,mix='포일 판: (+)극',size=20,anchor='end',fill=OX))
    return svg((560,340),520,'다니엘 전지 두 개를 직렬로 이어 흑연 펜을 (−)극, 알루미늄 포일 판을 (+)극에 연결하고, 황산 나트륨과 페놀프탈레인을 적신 종이 위에 펜으로 그리면 붉은 선이 생긴다',s)
FIG['ART']=art()

# ═══ 조립
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
assert (OUT+'slides.html').endswith('/3-M_대단원_Ⅲ_마무리/slides.html')
open(OUT+'slides.html','w',encoding='utf-8').write(out)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused)
