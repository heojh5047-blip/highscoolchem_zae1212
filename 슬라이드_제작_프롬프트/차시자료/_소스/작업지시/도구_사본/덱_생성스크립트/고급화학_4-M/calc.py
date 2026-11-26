import math
R=8.3145
# 1
x=-92220/R*(1/298-1/400); print('1 lnK2/K1',x,'K2',6.8e5*math.exp(x), 'R=8.314',6.8e5*math.exp(-92220/8.314*(1/298-1/400)))
# 2
s=(1.4e-7/4)**(1/3); print('2 s',s)
# 5
Ka=1.3e-5; xx=math.sqrt(Ka*0.1); print('5 0mL',xx,-math.log10(xx),'exact', (-Ka+math.sqrt(Ka*Ka+4*Ka*0.1))/2, -math.log10((-Ka+math.sqrt(Ka*Ka+4*Ka*0.1))/2))
print(' 10mL',-math.log10(Ka*4),' 20mL',-math.log10(Ka*1.5),' 25',-math.log10(Ka))
Kb=1e-14/Ka; c=0.005/0.1; oh=math.sqrt(Kb*c); print(' eq 50mL',14+math.log10(oh))
# 6
k=math.log(2)/1200; print('6 k',k, math.log(100/12.5)/k)
# 7
print('7 k',1/(100*0.01))
# vitC redox
n=0.00500*12.50e-3; m=n*176.12; print('vitC I2 mol',n,'mg',m*1000,'per100',m*1000*4)
# neutral
n2=0.100*7.10e-3; print('NaOH mol',n2,'mg/25',n2*176.12*1000,'tablet',n2*176.12*4*1000)
A=n2/(0.025+0.0071); Kb2=1e-14/10**-4.10; oh=math.sqrt(Kb2*A); print('eqpH',14+math.log10(oh),A)
# vitC 0.5 M pH from pKa1
Ka1=10**-4.10; h=(-Ka1+math.sqrt(Ka1**2+4*Ka1*0.5))/2; print('0.5M pH',-math.log10(h))
# collision NO+O3
d=0.36e-9; sig=math.pi*d*d; mu=30*48/78/1000; v=math.sqrt(8*R*300/(math.pi*mu)); NA=6.022e23
Ath=sig*v*NA*1000; print('sig nm2',sig*1e18,'v',v,'Ath L/mol s',Ath)
Aexp=3.0e-12*NA/1000; Ea=1500*R; print('Aexp',Aexp,'Ea',Ea,'p',Aexp/Ath)
f=math.exp(-Ea/(R*300)); print('f300',f,'k300',Aexp*f)
nB=101325/(1.380649e-23*300); print('nB',nB,'z',sig*v*nB)
f298=math.exp(-Ea/(R*298)); print('k298',Aexp*f298)
# NH2OH
print('NH2OH k298', 1.6e8*math.exp(-65600/(R*298)))
# O3+O f
print('f O3+O 19kJ', math.exp(-19000/(R*298)))
# temp ratio f 300->310 for Ea 12.5 and 65.6
for E in (12470,65600): print(E, math.exp(-E/R*(1/310-1/300)))
print('Z ratio sqrt', math.sqrt(310/300))
