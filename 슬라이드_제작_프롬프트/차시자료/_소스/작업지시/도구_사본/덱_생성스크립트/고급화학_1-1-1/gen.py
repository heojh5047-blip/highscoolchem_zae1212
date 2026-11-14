# -*- coding: utf-8 -*-
"""고급화학 1-1-1 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다."""
import math, random, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/1-1-1_보어의_원자_모형과_현대적_원자_모형/slides.html'
INK='#16233D';PLUS='#D7263D';MINUS='#1F6FD1';FIELD='#2E9E6A';EQUI='#E08A2C';BF='#7B4FC8';MUTED='#5B6B7F';GRAV='#8C99A6'
HC={656:'#E8322B',486:'#21B5C9',434:'#3D4FE0',410:'#7B3FC4'}
def f(v): return ('%.1f'%v).rstrip('0').rstrip('.')
def T(x,y,tex=None,mix=None,size=20,anchor='middle',fill=None,halo=False,weight=None,extra=''):
    a=f'<text class="tex" x="{f(x)}" y="{f(y)}" '
    a+=(f'data-tex="{tex}" ' if tex is not None else f'data-mix="{mix}" ')
    a+=f'data-size="{size}" data-anchor="{anchor}"'
    if fill: a+=f' fill="{fill}"'
    if halo: a+=' data-halo="1"'
    if weight: a+=f' data-weight="{weight}"'
    return a+(' '+extra if extra else '')+'></text>'
def A(x1,y1,x2,y2,col='ink',w=3,d=False,extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}{",d" if d else ""}"{(" "+extra) if extra else ""}></g>'
def L(x1,y1,x2,y2,col=INK,w=2,dash=None,extra=''):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def P(pts,col=INK,w=2.5,fill='none',dash=None,extra='',close=False):
    d='M'+' L'.join(f'{f(x)} {f(y)}' for x,y in pts)+(' Z' if close else '')
    return f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def C(cx,cy,r,col=INK,w=2,fill='none',dash=None,extra=''):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def nuc(x,y,r=12): return f'<g data-chg="{f(x)},{f(y)},{r},+"></g>'
def ele(x,y,r=9): return f'<g data-chg="{f(x)},{f(y)},{r},-"></g>'
def wl_rgb(w):
    if w<380 or w>750: return None
    if w<440: r,g,b=-(w-440)/60,0,1
    elif w<490: r,g,b=0,(w-440)/50,1
    elif w<510: r,g,b=0,1,-(w-510)/20
    elif w<580: r,g,b=(w-510)/70,1,0
    elif w<645: r,g,b=1,-(w-645)/65,0
    else: r,g,b=1,0,0
    fac=.3+.7*(w-380)/40 if w<420 else (1 if w<=700 else .3+.7*(750-w)/50)
    return '#%02X%02X%02X'%tuple(int(255*(c*fac)**.8) for c in (r,g,b))
def wcol(w):
    for k,v in HC.items():
        if abs(w-k)<2.5: return v
    return wl_rgb(w)
def rainbow(gid,x1,x2):
    st=''.join(f'<stop offset="{(w-400)/300:.3f}" stop-color="{wl_rgb(w)}"/>' for w in range(400,701,20))
    return f'<defs><linearGradient id="{gid}" x1="0" x2="1" y1="0" y2="0">{st}</linearGradient></defs>'
def wave(x1,y1,x2,y2,col,amp=6,lam=14,w=3):
    dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
    pts=[]; n=int(Ln/2)
    for i in range(n+1):
        s=i/n*Ln; a=amp*math.sin(2*math.pi*s/lam)*(1 if s<Ln-14 else max(0,(Ln-s)/14))
        pts.append((x1+ux*s+px*a,y1+uy*s+py*a))
    return P(pts,col,w)
FIG={}
# ── radial functions
def R1(r): return 2*math.exp(-r)
def R2(r): return (2-r)*math.exp(-r/2)/(2*math.sqrt(2))
def R3(r): return 2/(81*math.sqrt(3))*(27-18*r+2*r*r)*math.exp(-r/3)
def Pr(Rf,r): return r*r*Rf(r)**2

# ═══ 표지
def cover():
    s=['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    cx,cy=270,205; rs=[30,62,104,156]
    for i,r in enumerate(rs): s.append(C(cx,cy,r,MUTED,1.8,dash='6 6'))
    s.append(nuc(cx,cy,14))
    for i,r in enumerate(rs):
        a=math.radians(135); s.append(T(cx-r*math.cos(math.radians(45))-2,cy+r*math.sin(math.radians(45))+8,tex=f'n={i+1}',size=20,halo=True))
    ang=math.radians(-55); e2=(cx+rs[1]*math.cos(ang),cy+rs[1]*math.sin(ang)); e3=(cx+rs[2]*math.cos(ang),cy+rs[2]*math.sin(ang))
    s.append(f'<circle cx="{f(e3[0])}" cy="{f(e3[1])}" r="9" fill="none" stroke="{MINUS}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    s.append(f'<g data-anim="move" data-from="{f(e3[0]-e2[0])},{f(e3[1]-e2[1])}" data-dur="1.4" data-delay=".4" data-ease="io">{ele(*e2)}</g>')
    s.append(f'<g data-anim="draw" data-dur="1.2" data-delay="1.6">{wave(e2[0]+14,e2[1]-6,420,92,HC[656],7,16,3)}</g>')
    s.append(T(384,156,mix='빛 방출',size=21,fill=HC[656],weight=700,halo=True))
    x0,x1=130,410; y0=390
    s.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="40" fill="#111" rx="3"/>')
    ln=''.join(f'<rect x="{f(x0+(w-380)/(720-380)*(x1-x0)-2.5)}" y="{y0}" width="5" height="40" fill="{wcol(w)}"/>' for w in (410.2,434.0,486.1,656.3))
    s.append(f'<g data-anim="fade" data-dur=".8" data-delay="2.4">{ln}</g>')
    s.append(T(270,458,mix='수소 원자의 선 스펙트럼',size=21))
    return f'<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="원자핵 둘레 네 개의 궤도에서 전자가 바깥 궤도에서 안쪽 궤도로 옮겨 가며 빨간빛을 내놓고, 아래에 네 개의 선으로 된 수소 선 스펙트럼이 있다">'+''.join(s)+'</svg>'
FIG['COVER']=cover()

# ═══ S4 원자 모형 발전
def models():
    s=[]; xs=[100,300,500,700,900]; cy=78
    names=['돌턴','톰슨','러더퍼드','보어','현대']
    sub=['더 쪼갤 수 없는 공','(+)전하 속 전자','원자핵과 전자','정해진 궤도','전자구름(확률)']
    g=[]
    # Dalton
    g.append(f'<circle cx="{xs[0]}" cy="{cy}" r="46" fill="#8C99A6" stroke="{INK}" stroke-width="2"/>')
    # Thomson
    t=[f'<circle cx="{xs[1]}" cy="{cy}" r="46" fill="#FDE2E4" stroke="{PLUS}" stroke-width="2"/>']
    random.seed(3)
    for (dx,dy) in [(-22,-18),(14,-26),(26,6),(-6,4),(-26,20),(10,26)]: t.append(ele(xs[1]+dx,cy+dy,7))
    g.append(''.join(t))
    # Rutherford
    r=[f'<ellipse cx="{xs[2]}" cy="{cy}" rx="48" ry="18" fill="none" stroke="{MUTED}" stroke-width="1.5" transform="rotate({a} {xs[2]} {cy})"/>' for a in (0,60,120)]
    r.append(nuc(xs[2],cy,8)); r+= [ele(xs[2]+48,cy,6), ele(xs[2]-24*0.5+0,cy-41.6*0.5-3,6)]
    g.append(''.join(r))
    b=[C(xs[3],cy,rr,MUTED,1.5,dash='4 4') for rr in (20,34,48)]; b.append(nuc(xs[3],cy,8)); b+=[ele(xs[3]+20,cy,6),ele(xs[3]-24,cy-24,6)]
    g.append(''.join(b))
    random.seed(7); m=[]
    for i in range(260):
        rr=-math.log(1-random.random()*0.985)*14; a=random.random()*6.283
        if rr<48: m.append(f'<circle cx="{f(xs[4]+rr*math.cos(a))}" cy="{f(cy+rr*math.sin(a))}" r="1.8" fill="{MINUS}" opacity=".55"/>')
    m.append(nuc(xs[4],cy,6)); g.append(''.join(m))
    for i in range(5):
        s.append(f'<g data-anim="pop" data-o="{xs[i]},{cy}" data-dur=".6" data-delay="{.2+.35*i:.2f}">{g[i]}</g>')
        s.append(T(xs[i],158,mix=names[i],size=21,weight=700)); s.append(T(xs[i],186,mix=sub[i],size=19,fill=MUTED))
        if i<4: s.append(A(xs[i]+58,cy,xs[i+1]-58,cy,'muted',2.5))
    return '<svg class="fig" viewBox="0 0 1000 196" style="width:1000px" aria-label="돌턴, 톰슨, 러더퍼드, 보어, 현대 원자 모형이 차례로 발전한 모습">'+''.join(s)+'</svg>'
FIG['MODELS']=models()

# ═══ S6 두 띠
def bands():
    s=[rainbow('grad-ac111-06',0,1)]
    s.append(f'<rect x="20" y="30" width="400" height="44" fill="url(#grad-ac111-06)" rx="3"/>')
    s.append(f'<rect x="20" y="140" width="400" height="44" fill="#111" rx="3"/>')
    for w in (410.2,434.0,486.1,656.3):
        x=20+(w-400)/300*400
        s.append(f'<g class="step" data-g="p1"><rect x="{f(x-2.5)}" y="140" width="5" height="44" fill="{wcol(w)}"/></g>')
    s.append(T(20,22,mix='(가) 무지개처럼 이어진 띠',size=20,anchor='start'))
    s.append(T(20,132,mix='(나) 몇 개의 밝은 선',size=20,anchor='start'))
    return '<svg class="fig" viewBox="0 0 440 200" style="width:440px" aria-label="(가) 무지개처럼 이어진 띠와 (나) 검은 바탕의 몇 개의 밝은 선">'+''.join(s)+'</svg>'
FIG['BANDS']=bands()

# ═══ S7 전자기 복사선 분류
def em():
    s=[rainbow('grad-ac111-07',0,1)]
    X=lambda lg: 50+(lg+5)*58   # log10(nm) -5..12 -> 50..1036
    regs=[('감마선',-5,-2,'#E7E1F5'),('X선',-2,1,'#E3E9F7'),('자외선',1,2.6,'#E6F1FB'),('',2.6,2.845,None),('적외선',2.845,6,'#FCE9E3'),('마이크로파',6,9,'#FDF1DE'),('라디오파',9,12,'#F1F6E6')]
    y0,h=52,46
    for nm,a,b,col in regs:
        if col: s.append(f'<rect x="{f(X(a))}" y="{y0}" width="{f(X(b)-X(a))}" height="{h}" fill="{col}" stroke="{MUTED}" stroke-width="1"/>')
        if nm: s.append(T((X(a)+X(b))/2,y0-12,mix=nm,size=20))
    s.append(f'<rect x="{f(X(2.6))}" y="{y0}" width="{f(X(2.845)-X(2.6))}" height="{h}" fill="url(#grad-ac111-07)"/>')
    for lg in range(-5,13,1):
        x=X(lg); s.append(L(x,y0+h,x,y0+h+6,MUTED,1.5))
        if lg%3==1 or lg in (-5,): pass
    for lg in (-4,-1,2,5,8):
        s.append(T(X(lg),y0+h+30,tex=f'10^{{{lg}}}',size=19))
    s.append(T(1050,y0+h+30,mix='파장(nm)',size=19,anchor='end',fill=MUTED))
    # zoom
    zx0,zx1,zy=330,830,180
    s.append(P([(X(2.6),y0+h),(zx0,zy)],MUTED,1.2,dash='4 4')); s.append(P([(X(2.845),y0+h),(zx1,zy)],MUTED,1.2,dash='4 4'))
    s.append(f'<rect x="{zx0}" y="{zy}" width="{zx1-zx0}" height="34" fill="url(#grad-ac111-07)" rx="3"/>')
    for w in (400,500,600,700):
        x=zx0+(w-400)/300*(zx1-zx0); s.append(L(x,zy+34,x,zy+40,MUTED,1.5)); s.append(T(x,zy+62,tex=f'{w}\\ \\text{{nm}}',size=19))
    s.append(T(zx0-14,zy+24,mix='가시광선',size=20,anchor='end',weight=700))
    s.append(A(870,182,1030,182,'ink',2.5)); s.append(T(950,172,mix='파장이 길어짐',size=19))
    s.append(A(1030,214,870,214,'equi',2.5)); s.append(T(950,240,mix='에너지가 커짐',size=19,fill=EQUI))
    return '<svg class="fig" viewBox="0 0 1080 256" style="width:1080px" aria-label="전자기 복사선의 분류: 파장이 짧은 쪽부터 감마선, X선, 자외선, 가시광선, 적외선, 마이크로파, 라디오파. 가시광선은 400–700 nm">'+''.join(s)+'</svg>'
FIG['EM']=em()

# ═══ S8 방전관 장치 + 스펙트럼
def tube():
    s=[rainbow('grad-ac111-08',0,1)]
    s.append(f'<rect x="40" y="40" width="44" height="190" rx="22" fill="#FBD3E0" stroke="#7E8B98" stroke-width="2.5"/>')
    s.append(f'<rect x="56" y="62" width="12" height="146" rx="6" fill="#F49AC1"/>')
    s.append(L(62,20,62,40,'#7E8B98',3)); s.append(L(62,230,62,250,'#7E8B98',3))
    s.append(T(4,274,mix='수소 기체 방전관',size=19,anchor='start'))
    s.append(f'<polygon points="84,125 170,118 170,142 84,135" fill="#FBD3E0" opacity=".7"/>')
    s.append(f'<rect x="170" y="70" width="12" height="120" fill="#C9B79C" stroke="{MUTED}"/><rect x="170" y="124" width="12" height="12" fill="#FBD3E0"/>')
    s.append(T(176,58,mix='슬릿',size=19))
    s.append(f'<polygon points="182,124 262,122 262,138 182,136" fill="#FBD3E0" opacity=".7"/>')
    s.append(f'<polygon points="262,170 318,70 374,170" fill="#E3EEF8" stroke="#7E8B98" stroke-width="2"/>')
    s.append(T(318,196,mix='프리즘',size=19))
    for w,y in ((410.2,28),(434.0,52),(486.1,82),(656.3,150)):
        s.append(f'<g class="step" data-g="t1">{L(330,126,470,y,wcol(w),4)}</g>')
    s.append(L(476,20,476,190,INK,3)); s.append(T(476,214,mix='검출기',size=19))
    # strips
    sx0,sx1=560,1060; X=lambda w: sx0+(w-400)/300*(sx1-sx0)
    s.append(T(sx0,62,mix='수소 기체 방전관의 빛',size=20,anchor='start',weight=700))
    s.append(f'<rect x="{sx0}" y="96" width="{sx1-sx0}" height="44" fill="#111" rx="3"/>')
    for w,lab,yy in ((410.2,'410.1',90),(434.0,'434.1',90),(486.1,'486.1',90),(656.3,'656.3',90)):
        s.append(f'<g class="step" data-g="t1"><rect x="{f(X(w)-2.5)}" y="96" width="5" height="44" fill="{wcol(w)}"/></g>')
    s.append(f'<g class="step" data-g="t1">'+T(X(410.2)-4,88,tex='410.1',size=18,anchor='end')+T(X(434.0)+4,88,tex='434.1',size=18,anchor='start')+T(X(486.1),88,tex='486.1',size=18)+T(X(656.3),88,tex='656.3',size=18)+'</g>')
    s.append(T(sx0,180,mix='태양빛',size=20,anchor='start',weight=700))
    s.append(f'<rect x="{sx0}" y="190" width="{sx1-sx0}" height="44" fill="url(#grad-ac111-08)" rx="3"/>')
    for w in (400,500,600,700): s.append(L(X(w),234,X(w),240,MUTED,1.5)); s.append(T(X(w),262,tex=str(w),size=18))
    s.append(T(1060,284,mix='파장(nm)',size=18,anchor='end',fill=MUTED))
    return '<svg class="fig" viewBox="0 0 1080 292" style="width:1080px" aria-label="수소 기체 방전관의 빛이 슬릿과 프리즘을 지나 네 개의 선(410.1, 434.1, 486.1, 656.3 nm)으로 나뉘고, 태양빛은 이어진 무지개 띠가 된다">'+''.join(s)+'</svg>'
FIG['TUBE']=tube()

# ═══ S10 회절격자 원리
def grating():
    s=[]; gx=170
    s.append(f'<rect x="{gx-5}" y="32" width="10" height="250" fill="#C9D3DD"/>')
    slits=[70,130,190,250]
    for y in slits: s.append(f'<rect x="{gx-5}" y="{y-6}" width="10" height="12" fill="#fff"/>')
    for y in slits: s.append(A(40,y,gx-12,y,'ink',2))
    s.append(T(60,300,mix='들어오는 빛',size=19,anchor='start'))
    th=math.radians(28); Ln=230
    for i,y in enumerate(slits[1:3]):
        s.append(A(gx+6,y,gx+6+Ln*math.cos(th),y-Ln*math.sin(th),'minus' if i==0 else 'minus',2.5))
    yA,yB=130,190
    # path difference: from slit A draw perpendicular to ray from B
    # ray dir u=(cos,-sin); foot of A onto B's ray
    ux,uy=math.cos(th),-math.sin(th); bx,by=gx+6,yB; ax,ay=gx+6,yA
    t=(ax-bx)*ux+(ay-by)*uy; fx,fy=bx+ux*t,by+uy*t
    s.append(L(ax,ay,fx,fy,MUTED,1.8,dash='5 4'))
    s.append(L(bx,by,fx,fy,EQUI,6,extra='stroke-linecap="round" opacity=".85"'))
    s.append(T(fx-4,by+34,mix='경로 차 $d\\sin\\theta$',size=20,anchor='start',fill=EQUI,halo=True))
    s.append(L(gx-22,yA,gx-22,yB,MUTED,1.5)); s.append(L(gx-27,yA,gx-17,yA,MUTED,1.5)); s.append(L(gx-27,yB,gx-17,yB,MUTED,1.5))
    s.append(T(gx-30,(yA+yB)/2+7,tex='d',size=22,anchor='end',halo=True))
    s.append(L(gx+6,yB,gx+6+90,yB,MUTED,1.5,dash='4 4'))
    pts=[(gx+6+70*math.cos(a),yB-70*math.sin(a)) for a in [i*th/20 for i in range(21)]]
    s.append(P(pts,MUTED,1.8)); s.append(T(gx+6+82,yB-14,tex='\\theta',size=22,anchor='start'))
    s.append(T(gx,24,mix='회절격자',size=19))
    s.append(T(505,300,mix='보강 간섭 → 밝은 선',size=19,anchor='end',fill=MINUS))
    return '<svg class="fig" viewBox="0 0 520 312" style="width:500px" aria-label="회절격자의 이웃한 두 틈을 지난 빛이 각 theta로 나아갈 때 경로 차가 d sin theta이다">'+''.join(s)+'</svg>'
FIG['GRATING']=grating()

# ═══ S11 과정 카드 그림
def step1():
    s=[f'<rect x="40" y="40" width="200" height="80" rx="6" fill="#F3E7D3" stroke="{INK}" stroke-width="2"/>',
       f'<rect x="36" y="64" width="8" height="32" fill="#fff" stroke="{INK}" stroke-width="1.5"/>',L(40,74,40,86,'#111',3),
       T(40,30,mix='슬릿(1 mm 이하)',size=19,anchor='start'),T(140,88,mix='종이 상자',size=19)]
    return '<svg viewBox="0 0 280 140" aria-label="종이 상자 한쪽 끝의 좁은 슬릿">'+''.join(s)+'</svg>'
def step2():
    s=[f'<rect x="40" y="40" width="200" height="80" rx="6" fill="#F3E7D3" stroke="{INK}" stroke-width="2"/>',
       f'<rect x="232" y="50" width="14" height="60" fill="#D9E6F2" stroke="{MINUS}" stroke-width="2" transform="rotate(-20 239 80)"/>',
       T(236,32,mix='회절격자 필름',size=19,anchor='end'),T(130,88,mix='반대쪽 끝',size=19)]
    return '<svg viewBox="0 0 280 140" aria-label="반대쪽 끝에 비스듬히 붙인 회절격자 필름">'+''.join(s)+'</svg>'
def step3():
    s=[f'<circle cx="34" cy="70" r="20" fill="#FFF3B0" stroke="{EQUI}" stroke-width="2"/>',T(34,116,mix='광원',size=19),
       f'<rect x="70" y="50" width="130" height="40" rx="5" fill="#F3E7D3" stroke="{INK}" stroke-width="2"/>',
       f'<path d="M224 70 q14 -14 28 0 q-14 14 -28 0 Z" fill="#fff" stroke="{INK}" stroke-width="2"/><circle cx="238" cy="70" r="5" fill="{INK}"/>',
       A(204,70,220,70,'ink',2),T(238,116,mix='눈',size=19)]
    return '<svg viewBox="0 0 280 140" aria-label="광원을 향해 슬릿을 두고 격자 쪽에서 들여다보기">'+''.join(s)+'</svg>'
FIG['STEP1']=step1();FIG['STEP2']=step2();FIG['STEP3']=step3()

# ═══ S14 계단과 비탈
def stairs():
    s=[]; x0,y0=30,190
    pts=[(x0,y0)]
    for i in range(4): pts+= [(x0+i*55,y0-i*40-40),(x0+(i+1)*55,y0-i*40-40)]
    s.append(P(pts+[(x0+220,y0),(x0,y0)],INK,2,fill='#EEF3F8',close=True))
    s.append(f'<g data-anim="move" data-from="0,-40" data-dur=".9" data-delay=".6" data-ease="bounce">{C(x0+82,y0-80-12,12,INK,2,fill="#8C99A6")}</g>')
    s.append(T(140,214,mix='계단: 정해진 높이만',size=19))
    s.append(P([(300,190),(500,30),(500,190)],INK,2,fill='#EEF3F8',close=True))
    s.append(C(390,190-72*160/200-12-2,12,INK,2,fill='#8C99A6'))
    s.append(T(400,214,mix='비탈: 어떤 높이든',size=19))
    return '<svg class="fig" viewBox="0 0 520 224" style="width:440px" aria-label="계단 위 공은 정해진 높이에만 놓이고, 비탈 위 공은 어떤 높이에도 놓일 수 있다">'+''.join(s)+'</svg>'
FIG['STAIRS']=stairs()

# ═══ S15 고전 vs 보어
def classical():
    s=[]; cx,cy=150,140
    pts=[]
    for i in range(0,400):
        t=i/400*4*math.pi; r=110*math.exp(-t/4.5); pts.append((cx+r*math.cos(t),cy-r*math.sin(t)))
    s.append(P(pts,MUTED,1.8,dash='5 4')); s.append(nuc(cx,cy,12))
    ex,ey=pts[-1]
    s.append(f'<g data-anim="move" data-from="{f(cx+110-ex)},{f(cy-ey)}" data-dur="1.8" data-delay=".3" data-ease="in">{ele(ex+14,ey-6,9)}</g>')
    s.append(T(150,282,mix='에너지를 잃고 핵에 떨어진다?',size=19))
    return '<svg class="fig" viewBox="0 0 300 296" style="width:300px" aria-label="고전 역학에 따르면 전자가 나선을 그리며 원자핵에 떨어진다">'+''.join(s)+'</svg>'
def bohrorb():
    s=[]; cx,cy=150,140
    for r in (40,75,110): s.append(C(cx,cy,r,MUTED,1.8,dash='6 6'))
    s.append(nuc(cx,cy,12))
    s.append(f'<g data-anim="spin" data-o="{cx},{cy}" data-speed="40">{ele(cx+75,cy,9)}</g>')
    for i,r in enumerate((40,75,110)): s.append(T(cx+r*0.71+4,cy+r*0.71+16,tex=f'n={i+1}',size=19,anchor='start',halo=True))
    s.append(T(150,282,mix='정해진 원 궤도에서는 안정',size=19))
    return '<svg class="fig" viewBox="0 0 300 296" style="width:300px" aria-label="보어 모형: 정해진 원 궤도를 도는 전자는 에너지를 잃지 않는다">'+''.join(s)+'</svg>'
FIG['CLASSIC']=classical();FIG['BOHRORB']=bohrorb()

# ═══ S16 준위 도표
def levels():
    s=[]; E0=2.178e-18
    Y=lambda n: 30 if n==0 else 30+360*(1/n**2)   # n=0 => infinity
    s.append(A(24,400,24,24,'ink',2.5)); s.append(T(36,24,mix='에너지',size=19,anchor='start'))
    vals={1:'-2.178\\times10^{-18}',2:'-5.45\\times10^{-19}',3:'-2.42\\times10^{-19}',4:'-1.36\\times10^{-19}'}
    lv=[]
    for n in (1,2,3,4,5,6,0):
        y=Y(n); dash='6 5' if n==0 else None
        lv.append(L(220,y,420,y,INK,2.5 if n and n<5 else 1.6,dash))
    s.append('<g data-anim="draw" data-dur="1.2" data-delay=".2">'+''.join(lv)+'</g>')
    for n in (1,2,3,0):
        y=Y(n); s.append(T(430,y+7,tex='n=\\infty' if n==0 else f'n={n}',size=20,anchor='start'))
        s.append(T(210,y+7,tex=('0' if n==0 else vals[n]),size=19,anchor='end'))
    s.append(T(205,420,mix='단위: J',size=19,anchor='end',fill=MUTED))
    s.append(T(320,Y(1)-12,mix='바닥상태',size=19,fill=FIELD,weight=700))
    s.append(T(320,Y(2)-12,mix='들뜬상태',size=19,fill=MUTED))
    return '<svg class="fig" viewBox="0 0 500 430" style="width:470px" aria-label="수소 원자의 에너지 준위: n=1 -2.178e-18 J, n=2 -5.45e-19 J, n=3 -2.42e-19 J, n=무한대 0">'+''.join(s)+'</svg>'
FIG['LEVELS']=levels()

# ═══ S17 전이 도표
def trans():
    s=[]; Y=lambda n: 30 if n==0 else 30+400*(1/n**2)
    for n in (1,2,3,4,5,6,0):
        s.append(L(60,Y(n),540,Y(n),INK,2.2 if n and n<4 else 1.4,'6 5' if n==0 else None))
    for n in (1,2,3,0): s.append(T(546,Y(n)+(2 if n==0 else 9),tex='n=\\infty' if n==0 else f'n={n}',size=22,anchor='start'))
    s.append(A(30,470,30,30,'ink',2.5)); s.append(T(40,24,mix='에너지',size=22,anchor='start'))
    for k,ni in enumerate((2,3,4,5,6)): s.append(A(100+k*18,Y(ni),100+k*18,Y(1),'ink',2.2))
    s.append(T(150,Y(1)+30,mix='라이먼 계열 (자외선)',size=22))
    bal={3:HC[656],4:HC[486],5:HC[434],6:HC[410]}
    s.append('<g class="step" data-g="b1">'+''.join(f'<g data-anim="draw" data-on="step" data-dur=".5" data-delay="{.15*k:.2f}">{A(255+k*26,Y(ni),255+k*26,Y(2),bal[ni],3.2)}</g>' for k,ni in enumerate((3,4,5,6)))+'</g>')
    s.append(T(300,Y(2)+30,mix='발머 계열 (가시광선)',size=22))
    for k,ni in enumerate((4,5,6)): s.append(A(440+k*22,Y(ni),440+k*22,Y(3),'ink',2.2))
    s.append(T(440,Y(3)+32,mix='파센 계열 (적외선)',size=22,halo=True))
    # 파장 띠
    bx0,bx1,by=60,560,512; X=lambda w: bx0+w/2000*(bx1-bx0)
    s.append(f'<rect x="{bx0}" y="{by}" width="{bx1-bx0}" height="30" fill="#2A2F38"/>')
    lam=lambda nf,ni: 6.626e-34*3.00e8/(2.178e-18*(1/nf**2-1/ni**2))*1e9
    for nf,nis in ((1,range(2,8)),(2,range(3,8)),(3,range(4,9))):
        for ni in nis:
            w=lam(nf,ni); col=wcol(w) or '#E9EEF3'
            s.append(f'<rect x="{f(X(w)-1.5)}" y="{by}" width="3" height="30" fill="{col}"/>')
    for w in (0,500,1000,1500,2000): s.append(L(X(w),by+30,X(w),by+36,MUTED,1.5)); s.append(T(X(w),by+60,tex=str(w),size=21))
    s.append(T(X(2000),by-8,mix='파장(nm)',size=21,anchor='end',fill=MUTED))
    s.append(T(X(150),by-8,mix='자외선',size=21)); s.append(T(X(560),by-8,mix='가시광선',size=21)); s.append(T(X(1250),by-8,mix='적외선',size=21))
    return '<svg class="fig" viewBox="0 0 620 578" style="width:500px" aria-label="수소 원자의 전자 전이: n=1로 가는 라이먼 계열(자외선), n=2로 가는 발머 계열(가시광선), n=3으로 가는 파센 계열(적외선)과 파장 띠">'+''.join(s)+'</svg>'
FIG['TRANS']=trans()

# ═══ S20 힘 그림
def force():
    s=[]; cx,cy=150,150; r=100
    s.append(C(cx,cy,r,MUTED,1.8,dash='6 6')); s.append(nuc(cx,cy,14)); s.append(T(cx,cy+40,tex='+Ze',size=20,fill=PLUS))
    ex,ey=cx+r*math.cos(math.radians(-40)),cy+r*math.sin(math.radians(-40))
    s.append(ele(ex,ey,10)); s.append(T(ex+16,ey-12,tex='-e',size=20,anchor='start',fill=MINUS))
    u=((cx-ex)/r,(cy-ey)/r)
    s.append(A(ex+u[0]*14,ey+u[1]*14,ex+u[0]*62,ey+u[1]*62,'plus',3))
    s.append(T(ex+u[0]*38+14,ey+u[1]*38+26,mix='쿨롱 힘',size=19,fill=PLUS,anchor='start',halo=True))
    t=(-u[1],u[0])  # tangent
    s.append(A(ex+t[0]*14,ey+t[1]*14,ex+t[0]*-0+t[0]*70,ey+t[1]*70,'ink',3))
    s.append(T(ex+t[0]*78+6,ey+t[1]*78,tex='v',size=22,anchor='start'))
    s.append(L(cx,cy,cx-r,cy,MUTED,1.5)); s.append(T(cx-r/2,cy-8,tex='r',size=22))
    return '<svg class="fig" viewBox="0 0 320 300" style="width:300px" aria-label="원자핵 +Ze 둘레를 반지름 r로 도는 전자 -e, 원자핵 쪽 쿨롱 힘과 접선 방향 속도 v">'+''.join(s)+'</svg>'
FIG['FORCE']=force()

# ═══ S21 궤도 반지름 비
def radii():
    s=[]; cx,cy=150,150; k=13
    for n in (1,2,3):
        s.append(f'<g data-anim="scale" data-from=".2" data-o="{cx},{cy}" data-dur="1" data-delay="{.2+.3*n:.1f}">{C(cx,cy,k*n*n,MUTED,1.8,dash="5 5")}</g>')
    s.append(nuc(cx,cy,6))
    s.append(T(cx+k*1+4,cy-6,tex='r_1',size=18,anchor='start',halo=True))
    s.append(T(cx+k*4*0.71+6,cy-k*4*0.71,tex='r_2=4r_1',size=19,anchor='start',halo=True))
    s.append(T(cx+k*9*0.6,cy+k*9*0.8+4,tex='r_3=9r_1',size=19,anchor='start',halo=True))
    return '<svg class="fig" viewBox="0 0 300 300" style="width:280px" aria-label="수소 원자 궤도 반지름 r1, 4r1, 9r1">'+''.join(s)+'</svg>'
FIG['RADII']=radii()

# ═══ S25 정상파
def standing():
    s=[]; R0=66; A0=11
    def ring(cx,cy,n,laps=1,th0=0):
        pts=[]; N=360*laps
        for i in range(N+1):
            t=th0+i/360*2*math.pi
            pts.append((cx+(R0+A0*math.sin(n*t))*math.cos(t),cy-(R0+A0*math.sin(n*t))*math.sin(t)))
        return pts
    labs=[('(가)','n=4'),('(나)','n=5'),('(다)','n=4\\tfrac{1}{3}')]
    for i,(nm,nn) in enumerate(labs):
        cx=110+i*230; cy=110
        s.append(C(cx,cy,R0,MUTED,1.5,fill='#FFF8E1'))
        if i<2:
            s.append(P(ring(cx,cy,4+i),PLUS,2.5))
        else:
            p=ring(cx,cy,4+1/3,2); s.append(P(p[:361],PLUS,2.5)); s.append(f'<g data-anim="draw" data-dur="1.6" data-delay=".6">{P(p[360:],PLUS,2.5)}</g>')
            s.append(T(cx,cy-12,mix='불일치',size=19,fill=PLUS,weight=700))
        s.append(T(cx,cy+(20 if i==2 else 8),tex=nn,size=22))
        s.append(T(cx,214,mix=nm,size=20))
    return '<svg class="fig" viewBox="0 0 680 226" style="width:640px" aria-label="원주가 파장의 정수배인 n=4, n=5 정상파와, 정수배가 아닌 n=4와 1/3의 불일치">'+''.join(s)+'</svg>'
FIG['STAND']=standing()

# ═══ S26 회절
def diffr():
    s=[f'<rect x="20" y="96" width="90" height="48" rx="6" fill="#E3EEF8" stroke="{INK}" stroke-width="2"/>',T(65,170,mix='전자총',size=19)]
    s.append(f'<g data-anim="dash" data-speed="40" data-flow="1">{L(112,120,236,120,MINUS,3,"8 8")}</g>')
    s.append(L(112,120,236,120,MINUS,2.5)); s.append(T(174,108,mix='전자살',size=19,fill=MINUS))
    for i in range(5):
        for j in range(5): s.append(f'<circle cx="{250+i*14}" cy="{92+j*14}" r="4" fill="{GRAV}"/>')
    s.append(T(278,182,mix='니켈 단결정',size=19))
    for a in (-28,-14,0,14,28): s.append(L(318,120,500,120+math.tan(math.radians(a))*182,MINUS,1.4,"4 4"))
    s.append(f'<ellipse cx="520" cy="120" rx="16" ry="100" fill="#F3F5F8" stroke="{INK}" stroke-width="2"/>')
    for r,o in ((80,.35),(52,.55),(26,.75)): s.append(f'<ellipse cx="520" cy="120" rx="{r*0.16:.1f}" ry="{r}" fill="none" stroke="{MINUS}" stroke-width="3.5" opacity="{o}"/>')
    s.append(f'<circle cx="520" cy="120" r="4" fill="{MINUS}"/>')
    s.append(T(560,236,mix='회절 무늬',size=19,anchor='end'))
    return '<svg class="fig" viewBox="0 0 600 248" style="width:560px" aria-label="전자총에서 나온 전자살이 니켈 단결정에서 회절해 화면에 동심원 무늬를 만든다">'+''.join(s)+'</svg>'
FIG['DIFFR']=diffr()

# ═══ S27 불확정성 (파속)
def unc():
    s=[]
    def packet(y,sig,k):
        pts=[];
        for i in range(0,401):
            x=40+i; t=(x-220)
            pts.append((x,y-34*math.exp(-t*t/(2*sig*sig))*math.cos(k*t)))
        return pts
    s.append(L(40,70,400,70,MUTED,1,'3 4')); s.append(P(packet(70,14,.45),MINUS,2.5))
    s.append(L(196,112,244,112,EQUI,3)); s.append(T(220,136,tex='\\Delta x\\ \\text{작음}',size=19))
    for a in (-34,-18,0,16,30): s.append(A(440,70,440+70*math.cos(math.radians(a)),70+70*math.sin(math.radians(a))*0.9,'ink',2))
    s.append(T(560,138,tex='\\Delta p\\ \\text{큼}',size=19,anchor='end'))
    s.append(L(40,220,400,220,MUTED,1,'3 4')); s.append(P(packet(220,70,.25),MINUS,2.5))
    s.append(L(80,262,360,262,EQUI,3)); s.append(T(220,286,tex='\\Delta x\\ \\text{큼}',size=19))
    s.append(A(440,220,540,220,'ink',2.5)); s.append(T(560,252,tex='\\Delta p\\ \\text{작음}',size=19,anchor='end'))
    s.append(T(16,30,mix='(가)',size=20,anchor='start')); s.append(T(16,180,mix='(나)',size=20,anchor='start'))
    return '<svg class="fig" viewBox="0 0 580 298" style="width:520px" aria-label="(가) 좁게 모인 파동은 위치 불확정성이 작고 운동량이 여러 방향으로 퍼진다. (나) 길게 퍼진 파동은 위치 불확정성이 크고 운동량이 하나로 정해진다">'+''.join(s)+'</svg>'
FIG['UNC']=unc()

# ═══ S28 psi, psi^2
def psi():
    s=[]; x0,x1=40,480; X=lambda r: x0+r/12*(x1-x0)
    f2=lambda r:(2-r)*math.exp(-r/2)
    y1=90; y2=250
    s.append(A(x0,y1,x1+10,y1,'muted',1.6)); s.append(A(x0,y1+50,x0,y1-70,'muted',1.6))
    s.append(P([(X(r/50),y1-34*f2(r/50)) for r in range(0,601)],INK,2.6))
    s.append(T(x0+10,y1-60,tex='\\psi',size=22,anchor='start'))
    s.append(A(x0,y2,x1+10,y2,'muted',1.6)); s.append(A(x0,y2+6,x0,y2-110,'muted',1.6))
    s.append(P([(X(r/50),y2-24*f2(r/50)**2) for r in range(0,601)],MINUS,2.6))
    s.append(T(x0+10,y2-92,tex='\\psi^2',size=22,anchor='start',fill=MINUS))
    s.append(L(X(2),y1-70,X(2),y2+6,MUTED,1.6,'5 5')); s.append(T(X(2)+8,y1+36,mix='마디',size=19,anchor='start',halo=True))
    s.append(T(x1+6,y1+30,tex='r',size=20,anchor='end')); s.append(T(x1+6,y2+30,tex='r',size=20,anchor='end'))
    s.append(f'<circle cx="{f(X(2))}" cy="{y2}" r="5" fill="{EQUI}"/>')
    s.append(T(X(5),y1+30,mix='(−) 부분',size=19,fill=MUTED))
    return '<svg class="fig" viewBox="0 0 500 290" style="width:470px" aria-label="파동 함수 psi는 부호가 바뀌고, 확률 밀도 psi 제곱은 0 이상이며, psi가 0인 곳이 마디이다">'+''.join(s)+'</svg>'
FIG['PSI']=psi()

# ═══ S29 구형 극좌표
def polar():
    s=[]; O=(170,200); Z=(170,30); Xa=(60,300); Ya=(350,215)
    s.append(A(*O,*Z,'ink',2)); s.append(A(*O,*Xa,'ink',2)); s.append(A(*O,*Ya,'ink',2))
    s.append(T(182,34,tex='z',size=22,anchor='start')); s.append(T(56,290,tex='x',size=22,anchor='end')); s.append(T(352,236,tex='y',size=22,anchor='start'))
    Pp=(275,92); Q=(262,236)
    s.append(L(*O,*Pp,MINUS,3)); s.append(L(*Pp,*Q,MUTED,1.6,'5 4')); s.append(L(*O,*Q,MUTED,1.6,'5 4'))
    s.append(f'<circle cx="{Pp[0]}" cy="{Pp[1]}" r="6" fill="{MINUS}"/>'); s.append(T(Pp[0]+12,Pp[1]-6,tex='P',size=22,anchor='start'))
    s.append(T((O[0]+Pp[0])/2+14,(O[1]+Pp[1])/2+8,tex='r',size=22,anchor='start',fill=MINUS,halo=True))
    def arc(c,a1,a2,rr,sx=1,sy=1):
        return [(c[0]+rr*math.cos(math.radians(a1+(a2-a1)*i/20))*sx,c[1]-rr*math.sin(math.radians(a1+(a2-a1)*i/20))*sy) for i in range(21)]
    angP=math.degrees(math.atan2(O[1]-Pp[1],Pp[0]-O[0]))
    s.append(P(arc(O,90,angP,48),EQUI,2.2)); s.append(T(O[0]+24,O[1]-56,tex='\\theta',size=22,fill=EQUI))
    angX=math.degrees(math.atan2(O[1]-Xa[1],Xa[0]-O[0])); angQ=math.degrees(math.atan2(O[1]-Q[1],Q[0]-O[0]))
    s.append(P(arc(O,angX,angQ+360 if angQ<angX else angQ,40),EQUI,2.2)); s.append(T(O[0]+2,O[1]+62,tex='\\phi',size=22,fill=EQUI))
    return '<svg class="fig" viewBox="0 0 380 310" style="width:340px" aria-label="구형 극좌표계: 원점에서 점 P까지 거리 r, z축과 이루는 각 theta, x축에서 잰 각 phi">'+''.join(s)+'</svg>'
FIG['POLAR']=polar()

# ═══ S30 1s
def ones():
    s=[]; random.seed(11); cx,cy=130,150
    for i in range(700):
        u=random.random()
        # sample r from P(r)=4 r^2 e^{-2r}: gamma(3, 1/2)
        r=sum(-math.log(random.random()) for _ in range(3))/2
        a=random.random()*6.283; rr=r*34*abs(math.cos(random.random()*1.57))  # 2D projection
        if rr<120: s.append(f'<circle cx="{f(cx+rr*math.cos(a))}" cy="{f(cy+rr*math.sin(a))}" r="1.9" fill="{MINUS}" opacity=".5"/>')
    s.append(nuc(cx,cy,5)); s.append(T(cx,304,mix='(가) 전자구름',size=19))
    # graph R^2
    gx0,gx1,gy0,gy1=320,620,250,50; X=lambda r: gx0+r/5*(gx1-gx0)
    s.append(A(gx0,gy0,gx1+12,gy0,'muted',1.6)); s.append(A(gx0,gy0,gx0,gy1-14,'muted',1.6))
    s.append(P([(X(r/40),gy0-(gy0-gy1)*math.exp(-2*r/40)) for r in range(0,201)],MINUS,2.8))
    s.append(T(gx0+12,gy1-2,mix='확률 밀도 $R^2(r)$',size=19,anchor='start',fill=MINUS))
    s.append(T(gx1+4,gy0+28,mix='$r$',size=20,anchor='end'))
    s.append(T((gx0+gx1)/2,304,mix='(나) 확률 밀도',size=19))
    # graph P
    hx0,hx1=700,1020; Xh=lambda r: hx0+r/5*(hx1-hx0); Pm=4*math.exp(-2)
    s.append(A(hx0,gy0,hx1+12,gy0,'muted',1.6)); s.append(A(hx0,gy0,hx0,gy1-14,'muted',1.6))
    s.append(P([(Xh(r/40),gy0-(gy0-gy1)*0.95*Pr(R1,r/40)/Pm) for r in range(0,201)],INK,2.8))
    s.append(L(Xh(1),gy0,Xh(1),gy0-(gy0-gy1)*0.95,MUTED,1.5,'5 4'))
    s.append(f'<circle cx="{f(Xh(1))}" cy="{f(gy0-(gy0-gy1)*0.95)}" r="6" fill="{EQUI}"/>')
    s.append(T(Xh(1),gy0+24,tex='a_0',size=20,fill=EQUI))
    s.append(T(Xh(1)+16,gy1+6,mix='$P(r)=r^2R^2(r)$',size=19,anchor='start'))
    s.append(T(hx1+4,gy0+28,mix='$r$',size=20,anchor='end'))
    s.append(T((hx0+hx1)/2,304,mix='(다) 방사 방향 확률 분포',size=19))
    return '<svg class="fig" viewBox="0 0 1050 314" style="width:1050px" aria-label="1s 오비탈: 전자구름은 원자핵 가까이 진하고, 확률 밀도는 원자핵에서 가장 크며, 방사 방향 확률 분포는 보어 반지름 a0에서 가장 크다">'+''.join(s)+'</svg>'
FIG['ONES']=ones()

# ═══ S31 1s 2s 3s
def rdf():
    s=[]; x0,x1,y0,y1=70,600,300,30; X=lambda r: x0+r/20*(x1-x0); Y=lambda p: y0-(p/0.6)*(y0-y1)
    for p in (0.1,0.2,0.3,0.4,0.5): s.append(L(x0,Y(p),x1,Y(p),'#E2E7EC',1)); s.append(T(x0-8,Y(p)+6,tex=f'{p:.1f}',size=18,anchor='end'))
    s.append(A(x0,y0,x1+14,y0,'muted',1.6)); s.append(A(x0,y0,x0,y1-14,'muted',1.6))
    for r in (0,5,10,15,20): s.append(L(X(r),y0,X(r),y0+6,MUTED,1.5)); s.append(T(X(r),y0+28,tex=str(r),size=18))
    s.append(T((x0+x1)/2,y0+56,mix='거리 $r$ ($a_0$)',size=19))
    for nm,Rf,col,g in (('1s',R1,INK,'c1'),('2s',R2,FIELD,'c2'),('3s',R3,BF,'c3')):
        pts=[(X(i/100),Y(Pr(Rf,i/100))) for i in range(0,2001)]
        s.append(f'<g data-anim="draw" data-dur="1.4" data-delay="{ {"c1":.2,"c2":.8,"c3":1.4}[g] }">{P(pts,col,2.8)}</g>')
    s.append(T(X(1)+10,Y(0.54)+4,tex='1s',size=20,anchor='start',fill=INK))
    s.append(T(X(5.24),Y(0.191)-12,tex='2s',size=20,fill=FIELD))
    s.append(T(X(13.07),Y(0.1015)-12,tex='3s',size=20,fill=BF))
    for r in (2.0,): s.append(L(X(r),y0,X(r),Y(0.13),FIELD,1.6,'4 4'))
    for r in (1.902,7.098): s.append(L(X(r),y0,X(r),Y(0.1),BF,1.6,'4 4'))
    s.append(T(X(7.098)+4,Y(0.1)-6,mix='마디',size=18,anchor='start',fill=MUTED,halo=True))
    s.append(T(x0+10,24,mix='방사 방향 확률 분포',size=18,anchor='start'))
    return '<svg class="fig" viewBox="0 0 620 366" style="width:550px" aria-label="수소 1s, 2s, 3s 오비탈의 방사 방향 확률 분포: 1s는 a0에서 최대, 2s는 봉우리 2개와 마디 1개, 3s는 봉우리 3개와 마디 2개">'+''.join(s)+'</svg>'
FIG['RDF']=rdf()
def bound():
    s=[]; k=5.1; cy=105; x=4
    for i,(nm,r90,nodes) in enumerate((('1s',2.66,[]),('2s',9.13,[2.0]),('3s',19.44,[1.902,7.098]))):
        rr=r90*k; cxx=x+rr; x=cxx+rr+12
        s.append(f'<circle cx="{f(cxx)}" cy="{cy}" r="{f(rr)}" fill="{MINUS}" fill-opacity=".16" stroke="{MINUS}" stroke-width="1.6"/>')
        for nd in nodes: s.append(C(cxx,cy,nd*k,MUTED,1.4,dash='3 3'))
        s.append(f'<circle cx="{f(cxx)}" cy="{cy}" r="2.5" fill="{INK}"/>')
        s.append(T(cxx,cy+rr+24 if i<2 else cy+rr+24,tex=nm,size=20))
    return '<svg class="fig" viewBox="0 0 352 244" style="width:300px" aria-label="1s, 2s, 3s 오비탈의 90 퍼센트 경계면 크기 비교와 마디(점선 원)">'+''.join(s)+'</svg>'
FIG['BOUND']=bound()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out))
