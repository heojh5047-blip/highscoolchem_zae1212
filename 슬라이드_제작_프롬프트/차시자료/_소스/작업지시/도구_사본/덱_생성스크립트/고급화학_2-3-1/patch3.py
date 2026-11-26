s=open('gen.py',encoding='utf-8').read()
R=[
("pr2=lambda p:rot(p,20,32,(0,0,0))","pr2=lambda p:rot(p,20,22,(0,0,0))"),
("for k,z in enumerate((-1.6,0,1.6)):","for k,z in enumerate((-2.4,0,2.4)):"),
("if math.hypot(x,y)<1.75: pts.append((x*.95,y*.95))","if math.hypot(x,y)<1.45: pts.append((x*.95,y*.95))"),
("hp=honey(); items=[]; S2=58; ox2,oy2=440,165","hp=honey(); items=[]; S2=50; ox2,oy2=440,150"),
("""    s.append(A(592,112,592,146,'muted',2,True)); s.append(A(592,146,592,112,'muted',2,True))
    s.append(T(600,92,mix='약한||결합력',size=18,fill=MUTED,anchor='end'))""","""    s.append(A(560,120,560,90,'muted',2,True)); s.append(A(560,90,560,120,'muted',2,True))
    s.append(T(568,112,mix='약한||결합력',size=18,fill=MUTED,anchor='start'))"""),
("return svg((620,340),600,'다이아몬드와 흑연의 구조',s)","return svg((640,340),600,'다이아몬드와 흑연의 구조',s)"),
("s.append(T(x1+6,y+62,tex='r^+/r^-',size=20,anchor='end'))","s.append(T(x0,y+62,tex='r^+/r^-',size=20,anchor='start'))"),
("return svg((380,370),360,{","return svg((380,370),430,{"),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)
open('gen.py','w',encoding='utf-8').write(s)
t=open('tpl.html',encoding='utf-8').read()
for k in ('ZNS','NACL','CSCL'):
    a=f'<div class="col" style="flex:0 0 380px">{{{{{k}}}}}</div>'
    assert a in t, k; t=t.replace(a,f'<div class="col" style="flex:0 0 440px">{{{{{k}}}}}</div>')
open('tpl.html','w',encoding='utf-8').write(t); print('ok')
