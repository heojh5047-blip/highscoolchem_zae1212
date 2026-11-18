# -*- coding: utf-8 -*-
"""고급화학 1-4-2 그림 생성: gen_head.py(OUT=이 덱, 1-2-1 lewis 도우미 + 축약 원자단 grp) + lib131.py·chem.py·base141.py(1-4-1 사본)
   → tpl.html의 {{KEY}}를 바꿔 slides.html (실험실 없음 — labs.js 만들지 않음)"""
import math, re, sys, os
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/1-4-2_탄화수소_유도체와_방향족_화합물의_구조/slides.html')
exec(open(os.path.join(HERE,'lib131.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,'chem.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,'base141.py'),encoding='utf-8').read())
VAL['Br']=7; VAL['N']=5
CW.update({'R':.72,"'":.22,'(':.34,')':.34,'-':.5})
OXC='#C2410C'; RDC='#0E7490'
def popa(x,y,d,dur='.6'): return {'o':f'{f(x)},{f(y)}','dur':dur,'delay':f'{d:.1f}'}
def POP(body,x,y,d=0.2): return an('pop',body,**popa(x,y,d))

# ── 원자 수 검산
def fcount(atoms):
    c=Counter()
    for a in atoms:
        if a.get('grp'):
            for el,n in re.findall(r'([A-Z][a-z]?)(\d*)',a['grp']): c[el]+=int(n or 1)
        else: c[a['el']]+=1
    return c
def fstr(c): return ''.join(f'{e}{c[e] if c[e]>1 else ""}' for e in sorted(c,key=lambda e:('CHBrClNO'.find(e) if e in 'CHNO' else 9,e)) if c[e])
def chk(c,want,name):
    w=Counter({el:int(n or 1) for el,n in re.findall(r'([A-Z][a-z]?)(\d*)',want)})
    if +c!=+w: sys.exit(f'[{name}] 원자 수 {dict(c)} ≠ {want}')
def M(atoms,bonds,want,S=24,name='',show=True,**k):
    """lewis 그리기 + 분자식 assert. show=False면 비공유 전자쌍 숨김"""
    if want: chk(fcount(atoms),want,name)
    return lewis(atoms,bonds,S=S,name=name,showlp=show,**k)
def G_(t,x,y,**k): d=dict(el='C',x=x,y=y,grp=t); d.update(k); return d
def O_(x,y,lp,**k): return A_('O',x,y,lp=lp,**k)
def N_(x,y,lp,**k): return A_('N',x,y,lp=lp,**k)
def hlrect(x,y,w,h): return f'<rect x="{f(x-w/2)}" y="{f(y-h/2)}" width="{f(w)}" height="{f(h)}" rx="7" fill="{HL}" fill-opacity=".45"/>'
def dlab(x,y,sign,size=20):
    return T(x,y,tex='\\delta^{'+('+' if sign>0 else '-')+'}',size=size,fill=PLUS if sign>0 else MINUS,weight=700)
def dipole(x1,y,x2,col='plus',w=3):
    """쌍극자 화살표(δ+ → δ−) + 꼬리 막대"""
    L0=x2-x1; xt=x1+0.15*L0
    return A(x1,y,x2,y,col,w)+L(xt,y-7,xt,y+7,PLUS,w)

# ── 벤젠 고리 선 구조: 꼭짓점 k=0 위, 시계 방향. subs={k:(tex,hl)} 치환기
def bverts(cx,cy,R): return [(cx+R*math.cos(math.radians(90-60*k)),cy-R*math.sin(math.radians(90-60*k))) for k in range(6)]
def benz(cx,cy,R,kek=0,hybrid=False,subs=None,size=22,slen=None,w=2.6,dash_circle=False):
    subs=subs or {}; V=bverts(cx,cy,R); s=[]; slen=slen or R*.62
    for k in range(6):
        a,b=V[k],V[(k+1)%6]; s.append(L(*a,*b,INK,w,extra='stroke-linecap="round"'))
        if not hybrid and (k%2==kek%2):
            mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2; ix,iy=cx-mx,cy-my; n=math.hypot(ix,iy); ix,iy=ix/n,iy/n
            o=0.17*R; t=.2
            p1=(a[0]+(b[0]-a[0])*t+ix*o,a[1]+(b[1]-a[1])*t+iy*o); p2=(a[0]+(b[0]-a[0])*(1-t)+ix*o,a[1]+(b[1]-a[1])*(1-t)+iy*o)
            s.append(L(*p1,*p2,INK,w,extra='stroke-linecap="round"'))
    if hybrid: s.append(C(cx,cy,R*.56,INK,w,dash='7 5' if dash_circle else None))
    for k,(tex,hl) in subs.items():
        ang=math.radians(90-60*k); ux,uy=math.cos(ang),-math.sin(ang)
        x1,y1=V[k]; x2,y2=x1+ux*slen,y1+uy*slen; s.append(L(x1,y1,x2,y2,INK,w,extra='stroke-linecap="round"'))
        wd=gw(tex,size); gap=size*.32
        if abs(ux)<.3: lx,ly,anc=x2,(y2-gap-size*.1 if uy<0 else y2+gap+size*.8),'middle'; bx=lx
        elif ux>0: lx,ly,anc=x2+gap*.6,y2+size*.36,'start'; bx=lx+wd/2
        else: lx,ly,anc=x2-gap*.6,y2+size*.36,'end'; bx=lx-wd/2
        if hl: s.append(hlrect(bx,ly-size*.36,wd+10,size*1.2))
        s.append(T(lx,ly,tex='\\ce{'+tex+'}',size=size,anchor=anc))
    c=Counter({'C':6,'H':6-len(subs)})
    for tex,_ in subs.values():
        for el,n in re.findall(r'([A-Z][a-z]?)(\d*)',tex): c[el]+=int(n or 1)
    return ''.join(s),c
def benzL(cx,cy,R=56,kek=0,S=24,HR=None,name='벤젠'):
    """벤젠 전개 구조식(lewis, 전자 수 검산)"""
    V=bverts(cx,cy,R); HR=HR or R*1.78; at=[]; bd=[]
    for k,(x,y) in enumerate(V): at.append(Cc(x,y))
    for k in range(6):
        ang=math.radians(90-60*k); at.append(H_(cx+HR*math.cos(ang),cy-HR*math.sin(ang)))
        bd.append((k,(k+1)%6,2 if k%2==kek%2 else 1,'l')); bd.append((k,6+k,1,'l'))
    chk(fcount(at),'C6H6',name)
    return lewis(at,bd,S=S,name=name)

# ═══ S1 표지
def cover():
    s=[]; cx,cy=270,250
    s.append(benzL(cx,cy,R=74,S=28,HR=132,name='표지 벤젠'))
    s.append(an('fade',C(cx,cy,42,FIELD,2.6,fill=MINUS,dash='7 5',extra='fill-opacity=".10"'),dur='1.2',delay='.5'))
    chips=[(150,110,'–OH'),(392,110,'–COOH'),(150,398,'–NH_2'),(392,398,'C=O')]
    for i,(x,y,t) in enumerate(chips):
        g=hlrect(x,y-8,104,40)+T(x,y+4,tex='\\mathrm{'+t.replace('–','-')+'}',size=26)
        s.append(POP(g,x,y,.8+.25*i))
    s.append(T(cx,446,tex='\\ce{C6H6}',size=28,weight=700)); s.append(T(cx,476,mix='벤젠',size=21,fill=MUTED))
    return svg('0 0 540 530',520,'벤젠의 전개 구조식과 고리 위로 퍼진 π 전자, 둘레에 여러 작용기',s,cls='cover-fig')
FIG['COVER']=cover()

# ═══ S3 생각 열기: 에탄올 vs 다이메틸 에테르
def openfig():
    s=[]; S=24; y1=86; y2=236; d=62
    xs=[40,40+d,40+2*d,40+3*d,40+4*d]
    a=[H_(xs[0],y1),Cc(xs[1],y1),Cc(xs[2],y1),O_(xs[3],y1,['u','d']),H_(xs[4],y1),H_(xs[1],y1-52),H_(xs[1],y1+52),H_(xs[2],y1-52),H_(xs[2],y1+52)]
    b=[(0,1,1,'l'),(1,2,1,'l'),(2,3,1,'l'),(3,4,1,'l'),(1,5,1,'l'),(1,6,1,'l'),(2,7,1,'l'),(2,8,1,'l')]
    g=hlrect((xs[3]+xs[4])/2,y1-6,96,50)+M(a,b,'C2H6O',S=S,name='에탄올')
    g+=T(400,y1-6,mix='에탄올',size=22,anchor='start',weight=700)+T(400,y1+26,mix='끓는점 78 °C',size=21,anchor='start',fill=PLUS)
    s.append(POP(g,180,y1,.2))
    a=[H_(xs[0],y2),Cc(xs[1],y2),O_(xs[2],y2,['u','d']),Cc(xs[3],y2),H_(xs[4],y2),H_(xs[1],y2-52),H_(xs[1],y2+52),H_(xs[3],y2-52),H_(xs[3],y2+52)]
    b=[(0,1,1,'l'),(1,2,1,'l'),(2,3,1,'l'),(3,4,1,'l'),(1,5,1,'l'),(1,6,1,'l'),(3,7,1,'l'),(3,8,1,'l')]
    g=hlrect(xs[2],y2-6,52,50)+M(a,b,'C2H6O',S=S,name='다이메틸 에테르')
    g+=T(400,y2-6,mix='다이메틸 에테르',size=22,anchor='start',weight=700)+T(400,y2+26,mix='끓는점 −24 °C',size=21,anchor='start',fill=MINUS)
    s.append(POP(g,180,y2,.7))
    return svg('0 0 580 316',560,'분자식이 C2H6O로 같은 에탄올과 다이메틸 에테르의 구조식과 끓는점',s)
FIG['OPEN']=openfig()

# ═══ S4 탄화수소 유도체
def deriv():
    s=[]; size=26
    s.append(T(150,133,tex='\\ce{CH3CH3}',size=30,weight=700)); s.append(T(150,172,mix='에테인(무극성)',size=20,fill=MUTED))
    items=[('Cl','클로로에테인','할로젠기'),('OH','에탄올','하이드록시기'),('NH2','에틸아민','아미노기')]
    for i,(grp,nm,gn) in enumerate(items):
        y=52+i*82
        g=[A(250,125,440,y-8,'ink',2.6)]
        groups=['CH3','CH2',grp]; ws=[gw(t,size) for t in groups]; W=sum(ws); x0=600-W/2
        cx=[x0+sum(ws[:j])+ws[j]/2 for j in range(3)]
        g.append(hlrect(cx[2],y-8,ws[2]+12,size*1.25))
        g.append(T(600,y,tex='\\ce{CH3CH2'+grp+'}',size=size))
        g.append(dlab(cx[1],y-30,1,19)); g.append(dlab(cx[2],y-30,-1,19))
        g.append(T(720,y,mix=nm,size=21,anchor='start'))
        g.append(T(880,y,mix=gn,size=19,anchor='start',fill=MUTED))
        s.append(an('pop',''.join(g),**popa(600,y,.3+.35*i)))
    return svg('0 0 1000 250',960,'에테인의 수소 하나가 할로젠기, 하이드록시기, 아미노기로 치환된 탄화수소 유도체와 부분 전하',s)
FIG['DERIV']=deriv()

# ═══ S5 그림 Ⅰ-49 할로젠화 알킬
def rx():
    s=[]; cx,cy=170,118; xx=310
    s.append(L(cx,cy,cx-58,cy-44,INK,2.6)); s.append(wedge(cx,cy,cx-66,cy+30,13)); s.append(hashw(cx,cy,cx-28,cy+62,13))
    s.append(L(cx+18,cy-8,xx-20,cy-8,INK,2.8))
    s.append(T(cx,cy,tex='\\mathrm{C}',size=30)); s.append(T(xx,cy,tex='\\mathrm{X}',size=30))
    s.append(dlab(cx+2,cy-44,1,24)); s.append(dlab(xx,cy-44,-1,24))
    s.append(an('draw',dipole(cx+4,cy+34,xx+2),dur='.8',delay='.4'))
    s.append(T(240,cy+82,tex='\\mathrm{X = F,\\ Cl,\\ Br,\\ I}',size=22))
    s.append('<defs><linearGradient id="grad-ac142-05" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#D7263D" stop-opacity=".55"/><stop offset=".5" stop-color="#F4E9F0" stop-opacity=".5"/><stop offset="1" stop-color="#1F6FD1" stop-opacity=".6"/></linearGradient></defs>')
    s.append(f'<ellipse cx="240" cy="266" rx="170" ry="30" fill="url(#grad-ac142-05)" stroke="{MUTED}" stroke-width="1.2"/>')
    s.append(T(240,273,mix='전자 밀도: 작음 ← C — X → 큼',size=19,halo=True))
    return svg('0 0 480 310',440,'할로젠화 알킬의 탄소는 부분적 양전하, 할로젠은 부분적 음전하를 띤다. 쌍극자 화살표와 전자 밀도',s)
FIG['RX']=rx()

# ═══ S6 친핵성 치환 반응
def sn2():
    s=[]; S=26; y=112
    a=[H_(36,y),O_(92,y,['u','d','r'],fc=-1,fcp='ul')]
    s.append(M(a,[(0,1,1,'l')],'HO',S=S,name='OH-'))
    s.append(T(160,y+9,tex='+',size=26))
    cx=290; a=[Cc(cx,y),H_(cx-58,y),H_(cx,y-58),H_(cx,y+58),A_('Br',cx+80,y,lp=['u','d','r'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],'CH3Br',S=S,name='브로모메테인'))
    s.append(an('draw',curved(118,y-6,cx-20,y-16,bend=-46),dur='.7',delay='.4'))
    s.append(an('draw',curved(cx+40,y-8,cx+74,y-26,bend=-18),dur='.6',delay='1.0'))
    s.append(T(132,y-50,mix='친핵체',size=19,fill=MINUS)); s.append(T(cx+4,y+104,mix='브로모메테인',size=19,fill=MUTED))
    s.append(harrow(440,520,y-4))
    ox=636; a=[H_(ox-56,y),O_(ox,y,['u','d']),Cc(ox+70,y),H_(ox+70,y-58),H_(ox+70,y+58),H_(ox+128,y)]
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l'),(2,3,1,'l'),(2,4,1,'l'),(2,5,1,'l')],'CH4O',S=S,name='메탄올'))
    s.append(T(ox+40,y+104,mix='메탄올',size=19,fill=MUTED))
    s.append(T(818,y+9,tex='+',size=26))
    a=[A_('Br',900,y,lp=['u','d','l','r'],fc=-1,fcp='ur')]
    s.append(M(a,[],'Br',S=S,name='Br-'))
    return svg('0 0 1000 230',960,'수산화 이온이 브로모메테인의 탄소를 공격하여 메탄올과 브로민화 이온이 생기는 친핵성 치환 반응. 굽은 화살표는 전자쌍의 이동',s)
FIG['SN']=sn2()

# ═══ S7 제거 반응
def e2():
    s=[]; S=25; y=150; c1=230; c2=314
    a=[H_(64,46),O_(116,46,['u','l','d'],fc=-1,fcp='ul')]
    s.append(M(a,[(0,1,1,'l')],'HO',S=S,name='OH- 제거'))
    a=[Cc(c1,y),Cc(c2,y),H_(c1-58,y),H_(c1,y-58),H_(c1,y+58),G_('CH3',c2,y-60),H_(c2+60,y),A_('Br',c2,y+66,lp=['l','r','d'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(1,5,1,'l'),(1,6,1,'l'),(1,7,1,'l')],'C3H7Br',S=S,name='2-브로모프로페인'))
    s.append(an('draw',curved(140,46,c1-14,y-62,bend=-26),dur='.6',delay='.3'))
    s.append(an('draw',curved(c1+8,y-30,c1+44,y-10,bend=-16),dur='.6',delay='.8'))
    s.append(an('draw',curved(c2+10,y+30,c2+26,y+54,bend=-14),dur='.6',delay='1.3'))
    s.append(T(150,22,mix='친핵체',size=19,fill=MINUS,anchor='start'))
    s.append(T(c1+40,y+136,mix='2-브로모프로페인',size=19,fill=MUTED))
    s.append(harrow(430,510,y-4))
    p1=600; p2=680
    a=[Cc(p1,y),Cc(p2,y),H_(p1-50,y-42),H_(p1-50,y+42),G_('CH3',p2+56,y-46),H_(p2+50,y+42)]
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],'C3H6',S=S,name='프로펜'))
    s.append(T(p1+40,y+90,mix='프로펜',size=19,fill=MUTED))
    s.append(T(784,y+9,tex='+',size=26))
    s.append(M([A_('Br',838,y,lp=['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='Br- 제거'))
    s.append(T(902,y+9,tex='+',size=26))
    a=[O_(960,y-10,[120,60]),H_(930,y+30),H_(990,y+30)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l')],'H2O',S=S,name='물 제거'))
    return svg('0 0 1020 300',930,'수산화 이온이 2-브로모프로페인의 수소를 떼어 내어 프로펜, 브로민화 이온, 물이 생기는 제거 반응. 굽은 화살표 3개',s)
FIG['E2']=e2()

# ═══ S8 표 Ⅰ-8 카보닐 화합물
def carb(kind,gen):
    """kind: ald, ket, acid, ester / gen: True 일반 분자식"""
    S=21; y=74; s=[]; cx=None
    R1,R2=('R',"R'") if gen else ('CH3','CH3')
    xR=50 if gen else 54
    at=[G_(R1,xR,y)]; xC=xR+64 if gen else xR+70
    at+= [Cc(xC,y),O_(xC,y-48,['ul','ur'] if False else [150,30])]; bd=[(0,1,1,'l'),(1,2,2,'l')]
    if kind=='ald': at.append(H_(xC+60,y)); bd.append((1,3,1,'l')); want=None if gen else 'C2H4O'
    elif kind=='ket': at.append(G_(R2,xC+(60 if gen else 68),y)); bd.append((1,3,1,'l')); want=None if gen else 'C3H6O'
    elif kind=='acid': at+= [O_(xC+60,y,['u','d']),H_(xC+116,y)]; bd+= [(1,3,1,'l'),(3,4,1,'l')]; want=None if gen else 'C2H4O2'
    else:
        R3=R2 if gen else 'CH2CH3'
        at+= [O_(xC+60,y,['u','d']),G_(R3,xC+(118 if gen else 150),y)]; bd+= [(1,3,1,'l'),(3,4,1,'l')]; want=None if gen else 'C4H8O2'
    s.append(hlrect(xC,y-30,34,92))
    s.append(M(at,bd,want,S=S,name=kind+str(gen),show=False))
    W=max(a['x']+gw(a.get('grp') or a['el'],S)/2 for a in at)+16
    return svg(f'0 0 {f(W)} 96',W*0.92,('일반 분자식' if gen else '구조식')+' '+kind,s,cls='fig ac142-cell')
for k in ('ald','ket','acid','ester'):
    FIG['CG_'+k]=carb(k,True); FIG['CS_'+k]=carb(k,False)

# ═══ S9 카보닐기의 극성
def copol():
    s=[]; S=30; y=150; xc=190; xo=316
    a=[Cc(xc,y),O_(xo,y,[45,-45]),G_('R',xc-60,y-50),G_("R'",xc-60,y+50)]
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l')],None,S=S,name='카보닐'))
    s.append(dlab(xc+4,y-38,1,24)); s.append(dlab(xo,y-50,-1,24))
    s.append(an('draw',dipole(xc+4,y+44,xo+4),dur='.8',delay='.3'))
    g=T(xc+10,y+124,tex='\\mathrm{Nu}^{-}',size=26,fill=MINUS)+A(xc+8,y+98,xc+4,y+64,'minus',3)+T(xc+40,y+124,mix='친핵체',size=19,fill=MINUS,anchor='start')
    s.append(an('move',g,**{'from':'0,36','dur':'1','delay':'.6','ease':'out'}))
    g=T(xo+96,y-82,tex='\\mathrm{E}^{+}',size=26,fill=PLUS)+A(xo+80,y-74,xo+30,y-30,'plus',3)+T(xo+96,y-112,mix='친전자체',size=19,fill=PLUS)
    s.append(an('move',g,**{'from':'40,-30','dur':'1','delay':'.9','ease':'out'}))
    return svg('0 0 480 300',440,'카보닐기의 탄소는 부분적 양전하로 친핵체의 공격을, 산소는 부분적 음전하로 친전자체의 공격을 받는다',s)
FIG['COPOL']=copol()

# ═══ S10 벤즈알데하이드 + HCN
def cyan(x,y,S=24,fcp='ul'):
    return [A_('C',x,y,lp=['l'],fc=-1,fcp=fcp),A_('N',x+56,y,lp=['r'])],[(0,1,3,'l')]
def hcn():
    s=[]; S=24; R=44
    # 벤즈알데하이드
    bx,by=78,150; ring,c=benz(bx,by,R,kek=0); s.append(ring)
    V=bverts(bx,by,R); vx,vy=V[1]; ux,uy=math.cos(math.radians(30)),-math.sin(math.radians(30))
    cx,cy=vx+ux*50,vy+uy*50
    a=[Cc(cx,cy),O_(cx,cy-54,[150,30]),H_(cx+44,cy+26),G_('_',vx,vy)]
    chk(fcount(a)+Counter({'C':6,'H':5}),'C7H6O','벤즈알데하이드')
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l')],None,S=S,name='벤즈알데하이드'))
    s.append(T(bx+30,by+82,mix='벤즈알데하이드',size=19,fill=MUTED))
    ca,cb=cyan(262,cy-2,S,fcp='ur')
    s.append(M(ca,cb,'CN',S=S,name='CN-'))
    s.append(an('draw',curved(244,cy-6,cx+16,cy-6,bend=-22),dur='.6',delay='.3'))
    s.append(an('draw',curved(cx-7,cy-24,cx-16,cy-56,bend=16),dur='.5',delay='.9'))
    s.append(harrow(338,384,by-10))
    # 정사면체 중간체
    ix=470; ring,_=benz(ix,by,R,kek=0); V=bverts(ix,by,R); vx,vy=V[1]; cx2,cy2=vx+ux*50,vy+uy*50
    g=[ring]
    a=[Cc(cx2,cy2),O_(cx2,cy2-56,['l','u','r'],fc=-1,fcp='dl'),G_('CN',cx2+62,cy2),H_(cx2,cy2+54),G_('_',vx,vy)]
    chk(fcount(a)+Counter({'C':6,'H':5}),'C8H6NO','중간체')
    g.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],None,S=S,name='중간체'))
    g.append(P([(410,40),(400,40),(400,236),(410,236)],INK,2.2)); g.append(P([(640,40),(650,40),(650,236),(640,236)],INK,2.2))
    g.append(T(525,262,mix='정사면체 중간체',size=19,fill=MUTED))
    s.append(step(''.join(g),'h1'))
    s.append(step(harrow(670,750,by-10,lab='$\\ce{HCN}$'),'h2'))
    mx=826; ring,_=benz(mx,by,R,kek=0); V=bverts(mx,by,R); vx,vy=V[1]; cx3,cy3=vx+ux*50,vy+uy*50
    g=[ring]
    a=[Cc(cx3,cy3),G_('OH',cx3,cy3-58),G_('CN',cx3+62,cy3),H_(cx3,cy3+54),G_('_',vx,vy)]
    chk(fcount(a)+Counter({'C':6,'H':5}),'C8H7NO','만델로나이트릴')
    g.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],None,S=S,name='만델로나이트릴'))
    g.append(T(mx+30,by+82,mix='만델로나이트릴',size=19,fill=MUTED))
    g.append(T(1012,by+9,tex='+',size=24))
    ca,cb=cyan(1050,by,S,fcp='ul'); g.append(M(ca,cb,'CN',S=S,name='CN- 재생'))
    s.append(step(''.join(g),'h2'))
    return svg('0 0 1130 280',1100,'벤즈알데하이드에 시안화 이온이 첨가되어 정사면체 중간체를 거치고, HCN과 반응해 만델로나이트릴이 되는 친핵성 첨가 반응',s)
FIG['HCN']=hcn()

# ═══ 끓는점 막대그래프 공통
def bars(items,W,H,tmin,tmax,ticks,x0=70,top=30,bw=58,anim=True,ylab='끓는점 [°C]',names_y=None):
    s=[]; y0=H-70; Hh=y0-top; n=len(items); gap=(W-x0-20)/n
    Y=lambda t:y0-(t-tmin)/(tmax-tmin)*Hh
    s.append(L(x0,top-8,x0,y0,MUTED,1.6))
    for t in ticks:
        s.append(L(x0-6,Y(t),x0,Y(t),MUTED,1.4)); s.append(T(x0-10,Y(t)+6,mix=str(t),size=18,anchor='end'))
        if t!=0: s.append(L(x0,Y(t),W-10,Y(t),'#E2E7EC',1))
    s.append(L(x0,Y(0),W-10,Y(0),MUTED,1.6))
    for i,(nm,sub,t,col) in enumerate(items):
        xc=x0+gap*(i+.5); yb=Y(0); yt=Y(t)
        r=f'<rect x="{f(xc-bw/2)}" y="{f(min(yb,yt))}" width="{bw}" height="{f(abs(yb-yt))}" fill="{col}" fill-opacity=".75" stroke="{INK}" stroke-width="1.2"/>'
        s.append(an('scale',r,**{'from':'1,0','o':f'{f(xc)},{f(yb)}','dur':'.7','delay':f'{.2+.2*i:.1f}'}) if anim else r)
        s.append(T(xc,(yt-8) if t>=0 else (yt+24),mix=(str(t).replace('-','−')),size=19,weight=700))
        ny=names_y or (H-40)
        s.append(T(xc,ny,mix=nm,size=19)); s.append(T(xc,ny+24,mix=sub,size=18,fill=MUTED))
    s.append(T(x0-56,top-16,mix=ylab,size=19,anchor='start'))
    return s
GR='#8C99A6'
def bp5():
    it=[('뷰테인','알케인 58',-0.5,GR),('프로판알','알데하이드 58',48,EQUI),('아세톤','케톤 58',56,EQUI),('1-프로판올','알코올 60',97,MINUS),('아세트산','카복실산 60',118,PLUS)]
    s=bars(it,560,360,-20,130,[0,40,80,120],top=40)
    return svg('0 0 560 360',540,'몰질량이 비슷한 뷰테인, 프로판알, 아세톤, 1-프로판올, 아세트산의 끓는점 막대그래프',s)
FIG['BP5']=bp5()

# ═══ S12 아세트산 이합체(수소 결합)
def dimer():
    s=[]; S=24; y=100
    a=[G_('CH3',50,y),Cc(118,y),O_(160,y-46,[90,0]),O_(160,y+46,[270,180]),H_(214,y+46)]
    s.append(M(a,[(0,1,1,'l'),(1,2,2,'l'),(1,3,1,'l'),(3,4,1,'l')],'C2H4O2',S=S,name='아세트산1'))
    g=[]
    a=[G_('CH3',410,y),Cc(342,y),O_(300,y+46,[270,180]),O_(300,y-46,[90,0]),H_(246,y-46)]
    a[2]['lp']=[270,0]; a[3]['lp']=[90,180]
    g.append(M(a,[(0,1,1,'l'),(1,2,2,'l'),(1,3,1,'l'),(3,4,1,'l')],'C2H4O2',S=S,name='아세트산2'))
    g.append(L(226,y+46,282,y+46,MUTED,2.4,dash='5 5')); g.append(L(176,y-46,234,y-46,MUTED,2.4,dash='5 5'))
    s.append(an('move',''.join(g),**{'from':'50,0','dur':'1','delay':'.3','ease':'out'}))
    s.append(T(230,y+5,mix='수소 결합',size=19,fill=MUTED,halo=True))
    return svg('0 0 460 200',440,'아세트산 두 분자가 카복실기끼리 수소 결합 2개로 이어진 모습',s)
FIG['DIMER']=dimer()
def acidline():
    s=[]; y=70; xs=[90,390,650,910]; labs=['\\ce{HCl}','\\ce{CH3COOH}','\\ce{H2CO3}','\\mathrm{R{-}OH}']; nm=['염산','아세트산(카복실산)','탄산','알코올']
    s.append(A(980,22,40,22,'ink',2.4)); s.append(T(510,10,mix='산의 세기 강함 ←',size=19,fill=MUTED))
    for i,x in enumerate(xs):
        s.append(T(x,y,tex=labs[i],size=26,weight=700)); s.append(T(x,y+30,mix=nm[i],size=19,fill=MUTED))
    s.append(T(240,y,tex='\\gg',size=28)); s.append(T(520,y,tex='>',size=28)); s.append(T(780,y,tex='>',size=28))
    s.append(P([(400,y+44),(400,y+54),(650,y+54),(650,y+44)],EQUI,2)); s.append(T(525,y+80,mix='40배 이상',size=19,fill=EQUI))
    s.append(P([(380,y+90),(380,y+100),(910,y+100),(910,y+90)],EQUI,2)); s.append(T(780,y+126,mix='$10^9$배 이상',size=19,fill=EQUI))
    return svg('0 -18 1000 224',840,'산의 세기: 염산이 가장 강하고, 아세트산은 탄산보다 40배 이상, 알코올보다 10의 9제곱 배 이상 강하다',s)
FIG['ACID']=acidline()

# ═══ S13 에스터화
def ester():
    s=[]; S=22; y=104
    a=[G_('CH3',40,y),Cc(102,y),O_(102,y-48,[150,30]),O_(160,y,['u','d']),H_(212,y)]
    s.append(hlrect(186,y-6,64,44))
    s.append(M(a,[(0,1,1,'l'),(1,2,2,'l'),(1,3,1,'l'),(3,4,1,'l')],'C2H4O2',S=S,name='에스터 산'))
    s.append(T(100,y+66,mix='아세트산',size=19,fill=MUTED))
    s.append(T(256,y+8,tex='+',size=24))
    a=[H_(300,y),O_(350,y,['u','d']),G_('CH2CH3',438,y)]
    s.append(hlrect(300,y-6,36,44))
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l')],'C2H6O',S=S,name='에스터 알코올'))
    s.append(T(380,y+66,mix='에탄올',size=19,fill=MUTED))
    s.append(T(560,y-4,tex='\\ce{<=>[H+]}',size=26))
    a=[G_('CH3',640,y),Cc(702,y),O_(702,y-48,[150,30]),O_(760,y,['u','d']),G_('CH2CH3',848,y)]
    s.append(hlrect(731,y-24,96,90))
    s.append(M(a,[(0,1,1,'l'),(1,2,2,'l'),(1,3,1,'l'),(3,4,1,'l')],'C4H8O2',S=S,name='아세트산 에틸'))
    s.append(T(760,y+66,mix='아세트산 에틸',size=19,fill=MUTED))
    g=T(932,y+8,tex='+',size=24)+M([O_(985,y-8,[120,60]),H_(958,y+26),H_(1012,y+26)],[(0,1,1,'l'),(0,2,1,'l')],'H2O',S=S,name='에스터 물')
    s.append(an('move',g,**{'from':'-260,0','dur':'1.2','delay':'.4','ease':'out'}))
    return svg('0 0 1040 190',1000,'아세트산과 에탄올이 산 촉매에서 에스터화 반응하여 아세트산 에틸과 물이 생긴다',s)
FIG['ESTER']=ester()
def fruit():
    s=[]
    s.append(C(70,92,40,INK,1.6,fill='#E5484D')); s.append(P([(70,52),(74,36)],'#5B6B7F',3)); s.append(f'<ellipse cx="88" cy="40" rx="14" ry="7" fill="#2E9E6A" transform="rotate(-25 88 40)"/>')
    s.append(f'<path d="M140 70 Q160 40 196 50 Q178 60 170 100 Q150 104 140 70 Z" fill="#F5C84C" stroke="{INK}" stroke-width="1.4"/>')
    w=''.join(P([(x,30),(x+8,20),(x,10),(x+8,0)],MUTED,2) for x in (110,126,142))
    s.append(an('move',f'<g transform="translate(0,10)">{w}</g>',**{'from':'0,8','dur':'1.2','rep':'alt','ease':'sine'}))
    return svg('0 0 220 140',200,'에스터의 향기를 내는 과일',s)
FIG['FRUIT']=fruit()

# ═══ S14 알코올 — 물의 유도체
def bentO(x,y,l,r,S=26,name='',want=None,lab=''):
    a=[O_(x,y,[60,120])]
    for t,ang in ((l,215),(r,325)):
        xx,yy=x+64*math.cos(math.radians(ang)),y-64*math.sin(math.radians(ang))
        a.append(H_(xx,yy) if t=='H' else G_(t,xx-(14 if ang==215 else -14),yy+4))
    return M(a,[(0,1,1,'l'),(0,2,1,'l')],want,S=S,name=name)
def alc():
    s=[]; y=96
    for i,(l,r,nm,wt) in enumerate([('H','H','물','H2O'),('CH3','H','메탄올 (알코올)','CH4O'),('CH3','CH3','다이메틸 에테르 (에테르)','C2H6O')]):
        x=150+i*330
        g=bentO(x,y,l,r,name=nm,want=wt)+T(x,y+100,mix=nm,size=20,fill=MUTED)
        s.append(an('pop',g,**popa(x,y,.2+.4*i)))
        if i<2: s.append(A(x+110,y+10,x+210,y+10,'muted',2.4)); s.append(T(x+160,y-8,mix='H → R–' if i==0 else 'H → R–',size=18,fill=MUTED))
    return svg('0 0 1000 220',940,'물, 메탄올, 다이메틸 에테르의 굽은 구조: 물의 수소를 알킬기로 바꾼 유도체',s)
FIG['ALC']=alc()
def hbond():
    s=[]; S=22
    a=[G_('CH3CH2',60,70),O_(130,70,['u','d']),H_(178,70)]
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l')],'C2H6O',S=S,name='에탄올 hb1'))
    g=M([G_('CH3CH2',214,150),O_(250,104,['l','r']),H_(296,150)],[(0,1,1,'l'),(1,2,1,'l')],'C2H6O',S=S,name='에탄올 hb2')
    g+=L(192,78,244,94,MUTED,2.4,dash='5 5')
    s.append(an('fade',g,dur='.8',delay='.4'))
    s.append(T(330,62,mix='수소 결합',size=19,fill=MUTED,anchor='end'))
    return svg('0 0 340 180',320,'에탄올 분자 사이의 수소 결합',s)
FIG['HBOND']=hbond()

# ═══ S15 알코올의 산화와 환원
def oxid():
    s=[]; S=22; y=110
    # 에탄올
    a=[G_('CH3',40,y),Cc(104,y),H_(104,y-52),H_(104,y+52),O_(162,y,['u','d']),H_(212,y)]
    s.append(hlrect(186,y-6,64,40))
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l'),(1,3,1,'l'),(1,4,1,'l'),(4,5,1,'l')],'C2H6O',S=S,name='산화 에탄올',show=False))
    s.append(T(120,y+92,mix='에탄올',size=19,fill=MUTED))
    a=[G_('CH3',400,y),Cc(464,y),O_(464,y-50,[150,30]),H_(518,y)]
    s.append(hlrect(490,y-24,68,86))
    s.append(M(a,[(0,1,1,'l'),(1,2,2,'l'),(1,3,1,'l')],'C2H4O',S=S,name='산화 아세트알데하이드',show=False))
    s.append(T(462,y+92,mix='아세트알데하이드',size=19,fill=MUTED))
    a=[G_('CH3',720,y),Cc(784,y),O_(784,y-50,[150,30]),O_(842,y,['u','d']),H_(892,y)]
    s.append(hlrect(824,y-24,110,86))
    s.append(M(a,[(0,1,1,'l'),(1,2,2,'l'),(1,3,1,'l'),(3,4,1,'l')],'C2H4O2',S=S,name='산화 아세트산',show=False))
    s.append(T(806,y+92,mix='아세트산',size=19,fill=MUTED))
    for (x1,x2) in ((240,370),(560,690)):
        s.append(A(x1,y-14,x2,y-14,OXC,3)); s.append(T((x1+x2)/2,y-28,mix='산화',size=20,fill=OXC,weight=700))
        s.append(A(x2,y+18,x1,y+18,RDC,3)); s.append(T((x1+x2)/2,y+48,mix='환원',size=20,fill=RDC,weight=700))
    for (x,v,g) in ((104,'-1','o1'),(464,'+1','o2'),(784,'+3','o3')):
        s.append(step(T(x+22,y-74 if x!=104 else y-74,tex='\\mathrm{C}:\\ '+v,size=20,fill=OXC,weight=700),g))
    return svg('0 0 960 220',940,'에탄올이 산화되어 아세트알데하이드, 다시 아세트산이 되고 거꾸로 환원된다. 작용기 탄소의 산화수 -1, +1, +3',s)
FIG['OXID']=oxid()

# ═══ S16 예제: 발효 통
def ferm():
    s=[]
    s.append(f'<path d="M40 60 L40 170 Q40 186 56 186 L164 186 Q180 186 180 170 L180 60" fill="#F3E3C3" stroke="{INK}" stroke-width="2.4"/>')
    s.append(f'<rect x="40" y="96" width="140" height="90" fill="#E8C36A" fill-opacity=".6"/>')
    s.append(L(40,96,180,96,INK,1.4))
    b=''.join(C(x,y,r,MUTED,1.4,fill='#fff') for x,y,r in ((70,150,6),(104,130,5),(140,160,7),(158,118,4),(90,112,4)))
    s.append(an('move',b,**{'from':'0,30','dur':'1.6','rep':'loop','ease':'lin'}))
    s.append(T(110,214,mix='곡물·당의 발효',size=19,fill=MUTED))
    return svg('0 0 220 226',200,'곡물과 당을 발효하는 통에서 기체 방울이 올라온다',s)
FIG['FERM']=ferm()

# ═══ S17 에테르
def ether():
    s=[]; y=80
    for x in (134,434):
        s.append(bentO(x,y,'CH3CH2','CH2CH3',S=22,name='다이에틸 에테르',want='C4H10O'))
    s.append(T(284,y-8,tex='\\times',size=34,fill=PLUS)); s.append(T(284,y-46,mix='수소 결합 없음',size=19,fill=PLUS))
    s.append(T(284,y+130,mix='에테르 + 에테르',size=19,fill=MUTED))
    x=700; s.append(bentO(x,y,'CH3CH2','CH2CH3',S=22,name='다이에틸 에테르2',want='C4H10O'))
    g=M([O_(932,y-36,[90,0]),H_(876,y-36),H_(932,y+20)],[(0,1,1,'l'),(0,2,1,'l')],'H2O',S=22,name='물 에테르')
    g+=L(866,y-34,728,y-34,MUTED,2.4,dash='5 5')
    s.append(an('move',g,**{'from':'60,0','dur':'1','delay':'.3','ease':'out'}))
    s.append(T(800,y-48,mix='수소 결합',size=19,fill=MUTED))
    s.append(T(780,y+130,mix='에테르 + 물',size=19,fill=MUTED))
    return svg('0 0 1000 230',940,'다이에틸 에테르끼리는 수소 결합을 하지 못하지만 물과는 수소 결합을 한다',s)
FIG['ETHER']=ether()

# ═══ S18 아민
def amine():
    s=[]; y=92
    items=[(('H','H','H'),'암모니아','NH3'),(('CH3','H','H'),'1차 아민','CH5N'),(('CH3','CH3','H'),'2차 아민','C2H7N'),(('CH3','CH3','CH3'),'3차 아민','C3H9N')]
    for i,(sub,nm,wt) in enumerate(items):
        x=120+i*250; a=[N_(x,y,[90])]
        for t,ang in zip(sub,(210,330,270)):
            xx,yy=x+60*math.cos(math.radians(ang)),y-60*math.sin(math.radians(ang))
            if t=='H': a.append(H_(xx,yy))
            else: a.append(G_(t,xx+(-14 if ang==210 else 14 if ang==330 else 0),yy+(4 if ang!=270 else 6)))
        g=f'<ellipse cx="{x}" cy="{y-36}" rx="22" ry="15" fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="1.5"/>'
        g+=M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')],wt,S=24,name=nm)
        nmf={'NH3':'$\\ce{NH3}$','CH5N':'$\\ce{CH3NH2}$','C2H7N':'$\\ce{(CH3)2NH}$','C3H9N':'$\\ce{(CH3)3N}$'}[wt]
        g+=T(x,y+104,mix=nm,size=20,weight=700)+T(x,y+132,mix=nmf,size=20,fill=MUTED)
        s.append(an('pop',g,**popa(x,y,.2+.3*i)))
    return svg('0 0 1000 240',940,'암모니아와 1차, 2차, 3차 아민의 구조식: 질소의 비공유 전자쌍',s)
FIG['AMINE']=amine()

# ═══ S21 방향족 화합물 예
def arom():
    s=[]; y=124; R=50
    r1,c1=benz(160,y,R); chk(c1,'C6H6','벤젠')
    r2,c2=benz(500,y,R,subs={0:('CHO',True)}); chk(c2,'C7H6O','벤즈알데하이드2')
    r3,c3=benz(840,y,R,subs={0:('COOH',True),1:('OH',True)}); chk(c3,'C7H6O3','살리실산')
    for i,(r,x,nm,src) in enumerate(((r1,160,'벤젠','석유·석탄의 증류물'),(r2,500,'벤즈알데하이드','과일·견과류의 향기 성분'),(r3,840,'살리실산','버드나무 껍질 → 아스피린 원료'))):
        s.append(an('pop',r+T(x,y+98,mix=nm,size=21,weight=700)+T(x,y+126,mix=src,size=19,fill=MUTED),**popa(x,y,.2+.3*i)))
    return svg('0 0 1000 268',940,'방향족 화합물의 예: 벤젠, 벤즈알데하이드, 살리실산',s)
FIG['AROM']=arom()

# ═══ S22 벤젠 공명 구조(그림 Ⅰ-50)
def bres():
    s=[]
    s.append(an('pop',benzL(140,150,R=54,S=24,HR=96,name='공명1'),**popa(140,150,.2)))
    s.append(rarrow(262,318,150))
    s.append(an('pop',benzL(440,150,R=54,kek=1,S=24,HR=96,name='공명2'),**popa(440,150,.6)))
    V=bverts(140,150,54); x,y=V[0]
    s.append(arcA(x,y,240,300,20,'120^\\circ',lr=40,size=18))
    return svg('0 0 580 300',560,'벤젠의 두 공명 구조: 2중 결합과 단일 결합의 자리가 바뀐 전개 구조식',s)
FIG['BRES']=bres()

# ═══ S23 벤젠의 p 오비탈과 π 전자 도넛(그림 Ⅰ-51)
def b3d():
    s=[]; cx,cy=280,196; Rx,Ry=160,70; L0=74
    th=[math.radians(a) for a in range(0,360,60)]
    P_=[(cx+Rx*math.cos(t),cy+Ry*math.sin(t)) for t in th]
    back=[k for k in range(6) if math.sin(th[k])<-0.01]; front=[k for k in range(6) if k not in back]
    side=[k for k in range(6) if abs(math.sin(th[k]))<=0.01]
    def lobes(k):
        x,y=P_[k]; return lob(x,y,90,L0,1,W=.5,lsize=18)+lob(x,y,270,L0,-1,W=.5,lsize=18)
    for k in back: s.append(lobes(k))
    for k in range(6):
        a,b=P_[k],P_[(k+1)%6]; s.append(L(*a,*b,INK,3.4,extra='stroke-linecap="round"'))
    for k in range(6):
        x,y=P_[k]; hx,hy=cx+(Rx+46)*math.cos(th[k]),cy+(Ry+20)*math.sin(th[k])
        s.append(L(x,y,hx,hy,INK,2)); s.append(T(hx+(12 if math.cos(th[k])>.3 else -12 if math.cos(th[k])<-.3 else 0),hy+7+(10 if math.sin(th[k])>.3 else -4 if math.sin(th[k])<-.3 else 0),tex='\\mathrm{H}',size=19,halo=True))
    for k in front: s.append(lobes(k))
    def donut(yc):
        return (f'<path d="M{cx-Rx-14} {yc} a{Rx+14} {Ry+8} 0 1 0 {2*(Rx+14)} 0 a{Rx+14} {Ry+8} 0 1 0 {-2*(Rx+14)} 0 Z M{cx-Rx+44} {yc} a{Rx-44} {Ry-18} 0 1 1 {2*(Rx-44)} 0 a{Rx-44} {Ry-18} 0 1 1 {-2*(Rx-44)} 0 Z" fill="{MINUS}" fill-opacity=".16" fill-rule="evenodd" stroke="{FIELD}" stroke-width="2.6" stroke-dasharray="8 6"/>')
    s.append(step(an('fade',donut(cy-60)+donut(cy+60),dur='1'),'d1'))
    s.append(step(T(cx,30,mix='π 전자 구름(도넛 모양) — 고리 위',size=19,fill=FIELD,weight=700),'d1'))
    s.append(step(T(cx,cy+156,mix='고리 아래',size=19,fill=FIELD,weight=700),'d1'))
    return svg('0 0 570 370',550,'벤젠의 탄소 6개마다 평면에 수직인 p 오비탈이 이웃과 똑같이 겹쳐 고리 위아래에 도넛 모양의 π 전자 구름을 만든다',s)
FIG['B3D']=b3d()

# ═══ S24 케쿨레와 꿈
def kek():
    s=[]; cx,cy=210,180
    r,_=benz(cx,cy,62); s.append(r)
    sn=[]; R0=128
    pts=[(cx+R0*math.cos(math.radians(a)),cy-R0*math.sin(math.radians(a))) for a in range(18,352,6)]
    sn.append(P(pts,'#4F8A3C',16,extra='stroke-linecap="round" stroke-opacity=".85"'))
    pts2=[(cx+R0*math.cos(math.radians(a)),cy-R0*math.sin(math.radians(a))) for a in range(18,352,12)]
    sn.append(P(pts2,'#C7E3B5',3,dash='4 10'))
    hx,hy=cx+R0*math.cos(math.radians(10)),cy-R0*math.sin(math.radians(10))
    sn.append(f'<ellipse cx="{f(hx+4)}" cy="{f(hy-10)}" rx="20" ry="14" fill="#4F8A3C" transform="rotate(-80 {f(hx+4)} {f(hy-10)})"/>')
    sn.append(C(hx+10,hy-12,3,'#fff',1,fill='#fff'))
    s.append(an('rot',''.join(sn),**{'from':'-120','o':f'{cx},{cy}','dur':'2','ease':'out'}))
    s.append(T(cx,cy+178,mix='자기 꼬리를 문 뱀 → 고리 모양',size=19,fill=MUTED))
    return svg('0 0 420 370',400,'자기 꼬리를 문 뱀과 그 안의 벤젠 고리: 케쿨레의 꿈',s)
FIG['KEK']=kek()

# ═══ S25 벤젠의 표현 + 페놀·벤즈알데하이드·벤조산
def brep():
    s=[]; y=86; R=46
    s.append(benz(100,y,R,kek=0)[0]); s.append(rarrow(170,224,y)); s.append(benz(294,y,R,kek=1)[0])
    s.append(T(392,y+10,tex='=',size=30))
    s.append(step(benz(490,y,R,hybrid=True)[0]+T(620,y-6,mix='공명 혼성체',size=20,anchor='start',weight=700)+T(620,y+22,mix='(고리 안 원: 비편재화된 π 전자)',size=19,anchor='start',fill=MUTED),'r1'))
    s.append(T(196,y+82,mix='공명 구조(편의상 이 중 하나로 나타낸다)',size=19,fill=MUTED))
    return svg('0 0 900 180',780,'벤젠의 두 공명 구조와 공명 혼성체의 표현',s)
FIG['BREP']=brep()
def bders():
    s=[]; y=116; R=46
    for i,(sub,nm,gn,wt) in enumerate((('OH','페놀','하이드록시기','C6H6O'),('CHO','벤즈알데하이드','포밀기','C7H6O'),('COOH','벤조산','카복실기','C7H6O2'))):
        x=150+i*300; r,c=benz(x,y,R,subs={0:(sub,True)}); chk(c,wt,nm)
        s.append(an('pop',r+T(x,y+82,mix=nm,size=21,weight=700)+T(x,y+108,mix=f'$-\\ce{{{sub}}}$ {gn}',size=19,fill=MUTED),**popa(x,y,.2+.3*i)))
    return svg('60 0 780 236',740,'벤젠 고리의 수소 대신 하이드록시기, 포밀기, 카복실기가 붙은 페놀, 벤즈알데하이드, 벤조산',s)
FIG['BDERS']=bders()

# ═══ S26 방향족 안정성 에너지 도표
def stab():
    s=[]; x1,x2=120,330; yh,yb,yc=64,64+150*.66,64+360*.66
    s.append(A(46,300,46,24,'ink',2.4)); s.append(T(30,40,mix='에너지',size=19,anchor='end' if False else 'middle'))
    s.append(L(x1,yh,x2,yh,INK,3,dash='8 6')); s.append(T(x2+10,yh-6,mix='편재된 π 결합 3개를',size=19,anchor='start')); s.append(T(x2+10,yh+20,mix='가정한 구조',size=19,anchor='start'))
    s.append(L(x1,yb,x2,yb,INK,3.4)); s.append(T(x2+10,yb+7,mix='실제 벤젠(비편재화)',size=19,anchor='start',weight=700))
    s.append(L(x1-20,yc,x2,yc,INK,3)); s.append(T(x2+10,yc+7,mix='사이클로헥세인 $\\ce{C6H12}$',size=19,anchor='start'))
    s.append(step(dimline(x2-24,yh,x2-24,yb,'150 kJ/mol',off=0,size=20,side=-1)+'','s1'))
    s.append(step(an('draw',A(150,yh+4,150,yc-4,'muted',2.6,d=True),dur='.8')+T(142,(yh+yc)/2+40,mix='$-360$ (예상)',size=19,anchor='end',fill=MUTED,halo=True),'s2'))
    s.append(step(an('draw',A(250,yb+4,250,yc-4,'ink',2.6),dur='.8')+T(258,(yb+yc)/2+8,mix='$-208$ (실제)',size=19,anchor='start',halo=True),'s2'))
    s.append(step(T(205,yc+40,mix='$+\\,3\\ce{H2}$ 수소 첨가 엔탈피 [kJ/mol]',size=19,fill=MUTED),'s2'))
    return svg('0 0 560 350',520,'벤젠은 편재된 π 결합 3개를 가정한 구조보다 150 kJ/mol 더 안정하다. 수소 첨가 엔탈피 예상 -360, 실제 -208',s)
FIG['STAB']=stab()

# ═══ S29 아스피린 연표 + 구조
def asptl():
    s=[]; y=100; ev=[('기원전 400쯤','히포크라테스','버드나무 껍질 해열 진통'),('1828','뷰흐너','살리신 분리'),('1838','피리아','살리실산 만듦'),('1853','게르하르트','아세틸살리실산 처음 합성'),('1897','호프만','순수한 아세틸살리실산'),('1899','「아스피린」','이름으로 판매'),('1971','베인','작용 원리 규명')]
    s.append(L(40,y,1080,y,MUTED,3))
    for i,(yr,who,what) in enumerate(ev):
        x=95+i*155; up=(i%2==0)
        g=C(x,y,9,INK,2,fill=EQUI)+T(x,y-62 if up else y+40,mix=yr,size=20,weight=700)
        if up: g+=T(x,y-38,mix=who,size=19)+T(x,y-16,mix=what,size=18,fill=MUTED)
        else: g+=T(x,y+66,mix=who,size=19)+T(x,y+90,mix=what,size=18,fill=MUTED)
        s.append(an('pop',g,**popa(x,y,.2+.2*i)))
    return svg('0 0 1120 206',1080,'아스피린 개발의 연표: 히포크라테스의 버드나무 껍질부터 베인의 작용 원리 규명까지',s)
FIG['ASPTL']=asptl()
def aspst():
    s=[]; y=110; R=44
    r,c=benz(150,y,R,subs={0:('COOH',False),1:('OH',True)}); chk(c,'C7H6O3','살리실산2'); s.append(r)
    s.append(T(150,y+84,mix='살리실산',size=20,weight=700))
    s.append(harrow(260,380,y-4,lab='아세틸화'))
    r,c=benz(500,y,R,subs={0:('COOH',False),1:('OCOCH3',True)}); chk(c,'C9H8O4','아세틸살리실산'); s.append(r)
    s.append(T(500,y+84,mix='아세틸살리실산(아스피린)',size=20,weight=700))
    s.append(T(370,232,tex='\\ce{C7H6O3 + (CH3CO)2O -> C9H8O4 + CH3COOH}',size=22))
    return svg('0 0 740 250',640,'살리실산의 하이드록시기를 아세틸화하여 에스터인 아세틸살리실산을 만든다',s)
FIG['ASPST']=aspst()

# ═══ S30 의약품과 활성 자리
def drug():
    s=[]
    s.append(f'<path d="M30 300 L30 150 L150 150 L170 110 L210 110 L230 150 C230 186 290 186 290 150 L410 150 L410 300 Z" fill="#C9D3DD" stroke="{INK}" stroke-width="2"/>')
    s.append(T(220,262,mix='세포막의 활성 자리',size=20))
    d=f'<path d="M150 150 L170 110 L210 110 L230 150 C230 186 290 186 290 150 L290 140 L150 140 Z" fill="{EQUI}" fill-opacity=".8" stroke="{INK}" stroke-width="2" transform="translate(0,-2)"/>'
    d+=T(220,100,mix='의약품 분자',size=20,weight=700)
    s.append(an('move',d,**{'from':'0,-80','dur':'1.4','delay':'.3','ease':'out'}))
    return svg('0 0 440 320',400,'의약품 분자가 세포막 활성 자리의 모양에 꼭 맞게 들어간다',s)
FIG['DRUG']=drug()

# ═══ S31 연습 문제 1
CONDS={(5,()):(['CH3','CH2','CH2','CH2','CH3'],[]),(4,(2,)):(['CH3','CH','CH2','CH3'],[(1,'u','CH3',True)]),
       (3,(2,2)):(['CH3','C','CH3'],[(1,'u','CH3',True),(1,'d','CH3',True)])}
CONDS.update({(6,()):(['CH3','CH2','CH2','CH2','CH2','CH3'],[]),(5,(2,)):(['CH3','CH','CH2','CH2','CH3'],[(1,'u','CH3',True)]),
   (5,(3,)):(['CH3','CH2','CH','CH2','CH3'],[(2,'u','CH3',True)]),(4,(2,3)):(['CH3','CH','CH','CH3'],[(1,'u','CH3',True),(2,'d','CH3',True)]),
   (4,(2,2)):(['CH3','C','CH2','CH3'],[(1,'u','CH3',True),(1,'d','CH3',True)])})
EX1=[[(5,(),'펜테인'),(4,(2,),'2-메틸뷰테인'),(3,(2,2),'2,2-다이메틸프로페인')],[(6,(),'헥세인'),(5,(2,),'2-메틸펜테인'),(5,(3,),'3-메틸펜테인'),(4,(2,3),'2,3-다이메틸뷰테인'),(4,(2,2),'2,2-다이메틸뷰테인')]]
for row,nC in zip(EX1,(5,6)):
    ks={canon_edges(*skel(Ln,list(br))[:2]) for Ln,br,_ in row}; assert len(ks)==len(row)==(3 if nC==5 else 5)
    for Ln,br,_ in row: assert Ln+len(br)==nC
def ex1():
    s=[]
    for r,(row,y) in enumerate(zip(EX1,(74,226))):
        sz=19; gap=28
        s.append(T(14,y-50,tex='\\ce{C5H12}' if r==0 else '\\ce{C6H14}',size=22,anchor='start',weight=700))
        ws=[max(sum(gw(t,sz) for t in CONDS[(Ln,tuple(br))][0]),170) for Ln,br,_ in row]
        x0=60+(1020-sum(ws)-gap*(len(row)-1))/2; assert x0>=60, x0
        for i,(Ln,br,nm) in enumerate(row):
            x=x0+sum(ws[:i])+gap*i+ws[i]/2
            g,brr=CONDS[(Ln,tuple(br))]
            s.append(step(cond(x,y,g,brr,size=sz)+T(x,y+68,mix=nm,size=19,fill=MUTED),f'e1{r}'))
    return svg('0 0 1080 306',1040,'C5H12의 구조 이성질체 3개와 C6H14의 구조 이성질체 5개의 축약 구조식',s)
FIG['EX1']=ex1()

# ═══ S32 연습 문제 2
def ex2():
    s=[]; S=28; y=110; xs=[90,250,390,540,690]
    a=[G_('CH3',xs[0],y),G_('CH',xs[1],y),G_('CH',xs[2],y),Cc(xs[3],y),G_('CH',xs[4],y)]
    s.append(lewis(a,[(0,1,1,'l'),(1,2,2,'l'),(2,3,1,'l'),(3,4,3,'l')],S=S,check=False))
    chk(fcount(a),'C5H6','연습 2')
    for i,x in enumerate(xs): s.append(T(x,y-70,tex='\\mathrm{C}_{'+str(i+1)+'}',size=19,fill=MUTED))
    hy=['sp^3','sp^2','sp^2','sp','sp']
    for i,x in enumerate(xs): s.append(step(T(x,y-40,tex=hy[i],size=22,fill=FIELD,weight=700),'x1'))
    bl=['σ','σ + π','σ','σ + 2π']
    for i in range(4):
        s.append(step(T((xs[i]+xs[i+1])/2,y+56,mix=bl[i],size=21,weight=700),'x2'))
    return svg('0 0 780 190',760,'CH3-CH=CH-C≡CH의 탄소 번호, 혼성, 탄소-탄소 결합의 σ·π 결합',s)
FIG['EX2']=ex2()

# ═══ S33 연습 문제 3 컨쥬게이션
def zig(x0,y0,n,dx=56,dy=30,dbl=()):
    pts=[(x0+i*dx,y0+(0 if i%2==0 else -dy)) for i in range(n)]; s=[]
    for i in range(n-1):
        a,b=pts[i],pts[i+1]; s.append(L(*a,*b,INK,3,extra='stroke-linecap="round"'))
        if i in dbl:
            mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2; dxn,dyn=b[0]-a[0],b[1]-a[1]; n_=math.hypot(dxn,dyn); px,py=-dyn/n_,dxn/n_
            sg=1 if i%2==0 else -1; o=9
            s.append(L(a[0]+dxn*.18+px*o*sg,a[1]+dyn*.18+py*o*sg,b[0]-dxn*.18+px*o*sg,b[1]-dyn*.18+py*o*sg,INK,3,extra='stroke-linecap="round"'))
    return ''.join(s)
def ex3():
    s=[]
    s.append(step(T(240,50,tex='\\ce{CH2=CH-CH=CH2}',size=26)+an('draw',zig(156,150,4,dbl=(0,2)),dur='1')+T(240,206,mix='2중 결합 2개 (1,3-뷰타다이엔)',size=19,fill=MUTED),'c1'))
    s.append(step(T(720,50,tex='\\ce{CH2=CH-CH=CH-CH=CH2}',size=26)+an('draw',zig(580,150,6,dbl=(0,2,4)),dur='1.2')+T(720,206,mix='2중 결합 3개 (1,3,5-헥사트라이엔)',size=19,fill=MUTED),'c2'))
    return svg('0 0 980 220',940,'2중 결합이 2개, 3개인 가장 간단한 컨쥬게이션 분자: 1,3-뷰타다이엔과 1,3,5-헥사트라이엔',s)
FIG['EX3']=ex3()

# ═══ S34 연습 문제 4 끓는점
def ex4():
    it=[('1) 펜테인','72 g/mol',36,GR),('2) 1-뷰탄올','74 g/mol',118,MINUS),('3) 다이에틸 에테르','74 g/mol',35,EQUI)]
    s=bars(it,560,300,0,130,[0,40,80,120],top=36,bw=70)
    return svg('0 0 560 300',500,'펜테인 36도, 1-뷰탄올 118도, 다이에틸 에테르 35도의 끓는점 막대그래프',s)
FIG['EX4']=ex4()

tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused)
