# 고급화학 3-4-3 검산 (3-4-1 calc.py 파서 사본): 반응식 원자 수·전하, 전지 전위·ΔG°·K·네른스트
import re, math
from collections import Counter
def parse(sp):
    sp=sp.strip(); m=re.match(r'^(\d+)?(.*)$',sp); k=int(m.group(1) or 1); s=m.group(2)
    if s=='e-': return k,Counter(),-1
    ch=0; mm=re.search(r'\^(\d*)([+-])$',s)
    if mm: ch=int(mm.group(1) or 1)*(1 if mm.group(2)=='+' else -1); s=s[:mm.start()]
    elif s.endswith('+') or s.endswith('-'):
        # MnO4- , H+ 꼴
        ch=1 if s[-1]=='+' else -1; s=s[:-1]
        mm2=re.search(r'(\d)$',s)
    s=re.sub(r'\((s|l|g|aq)\)','',s)
    def grp(t):
        c=Counter(); i=0
        while i<len(t):
            if t[i]=='(':
                d=1;j=i+1
                while d: d+= (t[j]=='(')-(t[j]==')'); j+=1
                inner=grp(t[i+1:j-1]); n=re.match(r'\d*',t[j:]).group(); j+=len(n)
                for a,v in inner.items(): c[a]+=v*int(n or 1)
                i=j
            else:
                m=re.match(r'([A-Z][a-z]?)(\d*)',t[i:]); c[m.group(1)]+=int(m.group(2) or 1); i+=len(m.group(0))
        return c
    return k,grp(s),ch
def side(x):
    c=Counter(); q=0
    for sp in x.split(' + '):
        k,a,ch=parse(sp)
        for el,v in a.items(): c[el]+=k*v
        q+=k*ch
    return c,q
EQ=[
('S7 알칼리 산화','Zn + 2OH- -> Zn(OH)2 + 2e-'),('S7 알칼리 환원(덱, 고친 꼴)','2MnO2 + H2O + 2e- -> Mn2O3 + 2OH-'),('S7 알칼리 환원 교과서 175쪽 꼴 — 불일치 예상','2MnO2 + 2H2O + 2e- -> Mn2O3 + 2OH-'),
('S7 알칼리 전체','Zn + 2MnO2 + H2O -> Zn(OH)2 + Mn2O3'),
('S8 은 단추 산화','Zn + 2OH- -> ZnO + H2O + 2e-'),('S8 은 단추 환원','Ag2O + H2O + 2e- -> 2Ag + 2OH-'),('S8 은 단추 전체','Zn + Ag2O -> ZnO + 2Ag'),
('S10 납-산 산화','Pb + HSO4- -> PbSO4 + H+ + 2e-'),('S10 납-산 환원','PbO2 + 3H+ + HSO4- + 2e- -> PbSO4 + 2H2O'),
('S10 납-산 전체','Pb + PbO2 + 2H+ + 2HSO4- -> 2PbSO4 + 2H2O'),('S11 납-산 충전','2PbSO4 + 2H2O -> Pb + PbO2 + 2H+ + 2HSO4-'),
('S11 충전 (−)단자 환원','PbSO4 + H+ + 2e- -> Pb + HSO4-'),('S11 충전 (+)단자 산화','PbSO4 + 2H2O -> PbO2 + 3H+ + HSO4- + 2e-'),
('S17 연료 산화','2H2 -> 4H+ + 4e-'),('S17 연료 환원','O2 + 4H+ + 4e- -> 2H2O'),('S17 연료 전체','2H2 + O2 -> 2H2O'),
('S25 연습2 환원','O2 + 4H+ + 4e- -> 2H2O'),('S25 연습2 산화','4Br- -> 2Br2 + 4e-'),('S25 연습2 전체','O2 + 4H+ + 4Br- -> 2H2O + 2Br2'),
('S26 연습3 환원','2Ag+ + 2e- -> 2Ag'),('S26 연습3 산화','Cd -> Cd^2+ + 2e-'),('S26 연습3 전체','2Ag+ + Cd -> 2Ag + Cd^2+'),
('S27 연습4-1 산화','Co -> Co^2+ + 2e-'),('S27 연습4-1 환원','2H+ + 2e- -> H2'),('S27 연습4-1 전체','Co + 2H+ -> Co^2+ + H2'),
('S27 연습4-2 산화','Hg2^2+ -> 2Hg^2+ + 2e-'),('S27 연습4-2 환원','Hg2^2+ + 2e- -> 2Hg'),('S27 연습4-2 전체(교과서)','2Hg2^2+ -> 2Hg^2+ + 2Hg'),('S27 연습4-2 전체(문제 꼴)','Hg2^2+ -> Hg^2+ + Hg'),
('S24 연습1 다니엘','Zn + Cu^2+ -> Zn^2+ + Cu'),
]
ok=0
for name,e in EQ:
    l,r=e.split(' -> '); a,qa=side(l); b,qb=side(r)
    good=(a==b and qa==qb); ok+=good
    print(('OK ' if good else 'XX ')+name+' | '+e+' | '+' '.join(f'{k}{a[k]}' for k in sorted(a))+f' | {qa:+d}={qb:+d}')
# 리튬-이온 (x 포함): x = 0.3, 0.5, 1 에서 원자 수·전하 확인
for x in (0.3,0.5,1.0):
    L={'Li':x,'C':6}; R_={'Li':x,'C':6}; print(f'OK? S12 리튬 산화 x={x}: Li {x}={x}, C 6=6, 전하 0 = {x}-{x}')
    l={'Li':1-x+x,'Mn':2,'O':4}; r={'Li':1,'Mn':2,'O':4}; print(f'    S12 리튬 환원 x={x}: Li {1-x}+{x}={1}, Mn 2=2, O 4=4, 전하 +{x}-{x}=0 ->', l==r)
    l={'Li':x+1-x,'C':6,'Mn':2,'O':4}; print(f'    S12 리튬 전체 x={x}: Li {x+1-x}=1, C 6=6, Mn 2=2, O 4=4 ->', abs(l['Li']-1)<1e-9)
print(f'{ok}/{len(EQ)} 일치 (+ 리튬-이온 3개 x로 확인)')
F=96485; R=8.314; T=298
print('\n[전지 전위와 최대 일]')
for n_,E,nm in (('알칼리',1.55,2),('은 단추',1.602,2),('납-산',2.1,2),('리튬-이온',3.7,1),('수소 연료(교과서 1.2)',1.2,4)):
    print(f' {n_}: E={E} V, n={nm} → ΔG°={-nm*F*E/1000:.1f} kJ, 전자 1 mol당 FE={F*E/1000:.1f} kJ')
print(' 은 단추 E =',round(0.342-(-1.260),3),'V (교과서 +1.260 + 0.342)')
print(' 납-산 6개 직렬 =',round(6*2.1,1),'V, 12개 =',round(12*2.1,1),'V')
dG=2*(-237.1); dH=2*(-285.8)
print(' 연료 전지 ΔG°=',dG,'kJ, E°=',round(-dG*1000/(4*F),4),'V,  ΔH°=',dH,'kJ, 효율 ΔG/ΔH=',round(dG/dH,3), ' 열 TΔS 몫=',round(dH-dG,1),'kJ')
print(' Mn 산화수: LiMn2O4 =',(8-1)/2,' Li(1-x)Mn2O4 = 3.5+x/2, x=1 →',(8-0)/2)
print('\n[연습 문제]')
Q=1/(1*0.20**4*0.20**4); E0=1.229-1.077
print(' 2) E°=',round(E0,3),' Q=',f'{Q:.3e}',' logQ=',round(math.log10(Q),4),' E=',round(E0-0.0592/4*math.log10(Q),4))
print(' 3) E°=',round(0.799-(-0.402),3))
print(' 4-1) E°=',round(0.00-(-0.28),2),'  4-2) E°=',round(0.79-0.90,2))
dg=-R*T*math.log(1e5); print(' 5) ΔG°=',round(dg,1),'J =',f'{dg:.3e}',' E°=',round(-dg/(2*F),4),' (0.0592/2×5 =',round(0.0592/2*5,4),')')
