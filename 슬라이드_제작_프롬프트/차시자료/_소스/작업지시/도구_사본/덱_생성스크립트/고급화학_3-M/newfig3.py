def ladder9():
    s=[]; Y=lambda E: 400-(E+0.3)*(360/1.8); X0=170
    s.append(A(X0,420,X0,22,'muted',2)); s.append(T(X0-10,26,mix='$E^\\circ$ [V]',size=20,anchor='end',fill=MUTED))
    items=[('\\ce{Cl2}/\\ce{Cl-}',1.36),('\\ce{Ag+}/\\ce{Ag}',0.80),('\\ce{Cu^2+}/\\ce{Cu}',0.34),('\\ce{H+}/\\ce{H2}',0.00),('\\ce{Pb^2+}/\\ce{Pb}',-0.13)]
    for t,E in items:
        y=Y(E); s.append(L(X0-8,y,X0+60,y,INK,2.5)); s.append(T(X0-14,y+7,mix=f'${t}$',size=20,anchor='end')); s.append(T(X0+66,y+7,mix=('%+.2f'%E).replace('+0.00','0.00'),size=20,anchor='start'))
    s.append(draw(A(280,Y(-0.13)-3,280,Y(1.36)+3,'field',3.5),delay='.3')); s.append(T(292,Y(1.12),mix='2) $+1.49$ V',size=21,anchor='start',fill=FIELD,weight=700,halo=True))
    s.append(T(292,Y(1.12)+26,mix='자발적',size=20,anchor='start',fill=FIELD))
    s.append(draw(A(440,Y(0.80)+3,440,Y(0.34)-3,'plus',3.5,d=True),delay='.8')); s.append(T(428,Y(0.62),mix='1) $-0.46$ V',size=21,anchor='end',fill=PLUS,weight=700,halo=True))
    s.append(T(428,Y(0.62)+26,mix='비자발적',size=20,anchor='end',fill=PLUS))
    s.append(T(280,Y(-0.13)+34,mix='화살표: 산화 전극 → 환원 전극',size=19,fill=MUTED))
    return svg((470,450),440,'표준 환원 전위 사다리: 납에서 염소로 가는 반응은 +1.49 V로 자발적, 은에서 구리 이온으로 가는 반응은 −0.46 V로 비자발적',s)
FIG['LAD9']=ladder9()
