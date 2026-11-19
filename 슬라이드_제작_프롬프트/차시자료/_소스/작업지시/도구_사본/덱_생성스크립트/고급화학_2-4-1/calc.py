# 고급화학 2-4-1 검산 (python3 -I calc.py)
import math
print('== a ==')
# 진한 염산
m=1000*1.18*0.37; print('HCl g',m, 'mol',m/36.46, 'M formula',10*1.18*37/36.46)
print('HCl molality 37%', 1000*37/(36.46*63))
# 예제 II-5
n=6.56/180.16; V=100/1.03; print('ex II-5 mol',n,'L',V/1000,'M',n/(V/1000),'formula',10*1.03*6.56/180.16)
print('ex II-5 molality', 1000*6.56/(180.16*(100-6.56)))
# 희석
print('dilution V1 mL', 0.015*1000/5.0)
# 생리 식염수 0.9 % (w/v 근사: 밀도 1.005)
print('saline M', 10*1.005*0.9/58.44)
# CuSO4·5H2O 0.500 M 100 mL
Mh=63.55+32.07+4*16.00+5*18.02; print('CuSO4.5H2O',Mh, 'g',0.5*0.1*Mh)
for c in (0.1,0.2,0.3,0.4): print('V1 for 50 mL',c, c*50/0.5)
# ppb 예
print('ppb', 0.010e-3/1000*1e9)
# 흡광도 모형
def eps(l): return 12.0*math.exp(-((1e7/l-12500)**2)/(2*2400**2))
def obs(A,s=0.002): return -math.log10(10**(-A)+s)
for l in (450,500,550,600,650,700,750,800,850,900):
    print(l, round(eps(l),2), 'A0.5', round(0.5*eps(l),2), 'obs', round(obs(0.5*eps(l)),3))
for l in (600,800):
    print('lam',l,[round(obs(c*eps(l)),3) for c in (0.1,0.2,0.3,0.4,0.5)], 'unk0.26',round(obs(0.26*eps(l)),3))
print('== b ==')
# 연습 문제
w=78.5/0.105; print('Q1 g',w,'mL',w/1.04)
n=15.0/62.07; print('Q2 mol',n,'M',n/0.512,'(0.242)',0.242/0.512,'m',n/0.5,'%',15/515*100,'X',n/(n+500/18.02),'(0.242,27.7)',0.242/(0.242+27.7))
print('Q3 g',0.040*0.250*159.6)
print('Q4',786-783)
print('Q5',0.6*515,0.4*332,0.6*515+0.4*332,(0.6*515+0.4*332)/760)
# 라울 확인 문제: 물 90.0 g + 포도당 18.0 g
nw=90.0/18.02; ng=18.0/180.16; X=nw/(nw+ng); print('raoult X',X,'P',X*23.8,'dP',23.8-X*23.8)
# 앙투안(물) kPa
def pw(t): return 10**(8.07131-1730.63/(233.426+t))*0.133322
Kb=0.512; Kf=1.86
for name,i in (('sugar',1),('NaCl',2)):
    m=0.15; xs=i*m/(i*m+1000/18.015)
    print(name,'X_solute',xs,'dTb',Kb*i*m,'dTf',Kf*i*m)
    for t in (20,30,40,50,60,70,80): print('  ',t,round(pw(t),3),round(pw(t)*(1-xs),3),'dP',round(pw(t)*xs,4))
print('pw100',pw(100))
# 끓는점: P_sol(T)=101.325 → 풀기
def bp(xs):
    lo,hi=99,101
    for _ in range(60):
        mid=(lo+hi)/2
        if pw(mid)*(1-xs)<101.325: lo=mid
        else: hi=mid
    return lo
b0=bp(0); print('bp water',b0)
for name,i in (('sugar',1),('NaCl',2)):
    xs=i*0.15/(i*0.15+1000/18.015); print(name,'bp',bp(xs),'dTb raoult',bp(xs)-b0)
# 0.1 m NaCl vs 포도당
print('dTf 0.1 m NaCl',1.86*0.2,'glucose',1.86*0.1)
