import math
Kw=1e-14
def hyd(C,K): x=math.sqrt(C*K); return x
for n,C,K,base in [('CH3COONa',0.1,Kw/1.8e-5,1),('NH4Cl.01',0.01,Kw/1.8e-5,0),('NH4NO3',0.2,Kw/1.8e-5,0),('NH4Cl.1',0.1,Kw/1.8e-5,0),('HCOONa',0.1,Kw/1.8e-4,1),('NaClO',0.1,Kw/4e-8,1),('eq',0.05,Kw/1.8e-5,1),('NaA',0.1,1e-8,1),
 ('CH3COONa.01',0.01,Kw/1.8e-5,1),('HCOONa.01',0.01,Kw/1.8e-4,1),('NaClO.01',0.01,Kw/4e-8,1)]:
  x=hyd(C,K); p=-math.log10(x); xw=math.sqrt(C*K+Kw); pw=-math.log10(xw)
  print(n,'K=%.3g x=%.3g'%(K,x),'pH=%.2f'%((14-p) if base else p),'withKw=%.2f'%((14-pw) if base else pw))
