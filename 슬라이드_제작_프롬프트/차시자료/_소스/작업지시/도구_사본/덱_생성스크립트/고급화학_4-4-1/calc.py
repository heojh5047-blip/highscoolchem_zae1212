# 고급화학 4-4-1 검산 (python3 -I calc.py)
from math import *
R=8.314
def Ea2(k1,k2,T1,T2): return R*log(k2/k1)/(1/T1-1/T2)
def frac(Ea,T):  # 맥스웰–볼츠만 에너지 분포(3차원)에서 E>=Ea 분율, Ea J/mol
    x=Ea/(R*T); return erfc(sqrt(x))+2*sqrt(x/pi)*exp(-x)
print('예제1 Ea', Ea2(1,4,273,293)/1000)
print('예제2 2배', Ea2(1,2,293,303)/1000, '3배', Ea2(1,3,293,303)/1000)
print('예제3 ln', log(3.5e-3/2.7e-4), '1/T차', 1/600-1/650, 'Ea', Ea2(2.7e-4,3.5e-3,600,650)/1000)
print('  교과서 반올림식 2.56*8.314/1.28e-4 =', 2.56*8.314/1.28e-4)
Ea=Ea2(4.7e-5,5.3e-4,273,298); print('연습1 Ea',Ea/1000,'ln비',log(5.3e-4/4.7e-5),'1/T차',1/273-1/298)
A2=5.3e-4*exp(Ea/(R*298)); A1=4.7e-5*exp(Ea/(R*273)); print('  A (T2)',A2,'A (T1)',A1)
A65=5.3e-4*exp(65600/(R*298)); print('  A with Ea 65.6 kJ', A65, ' with 65.55',5.3e-4*exp(65550/(R*298)))
print('  textbook A 1.95e8 → Ea that gives it:', R*298*log(1.95e8/5.3e-4)/1000)
print('연습2 Ea,r', 19-(-392))
print('NO2+CO Ea,r', 132-(-226))
print('Z 비 sqrt(308/298)', sqrt(308/298))
for E in (10e3,50e3,60e3,80e3):
    print('Ea',E/1000,'e^-Ea/RT 비 298→308', exp(E/R*(1/298-1/308)), '분율비', frac(E,308)/frac(E,298))
print('지도서13 300→310 2배 Ea', Ea2(1,2,300,310)/1000)
print('그림32 모형 Ea10 300/600 분율', frac(10e3,300), frac(10e3,600), frac(10e3,600)/frac(10e3,300))
# N2O5 Arrhenius 모형: Ea 103 kJ, k(318.15)=ln2/(24*60)
k45=log(2)/(24*60); EaN=103e3; AN=k45*exp(EaN/(R*318.15)); print('N2O5 A',AN,'lnA',log(AN))
for t in (25,35,45,55,65):
    T=t+273.15; k=AN*exp(-EaN/(R*T)); print('  ',t,'1/T',1/T,'k',k,'ln k',log(k))
xs=[1/(t+273.15) for t in (25,35,45,55,65)]; ys=[log(AN)-EaN/(R*x**-1) for x in xs]
b=(ys[-1]-ys[0])/(xs[-1]-xs[0]); print('  기울기',b,'Ea',-b*R/1000)
# 확인 03
print('확인03 Ea,f 180 Ea,r 100 → ΔH', 180-100)
# 10 °C 비 for Ea 10, 60
for E in (10e3,60e3): print('Ea',E/1000,'k 비 298→308',exp(E/R*(1/298-1/308)))
# 활성화 에너지 80 kJ: 298 K e^-x
for E in (40e3,80e3,132e3,300e3): print('Ea',E/1000,'e^-Ea/RT at 298',exp(-E/(R*298)))
