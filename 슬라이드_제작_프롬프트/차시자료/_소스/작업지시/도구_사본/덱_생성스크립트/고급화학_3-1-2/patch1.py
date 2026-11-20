import re
p='gen.py'; s=open(p,encoding='utf-8').read()
def repl(name,new):
    global s
    a=s.index('def '+name+'(')
    b=s.index('\n# ═════',a)
    # keep FIG lines: new must include its own FIG assignment
    s=s[:a]+new.strip('\n')+'\n'+s[b:]
repl('cover',r'''
def cover():
    e=EN(342,1.20,'표지'); s=[]
    s.append(e.lev(100,240,0,tex='\\ce{N2(g) + 2O2(g)}',dy=30,lx=170))
    s.append(L(240,e.Y(0),372,e.Y(0),MUTED,1.5,'5 4'))
    s.append(e.lev(130,300,180,tex='\\ce{2NO(g) + O2(g)}',lx=215))
    s.append(e.lev(270,380,68,tex='\\ce{2NO2(g)}',dy=-12,lx=330))
    s.append(an('draw',e.arr(165,0,180,'field',4),dur='1.0'))
    s.append(T(157,e.Y(100),tex='+180',size=22,anchor='end',fill=FIELD))
    s.append(an('draw',e.arr(285,180,68,'bfield',4),dur='1.0',delay='.9'))
    s.append(T(277,e.Y(130),tex='-112',size=22,anchor='end',fill=BF))
    s.append(an('draw',e.arr(355,0,68,'ink',4),dur='.9',delay='1.8'))
    s.append(T(347,e.Y(30)+8,tex='+68',size=22,anchor='end',halo=True))
    return svg((460,460),430,'헤스 법칙: 질소가 두 단계(+180 kJ, −112 kJ)를 거쳐도 한 단계(+68 kJ)로 반응해도 엔탈피 변화는 같다',s,'fig cover-fig')
FIG['COVER']=cover()
''')
s=s.replace("T(80,266,tex='\\\\ce{CO2}\\\\ \\\\text{배출·고갈}',size=19,fill=MUTED)","T(80,266,mix='$\\\\ce{CO2}$ 배출, 고갈',size=19,fill=MUTED)")
# openfig titles
s=s.replace("s.append(T(125,60,mix='(가) 단단한 통',size=21,weight=700))","s.append(T(125,22,mix='(가) 단단한 통',size=21,weight=700))")
s=s.replace("x=330; s.append(an('move',cyl(x,60,170,260,120,SYSBG,9,11)","x=330; s.append(an('move',cyl(x,70,170,260,124,SYSBG,9,11)")
s=s.replace("for xx in (365,415,465): s.append(A(xx,52,xx,104,'ink',3))\n    s.append(T(415,40,mix='대기압 약 $1\\\\ \\\\text{atm}$',size=19))",
            "for xx in (365,415,465): s.append(A(xx,64,xx,110,'ink',3))\n    s.append(T(415,54,mix='대기압 약 $1\\\\ \\\\text{atm}$',size=19))")
s=s.replace("s.append(L(x+3,146,x+167,146,MUTED,1.5,'5 4')+T(x+176,150,mix='처음',size=18,anchor='start',fill=MUTED))\n    s.append(A(x+188,132,x+188,98,'ink',4)+T(x+178,92,mix='대기를||밀어냄',size=18,anchor='start'))",
            "s.append(L(x+3,150,x+167,150,MUTED,1.5,'5 4')+T(x+176,156,mix='처음',size=18,anchor='start',fill=MUTED))\n    s.append(A(x+190,140,x+190,104,'ink',4)+T(x+180,192,mix='대기를||밀어냄',size=18,anchor='start'))")
# hdef
s=s.replace("s.append(T(158,88,tex='\\\\equiv',size=38)+T(296,88,tex='+',size=38))","s.append(T(158,88,tex='\\\\equiv',size=38)+T(313,88,tex='+',size=38))")
s=s.replace("boxes=[(20,'H','엔탈피',PLUS),(200,'U','내부 에너지',INK),(330,'P','압력',INK),(450,'V','부피',INK)]","boxes=[(20,'H','엔탈피',PLUS),(200,'U','내부 에너지',INK),(334,'P','압력',INK),(450,'V','부피',INK)]")
s=s.replace("s.append(T(355,190,mix='셋 다 상태 함수 → $H$도 상태 함수',size=20,fill=FIELD,weight=700))\n    s.append(P([(220,166),(220,172),(530,172),(530,166)],FIELD,2))",
            "s.append(T(373,200,mix='셋 다 상태 함수 → $H$도 상태 함수',size=20,fill=FIELD,weight=700))\n    s.append(P([(216,158),(216,166),(540,166),(540,158)],FIELD,2))")
s=s.replace("return svg((570,210),540,'엔탈피 H는","return svg((570,214),540,'엔탈피 H는")
# cup/bomb label sizes
for a,b in (("mix='온도계',size=21,anchor='start')+T(140,54,mix='젓개',size=21","mix='온도계',size=25,anchor='start')+T(140,54,mix='젓개',size=25"),
            ("T(180,92,mix='뚜껑',size=21,halo=True)","T(180,92,mix='뚜껑',size=25,halo=True)"),
            ("T(180,372,mix='대기압에서 반응',size=22)","T(180,376,mix='대기압에서 반응',size=25)"),
            ("T(200,36,mix='점화 단자',size=21)+T(318,62,mix='온도계',size=21,anchor='start')","T(200,34,mix='점화 단자',size=25)+T(312,62,mix='온도계',size=25,anchor='start')"),
            ("T(100,318,mix='물',size=21)+T(146,160,mix='강철 통',size=21,anchor='end')","T(100,318,mix='물',size=25)+T(146,160,mix='강철 통',size=25,anchor='end')"),
            ("T(200,372,mix='부피 일정',size=22)","T(200,376,mix='부피 일정',size=25)")):
    assert a in s,a; s=s.replace(a,b)
s=s.replace("return svg((380,390),w,'컵 열량계","return svg((400,392),w,'컵 열량계").replace("return svg((400,390),w,'통열량계","return svg((420,392),w,'통열량계")
repl('sign',r'''
def sign():
    sc=0.80; s=[haxis(24,26,350)]
    e1=EN(96,sc,'S8 발열·흡열')
    s.append(e1.lev(60,240,0,tex='\\ce{Zn(s) + I2(s)}'))
    s.append(e1.lev(60,240,-208,tex='\\ce{ZnI2(s)}',dy=30))
    s.append(an('draw',e1.arr(160,0,-208,'ink',4),dur='1.1'))
    s.append(T(172,e1.Y(-104)+8,tex='-208\\ \\text{kJ}',size=21,anchor='start',halo=True))
    s.append(an('fade',A(150,e1.Y(-130),90,e1.Y(-130),'equi',4),dur='1',rep='loop')+T(118,e1.Y(-130)-14,mix='열 방출',size=19,fill=EQUI))
    s.append(T(150,378,mix='발열: $\\Delta H&lt;0$',size=21,weight=700))
    e2=EN(300,sc,'S8 발열·흡열')
    s.append(e2.lev(360,560,0,tex='\\ce{N2(g) + O2(g)}',dy=30))
    s.append(e2.lev(360,560,180,tex='\\ce{2NO(g)}'))
    s.append(an('draw',e2.arr(460,0,180,'ink',4),dur='1.1',delay='.6'))
    s.append(T(472,e2.Y(90)+8,tex='+180\\ \\text{kJ}',size=21,anchor='start',halo=True))
    s.append(an('fade',A(392,e2.Y(60),450,e2.Y(60),'equi',4),dur='1',rep='loop')+T(420,e2.Y(60)-14,mix='열 흡수',size=19,fill=EQUI))
    s.append(T(460,378,mix='흡열: $\\Delta H&gt;0$',size=21,weight=700))
    return svg((600,392),560,'같은 비율의 엔탈피 도표: 아이오딘화 아연 생성은 208 kJ 발열, 일산화 질소 생성은 180 kJ 흡열',s)
FIG['SIGN']=sign()
''')
repl('ch4st',r'''
def ch4st():
    e=EN(70,0.30,'S12 그림 Ⅲ-11'); s=[haxis(26,30,370)]
    s.append(e.lev(60,420,0,tex='\\ce{CH4(g) + 2O2(g)}',lx=240))
    s.append(e.lev(60,290,-802,tex='\\ce{CO2(g) + 2H2O(g)}',lx=190))
    s.append(e.lev(60,420,-890,tex='\\ce{CO2(g) + 2H2O(l)}',dy=30,lx=240))
    s.append(an('draw',e.arr(84,0,-802,'ink',4),dur='1.1'))
    s.append(T(96,e.Y(-400),tex='-802\\ \\text{kJ}',size=21,anchor='start',halo=True))
    s.append(an('draw',e.arr(390,0,-890,'ink',4),dur='1.2',delay='.4'))
    s.append(T(380,e.Y(-445),tex='-890\\ \\text{kJ}',size=21,anchor='end',halo=True))
    s.append(L(290,e.Y(-802),336,e.Y(-802),MUTED,1.5,'5 4'))
    s.append(an('draw',e.arr(316,-802,-890,'equi',3,2),dur='.6',delay='1.4'))
    s.append(T(328,e.Y(-846)+7,tex='-88\\ \\text{kJ}',size=20,anchor='start',fill=EQUI,halo=True))
    return svg((520,380),470,'메테인 연소의 엔탈피 변화: 수증기가 생기면 −802 kJ, 물이 생기면 −890 kJ, 차이 88 kJ',s)
FIG['CH4ST']=ch4st()
''')
repl('diam',r'''
def diam():
    e=EN(96,0.70,'S16 예제 Ⅲ-4'); s=[haxis(26,24,396)]
    s.append(e.lev(60,190,2,tex='\\mathrm{C}_\\text{다이아몬드}(s)+\\ce{O2(g)}',dy=-12,lx=125))
    s.append(e.lev(210,360,0,tex='\\mathrm{C}_\\text{흑연}(s)+\\ce{O2(g)}',dy=-12,lx=290))
    s.append(e.lev(60,360,-394,tex='\\ce{CO2(g)}',dy=30))
    s.append(an('draw',e.arr(110,2,-394,'bfield',4),dur='1.1'))
    s.append(T(122,e.Y(-190),tex='-396\\ \\text{kJ}',size=21,anchor='start',fill=BF,halo=True))
    s.append(an('draw',e.arr(300,0,-394,'field',4),dur='1.1',delay='.4'))
    s.append(T(312,e.Y(-250),tex='-394\\ \\text{kJ}',size=21,anchor='start',fill=FIELD,halo=True))
    cx,cy,r=448,196,58; z=40
    s.append(C(200,e.Y(1),14,MUTED,1.5,'none','3 3')+L(213,e.Y(1)+5,cx-r+3,cy-12,MUTED,1.5,'3 3'))
    yd,yg=cy-z*0.7*1,cy+z*0.7*1
    s.append(C(cx,cy,r,MUTED,2,'#FFFFFF'))
    s.append(L(cx-44,yd,cx-4,yd,INK,3)+L(cx+4,yg,cx+44,yg,INK,3)+L(cx-4,yd,cx+44,yd,MUTED,1.5,'4 3'))
    s.append(an('draw',A(cx+24,yg-3,cx+24,yd+3,'ink',3),dur='.6',delay='1.4'))
    s.append(T(cx,cy+r+24,tex='+2\\ \\text{kJ}',size=21,weight=700)+T(cx,cy-r-10,mix='확대 ×40',size=18,fill=MUTED))
    return svg((520,410),480,'흑연과 다이아몬드의 연소 엔탈피 도표: 다이아몬드가 흑연보다 2 kJ 높다(확대 원)',s)
FIG['DIAM']=diam()
''')
s=s.replace("s.append(T(x0,30,mix='원소 = 0',size=19,fill=MUTED))","s.append(T(x0,30,mix='원소 = 0',size=22,fill=MUTED))")
s=s.replace("s.append(T(400,top+8*hh+34,mix='$\\\\Delta H_\\\\mathrm{f}^\\\\circ$ (kJ/mol, 25 °C)',size=20,fill=MUTED))\n    return svg((740,388)",
            "s.append(T(400,top+8*hh+36,mix='$\\\\Delta H_\\\\mathrm{f}^\\\\circ$ (kJ/mol, 25 °C)',size=21,fill=MUTED))\n    return svg((740,402)")
repl('pathd',r'''
def pathd():
    e=EN(56,0.34,'S21 경로 도표'); s=[haxis(24,22,392)]
    s.append(e.lev(160,470,0,tex='\\mathrm{C}_\\text{흑연}+\\ce{2H2 + 2O2}\\ (\\text{원소})',dy=-12,lx=330))
    s.append(e.lev(40,200,-75,tex='\\ce{CH4 + 2O2}',dy=30,lx=110))
    s.append(e.lev(250,470,-394,tex='\\ce{CO2 + 2H2 + O2}',dy=-12,lx=380))
    s.append(e.lev(40,470,-966,tex='\\ce{CO2 + 2H2O(l)}',dy=30,lx=290))
    s.append(an('draw',e.arr(190,-75,0,'field',3,2),dur='.6'))
    s.append(T(182,e.Y(-37)+8,tex='+75',size=19,anchor='end',fill=FIELD))
    s.append(an('draw',e.arr(300,0,-394,'bfield',3),dur='.9',delay='.5'))
    s.append(T(310,e.Y(-200),tex='-394',size=19,anchor='start',fill=BF))
    s.append(an('draw',e.arr(430,-394,-966,'bfield',3),dur='1',delay='1.2'))
    s.append(T(422,e.Y(-680),tex='-572',size=19,anchor='end',fill=BF))
    s.append(an('draw',e.arr(80,-75,-966,'ink',4),dur='1.1',delay='2'))
    s.append(T(92,e.Y(-560),tex='\\Delta H^\\circ=-891\\ \\text{kJ}',size=21,anchor='start',halo=True,weight=700))
    return svg((490,412),470,'메테인 연소의 엔탈피 도표: 원소를 거치는 경로의 합이 −891 kJ',s)
FIG['PATHD']=pathd()
''')
repl('hess2',r'''
def hess2():
    e=EN(330,1.30,'S25 그림 Ⅲ-14'); s=[haxis(24,30,350,'$H$ (kJ)')]
    s.append(e.lev(90,230,0,tex='\\ce{N2(g), 2O2(g)}',dy=30,lx=160))
    s.append(e.lev(110,270,180,tex='\\ce{O2(g), 2NO(g)}',lx=190))
    s.append(e.lev(220,360,68,tex='\\ce{2NO2(g)}',lx=300,dy=-12))
    s.append(L(230,e.Y(0),290,e.Y(0),MUTED,1.5,'5 4'))
    s.append(an('draw',e.arr(150,0,180,'field',4),dur='1'))
    s.append(T(142,e.Y(95),tex='\\Delta H_2=+180',size=20,anchor='end',fill=FIELD,halo=True))
    s.append(an('draw',e.arr(250,180,68,'bfield',4),dur='.9',delay='.8'))
    s.append(T(260,e.Y(140),tex='\\Delta H_3=-112',size=20,anchor='start',fill=BF))
    s.append(an('draw',e.arr(280,0,68,'ink',4),dur='.7',delay='1.6'))
    s.append(T(290,e.Y(30)+6,tex='\\Delta H_1',size=20,anchor='start'))
    s.append(T(190,22,mix='2단계 반응',size=21,weight=700,fill=MUTED))
    x=470
    s.append(e.lev(x,x+190,0,tex='\\ce{N2(g), 2O2(g)}',dy=30))
    s.append(e.lev(x,x+190,68,tex='\\ce{2NO2(g)}'))
    s.append(an('draw',e.arr(x+50,0,68,'ink',4),dur='.8',delay='2.2'))
    s.append(T(x+62,e.Y(34)+8,tex='\\Delta H_1=+68\\ \\text{kJ}',size=20,anchor='start',halo=True))
    s.append(T(x+95,e.Y(180)+20,mix='1단계 반응',size=21,weight=700,fill=MUTED))
    s.append(f'<g class="step" data-g="h1">'+T(x+95,e.Y(130),tex='=\\Delta H_2+\\Delta H_3',size=20)+T(x+95,e.Y(130)+30,tex='=180-112\\ \\text{(kJ)}',size=20)+'</g>')
    return svg((680,370),640,'그림 Ⅲ-14 헤스 법칙의 원리: 2단계 반응의 엔탈피 변화 합 +180 − 112와 1단계 반응의 +68 kJ이 같다',s)
FIG['HESS2']=hess2()
''')
s=s.replace("e=EN(262,0.075,'S27 결합 엔탈피'); s=[haxis(24,22,350)]","e=EN(292,0.075,'S27 결합 엔탈피'); s=[haxis(24,22,384)]")
s=s.replace("return svg((490,358),470,'결합 엔탈피 경로","return svg((490,398),470,'결합 엔탈피 경로")
s=s.replace("s.append(T(ax.X(V1)-4,ax.Y(2.0)-14,mix='처음 (24.6 L, 2.00 atm)',size=18,anchor='middle',halo=True))","s.append(T(ax.X(V1)+4,ax.Y(2.0)-16,mix='처음 (24.6 L, 2.00 atm)',size=18,anchor='end',halo=True))")
s=s.replace("T(102,e.Y(-300),tex='-443.7\\\\ \\\\text{kJ}'","T(102,e.Y(-210),tex='-443.7\\\\ \\\\text{kJ}'")
open(p,'w',encoding='utf-8').write(s)
