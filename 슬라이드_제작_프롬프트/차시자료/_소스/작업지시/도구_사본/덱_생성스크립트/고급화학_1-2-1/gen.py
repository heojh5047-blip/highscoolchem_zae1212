# -*- coding: utf-8 -*-
"""고급화학 1-2-1 공유 결합 그림 생성: tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다."""
import math, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
# ★ 출력 경로: 반드시 이 덱(1-2-1) 폴더
OUT='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/1-2-1_공유_결합/slides.html'
assert '1-2-1_공유_결합' in OUT
exec(open(os.path.join(HERE,'helpers.py'),encoding='utf-8').read())
FIG={}
BOND='#9AA5B1'
def svg(vb,w,label,body,cls='fig',extra=''):
    return f'<svg class="{cls}" viewBox="{vb}" style="width:{w}px" aria-label="{label}"{(" "+extra) if extra else ""}>'+''.join(body)+'</svg>'
def G(body,attrs=''):
    return f'<g {attrs}>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def an(kind,body,**kw):
    a=f'data-anim="{kind}"'+''.join(f' data-{k.replace("_","-")}="{v}"' for k,v in kw.items())
    return G(body,a)

# ═════ 루이스 구조 도우미 ═════
VAL={'H':1,'B':3,'C':4,'N':5,'O':6,'F':7,'P':5,'Cl':7,'S':6}
SIDE={'r':0,'u':90,'l':180,'d':270}
def _b(el,S,ux,uy):
    rx=(0.62 if len(el)>1 else 0.40)*S; ry=0.46*S
    return 1/math.sqrt((ux/rx)**2+(uy/ry)**2)
def _dir(a):
    a=SIDE.get(a,a); t=math.radians(a); return math.cos(t),-math.sin(t)
def lewis(atoms,bonds,S=34,check=True,name='',num=None,fcshow=True,bw=2.6,elcol=None):
    """atoms: [dict(el,x,y,lp=[방향],rad=[방향],fc=정수,fcp='ur',oct=8,col=None)]
    bonds: [(i,j,차수,모양)] 모양 'l' 선, 'd' 점(전자쌍), 'p' 선+점선(공명 혼성), 'q' 점선만"""
    s=[]
    elec=[0]*len(atoms); bsum=[0]*len(atoms)
    for (i,j,o,st) in bonds:
        a,b=atoms[i],atoms[j]
        dx,dy=b['x']-a['x'],b['y']-a['y']; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
        ba=_b(a['el'],S,ux,uy)+0.10*S; bb=_b(b['el'],S,ux,uy)+0.10*S
        x1,y1=a['x']+ux*ba,a['y']+uy*ba; x2,y2=b['x']-ux*bb,b['y']-uy*bb
        if st=='d':
            mx,my=(a['x']+b['x'])/2,(a['y']+b['y'])/2
            offs={1:[0],2:[-0.14*S,0.14*S],3:[-0.26*S,0,0.26*S]}[o]
            for t in offs:
                cx,cy=mx+ux*t,my+uy*t
                for sg in (-1,1): s.append(f'<circle cx="{f(cx+px*sg*0.18*S)}" cy="{f(cy+py*sg*0.18*S)}" r="{f(0.1*S)}" fill="{INK}"/>')
        else:
            offs={1:[0],2:[-0.12*S,0.12*S],3:[-0.17*S,0,0.17*S]}[o if st not in 'pq' else (2 if st=='p' else 1)]
            for k,t in enumerate(offs):
                dash=None
                if st=='p' and k==1: dash='5 4'
                if st=='q': dash='6 5'
                s.append(L(x1+px*t,y1+py*t,x2+px*t,y2+py*t,INK,bw,dash=dash,extra='stroke-linecap="round"'))
        for k in (i,j): bsum[k]+=o; elec[k]+=2*o
    for k,a in enumerate(atoms):
        el=a['el']; x,y=a['x'],a['y']
        for d in a.get('lp',[]):
            ux,uy=_dir(d); bd=_b(el,S,ux,uy)+0.26*S; cx,cy=x+ux*bd,y+uy*bd; px,py=-uy,ux
            for sg in (-1,1): s.append(f'<circle cx="{f(cx+px*sg*0.18*S)}" cy="{f(cy+py*sg*0.18*S)}" r="{f(0.1*S)}" fill="{INK}"/>')
            elec[k]+=2
        for d in a.get('rad',[]):
            ux,uy=_dir(d); bd=_b(el,S,ux,uy)+0.26*S
            s.append(f'<circle cx="{f(x+ux*bd)}" cy="{f(y+uy*bd)}" r="{f(0.1*S)}" fill="{INK}"/>'); elec[k]+=1
        s.append(T(x,y+0.36*S,tex='\\mathrm{'+el+'}',size=S,fill=a.get('col') or elcol))
        nl=len(a.get('lp',[])); nr=len(a.get('rad',[]))
        fcal=VAL[el]-2*nl-nr-bsum[k]
        if check:
            need=a.get('oct',2 if el=='H' else 8)
            if need is not None and elec[k]!=need: sys.exit(f'[{name}] {el}{k} 전자 {elec[k]} ≠ {need}')
            if a.get('fc',0)!=fcal: sys.exit(f'[{name}] {el}{k} 형식 전하 {fcal} ≠ {a.get("fc",0)}')
        fc=a.get('fc',0)
        if fc and fcshow:
            p=a.get('fcp','ur'); w2=(0.98 if len(el)>1 else 0.80)*S
            ox={'ur':w2,'ul':-w2,'dr':w2,'dl':-w2,'u':0,'d':0,'r':w2*1.25,'l':-w2*1.25}[p]
            oy={'ur':-0.74*S,'ul':-0.74*S,'dr':0.74*S,'dl':0.74*S,'u':-1.25*S,'d':1.25*S,'r':-0.2*S,'l':-0.2*S}[p]
            col=PLUS if fc>0 else MINUS
            tx={1:'+',-1:'-',2:'2+',-2:'2-'}[fc]
            rr=12 if abs(fc)==1 else 15
            s.append(C(x+ox,y+oy,rr,col,1.8,fill='#fff'))
            s.append(T(x+ox,y+oy+6.3,tex=tx,size=18,fill=col,weight=700))
        if num is not None and num[k] is not None:
            s.append(T(x,y-1.25*S,tex=num[k],size=19,fill=MUTED))
    return ''.join(s)
def bracket(x1,y1,x2,y2,ch='-',size=22):
    s=P([(x1+9,y1),(x1,y1),(x1,y2),(x1+9,y2)],INK,2.2)+P([(x2-9,y1),(x2,y1),(x2,y2),(x2-9,y2)],INK,2.2)
    return s+T(x2+4,y1+size*0.55,tex=ch,size=size,anchor='start',weight=700)
def rarrow(x1,x2,y,col=INK,w=2.4):
    return (L(x1+2,y,x2-2,y,col,w)+P([(x1+10,y-6),(x1,y),(x1+10,y+6)],col,w,extra='stroke-linecap="round"')
            +P([(x2-10,y-6),(x2,y),(x2-10,y+6)],col,w,extra='stroke-linecap="round"'))
def hbox(x,y,w,h,kind,g=None,extra=''):
    col=FIELD if kind=='s' else EQUI
    cls=f' class="step" data-g="{g}"' if g else ''
    return f'<rect{cls} x="{f(x-w/2)}" y="{f(y-h/2)}" width="{f(w)}" height="{f(h)}" rx="8" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1.5"{(" "+extra) if extra else ""}/>'
def A_(el,x,y,**k):
    d=dict(el=el,x=x,y=y); d.update(k); return d
def hatom(x,y,cloud=34,lab=True,ncol=PLUS):
    s=f'<circle cx="{f(x)}" cy="{f(y)}" r="{cloud}" fill="{MINUS}" fill-opacity=".14" stroke="{MINUS}" stroke-opacity=".35" stroke-width="1.2"/>'
    s+=nuc(x,y,9)
    return s

# ═══ S1 표지
def cover():
    s=['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    y=150
    s.append(an('move',hatom(233,y,58),**{'from':'-80,0','dur':'1.4','delay':'.3','ease':'out'}))
    s.append(an('move',hatom(307,y,58),**{'from':'80,0','dur':'1.4','delay':'.3','ease':'out'}))
    s.append(T(270,y+92,tex='\\ce{H2}',size=26,weight=700))
    # 곡선
    x0,x1,yT,yB=110,470,300,480
    X=lambda r:x0+(r)*(x1-x0)/250; Y=lambda v:yT+(150-v)*(yB-yT)/650
    s.append(A(x0,Y(0)+0,x1+10,Y(0),'muted',1.6)); s.append(A(x0,yB,x0,yT-12,'muted',1.6))
    s.append(T(x1-2,Y(0)-10,mix='핵간 거리',size=19,anchor='end'))
    s.append(T(x0-8,Y(0)+6,tex='0',size=18,anchor='end'))
    pts=[]
    for i in range(0,231):
        r=24+i; v=436*((1-math.exp(-0.0194*(r-74)))**2-1)
        if v<=150: pts.append((X(r),Y(v)))
    s.append(L(X(74),Y(0),X(74),Y(-436),MUTED,1.5,dash='5 4'))
    s.append(an('draw',P(pts,INK,3),dur='1.6',delay='1.2'))
    s.append(f'<circle cx="{f(X(74))}" cy="{f(Y(-436))}" r="6" fill="{EQUI}"/>')
    s.append(T(X(74)+14,Y(-436)+8,tex='74\\ \\text{pm}',size=19,anchor='start'))
    s.append(T(x0+8,yT+8,mix='위치 에너지',size=19,anchor='start'))
    return svg('0 0 540 540',540,'두 수소 원자가 양쪽에서 다가와 전자구름이 겹친 수소 분자가 되고, 아래에 핵간 거리에 따른 위치 에너지 곡선이 74 pm에서 가장 낮다',s,cls='cover-fig',extra='data-audit="skip"')
FIG['COVER']=cover()

# ═══ S2 중단원 도입: 네 가지 결합
def units():
    s=[]
    cx=[110,360,610,860]; cap=['01 공유 결합','02 이온 결합','03 금속 결합','04 전이 금속의 결합']
    # 공유: 물
    g=[]; ox,oy=110,70; a=math.radians(52.25)
    for sg in (-1,1):
        hx,hy=ox+sg*54*math.sin(a),oy+54*math.cos(a)
        g.append(f'<line x1="{ox}" y1="{oy}" x2="{f(hx)}" y2="{f(hy)}" stroke="{BOND}" stroke-width="7" stroke-linecap="round"/>')
    for sg in (-1,1): g.append(f'<g data-atom="{f(ox+sg*54*math.sin(a))},{f(oy+54*math.cos(a))},18,H"></g>')
    g.append(f'<g data-atom="{ox},{oy},24,O"></g>')
    s.append(an('pop',g,o=f'{ox},{oy+20}',dur='.6',delay='.2'))
    # 이온: 격자 조각
    g=[]
    for i in range(4):
        for j in range(3):
            na=(i+j)%2==0; x=300+i*40; y=40+j*40
            g.append(f'<g data-atom="{x},{y},{14 if na else 22},{"Na" if na else "Cl"},-"></g>')
    s.append(an('pop',g,o='360,80',dur='.6',delay='.5'))
    # 금속: 양이온 + 전자 바다
    g=[f'<rect x="540" y="20" width="140" height="120" rx="14" fill="{MINUS}" fill-opacity=".10"/>']
    for i in range(3):
        for j in range(3):
            g.append(f'<g data-chg="{560+i*50},{40+j*40},13,+"></g>')
    for (x,y) in ((585,58),(635,100),(610,30),(560,120),(660,64),(585,130)):
        g.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{MINUS}"/>')
    s.append(an('pop',g,o='610,80',dur='.6',delay='.8'))
    # 착이온
    g=[]
    for k in range(6):
        t=math.radians(60*k+30); x,y=860+52*math.cos(t),80+48*math.sin(t)
        g.append(L(860,80,x,y,BOND,5,extra='stroke-linecap="round"'))
    for k in range(6):
        t=math.radians(60*k+30); x,y=860+52*math.cos(t),80+48*math.sin(t)
        g.append(f'<g data-atom="{f(x)},{f(y)},14,N,-"></g>')
    g.append(f'<g data-atom="860,80,24,Fe,-"></g>')
    s.append(an('pop',g,o='860,80',dur='.6',delay='1.1'))
    for x,c in zip(cx,cap): s.append(T(x if x!=360 else 360,178,mix=c,size=20,weight=700))
    return svg('0 0 980 196',980,'공유 결합(물 분자), 이온 결합(양이온과 음이온이 번갈아 쌓임), 금속 결합(양이온과 자유 전자), 전이 금속의 결합(중심 금속과 둘레 리간드 여섯)',s)
FIG['UNITS']=units()
def one(k,kind='fade'):
    v=re.sub(r'<g data-anim="[^"]*"(?: data-[a-z]+="[^"]*")*>','<g>',FIG[k])
    i=v.index('>')+1; FIG[k]=v[:i]+f'<g data-anim="{kind}" data-dur="1" data-delay=".2">'+v[i:-6]+'</g></svg>'
one('UNITS')

# ═══ S4 플루오린 원자
def fatom():
    s=[lewis([A_('F',60,62,lp=['u','l','d'],rad=['r'],oct=7)],[],S=40,name='Fatom')]
    def box(x,y,o):
        r=f'<rect x="{x}" y="{y}" width="36" height="36" fill="{EQUI if len(o)==1 else "#fff"}" fill-opacity="{".18" if len(o)==1 else "1"}" stroke="{INK}" stroke-width="1.5"/>'
        xs=[x+18] if len(o)==1 else [x+12,x+24]
        for xx,ch in zip(xs,o):
            r+=P([(xx,y+30),(xx,y+6),(xx-6,y+14)] if ch=='u' else [(xx,y+6),(xx,y+30),(xx+6,y+22)],INK,2.4,extra='stroke-linecap="round"')
        return r
    x=150
    s.append(box(x,40,'ud')+T(x+18,100,tex='2s',size=19))
    s.append(box(x+52,40,'ud')+box(x+88,40,'ud')+box(x+124,40,'u')+T(x+106,100,tex='2p',size=19))
    return svg('0 0 320 112',320,'플루오린 원자의 전자점식: 점 일곱 개(쌍 셋과 홀전자 하나), 오른쪽에 2s 짝, 2p 짝 둘과 홀전자 하나',s)
FIG['FATOM']=fatom()

# ═══ S5 H + H → H:H
def h2dot():
    s=[]
    s.append(an('move',lewis([A_('H',50,50,rad=['r'],oct=1)],[],S=40,name='H1'),**{'from':'-30,0','dur':'1','delay':'.2'}))
    s.append(T(130,64,tex='+',size=34))
    s.append(an('move',lewis([A_('H',210,50,rad=['l'],oct=1)],[],S=40,name='H2'),**{'from':'30,0','dur':'1','delay':'.2'}))
    s.append(A(262,50,326,50,'ink',3))
    s.append(lewis([A_('H',380,50),A_('H',452,50)],[(0,1,1,'d')],S=40,name='H2dot'))
    s.append(T(130,112,mix='원자 2개',size=19,fill=MUTED)); s.append(T(416,112,mix='공유 전자쌍 1개',size=19,fill=FIELD))
    s.append(hbox(416,50,30,40,'s'))
    return svg('0 0 500 124',500,'수소 원자 두 개가 전자를 하나씩 내놓아 전자쌍 하나를 공유한 수소 분자가 된다',s)
FIG['H2DOT']=h2dot()

# ═══ S6 F + F → F2
def f2dot():
    s=[]
    s.append(lewis([A_('F',50,70,lp=['u','l','d'],rad=['r'],oct=7)],[],S=36,name='Fa'))
    s.append(T(122,82,tex='+',size=32))
    s.append(lewis([A_('F',194,70,lp=['u','r','d'],rad=['l'],oct=7)],[],S=36,name='Fb'))
    s.append(A(244,70,296,70,'ink',3))
    s.append(lewis([A_('F',350,70,lp=['u','l','d']),A_('F',420,70,lp=['u','r','d'])],[(0,1,1,'d')],S=36,name='F2'))
    s.append(hbox(385,70,26,36,'s',g='f1'))
    s.append(hbox(350,43,38,20,'n',g='f2'))
    s.append(G([T(385,140,mix='공유 전자쌍',size=19,fill=FIELD)],'class="step" data-g="f1"'))
    s.append(G([T(350,20,mix='비공유 전자쌍',size=19,fill=EQUI)],'class="step" data-g="f2"'))
    s.append(T(500,82,mix='또는',size=19,fill=MUTED))
    s.append(lewis([A_('F',570,70,lp=['u','l','d']),A_('F',650,70,lp=['u','r','d'])],[(0,1,1,'l')],S=36,name='F2l'))
    return svg('0 0 700 152',700,'플루오린 원자 둘이 홀전자를 하나씩 내놓아 공유 전자쌍 하나를 이루고, 각 원자에 비공유 전자쌍 셋이 남는다. 결합선으로 쓰면 F–F',s)
FIG['F2DOT']=f2dot()

# ═══ S7 다중 결합
def multi():
    s=[]
    S=36
    s.append(lewis([A_('H',40,60),A_('H',118,60)],[(0,1,1,'l')],S=S,name='H2'))
    s.append(lewis([A_('O',250,60,lp=[135,225]),A_('O',330,60,lp=[45,315])],[(0,1,2,'l')],S=S,name='O2'))
    s.append(lewis([A_('N',470,60,lp=['l']),A_('N',550,60,lp=['r'])],[(0,1,3,'l')],S=S,name='N2'))
    for x,a,b in ((79,'단일 결합','결합 차수 1'),(290,'2중 결합','결합 차수 2'),(510,'3중 결합','결합 차수 3')):
        s.append(T(x,128,mix=a,size=21,weight=700)); s.append(T(x,156,mix=b,size=19,fill=MUTED))
    return svg('0 0 600 170',600,'수소 분자 H–H 단일 결합, 산소 분자 O=O 2중 결합(원자마다 비공유 전자쌍 둘), 질소 분자 N≡N 3중 결합(원자마다 비공유 전자쌍 하나)',s)
FIG['MULTI']=multi()

# ═══ S9 NO2- 그리기 단계
def no2steps():
    s=[]; S=34; y=56
    s.append(G([T(20,y+12,mix='골격',size=19,anchor='start',fill=MUTED),
                lewis([A_('O',130,y,oct=None),A_('N',210,y,oct=None),A_('O',290,y,oct=None)],[(0,1,1,'l'),(1,2,1,'l')],S=S,check=False)],'class="step" data-g="n2"'))
    y2=150
    s.append(G([T(20,y2+12,mix='③④',size=19,anchor='start',fill=MUTED),
                lewis([A_('O',130,y2,oct=None),A_('N',210,y2,oct=None),A_('O',290,y2,oct=None)],[(0,1,2,'l'),(1,2,1,'l')],S=S,check=False)],'class="step" data-g="n3"'))
    y3=250
    st=lewis([A_('O',130,y3,lp=[135,225]),A_('N',210,y3,lp=['u']),A_('O',290,y3,lp=['u','r','d'],fc=-1)],[(0,1,2,'l'),(1,2,1,'l')],S=S,fcshow=False,name='NO2-')
    s.append(G([T(20,y3+12,mix='⑤',size=19,anchor='start',fill=MUTED),st,bracket(88,y3-44,340,y3+44,'-')],'class="step" data-g="n4"'))
    return svg('0 0 380 300',380,'질산 이온의 루이스 구조를 단계별로: O–N–O 골격, O=N–O, 비공유 전자쌍을 채우고 대괄호와 음전하',s)
FIG['NO2STEPS']=no2steps()

def no2(y=60,x0=60,S=34,fc=True,num=None,mirror=False,ch=True,fcshow=True):
    if not mirror:
        at=[A_('O',x0,y,lp=[135,225]),A_('N',x0+80,y,lp=['u']),A_('O',x0+160,y,lp=['u','r','d'],fc=-1)]
        bd=[(0,1,2,'l'),(1,2,1,'l')]
    else:
        at=[A_('O',x0,y,lp=['u','l','d'],fc=-1,fcp='ul'),A_('N',x0+80,y,lp=['u']),A_('O',x0+160,y,lp=[45,315])]
        bd=[(0,1,1,'l'),(1,2,2,'l')]
    s=lewis(at,bd,S=S,name='NO2-',num=num,fcshow=fcshow)
    if ch: s+=bracket(x0-44,y-46,x0+204,y+46,'-')
    return s
# ═══ S10 형식 전하 NO2-
FIG['NO2FC']=svg('0 0 330 130',330,'질산 이온의 루이스 구조 위에 형식 전하 0, 0, −1',[no2(y=72,x0=60,num=['0','0','-1'],fcshow=False)])

# ═══ S11 CO2 두 구조
def co2():
    S=34; s=[]
    s.append(T(20,30,mix='(가)',size=21,anchor='start',weight=700))
    s.append(lewis([A_('O',70,80,lp=[135,225]),A_('C',150,80),A_('O',230,80,lp=[45,315])],[(0,1,2,'l'),(1,2,2,'l')],S=S,name='CO2a'))
    s.append(T(300,30,mix='(나)',size=21,anchor='start',weight=700))
    s.append(lewis([A_('O',350,80,lp=['l'],fc=1),A_('C',430,80),A_('O',510,80,lp=['u','r','d'],fc=-1)],[(0,1,3,'l'),(1,2,1,'l')],S=S,name='CO2b'))
    return svg('0 0 570 130',570,'이산화 탄소의 루이스 구조 두 가지: (가) O=C=O, (나) 형식 전하 +1인 O와 3중 결합한 C, 단일 결합한 O는 −1',s)
FIG['CO2']=co2()

# ═══ S12 NO2- 공명
def no2res():
    s=[]
    s.append(no2(y=60,x0=56))
    s.append(rarrow(286,346,60))
    s.append(no2(y=60,x0=420,mirror=True))
    # 혼성체
    y=190; x0=238
    g=[lewis([A_('O',x0,y,oct=None),A_('N',x0+80,y,lp=['u'],oct=None),A_('O',x0+160,y,oct=None)],[(0,1,1,'p'),(1,2,1,'p')],S=34,check=False),
       bracket(x0-46,y-46,x0+206,y+46,'-'),
       T(x0,y-52,tex='-\\tfrac{1}{2}',size=20,fill=MINUS),T(x0+160,y-52,tex='-\\tfrac{1}{2}',size=20,fill=MINUS),
       T(x0-70,y+8,mix='공명 혼성체',size=20,anchor='end',weight=700)]
    s.append(G([an('fade',g,dur='1',delay='.2')],'class="step" data-g="r1"'))
    return svg('0 0 660 250',650,'질산 이온의 두 공명 구조가 양쪽 화살표로 이어지고, 아래 공명 혼성체는 두 N–O 결합이 모두 실선과 점선이며 두 O가 −1/2씩 띤다',s)
FIG['NO2RES']=no2res()

# ═══ S13 CO3 2- 공명
def co3(x,y,dbl,S=28):
    # 위 O(0), 왼아래 O(1), 오른아래 O(2) / C 가운데
    pos=[(x,y-62),(x-58,y+34),(x+58,y+34)]
    at=[A_('C',x,y)]; bd=[]
    lpd={0:[90,0,180],1:[210,120,300],2:[330,60,240]}
    lpdd={0:[45,135],1:[165,255],2:[15,285]}
    for k,(px,py) in enumerate(pos):
        if k==dbl: at.append(A_('O',px,py,lp=lpdd[k])); bd.append((0,k+1,2,'l'))
        else: at.append(A_('O',px,py,lp=lpd[k],fc=-1)); bd.append((0,k+1,1,'l'))
    return lewis(at,bd,S=S,name='CO3',fcshow=False)
def co3res():
    s=[]; y=110
    xs=[100,360,620]
    for k,x in enumerate(xs):
        s.append(co3(x,y,k,S=26))
        s.append(bracket(x-88,y-104,x+88,y+86,'2-',20))
    s.append(rarrow(218,266,y+10)); s.append(rarrow(478,526,y+10))
    # 혼성체
    x,y2=900,110
    g=[]
    pos=[(x,y2-62),(x-58,y2+34),(x+58,y2+34)]
    at=[A_('C',x,y2)]+[A_('O',px,py) for px,py in pos]
    g.append(lewis(at,[(0,1,1,'p'),(0,2,1,'p'),(0,3,1,'p')],S=26,check=False))
    for px,py in pos: g.append(T(px,py+(-24 if px==x else 46),tex='-\\tfrac{2}{3}',size=19,fill=MINUS))
    g.append(bracket(x-88,y2-104,x+88,y2+86,'2-',20))
    g.append(T(x,236,mix='공명 혼성체',size=20,weight=700))
    s.append(G([an('fade',g,dur='1',delay='.2')],'class="step" data-g="c2"'))
    s.append(T(360,236,mix='공명 구조 3개',size=20,weight=700))
    return svg('0 -8 1030 258',900,'탄산 이온의 공명 구조 세 개(2중 결합 위치만 다름)와 세 C–O 결합이 모두 같은 공명 혼성체, O마다 −2/3',s)
FIG['CO3RES']=co3res()

# ═══ S14 NO, BF3
FIG['NO']=svg('0 0 260 110',260,'일산화 질소의 루이스 구조: N=O, N에 비공유 전자쌍 하나와 홀전자 하나, O에 비공유 전자쌍 둘',
    [lewis([A_('N',90,58,lp=[225],rad=[135],oct=7),A_('O',170,58,lp=[45,315])],[(0,1,2,'l')],S=36,name='NO'),
     G([C(72.5,40.5,12,EQUI,2,fill=EQUI,extra='fill-opacity=".18"')],'class="step" data-g="o1"')])
def bf3(cx=150,cy=118,S=34,nh3=False):
    pos=[(cx,cy-84),(cx-73,cy+42),(cx+73,cy+42)]
    at=[A_('B',cx,cy,oct=6 if not nh3 else 8,fc=0 if not nh3 else -1,fcp='dl')]
    lpd=[[90,0,180],[210,120,300],[330,60,240]]
    for (x,y),l in zip(pos,lpd): at.append(A_('F',x,y,lp=l))
    bd=[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')]
    return at,bd
at,bd=bf3()
FIG['BF3']=svg('0 0 300 220',300,'삼플루오린화 붕소: B에 F 셋이 단일 결합, B 둘레 전자 여섯 개',[lewis(at,bd,S=34,name='BF3')])

# ═══ S15 배위 공유 결합
def coord():
    s=[]
    # BF3 (왼쪽, B at 150,120) 와 NH3 (오른쪽, N)
    S=32
    pos=[(150,40),(80,160),(220,160)]
    at=[A_('B',150,120,oct=6)]
    lpd=[[90,0,180],[210,120,300],[330,60,240]]
    for (x,y),l in zip(pos,lpd): at.append(A_('F',x,y,lp=l))
    s.append(lewis(at,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')],S=S,name='BF3c'))
    s.append(T(150,212,tex='\\ce{BF3}',size=20,fill=MUTED))
    nh=[A_('N',370,120,lp=['l']),A_('H',440,120),A_('H',400,52),A_('H',400,188)]
    g=[lewis(nh,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')],S=S,name='NH3'),hbox(349,120,22,40,'n'),T(430,232,tex='\\ce{NH3}',size=20,fill=MUTED)]
    s.append(an('move',g,**{'from':'40,0','dur':'1.2','delay':'.3','ease':'out'}))
    s.append(A(322,112,198,114,'equi',2.6))
    s.append(T(262,98,mix='전자쌍',size=19,fill=EQUI))
    # 결과
    g=[]
    bx,by=640,120
    at2=[A_('B',bx,by,fc=-1,fcp='u')]
    for a in (120,180,240):
        ux,uy=_dir(a); at2.append(A_('F',bx+ux*76,by+uy*76,lp=[a,a+90,a-90]))
    nx=bx+86; at2.append(A_('N',nx,by,fc=1,fcp='u'))
    for a in (0,60,300):
        ux,uy=_dir(a); at2.append(A_('H',nx+ux*70,by+uy*70))
    bd2=[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(4,5,1,'l'),(4,6,1,'l'),(4,7,1,'l')]
    g.append(lewis(at2,bd2,S=S,name='F3BNH3'))
    g.append(hbox(bx+43,by,50,26,'s'))
    g.append(T(bx+43,by+50,mix='배위 공유 결합',size=19,fill=FIELD,halo=True))
    s.append(A(470,120,520,120,'ink',3))
    s.append(G(g,'class="step" data-g="b1"'))
    return svg('0 0 820 240',820,'암모니아의 질소가 가진 비공유 전자쌍이 삼플루오린화 붕소의 붕소 쪽으로 가서, B–N 배위 공유 결합이 생긴다. 결과물에서 B는 형식 전하 −1, N은 +1',s)
FIG['COORD']=coord()

# ═══ S16 PCl4+, PCl6-, PCl5(g)
def pcl():
    s=[]; S=26; D=68
    def term(ang):
        return [ang,ang+90,ang-90]
    # (a) PCl4+
    cx,cy=125,150
    dirs=[90,0,270,180]
    at=[A_('P',cx,cy,fc=1,fcp='ur')]; bd=[]
    for k,a in enumerate(dirs):
        ux,uy=_dir(a); at.append(A_('Cl',cx+ux*D,cy+uy*D,lp=term(a))); bd.append((0,k+1,1,'l'))
    # 형식 전하는 이온 전하와 겹치므로 그림에서는 대괄호 전하만
    s.append(lewis(at,bd,S=S,name='PCl4+',fcshow=False)+bracket(cx-112,cy-112,cx+112,cy+112,'+',20))
    s.append(T(cx,cy+150,tex='(\\text{a})\\ \\ce{PCl4+}',size=19))
    s.append(T(cx,cy+176,mix='P 둘레 8개',size=19,fill=MUTED))
    # (b) PCl6-
    cx,cy=390,150
    dirs=[90,30,330,270,210,150]
    at=[A_('P',cx,cy,fc=-1,oct=12)]; bd=[]
    for k,a in enumerate(dirs):
        ux,uy=_dir(a); at.append(A_('Cl',cx+ux*D,cy+uy*D,lp=term(a))); bd.append((0,k+1,1,'l'))
    s.append(an('pop',lewis(at,bd,S=S,name='PCl6-',fcshow=False),o=f'{cx},{cy}',dur='.7',delay='.3')+bracket(cx-118,cy-112,cx+118,cy+112,'-',20))
    s.append(T(cx,cy+150,tex='(\\text{b})\\ \\ce{PCl6-}',size=19))
    s.append(T(cx,cy+176,mix='P 둘레 12개',size=19,fill=MUTED))
    # PCl5(g)
    cx,cy=650,150
    dirs=[90,270,180,30,330]
    at=[A_('P',cx,cy,oct=10)]; bd=[]
    for k,a in enumerate(dirs):
        ux,uy=_dir(a); at.append(A_('Cl',cx+ux*D,cy+uy*D,lp=term(a))); bd.append((0,k+1,1,'l'))
    s.append(an('pop',lewis(at,bd,S=S,name='PCl5'),o=f'{cx},{cy}',dur='.7',delay='.6'))
    s.append(T(cx,cy+150,tex='\\ce{PCl5}(g)',size=19))
    s.append(T(cx,cy+176,mix='P 둘레 10개',size=19,fill=MUTED))
    s.append(f'<rect x="4" y="2" width="516" height="338" rx="12" fill="none" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="6 5"/>')
    s.append(T(16,26,tex='\\ce{PCl5}(s)',size=20,fill=MUTED,anchor='start',halo=True))
    return svg('0 0 780 344',780,'고체 오염화 인을 이루는 PCl4 양이온(P 둘레 8개)과 PCl6 음이온(P 둘레 12개), 기체 오염화 인 분자(P 둘레 10개)의 루이스 구조',s)
FIG['PCL']=pcl()

# ═══ S17·S18 B2H6
def b2h6(threec=False,lab=True):
    s=[]
    b1,b2=(170,130),(330,130)
    hb=[(250,62),(250,198)]
    S=30
    if threec:
        for (hx,hy) in hb:
            pts=[]
            for i in range(41):
                t=i/40;
                # 바나나 모양: B1 → H → B2 를 지나는 띠
                x=b1[0]+(b2[0]-b1[0])*t; yc=b1[1]+(hy-b1[1])*4*t*(1-t)
                pts.append((x,yc))
            up=[(x,y-16*math.sin(math.pi*i/40)-6) for i,(x,y) in enumerate(pts)]
            dn=[(x,y+16*math.sin(math.pi*i/40)+6) for i,(x,y) in enumerate(pts)]
            s.append(an('fade',P(up+dn[::-1],BF,1.5,fill=BF,close=True,extra='fill-opacity=".18"'),dur='1',delay='.3'))
    # 다리 결합 (곡선 대신 선 4개)
    for (hx,hy) in hb:
        for (bx,by) in (b1,b2):
            ux,uy=hx-bx,hy-by; n=math.hypot(ux,uy); ux,uy=ux/n,uy/n
            s.append(L(bx+ux*22,by+uy*22,hx-ux*16,hy-uy*16,INK,2.6,extra='stroke-linecap="round"'))
    # 끝 H: 쐐기(앞)·점선 쐐기(뒤)
    def wedge(x1,y1,x2,y2,kind):
        ux,uy=x2-x1,y2-y1; n=math.hypot(ux,uy); ux,uy=ux/n,uy/n; px,py=-uy,ux
        a=(x1+ux*20,y1+uy*20); b=(x2-ux*16,y2-uy*16)
        if kind=='w': return f'<polygon points="{f(a[0])},{f(a[1])} {f(b[0]+px*7)},{f(b[1]+py*7)} {f(b[0]-px*7)},{f(b[1]-py*7)}" fill="{INK}"/>'
        out=''
        for k in range(1,8):
            t=k/7; mx,my=a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t; w=7*t
            out+=L(mx+px*w,my+py*w,mx-px*w,my-py*w,INK,2.2)
        return out
    ends=[((b1),(92,82),'w'),((b1),(92,178),'d'),((b2),(408,82),'w'),((b2),(408,178),'d')]
    for (bx,by),(hx,hy),k in ends: s.append(wedge(bx,by,hx,hy,k))
    for (x,y) in [b1,b2]: s.append(T(x,y+0.36*S,tex='\\mathrm{B}',size=S))
    for (x,y) in hb+[(92,82),(92,178),(408,82),(408,178)]: s.append(T(x,y+0.36*S,tex='\\mathrm{H}',size=S))
    return s
FIG['B2H6']=svg('0 0 500 260',500,'다이보레인: B 원자 두 개가 위아래 다리 H 두 개로 이어지고, 각 B에 끝 H 두 개(하나는 앞쪽 쐐기, 하나는 뒤쪽 점선 쐐기)',b2h6())
def b2h6b():
    s=b2h6(True)
    s.append(T(250,22,mix='3중심 2전자 결합',size=19,fill=BF,halo=True))
    s.append(T(250,254,mix='3중심 2전자 결합',size=19,fill=BF,halo=True))
    return svg('0 0 500 266',500,'다이보레인의 두 다리 결합 B–H–B 영역이 각각 옅은 보라색 띠로 표시되어, 원자 세 개가 전자 두 개를 나누어 가진다',s)
FIG['B2H6B']=b2h6b()

# ═══ S19 접근 단계 카드 (세 그림)
def approach(d,arrows):
    s=[]; y=70; cx=150
    x1,x2=cx-d/2,cx+d/2
    s.append(hatom(x1,y,40)); s.append(hatom(x2,y,40))
    if arrows=='att':
        s.append(A(x1+12,y-6,x2-44,y-6,'field',2.4)); s.append(A(x2-12,y+6,x1+44,y+6,'field',2.4))
        s.append(T(cx,y+70,mix='인력',size=19,fill=FIELD))
    elif arrows=='rep':
        s.append(A(x1-12,y,x1-58,y,'plus',2.6)); s.append(A(x2+12,y,x2+58,y,'plus',2.6))
        s.append(T(cx,y+70,mix='반발',size=19,fill=PLUS))
    else:
        s.append(T(cx,y+70,mix='상호 작용 없음',size=19,fill=MUTED))
    return svg('0 0 300 150',300,{'none':'멀리 떨어진 두 수소 원자','att':'가까워진 두 수소 원자: 원자핵과 상대 원자의 전자 사이 인력','rep':'너무 가까운 두 수소 원자: 원자핵 사이·전자 사이 반발'}[arrows],s)
FIG['APP1']=approach(200,'none'); FIG['APP2']=approach(110,'att'); FIG['APP3']=approach(40,'rep')

# ═══ S20 위치 에너지 곡선
def pecurve():
    s=[]
    x0,x1,yT,yB=96,600,40,380
    X=lambda r:x0+r*(x1-x0)/250; Y=lambda v:yT+(100-v)*(yB-yT)/600
    for v in (0,-100,-200,-300,-400,-500):
        s.append(L(x0-6,Y(v),x0,Y(v),MUTED,1.5)); s.append(T(x0-10,Y(v)+6,tex=str(v) if v else '0',size=18,anchor='end'))
    s.append(L(x0,Y(0),x1,Y(0),MUTED,1.4,dash='6 5'))
    for r in (50,100,150,200):
        s.append(L(X(r),Y(-500),X(r),Y(-500)+6,MUTED,1.5)); s.append(T(X(r),Y(-500)+28,tex=str(r),size=18))
    s.append(A(x0,Y(-500),x1+16,Y(-500),'muted',1.6)); s.append(A(x0,Y(-500),x0,yT-18,'muted',1.6))
    s.append(T(x1+10,Y(-500)+50,mix='핵간 거리 (pm)',size=19,anchor='end'))
    s.append(T(x0+10,yT-6,mix='위치 에너지 (kJ/mol)',size=19,anchor='start'))
    pts=[]
    for i in range(0,600):
        r=26+i*0.4; v=436*((1-math.exp(-0.0194*(r-74)))**2-1)
        if v<=100 and r<=245: pts.append((X(r),Y(v)))
    s.append(L(X(74),Y(-500),X(74),Y(-436),MUTED,1.5,dash='5 4'))
    s.append(L(x0,Y(-436),X(74),Y(-436),MUTED,1.5,dash='5 4'))
    s.append(an('draw',P(pts,INK,3),dur='1.8',delay='.2'))
    s.append(f'<circle cx="{f(X(74))}" cy="{f(Y(-436))}" r="6" fill="{EQUI}"/>')
    s.append(T(x0+6,Y(-436)-8,tex='-436',size=18,anchor='start',fill=EQUI,halo=True))
    s.append(T(X(74),Y(-500)+52,mix='결합 길이 74',size=19,fill=INK))
    # 우물 깊이 치수선
    xd=X(150)
    s.append(A(xd,Y(0)+4,xd,Y(-436)-2,'equi',2)); s.append(A(xd,Y(-436)-2,xd,Y(0)+4,'equi',2))
    s.append(L(X(74)+10,Y(-436),xd+8,Y(-436),MUTED,1.2,dash='3 4'))
    s.append(T(xd+12,Y(-218)+6,tex='436\\ \\text{kJ/mol}',size=20,anchor='start',fill=EQUI,halo=True))
    # 작은 원자 그림
    def pair(r,yy,cl=13):
        xm=X(r)
        d=max(r*0.22,8)
        return (f'<circle cx="{f(xm-d)}" cy="{f(yy)}" r="{cl}" fill="{MINUS}" fill-opacity=".15"/><circle cx="{f(xm+d)}" cy="{f(yy)}" r="{cl}" fill="{MINUS}" fill-opacity=".15"/>'
                f'<circle cx="{f(xm-d)}" cy="{f(yy)}" r="3.5" fill="{PLUS}"/><circle cx="{f(xm+d)}" cy="{f(yy)}" r="3.5" fill="{PLUS}"/>')
    s.append(pair(220,Y(0)-20))
    return svg('0 0 640 440',600,'수소 원자핵 사이 거리에 따른 위치 에너지 곡선: 멀리서는 0이고, 가까워지면 낮아져 74 pm에서 −436 kJ/mol로 가장 낮으며, 더 가까워지면 급히 높아진다',s)
FIG['PECURVE']=pecurve()

# ═══ S21 H2 해리
def h2diss():
    s=[]
    s.append(lewis([A_('H',70,60),A_('H',140,60)],[(0,1,1,'l')],S=36,name='H2d'))
    s.append(A(196,60,276,60,'ink',3))
    s.append(an('move',lewis([A_('H',330,60,rad=['r'],oct=1)],[],S=36,name='Ha'),**{'from':'40,0','dur':'1.2','delay':'.3','ease':'out'}))
    s.append(an('move',lewis([A_('H',450,60,rad=['l'],oct=1)],[],S=36,name='Hb'),**{'from':'-40,0','dur':'1.2','delay':'.3','ease':'out'}))
    s.append(A(236,124,236,84,'equi',3))
    s.append(T(236,146,mix='열 흡수',size=19,fill=EQUI))
    return svg('0 0 500 160',500,'수소 분자가 열을 흡수하여 수소 원자 두 개로 떨어진다',s)
FIG['H2DISS']=h2diss()

# ═══ S22 CH4 단계 막대
def ch4bars():
    s=[]; vals=[435,453,425,339]; labs=['\\ce{CH4}','\\ce{CH3}','\\ce{CH2}','\\ce{CH}']
    x0,yB=60,260; sc=0.42
    s.append(L(x0-10,yB,x0+4*110,yB,MUTED,1.5))
    for k,v in enumerate(vals):
        x=x0+k*110; h=v*sc
        bar=f'<rect x="{x+10}" y="{f(yB-h)}" width="70" height="{f(h)}" fill="{INK}" fill-opacity=".82"/>'
        s.append(an('scale',bar,**{'from':'1,0','o':f'{x+45},{yB}','dur':'.8','delay':f'{.2+.3*k:.1f}'}))
        s.append(T(x+45,yB-h-10,tex=str(v),size=19))
        s.append(T(x+45,yB+28,tex=labs[k],size=19))
    ya=yB-413*sc
    s.append(L(x0-4,ya,x0+4*110-6,ya,PLUS,2,dash='7 5'))
    s.append(T(x0+4*110-4,ya-10,tex='413',size=19,anchor='end',fill=PLUS,halo=True))
    s.append(T(x0-10,24,mix='$\\Delta H_\\mathrm{B}$ (kJ/mol)',size=19,anchor='start'))
    s.append(T(x0+220,yB+56,mix='떼어 내는 분자',size=19,fill=MUTED))
    return svg('0 0 520 330',470,'메테인에서 수소 원자를 하나씩 떼어 낼 때의 결합 엔탈피 435, 453, 425, 339 kJ/mol 막대와 평균 413 kJ/mol 점선',s)
FIG['CH4BARS']=ch4bars()

# ═══ S24 결합 차수 막대
def bondbars():
    s=[]
    data=[('C-C',347,154),('C=C',614,134),('C#C',839,121),('N-N',160,146),('N=N',418,122),('N#N',945,110),('C-O',358,143),('C=O',745,123),('C#O',1070,113)]
    x0=40; yB=236; sc=0.185; w=40; dx=66; bars=[]
    s.append(L(x0-14,yB,x0+9*dx,yB,MUTED,1.5))
    for k,(nm,e,l) in enumerate(data):
        x=x0+k*dx
        h=e*sc
        bars.append(f'<rect x="{x}" y="{f(yB-h)}" width="{w}" height="{f(h)}" fill="{INK}" fill-opacity=".82"/>')
        s.append(T(x+w/2,yB-h-8,tex=str(e),size=18))
        s.append(T(x+w/2,yB+28,tex='\\ce{'+nm+'}',size=19))
        s.append(T(x+w/2,yB+56,tex=str(l),size=18,fill=MUTED))
    s.insert(1,an('scale',bars,**{'from':'1,0','o':f'320,{yB}','dur':'1','delay':'.2'}))
    for k in (1,2):
        xs=x0+k*3*dx-13; s.append(L(xs,24,xs,yB+62,'#C9D3DD',1.5,dash='4 4'))
    s.append(T(x0+9*dx-10,yB+84,mix='막대·검은 숫자: 결합 에너지 (kJ/mol)  ·  회색 숫자: 결합 길이 (pm)',size=18,anchor='end',fill=MUTED))
    return svg('0 0 640 336',640,'결합 에너지 막대: C–C 347, C=C 614, C≡C 839, N–N 160, N=N 418, N≡N 945, C–O 358, C=O 745, C≡O 1070 kJ/mol, 아래 결합 길이 154, 134, 121, 146, 122, 110, 143, 123, 113 pm',s)
FIG['BONDBARS']=bondbars()

# ═══ S25 Cl2, HCl 공명 혼성
def ionres(el1,el2,y,S=30):
    s=[]
    c1=lewis([A_(el1,60 if el1=='Cl' else 50,y,lp=([] if el1=='H' else ['u','l','d'])),A_(el2,130,y,lp=['u','r','d'])],[(0,1,1,'l')],S=S,name='cov')
    s.append(c1)
    s.append(rarrow(186,236,y))
    # 이온성 1: el1(-) el2(+)
    if el1=='Cl':
        a=lewis([A_('Cl',300,y,lp=['u','l','d','r'],fc=-1),A_('Cl',380,y,lp=['u','r','d'],oct=6,fc=1)],[],S=S,name='ion1')
        b=lewis([A_('Cl',530,y,lp=['u','l','d'],oct=6,fc=1),A_('Cl',610,y,lp=['u','r','d','l'],fc=-1)],[],S=S,name='ion2')
    else:
        a=lewis([A_('H',300,y,lp=['r'],fc=-1),A_('Cl',380,y,lp=['u','r','d'],oct=6,fc=1)],[],S=S,name='ion1h')
        b=lewis([A_('H',530,y,oct=0,fc=1),A_('Cl',610,y,lp=['u','r','d','l'],fc=-1)],[],S=S,name='ion2h')
    s.append(a); s.append(rarrow(446,496,y)); s.append(b)
    return ''.join(s)
FIG['CL2RES']=svg('0 0 680 90',680,'염소 분자의 공명 혼성: 공유 구조 Cl–Cl과 두 이온성 구조(왼쪽이 −, 오른쪽이 + / 왼쪽이 +, 오른쪽이 −)',[ionres('Cl','Cl',48)])
FIG['HCLRES']=svg('0 0 680 90',680,'염화 수소의 공명 혼성: 공유 구조 H–Cl, 이온성 구조 H 음이온·Cl 양이온, 이온성 구조 H 양이온·Cl 음이온',[ionres('H','Cl',48)])

# ═══ S26 HCl 전자 밀도
def hclcloud():
    s=[]
    hx,cx,y=150,290,110
    s.append(f'<ellipse cx="225" cy="{y}" rx="170" ry="70" fill="#fff" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    s.append(an('move',[f'<ellipse cx="262" cy="{y}" rx="118" ry="60" fill="{MINUS}" fill-opacity=".16"/>',f'<ellipse cx="300" cy="{y}" rx="66" ry="44" fill="{MINUS}" fill-opacity=".16"/>'],**{'from':'-40,0','dur':'1.4','delay':'.3','ease':'out'}))
    s.append(L(hx+18,y,cx-29,y,BOND,7,extra='stroke-linecap="round"'))
    s.append(f'<g data-atom="{hx},{y},18,H"></g><g data-atom="{cx},{y},29,Cl"></g>')
    s.append(T(hx,y-44,tex='\\delta^+',size=26,fill=PLUS,weight=700))
    s.append(T(cx,y-64,tex='\\delta^-',size=26,fill=MINUS,weight=700,halo=True))
    s.append(T(hx-10,y+96,mix='전자 밀도 낮음',size=19,fill=MUTED))
    s.append(T(cx+20,y+96,mix='전자 밀도 높음',size=19,fill=MINUS))
    return svg('0 0 430 220',430,'염화 수소 분자: 전자 구름이 염소 쪽으로 치우쳐 수소는 부분 양전하, 염소는 부분 음전하를 띤다',s)
FIG['HCLCLOUD']=hclcloud()

# ═══ S28 전기음성도 주기율표 (교과서 그림 Ⅰ-18 값)
EN=[[('H',2.20)]+[None]*16,
    [('Li',.98),('Be',1.57)]+[None]*10+[('B',2.04),('C',2.55),('N',3.04),('O',3.44),('F',3.98)],
    [('Na',.93),('Mg',1.31)]+[None]*10+[('Al',1.61),('Si',1.90),('P',2.19),('S',2.58),('Cl',3.16)],
    [('K',.82),('Ca',1.00),('Sc',1.36),('Ti',1.54),('V',1.63),('Cr',1.66),('Mn',1.55),('Fe',1.90),('Co',1.88),('Ni',1.91),('Cu',1.95),('Zn',1.65),('Ga',1.81),('Ge',2.01),('As',2.18),('Se',2.55),('Br',2.96)],
    [('Rb',.82),('Sr',.95),('Y',1.22),('Zr',1.33),('Nb',1.60),('Mo',2.24),('Tc',1.90),('Ru',2.20),('Rh',2.28),('Pd',2.20),('Ag',1.93),('Cd',1.69),('In',1.78),('Sn',1.88),('Sb',2.05),('Te',2.10),('I',2.66)],
    [('Cs',.79),('Ba',.89),('Lu',1.27),('Hf',1.30),('Ta',1.50),('W',2.36),('Re',1.90),('Os',2.20),('Ir',2.20),('Pt',2.28),('Au',2.54),('Hg',2.00),('Tl',1.83),('Pb',2.10),('Bi',2.02),('Po',2.00),('At',2.20)]]
def encol(v):
    return '#F4F6F8' if v<1.5 else '#E6EBF0' if v<2.0 else '#FFF1B8' if v<2.5 else '#FFD98A' if v<3.0 else '#FFB866'
def entable():
    s=[]; w,h=58,52; x0,y0=40,72
    for gi in range(17): s.append(T(x0+gi*w+w/2,y0-12,tex=str(gi+1),size=18,fill=MUTED))
    for pi,row in enumerate(EN):
        cells=[]
        for gi,c in enumerate(row):
            if not c: continue
            el,v=c; x=x0+gi*w; y=y0+pi*h
            cells.append(f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="4" fill="{encol(v)}" stroke="#C9D3DD" stroke-width="1"/>')
            cells.append(T(x+w/2,y+21,tex='\\mathrm{'+el+'}',size=20))
            cells.append(T(x+w/2,y+46,tex=f'{v:.2f}',size=18,fill=INK))
        s.extend(cells)
        s.append(T(x0-12,y0+pi*h+31,tex=str(pi+1),size=18,anchor='end',fill=MUTED))
    # 경향 화살표 (표 바깥)
    xe=x0+17*w
    s.append(A(x0+3*w,y0-50,x0+10*w,y0-50,'ink',3)); s.append(T(x0+10*w+10,y0-43,mix='전기음성도 증가',size=19,anchor='start'))
    s.append(A(xe+30,y0+6*h,xe+30,y0+40,'ink',3)); s.append(T(xe+30,y0+6*h+28,mix='증가',size=19))
    # 범례
    ly=y0+6*h+24
    for k,(a,b,lab) in enumerate([(0,1.5,'< 1.5'),(1.5,2,'1.5–2.0'),(2,2.5,'2.0–2.5'),(2.5,3,'2.5–3.0'),(3,4,'≥ 3.0')]):
        x=x0+k*130
        s.append(f'<rect x="{x}" y="{ly}" width="26" height="22" rx="3" fill="{encol(a+0.01)}" stroke="#C9D3DD"/>')
        s.append(T(x+34,ly+18,mix=lab,size=18,anchor='start'))
    s.append(T(x0+17*w,ly+18,mix='족 번호 위, 주기 번호 왼쪽 · 18족 제외',size=18,anchor='end',fill=MUTED))
    return svg(f'0 0 {x0+17*w+70} {ly+34}',1060,'주기율표 1–6주기(18족 제외)의 전기음성도 값. H 2.20, F 3.98이 가장 크고 Cs 0.79가 가장 작으며, 오른쪽과 위쪽으로 갈수록 커진다',s)
FIG['ENTABLE']=entable(); one('ENTABLE')

# ═══ S29 HF 쌍극자
def hfdip():
    s=[]; hx,fx,y=120,280,120
    s.append(L(hx+18,y,fx-24,y,BOND,7,extra='stroke-linecap="round"'))
    s.append(f'<g data-atom="{hx},{y},18,H"></g><g data-atom="{fx},{y},24,F"></g>')
    s.append(T(hx,y-36,tex='+\\delta',size=24,fill=PLUS,weight=700))
    s.append(T(fx,y-42,tex='-\\delta',size=24,fill=MINUS,weight=700))
    ya=y+56
    s.append(A(hx,ya,fx,ya,'ink',3)); L1=fx-hx; tx=hx+0.15*L1
    s.append(L(tx,ya-8,tx,ya+8,INK,3))
    s.append(T((hx+fx)/2,ya+30,tex='\\mu',size=22))
    # R 치수선
    yr=y-86
    s.append(A((hx+fx)/2,yr,hx,yr,'muted',1.6)); s.append(A((hx+fx)/2,yr,fx,yr,'muted',1.6))
    s.append(L(hx,yr-8,hx,y-24,MUTED,1.2,dash='3 3')); s.append(L(fx,yr-8,fx,y-30,MUTED,1.2,dash='3 3'))
    s.append(T((hx+fx)/2,yr-10,tex='R=0.917\\ \\text{Å}',size=20,halo=True))
    return svg('0 0 400 220',400,'플루오린화 수소: H는 +δ, F는 −δ, 쌍극자 모멘트 화살표가 H에서 F 쪽을 향하고 꼬리에 + 막대, 두 원자핵 사이 거리 R = 0.917 Å',s)
FIG['HFDIP']=hfdip()

# ═══ S32 OCN-
def ocn():
    s=[]; S=30; xs=[60,330,600]; y=70
    specs=[('가',[A_('O',0,0,lp=[135,225]),A_('C',74,0),A_('N',148,0,lp=[45,315],fc=-1)],[(0,1,2,'l'),(1,2,2,'l')]),
           ('나',[A_('O',0,0,lp=['u','l','d'],fc=-1,fcp='ul'),A_('C',74,0),A_('N',148,0,lp=['r'])],[(0,1,1,'l'),(1,2,3,'l')]),
           ('다',[A_('O',0,0,lp=['l'],fc=1,fcp='ul'),A_('C',74,0),A_('N',148,0,lp=['u','r','d'],fc=-2)],[(0,1,3,'l'),(1,2,1,'l')])]
    for (nm,at,bd),x in zip(specs,xs):
        for a in at: a['x']+=x; a['y']+=y
        s.append(T(x-40,22,mix=f'({nm})',size=20,anchor='start',weight=700))
        s.append(lewis(at,bd,S=S,name='OCN'+nm,fcshow=False))
        s.append(bracket(x-38,y-40,x+186,y+40,'-',20))
    return svg('0 0 840 130',840,'시안산 이온의 세 구조: (가) O=C=N, (나) O–C≡N, (다) O≡C–N, 각각 대괄호와 음전하',s)
FIG['OCN']=ocn()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='))
