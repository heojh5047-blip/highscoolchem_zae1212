# 고급화학 3-4-1 검산: 반응식 원자 수·전하, 전지 전위·ΔG°·K·네른스트
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
('a S8 볼타 산화','Zn -> Zn^2+ + 2e-'),('a S8 볼타 환원','2H+ + 2e- -> H2'),
('a S9 다니엘 환원','Cu^2+ + 2e- -> Cu'),('a S9 다니엘 전체','Zn + Cu^2+ -> Zn^2+ + Cu'),
('a S16 비활성 산화','2I- -> I2 + 2e-'),('a S16 비활성 환원','MnO4- + 8H+ + 5e- -> Mn^2+ + 4H2O'),
('a S16 비활성 전체','2MnO4- + 16H+ + 10I- -> 2Mn^2+ + 5I2 + 8H2O'),
('a S17 예제10-1 환원','Co^3+ + e- -> Co^2+'),('a S17 예제10-1 전체(덱)','Zn + 2Co^3+ -> Zn^2+ + 2Co^2+'),
('a S17 예제10-1 교과서 풀이','3Zn + 2Co^3+ -> 3Zn^2+ + 2Co'),
('a S18 예제10-2 산화','Ni -> Ni^2+ + 2e-'),('a S18 예제10-2 환원','Ag+ + e- -> Ag'),('a S18 예제10-2 전체','Ni + 2Ag+ -> Ni^2+ + 2Ag'),
('a S19 확인02','Mg + 2H+ -> Mg^2+ + H2'),
('a S24 알칼리 전지','Zn + 2MnO2 + H2O -> Zn(OH)2 + Mn2O3'),
('b 표Ⅲ-10 F2','F2 + 2e- -> 2F-'),('b 표 O2산성','O2 + 4H+ + 4e- -> 2H2O'),('b 표 Hg2+','2Hg^2+ + 2e- -> Hg2^2+'),
('b 표 Hg2^2+','Hg2^2+ + 2e- -> 2Hg'),('b 표 O2염기','O2 + 2H2O + 4e- -> 4OH-'),('b 표 H+','2H+ + 2e- -> H2'),
('b 표 Co','Co^2+ + 2e- -> Co'),('b 표 Cd','Cd^2+ + 2e- -> Cd'),('b 표 Zn','Zn^2+ + 2e- -> Zn'),('b 표 Mg','Mg^2+ + 2e- -> Mg'),('b 표 Na','Na+ + e- -> Na'),
('b S9 표준 수소 전극(H3O+)','2H3O+ + 2e- -> H2 + 2H2O'),
('b 확인01 Mg-Co','Mg + Co^2+ -> Mg^2+ + Co'),('b S13 Co-Cd','Co + Cd^2+ -> Co^2+ + Cd'),
('b 예제11 Fe','Fe^3+ + e- -> Fe^2+'),('b 예제11 I3','I3- + 2e- -> 3I-'),('b 예제11 전체','2Fe^3+ + 3I- -> 2Fe^2+ + I3-'),
('b 예제12 Cr','Cr2O7^2- + 14H+ + 6e- -> 2Cr^3+ + 7H2O'),
]
ok=0
for name,e in EQ:
    l,r=e.split(' -> '); a,qa=side(l); b,qb=side(r)
    good=(a==b and qa==qb); ok+=good
    print(('OK ' if good else 'XX ')+name+' | '+e+' | '+' '.join(f'{k}{a[k]}' for k in sorted(a))+f' | {qa:+d}={qb:+d}')
print(f'{ok}/{len(EQ)} 일치')
F=96485; R=8.314; T=298.15
k=R*T/F*math.log(10); print('RT ln10/F =',round(k,5))
E=0.34-(-0.76); print('다니엘 E° =',round(E,2))
print('다니엘 ΔG° =',round(-2*F*E/1000,1),'kJ; log K(0.0592) =',round(2*E/0.0592,2),' K =',f'{10**(2*E/0.0592):.2e}', ' (0.05916:',f'{10**(2*E/0.05916):.2e})')
print('Mg-Co E° =',round(-0.28-(-2.37),2),' Co-Cd E° =',round(-0.40-(-0.28),2))
print('예제11 E° =',round(0.771-0.536,3),' ΔG°=',round(-2*F*0.235/1000,1),'kJ  K=',f'{math.exp(2*F*0.235/(R*T)):.2e}')
lq=math.log10((1e-2)**2/((1e-3)*(1e-3)**14)); print('예제12 log Q =',lq,' E =',round(1.33-0.0592/6*lq,4))
print('확인04 Zn(0.10)|Cu(1e-3): E =',round(1.10-0.0592/2*math.log10(0.10/1e-3),4))
print('농도차 전지 Cu 0.010 | 1.0: E =',round(0-0.0592/2*math.log10(0.010/1.0),4))
for c in (1.0,0.10,0.010,0.0010): print(' [Cu2+]',c,'[Zn2+]=1.0  E =',round(1.10-0.0296*math.log10(1.0/c),3))
print('1.5 V × 1 C =',1.5,'J;  납축전지 6×2.1 =',6*2.1,'V;  뱀장어 5000×0.15 =',5000*0.15,'V')
print('1 mol 전자 × 1.10 V =',round(F*1.10/1000,1),'kJ')
print('Zn-Co E° =',round(-0.28-(-0.76),2),';  ΔG° ×2 =',round(-4*F*1.10/1000,1),'kJ;  1.5 V × 2.0 C =',1.5*2.0,'J')
