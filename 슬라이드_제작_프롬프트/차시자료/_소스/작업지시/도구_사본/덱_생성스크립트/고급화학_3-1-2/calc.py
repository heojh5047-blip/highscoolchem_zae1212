# 고급화학 3-1-2 엔탈피 — 계산·반응식 검산
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
EQ=[('표지·S25 헤스','N2(g) + 2O2(g) -> 2NO2(g)'),('S25','N2(g) + O2(g) -> 2NO(g)'),('S25','2NO(g) + O2(g) -> 2NO2(g)'),
('S8','Zn(s) + I2(s) -> ZnI2(s)'),('S11·S12','CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)'),('S12','CH4(g) + 2O2(g) -> CO2(g) + 2H2O(g)'),
('S11','2CH4(g) + 4O2(g) -> 2CO2(g) + 4H2O(l)'),('S14','2H2(g) + O2(g) -> 2H2O(l)'),('S14','H2O(l) -> H2(g) + 1/2 O2(g)'),
('S16','C(흑연) + O2(g) -> CO2(g)'),('S16','C(다이아몬드) + O2(g) -> CO2(g)'),('S16','C(흑연) -> C(다이아몬드)'),
('S18','1/2 N2(g) + O2(g) -> NO2(g)'),('S18','C(흑연) + 2H2(g) + 1/2 O2(g) -> CH3OH(l)'),('S21','C(흑연) + 2H2(g) -> CH4(g)'),
('S21','H2(g) + 1/2 O2(g) -> H2O(l)'),('S20','1/2 N2(g) + 3/2 H2(g) -> NH3(g)'),('S20','CO(g) + 1/2 O2(g) -> CO2(g)'),
('S23','2Al(s) + Fe2O3(s) -> Al2O3(s) + 2Fe(s)'),('S24','2C(s) + 3H2(g) + 1/2 O2(g) -> C2H5OH(l)'),('S24','C2H5OH(l) + 3O2(g) -> 2CO2(g) + 3H2O(l)'),
('S27','C6H4(OH)2(aq) + H2O2(aq) -> C6H4O2(aq) + 2H2O(l)'),('S27','C6H4(OH)2(aq) -> C6H4O2(aq) + H2(g)'),('S27','H2O2(aq) -> H2(g) + O2(g)'),
('S27','2H2(g) + O2(g) -> 2H2O(g)'),('S27','2H2O(g) -> 2H2O(l)'),('S26','CH4(g) + 2O2(g) -> C(g) + 4H(g) + 4O(g)'),
('S29–33','NaOH(s) -> Na+(aq) + OH-(aq)'),('S29–33','Na+(aq) + OH-(aq) + H+(aq) + Cl-(aq) -> Na+(aq) + Cl-(aq) + H2O(l)'),
('S29–33','NaOH(s) + H+(aq) + Cl-(aq) -> Na+(aq) + Cl-(aq) + H2O(l)'),('S38','PCl3(l) + Cl2(g) -> PCl5(s)'),
('S39','2B(s) + 3H2(g) -> B2H6(g)'),('S39','2B(s) + 3/2 O2(g) -> B2O3(s)'),('S39','B2H6(g) + 3O2(g) -> B2O3(s) + 3H2O(g)'),('S39','H2O(l) -> H2O(g)'),('S40','4NH3(g) + 7O2(g) -> 4NO2(g) + 6H2O(l)'),
('S37 연습2','CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)'),('S37 연습2','2H2(g) + O2(g) -> 2H2O(l)')]
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
print('--- 계산')
print('예제III-3 dH',-50,'dU',-50+(-20))
print('확인01 dH',+30,'dU',30+5)
print('열화학 2배',2*-890,'역',+890,'차',-802-(-890),'44x2',44*2)
print('확인02',2*-286,+286,+802,+88)
print('예제III-4',-394-(-396))
print('메테인 경로',75+0-394-2*286,'일반식',(-394+2*-286)-(-75+0))
print('확인04 테르밋',(-1676+0)-(0+-826))
print('확인05 에탄올',2*-393.5+3*-285.8-(-1366.8))
print('결합 끊',4*413+2*498,'만듦',2*799+4*467,'dH',4*413+2*498-(2*799+4*467))
print('탐21',177.4+191.2-2*241.8-2*43.8)
print('헤스 N2',180-112)
print('--- 연습 문제')
print('2 CH4',11.3*10.3,11.3*10.3/1.50,'H2',11.3*14.3,11.3*14.3/1.150, 'ratio',(11.3*14.3/1.150)/(11.3*10.3/1.50))
w=-2.00*8.3145*300*math.log(0.5); print('3 w',w,'q',-w,'V처음',2*0.08206*300/2.00)
print('4 PCl5',-124+(-319.7))
print('5 B2H6',-1273-(-2035)+3*-286+3*44)
print('--- 실험실 모형 (c=4.18, 밀도 1.00)')
EX={'1 용해':(44.5,102.0),'2 중화':(55.8,100.0),'3 직접':(100.3,102.0)}
for lid,eff in (('덮음',0.98),('안 덮음',0.92)):
    hs=[]
    for k,(H,m) in EX.items():
        dT=0.0500*H*1000/(m*4.18)*eff; q=m*4.18*dT; h=-q/1000/0.0500; hs.append(h)
        print(lid,k,'dT %.2f'%dT,'q %.0f J'%q,'dH %.1f'%h)
    print(lid,'1+2 %.1f vs 3 %.1f'%(hs[0]+hs[1],hs[2]))
print('true dT',[round(0.05*H*1000/(m*4.18),3) for H,m in EX.values()])
print('S40',4*34+6*-286-4*-46)
