# -*- coding: utf-8 -*-
"""고급화학 4-3-1 검산 — python3 -I calc.py > calc_out.txt"""
import math
from math import log, exp
ln2=log(2)
def lsq(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sxx=sum((x-mx)**2 for x in xs); sxy=sum((x-mx)*(y-my) for x,y in zip(xs,ys)); syy=sum((y-my)**2 for y in ys)
    b=sxy/sxx; a=my-b*mx; r2=sxy*sxy/(sxx*syy); return b,a,r2
# ── 그림 Ⅳ-23/24 (덱 계산 모형): [N2O5]0 = 0.160 M, k = 0.30 /min
K23=0.30; A23=0.160
N=lambda t:A23*exp(-K23*t)
print('Fig23 table t,N2O5,NO2,O2')
for t in (0,2,4,6,8,10,12): n=N(t); print(t,round(n,4),round(2*(A23-n),4),round((A23-n)/2,4))
print('avg 0-2 N2O5', (A23-N(2))/2, 'NO2',2*(A23-N(2))/2,'O2',(A23-N(2))/4,'rate',(A23-N(2))/4)
print('avg NO2 0-4',2*(A23-N(4))/4,' tangent NO2 at 4',2*K23*N(4),' initial NO2',2*K23*A23, 'initial N2O5 decomposition',K23*A23)
print('avg NO2 2-6',2*(N(2)-N(6))/4)
# 예제 Ⅳ-4
print('ex IV-4 H2O',2*0.24,'H2',2*0.24)
# 표 Ⅳ-10
k=3.20e-3/(1.10e-2*(1.30e-2)**2); print('k tab10',k, 'exp2',6.40e-3/(2.20e-2*(1.30e-2)**2),'exp3',2.56e-2/(2.20e-2*(2.60e-2)**2))
# 확인 문제 04 (a): 2NO + 2H2 -> N2 + 2H2O, v = k[NO]^2[H2], k = 1.23
kk=1.23; 
for no,h2 in ((0.10,0.10),(0.10,0.20),(0.20,0.10)): print('q04',no,h2,kk*no*no*h2)
print('q05a: [NO]x3,[O2]x1/2 ->',9*0.5)
# ── b
# 그림 Ⅳ-28: 45 C, t1/2 24 min, [N2O5]0 0.0600
k28=ln2/24; print('k28 /min',k28,'/s',k28/60)
for t in (0,24,48,72,96): print('fig28',t,0.06*exp(-k28*t))
# 확인 01(b): k=2.0e-3 /s, 0.50 M, 600 s
print('b-q01',0.50*exp(-2.0e-3*600), 'kt',2.0e-3*600)
# 확인 02(b)
ts=[0,100,200,300,400]; As=[0.100,0.0500,0.0333,0.0250,0.0200]
print('b-q02 1/A',[round(1/a,1) for a in As], lsq(ts,[1/a for a in As]), 'lnA r2',lsq(ts,[log(a) for a in As])[2],'A r2',lsq(ts,As)[2])
# 2차 반감기 연속: k=0.10, A0=0.100 -> 1/(kA0)=100 s, next 200, 400
# 0차: A0=4.0e-3, k=1.0e-5 -> t1/2=200 s, next 100, 50
print('0th t1/2',4.0e-3/(2*1.0e-5))
# ── 연습 문제
# 2
print('Ex2 k',0.5e-2/0.5,1.0e-2/1.0,1.5e-2/1.5)
# 3
k3=ln2/4.03e4; print('Ex3 k',k3,'24h frac',exp(-k3*86400),'kt',k3*86400)
# 4
k4=1.8e-5; print('Ex4 t1/2',ln2/k4,'4h',0.3*exp(-k4*14400),'90%',log(10)/k4, log(0.3/0.03)/k4, 'hours',log(10)/k4/3600)
# 5
t5=[0,50,100,150,200,300,400,500]; c5=[8.00e-3,6.58e-3,5.59e-3,4.85e-3,4.29e-3,3.48e-3,2.93e-3,2.53e-3]
b,a,r2=lsq(t5,[1/c for c in c5]); print('Ex5 1/c',[round(1/c,1) for c in c5],'slope',b,'int',a,'r2',r2)
print('Ex5 ln r2',lsq(t5,[log(c) for c in c5])[2],'c r2',lsq(t5,c5)[2])
print('Ex5 20min correct',1/(0.541*1200+1/8.00e-3),' textbook(1/0.003)',1/(0.541*1200+1/0.003))
print('Ex5 t1/2',1/(0.541*3.0e-3))
# 실험실 CV: k2 = 0.20 /M/s
for oh in (0.025,0.050,0.10): kp=0.20*oh; print('CV',oh,'k1',kp,'t1/2',ln2/kp,'stop t (A<0.02 from 0.80)',log(40)/kp)
# CV 예시 결과 (0.050 M, 0-600 s, 15 s, 측정 0.02 미만 멈춤): 잡음 없는 R2
kp=0.010; ts=[i*15 for i in range(41) if 0.80*exp(-kp*i*15)>=0.02]; As=[0.80*exp(-kp*t) for t in ts]
print('CV n',len(ts),'R2 A',lsq(ts,As)[2],'lnA',lsq(ts,[log(x) for x in As])[2],'1/A',lsq(ts,[1/x for x in As])[2])
# 방사성: Tc-99m 6.0 h 24h; C-14 25%
print('Tc 24h',0.5**4,'C14 25% ->',2*5730)
# NO2 (lab 나): k 0.541, 8.00e-3, 0-500
# NH3 (lab 다): 4.0e-3 M, k 1.0e-5 M/s
