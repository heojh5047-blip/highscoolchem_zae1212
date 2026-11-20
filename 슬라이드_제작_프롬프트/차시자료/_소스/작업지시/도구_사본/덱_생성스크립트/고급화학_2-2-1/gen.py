# -*- coding: utf-8 -*-
"""고급화학 2-2-1(a/b) 그림 생성: tpl_a.html, tpl_b.html의 {{KEY}}를 SVG로 바꿔 각 덱 slides.html을 만든다.
   labs.js·extra.css도 이 폴더의 labs_src.js·extra_src.css를 두 덱에 복사한다.
   python3 -I gen.py   (출력 경로는 아래 OUT — 이 덱 두 폴더만, assert로 막음)"""
import math, random, re, sys, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
DECK='2-2-1_액체의_증기압_끓는점과_물의_특성'
OUT={'a':BASE+DECK+'a/','b':BASE+DECK+'b/'}
for k,v in OUT.items():
    assert v==BASE+'2-2-1_액체의_증기압_끓는점과_물의_특성'+k+'/', v
FIG={}
# 액체 색(덱 약속): 물 minus, 에탄올 field, 다이에틸 에터 equi
LIQ={'water':(8.07131,1730.63,233.426,MINUS,'물'),'ethanol':(8.20417,1642.89,230.300,FIELD,'에탄올'),'ether':(6.92032,1064.07,228.80,EQUI,'다이에틸 에터')}
def pv(l,t):  # mmHg
    A,B,Cc=LIQ[l][:3]; return 10**(A-B/(Cc+t))
def kpa(l,t): return pv(l,t)*0.133322
def wat(x,y,ang=0,rO=16,rH=11,d=None,lab=False,extra_h=None):
    """물 분자: 굽은형 104.5°. ang = O→H 이등분선 방향(도). 결합 막대 뒤 원자."""
    d=d or rO*1.15; s=[]; hs=[]
    for sg in (-1,1):
        a=math.radians(ang+sg*52.25); hs.append((x+d*math.cos(a),y+d*math.sin(a)))
    for hx,hy in hs: s.append(L(x,y,hx,hy,'#9AA5B1',max(4,rO*.32),extra='stroke-linecap="round"'))
    s.append(f'<g data-atom="{f(x)},{f(y)},{rO},O{"" if lab else ",-"}"></g>')
    for hx,hy in hs: s.append(f'<g data-atom="{f(hx)},{f(hy)},{rH},H{"" if lab else ",-"}"></g>')
    return ''.join(s),hs
def hb(x1,y1,x2,y2,w=2.5): return L(x1,y1,x2,y2,MUTED,w,'5 5')
def legend_OH(x,y,rO=10,rH=7,size=18):
    return f'<g data-atom="{x},{y},{rO},O,-"></g>'+T(x+16,y+6,mix='O',size=size,anchor='start')+f'<g data-atom="{x+50},{y},{rH},H,-"></g>'+T(x+62,y+6,mix='H',size=size,anchor='start')

# ═════════ a ═════════
def cover_a():
    rnd=random.Random(5); s=[R(40,20,380,262,INK,3,'#FFFFFF',10)]
    s.append(R(42,186,376,94,'none',0,WATER))
    s.append(L(42,186,418,186,WATER_S,2))
    for row,yy in enumerate((206,228,250,270)):
        for i in range(16):
            xx=58+i*23.3+(11 if row%2 else 0)+rnd.uniform(-2,2)
            if xx>405: continue
            s.append(gm(xx,yy+rnd.uniform(-2,2),9.5))
    s.append(mol_box(46,26,368,150,8,11,r=9.5,arrow=20))
    s.append(f'<g data-anim="move" data-from="0,40" data-rep="loop" data-dur="1.8">'+A(150,176,150,140,'ink',2.5)+gm(150,186,9.5)+'</g>')
    s.append(f'<g data-anim="move" data-from="0,-40" data-rep="loop" data-dur="1.8" data-delay=".9">'+A(310,150,310,180,'ink',2.5)+gm(310,140,9.5)+'</g>')
    ax=Ax(80,470,330,140,100,800)
    s.append(L(80,470,420,470,MUTED,2)); s.append(L(80,470,80,320,MUTED,2))
    s.append(L(80,ax.Y(760),410,ax.Y(760),MUTED,1.5,'5 4'))
    for k,lab,xx in (('ether','',0),('ethanol','',0),('water','',0)):
        col=LIQ[k][3]
        tm=min(100,next((t/2 for t in range(0,201) if pv(k,t/2)>790),100))
        s.append(f'<g data-anim="draw" data-dur="1.4">'+ax.curve(lambda t:pv(k,t),0,tm,col=col,w=3.5)+'</g>')
    s.append(T(415,494,mix='온도',size=19,anchor='end',fill=MUTED)); s.append(T(90,316,mix='증기압',size=19,anchor='start',fill=MUTED))
    s=['<g transform="translate(0,30)">']+s+['</g>']
    return svg((460,530),430,'닫힌 용기 속 액체와 증기의 동적 평형, 세 액체의 증기압 곡선',s,'fig cover-fig')
FIG['COVER_A']=cover_a()

def leaf():
    s=[f'<path d="M30 230 Q170 70 430 120 Q300 260 30 230 Z" fill="#7CC38F" stroke="#2E7D4F" stroke-width="2.5"/>',
       f'<path d="M40 226 Q220 160 420 124" fill="none" stroke="#2E7D4F" stroke-width="2"/>']
    for (x,y,r) in ((170,150,30),(280,152,22),(350,138,14)):
        s.append(f'<g data-anim="pop" data-o="{x},{y+r}" data-delay="{f((r-14)/40)}"><ellipse cx="{x}" cy="{y}" rx="{r}" ry="{f(r*.9)}" fill="#E8F4FC" stroke="#5B8DB8" stroke-width="2" fill-opacity=".85"/><ellipse cx="{f(x-r*.35)}" cy="{f(y-r*.4)}" rx="{f(r*.22)}" ry="{f(r*.14)}" fill="#FFFFFF"/></g>')
    s.append(T(170,98,mix='거의 공 모양인 물방울',size=19,fill=MUTED))
    return svg((460,260),400,'매끈한 잎에 맺힌 공 모양의 물방울',s)
FIG['LEAF']=leaf()

def phases():
    rnd=random.Random(3); s=[]
    xs=(20,250,480); labs=('기체','액체','고체')
    for j,(x0,lab) in enumerate(zip(xs,labs)):
        s.append(R(x0,20,200,170,INK,2.5,'#FFFFFF',6)); s.append(T(x0+100,220,mix=lab,size=21,weight=700))
        if j==0:
            s.append(mol_box(x0,20,200,170,6,4,r=10,arrow=16))
        elif j==1:
            pts=[]
            for row in range(4):
                for i in range(8):
                    pts.append((x0+18+i*23.5+(10 if row%2 else 0)+rnd.uniform(-3,3),186-12-row*21+rnd.uniform(-2,2)))
            pts=[p for p in pts if p[0]<x0+190]
            for k,(px,py) in enumerate(pts):
                s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-4,4))},{f(rnd.uniform(-3,3))}" data-rep="alt" data-dur="{f(.8+rnd.random()*.6)}">'+gm(px,py,10)+'</g>' if k%3==0 else gm(px,py,10))
        else:
            for row in range(7):
                for i in range(8):
                    s.append(gm(x0+16+i*24,186-12-row*22.5,10))
    s.append(T(120,250,mix='인력 ≪ 운동 에너지',size=19,fill=MUTED)); s.append(T(350,250,mix='인력 ≈ 운동 에너지||자리를 바꾸며 흐름',size=19,fill=MUTED)); s.append(T(580,250,mix='인력 ≫ 운동 에너지||제자리에서 진동',size=19,fill=MUTED))
    return svg((700,300),700,'기체·액체·고체의 분자 배열 비교',s)
FIG['PHASES']=phases()

def bp_bar():
    s=[]; ax=Ax(90,300,330,250,1,120,ymin=-180)
    s.append(L(90,ax.Y(0),440,ax.Y(0),MUTED,2)); s.append(L(90,300,90,30,MUTED,2))
    for v in (-150,-100,-50,0,50,100):
        s.append(L(84,ax.Y(v),90,ax.Y(v),MUTED,1.5)); s.append(T(80,ax.Y(v)+6,tex=str(v).replace('-','-'),size=18,anchor='end'))
    for x,v,lab,col in ((170,-162,'\\ce{CH4}',GRAV),(340,100,'\\ce{H2O}',MINUS)):
        y0,y1=ax.Y(0),ax.Y(v)
        s.append(f'<g data-anim="scale" data-from="1,0" data-o="{x},{f(y0)}" data-dur="1.1">'+R(x-40,min(y0,y1),80,abs(y1-y0),col,2,col,extra='fill-opacity=".55"')+'</g>')
        s.append(T(x,(y1-12 if v>0 else y1+28),tex=f'{v}\\ {{}}^\\circ\\text{{C}}',size=20,weight=700))
        s.append(T(x,(ax.Y(0)+28 if v>0 else ax.Y(0)-14),tex=lab,size=22))
    s.append(T(170,ax.Y(0)-40,mix='분자량 16',size=18,fill=MUTED)); s.append(T(340,ax.Y(0)+54,mix='분자량 18',size=18,fill=MUTED))
    s.append(T(16,20,mix='끓는점 (°C)',size=18,fill=MUTED,anchor='start'))
    return svg((460,320),420,'메테인과 물의 끓는점 비교 막대그래프',s)
FIG['BPBAR']=bp_bar()

def ion_dip():
    s=[]
    for cx,cy,ion in ((150,150,'Na'),(450,150,'Cl')):
        for k in range(6):
            a=k*60+30; rr=78 if ion=='Na' else 88
            x,y=cx+rr*math.cos(math.radians(a)),cy+rr*math.sin(math.radians(a))
            ang=a if ion=='Na' else a+180   # Na+: O가 이온 쪽(H가 바깥) / Cl-: H가 이온 쪽
            body,_=wat(x,y,ang,15,10)
            s.append(body)
        if ion=='Na': s.append(f'<g data-anim="pop" data-o="{cx},{cy}"><g data-atom="{cx},{cy},26,Na,\\mathrm{{Na}}^{{+}}"></g></g>')
        else: s.append(f'<g data-anim="pop" data-o="{cx},{cy}" data-delay=".3"><g data-atom="{cx},{cy},34,Cl,\\mathrm{{Cl}}^{{-}}"></g></g>')
    s.append(T(150,272,mix='O(δ−) 쪽이 양이온을 향함',size=19,fill=MUTED)); s.append(T(450,272,mix='H(δ+) 쪽이 음이온을 향함',size=19,fill=MUTED))
    s.append(legend_OH(230,24))
    return svg((600,290),560,'물 분자가 나트륨 이온과 염화 이온을 둘러싼 수화',s)
FIG['IONDIP']=ion_dip()

def hcl_row():
    s=[]
    def hcl(x,y,flip=False,delay=0):
        hx,cx=(x-22,x+20) if not flip else (x+22,x-20)
        b=L(hx,y,cx,y,'#9AA5B1',7,extra='stroke-linecap="round"')+f'<g data-atom="{f(cx)},{y},29,Cl"></g><g data-atom="{f(hx)},{y},18,H"></g>'
        b+=T(hx,y-26,tex='\\delta^+',size=20,fill=PLUS)+T(cx,y-36,tex='\\delta^-',size=20,fill=MINUS)
        return b
    pos=[(80,70),(220,70),(360,70),(150,170),(290,170),(430,170)]
    for i,(x,y) in enumerate(pos): s.append(hcl(x,y))
    for (x1,x2,y) in ((100,180,70),(240,320,70),(170,250,170),(310,390,170)):
        s.append(hb(x1+28,y,x2-26,y,2))
    s.append(T(250,232,mix='δ+ 와 δ− 가 마주 보도록 늘어서 서로 끌어당긴다(점선)',size=19,fill=MUTED))
    return svg((520,250),500,'염화 수소 분자들의 쌍극자–쌍극자 상호 작용',s)
FIG['HCL']=hcl_row()

def disp():
    s=[]
    def cloud(x,y,shift,lab=True,cid=''):
        o=f'<ellipse cx="{f(x+shift)}" cy="{y}" rx="62" ry="40" fill="#CFE3F7" stroke="{MINUS}" stroke-width="2" fill-opacity=".8"/>'
        o+=L(x-20,y,x+20,y,'#9AA5B1',6,extra='stroke-linecap="round"')+C(x-20,y,7,INK,1.5,'#FFFFFF')+C(x+20,y,7,INK,1.5,'#FFFFFF')
        return o
    s.append(cloud(80,90,0)+cloud(220,90,0)); s.append(T(150,160,mix='① 평균적으로 고른 전자 구름||(무극성)',size=19,fill=MUTED))
    s.append(A(290,90,330,90,'ink',3))
    s.append(f'<g data-anim="move" data-from="10,0" data-rep="alt" data-dur="1.2">'+cloud(410,90,-14)+'</g>')
    s.append(T(360,52,tex='\\delta^-',size=21,fill=MINUS)); s.append(T(462,52,tex='\\delta^+',size=21,fill=PLUS))
    s.append(f'<g data-anim="move" data-from="10,0" data-rep="alt" data-dur="1.2" data-delay=".25">'+cloud(560,90,-14)+'</g>')
    s.append(T(510,52,tex='\\delta^-',size=21,fill=MINUS)); s.append(T(612,52,tex='\\delta^+',size=21,fill=PLUS))
    s.append(T(410,160,mix='② 순간 쌍극자',size=19,fill=MUTED)); s.append(T(560,160,mix='③ 이웃 분자에||유도된 쌍극자',size=19,fill=MUTED))
    s.append(hb(468,90,500,90,2))
    return svg((660,210),600,'무극성 분자의 편극: 순간 쌍극자가 이웃 분자에 쌍극자를 유도함',s)
FIG['DISP']=disp()

def halo_bp():
    s=[]; ax=Ax(80,250,360,210,1,200,ymin=-200)
    s.append(L(80,ax.Y(0),450,ax.Y(0),MUTED,2)); s.append(L(80,250,80,24,MUTED,2))
    for v in (-200,-100,0,100,200):
        s.append(L(74,ax.Y(v),80,ax.Y(v),MUTED,1.5)); s.append(T(70,ax.Y(v)+6,tex=str(v),size=18,anchor='end'))
    data=(('F2',38,-188),('Cl2',71,-34),('Br2',160,59),('I2',254,184))
    for i,(fm,M,bp) in enumerate(data):
        x=140+i*88; y0,y1=ax.Y(0),ax.Y(bp)
        s.append(f'<g data-anim="scale" data-from="1,0" data-o="{x},{f(y0)}" data-delay="{f(i*.2)}">'+R(x-26,min(y0,y1),52,abs(y1-y0),BF,2,BF,extra='fill-opacity=".45"')+'</g>')
        s.append(T(x,(y1-10 if bp>0 else y1+24),tex=f'{bp}',size=19,weight=700))
        s.append(T(x,(y0+26 if bp>0 else y0-12),tex=f'\\ce{{{fm}}}',size=20))
    s.append(T(10,22,mix='끓는점 (°C)',size=18,fill=MUTED,anchor='start'))
    s.append(A(130,276,420,276,'muted',2)); s.append(T(275,300,mix='분자량·편극도 증가',size=19,fill=MUTED))
    return svg((460,310),440,'할로젠 분자의 끓는점: 분자량이 클수록 높다',s)
FIG['HALO']=halo_bp()

def evap():
    s=[R(20,60,420,190,'none',0,WATER),L(20,60,440,60,WATER_S,2)]
    s.append(T(30,48,mix='표면',size=19,fill=MUTED,anchor='start'))
    pts={}
    for r in range(4):
        for i in range(9):
            x=50+i*45+(22 if r%2 else 0); y=80+r*44
            if x>420: continue
            pts[(r,i)]=(x,y)
    for (r,i),(x,y) in pts.items():
        s.append(gm(x,y,11))
    # 표면 분자 (0,2) / 내부 분자 (2,4)
    sx,sy=pts[(0,2)]; ix,iy=pts[(2,4)]
    s.append(C(sx,sy,15,PLUS,2.5)); s.append(C(ix,iy,15,FIELD,2.5))
    for a in (0,180,60,120):
        s.append(A(sx+16*math.cos(math.radians(a)),sy+16*math.sin(math.radians(a)),sx+34*math.cos(math.radians(a)),sy+34*math.sin(math.radians(a)),'plus',2))
    for a in range(0,360,60):
        s.append(A(ix+16*math.cos(math.radians(a)),iy+16*math.sin(math.radians(a)),ix+34*math.cos(math.radians(a)),iy+34*math.sin(math.radians(a)),'field',2))
    s.append(f'<g data-anim="move" data-from="0,40" data-dur="1.4" data-rep="loop">'+A(320,10+18,320,-0+6,'ink',2.5)+gm(320,36,11)+'</g>')
    s.append(T(360,34,mix='운동 에너지가 큰||표면 분자가 떠남',size=18,fill=INK,anchor='start'))
    s.append(T(110,274,mix='표면: 위쪽 인력 없음',size=19,fill=PLUS)); s.append(T(350,274,mix='내부: 모든 방향으로 당김',size=19,fill=FIELD))
    return svg((500,290),480,'액체 내부와 표면 분자의 상호 작용과 증발',s)
FIG['EVAP']=evap()

def kedist():
    s=[]; ax=Ax(60,240,400,200,6,0.9)
    fE=lambda E,kT:2*math.sqrt(E/math.pi)*kT**-1.5*math.exp(-E/kT)
    s.append(L(60,240,470,240,MUTED,2)); s.append(L(60,240,60,30,MUTED,2))
    Ec=3.2
    pts=[(ax.X(Ec),ax.Y(0))]+[(ax.X(Ec+i*(6-Ec)/60),ax.Y(fE(Ec+i*(6-Ec)/60,1.25))) for i in range(61)]+[(ax.X(6),ax.Y(0))]
    s.append(P(pts,'none',0,'#FFE45C',extra='fill-opacity=".45"',close=True))
    s.append(f'<g data-anim="draw" data-dur="1.2">'+ax.curve(lambda E:fE(E,0.8),0.001,6,col=MINUS,w=3.5)+'</g>')
    s.append(f'<g data-anim="draw" data-dur="1.2" data-delay=".5">'+ax.curve(lambda E:fE(E,1.25),0.001,6,col=PLUS,w=3.5)+'</g>')
    s.append(L(ax.X(Ec),240,ax.X(Ec),40,EQUI,2.5,'6 4'))
    s.append(T(ax.X(Ec)+8,56,mix='표면을 떠날 수 있는 에너지',size=18,fill=EQUI,anchor='start'))
    s.append(T(ax.X(.55)+6,ax.Y(fE(.4,.8))-6,tex='T_1',size=21,fill=MINUS,anchor='start'))
    s.append(T(ax.X(2.2),ax.Y(fE(2.2,1.25))-12,tex='T_2',size=21,fill=PLUS,anchor='start'))
    s.append(T(470,268,mix='분자의 운동 에너지',size=19,anchor='end',fill=MUTED)); s.append(T(70,24,mix='분자 수의 비율',size=19,anchor='start',fill=MUTED))
    s.append(T(400,200,mix='$T_1&lt;T_2$',size=19,fill=MUTED))
    return svg((490,280),470,'액체 분자의 운동 에너지 분포와 증발할 수 있는 분자의 비율(T1 < T2)',s)
FIG['KEDIST']=kedist()

def eq_stage(k):
    rnd=random.Random(20+k); s=[R(10,10,180,190,INK,2.5,'#FFFFFF',6),R(12,140,176,58,'none',0,WATER),L(12,140,188,140,WATER_S,2)]
    for i in range(7):
        for r in range(2):
            s.append(gm(26+i*24+(12 if r else 0),156+r*22,8.5)) if 26+i*24+(12 if r else 0)<182 else None
    nv=(1,5,9)[k]
    pts=[]
    while len(pts)<nv:
        p=(rnd.uniform(28,172),rnd.uniform(28,118))
        if all(math.hypot(p[0]-a,p[1]-b)>26 for a,b in pts): pts.append(p)
    for p in pts: s.append(gm(p[0],p[1],8.5))
    up=(4,4,4)[k]; dn=(0,2,4)[k]
    s.append(A(70,136,70,136-14-6*up,'field',3)); s.append(T(56,104,mix='증발',size=18,fill=FIELD,anchor='end') if k==0 else '')
    if dn: s.append(A(130,136-14-6*dn,130,136,'bfield',3))
    return svg((200,210),190,['처음: 증발만 일어남','응축이 시작됨','증발 속도 = 응축 속도'][k],s)
for k in range(3): FIG[f'EQ{k+1}']=eq_stage(k)

def three_cont():
    s=[]
    for j,(x,w,h) in enumerate(((20,120,50),(190,120,110),(350,220,40))):
        s.append(R(x,60,w,140,INK,2.5,'#FFFFFF',6)); s.append(R(x+2,198-h,w-4,h,'none',0,WATER)); s.append(L(x+2,198-h,x+w-2,198-h,WATER_S,2))
        gx=x+w/2; s.append(L(gx,60,gx,44,INK,2.5)); s.append(C(gx,30,15,INK,2,'#FFFFFF'))
        s.append(f'<g data-anim="move" data-from="0,0" data-dur="1"><line x1="{f(gx)}" y1="30" x2="{f(gx+9)}" y2="20" stroke="{PLUS}" stroke-width="2.5" data-anim="spin"/></g>' if False else L(gx,30,gx+9,21,PLUS,2.5))
    labs=('물 조금','물 많이','표면적 넓게')
    for (x,w),lab in zip(((20,120),(190,120),(350,220)),labs):
        s.append(T(x+w/2,226,mix=lab,size=19,fill=MUTED))
        s.append(T(x+w/2,110,mix='$P=\\ ?$',size=20))
    s.append(T(300,256,mix='세 용기 모두 25 °C, 닫힌 용기, 충분한 시간 뒤',size=19,fill=MUTED))
    return svg((590,270),560,'온도가 같고 액체의 양과 표면적이 다른 세 닫힌 용기',s)
FIG['THREE']=three_cont()

def vp_curves(w=540,lab=True):
    s=[]; ax=Ax(80,330,420,290,100,900)
    s.append(ax.frame([0,20,40,60,80,100],[0,200,400,600,800],L(0,0,0,0),'',size=18))
    s.append(T(500,384,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)); s.append(T(20,24,mix='증기압 $P_\\text{vap}$ (mmHg)',size=19,anchor='start',fill=MUTED))
    s.append(L(80,ax.Y(760),500,ax.Y(760),MUTED,1.5,'6 4')); s.append(T(88,ax.Y(760)+24,mix='760 mmHg',size=18,anchor='start',fill=MUTED))
    for i,(k,bp,lx) in enumerate((('ether',34.6,0),('ethanol',78.4,0),('water',100.0,0))):
        col=LIQ[k][3]; tmax=min(100,bp+8) if k!='water' else 100
        tt=0
        while pv(k,tt)<900 and tt<100: tt+=.5
        s.append(f'<g data-anim="draw" data-dur="1.2" data-delay="{f(i*.3)}">'+ax.curve(lambda t:pv(k,t),0,min(tt,100),col=col,w=3.5)+'</g>')
        s.append(C(ax.X(bp),ax.Y(760),5,col,2,col))
        s.append(T(ax.X(bp)-(6 if k!='water' else 6),ax.Y(760)-12,tex=f'{bp}\\ {{}}^\\circ\\text{{C}}',size=18,fill=col,anchor='end',halo=True))
    s.append(T(ax.X(28),ax.Y(600),mix='다이에틸||에터',size=19,fill=EQUI,anchor='start',halo=True))
    s.append(T(ax.X(60),ax.Y(420),mix='에탄올',size=19,fill=FIELD,anchor='end',halo=True))
    s.append(T(ax.X(88),ax.Y(250),mix='물',size=19,fill=MINUS,anchor='start',halo=True))
    return svg((520,400),w,'다이에틸 에터, 에탄올, 물의 온도에 따른 증기압 곡선',s)
FIG['VPC']=vp_curves()

def lnp():
    s=[]; ax=Ax(80,320,400,280,3.6,7.5,xmin=2.6,ymin=1.5)
    s.append(ax.frame([2.6,2.8,3.0,3.2,3.4,3.6],[2,3,4,5,6,7],L(0,0,0,0),'',xfmt=lambda v:f'{v:.1f}',size=18))
    s.append(T(480,378,mix='$1/T$ ($10^{-3}\\ \\text{K}^{-1}$)',size=19,anchor='end',fill=MUTED)); s.append(T(20,22,mix='$\\ln P_\\text{vap}$ ($P$: mmHg)',size=19,anchor='start',fill=MUTED))
    for i,k in enumerate(('ether','ethanol','water')):
        col=LIQ[k][3]
        fn=lambda x,k=k:math.log(pv(k,1000/x-273.15))
        x0=next((2.68+j*0.005 for j in range(200) if fn(2.68+j*0.005)<7.4),2.68)
        s.append(f'<g data-anim="draw" data-dur="1.2" data-delay="{f(i*.3)}">'+ax.curve(fn,x0,3.6,col=col,w=3.5)+'</g>')
    s.append(T(ax.X(3.42),ax.Y(6.55),mix='다이에틸 에터',size=19,fill=EQUI,anchor='start',halo=True))
    s.append(T(ax.X(3.05),ax.Y(3.65),mix='에탄올',size=19,fill=FIELD,anchor='end',halo=True))
    s.append(T(ax.X(3.33),ax.Y(2.55),mix='물',size=19,fill=MINUS,anchor='end',halo=True))
    s.append(T(ax.X(2.65),ax.Y(1.95),mix='기울기 $=-\\dfrac{\\Delta H^\\circ_\\text{vap}}{R}$',size=19,anchor='start'))
    return svg((520,390),500,'세 액체의 ln P와 1/T의 직선 관계',s)
FIG['LNP']=lnp()

def syringe(x,y,stage,s):
    # 주사기(가로): 몸통 x..x+150, 높이 36
    s.append(R(x,y,150,36,GLASS,2.2,'#FFFFFF',3))
    for i in range(1,6): s.append(L(x+i*25,y,x+i*25,y+9,MUTED,1.2))
    if stage==0:
        s.append(R(x+2,y+2,60,32,'none',0,WATER)); s.append(R(x+62,y-2,10,40,INK,1.5,'#C9D2DB')); s.append(L(x+72,y+18,x+150+30,y+18,INK,4)); s.append(R(x+176,y+4,10,28,INK,1.5,'#C9D2DB'))
        s.append(L(x-16,y+18,x,y+18,GLASS,4))
    else:
        s.append(R(x+2,y+2,40,32,'none',0,WATER)); s.append(R(x+130,y-2,10,40,INK,1.5,'#C9D2DB')); s.append(L(x+140,y+18,x+190,y+18,INK,4)); s.append(R(x+186,y+4,10,28,INK,1.5,'#C9D2DB'))
        s.append(R(x-12,y+10,12,16,INK,1.5,INK))
        if stage==2:
            rnd=random.Random(9)
            for i in range(6): s.append(C(x+50+rnd.uniform(0,72),y+6+rnd.uniform(0,24),3.6,GAS_S,1,GAS))
def syr_steps():
    s=[]
    for j in range(3):
        x0=30+j*240
        syringe(x0,60,j,s)
    s.append(T(110,136,mix='① 기포 없이||물을 조금 채운다',size=19,fill=MUTED)); s.append(T(345,136,mix='② 입구를 막고||피스톤을 당긴다',size=19,fill=MUTED)); s.append(T(590,136,mix='③ 빈 공간이 수증기로 채워져||동적 평형 → 압력 = 증기압',size=19,fill=MUTED))
    s.append(T(345,40,mix='진공 공간',size=18,fill=MUTED)); s.append(T(80,40,mix='물',size=18,fill=MINUS))
    return svg((740,190),740,'주사기로 물의 증기압을 만드는 세 단계',s)
FIG['SYR']=syr_steps()

def vp_res():
    s=[]; ax=Ax(70,290,380,240,90,50,xmin=10)
    s.append(ax.frame([10,30,50,70,90],[0,10,20,30,40,50],L(0,0,0,0),'',size=18))
    s.append(T(460,342,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)); s.append(T(16,22,mix='증기압 (kPa)',size=19,anchor='start',fill=MUTED))
    s.append(f'<g data-anim="draw" data-dur="1.4">'+ax.curve(lambda t:kpa('water',t),10,82,col=MINUS,w=3)+'</g>')
    for i,(t,p) in enumerate(EXV):
        s.append(f'<g data-anim="pop" data-o="{f(ax.X(t))},{f(ax.Y(p))}" data-delay="{f(.15*i)}">'+C(ax.X(t),ax.Y(p),6,INK,2,'#FFFFFF')+'</g>')
    return svg((480,350),460,'측정한 물의 증기압 곡선(예시 값)',s)
EXV=[(20,2.3),(30,4.2),(40,7.4),(50,12.3),(60,19.9),(70,31.1),(80,47.3)]
FIG['VPRES']=vp_res()

def boil():
    rnd=random.Random(4); s=[]
    s.append(f'<path d="M120 40 L120 250 Q120 266 136 266 L344 266 Q360 266 360 250 L360 40" fill="none" stroke="{GLASS}" stroke-width="3"/>')
    s.append(f'<path d="M122 80 L358 80 L358 250 Q358 264 344 264 L136 264 Q122 264 122 250 Z" fill="{WATER}"/>')
    s.append(L(122,80,358,80,WATER_S,2))
    s.append(R(150,272,180,16,INK,2,'#E9ECEF',3))
    for i in range(5): s.append(f'<path d="M{170+i*36} 296 q6 -6 0 -12 q-6 -6 0 -12" fill="none" stroke="{OX}" stroke-width="2.5"/>' if False else '')
    for i in range(6): s.append(f'<path d="M{165+i*30} 304 l8 -10 l8 10 z" fill="#F28C28" stroke="{OX}" stroke-width="1.5"/>')
    for k,(bx,by,br) in enumerate(((180,230,16),(250,190,20),(300,240,13),(210,140,22),(290,120,15))):
        inner=C(bx,by,br,'#7FA8C9',2,'#FFFFFF')
        for j in range(2 if br<18 else 3): inner+=C(bx+rnd.uniform(-br*.45,br*.45),by+rnd.uniform(-br*.45,br*.45),3.2,GAS_S,1,GAS)
        s.append(f'<g data-anim="move" data-from="0,{f(90-k*10)}" data-rep="loop" data-dur="{f(1.6+k*.2)}" data-delay="{f(k*.35)}">'+inner+'</g>')
    s.append(A(380,180,312,128,'ink',2)); s.append(T(386,186,mix='기포 속은||수증기($\\ce{H2O}$ 분자)',size=19,anchor='start'))
    s.append(A(100,40,100,72,'ink',3)); s.append(T(100,30,mix='외부 압력',size=19))
    s.append(T(240,326,mix='증기압 = 외부 압력 → 내부에서도 기화',size=19,fill=MUTED))
    return svg((560,340),520,'끓음: 액체 내부에서 수증기 기포가 생김',s)
FIG['BOIL']=boil()

def pext():
    s=[]; ax=Ax(80,300,420,260,130,220,xmin=60)
    s.append(ax.frame([60,70,80,90,100,110,120,130],[0,50,100,150,200],L(0,0,0,0),'',size=18))
    s.append(T(500,354,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)); s.append(T(20,22,mix='증기압 (kPa)',size=19,anchor='start',fill=MUTED))
    s.append(f'<g data-anim="draw" data-dur="1.3">'+ax.curve(lambda t:kpa('water',t),60,124,col=MINUS,w=3.5)+'</g>')
    for i,(Pk,bp,lab,col) in enumerate(((70,90.0,'높은 산',BF),(101.325,100.0,'1 atm',INK),(200,120.1,'압력솥',PLUS))):
        y=ax.Y(Pk)
        s.append(f'<g class="step" data-g="pe{i}">'+L(80,y,ax.X(bp),y,col,2,'6 4')+L(ax.X(bp),y,ax.X(bp),300,col,2,'6 4')+C(ax.X(bp),y,6,col,2,col)+T(ax.X(bp)-10,y-10,mix=f'{lab} → {bp:.0f} °C',size=19,fill=col,anchor='end',halo=True)+'</g>')
    return svg((520,362),500,'외부 압력에 따른 물의 끓는점',s)
FIG['PEXT']=pext()

def fig11():
    s=[]; ax=Ax(80,290,380,250,120,160,xmin=80,ymin=10)
    s.append(ax.frame([80,90,100,110,120],[10,60,110,160],L(0,0,0,0),'',size=18))
    s.append(T(460,344,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)); s.append(T(20,22,mix='증기압 (kPa)',size=19,anchor='start',fill=MUTED))
    s.append(f'<g data-anim="draw" data-dur="1.2">'+ax.curve(lambda t:kpa('water',t),80,113,col=MINUS,w=3.5)+'</g>')
    y=ax.Y(101.325)
    s.append(L(80,y,460,y,INK,2,'6 4')); s.append(T(90,y-10,mix='101.325 kPa (= 1 atm = 760 mmHg)',size=18,anchor='start',halo=True))
    s.append(f'<g class="step" data-g="f11">'+L(ax.X(100),y,ax.X(100),290,PLUS,2.5,'6 4')+C(ax.X(100),y,6,PLUS,2,PLUS)+T(ax.X(100)+10,270,mix='100 °C',size=20,fill=PLUS,anchor='start',weight=700)+'</g>')
    return svg((480,352),460,'물의 증기압 곡선과 기준 끓는점',s)
FIG['FIG11']=fig11()

def surf():
    s=[R(20,70,400,190,'none',0,WATER),L(20,70,420,70,WATER_S,2.5)]
    for r in range(4):
        for i in range(8):
            x=55+i*48+(24 if r%2 else 0); y=90+r*46
            if x<410: s.append(gm(x,y,11))
    sx,sy=151,90; ix,iy=223,182
    s.append(C(sx,sy,15,PLUS,2.5)); s.append(C(ix,iy,15,FIELD,2.5))
    for a in (0,180,45,135,90):
        s.append(A(sx+15*math.cos(math.radians(a)),sy+15*math.sin(math.radians(a)),sx+38*math.cos(math.radians(a)),sy+38*math.sin(math.radians(a)),'plus',2))
    for a in range(0,360,45):
        s.append(A(ix+15*math.cos(math.radians(a)),iy+15*math.sin(math.radians(a)),ix+38*math.cos(math.radians(a)),iy+38*math.sin(math.radians(a)),'field',2))
    s.append(f'<g data-anim="move" data-from="0,-14" data-rep="alt" data-dur="1">'+A(sx-70,40,sx-70,92,'ink',4)+'</g>')
    s.append(T(sx-80,30,mix='알짜 인력(안쪽)',size=19,anchor='start'))
    s.append(T(300,40,mix='표면: 위로 당기는 분자 없음',size=19,fill=PLUS,anchor='start'))
    s.append(T(ix,282,mix='내부: 사방으로 당겨져 알짜 힘 0',size=19,fill=FIELD))
    return svg((560,300),520,'표면 장력의 원인: 표면 분자에 작용하는 안쪽 알짜 인력',s)
FIG['SURF']=surf()

def clip():
    s=[R(20,100,460,120,'none',0,WATER)]
    s.append(f'<path d="M20 100 L180 100 Q250 128 320 100 L480 100" fill="none" stroke="{WATER_S}" stroke-width="2.5"/>')
    s.append(f'<path d="M180 100 L480 100 L480 220 L20 220 L20 100 Z" fill="none"/>')
    s.append(f'<g data-anim="move" data-from="0,-30" data-dur="1.2">'+f'<path d="M190 108 L310 108 Q322 108 322 100 Q322 92 310 92 L206 92 Q198 92 198 98 Q198 104 206 104 L300 104" fill="none" stroke="{GRAV}" stroke-width="4" stroke-linejoin="round"/>'+'</g>')
    for x in (214,286): s.append(A(x,128,x-34*(1 if x<250 else -1)+0,104,'ink',2))
    s.append(T(250,60,mix='클립(밀도 > 물)이 떠 있음',size=20)); s.append(T(250,180,mix='표면이 조금 늘어나려 하면||표면 장력이 되돌림',size=19,fill=MUTED))
    return svg((500,230),460,'표면 장력으로 물 위에 뜬 클립',s)
FIG['CLIP']=clip()

def menis():
    s=[]
    s.append(R(20,180,330,60,'none',0,WATER)); s.append(L(20,180,350,180,WATER_S,2))
    for i,(x,r,h) in enumerate(((70,14,70),(160,9,110),(250,5,150))):
        top=180-h
        s.append(R(x-r-2,40,2*r+4,190,GLASS,1.8,'none'))
        s.append(f'<g data-anim="scale" data-from="1,0.3" data-o="{x},230" data-delay="{f(i*.2)}"><path d="M{x-r} 230 L{x-r} {top} Q{x} {top+r*1.1} {x+r} {top} L{x+r} 230 Z" fill="{WATER}" stroke="{WATER_S}" stroke-width="1.5"/></g>')
    s.append(T(160,270,mix='물: 관이 가늘수록 높이 올라감',size=19,fill=MUTED))
    s.append(R(420,180,150,60,'none',0,'#C8CDD3')); s.append(L(420,180,570,180,'#7E8B98',2))
    x,r=495,12; top=200
    s.append(R(x-r-2,40,2*r+4,190,GLASS,1.8,'none'))
    s.append(f'<path d="M{x-r} 230 L{x-r} {top} Q{x} {top-r*1.3} {x+r} {top} L{x+r} 230 Z" fill="#AEB6BF" stroke="#5B6B7F" stroke-width="1.5"/>')
    s.append(T(495,270,mix='수은: 볼록·내려감',size=19,fill=MUTED))
    s.append(A(300,90,268,104,'ink',2)); s.append(T(304,80,mix='오목한||메니스커스',size=18,anchor='start'))
    s.append(A(560,140,512,186,'ink',2)); s.append(T(560,120,mix='볼록',size=18,anchor='middle'))
    return svg((600,290),580,'유리관 속 물(오목, 올라감)과 수은(볼록, 내려감)의 메니스커스',s)
FIG['MENIS']=menis()

def stapp():
    s=[]
    s.append(L(60,30,330,30,INK,4)); s.append(L(80,30,80,310,INK,4))
    s.append(C(250,46,14,INK,2.5,'#E9ECEF')); s.append(C(250,46,3,INK,1,INK))
    s.append(L(264,46,264,140,INK,1.5)); s.append(L(236,46,170,30+0,INK,1.5)); s.append(L(170,30,150,130,INK,1.5))
    s.append(T(150,152,mix='당김',size=18,fill=MUTED))
    s.append(A(150,190,150,206,'ink',2.5) if False else '')
    # 원통(캔 고리)
    s.append(L(264,140,236,170,INK,1.3)); s.append(L(264,140,292,170,INK,1.3))
    s.append(f'<ellipse cx="264" cy="172" rx="34" ry="8" fill="none" stroke="{GRAV}" stroke-width="3"/>')
    s.append(L(230,172,230,184,GRAV,3)); s.append(L(298,172,298,184,GRAV,3))
    s.append(f'<ellipse cx="264" cy="184" rx="34" ry="8" fill="none" stroke="{GRAV}" stroke-width="3"/>')
    # 비커 + 액체
    s.append(f'<path d="M196 160 L196 250 Q196 258 204 258 L324 258 Q332 258 332 250 L332 160" fill="none" stroke="{GLASS}" stroke-width="2.5"/>')
    s.append(R(198,186,132,70,'none',0,WATER)); s.append(L(198,186,330,186,WATER_S,2))
    # 저울
    s.append(R(170,258,190,46,INK,2.5,'#F1F3F5',6)); s.append(R(220,270,90,24,INK,1.5,'#16233D',3))
    s.append(T(265,289,mix='−3.08 g',size=18,fill='#9BE7A6'))
    s.append(A(380,180,302,180,'ink',2)); s.append(T(384,186,mix='알루미늄 원통||(캔 고리)',size=18,anchor='start'))
    s.append(A(380,282,362,282,'ink',2)); s.append(T(384,288,mix='전자저울',size=18,anchor='start'))
    s.append(A(290,58,262,52,'ink',2)) if False else None
    s.append(T(300,22,mix='도르래',size=18,anchor='start'))
    return svg((500,320),470,'표면 장력 측정 장치: 도르래, 알루미늄 원통, 액체, 전자저울',s)
FIG['STAPP']=stapp()

# ═════════ b ═════════
def cover_b():
    s=['<g transform="translate(0,40)">']
    # 얼음 육각 구조(2차원 투영)
    O=[]; a=46
    for r in range(4):
        for c in range(5):
            cx=60+c*a*math.sqrt(3)+(a*math.sqrt(3)/2 if r%2 else 0); cy=60+r*a*1.5
            for k in range(6):
                ang=math.radians(60*k+30); O.append((round(cx+a*math.cos(ang),1),round(cy+a*math.sin(ang),1)))
    O=sorted(set(O)); O=[p for p in O if 20<p[0]<440 and 20<p[1]<400]
    bonds=set()
    for i,p in enumerate(O):
        for j,q in enumerate(O):
            if i<j and abs(math.hypot(p[0]-q[0],p[1]-q[1])-a)<2: bonds.add((i,j))
    for i,j in bonds:
        (x1,y1),(x2,y2)=O[i],O[j]
        hx,hy=x1+(x2-x1)*.3,y1+(y2-y1)*.3
        s.append(L(x1,y1,hx,hy,'#9AA5B1',4)); s.append(hb(hx,hy,x2,y2,2))
        s.append(f'<g data-atom="{f(hx)},{f(hy)},6,H,-"></g>')
    for k,(x,y) in enumerate(O): s.append(f'<g data-atom="{f(x)},{f(y)},11,O,-"></g>')
    s.append('</g>')
    return svg((460,460),440,'얼음의 열린 육각형 결정 구조(산소 빨강, 수소 흰색, 수소 결합 점선)',s,'fig cover-fig')
FIG['COVER_B']=cover_b()

def hydrides():
    s=[]; ax=Ax(80,300,380,270,5,120,xmin=1,ymin=-180)
    s.append(ax.frame([2,3,4,5],[-150,-100,-50,0,50,100],L(0,0,0,0),'',size=18))
    s.append(T(470,352,mix='주기',size=19,anchor='end',fill=MUTED)); s.append(T(16,20,mix='끓는점 (°C)',size=19,anchor='start',fill=MUTED))
    D=(('14족',GRAV,'',[-162,-112,-88,-52],['CH4','SiH4','GeH4','SnH4']),('15족',RD,'8 5',[-33,-88,-62,-17],['NH3','PH3','AsH3','SbH3']),('16족',MINUS,'',[100,-60,-41,-2],['H2O','H2S','H2Se','H2Te']),('17족',FIELD,'3 4',[20,-85,-67,-35],['HF','HCl','HBr','HI']))
    for i,(g,col,dash,v,nm) in enumerate(D):
        pts=[(ax.X(p+2),ax.Y(b)) for p,b in enumerate(v)]
        s.append(f'<g data-anim="draw" data-dur="1.1" data-delay="{f(i*.25)}">'+P(pts,col,3,dash=dash or None)+'</g>')
        for x,y in pts: s.append(C(x,y,5,col,2,col))
        s.append(L(392,40+i*26,420,40+i*26,col,3,dash or None)); s.append(T(428,46+i*26,mix=g,size=18,fill=col,anchor='start'))
    s.append(T(ax.X(2)+10,ax.Y(100)+6,tex='\\ce{H2O}',size=20,fill=MINUS,anchor='start',halo=True))
    s.append(T(ax.X(2)+10,ax.Y(20)+6,tex='\\ce{HF}',size=19,fill=FIELD,anchor='start',halo=True))
    s.append(T(ax.X(2)+10,ax.Y(-33)+4,tex='\\ce{NH3}',size=19,fill=RD,anchor='start',halo=True))
    s.append(T(ax.X(2)+10,ax.Y(-162)+6,tex='\\ce{CH4}',size=19,fill=GRAV,anchor='start',halo=True))
    return svg((520,362),500,'14–17족 원소의 수소 화합물의 끓는점',s)
FIG['HYD']=hydrides()

def hb2():
    s=[]
    b1,h1=wat(110,140,-30,24,18,d=40,lab=True); s.append(b1)
    hx,hy=h1[1]
    a=math.radians(22.25); ox,oy=hx+68*math.cos(a),hy+68*math.sin(a)
    b2,h2=wat(ox,oy,22.25,24,18,d=40,lab=True)
    s.append(f'<g data-anim="move" data-from="40,16" data-dur="1.2">'+b2+T(ox-8,oy-30,tex='\\delta^-',size=21,fill=MINUS)+'</g>')
    s.append(hb(hx+18*math.cos(a),hy+18*math.sin(a),ox-24*math.cos(a),oy-24*math.sin(a),3))
    s.append(T(72,104,tex='\\delta^-',size=21,fill=MINUS)); s.append(T(hx+4,hy-26,tex='\\delta^+',size=21,fill=PLUS))
    s.append(T((hx+ox)/2-4,(hy+oy)/2+34,mix='수소 결합',size=20,anchor='end'))
    s.append(T(16,240,mix='실선: 공유 결합 O–H',size=18,fill=MUTED,anchor='start'))
    return svg((300,250),380,'두 물 분자 사이의 수소 결합',s)
FIG['HB2']=hb2()

def tetra():
    s=[]; cx,cy=230,165
    dirs=[(-125,True),(-55,True),(45,False),(150,False)]  # (방향, 중심 분자의 H 쪽인지)
    ctr,hs=wat(cx,cy,-90,20,13,d=33)
    for k,(ang,isH) in enumerate(dirs):
        a=math.radians(ang)
        if isH:
            hx,hy=cx+33*math.cos(a),cy+33*math.sin(a)
            ox,oy=cx+105*math.cos(a),cy+105*math.sin(a)
            body,_=wat(ox,oy,ang,20,13,d=33)
            s.append(hb(hx+8*math.cos(a),hy+8*math.sin(a),ox-20*math.cos(a),oy-20*math.sin(a)))
        else:
            ox,oy=cx+100*math.cos(a),cy+100*math.sin(a)
            hxx,hyy=ox-33*math.cos(a),oy-33*math.sin(a)
            body=L(ox,oy,hxx,hyy,'#9AA5B1',6,extra='stroke-linecap="round"')
            oth=math.radians(ang+180-104.5)
            hx2,hy2=ox+33*math.cos(oth+math.pi),oy+33*math.sin(oth+math.pi)
            body+=L(ox,oy,hx2,hy2,'#9AA5B1',6,extra='stroke-linecap="round"')
            body+=f'<g data-atom="{f(ox)},{f(oy)},20,O,-"></g><g data-atom="{f(hxx)},{f(hyy)},13,H,-"></g><g data-atom="{f(hx2)},{f(hy2)},13,H,-"></g>'
            s.append(hb(cx+22*math.cos(a),cy+22*math.sin(a),hxx-12*math.cos(a),hyy-12*math.sin(a)))
        s.append(f'<g data-anim="pop" data-o="{f(ox)},{f(oy)}" data-delay="{f(.2*k)}">'+body+'</g>')
    s.append(ctr)
    s.append(legend_OH(20,300)); s.append(T(300,306,mix='점선: 수소 결합 4개',size=18,fill=MUTED,anchor='start'))
    return svg((460,320),420,'한 물 분자가 이웃 4개와 수소 결합하여 사면체 배열을 이룸',s)
FIG['TETRA']=tetra()

def ice():
    s=[]; O=[]; a=52
    for r in range(3):
        for c in range(4):
            cx=70+c*a*math.sqrt(3)+(a*math.sqrt(3)/2 if r%2 else 0); cy=70+r*a*1.5
            for k in range(6):
                ang=math.radians(60*k+30); O.append((round(cx+a*math.cos(ang),1),round(cy+a*math.sin(ang),1)))
    O=sorted(set(O)); O=[p for p in O if 10<p[0]<470 and 10<p[1]<300]
    bonds=[(i,j) for i in range(len(O)) for j in range(i+1,len(O)) if abs(math.hypot(O[i][0]-O[j][0],O[i][1]-O[j][1])-a)<2]
    for i,j in bonds:
        (x1,y1),(x2,y2)=O[i],O[j]; hx,hy=x1+(x2-x1)*.32,y1+(y2-y1)*.32
        s.append(L(x1,y1,hx,hy,'#9AA5B1',4)); s.append(hb(hx,hy,x2,y2,2)); s.append(f'<g data-atom="{f(hx)},{f(hy)},7,H,-"></g>')
    for x,y in O: s.append(f'<g data-atom="{f(x)},{f(y)},12,O,-"></g>')
    cx=70+1*a*math.sqrt(3)+a*math.sqrt(3)/2; cy=70+a*1.5
    s.append(f'<g data-anim="pop" data-o="{f(cx)},{f(cy)}" data-delay=".4">'+C(cx,cy,24,EQUI,2.5,'#FFE45C',extra='fill-opacity=".5"')+'</g>')
    s.append(T(cx,cy+7,mix='빈 공간',size=18,weight=700))
    return svg((480,310),440,'얼음의 열린 육각형 결정 구조와 육각형 안의 빈 공간',s)
FIG['ICE']=ice()

def solv():
    s=[]
    b,_=wat(110,110,0,24,18,d=40,lab=True); s.append(b)
    s.append(T(96,62,tex='\\delta^-',size=21,fill=MINUS)); s.append(T(170,74,tex='\\delta^+',size=21,fill=PLUS))
    s.append(f'<g data-anim="move" data-from="16,0" data-rep="alt" data-dur="1.3">'+f'<ellipse cx="300" cy="110" rx="70" ry="44" fill="#CFE3F7" stroke="{MINUS}" stroke-width="2" fill-opacity=".85"/>'+'</g>')
    s.append(L(272,110,328,110,'#9AA5B1',7)); s.append(f'<g data-atom="272,110,24,O"></g><g data-atom="328,110,24,O"></g>')
    s.append(T(234,66,tex='\\delta^-',size=21,fill=MINUS)); s.append(T(368,66,tex='\\delta^+',size=21,fill=PLUS))
    s.append(T(300,190,mix='$\\ce{O2}$(무극성)에 쌍극자가 유도됨',size=19,fill=MUTED)); s.append(T(110,190,mix='극성인 물',size=19,fill=MUTED))
    return svg((420,210),400,'극성인 물 분자가 산소 분자에 쌍극자를 유도함',s)
FIG['SOLV']=solv()

def climate():
    s=[]; ax=Ax(70,230,400,190,24,40,ymin=0)
    s.append(L(70,230,480,230,MUTED,2)); s.append(L(70,230,70,30,MUTED,2))
    for h in (0,6,12,18,24): s.append(L(ax.X(h),230,ax.X(h),236,MUTED,1.5)); s.append(T(ax.X(h),256,tex=str(h),size=18))
    s.append(T(480,282,mix='시각 (시)',size=19,anchor='end',fill=MUTED)); s.append(T(16,22,mix='기온',size=19,anchor='start',fill=MUTED))
    fc=lambda h:22+3.5*math.cos(2*math.pi*(h-14)/24); fl=lambda h:22+10*math.cos(2*math.pi*(h-14)/24)
    s.append(f'<g data-anim="draw" data-dur="1.2">'+ax.curve(fl,0,24,col=OX,w=3.5)+'</g>')
    s.append(f'<g data-anim="draw" data-dur="1.2" data-delay=".4">'+ax.curve(fc,0,24,col=RD,w=3.5,dash='9 5')+'</g>')
    s.append(L(300,30,330,30,OX,3.5)); s.append(T(338,36,mix='내륙(일교차 큼)',size=18,fill=OX,anchor='start')); s.append(L(300,56,330,56,RD,3.5,'9 5')); s.append(T(338,62,mix='해안(일교차 작음)',size=18,fill=RD,anchor='start'))
    return svg((500,290),470,'해안 도시와 내륙의 하루 기온 변화 비교(개념 그림)',s)
FIG['CLIM']=climate()

def phase():
    s=[]
    s.append(L(80,300,480,300,MUTED,2)); s.append(L(80,300,80,30,MUTED,2))
    tx,ty=170,250
    s.append(f'<path d="M{tx} {ty} L178 40" fill="none" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<path d="M{tx} {ty} Q300 200 460 70" fill="none" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<path d="M100 296 Q140 268 {tx} {ty}" fill="none" stroke="{INK}" stroke-width="3"/>')
    s.append(C(tx,ty,6,PLUS,2,PLUS)); s.append(T(tx+12,ty+24,mix='삼중점||(0.01 °C, 4.6 mmHg)',size=18,fill=PLUS,anchor='start'))
    y760=110; s.append(L(80,y760,470,y760,MUTED,1.5,'6 4')); s.append(T(74,y760+6,tex='760',size=18,anchor='end')); s.append(T(74,ty+6,tex='4.6',size=18,anchor='end'))
    x0=176.5; x100=388
    s.append(L(x0,y760,x0,300,MUTED,1.5,'4 4')); s.append(L(x100,y760,x100,300,MUTED,1.5,'4 4'))
    s.append(T(x0,322,tex='0',size=18)); s.append(T(x100,322,tex='100',size=18))
    s.append(T(120,150,mix='얼음',size=21,weight=700)); s.append(T(280,120,mix='물',size=21,weight=700)); s.append(T(400,232,mix='수증기',size=21,weight=700))
    s.append(T(470,346,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)); s.append(T(16,22,mix='압력 (mmHg)',size=19,anchor='start',fill=MUTED))
    s.append(f'<g class="step" data-g="ph1">'+f'<g data-anim="move" data-from="0,50" data-dur="1">'+A(150,180,150,90,'plus',3)+'</g>'+T(146,72,mix='압력↑ → 녹음',size=18,fill=PLUS,anchor='end',halo=True)+'</g>')
    s.append(T(196,58,mix='융해 곡선(음의 기울기)',size=18,fill=MUTED,anchor='start',halo=True))
    return svg((500,350),470,'물의 상평형 그림(눈금 비례 아님)',s)
FIG['PHASE']=phase()

DL=[(-30,0.9838),(-20,0.99355),(-10,0.99817),(0,0.99984),(4,0.99997),(10,0.99970),(20,0.99820),(30,0.99565),(40,0.99222),(50,0.98804),(60,0.98320),(70,0.97777),(80,0.97179),(90,0.96531),(100,0.95835)]
def dens():
    s=[]; ax=Ax(80,300,400,250,100,1.02,xmin=-40,ymin=0.90)
    s.append(ax.frame([-40,-20,0,20,40,60,80,100],[0.90,0.92,0.94,0.96,0.98,1.00,1.02],L(0,0,0,0),'',yfmt=lambda v:('' if v<0.91 else f'{v:.2f}'),size=18))
    s.append(T(480,356,mix='온도 (°C)',size=19,anchor='end',fill=MUTED)); s.append(T(16,20,mix='밀도 ($\\text{g/cm}^3$)',size=19,anchor='start',fill=MUTED))
    # 보간
    def fl(t):
        for (t1,d1),(t2,d2) in zip(DL,DL[1:]):
            if t1<=t<=t2: return d1+(d2-d1)*(t-t1)/(t2-t1)
        return DL[-1][1]
    s.append(ax.curve(fl,-30,0,col=MINUS,w=3,dash='6 4'))
    s.append(f'<g data-anim="draw" data-dur="1.3">'+ax.curve(fl,0,100,col=MINUS,w=3.5)+'</g>')
    s.append(ax.curve(lambda t:0.9167-0.00012*t,-40,0,col=BF,w=3.5))
    s.append(L(ax.X(0),ax.Y(0.9998),ax.X(0),ax.Y(0.9167),MUTED,2,'4 4'))
    s.append(C(ax.X(4),ax.Y(0.99997),6,PLUS,2,PLUS)); s.append(T(ax.X(4)+10,ax.Y(1.00)-14,mix='4 °C 최대 밀도',size=18,fill=PLUS,anchor='start',halo=True))
    s.append(T(ax.X(-20),ax.Y(0.9195)-14,mix='고체(얼음)',size=18,fill=BF,halo=True))
    s.append(T(ax.X(-22),ax.Y(0.985)+30,mix='과냉각 액체',size=18,fill=MINUS,halo=True))
    s.append(T(ax.X(70),ax.Y(0.977)+30,mix='액체',size=19,fill=MINUS,halo=True))
    s.append(A(ax.X(0)+44,ax.Y(0.95),ax.X(0)+6,ax.Y(0.95),'ink',2)); s.append(T(ax.X(0)+48,ax.Y(0.95)+6,mix='얼면 약 9 % 부피 증가',size=18,anchor='start',halo=True))
    return svg((500,364),480,'온도에 따른 물과 얼음의 밀도',s)
FIG['DENS']=dens()

def lake():
    s=[R(20,40,420,200,'none',0,'#CFE6F5'),R(20,40,420,30,INK,1.5,'#EEF6FB')]
    s.append(T(230,62,mix='얼음 0 °C',size=19,weight=700))
    for i,(y,t) in enumerate(((100,'1 °C'),(150,'3 °C'),(210,'4 °C'))): s.append(T(400,y,mix=t,size=19,anchor='end',fill=MINUS))
    s.append(f'<g data-anim="move" data-from="-40,0" data-rep="alt" data-dur="2.2"><path d="M120 190 q20 -16 46 0 q-26 16 -46 0 z M120 190 l-14 -10 l0 20 z" fill="{EQUI}" stroke="{INK}" stroke-width="1.5"/></g>')
    s.append(T(230,270,mix='밀도가 가장 큰 4 °C 물이 바닥에 — 물고기가 겨울을 남',size=19,fill=MUTED))
    return svg((460,290),440,'겨울 호수: 표면부터 얼고 바닥에는 4 °C 물',s)
FIG['LAKE']=lake()

EX2=[(20,2.3),(30,4.2),(40,7.4),(50,12.3),(60,19.9),(70,31.1),(80,47.3)]
def fit(pts):
    X=[a for a,b in pts];Y=[b for a,b in pts];n=len(X);mx=sum(X)/n;my=sum(Y)/n
    b=sum((x-mx)*(y-my) for x,y in pts)/sum((x-mx)**2 for x in X); a=my-b*mx
    r2=1-sum((y-(a+b*x))**2 for x,y in pts)/sum((y-my)**2 for y in Y); return b,a,r2
CC=[(1/(t+273.15),math.log(p)) for t,p in EX2]
CCB,CCA,CCR2=fit(CC)
def ccfig():
    s=[]; ax=Ax(80,290,400,250,3.45,4.0,xmin=2.8,ymin=0.5)
    s.append(ax.frame([2.8,2.9,3.0,3.1,3.2,3.3,3.4],[1,2,3,4],L(0,0,0,0),'',xfmt=lambda v:f'{v:.1f}',size=18))
    s.append(T(480,346,mix='$1/T$ ($10^{-3}\\ \\text{K}^{-1}$)',size=19,anchor='end',fill=MUTED)); s.append(T(16,22,mix='$\\ln P$ ($P$: kPa)',size=19,anchor='start',fill=MUTED))
    s.append(f'<g class="step" data-g="ccf">'+P([(ax.X(2.8),ax.Y(CCA+CCB*2.8e-3)),(ax.X(3.45),ax.Y(CCA+CCB*3.45e-3))],FIELD,3)+T(ax.X(3.0),ax.Y(CCA+CCB*3.0e-3)-40,mix=f'$y={CCB:.0f}\\,x+{CCA:.2f}$',size=19,fill=FIELD,anchor='start',halo=True)+'</g>')
    for i,(x,y) in enumerate(CC):
        s.append(f'<g data-anim="pop" data-o="{f(ax.X(x*1000))},{f(ax.Y(y))}" data-delay="{f(.12*i)}">'+C(ax.X(x*1000),ax.Y(y),6,MINUS,2,'#FFFFFF')+'</g>')
    return svg((500,354),480,'물의 ln P와 1/T 그래프와 추세선(예시 값)',s)
FIG['CCFIG']=ccfig()

P2=[(200,0.80),(220,4.50),(240,21.0),(260,71.0),(280,197),(300,391)]
P2B,P2A,P2R=fit([(1/t,math.log(p)) for t,p in P2])
def p2fig():
    s=[]; ax=Ax(70,250,330,210,5.1,6.5,xmin=3.2,ymin=-1)
    s.append(ax.frame([3.2,3.6,4.0,4.4,4.8],[-1,1,3,5],L(0,0,0,0),'',xfmt=lambda v:f'{v:.1f}',size=18))
    s.append(T(410,304,mix='$1/T$ ($10^{-3}\\ \\text{K}^{-1}$)',size=19,anchor='end',fill=MUTED)); s.append(T(12,20,mix='$\\ln P$',size=19,anchor='start',fill=MUTED))
    s.append(f'<g class="step" data-g="p2f">'+P([(ax.X(3.25),ax.Y(P2A+P2B*3.25e-3)),(ax.X(5.05),ax.Y(P2A+P2B*5.05e-3))],FIELD,3)+'</g>')
    for t,p in P2: s.append(C(ax.X(1000/t),ax.Y(math.log(p)),5.5,BF,2,'#FFFFFF'))
    return svg((420,312),400,'다이클로로메테인의 ln P와 1/T',s)
FIG['P2FIG']=p2fig()

def dce():
    s=[]
    def mol(x0,cis):
        o=L(x0+60,90,x0+120,90,INK,3)+L(x0+60,100,x0+120,100,INK,3)
        sub=[('Cl','H'),('Cl','H')] if cis else [('Cl','H'),('H','Cl')]
        # 왼쪽 C 위·아래, 오른쪽 C 위·아래
        LU,LD=('Cl','H') ; RU,RD=('Cl','H') if cis else ('H','Cl')
        for (x1,y1,x2,y2,lab) in ((x0+60,90,x0+30,50,LU),(x0+60,100,x0+30,140,LD),(x0+120,90,x0+150,50,RU),(x0+120,100,x0+150,140,RD)):
            o+=L(x1,y1,x2+(6 if x2<x1 else -6),y2+(6 if y2<y1 else -6),INK,3)+T(x2,y2+8,tex=f'\\mathrm{{{lab}}}',size=24)
        o+=T(x0+60,103,tex='\\mathrm{C}',size=24,halo=True)+T(x0+120,103,tex='\\mathrm{C}',size=24,halo=True)
        return o
    s.append(mol(10,True)); s.append(mol(230,False))
    s.append(f'<g class="step" data-g="q4c">'+A(188,140,188,50,'plus',4)+L(180,126,196,126,PLUS,4)+T(100,190,mix='극성 (쌍극자 합 ≠ 0)',size=18,fill=PLUS)+T(320,190,mix='무극성 (합 = 0)',size=18,fill=MUTED)+'</g>')
    s.append(T(100,26,mix='시스',size=19,weight=700)); s.append(T(320,26,mix='트랜스',size=19,weight=700))
    return svg((440,200),420,'시스-다이클로로에텐과 트랜스-다이클로로에텐의 구조',s)
FIG['DCE']=dce()

# ═════════ 출력 ═════════
for d in 'ab':
    tpl=open(os.path.join(HERE,f'tpl_{d}.html'),encoding='utf-8').read()
    def rep(m):
        k=m.group(1)
        if k not in FIG: sys.exit('no fig '+k)
        return FIG[k]
    out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
    os.makedirs(OUT[d],exist_ok=True)
    open(OUT[d]+'slides.html','w',encoding='utf-8').write(out)
    for src,dst in (('labs_src.js','labs.js'),('extra_src.css','extra.css')):
        if os.path.exists(os.path.join(HERE,src)): shutil.copy(os.path.join(HERE,src),OUT[d]+dst)
    print('ok',d,len(out))
if '--calc' in sys.argv:
    print('CC slope',CCB,'int',CCA,'r2',CCR2,'dH',-CCB*8.314)
    print('P2 slope',P2B,P2A,P2R,-P2B*8.314)
    for t,p in EX2: print(t,round(1000/(t+273.15),3),round(math.log(p),3))
