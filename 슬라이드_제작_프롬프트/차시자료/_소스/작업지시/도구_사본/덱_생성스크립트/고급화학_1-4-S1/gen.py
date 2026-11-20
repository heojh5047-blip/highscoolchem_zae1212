# -*- coding: utf-8 -*-
"""고급화학 1-4-S1 [심화] 그림 생성: gen_head.py(OUT=이 덱 — assert, 1-2-1 lewis 도우미 + 결합 모양 'n'·'h') + lib131·chem·base141(1-4-1 사본)
   → tpl.html의 {{KEY}}를 바꿔 slides.html. 그림마다 원자 전자 수·형식 전하(lewis), 분자식(M), 단계별 원자 수·전하(rxn), 반응식(eqchk)을 assert."""
import math, re, sys, os
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/1-4-S1_심화_친핵성_치환_제거_반응과_첨가_반응/slides.html') and '1-4-2_' not in OUT
exec(open(os.path.join(HERE,'lib131.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,'chem.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,'base141.py'),encoding='utf-8').read())
VAL.update({'Br':7,'N':5,'I':7,'Cl':7})
CW.update({'R':.72,"'":.22,'(':.34,')':.34,'-':.5,'I':.36})
def wave(*a,**k): raise RuntimeError('wave()는 이 덱에서 쓰지 않음(사본에서 잘림)')
def popa(x,y,d,dur='.6'): return {'o':f'{f(x)},{f(y)}','dur':dur,'delay':f'{d:.1f}'}
def POP(body,x,y,d=0.2): return an('pop',body,**popa(x,y,d))
def DRAW(body,d=0.3,dur='.7'): return an('draw',body,dur=dur,delay=f'{d:.1f}')

# ═════ 검산 ═════
def fcount(atoms):
    c=Counter()
    for a in atoms:
        if a.get('grp'):
            if a['grp']=='_': continue
            c+=formula(a['grp'])
        else: c[a['el']]+=1
    return c
def formula(t):
    """괄호·곱수 있는 화학식 → Counter (결합 기호 = # - 는 무시)"""
    t=re.sub(r'[=#\-]','',t)
    def p(s,i):
        c=Counter()
        while i<len(s):
            ch=s[i]
            if ch=='(':
                sub,i=p(s,i+1); m=re.match(r'\d+',s[i:]); k=int(m.group()) if m else 1; i+=len(m.group()) if m else 0
                for e in sub: c[e]+=sub[e]*k
            elif ch==')': return c,i+1
            else:
                m=re.match(r'([A-Z][a-z]?)(\d*)',s[i:]); assert m,(s,i)
                c[m.group(1)]+=int(m.group(2) or 1); i+=len(m.group())
        return c,i
    return p(t,0)[0]
def chk(c,want,name):
    if +c!=+formula(want): sys.exit(f'[{name}] 원자 수 {dict(c)} ≠ {want}')
SPEC={}
def M(atoms,bonds,want,S=24,name='',show=True,**k):
    """lewis 그리기 + 분자식 assert. SPEC[name] = (원자 수, 전하)"""
    if want: chk(fcount(atoms),want,name)
    SPEC[name]=(fcount(atoms),sum(a.get('fc',0) for a in atoms))
    return lewis(atoms,bonds,S=S,name=name,showlp=show,**k)
def rxn(left,right,name):
    """메커니즘 한 단계: 왼쪽·오른쪽 화학종(SPEC 이름)의 원자 수·형식 전하 합이 같아야 한다"""
    cl=sum((SPEC[n][0] for n in left),Counter()); cr=sum((SPEC[n][0] for n in right),Counter())
    ql=sum(SPEC[n][1] for n in left); qr=sum(SPEC[n][1] for n in right)
    if +cl!=+cr or ql!=qr: sys.exit(f'[단계 {name}] {dict(cl)},{ql} ≠ {dict(cr)},{qr}')
    RXN.append(name)
RXN=[]
def sp(s):
    s=s.strip(); m=re.match(r'^(\d+)(?=[A-Z(])',s); k=int(m.group(1)) if m else 1
    if m: s=s[len(m.group(1)):]
    q=0; m=re.search(r'\^(\d*)([+-])$',s) or re.search(r'()([+-])$',s)
    if m:
        q=(int(m.group(1) or 1))*(1 if m.group(2)=='+' else -1); s=s[:m.start()]
    c=formula(s)
    return Counter({e:v*k for e,v in c.items()}),q*k
EQLOG=[]
def eqchk(eq,tag=''):
    e=re.sub(r'(->|<=>)\[[^\]]*\]',r'\1',eq)
    lhs,rhs=re.split(r'->|<=>',e)
    def side(x):
        c=Counter(); q=0
        for t in re.split(r'\s\+\s',x):
            a,b=sp(t); c+=a; q+=b
        return c,q
    (cl,ql),(cr,qr)=side(lhs),side(rhs)
    if +cl!=+cr or ql!=qr: sys.exit(f'[반응식 {tag}] {eq}: {dict(cl)},{ql} ≠ {dict(cr)},{qr}')
    EQLOG.append((tag,eq,dict(cl),ql))
EQS=[('S4','HO- + H+ -> H2O'),('S4','(CH3)3CBr -> (CH3)3C+ + Br-'),('S4','CH2=CH2 + H+ -> CH3CH2+'),
 ('S6','CH3COOH + CH3CH2OH <=>[H2SO4] CH3COOCH2CH3 + H2O'),('S8','HO- + CH3Br -> CH3OH + Br-'),
 ('S9','HO- + CH3CH2CHBrCH3 -> CH3CH2CH(OH)CH3 + Br-'),('S13','(CH3)3CBr + 2H2O -> (CH3)3COH + H3O+ + Br-'),
 ('S13','(CH3)3C+ + H2O -> (CH3)3COH2+'),('S13','(CH3)3COH2+ + H2O -> (CH3)3COH + H3O+'),
 ('S18','CH3CH2CHBrCH3 + CH3CH2O- -> CH3CH=CHCH3 + CH3CH2OH + Br-'),('S19','CH3CH2Br + CH3CH2O- -> CH2=CH2 + CH3CH2OH + Br-'),
 ('S20','(CH3)3CCl + H2O -> (CH3)2C=CH2 + H3O+ + Cl-'),('S20','(CH3)3CCl + 2H2O -> (CH3)3COH + H3O+ + Cl-'),
 ('S21','(CH3)2C(OH)CH2COCH3 -> (CH3)2C=CHCOCH3 + H2O'),('S21','C6H12O2 + OH- -> C6H11O2- + H2O'),('S21','C6H11O2- -> C6H10O + OH-'),
 ('S25','CH3CH2CH2CH2Br + CN- -> CH3CH2CH2CH2CN + Br-'),('S25','(CH3)2CBrCH2CH3 + CH3CH2O- -> (CH3)2C=CHCH3 + CH3CH2OH + Br-'),
 ('S26','CH3CH2CHBrCH3 + I- -> CH3CH2CHICH3 + Br-'),('S27','(CH3)3COH + HBr -> (CH3)3CBr + H2O'),
 ('S27','CH3CH2O- + CH3I -> CH3CH2OCH3 + I-'),('S27','(CH3)3CO- + CH3I -> (CH3)3COCH3 + I-'),
 ('S27','CH3O- + (CH3)3CCl -> (CH3)2C=CH2 + CH3OH + Cl-'),('S29','CH4 + Cl2 ->[h\\nu] CH3Cl + HCl'),
 ('S29','Cl2 -> 2Cl'),('S29','Cl + CH4 -> HCl + CH3'),('S29','CH3 + Cl2 -> CH3Cl + Cl'),('S29','Cl + CH3 -> CH3Cl'),
 ('S31','CH2=CH2 + HBr -> CH3CH2Br'),('S32','(CH3)2C=CH2 + HBr -> (CH3)3CBr'),('S33','CH3CH=CH2 + H2O -> CH3CH(OH)CH3'),
 ('S33','CH3CH=CH2 + H2O -> CH3CH2CH2OH'),('S33','CH2=CH2 + H2O -> CH3CH2OH'),('S34','C5H8 + Br2 -> C5H8Br2'),
 ('S34','CH2=CH2 + Br2 -> C2H4Br+ + Br-'),('S34','C2H4Br+ + Br- -> CH2BrCH2Br'),('S35','HC#C- + CH3Br -> HC#CCH3 + Br-'),
 ('S35','CH3C#CCH3 + H2 -> CH3CH=CHCH3'),('S35','CH3CH2C#CH + H2O -> CH3CH2COCH3'),('S36','CH2=CHCH=CH2 + HBr -> CH3CHBrCH=CH2'),
 ('S36','CH2=CHCH=CH2 + HBr -> CH3CH=CHCH2Br'),('S37','CH2=CHCH=CH2 + CH2=CH2 -> C6H10'),('S37','C4H6 + C3H4O -> C7H10O'),
 ('S38','(CH3)2C=CHCH3 + HBr -> (CH3)2CBrCH2CH3'),('S38','(CH3)2C=CHCH3 + H2O -> (CH3)2CHCH(OH)CH3')]
for tg,e in EQS: eqchk(e,tg)

# ═════ 그림 도우미 ═════
def G_(t,x,y,**k): d=dict(el='C',x=x,y=y,grp=t); d.update(k); return d
def O_(x,y,lp,**k): return A_('O',x,y,lp=lp,**k)
def hlrect(x,y,w,h): return f'<rect x="{f(x-w/2)}" y="{f(y-h/2)}" width="{f(w)}" height="{f(h)}" rx="7" fill="{HL}" fill-opacity=".45"/>'
def dlab(x,y,sign,size=20):
    return T(x,y,tex='\\delta^{'+('+' if sign>0 else '-')+'}',size=size,fill=PLUS if sign>0 else MINUS,weight=700)
def X_(el,x,y,lp=(),**k): return A_(el,x,y,lp=list(lp),**k)
def hyd(x,y,S=24,lpd=('u','d','r'),fcp='u',name='OH-',left=True):
    """수산화 이온 H–O(−): H 왼쪽"""
    a=[H_(x-0.62*S*(1 if left else -1)*1.6,y),O_(x,y,list(lpd),fc=-1,fcp=fcp)]
    return M(a,[(0,1,1,'l')],'HO',S=S,name=name)
def lpxy(x,y,d,el='O',S=24):
    ux,uy=_dir(d); bd=_b(el,S,ux,uy)+0.26*S; return x+ux*bd,y+uy*bd
def fish(x1,y1,x2,y2,bend=30,col=INK,w=2.4,up=True):
    """한쪽 미늘 굽은 화살표(전자 1개)"""
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); px,py=-dy/n,dx/n
    cx,cy=mx+px*bend,my+py*bend; tx,ty=x2-cx,y2-cy; tn=math.hypot(tx,ty); tx,ty=tx/tn,ty/tn; qx,qy=-ty,tx
    sg=1 if up else -1
    head=P([(x2-tx*11+qx*6*sg,y2-ty*11+qy*6*sg),(x2,y2)],col,w,extra='stroke-linecap="round"')
    return f'<path d="M{f(x1)} {f(y1)} Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'+head
def trim(x1,y1,x2,y2,r1,r2):
    dx,dy=x2-x1,y2-y1; n=math.hypot(dx,dy); ux,uy=dx/n,dy/n
    return x1+ux*r1,y1+uy*r1,x2-ux*r2,y2-uy*r2
def wdg(x1,y1,x2,y2,r1=12,r2=14,kind='w',w=12):
    a=trim(x1,y1,x2,y2,r1,r2)
    if kind=='w': return wedge(*a,w)
    if kind=='h': return hashw(*a,w)
    return L(*a,INK,2.6,extra='stroke-linecap="round"')
def cond(x,y,tex,size=22,anchor='middle',fill=None,weight=None): return T(x,y,tex='\\ce{'+tex+'}',size=size,anchor=anchor,fill=fill,weight=weight)
def lab(x,y,t,size=19,fill=MUTED,anchor='middle',weight=None,halo=False): return T(x,y,mix=t,size=size,fill=fill,anchor=anchor,weight=weight,halo=halo)
def plus(x,y,size=26): return T(x,y+9,tex='+',size=size)
def tsb(x1,y1,x2,y2,size=26):
    """전이 상태 괄호 + ‡"""
    s=P([(x1+10,y1),(x1,y1),(x1,y2),(x1+10,y2)],INK,2.2)+P([(x2-10,y1),(x2,y1),(x2,y2),(x2-10,y2)],INK,2.2)
    return s+T(x2+6,y1+size*0.6,tex='\\ddagger',size=size,anchor='start')
def ecurve(pts,col=INK,w=3,dash=None,extra=''):
    """극점 목록을 수평 접선 3차 베지어로 잇는 에너지 곡선"""
    d=f'M{f(pts[0][0])} {f(pts[0][1])}'
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        h=(x2-x1)/2; d+=f' C{f(x1+h)} {f(y1)} {f(x2-h)} {f(y2)} {f(x2)} {f(y2)}'
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(f' {extra}' if extra else '')+'/>'
def eaxes(x0,y0,x1,y1,yl='에너지',xl='반응 경로',size=19):
    s=A(x0,y0,x0,y1,'muted',2)+A(x0,y0,x1,y0,'muted',2)
    s+=T(x0+8,y1+10,mix=yl,size=size,anchor='start',fill=MUTED)+T(x1-4,y0+26,mix=xl,size=size,anchor='end',fill=MUTED)
    return s
def eadim(x,y1,y2,lab_='E_\\mathrm{a}',size=20,side=1):
    s=L(x,y1,x,y2,EQUI,2)+P([(x-5,y2+9),(x,y2),(x+5,y2+9)],EQUI,2)+P([(x-5,y1-9),(x,y1),(x+5,y1-9)],EQUI,2)
    return s+T(x+8*side,(y1+y2)/2+7,tex=lab_,size=size,anchor='start' if side>0 else 'end',fill=EQUI,halo=True)
def seg(x1,x2,y,col=INK,w=3,dash=None): return L(x1,y,x2,y,col,w,dash=dash)

# ═══ S1 표지: SN2 뒤쪽 공격
def sn2fig(nu='OH',S=28,x0=0,y0=0,lab_=True,name='표지'):
    s=[]; y=y0+200; cx=x0+300; bx=cx+92
    if nu=='OH':
        s.append(hyd(x0+130,y,S=S,name=name+' OH-'))
        sx,sy=lpxy(x0+130,y,'r','O',S); s.append(DRAW(curved(sx+4,sy-6,cx-34,y-12,bend=-44),.4))
    a=[Cc(cx,y),H_(cx-22,y-62),G_('CH3',cx-58,y+40),G_('C2H5',cx-14,y+76),X_('Br',bx,y,['u','d','r'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'n'),(0,3,1,'n'),(0,4,1,'l')],'C4H9Br',S=S,name=name+' RBr'))
    s.append(wdg(cx,y,cx-58,y+40,14,30,'h',13)); s.append(wdg(cx,y,cx-14,y+76,14,18,'w',13))
    s.append(DRAW(curved(cx+44,y-6,bx-8,y-26,bend=-22),1.0))
    if lab_:
        s.append(dlab(cx+16,y-40,1,22)); s.append(lab(x0+110,y-64,'친핵체',20,MINUS)); s.append(lab(bx+10,y+72,'이탈기',20,MUTED))
    return ''.join(s)
def cover():
    s=[sn2fig(S=28,x0=-40)]
    s.append(T(270,372,tex='\\mathrm{S_N2}',size=30,weight=700)); s.append(lab(270,410,'뒤쪽에서 공격 → 입체 배열 반전',21,INK))
    return svg('0 0 540 440',520,'수산화 이온이 2-브로모뷰테인의 브로민 반대편에서 탄소를 공격하는 SN2 반응과 굽은 화살표',s,cls='cover-fig')
FIG['COVER']=cover()

# ═══ S3 생각 열기: 같은 기질, 두 생성물
def openfig():
    s=[]; cx,cy=220,150
    s.append(cond(cx,cy+8,'CH3CHBrCH3',28,weight=700)); s.append(lab(cx,cy+44,'2-브로모프로페인'))
    s.append(hlrect(cx+6,cy,38,40))
    g=A(330,cy-20,560,70,'ink',2.6)+lab(430,72,'$\\ce{OH-}$, 물',20,INK)+cond(700,78,'CH3CH(OH)CH3',26)+lab(700,112,'2-프로판올 (치환)',20,FIELD)
    s.append(POP(g,700,70,.3))
    g=A(330,cy+20,560,236,'ink',2.6)+lab(424,250,'$\\ce{OH-}$, 에탄올, 가열',20,INK)+cond(700,244,'CH2=CHCH3',26)+lab(700,278,'프로펜 (제거)',20,BF)
    s.append(POP(g,700,236,.8))
    return svg('0 0 860 300',760,'2-브로모프로페인과 수산화 이온이 조건에 따라 2-프로판올 또는 프로펜이 되는 모습',s)
FIG['OPEN']=openfig()

# ═══ S4 굽은 화살표 세 칸
def arr1():
    S=24; s=[]; y=60
    s.append(hyd(70,y,S=S,name='c1 OH-'))
    s.append(M([A_('H',190,y,oct=0,fc=1,fcp='ur')],[],'H',S=S,name='c1 H+'))
    sx,sy=lpxy(70,y,'r'); s.append(DRAW(curved(sx+3,sy-4,180,y-8,bend=-30),.4))
    s.append(harrow(120,170,150))
    a=[O_(250,140,[135,45]),H_(214,170),H_(286,170)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l')],'H2O',S=S,name='c1 H2O'))
    rxn(['c1 OH-','c1 H+'],['c1 H2O'],'S4-1')
    return svg('0 0 320 200',300,'수산화 이온의 비공유 전자쌍이 수소 이온으로 이동하여 물이 생김',s)
def tbu(x,y,S,cat=False,X=None,name='',XL=60):
    """(CH3)3C–X 또는 (CH3)3C+ : 가운데 C 명시, CH3 셋은 축약"""
    a=[A_('C',x,y,**({'oct':6,'fc':1,'fcp':'ur'} if cat else {})),G_('CH3',x-56,y),G_('CH3',x,y-46),G_('CH3',x,y+46)]
    b=[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')]
    if X: a.append(X_(X,x+XL,y,['u','d','r'])); b.append((0,4,1,'l'))
    return a,b
def arr2():
    S=22; s=[]
    a,b=tbu(90,80,S,X='Br'); s.append(M(a,b,'C4H9Br',S=S,name='c2 RBr'))
    s.append(DRAW(curved(122,74,146,62,bend=-14),.4))
    s.append(harrow(40,80,190))
    a,b=tbu(160,190,S,cat=True); s.append(M(a,b,'C4H9',S=S,name='c2 R+'))
    s.append(plus(214,190)); s.append(M([X_('Br',262,190,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='c2 Br-'))
    rxn(['c2 RBr'],['c2 R+','c2 Br-'],'S4-2')
    return svg('0 0 320 256',300,'탄소-브로민 결합의 전자쌍이 브로민으로 이동하여 탄소 양이온과 브로민화 이온이 생김',s)
def arr3():
    S=22; s=[]; y=62
    a=[Cc(70,y),Cc(130,y),H_(40,y-40),H_(40,y+40),H_(160,y-40),H_(160,y+40)]
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],'C2H4',S=S,name='c3 C2H4'))
    s.append(M([A_('H',240,y,oct=0,fc=1,fcp='ur')],[],'H',S=S,name='c3 H+'))
    s.append(DRAW(curved(100,y-10,230,y-10,bend=-36),.4))
    s.append(harrow(40,80,168))
    a=[G_('CH3',140,168),A_('C',206,168,oct=6,fc=1,fcp='ur'),H_(240,136),H_(240,200)]
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l'),(1,3,1,'l')],'C2H5',S=S,name='c3 cat'))
    rxn(['c3 C2H4','c3 H+'],['c3 cat'],'S4-3')
    return svg('0 0 320 220',300,'에틸렌의 π 결합 전자쌍이 수소 이온으로 이동하여 탄소 양이온이 생김',s)
FIG['ARR1']=arr1(); FIG['ARR2']=arr2(); FIG['ARR3']=arr3()

# ═══ S5 친핵성과 염기성
def nucfig():
    S=24; s=[]
    s.append(hyd(96,160,S=S,lpd=('u','d','r'),name='n OH-')); s.append(lab(86,214,'친핵체 = 염기',20,MINUS))
    a=[G_('H3C',390,96),X_('Br',466,96,['u','d','r'])]
    s.append(M(a,[(0,1,1,'l')],'CH3Br',S=S,name='n CH3Br')); s.append(dlab(402,62,1,20)); s.append(dlab(466,54,-1,20))
    s.append(M([A_('H',400,236,oct=0,fc=1,fcp='ur')],[],'H',S=S,name='n H+'))
    sx,sy=lpxy(96,160,'r')
    s.append(DRAW(curved(sx+4,sy-6,366,104,bend=-26),.3)); s.append(DRAW(curved(sx+4,sy+6,386,232,bend=26),.9))
    s.append(lab(300,30,'탄소에 전자쌍 → 친핵성',20,INK)); s.append(lab(300,290,'수소 이온에 전자쌍 → 염기성',20,INK))
    return svg('0 0 520 310',500,'수산화 이온이 브로모메테인의 탄소에 전자쌍을 주면 친핵성, 수소 이온에 주면 염기성',s)
FIG['NUC']=nucfig()

# ═══ S7 치환과 제거: α·β
def subelim():
    S=24; s=[]; cb,ca,y=200,290,150
    a=[Cc(cb,y),Cc(ca,y),H_(cb,y-58),H_(cb-58,y),H_(cb,y+58),H_(ca,y-58),H_(ca,y+58),X_('Br',ca+86,y,['u','d','r'])]
    s.append(hlrect(cb,y-58,34,34))
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(1,5,1,'l'),(1,6,1,'l'),(1,7,1,'l')],'C2H5Br',S=S,name='bromoethane'))
    s.append(lab(cb-24,y-22,'β',21,INK,weight=700)); s.append(lab(ca+24,y+36,'α',21,INK,weight=700))
    s.append(dlab(ca+26,y-24,1,20)); s.append(dlab(ca+86,y-34,-1,20))
    g=T(118,264,tex='\\mathrm{Nu}^-',size=24,fill=MINUS)+curved(140,256,ca-16,y+20,bend=40)+lab(206,286,'치환: α 탄소 공격',19,FIELD)
    s.append(POP(g,180,240,.3))
    g=T(80,52,tex='\\mathrm{B}^-',size=24,fill=MINUS)+curved(100,44,cb-18,y-64,bend=-22)+lab(92,92,'제거: β 수소',19,BF)
    s.append(POP(g,110,60,.8))
    return svg('0 0 460 300',440,'브로모에테인의 α 탄소와 β 수소. 친핵체가 α 탄소를 공격하면 치환, 염기가 β 수소를 떼어 내면 제거',s)
FIG['SUBEL']=subelim()

# ═══ S9 SN2 메커니즘과 발덴 반전 (2-브로모뷰테인)
def chir(c,groups):
    """groups: [(우선순위, (x,y,z))] (수학 좌표, y 위) → 'R'/'S'"""
    g=sorted(groups); a,b,cc,d=[v for _,v in g]
    def sub(u,v): return tuple(p-q for p,q in zip(u,v))
    def cross(u,v): return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    t=sum(p*q for p,q in zip(sub(a,d),cross(sub(b,d),sub(cc,d))))
    return 'R' if t<0 else 'S'
def ang(t,z=0): return (math.cos(math.radians(t)),math.sin(math.radians(t)),z)
# 시험: (R)-CHFClBr 기준 확인 — 우선 Br>Cl>F>H, H 뒤쪽(z−), Br·Cl·F 시계 방향이면 R
assert chir(None,[(1,ang(90,0.3)),(2,ang(-30,0.3)),(3,ang(210,0.3)),(4,(0,0,-1))])=='R'
REAC=[(1,ang(0)),(2,ang(250,0.7)),(3,ang(210,-0.7)),(4,ang(110))]   # Br, C2H5(쐐기), CH3(점선), H
PROD=[(1,ang(180)),(2,ang(290,0.7)),(3,ang(330,-0.7)),(4,ang(70))]  # OH, C2H5, CH3, H
assert chir(None,REAC)=='S' and chir(None,PROD)=='R', (chir(None,REAC),chir(None,PROD))
def rbr(cx,y,S,X='Br',name='S9 RBr'):
    s=[]; L0=60
    p=lambda t:(cx+L0*math.cos(math.radians(t)),y-L0*math.sin(math.radians(t)))
    (hx,hy),(mx,my),(ex,ey)=p(110),p(210),p(250)
    a=[Cc(cx,y),H_(hx,hy),G_('CH3',mx-8,my),G_('C2H5',ex-4,ey+12),X_(X,cx+84,y,['u','d','r'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'n'),(0,3,1,'n'),(0,4,1,'l')],'C4H9'+X,S=S,name=name))
    s.append(wdg(cx,y,mx-8,my,13,28,'h',12)); s.append(wdg(cx,y,ex-4,ey+12,13,16,'w',12))
    return ''.join(s)
def roh(cx,y,S,Nu='OH',name='S9 ROH'):
    s=[]; L0=60
    p=lambda t:(cx+L0*math.cos(math.radians(t)),y-L0*math.sin(math.radians(t)))
    (hx,hy),(mx,my),(ex,ey)=p(70),p(330),p(290)
    inner=[]
    a=[Cc(cx,y),H_(hx,hy),G_('CH3',mx+8,my),G_('C2H5',ex+4,ey+12)]
    b=[(0,1,1,'l'),(0,2,1,'n'),(0,3,1,'n')]
    if Nu=='OH': a+=[O_(cx-70,y,['u','d']),H_(cx-120,y)]; b+=[(0,4,1,'l'),(4,5,1,'l')]; want='C4H10O'
    else: a+=[X_(Nu,cx-80,y,['u','d','l'])]; b+=[(0,4,1,'l')]; want='C4H9'+Nu
    body=M(a,b,want,S=S,name=name)+wdg(cx,y,mx+8,my,13,28,'h',12)+wdg(cx,y,ex+4,ey+12,13,16,'w',12)
    return body
def sn2mech():
    S=24; s=[]; y=150
    s.append(hyd(70,y,S=S,name='S9 OH-'))
    s.append(rbr(250,y,S))
    sx,sy=lpxy(70,y,'r'); s.append(DRAW(curved(sx+4,sy-6,226,y-10,bend=-40),.3)); s.append(DRAW(curved(288,y-6,322,y-24,bend=-18),.8))
    s.append(lab(52,y-58,'친핵체',19,MINUS)); s.append(lab(250,y+118,'(S)-2-브로모뷰테인',19,MUTED))
    s.append(harrow(388,424,y))
    # 전이 상태
    tx=560
    a=[Cc(tx,y),O_(tx-80,y,['u','d']),H_(tx-130,y),X_('Br',tx+84,y,['u','d','r']),H_(tx,y-58),G_('CH3',tx-36,y+52),G_('C2H5',tx+40,y+56)]
    s.append(lewis(a,[(0,1,1,'h'),(1,2,1,'l'),(0,3,1,'h'),(0,4,1,'l'),(0,5,1,'n'),(0,6,1,'n')],S=S,check=False))
    s.append(wdg(tx,y,tx-36,y+52,13,22,'h',12)); s.append(wdg(tx,y,tx+40,y+56,13,20,'w',12))
    s.append(dlab(tx-80,y-38,-1,19)); s.append(dlab(tx+84,y-40,-1,19))
    s.append(tsb(tx-156,y-78,tx+124,y+96)); s.append(lab(tx-16,y+122,'전이 상태: 세 원자단이 한 평면',19,MUTED))
    s.append(harrow(708,744,y))
    g=an('scale',roh(880,y,S),**{'from':'-1,1','o':f'880,{y}','dur':'1.1','delay':'1.4','ease':'back'})
    s.append(g); s.append(lab(860,y+118,'(R)-2-뷰탄올',19,MUTED))
    s.append(plus(978,y)); s.append(M([X_('Br',1016,y,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='S9 Br-'))
    rxn(['S9 OH-','S9 RBr'],['S9 ROH','S9 Br-'],'S9')
    return svg('0 0 1060 290',1040,'수산화 이온이 브로민 반대편에서 탄소를 공격하여 전이 상태를 지나 입체 배열이 반전된 2-뷰탄올이 되는 SN2 메커니즘',s)
FIG['SN2']=sn2mech()

# ═══ S10 SN2 에너지 도표 + 입체 장애
def esn2(W=440,H=300,small=False):
    s=[]; x0,y0=50,H-40
    s.append(eaxes(x0,y0,W-14,24))
    pts=[(x0+20,y0-90),(x0+(W-x0)/2-10,58),(W-40,y0-40)]
    s.append(DRAW(ecurve(pts),.2,'1.2'))
    s.append(seg(x0+6,x0+70,y0-90)); s.append(seg(W-100,W-24,y0-40))
    s.append(lab(x0+44,y0-104,'반응물',19,INK)); s.append(lab(W-62,y0-54,'생성물',19,INK))
    s.append(lab(pts[1][0],44,'전이 상태 ‡',19,INK)); s.append(eadim(x0+96,y0-90,62,side=1))
    s.append(lab(pts[1][0]+20,y0-6,'중간체 없음 · 언덕 1개',19,MUTED))
    return svg(f'0 0 {W} {H}',W,'SN2 반응의 에너지 도표: 전이 상태 하나, 중간체 없음',s)
FIG['ESN2']=esn2()
def crowd():
    s=[]; k=0.8; rH,rC,rB=18*k,24*k,32*k
    sets=[('메틸','HHH','CH3Br'),('1차','CHH','RCH2Br'),('2차','CCH','R2CHBr'),('3차','CCC','R3CBr')]
    for i,(nm,sub,fm) in enumerate(sets):
        x=70+i*130; y=96; g=[]
        pos=[(x-22,y-34),(x-36,y+8),(x-12,y+36)]
        for (px,py),e in zip(pos,sub): g.append(L(x,y,px,py,BOND,6,extra='stroke-linecap="round"'))
        g.append(L(x,y,x+40,y,BOND,6,extra='stroke-linecap="round"'))
        g.append(atom(x+40,y,rB,'Br','-'))
        for (px,py),e in zip(pos,sub): g.append(atom(px,py,rC if e=='C' else rH,'C' if e=='C' else 'H','-'))
        g.append(atom(x,y,rC,'C','-'))
        ln={0:44,1:40,2:22,3:10}[i]
        g.append(A(x-98+ (0 if i<2 else 18),y,x-98+(0 if i<2 else 18)+ln,y,'minus',3))
        if i==3: g.append(L(x-74,y-9,x-62,y+9,PLUS,3)+L(x-74,y+9,x-62,y-9,PLUS,3))
        g.append(lab(x,y+86,nm,20,INK,weight=700))
        s.append(''.join(g))
    s.append(A(40,214,540,214,'muted',2)); s.append(lab(60,240,'빠름',19,FIELD,anchor='start')); s.append(lab(530,240,'거의 없음',19,PLUS,anchor='end'))
    s.append(lab(290,240,'(크기 비례 아님)',19,MUTED))
    s.append(lab(290,272,'흰 공 H · 검은 공 C(알킬기) · 적갈색 공 Br · 파란 화살표 친핵체',19,MUTED))
    return svg('0 0 580 290',560,'메틸, 1차, 2차, 3차 브로민화 알킬에서 친핵체가 뒤쪽으로 다가가는 길이 알킬기로 막히는 모습',s)
FIG['CROWD']=crowd()

# ═══ S11 용매: 양성자성 용매가 친핵체를 둘러쌈
def solv():
    s=[]
    cx,cy=120,110
    for k in range(5):
        t=math.radians(90+72*k); ox,oy=cx+70*math.cos(t),cy-70*math.sin(t)
        hx,hy=cx+46*math.cos(t),cy-46*math.sin(t)
        t2=t+math.radians(105); h2x,h2y=ox+26*math.cos(t2),oy-26*math.sin(t2)
        s.append(L(cx+22*math.cos(t),cy-22*math.sin(t),hx-8*math.cos(t),hy+8*math.sin(t),MUTED,2,dash='4 4'))
        s.append(L(ox,oy,hx,hy,BOND,5)); s.append(L(ox,oy,h2x,h2y,BOND,5))
        s.append(atom(ox,oy,12,'O','-')); s.append(atom(hx,hy,8,'H','-')); s.append(atom(h2x,h2y,8,'H','-'))
    s.append(C(cx,cy,20,MINUS,2,fill='#E3EEFB')); s.append(T(cx,cy+8,tex='\\mathrm{Nu}^-',size=20,fill=MINUS))
    s.append(lab(cx,212,'양성자성 용매(물)',19,INK)); s.append(lab(cx,236,'수소 결합으로 둘러쌈',19,MUTED))
    s.append(C(330,cy,20,MINUS,2,fill='#E3EEFB')); s.append(T(330,cy+8,tex='\\mathrm{Nu}^-',size=20,fill=MINUS))
    s.append(lab(330,212,'비양성자성 용매',19,INK)); s.append(lab(330,236,'맨몸 → 반응성 큼',19,MUTED))
    return svg('0 0 430 250',380,'양성자성 용매의 물 분자가 친핵체를 수소 결합으로 둘러싼 모습과 비양성자성 용매의 맨몸 친핵체',s)
FIG['SOLV']=solv()

# ═══ S13 SN1 세 단계 카드
def water(x,y,S,name,lpd=(135,45),hd=1):
    a=[O_(x,y,list(lpd)),H_(x-30,y+30*hd),H_(x+30,y+30*hd)]
    return M(a,[(0,1,1,'l'),(0,2,1,'l')],'H2O',S=S,name=name)
def sn1a():
    S=22; s=[]
    a,b=tbu(90,74,S,X='Br'); s.append(M(a,b,'C4H9Br',S=S,name='1a RBr'))
    s.append(DRAW(curved(122,68,146,56,bend=-14),.4))
    s.append(harrow(44,84,200)); s.append(lab(64,184,'느림',19,PLUS,weight=700))
    a,b=tbu(170,200,S,cat=True); s.append(M(a,b,'C4H9',S=S,name='1a R+'))
    s.append(plus(226,200)); s.append(M([X_('Br',276,200,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='1a Br-'))
    rxn(['1a RBr'],['1a R+','1a Br-'],'S13-1')
    return svg('0 -12 344 282',310,'1단계: 탄소-브로민 결합이 끊어져 탄소 양이온과 브로민화 이온이 생김(느림)',s)
def sn1b():
    S=22; s=[]
    a,b=tbu(80,74,S,cat=True); s.append(M(a,b,'C4H9',S=S,name='1b R+'))
    s.append(plus(140,74)); s.append(water(210,68,S,'1b H2O',lpd=('l',90)))
    sx,sy=lpxy(210,68,'l'); s.append(DRAW(curved(sx-3,sy,96,52,bend=-22),.4))
    s.append(harrow(44,84,186)); s.append(lab(64,170,'빠름',19,FIELD,weight=700))
    a=[A_('C',160,186),G_('CH3',104,186),G_('CH3',160,140),G_('CH3',160,232),O_(222,186,['u'],fc=1,fcp='ur'),H_(262,160),H_(262,212)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(4,5,1,'l'),(4,6,1,'l')],'C4H11O',S=S,name='1b ROH2+'))
    rxn(['1b R+','1b H2O'],['1b ROH2+'],'S13-2')
    return svg('0 -12 344 272',310,'2단계: 물 분자의 비공유 전자쌍이 탄소 양이온을 공격',s)
def sn1c():
    S=22; s=[]
    a=[A_('C',70,74),G_('CH3',16,74),G_('CH3',70,30),G_('CH3',70,118),O_(130,74,['d'],fc=1,fcp='dl'),H_(166,50),H_(166,100)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(4,5,1,'l'),(4,6,1,'l')],'C4H11O',S=S,name='1c ROH2+'))
    s.append(water(262,50,S,'1c H2O',lpd=('l',90)))
    sx,sy=lpxy(262,50,'l'); s.append(DRAW(curved(sx-3,sy,178,36,bend=-14),.4))
    s.append(DRAW(curved(148,62,136,60,bend=-12),.9))
    s.append(harrow(44,84,186)); s.append(lab(64,170,'빠름',19,FIELD,weight=700))
    a=[A_('C',150,186),G_('CH3',96,186),G_('CH3',150,142),G_('CH3',150,230),O_(206,186,['u','d']),H_(240,186)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(4,5,1,'l')],'C4H10O',S=S,name='1c ROH'))
    s.append(plus(262,186)); s.append(cond(312,194,'H3O+',22))
    SPEC['1c H3O+']=(formula('H3O'),1)
    rxn(['1c ROH2+','1c H2O'],['1c ROH','1c H3O+'],'S13-3')
    return svg('-14 -12 358 272',330,'3단계: 다른 물 분자가 양성자를 떼어 내어 알코올과 하이드로늄 이온이 생김',s)
FIG['SN1A']=sn1a(); FIG['SN1B']=sn1b(); FIG['SN1C']=sn1c()

# ═══ S14 SN1 에너지 도표
def esn1():
    W,H=560,330; s=[]; x0,y0=50,H-36
    s.append(eaxes(x0,y0,W-12,22))
    R=(x0+24,y0-110); T1=(150,52); I1=(230,160); T2=(300,118); I2=(370,172); T3=(430,140); P_=(W-36,y0-60)
    s.append(DRAW(ecurve([R,T1,I1,T2,I2,T3,P_]),.2,'1.6'))
    s.append(seg(x0+6,x0+56,R[1])); s.append(seg(W-80,W-20,P_[1]))
    s.append(lab(x0+30,R[1]-14,'반응물',19,INK)); s.append(lab(W-50,P_[1]+30,'생성물',19,INK))
    s.append(C(I1[0],I1[1],6,EQUI,2,fill=EQUI)); s.append(lab(I1[0],I1[1]+34,'탄소 양이온',19,EQUI,weight=700)); s.append(lab(I1[0],I1[1]+56,'(중간체)',19,EQUI))
    s.append(C(I2[0],I2[1],6,EQUI,2,fill=EQUI)); s.append(lab(I2[0]+10,I2[1]+34,'양성자가 붙은',19,EQUI)); s.append(lab(I2[0]+10,I2[1]+56,'알코올',19,EQUI))
    s.append(eadim(x0+70,R[1],T1[1]+4,side=-1))
    s.append(lab(T1[0]+50,T1[1]-14,'속도 결정 단계',19,PLUS,weight=700))
    return svg(f'0 0 {W} {H}',W,'SN1 반응의 에너지 도표: 첫 언덕이 가장 높은 속도 결정 단계, 골짜기에 탄소 양이온 중간체',s)
FIG['ESN1']=esn1()

# ═══ S15 탄소 양이온의 구조
def cation():
    s=[]; cx,cy=230,160
    s.append(f'<ellipse cx="{cx}" cy="{cy-62}" rx="26" ry="56" fill="{GRAV}" fill-opacity=".12" stroke="{GRAV}" stroke-width="2" stroke-dasharray="6 5"/>')
    s.append(f'<ellipse cx="{cx}" cy="{cy+62}" rx="26" ry="56" fill="{GRAV}" fill-opacity=".12" stroke="{GRAV}" stroke-width="2" stroke-dasharray="6 5"/>')
    a=[A_('C',cx,cy,oct=6,fc=1,fcp='dl'),G_('CH3',cx-92,cy),G_('CH3',cx+84,cy-24),G_('CH3',cx+84,cy+30)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'n'),(0,3,1,'n')],'C4H9',S=24,name='planar cation'))
    s.append(wdg(cx,cy,cx+84,cy-24,12,26,'h',12)); s.append(wdg(cx,cy,cx+84,cy+30,12,26,'w',12))
    s.append(lab(cx+42,cy-108,'빈 p 오비탈',19,MUTED,anchor='start'))
    g=cond(70,58,'H2O',22,fill=MINUS)+curved(92,62,cx-22,cy-80,bend=-20)+lab(70,30,'위에서 50 %',19,INK)
    s.append(POP(g,80,58,.3))
    g=cond(70,290,'H2O',22,fill=MINUS)+curved(92,282,cx-22,cy+80,bend=20)+lab(70,318,'아래에서 50 %',19,INK)
    s.append(POP(g,80,290,.7))
    return svg('0 0 400 330',380,'평면 삼각형 탄소 양이온과 빈 p 오비탈, 물 분자가 위와 아래에서 같은 확률로 공격',s)
FIG['CATION']=cation()
def catrow():
    s=[]; items=[('CH3+','메틸'),('RCH2+','1차'),('R2CH+','2차'),('R3C+','3차')]
    for i,(t,n) in enumerate(items):
        x=80+i*170; s.append(cond(x,44,t,26)); s.append(lab(x,78,n,19))
        if i<3: s.append(T(x+85,52,tex='<',size=28,fill=MUTED))
    s.append(A(40,104,620,104,'field',3)); s.append(lab(330,132,'안정성 증가 (알킬기가 많을수록)',19,FIELD))
    return svg('0 0 660 140',640,'탄소 양이온의 안정성: 메틸 < 1차 < 2차 < 3차',s)
FIG['CATROW']=catrow()

# ═══ S17 병목
def neck():
    s=[]; y=110
    s.append(P([(20,40),(170,40),(200,92),(320,92),(350,40),(500,40)],MUTED,2.5))
    s.append(P([(20,180),(170,180),(200,128),(320,128),(350,180),(500,180)],MUTED,2.5))
    for i,x in enumerate([50,90,130,60,110,150,400,440]):
        yy=y+(-40 if i%3==0 else (40 if i%3==1 else 0))
        if 200<x<320: yy=y
        s.append(C(x,yy,9,INK,1.5,fill='#DDEEF8'))
    for x in (215,245,275,305): s.append(C(x,y,9,INK,1.5,fill='#DDEEF8'))
    s.append(lab(95,218,'빠른 단계',19,FIELD)); s.append(lab(260,218,'가장 느린 단계',19,PLUS,weight=700)); s.append(lab(425,218,'빠른 단계',19,FIELD))
    s.append(A(220,72,300,72,'ink',2)); s.append(lab(260,62,'전체 흐름을 정함',19,INK))
    return svg('0 0 520 240',480,'가장 좁은 구간이 전체 흐름을 정하는 것처럼 가장 느린 단계가 반응 속도를 정한다',s)
FIG['NECK']=neck()

# ═══ S18 자이체프
def zaitsev():
    s=[]
    s.append(cond(150,150,'CH3CH2CHBrCH3',26,weight=700)); s.append(lab(150,184,'2-브로모뷰테인',19))
    s.append(lab(150,108,'+ $\\ce{CH3CH2O-}$',20,INK))
    s.append(A(270,140,400,80,'ink',2.6)); s.append(A(270,160,400,220,'ink',2.6))
    s.append(hlrect(520,72,64,40)); s.append(cond(520,80,'CH3CH=CHCH3',26)); s.append(lab(520,112,'2-뷰텐 (주생성물)',19,BF))
    s.append(cond(520,228,'CH2=CHCH2CH3',26)); s.append(lab(520,260,'1-뷰텐',19,MUTED))
    x0=690; Wb=260
    s.append(an('scale',f'<rect x="{x0}" y="56" width="{f(Wb*.81)}" height="30" rx="5" fill="{BF}" fill-opacity=".55"/>',**{'from':'0,1','o':f'{x0},71','dur':'1','delay':'.4'}))
    s.append(lab(x0+Wb*.81+10,78,'약 81 %',20,INK,anchor='start',weight=700))
    s.append(an('scale',f'<rect x="{x0}" y="204" width="{f(Wb*.19)}" height="30" rx="5" fill="{GRAV}" fill-opacity=".55"/>',**{'from':'0,1','o':f'{x0},219','dur':'1','delay':'.6'}))
    s.append(lab(x0+Wb*.19+10,226,'약 19 %',20,INK,anchor='start',weight=700))
    return svg('0 40 1000 236',940,'2-브로모뷰테인과 에탄올산 이온의 제거 반응에서 2-뷰텐 약 81퍼센트, 1-뷰텐 약 19퍼센트',s)
FIG['ZAIT']=zaitsev()

# ═══ S19 E2 (anti 동일 평면)
def e2mech():
    S=24; s=[]; cb,ca,y=300,390,160
    a=[G_('CH3CH2',120,64),O_(196,64,['u','d','r'],fc=-1,fcp='ul')]
    s.append(M(a,[(0,1,1,'l')],'C2H5O',S=S,name='E2 EtO-'))
    p=lambda c,t,L0=58:(c+L0*math.cos(math.radians(t)),y-L0*math.sin(math.radians(t)))
    hb=p(cb,90); h1=p(cb,200); h2=p(cb,240); h3=p(ca,20); h4=p(ca,60); br=(ca,y+70)
    a=[Cc(cb,y),Cc(ca,y),H_(*hb),H_(*h1),H_(*h2),H_(*h3),H_(*h4),X_('Br',*br,['l','r','d'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'n'),(0,4,1,'n'),(1,5,1,'n'),(1,6,1,'n'),(1,7,1,'l')],'C2H5Br',S=S,name='E2 RBr'))
    s.append(wdg(cb,y,*h1,12,12,'w',11)); s.append(wdg(cb,y,*h2,12,12,'h',11)); s.append(wdg(ca,y,*h3,12,12,'h',11)); s.append(wdg(ca,y,*h4,12,12,'w',11))
    sx,sy=lpxy(196,64,'r')
    s.append(DRAW(curved(sx+4,sy+2,hb[0]-14,hb[1]-8,bend=-18),.3))
    s.append(DRAW(curved(cb+8,y-34,(cb+ca)/2,y-10,bend=-14),.8))
    s.append(DRAW(curved(ca+8,y+30,ca+22,y+50,bend=-12),1.3))
    s.append(lab(196,112,'염기',19,MINUS))
    s.append(harrow(470,520,y))
    a=[Cc(590,y),Cc(650,y),H_(560,y-40),H_(560,y+40),H_(680,y-40),H_(680,y+40)]
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],'C2H4',S=S,name='E2 C2H4'))
    s.append(plus(712,y))
    a=[G_('CH3CH2',770,y),O_(836,y,['u','d']),H_(876,y)]
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l')],'C2H6O',S=S,name='E2 EtOH'))
    s.append(plus(904,y)); s.append(M([X_('Br',946,y,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='E2 Br-'))
    rxn(['E2 EtO-','E2 RBr'],['E2 C2H4','E2 EtOH','E2 Br-'],'S19')
    return svg('0 30 1000 224',940,'에탄올산 이온이 β 수소를 떼어 내는 순간 탄소-탄소 2중 결합이 생기고 브로민화 이온이 떨어지는 E2 메커니즘',s)
FIG['E2']=e2mech()

# ═══ S20 E1과 SN1 경쟁
def e1fig():
    S=22; s=[]
    a,b=tbu(80,150,S,X='Cl',XL=58); s.append(M(a,b,'C4H9Cl',S=S,name='E1 RCl'))
    s.append(DRAW(curved(110,144,132,132,bend=-12),.3))
    s.append(harrow(170,214,150)); s.append(lab(192,134,'느림',19,PLUS,weight=700))
    cx,cy,bx=310,150,384
    a=[A_('C',cx,cy,oct=6,fc=1,fcp='d'),G_('CH3',cx-46,cy-40),G_('CH3',cx-46,cy+40),Cc(bx,cy),H_(bx,cy-48),H_(bx+48,cy),H_(bx,cy+50)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(3,4,1,'l'),(3,5,1,'l'),(3,6,1,'l')],'C4H9',S=S,name='E1 R+'))
    SPEC['E1 Cl-']=(formula('Cl'),-1); rxn(['E1 RCl'],['E1 R+','E1 Cl-'],'S20-1')
    s.append(water(cx,42,S,'E1 H2O a',lpd=(270,180),hd=-1))
    s.append(DRAW(curved(cx+2,62,cx+2,cy-18,bend=-12),.9))
    s.append(water(bx+110,cy+82,S,'E1 H2O b',lpd=(180,90)))
    sx,sy=lpxy(bx+110,cy+82,'l',S=S); s.append(DRAW(curved(sx-3,sy,bx+12,cy+56,bend=16),1.3))
    s.append(DRAW(curved(bx-8,cy+30,(cx+bx)/2,cy+8,bend=12),1.7))
    s.append(lab(cx-30,cy+86,'탄소 양이온',19,EQUI,weight=700))
    s.append(harrow(540,600,62)); s.append(lab(570,40,'치환 ($\\mathrm{S_N1}$)',19,FIELD,weight=700))
    s.append(lab(470,62,'물이 양이온 공격',19,INK))
    s.append(cond(710,70,'(CH3)3COH',24)); s.append(lab(710,102,'2-메틸-2-프로판올',19))
    s.append(harrow(560,620,238)); s.append(lab(590,216,'제거 ($\\mathrm{E1}$)',19,BF,weight=700))
    s.append(cond(730,246,'(CH3)2C=CH2',24)); s.append(lab(730,278,'2-메틸프로펜',19))
    return svg('0 -16 840 300',760,'2-클로로-2-메틸프로페인이 탄소 양이온이 된 뒤 물이 양이온을 공격하면 치환, 이웃 탄소의 수소를 떼어 내면 제거',s)
FIG['E1']=e1fig()

# ═══ S21 E1cB
def e1cb():
    S=20; s=[]; y=128
    def chain(x,stage):
        c4,c3,c2=x+60,x+130,x+200
        a=[G_('CH3',x,y),Cc(c4,y),G_('CH3',c4,y+48)]
        b=[(0,1,1,'l'),(1,2,1,'l')]
        if stage<2:
            a+=[O_(c4,y-50,['l','r']),H_(c4,y-92)]; b+=[(1,3,1,'l'),(3,4,1,'l')]
        else: a+=[G_('_',c4,y-30)]; b+=[]
        i3=len(a); a.append(Cc(c3,y))
        b.append((1,i3,1 if stage<1 or (stage==1) else 2,'l'))
        if stage==0: a+=[H_(c3,y-46),H_(c3,y+46)]; b+=[(i3,i3+1,1,'l'),(i3,i3+2,1,'l')]
        else: a+=[H_(c3,y-46)]; b+=[(i3,i3+1,1,'l')]
        i2=len(a); a.append(Cc(c2,y))
        if stage==1:
            a+=[O_(c2,y-52,['l','u','r'],fc=-1,fcp='ur'),G_('CH3',c2+64,y)]; b+=[(i3,i2,2,'l'),(i2,i2+1,1,'l'),(i2,i2+2,1,'l')]
        else:
            a+=[O_(c2,y-52,[135,45]),G_('CH3',c2+64,y)]; b+=[(i3,i2,1,'l'),(i2,i2+1,2,'l'),(i2,i2+2,1,'l')]
        if stage==2:
            a=[x for x in a if x.get('grp')!='_']
        return a,b
    # 0 반응물
    a,b=chain(30,0); s.append(M(a,b,'C6H12O2',S=S,name='cb R'))
    s.append(hyd(150,222,S=S,lpd=('u','d','r'),name='cb OH-'))
    sx,sy=lpxy(150,222,'r',S=S); s.append(DRAW(curved(sx+2,sy-4,160+14,y+50,bend=-18),.3))
    s.append(DRAW(curved(160-6,y+26,195,y-6,bend=-14),.8)); s.append(DRAW(curved(230,y-30,226,y-58,bend=-14),1.2))
    s.append(lab(150,y+130,'4-하이드록시-4-메틸-2-펜탄온',19,MUTED))
    s.append(harrow(318,350,y))
    # 1 에놀레이트
    a,b=chain(380,1)
    # 단계 ① 생성물: 에놀레이트 + 물 (반응물의 H 하나 → 물)
    s.append(M(a,b,'C6H11O2',S=S,name='cb enolate'))
    SPEC['cb H2O']=(formula('H2O'),0); rxn(['cb R','cb OH-'],['cb enolate','cb H2O'],'S21-1')
    s.append(DRAW(curved(578,y-80,562,y-26,bend=24),1.7)); s.append(DRAW(curved(530,y-8,476,y-8,bend=16),2.1)); s.append(DRAW(curved(440,y-28,418,y-60,bend=-14),2.5))
    s.append(lab(530,y+130,'에놀레이트(공명으로 안정)',19,EQUI,weight=700))
    s.append(harrow(668,700,y))
    # 2 생성물
    a=[G_('CH3',730,y),Cc(790,y),G_('CH3',790,y+48),Cc(860,y),H_(860,y-46),Cc(930,y),O_(930,y-52,[135,45]),G_('CH3',994,y)]
    b=[(0,1,1,'l'),(1,2,1,'l'),(1,3,2,'l'),(3,4,1,'l'),(3,5,1,'l'),(5,6,2,'l'),(5,7,1,'l')]
    s.append(M(a,b,'C6H10O',S=S,name='cb P')); s.append(plus(1034,y)); s.append(T(1074,y+8,tex='\\ce{OH-}',size=22))
    SPEC['cb OH- 2']=(formula('HO'),-1); rxn(['cb enolate'],['cb P','cb OH- 2'],'S21-2')
    s.append(lab(880,y+130,'4-메틸-3-펜텐-2-온',19,MUTED))
    return svg('0 0 1100 272',1040,'수산화 이온이 카보닐기 옆 탄소의 수소를 떼어 에놀레이트가 생기고, 에놀레이트가 이웃 탄소의 수산화 이온을 밀어내는 E1cB 메커니즘',s)
FIG['E1CB']=e1cb()

# ═══ S23 경로 고르기 흐름도
def box(x,y,w,h,txt,kind='n',size=20,g=None):
    col={'n':MUTED,'s':FIELD,'e':BF,'q':INK}[kind]; fill={'n':'#fff','s':'#EAF6EF','e':'#F1ECFA','q':'#F7F8FA'}[kind]
    b=f'<rect x="{f(x-w/2)}" y="{f(y-h/2)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{fill}" stroke="{col}" stroke-width="2"/>'
    lines=txt.split('||'); n=len(lines)
    for i,t in enumerate(lines): b+=T(x,y+size*0.36+(i-(n-1)/2)*size*1.25,mix=t,size=size,weight=700 if kind in 'se' else None)
    return b
def flow():
    s=[]; top=34
    s.append(box(560,top,280,44,'할로젠화 알킬: 기질의 차수는?','q'))
    xs=[90,300,650,990]; names=['메틸','1차','2차','3차']
    for i,(x,n) in enumerate(zip(xs,names)):
        s.append(L(560,top+22,x,104,MUTED,2)); s.append(box(x,118,120,36,n,'q'))
    def br(g,items): return step(items,g)
    s.append(br('b1',[L(90,136,90,180,MUTED,2),box(90,206,130,52,'$\\mathrm{S_N2}$','s',22),lab(90,262,'β 수소 없음',19),lab(90,286,'→ 제거 불가',19)]))
    s.append(br('b2',[L(300,136,230,180,MUTED,2),L(300,136,380,180,MUTED,2),
        box(230,206,120,52,'$\\mathrm{S_N2}$','s',22),lab(230,262,'좋은 친핵체',19),
        box(380,206,120,52,'$\\mathrm{E2}$','e',22),lab(380,262,'부피 큰 강한 염기',19),lab(380,286,'$\\ce{(CH3)3CO-}$',19)]))
    s.append(br('b3',[L(650,136,530,180,MUTED,2),L(650,136,650,180,MUTED,2),L(650,136,770,180,MUTED,2),
        box(530,206,110,52,'$\\mathrm{S_N2}$','s',22),lab(530,262,'$\\ce{I-}$, $\\ce{CN-}$',19),lab(530,286,'비양성자성',19),
        box(650,206,110,52,'$\\mathrm{E2}$','e',22),lab(650,262,'강한 염기',19),
        box(770,206,110,52,'$\\mathrm{S_N1}$·$\\mathrm{E1}$','n',20),lab(770,262,'물·알코올',19),lab(770,286,'(느림)',19)]))
    s.append(br('b4',[L(990,136,930,180,MUTED,2),L(990,136,1054,180,MUTED,2),
        box(930,206,100,52,'$\\mathrm{E2}$','e',22),lab(930,262,'강한 염기',19),
        box(1054,206,116,52,'$\\mathrm{S_N1}$+$\\mathrm{E1}$','n',20),lab(1054,262,'물·알코올',19),lab(1054,286,'(중성)',19),lab(990,320,'$\\mathrm{S_N2}$ 불가(입체 장애)',19,PLUS)]))
    s.append(box(560,354,600,40,'카보닐기 옆 산성 수소 → 차수와 관계없이 $\\mathrm{E1cB}$','n',19))
    return svg('0 0 1120 380',1100,'할로젠화 알킬의 반응 경로 고르기 흐름도: 기질의 차수, 시약의 염기성, 용매의 종류',s)
FIG['FLOW']=flow()

# ═══ S26 (S) → (R)-2-아이오도뷰테인
def sn2I():
    S=22; s=[]; y=110
    s.append(M([X_('I',40,y,['u','d','l','r'],fc=-1,fcp='ul')],[],'I',S=S,name='26 I-'))
    s.append(DRAW(curved(62,y-6,178,y-12,bend=-34),.3)); s.append(DRAW(curved(234,y-6,264,y-22,bend=-16),.7))
    s.append(rbr(200,y,S,name='26 RBr')); s.append(lab(200,y+106,'(S)-2-브로모뷰테인',19,MUTED))
    s.append(harrow(330,376,y))
    s.append(an('scale',roh(500,y,S,Nu='I',name='26 RI'),**{'from':'-1,1','o':f'500,{y}','dur':'1.1','delay':'1.0','ease':'back'}))
    s.append(lab(480,y+106,'(R)-2-아이오도뷰테인',19,MUTED))
    s.append(plus(596,y)); s.append(M([X_('Br',636,y,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='26 Br-'))
    rxn(['26 I-','26 RBr'],['26 RI','26 Br-'],'S26')
    return svg('0 0 680 236',640,'아이오딘화 이온이 (S)-2-브로모뷰테인을 뒤쪽에서 공격하여 반전된 (R)-2-아이오도뷰테인이 생김',s)
FIG['SN2I']=sn2I()

# ═══ S27 윌리엄슨
def wil():
    S=22; s=[]; y=80
    a=[G_('CH3CH2',58,y),O_(126,y,['u','d','r'],fc=-1,fcp='ul')]
    s.append(M(a,[(0,1,1,'l')],'C2H5O',S=S,name='W EtO-'))
    a=[Cc(220,y),H_(198,y-50),H_(178,y+34),H_(212,y+52),X_('I',290,y,['u','d','r'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],'CH3I',S=S,name='W CH3I'))
    sx,sy=lpxy(126,y,'r',S=S); s.append(DRAW(curved(sx+3,sy-5,200,y-8,bend=-26),.3)); s.append(DRAW(curved(252,y-6,280,y-22,bend=-14),.8))
    s.append(harrow(150,200,176)); s.append(cond(290,184,'CH3CH2OCH3',22)); s.append(lab(290,212,'에틸 메틸 에테르',19))
    s.append(plus(380,176)); s.append(cond(410,184,'I-',22))
    SPEC['W P']=(formula('C3H8O'),0); SPEC['W I-']=(formula('I'),-1); rxn(['W EtO-','W CH3I'],['W P','W I-'],'S27')
    return svg('0 0 450 230',420,'에탄올산 이온이 아이오도메테인을 뒤쪽에서 공격하여 에틸 메틸 에테르가 생기는 윌리엄슨 에테르 합성',s)
FIG['WIL']=wil()

# ═══ S28 해먼드 가설
def hammond():
    W,H=440,300; s=[]; x0,y0=50,H-36
    s.append(eaxes(x0,y0,W-12,22))
    R=(x0+30,y0-50); TS=(290,70); I=(370,98)
    s.append(DRAW(ecurve([R,TS,I]),.2,'1.2'))
    s.append(seg(x0+8,x0+70,R[1])); s.append(lab(x0+40,R[1]+28,'반응물',19,INK))
    s.append(C(I[0],I[1],6,EQUI,2,fill=EQUI)); s.append(lab(I[0]+8,I[1]+34,'중간체',19,EQUI,weight=700))
    s.append(lab(TS[0]-20,TS[1]-16,'전이 상태',19,INK))
    s.append(f'<ellipse cx="{(TS[0]+I[0])/2+4}" cy="{(TS[1]+I[1])/2-2}" rx="66" ry="34" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 5"/>')
    s.append(lab(190,170,'흡열 단계: 전이 상태 ≈ 중간체',19,MUTED,halo=True))
    return svg(f'0 0 {W} {H}',W,'흡열 단계의 에너지 도표: 전이 상태가 중간체와 에너지와 구조가 비슷하다',s)
FIG['HAM']=hammond()

# ═══ S29 라디칼 연쇄 네 칸
def clx(x,y,lp,S,name,rad=None,**k):
    d=dict(lp=list(lp)); 
    if rad: d['rad']=[rad]; d['oct']=7
    d.update(k); return A_('Cl',x,y,**d)
def rad1():
    S=20; s=[]; y=70
    a=[clx(80,y,'uld',S,''),clx(140,y,'udr',S,'')]
    s.append(M(a,[(0,1,1,'l')],'Cl2',S=S,name='r1 Cl2'))
    s.append(DRAW(fish(110,y-4,84,y-24,bend=-14,up=True),.3)); s.append(DRAW(fish(110,y-4,136,y-24,bend=14,up=False),.5))
    s.append(T(110,y-40,tex='h\\nu',size=20,fill=EQUI))
    s.append(harrow(40,80,164))
    s.append(M([clx(120,164,'uld',S,'',rad='r')],[],'Cl',S=S,name='r1 Cl a')); s.append(plus(166,164))
    s.append(M([clx(210,164,'udr',S,'',rad='l')],[],'Cl',S=S,name='r1 Cl b'))
    rxn(['r1 Cl2'],['r1 Cl a','r1 Cl b'],'S29-개시')
    return svg('0 0 270 226',250,'개시: 빛에너지로 염소 분자가 균일 분해되어 염소 라디칼 두 개가 생김',s)
def methyl(x,y,rad=None,Xel=None,S=20,side='r'):
    a=[Cc(x,y),H_(x,y-40),H_(x,y+40),H_(x-40 if side=='r' else x+40,y)]; b=[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l')]
    if rad: a[0]['rad']=[rad]; a[0]['oct']=7
    return a,b
def rad2():
    S=20; s=[]; y=70
    s.append(M([clx(30,y,'uld',S,'',rad='r')],[],'Cl',S=S,name='r2 Cl'))
    a=[H_(84,y),Cc(124,y),H_(124,y-40),H_(124,y+40),H_(164,y)]
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l'),(1,3,1,'l'),(1,4,1,'l')],'CH4',S=S,name='r2 CH4'))
    s.append(DRAW(fish(48,y-6,62,y-14,bend=-10,up=True),.3)); s.append(DRAW(fish(104,y-4,74,y-12,bend=12,up=False),.5)); s.append(DRAW(fish(104,y-4,118,y-18,bend=-10,up=True),.7))
    s.append(harrow(14,44,164))
    a=[H_(66,164),clx(108,164,'urd',S,'')]
    s.append(M(a,[(0,1,1,'l')],'HCl',S=S,name='r2 HCl')); s.append(plus(150,164))
    a,b=methyl(222,164,rad='r',side='r'); s.append(M(a,b,'CH3',S=S,name='r2 CH3'))
    rxn(['r2 Cl','r2 CH4'],['r2 HCl','r2 CH3'],'S29-전파1')
    return svg('0 0 270 226',250,'전파 1: 염소 라디칼이 메테인의 수소를 떼어 내어 염화 수소와 메틸 라디칼이 생김',s)
def rad3():
    S=20; s=[]; y=70
    a,b=methyl(60,y,rad='r'); s.append(M(a,b,'CH3',S=S,name='r3 CH3'))
    a=[clx(130,y,'uld',S,''),clx(190,y,'udr',S,'')]
    s.append(M(a,[(0,1,1,'l')],'Cl2',S=S,name='r3 Cl2'))
    s.append(DRAW(fish(78,y-6,98,y-14,bend=-10,up=True),.3)); s.append(DRAW(fish(160,y-4,104,y-14,bend=16,up=False),.5)); s.append(DRAW(fish(160,y-4,186,y-24,bend=-12,up=True),.7))
    s.append(harrow(30,70,164))
    a,b=methyl(120,164); a.append(clx(166,164,'urd',S,'')); b.append((0,4,1,'l'))
    s.append(M(a,b,'CH3Cl',S=S,name='r3 CH3Cl')); s.append(plus(206,164))
    s.append(M([clx(240,164,'udr',S,'',rad='l')],[],'Cl',S=S,name='r3 Cl'))
    rxn(['r3 CH3','r3 Cl2'],['r3 CH3Cl','r3 Cl'],'S29-전파2')
    return svg('0 0 270 226',250,'전파 2: 메틸 라디칼이 염소 분자의 염소를 떼어 내어 클로로메테인과 염소 라디칼이 다시 생김',s)
def rad4():
    S=20; s=[]; y=70
    s.append(M([clx(40,y,'uld',S,'',rad='r')],[],'Cl',S=S,name='r4 Cl'))
    a,b=methyl(150,y,rad='l',side='l'); s.append(M(a,b,'CH3',S=S,name='r4 CH3'))
    s.append(DRAW(fish(58,y-6,94,y-12,bend=-12,up=True),.3)); s.append(DRAW(fish(132,y-6,100,y-12,bend=12,up=False),.5))
    s.append(harrow(30,70,164))
    a,b=methyl(196,164); a.append(clx(240,164,'urd',S,'')); b.append((0,4,1,'l'))
    s.append(M(a,b,'CH3Cl',S=S,name='r4 CH3Cl'))
    rxn(['r4 Cl','r4 CH3'],['r4 CH3Cl'],'S29-종결')
    return svg('0 0 270 226',250,'종결: 두 라디칼이 만나 결합하면 연쇄가 끝남',s)
FIG['RAD1']=rad1(); FIG['RAD2']=rad2(); FIG['RAD3']=rad3(); FIG['RAD4']=rad4()

# ═══ S30 2-메틸프로페인의 수소
def isobut():
    S=20; s=[]; cx,cy=180,130; d=56
    a=[Cc(cx,cy),H_(cx,cy-46)]; b=[(0,1,1,'l')]
    cs=[(cx-d*1.3,cy),(cx+d*1.3,cy),(cx,cy+d*1.25)]
    hpos={0:[(-1,0),(0,-1),(0,1)],1:[(1,0),(0,-1),(0,1)],2:[(-1,0),(1,0),(0,1)]}
    one=[]
    for i,(x,y) in enumerate(cs):
        ci=len(a); a.append(Cc(x,y)); b.append((0,ci,1,'l'))
        for dx,dy in hpos[i]:
            hx,hy=x+dx*42,y+dy*42; a.append(H_(hx,hy)); b.append((ci,len(a)-1,1,'l')); one.append((hx,hy))
    s.append(hlrect(cx,cy-46,30,30))
    for hx,hy in one: s.append(C(hx,hy,15,FIELD,1.8,dash='4 3'))
    s.append(M(a,b,'C4H10',S=S,name='isobutane'))
    s.append(lab(330,60,'3차 H 1개',19,INK,anchor='start')); s.append(lab(330,86,'(형광펜)',19,MUTED,anchor='start'))
    s.append(lab(330,150,'1차 H 9개',19,FIELD,anchor='start')); s.append(lab(330,176,'(점선 동그라미)',19,MUTED,anchor='start'))
    return svg('0 0 450 262',390,'2-메틸프로페인의 3차 수소 1개와 1차 수소 9개',s)
FIG['ISOB']=isobut()

# ═══ S31 에틸렌 + HBr
def hbradd():
    S=24; s=[]; y=110
    a=[Cc(80,y),Cc(146,y),H_(46,y-44),H_(46,y+44),H_(180,y-44),H_(180,y+44)]
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],'C2H4',S=S,name='31 C2H4'))
    a=[H_(250,y),X_('Br',310,y,['u','d','r'])]; s.append(M(a,[(0,1,1,'l')],'HBr',S=S,name='31 HBr'))
    s.append(DRAW(curved(113,y-10,240,y-12,bend=-40),.3)); s.append(DRAW(curved(280,y-6,306,y-26,bend=-14),.8))
    s.append(lab(113,y+92,'π 전자 → H',19,INK)); s.append(harrow(370,420,y)); s.append(lab(395,y-14,'느림',19,PLUS,weight=700))
    a=[G_('CH3',480,y),A_('C',546,y,oct=6,fc=1,fcp='ur'),H_(578,y-44),H_(578,y+44)]
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l'),(1,3,1,'l')],'C2H5',S=S,name='31 cat'))
    s.append(plus(624,y)); s.append(M([X_('Br',684,y,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='31 Br-'))
    sx,sy=lpxy(684,y,'u','Br',S); s.append(DRAW(curved(sx-6,sy-2,562,y-30,bend=-30),1.3))
    rxn(['31 C2H4','31 HBr'],['31 cat','31 Br-'],'S31-1')
    s.append(harrow(740,790,y)); s.append(lab(765,y-14,'빠름',19,FIELD,weight=700))
    a=[G_('CH3',860,y),Cc(926,y),H_(926,y-48),H_(926,y+48),X_('Br',996,y,['u','d','r'])]
    s.append(hlrect(961,y,60,40))
    s.append(M(a,[(0,1,1,'l'),(1,2,1,'l'),(1,3,1,'l'),(1,4,1,'l')],'C2H5Br',S=S,name='31 P'))
    rxn(['31 cat','31 Br-'],['31 P'],'S31-2')
    return svg('0 0 1060 220',1040,'에틸렌의 π 전자가 브로민화 수소의 수소를 공격하여 탄소 양이온이 되고, 브로민화 이온이 결합하여 브로모에테인이 생김',s)
FIG['HBR']=hbradd()

# ═══ S32 마르코브니코프: 두 경로 + 에너지
def markpath():
    s=[]
    s.append(cond(90,150,'(CH3)2C=CH2',24,weight=700)); s.append(lab(90,182,'2-메틸프로펜',19))
    s.append(lab(90,112,'+ $\\ce{H+}$',20,INK))
    s.append(A(190,136,250,76,'ink',2.6)); s.append(cond(340,76,'(CH3)3C+',26)); s.append(lab(340,108,'3차 탄소 양이온',19,FIELD,weight=700))
    s.append(A(410,70,450,70,'ink',2.6)); s.append(lab(430,54,'$\\ce{Br-}$',19,INK))
    s.append(hlrect(510,64,140,40)); s.append(cond(510,72,'(CH3)3CBr',24))
    s.append(A(190,164,250,224,'muted',2.6,d=True)); s.append(cond(350,232,'(CH3)2CHCH2+',24,fill=MUTED)); s.append(lab(350,264,'1차 탄소 양이온 (불안정)',19,MUTED))
    s.append(L(470,220,486,236,PLUS,3)+L(470,236,486,220,PLUS,3))
    return svg('0 0 600 280',560,'2-메틸프로펜에 수소 이온이 붙을 때 3차 탄소 양이온을 거치는 경로가 1차 탄소 양이온을 거치는 경로보다 유리함',s)
FIG['MARK']=markpath()
def emark():
    W,H=400,300; s=[]; x0,y0=46,H-34
    s.append(eaxes(x0,y0,W-10,22))
    R=(x0+26,y0-70)
    s.append(DRAW(ecurve([R,(170,120),(250,170)]),.2,'1.1'))
    s.append(ecurve([R,(170,48),(250,84)],MUTED,2.6,dash='7 6'))
    s.append(seg(x0+6,x0+60,R[1])); s.append(lab(x0+34,R[1]+28,'알켄 + $\\ce{H+}$',19,INK))
    s.append(C(250,170,6,EQUI,2,fill=EQUI)); s.append(lab(262,196,'3차 양이온',19,FIELD,anchor='start',weight=700))
    s.append(C(250,84,6,GRAV,2,fill=GRAV)); s.append(lab(262,90,'1차 양이온',19,MUTED,anchor='start'))
    s.append(lab(170,40,'느림',19,MUTED)); s.append(lab(170,140,'빠름',19,FIELD,weight=700))
    return svg(f'0 0 {W} {H}',W,'3차 탄소 양이온을 거치는 경로가 활성화 에너지가 작아 빠르다',s)
FIG['EMARK']=emark()

# ═══ S33 프로펜 → 두 알코올
def hyd2():
    s=[]
    s.append(cond(110,80,'CH3CH=CH2',26,weight=700)); s.append(lab(110,112,'프로펜',19))
    s.append(A(220,66,350,40,'ink',2.4)); s.append(lab(214,34,'산 촉매 수화 · 옥시수은화',19,INK,anchor='end'))
    s.append(hlrect(492,36,58,36)); s.append(cond(470,44,'CH3CH(OH)CH3',24)); s.append(lab(640,44,'2-프로판올 (마르코브니코프)',19,INK,anchor='start'))
    s.append(A(220,94,350,120,'ink',2.4)); s.append(lab(214,134,'수소붕소화–산화',19,INK,anchor='end'))
    s.append(hlrect(530,116,46,36)); s.append(cond(470,124,'CH3CH2CH2OH',24)); s.append(lab(640,124,'1-프로판올 (반마르코브니코프)',19,INK,anchor='start'))
    return svg('0 0 960 160',900,'프로펜의 수화: 산 촉매 수화와 옥시수은화는 2-프로판올, 수소붕소화-산화는 1-프로판올',s)
FIG['HYD2']=hyd2()

# ═══ S34 브로모늄 이온 → anti 첨가
def bromo():
    S=22; s=[]; y=176
    a=[Cc(60,y),Cc(120,y),H_(30,y-40),H_(30,y+40),H_(150,y-40),H_(150,y+40)]
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],'C2H4',S=S,name='34 C2H4'))
    a=[X_('Br',90,y-90,['l','r','u']),X_('Br',90,y-146,['l','r','u'])]
    s.append(M(a,[(0,1,1,'l')],'Br2',S=S,name='34 Br2'))
    s.append(DRAW(curved(96,y-10,94,y-72,bend=-22),.3)); s.append(DRAW(curved(96,y-116,118,y-142,bend=-16),.7))
    s.append(harrow(180,220,y))
    cx=300
    a=[Cc(cx-30,y),Cc(cx+30,y),X_('Br',cx,y-66,['l','r'],fc=1,fcp='ur'),H_(cx-60,y-30),H_(cx-60,y+40),H_(cx+60,y-30),H_(cx+60,y+40)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(1,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(1,5,1,'l'),(1,6,1,'l')],'C2H4Br',S=S,name='34 bromonium'))
    s.append(lab(cx-40,y+82,'브로모늄 이온',19,EQUI,weight=700))
    s.append(M([X_('Br',cx+40,y+124,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='34 Br-'))
    rxn(['34 C2H4','34 Br2'],['34 bromonium','34 Br-'],'S34-1')
    s.append(DRAW(curved(cx+26,y+110,cx+30,y+18,bend=-20),1.2)); s.append(DRAW(curved(cx+18,y-30,cx+4,y-50,bend=-10),1.6))
    s.append(lab(cx+40,y+164,'반대쪽 면에서 공격',19,MINUS))
    s.append(harrow(390,430,y))
    a=[Cc(490,y),Cc(550,y),X_('Br',490,y-66,['l','r','u']),X_('Br',550,y+66,['l','r','d']),H_(450,y+20),H_(510,y+44),H_(590,y-20),H_(530,y-44)]
    s.append(hlrect(490,y-66,40,36)); s.append(hlrect(550,y+66,40,36))
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(1,3,1,'l'),(0,4,1,'l'),(0,5,1,'l'),(1,6,1,'l'),(1,7,1,'l')],'C2H4Br2',S=S,name='34 P'))
    rxn(['34 bromonium','34 Br-'],['34 P'],'S34-2')
    s.append(lab(520,y+130,'anti 첨가',19,INK,weight=700))
    return svg('0 0 620 350',600,'알켄의 π 전자가 브로민을 공격하여 브로모늄 이온이 생기고, 브로민화 이온이 반대쪽 면에서 공격하여 anti 첨가',s)
FIG['BROMO']=bromo()

# ═══ S36 알릴 양이온과 1,2-·1,4-첨가
def allyl():
    S=20; s=[]
    def cat(x,y,pos):
        c=[x,x+64,x+128,x+192]
        a=[G_('CH3',c[0],y),A_('C',c[1],y,**({'oct':6,'fc':1,'fcp':'ur'} if pos==2 else {})),H_(c[1],y+42),
           A_('C',c[2],y),H_(c[2],y+42),A_('C',c[3],y,**({'oct':6,'fc':1,'fcp':'ur'} if pos==4 else {})),H_(c[3]+30,y-30),H_(c[3]+30,y+30)]
        b=[(0,1,1,'l'),(1,2,1,'l'),(1,3,1 if pos==2 else 2,'l'),(3,4,1,'l'),(3,5,2 if pos==2 else 1,'l'),(5,6,1,'l'),(5,7,1,'l')]
        return a,b
    s.append(cond(300,30,'CH2=CH-CH=CH2 + H+ ->[\\text{C1에}]',22))
    a,b=cat(40,110,2); s.append(M(a,b,'C4H7',S=S,name='allyl2'))
    s.append(DRAW(curved(200,96,138,96,bend=18),.4))
    s.append(T(300,118,tex='\\ce{<->}',size=28))
    a,b=cat(350,110,4); s.append(M(a,b,'C4H7',S=S,name='allyl4'))
    for x0 in (40,350):
        for k in range(4): s.append(T(x0+64*k-(0 if k else 0),72,tex='\\mathrm{C'+str(k+1)+'}',size=19,fill=MUTED))
    s.append(lab(330,192,'알릴 양이온(공명)',19,EQUI,weight=700))
    g=A(130,190,130,232,'minus',2.4)+lab(130,212,'',19)+cond(130,262,'CH3CHBrCH=CH2',22)+lab(130,290,'1,2-첨가 (3-브로모-1-뷰텐)',19,INK)
    s.append(POP(g,130,250,.9))
    g=A(540,190,540,232,'minus',2.4)+cond(470,262,'CH3CH=CHCH2Br',22)+lab(470,290,'1,4-첨가 (1-브로모-2-뷰텐)',19,INK)
    s.append(POP(g,470,250,1.3))
    s.append(lab(330,222,'$\\ce{Br-}$이 $\\mathrm{C2}$ 또는 $\\mathrm{C4}$를 공격',19,MINUS))
    return svg('0 0 640 310',600,'1,3-뷰타다이엔에 수소 이온이 붙어 생긴 알릴 양이온의 두 공명 구조와 1,2-첨가, 1,4-첨가 생성물',s)
FIG['ALLYL']=allyl()
def ediene():
    W,H=400,300; s=[]; x0,y0=46,H-34
    s.append(eaxes(x0,y0,W-10,22))
    I=(x0+30,96)
    s.append(DRAW(ecurve([I,(170,52),(300,150)]),.2,'1.1'))
    s.append(ecurve([I,(190,30),(320,196)],INK,2.6,dash='7 6'))
    s.append(C(I[0],I[1],6,EQUI,2,fill=EQUI)); s.append(lab(I[0]+6,I[1]+30,'알릴 양이온',19,EQUI,anchor='start'))
    s.append(seg(270,330,150)); s.append(lab(300,140,'1,2-생성물',19,INK))
    s.append(seg(290,350,196,INK,3,dash='7 6')); s.append(lab(320,224,'1,4-생성물',19,INK))
    s.append(lab(160,74,'빠름',19,FIELD,weight=700)); s.append(lab(232,40,'느림',19,MUTED))
    s.append(lab(330,250,'더 안정',19,INK))
    return svg(f'0 0 {W} {H}',W,'1,2-첨가는 활성화 에너지가 작아 빠르고, 1,4-생성물은 에너지가 낮아 더 안정하다',s)
FIG['EDIENE']=ediene()

# ═══ S37 딜스–알더
def da():
    s=[]; R=56
    def hexv(cx,cy,r): return [(cx+r*math.cos(math.radians(90+60*k)),cy-r*math.sin(math.radians(90+60*k))) for k in range(6)]
    # k: 0 위, 1 왼쪽 위, 2 왼쪽 아래, 3 아래, 4 오른쪽 아래, 5 오른쪽 위 (시계 반대)
    def ln(p,q,dash=None): return L(*p,*q,INK,2.6,dash=dash,extra='stroke-linecap="round"')
    def dbl(p,q,c):
        mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2; ix,iy=c[0]-mx,c[1]-my; n=math.hypot(ix,iy); ix,iy=ix/n*8,iy/n*8; t=.18
        return L(p[0]+(q[0]-p[0])*t+ix,p[1]+(q[1]-p[1])*t+iy,p[0]+(q[0]-p[0])*(1-t)+ix,p[1]+(q[1]-p[1])*(1-t)+iy,INK,2.6,extra='stroke-linecap="round"')
    def mid(p,q,dx=0,dy=0): return ((p[0]+q[0])/2+dx,(p[1]+q[1])/2+dy)
    c=(150,140); V=hexv(*c,R); sh=34
    D=[V[0],V[1],V[2],V[3]]; E=[(V[4][0]+sh,V[4][1]),(V[5][0]+sh,V[5][1])]
    s.append(ln(D[0],D[1])+ln(D[1],D[2])+ln(D[2],D[3])+dbl(D[0],D[1],c)+dbl(D[2],D[3],c))
    s.append(ln(E[0],E[1])+dbl(E[0],E[1],(c[0]+sh,c[1])))
    a1=mid(D[0],D[1]); a2=mid(D[1],D[2]); b1=mid(D[2],D[3]); e1=mid(E[0],E[1])
    g1=mid(D[0],E[1],0,-4); g2=mid(D[3],E[0],0,4)
    s.append(DRAW(curved(*mid(D[0],D[1],-8,-8),*g1,bend=-26),.3))
    s.append(DRAW(curved(e1[0]+12,e1[1],*g2,bend=30),.7))
    s.append(DRAW(curved(*mid(D[2],D[3],-8,8),*mid(D[1],D[2],-12,0),bend=24),1.1))
    s.append(lab(112,238,'다이엔 (s-cis)',19,INK)); s.append(lab(214,238,'친다이엔체',19,INK))
    s.append(harrow(270,316,140))
    c2=(410,140); V2=hexv(*c2,R)
    for k in range(6): s.append(ln(V2[k],V2[(k+1)%6],dash='6 5' if k in (3,5) else None))
    s.append(f'<circle cx="{c2[0]}" cy="{c2[1]}" r="26" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 5"/>')
    s.append(tsb(340,66,480,214)); s.append(lab(410,238,'고리 모양 전이 상태',19,MUTED))
    s.append(harrow(520,566,140))
    c3=(650,140); V3=hexv(*c3,R)
    for k in (3,5): s.append(hlrect(*mid(V3[k],V3[(k+1)%6]),30,30))
    for k in range(6): s.append(ln(V3[k],V3[(k+1)%6]))
    s.append(dbl(V3[1],V3[2],c3))
    s.append(lab(650,238,'사이클로헥센',19,INK)); s.append(lab(650,262,'새 σ 결합 2개(형광펜)',19,MUTED))
    return svg('0 50 760 230',640,'s-cis 1,3-뷰타다이엔과 에틸렌이 고리 모양 전이 상태를 지나 사이클로헥센이 되는 딜스-알더 반응. 굽은 화살표 3개',s)
FIG['DA']=da()

# ═══ S38 2-메틸-2-뷰텐
def mb2():
    s=[]
    s.append(cond(230,90,'CH3-C(CH3)=CH-CH3',30,weight=700))
    for x,n in ((70,'1'),(186,'2'),(300,'3'),(394,'4')): s.append(lab(x,44,n,19,MUTED))
    s.append(lab(230,136,'2-메틸-2-뷰텐',20,INK))
    return svg('0 0 460 160',440,'2-메틸-2-뷰텐의 축약 구조식과 탄소 번호',s)
FIG['MB2']=mb2()

# ═════ 조립 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
assert OUT.endswith('1-4-S1_심화_친핵성_치환_제거_반응과_첨가_반응/slides.html')
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused,'eq',len(EQLOG),'rxn',len(RXN),RXN)
