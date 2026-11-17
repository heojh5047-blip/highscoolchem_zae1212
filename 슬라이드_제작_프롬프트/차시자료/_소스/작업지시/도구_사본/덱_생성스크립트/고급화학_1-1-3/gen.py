# -*- coding: utf-8 -*-
"""고급화학 1-1-3 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다."""
import math, random, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/1-1-3_원자_오비탈의_모양과_원자의_전자_배치/slides.html'
exec(open(os.path.join(HERE,'helpers.py'),encoding='utf-8').read())
PLUS_='#D7263D'
FIG={}
def svg(vb,w,label,body,cls='fig',extra=''):
    return f'<svg class="{cls}" viewBox="{vb}" style="width:{w}px" aria-label="{label}"{(" "+extra) if extra else ""}>'+''.join(body)+'</svg>'

# ── 전자 배치 상자
def harp(cx,y,h,up,col=INK,w=2.6):
    if up: return P([(cx,y+h-6),(cx,y+6),(cx-6,y+14)],col,w,extra='stroke-linecap="round"')
    return P([(cx,y+6),(cx,y+h-6),(cx+6,y+h-14)],col,w,extra='stroke-linecap="round"')
def ebox(x,y,occ,w=36,h=36,new=(),lab=None,lsize=20,hund=True,wrap=None):
    """occ: 칸마다 '', 'u', 'd', 'ud', 'uud'(3개, 틀린 예). new: {(칸, 'u'|'d')} → field"""
    s=[]
    for i,o in enumerate(occ):
        bx=x+i*w
        fill=f'fill="{EQUI}" fill-opacity=".18"' if (hund and len(o)==1) else 'fill="#fff"'
        s.append(f'<rect x="{f(bx)}" y="{f(y)}" width="{w}" height="{h}" {fill} stroke="{INK}" stroke-width="1.5"/>')
        cx=bx+w/2
        if len(o)==1: xs=[cx]
        elif len(o)==2: xs=[cx-6,cx+6]
        else: xs=[cx-9,cx,cx+9]
        for j,ch in enumerate(o):
            col=FIELD if (i,ch) in new else INK
            s.append(harp(xs[j],y,h,ch=='u',col))
    if lab: s.append(T(x+len(occ)*w/2,y+h+lsize+4,tex=lab,size=lsize))
    g=''.join(s)
    return f'<g {wrap}>{g}</g>' if wrap else g

# ── 오비탈 엽 (화면 투영)
AX={'x':(-0.56,0.46),'y':(1.0,0.0),'z':(0.0,-1.0)}
def proj(d):
    return (d[0]*AX['x'][0]+d[1]*AX['y'][0]+d[2]*AX['z'][0], d[0]*AX['x'][1]+d[1]*AX['y'][1]+d[2]*AX['z'][1])
def lobe(cx,cy,d,L,sign,W=1.35,lab=True,lsize=20):
    vx,vy=proj(d); k=math.hypot(vx,vy); ux,uy=vx/k,vy/k; px,py=-uy,ux; Ls=L*max(k,0.55)
    pts=[]
    for i in range(0,61):
        th=math.radians(-90+3*i); rho=Ls*math.cos(th)**2
        a=rho*math.cos(th); b=W*L*0.62*math.cos(th)**2*math.sin(th)
        pts.append((cx+ux*a+px*b,cy+uy*a+py*b))
    col=BF if sign>0 else GRAV
    s=P(pts,col,1.8,fill=col,close=True,extra='fill-opacity=".30"')
    if lab: s+=T(cx+ux*Ls*0.6,cy+uy*Ls*0.6+lsize*0.36,tex='+' if sign>0 else '-',size=lsize,weight=700)
    return s
def axes(cx,cy,A=90,lsize=20,labs=True):
    s=[]
    for k,(vx,vy) in AX.items():
        sc=0.8 if k=='x' else 1
        x2,y2=cx+vx*A*sc,cy+vy*A*sc; x1,y1=cx-vx*A*sc*0.85,cy-vy*A*sc*0.85
        s.append(L(x1,y1,x2,y2,MUTED,1.4))
        if labs:
            off={'x':(-8,16),'y':(12,6),'z':(10,4)}[k]
            s.append(T(x2+off[0],y2+off[1],tex=k,size=lsize,anchor='middle',fill=MUTED))
    return ''.join(s)
def plane(cx,cy,a,b,A):
    (ax,ay),(bx,by)=proj(a),proj(b)
    pts=[(cx+A*(sa*ax+sb*bx),cy+A*(sa*ay+sb*by)) for sa,sb in ((1,1),(1,-1),(-1,-1),(-1,1))]
    return P(pts,MUTED,1.3,dash='5 4',close=True)

# ═══ 표지
def cover():
    s=['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    cx,cy=270,200
    s.append(axes(cx,cy,150,22))
    ds=[((1,0,0),'x'),((0,1,0),'y'),((0,0,1),'z')]
    for i,(d,nm) in enumerate(ds):
        g=lobe(cx,cy,(-d[0],-d[1],-d[2]),110,-1,lab=False)+lobe(cx,cy,d,110,1,lab=False)
        s.append(f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".7" data-delay="{.2+.4*i:.1f}">{g}</g>')
    s.append(T(cx+128,cy-8,tex='2p_y',size=22,anchor='start',halo=True))
    s.append(T(cx+12,cy-118,tex='2p_z',size=22,anchor='start',halo=True))
    s.append(T(cx-104,cy+106,tex='2p_x',size=22,anchor='end',halo=True))
    occ=['ud','ud','ud','u','u']; x0=[118,186,262]
    s.append(ebox(118,414,['ud'],40,40,lab='1s'))
    s.append(ebox(186,414,['ud'],40,40,lab='2s'))
    s.append(f'<g data-anim="fade" data-dur=".8" data-delay="1.6">'+ebox(262,414,['ud','u','u'],40,40,lab='2p')+'</g>')
    s.append(T(270,400,mix='산소 원자의 전자 배치',size=20))
    return svg('0 0 540 540',540,'세 축 방향의 2p 오비탈 엽과 산소 원자의 전자 배치 상자(1s 둘, 2s 둘, 2p 넷 중 홀전자 둘)',s,cls='cover-fig',extra='data-audit="skip"')
FIG['COVER']=cover()

# ═══ S3 경계면 비교(1-1-1과 같은 비율)
def bound():
    s=[]; k=4.2; cy=90; x=4
    for i,(nm,r90,nodes) in enumerate((('1s',2.66,[]),('2s',9.13,[2.0]),('3s',19.44,[1.902,7.098]))):
        rr=r90*k; cxx=x+rr; x=cxx+rr+14
        s.append(f'<circle cx="{f(cxx)}" cy="{cy}" r="{f(rr)}" fill="{MINUS}" fill-opacity=".16" stroke="{MINUS}" stroke-width="1.6"/>')
        for nd in nodes: s.append(C(cxx,cy,nd*k,MUTED,1.4,dash='3 3'))
        s.append(f'<circle cx="{f(cxx)}" cy="{cy}" r="2.5" fill="{INK}"/>')
        s.append(T(cxx,cy+rr+24,tex=nm,size=20))
    return svg('0 0 300 210',300,'1s, 2s, 3s 오비탈의 경계면 크기 비교와 마디(점선 원)',s)
FIG['BOUND']=bound()

# ═══ S5 껍질
def shells():
    s=[]; cx,cy=170,186; rs=[26,62,102,146]; names=['K','L','M','N']
    for i,r in enumerate(rs):
        g=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{MINUS}" stroke-width="14" stroke-opacity=".22"/>'+C(cx,cy,r,MINUS,1.2)
        s.append(f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.2+.3*i:.1f}">{g}</g>')
    s.append(nuc(cx,cy,10))
    for i,r in enumerate(rs):
        s.append(T(cx+r,cy+7,tex=names[i],size=20,halo=True,weight=700))
        s.append(T(cx-r,cy+7,tex=str(i+1),size=20,halo=True))
    s.append(T(cx-100,26,mix='주 양자수 $n$',size=19)); s.append(T(cx+100,26,mix='껍질',size=19))
    return svg('0 0 340 340',330,'원자핵을 중심으로 n=1 K, n=2 L, n=3 M, n=4 N 껍질이 바깥으로 갈수록 커진다',s)
FIG['SHELLS']=shells()

# ═══ S8 껍질-부껍질-오비탈 (수소)
def tree():
    s=[]; ys={1:286,2:180,3:70}; w=34; xs={'s':150,'p':236,'d':390}
    s.append(A(26,318,26,24,'muted',2)); s.append(T(40,30,mix='에너지',size=19,anchor='start',fill=MUTED))
    s.append(T(xs['s']+17,18,mix='s ($l=0$)',size=19)); s.append(T(xs['p']+51,18,mix='p ($l=1$)',size=19)); s.append(T(xs['d']+85,18,mix='d ($l=2$)',size=19))
    shell={1:'K',2:'L',3:'M'}
    for n in (1,2,3):
        y=ys[n]; g=[]
        g.append(T(48,y+7,mix=f'$n={n}$ ({shell[n]})',size=20,anchor='start'))
        g.append(ebox(xs['s'],y-17,[''],w,34,hund=False)); g.append(T(xs['s']+17,y+40,tex=f'{n}s',size=19))
        if n>=2:
            g.append(ebox(xs['p'],y-17,['']*3,w,34,hund=False))
            for j,m in enumerate((-1,0,1)): g.append(T(xs['p']+17+j*w,y+38,tex=str(m),size=18))
            g.append(T(xs['p']+3*w+8,y+7,tex=f'{n}p',size=19,anchor='start'))
        if n>=3:
            g.append(ebox(xs['d'],y-17,['']*5,w,34,hund=False))
            for j,m in enumerate((-2,-1,0,1,2)): g.append(T(xs['d']+17+j*w,y+38,tex=str(m),size=18))
            g.append(T(xs['d']+5*w+8,y+7,tex=f'{n}d',size=19,anchor='start'))
        s.append(f'<g data-anim="fade" data-dur=".6" data-delay="{.2+.4*(n-1):.1f}">{"".join(g)}</g>')
    s.append(T(xs['p']+51,ys[2]+64,mix='칸 아래 숫자: $m_l$',size=18,fill=MUTED))
    return svg('0 0 620 336',600,'수소 원자의 껍질, 부껍질, 오비탈: n=1에 1s, n=2에 2s와 2p 세 칸, n=3에 3s, 3p 세 칸, 3d 다섯 칸이 같은 높이에 있다',s)
FIG['TREE']=tree()

# ═══ S9 s, p 오비탈
def sp():
    s=[]; W=250
    # 1s
    cx,cy=125,130
    s.append(axes(cx,cy,92))
    s.append(f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay=".2"><circle cx="{cx}" cy="{cy}" r="58" fill="{MINUS}" fill-opacity=".22" stroke="{MINUS}" stroke-width="1.6"/></g>')
    s.append(T(cx,262,tex='1s',size=22))
    for i,(d,nm,pl) in enumerate((((1,0,0),'2p_x',((0,1,0),(0,0,1))),((0,1,0),'2p_y',((1,0,0),(0,0,1))),((0,0,1),'2p_z',((1,0,0),(0,1,0)))) ):
        cx=125+W*(i+1)
        s.append(plane(cx,cy,pl[0],pl[1],46))
        s.append(axes(cx,cy,92))
        g=lobe(cx,cy,(-d[0],-d[1],-d[2]),70,-1)+lobe(cx,cy,d,70,1)
        s.append(f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.5+.35*i:.2f}">{g}</g>')
        s.append(T(cx,262,tex=nm,size=22))
    s.append(T(985,30,mix='점선: 마디면',size=18,anchor='end',fill=MUTED))
    return svg('0 0 1000 276',1000,'1s 오비탈은 구 모양이고, 2px, 2py, 2pz 오비탈은 각각 x, y, z 축 방향의 아령 모양으로 원자핵을 지나는 마디면으로 나뉜 두 엽(+와 −)으로 되어 있다',s)
FIG['SP']=sp()

# ═══ S10 3d 오비탈
def dorb():
    s=[]; W=212; cy=118; L=58
    r2=1/math.sqrt(2)
    defs=[('3d_{xz}',[((r2,0,r2),1),((-r2,0,-r2),1),((r2,0,-r2),-1),((-r2,0,r2),-1)]),
          ('3d_{yz}',[((0,r2,r2),1),((0,-r2,-r2),1),((0,r2,-r2),-1),((0,-r2,r2),-1)]),
          ('3d_{xy}',[((r2,r2,0),1),((-r2,-r2,0),1),((r2,-r2,0),-1),((-r2,r2,0),-1)]),
          ('3d_{x^2-y^2}',[((1,0,0),1),((-1,0,0),1),((0,1,0),-1),((0,-1,0),-1)]),
          ('3d_{z^2}',None)]
    for i,(nm,lb) in enumerate(defs):
        cx=106+W*i; g=[]
        s.append(axes(cx,cy,86,19))
        if lb:
            lb=sorted(lb,key=lambda t:-t[0][0])  # 뒤쪽(-x)부터
            lb=sorted(lb,key=lambda t:t[0][0])
            for d,sg in lb: g.append(lobe(cx,cy,d,L,sg,W=1.25,lsize=19))
        else:
            g.append(lobe(cx,cy,(0,0,-1),L+4,1,W=1.1,lsize=19))
            g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="38" ry="15" fill="{GRAV}" fill-opacity=".30" stroke="{GRAV}" stroke-width="1.8"/>')
            g.append(T(cx+50,cy+12,tex='-',size=19,weight=700))
            g.append(lobe(cx,cy,(0,0,1),L+4,1,W=1.1,lsize=19))
        s.append(f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.2+.3*i:.1f}">{"".join(g)}</g>')
        s.append(T(cx,240,tex=nm,size=22))
    return svg('0 0 1060 254',1060,'3d 오비탈 다섯 개: dxz, dyz, dxy는 두 축 사이로 네 엽, dx2-y2는 x축과 y축 위에 네 엽, dz2는 z축 위 두 엽과 가운데 고리',s)
FIG['DORB']=dorb()

# ═══ S11 연대표
def timeline():
    s=[]; x0,x1,y=200,880,62; X=lambda yr: x0+(yr-1920)/(1965-1920)*(x1-x0)
    s.append(A(x0-20,y,x1+16,y,'muted',2))
    ev=[(1923,'X선의 입자성 발견',-1,255,'end'),(1926,'파동 방정식 발표',1,300,'end'),(1927,'전자의 파동성 증명',-1,296,'start'),(1933,'노벨 물리학상',1,380,'start'),(1944,'「생명은 무엇인가?」',-1,660,'middle'),(1961,'「나의 세계관」',1,890,'end')]
    for yr,t,up,lx,anc in ev:
        x=X(yr); ly=y-22 if up>0 else y+38
        s.append(f'<circle cx="{f(x)}" cy="{y}" r="6" fill="{INK if yr!=1926 else EQUI}"/>')
        s.append(T(lx,ly,mix=f'{yr} · {t}',size=19,anchor=anc,weight=700 if yr==1926 else None))
    return svg('0 0 900 110',900,'1923년 X선의 입자성 발견, 1926년 슈뢰딩거 파동 방정식 발표, 1927년 전자의 파동성 증명, 1933년 노벨 물리학상, 1944년 책 출간, 1961년 책 출간',s)
FIG['TIME']=timeline()

# ═══ S12 스펙트럼 비교
def specs():
    s=[]; x0,x1=110,700; X=lambda w: x0+(w-380)/(720-380)*(x1-x0)
    data=[('수소',[(410.2,.5),(434.0,.6),(486.1,.8),(656.3,1)]),
          ('수은',[(404.7,.7),(407.8,.4),(435.8,1),(491.6,.3),(546.1,1),(577.0,.8),(579.1,.8),(623.4,.3),(690.7,.3)]),
          ('스트론튬',[(407.8,.8),(421.6,.7),(430.5,.4),(460.7,1),(483.2,.5),(487.2,.4),(496.2,.6),(515.6,.3),(548.1,.4),(640.8,.9),(650.4,.7),(655.0,.4),(661.7,.4),(687.8,.6),(707.0,.7)])]
    for i,(nm,ln) in enumerate(data):
        y=14+i*58
        s.append(T(x0-14,y+27,mix=nm,size=20,anchor='end',weight=700))
        s.append(f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="40" fill="#111" rx="3"/>')
        g=''.join(f'<rect x="{f(X(w)-1.6)}" y="{y}" width="3.2" height="40" fill="{wcol(w)}" opacity="{.45+.55*a:.2f}"/>' for w,a in ln)
        s.append(f'<g data-anim="fade" data-dur=".8" data-delay="{.2+.4*i:.1f}">{g}</g>')
    yb=14+3*58-10
    for w in (400,500,600,700): s.append(L(X(w),yb,X(w),yb+6,MUTED,1.5)); s.append(T(X(w),yb+28,tex=str(w),size=18))
    s.append(T(x1,yb+52,mix='파장(nm)',size=18,anchor='end',fill=MUTED))
    return svg('0 0 720 246',720,'수소는 선 네 개, 수은과 스트론튬은 선이 많고 가까이 몰린 선 스펙트럼을 보인다',s)
FIG['SPECS']=specs()

# ═══ S13 가려막기
def shield():
    s=[]; cx,cy=150,160
    s.append(f'<g data-anim="fade" data-dur="1" data-delay=".2"><circle cx="{cx}" cy="{cy}" r="70" fill="{MINUS}" fill-opacity=".16" stroke="{MINUS}" stroke-width="1.5" stroke-dasharray="5 4"/></g>')
    random.seed(5)
    for i in range(10):
        a=random.random()*6.283; r=24+random.random()*38
        s.append(ele(cx+r*math.cos(a),cy+r*math.sin(a),7))
    s.append(nuc(cx,cy,13))
    s.append(T(cx,cy-82,mix='안쪽 전자 10개',size=19,fill=MINUS))
    s.append(T(cx-10,cy+98,mix='원자핵 (핵전하 $+11$)',size=19))
    ex,ey=372,cy
    s.append(P([(cx+222*math.cos(math.radians(a)),cy+222*math.sin(math.radians(a))) for a in range(-40,41,2)],MUTED,1.4,dash='5 5'))
    s.append(ele(ex,ey,10))
    s.append(A(ex-16,ey,232,ey,'ink',4)); s.append(T(300,ey-14,mix='$Z_\\text{eff}$',size=20,halo=True))
    s.append(T(ex+16,ey+36,mix='바깥 전자',size=19,fill=MINUS,anchor='start'))
    s.append(T(330,ey+76,mix='실제로 느끼는 핵전하는||$+11$보다 작다',size=18))
    return svg('0 0 460 290',440,'원자핵(+11) 둘레의 안쪽 전자 10개가 가려막아, 바깥 전자 하나가 실제로 느끼는 핵전하 Zeff는 +11보다 작다',s)
FIG['SHIELD']=shield()

# ═══ S14 3s 3p 3d 방사 분포
s3,s6,s30=math.sqrt(3),math.sqrt(6),math.sqrt(30)
R3s=lambda r:2/(81*s3)*(27-18*r+2*r*r)*math.exp(-r/3)
R3p=lambda r:4/(81*s6)*(6*r-r*r)*math.exp(-r/3)
R3d=lambda r:4/(81*s30)*r*r*math.exp(-r/3)
def rdf3():
    s=[]; x0,x1,y0,y1=70,600,290,34; X=lambda r: x0+r/30*(x1-x0); Y=lambda p: y0-(p/0.12)*(y0-y1)
    for p in (0.04,0.08,0.12): s.append(L(x0,Y(p),x1,Y(p),'#E2E7EC',1)); s.append(T(x0-8,Y(p)+6,tex=f'{p:.2f}',size=18,anchor='end'))
    s.append(A(x0,y0,x1+14,y0,'muted',1.6)); s.append(A(x0,y0,x0,y1-18,'muted',1.6))
    for r in (0,10,20,30): s.append(L(X(r),y0,X(r),y0+6,MUTED,1.5)); s.append(T(X(r),y0+28,tex=str(r),size=18))
    s.append(T((x0+x1)/2,y0+54,mix='거리 $r$ ($a_0$)',size=19))
    s.append(f'<ellipse cx="{f(X(2.6))}" cy="{f(Y(0.02))}" rx="58" ry="34" fill="{EQUI}" fill-opacity=".14" stroke="{EQUI}" stroke-width="1.8" stroke-dasharray="5 4"/>')
    for i,(nm,Rf,col) in enumerate((('3d',R3d,PLUS_),('3p',R3p,FIELD),('3s',R3s,BF))):
        pts=[(X(j/40),Y((j/40)**2*Rf(j/40)**2)) for j in range(0,1201)]
        s.append(f'<g data-anim="draw" data-dur="1.4" data-delay="{.2+.6*i:.1f}">{P(pts,col,2.8)}</g>')
    s.append(T(X(9)-6,Y(0.107)-12,tex='3d',size=21,fill=PLUS_,anchor='end',weight=700))
    s.append(T(X(12),Y(0.102)-14,tex='3p',size=21,fill=FIELD,weight=700))
    s.append(T(X(16.4),Y(0.092),tex='3s',size=21,fill=BF,anchor='start',weight=700))
    s.append(T(X(2.6)+66,Y(0.045),mix='3s의 작은 봉우리:||원자핵 가까이',size=18,fill=EQUI,anchor='start',halo=True))
    s.append(T(x0+10,24,mix='방사 방향 확률 분포',size=18,anchor='start'))
    return svg('0 0 620 352',560,'수소 원자의 3s, 3p, 3d 오비탈의 방사 방향 확률 분포: 3s는 원자핵 가까이 작은 봉우리가 두 개 있어 가장 잘 침투하고, 3d는 봉우리 하나',s)
FIG['RDF3']=rdf3()

# ═══ S15 에너지 준위 비교
def elev():
    s=[]
    hy={1:360,2:262,3:180,4:112}
    my={'1s':360,'2s':290,'2p':258,'3s':205,'3p':178,'4s':142,'3d':124,'4p':92}
    col_h={'s':40,'p':96,'d':152,'f':208}; col_m={'s':330,'p':402,'d':474}
    s.append(A(16,384,16,40,'muted',2)); s.append(T(26,40,mix='에너지',size=19,anchor='start',fill=MUTED))
    s.append(T(150,26,mix='수소 원자',size=20,weight=700)); s.append(T(430,26,mix='다전자 원자',size=20,weight=700))
    for n in (1,2,3,4):
        for l,lt in enumerate('spdf'[:n]):
            x=col_h[lt]; y=hy[n]
            s.append(L(x,y,x+44,y,INK,3)); s.append(T(x+22,y-8,tex=f'{n}{lt}',size=18))
    for i,(nm,y) in enumerate(my.items()):
        n=int(nm[0]); lt=nm[1]; x=col_m[lt]; dy=hy[n]-y
        g=L(x,y,x+50,y,INK,3)+T(x+25,y-8,tex=nm,size=18)
        s.append(f'<g data-anim="move" data-from="0,{dy}" data-dur="1" data-delay="{.3+.08*i:.2f}" data-ease="io">{g}</g>')
    s.append(A(262,230,316,230,'muted',2.5))
    return svg('0 0 540 396',500,'수소 원자는 주 양자수가 같으면 에너지가 같지만, 다전자 원자는 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p 순으로 에너지가 높아진다',s)
FIG['ELEV']=elev()
def diag():
    s=[]; cw,ch=58,40; x0,y0=34,26
    rows={1:'s',2:'sp',3:'spd',4:'spdf',5:'spdf',6:'spd',7:'sp'}
    pos={}
    for n,ls in rows.items():
        for l,lt in enumerate(ls):
            x=x0+l*cw+cw/2; y=y0+(n-1)*ch+ch/2; pos[(n,l)]=(x,y)
            s.append(T(x,y+7,tex=f'{n}{lt}',size=20))
    for k in range(1,9):
        cells=sorted([(n,l) for (n,l) in pos if n+l==k],key=lambda t:-t[1])
        (xa,ya),(xb,yb)=pos[cells[0]],pos[cells[-1]]
        s.append(A(xa+22,ya-17,xb-22,yb+17,'equi',1.8))
    return svg('0 0 270 312',250,'채우는 순서 대각선 그림: 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, 5p, 6s, 4f, 5d, 6p, 7s 순',s)
FIG['DIAG']=diag()

# ═══ S16 스핀
def spin():
    s=[]
    s.append(f'<rect x="10" y="96" width="60" height="44" rx="6" fill="#E3EEF8" stroke="#7E8B98" stroke-width="2"/>')
    s.append(T(62,166,mix='수소 원자살',size=18))
    s.append(f'<polygon points="190,40 290,40 266,104 214,104" fill="#E9B9B9" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<rect x="190" y="132" width="100" height="52" fill="#B9C9E9" stroke="{INK}" stroke-width="1.6"/>')
    s.append(T(240,82,tex='N',size=22,weight=700)); s.append(T(240,166,tex='S',size=22,weight=700))
    s.append(T(240,212,mix='불균일한 자기장',size=18))
    beam=f'<g data-anim="draw" data-dur="1.2" data-delay=".2">'+P([(70,118),(210,118)],MINUS,3)+P([(210,118),(300,118),(400,58)],MINUS,3)+P([(210,118),(300,118),(400,178)],MINUS,3)+'</g>'
    s.append(beam)
    s.append(L(404,30,404,206,INK,3)); s.append(T(404,226,mix='검출판',size=18))
    s.append(f'<circle cx="404" cy="58" r="7" fill="{MINUS}"/><circle cx="404" cy="178" r="7" fill="{MINUS}"/>')
    s.append(T(404,124,mix='두 갈래',size=18,fill=MINUS,halo=True))
    for i,(cx,up) in enumerate(((560,True),(700,False))):
        cy=118
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="44" ry="12" fill="none" stroke="{MUTED}" stroke-width="1.6"/>')
        s.append(ele(cx,cy,22))
        ax=A(cx,cy+46,cx,cy-50,'ink',3) if up else A(cx,cy-46,cx,cy+50,'ink',3)
        s.append(ax)
        # 회전 방향 화살
        if up: s.append(A(cx+30,cy+9,cx-14,cy+12,'muted',2))
        else: s.append(A(cx-30,cy+9,cx+14,cy+12,'muted',2))
        s.append(T(cx,cy+90,tex=('m_s=+\\tfrac{1}{2}' if up else 'm_s=-\\tfrac{1}{2}'),size=21))
    s.append(T(630,26,mix='스핀 방향이 다른 두 전자',size=18,fill=MUTED))
    return svg('0 0 770 236',770,'수소 원자살이 불균일한 자기장을 지나며 두 갈래로 나뉘고, 오른쪽에 스핀 방향이 반대인 두 전자 ms = +1/2, -1/2',s)
FIG['SPIN']=spin()

# ═══ S17 파울리
def pauli():
    s=[]; items=[(['ud'],'○','반대 스핀 2개',INK),(['uu'],'×','네 양자수가 모두 같다',PLUS_),(['uud'],'×','3개는 들어갈 수 없다',PLUS_)]
    for i,(occ,mk,why,col) in enumerate(items):
        x=70+i*210
        b=ebox(x,40,[occ[0].replace('uu','uu')],60,60,hund=False)
        if occ[0]=='uu':
            b=f'<rect x="{x}" y="40" width="60" height="60" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'+harp(x+22,40,60,True)+harp(x+38,40,60,True)
        s.append(b)
        g=T(x+98,82,mix=mk,size=30,fill=col,weight=700)
        s.append(f'<g data-anim="pop" data-o="{x+98},72" data-dur=".5" data-delay="{.3+.4*i:.1f}">{g}</g>')
        s.append(T(x+44,136,mix=why,size=19))
    return svg('0 0 640 152',620,'오비탈 한 칸: 반대 스핀 두 전자는 가능, 같은 스핀 두 전자와 전자 세 개는 불가능',s)
FIG['PAULI']=pauli()

# ═══ S18 훈트
def hund():
    s=[]; items=[(['u','u','u'],'○','홀전자 3개',INK),(['ud','u',''],'×','홀전자 1개',PLUS_),(['u','d','u'],'×','스핀이 나란하지 않다',PLUS_)]
    for i,(occ,mk,why,col) in enumerate(items):
        x=20+i*250
        g=ebox(x,40,occ,48,48,lab='2p',hund=(i==0))
        s.append(f'<g data-anim="fade" data-dur=".6" data-delay="{.2+.35*i:.2f}">{g}</g>')
        s.append(T(x+174,74,mix=mk,size=30,fill=col,weight=700))
        s.append(T(x+72,146,mix=why,size=19))
    return svg('0 0 760 160',740,'질소의 2p 전자 세 개: 세 칸에 같은 스핀으로 하나씩(○), 한 칸에 짝지음(×), 스핀이 나란하지 않음(×)',s)
FIG['HUND']=hund()
def carb(): return svg('0 0 170 84',170,'탄소의 2p 오비탈: 두 칸에 같은 스핀 전자 하나씩, 한 칸은 비어 있다',[ebox(4,4,['u','u',''],48,48,lab='2p',lsize=18)])
FIG['CARB']=carb()

# ═══ S19 표 Ⅰ-2 상자
T2=[('',['u'],['','',''],{(0,'u')},set()),('',['ud'],['','',''],{(0,'d')},set()),
    ('',['ud'],['u','',''],set(),{(0,'u')}),('',['ud'],['u','u',''],set(),{(1,'u')}),
    ('',['ud'],['u','u','u'],set(),{(2,'u')}),('',['ud'],['ud','u','u'],set(),{(0,'d')}),
    ('',['ud'],['ud','ud','u'],set(),{(1,'d')}),('',['ud'],['ud','ud','ud'],set(),{(2,'d')})]
for i,(_,a,b,na,nb) in enumerate(T2):
    body=[ebox(2,2,a,30,30,new=na),ebox(50,2,b,30,30,new=nb)]
    FIG[f'T2_{11+i}']=svg('0 0 144 34',144,'3s, 3p 오비탈 도표',body)

# ═══ S25 주기율표
PT=["H,,,,,,,,,,,,,,,,,He","Li,Be,,,,,,,,,,,B,C,N,O,F,Ne","Na,Mg,,,,,,,,,,,Al,Si,P,S,Cl,Ar",
    "K,Ca,Sc,Ti,V,Cr,Mn,Fe,Co,Ni,Cu,Zn,Ga,Ge,As,Se,Br,Kr","Rb,Sr,Y,Zr,Nb,Mo,Tc,Ru,Rh,Pd,Ag,Cd,In,Sn,Sb,Te,I,Xe",
    "Cs,Ba,La*,Hf,Ta,W,Re,Os,Ir,Pt,Au,Hg,Tl,Pb,Bi,Po,At,Rn","Fr,Ra,Ac*,Rf,Db,Sg,Bh,Hs,Mt,Ds,Rg,Cn,Nh,Fl,Mc,Lv,Ts,Og"]
FR=["Ce,Pr,Nd,Pm,Sm,Eu,Gd,Tb,Dy,Ho,Er,Tm,Yb,Lu","Th,Pa,U,Np,Pu,Am,Cm,Bk,Cf,Es,Fm,Md,No,Lr"]
BLK={'s':'#E6F1FB','p':'#E9F6EF','d':'#FDF1DE','f':'#F1ECFA'}
METALLOID={'B','Si','Ge','As','Sb','Te'}
def ptable():
    s=[]; cw,ch=44,34; x0,y0=6,30
    def tx(sym): return '\\mathrm{'+sym.replace('*','')+'}'+('^{*}' if '*' in sym else '')
    for g in range(18): s.append(T(x0+g*cw+cw/2,y0-8,tex=str(g+1),size=18,fill=MUTED))
    groups={b:[] for b in 'spdf'}; mlo=[]
    for p,row in enumerate(PT):
        for g,sym in enumerate(row.split(',')):
            if not sym: continue
            b='s' if (g<2 or sym=='He') else ('d' if g<12 else 'p')
            x=x0+g*cw; y=y0+p*ch
            groups[b].append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{BLK[b]}" stroke="#AAB5C0" stroke-width="1"/>'+T(x+cw/2,y+ch/2+7,tex=tx(sym),size=18))
            if sym in METALLOID: mlo.append(f'<rect x="{x+1.5}" y="{y+1.5}" width="{cw-3}" height="{ch-3}" fill="none" stroke="{INK}" stroke-width="3"/>')
    fy=y0+7*ch+14
    for r,row in enumerate(FR):
        for j,sym in enumerate(row.split(',')):
            x=x0+(j+3)*cw; y=fy+r*ch
            groups['f'].append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{BLK["f"]}" stroke="#AAB5C0" stroke-width="1"/>'+T(x+cw/2,y+ch/2+7,tex=tx(sym),size=18))
    for i,b in enumerate('spdf'):
        s.append(f'<g data-anim="fade" data-dur=".6" data-delay="{.2+.35*i:.2f}">{"".join(groups[b])}</g>')
    s+=mlo
    s.append(T(x0+2*cw+4,fy+ch/2+7,mix='*란타넘족',size=18,anchor='end'))
    s.append(T(x0+2*cw+4,fy+ch*1.5+7,mix='*악티늄족',size=18,anchor='end'))
    s.append(T(x0+7.5*cw,y0+ch*1.1,mix='전이 원소 (3–12족)',size=20,weight=700))
    s.append(P([(x0+2*cw+6,y0+ch*1.55),(x0+2*cw+6,y0+ch*2.4),(x0+12*cw-6,y0+ch*2.4),(x0+12*cw-6,y0+ch*1.55)],MUTED,1.6))
    # 범례
    ly=fy+2*ch+30; lx=x0
    for i,(b,nm) in enumerate((('s','s 블록'),('p','p 블록'),('d','d 블록'),('f','f 블록'))):
        s.append(f'<rect x="{lx+i*120}" y="{ly-16}" width="22" height="20" fill="{BLK[b]}" stroke="#AAB5C0"/>'); s.append(T(lx+i*120+30,ly,mix=nm,size=18,anchor='start'))
    s.append(f'<rect x="{lx+490}" y="{ly-16}" width="22" height="20" fill="#fff" stroke="{INK}" stroke-width="3"/>'); s.append(T(lx+520,ly,mix='준금속',size=18,anchor='start'))
    return svg(f'0 0 {x0*2+18*cw} {ly+12}',800,'현대적 주기율표: 1–2족 s 블록, 13–18족 p 블록, 3–12족 d 블록(전이 원소), 아래 두 줄 f 블록. 준금속 B, Si, Ge, As, Sb, Te는 굵은 테',s)
FIG['PT']=ptable()

# ═══ S26 원자 반지름
def radii():
    s=[]; k=0.2
    col=[('Li',152,40),('Na',186,0),('K',227,0)]
    xC=118; rL,rN,rK=152*k,186*k,227*k
    yL=14+rL; yN=yL+rL+16+rN; yK=yN+rN+16+rK
    def atom(x,y,sym,pm,i):
        r=pm*k
        g=f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{GRAV}" fill-opacity=".28" stroke="{MUTED}" stroke-width="1.6"/>'+T(x,y+7,tex='\\mathrm{'+sym+'}',size=20,weight=700)
        return f'<g data-anim="pop" data-o="{f(x)},{f(y)}" data-dur=".5" data-delay="{.2+.12*i:.2f}">{g}</g>'
    s.append(atom(xC,yL,'Li',152,0)); s.append(T(xC-rL-8,yL+6,tex='152',size=18,anchor='end'))
    s.append(atom(xC,yN,'Na',186,1)); s.append(T(xC-rN-8,yN+6,tex='186',size=18,anchor='end'))
    s.append(atom(xC,yK,'K',227,2)); s.append(T(xC-rK-8,yK+6,tex='227',size=18,anchor='end'))
    row=[('Mg',160),('Al',143),('Si',118),('P',110),('S',103),('Cl',99)]
    x=xC; pr=rN
    for i,(sym,pm) in enumerate(row):
        r=pm*k; x=x+pr+14+r; pr=r
        s.append(atom(x,yN,sym,pm,3+i)); s.append(T(x,yN+r+24,tex=str(pm),size=18))
    xe=x+pr
    s.append(A(xC+rN+14,yN-rN-22,xe,yN-rN-22,'ink',2.5)); s.append(T((xC+rN+xe)/2,yN-rN-32,mix='같은 주기: 작아짐',size=19))
    s.append(A(xC+rK+30,yN+rN+44,xC+rK+30,yK+rK-6,'ink',2.5)); s.append(T(xC+rK+42,yK+10,mix='같은 족: 커짐',size=19,anchor='start'))
    s.append(T(xe,yK+rK+4,mix='단위: pm',size=18,anchor='end',fill=MUTED))
    return svg(f'0 0 {f(xe+16)} {f(yK+rK+12)}',560,'원자 반지름: 3주기 Na 186, Mg 160, Al 143, Si 118, P 110, S 103, Cl 99 pm로 작아지고, 1족 Li 152, Na 186, K 227 pm로 커진다',s)
FIG['RADII']=radii()

# ═══ S27 이온화 에너지
IE=[1312,2372,520,899,801,1086,1402,1314,1681,2081,496,738,578,787,1012,1000,1251,1521,419,590]
SYM=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca']
def iegraph():
    s=[]; x0,x1,y0,y1=76,590,282,30; X=lambda z: x0+z*(x1-x0)/21; Y=lambda e: y0-e/2500*(y0-y1)
    for e in (500,1000,1500,2000,2500): s.append(L(x0,Y(e),x1,Y(e),'#E2E7EC',1)); s.append(T(x0-8,Y(e)+6,tex=str(e),size=18,anchor='end'))
    s.append(A(x0,y0,x1+14,y0,'muted',1.6)); s.append(A(x0,y0,x0,y1-16,'muted',1.6))
    for z in (1,5,10,15,20): s.append(L(X(z),y0,X(z),y0+6,MUTED,1.5)); s.append(T(X(z),y0+28,tex=str(z),size=18))
    s.append(T((x0+x1)/2,y0+54,mix='원자 번호',size=19))
    s.append(T(x0+8,20,mix='첫째 이온화 에너지 (kJ/mol)',size=18,anchor='start'))
    pts=[(X(z+1),Y(e)) for z,e in enumerate(IE)]
    s.append(f'<g data-anim="draw" data-dur="1.8" data-delay=".2">{P(pts,INK,2.4)}</g>')
    for z,e in enumerate(IE):
        c=PLUS_ if SYM[z] in ('He','Ne','Ar') else (MINUS if SYM[z] in ('Li','Na','K') else INK)
        s.append(f'<circle cx="{f(X(z+1))}" cy="{f(Y(e))}" r="{6 if c!=INK else 4}" fill="{c}"/>')
        if SYM[z] in ('He','Ne','Ar'): s.append(T(X(z+1)+10,Y(e)+2,tex='\\mathrm{'+SYM[z]+'}',size=18,anchor='start',fill=PLUS_))
        if SYM[z] in ('Li','Na','K'): s.append(T(X(z+1),Y(e)+28,tex='\\mathrm{'+SYM[z]+'}',size=18,fill=MINUS))
    return svg('0 0 610 346',610,'원자 번호 1–20의 첫째 이온화 에너지: 18족 He, Ne, Ar에서 가장 크고 1족 Li, Na, K에서 가장 작으며, 한 주기에서 대체로 증가한다',s)
FIG['IE']=iegraph()

# ═══ S29 철 3d
def fe3d():
    s=[]
    s.append(T(4,30,tex='\\mathrm{Fe}',size=20,anchor='start')); s.append(ebox(70,6,['ud','u','u','u','u'],38,38,lab='3d',lsize=18)); s.append(ebox(276,6,['ud'],38,38,lab='4s',lsize=18))
    s.append(T(4,110,tex='\\mathrm{Fe^{2+}}',size=20,anchor='start')); s.append(ebox(70,86,['ud','u','u','u','u'],38,38,lab='3d',lsize=18)); s.append(ebox(276,86,[''],38,38,lab='4s',lsize=18))
    s.append(T(4,190,tex='\\mathrm{Cr}',size=20,anchor='start')); s.append(ebox(70,166,['u','u','u','u','u'],38,38,lab='3d',lsize=18)); s.append(ebox(276,166,['u'],38,38,lab='4s',lsize=18))
    return svg('0 0 330 242',330,'철: 3d 짝 하나와 홀전자 넷, 4s 짝. 철(Ⅱ) 이온: 3d 같고 4s 빔. 크로뮴: 3d 다섯 칸과 4s 한 칸에 홀전자 하나씩',s)
FIG['FE3D']=fe3d()

def one(k,kind='fade'):
    v=re.sub(r'<g data-anim="[^"]*"(?: data-[a-z]+="[^"]*")*>','<g>',FIG[k])
    i=v.index('>')+1; FIG[k]=v[:i]+f'<g data-anim="{kind}" data-dur="1" data-delay=".2">'+v[i:-6]+'</g></svg>'
for k in ('SHELLS','TREE','DORB','SPECS','PAULI','HUND','PT','RADII'): one(k)
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out))
