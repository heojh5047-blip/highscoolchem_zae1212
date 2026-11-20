# 1-3 액체의 분자 간 상호작용 — 그림 생성 (slides.tpl.html 의 @@이름@@ 을 채워 slides.html 로)
import math, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT='/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/물질과에너지_미래엔_1-3/gen_out.html'

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
def T(x,y,s,size=20,anchor='middle',weight=None,fill=None,halo=False,cls='',extra=''):
    o=f'<text class="tex{(" "+cls) if cls else ""}" x="{x:.1f}" y="{y:.1f}" data-mix="{esc(s)}" data-size="{size}" data-anchor="{anchor}"'
    if weight: o+=f' data-weight="{weight}"'
    if halo: o+=' data-halo="1"'
    if fill: o+=f' fill="{fill}"'
    return o+extra+'></text>'
def A(x,y,r,el,lab=None,d=False):
    return f'<g data-atom="{x:.1f},{y:.1f},{r},{el}{(","+lab) if lab is not None else ""}{",d" if d else ""}"></g>'
def B(x1,y1,x2,y2,w=7): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#9AA5B1" stroke-width="{w}" stroke-linecap="round"/>'
def D(x1,y1,x2,y2,w=2.5,col='#5B6B7F'): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="5 5"/>'
def ARW(x1,y1,x2,y2,col='ink',w=3,d=False,extra=''): return f'<g data-arw="{x1:.1f},{y1:.1f},{x2:.1f},{y2:.1f},{col},{w}{",d" if d else ""}"{extra}></g>'
def L(x1,y1,x2,y2,col='#5B6B7F',w=2,extra=''): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{extra}/>'
def poly(pts): return ' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def svg(w,h,label,body,disp=None,cls='fig',extra=''):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" style="width:{disp or w}px" aria-label="{esc(label)}"{extra}>{body}</svg>'
PLUS='#D7263D'; MINUS='#1F6FD1'; MUTED='#5B6B7F'; INK='#16233D'
def dplus(x,y,size=22): return T(x,y,r'$\delta^+$',size,fill=PLUS,weight=700)
def dminus(x,y,size=22): return T(x,y,r'$\delta^-$',size,fill=MINUS,weight=700)
def cloud(cx,cy,rx,ry,pol=0):
    """전자 구름: pol=0 무극성, pol=-1 왼쪽이 δ−, pol=+1 왼쪽이 δ+"""
    if pol==0: return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#D5DCE4" stroke="#8C99A6" stroke-width="1.5"/>'
    cl='#BFD6F6' if pol<0 else '#F6C9CF'; cr='#F6C9CF' if pol<0 else '#BFD6F6'
    return (f'<path d="M{cx} {cy-ry} A{rx} {ry} 0 0 0 {cx} {cy+ry} Z" fill="{cl}"/>'
            f'<path d="M{cx} {cy-ry} A{rx} {ry} 0 0 1 {cx} {cy+ry} Z" fill="{cr}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#8C99A6" stroke-width="1.5"/>')
def dipole(x1,y,x2,col='ink',w=3):
    """쌍극자 모멘트 화살표 (+ 꼬리) x1→x2"""
    tx=x1+0.15*(x2-x1)
    return ARW(x1,y,x2,y,col,w)+L(tx,y-7,tx,y+7,INK if col=='ink' else col,w)

F={}
# ───────── 그래프 도우미 ─────────
def axes(x0,y0,x1,y1,xt,yt,fx,fy,xlab,ylab,xls=19,tick=18,grid=True):
    o=''
    if grid:
        for v in xt: o+=L(fx(v),y0,fx(v),y1,'#E3E8EE',1)
        for v in yt: o+=L(x0,fy(v),x1,fy(v),'#E3E8EE',1)
    o+=L(x0,y0,x1,y0,MUTED,2)+L(x0,y0,x0,y1,MUTED,2)
    for v in xt: o+=L(fx(v),y0,fx(v),y0+6,MUTED,2)+T(fx(v),y0+26,str(v),tick)
    for v in yt: o+=L(x0-6,fy(v),x0,fy(v),MUTED,2)+T(x0-10,fy(v)+6,str(v).replace('-','−'),tick,'end')
    o+=T(x1,y0+50,xlab,xls,'end')+T(x0-4,y1-16,ylab,xls,'start')
    return o

# ───────── S1 표지 ─────────
def water(ox,oy,ang,ro=24,rh=18,d=46,lab=True,hb=None):
    """물 분자: O 중심, 이등분선 각 ang(도, y 아래 +), 반환 (svg, [H 위치])"""
    hs=[]
    for s in (-52.25,52.25):
        a=math.radians(ang+s); hs.append((ox+d*math.cos(a),oy+d*math.sin(a)))
    o=''.join(B(ox,oy,hx,hy) for hx,hy in hs)
    o+=A(ox,oy,ro,'O',None if lab else '-')+''.join(A(hx,hy,rh,'H',None if lab else '-') for hx,hy in hs)
    return o,hs
def cover():
    o='<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    # 비커
    o+='<path d="M120 200 V470 Q120 490 140 490 H400 Q420 490 420 470 V200" fill="#F8FBFD" stroke="#7E8B98" stroke-width="5"/>'
    o+='<rect x="124" y="300" width="292" height="186" rx="6" fill="#DDEEF8"/><line x1="124" y1="300" x2="416" y2="300" stroke="#9FC3DD" stroke-width="3"/>'
    import random; rnd=random.Random(5)
    pos=[(170,345,60),(240,335,150),(310,350,20),(370,340,200),(150,420,250),(215,410,100),(285,425,300),(355,415,170),(190,470,320),(265,470,30),(340,468,120)]
    liq=''
    for x,y,a in pos:
        w,_=water(x,y,a,ro=14,rh=9,d=22,lab=False); liq+=w
    o+=f'<g data-anim="move" data-from="1.5,-1" data-rep="swing" data-dur="0.5">{liq}</g>'
    vap=''
    for x,y,a in [(200,150,40),(330,110,210)]:
        w,_=water(x,y,a,ro=14,rh=9,d=22,lab=False); vap+=w
    o+=f'<g data-anim="move" data-from="6,-10" data-rep="swing" data-dur="0.9">{vap}</g>'
    o+=ARW(260,290,260,215,'ink',3)+ARW(392,262,392,190,'ink',3)
    o+=D(170,345,198,380)+D(285,425,310,350)
    return f'<svg class="cover-fig" viewBox="0 0 540 540" aria-label="비커 속 물 분자들이 서로 가까이 모여 있고, 일부 분자가 증발해 위로 날아가는 모습" data-audit="skip">{o}</svg>'
F['cover']=cover()

# ───────── S3 생각 열기: 탄산음료 ─────────
def soda():
    o='<path d="M120 60 L150 300 H290 L320 60" fill="#F8FBFD" stroke="#7E8B98" stroke-width="4"/>'
    o+='<path d="M131 110 L150 296 H290 L309 110 Z" fill="#E9D7B8"/>'
    bub=''
    for i,(x,y,r) in enumerate([(180,250,7),(220,200,6),(260,240,8),(205,150,6),(245,130,7),(275,175,5),(190,195,5)]):
        bub+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#9FC3DD" stroke-width="2"/>'
    o+=f'<g data-anim="move" data-from="0,60" data-dur="1.6" data-rep="loop" data-ease="lin">{bub}</g>'
    o+=ARW(220,95,220,25,'ink',3)+ARW(270,95,290,30,'ink',3)
    o+=T(330,40,r'$\ce{CO2}$ 기체로',20,'start')+T(330,66,'날아감',20,'start')
    o+=T(220,335,'물은 액체로 남음',20)
    return svg(440,350,'탄산음료가 담긴 컵에서 이산화 탄소 기포가 올라와 날아가는 모습',o)
F['soda']=soda()

# ───────── S4 상태와 분자 간 상호작용: 두 카드 ─────────
def state_card(kind):
    o='<rect x="10" y="10" width="300" height="170" rx="12" fill="%s" stroke="#7E8B98" stroke-width="2"/>'%('#FDE2E4' if kind=='hot' else '#E3EEFB')
    if kind=='hot':
        pts=[(60,50,30),(150,120,200),(250,60,120),(90,140,300),(230,145,250),(170,45,80)]
        m=''
        for x,y,a in pts:
            ar=math.radians(a)
            m+=f'<circle cx="{x}" cy="{y}" r="11" fill="#6C8EBF" stroke="#3E5F8F" stroke-width="1.5"/>'+ARW(x+13*math.cos(ar),y+13*math.sin(ar),x+45*math.cos(ar),y+45*math.sin(ar),'ink',2)
        o+=f'<g data-anim="move" data-from="4,-3" data-rep="swing" data-dur="0.45">{m}</g>'
    else:
        pts=[(110,80),(134,78),(158,84),(120,102),(146,104),(170,106),(196,92),(100,126),(126,128),(152,130),(180,128),(206,118)]
        m=''
        for i,(x,y) in enumerate(pts):
            m+=f'<circle cx="{x+20}" cy="{y}" r="11" fill="#6C8EBF" stroke="#3E5F8F" stroke-width="1.5"/>'
        o+=f'<g data-anim="move" data-from="1.5,-1" data-rep="swing" data-dur="0.6">{m}</g>'
    return svg(320,190,'분자 운동이 활발해 흩어진 기체 분자' if kind=='hot' else '분자 간 인력으로 서로 붙들린 분자',o)
F['st_hot']=state_card('hot'); F['st_cold']=state_card('cold')

# ───────── S5 세 가지 상태 ─────────
def three_states():
    o=''
    names=['기체','액체','고체']
    for k in range(3):
        x0=10+k*300
        o+=f'<rect x="{x0}" y="10" width="260" height="200" rx="12" fill="#F4F8FB" stroke="#7E8B98" stroke-width="2.5"/>'
        o+=T(x0+130,242,names[k],26,weight=700)
    gas=[(50,50),(200,40),(120,110),(230,160),(60,170),(170,175)]
    m=''.join(f'<circle cx="{10+x}" cy="{10+y}" r="12" fill="#6C8EBF" stroke="#3E5F8F" stroke-width="1.5"/>' for x,y in gas)
    o+=f'<g data-anim="move" data-from="7,-5" data-rep="swing" data-dur="0.5">{m}</g>'
    liq=[(52,120),(78,112),(104,122),(130,114),(156,124),(182,116),(208,122),(64,144),(90,140),(116,148),(142,140),(168,148),(194,142),(220,150),(50,170),(76,168),(102,174),(128,170),(154,176),(180,170),(206,176)]
    m=''.join(f'<circle cx="{310+x}" cy="{10+y}" r="12" fill="#6C8EBF" stroke="#3E5F8F" stroke-width="1.5"/>' for x,y in liq)
    o+=f'<g data-anim="move" data-from="2.5,-1.5" data-rep="swing" data-dur="0.55">{m}</g>'
    sol=''
    for i in range(6):
        for j in range(5):
            sol+=f'<circle cx="{610+60+i*28}" cy="{10+52+j*28}" r="12" fill="#6C8EBF" stroke="#3E5F8F" stroke-width="1.5"/>'
    o+=f'<g data-anim="move" data-from="1.2,0" data-rep="swing" data-dur="0.18">{sol}</g>'
    return svg(880,252,'기체는 분자가 멀리 흩어져 있고, 액체는 분자가 가까이 붙어 무질서하며, 고체는 분자가 규칙적으로 배열된 모습',o)
F['three']=three_states()

# ───────── S6 HCl 쌍극자 ─────────
def hcl():
    o=cloud(205,120,135,72,pol=+1)
    o+=B(150,120,250,120)+A(150,120,18,'H')+A(250,120,29,'Cl')
    o+=dplus(150,36)+dminus(250,36)
    o+=dipole(150,222,262)+T(206,258,'쌍극자 모멘트',19)
    o+=T(392,128,'공유 전자쌍이',19,'middle')+T(392,154,'Cl 쪽으로',19,'middle')
    return svg(470,270,'염화 수소 분자: 수소 쪽이 부분적인 양전하, 염소 쪽이 부분적인 음전하를 띠고, 쌍극자 모멘트 화살표가 수소에서 염소를 향하는 모습',o)
F['hcl']=hcl()

# ───────── S7 쌍극자·쌍극자 힘 ─────────
def dd():
    o=''
    rH,rC,bl=15,23,38
    rows=[(80,+1),(190,-1)]
    for ry,dirn in rows:
        for k in range(3):
            cx=70+k*125
            if dirn>0: hx,cx2=cx,cx+bl
            else: hx,cx2=cx+bl,cx
            mol=cloud((hx+cx2)/2,ry,46,32,pol=(+1 if dirn>0 else -1))+B(hx,ry,cx2,ry,6)+A(hx,ry,rH,'H','-')+A(cx2,ry,rC,'Cl','-')
            o+=f'<g data-anim="rot" data-from="{28 if (k+ry)%2 else -24}" data-o="{(hx+cx2)/2:.0f},{ry}" data-dur="1.4" data-ease="out">{mol}</g>'
    # 인력 점선: 가로(같은 줄 Cl…H), 세로(위 H…아래 Cl)
    for k in range(2):
        o+=D(70+k*125+bl+rC+2,80,70+(k+1)*125-rH-2,80)
        o+=D(70+k*125+rC+2,190,70+(k+1)*125+bl-rH-2,190)
    for k in range(3):
        o+=D(70+k*125,80+30,70+k*125,190-30)+D(70+k*125+bl,80+30,70+k*125+bl,190-30)
    o+=dplus(70,40,20)+dminus(108,40,20)
    o+=T(400,262,'점선: 쌍극자·쌍극자 힘(인력)',19,'end',fill=MUTED)
    lg=A(30,258,12,'H','-')+T(48,264,'H',19,'start')+A(80,258,14,'Cl','-')+T(100,264,'Cl',19,'start')
    o+=lg
    return svg(420,280,'염화 수소 분자들이 부분 양전하 쪽과 부분 음전하 쪽이 마주 보도록 배열하고 그 사이에 점선으로 인력이 표시된 모습',o)
F['dd']=dd()

# ───────── S9 분산력 단계 카드 ─────────
def disp(n):
    o=''
    if n==1:
        o+=cloud(90,80,62,42)+cloud(230,80,62,42)
        o+=f'<circle cx="90" cy="80" r="6" fill="{INK}"/><circle cx="230" cy="80" r="6" fill="{INK}"/>'
    elif n==2:
        o+=f'<g data-anim="move" data-from="10,0" data-dur="1" data-ease="out">{cloud(90,80,62,42,pol=-1)}</g>'+cloud(230,80,62,42)
        o+=f'<circle cx="90" cy="80" r="6" fill="{INK}"/><circle cx="230" cy="80" r="6" fill="{INK}"/>'
        o+=dminus(52,30,20)+dplus(128,30,20)
    else:
        o+=cloud(90,80,62,42,pol=-1)+f'<g data-anim="move" data-from="10,0" data-dur="1" data-delay=".3" data-ease="out">{cloud(230,80,62,42,pol=-1)}</g>'
        o+=f'<circle cx="90" cy="80" r="6" fill="{INK}"/><circle cx="230" cy="80" r="6" fill="{INK}"/>'
        o+=dminus(52,30,20)+dplus(128,30,20)+dminus(192,30,20)+dplus(268,30,20)
        o+=D(152,80,168,80,3)+T(160,150,'분산력',20,weight=700)
    return svg(320,160,['두 무극성 분자의 전자 구름이 고르게 분포한 모습','왼쪽 분자의 전자 분포가 순간적으로 한쪽으로 치우쳐 쌍극자가 생긴 모습','이웃 분자에도 쌍극자가 유도되어 두 쌍극자 사이에 분산력이 작용하는 모습'][n-1],o)
for n in (1,2,3): F[f'disp{n}']=disp(n)

# ───────── S10 할로젠 그래프 ─────────
def halo():
    x0,x1,y0,y1=80,500,320,40
    fx=lambda v:x0+(v)*(x1-x0)/300; fy=lambda v:y0-(v+200)*(y0-y1)/400
    o=axes(x0,y0,x1,y1,[0,50,100,150,200,250,300],[-200,-100,0,100,200],fx,fy,'분자량','끓는点'.replace('点','점')+' [°C]')
    d=[('F2',38,-188),('Cl2',71,-34),('Br2',160,59),('I2',254,184)]
    pts=[(fx(m),fy(b)) for _,m,b in d]
    o+=f'<polyline points="{poly(pts)}" fill="none" stroke="{INK}" stroke-width="3" data-anim="draw" data-dur="1.6"/>'
    off=[(14,4,'start'),(14,10,'start'),(0,-16,'middle'),(-14,6,'end')]
    for (nm,m,b),(x,y),(dx,dy,an) in zip(d,pts,off):
        o+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{INK}"/>'+T(x+dx,y+dy,'$\\ce{'+nm+'}$',20,an,halo=True)
    return svg(520,380,'플루오린, 염소, 브로민, 아이오딘의 분자량이 커질수록 끓는점이 높아지는 그래프',o)
F['halo']=halo()

# ───────── S11 알케인 ─────────
def alkane(n):
    o=''; y=105; cs=[]
    if n==1: cs=[150]
    elif n==2: cs=[115,185]
    else: cs=[80,150,220]
    hs=[]
    for c in cs: hs+= [(c,y-58),(c,y+58)]
    hs+=[(cs[0]-60,y),(cs[-1]+60,y)]
    for a,b in zip(cs,cs[1:]): o+=B(a,y,b,y)
    for hx,hy in hs:
        c=min(cs,key=lambda c:abs(c-hx)); o+=B(c,y,hx,hy)
    o+=''.join(A(c,y,24,'C') for c in cs)+''.join(A(hx,hy,18,'H') for hx,hy in hs)
    nm=['CH4','C2H6','C3H8'][n-1]
    return svg(300,210,'메테인 에테인 프로페인'.split()[n-1]+' 분자 모형',o)
for n in (1,2,3): F[f'alk{n}']=alkane(n)

# ───────── S12 물 / 클로로메테인 ─────────
def h2o_mol():
    o,_=water(110,70,90)
    return svg(220,150,'굽은 형인 물 분자 모형',o)
def ch3cl():
    o=B(110,95,110,35)+B(110,95,55,130)+B(110,95,165,130)+B(110,95,110,150)
    o+=A(110,150,18,'H')+A(55,130,18,'H')+A(165,130,18,'H')+A(110,95,24,'C')+A(110,35,29,'Cl')
    return svg(220,180,'클로로메테인 분자 모형',o)
F['h2o']=h2o_mol(); F['ch3cl']=ch3cl()

# ───────── S13 수소 결합: 물 그물 + HF 사슬 ─────────
def hbond():
    o=''; d=46; hb=50
    def U(a): return (math.cos(math.radians(a)),math.sin(math.radians(a)))
    mols=[]
    O0=(205,180); mols.append((O0,90))
    # O0의 두 H(38°, 142°)가 이웃 O로 수소 결합
    for a,bis in ((37.75,-20),(142.25,200)):
        ux,uy=U(a); mols.append(((O0[0]+ux*(d+hb+18),O0[1]+uy*(d+hb+18)),bis))
    # 위쪽 분자: H 하나가 O0를 향함(90°)
    Ot=(O0[0],O0[1]-(d+hb+18)); mols.append((Ot,90-52.25))
    lines=''
    for (ox,oy),bis in mols:
        w,_=water(ox,oy,bis); o+=w
    # 수소 결합 점선
    hb_lines=''
    ux,uy=U(37.75); hb_lines+=D(O0[0]+ux*(d+20),O0[1]+uy*(d+20),O0[0]+ux*(d+hb-6),O0[1]+uy*(d+hb-6),3)
    ux,uy=U(142.25); hb_lines+=D(O0[0]+ux*(d+20),O0[1]+uy*(d+20),O0[0]+ux*(d+hb-6),O0[1]+uy*(d+hb-6),3)
    hb_lines+=D(O0[0],Ot[1]+d+20,O0[0],O0[1]-26,3)
    o+=f'<g data-anim="fade" data-dur="1" data-delay=".4">{hb_lines}</g>'
    o+=T(O0[0]+16,O0[1]-62,'수소 결합',19,'start',weight=700,halo=True)
    return svg(400,340,'물 분자의 수소 원자와 이웃 물 분자의 산소 원자 사이에 점선으로 수소 결합이 표시된 모습',o)
def hf():
    o=''; x=40; y=60; s=''
    pts=[]
    for k in range(3):
        fx_,fy_=34+k*122,60+(k%2)*40
        hx_,hy_=fx_+44,fy_+(20 if k%2==0 else -20)
        pts.append(((fx_,fy_),(hx_,hy_)))
    for (f_,h_) in pts: o+=B(*f_,*h_)
    for i,((f_,h_)) in enumerate(pts):
        o+=A(*f_,24,'F')+A(*h_,18,'H')
    for i in range(2):
        h_=pts[i][1]; f2=pts[i+1][0]
        vx,vy=f2[0]-h_[0],f2[1]-h_[1]; n=math.hypot(vx,vy); vx/=n; vy/=n
        o+=f'<g data-anim="fade" data-dur="1" data-delay=".4">{D(h_[0]+vx*20,h_[1]+vy*20,f2[0]-vx*27,f2[1]-vy*27,3)}</g>'
    return svg(340,140,'플루오린화 수소 분자들이 수소 결합으로 사슬처럼 이어진 모습',o)
F['hbond']=hbond(); F['hf']=hf()

# ───────── S14 세기 막대 ─────────
def strength():
    o=''
    rows=[('수소 결합',380),('쌍극자·쌍극자 힘',230),('분산력',120)]
    for i,(nm,w) in enumerate(rows):
        y=20+i*62
        o+=T(190,y+30,nm,21,'end',weight=700)
        o+=f'<g data-anim="scale" data-from="0,1" data-o="205,{y+20}" data-dur="1" data-delay="{.2*i:.1f}"><rect x="205" y="{y}" width="{w}" height="40" rx="6" fill="#E9EEF3" stroke="#5B6B7F" stroke-width="2"/></g>'
    o+=T(590,214,'(분자량이 비슷할 때 · 크기 비례 아님)',19,'end',fill=MUTED)
    return svg(600,226,'분자량이 비슷할 때 수소 결합, 쌍극자·쌍극자 힘, 분산력 순으로 세기가 약해지는 막대',o)
F['strength']=strength()

# ───────── 수소 화합물 자료 ─────────
DATA=[ # (족, 주기, 식, 분자량, 끓는점, 극성, 수소결합)
 (14,2,'CH4',16,-161.5,0,0),(14,3,'SiH4',32,-111.9,0,0),(14,4,'GeH4',77,-88.5,0,0),(14,5,'SnH4',123,-52.0,0,0),
 (15,2,'NH3',17,-33.3,1,1),(15,3,'PH3',34,-87.7,1,0),(15,4,'AsH3',78,-62.5,1,0),(15,5,'SbH3',125,-17.0,1,0),
 (16,2,'H2O',18,100.0,1,1),(16,3,'H2S',34,-60.3,1,0),(16,4,'H2Se',81,-41.3,1,0),(16,5,'H2Te',130,-2.0,1,0),
 (17,2,'HF',20,19.5,1,1),(17,3,'HCl',36.5,-85.0,1,0),(17,4,'HBr',81,-66.7,1,0),(17,5,'HI',128,-35.4,1,0)]
GC={14:'#16233D',15:'#7B4FC8',16:'#2E9E6A',17:'#E08A2C'}
# 라벨 자리 (dx, dy, anchor)
LOFF={'CH4':(-12,8,'end'),'SiH4':(-12,10,'end'),'GeH4':(0,30,'middle'),'SnH4':(-12,10,'end'),
 'NH3':(-12,6,'end'),'PH3':(-12,14,'end'),'AsH3':(-10,-12,'end'),'SbH3':(-12,4,'end'),
 'H2O':(14,8,'start'),'H2S':(12,-6,'start'),'H2Se':(0,-14,'middle'),'H2Te':(12,0,'start'),
 'HF':(14,6,'start'),'HCl':(12,16,'start'),'HBr':(12,18,'start'),'HI':(12,10,'start')}
def marker(x,y,g,r=7,fill=None,extra=''):
    c=GC[g]; f=fill or c
    if g==14: return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{f}" stroke="{c}" stroke-width="2"{extra}/>'
    if g==15: return f'<rect x="{x-r:.1f}" y="{y-r:.1f}" width="{2*r}" height="{2*r}" fill="{f}" stroke="{c}" stroke-width="2"{extra}/>'
    if g==16: return f'<polygon points="{poly([(x,y-r-2),(x+r+1,y+r-1),(x-r-1,y+r-1)])}" fill="{f}" stroke="{c}" stroke-width="2"{extra}/>'
    return f'<polygon points="{poly([(x,y-r-2),(x+r+2,y),(x,y+r+2),(x-r-2,y)])}" fill="{f}" stroke="{c}" stroke-width="2"{extra}/>'
def hgraph(mode='all'):
    x0,x1,y0,y1=80,570,430,44
    fx=lambda v:x0+v*(x1-x0)/140; fy=lambda v:y0-(v+200)*(y0-y1)/350
    o=axes(x0,y0,x1,y1,[0,20,40,60,80,100,120,140],[-200,-150,-100,-50,0,50,100,150],fx,fy,'분자량','끓는점 [°C]')
    dimset={'NH3','H2O','HF'} if mode=='nohb' else set()
    for g in (14,15,16,17):
        rows=[r for r in DATA if r[0]==g]
        pts=[(fx(r[3]),fy(r[4])) for r in rows]
        if mode=='nohb' and g!=14:
            o+=f'<polyline points="{poly(pts[:2])}" fill="none" stroke="{GC[g]}" stroke-width="2.5" stroke-dasharray="4 5" opacity=".45"/>'
            o+=f'<polyline points="{poly(pts[1:])}" fill="none" stroke="{GC[g]}" stroke-width="3" data-anim="draw" data-dur="1.2"/>'
        else:
            o+=f'<polyline points="{poly(pts)}" fill="none" stroke="{GC[g]}" stroke-width="3" data-anim="draw" data-dur="1.4"/>'
    for r in DATA:
        x,y=fx(r[3]),fy(r[4]); dim=r[2] in dimset
        o+=marker(x,y,r[0],extra=' opacity=".45"' if dim else '')
        dx,dy,an=LOFF[r[2]]
        o+=T(x+dx,y+dy,'$\\ce{'+r[2]+'}$',18,an,halo=True,extra=' data-overlap="ok"' if False else '')
    if mode=='hb':
        for nm in ('NH3','H2O','HF'):
            r=[q for q in DATA if q[2]==nm][0]
            o+=f'<circle cx="{fx(r[3]):.1f}" cy="{fy(r[4]):.1f}" r="22" fill="#FFE45C" fill-opacity=".35" stroke="{PLUS}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    # 범례
    for i,g in enumerate((14,15,16,17)):
        ly=70+i*30
        o+=L(450,ly,486,ly,GC[g],3)+marker(468,ly,g,6)+T(496,ly+7,f'{g}족',19,'start')
    return o
F['hg_all']=svg(620,490,'14족~17족 원소의 수소 화합물의 분자량에 따른 끓는점 그래프',hgraph('all'))
F['hg_nohb']=svg(620,490,'암모니아, 물, 플루오린화 수소를 흐리게 하고 나머지 수소 화합물의 분자량에 따른 끓는점을 나타낸 그래프',hgraph('nohb'))
F['hg_hb']=svg(620,490,'암모니아, 물, 플루오린화 수소의 끓는점이 같은 족의 다른 수소 화합물보다 매우 높은 것을 강조한 그래프',hgraph('hb'))

# ───────── S21 14족 막대 ─────────
def g14bars():
    o=''; base=250
    rows=[r for r in DATA if r[0]==14]
    o+=L(40,base,460,base,MUTED,2)
    for i,r in enumerate(rows):
        h=(r[4]+200)*1.0; x=70+i*100
        o+=f'<g data-anim="scale" data-from="1,0" data-o="{x+30},{base}" data-dur=".9" data-delay="{.15*i:.2f}"><rect x="{x}" y="{base-h:.1f}" width="60" height="{h:.1f}" fill="#E3E8EE" stroke="{INK}" stroke-width="2"/></g>'
        o+=T(x+30,base-h-12,f'{r[4]:.0f}'.replace('-','−')+' °C',19)
        o+=T(x+30,base+28,'$\\ce{'+r[2]+'}$',20)+T(x+30,base+54,f'분자량 {r[3]}',19)
    o+=T(460,base-4+0,'',19)
    return svg(480,320,'14족 수소 화합물 메테인, 실레인, 저메인, 스테인의 끓는점 막대: 분자량이 클수록 높다',o)
F['g14']=g14bars()

# ───────── 증기압 ─────────
ANT={'ether':(6.92032,1064.07,228.8),'ethanol':(8.20417,1642.89,230.3),'water':(8.07131,1730.63,233.426),'acetic':(7.38782,1533.313,222.309)}
def vp(k,t): a,b,c=ANT[k]; return 10**(a-b/(c+t))
def bp(k,P): a,b,c=ANT[k]; return b/(a-math.log10(P))-c
VC={'ether':'#7B4FC8','ethanol':'#E08A2C','water':'#0E7490','acetic':'#2E9E6A'}
VN={'ether':'다이에틸 에터','ethanol':'에탄올','water':'물','acetic':'아세트산'}
def vpgraph(keys,W=560,H=380,tmax=120,pmax=800,anim=True,lab=True,line760=True,extra=''):
    x0,x1,y0,y1=80,W-30,H-60,46
    fx=lambda v:x0+v*(x1-x0)/tmax; fy=lambda v:y0-v*(y0-y1)/pmax
    yt=list(range(0,pmax+1,200)) if pmax<=800 else list(range(0,pmax+1,400))
    o=axes(x0,y0,x1,y1,list(range(0,tmax+1,20)),yt,fx,fy,'$t$ [°C]','증기압 [mmHg]')
    if line760:
        o+=f'<line x1="{x0}" y1="{fy(760):.1f}" x2="{x1}" y2="{fy(760):.1f}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="7 6"/>'+T(x0+6,fy(760)+22,'760',18,'start',fill=MUTED)
    for k in keys:
        pts=[]
        t=0.0
        while t<=tmax:
            p=vp(k,t)
            if p>pmax:
                # 끝점 보간
                tt=bp(k,pmax); pts.append((fx(tt),fy(pmax))); break
            pts.append((fx(t),fy(p))); t+=1
        o+=f'<polyline points="{poly(pts)}" fill="none" stroke="{VC[k]}" stroke-width="3.5"'+(' data-anim="draw" data-dur="1.5"' if anim else '')+'/>'
    o+=extra
    return o,fx,fy
def vp_water():
    o,fx,fy=vpgraph(['water'],W=520,H=360)
    o+=f'<line x1="{fx(100):.1f}" y1="{fy(760):.1f}" x2="{fx(100):.1f}" y2="{fy(0):.1f}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 5"/>'
    o+=f'<circle cx="{fx(100):.1f}" cy="{fy(760):.1f}" r="7" fill="{PLUS}"/>'+T(fx(100)-12,fy(760)-12,'기준 끓는점 100 °C',19,'end',weight=700,halo=True)
    o+=T(fx(60)+10,fy(vp('water',60))-14,'물',20,'end',fill=VC['water'],weight=700,halo=True)
    return svg(520,360,'물의 증기 압력 곡선: 온도가 높을수록 증기압이 커지고 100 °C에서 760 mmHg가 된다',o)
F['vp_water']=vp_water()
def vp4():
    o,fx,fy=vpgraph(['ether','ethanol','water','acetic'],W=560,H=380)
    pos={'ether':(bp('ether',420)+4,420,'start'),'ethanol':(bp('ethanol',620)-4,620,'end'),'water':(bp('water',540)-4,540,'end'),'acetic':(bp('acetic',300)+3,300,'start')}
    for k,(t,p,an) in pos.items(): o+=T(fx(t),fy(p),VN[k],19,an,fill=VC[k],weight=700,halo=True)
    return svg(560,380,'다이에틸 에터, 에탄올, 물, 아세트산의 증기 압력 곡선과 760 mmHg 기준선',o)
F['vp4']=vp4()
def vp_cook():
    o,fx,fy=vpgraph(['water'],W=470,H=360,tmax=140,pmax=1600,line760=False)
    for P,nm,c in ((1520,'압력솥(약 2 기압)',PLUS),(760,'1 기압',INK),(532,'높은 산(약 0.7 기압)',MINUS)):
        t=bp('water',P)
        o+=f'<line x1="{fx(0):.1f}" y1="{fy(P):.1f}" x2="{fx(t):.1f}" y2="{fy(P):.1f}" stroke="{c}" stroke-width="2" stroke-dasharray="7 6"/>'
        o+=f'<line x1="{fx(t):.1f}" y1="{fy(P):.1f}" x2="{fx(t):.1f}" y2="{fy(0):.1f}" stroke="{c}" stroke-width="1.5" stroke-dasharray="3 5"/>'
        o+=f'<circle cx="{fx(t):.1f}" cy="{fy(P):.1f}" r="6" fill="{c}"/>'
        o+=T(fx(t)-10,fy(P)+(22 if P>1000 else -10),f'{nm} {t:.0f} °C',18,'end',fill=c,weight=700,halo=True)
    return svg(470,360,'물의 증기 압력 곡선에서 외부 압력이 2 기압, 1 기압, 0.7 기압일 때의 끓는점',o)
F['vp_cook']=vp_cook()

# ───────── S24 유리판 위 방울 ─────────
def drops():
    o='<rect x="20" y="150" width="440" height="16" rx="3" fill="#E6EDF3" stroke="#7E8B98" stroke-width="2"/>'
    o+='<g data-anim="scale" data-from="2.2,2.2" data-o="130,150" data-dur="2.4" data-ease="out"><path d="M95 150 Q130 120 165 150 Z" fill="#F3E9FB" stroke="#9C7BC9" stroke-width="2"/></g>'
    o+='<path d="M290 150 Q350 94 410 150 Z" fill="#DDEEF8" stroke="#9FC3DD" stroke-width="2"/>'
    o+=f'<g data-anim="move" data-from="0,40" data-dur="1.6" data-rep="loop" data-ease="lin"><circle cx="118" cy="80" r="6" fill="#B79AD9"/><circle cx="145" cy="58" r="6" fill="#B79AD9"/><circle cx="128" cy="30" r="6" fill="#B79AD9"/></g>'
    o+=f'<g data-anim="move" data-from="0,30" data-dur="2.6" data-rep="loop" data-ease="lin"><circle cx="352" cy="62" r="6" fill="#7FB6DA"/></g>'
    o+=T(130,200,'에탄올: 빨리 증발',20,weight=700)+T(350,200,'물: 천천히 증발',20,weight=700)
    return svg(480,215,'유리판 위의 에탄올 방울은 빨리 작아지고 물 방울은 천천히 증발하는 모습',o)
F['drops']=drops()

# ───────── S25 플라스크 동적 평형 ─────────
def flask(n):
    o='<path d="M120 20 H160 V70 L250 190 Q258 205 240 205 H40 Q22 205 30 190 L120 70 Z" fill="#F8FBFD" stroke="#7E8B98" stroke-width="3"/>'
    o+='<rect x="114" y="8" width="52" height="18" rx="4" fill="#B7C2CE"/>'
    lv=[150,158,158][n-1]
    xl=lambda y:120-(y-70)*(90/120)
    o+=f'<path d="M{xl(lv):.1f} {lv} H{280-xl(lv):.1f} L250 190 Q258 205 240 205 H40 Q22 205 30 190 Z" fill="#DDEEF8" stroke="#9FC3DD" stroke-width="2"/>'
    vap={1:[],2:[(110,110),(165,95),(140,128),(190,135)],3:[(110,110),(165,95),(140,128),(190,135),(95,138),(150,80),(125,90),(178,118)]}[n]
    m=''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#7FB6DA" stroke="#3E7FA8" stroke-width="1.2"/>' for x,y in vap)
    if m: o+=f'<g data-anim="move" data-from="3,-3" data-rep="swing" data-dur="0.5">{m}</g>'
    up,dn={1:(46,0),2:(46,22),3:(46,46)}[n]
    o+=ARW(282,lv+6,282,lv+6-up,'ink',3)+T(282,lv-52,'증발',22)
    if dn: o+=ARW(342,lv-40,342,lv-40+dn,'ink',3)+T(342,lv-52,'응축',22)
    return svg(380,215,['처음 상태: 액체가 증발만 하는 플라스크','동적 평형 전: 증발이 응축보다 많은 플라스크','동적 평형: 증발과 응축의 속도가 같은 플라스크'][n-1],o)
for n in (1,2,3): F[f'fl{n}']=flask(n)

# ───────── S26 증기압 막대 ─────────
def vpbars():
    o=''
    rows=[('다이에틸 에터',502),('에탄올',59),('물',23.8)]
    for i,(nm,p) in enumerate(rows):
        y=20+i*62; w=p*0.78
        o+=T(150,y+30,nm,21,'end',weight=700)
        o+=f'<g data-anim="scale" data-from="0,1" data-o="165,{y+20}" data-dur="1.1" data-delay="{.2*i:.1f}"><rect x="165" y="{y}" width="{w:.1f}" height="40" rx="6" fill="#E3EEFB" stroke="#5B6B7F" stroke-width="2"/></g>'
        o+=T(165+w+10,y+28,f'{p:g} mmHg',20,'start',weight=700)
    o+=T(690,206,'25 °C의 증기압 (자료: 미국국립표준기술연구소)',19,'end',fill=MUTED)
    return svg(700,218,'25 °C에서 다이에틸 에터 502 mmHg, 에탄올 59 mmHg, 물 23.8 mmHg의 증기압 막대',o)
F['vpbars']=vpbars()

# ───────── 상평형 그림 ─────────
def qpt(p0,c,p1,t): return ((1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0],(1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1])
def solve_y(p0,c,p1,y):
    lo,hi=0.0,1.0
    f=lambda t:qpt(p0,c,p1,t)[1]-y
    for _ in range(60):
        m=(lo+hi)/2
        if (f(lo)>0)==(f(m)>0): lo=m
        else: hi=m
    return qpt(p0,c,p1,(lo+hi)/2)
def phase(kind):
    W,H=480,380; X0,Y0=70,320
    if kind=='w':
        Tp=(200,236); Bp=(184,40); Cp=(440,62); Ap=(84,310); cA=(150,286); cC=(360,226); y1=170
    else:
        Tp=(250,200); Bp=(290,40); Cp=(440,62); Ap=(84,310); cA=(170,280); cC=(380,190); y1=270
    o=f'<path d="M{X0} 40 L{Bp[0]} 40 L{Tp[0]} {Tp[1]} Q{cA[0]} {cA[1]} {Ap[0]} {Ap[1]} L{X0} {Ap[1]+8} Z" fill="#E7DDF3"/>'
    o+=f'<path d="M{Tp[0]} {Tp[1]} L{Bp[0]} 40 L{Cp[0]} 40 L{Cp[0]} {Cp[1]} Q{cC[0]} {cC[1]} {Tp[0]} {Tp[1]} Z" fill="#DDEEF8"/>'
    o+=L(X0,Y0,W-20,Y0,MUTED,2)+L(X0,Y0,X0,30,MUTED,2)
    o+=f'<path d="M{Ap[0]} {Ap[1]} Q{cA[0]} {cA[1]} {Tp[0]} {Tp[1]}" fill="none" stroke="{INK}" stroke-width="3"/>'
    o+=f'<path d="M{Tp[0]} {Tp[1]} L{Bp[0]} {Bp[1]}" fill="none" stroke="{INK}" stroke-width="3"/>'
    o+=f'<path d="M{Tp[0]} {Tp[1]} Q{cC[0]} {cC[1]} {Cp[0]} {Cp[1]}" fill="none" stroke="{INK}" stroke-width="3"/>'
    o+=f'<circle cx="{Tp[0]}" cy="{Tp[1]}" r="6" fill="{PLUS}"/><circle cx="{Cp[0]}" cy="{Cp[1]}" r="4" fill="{INK}"/>'
    o+=T(Tp[0]+12,Tp[1]+22,'T',20,'start',weight=700)+T(Bp[0]+(10 if kind=='w' else 10),Bp[1]+18,'B',20,'start',weight=700)+T(Cp[0]+8,Cp[1]-6,'C',20,'start',weight=700)+T(Ap[0]-4,Ap[1]-12,'A',20,'end',weight=700)
    if kind=='w':
        o+=T(118,130,'고체',22,weight=700)+T(300,110,'액체',22,weight=700)+T(370,280,'기체',22,weight=700)
        o+=T(172,88,'융해 곡선',19,'end',halo=True)+T(462,196,'증기 압력 곡선',19,'end',halo=True)+T(110,262,'승화 곡선',19,'start',halo=True)
    else:
        o+=T(150,140,'고체',22,weight=700)+T(370,110,'액체',22,weight=700)+T(380,270,'기체',22,weight=700)
        o+=T(258,110,'융해 곡선',19,'end',halo=True)+T(424,150,'증기 압력 곡선',19,'end',halo=True)+T(118,254,'승화 곡선',19,'start',halo=True)
    # 1 기압 선, 삼중점 선
    if kind=='w':
        xf=Tp[0]+(Bp[0]-Tp[0])*(Tp[1]-y1)/(Tp[1]-Bp[1]); xb=solve_y(Tp,cC,Cp,y1)[0]
        o+=f'<path d="M{X0} {y1} H{xb:.1f}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>'
        o+=f'<path d="M{xf:.1f} {y1} V{Y0} M{xb:.1f} {y1} V{Y0} M{X0} {Tp[1]} H{Tp[0]}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="3 4"/>'
        o+=T(X0-8,y1+6,'1',18,'end')+T(X0-8,Tp[1]+6,'0.006',18,'end')
        o+=T(xf-4,Y0+24,'0',18,'end')+T(xb,Y0+24,'100',18)
    else:
        xs=solve_y(Ap,cA,Tp,y1)[0]
        o+=f'<path d="M{X0} {y1} H{xs:.1f}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>'
        o+=f'<path d="M{xs:.1f} {y1} V{Y0} M{Tp[0]} {Tp[1]} V{Y0} M{X0} {Tp[1]} H{Tp[0]}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="3 4"/>'
        o+=T(X0-8,y1+6,'1.0',18,'end')+T(X0-8,Tp[1]+6,'5.1',18,'end')
        o+=T(xs,Y0+24,'−78',18)+T(Tp[0]+4,Y0+24,'−57',18)
    o+=T(W-20,Y0+48,'$t$ [°C]',19,'end')+T(X0-4,22,'압력 [기압]',19,'start')
    o+=T(W-20,22,'(크기 비례 아님)',18,'end',fill=MUTED)
    return svg(W,H,('물' if kind=='w' else '이산화 탄소')+'의 상평형 그림: 고체, 액체, 기체 영역과 융해 곡선, 증기 압력 곡선, 승화 곡선, 삼중점 T',o)
F['ph_w']=phase('w'); F['ph_c']=phase('c')

# ───────── 대단원 마무리 05 그림 ─────────
def q05():
    o=''
    # (가) H2 … O2
    o+=B(30,50,62,50,6)+A(30,50,18,'H')+A(62,50,18,'H')+D(84,50,104,50,3)+B(128,50,170,50,6)+A(128,50,24,'O')+A(170,50,24,'O')
    o+=T(100,110,'(가) 분산력',20,weight=700)
    # (나) HCl … HCl
    x=250
    o+=B(x,50,x+42,50,6)+A(x,50,18,'H')+A(x+42,50,29,'Cl')+D(x+74,50,x+96,50,3)+B(x+114,50,x+156,50,6)+A(x+114,50,18,'H')+A(x+156,50,29,'Cl')
    o+=T(x+80,110,'(나) 쌍극자·쌍극자 힘',20,weight=700)
    x=500
    o+=B(x,50,x+40,50,6)+A(x,50,18,'H')+A(x+40,50,24,'F')+D(x+66,50,x+90,50,3)+B(x+108,50,x+148,50,6)+A(x+108,50,18,'H')+A(x+148,50,24,'F')
    o+=T(x+76,110,'(다) 수소 결합',20,weight=700)
    return svg(680,124,'분자 간 상호작용의 세 유형: (가) 수소 분자와 산소 분자 사이 분산력, (나) 염화 수소 분자 사이 쌍극자·쌍극자 힘, (다) 플루오린화 수소 분자 사이 수소 결합',o)
F['q05']=q05()

# ───────── 대단원 마무리 06 그래프 ─────────
def q06():
    W,H=470,330; x0,x1,y0,y1=80,450,270,40
    fx=lambda v:x0+v*(x1-x0)/100; fy=lambda v:y0-v*(y0-y1)/700
    o=axes(x0,y0,x1,y1,[0,20,40,60,80,100],[0,100,200,300,400,500,600,700],fx,fy,'$t$ [°C]','증기압 [mmHg]',tick=18)
    def P(tb,t): return 760*math.exp(3800*(1/(tb+273)-1/(t+273)))
    for nm,tb in (('A',36),('B',70),('C',90)):
        pts=[]; t=0
        while t<=100:
            p=P(tb,t)
            if p>700:
                tt=1/(1/(tb+273)-math.log(700/760)/3800)-273; pts.append((fx(tt),fy(700))); break
            pts.append((fx(t),fy(p))); t+=1
        o+=f'<polyline points="{poly(pts)}" fill="none" stroke="{INK}" stroke-width="3"/>'
        o+=T(pts[-1][0]-6,fy(700)+24,nm,20,'end',weight=700,halo=True)
    return svg(W,H,'물질 A, B, C의 온도에 따른 증기압 그래프: 같은 온도에서 증기압은 A가 가장 크고 C가 가장 작다',o)
F['q06']=q06()

# ───────── 실행 ─────────
tpl=open(os.path.join(HERE,'slides.tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in F: sys.exit('없는 그림: '+k)
    return F[k]
out=re.sub(r'@@(\w+)@@',rep,tpl)
open(OUT,'w',encoding='utf-8').write(out)
print('ok', len(out), 'slides', out.count('<section'))
