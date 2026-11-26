# -*- coding: utf-8 -*-
"""고급화학 4-2-1 산 염기의 정의와 산과 염기의 세기 — 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다.
   extra_src.css를 extra.css로 복사하고 meta.json을 쓴다(실험실 없음 → labs.js 없음).
   python3 -I gen.py   (출력 경로 OUT — 이 덱 폴더만, assert로 막음)
   그래프는 calc.py 계산값(표 Ⅳ-5 맞춤, 약산 정확한 해, 바닷물 탄산 평형 모형)."""
import math, random, re, sys, os, shutil
from math import log10, sqrt
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
from calc import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FOLDER='4-2-1_산_염기의_정의와_산과_염기의_세기'
OUT=BASE+FOLDER+'/'
assert OUT=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-2-1_산_염기의_정의와_산과_염기의_세기/', OUT
os.makedirs(OUT,exist_ok=True); assert os.path.isdir(OUT) and OUT.rstrip('/').endswith(FOLDER), OUT
FIG={}
HL='#FFE45C'
ACID_F='#F8D3D8'; BASE_F='#D3E3F8'; HA_F='#E4E9EF'
UNI=['#C8102E','#E0262F','#EE4B2B','#F47B20','#F9A11B','#F7C51E','#E3D21F','#9CCB3B','#4CB848','#1FA37A','#1B9AAA','#2278B5','#3B5BA9','#4B3F97','#5A2D82']
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def mv(body,frm,**k): k['from']=frm; return an('move',body,**k)
def stp(body,g=None): return f'<g class="step"'+(f' data-g="{g}"' if g else '')+f'>{body}</g>'
def atom(x,y,r,el,lab=None):
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
RH,RO=18,24
def pol(cx,cy,d,ang): a=math.radians(ang); return cx+d*math.cos(a),cy+d*math.sin(a)
def molH(cx,cy,el,angs,rc=RO,rh=RH,d=30,lab=True,skip=()):
    """중심 원자 + H 여러 개 (H 먼저 그려 중심 원자가 위)"""
    o=''
    for i,a in enumerate(angs):
        if i in skip: continue
        x,y=pol(cx,cy,d,a); o+=atom(x,y,rh,'H',None if lab else '-')
    return o+atom(cx,cy,rc,el,None if lab else '-')
def chg(x,y,sign,size=26):
    return T(x,y,mix=('+' if sign>0 else '−'),size=size,weight=700,fill=PLUS if sign>0 else MINUS)
def ionc(x,y,r,sign,lab=None,size=18):
    o=C(x,y,r,PLUS if sign>0 else MINUS,2,ACID_F if sign>0 else BASE_F)
    if lab: o+=T(x,y+size*0.36,tex=lab,size=size)
    else: o+=T(x,y+8,mix=('+' if sign>0 else '−'),size=22,weight=700,fill=PLUS if sign>0 else MINUS)
    return o
def hamol(x,y,s=1.0):   # 이온화하지 않은 산 HA: A(회색) + H(흰)
    return C(x+5*s,y,11*s,INK,1.5,HA_F)+C(x-11*s,y-4*s,7*s,INK,1.5,'#FFFFFF')
def beaker(x,y,w,h,fill=WATER,lev=26):
    return R(x,y+lev,w,h-lev,'none',0,fill)+P([(x,y),(x,y+h),(x+w,y+h),(x+w,y)],GLASS,3)
def lone(x,y,ang,dist=27):
    """비공유 전자쌍 로브 (중심 x,y에서 ang 방향)"""
    cx,cy=pol(x,y,dist,ang)
    o=f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="12" ry="8" transform="rotate({f(ang)} {f(cx)} {f(cy)})" fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="1.5"/>'
    for s_ in (-1,1):
        px,py=pol(cx,cy,4.5,ang+90*s_); o+=C(px,py,2.6,INK,0,INK)
    return o
def curve_arrow(x1,y1,cx,cy,x2,y2,col=INK,w=3):
    """2차 베지에 굽은 화살표 (끝 화살촉은 data-arw로)"""
    # 끝 방향
    tx,ty=x2-cx,y2-cy; Ln=math.hypot(tx,ty); ux,uy=tx/Ln,ty/Ln
    bx,by=x2-ux*12,y2-uy*12
    path=f'<path d="M{f(x1)} {f(y1)} Q{f(cx)} {f(cy)} {f(bx)} {f(by)}" fill="none" stroke="{col}" stroke-width="{w}"/>'
    return path+A(bx-ux*2,by-uy*2,x2,y2,col if col.startswith('#')==False else 'ink',w)

# ═════ 1 표지 ═════
def cover():
    s=[]
    s.append(molH(150,110,'O',(232,128)))
    s.append(molH(330,110,'O',(52,-52)))
    s.append(T(240,118,mix='+',size=28,weight=700))
    s.append(T(150,178,tex='\\ce{H2O}',size=20)+T(330,178,tex='\\ce{H2O}',size=20))
    # ⇌ (세로, 정반응 field 아래로, 역반응 bfield 위로)
    s.append(A(232,192,232,250,'field',3)+A(250,250,250,192,'bfield',3))
    s.append(an('pop',molH(150,300,'O',(270,30,150))+chg(196,282,1),o='150,300',delay='.4'))
    s.append(an('pop',molH(330,300,'O',(0,))+chg(388,282,-1),o='330,300',delay='.7'))
    s.append(T(240,308,mix='+',size=28,weight=700))
    s.append(T(150,362,tex='\\ce{H3O+}',size=20,fill=PLUS)+T(330,362,tex='\\ce{OH-}',size=20,fill=MINUS))
    # pH 띠
    x0,y0,w=95,388,290; cw=w/15
    band=''.join(R(x0+i*cw,y0,cw+0.5,26,'none',0,UNI[i]) for i in range(15))
    s.append(an('scale',band,**{'from':'0,1','o':f'{x0},{y0}','dur':'1.4'}))
    s.append(R(x0,y0,w,26,INK,1.5))
    for v in (0,7,14): s.append(T(x0+(v+0.5)*cw,y0+50,tex=str(v),size=19))
    s.append(T(x0+3.5*cw,y0+50,mix='산성',size=18,fill=PLUS,weight=700)+T(x0+11.5*cw,y0+50,mix='염기성',size=18,fill=MINUS,weight=700))
    s.append(T(x0-6,y0+20,mix='pH',size=19,anchor='end',fill=MUTED))
    return svg((470,470),450,'물 분자 두 개가 양성자를 주고받아 하이드로늄 이온과 수산화 이온이 되는 모습과 pH 띠',s,'fig cover-fig')
FIG['COVER']=cover()

# ═════ 2 중단원 도입: 토양 pH 측정 ═════
def mid():
    s=[]
    bx,by,bw,bh=40,120,190,170
    s.append(beaker(bx,by,bw,bh,'#E9DCC6',30))
    rnd=random.Random(3)
    for i in range(16):
        x=bx+16+rnd.random()*(bw-32); y=by+bh-14-rnd.random()*40
        s.append(C(x,y,4+rnd.random()*3,'#8A6A44',1,'#B08A5A'))
    s.append(T(bx+bw/2,by+bh+30,mix='흙 + 증류수',size=19))
    # pH 측정기
    mx,my=270,60
    s.append(R(mx,my,150,110,INK,2.5,'#F4F6F8',10))
    s.append(R(mx+16,my+18,118,50,INK,1.5,'#DDE8D8',4))
    s.append(T(mx+75,my+54,mix='pH 6.2',size=24,weight=700))
    s.append(T(mx+75,my+96,mix='pH 측정기',size=18,fill=MUTED))
    # 전극(유리 전극)
    probe=P([(mx+40,my+110),(mx+40,my+140),(bx+bw-40,my+140),(bx+bw-40,by+20)],INK,2.5)
    probe+=R(bx+bw-50,by+20,20,110,GLASS,2,'#EEF3F7',6)
    s.append(mv(probe,'0,-40',dur='1.2',ease='out'))
    return svg((440,330),430,'흙을 증류수에 섞은 현탁액에 pH 측정기 전극을 넣어 pH를 재는 모습',s)
FIG['MID']=mid()

# ═════ 4 생각 열기: 유리관 속 흰 연기 고리 ═════
def tube():
    s=[]
    x0,x1,y0,y1=40,470,110,160
    s.append(R(x0,y0,x1-x0,y1-y0,GLASS,3,'#F7FAFC',22))
    s.append(R(x0+4,y0+6,46,y1-y0-12,'#B9A8A0',1.5,'#FFFFFF',10)+R(x1-50,y0+6,46,y1-y0-12,'#B9A8A0',1.5,'#FFFFFF',10))
    frac=1/(1+sqrt(36.5/17.0)); xr=x0+50+frac*(x1-x0-100)
    rnd=random.Random(11)
    for i in range(5):
        x=x0+70+i*((xr-30-x0-70)/4); y=122+(i%2)*24
        b=atom(x-6,y,7,'H','-')+atom(x+6,y,11,'Cl','-')
        s.append(mv(b,f'{-20-6*i},0',dur=f(1.6+0.1*i),ease='out'))
    for i in range(7):
        x=xr+34+i*((x1-70-xr-34)/6); y=124+(i%2)*22
        b=atom(x+9,y-7,7,'H','-')+atom(x+9,y+7,7,'H','-')+atom(x-10,y,7,'H','-')+atom(x,y,10,'N','-')
        s.append(mv(b,f'{24+5*i},0',dur=f(1.3+0.08*i),ease='out'))
    ring=f'<ellipse cx="{f(xr)}" cy="135" rx="14" ry="27" fill="#FFFFFF" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 3"/>'
    s.append(an('pop',ring,o=f'{f(xr)},135',delay='1.6'))
    s.append(A(xr,74,xr,104,'ink',2)+T(xr,64,mix='흰 연기 고리 $\\ce{NH4Cl(s)}$',size=19,weight=700))
    s.append(T(x0+26,y1+36,mix='진한 염산',size=19,weight=700)+T(x0+26,y1+60,tex='\\ce{HCl(g)}',size=19,fill=MUTED))
    s.append(T(x1-26,y1+36,mix='진한 암모니아수',size=19,weight=700,anchor='end')+T(x1-26,y1+60,tex='\\ce{NH3(g)}',size=19,fill=MUTED,anchor='end'))
    s.append(A(x0+110,y1+82,x0+170,y1+82,'ink',2.5)+A(x1-110,y1+82,x1-190,y1+82,'ink',2.5))
    s.append(T(x0+60,y1+118,mix='무거운 $\\ce{HCl}$은 느리게',size=18,anchor='start',fill=MUTED)+T(x1-20,y1+118,mix='가벼운 $\\ce{NH3}$는 빠르게',size=18,anchor='end',fill=MUTED))
    # 범례
    s.append(atom(70,30,7,'H','-')+T(82,36,tex='\\mathrm{H}',size=18,anchor='start')+atom(120,30,10,'N','-')+T(134,36,tex='\\mathrm{N}',size=18,anchor='start')+atom(176,30,11,'Cl','-')+T(192,36,tex='\\mathrm{Cl}',size=18,anchor='start'))
    return svg((510,300),510,'유리관 양 끝의 염산과 암모니아수에서 나온 기체가 만나 염산 쪽에 가까운 곳에 흰 연기 고리가 생긴다',s)
FIG['TUBE']=tube()

# ═════ 6 정의의 발전 연표 ═════
def hist():
    s=[]; y=92
    s.append(L(40,y,1060,y,MUTED,3)); s.append(A(980,y,1070,y,'muted',3))
    nodes=[(120,'라부아지에','18세기 말','산소를 포함한||물질의 일부'),
           (330,'리비히','1838년','금속과 치환할 수||있는 수소를 포함'),
           (540,'아레니우스','1884년','수용액에서||$\\ce{H+}$ · $\\ce{OH-}$를 냄'),
           (760,'브뢴스테드·라우리','1923년','양성자 주개·받개'),
           (970,'루이스','1923년','전자쌍 받개·주개')]
    for i,(x,nm,yr,key) in enumerate(nodes):
        col=[GRAV,GRAV,INK,INK,INK][i]
        g=C(x,y,12,col,3,'#FFFFFF')+T(x,y-48,mix=nm,size=21,weight=700)+T(x,y-22,mix=yr,size=18,fill=MUTED)+T(x,y+42,mix=key,size=18)
        s.append(an('pop',g,o=f'{x},{y}',delay=f(0.25*i)))
    s.append(T(1060,y+118,mix='적용 범위가 넓어짐 →',size=18,anchor='end',fill=MUTED))
    return svg((1100,220),1100,'라부아지에, 리비히, 아레니우스, 브뢴스테드와 라우리, 루이스로 이어지는 산 염기 정의의 발전',s)
FIG['HIST']=hist()

# ═════ 7 아레니우스: 두 수용액 ═════
def arr():
    s=[]
    for k,(bx,lab,ions) in enumerate(((30,'\\ce{HCl(aq)}',[('\\ce{H+}',1),('\\ce{Cl-}',-1)]),(280,'\\ce{NaOH(aq)}',[('\\ce{Na+}',1),('\\ce{OH-}',-1)]))):
        bw,bh,by=210,190,40
        s.append(beaker(bx,by,bw,bh))
        pos=[(bx+45,by+80),(bx+110,by+66),(bx+168,by+92),(bx+60,by+150),(bx+125,by+130),(bx+170,by+160)]
        for i,(x,y) in enumerate(pos):
            tex,sg=ions[i%2] if i<3 else ions[(i+1)%2]
            s.append(mv(ionc(x,y,23,sg,tex,17),f'{(-1)**i*5},{(-1)**(i//2)*4}',rep='alt',dur=f(1.1+0.12*i),ease='io'))
        s.append(T(bx+bw/2,by+bh+34,tex=lab,size=22))
    return svg((520,270),500,'염산에는 수소 이온과 염화 이온이, 수산화 나트륨 수용액에는 나트륨 이온과 수산화 이온이 있다',s)
FIG['ARR']=arr()

# ═════ 8 브뢴스테드·라우리: HCl + NH3 ═════
def bl():
    s=[]; y=120
    # HCl
    s.append(atom(60,y,RH,'H')+atom(98,y,29,'Cl'))
    s.append(T(80,y+70,tex='\\ce{HCl}',size=21)+T(80,y+98,mix='산',size=19,fill=PLUS,weight=700)+T(80,y+122,mix='양성자 주개',size=18,fill=PLUS))
    s.append(T(158,y+8,mix='+',size=28,weight=700))
    # NH3 (비공유 전자쌍 왼쪽)
    s.append(lone(240,y,180,30)+molH(240,y,'N',(0,118,-118)))
    s.append(T(245,y+70,tex='\\ce{NH3}',size=21)+T(245,y+98,mix='염기',size=19,fill=MINUS,weight=700)+T(245,y+122,mix='양성자 받개',size=18,fill=MINUS))
    s.append(f'<path d="M60 {y-24} Q130 {y-80} 205 {y-14}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="7 5"/>'+A(196,y-22,207,y-12,'ink',2.5))
    s.append(T(130,y-66,tex='\\ce{H+}',size=19,halo=True))
    s.append(A(318,y,368,y,'ink',3.5))
    # NH4+ + Cl-
    nh4=molH(450,y,'N',(-90,90,0),skip=())
    newH=mv(atom(420,y,RH,'H'),'150,0',dur='1.4',ease='io',delay='.4')
    s.append(newH+nh4+chg(492,y-36,1))
    s.append(atom(580,y,29,'Cl')+chg(612,y-30,-1))
    s.append(T(450,y+70,tex='\\ce{NH4+}',size=21)+T(580,y+70,tex='\\ce{Cl-}',size=21))
    return svg((640,260),640,'염화 수소의 수소 이온이 암모니아의 비공유 전자쌍 쪽으로 옮겨 가 암모늄 이온과 염화 이온이 된다',s)
FIG['BL']=bl()

# ═════ 9 루이스: 그림 Ⅳ-15 ═════
SZ=30
def ldots(x,y,dirs):
    o=''
    for d in dirs:
        if d in 'ud':
            yy=y+(-0.75 if d=='u' else 0.75)*SZ
            for s_ in (-1,1): o+=C(x+s_*0.18*SZ,yy,3.6,INK,0,INK)
        else:
            xx=x+(-0.70 if d=='l' else 0.70)*SZ
            for s_ in (-1,1): o+=C(xx,y+s_*0.18*SZ,3.6,INK,0,INK)
    return o
def lsym(x,y,sym,col=None): return T(x,y+0.36*SZ,tex=f'\\mathrm{{{sym}}}',size=SZ,fill=col)
def lbond(x1,y1,x2,y2,col=INK,w=2.5):
    dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; k=20
    return L(x1+ux*k,y1+uy*k,x2-ux*k,y2-uy*k,col,w)
def bf3(x,y,d=62):
    o=''
    for (fx,fy,dirs) in ((x,y-d,'ulr'),(x-d,y,'uld'),(x,y+d,'ldr')):
        o+=lbond(x,y,fx,fy)+lsym(fx,fy,'F')+ldots(fx,fy,dirs)
    return o+lsym(x,y,'B',BF)
def nh3(x,y,d=62,pair=True):
    o=''
    for (hx,hy) in ((x,y-d),(x+d,y),(x,y+d)):
        o+=lbond(x,y,hx,hy)+lsym(hx,hy,'H')
    if pair: o+=ldots(x,y,'l')
    return o+lsym(x,y,'N',BLUE_N)
BLUE_N='#2F4FB8'
def lewis():
    s=[]; y=140
    s.append(bf3(95,y)); s.append(nh3(215,y))
    s.append(T(155,y+10,mix='+',size=26,weight=700))
    # 굽은 화살표: N의 비공유 전자쌍 → B
    s.append(an('draw',f'<path d="M190 {y-10} Q160 {y-70} 118 {y-22}" fill="none" stroke="{INK}" stroke-width="3"/>',dur='.9'))
    s.append(A(126,y-34,116,y-18,'ink',3,extra='data-delay=".8"'))
    s.append(T(95,y+120,mix='산',size=20,fill=PLUS,weight=700)+T(95,y+144,mix='전자쌍 받개',size=18,fill=PLUS))
    s.append(T(215,y+120,mix='염기',size=20,fill=MINUS,weight=700)+T(215,y+144,mix='전자쌍 주개',size=18,fill=MINUS))
    s.append(A(300,y,356,y,'ink',3.5))
    pr=bf3(450,y)+nh3(552,y,pair=False)
    pr+=f'<rect x="{f(472)}" y="{f(y-12)}" width="58" height="24" rx="6" fill="{FIELD}" fill-opacity=".18" stroke="{FIELD}" stroke-width="1.5"/>'
    pr+=lbond(450,y,552,y,INK,3)
    s.append(an('pop',pr,o=f'500,{y}',delay='.9'))
    s.append(T(500,y+120,mix='첨가 생성물',size=20,weight=700)+T(500,y+144,mix='$\\ce{BF3NH3}$',size=18,fill=MUTED))
    return svg((640,300),640,'삼플루오린화 붕소의 붕소가 암모니아 질소의 비공유 전자쌍을 받아 첨가 생성물을 만든다',s)
FIG['LEWIS']=lewis()

# ═════ 10 세 정의 비교: 포함 관계 ═════
def venn():
    s=[]
    s.append(an('pop',f'<ellipse cx="250" cy="170" rx="235" ry="155" fill="#F1F3F7" stroke="{INK}" stroke-width="2.5"/>',o='250,170'))
    s.append(an('pop',f'<ellipse cx="215" cy="190" rx="165" ry="110" fill="#E3E9F0" stroke="{INK}" stroke-width="2.5"/>',o='215,190',delay='.3'))
    s.append(an('pop',f'<ellipse cx="185" cy="210" rx="95" ry="62" fill="#D3DCE6" stroke="{INK}" stroke-width="2.5"/>',o='185,210',delay='.6'))
    s.append(T(250,42,mix='루이스',size=21,weight=700)+T(215,104,mix='브뢴스테드·라우리',size=20,weight=700)+T(185,180,mix='아레니우스',size=19,weight=700))
    s.append(T(150,224,tex='\\ce{HCl}',size=20)+T(222,224,tex='\\ce{NaOH}',size=20))
    s.append(T(332,180,tex='\\ce{NH3}',size=20)+T(332,238,tex='\\ce{HS-}',size=20))
    s.append(T(415,140,tex='\\ce{BF3}',size=20)+T(418,214,tex='\\ce{Fe^3+}',size=20)+T(395,280,tex='\\ce{AlCl3}',size=20))
    return svg((500,340),480,'루이스 정의가 브뢴스테드·라우리 정의를, 브뢴스테드·라우리 정의가 아레니우스 정의를 포함한다',s)
FIG['VENN']=venn()

# ═════ 12 양성자 + 물 → 하이드로늄 이온 ═════
def h3o():
    s=[]; y=110
    s.append(C(60,y,10,PLUS,2,ACID_F)+T(60,y-22,tex='\\ce{H+}',size=20,fill=PLUS))
    s.append(T(98,y+8,mix='+',size=26,weight=700))
    s.append(lone(165,y,190,30)+molH(165,y,'O',(-52+0,52+0)))
    s.append(T(165,y+68,tex='\\ce{H2O}',size=20))
    s.append(A(222,y,272,y,'ink',3.5))
    newH=mv(atom(352,y+15,RH,'H'),'-210,-15',dur='1.3',ease='io',delay='.3')
    s.append(newH+molH(380,y,'O',(-90,30))+chg(426,y-30,1))
    s.append(T(380,y+68,tex='\\ce{H3O+}',size=20,fill=PLUS)+T(380,y+94,mix='하이드로늄 이온',size=18))
    return svg((460,220),440,'양성자가 물 분자의 비공유 전자쌍과 결합해 하이드로늄 이온이 된다',s)
FIG['H3O']=h3o()

# ═════ 13 물의 농도는 거의 일정 (로그 막대) ═════
def logbar():
    s=[]; x0,x1=150,480; lo,hi=-4,2
    X=lambda v:x0+(log10(v)-lo)/(hi-lo)*(x1-x0)
    for e in range(lo,hi+1):
        xx=x0+(e-lo)/(hi-lo)*(x1-x0)
        s.append(L(xx,40,xx,230,'#E2E7EC',1)+T(xx,256,tex=yt_l(e),size=18))
    rows=[('$[\\ce{H2O}]$',55.5,GRAV,'#E3E8EE','55.5 M'),('$[\\ce{CH3COOH}]_0$',0.10,INK,HA_F,'0.10 M'),('$[\\ce{H3O+}]$',1.33e-3,PLUS,ACID_F,'0.0013 M')]
    for i,(lab,v,c,fl,txt) in enumerate(rows):
        y=60+i*62
        s.append(T(x0-12,y+27,mix=lab,size=19,anchor='end'))
        s.append(an('scale',R(x0,y,X(v)-x0,36,c,2,fl,4),**{'from':'0,1','o':f'{x0},{y+18}','delay':f(0.3*i)}))
        s.append(T(X(v)+8,y+26,mix=txt,size=18,anchor='start'))
    s.append(L(x0,232,x1+8,232,MUTED,2))
    s.append(T(x1,290,mix='몰농도 [M] (로그 눈금)',size=18,anchor='end',fill=MUTED))
    return svg((560,300),520,'0.10 M 아세트산 수용액에서 물의 농도 55.5 M, 아세트산 0.10 M, 하이드로늄 이온 0.0013 M을 로그 눈금 막대로 비교',s)
def yt_l(e): return '10^{%d}'%e if e not in (0,1) else ('1' if e==0 else '10')
FIG['LOGBAR']=logbar()

# ═════ 14 짝산과 짝염기: 그림 Ⅳ-16 ═════
def conj():
    s=[]; y=140
    xs=[(70,'\\ce{H2S}','산',PLUS),(140,'+',None,None),(220,'\\ce{NH3}','염기',MINUS),(310,'\\ce{&lt;=&gt;}',None,None),(400,'\\ce{HS-}','짝염기',MINUS),(470,'+',None,None),(550,'\\ce{NH4+}','짝산',PLUS)]
    for x,t,lab,c in xs:
        if t=='+': s.append(T(x,y+8,mix='+',size=26,weight=700))
        else: s.append(T(x,y+8,tex=t,size=28))
        if lab: s.append(T(x,y+44,mix=lab,size=19,fill=c,weight=700))
    # 위 괄호: H2S – HS-
    top=P([(70,y-30),(70,y-62),(400,y-62),(400,y-30)],PLUS,2.5)
    s.append(an('draw',top,dur='.9'))
    s.append(T(235,y-74,mix='짝산과 짝염기 쌍 ①',size=19,weight=700,fill=PLUS)+T(70,y-74,mix='$\\ce{H+}$ 잃음',size=18,anchor='start',fill=MUTED))
    bot=P([(220,y+62),(220,y+96),(550,y+96),(550,y+62)],MINUS,2.5)
    s.append(an('draw',bot,dur='.9',delay='.6'))
    s.append(T(385,y+124,mix='짝산과 짝염기 쌍 ②',size=19,weight=700,fill=MINUS)+T(550,y+124,mix='$\\ce{H+}$ 얻음',size=18,anchor='end',fill=MUTED))
    return svg((620,280),600,'황화 수소와 암모니아의 반응에서 짝산과 짝염기 쌍 두 개',s)
FIG['CONJ']=conj()

# ═════ 17 세기와 농도 2×2 ═════
def grid4():
    s=[]
    rnd=random.Random(5)
    cells=[(0,0,'진한 강산',(0,7)),(1,0,'진한 약산',(9,1)),(0,1,'묽은 강산',(0,2)),(1,1,'묽은 약산',(3,1))]
    for cx,cy,nm,(nha,nion) in cells:
        bx=50+cx*250; by=40+cy*190; bw,bh=200,140
        s.append(beaker(bx,by,bw,bh,WATER,18))
        slots=[(bx+24+i*30+rnd.uniform(-4,4),by+42+j*30+rnd.uniform(-3,3)) for j in range(3) for i in range(6)]
        rnd.shuffle(slots); pts=slots[:nha+2*nion]
        k=0
        for i in range(nha): s.append(hamol(*pts[k])); k+=1
        for i in range(nion):
            s.append(ionc(*pts[k],11,1)); k+=1; s.append(ionc(*pts[k],11,-1)); k+=1
        s.append(T(bx+bw/2,by+bh+28,mix=nm,size=19,weight=700))
    s.append(T(150,26,mix='강산',size=21,weight=700)+T(400,26,mix='약산',size=21,weight=700))
    # 범례
    ly=440
    s.append(hamol(60,ly)+T(80,ly+7,tex='\\ce{HA}',size=21,anchor='start')+ionc(160,ly,11,1)+T(178,ly+7,tex='\\ce{H3O+}',size=21,anchor='start')+ionc(280,ly,11,-1)+T(298,ly+7,tex='\\ce{A-}',size=21,anchor='start')+T(490,ly+7,mix='(물 분자 생략)',size=20,anchor='end',fill=MUTED))
    return svg((500,460),440,'진한 강산, 진한 약산, 묽은 강산, 묽은 약산 수용액의 입자 모형',s)
FIG['GRID4']=grid4()

# ═════ 18 그림 Ⅳ-17 강산과 약산의 이온화 (막대) ═════
def ionbars():
    s=[]
    a=alpha(0.10,1.8e-5)
    for k,(x0,ttl,after,eq) in enumerate(((80,'(가) 강산',(0,1,1),'\\ce{HA + H2O -&gt; H3O+ + A-}'),(350,'(나) 약산',(1-a,a,a),'\\ce{HA + H2O &lt;=&gt; H3O+ + A-}'))):
        y0=240; hh=170
        s.append(L(x0,y0,x0+240,y0,MUTED,2))
        s.append(T(x0+125,26,mix=ttl,size=20,weight=700))
        def bar(x,v,fl,c,lab,dl):
            h_=max(v*hh,1.5)
            return an('scale',R(x,y0-h_,34,h_,c,2,fl),**{'from':'1,0','o':f'{x+17},{y0}','delay':dl})+T(x+17,y0+26,tex=lab,size=18)
        s.append(bar(x0+14,1,HA_F,INK,'\\ce{HA}','0'))
        s.append(T(x0+31,y0-hh-10,mix='이온화 전',size=18,fill=MUTED))
        s.append(A(x0+66,y0-90,x0+92,y0-90,'ink',2.5))
        for j,(v,fl,c,lab) in enumerate(((after[0],HA_F,INK,'\\ce{HA}'),(after[1],ACID_F,PLUS,'\\ce{H3O+}'),(after[2],BASE_F,MINUS,'\\ce{A-}'))):
            s.append(bar(x0+104+j*50,v,fl,c,lab,f(0.4+0.2*j)))
        s.append(T(x0+177,y0-hh-10,mix='이온화 후',size=18,fill=MUTED))
        s.append(T(x0+125,y0+62,tex=eq,size=18))
        if k==1: s.append(T(x0+171,y0-18,mix=f'{a*100:.1f} %',size=18,fill=PLUS))
    s.append(T(8,120,mix='상대적||몰수',size=18,anchor='start',fill=MUTED))
    return svg((620,320),600,'강산은 모두 이온화해 HA가 남지 않고, 약산(0.10 M 아세트산)은 1.3 %만 이온화한다',s)
FIG['IONBARS']=ionbars()

# ═════ 19 그림 Ⅳ-18 물의 자동 이온화 ═════
def autoion():
    s=[]
    s.append(lone(130,90,180,30)+molH(130,90,'O',(-52,52)))
    s.append(molH(320,90,'O',(232,128)))
    s.append(T(225,98,mix='+',size=26,weight=700))
    s.append(T(130,152,tex='\\ce{H2O(l)}',size=19)+T(320,152,tex='\\ce{H2O(l)}',size=19))
    s.append(T(130,176,mix='염기 ($\\ce{H+}$ 받음)',size=18,fill=MINUS)+T(320,176,mix='산 ($\\ce{H+}$ 줌)',size=18,fill=PLUS))
    s.append(A(216,196,216,248,'field',3)+A(234,248,234,196,'bfield',3))
    y=300
    newH=mv(atom(102,y+15,RH,'H'),'198,-225',dur='1.5',ease='io',delay='.3')
    s.append(newH+molH(130,y,'O',(-90,30))+chg(176,y-30,1))
    s.append(molH(320,y,'O',(0,))+chg(374,y-24,-1))
    s.append(T(225,y+8,mix='+',size=26,weight=700))
    s.append(T(130,y+62,tex='\\ce{H3O+(aq)}',size=19,fill=PLUS)+T(320,y+62,tex='\\ce{OH-(aq)}',size=19,fill=MINUS))
    return svg((450,380),450,'한 물 분자가 다른 물 분자에 양성자를 주어 하이드로늄 이온과 수산화 이온이 생긴다',s)
FIG['AUTOION']=autoion()

# ═════ 20 표 Ⅳ-5 중성인 물의 pH–온도 ═════
def kwt():
    s=[]; ax=Ax(70,300,330,250,60,7.6,xmin=0,ymin=6.4)
    s.append(ax.frame([0,20,40,60],[6.6,6.8,7.0,7.2,7.4,7.6],
        T(ax.x0+ax.w,ax.y0+54,mix='$t$ [°C]',size=20,anchor='end',fill=MUTED),
        T(ax.x0-6,ax.y0-ax.h-22,mix='중성인 물의 pH',size=20,anchor='start',fill=MUTED),
        yfmt=lambda v:'%.1f'%v,size=20))
    b,a0=kw_fit()
    fn=lambda t:-0.5*(a0+b/(t+273.15))/math.log(10)
    s.append(an('draw',ax.curve(fn,0,60,col=INK,w=3),dur='1.2'))
    s.append(L(ax.X(0),ax.Y(7.0),ax.X(60),ax.Y(7.0),MUTED,1.5,'6 5'))
    for i,(t,k) in enumerate(KWT):
        ph=-log10(sqrt(k*1e-14))
        s.append(an('pop',C(ax.X(t),ax.Y(ph),6,PLUS,2,'#FFFFFF'),o=f'{f(ax.X(t))},{f(ax.Y(ph))}',delay=f(0.15*i)))
    s.append(T(ax.X(60),ax.Y(6.51)-16,mix='60 °C: 6.51',size=20,anchor='end',fill=PLUS,halo=True))
    s.append(T(ax.X(0)+12,ax.Y(7.47)+30,mix='0 °C: 7.47',size=20,anchor='start',fill=PLUS,halo=True))
    return svg((430,370),430,'온도가 높아질수록 중성인 물의 pH가 7.47에서 6.51로 낮아진다',s)
FIG['KWT']=kwt()

# ═════ 21 pH 척도 ═════
def phscale():
    s=[]; x0,w,y0=110,950,150; cw=w/14
    X=lambda v:x0+v*cw
    for i in range(14): s.append(R(X(i),y0,cw+0.5,34,'none',0,UNI[i] if i<7 else UNI[i+1]))
    s.append(R(x0,y0,w,34,INK,1.5))
    for v in range(15):
        s.append(L(X(v),y0+34,X(v),y0+42,MUTED,1.5)+T(X(v),y0+64,tex=str(v),size=19))
        if v%2==0: s.append(T(X(v),y0+100,tex=yt_l(-v),size=18,fill=PLUS))
    s.append(T(x0-14,y0+64,mix='pH',size=19,anchor='end')+T(x0-14,y0+100,mix='$[\\ce{H3O+}]$',size=18,anchor='end',fill=PLUS))
    items=[(1.5,'위액'),(2.3,'레몬즙'),(2.9,'식초'),(5.0,'커피'),(7.0,'순수한 물'),(7.4,'혈액'),(8.1,'바닷물'),(10.0,'비눗물'),(11.6,'암모니아수'),(13.5,'하수구 세척제')]
    for i,(v,nm) in enumerate(items):
        hy=y0-14-(i%2)*44
        s.append(an('pop',P([(X(v),y0-2),(X(v)-7,y0-14),(X(v)+7,y0-14)],INK,1,INK,close=True)+L(X(v),y0-14,X(v),hy+6,MUTED,1.2)+T(X(v),hy,mix=nm,size=18,halo=True),o=f'{f(X(v))},{y0}',delay=f(0.1*i)))
    s.append(T(X(3),y0+136,mix='← 산성',size=19,fill=PLUS,weight=700)+T(X(7),y0+136,mix='중성 (25 °C)',size=19,weight=700)+T(X(11),y0+136,mix='염기성 →',size=19,fill=MINUS,weight=700))
    return svg((1100,300),1100,'pH 척도와 생활 속 물질의 대략적인 pH, 그리고 하이드로늄 이온 농도',s)
FIG['PHSCALE']=phscale()

# ═════ 23 같은 0.5 M: 염산과 아스코르브산 ═════
def hclvc():
    s=[]; x0,y0,h=110,300,250; lo,hi=-4,0
    Y=lambda v:y0-(log10(v)-lo)/(hi-lo)*h
    for e in range(lo,hi+1):
        s.append(L(x0,Y(10**e),x0+300,Y(10**e),'#E2E7EC',1)+T(x0-10,Y(10**e)+6,tex=yt_l(e),size=18,anchor='end'))
    s.append(L(x0,y0,x0+310,y0,MUTED,2)+L(x0,y0,x0,y0-h-8,MUTED,2))
    s.append(L(x0,Y(0.5),x0+300,Y(0.5),INK,1.5,'7 5')+T(x0+300,Y(0.5)-10,mix='넣은 산 0.5 M',size=18,anchor='end',fill=MUTED))
    for i,(x,v,lab,ph) in enumerate(((150,0.5,'염산','pH 0.30'),(260,10**-2.65,'아스코르브산','pH 2.65'))):
        s.append(an('scale',R(x-26,Y(v),52,y0-Y(v),PLUS,2,ACID_F),**{'from':'1,0','o':f'{x},{y0}','delay':f(0.3*i)}))
        s.append(T(x,y0+28,mix=lab,size=19,weight=700)+T(x,Y(v)-12,mix=ph,size=18,fill=PLUS,halo=True))
    s.append(T(x0+4,y0-h-16,mix='$[\\ce{H3O+}]$ [M] (로그 눈금)',size=18,anchor='start',fill=MUTED))
    return svg((440,340),420,'같은 0.5 M에서 염산의 하이드로늄 이온 농도는 0.50 M, 아스코르브산은 0.0022 M이다',s)
FIG['HCLVC']=hclvc()

# ═════ 24 그림 Ⅳ-19 산과 염기의 세기와 pKa ═════
def pka():
    s=[]; ax_x=270; top,bot=100,470; lo,hi=-2,16
    Y=lambda v:top+(v-lo)/(hi-lo)*(bot-top)
    s.append(L(ax_x,top-10,ax_x,bot+10,MUTED,2))
    for v in range(-2,17,2):
        s.append(L(ax_x-6,Y(v),ax_x+6,Y(v),MUTED,1.5)+T(ax_x+12,Y(v)+6,tex=str(v) if v>=0 else '-2',size=19,anchor='start',fill=MUTED))
    s.append(T(ax_x,top-62,mix='$\\mathrm{p}K_\\mathrm{a}$',size=20))
    rows=[(None,'\\ce{HCl}','\\ce{Cl-}','약 −7'),(0,'\\ce{H3O+}','\\ce{H2O}',None),(2.0,'\\ce{HSO4-}','\\ce{SO4^2-}',None),(3.2,'\\ce{HF}','\\ce{F-}',None),(7.2,'\\ce{HSO3-}','\\ce{SO3^2-}',None),(9.3,'\\ce{NH4+}','\\ce{NH3}',None),(11.6,'\\ce{H2O2}','\\ce{HO2-}',None),(14.0,'\\ce{H2O}','\\ce{OH-}',None),('b','\\ce{H2}','\\ce{H-}','약 35')]
    for v,acid,base,note in rows:
        if v is None: y=top-38
        elif v=='b': y=bot+30
        else: y=Y(v)
        s.append(L(160,y,ax_x-8,y,'#C9D3DD',1,'3 4')+L(ax_x+40,y,380,y,'#C9D3DD',1,'3 4'))
        s.append(T(150,y+7,tex=acid,size=20,anchor='end')+T(390,y+7,tex=base,size=20,anchor='start'))
        if note: s.append(T(ax_x+40,y+7,mix=note,size=18,anchor='start',fill=MUTED))
    s.append(an('draw',A(40,bot,40,top,'plus',5),dur='1'))
    s.append(T(24,top-48,mix='산의 세기',size=19,anchor='start',fill=PLUS,weight=700))
    s.append(an('draw',A(520,top,520,bot,'minus',5),dur='1',delay='.4'))
    s.append(T(540,bot+38,mix='염기의 세기',size=19,anchor='end',fill=MINUS,weight=700))
    s.append(T(150,26,mix='산',size=20,weight=700,fill=PLUS,anchor='end')+T(390,26,mix='짝염기',size=20,weight=700,fill=MINUS,anchor='start'))
    return svg((560,520),520,'pKa가 작을수록 강한 산이고, 그 짝염기는 약하다',s)
FIG['PKA']=pka()

# ═════ 25 약염기 NH3 + H2O ═════
def kb():
    s=[]; y=110
    s.append(lone(70,y,0,30)+molH(70,y,'N',(180,62,-62)))
    s.append(T(70,y+70,tex='\\ce{NH3}',size=20)+T(70,y+96,mix='염기',size=19,fill=MINUS,weight=700))
    s.append(T(132,y+8,mix='+',size=26,weight=700))
    s.append(molH(200,y,'O',(232,128)))
    s.append(T(200,y+70,tex='\\ce{H2O}',size=20)+T(200,y+96,mix='산',size=19,fill=PLUS,weight=700))
    s.append(T(274,y+4,tex='\\ce{&lt;=&gt;}',size=26))
    newH=mv(atom(380,y,RH,'H'),'-198,-24',dur='1.4',ease='io',delay='.3')
    s.append(newH+molH(410,y,'N',(-90,90,0))+chg(452,y-36,1))
    s.append(molH(530,y,'O',(0,))+chg(584,y-24,-1))
    s.append(T(410,y+70,tex='\\ce{NH4+}',size=20)+T(410,y+96,mix='짝산',size=19,fill=PLUS,weight=700))
    s.append(T(540,y+70,tex='\\ce{OH-}',size=20)+T(540,y+96,mix='짝염기',size=19,fill=MINUS,weight=700))
    return svg((620,230),600,'암모니아가 물에서 양성자를 받아 암모늄 이온과 수산화 이온이 된다',s)
FIG['KB']=kb()

# ═════ 26 pKa + pKb = 14 막대 ═════
def pksum():
    s=[]; x0,w=20,480; X=lambda v:x0+v/14*w
    for v in range(0,15,2): s.append(L(X(v),30,X(v),200,'#E2E7EC',1)+T(X(v),224,tex=str(v),size=19))
    s.append(L(x0,200,x0+w+6,200,MUTED,2))
    rows=[('\\ce{NH4+}/\\ce{NH3}',-log10(KW/1.8e-5)),('\\ce{CH3COOH}/\\ce{CH3COO-}',-log10(1.8e-5))]
    for i,(lab,pk) in enumerate(rows):
        y=58+i*84
        s.append(T(x0,y-10,tex=lab,size=19,anchor='start'))
        s.append(an('scale',R(x0,y,X(pk)-x0,38,PLUS,2,ACID_F),**{'from':'0,1','o':f'{x0},{y+19}','delay':f(0.4*i)}))
        s.append(an('scale',R(X(pk),y,x0+w-X(pk),38,MINUS,2,BASE_F),**{'from':'0,1','o':f'{f(x0+w)},{y+19}','delay':f(0.4*i+0.2)}))
        s.append(T((x0+X(pk))/2,y+27,mix=f'p$K_\\mathrm{{a}}$ {pk:.2f}',size=19)+T((X(pk)+x0+w)/2,y+27,mix=f'p$K_\\mathrm{{b}}$ {14-pk:.2f}',size=19))
    s.append(T(x0+w,262,mix='합 = 14.00 (25 °C)',size=19,anchor='end',weight=700))
    return svg((520,275),520,'암모늄 이온과 암모니아, 아세트산과 아세트산 이온에서 pKa와 pKb의 합은 14.00',s)
FIG['PKSUM']=pksum()

# ═════ 29 이온화도와 농도 ═════
def alph():
    s=[]; ax=Ax(90,300,380,250,0,40,xmin=-4,ymin=0)
    s.append(ax.frame([-4,-3,-2,-1,0],[10,20,30,40],
        T(ax.x0+ax.w,ax.y0+52,mix='처음 농도 $C$ [M] (로그 눈금)',size=18,anchor='end',fill=MUTED),
        T(ax.x0-6,ax.y0-ax.h-22,mix='이온화도 $\\alpha$ [%]',size=18,anchor='start',fill=MUTED),
        xfmt=lambda v:yt_l(v)))
    s.append(an('draw',ax.curve(lambda e:100*alpha(10**e,1.8e-5),-4,0,col=INK,w=3.5),dur='1.2'))
    s.append(L(ax.X(-4),ax.Y(5),ax.X(0),ax.Y(5),EQUI,2,'8 5')+T(ax.X(-3.95),ax.Y(5)-10,mix='5 %',size=18,anchor='start',fill=EQUI,halo=True))
    for i,e in enumerate((0,-1,-2,-3)):
        a_=100*alpha(10**e,1.8e-5)
        s.append(an('pop',C(ax.X(e),ax.Y(a_),6,PLUS,2,'#FFFFFF'),o=f'{f(ax.X(e))},{f(ax.Y(a_))}',delay=f(0.8+0.15*i)))
        s.append(T(ax.X(e)+{0:-10,-1:0}.get(e,10),ax.Y(a_)-{0:30,-1:20}.get(e,14),mix=f'{a_:.1f} %',size=18,anchor={0:'end',-1:'middle'}.get(e,'start'),halo=True))
    return svg((500,370),470,'아세트산을 묽힐수록 이온화도가 커진다',s)
FIG['ALPHA']=alph()

# ═════ 31 헨더슨·하셀발흐: 아세트산 분율 ═════
def hh():
    s=[]; pKa=-log10(1.8e-5)
    ax=Ax(90,290,400,240,8,1,xmin=1,ymin=0)
    s.append(ax.frame([1,2,3,4,5,6,7,8],[0,0.5,1],
        T(ax.x0+ax.w,ax.y0+52,mix='pH',size=19,anchor='end',fill=MUTED),
        T(ax.x0-6,ax.y0-ax.h-22,mix='분율',size=19,anchor='start',fill=MUTED),yfmt=lambda v:{0:'0',0.5:'0.5',1:'1'}[v]))
    s.append(an('draw',ax.curve(lambda p:1-frac_base(p,pKa),1,8,col=PLUS,w=3.5),dur='1.2'))
    s.append(an('draw',ax.curve(lambda p:frac_base(p,pKa),1,8,col=MINUS,w=3.5,dash='10 6'),dur='1.2',delay='.3'))
    s.append(T(ax.X(1.3),ax.Y(0.92),mix='$\\ce{CH3COOH}$',size=19,anchor='start',fill=PLUS,halo=True))
    s.append(T(ax.X(7.9),ax.Y(0.92),mix='$\\ce{CH3COO-}$',size=19,anchor='end',fill=MINUS,halo=True))
    px,py=ax.X(pKa),ax.Y(0.5)
    s.append(L(px,py,px,ax.y0,EQUI,2,'6 4'))
    s.append(an('pop',C(px,py,8,INK,2,EQUI),o=f'{f(px)},{f(py)}',delay='1.3'))
    s.append(T(px+14,py-14,mix='pH = p$K_\\mathrm{a}$ = 4.74',size=19,anchor='start',fill=EQUI,weight=700,halo=True))
    return svg((520,360),500,'아세트산 수용액에서 pH에 따른 아세트산과 아세트산 이온의 분율, 두 곡선은 pH 4.74에서 만난다',s)
FIG['HH']=hh()

# ═════ 33 탐구: 바다의 이산화 탄소 평형 ═════
def sea():
    s=[]
    s.append(R(0,0,560,90,'none',0,'#F2F7FB'))
    s.append(R(0,90,560,330,'none',0,'#DDEEF8')+L(0,90,560,90,'#7FB0D6',3))
    for i,x in enumerate((70,170,290,410,500)):
        g=atom(x-17,60,10,'O','-')+atom(x+17,60,10,'O','-')+atom(x,60,11,'C','-')
        s.append(mv(g,'0,-14',rep='alt',dur=f(1.2+0.1*i),ease='io'))
    s.append(T(552,24,mix='대기 $\\ce{CO2}$ 280 → 413 ppm',size=18,anchor='end',weight=700))
    s.append(mv(atom(103,130,10,'O','-')+atom(137,130,10,'O','-')+atom(120,130,11,'C','-'),'0,-70',dur='1.6',ease='io',delay='.3'))
    s.append(A(120,74,120,110,'ink',2.5))
    lines=['① $\\ce{CO2(g) &lt;=&gt; CO2(aq)}$','② $\\ce{CO2(aq) + H2O(l) &lt;=&gt; H2CO3(aq)}$','③ $\\ce{H2CO3(aq) + H2O(l) &lt;=&gt; HCO3^-(aq) + H3O+(aq)}$','④ $\\ce{CO3^2-(aq) + H3O+(aq) -&gt; HCO3^-(aq) + H2O(l)}$','⑤ $\\ce{CaCO3(s) &lt;=&gt; Ca^2+(aq) + CO3^2-(aq)}$']
    for i,t in enumerate(lines):
        s.append(T(20 if i else 170,(136 if i==0 else 136+i*50),mix=t,size=18,anchor='start'))
    # 조개껍데기
    sh=f'<path d="M430 400 Q470 340 510 400 Z" fill="#F3E9DA" stroke="{INK}" stroke-width="2"/>'+''.join(L(470,350+0*k,440+k*14,398,INK,1) for k in range(5))
    s.append(sh+T(410,404,tex='\\ce{CaCO3}',size=18,anchor='end'))
    s.append(atom(30,398,11,'C','-')+T(46,404,tex='\\mathrm{C}',size=18,anchor='start')+atom(80,398,10,'O','-')+T(95,404,tex='\\mathrm{O}',size=18,anchor='start'))
    return svg((560,420),540,'대기의 이산화 탄소가 바닷물에 녹아 탄산이 되고, 하이드로늄 이온이 생기며, 탄산 이온과 탄산 칼슘 껍데기에 영향을 준다',s)
FIG['SEA']=sea()

# ═════ 34 탐구: 모형으로 본 해수 pH ═════
def ocean_fig():
    s=[]; ax=Ax(90,300,400,240,1200,8.3,xmin=200,ymin=7.5)
    s.append(ax.frame([200,400,600,800,1000,1200],[7.7,7.9,8.1,8.3],
        T(ax.x0+ax.w,ax.y0+52,mix='대기 $\\ce{CO2}$ [ppm]',size=19,anchor='end',fill=MUTED),
        T(ax.x0-6,ax.y0-ax.h-22,mix='표층 해수의 pH (모형)',size=19,anchor='start',fill=MUTED),yfmt=lambda v:'%.1f'%v))
    s.append(an('draw',ax.curve(lambda p:ocean(p)[0],220,1200,n=120,col=INK,w=3.5),dur='1.3'))
    pts=[(280,'1850년',PLUS,'start',14,-10),(413,'2020년',PLUS,'start',14,-12),(600,'2100년 중간 배출',EQUI,'start',14,-14),(1100,'2100년 높은 배출',MINUS,'end',-10,30)]
    for i,(p,lab,c,anc,dx,dy) in enumerate(pts):
        ph=ocean(p)[0]; x,y=ax.X(p),ax.Y(ph)
        s.append(an('pop',C(x,y,7,c,2.5,'#FFFFFF'),o=f'{f(x)},{f(y)}',delay=f(1.0+0.2*i)))
        s.append(T(x+dx,y+dy,mix=f'{lab} {ph:.2f}',size=18,anchor=anc,fill=c,weight=700,halo=True))
    return svg((520,370),500,'대기 이산화 탄소 농도가 높아질수록 모형으로 계산한 표층 해수의 pH가 낮아진다',s)
FIG['OCEAN']=ocean_fig()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=set(FIG)-set(re.findall(r'\{\{(\w+)\}\}',tpl))
if unused: print('unused figs',unused)
open(OUT+'slides.html','w',encoding='utf-8').write(out)
shutil.copy(os.path.join(HERE,'extra_src.css'),OUT+'extra.css')
open(OUT+'meta.json','w',encoding='utf-8').write('{"title": "산 염기의 정의와 산과 염기의 세기", "file": "4-2-1_산_염기의_정의와_산과_염기의_세기", "header": "Ⅳ-2-1 산 염기의 정의와 산과 염기의 세기 (고등 고급 화학 209–217쪽)"}\n')
print('ok',len(out),'sections',out.count('<section'),'anim',out.count('data-anim'))
