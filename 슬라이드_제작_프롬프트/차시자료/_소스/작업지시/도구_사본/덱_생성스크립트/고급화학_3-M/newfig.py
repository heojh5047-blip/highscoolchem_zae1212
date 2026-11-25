def pump():
    s=[]; x0,x1,y0,y1=60,370,60,140
    s.append(R(x0,y0,x1-x0,y1-y0,col='none',sw=0,fill=SYS_BG))
    s.append(P([(x1,y0),(x0,y0),(x0,y1),(x1,y1)],INK,3)); s.append(P([(x0,94),(34,94)],INK,3)+P([(x0,106),(34,106)],INK,3))
    s.append(L(340,y0+3,340,y1-3,MUTED,2,dash='6 5')); s.append(T(340,y0-10,mix='처음',size=20,fill=MUTED))
    for i,(gx,gy) in enumerate([(90,82),(130,118),(170,86),(200,122),(105,108),(185,104)]):
        s.append(mvalt(gas(gx,gy),random.choice([-1,1])*6,random.choice([-1,1])*5,dur=f'{1.1+0.1*i:.1f}'))
    pis=[R(220,y0+3,16,y1-y0-6,INK,2,'#C9D2DB',2),L(236,100,400,100,INK,5),R(400,72,14,56,INK,2,'#C9D2DB',3),A(470,100,420,100,'ink',4)]
    s.append(an('move',''.join(pis),**{'from':'120,0','dur':'1.6','ease':'io'}))
    s.append(T(560,72,mix='$P_\\text{외부}=2.00\\ \\text{atm}$',size=21,anchor='end'))
    s.append(L(228,y1+30,340,y1+30,MUTED,1.5)+L(228,y1+22,228,y1+38,MUTED,1.5)+L(340,y1+22,340,y1+38,MUTED,1.5))
    s.append(T(284,y1+58,mix='20 cm',size=21))
    s.append(L(40,y0,40,y1,MUTED,1.5)+L(34,y0,46,y0,MUTED,1.5)+L(34,y1,46,y1,MUTED,1.5)+T(20,y1+58,mix='지름 3.0 cm',size=21,anchor='start'))
    s.append(T(130,y0-10,mix='계: 펌프 안 공기',size=20,fill=MUTED))
    return svg((570,215),560,'자전거 펌프의 피스톤을 2.00 atm 외부 압력으로 20 cm 밀어 안의 공기를 압축한다',s)
FIG['PUMP']=pump()
