import math
R=8.314
# 예제 II-3
T1,T2=57.8+273.15,25.0+273.15
x=-33050/R*(1/T2-1/T1); print('ex3 T',round(T1,1),round(T2,1),'ln',round(x,4),'P2',405*math.exp(x))
# 연습 2
T=[200,220,240,260,280,300];P=[0.80,4.50,21.0,71.0,197,391]
X=[1/t for t in T];Y=[math.log(p) for p in P];n=len(X)
mx=sum(X)/n;my=sum(Y)/n;b=sum((a-mx)*(c-my) for a,c in zip(X,Y))/sum((a-mx)**2 for a in X);a0=my-b*mx
r2=1-sum((c-(a0+b*a))**2 for a,c in zip(X,Y))/sum((c-my)**2 for c in Y)
print('prob2 slope',b,'int',a0,'dH',-b*R,'r2',r2)
for t,p in zip(T,P): print(' ',t,round(1/t*1000,3),round(math.log(p),3))
# 연습 3
T1=34.9+273.15;P1=13.3e3;P2=1.013e5;dH=4.35e4
inv=1/T1-R/dH*math.log(P2/P1); print('prob3 1/T2',inv,'T2',1/inv, 1/inv-273.15)
# Antoine (mmHg, C)
ANT={'water':(8.07131,1730.63,233.426),'ethanol':(8.20417,1642.89,230.300),'ether':(6.92032,1064.07,228.80)}
def pv(l,t): A,B,C=ANT[l]; return 10**(A-B/(C+t))
for l in ANT:
  # bp
  lo,hi=0,150
  for _ in range(60):
    m=(lo+hi)/2
    if pv(l,m)<760: lo=m
    else: hi=m
  print(l,'bp',round(lo,2),[round(pv(l,t),1) for t in (0,20,25,30,40,50,60,70,80,90,100)])
for t in (20,30,40,50,60,70,80): print('water kPa',t,round(pv('water',t)*0.133322,2))
for l in ANT:
  ts=[20,30,40,50,60,70,80] if l!='ether' else [0,5,10,15,20,25,30]
  X=[1/(t+273.15) for t in ts];Y=[math.log(pv(l,t)*0.133322) for t in ts];n=len(X)
  mx=sum(X)/n;my=sum(Y)/n;b=sum((a-mx)*(c-my) for a,c in zip(X,Y))/sum((a-mx)**2 for a in X)
  print(l,'cc dH',round(-b*R/1000,2))
# water kPa near 100 for fig II-11
for t in (80,90,100,110,120): print('w',t,round(pv('water',t)*0.133322,1))
# boiling at 70 kPa and 200 kPa
for Pk in (70,101.325,200):
  lo,hi=50,150
  for _ in range(60):
    m=(lo+hi)/2
    if pv('water',m)*0.133322<Pk: lo=m
    else: hi=m
  print('bp at',Pk,round(lo,1))
# surface tension apparatus
for name,g in (('water',0.0728),('ethanol',0.0223),('acetone',0.0237),('glycerol',0.0634),('hexane',0.0184)):
  d=0.066; l=math.pi*d; F=2*l*g; print(name,'l',round(l,4),'F',round(F,4),'g-reading',round(F/9.80*1000,3))
for r in (0.25,0.5,1.0):
  print('cap water r mm',r,round(2*0.0728/(998*9.8*r/1000)*1000,1))
print('Hg r0.5',2*0.485*math.cos(math.radians(140))/(13534*9.8*0.0005)*1000)
