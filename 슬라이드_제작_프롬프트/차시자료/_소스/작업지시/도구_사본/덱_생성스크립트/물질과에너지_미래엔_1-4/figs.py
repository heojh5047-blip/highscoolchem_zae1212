# 1-4 고체의 종류와 구조 — 그림 생성 (slides.tpl.html 의 @@이름@@ 을 채워 slides.html 로)
import math, re, sys, os, random
HERE=os.path.dirname(os.path.abspath(__file__))
OUT='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/물질과에너지_미래엔/1-4_고체의_종류와_구조/slides.html'

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
def T(x,y,s,size=20,anchor='middle',weight=None,fill=None,halo=False,cls='',extra=''):
    o=f'<text class="tex{(" "+cls) if cls else ""}" x="{x:.1f}" y="{y:.1f}" data-mix="{esc(s)}" data-size="{size}" data-anchor="{anchor}"'
    if weight: o+=f' data-weight="{weight}"'
    if halo: o+=' data-halo="1"'
    if fill: o+=f' fill="{fill}"'
    return o+extra+'></text>'
def A(x,y,r,el,lab='-',d=False):
    return f'<g data-atom="{x:.1f},{y:.1f},{r},{el}{(","+lab) if lab is not None else ""}{",d" if d else ""}"></g>'
def CH(x,y,r,s): return f'<g data-chg="{x:.1f},{y:.1f},{r},{s}"></g>'
def EL(x,y,r=5): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#1F6FD1" stroke="#fff" stroke-width="1.2"/>'
def B(x1,y1,x2,y2,w=6,col='#9AA5B1'): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
def D(x1,y1,x2,y2,w=2.2,col='#5B6B7F',da='4 4'): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{da}"/>'
def ARW(x1,y1,x2,y2,col='ink',w=3,d=False,extra=''): return f'<g data-arw="{x1:.1f},{y1:.1f},{x2:.1f},{y2:.1f},{col},{w}{",d" if d else ""}"{extra}></g>'
def L(x1,y1,x2,y2,col='#5B6B7F',w=2,extra=''): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{extra}/>'
def R(x,y,w,h,fill='#fff',stroke='#7E8B98',sw=2,rx=10,extra=''): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
def poly(pts): return ' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def svg(w,h,label,body,disp=None,cls='fig',extra=''):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" style="width:{disp or w}px" aria-label="{esc(label)}"{extra}>{body}</svg>'
def G(body,anim=None,**kw):
    a=''
    if anim: a+=f' data-anim="{anim}"'
    for k,v in kw.items(): a+=f' data-{k.replace("_","-")}="{v}"'
    return f'<g{a}>{body}</g>'
PLUS='#D7263D'; MINUS='#1F6FD1'; MUTED='#5B6B7F'; INK='#16233D'; FIELD='#2E9E6A'; EQUI='#E08A2C'
WATER='#DDEEF8'; WATERE='#9FC3DD'; GLASS='#7E8B98'; CUSO4='#3E8ED0'
F={}

# ───────── 공통 부품 ─────────
NA,CL=11,19   # 0.6배 이온 반지름
def ion_grid(x0,y0,nx,ny,s,start='+',rp=NA,rm=CL,skip=()):
    o=''
    for j in range(ny):
        for i in range(nx):
            if (i,j) in skip: continue
            pos=((i+j)%2==0)==(start=='+')
            o+=CH(x0+i*s,y0+j*s,rp if pos else rm,'+' if pos else '-')
    return o
def ion_legend(x,y,size=19,gap=110):
    return CH(x,y,NA,'+')+T(x+18,y+7,r'$\ce{Na+}$',size,'start')+CH(x+gap,y,CL,'-')+T(x+gap+26,y+7,r'$\ce{Cl-}$',size,'start')
RM=18
def metal(x0,y0,nx,ny,s,anim=True,seed=3,er=5,halo=False):
    rnd=random.Random(seed)
    o=''
    for j in range(ny):
        for i in range(nx):
            x,y=x0+i*s,y0+j*s
            if halo: o+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{RM+8}" fill="#F6C9CF" opacity=".55"/>'
            o+=CH(x,y,RM,'+')
    # 자유 전자: 양이온 네 개 사이 칸 가운데 근처(고정 시드)
    groups=['','','']; k=0
    for j in range(ny-1):
        for i in range(nx-1):
            groups[k%3]+=EL(x0+(i+0.5)*s+rnd.uniform(-7,7),y0+(j+0.5)*s+rnd.uniform(-7,7),er); k+=1
    if not anim: return o+''.join(groups)
    froms=['9,-5','-8,6','5,8']; durs=['0.7','0.9','0.8']
    return o+''.join(G(g,'move',**{'from':froms[i],'rep':'swing','dur':durs[i]}) for i,g in enumerate(groups))
def i2(x,y,ang,r=21,d=None,lab='-'):
    d=d or 1.55*r; a=math.radians(ang); dx,dy=d/2*math.cos(a),d/2*math.sin(a)
    return A(x-dx,y-dy,r,'I',lab)+A(x+dx,y+dy,r,'I',lab)
def water(ox,oy,h1ang,h2ang,ro=14,rh=10,d=26):
    o=''; hs=[]
    for a in (h1ang,h2ang):
        aa=math.radians(a); hs.append((ox+d*math.cos(aa),oy+d*math.sin(aa)))
    o+=''.join(B(ox,oy,hx,hy,5) for hx,hy in hs)+A(ox,oy,ro,'O')+''.join(A(hx,hy,rh,'H') for hx,hy in hs)
    return o,hs
def honey(cx,cy,a,nx,ny):
    """벌집 격자 꼭짓점과 변 (뾰족 위 육각형), a = 변 길이"""
    pts={}; edges=set()
    w=math.sqrt(3)*a
    for j in range(ny):
        for i in range(nx):
            hx=cx+i*w+(j%2)*w/2; hy=cy+j*1.5*a
            ring=[]
            for k in range(6):
                ang=math.radians(90+60*k); p=(round(hx+a*math.cos(ang),1),round(hy-a*math.sin(ang),1))
                ring.append(p); pts[p]=1
            for k in range(6): edges.add(tuple(sorted((ring[k],ring[(k+1)%6]))))
    return list(pts.keys()),list(edges)
def graphite_layer(cx,cy,a,nx,ny,sq=0.42,col='#3A3F47',r=7,hl=None,lab=False):
    """비스듬히 본 흑연 층: 벌집을 y 방향으로 sq배 눌러 투영"""
    pts,edges=honey(0,0,a,nx,ny)
    mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
    P=lambda p:(cx+(p[0]-mx)+0.35*(p[1]-my)*0, cy+(p[1]-my)*sq)
    o=''.join(B(*P(e[0]),*P(e[1]),3.2,'#6B7480') for e in edges)
    o+=''.join(A(*P(p),r,'C','-') for p in pts)
    return o,[P(p) for p in pts],[(P(e[0]),P(e[1])) for e in edges]
def diamond(cx,cy,sc,rad=0.95,rx=22,ry=-32,r=8,hl=True):
    """다이아몬드 그물 조각(3차원 좌표 → 회전 투영). 단위 세포 상자는 그리지 않음"""
    base=[(0,0,0),(0,.5,.5),(.5,0,.5),(.5,.5,0)]
    P=[]
    for i in range(-2,3):
        for j in range(-2,3):
            for k in range(-2,3):
                for b in base:
                    for off in ((0,0,0),(.25,.25,.25)):
                        p=(i+b[0]+off[0]-.125,j+b[1]+off[1]-.125,k+b[2]+off[2]-.125)
                        if p[0]**2+p[1]**2+p[2]**2<=rad**2: P.append(p)
    P=list(set(P))
    bl=math.sqrt(3)/4
    E=[(a,b) for ia,a in enumerate(P) for b in P[ia+1:] if abs(math.dist(a,b)-bl)<1e-6]
    ax,ay=math.radians(rx),math.radians(ry)
    def rot(p):
        x,y,z=p
        x,z=x*math.cos(ay)+z*math.sin(ay),-x*math.sin(ay)+z*math.cos(ay)
        y,z=y*math.cos(ax)-z*math.sin(ax),y*math.sin(ax)+z*math.cos(ax)
        return x,y,z
    Q={p:rot(p) for p in P}
    pr=lambda p:(cx+Q[p][0]*sc,cy+Q[p][1]*sc)
    items=[]
    for a,b in E: items.append(((Q[a][2]+Q[b][2])/2-0.01,'b',a,b))
    for p in P: items.append((Q[p][2],'a',p,None))
    items.sort(key=lambda t:t[0])
    # 가운데에 가장 가까운 원자(이웃 4개) 강조
    c=min([p for p in P if sum(1 for e in E if p in e)==4],key=lambda p:p[0]**2+p[1]**2+p[2]**2)
    o=''
    for z,kind,a,b in items:
        if kind=='b':
            hi=hl and (a==c or b==c)
            o+=B(*pr(a),*pr(b),5 if hi else 3.2,FIELD if hi else '#6B7480')
        else:
            rr=r*(1+0.18*Q[a][2]); o+=A(*pr(a),round(rr,1),'C','-')
    if hl: o+=f'<circle cx="{pr(c)[0]:.1f}" cy="{pr(c)[1]:.1f}" r="{r+6}" fill="none" stroke="{FIELD}" stroke-width="2.5"/>'
    return o,pr(c)

# ───────── S1 표지 ─────────
def cover():
    o='<circle cx="270" cy="270" r="262" fill="#EEF3F8"/>'
    cen=[(158,158,'분자 결정'),(382,158,'공유 결정'),(158,382,'이온 결정'),(382,382,'금속 결정')]
    for cx,cy,nm in cen: o+=f'<circle cx="{cx}" cy="{cy}" r="104" fill="#fff" stroke="#D5DCE4" stroke-width="2"/>'
    # 분자 결정
    m=''
    for j in range(3):
        for i in range(3):
            m+=i2(158-44+i*44,158-58+j*36,35 if (i+j)%2==0 else -35,r=11)
    o+=G(m,'move',**{'from':'1.2,0','rep':'swing','dur':'0.2'})
    # 공유 결정 (벌집)
    pts,edges=honey(0,0,19,3,3)
    mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
    P=lambda p:(382+p[0]-mx,158-20+p[1]-my)
    o+=''.join(B(*P(a),*P(b),3.5,'#6B7480') for a,b in edges)+''.join(A(*P(p),7,'C','-') for p in pts)
    # 이온 결정
    o+=G(ion_grid(158-56,382-62,5,4,28,rp=9,rm=15),'move',**{'from':'1.2,0','rep':'swing','dur':'0.18'})
    # 금속 결정
    o+=metal(382-57,382-60,4,3,38)
    for cx,cy,nm in cen: o+=T(cx,cy+78,nm,23,weight=700,halo=True)
    return svg(540,540,'분자 결정, 공유 결정, 이온 결정, 금속 결정의 입자 배열을 네 칸에 나타낸 그림',o,cls='cover-fig',extra=' data-audit="skip"')
F['cover']=cover()

# ───────── S3 생각 열기: 유리컵과 금속 컵 ─────────
def cups():
    o='<rect x="10" y="236" width="420" height="16" rx="4" fill="#B98A5A"/><rect x="30" y="252" width="14" height="50" fill="#9C7146"/><rect x="396" y="252" width="14" height="50" fill="#9C7146"/>'
    # 유리컵(금 감)
    g=f'<path d="M70 110 L84 236 H166 L180 110 Z" fill="#F4FAFD" stroke="{GLASS}" stroke-width="4"/>'
    g+=f'<path d="M100 150 L118 172 L108 190 L126 214" fill="none" stroke="{INK}" stroke-width="2.5"/><path d="M150 132 L138 158 L152 176" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    g+=f'<path d="M58 220 l-12 6 m40 6 l-8 10 m86 -14 l14 6" stroke="{GLASS}" stroke-width="3"/>'
    o+=G(g,'rot',**{'from':'4','o':'125,236','rep':'damp','dur':'0.25'})
    # 금속 컵(패임)
    m=f'<path d="M270 110 V226 Q270 236 280 236 H360 Q370 236 370 226 V110 Z" fill="#C9CED6" stroke="#8A919C" stroke-width="4"/>'
    m+=f'<path d="M370 140 Q384 140 384 160 V190 Q384 206 370 206" fill="none" stroke="#8A919C" stroke-width="7"/>'
    m+=f'<path d="M300 150 Q318 166 304 186" fill="none" stroke="#8A919C" stroke-width="3"/><ellipse cx="300" cy="168" rx="9" ry="16" fill="#AEB4BD" opacity=".7"/>'
    m+=f'<rect x="282" y="120" width="10" height="100" rx="5" fill="#fff" opacity=".45"/>'
    o+=m
    o+=T(125,92,'유리컵',22,weight=700)+T(320,92,'금속 컵',22,weight=700)
    o+=T(125,40,'깨진다',22,fill=PLUS,weight=700)+T(320,40,'깨지지 않는다',22,fill=MINUS,weight=700)
    return svg(440,310,'탁자 위의 금이 간 유리컵과 움푹 패었지만 깨지지 않은 금속 컵',o)
F['cups']=cups()

# ───────── S4 결정·비결정 배열 ─────────
def arr_box(kind):
    o=R(8,8,284,154,'#F4F8FB','#7E8B98',2,12)
    rnd=random.Random(7)
    pts=[]
    for j in range(4):
        for i in range(7):
            x,y=40+i*37,35+j*34
            if kind=='irr': x+=rnd.uniform(-12,12); y+=rnd.uniform(-10,10)
            pts.append((x,y))
    body=''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#6C8EBF" stroke="#3E5F8F" stroke-width="1.5"/>' for x,y in pts)
    o+=G(body,'move',**{'from':'1.2,0','rep':'swing','dur':'0.18'})
    lab='규칙적인 배열' if kind=='reg' else '불규칙한 배열'
    return svg(300,170,lab+'로 놓인 고체 속 입자',o,disp=300)
F['arr_reg']=arr_box('reg'); F['arr_irr']=arr_box('irr')
def solid_small():
    o=R(6,6,208,128,'#E3EEFB','#7E8B98',2,12)
    body=''
    for j in range(3):
        for i in range(5): body+=f'<circle cx="{40+i*35}" cy="{36+j*34}" r="12" fill="#6C8EBF" stroke="#3E5F8F" stroke-width="1.5"/>'
    o+=G(body,'move',**{'from':'1.5,0','rep':'swing','dur':'0.16'})
    return svg(220,140,'고정된 위치에서 진동하는 고체 입자',o)
F['solid_small']=solid_small()

# ───────── S5 석영과 유리 ─────────
def sio2(kind):
    a=34
    pts,edges=honey(0,0,a,4,3)
    mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
    rnd=random.Random(11)
    jit={p:((rnd.uniform(-11,11),rnd.uniform(-11,11)) if kind=='glass' else (0,0)) for p in pts}
    P=lambda p:(170+p[0]-mx+jit[p][0],138+p[1]-my+jit[p][1])
    E=edges
    if kind=='glass':
        rnd2=random.Random(5); E=[e for e in edges if rnd2.random()>0.13]
    o=R(6,6,328,264,'#FBFCFD','#7E8B98',2,14)
    body=''
    for e in E:
        (x1,y1),(x2,y2)=P(e[0]),P(e[1])
        mxx,myy=(x1+x2)/2,(y1+y2)/2
        # O는 변 가운데에서 살짝 비켜(굽은 Si–O–Si)
        nx,ny=-(y2-y1),(x2-x1); n=math.hypot(nx,ny); ox,oy=mxx+nx/n*5,myy+ny/n*5
        body+=B(x1,y1,ox,oy,3,'#8E7A52')+B(ox,oy,x2,y2,3,'#8E7A52')
    sis=''.join(A(*P(p),12,'Si','-') for p in pts)
    os_=''
    for e in E:
        (x1,y1),(x2,y2)=P(e[0]),P(e[1]); mxx,myy=(x1+x2)/2,(y1+y2)/2
        nx,ny=-(y2-y1),(x2-x1); n=math.hypot(nx,ny); os_+=A(mxx+nx/n*5,myy+ny/n*5,7,'O','-')
    o+=body+sis+os_
    nm='석영(결정성 고체)' if kind=='quartz' else '유리(비결정성 고체)'
    return svg(340,276,nm+': 규소와 산소 원자가 '+('규칙적인' if kind=='quartz' else '불규칙한')+' 그물을 이룬 모형',o,disp=340)
F['quartz']=sio2('quartz'); F['glass']=sio2('glass')
F['sio2_leg']=svg(330,40,'범례: 규소 원자와 산소 원자',A(20,20,12,'Si','-')+T(40,27,'규소($\\ce{Si}$)',19,'start')+A(170,20,7,'O','-')+T(186,27,'산소($\\ce{O}$)',19,'start'))

# ───────── S6 가열 곡선 ─────────
def heat():
    W,H=560,330; x0,y0,x1,y1=70,280,530,30
    o=L(x0,y0,x1,y0,MUTED,2)+L(x0,y0,x0,y1,MUTED,2)
    o+=T(x1,y0+34,'가열 시간',19,'end')+T(x0+8,y1+4,'온도',19,'start')
    c=[(x0,250),(170,160),(330,160),(470,60)]
    o+=G(f'<polyline points="{poly(c)}" fill="none" stroke="{INK}" stroke-width="4"/>','draw',dur='1.4')
    o+=D(x0,160,170,160,1.8)+T(x0-8,166,'녹는점',19,'end')
    o+=T(252,190,'녹는 동안 온도 일정',19,'start',fill=INK,halo=True)
    pts=[]
    for k in range(41):
        t=k/40; x=x0+t*(470-x0); y=250-190*(t**1.15*(3-2*t)*0.5+0.5*t)
        pts.append((x,y))
    o+=G(f'<polyline points="{poly(pts)}" fill="none" stroke="{EQUI}" stroke-width="4" stroke-dasharray="10 7"/>','fade',dur='1.2',delay='0.6')
    o+=T(420,70,'결정성 고체',20,'end',fill=INK,weight=700,halo=True)
    o+=T(330,226,'비결정성 고체',20,fill=EQUI,weight=700,halo=True)+T(330,250,'(점점 물러짐)',19,fill=EQUI,halo=True)
    o+=T(W-10,24,'크기 비례 아님',18,'end',fill=MUTED)
    return svg(W,H,'가열 시간에 따른 온도 그래프: 결정성 고체는 녹는 동안 온도가 일정한 구간이 있고, 비결정성 고체는 그런 구간 없이 온도가 계속 오른다',o)
F['heat']=heat()

# ───────── S7 결정 만들기 단계 그림 ─────────
def beaker(x,y,w,h,fill_h,fill='#DDEEF8'):
    o=f'<path d="M{x} {y} V{y+h-8} Q{x} {y+h} {x+8} {y+h} H{x+w-8} Q{x+w} {y+h} {x+w} {y+h-8} V{y}" fill="#F8FBFD" stroke="{GLASS}" stroke-width="3.5"/>'
    o+=f'<rect x="{x+3}" y="{y+h-fill_h}" width="{w-6}" height="{fill_h-3}" rx="4" fill="{fill}"/>'
    return o
def make1():
    o=beaker(70,60,150,140,96,'#9CC6EA')
    o+=f'<path d="M210 30 L150 120" stroke="#C9CED6" stroke-width="7" stroke-linecap="round"/>'
    o+=G(''.join(f'<circle cx="{150+dx}" cy="{126+dy}" r="4" fill="{CUSO4}"/>' for dx,dy in ((0,0),(-8,8),(6,12),(-2,22),(10,30))),'move',**{'from':'0,-20','dur':'1.2','rep':'loop'})
    o+=T(145,226,'약 $60\\ {}^\\circ\\text{C}$ 물 $50\\ \\text{mL}$',19)
    return svg(290,240,'더운물에 황산 구리(II)를 더 녹지 않을 때까지 녹이는 모습',o)
def make2():
    o=beaker(70,70,150,130,96,'#7FB3E3')
    o+=f'<rect x="56" y="58" width="178" height="10" rx="3" fill="#F2F2EC" stroke="#B9B9AE" stroke-width="1.5"/>'
    o+=f'<rect x="50" y="44" width="190" height="9" rx="4" fill="#C79A5B"/>'
    o+=f'<path d="M110 52 Q112 120 130 168 Q145 190 160 168 Q178 120 180 52" fill="none" stroke="#7A5C9E" stroke-width="3"/>'
    o+=T(270,40,'나무젓가락',19,'end')+T(268,84,'거름종이',19,'end',halo=True)+T(145,226,'털실을 걸치고 덮기',19)
    return svg(290,240,'나무젓가락에 묶은 털실을 비커에 걸치고 거름종이로 덮은 모습',o)
def crystal(x,y,s,ang=0,col=CUSO4):
    a=math.radians(ang)
    pts=[(-1,-.6),(.3,-.9),(1,-.2),(.7,.7),(-.5,.9),(-1.1,.2)]
    P=[(x+s*(px*math.cos(a)-py*math.sin(a)),y+s*(px*math.sin(a)+py*math.cos(a))) for px,py in pts]
    o=f'<polygon points="{poly(P)}" fill="{col}" stroke="#1F5F99" stroke-width="2"/>'
    o+=f'<polyline points="{poly([P[0],(x,y),P[2]])}" fill="none" stroke="#BFE0FA" stroke-width="1.5"/><line x1="{x:.1f}" y1="{y:.1f}" x2="{P[4][0]:.1f}" y2="{P[4][1]:.1f}" stroke="#1F5F99" stroke-width="1.5"/>'
    return o
def make3():
    o=beaker(70,70,150,130,70,'#B5D6F2')
    o+=f'<rect x="50" y="44" width="190" height="9" rx="4" fill="#C79A5B"/>'
    o+=f'<path d="M110 52 Q112 120 130 168 Q145 190 160 168 Q178 120 180 52" fill="none" stroke="#7A5C9E" stroke-width="3"/>'
    o+=G(crystal(120,140,14,10)+crystal(150,178,17,-20)+crystal(172,128,11,30)+crystal(113,110,9,-10),'pop',dur='0.9')
    o+=T(145,226,'며칠 뒤 결정이 생김',19)
    return svg(290,240,'며칠 뒤 털실에 푸른 황산 구리(II) 결정이 붙은 모습',o)
F['make1']=make1(); F['make2']=make2(); F['make3']=make3()
def grown():
    o=f'<rect x="20" y="20" width="320" height="10" rx="4" fill="#C79A5B"/>'
    o+=f'<path d="M180 30 V250" stroke="#7A5C9E" stroke-width="3"/>'
    for (x,y,s,a) in ((176,80,30,8),(196,148,40,-14),(160,206,26,24),(205,232,18,0),(150,120,20,-30)):
        o+=crystal(x,y,s,a)
    o+=T(250,96,'평평한 면',19,'start',halo=True)+L(256,102,222,134,MUTED,1.5)
    o+=T(40,170,'곧은 모서리',19,'start',halo=True)+L(118,176,150,190,MUTED,1.5)
    return svg(360,270,'털실에 붙어 자란 푸른 황산 구리(II) 결정: 평평한 면과 곧은 모서리를 가진다',o)
F['grown']=grown()
def alloy():
    o=''
    # 톱니바퀴
    g=''
    for k in range(10):
        a=math.radians(36*k); g+=f'<rect x="-6" y="-38" width="12" height="12" fill="#9AA5B1" transform="translate(60 50) rotate({36*k})"/>'
    o+=G(g+'<circle cx="60" cy="50" r="30" fill="#B7C2CE" stroke="#7E8B98" stroke-width="2"/><circle cx="60" cy="50" r="10" fill="#fff" stroke="#7E8B98" stroke-width="2"/>','spin',o='60,50',speed='40')
    o+=T(60,112,'기계 부품',19)
    o+=f'<rect x="160" y="10" width="54" height="86" rx="9" fill="#3A3F47"/><rect x="166" y="20" width="42" height="64" rx="3" fill="#8FB8E0"/>'+T(187,112,'스마트폰',19)
    o+=f'<path d="M300 10 L300 82" stroke="#5B6B7F" stroke-width="5" stroke-linecap="round"/><path d="M300 82 Q300 96 316 96 H334 Q340 96 340 90 Q340 84 330 84 H306" fill="#C9CED6" stroke="#8A919C" stroke-width="2"/>'+T(316,112,'스포츠용품',19)
    return svg(370,124,'비결정성 합금이 쓰이는 기계 부품, 스마트폰, 스포츠용품',o)
F['alloy']=alloy()

# ───────── S10 네 결정 카드 그림 ─────────
def mini(kind):
    o=R(4,4,212,122,'#FBFCFD','#C9D3DD',1.5,10)
    if kind=='mol':
        for j in range(2):
            for i in range(4): o+=i2(42+i*46,42+j*48,35 if (i+j)%2==0 else -35,r=12)
        o+=D(64,42,88,42,1.6)+D(156,90,180,90,1.6)
    elif kind=='cov':
        pts,edges=honey(0,0,20,4,2); mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
        P=lambda p:(110+p[0]-mx,66+p[1]-my)
        o+=''.join(B(*P(a),*P(b),3,'#6B7480') for a,b in edges)+''.join(A(*P(p),6,'C','-') for p in pts)
    elif kind=='ion':
        o+=ion_grid(35,28,6,3,30,rp=9,rm=15)
    else:
        o+=metal(40,30,4,2,44,anim=False)
    return svg(220,130,{'mol':'분자 결정 모형','cov':'공유 결정 모형','ion':'이온 결정 모형','met':'금속 결정 모형'}[kind],o)
for k in ('mol','cov','ion','met'): F['mini_'+k]=mini(k)

# ───────── S11 분자 결정: 아이오딘과 얼음 ─────────
def iodine(W=400,H=290,anim=True):
    o=R(6,6,W-12,H-60,'#FBFCFD','#C9D3DD',1.5,12)
    m=''; cs=[]
    for j in range(3):
        for i in range(4):
            x,y=70+i*88,58+j*66; cs.append((x,y)); m+=i2(x,y,35 if (i+j)%2==0 else -35)
    dots=D(cs[1][0]-40,cs[1][1]+4,cs[1][0]-48+0,cs[1][1]+4,0)  # 자리 맞춤용(보이지 않음)
    dots=D(114,58,128,58,2.4)+D(202,124,216,124,2.4)+D(290,190,304,190,2.4)+D(158,91,158,100,2.4)
    o+=G(m,'move',**{'from':'1.2,0','rep':'swing','dur':'0.2'}) if anim else m
    o+=dots
    o+=T(W/2,H-24,'점선: 분자 간 인력(크기 비례 아님)',19,fill=MUTED)
    return svg(W,H,'아이오딘 분자들이 분자 간 인력으로 규칙적으로 배열된 분자 결정 모형',o)
F['iodine']=iodine()
def ice():
    W,H=400,290
    o=R(6,6,W-12,H-60,'#FBFCFD','#C9D3DD',1.5,12)
    cx,cy,rr=200,118,84
    Os=[(cx+rr*math.cos(math.radians(90+60*k)),cy-rr*math.sin(math.radians(90+60*k))) for k in range(6)]
    body=''; hb=''
    for k in range(6):
        ox,oy=Os[k]; nx,ny=Os[(k+1)%6]
        a1=math.degrees(math.atan2(ny-oy,nx-ox))
        outa=math.degrees(math.atan2(oy-cy,ox-cx))
        a2=a1+104.5 if ((a1-outa+540)%360-180)>0 else a1-104.5
        a2=outa+ (a1-outa)*0 + ( -30 if ((a1-outa+540)%360-180)>0 else 30)
        s,hs=water(ox,oy,a1,a2); body+=s
        hx,hy=hs[0]; hb+=D(hx,hy,nx-(nx-hx)*0.42,ny-(ny-hy)*0.42,2.4)
    o+=hb+body
    o+=T(W/2,H-24,'점선: 수소 결합',19,fill=MUTED)
    return svg(W,H,'물 분자 여섯 개가 수소 결합으로 육각형 고리를 이룬 얼음 결정 모형',o)
F['ice']=ice()

# ───────── S12 아이오딘이 녹을 때 ─────────
def melt():
    W,H=600,250
    o=R(6,6,280,200,'#E3EEFB','#7E8B98',2,12)+R(314,6,280,200,'#FDE2E4','#7E8B98',2,12)
    sol=[(56+i*84,52+j*68,35 if (i+j)%2==0 else -35) for j in range(3) for i in range(3)][:6]
    sol=[(60+i*80,60+j*90,35 if (i+j)%2==0 else -35) for j in range(2) for i in range(3)]
    o+=''.join(i2(x,y,a,r=19) for x,y,a in sol)
    liq=[(370,58,-10),(470,92,60),(548,46,20),(392,150,80),(482,170,-40),(552,132,10)]
    for (sx,sy,sa),(lx,ly,la) in zip(sol,liq):
        o+=G(G(i2(lx,ly,la,r=19),'rot',**{'from':str(sa-la),'o':f'{lx},{ly}','dur':'1.6','ease':'soft'}),'move',**{'from':f'{sx+0-lx+0},{sy-ly}','dur':'1.6','ease':'soft'})
    o+=ARW(290,106,310,106,'ink',3)
    o+=T(146,236,'고체 아이오딘',20,weight=700)+T(454,236,'액체 아이오딘',20,weight=700)
    return svg(W,H,'고체 아이오딘의 규칙적으로 배열된 분자 6개가 녹으면 분자 6개가 그대로 흩어진 모형: 원자 12개가 보존되고 분자 속 결합은 유지된다',o)
F['melt']=melt()

# ───────── S13 공유 결정: 다이아몬드와 흑연 ─────────
def dia_fig(W=360,H=300,sc=165,lab=True):
    o=R(6,6,W-12,H-12,'#FBFCFD','#C9D3DD',1.5,12)
    s,(hx,hy)=diamond(W/2,H/2-6,sc)
    o+=s
    if lab: o+=T(hx+52,hy-52,'결합 4개',20,'start',fill=FIELD,weight=700,halo=True)+L(hx+50,hy-58,hx+12,hy-10,FIELD,1.5)
    return svg(W,H,'다이아몬드: 탄소 원자 하나가 이웃한 탄소 원자 4개와 공유 결합해 입체 그물을 이룬 모형',o)
def gra_fig(W=360,H=300,lab=True):
    o=R(6,6,W-12,H-12,'#FBFCFD','#C9D3DD',1.5,12)
    lay=[]
    for k,yy in enumerate((70,150,230)):
        s,pts,ed=graphite_layer(W/2+(14 if k==1 else 0),yy,24,4,2,sq=0.38)
        lay.append((s,pts))
    for k in range(2):
        for p in (lay[k][1][3],lay[k][1][9],lay[k][1][14]):
            q=min(lay[k+1][1],key=lambda t:(t[0]-p[0])**2+(t[1]-p[1]-80)**2)
            o+=D(p[0],p[1]+8,q[0],q[1]-8,2)
    for s,_ in lay: o+=s
    if lab:
        o+=T(W-18,112,'약한 인력',19,'end',fill=MUTED,halo=True)
        p=lay[0][1][6]
        o+=f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="13" fill="none" stroke="{FIELD}" stroke-width="2.5"/>'
        o+=T(W-18,34,'결합 3개',20,'end',fill=FIELD,weight=700,halo=True)
    return svg(W,H,'흑연: 탄소 원자 하나가 3개의 공유 결합으로 육각형 그물 층을 이루고, 층과 층 사이는 약한 인력으로 연결된 모형',o)
F['dia']=dia_fig(); F['gra']=gra_fig()
F['dia_s']=dia_fig(300,250,140,False); F['gra_s']=gra_fig(300,250,False)
def gra_cond():
    W,H=560,230
    o=R(6,6,W-12,H-12,'#FBFCFD','#C9D3DD',1.5,12)
    s,pts,ed=graphite_layer(W/2,108,34,6,2,sq=0.62)
    o+=s
    el=''
    for k,(x,y) in enumerate(((140,84),(230,128),(320,92),(400,132),(190,104),(360,112))):
        el+=EL(x,y-12 if k%2 else y+14,7)
    o+=G(el,'move',**{'from':'-60,0','dur':'1.6','rep':'loop','ease':'lin'})
    o+=f'<rect x="20" y="60" width="14" height="110" rx="3" fill="#7E8B98"/><rect x="{W-34}" y="60" width="14" height="110" rx="3" fill="#7E8B98"/>'
    o+=T(27,52,'(−)극',19)+T(W-27,52,'(+)극',19)
    o+=ARW(200,206,360,206,'minus',3)+T(380,213,'$e^-$',20,'start',fill=MINUS)
    return svg(W,H,'흑연 층에 전압을 걸면 공유 결합에 쓰이지 않은 전자가 층을 따라 (+)극 쪽으로 이동하는 모형',o)
F['gra_cond']=gra_cond()

# ───────── S15 염화 나트륨 결정 ─────────
def nacl():
    W,H=440,330
    o=R(6,6,W-12,H-62,'#FBFCFD','#C9D3DD',1.5,12)
    o+=G(ion_grid(60,48,8,5,46),'move',**{'from':'1.2,0','rep':'swing','dur':'0.18'})
    o+=ion_legend(140,H-28)
    return svg(W,H,'나트륨 이온과 염화 이온이 번갈아 규칙적으로 배열된 염화 나트륨 결정 모형',o)
F['nacl']=nacl()

# ───────── S16 이온 결정의 쪼개짐 ─────────
def cleave(stage,W=300,H=270):
    s=40; x0,y0=64,70
    o=''
    top=ion_grid(x0,y0,5,2,s)
    bot=ion_grid(x0,y0+2*s,5,2,s)
    if stage==1:
        o+=top+bot
        o+=f'<rect x="{x0-58}" y="{y0-18}" width="22" height="76" rx="6" fill="#9AA5B1" stroke="#5B6B7F" stroke-width="2"/>'
        o+=ARW(x0-36,y0+20,x0-21,y0+20,'ink',4)+T(x0-47,y0-28,'힘',20,weight=700)
    elif stage==2:
        o+=G(ion_grid(x0+s,y0,5,2,s),'move',**{'from':f'{-s},0','dur':'1.2','ease':'soft'})+bot
        for i in range(1,5):
            o+=f'<rect x="{x0+i*s-24}" y="{y0+s+12}" width="48" height="16" rx="6" fill="#FFE45C" opacity=".55"/>'
    else:
        o+=G(ion_grid(x0+s,y0-30,5,2,s),'move',**{'from':'0,30','dur':'1.0','ease':'out','delay':'0.3'})+bot
        for i in (1,3):
            o+=ARW(x0+i*s+20,y0+s+28,x0+i*s+20,y0+s-6,'ink',2.5)+ARW(x0+i*s+20,y0+s+36,x0+i*s+20,y0+2*s-14,'ink',2.5)
        o+=T(x0+2*s,H-12,'반발력(같은 전하끼리)',19,weight=700)
    return svg(W,H,['','힘을 가하기 전 양이온과 음이온이 번갈아 배열된 이온 결정','힘을 받아 이온 층이 밀려 같은 전하의 이온끼리 마주 본 모습','같은 전하 사이의 반발력으로 결정이 쪼개진 모습'][stage],o)
for k in (1,2,3): F[f'cleave{k}']=cleave(k)

# ───────── S17 고체·액체·수용액의 전기 전도성 ─────────
def cond(kind,W=320,H=236):
    o=R(40,40,240,184,'#F4F8FB' if kind=='solid' else ('#FDEFE6' if kind=='liq' else WATER),'#7E8B98',2.5,12)
    o+=f'<rect x="54" y="32" width="12" height="196" rx="3" fill="#7E8B98"/><rect x="254" y="32" width="12" height="196" rx="3" fill="#7E8B98"/>'
    o+=T(60,24,'(+)극',19)+T(260,24,'(−)극',19)
    if kind=='solid':
        o+=G(ion_grid(98,82,6,4,25,rp=9,rm=13),'move',**{'from':'1,0','rep':'swing','dur':'0.18'})
    else:
        rnd=random.Random(4 if kind=='liq' else 9)
        n=5 if kind=='liq' else 4
        if kind=='aq':
            wat=''
            for k in range(26):
                wat+=f'<circle cx="{rnd.uniform(84,236):.1f}" cy="{rnd.uniform(56,214):.1f}" r="5" fill="#8C99A6" opacity=".45"/>'
            o+=wat
        pos=''; neg=''
        for k in range(n):
            y=64+k*(140/(n-1))
            pos+=CH(150+rnd.uniform(40,80),y+rnd.uniform(-6,6),9,'+')
            neg+=CH(170-rnd.uniform(40,80),y+12+rnd.uniform(-6,6),13,'-')
        o+=G(pos,'move',**{'from':'-50,0','dur':'1.8','rep':'loop','ease':'lin'})+G(neg,'move',**{'from':'50,0','dur':'1.8','rep':'loop','ease':'lin'})
    nm={'solid':'고체','liq':'액체','aq':'수용액'}[kind]
    lab={'solid':'고체 염화 나트륨: 이온이 제자리에 고정되어 이동하지 못함','liq':'액체 염화 나트륨: 나트륨 이온은 (−)극 쪽, 염화 이온은 (+)극 쪽으로 이동','aq':'염화 나트륨 수용액: 물 분자 사이에서 나트륨 이온은 (−)극 쪽, 염화 이온은 (+)극 쪽으로 이동'}[kind]
    return svg(W,H,lab,o)
for k in ('solid','liq','aq'): F['cond_'+k]=cond(k)

# ───────── S19 금속 결합 ─────────
def metal_big():
    W,H=460,330
    o=R(6,6,W-12,H-62,'#FBFCFD','#C9D3DD',1.5,12)
    o+=metal(62,52,7,4,56)
    o+=CH(120,H-28,RM,'+')+T(146,H-21,'금속 양이온',19,'start')+EL(290,H-28,6)+T(304,H-21,'자유 전자',19,'start')
    return svg(W,H,'규칙적으로 배열된 금속 양이온 사이를 자유 전자가 자유롭게 움직이는 금속 결합 모형',o)
F['metal_big']=metal_big()

# ───────── S20 금속 결정의 성질 카드 ─────────
def m_cond():
    W,H=300,202
    o=R(40,40,220,120,'#EEF0F3','#8A919C',2,8)
    o+=''.join(CH(70+i*40,70+j*60,13,'+') for i in range(5) for j in range(2))
    o+=G(''.join(EL(90+i*40,100+(8 if i%2 else -8),5) for i in range(4)),'move',**{'from':'-40,0','dur':'1.4','rep':'loop','ease':'lin'})
    o+=f'<rect x="22" y="30" width="12" height="140" rx="3" fill="#7E8B98"/><rect x="266" y="30" width="12" height="140" rx="3" fill="#7E8B98"/>'
    o+=T(28,22,'(−)극',19)+T(272,22,'(+)극',19)
    o+=ARW(110,180,190,180,'minus',3)+T(200,187,'$e^-$',19,'start',fill=MINUS)
    return svg(W,H,'금속에 전압을 걸면 자유 전자가 (+)극 쪽으로 이동하는 모습',o)
def m_shine():
    W,H=300,190
    o=f'<rect x="20" y="120" width="260" height="52" rx="6" fill="#C9CED6" stroke="#8A919C" stroke-width="2"/>'
    o+=''.join(CH(42+i*36,146,11,'+') for i in range(7))
    o+=ARW(60,30,140,114,'equi',3.5)+ARW(160,114,240,30,'equi',3.5)
    o+=T(70,64,'빛',20,'end',fill=EQUI,weight=700)+T(238,64,'반사',20,'start',fill=EQUI,weight=700)
    return svg(W,H,'금속 표면에서 빛이 반사되어 광택이 나는 모습',o)
def m_wire():
    W,H=300,190
    o=f'<path d="M30 150 C80 60 130 60 150 110 S230 160 270 60" fill="none" stroke="#C8803A" stroke-width="5"/>'
    o+=f'<path d="M30 40 L150 40 L170 70 L50 70 Z" fill="#DDE2E8" stroke="#8A919C" stroke-width="2"/>'
    o+=T(100,26,'얇게 펴짐(포일)',19)+T(220,174,'가늘게 뽑힘(구리 선)',19)
    return svg(W,H,'얇게 펴진 금속 포일과 가늘게 뽑힌 구리 선',o)
F['m_cond']=m_cond(); F['m_shine']=m_shine(); F['m_wire']=m_wire()

# ───────── S21 금속 결정의 변형 ─────────
def deform():
    W,H=420,270
    s=46; x0,y0=96,46
    o=''
    top=''.join(CH(x0+i*s,y0+j*s,RM,'+') for j in range(2) for i in range(5))
    bot=''.join(CH(x0+i*s,y0+(j+2)*s,RM,'+') for j in range(2) for i in range(5))
    rnd=random.Random(2)
    te=''.join(EL(x0+(i+0.5)*s+rnd.uniform(-6,6),y0+(j+0.5)*s+rnd.uniform(-6,6)) for j in range(2) for i in range(4))
    be=''.join(EL(x0+(i+0.5)*s+rnd.uniform(-6,6),y0+(j+2.5)*s+rnd.uniform(-6,6)) for j in range(1) for i in range(4))+''.join(EL(x0+(i+0.2)*s,y0+1.5*s+rnd.uniform(-5,5)) for i in range(5))
    o+=G(top+te,'move',**{'from':f'{-s},0','dur':'1.4','ease':'soft'})+bot+G(be,'move',**{'from':'-14,6','rep':'swing','dur':'0.6'})
    o+=f'<rect x="{x0-90}" y="{y0-24}" width="30" height="{2*s}" rx="6" fill="#9AA5B1" stroke="#5B6B7F" stroke-width="2"/>'
    o+=ARW(x0-56,y0+s/2-6,x0-28,y0+s/2-6,'ink',4)+T(x0-42,y0-14,'힘',20,weight=700)
    o+=T(W-20,H-12,'층이 밀려도 결합 유지 → 변형됨',19,'end',fill=FIELD,weight=700)
    return svg(W,H,'금속 결정에 힘을 가하면 위쪽 층이 밀려도 자유 전자가 움직여 결합이 유지되어 모양만 변하는 모습',o)
F['deform']=deform()
F['cleave_s']=cleave(3,300,270)

# ───────── S28 디지털 소양: 예시 순서도 ─────────
def box(x,y,w,h,txt,fill='#fff',stroke='#C9D3DD',size=19,weight=None,rx=10,cls=''):
    lines=txt.split('||'); o=R(x,y,w,h,fill,stroke,2,rx)
    for k,t in enumerate(lines):
        o+=T(x+w/2,y+h/2+7+(k-(len(lines)-1)/2)*24,t,size,weight=weight)
    return o
def flow_mine():
    W,H=640,410
    o=''
    q=('#EEF4FC','#9FC0EA'); r=('#EAF6EF','#2E9E6A')
    o+=box(150,10,340,52,'고체 상태에서 전기 전도성이 있는가?',*q,size=19)
    o+=box(150,118,340,46,'액체 상태에서 전기 전도성이 있는가?',*q)
    o+=box(150,222,340,46,'분자 간 인력으로 형성된 고체인가?',*q)
    o+=L(320,62,320,116,MUTED,2.5)+L(320,164,320,220,MUTED,2.5)
    o+=T(330,96,'아니요',19,'start')+T(330,200,'아니요',19,'start')
    o+=L(490,36,540,36,MUTED,2.5)+L(490,141,540,141,MUTED,2.5)+L(490,245,540,245,MUTED,2.5)+L(320,268,320,330,MUTED,2.5)
    o+=T(515,26,'예',19)+T(515,131,'예',19)+T(515,235,'예',19)+T(334,304,'아니요',19,'start')
    o+=f'<g class="step">'+box(542,14,92,44,'금속 결정',*r,weight=700)+'</g>'
    o+=f'<g class="step">'+box(542,119,92,44,'이온 결정',*r,weight=700)+'</g>'
    o+=f'<g class="step">'+box(542,223,92,44,'분자 결정',*r,weight=700)+'</g>'
    o+=f'<g class="step">'+box(270,332,100,44,'공유 결정',*r,weight=700)+'</g>'
    o+=T(20,400,'결정성 고체에서 시작',19,'start',fill=MUTED)
    return svg(W,H,'결정성 고체를 분류하는 예시 순서도: 고체 전기 전도성, 액체 전기 전도성, 분자 간 인력으로 형성된 고체인지 순서로 묻는다',o)
F['flow_mine']=flow_mine()

# ───────── S29 대단원 마무리 07 ─────────
def q07():
    W,H=380,230
    o=''
    s=62; x0,y0=90,50
    o+=''.join(f'<circle cx="{x0+i*s}" cy="{y0+j*s}" r="26" fill="#F6C9CF" opacity=".6"/>' for j in range(3) for i in range(4))
    o+=''.join(CH(x0+i*s,y0+j*s,RM,'+') for j in range(3) for i in range(4))
    rnd=random.Random(6); el=''
    for j in range(3):
        for i in range(3):
            ex,ey=x0+(i+0.5)*s+rnd.uniform(-8,8),y0+(j+0.5)*s-(0 if j<2 else 2*s/2)+rnd.uniform(-8,8)
            if j==2: ey=y0+2*s-14
            el+=EL(ex,ey,6)
    o+=G(el,'move',**{'from':'6,-4','rep':'swing','dur':'0.7'})
    o+=T(22,46,'A',26,weight=700)+L(34,44,x0-22,y0-4,INK,1.5)
    o+=T(22,120,'B',26,weight=700)
    bx,by=x0+0.5*s,y0+0.5*s
    o+=L(34,112,x0+10,108,INK,1.5)
    return svg(W,H,'고체 X의 결합 모형: 큰 입자 A가 규칙적으로 배열되어 있고 그 사이에 작은 입자 B가 흩어져 있다',o)
F['q07']=q07()

# ───────── S30 대단원 마무리 08 순서도 ─────────
def q08():
    W,H=560,440
    o=''
    q=('#EEF4FC','#9FC0EA')
    o+=box(80,6,400,40,'분자 결정, 공유 결정, 이온 결정, 금속 결정','#E8EDF3','#9AA5B1',19,700,8)
    o+=box(170,74,220,44,'고체의 전기 전도성',*q,rx=22)
    o+=box(170,174,220,44,'녹는점',*q,rx=22)
    o+=box(170,276,220,44,'액체의 전기 전도성',*q,rx=22)
    o+=L(280,46,280,72,MUTED,2.5)+L(280,118,280,172,MUTED,2.5)+L(280,218,280,274,MUTED,2.5)
    o+=L(170,96,90,96,MUTED,2.5)+L(90,96,90,124,MUTED,2.5)+T(120,86,'있다.',19)
    o+=L(170,196,90,196,MUTED,2.5)+L(90,196,90,226,MUTED,2.5)+T(120,186,'대체로 낮다.',19)
    o+=L(170,298,90,298,MUTED,2.5)+L(90,298,90,346,MUTED,2.5)+T(120,288,'있다.',19)
    o+=L(390,298,470,298,MUTED,2.5)+L(470,298,470,346,MUTED,2.5)+T(440,288,'없다.',19)
    o+=T(292,152,'없다.',19,'start')+T(292,254,'대체로 높다.',19,'start')
    for (x,y,t) in ((40,126,'A'),(40,228,'B'),(40,348,'C'),(420,348,'D')):
        o+=box(x,y,100,40,t,'#fff','#5B6B7F',22,700,8)
    return svg(W,H,'고체를 분류하는 순서도: 고체의 전기 전도성이 있으면 A, 없고 녹는점이 대체로 낮으면 B, 높고 액체의 전기 전도성이 있으면 C, 없으면 D',o)
F['q08']=q08()


# ───────── S17 범례, S23 해 보기 과정 그림 ─────────
F['ionleg']=svg(260,36,'범례: 나트륨 이온과 염화 이온',ion_legend(20,18))
def tester(x,y):
    o=f'<rect x="{x}" y="{y}" width="56" height="74" rx="10" fill="#F4F6F8" stroke="#7E8B98" stroke-width="2.5"/><circle cx="{x+28}" cy="{y+24}" r="10" fill="#FFE45C" stroke="#B59A1E" stroke-width="2"/>'
    o+=f'<line x1="{x+18}" y1="{y+74}" x2="{x+18}" y2="{y+124}" stroke="#5B6B7F" stroke-width="4"/><line x1="{x+38}" y1="{y+74}" x2="{x+38}" y2="{y+124}" stroke="#5B6B7F" stroke-width="4"/>'
    return o
def test1():
    o='<rect x="40" y="170" width="220" height="16" rx="4" fill="#E9E4D8" stroke="#B9B2A0" stroke-width="1.5"/>'
    o+='<path d="M110 170 Q140 150 170 170 Z" fill="#fff" stroke="#9AA5B1" stroke-width="2"/>'
    o+=G('<rect x="122" y="20" width="16" height="110" rx="5" fill="#B98A5A" transform="rotate(-30 130 75)"/><rect x="150" y="96" width="76" height="34" rx="6" fill="#7E8B98" transform="rotate(-30 188 113)"/>','rot',**{'from':'-25','o':'110,40','dur':'0.5','rep':'loop','ease':'in'})
    o+=T(150,214,'종이로 싼 고체',19)
    return svg(300,230,'종이로 싼 고체를 망치로 치는 모습',o)
def test2():
    o='<rect x="40" y="186" width="220" height="12" rx="4" fill="#E9E4D8" stroke="#B9B2A0" stroke-width="1.5"/>'
    o+=crystal(150,170,22,0,'#E6EAF0')+tester(122,30)
    o+=T(150,224,'고체에 두 전극을 댐',19)
    return svg(300,234,'전기 전도성 측정기의 두 전극을 고체에 댄 모습',o)
def test3():
    o=beaker(80,90,140,110,80)+tester(122,10)
    o+=T(150,224,'수용액에 두 전극을 담금',19)
    return svg(300,234,'전기 전도성 측정기의 두 전극을 수용액에 담근 모습',o)
F['test1']=test1(); F['test2']=test2(); F['test3']=test3()

# ───────── 실행 ─────────
tpl=open(os.path.join(HERE,'slides.tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in F: sys.exit('없는 그림: '+k)
    return F[k]
out=re.sub(r'@@(\w+)@@',rep,tpl)
open(OUT,'w',encoding='utf-8').write(out)
print('ok', len(out), 'slides', out.count('<section'))
