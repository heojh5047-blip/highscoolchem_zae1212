import math
R=8.314; Ra=0.08206; LA=101.325
print('ExIII-1 w L.atm',-1.20*0.500,'J',-1.20*0.500*LA)
wA=-1.00*8.3145*292*math.log(20/8); print('ExIII-2 A w',wA,'q',-wA)
print('P1',Ra*292/8.00,'P2',Ra*292/20.00)
wB=-1.20*(20.00-8.00)*LA; print('ExIII-2 B w',wB, -14.4*LA)
print('check01 q cal',10.0*2.50)
print('deep Q 2x 300K', -1.00*R*300*math.log(2))
for P,V2,q in [(1.20,8.50,0),(2.00,6.00,0),(1.00,10.00,500),(0,16.00,0)]:
    w=-P*(V2-8.00)*LA; print('lab',P,V2,q,'w',round(w,1),'dU',round(q+w,1))
w=-1*R*292*math.log(20/8); P2=Ra*292/20; wi=-P2*12*LA; print('lab rev',w,P2,wi)
w=-1*R*292*math.log(4/8); P2=Ra*292/4; wi=-P2*(4-8)*LA; print('lab rev comp',w,P2,wi)
