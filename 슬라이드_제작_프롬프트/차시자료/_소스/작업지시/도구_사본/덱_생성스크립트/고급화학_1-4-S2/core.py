import math, re, sys, os
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'gen_head.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/1-4-S2_심화_방향족_치환과_카보닐_화합물의_반응/slides.html') and '1-4-S1_' not in OUT
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

