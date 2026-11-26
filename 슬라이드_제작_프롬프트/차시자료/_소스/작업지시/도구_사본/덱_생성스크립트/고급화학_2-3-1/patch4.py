import re
s=open('gen.py',encoding='utf-8').read()
R=[
("""    s.append(T(140,300,mix='사면체 자리 (배위수 4)',size=20,weight=700))""","""    s.append(T(140,322,mix='사면체 자리 (배위수 4)',size=20,weight=700))"""),
("""    s.append(T(430,300,mix='팔면체 자리 (배위수 6)',size=20,weight=700))
    s.append(ball(170,336,13,ION['Cl'])+T(190,342,mix='큰 음이온',size=19,anchor='start')+ball(330,336,8,ION['Na'])+T(346,342,mix='작은 양이온',size=19,anchor='start'))
    return svg((580,355),540,""","""    s.append(T(430,322,mix='팔면체 자리 (배위수 6)',size=20,weight=700))
    s.append(ball(170,356,13,ION['Cl'])+T(190,362,mix='큰 음이온',size=19,anchor='start')+ball(330,356,8,ION['Na'])+T(346,362,mix='작은 양이온',size=19,anchor='start'))
    return svg((580,375),540,"""),
("""    def rows(x0,y0,shift,top_anim=False):""","""    def rows(x0,y0,shift,top_anim=False,lift=0):"""),
("""                x=x0+i*d+(shift if j==0 else 0); y=y0+j*d""","""                x=x0+i*d+(shift if j==0 else 0); y=y0+j*d-(lift if j==0 else 0)"""),
("""        if top_anim: tt=f'<g data-anim="move" data-from="{-shift},0" data-dur="1.2" data-delay=".4" data-ease="io">'+tt+'</g>'""","""        if top_anim: tt=f'<g data-anim="move" data-from="{-shift},{lift}" data-dur="1.2" data-delay=".4" data-ease="io">'+tt+'</g>'"""),
("""    s.append(rows(340,70,d,True))
    for i in range(5):
        x=340+d+i*d
        s.append(f'<g class="step" data-g="rep">'+A(x,62-12,x,44-12,'plus',2.5)+A(x,118-40+28,x,118-40+44,'plus',2.5)+'</g>')""","""    s.append(rows(340,70,d,True,14))
    for i in range(5):
        x=340+d+i*d
        s.append(f'<g class="step" data-g="rep">'+A(x,77,x,63,'plus',2.5)+A(x,80,x,94,'plus',2.5)+'</g>')"""),
("""    s.append(T(150,86,mix='탄소 전극',size=18,anchor='end',fill=MUTED))""","""    s.append(T(150,86,mix='전극',size=18,anchor='end',fill=MUTED))"""),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)
open('gen.py','w',encoding='utf-8').write(s)
t=open('tpl.html',encoding='utf-8').read()
# 24–26: 그림 열을 글 열 뒤로(DOM) 옮기고 order:-1 로 왼쪽에 둠 → 배위수 단계(cn)가 마지막
for k in ('ZNS','NACL','CSCL'):
    pat=re.compile(r'(  <div class="row">\n)(    <div class="col" style="flex:0 0 440px">\{\{'+k+r'\}\}</div>\n)(    <div class="col stack">\n(?:.*\n)*?    </div>\n)(  </div>\n</section>)')
    m=pat.search(t); assert m, k
    fig=m.group(2).replace('style="flex:0 0 440px"','style="flex:0 0 440px;order:-1"')
    t=t[:m.start()]+m.group(1)+m.group(3)+fig+m.group(4)+t[m.end():]
R2=[("<li><b>고체</b> 도가니에 $\\ce{KNO3}$ 고체를 담고 탄소 전극을 꽂아","<li><b>고체</b> 도가니에 $\\ce{KNO3}$ 고체를 담고 전극 두 개를 꽂아"),
("""      <div class="answer step">$l=3.93\\times10^{-10}\\ \\text{m}\\ (393\\ \\text{pm})$, &nbsp; 밀도 $=\\dfrac{1.296\\times10^{-21}\\ \\text{g}}{6.07\\times10^{-23}\\ \\text{cm}^3}\\approx21.4\\ \\text{g/cm}^3$</div>""","""      <div class="answer step">$l=3.93\\times10^{-10}\\ \\text{m}\\ (393\\ \\text{pm})$, &nbsp; 밀도 $=\\dfrac{1.296\\times10^{-21}\\ \\text{g}}{6.07\\times10^{-23}\\ \\text{cm}^3}\\approx21.4\\ \\text{g/cm}^3$</div>
      <p class="small step">부피를 반올림하지 않고 계산하면 $21.3\\ \\text{g/cm}^3$ — 반올림 자리에 따른 차이이다(실제 백금 약 $21.4\\ \\text{g/cm}^3$).</p>"""),
]
for a,b in R2:
    assert a in t, a[:60]; t=t.replace(a,b)
open('tpl.html','w',encoding='utf-8').write(t); print('ok')
