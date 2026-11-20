# 고급화학 3-5-1 검산 (3-4-3 calc.py 파서 사본): 반응식 원자 수·전하, 전기 분해 양적 관계
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
('S6 물 환원 전극','4H2O + 4e- -> 2H2 + 4OH-'),('S6 물 산화 전극','2H2O -> O2 + 4H+ + 4e-'),('S6 물 전체','2H2O -> 2H2 + O2'),
('S8 다니엘 산화','Zn -> Zn^2+ + 2e-'),('S8 다니엘 환원','Cu^2+ + 2e- -> Cu'),('S8 다니엘 전체','Zn + Cu^2+ -> Zn^2+ + Cu'),('S8 역반응','Zn^2+ + Cu -> Zn + Cu^2+'),
('S8 역반응 환원 전극','Zn^2+ + 2e- -> Zn'),('S8 역반응 산화 전극','Cu -> Cu^2+ + 2e-'),
('S11 녹은 NaCl 환원','Na+ + e- -> Na'),('S11 녹은 NaCl 산화','2Cl- -> Cl2 + 2e-'),('S11 녹은 NaCl 전체','2NaCl -> 2Na + Cl2'),
('S12 물의 환원(1:2 꼴)','2H2O + 2e- -> H2 + 2OH-'),('S12 Cu 석출','Cu^2+ + 2e- -> Cu'),
('S13 진한 NaCl 전체','2H2O + 2Cl- -> H2 + Cl2 + 2OH-'),('S13 Na2SO4 전체','2H2O -> 2H2 + O2'),('S13 CuSO4(Pt) 전체','2Cu^2+ + 2H2O -> 2Cu + O2 + 4H+'),
('S13 CuSO4(Cu) 산화','Cu -> Cu^2+ + 2e-'),
('S14 CuCl2 전체','Cu^2+ + 2Cl- -> Cu + Cl2'),('S14 AgNO3 환원','Ag+ + e- -> Ag'),('S14 AgNO3 전체','4Ag+ + 2H2O -> 4Ag + O2 + 4H+'),
('S15 은 도금 산화','Ag -> Ag+ + e-'),('S15 정련 불순물','Zn -> Zn^2+ + 2e-'),
('S19 예제 Au','Au^3+ + 3e- -> Au'),
('S23 Al 환원','Al^3+ + 3e- -> Al'),('S23 Al 산화(탄소)','C + 2O^2- -> CO2 + 4e-'),('S23 Al 전체','2Al2O3 + 3C -> 4Al + 3CO2'),('S23 Mg 환원','Mg^2+ + 2e- -> Mg'),
('S24 연습1 볼타 산화','Sn -> Sn^2+ + 2e-'),('S24 연습1 전해 환원','Sn^2+ + 2e- -> Sn'),('S24 연습1 전해 전체','Cu + Sn^2+ -> Cu^2+ + Sn'),('S24 연습1 볼타 전체','Sn + Cu^2+ -> Sn^2+ + Cu'),
('S26 연습3 환원','4H+ + 4e- -> 2H2'),
]
ok=0
for name,e in EQ:
    l,r=e.split(' -> '); a,qa=side(l); b,qb=side(r)
    good=(a==b and qa==qb); ok+=good
    print(('OK ' if good else 'XX ')+name+' | '+e+' | '+' '.join(f'{k}{a[k]}' for k in sorted(a))+f' | {qa:+d}={qb:+d}')
print(f'{ok}/{len(EQ)} 일치')
F=96485
print('\n[자유 에너지·전위]')
print(' 다니엘 ΔG° = -2×F×1.10 =',round(-2*F*1.10/1000,1),'kJ ; E° = 0.34-(-0.76) =',round(0.34+0.76,2))
dG=2*237.1; print(' 물 분해 ΔG° = +',dG,'kJ ; E° = -ΔG/(4F) =',round(-dG*1000/(4*F),4),'V')
print(' 연습1 Cu+Sn2+ E° = -0.14-0.34 =',round(-0.14-0.34,2),'V')
print(' 진한 NaCl: 환원 경쟁 Na+ -2.70 vs H2O -0.83 ; 산화 경쟁 Cl2/Cl- 1.36 vs O2/H2O 1.23 → 최소 전압 Cl2 경로', round(1.36-(-0.83),2),'V, O2 경로',round(1.23-(-0.83),2),'V (O2 쪽은 과전압 큼)')
print(' CuSO4(Pt) 최소 전압 1.23-0.34 =',round(1.23-0.34,2))
print('\n[양적 관계]')
n=3.0/197.0; print(' 예제 Ⅲ-13: n(Au)=',round(n,5),' n(e)=',round(n*3,5),' Q=',round(n*3*F),'C')
Q=2.00*30.0*60; ne=Q/F; print(' 확인03: Q=',Q,'C ne=',round(ne,6),' Cu mol',round(ne/2,6),' g',round(ne/2*63.55,4),' O2 mol',round(ne/4,7),' L(24.5)',round(ne/4*24.5,4),' H+ mol',round(ne,4))
nAg=1.08/107.9; Qa=nAg*F; print(' 확인04: n(Ag)=',round(nAg,6),' Q=',round(Qa,1),'C t(0.500 A)=',round(Qa/0.5,1),'s =',round(Qa/0.5/60,2),'min')
print(' 1 t당 전하량 (1.000e6 g):')
for nm,z,M in (('Al',3,26.98),('Mg',2,24.31),('Na',1,22.99),('Cu',2,63.55),('Cl2',2,70.90),('H2',2,2.016)):
    mol=1e6/M; q=z*mol*F; print(f'   {nm}: mol={mol:.4g} e mol={z*mol:.4g} Q={q:.3e} C  (Q/1e9={q/1e9:.2f})')
