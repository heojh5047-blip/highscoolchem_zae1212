# -*- coding: utf-8 -*-
"""고급화학 2-3-1 검산: 입자 수·배위수·점유 비율(3D 좌표로), 예제·연습 문제 계산"""
import math, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from cells import *
NA=6.022e23
print('== 단위세포 속 입자 수 · 배위수 · 점유 비율 (cells.py 3D 좌표)')
for k in ('sc','bcc','fcc','hcp','nacl','cscl','zns','tio2'):
    c=count(k); bp=by_place(k)
    line=' + '.join(f'{t}:{pl} {n}×{w}' for (t,pl),(n,w) in sorted(bp.items()))
    s=f'{k:5s} 수 {dict((t,str(v)) for t,v in c.items())}  [{line}]'
    if k in CENTER:
        d,nb=neighbors(k,*CENTER[k]); s+=f'  배위수 {len(nb)} (거리 {d:.4f} a)'
    if k in ('sc','bcc','fcc','hcp'):
        pf,r=packing(k); s+=f'  r={r:.4f}a  점유 비율 {pf*100:.2f} %'
    print(s)
print('a–r: 단순 a=2r, 체심 a=4r/√3=%.4f r, 면심 a=2√2 r=%.4f r'%(4/math.sqrt(3),2*math.sqrt(2)))
print('표 Ⅱ-2 체심 부피 64/(3√3) r³=%.3f r³, 면심 16√2 r³=%.3f r³'%(64/(3*math.sqrt(3)),16*math.sqrt(2)))
print('== 반지름 비 (교과서 102쪽)')
for c,a in (('Zn','S'),('Na','Cl'),('Cs','Cl')): print(c,a,'%.3f'%(ION_R[c]/ION_R[a]))
print('임계 반지름 비: 사면체 √(3/2)−1=%.3f, 팔면체 √2−1=%.3f, 입방체 √3−1=%.3f'%(math.sqrt(1.5)-1,math.sqrt(2)-1,math.sqrt(3)-1))
print('== 예제 Ⅱ-4')
l=(4.32e-23)**(1/3); r=math.sqrt(3)*l/4
print('l=%.4e cm, r=%.4e cm = %.1f pm'%(l,r,r*1e10))
print('== 연습 문제 1 (브래그) d=λ/(2 sinθ)=%.1f pm'%(154/(2*math.sin(math.radians(28.3)))))
print('== 연습 문제 3 (Pt)')
a=2*math.sqrt(2)*139; V=(a*1e-10)**3; m=4*195.08/NA
print('a=%.1f pm, V=%.4e cm³, m1=%.4e g, 질량 %.4e g, 밀도 %.2f g/cm³ (반올림 경로: 3.93→V=%.3e → %.2f)'%(a,V,195.08/NA,m,m/V,(3.93e-8)**3,m/((3.93e-8)**3)))
print('== 연습 문제 4 (면심 입방 틈새): 사면체 자리 = 작은 정육면체 8개의 중심 → 8; 팔면체 = 모서리 12×1/4 + 체심 1 = 4')
import itertools
tet=[(x,y,z) for x,y,z in itertools.product((.25,.75),repeat=3)]
fs=[p for p,t in cubic_sites('fcc')]
ok=all(sorted(round(math.dist(q,p),4) for p in fs)[:4]==[round(math.sqrt(3)/4,4)]*4 for q in tet)
octs=[(.5,.5,.5)]+[p for p in itertools.product((0,.5,1),repeat=3) if sum(1 for c in p if c==.5)==1]
ok2=all(sorted(round(math.dist(q,p),4) for p in fs)[:6]==[.5]*6 for q in octs)
print('사면체 자리 8개 각각 이웃 4 =',ok,'; 팔면체 후보(모서리 중점 12 + 체심) 각각 이웃 6 =',ok2,'; 몫 12×1/4+1 =',12/4+1)
print('== 연습 문제 5 (TiO2)', {t:str(v) for t,v in count('tio2').items()})
print('== 밀도 (지도서 예시) Cu 면심 a=361.5 pm: %.2f, Na 체심 a=429 pm: %.3f g/cm³'%(4*63.55/NA/(361.5e-10)**3,2*22.99/NA/(429e-10)**3))
print('== 이온 결정 깨짐 모형: 두 층 사이 쿨롱 합 E(s) ∝ Σ q_i q_j / r (층 간격 = 이온 간격 1)')
def E(s,N=40):
    tot=0
    for i in range(-N,N+1):
        qi=(-1)**i
        for j in range(-N,N+1):
            qj=-((-1)**j)   # 아래층은 위층과 엇갈림(바로 아래가 반대 전하)
            tot+=qi*qj/math.hypot(j+s-i,1)
    return tot/(2*N+1)
for s in (0,.25,.5,.75,1): print('  s=%.2f  E=%.3f'%(s,E(s)))
