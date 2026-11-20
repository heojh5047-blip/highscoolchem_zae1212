# 고급화학 3-2-1 엔트로피 — 계산·반응식 검산
import math, re
from fractions import Fraction as F
def parse(side):
    tot={}
    for term in side.split(' + '):
        term=term.strip(); m=re.match(r'^(\d+/\d+|\d+)?\s*(.*)$',term); c=F(m.group(1)) if m.group(1) else F(1)
        f=re.sub(r'\((s|l|g|aq|흑연|다이아몬드)\)','',m.group(2))
        def cnt(s,mult):
            i=0; out={}
            while i<len(s):
                if s[i]=='(':
                    d=1;j=i+1
                    while d: d+= (s[j]=='(')-(s[j]==')'); j+=1
                    inner=s[i+1:j-1]; k=re.match(r'\d*',s[j:]).group(); n=int(k) if k else 1
                    for a,b in cnt(inner,1).items(): out[a]=out.get(a,0)+b*n
                    i=j+len(k)
                else:
                    m2=re.match(r'([A-Z][a-z]?)(\d*)',s[i:]); a=m2.group(1); n=int(m2.group(2) or 1)
                    out[a]=out.get(a,0)+n; i+=len(m2.group(0))
            return {a:b*mult for a,b in out.items()}
        for a,b in cnt(f,1).items(): tot[a]=tot.get(a,0)+b*c
    return tot
EQ=[('S4 생각 열기','4Fe(s) + 3O2(g) -> 2Fe2O3(s)'),('S4','H2O(s) -> H2O(l)'),('S2 중단원','CO2(s) -> CO2(g)'),
('S5','C(다이아몬드) -> C(흑연)'),('S29 예제III-7·S37','N2(g) + 3H2(g) -> 2NH3(g)'),('S31 확인04','CaCO3(s) -> CaO(s) + CO2(g)'),
('S30 확인03-1','2SO2(g) + O2(g) -> 2SO3(g)'),('S30 확인03-2','NH4NO3(s) -> N2O(g) + 2H2O(g)'),('S30 확인03-3','Ag+(aq) + Cl-(aq) -> AgCl(s)'),
('S30 확인03-4','H2O(l) -> H2O(g)'),('S33·S35','H2O(l) -> H2O(s)'),('S38 탐구','C6H12O6(s) + 6O2(g) -> 6CO2(g) + 6H2O(l)'),
('S38 탐구','6CO2(g) + 6H2O(l) -> C6H12O6(s) + 6O2(g)'),('S4 냉찜질','NH4NO3(s) -> NH4+(aq) + NO3-(aq)')]
def charge(side):
    c=0
    for t in side.split(' + '):
        m=re.match(r'^(\d+)?',t.strip()); k=int(m.group(1)) if m.group(1) else 1
        if '+(' in t: c+=k
        if '-(' in t: c-=k
    return c
for s,e in EQ:
    l,r=e.split(' -> '); L=parse(l.replace('+(','(').replace('-(','(')); R=parse(r.replace('+(','(').replace('-(','('))
    ok=L==R and charge(l)==charge(r)
    print(('일치' if ok else '불일치!!'),s,e,{k:str(v) for k,v in L.items()},'전하',charge(l),charge(r))
import math
k=1.381e-23; R=8.314; NA=6.022e23
print('--- 계산')
print('S10 1000J/300K',1000/300,'600K',1000/600)
print('S11 물 75.3 ln(348/298)',75.3*math.log(348/298))
print('S13 예제III-5',1.00*8.314*math.log(44.0/22.0))
print('S14 확인01-1',2.00*8.314*math.log(10.0/30.0),'01-2',6010/273.15)
print('S18 동전20 W',2**20,'S',k*math.log(2**20),'R ln2',R*math.log(2),'k NA',k*NA)
print('S19 예제III-6',k*math.log(1),k*math.log(16))
print('S25 확인02 벤젠',30800/(80.1+273.15),'T',80.1+273.15)
print('S29 예제III-7',2*192.4-(191.6+3*130.7))
print('S31 확인04',39.8+213.7-92.9)
for T in (263.15,273.15,283.15): print('S35 어는 과정 T',T,'S주위',6010/T,'전체',-22.0+6010/T)
print('S37 확인05 S주위',92000/298,'전체',-198.9+92000/298)
print('표지·실험실 예: N=4 a=2 b=2',2**4,4**4,(2/4)**4,4*math.log(2))
for N,a,b in ((4,2,2),(8,2,2),(4,2,4),(4,3,3),(6,3,3),(4,2,0),(8,6,6)):
    print('lab',N,a,b,'W1',a**N,'W2',(a+b)**N,'P',(a/(a+b))**N,'dS/k',N*math.log((a+b)/a),
          'dist',[round(math.comb(N,n)*a**n*b**(N-n)/(a+b)**N,4) for n in range(N+1)])
