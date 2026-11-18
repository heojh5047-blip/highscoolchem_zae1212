# ═══ S20 에텐 σ·π
def ethene():
    s=[]; y=150; xa,xb=200,330
    # σ 골격
    for x,sg in ((xa,-1),(xb,1)):
        for ang in (120,240) if sg<0 else (60,300):
            t=math.radians(ang); hx,hy=x+math.cos(t)*104,y-math.sin(t)*104*0.62
            s.append(lob(x,y,math.degrees(math.atan2(-(hy-y),hx-x)),86,1,lab=False,W=.5))
            s.append(sph(hx,hy,26,lab=False)); s.append(dotn(hx,hy,4))
            mx,my=x+(hx-x)*.72,y+(hy-y)*.72; s.append(sigbox(mx,my,17,17))
    s.append(lob(xa,y,0,74,1,lab=False,W=.5)); s.append(lob(xb,y,180,74,1,lab=False,W=.5)); s.append(sigbox(265,y,20,18))
    # π
    g=[]
    for x in (xa,xb):
        g.append(lob(x,y,90,80,1,W=.5,opa=.22,lab=(x==xa))); g.append(lob(x,y,270,80,-1,W=.5,opa=.22,lab=(x==xa)))
    s.append(an('fade',g,dur='.9',delay='.4'))
    s.append(sigbox(265,y-58,66,22,dash='6 5')); s.append(sigbox(265,y+58,66,22,dash='6 5'))
    s.append(dotn(xa,y,5)); s.append(dotn(xb,y,5))
    s.append(T(265,y-96,mix='π 결합 (p–p)',size=20,fill=FIELD,weight=700))
    s.append(T(265,y+122,mix='σ 결합 (sp²–sp², sp²–1s)',size=20,fill=FIELD))
    s.append(T(xa,y+30,tex='\\mathrm{C}',size=19)); s.append(T(xb,y+30,tex='\\mathrm{C}',size=19))
    return svg('0 0 540 290',540,'에틸렌: 탄소 sp2 혼성 오비탈이 만든 시그마 결합 골격과, 혼성하지 않은 p 오비탈이 위아래로 겹친 파이 결합',s)
FIG['ETHENE']=ethene()

# ═══ S21 sp 오비탈 + 에타인
def sporb():
    s=[]; cx,cy=130,130; yaw,pitch=24,-18
    items=[]
    for i,d in enumerate(((1,0,0),(-1,0,0))):
        for z,sv in hybrid(cx,cy,d,100,yaw,pitch): items.append((z,f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.3+.3*i:.1f}">{sv}</g>'))
    for d in ((0,1,0),(0,0,1)):
        for z,sv in porb(cx,cy,d,70,yaw,pitch,opa=.15,W=.55,lab=False): items.append((z,sv))
    s.append(zjoin(items)); s.append(dotn(cx,cy,5))
    s.append(T(130,262,mix='선형 배열, 180°',size=19))
    return svg('0 0 260 275',220,'sp 혼성 오비탈 2개는 180도 반대 방향, 혼성하지 않은 p 오비탈 2개는 수직',s)
FIG['SPORB']=sporb()
def ethyne():
    s=[]; y=120; xa,xb=170,280; yaw,pitch=24,-18
    for x,sg in ((xa,180),(xb,0)):
        hx=x+(-1 if sg==180 else 1)*96
        s.append(lob(x,y,sg,78,1,lab=False,W=.5)); s.append(sph(hx,y,24,lab=False)); s.append(dotn(hx,y,4)); s.append(sigbox(x+(hx-x)*.72,y,16,16))
    s.append(lob(xa,y,0,62,1,lab=False,W=.5)); s.append(lob(xb,y,180,62,1,lab=False,W=.5)); s.append(sigbox(225,y,18,16))
    g=[]
    for x in (xa,xb):
        for z,sv in porb(x,y,(0,1,0),66,yaw,pitch,opa=.2,W=.5,lab=(x==xa)): g.append((z,sv))
        for z,sv in porb(x,y,(0,0,1),66,yaw,pitch,opa=.2,W=.5,lab=False): g.append((z,sv))
    s.append(an('fade',zjoin(g),dur='.9',delay='.4'))
    s.append(sigbox(225,y-52,58,18,dash='6 5')); s.append(sigbox(225,y+52,58,18,dash='6 5'))
    s.append(dotn(xa,y,5)); s.append(dotn(xb,y,5))
    s.append(T(300,y-66,mix='π 결합 2개',size=20,anchor='start',fill=FIELD,weight=700))
    s.append(T(225,y+112,mix='σ 결합 3개 (sp–sp, sp–1s)',size=20,fill=FIELD))
    return svg('0 0 450 250',450,'아세틸렌: 시그마 결합 3개와 서로 수직인 파이 결합 2개',s)
FIG['ETHYNE']=ethyne()

