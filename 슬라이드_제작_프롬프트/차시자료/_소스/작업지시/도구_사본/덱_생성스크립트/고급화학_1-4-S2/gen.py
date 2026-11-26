# -*- coding: utf-8 -*-
"""고급화학 1-4-S2 [심화] 그림 생성: core.py(1-4-S1 gen.py 앞부분 사본 — gen_head(OUT=이 덱, assert)·lewis·M·rxn·eqchk)
   + 벤젠 고리 도우미 ring()(꼭짓점마다 결합 수·전하를 검산하고 고리 분자식을 assert) → tpl.html의 {{KEY}}를 바꿔 slides.html."""
import math, re, sys, os
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE,'core.py'),encoding='utf-8').read())
assert OUT.endswith('content/고급화학/1-4-S2_심화_방향족_치환과_카보닐_화합물의_반응/slides.html')
assert '1-4-S1' not in OUT and '1-4-2_' not in OUT
VAL.update({'Br':7,'N':5,'I':7,'Cl':7,'Mg':2})
CW.update({'R':.72,"'":.22,'(':.34,')':.34,'-':.5,'I':.36,'+':.6,'M':.9,'g':.6,'A':.72,'r':.42,'S':.66,'Y':.66})
def popa(x,y,d,dur='.6'): return {'o':f'{f(x)},{f(y)}','dur':dur,'delay':f'{d:.1f}'}
def POP(body,x,y,d=0.2): return an('pop',body,**popa(x,y,d))
def DRAW(body,d=0.3,dur='.7'): return an('draw',body,dur=dur,delay=f'{d:.1f}')
def FADE(body,d=0.2,dur='.6'): return an('fade',body,dur=dur,delay=f'{d:.1f}')
# 축약 원자단 분자식을 따로 줄 때(fm) — R, R′, Y 같은 가상 기호는 Q·Z 등으로 센다
def fcount(atoms):
    c=Counter()
    for a in atoms:
        if a.get('grp'):
            if a['grp']=='_': continue
            c+=formula(a.get('fm',a['grp']))
        else: c[a['el']]+=1
    return c

# ═════ 반응식 검산 (plan.md 3절과 같은 목록) ═════
EQS=[
 ('S3','C6H10 + Br2 -> C6H10Br2'),('S3','C6H6 + Br2 -> C6H5Br + HBr'),
 ('S4','C6H6 + E+ -> C6H6E+'),('S4','C6H6E+ + B- -> C6H5E + HB'),
 ('S7','Br2 + FeBr3 -> FeBr5'),('S7','C6H6 + FeBr5 -> C6H6Br+ + FeBr4-'),('S7','C6H6Br+ + FeBr4- -> C6H5Br + HBr + FeBr3'),
 ('S7','C6H6 + Cl2 -> C6H5Cl + HCl'),
 ('S8','HNO3 + H2SO4 <=> H2NO3+ + HSO4-'),('S8','H2NO3+ <=> H2O + NO2+'),('S8','C6H6 + NO2+ -> C6H6NO2+'),
 ('S8','C6H6NO2+ + H2O -> C6H5NO2 + H3O+'),('S8','C6H6 + HNO3 -> C6H5NO2 + H2O'),('S8','C6H5NO2 + 3H2 -> C6H5NH2 + 2H2O'),
 ('S9','SO3 + H2SO4 <=> HSO3+ + HSO4-'),('S9','C6H6 + HSO3+ <=> C6H6SO3H+'),('S9','C6H6SO3H+ + HSO4- <=> C6H5SO3H + H2SO4'),
 ('S9','C6H5SO3H + H2O -> C6H6 + H2SO4'),
 ('S10','(CH3)2CHCl + AlCl3 -> (CH3)2CH+ + AlCl4-'),('S10','C6H6 + (CH3)2CH+ -> C9H13+'),('S10','C9H13+ + AlCl4- -> C6H5CH(CH3)2 + HCl + AlCl3'),
 ('S10','C6H6 + (CH3)2CHCl -> C6H5CH(CH3)2 + HCl'),
 ('S11','C6H6 + CH3CH2CH2CH2Cl -> C6H5CH(CH3)CH2CH3 + HCl'),('S11','CH3CH2CH2CH2+ -> CH3CH2CHCH3+'),('S11','(CH3)3CCH2+ -> (CH3)2CCH2CH3+'),
 ('S12','CH3CH2COCl + AlCl3 -> CH3CH2CO+ + AlCl4-'),('S12','C6H6 + CH3CH2COCl -> C6H5COCH2CH3 + HCl'),('S12','C6H5COCH2CH3 + 2H2 -> C6H5CH2CH2CH3 + H2O'),
 ('S13','C6H6 + CH3COCl -> C6H5COCH3 + HCl'),('S13','C6H6 + (CH3)3CCl -> C6H5C(CH3)3 + HCl'),
 ('S21','C7H8 + SO3 -> C7H8SO3'),
 ('S23','C7H8 + CH3COCl -> C9H10O + HCl'),('S23','C9H10O + HNO3 -> C9H9NO3 + H2O'),('S23','C9H9NO3 + 5H2 -> C9H13N + 3H2O'),
 ('S24','C6H5Cl + CH3CH2Cl -> ClC6H4CH2CH3 + HCl'),('S24','C8H7NO3 + 5H2 -> C8H11N + 3H2O'),('S24','C7H8 + Cl2 -> C7H7Cl + HCl'),
 ('S24','C10H15N + SO3 -> C10H15NO3S'),
 ('S25','C6H5Br + NH2- -> C6H4Br- + NH3'),('S25','C6H4Br- -> C6H4 + Br-'),('S25','C6H4 + NH2- -> C6H4NH2-'),
 ('S25','C6H4NH2- + NH3 -> C6H5NH2 + NH2-'),('S25','C6H5Br + NH2- -> C6H5NH2 + Br-'),('S25','C6H5Cl + OH- -> C6H5OH + Cl-'),
 ('S26','HNO2 + H+ -> H2NO2+'),('S26','H2NO2+ -> NO+ + H2O'),('S26','C6H5NH2 + NO+ -> C6H5NH2NO+'),('S26','C6H5NH2NO+ -> C6H5NHNO + H+'),
 ('S26','C6H5NHNO -> C6H5NNOH'),('S26','C6H5NNOH + H+ -> C6H5N2+ + H2O'),('S26','C6H5NH2 + HNO2 + H2SO4 -> C6H5N2+ + HSO4- + 2H2O'),
 ('S27','C6H5N2+ + Cl- -> C6H5Cl + N2'),('S27','C6H5N2+ + I- -> C6H5I + N2'),('S27','C6H5N2+ + H2O -> C6H5OH + N2 + H+'),
 ('S27','C6H5N2+ + Cu+ -> C6H5N2 + Cu^2+'),('S27','C6H5N2 -> C6H5 + N2'),('S27','C6H5 + Cu^2+ + Br- -> C6H5Br + Cu+'),
 ('S28','C6H5N2+ + C6H5OH -> C12H10N2O + H+'),('S28','C6H5N2+ + C6H5N(CH3)2 -> C14H15N3 + H+'),
 ('S29','CH3CHO + CN- -> CH3CH(CN)O-'),
 ('S30','CH3Br + Mg -> CH3MgBr'),('S30','CH3MgBr + HCHO -> CH3CH2OMgBr'),('S30','CH3CH2OMgBr + H3O+ -> CH3CH2OH + Mg^2+ + Br- + H2O'),
 ('S31','C6H5Br + Mg -> C6H5MgBr'),('S31','C6H5MgBr + CH3COCH3 -> C6H5C(CH3)2OMgBr'),('S31','C6H5C(CH3)2OMgBr + H3O+ -> C6H5C(CH3)2OH + Mg^2+ + Br- + H2O'),
 ('S32','C2H4O + H+ -> C2H5O+'),('S32','C2H5O+ + CH4O -> C3H9O2+'),('S32','C3H9O2+ -> C3H8O2 + H+'),('S32','C3H8O2 + H+ -> C3H9O2+'),
 ('S32','C3H9O2+ -> C3H7O+ + H2O'),('S32','C3H7O+ + CH4O -> C4H11O2+'),('S32','C4H11O2+ -> C4H10O2 + H+'),
 ('S32','CH3CHO + 2CH3OH <=> CH3CH(OCH3)2 + H2O'),
 ('S33','CH3CHO + CH3NH2 -> CH3CH(OH)NHCH3'),('S33','CH3CH(OH)NHCH3 -> CH3CH=NCH3 + H2O'),
 ('S34','CH3COCl + CH3CH2OH -> CH3COOCH2CH3 + HCl'),('S34','CH3COCl + 2NH3 -> CH3CONH2 + NH4Cl'),
 ('S34','CH3COOCH2CH3 + OH- -> CH3COO- + CH3CH2OH'),
 ('S35','CH3CHO + OH- -> CH2CHO- + H2O'),('S35','CH2CHO- + CH3CHO -> CH3CH(O)CH2CHO-'),('S35','CH3CH(O)CH2CHO- + H2O -> CH3CH(OH)CH2CHO + OH-'),
 ('S35','CH3CH(OH)CH2CHO -> CH3CH=CHCHO + H2O'),('S35','2CH3CHO -> CH3CH(OH)CH2CHO'),
 ('S36','2CH3CH2CHO -> CH3CH2CH(OH)CH(CH3)CHO'),('S36','CH3CH2CH(OH)CH(CH3)CHO -> CH3CH2CH=C(CH3)CHO + H2O'),
 ('S37','C7H8 + 2Br2 -> C7H6Br2 + 2HBr'),('S37','C7H8 + HNO3 -> C7H7NO2 + H2O'),('S37','C7H7NO2 + 3H2 -> C7H9N + 2H2O'),
 ('S37','C7H9N + 2Br2 -> C7H7Br2N + 2HBr'),('S37','C7H7Br2N + HNO2 + HCl -> C7H5Br2N2+ + Cl- + 2H2O'),
 ('S37','C7H5Br2N2+ + H3PO2 + H2O -> C7H6Br2 + N2 + H3PO3 + H+'),
 ('S38','C8H9NO + HNO3 -> C8H8N2O3 + H2O'),('S38','C8H8N2O3 + H2O -> C6H6N2O2 + CH3COOH'),('S38','C6H6N2O2 + HNO2 + H+ -> C6H4N3O2+ + 2H2O'),
 ('S38','C6H4N3O2+ + C7H6O3 -> C13H9N3O5 + H+')]
for tg,e in EQS: eqchk(e,tg)

# ═════ 벤젠 고리 도우미 ═════
KEK=(2,1,2,1,2,1)
def rv(cx,cy,R,rot=90):
    return [(cx+R*math.cos(math.radians(rot-60*k)),cy-R*math.sin(math.radians(rot-60*k))) for k in range(6)]
def aren(s,c):
    """sp3 꼭짓점 s, 양전하 꼭짓점 c인 아레늄 이온 공명 구조의 고리 결합 차수"""
    p=[(s+i)%6 for i in range(1,6)]; i=p.index(c); assert i in (0,2,4),(s,c)
    e=[1]*6; rest=p[:i]+[None]+p[i+1:]
    for seg_ in (p[:i],p[i+1:]):
        for j in range(0,len(seg_),2):
            a,b=seg_[j],seg_[j+1]; e[a if (a+1)%6==b else b]=2
    return tuple(e)
RG={}
def sub(t,fm=None,o=1,ang=None,ln=None,fc=0,tex=None,hl=None,col=None,size=None,al=None,fcp=None,lp=0):
    return dict(t=t,fm=t if fm is None else fm,o=o,ang=ang,ln=ln,fc=fc,tex=tex,hl=hl,col=col,size=size,al=al,fcp=fcp,lp=lp)
def chg(x,y,sg,r=11):
    col=PLUS if sg>0 else MINUS
    return C(x,y,r,col,1.8,fill='#fff')+T(x,y+6.4,tex='+' if sg>0 else '-',size=18,fill=col,weight=700)
def ring(cx,cy,R=30,e=KEK,subs=None,cat=None,an_=None,rot=90,want=None,name='',S=20,box=None,lw=2.4,mark=None,dot=None):
    """벤젠 고리(꼭짓점 k: rot−60k 방향, 0=위, 시계 방향). e[k] = 꼭짓점 k–k+1 결합 차수.
    subs {k:[sub(...)]}; cat=양전하 꼭짓점, an_=음전하(비공유 전자쌍) 꼭짓점. 숨은 H는 원자가로 채우고 분자식 want와 대조."""
    subs=subs or {}; V=rv(cx,cy,R,rot); s=[]; c=Counter({'C':6}); q=0
    for k in range(6):
        need=3 if k in (cat,an_) else 4
        val=e[(k-1)%6]+e[k]+sum(x['o'] for x in subs.get(k,[]))
        nH=need-val
        if not 0<=nH<=2: sys.exit(f'[고리 {name}] 꼭짓점 {k} 결합 {val} (필요 {need})')
        c['H']+=nH
        for x in subs.get(k,[]):
            if x['fm']: c+=formula(x['fm'])
            q+=x['fc']
    q+=(1 if cat is not None else 0)-(1 if an_ is not None else 0)
    if want is not None and +c!=+formula(want): sys.exit(f'[고리 {name}] 분자식 {dict(c)} ≠ {want}')
    if name: SPEC[name]=(c,q)
    if box: s.append(f'<rect x="{f(cx-R-22)}" y="{f(cy-R-30)}" width="{f(2*R+44)}" height="{f(2*R+60)}" rx="10" fill="none" stroke="{box}" stroke-width="2.4"/>')
    for k in range(6):
        a,b=V[k],V[(k+1)%6]; s.append(L(*a,*b,INK,lw,extra='stroke-linecap="round"'))
        if e[k]>=2:
            mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2; ix,iy=cx-mx,cy-my; n=math.hypot(ix,iy); ix,iy=ix/n*0.2*R,iy/n*0.2*R; t=.2
            s.append(L(a[0]+(b[0]-a[0])*t+ix,a[1]+(b[1]-a[1])*t+iy,a[0]+(b[0]-a[0])*(1-t)+ix,a[1]+(b[1]-a[1])*(1-t)+iy,INK,lw,extra='stroke-linecap="round"'))
            if e[k]==3:
                t=.12; s.append(L(a[0]+(b[0]-a[0])*t-ix,a[1]+(b[1]-a[1])*t-iy,a[0]+(b[0]-a[0])*(1-t)-ix,a[1]+(b[1]-a[1])*(1-t)-iy,INK,lw,extra='stroke-linecap="round"'))
    if cat is not None:
        vx,vy=V[cat]; s.append(chg(vx+(cx-vx)*0.45,vy+(cy-vy)*0.45,1,10))
    if an_ is not None:
        vx,vy=V[an_]; ux,uy=(vx-cx)/R,(vy-cy)/R; px,py=-uy,ux; d=0.36*R
        for sg in (-1,1): s.append(f'<circle cx="{f(vx+ux*d+px*sg*5)}" cy="{f(vy+uy*d+py*sg*5)}" r="2.8" fill="{INK}"/>')
        s.append(chg(vx+ux*0.95*R+px*16,vy+uy*0.95*R+py*16,-1,10))
    if mark is not None:
        for k in (mark if isinstance(mark,(list,tuple)) else [mark]):
            vx,vy=V[k]; s.append(T(vx+(cx-vx)*0.42,vy+(cy-vy)*0.42+12,tex='*',size=24,fill=PLUS,weight=700))
    for k,lst in subs.items():
        vx,vy=V[k]; base=math.degrees(math.atan2(-(vy-cy),vx-cx))
        for x in lst:
            if x['fm']=='' and not x['t']: continue
            a=math.radians(base if x['ang'] is None else x['ang']); ux,uy=math.cos(a),-math.sin(a)
            sz=x['size'] or S; ln=x['ln'] or 0.62*R
            disp=x['t']; tex=x['tex'] or ('\\ce{'+disp+'}')
            w=gw(re.sub(r'[\\{}^]','',disp),sz); rx_,ry_=w/2+3,0.5*sz
            rl=1/math.sqrt((ux/rx_)**2+(uy/ry_)**2)
            ex,ey=vx+ux*ln,vy+uy*ln
            if x['o']==2:
                px,py=-uy*3.2,ux*3.2
                s.append(L(vx+px,vy+py,ex+px,ey+py,INK,lw)+L(vx-px,vy-py,ex-px,ey-py,INK,lw))
            else: s.append(L(vx,vy,ex,ey,INK,lw,extra='stroke-linecap="round"'))
            lx,ly=ex+ux*(rl+1),ey+uy*(rl+1)
            if x['al']=='first' or (x['al'] is None and abs(ux)<0.35 and len(disp)>3):
                lx=ex-0.36*sz*(0.9 if disp[0] in 'CNO' else 0.6); anchor='start'; ly=ey+uy*(ry_+2)
            else: anchor='middle'
            if x['hl']: s.append(f'<rect x="{f((lx-w/2 if anchor=="middle" else lx)-3)}" y="{f(ly-0.62*sz)}" width="{f(w+6)}" height="{f(1.2*sz)}" rx="5" fill="{HL}" fill-opacity=".55"/>')
            s.append(T(lx,ly+0.36*sz,tex=tex,size=sz,anchor=anchor,fill=x['col']))
            if x['fc']:
                fx=(lx+w/2+8 if anchor=='middle' else lx+w+8); s.append(chg(fx,ly-0.55*sz,x['fc'],10))
    RG[name or f'r{len(RG)}']=dict(V=V,c=(cx,cy),R=R)
    return ''.join(s)
def emid(nm,k,inner=0.2):
    g=RG[nm]; a,b=g['V'][k],g['V'][(k+1)%6]; cx,cy=g['c']; mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    return mx+(cx-mx)*inner*1.15,my+(cy-my)*inner*1.15
def vx_(nm,k,d=0):
    g=RG[nm]; (x,y)=g['V'][k]; cx,cy=g['c']; return x+(x-cx)/g['R']*d,y+(y-cy)/g['R']*d
def bm(nm,k,ang,ln,fr=.5):
    x,y=RG[nm]['V'][k]; a=math.radians(ang); return x+math.cos(a)*ln*fr,y-math.sin(a)*ln*fr
def hcen(nm,k=0,ang=50,ln=20): return bm(nm,k,ang,ln+12,1)
def deprot(nm,bx,by,k=0,ang=50,ln=20,edge=0,d1=.9,d2=1.1,bend=20):
    hx,hy=hcen(nm,k,ang,ln); 
    return DRAW(curved(bx,by,hx+8,hy-6,bend=bend),d1)+DRAW(curved(*bm(nm,k,ang,ln,.5),*emid(nm,edge),bend=-22),d2)
def same(names,tag):
    a=SPEC[names[0]]
    for n in names[1:]:
        if SPEC[n]!=a: sys.exit(f'[공명 {tag}] {n} {SPEC[n]} ≠ {a}')
    RXN.append('공명 '+tag)
def ion(name,fm,q): SPEC[name]=(formula(fm),q); return name
def combo(names,extra,want,tag):
    c=sum((SPEC[n][0] for n in names),Counter())+formula(extra);
    if +c!=+formula(want): sys.exit(f'[조합 {tag}] {dict(c)} ≠ {want}')
    RXN.append('조합 '+tag)
def lrarr(x1,x2,y,w=2.2): return T((x1+x2)/2,y+9,tex='\\longleftrightarrow',size=24,fill=INK)
def eqarr(x1,x2,y,col=INK):
    return (L(x1,y-4,x2,y-4,col,2.2)+P([(x2-10,y-10),(x2,y-4)],col,2.2)+L(x1,y+4,x2,y+4,col,2.2)+P([(x1+10,y+10),(x1,y+4)],col,2.2))
def brk(x1,y1,x2,y2,ch=None):
    s=P([(x1+9,y1),(x1,y1),(x1,y2),(x1+9,y2)],INK,2.2)+P([(x2-9,y1),(x2,y1),(x2,y2),(x2-9,y2)],INK,2.2)
    return s
def rlab(x,y,t,size=19,fill=INK,weight=None): return lab(x,y,t,size,fill,weight=weight)
H=lambda ang=None,**k: sub('H',ang=ang,**k)

# ═══ S1 표지
def cover():
    s=[]; R=42
    s.append(ring(140,120,R,name='cv C6H6',want='C6H6',S=24))
    s.append(cond(262,112,'Br+',30,fill=PLUS)); s.append(lab(262,150,'친전자체',20,PLUS))
    s.append(DRAW(curved(*emid('cv C6H6',0),240,100,bend=-40,w=3),.4))
    s.append(A(140,186,140,248,'ink',3)); s.append(lab(156,224,'① 느림: 방향성 잃음',20,PLUS,weight=700) if False else T(156,224,mix='① 느림: 방향성 잃음',size=20,anchor='start',fill=PLUS,weight=700))
    s.append(ring(140,330,R,e=aren(0,1),cat=1,subs={0:[H(50,ln=24),sub('Br',ang=128,ln=24)]},name='cv ar',want='C6H6Br',S=24))
    s.append(lab(140,404,'아레늄 이온',20,EQUI,weight=700)); s.append(lab(140,428,'(시그마 착물)',20,EQUI))
    s.append(DRAW(curved(*bm('cv ar',0,50,24),*emid('cv ar',0),bend=-26,w=3),1.0))
    s.append(harrow(228,320,330)); s.append(lab(274,312,'② 빠름',20,FIELD,weight=700)); s.append(lab(274,362,'$\\ce{-H+}$',20,INK))
    s.append(POP(ring(410,330,R,subs={0:[sub('Br')]},name='cv P',want='C6H5Br',S=24),410,330,1.4))
    s.append(lab(410,404,'치환 생성물',20,FIELD,weight=700)); s.append(lab(410,428,'(방향성 회복)',20,FIELD))
    SPEC['cv Br+']=(formula('Br'),1); ion('cv H+','H',1)
    rxn(['cv C6H6','cv Br+'],['cv ar'],'표지 1'); rxn(['cv ar'],['cv P','cv H+'],'표지 2')
    return svg('-20 40 580 420',540,'벤젠의 π 전자쌍이 친전자체를 공격해 아레늄 이온이 생기고, 수소 이온이 떨어져 방향성이 회복되는 친전자성 방향족 치환',s,cls='cover-fig')
FIG['COVER']=cover()

# ═══ S3 생각 열기: 알켄 첨가 vs 벤젠 치환
def openfig():
    s=[]; R=32; y1,y2=70,230
    s.append(ring(70,y1,R,e=(2,1,1,1,1,1),name='o hex',want='C6H10'))
    s.append(lab(70,y1+62,'사이클로헥센',19,INK))
    s.append(plus(140,y1)); s.append(cond(186,y1+8,'Br2',24))
    s.append(harrow(222,290,y1)); s.append(lab(256,y1-16,'첨가',19,INK,weight=700))
    s.append(POP(ring(360,y1,R,e=(1,)*6,subs={0:[sub('Br',ang=110)],1:[sub('Br',ang=-10)]},name='o dib',want='C6H10Br2'),360,y1,.4))
    s.append(lab(360,y1+62,'1,2-다이브로모사이클로헥세인',19,INK))
    s.append(lab(530,y1+8,'2중 결합이 사라짐',19,MUTED,anchor='start'))
    s.append(ring(70,y2,R,name='o bz',want='C6H6')); s.append(lab(70,y2+62,'벤젠',19,INK))
    s.append(plus(140,y2)); s.append(cond(186,y2+8,'Br2',24))
    s.append(harrow(222,290,y2)); s.append(cond(256,y2-14,'FeBr3',19,fill=FIELD)); s.append(lab(256,y2+28,'치환',19,INK,weight=700))
    s.append(POP(ring(360,y2,R,subs={0:[sub('Br')]},name='o pbr',want='C6H5Br'),360,y2,.8))
    s.append(plus(430,y2)); s.append(cond(476,y2+8,'HBr',24))
    s.append(lab(360,y2+62,'브로모벤젠',19,INK)); s.append(lab(530,y2+8,'고리의 π 전자 6개가 남음',19,FIELD,anchor='start'))
    SPEC['o Br2']=(formula('Br2'),0); ion('o HBr','HBr',0)
    rxn(['o hex','o Br2'],['o dib'],'S3 첨가'); rxn(['o bz','o Br2'],['o pbr','o HBr'],'S3 치환')
    return svg('0 -14 780 324',760,'사이클로헥센은 브로민과 첨가 반응을 하고, 벤젠은 브로민화 철 촉매에서 치환 반응을 하여 브로모벤젠이 된다',s)
FIG['OPEN']=openfig()

# ═══ S4 두 단계 메커니즘(일반)
def mech():
    s=[]; R=30; y=120
    s.append(ring(60,y,R,e=(1,2,1,2,1,2),name='m bz',want='C6H6'))
    s.append(cond(140,y+8,'E+',26,fill=PLUS)); s.append(DRAW(curved(*emid('m bz',5),124,y-12,bend=-58),.3))
    s.append(harrow(170,226,y)); s.append(lab(198,y-16,'느림',19,PLUS,weight=700))
    xs=[300,440,580]; cs=[5,3,1]; nm=[]
    s.append(brk(244,30,636,214))
    for i,(x,cc) in enumerate(zip(xs,cs)):
        n=f'm ar{i}'; nm.append(n)
        s.append(ring(x,y,R,e=aren(0,cc),cat=cc,subs={0:[H(50,ln=20),sub('E',ang=128,ln=20,col=PLUS)]},name=n,want='C6H6E'))
        if i<2: s.append(lrarr(x+44,x+96,y))
    s.append(lab(440,238,'아레늄 이온(시그마 착물): 양전하가 세 탄소에 퍼짐',19,EQUI,weight=700))
    same(nm,'S4')
    s.append(cond(690,y-58,'B-',24,fill=MINUS)); s.append(deprot('m ar2',676,y-64))
    s.append(harrow(660,716,y)); s.append(lab(688,y+28,'빠름',19,FIELD,weight=700))
    s.append(POP(ring(790,y,R,subs={0:[sub('E',col=PLUS)]},name='m P',want='C6H5E'),790,y,1.3))
    s.append(plus(850,y)); s.append(cond(896,y+8,'HB',24))
    SPEC['m E+']=(formula('E'),1); SPEC['m B-']=(formula('B'),-1); ion('m HB','HB',0)
    rxn(['m bz','m E+'],['m ar0'],'S4 1'); rxn(['m ar2','m B-'],['m P','m HB'],'S4 2')
    return svg('0 20 930 240',930,'벤젠의 π 전자쌍이 친전자체 E+를 공격하여 공명 구조 세 개를 가진 아레늄 이온이 생기고, 염기가 수소 이온을 떼어 내어 치환 생성물이 된다',s)
FIG['MECH']=mech()

# ═══ S5 에너지 도표
def ear():
    W,H_=560,330; s=[]; x0,y0=50,H_-36
    s.append(eaxes(x0,y0,W-12,22))
    R0=(x0+30,200); T1=(190,52); I=(270,140); T2=(330,112); P0=(W-50,236)
    s.append(DRAW(ecurve([R0,T1,I,T2,P0]),.2,'1.4'))
    s.append(ecurve([I,(390,128),(480,156)],MUTED,2.6,dash='7 6'))
    s.append(seg(R0[0]-22,R0[0]+30,R0[1])); s.append(lab(R0[0]+4,R0[1]+28,'$\\ce{C6H6 + E+}$',19,INK))
    s.append(seg(P0[0]-34,P0[0]+30,P0[1])); s.append(lab(P0[0]-6,P0[1]+28,'치환 생성물',19,FIELD,weight=700))
    s.append(seg(450,510,156,MUTED,2.6,dash='7 6')); s.append(lab(482,146,'첨가 생성물',19,MUTED))
    s.append(C(I[0],I[1],6,EQUI,2,fill=EQUI)); s.append(lab(I[0]+4,I[1]+34,'아레늄 이온',19,EQUI,weight=700)); s.append(lab(I[0]+4,I[1]+56,'(중간체)',19,EQUI))
    s.append(eadim(x0+64,R0[1],T1[1]+4,side=-1))
    s.append(lab(T1[0]+18,T1[1]-14,'속도 결정 단계',19,PLUS,weight=700))
    return svg(f'0 0 {W} {H_}',W,'친전자성 방향족 치환의 에너지 도표: 첫 언덕이 가장 높고 골짜기에 아레늄 이온 중간체, 첨가 생성물은 치환 생성물보다 에너지가 높다',s)
FIG['EAR']=ear()

# ═══ S6 여러 가지 치환 반응
def over():
    s=[]; R=26; cx,cy=290,190
    s.append(ring(cx,cy,32,name='ov bz',want='C6H6',S=20))
    items=[(90,70,'X','X','할로젠화','C6H5X'),(490,70,'NO2','NO2','나이트로화','C6H5NO2'),(90,320,'SO3H','SO3H','설폰화','C6H5SO3H'),
           (490,320,'COR','COR','아실화','C6H5COR'),(290,370,'R','R','알킬화','C6H5R')]
    for i,(x,y,t,fm,nm_,w) in enumerate(items):
        fm2=fm.replace('X','Cl').replace('R','Q'); w2=w.replace('X','Cl').replace('R','Q')
        dx,dy=x-cx,y-cy; n=math.hypot(dx,dy); ux,uy=dx/n,dy/n
        s.append(A(cx+ux*52,cy+uy*52,x-ux*58,y-uy*58,'muted',2.4))
        g=ring(x,y-10,R,subs={0:[sub(t,fm=fm2,col=PLUS)]},name=f'ov{i}',want=w2,S=20)+lab(x,y+42,nm_,19,INK,weight=700)
        s.append(POP(g,x,y,.2+.25*i))
    return svg('0 -24 580 444',500,'벤젠 고리의 친전자성 치환 반응: 할로젠화, 나이트로화, 설폰화, 알킬화, 아실화',s)
FIG['OVER']=over()

# ═══ S7 브로민화 메커니즘
def brom():
    s=[]; R=30; y=130
    s.append(ring(60,y,R,name='b bz',want='C6H6'))
    s.append(cond(196,y+8,'Br-Br-FeBr3',22)); s.append(dlab(132,y-22,1,19)); s.append(dlab(176,y-22,-1,19))
    s.append(DRAW(curved(*emid('b bz',0),124,y-8,bend=-34),.3)); s.append(DRAW(curved(150,y-12,174,y-12,bend=-16),.7))
    s.append(harrow(268,322,y)); s.append(lab(295,y-16,'① 느림',19,PLUS,weight=700))
    s.append(ring(400,y,R,e=aren(0,1),cat=1,subs={0:[H(50,ln=20),sub('Br',ang=128,ln=20)]},name='b ar',want='C6H6Br'))
    s.append(lab(400,y+64,'아레늄 이온(공명 3개)',19,EQUI))
    s.append(cond(500,y-46,'FeBr4-',22,fill=MINUS)); s.append(deprot('b ar',474,y-56))
    s.append(harrow(560,614,y)); s.append(lab(587,y-16,'② 빠름',19,FIELD,weight=700))
    s.append(POP(ring(690,y,R,subs={0:[sub('Br')]},name='b P',want='C6H5Br'),690,y,1.5))
    s.append(cond(790,y+8,'+ HBr + FeBr3',22))
    SPEC['b cx']=(formula('FeBr5'),0); ion('b FeBr4-','FeBr4',-1); ion('b HBr','HBr',0); ion('b FeBr3','FeBr3',0)
    rxn(['b bz','b cx'],['b ar','b FeBr4-'],'S7 1'); rxn(['b ar','b FeBr4-'],['b P','b HBr','b FeBr3'],'S7 2')
    return svg('0 40 880 200',880,'브로민화 철이 편극시킨 브로민을 벤젠이 공격해 아레늄 이온이 되고, 사브로민화 철 이온이 수소 이온을 떼어 내어 브로모벤젠이 된다',s)
FIG['BROM']=brom()

# ═══ S8 나이트로화
def nitr():
    s=[]; R=30; y=110
    s.append(ring(60,y,R,name='n bz',want='C6H6'))
    s.append(T(176,y+8,tex='\\mathrm{O{=}\\overset{+}{N}{=}O}',size=24,fill=PLUS)); s.append(DRAW(curved(*emid('n bz',0),150,y-14,bend=-34),.3))
    s.append(harrow(228,282,y)); s.append(lab(255,y-16,'느림',19,PLUS,weight=700))
    s.append(ring(360,y,R,e=aren(0,1),cat=1,subs={0:[H(50,ln=20),sub('NO2',ang=128,ln=20)]},name='n ar',want='C6H6NO2'))
    s.append(cond(452,y-52,'H2O',22,fill=MINUS)); s.append(deprot('n ar',434,y-58))
    s.append(harrow(470,524,y)); s.append(lab(497,y+28,'빠름',19,FIELD,weight=700))
    s.append(POP(ring(600,y,R,subs={0:[sub('NO2')]},name='n P',want='C6H5NO2'),600,y,1.3))
    s.append(cond(690,y+8,'+ H3O+',22)); s.append(lab(600,y+64,'나이트로벤젠',19,INK))
    ion('n NO2+','NO2',1); ion('n H2O','H2O',0); ion('n H3O+','H3O',1)
    rxn(['n bz','n NO2+'],['n ar'],'S8 1'); rxn(['n ar','n H2O'],['n P','n H3O+'],'S8 2')
    return svg('0 30 740 164',700,'나이트로늄 이온을 벤젠이 공격해 아레늄 이온이 되고 물이 수소 이온을 떼어 내어 나이트로벤젠이 된다',s)
FIG['NITR']=nitr()
def anil():
    s=[]; R=26; y=60
    s.append(ring(62,y,R,subs={0:[sub('NO2')]},name='an a',want='C6H5NO2',S=19))
    s.append(harrow(106,196,y)); s.append(lab(151,y-14,'1. Fe, $\\ce{H3O+}$',19,FIELD)); s.append(lab(148,y+26,'2. $\\ce{OH-}$',19,FIELD))
    s.append(ring(246,y,R,subs={0:[sub('NH2')]},name='an b',want='C6H7N',S=19))
    s.append(lab(246,y+52,'아닐린 (95 %)',19,INK)); s.append(lab(62,y+52,'나이트로벤젠',19,INK))
    return svg('0 -22 310 156',270,'나이트로벤젠을 철과 산으로 환원하면 아닐린이 된다',s)
FIG['ANIL']=anil()

# ═══ S9 설폰화
def sulf():
    s=[]; R=30; y=110
    s.append(ring(60,y,R,name='s bz',want='C6H6'))
    s.append(cond(150,y+8,'HSO3+',24,fill=PLUS)); s.append(DRAW(curved(*emid('s bz',0),128,y-14,bend=-34),.3))
    s.append(eqarr(194,244,y))
    s.append(ring(330,y,R,e=aren(0,1),cat=1,subs={0:[H(50,ln=20),sub('SO3H',ang=132,ln=20)]},name='s ar',want='C6H6SO3H'))
    s.append(cond(430,y-52,'HSO4-',22,fill=MINUS)); s.append(deprot('s ar',404,y-58))
    s.append(eqarr(446,496,y))
    s.append(POP(ring(570,y,R,subs={0:[sub('SO3H')]},name='s P',want='C6H5SO3H'),570,y,1.3))
    s.append(cond(670,y+8,'+ H2SO4',22)); s.append(lab(570,y+64,'벤젠설폰산',19,INK))
    ion('s HSO3+','HSO3',1); ion('s HSO4-','HSO4',-1); ion('s H2SO4','H2SO4',0)
    rxn(['s bz','s HSO3+'],['s ar'],'S9 1'); rxn(['s ar','s HSO4-'],['s P','s H2SO4'],'S9 2')
    return svg('0 20 730 180',730,'벤젠과 HSO3+가 아레늄 이온을 거쳐 벤젠설폰산이 되는 가역 반응',s)
FIG['SULF']=sulf()

# ═══ S10 프리델–크래프츠 알킬화
def fca():
    s=[]; R=30; y=120
    s.append(ring(60,y,R,name='f bz',want='C6H6'))
    s.append(cond(170,y+8,'(CH3)2CH+',24,fill=PLUS)); s.append(DRAW(curved(*emid('f bz',0),136,y-14,bend=-34),.3))
    s.append(harrow(234,288,y)); s.append(lab(261,y-16,'①',19,PLUS,weight=700))
    s.append(ring(372,y,R,e=aren(0,1),cat=1,subs={0:[H(50,ln=20),sub('CH(CH3)2',ang=162,ln=28,al='mid')]},name='f ar',want='C9H13'))
    s.append(cond(480,y-46,'AlCl4-',22,fill=MINUS)); s.append(deprot('f ar',452,y-56))
    s.append(harrow(540,594,y)); s.append(lab(567,y-16,'②',19,FIELD,weight=700))
    s.append(POP(ring(670,y,R,subs={0:[sub('CH(CH3)2')]},name='f P',want='C9H12'),670,y,1.3))
    s.append(cond(800,y+8,'+ HCl + AlCl3',22)); s.append(lab(670,y+64,'아이소프로필벤젠(쿠멘)',19,INK))
    ion('f R+','C3H7',1); ion('f AlCl4-','AlCl4',-1); ion('f HCl','HCl',0); ion('f AlCl3','AlCl3',0)
    rxn(['f bz','f R+'],['f ar'],'S10 1'); rxn(['f ar','f AlCl4-'],['f P','f HCl','f AlCl3'],'S10 2')
    return svg('0 30 890 190',890,'탄소 양이온을 벤젠이 공격하고 수소 이온이 떨어져 쿠멘이 되는 프리델-크래프츠 알킬화',s)
FIG['FCA']=fca()
def fcl():
    s=[]; R=26; y=56
    s.append(ring(50,y,R,name='fl bz',want='C6H6',S=19))
    s.append(harrow(92,206,y)); s.append(cond(149,y-12,'CH3(CH2)3Cl',19,fill=FIELD)); s.append(cond(149,y+28,'AlCl3',19,fill=FIELD))
    s.append(ring(262,y,R,subs={0:[sub('CH(CH3)CH2CH3',al='first')]},name='fl a',want='C10H14',S=19)); s.append(lab(262,y+52,'2-페닐뷰테인 65 %',19,INK))
    s.append(plus(380,y))
    s.append(ring(450,y,R,subs={0:[sub('CH2CH2CH2CH3',al='first')]},name='fl b',want='C10H14',S=19)); s.append(lab(450,y+52,'뷰틸벤젠 35 %',19,INK))
    return svg('0 -14 620 144',560,'벤젠과 1-클로로뷰테인의 알킬화에서 자리 옮김 생성물 2-페닐뷰테인이 65 %, 뷰틸벤젠이 35 % 생긴다',s)
FIG['FCL']=fcl()

# ═══ S12 아실화
def fcy():
    s=[]; R=26; y1,y2=60,190
    s.append(ring(50,y1,R,name='y bz',want='C6H6',S=19))
    s.append(harrow(92,206,y1)); s.append(cond(149,y1-12,'CH3CH2COCl',19,fill=FIELD)); s.append(cond(149,y1+28,'AlCl3',19,fill=FIELD))
    s.append(ring(262,y1,R,subs={0:[sub('COCH2CH3',al='first')]},name='y k',want='C9H10O',S=19)); s.append(lab(262,y1+52,'아릴 케톤',19,INK))
    s.append(harrow(318,410,y1)); s.append(cond(364,y1-12,'H2, Pd',19,fill=FIELD))
    s.append(POP(ring(470,y1,R,subs={0:[sub('CH2CH2CH3',al='first')]},name='y p',want='C9H12',S=19)+lab(470,y1+52,'프로필벤젠만',19,FIELD,weight=700),470,y1,.6))
    s.append(ring(50,y2,R,name='y bz2',want='C6H6',S=19))
    s.append(harrow(92,206,y2)); s.append(cond(149,y2-12,'CH3CH2CH2Cl',19,fill=FIELD)); s.append(cond(149,y2+28,'AlCl3',19,fill=FIELD))
    s.append(ring(262,y2,R,subs={0:[sub('CH(CH3)2',al='first')]},name='y i',want='C9H12',S=19))
    s.append(plus(340,y2)); s.append(ring(420,y2,R,subs={0:[sub('CH2CH2CH3',al='first')]},name='y p2',want='C9H12',S=19))
    s.append(lab(340,y2+52,'혼합물(자리 옮김)',19,PLUS,weight=700))
    ion('y acyl','C3H5ClO',0); ion('y HCl','HCl',0); rxn(['y bz','y acyl'],['y k','y HCl'],'S12 아실화')
    return svg('0 -10 600 274',540,'아실화한 뒤 환원하면 프로필벤젠만 생기지만, 1-클로로프로페인으로 직접 알킬화하면 자리 옮김 때문에 혼합물이 생긴다',s)
FIG['FCY']=fcy()

# ═══ S14 오쏘·메타·파라
def omp():
    s=[]; R=56; cx,cy=170,190
    s.append(ring(cx,cy,R,subs={0:[sub('Y',fm='Z',ln=36)]},name='omp',want='C6H5Z',S=26))
    V=RG['omp']['V']
    for k,t,c_ in ((1,'오쏘',PLUS),(5,'오쏘',PLUS),(2,'메타',MINUS),(4,'메타',MINUS),(3,'파라',FIELD)):
        x,y=vx_('omp',k,44); s.append(lab(x,y-4,t,20,c_,weight=700)); s.append(T(x,y+20,tex='\\mathrm{C'+str({1:2,5:6,2:3,4:5,3:4}[k])+'}',size=19,fill=MUTED))
    x,y=vx_('omp',0,0); s.append(T(x+16,y+4,tex='\\mathrm{C1}',size=19,fill=MUTED,anchor='start'))
    return svg('0 40 340 320',330,'치환기 Y가 붙은 탄소를 1번으로 할 때 2·6번은 오쏘, 3·5번은 메타, 4번은 파라 위치',s)
FIG['OMP']=omp()

# ═══ S15–S18 지향 효과 공명 구조
def subs_sp3(sv):
    a=math.degrees(math.atan2(-(rv(0,0,1)[sv][1]),rv(0,0,1)[sv][0]))
    if sv==1: return [H(a+44,ln=16),sub('NO2',ang=a-28,ln=16)]
    return [H(a+40,ln=16),sub('NO2',ang=a-34,ln=16)]
def ofig(key,Y,yfm,rows,R=28,yS=19,aria='',hlnote=None,W=840):
    s=[]; dy=148; y0=82
    for ri,(nm_,sv,pct,hlmap,ex4) in enumerate(rows):
        y=y0+ri*dy; xs=[214+i*186 for i in range(4)]
        s.append(lab(64,y-4,nm_+' 공격',20,INK,weight=700)); s.append(lab(64,y+24,pct,20,MUTED))
        order=[(sv+1)%6,(sv+3)%6,(sv+5)%6]; names=[]
        for i,cc in enumerate(order):
            n=f'{key}{ri}{i}'; names.append(n)
            s.append(ring(xs[i],y,R,e=aren(sv,cc),cat=cc,subs={0:[sub(Y,fm=yfm,size=yS)],sv:subs_sp3(sv)},name=n,S=19,box=hlmap.get(cc)))
            if i<2 or ex4: s.append(lrarr(xs[i]+88,xs[i]+128,y))
        if ex4:
            n=f'{key}{ri}3'; names.append(n); s.append(ex4(xs[3],y,n,sv,R))
        same(names,key+nm_)
    if hlnote: s.append(hlnote)
    H_=82+148*(len(rows)-1)+86
    return svg(f'0 0 {W} {H_}',W,aria,s)
def oxonium(Yt,Yfm,col):
    def f4(x,y,n,sv,R):
        # 넷째 구조: 치환기의 비공유 전자쌍이 고리로 들어가 C1=Y+ (고리 결합은 c=0 구조와 같음)
        g=ring(x,y,R,e=aren(sv,0),subs={0:[sub(Yt,fm=Yfm,o=2,fc=1,size=19)],sv:subs_sp3(sv)},name=n,S=19)
        return f'<rect x="{f(x-R-24)}" y="{f(y-R-36)}" width="{f(2*R+48)}" height="{f(2*R+68)}" rx="10" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-width="2.4"/>'+g
    return f4
FIG['TOL']=ofig('t','CH3','CH3',[('오쏘',1,'63 %',{0:FIELD},None),('메타',2,'3 %',{},None),('파라',3,'34 %',{0:FIELD},None)],
    aria='톨루엔의 나이트로화 중간체: 오쏘와 파라 공격에는 양전하가 메틸기가 붙은 3차 탄소에 오는 구조(초록 상자)가 있다',W=700)
FIG['PHE']=ofig('p','OH','OH',[('메타',2,'0 %',{},None),('파라',3,'50 %',{},oxonium('OH','OH',FIELD))],
    aria='페놀의 나이트로화 중간체: 파라 공격에서는 산소의 비공유 전자쌍이 양전하를 나누어 맡는 넷째 구조가 있다',W=940)
FIG['CLB']=ofig('c','Cl','Cl',[('메타',2,'1 %',{},None),('파라',3,'64 %',{},oxonium('Cl','Cl',FIELD))],
    aria='클로로벤젠의 나이트로화 중간체: 파라 공격에서 염소의 비공유 전자쌍이 양전하를 나누어 맡는 구조가 있다',W=940)
FIG['BZA']=ofig('a','CHO','CHO',[('메타',2,'72 %',{},None),('파라',3,'9 %',{0:PLUS},None)],
    aria='벤즈알데하이드의 나이트로화 중간체: 파라 공격에서는 양전하가 전자를 끄는 치환기 바로 옆에 오는 가장 불안정한 구조(빨간 상자)가 생긴다',W=700)

# ═══ S20 반응성 순서(로그 눈금)
def rate():
    s=[]; x0,x1,y=40,960,80; lo,hi=-8,3
    def X(e_): return x0+(e_-lo)/(hi-lo)*(x1-x0)
    s.append(f'<defs><linearGradient id="grad-ac14s2-20" x1="0" x2="1"><stop offset="0" stop-color="{MINUS}"/><stop offset=".55" stop-color="{BF}"/><stop offset="1" stop-color="{PLUS}"/></linearGradient></defs>')
    s.append(f'<rect x="{x0}" y="{y-6}" width="{x1-x0}" height="12" rx="6" fill="url(#grad-ac14s2-20)"/>')
    for e_ in range(lo,hi+1,2): s.append(L(X(e_),y+8,X(e_),y+16,MUTED,2)+T(X(e_),y+40,tex='10^{'+str(e_)+'}',size=19,fill=MUTED))
    pts=[(math.log10(6e-8),'-NO2','6\\times10^{-8}'),(math.log10(0.033),'-Cl','0.033'),(0,'-H','1'),(math.log10(25),'-CH3','25'),(3,'-OH','1000')]
    for i,(e_,t,v) in enumerate(pts):
        x=X(e_); g=C(x,y,7,INK,2,fill='#fff')+T(x,y-46,tex='\\ce{'+t+'}',size=21,weight=700)+T(x,y-22,tex=v,size=19,fill=MUTED)
        s.append(POP(g,x,y,.2+.2*i))
    s.append(lab(500,y+72,'나이트로화의 상대 속도 (벤젠 = 1, 로그 눈금)',19,MUTED))
    return svg('0 14 1000 150',1000,'나이트로화의 상대 속도: 나이트로벤젠 6×10⁻⁸, 클로로벤젠 0.033, 벤젠 1, 톨루엔 25, 페놀 1000',s)
FIG['RATE']=rate()

# ═══ S21 톨루엔 설폰화 예제
def ex1():
    s=[]; R=28; y=88
    s.append(ring(50,y,R,subs={0:[sub('CH3')]},name='e1 t',want='C7H8'))
    s.append(harrow(94,196,y)); s.append(cond(145,y-14,'SO3',19,fill=FIELD)); s.append(cond(145,y+28,'H2SO4',19,fill=FIELD))
    prods=[(290,{0:[sub('CH3')],3:[sub('SO3H')]},'파라 (주)',FIELD),(470,{0:[sub('CH3')],1:[sub('SO3H')]},'오쏘',INK),(650,{0:[sub('CH3')],2:[sub('SO3H')]},'메타 (소량)',MUTED)]
    for i,(x,sb,t,c_) in enumerate(prods):
        g=ring(x,y,R,subs=sb,name=f'e1 {i}',want='C7H8O3S')+lab(x,y+96,t,20,c_,weight=700)
        s.append(step(g,f'e1{i}'))
    return svg('0 10 760 200',760,'톨루엔의 설폰화 생성물: 파라가 주생성물, 오쏘, 메타는 소량',s)
FIG['EX1']=ex1()

# ═══ S22 곁사슬 산화
def oxi():
    s=[]; R=28; y1,y2=70,220
    s.append(ring(70,y1,R,subs={0:[sub('CH2CH2CH2CH3',al='first',hl=True)]},name='x b',want='C10H14'))
    s.append(harrow(130,236,y1)); s.append(cond(183,y1-12,'KMnO4',19,fill=FIELD)); s.append(cond(183,y1+28,'H2O',19,fill=FIELD))
    s.append(POP(ring(300,y1,R,subs={0:[sub('COOH',al='first')]},name='x a',want='C7H6O2'),300,y1,.4))
    s.append(lab(70,y1+56,'뷰틸벤젠',19,INK)); s.append(lab(300,y1+56,'벤조산 (85 %)',19,INK))
    s.append(ring(70,y2,R,subs={0:[sub('C(CH3)3',al='first')]},name='x t',want='C10H14'))
    s.append(harrow(130,236,y2)); s.append(cond(183,y2-12,'KMnO4',19,fill=FIELD)); s.append(lab(300,y2+8,'반응하지 않음',21,PLUS,weight=700))
    s.append(lab(70,y2+56,'tert-뷰틸벤젠',19,INK)); s.append(lab(300,y2+40,'(벤질 자리에 H 없음)',19,MUTED))
    return svg('0 -6 420 310',420,'뷰틸벤젠은 과망가니즈산 칼륨에 산화되어 벤조산이 되지만, 벤질 자리에 수소가 없는 tert-뷰틸벤젠은 산화되지 않는다',s)
FIG['OXI']=oxi()

# ═══ S23 예제 (1)
def ex2():
    s=[]; R=28; y=100
    s.append(ring(50,y,R,subs={0:[sub('CH3')]},name='e2 a',want='C7H8')); s.append(lab(50,y+74,'톨루엔',19,INK))
    s.append(harrow(92,186,y)); s.append(lab(139,y-16,'① 아실화',19,FIELD))
    g=ring(250,y,R,subs={0:[sub('CH3')],3:[sub('COCH3',al='first')]},name='e2 b',want='C9H10O')
    s.append(step(g,'e2b'))
    s.append(harrow(316,410,y)); s.append(lab(363,y-16,'② 나이트로화',19,FIELD))
    g=ring(474,y,R,subs={0:[sub('CH3')],1:[sub('NO2',hl=True)],3:[sub('COCH3',al='first')]},name='e2 c',want='C9H9NO3')
    s.append(step(g,'e2c'))
    s.append(harrow(560,654,y)); s.append(lab(607,y-16,'③ $\\ce{H2}$, Pd',19,FIELD))
    g=ring(720,y,R,subs={0:[sub('CH3')],1:[sub('NH2',hl=True)],3:[sub('CH2CH3',al='first',hl=True)]},name='e2 d',want='C9H13N')+lab(720,y+104,'5-에틸-2-메틸아닐린',19,FIELD,weight=700)
    s.append(step(g,'e2d'))
    return svg('0 10 820 206',820,'톨루엔을 아실화, 나이트로화, 환원하여 5-에틸-2-메틸아닐린을 얻는 과정',s)
FIG['EX2']=ex2()
def ex3(i):
    R=26; y=64; s=[]
    if i==2:
        s.append(ring(46,y,R,subs={0:[sub('Cl')]},name='e3 a',want='C6H5Cl',S=19)); s.append(harrow(84,178,y)); s.append(cond(131,y-12,'CH3CH2Cl',19,fill=FIELD)); s.append(cond(131,y+28,'AlCl3',19,fill=FIELD))
        g=ring(232,y,R,subs={0:[sub('Cl')],3:[sub('CH2CH3',al='first')]},name='e3 b',want='C8H9Cl',S=19)
        g+=ring(336,y,R,subs={0:[sub('Cl')],1:[sub('CH2CH3',al='first')]},name='e3 c',want='C8H9Cl',S=19)
    if i==3:
        s.append(ring(46,y,R,subs={0:[sub('COCH3',al='first')],1:[sub('NO2')]},name='e3 d',want='C8H7NO3',S=19)); s.append(harrow(110,196,y)); s.append(cond(153,y-12,'H2, Pd',19,fill=FIELD))
        g=ring(252,y,R,subs={0:[sub('CH2CH3',al='first')],1:[sub('NH2')]},name='e3 e',want='C8H11N',S=19)
    if i==4:
        s.append(ring(46,y,R,subs={0:[sub('CH3')]},name='e3 f',want='C7H8',S=19)); s.append(harrow(84,178,y)); s.append(lab(131,y-12,'1. $\\ce{Cl2}$, $\\ce{FeCl3}$',19,FIELD)); s.append(lab(131,y+28,'2. $\\ce{KMnO4}$',19,FIELD))
        g=ring(232,y,R,subs={0:[sub('COOH',al='first')],3:[sub('Cl')]},name='e3 g',want='C7H5ClO2',S=19)
        g+=ring(356,y,R,subs={0:[sub('COOH',al='first')],1:[sub('Cl')]},name='e3 h',want='C7H5ClO2',S=19)
    if i==5:
        s.append(ring(46,y,R,subs={0:[sub('N(CH2CH3)2',al='first')]},name='e3 i',want='C10H15N',S=19)); s.append(harrow(84,178,y)); s.append(cond(131,y-12,'SO3',19,fill=FIELD)); s.append(cond(131,y+28,'H2SO4',19,fill=FIELD))
        g=ring(252,y,R,subs={0:[sub('N(CH2CH3)2',al='first')],2:[sub('SO3H')]},name='e3 j',want='C10H15NO3S',S=19)
    s.append(step(g,f'e3{i}'))
    return svg('0 -14 450 152',420,f'예제 ({i})의 반응물과 생성물',s)
for i in (2,3,4,5): FIG[f'EX3_{i}']=ex3(i)

# ═══ S25 벤자인
def bzy():
    s=[]; R=28; y=86
    s.append(ring(50,y,R,subs={0:[sub('Br')]},name='z a',want='C6H5Br'))
    s.append(cond(124,y-44,'NH2-',20,fill=MINUS)); s.append(DRAW(curved(110,y-46,84,y-36,bend=-10),.3))
    s.append(harrow(104,160,y)); s.append(lab(132,y+30,'$\\ce{NH3}$ 생성',19,INK))
    s.append(ring(220,y,R,subs={0:[sub('Br')]},an_=1,name='z b',want='C6H4Br'))
    s.append(lab(220,y+70,'아릴 음이온',19,INK))
    s.append(harrow(282,338,y)); s.append(lab(310,y+30,'$\\ce{Br-}$ 이탈',19,INK)); s.append(lab(310,y-16,'제거',19,BF,weight=700))
    s.append(brk(352,y-48,452,y+48)); s.append(ring(402,y,R,e=(3,1,2,1,2,1),name='z c',want='C6H4'))
    s.append(lab(402,y+70,'벤자인',19,EQUI,weight=700))
    s.append(harrow(466,522,y)); s.append(lab(494,y-16,'첨가',19,FIELD,weight=700)); s.append(lab(494,y+30,'$\\ce{NH2-}$',19,MINUS))
    s.append(ring(586,y,R,subs={0:[sub('NH2')]},an_=1,name='z d',want='C6H6N'))
    s.append(harrow(648,704,y)); s.append(lab(676,y+30,'$\\ce{NH3}$',19,INK))
    s.append(POP(ring(770,y,R,subs={0:[sub('NH2')]},name='z e',want='C6H7N'),770,y,.8)); s.append(lab(770,y+70,'아닐린',19,INK))
    ion('z NH2-','NH2',-1); ion('z NH3','NH3',0); ion('z Br-','Br',-1)
    rxn(['z a','z NH2-'],['z b','z NH3'],'S25 1'); rxn(['z b'],['z c','z Br-'],'S25 2'); rxn(['z c','z NH2-'],['z d'],'S25 3'); rxn(['z d','z NH3'],['z e','z NH2-'],'S25 4')
    return svg('0 0 830 180',830,'브로모벤젠에서 수소 이온과 브로민화 이온이 떨어져 벤자인이 생기고, 아마이드 이온이 첨가되어 아닐린이 되는 제거-첨가 경로',s)
FIG['BZY']=bzy()
def bzy2():
    s=[]; R=26; y=60
    s.append(ring(46,y,R,subs={0:[sub('Br')]},mark=0,name='z2 a',want='C6H5Br',S=19))
    s.append(harrow(86,170,y)); s.append(cond(128,y-12,'NaNH2',19,fill=FIELD))
    s.append(ring(226,y,R,subs={0:[sub('NH2')]},mark=0,name='z2 b',want='C6H7N',S=19)); s.append(lab(226,y+56,'50 %',20,INK,weight=700))
    s.append(plus(290,y))
    s.append(ring(350,y,R,subs={1:[sub('NH2')]},mark=0,name='z2 c',want='C6H7N',S=19)); s.append(lab(350,y+56,'50 %',20,INK,weight=700))
    return svg('0 -26 420 160',400,'14C로 표지한 탄소(별표)에 아미노기가 붙은 것과 이웃 탄소에 붙은 것이 50 : 50으로 생긴다',s)
FIG['BZY2']=bzy2()

# ═══ S26 다이아조화
def diaz():
    s=[]; R=28; y=64
    s.append(ring(50,y,R,subs={0:[sub('NH2')]},name='d a',want='C6H7N')); s.append(lab(50,y+58,'아닐린',19,INK))
    s.append(harrow(96,234,y)); s.append(lab(165,y-14,'$\\ce{NaNO2}$, $\\ce{HCl}$',19,FIELD)); s.append(lab(165,y+30,'0~5 °C',19,FIELD))
    s.append(POP(ring(290,y,R,subs={0:[sub('N#N',fm='N2',fc=1,tex='\\mathrm{N{\\equiv}N}',al='first')]},name='d b',want='C6H5N2'),290,y,.4))
    s.append(lab(290,y+58,'벤젠다이아조늄 이온',19,INK))
    return svg('0 -16 400 160',380,'아닐린을 차갑게 아질산과 반응시키면 벤젠다이아조늄 이온이 생긴다',s)
FIG['DIAZ']=diaz()

# ═══ S27 다이아조늄 치환
def sand():
    s=[]; cx,cy=300,190
    s.append(ring(cx,cy,32,subs={0:[sub('N#N',fm='N2',fc=1,tex='\\mathrm{N{\\equiv}N}',al='first')]},name='sd',want='C6H5N2',S=20))
    items=[(-150,'CuCl','\\ce{C6H5Cl}','산드마이어'),(-110,'CuBr','\\ce{C6H5Br}','산드마이어'),(-70,'CuCN','\\ce{C6H5CN}','산드마이어'),
           (-30,'KI','\\ce{C6H5I}',''),(200,'H2O, 가열','\\ce{C6H5OH}',''),(160,'H3PO2','\\ce{C6H6}','$\\ce{NH2}$ 없애기')]
    pos=[(90,330),(220,360),(380,360),(520,300),(70,110),(70,210)]
    pos=[(80,330),(230,370),(390,370),(530,300),(80,80),(80,200)]
    for i,((x,y),(_,rg,pr,nt)) in enumerate(zip(pos,items)):
        dx,dy=x-cx,y-cy; n=math.hypot(dx,dy); ux,uy=dx/n,dy/n
        a=A(cx+ux*46,cy+uy*46,x-ux*44,y-uy*44,'muted',2.2)
        g=T(x,y+8,tex=pr,size=22,weight=700)+lab((cx+x)/2+uy*20,(cy+y)/2-ux*20+6,('$\\ce{'+rg+'}$' if ',' not in rg else '$\\ce{H2O}$, 가열'),19,FIELD,halo=True)
        if nt: g+=lab(x,y+34,nt,19,MUTED)
        s.append(POP(a+g,x,y,.2+.15*i))
    return svg('0 40 610 370',590,'벤젠다이아조늄 이온의 치환 반응: 염화·브로민화·사이안화 구리(I)로 산드마이어 반응, 아이오딘화 칼륨, 물, 하이포아인산',s)
FIG['SAND']=sand()

# ═══ S28 짝지음 반응(아조 화합물)
def azo(Y,yfm,want,nm,col,colname,x0=0):
    s=[]; R=26; y=60
    s.append(ring(x0+60,y,R,rot=0,subs={0:[sub('',fm='')]},name=nm+'A'))
    xa,ya=vx_(nm+'A',0,0); n1=(xa+30,ya+26); n2=(xa+66,ya);
    s.append(L(xa,ya,n1[0]-8,n1[1]-7,INK,2.4)); s.append(T(n1[0],n1[1]+8,tex='\\mathrm{N}',size=20))
    s.append(L(n1[0]+8,n1[1]-8,n2[0]-9,n2[1]+6,INK,2.4)+L(n1[0]+4,n1[1]-13,n2[0]-12,n2[1]+1,INK,2.4)); s.append(T(n2[0]+2,n2[1]+2,tex='\\mathrm{N}',size=20))
    rbx=n2[0]+40
    s.append(ring(rbx+R,ya+26,R,rot=0,subs={0:[sub(Y,fm=yfm,al='mid' if False else None)],3:[sub('',fm='')]},name=nm+'B'))
    xb,yb=vx_(nm+'B',3,0); s.append(L(n2[0]+10,n2[1]+6,xb,yb,INK,2.4))
    combo([nm+'A',nm+'B'],'N2',want,nm)
    s.append(f'<rect x="{x0+10}" y="{y+62}" width="34" height="22" rx="5" fill="{col}" stroke="{INK}" stroke-width="1"/>')
    s.append(lab(x0+52,y+80,colname,19,INK,anchor='start'))
    return s
def azofig():
    s=azo('OH','OH','C12H10N2O','az1','#F28C28','파라-하이드록시아조벤젠 (주황색)',0)
    s+=['<g transform="translate(0,150)">']+azo('N(CH3)2','N(CH3)2','C14H15N3','az2','#F2C200','파라-(다이메틸아미노)아조벤젠 (노란색)',0)+['</g>']
    return svg('0 10 400 290',400,'짝지음 반응으로 생긴 아조 화합물: 파라-하이드록시아조벤젠(주황색)과 파라-(다이메틸아미노)아조벤젠(노란색)',s)
FIG['AZO']=azofig()

# ═══ S29 카보닐 친핵성 첨가 (lewis)
def carb():
    S=24; s=[]; y=120
    s.append(M([A_('C',60,y,lp=['l'],fc=-1,fcp='u'),A_('N',112,y,lp=['r'])],[(0,1,3,'l')],'CN',S=S,name='cb CN-'))
    s.append(lab(86,y+60,'친핵체',19,MINUS))
    a=[A_('C',260,y),G_('R',214,y+54,fm='Q'),G_('H',214,y-54,fm='H'),O_(330,y,['u','d'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,2,'l')],'CHQO',S=S,name='cb ald'))
    s.append(dlab(262,y-30,1,20)); s.append(dlab(332,y-36,-1,20))
    sx,sy=lpxy(60,y,'l','C',S); s.append(DRAW(curved(sx-2,sy-6,238,y-18,bend=-70),.3)); s.append(DRAW(curved(290,y-10,326,y-30,bend=-18),.8))
    s.append(lab(300,y+96,'평면 삼각형 ($sp^2$)',19,INK))
    s.append(harrow(370,426,y))
    a=[A_('C',530,y),G_('R',486,y+54,fm='Q'),G_('H',530,y-56,fm='H'),G_('CN',464,y-24,fm='CN'),O_(598,y,['u','d','r'],fc=-1,fcp='ur')]
    s.append(POP(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],'C2HQNO',S=S,name='cb alk'),530,y,1.1))
    s.append(lab(540,y+86,'사면체 ($sp^3$) 알코올산 이온',19,EQUI,weight=700))
    rxn(['cb CN-','cb ald'],['cb alk'],'S29')
    return svg('0 40 680 200',660,'사이안화 이온이 알데하이드의 부분 양전하를 띤 카보닐 탄소를 공격하고 π 전자가 산소로 옮겨 가 사면체 알코올산 이온이 된다',s)
FIG['CARB']=carb()

# ═══ S30 그리냐르
def grig():
    S=22; s=[]; y=110
    a=[G_('R',40,y,fm='Q'),G_('MgBr',124,y,fm='MgBr')]
    s.append(M(a,[(0,1,1,'l')],'QMgBr',S=S,name='g RMgBr'))
    s.append(dlab(40,y-28,-1,20)); s.append(dlab(116,y-28,1,20))
    a=[A_('C',260,y),G_('R',214,y+50,fm='Z'),G_('R',214,y-50,fm='X'),O_(326,y,['u','d'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,2,'l')],'CXZO',S=S,name='g ket'))
    s.append(DRAW(curved(62,y-10,238,y-14,bend=-48),.3)); s.append(DRAW(curved(288,y-10,322,y-28,bend=-16),.8))
    s.append(harrow(362,410,y)); s.append(lab(386,y-16,'첨가',19,INK))
    a=[A_('C',500,y),G_('R',456,y+48,fm='Z'),G_('R',456,y-48,fm='X'),G_('R',500,y+56,fm='Q',col=PLUS),O_(564,y,['u','d','r'],fc=-1,fcp='u')]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],'CXZQO',S=S,name='g alk'))
    s.append(cond(620,y+8,'^+MgBr',20))
    s.append(harrow(664,722,y)); s.append(cond(693,y-14,'H3O+',19,fill=FIELD))
    a=[A_('C',806,y),G_('R',762,y+48,fm='Z'),G_('R',762,y-48,fm='X'),G_('R',806,y+56,fm='Q',col=PLUS),O_(868,y,['u','d']),A_('H',900,y)]
    s.append(POP(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(4,5,1,'l')],'CXZQOH',S=S,name='g ol'),806,y,1.3))
    ion('g MgBr+','MgBr',1)
    rxn(['g RMgBr','g ket'],['g alk','g MgBr+'],'S30 1')
    return svg('0 40 930 170',930,'그리냐르 시약의 부분 음전하를 띤 탄소가 카보닐 탄소에 첨가되어 알코올산 마그네슘이 되고 산 수용액으로 처리하면 알코올이 된다',s)
FIG['GRIG']=grig()
def exg():
    s=[]; R=26; y=70
    s.append(ring(46,y,R,subs={0:[sub('Br')]},name='eg a',want='C6H5Br',S=19)); s.append(lab(46,y+56,'브로모벤젠',19,INK))
    s.append(harrow(86,166,y)); s.append(lab(126,y-14,'Mg',19,FIELD)); s.append(lab(126,y+28,'에테르',19,FIELD))
    g=ring(214,y,R,subs={0:[sub('MgBr',al='first')]},name='eg b',want='C6H5MgBr',S=19)+lab(214,y+56,'브로민화 페닐마그네슘',19,INK)
    s.append(step(g,'eg1'))
    s.append(harrow(292,408,y)); s.append(lab(350,y-14,'1. $\\ce{CH3COCH3}$',19,FIELD)); s.append(lab(350,y+28,'2. $\\ce{H3O+}$',19,FIELD))
    g=ring(470,y,R,subs={0:[sub('C(CH3)2OH',al='first')]},name='eg c',want='C9H12O',S=19)+lab(470,y+56,'2-페닐-2-프로판올 (3차)',19,FIELD,weight=700)
    s.append(step(g,'eg2'))
    return svg('0 0 590 150',580,'브로모벤젠으로 그리냐르 시약을 만들어 아세톤에 첨가한 뒤 산으로 처리하면 2-페닐-2-프로판올이 된다',s)
FIG['EXG']=exg()

# ═══ S33 이민: pH와 빠르기(정성 개념도)
def phfig():
    W,H_=460,300; s=[]; x0,y0=56,250
    s.append(A(x0,y0,W-14,y0,'muted',2)+A(x0,y0,x0,30,'muted',2))
    s.append(T(x0+8,40,mix='이민 생성 빠르기(상대)',size=19,anchor='start',fill=MUTED)); s.append(T(W-16,y0+30,tex='\\text{pH}',size=20,anchor='end',fill=MUTED))
    def X(p): return x0+p/10*(W-120)
    pts=[]
    for i in range(0,101):
        p=i/10; v=math.exp(-((p-4.5)/1.6)**2); pts.append((X(p),y0-12-v*170))
    d='M'+' L'.join(f'{f(a)} {f(b)}' for a,b in pts)
    s.append(DRAW(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3"/>',.2,'1.2'))
    for p in (0,2,4,6,8,10): s.append(L(X(p),y0,X(p),y0+7,MUTED,2)+T(X(p),y0+28,tex=str(p),size=19,fill=MUTED))
    s.append(L(X(4.5),y0,X(4.5),y0-182,EQUI,2,dash='5 5')); s.append(lab(X(4.5)+12,y0-172,'가장 빠름 (pH 4~5)',19,EQUI,weight=700,anchor='start'))
    s.append(lab(X(1.2),y0-130,'아민이 $\\ce{RNH3+}$로',19,PLUS)); s.append(lab(X(1.2),y0-106,'친핵성 잃음',19,PLUS))
    s.append(lab(X(8.4),y0-130,'OH가 물로',19,MINUS)); s.append(lab(X(8.4),y0-106,'잘 떨어지지 않음',19,MINUS))
    return svg(f'0 0 {W} {H_+10}',W,'이민 생성 빠르기와 pH의 관계를 나타낸 정성적 개념도: pH 4~5에서 가장 빠르다',s)
FIG['PH']=phfig()

# ═══ S34 친핵성 아실 치환
def acyl():
    S=22; s=[]; y=110
    s.append(cond(40,y-50,'Nu-',22,fill=MINUS))
    a=[A_('C',160,y),G_('R',114,y+46,fm='Q'),G_('Y',214,y+46,fm='Z'),O_(160,y-62,['l','r'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,2,'l')],'CQZO',S=S,name='ac rcoy'))
    s.append(DRAW(curved(58,y-48,146,y-10,bend=-30),.3)); s.append(DRAW(curved(172,y-26,188,y-58,bend=-14),.6))
    s.append(lab(164,y+90,'카복실산 유도체',19,INK))
    s.append(harrow(250,300,y)); s.append(lab(275,y-16,'첨가',19,FIELD,weight=700))
    a=[A_('C',410,y),G_('R',364,y+46,fm='Q'),G_('Y',464,y+46,fm='Z'),G_('Nu',410,y+64,fm='E'),O_(410,y-62,['l','r','u'],fc=-1,fcp='ur')]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l')],'CQZEO',S=S,name='ac tet'))
    s.append(DRAW(curved(398,y-82,404,y-30,bend=-26),1.0)); s.append(DRAW(curved(430,y+16,464,y+24,bend=-10),1.2))
    s.append(lab(410,y+102,'사면체 중간체',19,EQUI,weight=700))
    s.append(harrow(510,560,y)); s.append(lab(535,y-16,'제거',19,BF,weight=700))
    a=[A_('C',650,y),G_('R',604,y+46,fm='Q'),G_('Nu',704,y+46,fm='E'),O_(650,y-62,['l','r'])]
    s.append(POP(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,2,'l')],'CQEO',S=S,name='ac prod'),650,y,1.5))
    s.append(cond(760,y+8,'+ Y-',22,fill=MINUS))
    SPEC['ac Nu-']=(formula('E'),-1); ion('ac Y-','Z',-1)
    rxn(['ac Nu-','ac rcoy'],['ac tet'],'S34 1'); rxn(['ac tet'],['ac prod','ac Y-'],'S34 2')
    return svg('0 10 800 210',800,'친핵체가 카보닐 탄소에 첨가되어 사면체 중간체가 생기고, 산소의 전자쌍이 C=O를 다시 만들며 이탈기 Y가 떨어져 나가는 첨가-제거 메커니즘',s)
FIG['ACYL']=acyl()

# ═══ S35 에놀레이트 공명 + 알돌
def enol():
    S=22; s=[]; y=90
    a=[A_('C',60,y),A_('H',60,y-50),A_('H',14,y+20),A_('H',60,y+52),A_('C',130,y),A_('H',130,y+52),O_(196,y-34,['l','r'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(4,5,1,'l'),(4,6,2,'l')],'C2H4O',S=S,name='en ald'))
    s.append(lab(94,y-26,'α',22,PLUS,weight=700))
    s.append(lab(100,y+100,'아세트알데하이드',19,INK))
    s.append(T(0,y-60,tex='\\ce{OH-}',size=20,fill=MINUS,anchor='start')); s.append(DRAW(curved(26,y-74,48,y-62,bend=-14),.3))
    s.append(harrow(220,270,y)); s.append(lab(245,y-16,'$\\ce{-H2O}$',19,INK))
    a=[A_('C',320,y,lp=['l'],fc=-1,fcp='ul'),A_('H',320,y-50),A_('H',320,y+52),A_('C',390,y),A_('H',390,y+52),O_(456,y-34,['l','r'])]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(3,4,1,'l'),(3,5,2,'l')],'C2H3O',S=S,name='en1'))
    sx,sy=lpxy(320,y,'l','C',S); s.append(DRAW(curved(sx-2,sy+6,352,y+8,bend=26),.9)); s.append(DRAW(curved(418,y-24,448,y-54,bend=-16),1.1))
    s.append(lrarr(476,526,y))
    a=[A_('C',570,y),A_('H',570,y-50),A_('H',570,y+52),A_('C',640,y),A_('H',640,y+52),O_(706,y-34,['l','r','u'],fc=-1,fcp='r')]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,2,'l'),(3,4,1,'l'),(3,5,1,'l')],'C2H3O',S=S,name='en2'))
    s.append(lab(510,y+100,'에놀레이트 이온: 음전하가 α 탄소와 산소에 퍼짐',19,EQUI,weight=700))
    same(['en1','en2'],'에놀레이트'); ion('en OH-','HO',-1); ion('en H2O','H2O',0); rxn(['en ald','en OH-'],['en1','en H2O'],'S35 1')
    return svg('-6 -10 766 220',740,'수산화 이온이 아세트알데하이드의 α 수소를 떼어 내어 음전하가 α 탄소와 산소에 퍼진 에놀레이트 이온이 생긴다',s)
FIG['ENOL']=enol()

# ═══ S37 합성 경로
def syn():
    s=[]; R=24; y=70; S=18
    def r_(x,sb,n,w): return ring(x,y,R,subs=sb,name=n,want=w,S=S)
    s.append(r_(36,{3:[sub('CH3')]},'sy0','C7H8')); s.append(lab(36,y+88,'톨루엔',19,INK))
    steps_=[('①','$\\ce{HNO3}$','$\\ce{H2SO4}$',{0:[sub('NO2')],3:[sub('CH3')]},'sy1','C7H7NO2','파라 분리'),
            ('②','$\\ce{H2}$, Pd','',{0:[sub('NH2')],3:[sub('CH3')]},'sy2','C7H9N','파라-톨루이딘'),
            ('③','$\\ce{2Br2}$','',{0:[sub('NH2')],1:[sub('Br',hl=True)],5:[sub('Br',hl=True)],3:[sub('CH3')]},'sy3','C7H7Br2N','$\\ce{NH2}$의 오쏘'),
            ('④','$\\ce{NaNO2}$','$\\ce{HCl}$',{0:[sub('N#N',fm='N2',fc=1,tex='\\mathrm{N_2}',al='mid')],1:[sub('Br')],5:[sub('Br')],3:[sub('CH3')]},'sy4','C7H5Br2N2','다이아조화'),
            ('⑤','$\\ce{H3PO2}$','',{1:[sub('Br')],5:[sub('Br')],3:[sub('CH3')]},'sy5','C7H6Br2','3,5-다이브로모톨루엔')]
    x=36
    for i,(no,r1,r2,sb,n,w,nm_) in enumerate(steps_):
        s.append(harrow(x+62,x+136,y)); s.append(lab(x+99,y-46,no+' '+r1,19,FIELD))
        if r2: s.append(lab(x+99,y+28,r2,19,FIELD))
        x+=190
        g=r_(x,sb,n,w)+lab(x,y+88,nm_,19,FIELD if i==4 else INK,weight=700 if i==4 else None)
        s.append(step(g,f'sy{i}'))
    return svg('0 -24 1100 206',1100,'톨루엔을 나이트로화, 환원, 브로민화, 다이아조화, 하이포아인산 처리하여 3,5-다이브로모톨루엔을 만드는 경로',s)
FIG['SYN']=syn()
def syn0():
    s=[]; R=24; y=60
    s.append(ring(40,y,R,subs={3:[sub('CH3')]},name='sz0',want='C7H8',S=18))
    s.append(harrow(84,170,y)); s.append(lab(127,y-12,'$\\ce{2Br2}$, $\\ce{FeBr3}$',19,FIELD))
    s.append(ring(220,y,R,subs={3:[sub('CH3')],2:[sub('Br')],0:[sub('Br')]},name='sz1',want='C7H6Br2',S=18)); s.append(lab(220,y+86,'2,4-다이브로모톨루엔',19,INK))
    return svg('0 -16 340 186',320,'톨루엔을 직접 브로민화하면 2,4-다이브로모톨루엔이 생긴다',s)
FIG['SYN0']=syn0()

# ═══ S38 도전 문제
def chal():
    s=[]; R=26; y=70; S=19
    s.append(ring(80,y,R,subs={0:[sub('NHCOCH3',al='first')]},name='ch0',want='C8H9NO',S=S)); s.append(lab(80,y+56,'아세트아닐라이드',19,INK))
    s.append(harrow(124,254,y)); s.append(lab(189,y-12,'1) $\\ce{HNO3}$, $\\ce{H2SO4}$',19,FIELD)); s.append(lab(189,y+28,'2) $\\ce{H3O+}$, 가열',19,FIELD))
    s.append(T(276,y+9,tex='\\mathbf{A}',size=26))
    s.append(harrow(298,396,y)); s.append(lab(347,y-12,'$\\ce{NaNO2}$, $\\ce{HCl}$',19,FIELD))
    s.append(harrow(414,566,y)); s.append(lab(490,y-12,'살리실산, $\\ce{NaOH}$',19,FIELD))
    s.append(T(590,y+9,tex='\\mathbf{B}',size=26))
    return svg('0 0 620 140',600,'아세트아닐라이드에서 A를 거쳐 B를 만드는 반응 도식',s)
FIG['CHAL']=chal()
def chalA():
    s=[]; R=26; y=72
    s.append(ring(60,y,R,subs={0:[sub('NH2')],3:[sub('NO2')]},name='chA',want='C6H6N2O2',S=19))
    s.append(lab(150,y+8,'A: 파라-나이트로아닐린',19,FIELD,weight=700,anchor='start') if False else '')
    return svg('0 0 120 150',120,'A: 파라-나이트로아닐린',s)
FIG['CHA']=chalA()
def chalB():
    s=[]; R=26; y=70
    s.append(ring(96,y,R,rot=0,subs={3:[sub('O2N',fm='NO2')],0:[sub('',fm='')]},name='chB1'))
    xa,ya=vx_('chB1',0,0); n1=(xa+30,ya+26); n2=(xa+66,ya)
    s.append(L(xa,ya,n1[0]-8,n1[1]-7,INK,2.4)); s.append(T(n1[0],n1[1]+8,tex='\\mathrm{N}',size=20))
    s.append(L(n1[0]+8,n1[1]-8,n2[0]-9,n2[1]+6,INK,2.4)+L(n1[0]+4,n1[1]-13,n2[0]-12,n2[1]+1,INK,2.4)); s.append(T(n2[0]+2,n2[1]+2,tex='\\mathrm{N}',size=20))
    rbx=n2[0]+40
    s.append(ring(rbx+R,ya+26,R,rot=0,subs={0:[sub('OH')],5:[sub('COOH',al='first')],3:[sub('',fm='')]},name='chB2'))
    xb,yb=vx_('chB2',3,0); s.append(L(n2[0]+10,n2[1]+6,xb,yb,INK,2.4))
    combo(['chB1','chB2'],'N2','C13H9N3O5','도전 B')
    return svg('0 10 440 130',420,'B: 2-하이드록시-5-[(4-나이트로페닐)아조]벤조산',s)
FIG['CHB']=chalB()

# ═════ 조립 ═════
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
def rep(m):
    k=m.group(1)
    if k not in FIG: sys.exit('no fig '+k)
    return FIG[k]
out=re.sub(r'\{\{(\w+)\}\}',rep,tpl)
unused=[k for k in FIG if '{{'+k+'}}' not in tpl]
assert OUT.endswith('1-4-S2_심화_방향족_치환과_카보닐_화합물의_반응/slides.html') and '1-4-S1' not in OUT
open(OUT,'w',encoding='utf-8').write(out)
print('ok',len(out),'anim',out.count('data-anim='),'slides',out.count('<section'),'unused',unused,'eq',len(EQLOG),'rxn',len(RXN))
# 검산 표(plan.md 3절용) — 덱 폴더가 아닌 작업 폴더에 쓴다
with open(os.path.join(HERE,'eq_table.md'),'w',encoding='utf-8') as fo:
    for i,(tg,eq,c,q) in enumerate(EQLOG,1):
        at=', '.join(f'{k} {v}' for k,v in sorted(c.items()))
        fo.write(f'| {i} | {tg} | $\\ce{{{eq}}}$ | {at} (양쪽 같음) | {q:+d} = {q:+d} | 일치 |\n')
    fo.write('\n메커니즘 단계·공명 검산(rxn·same·combo): '+', '.join(RXN)+'\n')
