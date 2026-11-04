import math
PLUS='#D7263D'; MINUS='#1F6FD1'; FIELD='#2E9E6A'; BF='#7B4FC8'; MUTED='#5B6B7F'; GRAV='#8C99A6'; EQUI='#E08A2C'
def T(x,y,tex=None,mix=None,size=22,anchor='middle',fill=None,extra=''):
    a=f'data-tex="{tex}"' if tex is not None else f'data-mix="{mix}"'
    f=f' fill="{fill}"' if fill else ''
    return f'<text class="tex" x="{x:g}" y="{y:g}" {a} data-size="{size}" data-anchor="{anchor}"{f}{extra}></text>'
def beaker(cx,top,bot,w,liq=None,stroke='#7E8B98'):
    l=cx-w/2; r=cx+w/2
    s=''
    if liq is not None:
        s+=f'<path d="M{l+2:g} {liq:g} L{l+2:g} {bot-16:g} Q{l+2:g} {bot-2:g} {l+16:g} {bot-2:g} L{r-16:g} {bot-2:g} Q{r-2:g} {bot-2:g} {r-2:g} {bot-16:g} L{r-2:g} {liq:g} Z" fill="#DDEEF8"/>'
        s+=f'<line x1="{l+2:g}" y1="{liq:g}" x2="{r-2:g}" y2="{liq:g}" stroke="#9FC3DD" stroke-width="2"/>'
    s+=f'<path d="M{l-8:g} {top:g} L{l:g} {top+8:g} L{l:g} {bot-16:g} Q{l:g} {bot:g} {l+16:g} {bot:g} L{r-16:g} {bot:g} Q{r:g} {bot:g} {r:g} {bot-16:g} L{r:g} {top:g}" fill="none" stroke="{stroke}" stroke-width="3" stroke-linejoin="round"/>'
    return s
def part(x,y,kind,r=14):
    if kind=='m': return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="#C9D3DD" stroke="{GRAV}" stroke-width="2"/>'
    if kind=='p': return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="#FBD5DA" stroke="{PLUS}" stroke-width="2.5"/><line x1="{x-6:g}" y1="{y:g}" x2="{x+6:g}" y2="{y:g}" stroke="{PLUS}" stroke-width="2.5"/><line x1="{x:g}" y1="{y-6:g}" x2="{x:g}" y2="{y+6:g}" stroke="{PLUS}" stroke-width="2.5"/>'
    if kind=='n': return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="#D6E6FA" stroke="{MINUS}" stroke-width="2.5"/><line x1="{x-6:g}" y1="{y:g}" x2="{x+6:g}" y2="{y:g}" stroke="{MINUS}" stroke-width="2.5"/>'

# ---------- S1 cover ----------
def cover():
    s='<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    for cx in (165,375):
        s+=beaker(cx,150,390,170,liq=210)
    ps=[(115,250),(160,240),(205,255),(130,300),(185,300),(120,350),(170,355),(215,345)]
    s+=''.join(part(x,y,'p',13) for x,y in ps)
    qs=[(325,250),(370,245),(420,255),(335,300),(395,305),(325,352),(380,350),(425,345)]
    for i,(x,y) in enumerate(qs): s+=part(x,y,'p' if i==4 else 'm',13)
    s+=T(165,128,mix='염산',size=26)+T(375,128,mix='아세트산 수용액',size=22)
    s+='<g data-anim="fade" data-dur=".8" data-delay=".6"><rect x="125" y="412" width="80" height="26" rx="4" fill="#E0505A"/></g>'
    s+='<g data-anim="fade" data-dur=".8" data-delay="1.1"><rect x="335" y="412" width="80" height="26" rx="4" fill="#F0A040"/></g>'
    s+=T(165,474,mix='pH 약 2',size=24,fill=PLUS)+T(375,474,mix='pH 약 4',size=24,fill='#C2410C')
    s+=T(270,512,mix='같은 농도, 다른 pH',size=22,fill=MUTED)
    return s

# ---------- S3 생각 열기 ----------
def think():
    s=''
    for cx,name in ((120,'염산'),(340,'아세트산 수용액')):
        s+=beaker(cx,60,230,150,liq=110)+T(cx,40,mix=name,size=22)
    s+='<g data-anim="fade" data-dur=".8" data-delay=".5"><rect x="85" y="255" width="70" height="24" rx="4" fill="#E0505A"/></g>'
    s+='<g data-anim="fade" data-dur=".8" data-delay="1"><rect x="305" y="255" width="70" height="24" rx="4" fill="#F0A040"/></g>'
    s+=T(120,310,mix='pH 약 2',size=22,fill=PLUS)+T(340,310,mix='pH 약 4',size=22,fill='#C2410C')
    s+=T(230,345,mix='농도가 같은 두 수용액',size=20,fill=MUTED)
    return s

# ---------- S5 이온화 정도 ----------
def ioniz():
    s=''
    cxs=[110,330,660,880]
    for cx in cxs: s+=beaker(cx,44,200,160,liq=70)
    s+=f'<g data-arw="200,120,240,120,muted,3"></g><g data-arw="750,120,790,120,muted,3"></g>'
    for cx,t in zip(cxs,['이온화하기 전','이온화한 후']*2): s+=T(cx,28,mix=t,size=20,fill=MUTED)
    six=[(-45,100),(0,95),(45,105),(-40,160),(5,165),(45,155)]
    for cx in (110,660): s+=''.join(part(cx+dx,y,'m') for dx,y in six)
    # HA after: 6 H3O+ 6 A-
    grid=[(dx,y) for y in (95,132,169) for dx in (-54,-18,18,54)]
    ions=''.join(part(330+dx,y,'p' if (i+i//4)%2==0 else 'n') for i,(dx,y) in enumerate(grid))
    s+=f'<g data-anim="fade" data-dur=".9" data-delay=".5">{ions}</g>'
    hb=[(-45,100),(10,95),(-40,160),(5,165),(48,155)]
    s+=''.join(part(880+dx,y,'m') for dx,y in hb)
    s+=f'<g data-anim="fade" data-dur=".9" data-delay="1.1">{part(928,100,"p")}{part(915,125,"n")}</g>'
    # bars
    base=300; k=10
    def bar(x,n,col,lab,delay):
        h=n*k
        b=f'<rect x="{x-13}" y="{base-h}" width="26" height="{h}" fill="{col}" opacity=".85"/>' if n else ''
        return (f'<g data-anim="scale" data-from="1,0" data-o="{x},{base}" data-dur=".8" data-delay="{delay}">{b}</g>' if n else '')+T(x,326,tex=lab,size=19)
    for cx in (110,660): s+=f'<line x1="{cx-60}" y1="{base}" x2="{cx+60}" y2="{base}" stroke="{MUTED}" stroke-width="2"/>'
    for cx in (330,880): s+=f'<line x1="{cx-80}" y1="{base}" x2="{cx+80}" y2="{base}" stroke="{MUTED}" stroke-width="2"/>'
    s+=bar(110,6,'#AEB9C5','\\ce{HA}',0)
    s+=bar(280,0,'#AEB9C5','\\ce{HA}',0)+bar(330,6,PLUS,'\\ce{H3O+}',.8)+bar(380,6,MINUS,'\\ce{A-}',.8)
    s+=bar(660,6,'#AEB9C5','\\ce{HB}',0)
    s+=bar(830,5,'#AEB9C5','\\ce{HB}',1.3)+bar(880,1,PLUS,'\\ce{H3O+}',1.3)+bar(930,1,MINUS,'\\ce{B-}',1.3)
    s+=T(22,240,mix='입자 수',size=18,anchor='start',fill=MUTED)
    # legend
    lx=250
    s+=part(lx,362,'m',10)+T(lx+18,369,mix='산 분자($\\ce{HA}$, $\\ce{HB}$)',size=19,anchor='start')
    s+=part(lx+250,362,'p',10)+T(lx+268,369,tex='\\ce{H3O+}',size=19,anchor='start')
    s+=part(lx+370,362,'n',10)+T(lx+388,369,mix='짝염기($\\ce{A-}$, $\\ce{B-}$)',size=19,anchor='start')
    s+=T(lx+620,369,mix='(물 분자는 생략)',size=19,anchor='start',fill=MUTED)
    return s

# ---------- S8 Ka bars ----------
def kabars():
    acids=[('\\ce{HF}','6.3\\times10^{-4}',6.3e-4),('\\ce{HCOOH}','1.8\\times10^{-4}',1.8e-4),('\\ce{CH3COOH}','1.8\\times10^{-5}',1.8e-5),('\\ce{H2CO3}','4.5\\times10^{-7}',4.5e-7),('\\ce{HClO}','4.0\\times10^{-8}',4.0e-8),('\\ce{HCN}','6.2\\times10^{-10}',6.2e-10)]
    X0=284;K=40
    s=''
    for e in (-10,-8,-6,-4):
        x=X0+K*(e+10)
        s+=f'<line x1="{x}" y1="20" x2="{x}" y2="312" stroke="#E2E7EC" stroke-width="1.5"/>'
        s+=T(x,340,tex=f'10^{{{e}}}',size=19,fill=MUTED)
    s+=f'<line x1="{X0}" y1="312" x2="{X0+K*7+8}" y2="312" stroke="{MUTED}" stroke-width="2"/>'
    for i,(f,v,ka) in enumerate(acids):
        y=40+50*i; L=K*(math.log10(ka)+10)
        s+=T(150,y+8,tex=f,size=22,anchor='end')+T(160,y+7,tex=v,size=19,anchor='start',fill=MUTED)
        s+=f'<g data-anim="scale" data-from="0,1" data-o="{X0},{y}" data-dur=".7" data-delay="{.2+.15*i:.2f}"><rect x="{X0}" y="{y-13}" width="{L:.1f}" height="26" rx="3" fill="{PLUS}" opacity=".78"/></g>'
    s+=T(X0+K*3.5,374,mix='$K_\\mathrm{a}$ (로그 눈금)',size=19,fill=MUTED)
    return s

def kbbars():
    bs=[('\\ce{NH3}','1.8\\times10^{-5}',1.8e-5),('\\ce{N2H4}','1.3\\times10^{-6}',1.3e-6)]
    X0=230;K=44;s=''
    for e in (-10,-8,-6,-4):
        x=X0+K*(e+10); s+=f'<line x1="{x}" y1="16" x2="{x}" y2="132" stroke="#E2E7EC" stroke-width="1.5"/>'+T(x,160,tex=f'10^{{{e}}}',size=19,fill=MUTED)
    s+=f'<line x1="{X0}" y1="132" x2="{X0+K*7}" y2="132" stroke="{MUTED}" stroke-width="2"/>'
    for i,(f,v,kb) in enumerate(bs):
        y=44+54*i; L=K*(math.log10(kb)+10)
        s+=T(100,y+8,tex=f,size=22,anchor='end')+T(110,y+7,tex=v,size=19,anchor='start',fill=MUTED)
        s+=f'<g data-anim="scale" data-from="0,1" data-o="{X0},{y}" data-dur=".7" data-delay="{.3+.3*i:.1f}"><rect x="{X0}" y="{y-13}" width="{L:.1f}" height="26" rx="3" fill="{MINUS}" opacity=".78"/></g>'
    s+=T(X0+K*3.5,192,mix='$K_\\mathrm{b}$ (로그 눈금)',size=19,fill=MUTED)
    return s

# ---------- S11 pair figure ----------
def pairs():
    xs=[100,300,548,752]
    fm=['\\ce{CH3COOH(aq)}','\\ce{H2O(l)}','\\ce{CH3COO-(aq)}','\\ce{H3O+(aq)}']
    s=''
    for x,t in zip(xs,fm): s+=T(x,128,tex=t,size=26)
    s+=T(218,128,tex='+',size=26)+T(410,128,tex='\\ce{<=>}',size=26)+T(660,128,tex='+',size=26)
    s+=T(914,128,tex='K_\\mathrm{a}=1.8\\times10^{-5}',size=22)
    s+=f'<g data-anim="draw" data-dur=".9" data-delay=".4"><path d="M100 92 L100 62 L548 62 L548 92" fill="none" stroke="{FIELD}" stroke-width="3" stroke-linejoin="round"/></g>'
    s+=T(320,50,mix='짝산·짝염기 쌍',size=20,fill=FIELD)
    rl=[('\\text{산}_1',PLUS),('\\text{염기}_2',MINUS),('\\text{염기}_1',MINUS),('\\text{산}_2',PLUS)]
    for x,(t,c) in zip(xs,rl): s+=T(x,168,tex=t,size=22,fill=c)
    s+=f'<g data-anim="draw" data-dur=".9" data-delay="1"><path d="M300 180 L300 202 L752 202 L752 180" fill="none" stroke="{BF}" stroke-width="3" stroke-linejoin="round"/></g>'
    s+=T(525,226,mix='짝산·짝염기 쌍',size=20,fill=BF)
    return s

def dom():
    s=f'<rect x="20" y="24" width="300" height="76" rx="38" fill="#fff" stroke="{GRAV}" stroke-width="2.5"/>'
    s+=f'<rect x="580" y="24" width="300" height="76" rx="38" fill="#fff" stroke="{BF}" stroke-width="2.5"/>'
    s+=T(170,72,tex='\\ce{CH3COOH + H2O}',size=26)+T(730,72,tex='\\ce{CH3COO- + H3O+}',size=26)
    s+=T(170,138,mix='상대적으로 약한 산과 염기',size=20,fill=MUTED)+T(730,138,mix='상대적으로 강한 산과 염기',size=20,fill=BF)
    s+=f'<g data-arw="350,48,550,48,field,2"></g>'+T(450,36,mix='정반응',size=19,fill=FIELD)
    s+=f'<g data-arw="550,84,350,84,bfield,7"></g>'+T(450,124,mix='역반응 우세',size=20,fill=BF,extra=' data-weight="700"')
    return s

def ladder():
    A=['\\ce{HCl}','\\ce{H3O+}','\\ce{HF}','\\ce{CH3COOH}','\\ce{H2CO3}','\\ce{HCN}','\\ce{H2O}']
    B=['\\ce{Cl-}','\\ce{H2O}','\\ce{F-}','\\ce{CH3COO-}','\\ce{HCO3-}','\\ce{CN-}','\\ce{OH-}']
    s=T(205,26,mix='산',size=21,fill=PLUS,extra=' data-weight="700"')+T(445,26,mix='짝염기',size=21,fill=MINUS,extra=' data-weight="700"')
    for i,(a,b) in enumerate(zip(A,B)):
        y=66+50*i
        s+=f'<rect x="140" y="{y-20}" width="130" height="40" rx="8" fill="#fff" stroke="#E2B9BF" stroke-width="1.5"/><rect x="380" y="{y-20}" width="130" height="40" rx="8" fill="#fff" stroke="#B9CDEB" stroke-width="1.5"/>'
        s+=T(205,y+8,tex=a,size=22)+T(445,y+8,tex=b,size=22)
        s+=f'<g data-arw="282,{y},368,{y},muted,2"></g>'
    s+=T(325,58,tex='-\\ce{H+}',size=18,fill=MUTED)
    s+=f'<g data-arw="96,380,96,48,plus,5"></g>'+T(56,190,mix='산의||세기||증가',size=20,fill=PLUS)
    s+=f'<g data-arw="554,48,554,380,minus,5"></g>'+T(598,190,mix='염기의||세기||증가',size=20,fill=MINUS)
    return s

def procfigs():
    # card1 four beakers
    a=''
    for i,(cx,lab) in enumerate(zip((40,110,180,250),('(가)','(나)','(다)','(라)'))):
        a+=beaker(cx,40,130,50,liq=85)+T(cx,158,mix=lab,size=19)
    a+=T(145,24,mix='각각 20 mL',size=19,fill=MUTED)
    # card2 meter
    b=beaker(150,70,170,110,liq=110)
    b+='<rect x="20" y="30" width="96" height="58" rx="8" fill="#16233D"/><rect x="28" y="38" width="80" height="30" rx="4" fill="#CFE8D8"/>'
    b+=T(68,61,mix='pH 2.91',size=18)
    b+='<g data-anim="move" data-from="0,-40" data-dur="1" data-delay=".4" data-ease="out"><line x1="150" y1="20" x2="150" y2="150" stroke="#3A3F47" stroke-width="7" stroke-linecap="round"/><ellipse cx="150" cy="150" rx="7" ry="10" fill="#9AA5B1"/></g>'
    b+='<path d="M116 52 Q140 40 146 24" fill="none" stroke="#3A3F47" stroke-width="2.5"/>'
    # card3 wash
    c=beaker(200,80,170,90,liq=120)+T(200,196,mix='폐액 비커',size=19,fill=MUTED)
    c+='<path d="M50 170 L50 95 Q50 80 65 80 L95 80 Q110 80 110 95 L110 170 Z" fill="#EAF4FB" stroke="#7E8B98" stroke-width="2.5"/><path d="M80 80 L80 60 L150 40" fill="none" stroke="#7E8B98" stroke-width="3"/>'
    c+=T(80,196,mix='증류수',size=19,fill=MUTED)
    c+='<line x1="200" y1="10" x2="200" y2="105" stroke="#3A3F47" stroke-width="7" stroke-linecap="round"/>'
    c+='<g data-anim="fade" data-dur=".6" data-delay=".5" data-rep="loop"><circle cx="168" cy="58" r="4" fill="#5FA8DD"/><circle cx="178" cy="72" r="4" fill="#5FA8DD"/></g>'
    return a,b,c

def resplot():
    th=[1.0,2.87,13.0,11.13]; me=[1.1,2.9,12.9,11.1]
    X=[110,210,310,410]; Y=lambda p:270-p*17
    s=f'<line x1="60" y1="20" x2="60" y2="270" stroke="{MUTED}" stroke-width="2"/><line x1="60" y1="270" x2="470" y2="270" stroke="{MUTED}" stroke-width="2"/>'
    for p in (0,7,14):
        s+=f'<line x1="54" y1="{Y(p)}" x2="60" y2="{Y(p)}" stroke="{MUTED}" stroke-width="2"/>'+T(48,Y(p)+6,tex=str(p),size=19,anchor='end',fill=MUTED)
    s+=f'<line x1="60" y1="{Y(7)}" x2="470" y2="{Y(7)}" stroke="{GRAV}" stroke-width="1.5" stroke-dasharray="6 5"/>'
    s+=T(70,26,tex='\\text{pH}',size=19,anchor='start',fill=MUTED)
    for x,f in zip(X,['\\ce{HCl}','\\ce{CH3COOH}','\\ce{NaOH}','\\ce{NH3}']): s+=T(x,300,tex=f,size=19)
    for x,t in zip(X,th):
        y=Y(t); s+=f'<path d="M{x-14} {y} L{x-6} {y-9} L{x+2} {y} L{x-6} {y+9} Z" fill="#fff" stroke="#16233D" stroke-width="2.5"/>'
    pts=''.join(f'<circle cx="{x+8}" cy="{Y(m):.1f}" r="7" fill="{EQUI}"/>' for x,m in zip(X,me))
    s+=f'<g data-anim="pop" data-o="260,150" data-dur=".7" data-delay=".5">{pts}</g>'
    s+=f'<path d="M120 333 L128 324 L136 333 L128 342 Z" fill="#fff" stroke="#16233D" stroke-width="2.5"/>'+T(144,340,mix='계산한 값',size=19,anchor='start')
    s+=f'<circle cx="268" cy="333" r="7" fill="{EQUI}"/>'+T(282,340,mix='측정한 값(예시)',size=19,anchor='start')
    return s
