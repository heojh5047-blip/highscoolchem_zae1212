s=open('gen.py',encoding='utf-8').read()
R=[
("items.append((dep+(0.6 if hh else 0),L(x1,y1,x2,y2","items.append((100+dep+(0.6 if hh else 0),L(x1,y1,x2,y2"),
("""    body,_=cell3d('nacl',230,240,205,rad,'ion',pop=True)
    s=[body,leg_ion(120,490,[('Na','\\\\ce{Na+}'),('Cl','\\\\ce{Cl-}')],size=22,gap=130,r=12)]
    return svg((460,520),430,""","""    body,_=cell3d('nacl',230,200,205,rad,'ion',pop=True)
    s=[body,leg_ion(130,418,[('Na','\\\\ce{Na+}'),('Cl','\\\\ce{Cl-}')],size=22,gap=130,r=12)]
    return svg((460,440),430,"""),
("""                for b in ((0,0),(1/3,2/3)):
                    x=(i+b[0])*1+(j+b[1])*.5; y=(j+b[1])*math.sqrt(3)/2""","""                for b in ((0,0),(.5,.5/math.sqrt(3))):
                    x=i+j*.5+b[0]; y=j*math.sqrt(3)/2+b[1]"""),
("""        b,_=cell3d(k,115+i*225,oy,112 if k!='fcc' else 104,RM,'met',coord=True,coord_step=f'c{i}')
        s.append(b); s.append(T(115+i*225,320,mix=n,size=21,weight=700))
        s.append(f'<g class="step" data-g="c{i}">'+T(115+i*225,348""","""        b,_=cell3d(k,140+i*235,oy,112 if k!='fcc' else 104,RM,'met',coord=True,coord_step=f'c{i}')
        s.append(b); s.append(T(140+i*235,320,mix=n,size=21,weight=700))
        s.append(f'<g class="step" data-g="c{i}">'+T(140+i*235,348"""),
("""    return svg((780,375),740,'세 단위세포""","""    return svg((800,375),740,'세 단위세포"""),
("""    s.append(T(x1+6,y-62,tex='r^+/r^-',size=20,anchor='end'))""","""    s.append(T(x1+6,y+62,tex='r^+/r^-',size=20,anchor='end'))"""),
("""FIG['ZNS']=ionic('zns',{'S':.14,'Zn':.07}""","""FIG['ZNS']=ionic('zns',{'S':.11,'Zn':.075}"""),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)
open('gen.py','w',encoding='utf-8').write(s)
j=open('labs_src.js',encoding='utf-8').read()
a="items.push({z:(a[2]+b[2])/2+(hid?.6:0),"
assert a in j; j=j.replace(a,"items.push({z:100+(a[2]+b[2])/2+(hid?.6:0),")
open('labs_src.js','w',encoding='utf-8').write(j)
print('ok')
