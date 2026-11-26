# -*- coding: utf-8 -*-
"""고급화학 4-2-3 염 용액의 성질과 중화 반응 (a/b) — 그림 생성: tpl_a.html·tpl_b.html의 {{KEY}}를 SVG로 바꿔 두 덱의 slides.html을 만든다.
   labs_src.js를 두 덱 labs.js로 나눠 쓰고(a: ac423titr, b: ac423buf), extra_src.css → extra.css, meta.json을 쓴다.
   python3 -I gen.py   (출력 경로 OUT_A/OUT_B — 이 덱 두 폴더만, assert로 막음)
   적정 곡선·완충 곡선은 모두 calc.py의 전하 균형 정확 해(근사 없음)."""
import math, random, re, sys, os, shutil
from math import log10, sqrt
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from h import *
from calc import *
BASE='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/'
FA='4-2-3_염_용액의_성질과_중화_반응a'; FB='4-2-3_염_용액의_성질과_중화_반응b'
OUT_A=BASE+FA+'/'; OUT_B=BASE+FB+'/'
assert OUT_A=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-2-3_염_용액의_성질과_중화_반응a/', OUT_A
assert OUT_B=='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/4-2-3_염_용액의_성질과_중화_반응b/', OUT_B
for o,fd in ((OUT_A,FA),(OUT_B,FB)):
    os.makedirs(o,exist_ok=True); assert os.path.isdir(o) and o.rstrip('/').endswith(fd), o
FIG={}
HL='#FFE45C'
ACID_F='#F8D3D8'; BASE_F='#D3E3F8'; HA_F='#E4E9EF'; SPEC_F='#EEF0F2'
BTB_G='#4FA86B'; BTB_Y='#E3C83A'; BTB_B='#2F6DB5'
MO_R='#D93A2B'; MO_Y='#F2C230'; PP_0='#FFFFFF'; PP_P='#E0409A'
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def mv(body,frm,**k): k['from']=frm; return an('move',body,**k)
def stp(body,g=None): return f'<g class="step"'+(f' data-g="{g}"' if g else '')+f'>{body}</g>'
def atom(x,y,r,el,lab='-'):
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def sgn(x,y,s,size=22,col=None):
    return T(x,y,mix=('+' if s>0 else '−'),size=size,weight=700,fill=col or (PLUS if s>0 else MINUS))
def beaker(x,y,w,h,fill=WATER,lev=26,op=1):
    return R(x,y+lev,w,h-lev,'none',0,fill,extra=f'fill-opacity="{op}"' if op!=1 else '')+P([(x,y),(x,y+h),(x+w,y+h),(x+w,y)],GLASS,3)
# ── 입자 (4-2-1 약속 + 이 덱): HA 회색 A + 흰 H, A⁻ 회색 + minus 테, H₃O⁺·OH⁻·H₂O·NH₄⁺·NH₃는 data-atom(라벨 없음 + 범례), 구경꾼 이온 grav
def p_HA(x,y): return C(x+5,y,11,INK,1.5,HA_F)+atom(x-11,y-4,7,'H')
def p_A(x,y): return C(x,y,11,MINUS,2.2,HA_F)+sgn(x+15,y-6,-1,18)
def p_H2O(x,y,a=0):
    o=''
    for d in (-52,52):
        t=math.radians(a+180+d); o+=atom(x+13*math.cos(t),y+13*math.sin(t),7,'H')
    return o+atom(x,y,10,'O')
def p_H3O(x,y):
    o=''.join(atom(x+13*math.cos(math.radians(t)),y+13*math.sin(math.radians(t)),7,'H') for t in (90,210,330))
    return o+atom(x,y,10,'O')+sgn(x+20,y-12,1,18)
def p_OH(x,y): return atom(x+12,y-6,7,'H')+atom(x,y,10,'O')+sgn(x-17,y-10,-1,18)
def p_NH4(x,y):
    o=''.join(atom(x+13*math.cos(math.radians(t)),y+13*math.sin(math.radians(t)),7,'H') for t in (45,135,225,315))
    return o+atom(x,y,10,'N')+sgn(x+21,y-13,1,18)
def p_NH3(x,y):
    o=''.join(atom(x+13*math.cos(math.radians(t)),y+13*math.sin(math.radians(t)),7,'H') for t in (90,210,330))
    return o+atom(x,y,10,'N')
def p_spec(x,y,s,lab=None):
    return C(x,y,10,GRAV,1.8,SPEC_F)+sgn(x,y+7,s,18,GRAV)
def legend(x,y,items,gap=None,size=18):
    """items: (그림함수 문자열, tex) — 가로로"""
    o=''; cx=x
    for fig,tex,w in items:
        o+=fig(cx,y)+T(cx+28,y+6,tex=tex,size=size,anchor='start'); cx+=w
    return o
def lab_txt(x,y,s,size=18,anchor='middle',fill=None,weight=None,halo=False): return T(x,y,mix=s,size=size,anchor=anchor,fill=fill,weight=weight,halo=halo)
def num(v,d=2): return f'{v:.{d}f}'

# 적정 곡선 공용 ───────────────────────────────
def curve_pts(fn,ax,a,b,n=500):
    pts=[]
    for i in range(n+1):
        v=a+(b-a)*i/n; p=fn(v); pts.append((ax.X(v),ax.Y(min(max(p,ax.ymin),ax.ymax))))
    return pts
def tframe(ax,xt,yt=(0,2,4,6,8,10,12,14),xlab='$V_{\\ce{NaOH}}$ [mL]',size=18):
    return ax.frame(list(xt),list(yt),T(ax.x0+ax.w+6,ax.y0+50,mix=xlab,size=19,anchor='end',fill=MUTED),
                    T(ax.x0-8,ax.y0-ax.h-20,tex='\\text{pH}',size=19,anchor='start',fill=MUTED),size=size)
def dot(x,y,col,r=7,fill=None,delay=None):
    b=C(x,y,r,col,2.5,fill or col)
    return an('pop',b,o=f'{f(x)},{f(y)}',delay=delay or '1.2',dur='.45')
def circ_no(x,y,n,col=INK):
    return C(x,y,13,col,2,'#FFFFFF')+T(x,y+6.5,mix=str(n),size=18,weight=700,fill=col)
SW=lambda V: titr_strong(V)
WK=lambda V: titr_weak(V)

# ═════ A1 표지 ═════
def cover_a():
    s=[]; ax=Ax(100,370,300,260,80,14)
    s.append(tframe(ax,(0,20,40,60,80)))
    v1,v2=50/11,500/11
    s.append(R(ax.X(v1),ax.Y(14),ax.X(v2)-ax.X(v1),ax.h,'none',0,FIELD,extra='fill-opacity=".15"'))
    s.append(T((ax.X(v1)+ax.X(v2))/2,ax.Y(13.1),mix='완충 구간',size=18,fill=FIELD,weight=700))
    s.append(an('draw',P(curve_pts(SW,ax,0,80),MUTED,2.5,dash='10 6'),dur='1.2'))
    s.append(an('draw',P(curve_pts(WK,ax,0,80),INK,3.5),dur='1.6',delay='.3'))
    xe,ye=ax.X(50),ax.Y(WK(50)); xh,yh=ax.X(25),ax.Y(WK(25))
    s.append(dot(xe,ye,PLUS,delay='1.6')+dot(xh,yh,EQUI,delay='1.8'))
    s.append(T(xe+14,ye+6,mix='당량점',size=19,anchor='start',fill=PLUS,weight=700,halo=True))
    s.append(T(xh,yh+34,mix='pH = p$K_\\mathrm{a}$',size=19,fill=EQUI,weight=700,halo=True))
    s.append(T(ax.X(78),ax.Y(SW(78))+30,mix='강산',size=18,anchor='end',fill=MUTED)+T(ax.X(14),ax.Y(WK(14))-14,mix='약산',size=18,anchor='middle',weight=700))
    return svg((480,480),480,'약산을 강염기로 적정한 곡선: 완충 구간, 반당량점에서 pH가 pKa와 같고 당량점의 pH가 7보다 크다. 강산 곡선을 점선으로 겹쳤다',s,cls='fig cover-fig')
FIG['COVER_A']=cover_a()

# ═════ A3 생각 열기: BTB 세 비커 ═════
def btb3():
    s=[]; items=[('\\ce{NaCl(aq)}',BTB_G,'초록'),('\\ce{NH4Cl(aq)}',BTB_Y,'노랑'),('\\ce{CH3COONa(aq)}',BTB_B,'파랑')]
    for i,(tex,col,nm) in enumerate(items):
        x=30+i*175; y=40; w,h=130,170
        s.append(R(x,y+40,w,h-40,'none',0,BTB_G,extra='fill-opacity=".85"'))
        if col!=BTB_G: s.append(an('fade',R(x,y+40,w,h-40,'none',0,col),delay=f(0.6+0.5*i),dur='1.0'))
        s.append(P([(x,y),(x,y+h),(x+w,y+h),(x+w,y)],GLASS,3))
        s.append(T(x+w/2,y+h+30,tex=tex,size=19))
        s.append(T(x+w/2,y+h+58,mix=f'BTB → {nm}',size=19,weight=700,fill=INK))
    s.append(T(285,24,mix='같은 농도(0.1 M)의 염 수용액에 BTB 용액을 떨어뜨림',size=18,fill=MUTED))
    return svg((560,290),540,'BTB 용액을 넣으면 염화 나트륨 수용액은 초록, 염화 암모늄 수용액은 노랑, 아세트산 나트륨 수용액은 파랑을 띤다',s)
FIG['BTB3']=btb3()

# ═════ A6 짝산–짝염기 세기 사다리 ═════
def ladder():
    s=[]
    rows=[('\\ce{HNO3}','\\ce{NO3-}','강산','매우 약함'),('\\ce{H3O+}','\\ce{H2O}','',''),('\\ce{CH3COOH}','\\ce{CH3COO-}','약산','약염기'),('\\ce{NH4+}','\\ce{NH3}','약산','약염기'),('\\ce{H2O}','\\ce{OH-}','','강염기')]
    y0=70; dy=64
    for i,(a,b,na,nb) in enumerate(rows):
        y=y0+i*dy
        s.append(R(110,y-24,130,44,PLUS,1.8,ACID_F,8)+T(175,y+7,tex=a,size=21))
        s.append(R(320,y-24,130,44,MINUS,1.8,BASE_F,8)+T(385,y+7,tex=b,size=21))
        s.append(A(244,y-6,316,y-6,'field',2.5)+A(316,y+6,244,y+6,'bfield',2.5))
        if na: s.append(T(100,y+7,mix=na,size=18,anchor='end',fill=MUTED))
        if nb: s.append(T(460,y+7,mix=nb,size=18,anchor='start',fill=MUTED))
    ym=y0+2*dy
    s.append(A(42,y0+4*dy+14,42,y0-20,'plus',4)+T(6,y0-30,mix='산의 세기',size=19,anchor='start',fill=PLUS,weight=700))
    s.append(A(560,y0-20,560,y0+4*dy+14,'minus',4)+T(596,y0+4*dy+44,mix='짝염기의 세기',size=19,anchor='end',fill=MINUS,weight=700))
    s.append(T(175,32,mix='산',size=19,weight=700,fill=PLUS)+T(385,32,mix='짝염기',size=19,weight=700,fill=MINUS))
    hl=R(316,ym-29,138,54,EQUI,3,'none',10,dash='6 4')
    s.append(an('pop',hl,o=f'385,{ym}',delay='1.0'))
    return svg((600,400),600,'짝산과 짝염기의 세기 사다리: 산이 강할수록 그 짝염기는 약하다. 질산 이온은 매우 약한 염기이고 아세트산 이온은 약염기이다',s)
FIG['LADDER']=ladder()

# ═════ A9 가수 분해 입자 모형 ═════
def hyd():
    s=[]
    # 왼쪽: 아세트산 나트륨 (CH3COO- + H2O -> CH3COOH + OH-)
    x=0
    s.append(beaker(x+10,40,270,190,WATER,22)+T(x+145,26,mix='$\\ce{CH3COONa}$ 수용액',size=19,weight=700))
    for (px,py) in [(x+40,110),(x+150,205),(x+250,90)]: s.append(p_spec(px,py,1))
    s.append(p_A(x+60,190)+p_A(x+240,170))
    s.append(p_OHfrom(x+100,120)+C(x+190,118,11,INK,1.5,HA_F)+mv(atom(x+174,114,7,'H'),'-50,0',dur='1.4',delay='.6',ease='io'))
    s.append(T(x+145,264,mix='염기성',size=20,weight=700,fill=MINUS)+T(x+145,292,tex='[\\ce{OH-}]>[\\ce{H3O+}]',size=19,fill=MINUS))
    # 오른쪽: 염화 암모늄 (NH4+ + H2O -> NH3 + H3O+)
    x=310
    s.append(beaker(x+10,40,270,190,WATER,22)+T(x+145,26,mix='$\\ce{NH4Cl}$ 수용액',size=19,weight=700))
    for (px,py) in [(x+40,100),(x+150,210),(x+255,195)]: s.append(p_spec(px,py,-1))
    s.append(p_NH4(x+60,180)+p_NH4(x+225,90))
    s.append(p_NH3(x+100,130)+mv(atom(x+168.7,123.5,7,'H'),'-55.7,6.5',dur='1.4',delay='1.0',ease='io')+p_H3O_rest(x+180,130))
    s.append(T(x+145,264,mix='산성',size=20,weight=700,fill=PLUS)+T(x+145,292,tex='[\\ce{H3O+}]>[\\ce{OH-}]',size=19,fill=PLUS))
    s.append(legend(20,330,[(p_HA,'\\ce{CH3COOH}',170),(p_A,'\\ce{CH3COO-}',170),(p_OH,'\\ce{OH-}',110),(p_NH4,'\\ce{NH4+}',120)]))
    s.append(legend(20,372,[(p_NH3,'\\ce{NH3}',110),(p_H3O,'\\ce{H3O+}',120),(lambda x,y:p_spec(x,y,1),'\\ce{Na+}',100),(lambda x,y:p_spec(x,y,-1),'\\ce{Cl-}',90)])+T(596,378,mix='(물 분자 생략)',size=18,anchor='end',fill=MUTED))
    return svg((600,395),600,'아세트산 이온이 물에서 수소 이온을 받아 수산화 이온이 생기고(염기성), 암모늄 이온이 물에 수소 이온을 주어 하이드로늄 이온이 생긴다(산성). 나트륨 이온과 염화 이온은 반응하지 않는다',s)
def p_HA_body(x,y):   # H가 움직여 붙은 HA (H는 따로 그림)
    return C(x-17,y+4,11,INK,1.5,HA_F)
def p_OHfrom(x,y):    # H2O에서 H를 잃은 OH-
    return atom(x+12,y-6,7,'H')+atom(x,y,10,'O')+sgn(x-17,y-10,-1,18)
def p_H3O_rest(x,y):  # H2O가 H를 받아 H3O+ (움직이는 H는 따로)
    return atom(x,y+13,7,"H")+atom(x+11.3,y-6.5,7,"H")+atom(x,y,10,"O")+sgn(x+20,y-14,1,18)
def p_HA_leg(x,y): return p_HA(x,y)
FIG['HYD']=hyd()

# ═════ A10 [Al(H2O)6]3+ 가수 분해 ═════
def alaq():
    s=[]; cx,cy=180,170
    for k in range(6):
        t=math.radians(30+60*k); ox,oy=cx+64*math.cos(t),cy+64*math.sin(t)
        s.append(L(cx,cy,ox,oy,'#9AA5B1',6,extra='stroke-linecap="round"'))
        for d in (-40,40):
            if k==0 and d==40: continue
            tt=t+math.radians(d); s.append(atom(ox+21*math.cos(tt),oy+21*math.sin(tt),9,'H'))
        s.append(atom(ox,oy,14,'O'))
    s.append(atom(cx,cy,26,'Al','\\mathrm{Al}'))
    s.append(T(cx+92,cy-92,tex='3+',size=22,fill=PLUS,anchor='start'))
    t=math.radians(30); ox,oy=cx+64*math.cos(t),cy+64*math.sin(t); tt=t+math.radians(40); hx,hy=ox+21*math.cos(tt),oy+21*math.sin(tt)
    wx,wy=hx+90,hy+6
    s.append(atom(wx+16,wy+10,9,'H')+atom(wx+16,wy-12,9,'H'))
    s.append(mv(atom(wx-16,wy,9,'H'),f'{f(hx-(wx-16))},{f(hy-wy)}',dur='1.4',delay='.8',ease='io'))
    s.append(atom(wx,wy,14,'O'))
    s.append(an('fade',T(wx+30,wy-20,mix='+',size=22,weight=700,fill=PLUS),delay='2.0'))
    s.append(T(wx+4,wy+46,tex='\\ce{H3O+}',size=19,fill=PLUS))
    s.append(T(cx,cy+124,tex='\\ce{[Al(H2O)6]^3+}',size=20))
    s.append(T(500,36,mix='전하가 큰 $\\ce{Al^3+}$가',size=18,anchor='end',fill=MUTED)+T(500,60,mix='$\\ce{O-H}$ 결합을 약하게 함',size=18,anchor='end',fill=MUTED))
    s.append(atom(340,316,9,'H')+T(354,322,tex='\\mathrm{H}',size=18,anchor='start')+atom(392,316,14,'O')+T(412,322,tex='\\mathrm{O}',size=18,anchor='start'))
    return svg((520,340),520,'알루미늄 이온에 배위한 물 분자 하나가 바깥 물 분자에 수소 이온을 넘겨 하이드로늄 이온이 생긴다',s)
FIG['ALAQ']=alaq()

# ═════ A11 Ka vs Kb 막대 ═════
def kbar():
    s=[]; x0=140; w=380
    def X(e): return x0+(e+14)/10*w     # log K -14 … -4
    for e in range(-14,-3,2):
        s.append(L(X(e),40,X(e),282,'#E2E7EC',1)+T(X(e),306,tex=f'10^{{{e}}}',size=18))
    s.append(L(x0,282,x0+w+6,282,MUTED,2)+T(x0+w,336,mix='이온화 상수 (로그 눈금)',size=18,anchor='end',fill=MUTED))
    rows=[('$\\ce{NH4CN}$',[('$K_\\mathrm{a}(\\ce{NH4+})$',KW/KB_NH3,PLUS,ACID_F),('$K_\\mathrm{b}(\\ce{CN-})$',KW/6.2e-10,MINUS,BASE_F)],'염기성'),
          ('$\\ce{CH3COONH4}$',[('$K_\\mathrm{a}(\\ce{NH4+})$',KW/KB_NH3,PLUS,ACID_F),('$K_\\mathrm{b}(\\ce{CH3COO-})$',KW/KA,MINUS,BASE_F)],'거의 중성')]
    y=56
    for i,(nm,bars,res) in enumerate(rows):
        s.append(T(10,y+34,mix=nm,size=19,anchor='start',weight=700))
        for j,(lab,v,c,fl) in enumerate(bars):
            yy=y+j*34; ww=X(log10(v))-x0
            s.append(an('scale',R(x0,yy,ww,26,c,1.8,fl,4),**{'from':'0,1','o':f'{x0},{yy}','dur':'1.0','delay':f(0.2+0.3*i)}))
            s.append(T(x0+8,yy+20,mix=lab,size=18,anchor='start'))
        s.append(T(x0+w+20,y+40,mix=f'→ {res}',size=19,anchor='end',weight=700,fill=MINUS if i==0 else INK,halo=True) if False else '')
        s.append(T(10,y+60,mix=f'→ {res}',size=19,anchor='start',fill=MINUS if i==0 else INK,weight=700))
        y+=112
    return svg((540,345),520,'시안화 암모늄에서는 시안화 이온의 Kb가 암모늄 이온의 Ka보다 커서 염기성, 아세트산 암모늄에서는 둘이 같아 거의 중성이다',s)
FIG['KBAR']=kbar()

# ═════ A16 중화 반응 입자 ═════
def neut():
    s=[]
    s.append(p_H3O_big(80,110)+T(80,180,tex='\\ce{H3O+}',size=20,fill=PLUS))
    s.append(T(150,118,mix='+',size=28,weight=700))
    s.append(p_OH_big(220,110)+T(220,180,tex='\\ce{OH-}',size=20,fill=MINUS))
    s.append(A(270,110,330,110,'ink',3))
    s.append(T(300,70,tex='K=1.0\\times10^{14}',size=18,anchor='middle'))
    # 생성물 2H2O, H 하나가 이동
    s.append(water_big(390,110,0)+T(390,180,tex='\\ce{H2O}',size=20))
    s.append(T(450,118,mix='+',size=28,weight=700))
    s.append(water_big(510,110,0,skipH=True)+mv(atom(510-22,110+14,12,'H'),'-118,-30',dur='1.4',delay='.5',ease='io')+T(510,180,tex='\\ce{H2O}',size=20))
    return svg((580,200),560,'하이드로늄 이온이 수산화 이온에 수소 이온을 넘겨 물 분자 두 개가 된다',s)
def p_H3O_big(x,y):
    o=''.join(atom(x+24*math.cos(math.radians(t)),y+24*math.sin(math.radians(t)),12,'H') for t in (90,210,330))
    return o+atom(x,y,18,'O')+sgn(x+34,y-24,1,22)
def p_OH_big(x,y): return atom(x+22,y-12,12,'H')+atom(x,y,18,'O')+sgn(x-30,y-22,-1,22)
def water_big(x,y,a,skipH=False):
    o=''
    for i,d in enumerate((-52,52)):
        if skipH and i==0: continue
        t=math.radians(90+d); o+=atom(x+24*math.cos(t),y+24*math.sin(t),12,'H')
    return o+atom(x,y,18,'O')
FIG['NEUT']=neut()

# ═════ A17 적정 장치 ═════
def titset(w=360,h=430,sensor=False):
    s=[]; bx=150
    s.append(R(20,h-30,250,10,MUTED,0,MUTED,2)+R(36,20,8,h-40,GRAV,1,'#AEB8C2'))
    s.append(L(40,130,bx-12,130,MUTED,5,extra='stroke-linecap="round"'))
    # 뷰렛
    s.append(R(bx-9,40,18,196,'none',0,'#E8F0F9'))
    s.append(an('scale',R(bx-9,40,18,196,'none',0,'#DDEEF8'),**{'from':'1,1.12','o':f'{bx},236','dur':'1.2'}) if False else '')
    s.append(P([(bx-10,24),(bx-10,236)],GLASS,2.4)+P([(bx+10,24),(bx+10,236)],GLASS,2.4))
    for k in range(9): s.append(L(bx-10,52+k*20,bx-2,52+k*20,MUTED,1.2))
    s.append(P([(bx-10,236),(bx-3,246),(bx-3,262),(bx+3,262),(bx+3,246),(bx+10,236)],GLASS,2.2))
    s.append(R(bx+6,240,16,8,MINUS,0,MINUS,2))
    s.append(an('fade',C(bx,276,4,WATER_S,0,WATER_S),delay='.4',rep='loop',dur='.8'))
    # 삼각 플라스크 또는 비커
    fy=300
    if not sensor:
        s.append(P([(bx-16,fy),(bx-16,fy+22),(bx-62,h-34),(bx+62,h-34),(bx+16,fy+22),(bx+16,fy)],GLASS,3)+P([(bx-44,h-70),(bx-58,h-36),(bx+58,h-36),(bx+44,h-70)],'none',0,fill=PP_P,extra='fill-opacity=".55"',close=True))
    else:
        s.append(beaker(bx-60,fy-10,120,h-34-fy+10,WATER,30))
        s.append(R(bx+18,fy-60,12,110,GLASS,2,'#EEF3F7',5)+P([(bx+24,fy-60),(bx+24,fy-90),(w-30,fy-90)],INK,2))
        s.append(R(bx-60,h-30,120,8,'none',0,'#3A3F47',2))
    lab=(T(bx+20,60,mix='뷰렛: 표준 용액',size=18,anchor='start')+T(bx+20,84,mix='$\\ce{NaOH(aq)}$ (농도를 앎)',size=18,anchor='start',fill=MINUS))
    s.append(lab)
    if not sensor:
        s.append(T(bx+70,fy+40,mix='시료 + 지시약',size=18,anchor='start')+T(bx+70,fy+64,mix='(부피를 앎)',size=18,anchor='start',fill=MUTED))
    else:
        s.append(R(w-110,fy-130,92,40,INK,0,INK,6)+R(w-104,fy-124,80,28,'none',0,'#CFE8D8',3)+T(w-64,fy-104,mix='pH',size=18,weight=700))
        s.append(T(w-64,fy-140,mix='pH 센서',size=18,fill=MUTED)+T(bx+120,h-40,mix='자석 교반기',size=18,anchor='start',fill=MUTED))
        s.append(T(bx+70,fy+40,mix='희석한 식초',size=18,anchor='start')+T(bx+70,fy+64,mix='25.0 mL',size=18,anchor='start',fill=MUTED))
    return svg((w,h),w,'뷰렛의 수산화 나트륨 표준 용액을 시료에 조금씩 넣는 중화 적정 장치' if not sensor else 'pH 센서를 꽂은 비커 속 희석한 식초에 뷰렛으로 수산화 나트륨 표준 용액을 넣고 자석 교반기로 젓는다',s)
FIG['TITSET']=titset()
FIG['LABSET_A']=titset(400,430,True)

# ═════ A19 그림 Ⅳ-20 강산–강염기 ═════
def curve_s(big=True):
    s=[]; ax=Ax(70,360,470,300,80,14)
    s.append(tframe(ax,(0,10,20,30,40,50,60,70,80)))
    s.append(L(ax.x0,ax.Y(7),ax.x0+ax.w,ax.Y(7),GRAV,1.5,'6 5'))
    s.append(an('draw',P(curve_pts(SW,ax,0,80),INK,3.5),dur='1.6'))
    xe,ye=ax.X(50),ax.Y(7)
    s.append(L(xe,ax.y0,xe,ax.Y(14),MUTED,1.5,'5 4'))
    s.append(dot(xe,ye,PLUS,delay='1.5'))
    s.append(T(xe+14,ye+26,mix='당량점 pH 7.00',size=19,anchor='start',fill=PLUS,weight=700,halo=True))
    for n,V,dy in ((1,0,-22),(2,25,-24),(3,50,0),(4,70,30)):
        x,y=ax.X(V),ax.Y(SW(V))
        if n==3: s.append(circ_no(x-24,y-6,3)); continue
        s.append(circ_no(x+(14 if n==1 else 0),y+dy,n))
    return svg((580,420),560,'0.100 M 염산 50.0 mL에 0.100 M 수산화 나트륨 수용액을 넣을 때의 pH 곡선(계산값): 당량점 50.0 mL에서 pH 7.00, 그 근처에서 pH가 급격히 변한다',s)
FIG['CURVE_S']=curve_s()

def pts_s():
    s=[]; ax=Ax(70,330,360,280,60,14,xmin=40)
    s.append(tframe(ax,(40,45,50,55,60)))
    s.append(P(curve_pts(SW,ax,40,60,800),INK,3))
    data=[(49,'pH 3.00','end',-12,-8),(50,'pH 7.00','start',14,6),(51,'pH 11.00','start',14,22)]
    for i,(V,lab,anc,dx,dy) in enumerate(data):
        x,y=ax.X(V),ax.Y(SW(V)); s.append(dot(x,y,PLUS if V==50 else INK,6,'#FFFFFF' if V!=50 else None,delay=f(.3+.3*i)))
        s.append(T(x+dx,y+dy,mix=lab,size=19,anchor=anc,weight=700,halo=True))
    s.append(P([(ax.X(49),ax.y0+0),(ax.X(49),ax.y0-6)],EQUI,0))
    s.append(T(ax.X(56.5),ax.Y(5.2),mix='2 mL 사이에',size=19,fill=EQUI,weight=700)+T(ax.X(56.5),ax.Y(5.2)+24,mix='pH 8 증가',size=19,fill=EQUI,weight=700))
    return svg((460,392),440,'당량점 근처를 확대한 강산–강염기 적정 곡선: 49 mL에서 pH 3.00, 50 mL에서 7.00, 51 mL에서 11.00',s)
FIG['PTS_S']=pts_s()

# ═════ A22 그림 Ⅳ-21 약산–강염기 ═════
def curve_w():
    s=[]; ax=Ax(70,360,470,300,80,14)
    s.append(tframe(ax,(0,10,20,30,40,50,60,70,80)))
    v1,v2=50/11,500/11
    s.append(R(ax.X(v1),ax.Y(14),ax.X(v2)-ax.X(v1),ax.h,'none',0,FIELD,extra='fill-opacity=".15"'))
    s.append(T((ax.X(v1)+ax.X(v2))/2,ax.Y(13.2),mix='완충 구간',size=18,fill=FIELD,weight=700))
    s.append(L(ax.x0,ax.Y(7),ax.x0+ax.w,ax.Y(7),GRAV,1.5,'6 5'))
    s.append(an('draw',P(curve_pts(WK,ax,0,80),INK,3.5),dur='1.6'))
    xe,ye=ax.X(50),ax.Y(WK(50)); xh,yh=ax.X(25),ax.Y(WK(25))
    s.append(L(xe,ax.y0,xe,ax.Y(12.5),MUTED,1.5,'5 4'))
    s.append(dot(xe,ye,PLUS,delay='1.5')+T(xe+14,ye+26,mix='당량점 pH 8.72',size=19,anchor='start',fill=PLUS,weight=700,halo=True))
    s.append(dot(xh,yh,EQUI,delay='1.8')+T(xh,yh-18,mix='pH = p$K_\\mathrm{a}$ = 4.74',size=19,fill=EQUI,weight=700,halo=True))
    for n,V,dx,dy in ((1,0,16,22),(2,12,0,30),(3,50,-24,-6),(4,70,0,30)):
        x,y=ax.X(V),ax.Y(WK(V)); s.append(circ_no(x+dx,y+dy,n))
    return svg((580,420),560,'0.100 M 아세트산 50.0 mL에 0.100 M 수산화 나트륨 수용액을 넣을 때의 pH 곡선(계산값): 완충 구간, 반당량점 25.0 mL에서 pH 4.74, 당량점 50.0 mL에서 pH 8.72',s)
FIG['CURVE_W']=curve_w()

def pts_w():
    s=[]; ax=Ax(70,330,360,280,60,14)
    s.append(tframe(ax,(0,10,20,30,40,50,60)))
    s.append(P(curve_pts(WK,ax,0,60,800),INK,3))
    data=[(0,'2.88','start',14,6),(45,'5.70','end',-12,-6),(50,'8.72','start',14,10),(51,'11.00','end',-12,-6)]
    for i,(V,lab,anc,dx,dy) in enumerate(data):
        x,y=ax.X(V),ax.Y(WK(V)); s.append(dot(x,y,PLUS if V==50 else INK,6,'#FFFFFF' if V!=50 else None,delay=f(.3+.3*i)))
        s.append(T(x+dx,y+dy,mix='pH '+lab,size=19,anchor=anc,weight=700,halo=True))
    return svg((460,392),440,'약산–강염기 적정 곡선의 계산점: 0 mL pH 2.88, 45 mL pH 5.70, 50 mL pH 8.72, 51 mL pH 11.00',s)
FIG['PTS_W']=pts_w()

# ═════ A25 두 곡선 비교 ═════
def cmp(ind=False):
    s=[]; ax=Ax(70,360,470,300,80,14)
    s.append(tframe(ax,(0,10,20,30,40,50,60,70,80)))
    if ind:
        bands=[(3.1,4.4,MO_R,MO_Y,'메틸 오렌지 3.1–4.4'),(6.0,7.6,BTB_Y,BTB_B,'BTB 6.0–7.6'),(8.2,10.0,'#F7F7F7',PP_P,'페놀프탈레인 8.2–10.0')]
        defs='<defs>'
        for i,(lo,hi,c1,c2,nm) in enumerate(bands):
            defs+=f'<linearGradient id="grad-ac423-{i}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
        s.append(defs+'</defs>')
        for i,(lo,hi,c1,c2,nm) in enumerate(bands):
            b=R(ax.x0,ax.Y(hi),ax.w,ax.Y(lo)-ax.Y(hi),'none',0,f'url(#grad-ac423-{i})',extra='fill-opacity=".45"')
            s.append(an('fade',b,delay=f(.2+.3*i)))
            s.append(T(ax.x0+ax.w-4,ax.Y((lo+hi)/2)+6,mix=nm.split(' ')[0] if i!=0 else '메틸 오렌지',size=18,anchor='end',weight=700,halo=True))
    s.append(L(ax.x0,ax.Y(7),ax.x0+ax.w,ax.Y(7),GRAV,1.5,'6 5'))
    s.append(an('draw',P(curve_pts(SW,ax,0,80),MUTED,3,dash='10 6'),dur='1.4'))
    s.append(an('draw',P(curve_pts(WK,ax,0,80),INK,3.5),dur='1.6',delay='.2'))
    s.append(dot(ax.X(50),ax.Y(7),PLUS,6,'#FFFFFF',delay='1.4')+dot(ax.X(50),ax.Y(WK(50)),PLUS,7,delay='1.6'))
    if not ind:
        s.append(dot(ax.X(25),ax.Y(WK(25)),EQUI,delay='1.8')+T(ax.X(25),ax.Y(WK(25))+34,mix='반당량점 pH = p$K_\\mathrm{a}$',size=18,fill=EQUI,weight=700,halo=True))
        s.append(T(ax.X(56),ax.Y(7)+6,mix='7.00',size=18,anchor='start',fill=PLUS,weight=700,halo=True)+T(ax.X(46),ax.Y(WK(50))+4,mix='8.72',size=18,anchor='end',fill=PLUS,weight=700,halo=True))
    s.append(T(ax.X(14),ax.Y(SW(14))+28,mix='강산 $\\ce{HCl}$',size=18,anchor='middle',fill=MUTED,weight=700,halo=True))
    s.append(T(ax.X(4),ax.Y(WK(4))-30,mix='약산 $\\ce{CH3COOH}$',size=18,anchor='start',weight=700,halo=True) if not ind else T(ax.X(30),ax.Y(WK(30))+30,mix='약산',size=18,anchor='middle',weight=700,halo=True))
    lab='0.100 M 염산(점선)과 0.100 M 아세트산(실선) 각 50.0 mL를 0.100 M 수산화 나트륨으로 적정한 곡선 비교'+(' — 메틸 오렌지, BTB, 페놀프탈레인의 변색 범위를 겹쳤다' if ind else '')
    return svg((580,420),560,lab,s)
FIG['CMP']=cmp(False)
FIG['IND']=cmp(True)

# ═════ A27 확인 문제 04 ═════
def q04():
    s=[]; ax=Ax(70,300,320,240,30,14)
    s.append(tframe(ax,(0,10,20,30)))
    ka=10**-4.20
    fn=lambda V: ph_mix(na=0.100*V/1000,ct=0.0800*25/1000,ka=ka,vol=(25+V)/1000)
    s.append(P(curve_pts(fn,ax,0,30,600),INK,3))
    s.append(L(ax.X(20),ax.y0,ax.X(20),ax.Y(13),MUTED,1.5,'5 4')+T(ax.X(20)+6,ax.Y(13),mix='20.0 mL',size=18,anchor='start',fill=MUTED))
    x,y=ax.X(10),ax.Y(4.20); s.append(dot(x,y,INK,6,'#FFFFFF',delay='.6')+T(x,y-16,mix='10.0 mL, pH 4.20',size=18,weight=700,halo=True))
    return svg((420,362),400,'약산 HA 25.0 mL를 0.100 M 수산화 나트륨으로 적정한 곡선: 당량점 부피 20.0 mL, 10.0 mL에서 pH 4.20',s)
FIG['Q04']=q04()

# ═════ A30 실험실 결과 예시: 식초 ═════
def labres_a():
    s=[]; ax=Ax(70,250,440,200,30,14,ymin=0)
    s.append(tframe(ax,(0,5,10,15,20,25,30),(0,7,14),size=18))
    fn=lambda V: titr_weak(V,0.0820,25.0)
    vs=[i*1.0 for i in range(0,19)]+[19.0,19.4,19.8,20.0,20.2,20.4,20.6,20.8,21.0,21.4,22]+[23,24,25,26,28,30]
    rnd=random.Random(423)
    pts=[(v,fn(v)+rnd.uniform(-.02,.02)) for v in vs]
    s.append(P([(ax.X(v),ax.Y(p)) for v,p in pts],INK,2))
    for i,(v,p) in enumerate(pts): s.append(C(ax.X(v),ax.Y(p),3.6,INK,1,'#FFFFFF'))
    s.append(L(ax.X(20.5),ax.y0,ax.X(20.5),ax.Y(14),PLUS,1.5,'5 4')+L(ax.X(10.25),ax.y0,ax.X(10.25),ax.Y(14),EQUI,1.5,'5 4'))
    s.append(dot(ax.X(10.25),ax.Y(fn(10.25)),EQUI,6,delay='.4')+T(ax.X(10.25)+8,ax.Y(fn(10.25))-14,mix='4.75',size=18,anchor='start',fill=EQUI,weight=700,halo=True))
    # ΔpH/ΔV
    bx=Ax(70,420,440,120,30,1,ymin=0)
    s.append(L(bx.x0,bx.y0,bx.x0+bx.w+6,bx.y0,MUTED,2)+L(bx.x0,bx.y0,bx.x0,bx.y0-bx.h-6,MUTED,2))
    for v in (0,5,10,15,20,25,30): s.append(L(bx.X(v),bx.y0,bx.X(v),bx.y0+5,MUTED,1.5)+T(bx.X(v),bx.y0+24,tex=str(v),size=18))
    der=[]
    for (v1,p1),(v2,p2) in zip(pts,pts[1:]): der.append(((v1+v2)/2,(p2-p1)/(v2-v1)))
    mx=max(d for _,d in der)
    for v,d in der:
        hgt=max(1,d/mx*bx.h); s.append(R(bx.X(v)-2.5,bx.y0-hgt,5,hgt,'none',0,PLUS if d==mx else INK))
    s.append(T(bx.x0+10,bx.y0-bx.h+8,tex='\\Delta\\text{pH}/\\Delta V',size=18,anchor='start',fill=MUTED))
    s.append(T(bx.X(20.5)-10,bx.y0-bx.h+34,mix='최대 → 당량점',size=18,anchor='end',fill=PLUS,weight=700,halo=True))
    s.append(T(ax.X(20.5)+8,ax.Y(2.0),mix='20.5',size=18,anchor='start',fill=PLUS,weight=700,halo=True)+T(ax.X(10.25)-6,ax.Y(12.5),mix='반당량점 10.25',size=18,anchor='end',fill=EQUI,weight=700,halo=True))
    s.append(T(ax.x0+ax.w+6,bx.y0+52,mix='$V_{\\ce{NaOH}}$ [mL]',size=19,anchor='end',fill=MUTED))
    return svg((540,484),520,'희석한 식초를 0.100 M 수산화 나트륨으로 적정한 예시 자료(계산값에 작은 오차): pH 곡선과 ΔpH/ΔV 막대, 당량점 20.5 mL, 반당량점 pH 4.75',s)
FIG['LABRES_A']=labres_a()

# ═════════════════ 덱 b ═════════════════
def bufcurve(c,ax,a,b,V0=0.050,n=300):
    return curve_pts(lambda m: buffer_add(c*V0,c*V0,m/1000,V0,1.0),ax,a,b,n)
def watercurve(ax,a,b,n=600):
    return curve_pts(lambda m: buffer_add(0,0,m/1000,0.050,1.0) if abs(m)>1e-9 else 7.0,ax,a,b,n)
def cover_b():
    s=[]; ax=Ax(100,370,300,260,5,14,xmin=-5)
    s.append(ax.frame([-5,-2.5,0,2.5,5],[0,2,4,6,8,10,12,14],T(ax.x0+ax.w+6,ax.y0+50,mix='산 ← 넣은 양(mmol) → 염기',size=18,anchor='end',fill=MUTED),
        T(ax.x0-8,ax.y0-ax.h-20,tex='\\text{pH}',size=19,anchor='start',fill=MUTED),xfmt=lambda v:('%g'%abs(v)),size=18))
    s.append(an('draw',P(watercurve(ax,-5,5),GRAV,3,dash='4 5'),dur='1.2'))
    s.append(an('draw',P(bufcurve(0.10,ax,-5,5),INK,4),dur='1.4',delay='.3'))
    s.append(T(ax.X(-3.4),ax.Y(2.2),mix='물',size=19,fill=MUTED,weight=700)+T(ax.X(2.6),ax.Y(4.74)-18,mix='완충 용액',size=19,weight=700,halo=True))
    return svg((480,480),480,'물 50 mL과 아세트산–아세트산 나트륨 완충 용액 50 mL에 강산·강염기를 넣을 때의 pH: 물은 급변하고 완충 용액은 거의 변하지 않는다(계산값)',s,cls='fig cover-fig')
FIG['COVER_B']=cover_b()

def review():
    s=[]; ax=Ax(70,300,330,240,80,14)
    s.append(tframe(ax,(0,20,40,60,80),(0,7,14)))
    v1,v2=50/11,500/11
    s.append(R(ax.X(v1),ax.Y(14),ax.X(v2)-ax.X(v1),ax.h,'none',0,FIELD,extra='fill-opacity=".15"')+T((ax.X(v1)+ax.X(v2))/2,ax.Y(12.6),mix='완충 구간',size=18,fill=FIELD,weight=700))
    s.append(P(curve_pts(WK,ax,0,80),INK,3))
    s.append(dot(ax.X(25),ax.Y(WK(25)),EQUI,6,delay='.4')+T(ax.X(25),ax.Y(WK(25))+32,mix='p$K_\\mathrm{a}$',size=18,fill=EQUI,weight=700,halo=True))
    s.append(dot(ax.X(50),ax.Y(WK(50)),PLUS,6,delay='.6')+T(ax.X(50)+10,ax.Y(WK(50))+24,mix='당량점',size=18,anchor='start',fill=PLUS,weight=700,halo=True))
    return svg((420,362),400,'아세트산 적정 곡선의 완충 구간, 반당량점, 당량점',s)
FIG['REVIEW']=review()

def meters():
    s=[]
    def meter(x,y,val,col=INK,w=104):
        return R(x,y,w,56,INK,2,'#F4F6F8',8)+R(x+8,y+8,w-16,30,INK,1,'#DDE8D8',3)+T(x+w/2,y+31,mix=val,size=21,weight=700,fill=col)
    rows=[(30,'비완충 용액 100 mL',('2.00',PLUS),('12.00',MINUS)),(220,'완충 용액 100 mL',('4.98',INK),('5.02',INK))]
    for y,nm,(va,ca),(vb,cb) in rows:
        s.append(T(150,y+18,mix=nm,size=19,weight=700))
        s.append(meter(98,y+30,'5.00'))
        s.append(A(150,y+92,80,y+124,'plus',2.5)+A(150,y+92,230,y+124,'minus',2.5))
        s.append(an('pop',meter(22,y+128,va,ca),o=f'74,{y+156}',delay='.6')+an('pop',meter(178,y+128,vb,cb),o=f'230,{y+156}',delay='.9'))
        s.append(T(48,y+112,mix='$\\ce{HCl}$',size=18,fill=PLUS,anchor='end')+T(252,y+112,mix='$\\ce{NaOH}$',size=18,fill=MINUS,anchor='start'))
    s.append(T(150,436,mix='1 M 용액 1 mL씩 넣음',size=18,fill=MUTED))
    return svg((320,446),300,'pH 5.00인 비완충 용액에 1 M 염산·수산화 나트륨 1 mL를 넣으면 pH가 2.00, 12.00이 되지만, 완충 용액은 4.98, 5.02로 거의 변하지 않는다',s)
FIG['METERS']=meters()

def common():
    s=[]; ax=Ax(80,300,400,250,4,6)
    s.append(ax.frame([],[0,1,2,3,4,5,6],T(ax.x0+ax.w+6,ax.y0+56,mix='첨가한 $[\\ce{CH3COO-}]$ [M]',size=18,anchor='end',fill=MUTED),T(ax.x0-8,ax.y0-ax.h-20,tex='\\text{pH}',size=19,anchor='start',fill=MUTED),size=18))
    data=[(0,'0',1.3),(0.050,'0.050',0.036),(0.10,'0.10',0.018),(0.15,'0.15',0.012)]
    for i,(b,lab,pc) in enumerate(data):
        p=ph_mix(na=b,ct=0.10+b,vol=1.0); x=ax.x0+30+i*95; hgt=ax.y0-ax.Y(p)
        s.append(an('scale',R(x,ax.Y(p),56,hgt,EQUI if i else INK,1.8,'#FBE3C8' if i else HA_F,3),**{'from':'1,0','o':f'{x},{ax.y0}','dur':'1.0','delay':f(.2*i)}))
        s.append(T(x+28,ax.Y(p)-10,mix=f'{p:.2f}',size=18,weight=700))
        s.append(T(x+28,ax.y0+24,mix=lab,size=18))
        s.append(T(x+28,ax.y0-14,mix=f'{pc}%'.replace('.',',') if False else f'{pc} %',size=18,fill=MUTED if i else INK))
    s.append(T(ax.x0+4,ax.y0+80,mix='막대 아래 숫자: 해리 백분율',size=18,anchor='start',fill=MUTED))
    return svg((500,390),480,'0.10 M 아세트산에 아세트산 이온을 더 넣을수록 해리 백분율은 1.3 %에서 0.012 %로 줄고 pH는 2.89 근처에서 4.92로 커진다(표 Ⅳ-8, 계산값)',s)
FIG['COMMON']=common()

def addpart(acid=True):
    s=[]
    rnd=random.Random(8 if acid else 9)
    def box(x,nha,na,extra=()):
        o=beaker(x,40,210,190,WATER,20)
        slots=[(x+32+i*48,40+52+j*44) for j in range(3) for i in range(4)]
        rnd2=random.Random(x)
        pts=slots[:]; rnd2.shuffle(pts); k=0
        for i in range(nha): o+=p_HA(*pts[k]); k+=1
        for i in range(na): o+=p_A(*pts[k]); k+=1
        return o,pts[k:]
    b1,free1=box(20,5,5); s.append(b1)
    if acid:
        s.append(mv(p_H3O(250,110),'0,-50',dur='1.0',ease='out')+T(250,160,tex='\\ce{H3O+}',size=19,fill=PLUS)+T(250,60,mix='산 첨가',size=18,fill=PLUS,weight=700))
        b2,free2=box(300,6,4)
        s.append(b2+an('pop',p_H2O(*free2[0]),o=f'{f(free2[0][0])},{f(free2[0][1])}',delay='.9'))
        s.append(T(125,268,mix='$\\ce{CH3COOH}$ 5 · $\\ce{CH3COO-}$ 5',size=18)+T(405,268,mix='$\\ce{CH3COOH}$ 6 · $\\ce{CH3COO-}$ 4',size=18))
    else:
        s.append(mv(p_OH(250,110),'0,-50',dur='1.0',ease='out')+T(250,160,tex='\\ce{OH-}',size=19,fill=MINUS)+T(250,60,mix='염기 첨가',size=18,fill=MINUS,weight=700))
        b2,free2=box(300,4,6)
        s.append(b2+an('pop',p_H2O(*free2[0]),o=f'{f(free2[0][0])},{f(free2[0][1])}',delay='.9'))
        s.append(T(125,268,mix='$\\ce{CH3COOH}$ 5 · $\\ce{CH3COO-}$ 5',size=18)+T(405,268,mix='$\\ce{CH3COOH}$ 4 · $\\ce{CH3COO-}$ 6',size=18))
    s.append(A(236,190,290,190,'ink',3))
    s.append(legend(30,304,[(p_HA,'\\ce{CH3COOH}',150),(p_A,'\\ce{CH3COO-}',150),(lambda x,y:p_H2O(x,y),'\\ce{H2O}',90)])+T(510,310,mix='($\\ce{Na+}$·물 생략)',size=18,anchor='end',fill=MUTED))
    lab=('완충 용액에 하이드로늄 이온을 넣으면 아세트산 이온이 받아 아세트산과 물이 된다: 아세트산 5→6, 아세트산 이온 5→4' if acid else
         '완충 용액에 수산화 이온을 넣으면 아세트산이 수소 이온을 주어 아세트산 이온과 물이 된다: 아세트산 5→4, 아세트산 이온 5→6')
    return svg((520,320),520,lab,s)
FIG['ADDACID']=addpart(True)
FIG['ADDBASE']=addpart(False)

def ratio22():
    s=[]
    nHA,nA=0.0330,0.0596
    vals=[('처음',nA/nHA,INK),('$\\ce{HCl}$ 넣음',(nA-0.001)/(nHA+0.001),PLUS),('$\\ce{NaOH}$ 넣음',(nA+0.001)/(nHA-0.001),MINUS)]
    x0,y0,hh=30,260,180
    s.append(L(x0,y0,x0+360,y0,MUTED,2)+T(x0-6,28,mix='$[\\ce{CH3COO-}]/[\\ce{CH3COOH}]$',size=18,anchor='start',fill=MUTED))
    for i,(nm,v,c) in enumerate(vals):
        x=x0+30+i*115; hgt=v/2.0*hh
        s.append(an('scale',R(x,y0-hgt,60,hgt,c,1.8,'#FFFFFF' if i==0 else (ACID_F if i==1 else BASE_F),3),**{'from':'1,0','o':f'{x},{y0}','delay':f(.2*i)}))
        s.append(T(x+30,y0-hgt-10,mix=f'{v:.2f}',size=18,weight=700)+T(x+30,y0+26,mix=nm,size=18))
    s.append(T(x0+180,y0+60,mix='비가 조금만 바뀜 → pH 4.98, 5.02',size=18,weight=700))
    return svg((400,330),400,'완충 용액(덱 계산: 0.330 M 아세트산 + 0.596 M 아세트산 나트륨)에 산이나 염기를 1 mmol 넣어도 아세트산 이온과 아세트산의 농도비는 1.81에서 1.72, 1.89로 조금만 바뀐다',s)
FIG['RATIO22']=ratio22()

def hhline():
    s=[]; ax=Ax(80,300,360,250,1.5,7,xmin=-1.5,ymin=2.5)
    s.append(ax.frame([-1.5,-1,0,1,1.5],[3,4,5,6,7],T(ax.x0+ax.w+6,ax.y0+68,mix='$\\log\\dfrac{[\\ce{A-}]}{[\\ce{HA}]}$',size=18,anchor='end',fill=MUTED),T(ax.x0-8,ax.y0-ax.h-20,tex='\\text{pH}',size=19,anchor='start',fill=MUTED),size=18,xfmt=lambda v:('%g'%v).replace('-','−')))
    s.append(R(ax.X(-1),ax.Y(7),ax.X(1)-ax.X(-1),ax.h,'none',0,FIELD,extra='fill-opacity=".15"')+T(ax.X(0),ax.Y(6.8),mix='완충 범위 p$K_\\mathrm{a}\\pm1$',size=18,fill=FIELD,weight=700))
    s.append(an('draw',L(ax.X(-1.5),ax.Y(4.74-1.5),ax.X(1.5),ax.Y(4.74+1.5),INK,3.5),dur='1.0'))
    for i,(r,lab) in enumerate(((-1,'1 : 10'),(0,'1 : 1'),(1,'10 : 1'))):
        x,y=ax.X(r),ax.Y(4.74+r); s.append(dot(x,y,EQUI if r==0 else INK,6,None if r==0 else '#FFFFFF',delay=f(.8+.2*i)))
        s.append(T(x+10,y+22,mix=lab,size=18,anchor='start',weight=700,halo=True))
    s.append(T(ax.X(0)-12,ax.Y(4.74)-14,mix='p$K_\\mathrm{a}$ 4.74',size=18,anchor='end',fill=EQUI,weight=700,halo=True))
    return svg((470,385),450,'아세트산 완충 용액에서 짝염기와 약산의 농도비의 로그에 따라 pH가 pKa를 중심으로 1씩 바뀐다. 비가 1:10에서 10:1 사이가 완충 범위이다',s)
FIG['HHLINE']=hhline()

def capc():
    s=[]; ax=Ax(70,370,470,320,8,13,xmin=-8,ymin=1)
    s.append(ax.frame([-8,-4,0,4,8],[1,3,5,7,9,11,13],T(ax.x0+ax.w+6,ax.y0+52,mix='넣은 $\\ce{HCl}$ ← mmol → 넣은 $\\ce{NaOH}$',size=18,anchor='end',fill=MUTED),
        T(ax.x0-8,ax.y0-ax.h-20,tex='\\text{pH}',size=19,anchor='start',fill=MUTED),xfmt=lambda v:'%g'%abs(v),size=18))
    s.append(R(ax.x0,ax.Y(5.74),ax.w,ax.Y(3.74)-ax.Y(5.74),'none',0,HL,extra='fill-opacity=".35"'))
    s.append(T(ax.x0+6,ax.Y(5.74)-8,mix='처음 pH ± 1',size=18,anchor='start',fill=INK,weight=700))
    s.append(an('draw',P(watercurve(ax,-8,8),GRAV,2.5,dash='3 5'),dur='1.0'))
    styles=[(0.010,MUTED,2.5,'2 4','각 0.010 M'),(0.050,INK,2.5,'10 6','각 0.050 M'),(0.20,INK,4,None,'각 0.20 M')]
    for i,(c,col,w,d,lab) in enumerate(styles):
        s.append(an('draw',P(bufcurve(c,ax,-8,8),col,w,dash=d),dur='1.2',delay=f(.3+.3*i)))
    s.append(T(ax.X(-1.2),ax.Y(1.8),mix='각 0.010 M',size=18,anchor='end',fill=MUTED,weight=700,halo=True))
    s.append(T(ax.X(-2.9),ax.Y(2.5),mix='0.050 M',size=18,anchor='end',weight=700,halo=True) if False else '')
    s.append(T(ax.X(-3.6),ax.Y(3.05),mix='각 0.050 M',size=18,anchor='end',weight=700,halo=True))
    s.append(T(ax.X(6.6),ax.Y(5.65)-6,mix='각 0.20 M',size=18,anchor='end',weight=700,halo=True))
    s.append(T(ax.X(3.4),ax.Y(12.3),mix='물',size=18,anchor='start',fill=MUTED,weight=700))
    return svg((580,432),560,'아세트산과 아세트산 나트륨을 같은 농도로 넣은 완충 용액 50 mL에 산·염기를 넣을 때 pH(계산값): 농도가 클수록 pH ±1 안에서 넣을 수 있는 양이 많다',s)
FIG['CAPC']=capc()

def prep():
    s=[]; x0,w=60,420
    X=lambda p: x0+(p-3)/8*w
    s.append(L(x0,250,x0+w+6,250,MUTED,2))
    for p in range(3,12): s.append(L(X(p),250,X(p),256,MUTED,1.5)+T(X(p),278,tex=str(p),size=18))
    s.append(T(x0+w+6,306,mix='pH',size=18,anchor='end',fill=MUTED))
    pairs=[(4.74,'$\\ce{CH3COOH}$ / $\\ce{CH3COO-}$',60),(7.21,'$\\ce{H2PO4-}$ / $\\ce{HPO4^2-}$',120),(9.26,'$\\ce{NH4+}$ / $\\ce{NH3}$',180)]
    for i,(pk,nm,y) in enumerate(pairs):
        s.append(an('scale',R(X(pk-1),y,X(pk+1)-X(pk-1),30,FIELD,1.5,'#DDF1E6',6),**{'from':'0,1','o':f'{f(X(pk))},{y}','delay':f(.2+.25*i)}))
        s.append(L(X(pk),y,X(pk),y+30,EQUI,3)+T(X(pk),y-8,mix=f'p$K_\\mathrm{{a}}$ {pk}',size=18,fill=EQUI,weight=700))
        s.append(T(X(pk+1)+8,y+22,mix=nm,size=18,anchor='start') if pk<9 else T(X(pk-1)-8,y+22,mix=nm,size=18,anchor='end'))
    s.append(L(X(7.4),40,X(7.4),250,PLUS,2,'5 4')+T(X(7.4)+6,36,mix='혈액 7.4',size=18,anchor='start',fill=PLUS,weight=700))
    return svg((560,320),540,'짝산–짝염기 쌍의 pKa와 완충 범위(pKa ± 1): 아세트산 4.74, 인산 이수소 이온 7.21, 암모늄 이온 9.26. 혈액 pH 7.4는 인산 쌍의 범위 안',s)
FIG['PREP']=prep()

def capres():
    s=[]; ax=Ax(80,290,360,240,0.20,9)
    s.append(ax.frame([0,0.05,0.10,0.15,0.20],[0,2,4,6,8],T(ax.x0+ax.w+6,ax.y0+52,mix='짝산·짝염기 각 농도 [M]',size=18,anchor='end',fill=MUTED),T(ax.x0-8,ax.y0-ax.h-20,mix='pH −1까지 넣은 $\\ce{HCl}$ [mmol]',size=18,anchor='start',fill=MUTED),xfmt=lambda v:'%g'%v,size=18))
    pts=[(c,capacity(c*0.05,c*0.05)[1]*1000) for c in (0.010,0.020,0.050,0.10,0.20)]
    s.append(an('draw',L(ax.X(0),ax.Y(0),ax.X(0.20),ax.Y(pts[-1][1]),FIELD,2.5,'6 4'),dur='1.0',delay='1.0'))
    for i,(c,m) in enumerate(pts):
        s.append(dot(ax.X(c),ax.Y(m),PLUS,6,'#FFFFFF',delay=f(.2+.15*i)))
    s.append(T(ax.X(0.20)-6,ax.Y(pts[-1][1])+30,mix=f'{pts[-1][1]:.1f} mmol',size=18,anchor='end',weight=700,halo=True))
    s.append(T(ax.X(0.10)+10,ax.Y(pts[3][1])+26,mix=f'{pts[3][1]:.1f}',size=18,anchor='start',weight=700,halo=True))
    s.append(T(ax.X(0.05)+10,ax.Y(pts[2][1])+24,mix=f'{pts[2][1]:.1f}',size=18,anchor='start',weight=700,halo=True))
    return svg((470,350),450,'짝산과 짝염기를 같은 농도로 넣은 완충 용액 50 mL에서 pH가 1 낮아질 때까지 넣을 수 있는 염산의 양은 농도에 비례한다(계산값)',s)
FIG['CAPRES']=capres()

def blood():
    s=[]
    box=lambda x,y,w,tex,c,fl: R(x,y,w,46,c,2,fl,10)+T(x+w/2,y+30,tex=tex,size=20)
    y=120
    s.append(box(10,y,110,'\\ce{CO2(g)}',INK,'#FFFFFF')+box(170,y,110,'\\ce{CO2(aq)}',INK,'#FFFFFF')+box(330,y,120,'\\ce{H2CO3(aq)}',PLUS,ACID_F)+box(500,y,140,'\\ce{HCO3^-(aq)}',MINUS,BASE_F))
    for x1,x2 in ((120,170),(280,330),(450,500)):
        s.append(A(x1+4,y+16,x2-4,y+16,'field',2.5)+A(x2-4,y+30,x1+4,y+30,'bfield',2.5))
    s.append(T(475,y-12,mix='$+\\ \\ce{H2O}$ → $+\\ \\ce{H3O+}$',size=18,fill=MUTED))
    s.append(T(65,y+80,mix='폐: 호흡으로',size=18,weight=700)+T(65,y+104,mix='$\\ce{CO2}$ 내보냄',size=18))
    s.append(T(570,y+80,mix='콩팥: $\\ce{HCO3-}$',size=18,weight=700)+T(570,y+104,mix='배설·재흡수',size=18))
    # 비 20:1
    yy=290
    s.append(an('scale',R(190,yy,300,30,MINUS,1.8,BASE_F,4),**{'from':'0,1','o':f'190,{yy}','delay':'.4'})+T(180,yy+22,tex='[\\ce{HCO3-}]',size=19,anchor='end'))
    s.append(an('scale',R(190,yy+40,15,30,PLUS,1.8,ACID_F,4),**{'from':'0,1','o':f'190,{yy+40}','delay':'.6'})+T(180,yy+62,tex='[\\ce{H2CO3}]',size=19,anchor='end'))
    s.append(T(500,yy+22,mix='20',size=20,anchor='start',weight=700)+T(215,yy+62,mix='1 (pH 7.40일 때)',size=19,anchor='start',weight=700))
    s.append(T(320,34,mix='젖산 같은 산이 들어오면 → $\\ce{HCO3-}$가 $\\ce{H3O+}$를 받음',size=18,fill=PLUS)+T(320,62,mix='염기가 들어오면 → $\\ce{H2CO3}$가 $\\ce{OH-}$를 중화',size=18,fill=MINUS))
    return svg((650,370),620,'혈액의 탄산 완충계: 이산화 탄소, 탄산, 탄산수소 이온 사이의 평형을 폐와 콩팥이 조절하고, pH 7.40에서 탄산수소 이온과 탄산의 비는 약 20 : 1이다',s)
FIG['BLOOD']=blood()

# ═════ 조립 ═════
def build(tplname,out,meta):
    tpl=open(os.path.join(HERE,tplname),encoding='utf-8').read()
    keys=re.findall(r'\{\{(\w+)\}\}',tpl)
    for k in keys:
        if k not in FIG: sys.exit('no fig '+k)
    html=re.sub(r'\{\{(\w+)\}\}',lambda m:FIG[m.group(1)],tpl)
    open(out+'slides.html','w',encoding='utf-8').write(html)
    shutil.copy(os.path.join(HERE,'extra_src.css'),out+'extra.css')
    open(out+'meta.json','w',encoding='utf-8').write(meta+'\n')
    print('ok',out[-30:],len(html),'sections',html.count('<section'),'anim',html.count('data-anim'))
    return set(keys)
used=build('tpl_a.html',OUT_A,'{"title": "염 용액의 성질과 중화 반응 (1) 염 용액의 성질과 중화 적정", "file": "4-2-3_염_용액의_성질과_중화_반응a", "header": "Ⅳ-2-3 염 용액의 성질과 중화 반응 (고등 고급 화학 218–229쪽)"}')
used|=build('tpl_b.html',OUT_B,'{"title": "염 용액의 성질과 중화 반응 (2) 완충 용액", "file": "4-2-3_염_용액의_성질과_중화_반응b", "header": "Ⅳ-2-3 염 용액의 성질과 중화 반응 (고등 고급 화학 218–229쪽)"}')
if set(FIG)-used: print('unused figs',set(FIG)-used)
src=open(os.path.join(HERE,'labs_src.js'),encoding='utf-8').read()
head,rest=src.split('/*@@A*/'); la,lb=rest.split('/*@@B*/')
open(OUT_A+'labs.js','w',encoding='utf-8').write(head+'window.DECK_LABS = {\n'+la+'};\n})();\n')
open(OUT_B+'labs.js','w',encoding='utf-8').write(head+'window.DECK_LABS = {\n'+lb+'};\n})();\n')
print('labs ok')
