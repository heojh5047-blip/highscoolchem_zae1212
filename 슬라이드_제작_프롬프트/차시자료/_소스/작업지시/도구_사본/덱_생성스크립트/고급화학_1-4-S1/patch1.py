import re
p='gen.py'; s=open(p,encoding='utf-8').read()
def func(name):
    m=re.search(r'\ndef '+name+r'\(.*?(?=\n(?:def |FIG\[|# ═))',s,flags=re.S); assert m,name; return m
def repl(name,new):
    global s; m=func(name); s=s[:m.start()]+'\n'+new.strip('\n')+s[m.end():]
def region(a,b):
    i=s.index(a); j=s.index(b,i); return i,j
s=s.replace("def hyd(x,y,S=24,lpd=('u','d','r'),fcp='ul',","def hyd(x,y,S=24,lpd=('u','d','r'),fcp='u',")
# arr2, sn1a-c : 아래로 10 내림
for nm in ('arr2','sn1a','sn1b','sn1c'):
    m=func(nm); body=m.group(0)
    body=re.sub(r"(tbu\(\d+,|Cc\(\d+,|A_\('C',\d+,|G_\('CH3',\d+,|O_\(\d+,|H_\(\d+,|water\(\d+,|X_\('Br',\d+,|plus\(\d+,|cond\(\d+,|lpxy\(\d+,|harrow\(\d+,\d+,|lab\(\d+,)(\d+)",lambda k:k.group(1)+str(int(k.group(2))+10),body)
    body=re.sub(r"curved\((\d+),(\d+),(\d+),(\d+)",lambda k:f"curved({k.group(1)},{int(k.group(2))+10},{k.group(3)},{int(k.group(4))+10}",body)
    body=body.replace("svg('0 0 320 220'","svg('0 0 320 236'").replace("svg('0 0 330 236'","svg('0 0 330 250'")
    s=s[:m.start()]+body+s[m.end():]
repl('nucfig','''
def nucfig():
    S=24; s=[]
    s.append(hyd(96,160,S=S,lpd=('u','d','r'),name='n OH-')); s.append(lab(86,214,'친핵체 = 염기',20,MINUS))
    a=[G_('H3C',390,96),X_('Br',466,96,['u','d','r'])]
    s.append(M(a,[(0,1,1,'l')],'CH3Br',S=S,name='n CH3Br')); s.append(dlab(402,62,1,20)); s.append(dlab(466,54,-1,20))
    s.append(M([A_('H',400,236,oct=0,fc=1,fcp='ur')],[],'H',S=S,name='n H+'))
    sx,sy=lpxy(96,160,'r')
    s.append(DRAW(curved(sx+4,sy-6,366,104,bend=-26),.3)); s.append(DRAW(curved(sx+4,sy+6,386,232,bend=26),.9))
    s.append(lab(300,30,'탄소에 전자쌍 → 친핵성',20,INK)); s.append(lab(300,290,'수소 이온에 전자쌍 → 염기성',20,INK))
    return svg('0 0 520 310',500,'수산화 이온이 브로모메테인의 탄소에 전자쌍을 주면 친핵성, 수소 이온에 주면 염기성',s)
''')
s=s.replace("s.append(lab(T1[0],T1[1]-14,'전이 상태 1',19,INK))\n","")
s=s.replace("s.append(lab(T1[0]+86,T1[1]+4,'속도 결정 단계',19,PLUS,weight=700))","s.append(lab(T1[0],T1[1]-14,'속도 결정 단계',19,PLUS,weight=700))")
repl('e1fig','''
def e1fig():
    S=22; s=[]
    a,b=tbu(80,150,S,X='Cl',XL=58); s.append(M(a,b,'C4H9Cl',S=S,name='E1 RCl'))
    s.append(DRAW(curved(110,144,132,132,bend=-12),.3))
    s.append(harrow(170,214,150)); s.append(lab(192,134,'느림',19,PLUS,weight=700))
    cx,cy,bx=310,150,384
    a=[A_('C',cx,cy,oct=6,fc=1,fcp='d'),G_('CH3',cx-46,cy-40),G_('CH3',cx-46,cy+40),Cc(bx,cy),H_(bx,cy-48),H_(bx+48,cy),H_(bx,cy+50)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(0,3,1,'l'),(3,4,1,'l'),(3,5,1,'l'),(3,6,1,'l')],'C4H9',S=S,name='E1 R+'))
    SPEC['E1 Cl-']=(formula('Cl'),-1); rxn(['E1 RCl'],['E1 R+','E1 Cl-'],'S20-1')
    s.append(water(cx,42,S,'E1 H2O a',lpd=(270,180),hd=-1))
    s.append(DRAW(curved(cx+2,62,cx+2,cy-18,bend=-12),.9))
    s.append(water(bx+110,cy+82,S,'E1 H2O b',lpd=(180,90)))
    sx,sy=lpxy(bx+110,cy+82,'l',S=S); s.append(DRAW(curved(sx-3,sy,bx+12,cy+56,bend=16),1.3))
    s.append(DRAW(curved(bx-8,cy+30,(cx+bx)/2,cy+8,bend=12),1.7))
    s.append(lab(cx-30,cy+86,'탄소 양이온',19,EQUI,weight=700))
    s.append(harrow(540,600,62)); s.append(lab(570,40,'치환 ($\\\\mathrm{S_N1}$)',19,FIELD,weight=700))
    s.append(lab(470,62,'물이 C+ 공격',19,INK))
    s.append(cond(710,70,'(CH3)3COH',24)); s.append(lab(710,102,'2-메틸-2-프로판올',19))
    s.append(harrow(560,620,238)); s.append(lab(590,216,'제거 ($\\\\mathrm{E1}$)',19,BF,weight=700))
    s.append(cond(730,246,'(CH3)2C=CH2',24)); s.append(lab(730,278,'2-메틸프로펜',19))
    return svg('0 0 840 296',800,'2-클로로-2-메틸프로페인이 탄소 양이온이 된 뒤 물이 양이온을 공격하면 치환, 이웃 탄소의 수소를 떼어 내면 제거',s)
''')
# e1cb 세로 줄임
m=func('e1cb'); b=m.group(0)
b=b.replace("S=20; s=[]; y=150","S=20; s=[]; y=128").replace("hyd(160,262","hyd(160,232").replace("lpxy(160,262","lpxy(160,232").replace("y+150,","y+112,").replace("svg('0 0 1100 310'","svg('0 0 1100 250'")
s=s[:m.start()]+b+s[m.end():]
repl('flow','''
def flow():
    s=[]; top=34
    s.append(box(560,top,280,44,'할로젠화 알킬: 기질의 차수는?','q'))
    xs=[90,300,650,990]; names=['메틸','1차','2차','3차']
    for i,(x,n) in enumerate(zip(xs,names)):
        s.append(L(560,top+22,x,104,MUTED,2)); s.append(box(x,118,120,36,n,'q'))
    def br(g,items): return step(items,g)
    s.append(br('b1',[L(90,136,90,180,MUTED,2),box(90,206,130,52,'$\\\\mathrm{S_N2}$','s',22),lab(90,262,'β 수소 없음',19),lab(90,286,'→ 제거 불가',19)]))
    s.append(br('b2',[L(300,136,230,180,MUTED,2),L(300,136,380,180,MUTED,2),
        box(230,206,120,52,'$\\\\mathrm{S_N2}$','s',22),lab(230,262,'좋은 친핵체',19),
        box(380,206,120,52,'$\\\\mathrm{E2}$','e',22),lab(380,262,'부피 큰 강한 염기',19),lab(380,286,'$\\\\ce{(CH3)3CO-}$',19)]))
    s.append(br('b3',[L(650,136,530,180,MUTED,2),L(650,136,650,180,MUTED,2),L(650,136,770,180,MUTED,2),
        box(530,206,110,52,'$\\\\mathrm{S_N2}$','s',22),lab(530,262,'$\\\\ce{I-}$, $\\\\ce{CN-}$',19),lab(530,286,'비양성자성',19),
        box(650,206,110,52,'$\\\\mathrm{E2}$','e',22),lab(650,262,'강한 염기',19),
        box(770,206,110,52,'$\\\\mathrm{S_N1}$·$\\\\mathrm{E1}$','n',20),lab(770,262,'물·알코올',19),lab(770,286,'(느림)',19)]))
    s.append(br('b4',[L(990,136,930,180,MUTED,2),L(990,136,1054,180,MUTED,2),
        box(930,206,100,52,'$\\\\mathrm{E2}$','e',22),lab(930,262,'강한 염기',19),
        box(1054,206,116,52,'$\\\\mathrm{S_N1}$+$\\\\mathrm{E1}$','n',20),lab(1054,262,'물·알코올',19),lab(1054,286,'(중성)',19),lab(990,320,'$\\\\mathrm{S_N2}$ 불가(입체 장애)',19,PLUS)]))
    s.append(box(560,354,600,40,'카보닐기 옆 산성 수소 → 차수와 관계없이 $\\\\mathrm{E1cB}$','n',19))
    return svg('0 0 1120 380',1100,'할로젠화 알킬의 반응 경로 고르기 흐름도: 기질의 차수, 시약의 염기성, 용매의 종류',s)
''')
m=func('wil'); b=m.group(0)
b=b.replace("G_('CH3CH2',40,y)","G_('CH3CH2',58,y)").replace("O_(108,y","O_(126,y").replace("lpxy(108,y","lpxy(126,y")
s=s[:m.start()]+b+s[m.end():]
for nm in ('rad1','rad2','rad3','rad4'):
    m=func(nm); b=m.group(0)
    b=b.replace("y=56","y=70").replace(",150,",",164,").replace("(40,80,150)","(40,80,164)").replace("(30,70,150)","(30,70,164)").replace("svg('0 0 270 190'","svg('0 0 270 214'").replace("svg('0 0 270 200'","svg('0 0 270 214'")
    b=b.replace("plus(166,164)","plus(166,164)")
    if nm=='rad2': b=b.replace("a=[H_(96,164),clx(140,164,'urd',S,'')]","a=[H_(70,164),clx(112,164,'urd',S,'')]").replace("plus(180,164)","plus(160,164)")
    s=s[:m.start()]+b+s[m.end():]
s=s.replace("s.append(A(220,66,360,40,'ink',2.4)); s.append(lab(290,30,'산 촉매 수화 · 옥시수은화',19,INK))","s.append(A(220,66,350,40,'ink',2.4)); s.append(lab(214,34,'산 촉매 수화 · 옥시수은화',19,INK,anchor='end'))")
s=s.replace("s.append(A(220,94,360,120,'ink',2.4)); s.append(lab(290,140,'수소붕소화–산화',19,INK))","s.append(A(220,94,350,120,'ink',2.4)); s.append(lab(214,134,'수소붕소화–산화',19,INK,anchor='end'))")
repl('bromo','''
def bromo():
    S=22; s=[]; y=176
    a=[Cc(60,y),Cc(120,y),H_(30,y-40),H_(30,y+40),H_(150,y-40),H_(150,y+40)]
    s.append(M(a,[(0,1,2,'l'),(0,2,1,'l'),(0,3,1,'l'),(1,4,1,'l'),(1,5,1,'l')],'C2H4',S=S,name='34 C2H4'))
    a=[X_('Br',90,y-90,['l','r','u']),X_('Br',90,y-146,['l','r','u'])]
    s.append(M(a,[(0,1,1,'l')],'Br2',S=S,name='34 Br2'))
    s.append(DRAW(curved(96,y-10,94,y-72,bend=-22),.3)); s.append(DRAW(curved(96,y-116,118,y-142,bend=-16),.7))
    s.append(harrow(180,220,y))
    cx=300
    a=[Cc(cx-30,y),Cc(cx+30,y),X_('Br',cx,y-66,['l','r'],fc=1,fcp='ur'),H_(cx-60,y-30),H_(cx-60,y+40),H_(cx+60,y-30),H_(cx+60,y+40)]
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(1,2,1,'l'),(0,3,1,'l'),(0,4,1,'l'),(1,5,1,'l'),(1,6,1,'l')],'C2H4Br',S=S,name='34 bromonium'))
    s.append(lab(cx-40,y+82,'브로모늄 이온',19,EQUI,weight=700))
    s.append(M([X_('Br',cx+40,y+124,['u','d','l','r'],fc=-1,fcp='ur')],[],'Br',S=S,name='34 Br-'))
    rxn(['34 C2H4','34 Br2'],['34 bromonium','34 Br-'],'S34-1')
    s.append(DRAW(curved(cx+26,y+110,cx+30,y+18,bend=-20),1.2)); s.append(DRAW(curved(cx+18,y-30,cx+4,y-50,bend=-10),1.6))
    s.append(lab(cx+40,y+164,'반대쪽 면에서 공격',19,MINUS))
    s.append(harrow(390,430,y))
    a=[Cc(490,y),Cc(550,y),X_('Br',490,y-66,['l','r','u']),X_('Br',550,y+66,['l','r','d']),H_(450,y+20),H_(510,y+44),H_(590,y-20),H_(530,y-44)]
    s.append(hlrect(490,y-66,40,36)); s.append(hlrect(550,y+66,40,36))
    s.append(M(a,[(0,1,1,'l'),(0,2,1,'l'),(1,3,1,'l'),(0,4,1,'l'),(0,5,1,'l'),(1,6,1,'l'),(1,7,1,'l')],'C2H4Br2',S=S,name='34 P'))
    rxn(['34 bromonium','34 Br-'],['34 P'],'S34-2')
    s.append(lab(520,y+130,'anti 첨가',19,INK,weight=700))
    return svg('0 0 620 350',600,'알켄의 π 전자가 브로민을 공격하여 브로모늄 이온이 생기고, 브로민화 이온이 반대쪽 면에서 공격하여 anti 첨가',s)
''')
m=func('allyl'); b=m.group(0)
b=b.replace("    s.append(lab(118,166,'+ C2',19,PLUS)); s.append(lab(546,166,'+ C4',19,PLUS))\n","    for x0 in (40,350):\n        for k in range(4): s.append(T(x0+64*k-(0 if k else 0),72,tex='\\\\mathrm{C'+str(k+1)+'}',size=19,fill=MUTED))\n")
b=b.replace("lab(330,224,'$\\\\ce{Br-}$이 C2 또는 C4를 공격',19,MINUS)","lab(330,224,'$\\\\ce{Br-}$이 $\\\\mathrm{C2}$ 또는 $\\\\mathrm{C4}$를 공격',19,MINUS)")
s=s[:m.start()]+b+s[m.end():]
repl('da','''
def da():
    s=[]; R=56
    def hexv(cx,cy,r): return [(cx+r*math.cos(math.radians(90+60*k)),cy-r*math.sin(math.radians(90+60*k))) for k in range(6)]
    # k: 0 위, 1 왼쪽 위, 2 왼쪽 아래, 3 아래, 4 오른쪽 아래, 5 오른쪽 위 (시계 반대)
    def ln(p,q,dash=None): return L(*p,*q,INK,2.6,dash=dash,extra='stroke-linecap="round"')
    def dbl(p,q,c):
        mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2; ix,iy=c[0]-mx,c[1]-my; n=math.hypot(ix,iy); ix,iy=ix/n*8,iy/n*8; t=.18
        return L(p[0]+(q[0]-p[0])*t+ix,p[1]+(q[1]-p[1])*t+iy,p[0]+(q[0]-p[0])*(1-t)+ix,p[1]+(q[1]-p[1])*(1-t)+iy,INK,2.6,extra='stroke-linecap="round"')
    def mid(p,q,dx=0,dy=0): return ((p[0]+q[0])/2+dx,(p[1]+q[1])/2+dy)
    c=(150,140); V=hexv(*c,R); sh=34
    D=[V[0],V[1],V[2],V[3]]; E=[(V[4][0]+sh,V[4][1]),(V[5][0]+sh,V[5][1])]
    s.append(ln(D[0],D[1])+ln(D[1],D[2])+ln(D[2],D[3])+dbl(D[0],D[1],c)+dbl(D[2],D[3],c))
    s.append(ln(E[0],E[1])+dbl(E[0],E[1],(c[0]+sh,c[1])))
    a1=mid(D[0],D[1]); a2=mid(D[1],D[2]); b1=mid(D[2],D[3]); e1=mid(E[0],E[1])
    s.append(DRAW(curved(*mid(D[0],D[1],-6,-6),D[0][0]+30,D[0][1]-6,bend=-22),.3))
    s.append(DRAW(curved(e1[0]+10,e1[1],E[0][0]-14,E[0][1]+18,bend=26),.7))
    s.append(DRAW(curved(*mid(D[2],D[3],-6,6),*mid(D[1],D[2],-12,0),bend=22),1.1))
    s.append(lab(112,238,'다이엔 (s-cis)',19,INK)); s.append(lab(214,238,'친다이엔체',19,INK))
    s.append(harrow(270,316,140))
    c2=(410,140); V2=hexv(*c2,R)
    for k in range(6): s.append(ln(V2[k],V2[(k+1)%6],dash='6 5' if k in (3,5) else None))
    s.append(f'<circle cx="{c2[0]}" cy="{c2[1]}" r="26" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 5"/>')
    s.append(tsb(340,66,480,214)); s.append(lab(410,238,'고리 모양 전이 상태',19,MUTED))
    s.append(harrow(520,566,140))
    c3=(650,140); V3=hexv(*c3,R)
    for k in (3,5): s.append(hlrect(*mid(V3[k],V3[(k+1)%6]),30,30))
    for k in range(6): s.append(ln(V3[k],V3[(k+1)%6]))
    s.append(dbl(V3[1],V3[2],c3))
    s.append(lab(650,238,'사이클로헥센',19,INK)); s.append(lab(650,262,'새 σ 결합 2개(형광펜)',19,MUTED))
    return svg('0 0 760 280',740,'s-cis 1,3-뷰타다이엔과 에틸렌이 고리 모양 전이 상태를 지나 사이클로헥센이 되는 딜스-알더 반응. 굽은 화살표 3개',s)
''')
open(p,'w',encoding='utf-8').write(s)
