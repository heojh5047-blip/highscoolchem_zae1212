s=open('gen.py',encoding='utf-8').read()
R=[
("""    rad={'Cl':.2,'Na':.11}
    body,_=cell3d('nacl',230,250,270,rad,'ion',pop=True)""","""    rad={'Cl':.17,'Na':.09}
    body,_=cell3d('nacl',230,240,205,rad,'ion',pop=True)"""),
("""    s.append(L(40,yy,560,yy,MUTED,1.5,'3 4'))""","""    s.append(L(40,yy,540,yy,MUTED,1.5,'3 4'))"""),
("""    s.append(T(48,y1-12,mix='원자 면',size=18,fill=MUTED,anchor='start'))""","""    s.append(T(48,y2+40,mix='원자 면',size=18,fill=MUTED,anchor='start'))"""),
("""        pr2=lambda p:rot(p,20,62,(0,0,0))""","""        pr2=lambda p:rot(p,20,32,(0,0,0))"""),
("""    for k,z in enumerate((-1.25,0,1.25)):""","""    for k,z in enumerate((-1.6,0,1.6)):"""),
("""    for yy in (118,198): s.append(A(600,yy-30,600,yy+12,'muted',2,True))
    s.append(T(596,98,mix='약한||결합력',size=18,fill=MUTED,anchor='end'))""","""    s.append(A(592,112,592,146,'muted',2,True)); s.append(A(592,146,592,112,'muted',2,True))
    s.append(T(600,92,mix='약한||결합력',size=18,fill=MUTED,anchor='end'))"""),
("""        s.append(R(250+i*110,16,18,18,'none',0,col[k][0],3)); s.append(T(274+i*110,32,mix=col[k][1],size=18,anchor='start'))""","""        s.append(R(200+i*105,16,18,18,'none',0,col[k][0],3)); s.append(T(224+i*105,32,mix=col[k][1],size=18,anchor='start'))"""),
("""        b,_=cell3d(k,110+i*215,140,140,RM,'pos' if not coord else 'met',pop=not coord,coord=coord,coord_step=(f'c{i}' if coord else None))
        s.append(b); s.append(T(110+i*215,268,mix=n,size=21,weight=700))""","""        b,_=cell3d(k,130+i*250,140,112,RM,'pos' if not coord else 'met',pop=not coord,coord=coord,coord_step=(f'c{i}' if coord else None))
        s.append(b); s.append(T(130+i*250,262,mix=n,size=21,weight=700))"""),
("""        oy=160 if k!='fcc' else 175
        b,_=cell3d(k,115+i*225,oy,122 if k!='fcc' else 112,RM,'met',coord=True,coord_step=f'c{i}')""","""        oy=180 if k!='fcc' else 190
        b,_=cell3d(k,115+i*225,oy,112 if k!='fcc' else 104,RM,'met',coord=True,coord_step=f'c{i}')"""),
("""    return svg((780,362),760,'세 단위세포""","""    return svg((780,375),740,'세 단위세포"""),
("""        s.append(C(cx,cy,r,'#2F5F98',1.2,'#4F86C6',extra='opacity=".18"')); s.append(f'<g {cp}>'""","""        s.append(f'<g {cp}>'"""),
("""        s.append(C(cx,cy,r,'#2F5F98',1.2,'#4F86C6' if (cx,cy)!=(x1+W/2,y1+H/2) else '#C0504D',extra='opacity=".18"'))
""",""),
("""        s.append(C(cx,cy,r,sc_,1.2,fc,extra='opacity=".18"')); s.append(f'<g {cp}>'""","""        s.append(f'<g {cp}>'"""),
("""    s.append(T(x1+6,y+28,tex='r^+/r^-',size=20,anchor='end'))""","""    s.append(T(x1+6,y-62,tex='r^+/r^-',size=20,anchor='end'))"""),
("""        s.append(f'<g class="step" data-g="r{i}">'+A(X(v),y+88,X(v),y+10,'plus',2.5)+T(X(v),y+112,tex=tex,size=21)+T(X(v),y+136,mix='%.2f'%v,size=18,fill=PLUS)+'</g>')""","""        s.append(f'<g class="step" data-g="r{i}">'+A(X(v),y+96,X(v),y+42,'plus',2.5)+T(X(v),y+120,tex=tex,size=21)+T(X(v),y+144,mix='%.2f'%v,size=18,fill=PLUS)+'</g>')"""),
("""    b,_=cell3d(key,190,175,250,rad,'ion',coord=True,coord_step='cn')""","""    b,_=cell3d(key,190,170,188,rad,'ion',coord=True,coord_step='cn')"""),
("""FIG['ZNS']=ionic('zns',{'S':.17,'Zn':.075}""","""FIG['ZNS']=ionic('zns',{'S':.14,'Zn':.07}"""),
("""FIG['NACL']=ionic('nacl',{'Cl':.19,'Na':.10}""","""FIG['NACL']=ionic('nacl',{'Cl':.15,'Na':.08}"""),
("""FIG['CSCL']=ionic('cscl',{'Cl':.2,'Cs':.185}""","""FIG['CSCL']=ionic('cscl',{'Cl':.155,'Cs':.145}"""),
("""    s.append(T(336,12,mix='전원',size=18))""","""    s.append(T(300,22,mix='전원',size=18,anchor='end'))"""),
("""    s.append(T(540,200,mix='양이온 + 전자(전체 중성)',size=18,fill=MUTED))""","""    s.append(T(600,200,mix='양이온 + 전자(전체 중성)',size=18,fill=MUTED,anchor='end'))"""),
("""FIG['Q4FIG']=svg((220,220),200,'면심 입방 구조로 쌓인 원자 14개',[fcc_balls(112,110,112,.3536)])""","""FIG['Q4FIG']=svg((220,220),200,'면심 입방 구조로 쌓인 원자 14개',[fcc_balls(92,110,110,.3536)])"""),
("""FIG['FCC14']=svg((220,230),200,'면심 입방 구조의 공 모형(원자 14개)',[fcc_balls(118,110,118,.3536,True)])""","""FIG['FCC14']=svg((220,220),200,'면심 입방 구조의 공 모형(원자 14개)',[fcc_balls(92,110,110,.3536,True)])"""),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)
open('gen.py','w',encoding='utf-8').write(s)
t=open('tpl.html',encoding='utf-8').read()
a='<h2><span class="tag">탐구 활동</span>3D 모델링 프로그램으로 단위세포 모형 만들기와 배위수 조사 <span'
assert a in t; t=t.replace(a,'<h2><span class="tag">탐구 활동</span>3D 단위세포 모형 만들기와 배위수 조사 <span')
a='''<button class="btn" data-k="hcp">육방 밀집</button></div>
      <div class="ac231-seg"><span class="small">이온</span><button'''
assert a in t; t=t.replace(a,'''<button class="btn" data-k="hcp">육방 밀집</button>
      <button''')
t=t.replace('<div class="ac231-seg"><span class="small">금속</span><button class="btn on" data-k="sc">','<div class="ac231-seg"><button class="btn on" data-k="sc">')
open('tpl.html','w',encoding='utf-8').write(t)
print('patched')
