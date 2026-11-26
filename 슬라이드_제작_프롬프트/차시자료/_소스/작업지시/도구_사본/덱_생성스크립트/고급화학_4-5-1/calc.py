# 고급화학 4-5-1 검산 (python3 -I calc.py) — 반응식 원자 수·전하, 단계 합 = 전체 반응식, 계산 문항, 실험실 모형
import re
from math import *
from collections import Counter
def parse(sp):
    m=re.match(r'^(\d*)(.*)$',sp.strip()); n=int(m.group(1) or 1); s=m.group(2)
    ch=0
    mc=re.search(r'\^?(\d*)([+-])$',s)
    if mc and not re.match(r'^[A-Z][a-z]?$',s):
        ch=int(mc.group(1) or 1)*(1 if mc.group(2)=='+' else -1); s=s[:mc.start()]
    def rec(s):
        c=Counter(); i=0; st=[Counter()]
        toks=re.findall(r'[A-Z][a-z]?|\d+|\(|\)',s); k=0
        while k<len(toks):
            t=toks[k]
            if t=='(' : st.append(Counter())
            elif t==')':
                g=st.pop(); mul=1
                if k+1<len(toks) and toks[k+1].isdigit(): mul=int(toks[k+1]); k+=1
                for a,v in g.items(): st[-1][a]+=v*mul
            elif t.isdigit(): pass
            else:
                mul=1
                if k+1<len(toks) and toks[k+1].isdigit(): mul=int(toks[k+1]); k+=1
                st[-1][t]+=mul
            k+=1
        return st[0]
    c=rec(s)
    return n,c,ch,s
def side(x):
    tot=Counter(); q=0; sp=Counter()
    for t in x.split(' + '):
        n,c,ch,s=parse(t); sp[s+('%+d'%ch if ch else '')]+=n
        for a,v in c.items(): tot[a]+=v*n
        q+=ch*n
    return tot,q,sp
def chk(eq):
    l,r=eq.split(' -> '); a,qa,_=side(l); b,qb,_=side(r)
    ok=(a==b and qa==qb); print(('일치 ' if ok else '불일치 ')+eq+'   원자 '+dict(a).__repr__()+' 전하 %d/%d'%(qa,qb)); return ok
def mech(steps,overall,mult=None):
    mult=mult or [1]*len(steps); L=Counter(); Rr=Counter()
    for s,m in zip(steps,mult):
        chk(s); l,r=s.split(' -> ')
        for k,v in side(l)[2].items(): L[k]+=v*m
        for k,v in side(r)[2].items(): Rr[k]+=v*m
    net_l=L-Rr; net_r=Rr-L
    ol,orr=overall.split(' -> '); OL=side(ol)[2]; OR=side(orr)[2]
    common=set(L)&set(Rr)
    inter=[k for k in common if any(k in side(s.split(' -> ')[1])[2] for s in steps[:1]) or True]
    ok=(net_l==OL and net_r==OR)
    print('  단계 합 → 왼쪽',dict(net_l),'오른쪽',dict(net_r),'| 전체',overall,'→','일치' if ok else '불일치')
    print('  양쪽에 나타나 지워진 화학종:',sorted(common))
    chk(overall); return ok
print('== 단일 반응식 ==')
for e in ['2N2O5 -> 4NO2 + O2','N2O5 -> NO2 + NO3','NO + O3 -> NO2 + O2','C2H4 + H2 -> C2H6','2NO + 2CO -> N2 + 2CO2',
          'S + O2 -> SO2','SO3 + H2O -> H2SO4','CH3COOH + CH3OH -> CH3COOCH3 + H2O','C4H9Br -> C4H9^+ + Br-','O3 + O -> 2O2']: chk(e)
print('== 메커니즘 ==')
mech(['NO2 + NO2 -> NO3 + NO','NO3 + CO -> NO2 + CO2'],'NO2 + CO -> NO + CO2')
mech(['NO + O2 -> NO3','NO3 + NO -> 2NO2'],'2NO + O2 -> 2NO2')
mech(['2NO + H2 -> N2 + H2O2','H2O2 + H2 -> 2H2O'],'2NO + 2H2 -> N2 + 2H2O')
mech(['H2O2 + I- -> H2O + IO-','H2O2 + IO- -> H2O + O2 + I-'],'2H2O2 -> 2H2O + O2')
mech(['2NO + O2 -> 2NO2','NO2 + SO2 -> NO + SO3'],'2SO2 + O2 -> 2SO3',[1,2])
mech(['Cl2 -> 2Cl','CH4 + Cl -> CH3 + HCl','CH3 + Cl -> CH3Cl'],'CH4 + Cl2 -> CH3Cl + HCl')
mech(['H2O2 -> H2O + O','O + CF2Cl2 -> ClO + CF2Cl','ClO + O3 -> Cl + 2O2','Cl + CF2Cl -> CF2Cl2'],'H2O2 + O3 -> H2O + 2O2')
print('== 계산 ==')
R=8.314
print('예제 Ⅳ-6 k\'/k = e^(6000/(8.314*298)) =',exp(6000/(R*298)),' 지수',6000/(R*298))
print('확인 03 76→57 kJ, 25 °C:',exp(19000/(R*298.15)),' (298 K)',exp(19000/(R*298)))
print('확인 03b 같은 Ea 차 6 kJ, 37 °C:',exp(6000/(R*310)))
Hf={'NO2':33.2,'NO3':71.1,'NO':91.3,'CO':-110.5,'CO2':-393.5}
print('NO2+CO ΔH',Hf['NO']+Hf['CO2']-Hf['NO2']-Hf['CO'],' 1단계 ΔH',Hf['NO3']+Hf['NO']-2*Hf['NO2'])
print('H2O2(aq) 분해 ΔH per mol H2O2', -285.83+191.17, ' (l)', -285.83+187.8)
print('초기 속도 가상 자료 k=0.50 L/(mol s): ',[0.5*c*c for c in (0.10,0.20,0.10)])
print('연습 3 ΔG° = -101.01 kJ/mol 주어짐')
print('== 실험실 모형 ==')
EA={'없음':76,'KI':57,'MnO2':50,'카탈레이스':23}; K25={'없음':2.0e-7,'KI':0.010,'MnO2':0.025,'카탈레이스':0.050}
den=lambda t:1/(1+exp((t-45)/3))
def k(c,t):
    T=t+273.15; v=K25[c]*exp(-EA[c]*1000/R*(1/T-1/298.15))
    if c=='카탈레이스': v*=den(t)/den(25)
    return v
def Vmax(p): return p*10/34.01*0.005/2*24.5*1000
for p in (1,2,3): print(' %d %% 5 mL → O2 최대 %.1f mL'%(p,Vmax(p)))
for c in EA:
    for t in (15,25,35,45,55):
        kk=k(c,t); V=lambda s:Vmax(3)*(1-exp(-kk*s))
        print(' %s %d °C k=%.3g /s t1/2=%s V30=%.1f V180=%.1f'%(c,t,kk,('%.0f s'%(log(2)/kk)) if kk>1e-4 else '—',V(30),V(180)))
for p in (1,2,3): kk=k('KI',25); print(' KI 25 °C %d %%: V30 %.1f V180 %.1f, 처음 30 s 평균 %.2f mL/s'%(p,Vmax(p)*(1-exp(-kk*30)),Vmax(p)*(1-exp(-kk*180)),Vmax(p)*(1-exp(-kk*30))/30))
print(' KI 25→35 비',k('KI',35)/k('KI',25),' MnO2',k('MnO2',35)/k('MnO2',25),' 카탈 35/25',k('카탈레이스',35)/k('카탈레이스',25),' 45/25',k('카탈레이스',45)/k('카탈레이스',25),' 55/25',k('카탈레이스',55)/k('카탈레이스',25))
# 연속 반응 A→I→P (중간체 그림): k1=1, k2=3
k1,k2=1.0,3.0
for t in (0,0.5,1,2,4): A=exp(-k1*t); I=k1/(k2-k1)*(exp(-k1*t)-exp(-k2*t)); print(' 연속 t=%.1f A %.3f I %.3f P %.3f'%(t,A,I,1-A-I))
