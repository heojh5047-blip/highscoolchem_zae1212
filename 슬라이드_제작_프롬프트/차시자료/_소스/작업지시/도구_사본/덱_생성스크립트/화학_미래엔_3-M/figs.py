import math
INK='#16233D';MUT='#5B6B7F';FIELD='#2E9E6A';BF='#7B4FC8';NO2C='#B5562A'
def T(x,y,s,size=20,anchor='middle',fill=INK,mix=True,extra=''):
    a='data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{x:.1f}" y="{y:.1f}" {a}="{s}" data-size="{size}" data-anchor="{anchor}" fill="{fill}"{extra}></text>'
def axes(x0,y0,x1,y1,ylab,xlab='시간',ticks=(),tickfmt=str,ystep=1.0,yscale=45):
    o=[f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{INK}" stroke-width="2"/>',
       f'<g data-arw="{x1-12},{y0},{x1+4},{y0},ink,2"></g>',
       f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{INK}" stroke-width="2"/>',
       f'<g data-arw="{x0},{y1+12},{x0},{y1-4},ink,2"></g>',
       T(x0+10,y1+14,ylab,19,'start',extra=''),
       T(x1-4,y0+30,xlab,19,'end'),T(x0-10,y0+22,'0',19,'end')]
    for v in ticks:
        y=y0-v/ystep*yscale
        o.append(f'<line x1="{x0-5}" y1="{y:.1f}" x2="{x0}" y2="{y:.1f}" stroke="{INK}" stroke-width="2"/>')
        o.append(T(x0-10,y+7,tickfmt(v),19,'end'))
    return o
def curve(x0,x2,v0,v1,y0,ystep,yscale,xend):
    pts=[]
    for i in range(41):
        u=i/40; f=1-(1-u)**2; x=x0+(x2-x0)*u; v=v0+(v1-v0)*f
        pts.append((x,y0-v/ystep*yscale))
    pts.append((xend,y0-v1/ystep*yscale))
    return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
def path(d,col,w=3.5,anim=True,delay=.3,dash=''):
    a=f' data-anim="draw" data-dur="1.6" data-delay="{delay}"' if anim else ''
    da=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{da}{a}/>'
def dot(x1,y1,x2,y2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{MUT}" stroke-width="1.6" stroke-dasharray="4 4"/>'
ORA='#E4572E';BLU='#3D8BD9';GRN='#43A047'
def g01():
    x0,y0,xp,xe,ys,sc=70,250,250,400,1,45
    o=axes(x0,y0,xe+20,25,'양 [mol]',ticks=(1,2,3,4))
    o.append(path(curve(x0,xp,4,1,y0,ys,sc,xe),ORA))
    o.append(path(curve(x0,xp,0,2,y0,ys,sc,xe),BLU,delay=.5))
    ut=1-math.sqrt(.5); xt=x0+(xp-x0)*ut
    o.append(dot(xt,y0,xt,y0-2.5*sc)); o.append(dot(x0,y0-sc,xt,y0-sc))
    o.append(dot(x0,y0-2*sc,xp,y0-2*sc)); o.append(dot(x0,y0-sc,xp,y0-sc));o.append(dot(xp,y0,xp,y0-2*sc))
    o.append(T(xt,y0+26,'$t$',20)); o.append(T(xe-20,y0-2*sc-12,'B',21,fill=BLU)); o.append(T(xe-20,y0-sc+30,'A',21,fill=ORA))
    return f'<svg class="fig" viewBox="0 0 440 290" style="width:440px" aria-label="A의 양은 4 몰에서 1 몰로 줄고 B의 양은 0에서 2 몰로 늘어 일정해지는 그래프. 시간 t에서 B는 1 몰">'+''.join(o)+'</svg>'
def g04():
    x0,y0,xp,xe,ys,sc=80,250,260,410,.1,52
    fmt=lambda v:f'{v:.1f}'
    o=axes(x0,y0,xe+20,22,'양 [mol]',ticks=(.1,.2,.3,.4),tickfmt=fmt,ystep=.1,yscale=sc)
    o.append(path(curve(x0,xp,.4,.1,y0,ys,sc,xe),ORA))
    o.append(path(curve(x0,xp,.3,.2,y0,ys,sc,xe),BLU,delay=.45))
    o.append(path(curve(x0,xp,0,.2,y0,ys,sc,xe),GRN,delay=.6))
    for f,lab in ((.5,'$t_1$'),(.8,'$t_2$')):
        u=1-math.sqrt(1-f); x=x0+(xp-x0)*u
        top=max(.4-.3*f,.3-.1*f)
        o.append(dot(x,y0,x,y0-top/ys*sc)); o.append(T(x,y0+26,lab,20))
    u1=1-math.sqrt(.5);x1=x0+(xp-x0)*u1
    o.append(dot(x0,y0-.1/ys*sc,x1,y0-.1/ys*sc))
    o.append(dot(x0,y0-.2/ys*sc,xp,y0-.2/ys*sc)); o.append(dot(x0,y0-.1/ys*sc,xp,y0-.1/ys*sc))
    o.append(T(x0+22,y0-.4/ys*sc+18,'A',20,fill=ORA)); o.append(T(x0+18,y0-.3/ys*sc+30,'B',20,fill=BLU)); o.append(T(x0+40,y0-30,'C',20,fill=GRN))
    return f'<svg class="fig" viewBox="0 0 450 290" style="width:450px" aria-label="A 0.4 몰이 0.1 몰로, B 0.3 몰이 0.2 몰로 줄고 C가 0에서 0.2 몰로 늘어 일정해지는 그래프. t1에서 A와 B의 양이 같고 t2에서 A와 C의 양이 같다">'+''.join(o)+'</svg>'
# --- particles (scale .5: N 12, O 12)
def no2(x,y,ang=0,r=12):
    d=1.35*r; o=[]
    for s in (-67,67):
        a=math.radians(ang+s-90)
        o.append(f'<g data-atom="{x+d*math.cos(a):.1f},{y+d*math.sin(a):.1f},{r},O,-"></g>')
    o.append(f'<g data-atom="{x:.1f},{y:.1f},{r},N,-"></g>')
    return ''.join(o)
def n2o4(x,y,r=12):
    d=.8*r
    return no2(x-d,y,-90,r)+no2(x+d,y,90,r)
def box(x,y,w,h,mols,tint,label,anim=''):
    o=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{NO2C}" fill-opacity="{tint}" stroke="#7E8B98" stroke-width="3"/>']
    for kind,mx,my in mols:
        o.append(no2(x+mx,y+my,0) if kind=='a' else n2o4(x+mx,y+my))
    o.append(T(x+w/2,y+h+30,label,20))
    return ''.join(o)
def legend(x,y):
    return (f'<g data-atom="{x},{y},12,N,-"></g>'+T(x+18,y+7,'N',19,'start')+
            f'<g data-atom="{x+60},{y},12,O,-"></g>'+T(x+78,y+7,'O',19,'start'))
def g13():
    lo=[('b',50,45),('b',140,110),('b',55,170),('a',150,40),('a',140,185)]
    hi=[('b',100,112),('a',38,45),('a',100,45),('a',162,45),('a',38,182),('a',100,182),('a',162,182)]
    o=[box(20,10,200,215,lo,.12,'온도가 낮을 때'),
       f'<g data-anim="fade" data-dur="1" data-delay=".4"><g data-arw="238,118,292,118,equi,4"></g></g>',T(265,100,'가열',19,fill='#E08A2C'),
       box(310,10,200,215,hi,.38,'온도가 높을 때'),legend(190,282)]
    return f'<svg class="fig" viewBox="0 0 530 300" style="width:530px" aria-label="온도가 낮을 때 상자에는 사산화 이질소 3개와 이산화 질소 2개, 온도가 높을 때는 사산화 이질소 1개와 이산화 질소 6개가 있어 적갈색이 진해진다">'+''.join(o)+'</svg>'
if __name__=='__main__':
    import sys; print(globals()[sys.argv[1]]())
def svg(vb,w,label,body):
    return f'<svg class="fig" viewBox="{vb}" style="width:{w}px" aria-label="{label}">'+''.join(body)+'</svg>'
def eqarrows(x,y,w,lab_f='',lab_b=''):
    # half-headed equilibrium arrows: forward (field) on top, reverse (bfield) below
    o=[f'<path d="M{x} {y-5} H{x+w} l-12 -9" fill="none" stroke="{FIELD}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>',
       f'<path d="M{x+w} {y+5} H{x} l12 9" fill="none" stroke="{BF}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>']
    if lab_f:o.append(T(x+w/2,y-18,lab_f,19,fill=FIELD))
    if lab_b:o.append(T(x+w/2,y+38,lab_b,19,fill=BF))
    return ''.join(o)
def cover():
    o=['<circle cx="270" cy="260" r="235" fill="#EEF3F8"/>']
    # sealed round flask
    fl='M235 70 H305 V150 A120 120 0 1 1 235 150 Z'
    o.append(f'<path d="{fl}" fill="#FFFFFF" stroke="none"/>')
    o.append(f'<g data-anim="fade" data-dur="1.6" data-delay=".2"><path d="{fl}" fill="{NO2C}" fill-opacity=".30" stroke="none"/></g>')
    mols=[('b',215,250),('b',330,330),('a',320,225),('a',215,345),('a',275,400),('b',270,300)]
    for k,x,y in mols:
        inner=no2(x,y,0) if k=='a' else n2o4(x,y)
        o.append(f'<g data-anim="move" data-from="{(-1)**int(x)*6},{-8}" data-rep="alt" data-dur="1.4" data-ease="sine">{inner}</g>' if False else inner)
    o.append(f'<path d="{fl}" fill="none" stroke="#7E8B98" stroke-width="4" stroke-linejoin="round"/>')
    o.append('<rect x="226" y="56" width="88" height="20" rx="5" fill="#8C99A6"/>')
    o.append(eqarrows(200,478,140,'정반응','역반응'))
    o.append(T(110,486,'$\\ce{2NO2}$',26,fill='#B5562A'))
    o.append(T(430,486,'$\\ce{N2O4}$',26))
    o.append(legend(380,92))
    return svg('0 0 540 540',540,'밀폐된 플라스크 안에서 적갈색 이산화 질소와 무색 사산화 이질소가 함께 있고, 정반응과 역반응이 동시에 일어나는 화학 평형',o)
def unitmap():
    o=[]
    xs=[90,255,420,600,765,930]; today=1058
    o.append(T(270,24,'1. 화학 평형',19,fill=FIELD,extra=' data-weight="700"'))
    o.append(f'<path d="M60 42 V34 H480 V42" fill="none" stroke="{FIELD}" stroke-width="2.5"/>')
    o.append(T(790,24,'2. 화학 평형 이동',19,fill=FIELD,extra=' data-weight="700"'))
    o.append(f'<path d="M580 42 V34 H1000 V42" fill="none" stroke="{FIELD}" stroke-width="2.5"/>')
    o.append('<line x1="40" y1="58" x2="1080" y2="58" stroke="#C9D3DD" stroke-width="6" stroke-linecap="round"/>')
    o.append(f'<path d="M40 58 H{today}" stroke="{FIELD}" stroke-width="6" stroke-linecap="round" fill="none" data-anim="draw" data-dur="1.6" data-delay=".3"/>')
    for x in xs:o.append(f'<circle cx="{x}" cy="58" r="11" fill="{FIELD}"/>')
    o.append(f'<circle cx="{today}" cy="58" r="16" fill="#FFE45C" stroke="{INK}" stroke-width="3"/>')
    labs=['01 가역 반응과||화학 평형','02 화학 평형과||평형 상수','03 화학 반응의||진행 방향 예측','01 농도·압력 변화와||화학 평형 이동','02 온도 변화와||화학 평형 이동','03 일상생활 속의||화학 평형 이동']
    for x,l in zip(xs,labs):o.append(T(x,100,l,18,fill=MUT))
    o.append(T(today,100,'오늘||대단원 마무리',18,extra=' data-weight="700"'))
    return svg('0 0 1112 150',1112,'대단원 Ⅲ 단원 지도에서 여섯 소단원을 마치고 오늘은 대단원 마무리',o)
def beaker(x,y,w,h):
    return (f'<path d="M{x} {y} V{y+h-14} Q{x} {y+h} {x+14} {y+h} H{x+w-14} Q{x+w} {y+h} {x+w} {y+h-14} V{y}" fill="#DDEEF8" stroke="none"/>',
            f'<path d="M{x-6} {y-6} L{x} {y} V{y+h-14} Q{x} {y+h} {x+14} {y+h} H{x+w-14} Q{x+w} {y+h} {x+w} {y+h-14} V{y} L{x+w+6} {y-6}" fill="none" stroke="#7E8B98" stroke-width="3" stroke-linejoin="round"/>')
def beaker05():
    w0,w1=beaker(60,40,300,190)
    o=[f'<rect x="60" y="60" width="300" height="170" fill="#DDEEF8"/>',w1]
    o=[w0,w1]
    o.append('<path d="M150 230 Q210 196 270 230 Z" fill="#E6E1D6" stroke="#9A8F78" stroke-width="2"/>')
    o.append(T(210,224,'A',19,fill='#6B5E45'))
    pts=[('B',110,90),('C',170,80),('C',240,100),('B',300,85),('C',120,150),('C',320,150)]
    for i,(k,x,y) in enumerate(pts):
        col='#E08A2C' if k=='B' else '#0E7490'
        o.append(f'<g data-anim="move" data-from="{(-1)**i*8},{30}" data-dur="1.4" data-delay="{.2+.12*i:.2f}" data-ease="soft"><circle cx="{x}" cy="{y}" r="16" fill="#fff" stroke="{col}" stroke-width="3"/>{T(x,y+7,k,19,fill=col)}</g>')
    o.append(T(210,270,'B 1개마다 C 2개 → $[\\mathrm{C}]=2[\\mathrm{B}]$',19))
    return svg('0 0 420 285',420,'물에 일부 녹은 고체 A, 용액 속 B 2개와 C 4개',o)
def tube(x,y,col,h=150,w=40):
    return (f'<path d="M{x} {y+40} V{y+h} a{w/2} {w/2} 0 0 0 {w} 0 V{y+40} Z" fill="{col}"/>',
            f'<path d="M{x} {y} V{y+h} a{w/2} {w/2} 0 0 0 {w} 0 V{y}" fill="none" stroke="#7E8B98" stroke-width="3"/>')
def tubes07():
    a0,a1=tube(70,20,'#F2D23C'); b0,b1=tube(310,20,'#F08A24')
    o=[a0,a1,f'<g data-anim="fade" data-dur="1.2" data-delay=".5">{b0}</g>',b1,
       T(90,225,'노란색',19),T(330,225,'주황색',19),
       T(90,255,'$\\ce{CrO4^2-}$ 많음',19),T(330,255,'$\\ce{Cr2O7^2-}$ 많음',19),
       f'<g data-arw="140,80,290,80,field,3.5"></g>',T(215,64,'$\\ce{HCl}(aq)$ 넣음',19,fill=FIELD),
       f'<g data-arw="290,130,140,130,bfield,3.5"></g>',T(215,162,'$\\ce{NaOH}(aq)$ 넣으면?',19,fill=BF)]
    return svg('0 0 420 270',420,'노란색 크로뮴산 칼륨 수용액에 염산을 넣으면 주황색이 되고, 수산화 나트륨 수용액을 넣으면 어떻게 될지 묻는 그림',o)
def o2(x,y,r=8):
    return f'<g data-atom="{x-r*.75:.1f},{y},{r},O,-"></g><g data-atom="{x+r*.75:.1f},{y},{r},O,-"></g>'
def hb10():
    o=[]
    # thermometer
    o.append('<rect x="30" y="30" width="22" height="170" rx="11" fill="#fff" stroke="#7E8B98" stroke-width="3"/><circle cx="41" cy="212" r="20" fill="#D7263D" stroke="#7E8B98" stroke-width="3"/>')
    o.append('<g data-anim="scale" data-from="1,0.45" data-o="41,212" data-dur="1.4" data-delay=".2"><rect x="35" y="70" width="12" height="140" fill="#D7263D"/></g>')
    o.append(T(41,262,'체온 ↑',19))
    # Hb protein
    o.append('<circle cx="200" cy="135" r="62" fill="#9C6B8E"/>'+T(200,143,'$\\ce{Hb}$',24,fill='#fff'))
    sites=[(150,85),(250,85),(150,185),(250,185)]
    away=[(-40,-35),(60,-40),(-45,40),(70,30)]
    for (x,y),(dx,dy) in zip(sites,away):
        o.append(f'<g data-anim="move" data-from="{-dx},{-dy}" data-dur="1.6" data-delay=".6" data-ease="soft">{o2(x+dx,y+dy)}</g>')
    o.append(f'<g data-arw="290,135,380,135,bfield,3.5"></g>'+T(335,120,'역반응',19,fill=BF))
    o.append(T(420,128,'조직에||$\\ce{O2}$ 공급',19))
    o.append(o2(395,180)+T(420,212,'$\\ce{O2}$',19,'start'))
    return svg('0 0 480 280',480,'체온이 올라가면 산소와 결합한 헤모글로빈에서 산소 분자가 떨어져 나와 조직에 공급된다',o)
def tubes11():
    o=[]
    spec=[(60,'#3E8ED0','얼음물','#E3EEFB','r1'),(240,'#5FA86B','처음(실온)',None,None),(420,'#C9BE2E','뜨거운 물','#FDE2E4','r2')]
    for x,col,lab,bath,g in spec:
        if bath:
            o.append(f'<rect x="{x-40}" y="90" width="120" height="120" rx="10" fill="{bath}" stroke="#7E8B98" stroke-width="2.5"/>')
        a0,a1=tube(x,20,col,h=150)
        if g:
            o.append(tube(x,20,'#5FA86B',h=150)[0])
            o.append(f'<g data-anim="fade" data-dur="1.4" data-on="g:{g}">{a0}</g>')
        else:o.append(a0)
        o.append(a1); o.append(T(x+20,248,lab,19))
    o.append(T(80,280,'파란색 진해짐',19,fill='#1F5FA8'))
    o.append(T(260,280,'초록색(기준)',19,fill='#2E7D4F'))
    o.append(T(440,280,'노란색 진해짐',19,fill='#8A7F10'))
    return svg('0 0 520 290',520,'초록색 평형 혼합물(처음, 실온)을 얼음물에 넣으면 파란색이, 뜨거운 물에 넣으면 노란색이 진해진다',o)
def chamber12():
    o=['<rect x="30" y="60" width="400" height="150" rx="75" fill="#F4F6F8" stroke="#7E8B98" stroke-width="4"/>',
       '<rect x="60" y="205" width="40" height="40" fill="#C9D3DD"/><rect x="360" y="205" width="40" height="40" fill="#C9D3DD"/>',
       '<ellipse cx="380" cy="135" rx="34" ry="52" fill="#DDEEF8" stroke="#7E8B98" stroke-width="3"/>',
       '<rect x="110" y="120" width="200" height="34" rx="17" fill="#F2C9B0"/><circle cx="125" cy="137" r="20" fill="#F2C9B0"/>']
    for i,(x,y) in enumerate([(160,90),(240,95),(300,180),(190,182),(330,92)]):
        o.append(f'<g data-anim="move" data-from="{0 if i%2 else 0},{-30 if y<130 else 30}" data-dur="1.3" data-delay="{.2+.15*i:.2f}" data-ease="soft">{o2(x,y)}</g>')
    o.append(f'<g data-arw="230,20,230,58,minus,3.5"></g>'+T(250,36,'압력 ↑, 순수한 $\\ce{O2}$',19,'start'))
    o.append(T(230,275,'고압 산소 치료실 (모식도)',19,fill=MUT))
    return svg('0 0 460 290',460,'고압 산소 치료실 안의 환자와 산소 분자, 치료실의 압력을 높인다',o)
def mol_co2(x,y,r=15):
    d=1.9*r
    return (f'<line x1="{x-d}" y1="{y-4}" x2="{x+d}" y2="{y-4}" stroke="#9AA5B1" stroke-width="4"/><line x1="{x-d}" y1="{y+4}" x2="{x+d}" y2="{y+4}" stroke="#9AA5B1" stroke-width="4"/>'
            f'<g data-atom="{x-d},{y},{r},O,-"></g><g data-atom="{x},{y},{r},C,-"></g><g data-atom="{x+d},{y},{r},O,-"></g>')
def mol_h2(x,y,r=11):
    return f'<line x1="{x-r}" y1="{y}" x2="{x+r}" y2="{y}" stroke="#9AA5B1" stroke-width="5"/><g data-atom="{x-r},{y},{r},H,-"></g><g data-atom="{x+r},{y},{r},H,-"></g>'
def bond(x1,y1,x2,y2):return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#9AA5B1" stroke-width="5"/>'
def mol_meoh(x,y,r=15,h=11):
    d=30; o=[]
    cx,cy=x-18,y; ox,oy=x+18,y
    Hs=[(cx-d*.9,cy),(cx-6,cy-d),(cx-6,cy+d)]
    ho=(ox+12,oy-d*.9)
    for hx,hy in Hs:o.append(bond(cx,cy,hx,hy))
    o.append(bond(cx,cy,ox,oy));o.append(bond(ox,oy,*ho))
    for hx,hy in Hs:o.append(f'<g data-atom="{hx:.1f},{hy:.1f},{h},H,-"></g>')
    o.append(f'<g data-atom="{ho[0]:.1f},{ho[1]:.1f},{h},H,-"></g>')
    o.append(f'<g data-atom="{cx},{cy},{r},C,-"></g><g data-atom="{ox},{oy},{r},O,-"></g>')
    return ''.join(o)
def mol_h2o(x,y,r=15,h=11):
    a=math.radians(52.25);d=28
    p1=(x-d*math.sin(a),y+d*math.cos(a));p2=(x+d*math.sin(a),y+d*math.cos(a))
    return bond(x,y,*p1)+bond(x,y,*p2)+f'<g data-atom="{p1[0]:.1f},{p1[1]:.1f},{h},H,-"></g><g data-atom="{p2[0]:.1f},{p2[1]:.1f},{h},H,-"></g><g data-atom="{x},{y},{r},O,-"></g>'
def card(x,y,w,h,fill='#fff',stroke='#C9D3DD'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def proj():
    o=[card(10,10,250,150,'#F3F8EE'),T(135,40,'재생 에너지로 물을||전기 분해 → 수소',19),
       f'<g data-anim="move" data-from="-30,0" data-dur="1.2" data-delay=".3" data-ease="soft">{mol_h2(80,125)}{mol_h2(140,125)}{mol_h2(200,125)}</g>',
       card(10,190,250,150,'#F3F8EE'),T(135,220,'바이오매스에서||이산화 탄소',19),
       f'<g data-anim="move" data-from="-30,0" data-dur="1.2" data-delay=".5" data-ease="soft">{mol_co2(135,302)}</g>',
       f'<g data-arw="268,85,330,160,field,4"></g>',f'<g data-arw="268,265,330,190,field,4"></g>',
       card(336,130,90,60,'#FFF6E0','#E08A2C'),T(381,167,'합성',20),
       f'<g data-arw="430,160,470,160,field,4"></g>',
       card(476,30,170,150,'#EEF3F8'),T(561,58,'그린 메탄올',19,extra=' data-weight="700"'),mol_meoh(561,110),
       card(476,200,170,120,'#EEF3F8'),T(561,230,'물(부산물)',19),mol_h2o(561,262),
       T(135,152,'$\\ce{H2}$',19,fill=MUT),T(135,335,'$\\ce{CO2}$',19,fill=MUT),T(561,172,'$\\ce{CH3OH}$',19,fill=MUT),T(561,314,'$\\ce{H2O}$',19,fill=MUT),
       f'<g data-arw="430,180,470,240,field,4"></g>']
    lx=40;ly=375
    for i,(el,lab) in enumerate((('H','H'),('C','C'),('O','O'))):
        o.append(f'<g data-atom="{lx+i*80},{ly},11,{el},-"></g>'+T(lx+i*80+16,ly+7,lab,19,'start'))
    return svg('0 0 660 395',580,'재생 에너지로 물을 전기 분해 해 얻은 수소와 바이오매스에서 얻은 이산화 탄소를 합성하여 그린 메탄올과 물을 만든다',o)
