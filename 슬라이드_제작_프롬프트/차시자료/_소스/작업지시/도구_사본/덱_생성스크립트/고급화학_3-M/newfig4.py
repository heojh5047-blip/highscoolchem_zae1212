def dryer():
    s=[L(100,30,100,360,INK,4),L(100,30,230,30,INK,4),R(50,360,150,12,INK,2,'#C9D2DB')]
    s.append(L(210,240,210,300,MUTED,1.5,dash='5 4')+R(185,300,50,40,MUTED,1.5,'none',4,dash='5 4')+T(243,330,mix='처음',size=20,fill=MUTED,anchor='start'))
    band=P([(204,32),(204,200),(216,200),(216,32)],RUB,3,close=True)
    s.append(an('scale',band,**{'from':'1,1.3','o':'210,32','dur':'1.6','delay':'.4','ease':'io'}))
    s.append(an('move',R(185,200,50,40,INK,2,'#8C99A6',4)+T(210,228,mix='추',size=20,fill='#FFFFFF',weight=700),**{'from':'0,50','dur':'1.6','delay':'.4','ease':'io'}))
    s.append(R(290,110,80,46,INK,2,'#F3D9B1',8)+R(362,125,32,16,INK,2,'#F3D9B1',3)+R(310,156,22,50,INK,2,'#F3D9B1',4))
    for i,yy in enumerate((112,133,154)):
        s.append(an('move',wave(282,yy,240,yy,EQUI,4,12,2.5),**{'from':'10,0','rep':'alt','dur':'.8','delay':f'{.2*i:.1f}','ease':'io'}))
    s.append(T(330,236,mix='가열',size=21,fill=EQUI,weight=700))
    s.append(A(262,300,262,250,'field',3)+T(272,282,mix='줄어듦',size=20,fill=FIELD,anchor='start'))
    return svg((400,380),360,'추를 매단 고무줄을 헤어드라이어로 가열하면 고무줄이 줄어 추가 올라간다',s)
FIG['DRYER']=dryer()
