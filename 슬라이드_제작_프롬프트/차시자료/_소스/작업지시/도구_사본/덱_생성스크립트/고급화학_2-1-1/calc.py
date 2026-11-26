import math
R=8.314; Ra=0.08206
def vs(T,M): M/=1000; return math.sqrt(2*R*T/M), math.sqrt(8*R*T/(math.pi*M)), math.sqrt(3*R*T/M)
print('ex1 N2 293', vs(293,28.02))
for g,M in [('He',4.00),('N2',28.02),('O2',32.00),('CO2',44.01),('H2',2.016)]:
  for T in (100,200,273,298,300,500,600):
    vp,va,vr=vs(T,M); print(g,T,round(vp),round(va),round(vr), 'fmax',round(0.8302/vp,5))
# Q1
v2=3*R*298/4e-3; print('Q1',v2, math.sqrt(v2))
# Q3
n=8000/28.02; print('Q3 n',n, n*Ra*573/100, n*Ra*573/(100-n*0.04)-1.40*(n/100)**2)
n=286; print('Q3 n286', n*Ra*573/100, n*Ra*573/(100-n*0.04)-1.40*(n/100)**2)
# Q4
nHe=24.2/4.00; nO=4.32/32.00; Pt=(nHe+nO)*Ra*298/12.5; print('Q4',nHe,nO,nHe/(nHe+nO),nO/(nHe+nO),Pt,nHe/(nHe+nO)*Pt,nO/(nHe+nO)*Pt)
# Q5
P=(760-23.78)/760; n=P*1/(Ra*298); print('Q5',P,n,n*32)
# ex2
print('ex2',1.5*0.08314*273/(5-1.5*0.084)-16.4*(1.5/5)**2)
# KE
print('Ek 298', 1.5*R*298)
# KClO3 lab example
m=1.00; nO2=m/122.55*1.5; mO2=nO2*32.00; print('KClO3',nO2,mO2)
P=(760-23.8)/760; V=nO2*Ra*298/P; print('V L',V)
# Dumas IPA
V=0.256;T=372;P=1.0; n=P*V/(Ra*T); print('IPA n',n,n*60.10)
# Boyle temp vdW = a/(Rb)
for g,a,b in [('H2',0.2452,0.0265),('He',0.0346,0.0238),('CH4',2.303,0.0431),('O2',1.382,0.0319),('N2',1.370,0.0387),('CO2',3.658,0.0429)]:
  print(g,'TB',a/(0.08314*b),'Tc',8*a/(27*0.08314*b))
# fraction above 1000 m/s N2 300K
def frac(vc,T,M):
  M/=1000; a=math.sqrt(2*R*T/M); x=vc/a
  return 1-math.erf(x)+2*x/math.sqrt(math.pi)*math.exp(-x*x)
print('frac N2 300 >1000',frac(1000,300,28.02),'600',frac(1000,600,28.02),'He300',frac(1000,300,4.0))
