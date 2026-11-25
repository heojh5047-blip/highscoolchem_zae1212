# 고급화학 4-1-1 화학 평형 — 계산·반응식 검산
import math, re, itertools
from math import log, exp, sqrt
def parse(side):
    tot={}; ch=0
    for term in side.split(' + '):
        term=term.strip(); m=re.match(r'^(\d+)?\s*(.*)$',term); c=int(m.group(1)) if m.group(1) else 1
        f=re.sub(r'\((s|l|g|aq)\)','',m.group(2))
        mc=re.search(r'\^(\d*)([+-])$',f)
        if mc: ch+=c*(int(mc.group(1) or 1))*(1 if mc.group(2)=='+' else -1); f=f[:mc.start()]
        for a,n in re.findall(r'([A-Z][a-z]?)(\d*)',f): tot[a]=tot.get(a,0)+c*int(n or 1)
    return tot,ch
EQ=[('S1·S7·S8 등','N2(g) + 3H2(g) <=> 2NH3(g)'),('S3 석회 동굴','CaCO3(s) + CO2(aq) + H2O(l) <=> Ca^2+(aq) + 2HCO3^-(aq)'),
('S5·확인05','2NO2(g) <=> N2O4(g)'),('S15 예제IV-1','2NO(g) + Cl2(g) <=> 2NOCl(g)'),('S19 확인03','H2(g) + I2(g) <=> 2HI(g)'),
('S13 보충','2NaHCO3(s) <=> Na2CO3(s) + H2O(g) + CO2(g)'),('S20–22 실험실','Fe^3+(aq) + SCN^-(aq) <=> FeSCN^2+(aq)'),
('S32 탐구1','CO2(g) <=> CO2(aq)'),('S32 탐구2','CO2(aq) + H2O(l) <=> H2CO3(aq)'),('S32 탐구3','H2CO3(aq) <=> H^+(aq) + HCO3^-(aq)'),
('S32 탐구4','HCO3^-(aq) <=> H^+(aq) + CO3^2-(aq)'),('S32 탐구5','Ca^2+(aq) + CO3^2-(aq) <=> CaCO3(s)'),('S7 비가역','CH4(g) + 2O2(g) <=> CO2(g) + 2H2O(l)')]
for s,e in EQ:
    l,r=e.split(' <=> '); L=parse(l); R=parse(r)
    print('일치' if L==R else '불일치!!',s,e,L)
print('=== 표 IV-1')
for n2,h2,nh3 in ((0.921,0.763,0.157),(0.399,1.197,0.203),(2.59,2.77,1.82)): print(' K',nh3**2/(n2*h2**3))
x=0.157/2; print(' 실험I ICE x',x,'N2',1-x,'H2',1-3*x)
print(' 실험II: NH3 1-0.203=',1-0.203,'/2 N2',(1-0.203)/2,'H2',3*(1-0.203)/2)
print(' 실험III: NH3 3-1.82=',3-1.82,'N2',2+(3-1.82)/2,'H2',1+3*(3-1.82)/2,' Q0',3**2/(2*1**3))
R=0.08206
print('Kp NH3 500C',6.02e-2*(R*773)**-2, 'RT',R*773)
print('=== 예제 IV-1 Kp',1.2**2/((5.0e-2)**2*0.30),'K',1.2**2/((5.0e-2)**2*0.30)*R*298,'(1.9e3)',1.9e3*R*298)
print('=== HI x',sqrt(50.5)/(2+sqrt(50.5)), ' check',(2*0.780)**2/(0.220**2))
print('=== 그림IV-2 K',1.5/0.50)
Rj=8.314
print('=== dG->K NH3 298: dG',-92+298*0.1989,'K',exp(-(-92000+298*198.9)/(Rj*298)))
print(' 5.7 kJ ->',exp(5700/(Rj*298)), ' dG for K=1e3 at 298',-Rj*298*log(1e3)/1000)
print(' ΔG°=+10 kJ 298 K',exp(-10000/(Rj*298)))
for T in (500,600,700,800): print(' thermo K',T,exp(-(-92000+T*198.9)/(Rj*T)),'lnK',(92000/(Rj*T))-198.9/Rj)
print(' slope',92000/Rj,'intercept',-198.9/Rj)
print('=== 표IV-3 van t Hoff 500/600:', -log(3/90)*Rj/(1/500-1/600) , ' 600/700',-log(0.3/3)*Rj/(1/600-1/700),' 700/800',-log(0.04/0.3)*Rj/(1/700-1/800))
pts=[(1/T*1e3,log(K)) for T,K in ((500,90),(600,3),(700,0.3),(800,0.04))]; print(' pts',pts)
n=len(pts); mx=sum(p[0] for p in pts)/n; my=sum(p[1] for p in pts)/n; b=sum((p[0]-mx)*(p[1]-my) for p in pts)/sum((p[0]-mx)**2 for p in pts); print(' fit slope(1e3 K)',b,'dH',-b*1e3*Rj/1000,'kJ int',my-b*mx)
print(' 예측 K(550 K) from 500 & dH -92:',90*exp(-92000/Rj*(1/550-1/500)))
# === 그림IV-3: 분압. 처음 평형 PN2 0.78 PH2 2.30 → Kp
PN,PH,PA=0.78,2.30,0.45; Kp=PA**2/(PN*PH**3); print('=== IV-3 Kp',Kp)
f=lambda y:(PA+2*y)**2/((PN-y)*(PH+1-3*y)**3)-Kp
lo,hi=0,0.25
for _ in range(80):
    m=(lo+hi)/2; (lo,hi)=(m,hi) if f(m)<0 else (lo,m)
y=lo; print(' y',y,'new',PN-y,PH+1-3*y,PA+2*y,' Q직후',PA**2/(PN*(PH+1)**3))
# === 그림IV-4 입자 수: N2 a, H2 b, NH3 c in V=1 ; after V=1/2 shift x
best=[]
for a in range(2,8):
  for b in range(3,13):
    for c in range(1,9):
      K1=c*c/(a*b**3)
      for xx in range(1,4):
        a2,b2,c2=a-xx,b-3*xx,c+2*xx
        if a2<1 or b2<1: continue
        K2=c2*c2*0.25/(a2*b2**3)
        err=abs(K2/K1-1)
        if a+b+c<=20 and err<0.12: best.append((err,a,b,c,xx,K1,K2))
best.sort(); print('=== IV-4 후보',best[:8])
# === 그림 IV-5 하버 수득률 (Kp atm^-2 from thermo)
def Kp_T(Tc): T=Tc+273.15; return exp(-(-92000+T*198.9)/(Rj*T))
def yld(Tc,P):
    K=Kp_T(Tc); lo,hi=0,0.9999
    for _ in range(100):
        m=(lo+hi)/2; nt=4-2*m; yA=2*m/nt; yN=(1-m)/nt; yH=3*(1-m)/nt
        Q=(yA*P)**2/((yN*P)*(yH*P)**3)
        (lo,hi)=(m,hi) if Q<K else (lo,m)
    return lo
for P in (100,200,300,400):
    print(' P',P,[round(100*yld(Tc,P),1) for Tc in (350,400,450,500,550)])
# === G 곡선 A<=>B K=3, P=2: G/RT = (1-x)(g0A+ln((1-x)P)) + x(g0B+ln(xP)), g0B-g0A=-ln3
def G(x):
    eps=1e-9; x=min(max(x,eps),1-eps); return (1-x)*(0+log((1-x)*2))+x*(-log(3)+log(x*2))
print('=== G min', min((G(i/1000),i/1000) for i in range(1,1000)),' G0',G(0),'G1',G(1))
# === 실험실 모형 (labs_src.js와 같은 식)
print('=== 실험실')
eps=4700; Rj=8.314
def Kt(t): return 200*exp(-25000/Rj*(1/298.15-1/(t+273.15)))*1 if False else 200*exp((-25000/Rj)*(1/298.15-1/(t+273.15)))
print(' K25',Kt(25),'K40',Kt(40))
def xeq(K,F,S):
    a=K; b=-(K*(F+S)+1); c=K*F*S; return (-b-sqrt(b*b-4*a*c))/(2*a)
frac=xeq(200,0.100,1e-5)/1e-5; slope=eps*frac; print(' 표준 전환율',frac,'기울기',slope)
for t in (25,40):
  ks=[];rs=[]
  for n in range(1,6):
    F=1e-3; S=2e-4*n; x=xeq(Kt(t),F,S); A=eps*x; xm=A/slope; Km=xm/((F-xm)*(S-xm)); r=xm/((F-xm)+(S-xm)); ks.append(Km); rs.append(r)
    print('  ',t,n,'A %.3f xm %.3e K %.1f ratio %.4f'%(A,xm,Km,r))
  m=sum(ks)/5; print('  mean K',m)
