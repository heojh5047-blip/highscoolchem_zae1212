import math
Ka=1.8e-5; Kw=1e-14
# sol: (CT acetate total mmol, Na from salt mmol) in 50 mL
S={'water':(0,0),'HAc':(10,0),'NaAc':(10,10),'buf':(10*0.5+10*0.5*0,0)}
S={'water':(0,0),'HAc':(10,0),'NaAc':(10,10),'buf':(10,5)}  # buffer 50 mL of 0.1/0.1 -> 5 HA + 5 A- = CT 10? no
S['buf']=(10,5)  # 50 mL of mixed: HA 0.1 M*50=5, A- 5 -> CT=10 mmol? 0.1*50=5 each -> CT=10
def pH(CT,Na,vb,va,V0=50,C=0.2):
    V=V0+vb+va; Ct=CT/V; Nat=(Na+C*vb)/V; Cl=C*va/V
    lo,hi=-15,1
    for _ in range(100):
        m=(lo+hi)/2; H=10**m
        f=H+Nat-Cl-Kw/H-Ct*Ka/(Ka+H)
        if f>0: hi=m
        else: lo=m
    return -m
for k,(ct,na) in S.items():
    print(k, *['%.2f'%pH(ct,na,vb,va) for vb,va in [(0,0),(5,0),(0,5),(1,0),(0,1),(10,0),(0,10)]])
print('09: HAc 0.1', -math.log10(math.sqrt(0.1*Ka)), 'NaAc 0.1', 14+math.log10(math.sqrt(0.1*Kw/Ka)))
print('blood ratio HCO3/H2CO3 at 7.4 with Ka1 4.5e-7:', 10**(-7.4)/4.5e-7)
