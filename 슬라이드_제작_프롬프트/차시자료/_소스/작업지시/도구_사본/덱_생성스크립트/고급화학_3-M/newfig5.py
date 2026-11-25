def ladder26():
    s=[]; Y=lambda E: 410-(E+2.6)*(380/3.6); X0=180
    s.append(A(X0,430,X0,20,'muted',2)); s.append(T(X0-10,24,mix='$E^\\circ$ [V]',size=20,anchor='end',fill=MUTED))
    for m,E in sorted(EP.items(),key=lambda t:-t[1]):
        y=Y(E); fl,st=MET[m]
        s.append(L(X0-8,y,X0+60,y,INK,2.5)+C(X0-30,y,11,st,1.5,fl)); s.append(T(X0-50,y+7,mix=f'$\\ce{{{m}}}$',size=21,anchor='end')); s.append(T(X0+66,y+7,mix=('%+.2f'%E),size=20,anchor='start'))
    s.append(draw(A(330,Y(-2.37)-3,330,Y(0.80)+3,'field',4),dur='1',delay='.3')); s.append(T(342,Y(-1.9),mix='$\\ce{Mg}$–$\\ce{Ag}$',size=21,anchor='start',fill=FIELD,weight=700,halo=True)+T(342,Y(-1.9)+28,mix='3.17 V',size=21,anchor='start',fill=FIELD,weight=700))
    s.append(draw(A(470,Y(-0.76)-3,470,Y(0.34)+3,'ink',3),dur='.6',delay='1')); s.append(T(460,Y(-1.05),mix='$\\ce{Zn}$–$\\ce{Cu}$ 1.10 V',size=20,anchor='end',halo=True))
    return svg((520,440),470,'금속 여섯 가지의 표준 환원 전위 사다리: 가장 멀리 떨어진 마그네슘과 은의 조합이 3.17 V로 가장 크다',s)
FIG['LAD26']=ladder26()

def art():
    s=[circ([["wire",[[242,40],[120,40],[120,150]]],["bat",[250,40],{"dir":"h","pos":"right","signs":True}],["wire",[[258,40],[312,40]]],["bat",[320,40],{"dir":"h","pos":"right","signs":True}],["wire",[[328,40],[480,40],[480,236]]]])]
    s.append(T(285,84,mix='다니엘 전지 2개 직렬 (약 2.2 V)',size=20,fill=MUTED))
    s.append(P([(40,300),(150,232),(550,232),(440,300)],INK,2,fill=MET['Al'][0],close=True))
    s.append(P([(70,292),(162,240),(520,240),(428,292)],'#C9D3DD',1.5,fill='#FBFAF5',close=True))
    line=[(330,270),(290,258),(250,268),(210,256),(172,264)]
    s.append(draw(P(line,PHE,6,extra='stroke-linecap="round"'),dur='1.4',delay='.3'))
    s.append(L(120,150,163,250,'#4A4F57',16,extra='stroke-linecap="round"')+P([(157,246),(172,264),(171,240)],INK,1.5,fill='#4A4F57',close=True))
    s.append(T(132,130,mix='흑연 펜: (−)극',size=20,fill=RD,anchor='start'))
    s.append(T(330,222,mix='$\\ce{OH-}$ 생김 → 붉은 선',size=20,fill=PHE,anchor='start'))
    s.append(T(20,326,mix='$\\ce{Na2SO4}$ + 페놀프탈레인 종이',size=20,anchor='start',fill=MUTED))
    s.append(T(552,326,mix='포일 판: (+)극',size=20,anchor='end',fill=OX))
    return svg((560,340),520,'다니엘 전지 두 개를 직렬로 이어 흑연 펜을 (−)극, 알루미늄 포일 판을 (+)극에 연결하고, 황산 나트륨과 페놀프탈레인을 적신 종이 위에 펜으로 그리면 붉은 선이 생긴다',s)
FIG['ART']=art()
