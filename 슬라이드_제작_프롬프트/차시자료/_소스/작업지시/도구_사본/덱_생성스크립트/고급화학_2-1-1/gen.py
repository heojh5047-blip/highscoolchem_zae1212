# -*- coding: utf-8 -*-
"""고급화학 2-1-1(a/b) 그림 생성: tpl_a.html, tpl_b.html의 {{KEY}}를 SVG로 바꿔 각 덱 slides.html을 만든다.
   python3 -I gen.py   (출력 경로는 아래 OUT — 이 덱 두 폴더만, assert로 막음)"""
import math, random, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
OUT={'a':BASE+'2-1-1_기체_분자_운동론과_실제_기체_혼합_기체a/slides.html',
     'b':BASE+'2-1-1_기체_분자_운동론과_실제_기체_혼합_기체b/slides.html'}
for k,v in OUT.items():
    assert v.startswith(BASE+'2-1-1_기체_분자_운동론과_실제_기체_혼합_기체') and v.endswith(k+'/slides.html'), v
FIG={}
N2=0.02802; HE=0.00400

# ═════════ a ═════════
def cover_a():
    s=[R(30,24,400,250,INK,3,'#FFFFFF',8)]
    s.append(mol_box(30,24,400,250,13,7,r=12,arrow=22))
    ax=Ax(60,420,360,100,1500,0.0036)
    s.append(L(60,420,430,420,MUTED,2)); s.append(L(60,420,60,310,MUTED,2))
    s.append(f'<g data-anim="draw" data-dur="1.4">'+ax.curve(lambda v:mb(v,150,N2),0,1500,col=MINUS,w=3.5)+'</g>')
    s.append(f'<g data-anim="draw" data-dur="1.4" data-delay=".4">'+ax.curve(lambda v:mb(v,600,N2),0,1500,col=PLUS,w=3.5)+'</g>')
    s.append(T(150,326,tex='T_1',size=22,fill=MINUS)); s.append(T(330,372,tex='T_2',size=22,fill=PLUS))
    s.append(T(424,446,mix='속력 $v$',size=19,anchor='end',fill=MUTED))
    s=['<g transform="translate(0,40)">']+s+['</g>']
    return svg((460,496),440,'상자 속에서 무질서하게 움직이는 기체 분자와 두 온도의 속력 분포 곡선(T1 < T2)',s,'fig cover-fig')
FIG['COVER_A']=cover_a()

def atm():
    s=[]
    # 고도 막대 0–100 km, 누적 대기 질량
    x0,y0,hh=150,330,290
    Y=lambda km:y0-km/100*hh
    s.append(f'<defs><linearGradient id="grad-ac211-03" x1="0" x2="0" y1="1" y2="0"><stop offset="0" stop-color="#9CC7F0"/><stop offset="1" stop-color="#0B1F3F"/></linearGradient></defs>')
    s.append(R(x0,Y(100),90,hh,INK,1.5,'url(#grad-ac211-03)'))
    s.append(f'<path d="M110 {y0} Q195 {y0-22} 280 {y0}" fill="#3FA36B" stroke="{INK}" stroke-width="1.5"/>')
    for km in (0,20,40,60,80,100):
        s.append(L(x0-6,Y(km),x0,Y(km),MUTED,1.5)); s.append(T(x0-10,Y(km)+6,tex=f'{km}',size=18,anchor='end'))
    s.append(T(x0-58,Y(50),mix='고도||(km)',size=18,fill=MUTED))
    s.append(f'<g data-anim="scale" data-from="1,0" data-o="{x0+45},{y0}" data-dur="1.2">'+R(x0+20,Y(5.5),50,Y(0)-Y(5.5),EQUI,1.5,EQUI,extra='fill-opacity=".7"')+'</g>')
    s.append(L(x0+90,Y(5.5),x0+120,Y(5.5),EQUI,2)); s.append(T(x0+126,Y(5.5)+6,mix='5.5 km 아래: 대기 질량의 약 50 %',size=19,anchor='start'))
    s.append(L(x0+90,Y(100),x0+120,Y(100),MUTED,2,'5 4')); s.append(T(x0+126,Y(100)+18,mix='100 km 아래: 99 % 이상',size=19,anchor='start'))
    s.append(T(x0+126,Y(55),mix='중력이 기체 분자를||지표 가까이 붙든다',size=19,anchor='start',fill=MUTED))
    return svg((560,350),520,'고도에 따른 대기 질량 분포: 5.5 km 아래에 약 50 %, 100 km 아래에 99 % 이상',s)
FIG['ATM']=atm()

def tire():
    s=[]
    for i,(x,lab,fast,col) in enumerate([(20,'겨울 (낮은 온도)',0.7,MINUS),(260,'여름 (높은 온도)',1.5,PLUS)]):
        s.append(R(x,30,200,170,col,3,'#FDE2E4' if i else '#E3EEFB',16))
        s.append(mol_box(x,30,200,170,7,11+i,r=10,arrow=16,fast=fast))
        s.append(T(x+100,226,mix=lab,size=20,fill=col,weight=700))
    return svg((480,240),440,'같은 부피의 타이어 속 기체: 온도가 높으면 분자의 속력이 빠르다(화살표 길이)',s)
FIG['TIRE']=tire()

def assume():
    s=[R(20,20,420,250,INK,3,'#FFFFFF',6)]
    s.append(mol_box(20,20,420,250,11,21,r=11,arrow=24))
    # 벽 충돌 강조
    s.append(C(440,150,26,EQUI,2,dash='5 4'))
    s.append(T(230,296,mix='분자 크기 ≪ 분자 사이 거리 (크기 비례 아님)',size=19,fill=MUTED))
    return svg((460,306),440,'기체 분자 운동론의 가정: 분자는 무질서하게 움직이며 벽과 완전 탄성 충돌',s)
FIG['ASSUME']=assume()

def mom():
    s=[R(330,20,26,250,GRAV,1.5,'#C9D3DD')]
    s.append(T(343,292,mix='용기 벽',size=19,fill=MUTED))
    s.append(f'<g data-anim="move" data-from="-120,0" data-dur="1.1" data-ease="in">'+gm(300,80,14)+'</g>')
    s.append(A(120,80,282,80,'plus',5)); s.append(T(200,62,tex='+mv_x',size=22,fill=PLUS))
    s.append(T(60,86,mix='충돌 전',size=20,weight=700))
    s.append(gm(300,200,14)); s.append(A(282,200,120,200,'minus',5)); s.append(T(200,182,tex='-mv_x',size=22,fill=MINUS))
    s.append(T(60,206,mix='충돌 후',size=20,weight=700))
    s.append(T(165,262,tex='\\Delta p=2mv_x',size=22))
    return svg((380,300),380,'벽에 수직으로 충돌하는 분자의 운동량 변화: +mv_x에서 −mv_x로, 크기 2mv_x',s)
FIG['MOM']=mom()

def coll():
    s=[]
    # 원근 상자
    s.append(R(40,40,330,220,INK,2.5,'#FFFFFF'))
    s.append(f'<rect x="250" y="40" width="120" height="220" fill="#FFE45C" fill-opacity=".35"/>')
    s.append(R(370,40,22,220,GRAV,1.5,'#C9D3DD'))
    s.append(L(250,40,250,260,MUTED,1.5,'5 4'))
    s.append(L(250,30,370,30,MUTED,1.5)); s.append(A(310,30,250,30,'muted',1.5)); s.append(A(310,30,370,30,'muted',1.5))
    s.append(T(310,26,tex='v_x\\Delta t',size=20,halo=True))
    s.append(T(381,284,mix='넓이 $A$',size=19,fill=MUTED))
    for (x,y,d) in [(290,90,1),(330,170,1),(280,215,-1),(345,120,-1),(140,110,1),(110,200,-1),(190,160,1)]:
        inside=x>250
        col='plus' if d>0 else 'muted'
        s.append(A(x+d*11,y,x+d*36,y,col,2.5)); s.append(gm(x,y,11))
    s.append(T(190,290,mix='벽 쪽으로 가는 분자만 충돌(절반)',size=19,fill=INK))
    return svg((410,300),400,'Δt 동안 벽에 충돌할 수 있는 분자: 벽에서 v_xΔt 안의 부피 Av_xΔt 속, 벽 쪽으로 움직이는 절반',s)
FIG['COLL']=coll()

def vec():
    s=[]; ox,oy=120,210
    s.append(A(ox,oy,ox+230,oy,'muted',2)); s.append(A(ox,oy,ox,oy-180,'muted',2)); s.append(A(ox,oy,ox-80,oy+60,'muted',2))
    s.append(T(ox+244,oy+8,tex='x',size=20,anchor='start')); s.append(T(ox,oy-190,tex='y',size=20)); s.append(T(ox-92,oy+72,tex='z',size=20))
    vx,vy,vz=150,-110,(-40,30)
    px,py=ox+vx+vz[0],oy+vy+vz[1]
    s.append(P([(ox+vx,oy),(ox+vx+vz[0],oy+vz[1]),(px,py)],MUTED,1.5,dash='4 4'))
    s.append(L(ox+vz[0],oy+vz[1],ox+vx+vz[0],oy+vz[1],MUTED,1.5,'4 4'))
    s.append(A(ox,oy,ox+vx,oy,'minus',3)); s.append(T(ox+vx/2,oy+24,tex='v_x',size=20,fill=MINUS))
    s.append(f'<g data-anim="draw" data-dur="1">'+L(ox,oy,px,py,PLUS,0)+'</g>')
    s.append(A(ox,oy,px,py,'plus',4)); s.append(T(px+10,py-6,tex='\\vec v',size=22,fill=PLUS,anchor='start'))
    s.append(gm(px,py,11))
    return svg((380,300),330,'3차원 속도 v와 x 성분 v_x',s)
FIG['VEC']=vec()

def laws():
    out={}
    s=[]
    for i,(x,fast,lab,col) in enumerate([(10,0.7,'$T$ 낮음',MINUS),(200,1.4,'$T$ 높음',PLUS)]):
        s.append(R(x,20,160,140,col,2.5,'#E3EEFB' if i==0 else '#FDE2E4',10)); s.append(mol_box(x,20,160,140,6,31,r=9,arrow=14,fast=fast))
        s.append(T(x+80,186,mix=lab,size=20,fill=col,weight=700))
    s.append(T(185,96,tex='\\Rightarrow',size=26))
    out['LAW_T']=svg((370,200),340,'부피가 일정할 때 온도가 높으면 분자가 빠르게 더 세게 더 자주 충돌',s)
    s=[]
    s.append(R(10,20,160,140,INK,2.5,'#FFFFFF',4)); s.append(mol_box(10,20,160,140,6,41,r=9,arrow=14))
    s.append(R(14,8,152,10,MUTED,1.5,GRAV)); s.append(A(90,-8,90,6,'ink',2.5))
    s.append(T(90,186,mix='$V$ 큼',size=20,weight=700))
    s.append(f'<g data-anim="scale" data-from="1,1.75" data-o="280,160" data-dur="1.4" data-ease="out">'+R(200,80,160,80,INK,2.5,'#FFFFFF',4)+'</g>')
    pts=[(225,100),(262,140),(300,108),(335,138),(240,140),(320,98)]
    s.append(f'<g data-anim="move" data-from="0,-30" data-dur="1.4" data-ease="out">'+R(204,68,152,10,MUTED,1.5,GRAV)+A(280,40,280,64,'ink',4)+T(272,40,mix='외부 압력 증가',size=19,anchor='end')+'</g>')
    s.append(mol_box(200,80,160,80,6,0,r=9,arrow=12,anim=False,pts=pts))
    s.append(T(280,186,mix='$V$ 작음',size=20,weight=700))
    out['LAW_P']=svg((370,200),340,'온도가 일정할 때 외부 압력이 커지면 부피가 줄어 단위 부피당 충돌 수 증가',s)
    return out
FIG.update(laws())

def mb_three():
    s=[]; ax=Ax(80,330,500,280,1200,0.0036)
    xl=T(580,388,mix='속력 $v$ [m/s]',size=19,anchor='end'); yl=T(18,40,mix='$f(v)$ [s/m]',size=19,anchor='start')
    s.append(ax.frame([0,200,400,600,800,1000,1200],[0,0.001,0.002,0.003],xl,yl,yfmt=lambda v:'0' if v==0 else f'{v:.3f}'))
    for T_,col,dl in [(100,MINUS,0),(300,INK,.4),(500,PLUS,.8)]:
        s.append(f'<g data-anim="draw" data-dur="1.3" data-delay="{dl}">'+ax.curve(lambda v:mb(v,T_,N2),0,1200,col=col,w=3.5)+'</g>')
        v=vp(T_,N2); s.append(T(ax.X(v)+14,ax.Y(mb(v,T_,N2))-10,tex=f'{T_}\\ \\text{{K}}',size=20,fill=col,anchor='start',halo=True))
    return svg((600,398),560,'질소 분자의 맥스웰 속력 분포(계산): 100 K, 300 K, 500 K',s)
FIG['MB3']=mb_three()

def mb_one():
    s=[]; ax=Ax(70,300,440,240,1200,0.0022); T_=300
    xl=T(520,358,mix='속력 $v$ [m/s]',size=19,anchor='end'); yl=T(14,40,mix='$f(v)$ [s/m]',size=19,anchor='start')
    s.append(ax.frame([0,400,800,1200],[0,0.001,0.002],xl,yl,yfmt=lambda v:'0' if v==0 else f'{v:.3f}'))
    # 넓이 음영
    pts=[(ax.X(0),ax.Y(0))]+[(ax.X(v),ax.Y(mb(v,T_,N2))) for v in range(0,1201,10)]+[(ax.X(1200),ax.Y(0))]
    s.append(P(pts,'none',0,fill='#2E9E6A',extra='fill-opacity=".12"',close=True))
    s.append(ax.curve(lambda v:mb(v,T_,N2),0,1200,col=INK,w=3.5))
    for v,lab,dy in [(vp(T_,N2),'v_\\text{p}',0),(vavg(T_,N2),'\\bar v',26),(vrms(T_,N2),'v_\\text{rms}',52)]:
        s.append(L(ax.X(v),ax.Y(0),ax.X(v),ax.Y(mb(v,T_,N2)),MUTED,1.5,'5 4'))
        s.append(T(ax.X(v)+6,ax.Y(0)-14-dy,tex=lab,size=19,anchor='start',halo=True))
    s.append(T(300,180,mix='넓이 = 1 (전체 분자)',size=19,fill=FIELD,anchor='start',halo=True))
    return svg((530,368),500,'300 K 질소의 속력 분포: 곡선 아래 넓이 1, 최빈 속력 < 평균 속력 < 제곱평균근 속력',s)
FIG['MB1']=mb_one()

def pred():
    out={}
    s=[]; ax=Ax(40,180,320,150,1200,0.0036)
    s.append(L(40,180,370,180,MUTED,2)); s.append(L(40,180,40,22,MUTED,2))
    s.append(ax.curve(lambda v:mb(v,200,N2),0,1200,col=MINUS,w=3))
    s.append(f'<g class="step" data-g="pr1">'+ax.curve(lambda v:mb(v,600,N2),0,1200,col=PLUS,w=3)+T(250,124,tex='600\\ \\text{K}',size=19,fill=PLUS,anchor='start',halo=True)+'</g>')
    s.append(T(118,40,tex='200\\ \\text{K}',size=19,fill=MINUS,anchor='start'))
    s.append(T(366,204,mix='$v$',size=19,anchor='end',fill=MUTED))
    out['PRED_T']=svg((380,214),340,'온도를 높일 때의 속력 분포 예측(질소 200 K → 600 K)',s)
    s=[]; ax=Ax(40,180,320,150,3000,0.0021)
    s.append(L(40,180,370,180,MUTED,2)); s.append(L(40,180,40,22,MUTED,2))
    s.append(ax.curve(lambda v:mb(v,300,N2),0,3000,col=INK,w=3))
    s.append(T(84,40,mix='$\\ce{N2}$',size=19,anchor='start'))
    s.append(f'<g class="step" data-g="pr2">'+ax.curve(lambda v:mb(v,300,HE),0,3000,col=INK,w=3,dash='9 6')+T(222,122,mix='$\\ce{He}$',size=19,anchor='start',halo=True)+'</g>')
    s.append(T(366,204,mix='$v$',size=19,anchor='end',fill=MUTED))
    out['PRED_M']=svg((380,214),340,'몰질량이 작을 때의 속력 분포 예측(300 K, 질소와 헬륨)',s)
    return out
FIG.update(pred())

def rapp():
    """KClO3 가열 → 산소 수상 치환 장치"""
    s=[]
    # 수조
    s.append(R(250,170,220,110,GLASS,2,WATER,6)); s.append(L(252,190,468,190,WATER_S,2))
    # 눈금실린더(거꾸로)
    s.append(R(330,40,56,196,GLASS,2.2,'#FFFFFF'))
    s.append(f'<rect x="331" y="112" width="54" height="123" fill="{WATER}"/>')
    for i in range(9): s.append(L(330,56+i*18,342,56+i*18,MUTED,1.2))
    s.append(f'<g data-anim="scale" data-from="1,0.2" data-o="358,40" data-dur="1.6" data-ease="out"><rect x="331" y="41" width="54" height="70" fill="#FFFFFF"/></g>')
    s.append(L(330,112,386,112,WATER_S,2))
    s.append(T(358,84,tex='\\ce{O2}',size=22))
    for (bx,by) in [(352,220),(364,200),(356,176),(362,150)]:
        s.append(f'<g data-anim="move" data-from="0,40" data-rep="loop" data-dur="1.6" data-delay="{f((by-150)/60)}">'+C(bx,by,4,WATER_S,1.5,'#FFFFFF')+'</g>')
    # 시험관 + 가열
    s.append(f'<g transform="rotate(-18 120 150)">'+f'<path d="M60 130 L170 130 A20 20 0 0 1 170 170 L60 170" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2.2"/>'
             +f'<path d="M150 156 Q168 150 186 160 L186 166 L150 166 Z" fill="#F4F1E6" stroke="{MUTED}" stroke-width="1"/>'+R(52,128,14,44,INK,1.5,'#8C6B4A',2)+'</g>')
    s.append(P([(64,132),(40,90),(40,60),(250,60),(250,230),(352,230)],INK,3))
    s.append(f'<path d="M160 236 Q150 214 166 200 Q170 218 180 210 Q186 228 172 238 Z" fill="#F28C28" stroke="{OX}" stroke-width="1.2"/>')
    s.append(R(150,238,40,30,INK,1.5,'#C9D3DD',3))
    s.append(T(170,296,mix='가열',size=19,fill=MUTED))
    s.append(T(72,232,mix='$\\ce{KClO3}$ +||$\\ce{MnO2}$',size=19))
    s.append(T(400,130,mix='수면 높이를||맞춘다',size=19,anchor='start',fill=MUTED))
    return svg((520,310),470,'염소산 칼륨과 이산화 망가니즈를 가열하여 발생한 산소를 수상 치환으로 눈금실린더에 모으는 장치',s)
FIG['RAPP']=rapp()

def icon(kind):
    s=[]
    if kind=='bal':
        s.append(R(20,70,140,30,INK,2,'#E9EDF1',6)); s.append(R(50,60,80,10,INK,1.5,'#FFFFFF',2))
        s.append(R(42,76,96,18,INK,1,'#16233D',3)); s.append(T(90,91,tex='12.345\\ \\text{g}',size=18,fill='#FFFFFF'))
        s.append(f'<path d="M78 58 L84 24 L96 24 L102 58 Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/>')
    elif kind=='col':
        s.append(R(20,60,140,46,GLASS,2,WATER,4)); s.append(R(70,6,30,90,GLASS,2,'#FFFFFF')); s.append(f'<rect x="71" y="46" width="28" height="49" fill="{WATER}"/>')
        s.append(L(70,46,100,46,WATER_S,2)); s.append(L(20,72,70,72,WATER_S,2,'4 3')); s.append(L(100,72,160,72,WATER_S,2,'4 3'))
    else:
        s.append(R(30,20,18,80,GLASS,2,'#FFFFFF',9)); s.append(f'<rect x="35" y="58" width="8" height="38" fill="{PLUS}"/>'); s.append(C(39,100,10,GLASS,2,PLUS))
        s.append(T(56,66,tex='t\\ {}^\\circ\\text{C}',size=18,anchor='start'))
        s.append(C(130,58,32,INK,2,'#FFFFFF')); s.append(L(130,58,148,40,PLUS,2.5)); s.append(T(130,84,mix='기압계',size=18))
    return svg((190,112),170,{'bal':'전자저울로 시험관 질량 측정','col':'수상 치환으로 모은 기체의 부피를 수면을 맞춰 읽음','tem':'물의 온도와 대기압 측정'}[kind],s)
FIG['IC_BAL']=icon('bal');FIG['IC_COL']=icon('col');FIG['IC_TEM']=icon('tem')

# ═════════ b ═════════
def cover_b():
    s=[]
    ax=Ax(60,330,360,270,800,2.2,ymin=0)
    s.append(R(30,20,420,350,'#E2E7EC',1,'#FFFFFF',10))
    s.append(L(60,330,430,330,MUTED,2)); s.append(L(60,330,60,50,MUTED,2))
    s.append(L(60,ax.Y(1),420,ax.Y(1),MUTED,2,'7 5'))
    for g,col,dl in [('H2',BF,0),('CH4',FIELD,.5)]:
        s.append(f'<g data-anim="draw" data-dur="1.4" data-delay="{dl}">'+ax.curve(lambda p,g=g:Zg(g,p),1,800,col=col,w=4)+'</g>')
    s.append(T(392,ax.Y(Zg('H2',800))-12,mix='$\\ce{H2}$',size=20,anchor='end',fill=BF,halo=True))
    s.append(T(250,ax.Y(Zg('CH4',300))+34,mix='$\\ce{CH4}$',size=20,fill=FIELD,halo=True))
    s.append(T(410,ax.Y(1)-10,mix='이상 기체',size=19,anchor='end',fill=MUTED))
    s.append(T(36,46,tex='Z',size=22,anchor='start')); s.append(T(426,356,mix='압력 $P$',size=19,anchor='end',fill=MUTED))
    return svg((470,390),430,'실제 기체의 압축 인자 곡선(수소, 메테인)과 이상 기체 선',s,'fig cover-fig')

# 반데르발스 압축 인자 (0 ℃, atm). 상수는 표 Ⅱ-1(bar) → atm: a/1.01325
VDW={'H2':(0.2452,0.0265),'He':(0.0346,0.0238),'CH4':(2.303,0.0431),'O2':(1.382,0.0319),'CO2':(3.658,0.0429),'N2':(1.370,0.0387)}
RA=0.08206
def Zg(g,P,T=273.15):
    a,b=VDW[g]; a/=1.01325
    lo,hi=b*1.0001,max(RA*T/P*3,b*10)
    fn=lambda V:RA*T/(V-b)-a/V/V-P
    for _ in range(200):
        m=(lo+hi)/2
        if fn(m)>0: lo=m
        else: hi=m
    return P*m/(RA*T)
FIG['COVER_B']=cover_b()

def real_cond():
    s=[]
    s.append(R(10,20,200,170,FIELD,2.5,'#FFFFFF',10)); s.append(mol_box(10,20,200,170,5,51,r=9,arrow=20,fast=1.3))
    s.append(T(110,214,mix='낮은 압력·높은 온도',size=20,weight=700)); s.append(T(110,240,mix='→ 이상 기체에 가깝다',size=19,fill=FIELD))
    pts=[(270,70),(292,74),(282,96),(318,150),(340,148),(330,128),(372,84),(390,100),(300,170),(352,176),(262,140),(380,160)]
    s.append(R(250,20,160,170,PLUS,2.5,'#FFFFFF',10))
    s.append(mol_box(250,20,160,170,12,0,r=9,arrow=6,fast=.5,pts=pts))
    for i,j in [(0,1),(1,2),(3,4),(4,5),(6,7),(8,9)]:
        (x1,y1),(x2,y2)=pts[i],pts[j]; s.append(L(x1,y1,x2,y2,MUTED,1.5,'3 3'))
    s.append(T(330,214,mix='높은 압력·낮은 온도',size=20,weight=700)); s.append(T(330,240,mix='→ 인력에 붙들린다',size=19,fill=PLUS))
    return svg((420,252),420,'낮은 압력·높은 온도와 높은 압력·낮은 온도에서 기체 분자의 거리와 인력(점선)',s)
FIG['REAL']=real_cond()

def zgraph(w=560):
    s=[]; ax=Ax(80,330,470,290,800,2.2)
    xl=T(560,388,mix='압력 $P$ [atm]',size=19,anchor='end'); yl=T(22,34,mix='압축 인자 $Z$',size=19,anchor='start')
    s.append(ax.frame([0,200,400,600,800],[0,0.5,1.0,1.5,2.0],xl,yl,yfmt=lambda v:'0' if v==0 else f'{v:.1f}'))
    s.append(L(ax.X(0),ax.Y(1),ax.X(800),ax.Y(1),MUTED,2.5,'8 6')); s.append(T(ax.X(796),ax.Y(1)+26,mix='이상 기체',size=19,anchor='end',fill=MUTED,halo=True))
    lab={'H2':(640,28,'middle'),'He':(560,-16,'end'),'CH4':(500,-14,'end'),'O2':(330,30,'middle')}
    for i,(g,col,dash) in enumerate([('H2',BF,None),('He',EQUI,'10 5'),('CH4',FIELD,None),('O2',RD,'10 5')]):
        s.append(f'<g data-anim="draw" data-dur="1.3" data-delay="{i*.3}">'+ax.curve(lambda p,g=g:Zg(g,p),0.5,800,col=col,w=3.5,dash=dash)+'</g>')
        x,dy,an=lab[g]; s.append(T(ax.X(x),ax.Y(Zg(g,x))+dy,mix=f'$\\ce{{{g}}}$',size=20,fill=col,anchor=an,halo=True))
    return svg((580,398),w,'반데르발스 식으로 계산한 0 ℃에서 압력과 압축 인자: 수소, 헬륨, 메테인, 산소',s)
FIG['ZG']=zgraph()

def vdw_fig():
    out={}
    s=[R(10,20,250,190,INK,2.5,'#FFFFFF',6),R(260,20,16,190,GRAV,1.5,'#C9D3DD')]
    pts=[(80,70),(140,140),(70,170),(180,80),(120,100),(200,170)]
    for (x,y) in pts: s.append(gm(x,y,11))
    for (x,y) in [(150,110),(120,165),(200,140)]: s.append(L(x,y,232,118,MUTED,1.5,'3 3'))
    s.append(gm(232,118,11)); s.append(A(244,118,258,118,'plus',3))
    s.append(A(222,118,170,118,'muted',3)); s.append(T(190,104,mix='인력',size=19,fill=MUTED,halo=True))
    s.append(T(135,238,mix='벽에 부딪히는 힘이 약해진다',size=19))
    out['VDW_A']=svg((290,252),290,'벽 가까이 온 분자를 안쪽 분자들이 잡아당겨 충돌이 약해짐',s)
    s=[R(10,20,250,190,INK,2.5,'#FFFFFF',6)]
    for (x,y) in [(60,70),(130,60),(205,80),(90,150),(170,140),(220,180),(50,185)]:
        s.append(C(x,y,24,EQUI,1.5,EQUI,'4 3','fill-opacity=".14"')); s.append(gm(x,y,12))
    s.append(T(135,238,mix='분자 부피만큼 공간이 준다',size=19))
    out['VDW_B']=svg((290,252),290,'분자 자체 부피 때문에 다른 분자가 들어갈 수 없는 영역(점선 원)',s)
    return out
FIG.update(vdw_fig())

def cyl(x,lab,P,mols,seed):
    s=[f'<path d="M{x} 92 Q{x} 70 {x+30} 66 L{x+70} 66 Q{x+100} 70 {x+100} 92 L{x+100} 270 Q{x+100} 280 {x+90} 280 L{x+10} 280 Q{x} 280 {x} 270 Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2.5"/>']
    s.append(R(x+42,48,16,18,INK,1.5,'#C9D3DD')); s.append(C(x+50,30,20,INK,2,'#FFFFFF')); s.append(L(x+50,30,x+50+14*math.cos(math.radians(-90+P*45)),30+14*math.sin(math.radians(-90+P*45)),PLUS,2.5))
    s.append(T(x+76,36,tex=f'{P:.1f}\\ \\text{{atm}}',size=20,anchor='start'))
    rnd=random.Random(seed); placed=[]
    for el,n in mols:
        k=0
        while k<n:
            px,py=rnd.uniform(x+20,x+80),rnd.uniform(102,262)
            if all(math.hypot(px-a,py-b)>24 for a,b in placed):
                placed.append((px,py)); th=rnd.uniform(0,math.pi)
                dx,dy=7*math.cos(th),7*math.sin(th)
                s.append(f'<g data-anim="move" data-from="{f(rnd.uniform(-5,5))},{f(rnd.uniform(-5,5))}" data-rep="alt" data-dur="{f(1+rnd.random()*.6)}"><g data-atom="{f(px-dx)},{f(py-dy)},8,{el},-"></g><g data-atom="{f(px+dx)},{f(py+dy)},8,{el},-"></g></g>'); k+=1
    s.append(T(x+50,306,mix=lab,size=20))
    return ''.join(s)
def dalton():
    s=[cyl(10,'$\\ce{O2}$',2.0,[('O',4)],3),cyl(170,'$\\ce{N2}$',3.0,[('N',6)],5),cyl(330,'혼합 기체',5.0,[('O',4),('N',6)],7)]
    s.append(T(140,180,tex='+',size=30)); s.append(T(300,180,tex='=',size=30))
    return svg((500,320),460,'같은 부피·온도에서 산소 2.0 atm과 질소 3.0 atm을 한 용기에 넣으면 5.0 atm (분자 수 4 + 6 = 10)',s)
FIG['DALTON']=dalton()

def dumas():
    s=[]
    s.append(R(60,140,260,130,GLASS,2,WATER,8)); s.append(L(62,160,318,160,WATER_S,2))
    for bx in (110,160,230,280):
        s.append(f'<g data-anim="move" data-from="0,60" data-rep="loop" data-dur="1.4" data-delay="{f((bx%70)/70)}">'+C(bx,190,4,WATER_S,1.5,'#FFFFFF')+'</g>')
    # 둥근바닥 플라스크
    s.append(f'<path d="M176 40 L176 110 A52 52 0 1 0 204 110 L204 40 Z" fill="#FFFFFF" fill-opacity=".85" stroke="{GLASS}" stroke-width="2.5"/>')
    s.append(f'<path d="M170 40 L210 40 L208 30 L172 30 Z" fill="#C9D3DD" stroke="{MUTED}" stroke-width="1.5"/>')
    s.append(L(190,30,190,18,MUTED,1.5)); s.append(T(214,22,mix='작은 구멍',size=18,anchor='start',fill=MUTED))
    for (x,y) in [(178,170),(204,182),(186,138),(210,150),(168,150)]: s.append(C(x,y,6,BF,1.2,BF,extra='fill-opacity=".35"'))
    s.append(T(190,250,mix='증기',size=18,fill=BF))
    s.append(R(40,270,300,18,INK,1.5,'#C9D3DD',3)); s.append(T(190,312,mix='가열 장치 (불꽃 사용 금지)',size=18,fill=MUTED))
    s.append(R(272,60,12,130,GLASS,1.8,'#FFFFFF',6)); s.append(f'<rect x="275" y="110" width="6" height="78" fill="{PLUS}"/>')
    s.append(T(290,74,tex='T',size=20,anchor='start'))
    s.append(T(30,110,mix='끓는 물||중탕',size=19,anchor='start',fill=MUTED))
    return svg((380,322),360,'알루미늄 포일에 작은 구멍을 낸 플라스크를 끓는 물에 담가 아이소프로필 알코올을 모두 기화시키는 장치',s)
FIG['DUMAS']=dumas()

def timeline():
    s=[L(30,90,690,90,MUTED,3)]
    ev=[(1660,'보일','연소에 공기가||필수'),(1674,'메이오','연소에 관여하는||성분이 따로'),(1774,'프리스틀리','$\\ce{HgO}$를 가열 → 산소||(탈플로지스톤화 공기)'),(1777,'라부아지에','산소(oxygen)||이름 붙임'),(1787,'라부아지에','「화학물질 명명법」')]
    xs=[60,195,350,500,640]
    for i,((yr,who,what),x) in enumerate(zip(ev,xs)):
        s.append(f'<g data-anim="pop" data-o="{x},90" data-delay="{f(i*.25)}">'+C(x,90,9,INK,2,EQUI if who=='라부아지에' else '#FFFFFF')+'</g>')
        s.append(T(x,64,mix=f'{yr}',size=20,weight=700)); s.append(T(x,124,mix=who,size=20,weight=700))
        s.append(T(x,154,mix=what,size=18,fill=MUTED))
    return svg((720,210),720,'산소 발견과 명명의 역사: 보일, 메이오, 프리스틀리, 라부아지에',s)
FIG['TIMELINE']=timeline()

def q2fig():
    s=[R(10,60,70,90,FIELD,2.5,'#FFFFFF',6),R(110,40,90,110,MINUS,2.5,'#FFFFFF',6),R(260,20,130,130,INK,2.5,'#FFFFFF',6)]
    s.append(T(45,44,mix='$\\ce{O2}$',size=20)); s.append(T(45,110,tex='2\\ \\text{L}',size=20)); s.append(T(45,176,tex='3\\ \\text{atm}',size=19))
    s.append(T(155,28,mix='$\\ce{N2}$',size=20)); s.append(T(155,100,tex='3\\ \\text{L}',size=20)); s.append(T(155,176,tex='4\\ \\text{atm}',size=19))
    s.append(T(325,90,tex='6\\ \\text{L}',size=22)); s.append(T(325,176,tex='P=\\ ?',size=19))
    s.append(A(205,95,252,95,'ink',3))
    return svg((400,190),380,'산소 2 L 3 atm과 질소 3 L 4 atm을 6 L 용기에 함께 넣음',s)
FIG['Q2']=q2fig()

for d in 'ab':
    tpl=open(os.path.join(HERE,f'tpl_{d}.html'),encoding='utf-8').read()
    def rep(m):
        k=m.group(1)
        if k not in FIG: sys.exit('no fig '+k)
        return FIG[k]
    out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
    os.makedirs(os.path.dirname(OUT[d]),exist_ok=True)
    open(OUT[d],'w',encoding='utf-8').write(out); print('ok',d,len(out))
if '--z' in sys.argv:
    for g in VDW:
        print(g,[round(Zg(g,p),3) for p in (1,100,200,400,600,800)])
