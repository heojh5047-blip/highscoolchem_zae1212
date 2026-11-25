# -*- coding: utf-8 -*-
"""고급화학 4-2-3 검산·물성 — 모든 pH는 전하 균형을 이분법으로 정확히 푼다(근사 없이).
   python3 -I calc.py  → 검산표 출력"""
from math import log10, sqrt
KW=1.0e-14; KA=1.8e-5          # 아세트산 (교과서)
KB_NH3=1.8e-5                  # 암모니아 (4-2-1과 같은 값)
def bis(f,lo=-15.5,hi=1.5):
    """f(h)가 h에 대해 증가하는 함수 → f(h)=0의 pH"""
    for _ in range(200):
        m=(lo+hi)/2; h=10**m
        if f(h)>0: hi=m
        else: lo=m
    return -(lo+hi)/2
def ph_mix(na=0.0,ct=0.0,ka=KA,cl=0.0,vol=1.0):
    """부피 vol(L) 속: Na+ na mol, 약산 전체(HA+A-) ct mol(Ka ka), Cl- cl mol → pH
       전하 균형 [H+] + [Na+] = [OH-] + [Cl-] + [A-]"""
    Na,Ct,Cl=na/vol,ct/vol,cl/vol
    return bis(lambda h: h+Na-KW/h-Cl-Ct*ka/(ka+h))
def titr_strong(V,Ca=0.100,Va=50.0,Cb=0.100):
    return ph_mix(na=Cb*V/1000,cl=Ca*Va/1000,vol=(Va+V)/1000)
def titr_weak(V,Ca=0.100,Va=50.0,Cb=0.100,ka=KA):
    return ph_mix(na=Cb*V/1000,ct=Ca*Va/1000,ka=ka,vol=(Va+V)/1000)
def buffer_add(nHA,nA,add,V0=0.100,Cadd=1.0,ka=KA):
    """nHA, nA (mol) 완충 용액 V0 L에 강산(add<0, mol) 또는 강염기(add>0) — Cadd M 용액으로 넣음"""
    vol=V0+abs(add)/Cadd
    na=nA+(add if add>0 else 0); cl=(-add if add<0 else 0)
    return ph_mix(na=na,ct=nHA+nA,ka=ka,cl=cl,vol=vol)
def capacity(nHA,nA,V0=0.050,Cadd=1.0,dpH=1.0,ka=KA):
    """처음 pH에서 ±dpH가 될 때까지 넣을 수 있는 강산·강염기 mol (이분법)"""
    p0=buffer_add(nHA,nA,0,V0,Cadd,ka)
    def find(sign):
        lo,hi=0.0,0.5
        for _ in range(100):
            m=(lo+hi)/2; p=buffer_add(nHA,nA,sign*m,V0,Cadd,ka)
            if abs(p-p0)<dpH: lo=m
            else: hi=m
        return lo
    return p0,find(-1),find(1)
def weak_ph(C,ka):
    x=(-ka+sqrt(ka*ka+4*ka*C))/2; return -log10(x),x
def pct(a,b): return 100*a/b

if __name__=='__main__':
    P=print
    P('── 그림 Ⅳ-20 강산–강염기 (0.100 M HCl 50.0 mL + 0.100 M NaOH)')
    for V in (0,10,25,40,45,49,49.9,50,50.1,51,60,80): P(f'  {V:5} mL  pH {titr_strong(V):.3f}')
    P('── 그림 Ⅳ-21 약산–강염기 (0.100 M CH3COOH 50.0 mL)')
    for V in (0,5,10,25,40,45,49,49.9,50,50.1,51,60,80): P(f'  {V:5} mL  pH {titr_weak(V):.3f}')
    p,x=weak_ph(0.100,KA); P(f'  처음 정확 {p:.3f} (x {x:.4e}), 근사 {-log10(sqrt(KA*0.1)):.3f}; 교과서 2.89')
    P(f'  45 mL 교과서식: [H+]=Ka*0.0053/0.0474={KA*0.0053/0.0474:.3e} pH {-log10(KA*0.0053/0.0474):.3f}; 정확 몰비 0.50/4.50 → {-log10(KA*0.5/4.5):.3f}')
    kb=KW/KA; xo=sqrt(kb*0.0500); P(f'  당량점 Kb {kb:.3e}, [OH-] {xo:.3e}, pOH {-log10(xo):.3f}, pH {14+log10(xo):.3f} (교과서 Kb 5.6e-10 → {14+log10(sqrt(5.6e-10*0.05)):.3f})')
    P(f'  반당량점 25 mL 정확 {titr_weak(25):.3f}, pKa {-log10(KA):.3f}')
    P(f'  급변 폭 49→51 mL: 강산 {titr_strong(51)-titr_strong(49):.2f}, 약산 {titr_weak(51)-titr_weak(49):.2f}')
    P('── 실험실 시료 25.0 mL (0.100 M NaOH)')
    for nm,f in (('HCl 0.100',lambda V:titr_strong(V,0.100,25.0)),('AcOH 0.100',lambda V:titr_weak(V,0.100,25.0)),('식초 0.0820',lambda V:titr_weak(V,0.0820,25.0))):
        P('  '+nm+' '+' '.join(f'{V}:{f(V):.2f}' for V in (0,5,10,10.25,12.5,15,20,20.5,21,24,25,26,30,40)))
    Ve=0.0820*25/0.100; P(f'  식초: Ve {Ve:.2f} mL, 원액 {0.0820*10:.3f} M, {0.820*60.05:.1f} g/L → 약 {0.820*60.05/1000*100:.2f} % (밀도 1.00 가정)')
    P('── 표 Ⅳ-8 공통 이온 효과 (0.10 M CH3COOH + CH3COO-)')
    for b in (0,0.050,0.10,0.15):
        p=ph_mix(na=b,ct=0.10+b,vol=1.0); h=10**-p
        # 해리된 HA = [A-] - b
        A=(0.10+b)*KA/(KA+h); P(f'  {b:5}: 해리 {pct(A-b,0.10):.4f} %, pH {p:.3f}')
    P('── 예제 Ⅳ-3: 0.15 M Ca(CH3COO)2')
    kb=KW/KA; x=sqrt(0.30*5.5e-10); P(f'  Kb {kb:.3e}; 교과서 5.5e-10: x {x:.3e} pOH {-log10(x):.3f} pH {14+log10(x):.3f}; 정확 {ph_mix(na=0.30,ct=0.30):.3f}; x/0.30 {x/0.30*100:.4f} %')
    P('── 확인 문제 02: 0.10 M NH4Cl')
    ka=KW/KB_NH3; x=sqrt(ka*0.10); P(f'  Ka {ka:.3e}, [H3O+] {x:.3e}, pH {-log10(x):.3f}')
    P('── 표 Ⅳ-7 예: NH4CN, NH4CH3COO, 산성염 음이온')
    P(f'  NH4+ Ka {KW/KB_NH3:.2e}; CN- Kb {KW/6.2e-10:.2e} (HCN Ka 6.2e-10) → 염기성')
    P(f'  HSO3- Ka2 6.4e-8 vs Kb {KW/1.4e-2:.1e}; HCO3- Ka2 4.7e-11 vs Kb {KW/4.5e-7:.1e}; H2PO4- Ka2 6.2e-8 vs Kb {KW/7.5e-3:.1e}')
    P('── 그림 Ⅳ-22 (100 mL, 1 M 1 mL = 1.0 mmol)')
    P(f'  비완충 pH 5.00 물(HCl 1e-5 M): +HCl {ph_mix(cl=1e-6+1e-3,vol=0.101):.2f}  +NaOH {ph_mix(na=1e-3,cl=1e-6,vol=0.101):.2f}')
    nHA,nA=0.0330,0.0596
    P(f'  완충 0.330 M HA + 0.596 M A- : {buffer_add(nHA,nA,0,0.100):.3f} → +HCl {buffer_add(nHA,nA,-1e-3,0.100):.3f}, +NaOH {buffer_add(nHA,nA,1e-3,0.100):.3f}')
    P('── 완충 용량 (50.0 mL, 1.0 M HCl/NaOH, pH ±1)')
    for c in (0.010,0.020,0.050,0.10,0.20):
        p0,a,b=capacity(c*0.05,c*0.05); P(f'  1:1 각 {c} M: pH0 {p0:.2f}, 산 {a*1000:.2f} mmol, 염기 {b*1000:.2f} mmol')
    for ha,a_ in ((0.10,0.02),(0.02,0.10),(0.18,0.02),(0.05,0.05)):
        p0,a,b=capacity(ha*0.05,a_*0.05); P(f'  HA {ha} A- {a_}: pH0 {p0:.2f}, 산 {a*1000:.2f}, 염기 {b*1000:.2f} mmol')
    P(f'  물 50 mL(pH 7): 산 {1e3*capacity(0,0,0.05)[1]:.5f} mmol')
    P('── 연습 문제')
    h=10**-3.5; c0=h/0.008; P(f'  1) [H+] {h:.4e}, [HA]0 {c0:.4e}, [HA] {c0-h:.4e}, Ka {h*h/(c0-h):.3e}')
    P(f'  2) [CH3COOH]평형 {(3e-3)**2/KA:.3f} M, 처음 {(3e-3)**2/KA+3e-3:.4f} M')
    kb=10**-4.75; x=kb*0.5/0.25; P(f'  3) Kb {kb:.3e}, [OH-] {x:.3e}, pOH {-log10(x):.3f}, pH {14+log10(x):.3f}; 정확 {14-(-log10(x)):.3f}')
    V=0.10*40/0.02; c=4.0e-3/0.240; x=sqrt(KW/KA*c); P(f'  4) V {V:.0f} mL, [A-] {c:.4e}, [OH-] {x:.3e}, pH {14+log10(x):.3f}; 1.7e-2로 {14+log10(sqrt(KW/KA*1.7e-2)):.3f}; 정확 {titr_weak(200,0.10,40,0.02):.3f}')
    P('── 확인 문제 04 (지도서 형성평가 11)')
    c=0.100*20.0/25.0; ka=10**-4.20; A=2.00/45.0; x=sqrt(KW/ka*A)
    P(f'  c {c:.4f} M, Ka {ka:.2e}, Kb {KW/ka:.2e}, [A-] {A:.4f}, [OH-] {x:.2e}, pH {14+log10(x):.3f}')
    P('── 혈액: pKa 6.1 → [HCO3-]/[H2CO3] at 7.40', f'{10**(7.40-6.1):.1f}', '7.35', f'{10**(7.35-6.1):.1f}', '7.45', f'{10**(7.45-6.1):.1f}')
    P('── 확인 문제 03: 0.050 M H2SO4 20.0 mL vs 0.10 M NaOH', 2*0.050*20.0/(1*0.10), 'mL')
