# -*- coding: utf-8 -*-
"""고급화학 4-2-1 검산·물성 계산 (gen.py가 import, 단독 실행하면 검산 출력)"""
from math import log10, log, sqrt, exp
KW=1.0e-14
def pH_of(h): return -log10(h)
def weak(C,K):
    """약산(약염기) 정확한 해: x^2/(C-x)=K"""
    return (-K+sqrt(K*K+4*K*C))/2
def alpha(C,K): return weak(C,K)/C
def frac_base(pH,pKa):  # [A-]/([HA]+[A-])
    return 1/(1+10**(pKa-pH))
# 표 Ⅳ-5 (교과서)
KWT=[(0,0.114),(10,0.292),(20,0.681),(25,1.01),(30,1.47),(40,2.92),(50,5.47),(60,9.61)]
def kw_fit():
    xs=[1/(t+273.15) for t,_ in KWT]; ys=[log(k*1e-14) for _,k in KWT]
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    b=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    return b, my-b*mx   # 기울기 = -dH/R
# ─── 바닷물 탄산 평형 모형 (총 알칼리도 일정, 15 °C, S=35) ───
TK=288.15; SAL=35.0; TA=2300e-6
def _consts(T=TK,S=SAL):
    lnK0=-60.2409+93.4517*(100/T)+23.3585*log(T/100)+S*(0.023517-0.023656*(T/100)+0.0047036*(T/100)**2)
    pK1=3633.86/T-61.2172+9.6777*log(T)-0.011555*S+0.0001152*S*S
    pK2=471.78/T+25.9290-3.16967*log(T)-0.01781*S+0.0001122*S*S
    lnKB=(-8966.90-2890.53*S**0.5-77.942*S+1.728*S**1.5-0.0996*S*S)/T+148.0248+137.1942*S**0.5+1.62142*S-(24.4344+25.085*S**0.5+0.2474*S)*log(T)+0.053105*S**0.5*T
    lnKw=148.9652-13847.26/T-23.6521*log(T)+(118.67/T-5.977+1.0495*log(T))*S**0.5-0.01615*S
    return exp(lnK0),10**-pK1,10**-pK2,exp(lnKB),exp(lnKw),0.0004157*S/35
def ocean(ppm):
    K0,K1,K2,KB,Kw,BT=_consts()
    co2=K0*ppm*1e-6
    lo,hi=6.0,9.5
    for _ in range(80):
        ph=(lo+hi)/2; h=10**-ph
        hco3=K1*co2/h; co3=K2*hco3/h; boh4=BT*KB/(KB+h)
        ta=hco3+2*co3+boh4+Kw/h-h
        if ta>TA: hi=ph
        else: lo=ph
    h=10**-ph; hco3=K1*co2/h; co3=K2*hco3/h
    return ph,co2,hco3,co3
if __name__=='__main__':
    print('0.010 M HCl pH',pH_of(0.010),' 0.020 M NaOH pH',14-pH_of(0.020))
    print('0.5 M HCl',pH_of(0.5),' ascorbic 10^-2.65',10**-2.65,'ratio',0.5/10**-2.65,'alpha',10**-2.65/0.5,'Ka from book',(10**-2.65)**2/(0.5-10**-2.65))
    print('real ascorbic pKa 4.10 -> pH',pH_of(weak(0.5,10**-4.10)))
    x=weak(0.10,1.8e-5); print('AcOH 0.10',x,pH_of(x),'alpha',x/0.10,'approx',sqrt(1.8e-6),pH_of(sqrt(1.8e-6)))
    for C in (1.0,0.10,0.010,0.0010,0.00010): print(' alpha',C,alpha(C,1.8e-5),pH_of(weak(C,1.8e-5)))
    y=weak(0.10,1.8e-5); print('NH3 0.10 OH',y,'pOH',pH_of(y),'pH',14-pH_of(y))
    print('NH4+ Ka',KW/1.8e-5,'pKa',-log10(KW/1.8e-5))
    print('AcO- Kb',KW/1.8e-5,'F- Kb',KW/6.8e-4)
    for t,k in KWT: print(' Kw',t,k,'pH',round(-log10(sqrt(k*1e-14)),3))
    b,a=kw_fit(); print('Kw fit slope',b,'dH kJ',-b*8.314/1000)
    print('pH drop 0.1 -> H+ x',10**0.1,' 0.3',10**0.3,' 0.4',10**0.4)
    for p in (280,300,413,560,600,800,1000,1100):
        ph,co2,hco3,co3=ocean(p); print(' ocean',p,round(ph,3),'CO3 umol',round(co3*1e6,1),'HCO3',round(hco3*1e6))
    print('H2PO4 pKa 7.21 blood 7.40 ratio',10**(7.40-7.21))
