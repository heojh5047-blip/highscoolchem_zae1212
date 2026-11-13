import math
Kw=1e-14
def ph(Ca,Va,Vb,Cb=0.1,Ka=None):
    Vt=(Va+Vb)/1000; na=Ca*Va/1000; nb=Cb*Vb/1000
    if Ka is None:
        d=(na-nb)/Vt; H=(d+math.sqrt(d*d+4*Kw))/2; return -math.log10(H)
    Ct=na/Vt; Na=nb/Vt
    lo,hi=-14.5,0.5
    for _ in range(100):
        m=(lo+hi)/2; H=10**m
        f=H+Na-Ct*Ka/(Ka+H)-Kw/H
        if f>0: hi=m
        else: lo=m
    return -m
for V in [0,2,4,5,6,8,10,12,14,15,16,17,18,19,19.5,19.9,19.95,20,20.05,20.1,20.5,21,22,23,25,30]:
    print(V, round(ph(0.1,20,V),2), round(ph(0.1,20,V,Ka=1.8e-5),2))
print('100mL',[ (V,round(ph(0.1,100,V),2)) for V in [0,50,90,99,99.9,100,100.1,101,110,120]])
