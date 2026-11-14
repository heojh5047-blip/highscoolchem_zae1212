import math
h=6.626e-34;c=3.00e8;R=3.29e15;E0=2.178e-18;me=9.11e-31;e=1.602e-19;eps=8.854e-12;NA=6.02e23
print('R from E0/h',E0/h)
for n1 in (1,2,3):
  for n2 in range(n1+1,n1+6):
    dE=E0*(1/n1**2-1/n2**2); lam=h*c/dE*1e9; nu=R*(1/n1**2-1/n2**2); print(n1,n2,'dE %.4g'%dE,'lam_E %.1f'%lam,'nu %.4g'%nu,'lam_R %.1f'%(c/nu*1e9))
for n in range(1,7): print('E',n,'%.4g'%(-E0/n**2))
a0=eps*h**2/(math.pi*me*e**2); print('a0',a0)
me2=9.109e-31
print('a0 9.109',eps*h**2/(math.pi*me2*e**2))
En=me2*e**4/(8*eps**2*h**2); print('E1',En, me*e**4/(8*eps**2*h**2))
v=h/(2*math.pi*me*5.29e-11); print('v',v,'lam',h/(me*v), 2*math.pi*5.29e-11)
v=h/(2*math.pi*me*5.3e-11); print('v5.3',v,'lam',h/(me*v))
print('IE kJ/mol',E0*NA/1000)
print('baseball',h/(0.145*40))
print('dust dv',h/(4*math.pi*1.0e-9*1.0e-6))
print('electron 0.1nm',h/(4*math.pi*me*1e-10))
print('ex4 check',6.626e-34/(4*3.14*9.11e-31*2.00e-10))
# radial
import numpy as np
r=np.linspace(0,60,600001);dr=r[1]-r[0]
R1=2*np.exp(-r);R2=(1/(2*math.sqrt(2)))*(2-r)*np.exp(-r/2);R3=2*(1/3)**1.5*(1-2*r/3+2*r**2/27)*np.exp(-r/3)
for nm,RR in (('1s',R1),('2s',R2),('3s',R3)):
  P=r**2*RR**2; print(nm,'norm',P.sum()*dr,'max at',r[P.argmax()],'Pmax',P.max(),'mean',(r*P).sum()*dr)
  cum=np.cumsum(P)*dr; print(' 90%',r[np.searchsorted(cum,0.9)], ' to15', cum[np.searchsorted(r,15)], 'to20',cum[np.searchsorted(r,20)])
  # local maxima
  idx=[i for i in range(1,len(P)-1) if P[i]>P[i-1] and P[i]>=P[i+1]]; print(' peaks',[(round(r[i],3),round(P[i],4)) for i in idx[:4]])
print('3s nodes',(18-math.sqrt(108))/4,(18+math.sqrt(108))/4,'2s inner',3-math.sqrt(5),3+math.sqrt(5))
# grid sum like spreadsheet 0.1 step to 15
rr=np.arange(0,15.0001,0.1)
print('sheet sums', (rr**2*(2*np.exp(-rr))**2).sum()*0.1, (rr**2*((1/(2*math.sqrt(2)))*(2-rr)*np.exp(-rr/2))**2).sum()*0.1)
