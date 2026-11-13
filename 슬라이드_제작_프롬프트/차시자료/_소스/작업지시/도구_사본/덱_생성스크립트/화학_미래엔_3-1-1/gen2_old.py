# 슬라이드 10–32 (gen.py 안에서 exec)
def T(tpl, **kw):
    for k,v in kw.items(): tpl=tpl.replace('[['+k+']]', v)
    return tpl
SECA='01 · 가역 반응과 비가역 반응'; SECD='01 · 동적 평형'; SECE='01 · 화학 평형'

# ---------- 10. 염화 코발트 종이 ----------
c=''
c+='<rect x="30" y="50" width="150" height="110" rx="6" fill="#3B6FD8" stroke="#2A4F9E" stroke-width="2"/>'
c+='<g data-anim="fade" data-dur="1.2" data-delay=".6"><rect x="380" y="50" width="150" height="110" rx="6" fill="#E46A9A" stroke="#B0436F" stroke-width="2"/></g>'
c+=eqarrows(214,105,132,lab_top='물 흡수 (입김)',lab_bot='가열 (드라이어)',size=19)
c+=tex(105,196,'푸른색',20,weight=700,fill='#2A4F9E')
c+=tex(455,196,'붉은색',20,weight=700,fill='#B0436F')
c+=tex(105,224,'$\\ce{CoCl2}$',20,fill=INK)
c+=tex(455,224,'$\\ce{CoCl2*6H2O}$',20,fill=INK)
add(T('''<!-- ════════ 10. 염화 코발트 종이 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="가역 반응의 예: 염화 코발트 종이">
  <h2><span class="no">1</span>가역 반응의 예 ① 염화 코발트 종이</h2>
  <p class="f22">염화 코발트(II) 종이는 마르면 <b>푸른색</b>이고, 물을 흡수하면 <b>붉은색</b>이 된다. 붉어진 종이를 말리면 다시 푸른색이 된다.</p>
  <div class="row mt12">
    <div class="col" style="flex:0 0 560px">
      <svg class="fig" viewBox="0 0 560 240" style="width:560px" aria-label="푸른 염화 코발트 종이가 물을 흡수하면 붉게, 가열하면 다시 푸르게 변함">[[C]]</svg>
    </div>
    <div class="col">
      <p class="f22" data-q><b>Q</b> 같은 종이를 여러 번 쓸 수 있는 까닭은 무엇일까?</p>
      <div class="answer step mt12" data-g="k1">정반응과 역반응이 모두 일어나는 <b>가역 반응</b>이기 때문이다.</div>
      <p class="small mt16">쓰임: 습도 표시 카드, 제습제의 습도 표시</p>
    </div>
  </div>
  <div class="formula sm mt12 step" data-g="k1">$\\ce{CoCl2(s) + 6H2O(l) &lt;=&gt; CoCl2*6H2O(s)}$
    <div class="unit">푸른색 &nbsp;⇄&nbsp; 붉은색</div></div>
  <div class="note q mt12"><b>안전</b> 염화 코발트(II)는 몸에 해로우므로 맨손으로 만지지 않고, 쓴 종이는 지정된 폐기물 통에 버린다.</div>
</section>''', S=SECA, C=c))

# ---------- 11. 석회 동굴 ----------
add(T('''<!-- ════════ 11. 석회 동굴 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="가역 반응의 예: 석회 동굴">
  <h2><span class="no">1</span>가역 반응의 예 ② 석회 동굴</h2>
  <div class="row">
    <div class="col" style="flex:0 0 440px">
      <svg class="fig" viewBox="0 0 440 280" style="width:440px" aria-label="석회 동굴 단면, 종유석과 석순">[[C]]</svg>
    </div>
    <div class="col">
      <div class="card"><p class="f21"><b class="c-field">정반응</b> 이산화 탄소가 녹은 물이 석회암(탄산 칼슘)을 녹인다 → <b>석회 동굴</b>이 생긴다.</p></div>
      <div class="card mt12"><p class="f21"><b style="color:#7B4FC8">역반응</b> 석회암이 녹은 물이 동굴 천장에서 물과 이산화 탄소를 잃으며 다시 탄산 칼슘이 쌓인다 → <b>종유석·석순</b>이 생긴다.</p></div>
    </div>
  </div>
  <p class="f22 mt12" data-q><b>Q</b> 두 과정을 하나의 반응식으로 나타내면?</p>
  <div class="formula step mt8">$\\ce{CaCO3(s) + H2O(l) + CO2(g) &lt;=&gt; Ca(HCO3)2(aq)}$
    <div class="unit">탄산 칼슘 + 물 + 이산화 탄소 &nbsp;⇄&nbsp; 탄산수소 칼슘</div></div>
</section>''', S=SECA, C=cave(0,-34,0.846,labels=True)))

# ---------- 12. 비가역 반응 ----------
fl='<path d="M50 92 H110" stroke="#16233D" stroke-width="3"/><path d="M80 90 Q56 64 72 40 Q76 56 84 50 Q80 30 94 16 Q92 44 104 58 Q110 76 80 90 Z" fill="#F2A541" stroke="#E08A2C" stroke-width="2"/><path d="M80 88 Q70 74 78 62 Q84 72 88 66 Q92 80 80 88 Z" fill="#FFE45C"/>'
pp='<path d="M66 8 V78 A14 14 0 0 0 94 78 V8" fill="#EAF2FA" stroke="#7E8B98" stroke-width="2.5"/><path d="M67 70 V78 A13 13 0 0 0 93 78 V70 Z" fill="#FFFFFF" stroke="#B8C2CC" stroke-width="1"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#B8C2CC"/>' for x,y in [(74,74),(84,80),(88,72),(78,84),(80,67)])
bb='<path d="M66 8 V78 A14 14 0 0 0 94 78 V8" fill="#EAF2FA" stroke="#7E8B98" stroke-width="2.5"/><rect x="74" y="66" width="12" height="22" fill="#B9B9B9" stroke="#8C99A6" stroke-width="1.5"/><g data-anim="move" data-from="0,40" data-dur="1.3" data-delay=".3" data-rep="loop" data-ease="lin">'+''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#FFFFFF" stroke="#7E8B98" stroke-width="1.3"/>' for x,y in [(76,40),(86,28),(80,18)])+'</g>'
ic=lambda body,lab: f'<svg class="fig" viewBox="0 0 160 100" style="width:150px" aria-label="{lab}">{body}</svg>'
add(T('''<!-- ════════ 12. 비가역 반응 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="비가역 반응">
  <h2><span class="no">1</span>비가역 반응</h2>
  <p class="f22"><mark>한쪽 방향으로만 일어나는 반응, 즉 역반응이 거의 일어나지 않는 반응</mark>을 <b>비가역 반응</b>이라고 한다.</p>
  <table class="tight mt12 cm311-irr">
    <tr><th style="width:170px">현상</th><th style="width:300px">예</th><th>화학 반응식</th></tr>
    <tr><td>[[I1]]</td><td class="l"><b>연소</b><br><span class="small">메테인이 타며 많은 열을 낸다</span></td><td>$\\ce{CH4(g) + 2O2(g) -&gt; CO2(g) + 2H2O(l)}$</td></tr>
    <tr><td>[[I2]]</td><td class="l"><b>앙금 생성</b><br><span class="small">흰색 앙금(염화 은)이 생긴다</span></td><td>$\\ce{NaCl(aq) + AgNO3(aq) -&gt; AgCl(s) + NaNO3(aq)}$</td></tr>
    <tr><td>[[I3]]</td><td class="l"><b>기체 발생</b><br><span class="small">수소 기체가 빠져나간다</span></td><td>$\\ce{Mg(s) + 2HCl(aq) -&gt; MgCl2(aq) + H2(g)}$</td></tr>
  </table>
  <p class="f22 mt12" data-q><b>Q</b> 세 반응에서 역반응이 거의 일어나지 않는 까닭은?</p>
  <div class="answer step mt8">생성물이 반응하는 곳을 빠져나가거나(기체·앙금), 매우 안정하여 <b>역반응이 거의 일어나지 않는다.</b></div>
</section>''', S=SECA, I1=ic(fl,'불꽃'), I2=ic(pp,'흰색 앙금이 생긴 시험관'), I3=ic(bb,'마그네슘 리본에서 기포가 생기는 시험관')))

# ---------- 13. 확인하기 ----------
add(T('''<!-- ════════ 13. 확인하기 ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 가역 반응일까?" data-tpl="check">
  <h2><span class="tag q">확인하기</span>가역 반응일까, 비가역 반응일까?</h2>
  <ol class="cm311-ox">
    <li>염화 코발트 종이에 입김을 불면 붉게 변하고, 말리면 다시 푸르게 된다. <span class="blank"><span class="step">가역 반응</span></span></li>
    <li>종이가 타서 재와 연기가 된다. <span class="blank"><span class="step">비가역 반응 (연소)</span></span></li>
    <li>염화 나트륨 수용액에 질산 은 수용액을 넣으면 흰색 앙금이 생긴다. <span class="blank"><span class="step">비가역 반응 (앙금 생성)</span></span></li>
    <li>물을 끓이면 수증기가 되고, 수증기를 식히면 다시 물이 된다. <span class="blank"><span class="step">두 방향으로 일어나는 변화 (상태 변화)</span></span></li>
  </ol>
  <div class="note mt28">4번은 화학 반응이 아닌 물리 변화이지만, 가역 반응처럼 <b>두 방향</b>으로 일어난다. 다음에 이 변화로 '평형'을 알아본다.</div>
</section>'''))

# ---------- 14. 연결: 밀폐 용기 물 ----------
op='<path d="M40 40 V200 Q40 214 54 214 H186 Q200 214 200 200 V40" fill="none" stroke="#7E8B98" stroke-width="3"/>'
op+='<rect x="42" y="150" width="156" height="62" rx="10" fill="#DDEEF8"/><path d="M42 150 H198" stroke="#9FC3DD" stroke-width="2"/>'
op+='<path d="M42 110 H198" stroke="#9FC3DD" stroke-width="2" stroke-dasharray="6 5"/>'+tex(120,104,'처음 수면',18,fill=MUTED)
op+=f'<g data-anim="move" data-from="0,30" data-dur="1.6" data-delay=".3" data-rep="loop" data-ease="out">{h2o(90,60,10,7)}{h2o(150,30,10,7,th=40)}</g>'
op+=tex(120,246,'뚜껑 없는 비커: 물이 줄어든다',19,fill=INK)
cl=jar(260,40,180,174,stop=True)
cl+='<rect x="262" y="120" width="176" height="92" rx="16" fill="#DDEEF8"/><path d="M262 120 H438" stroke="#9FC3DD" stroke-width="2"/>'
cl+=tex(350,246,'마개 닫은 용기: 수면 일정',19,fill=INK)
add(T('''<!-- ════════ 14. 연결: 닫힌 용기 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="닫힌 용기 속 물은 증발을 멈췄을까?">
  <h2><span class="tag alt">연결</span>닫힌 용기 속 물은 증발을 멈춘 것일까?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 480px">
      <svg class="fig" viewBox="0 0 470 260" style="width:470px" aria-label="뚜껑 없는 비커는 물이 줄고, 마개 닫은 용기는 수면이 일정함">[[C]]</svg>
    </div>
    <div class="col">
      <p class="f22">뚜껑 없는 비커의 물은 점점 줄어들지만, 마개를 닫은 용기의 물은 며칠이 지나도 수면의 높이가 변하지 않는다.</p>
      <p class="f22 mt12" data-q><b>Q</b> 닫힌 용기에서 물이 줄지 않는 것은 물 분자가 더 이상 증발하지 않기 때문일까?</p>
      <div class="card mt8"><p class="f21"><b>(가)</b> 증발이 멈추었다.</p></div>
      <div class="card mt8"><p class="f21"><b>(나)</b> 증발은 계속되지만, 같은 수만큼 응축된다.</p></div>
    </div>
  </div>
  <div class="answer step mt12"><b>(나)</b> — 다음 장에서 입자 수준으로 확인해 보자.</div>
</section>''', S=SECD, C=op+cl))

# ---------- 15. 상평형 ----------
def vap_card(nv,down,seed):
    o=jar(20,40,180,170)
    o+='<rect x="22" y="150" width="176" height="58" rx="16" fill="#DDEEF8"/><path d="M22 150 H198" stroke="#9FC3DD" stroke-width="2"/>'
    for (x,y,th) in [(45,170,80),(78,190,120),(110,168,60),(140,192,100),(172,172,140),(60,196,30),(160,197,10)]:
        o+=h2o(x,y,10,7,th)
    pts=place(nv,(45,70,178,128),26,seed)
    mv=''.join(h2o(x,y,10,7,(i*73)%360) for i,(x,y) in enumerate(pts))
    o+=f'<g data-anim="move" data-from="0,26" data-dur="1.2" data-delay=".4" data-ease="out">{mv}</g>'
    o+=arw(228,170,228,110,'field',3.5)
    if down: o+=arw(266,110,266,110+down,'bfield',3.5)
    o+=tex(222,234,'증발',23,fill=FIELD,weight=700)
    o+=tex(274,234,'응축',23,fill=BFIELD,weight=700)
    return o
cards=[('① 처음','증발 속도 &gt; 응축 속도',vap_card(1,6,3)),('② 시간이 지나면','수증기가 늘어 응축 속도가 커진다',vap_card(4,34,5)),('③ 평형','증발 속도 = 응축 속도',vap_card(6,60,8))]
st=''.join(f'<div class="stage"><h3>{a}</h3><svg viewBox="0 0 300 244" style="height:200px" aria-label="밀폐 용기 속 물과 수증기 분자, 증발과 응축 화살표">{c}</svg><p class="key">{b}</p></div>' for a,b,c in cards)
add(T('''<!-- ════════ 15. 상평형 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="동적 평형: 상평형">
  <h2><span class="no">2</span>동적 평형 — 물과 수증기</h2>
  <div class="stages">[[C]]</div>
  <p class="small mt8">화살표 길이 = 속도(1초 동안 증발하거나 응축하는 분자 수). 물 분자 모형: $\\mathrm{O}$ 빨간 공, $\\mathrm{H}$ 흰 공</p>
  <p class="f22 mt8 step" data-g="d1"><mark>정반응 속도와 역반응 속도가 같아서 겉으로는 변화가 없어 보이지만, 실제로는 두 반응이 계속 일어나는 상태</mark>를 <b>동적 평형</b>이라고 한다.</p>
  <p class="f22 mt8 step" data-g="d2">물과 수증기 사이의 동적 평형을 <b>상평형</b>이라고 한다: $\\ce{H2O(l) &lt;=&gt; H2O(g)}$</p>
</section>''', S=SECD, C=st))

# ---------- 16. 용해 평형 ----------
def sol_card(nd,pile,up,down,seed):
    o='<path d="M30 30 V196 Q30 212 46 212 H194 Q210 212 210 196 V30" fill="none" stroke="#7E8B98" stroke-width="3"/>'
    o+='<rect x="32" y="66" width="176" height="144" rx="14" fill="#DDEEF8" fill-opacity=".7"/><path d="M32 66 H208" stroke="#9FC3DD" stroke-width="2"/>'
    for i,(x,y) in enumerate(pile):
        o+=f'<rect x="{x}" y="{y}" width="16" height="14" rx="2" fill="#F3E9C6" stroke="#B59A4A" stroke-width="1.5"/>'
    pts=place(nd,(48,84,194,168),28,seed)
    o+=f'<g data-anim="move" data-from="0,30" data-dur="1.2" data-delay=".4" data-ease="out">'+''.join(hexagon(x,y) for x,y in pts)+'</g>'
    o+=arw(236,178,236,178-up,'field',3.5)
    o+=arw(272,178-down,272,178,'bfield',3.5)
    o+=tex(232,234,'용해',23,fill=FIELD,weight=700); o+=tex(280,234,'석출',23,fill=BFIELD,weight=700)
    return o
pileA=[(80,194),(96,194),(112,194),(128,194),(144,194),(88,180),(104,180),(120,180),(136,180),(96,166),(112,166),(128,166)]
pileB=[(88,194),(104,194),(120,194),(136,194),(96,180),(112,180),(128,180)]
cards=[('① 녹는 중','용해 속도 &gt; 석출 속도',sol_card(4,pileA,60,18,11)),('② 포화 용액','용해 속도 = 석출 속도',sol_card(9,pileB,50,50,12))]
st=''.join(f'<div class="stage"><h3>{a}</h3><svg viewBox="0 0 300 244" style="height:190px" aria-label="설탕 결정과 녹은 설탕 분자, 용해와 석출 화살표">{c}</svg><p class="key">{b}</p></div>' for a,b,c in cards)
add(T('''<!-- ════════ 16. 용해 평형 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="동적 평형: 용해 평형">
  <h2><span class="no">2</span>동적 평형 — 설탕의 용해 평형</h2>
  <div class="row">
    <div class="col" style="flex:0 0 640px"><div class="stages c2">[[C]]</div>
      <p class="small mt8">네모 = 설탕 결정, 육각형 = 녹은 설탕 분자, 화살표 길이 = 속도</p></div>
    <div class="col">
      <p class="f22">설탕을 물에 계속 넣으면 어느 순간 더 녹지 않는 것처럼 보인다(포화 용액).</p>
      <p class="f22 mt12 step" data-g="s1">용질이 녹는 속도와 석출되는 속도가 같은 동적 평형을 <b>용해 평형</b>이라고 한다.</p>
      <div class="formula sm mt8 step" data-g="s1">$\\ce{C12H22O11(s) &lt;=&gt; C12H22O11(aq)}$</div>
    </div>
  </div>
  <div class="note puzzle mt12 step" data-g="s2"><b>증거</b> 포화 용액에 모서리가 깨진 설탕 결정을 넣어 두면, 질량은 변하지 않지만 결정의 <b>모양이 바뀐다</b>. → 녹는 것과 석출되는 것이 계속 일어난다.</div>
</section>''', S=SECD, C=st))

# ---------- 17. 화학 평형 NO2 ----------
def no2_card(na,nb,op,fw,rv,seed,anim=False):
    o=jar(30,30,240,170,tint=NO2C,op=op)
    pts=place(na+nb,(62,60,238,178),44,seed)
    mv=''
    for i,(x,y) in enumerate(pts):
        mv+= no2(x,y,12,(i*97)%360) if i<na else n2o4(x,y,12,(i*53)%180)
    if anim: o+=f'<g data-anim="move" data-from="3,-3" data-rep="swing" data-dur=".9">{mv}</g>'
    else: o+=mv
    o+=tex(14,234,'정반응',23,anchor='start',fill=FIELD,weight=700)
    if fw: o+=arw(96,226,96+fw,226,'field',3.5)
    else: o+=tex(100,234,'거의 없음',22,anchor='start',fill=MUTED)
    o+=tex(14,264,'역반응',23,anchor='start',fill=BFIELD,weight=700)
    if rv: o+=arw(96+rv,256,96,256,'bfield',3.5)
    else: o+=tex(100,264,'거의 없음',22,anchor='start',fill=MUTED)
    return o
cards=[('① 처음','적갈색이 진하다 · $\\ce{NO2}$ 12개',no2_card(12,0,.5,150,0,21)),
       ('② 시간이 지나면','색이 옅어진다 · $\\ce{NO2}$ 8개, $\\ce{N2O4}$ 2개',no2_card(8,2,.34,100,40,22)),
       ('③ 평형','색이 일정하다 · $\\ce{NO2}$ 6개, $\\ce{N2O4}$ 3개',no2_card(6,3,.26,70,70,24,anim=True))]
st=''.join(f'<div class="stage"><h3>{a}</h3><svg viewBox="0 0 300 272" style="height:212px" aria-label="밀폐 용기 속 이산화 질소와 사산화 이질소 분자, 정반응과 역반응의 빠르기">{c}</svg><p class="key">{b}</p></div>' for a,b,c in cards)
add(T('''<!-- ════════ 17. 화학 평형 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="화학 평형: 2NO₂ ⇌ N₂O₄">
  <h2><span class="no">3</span>화학 평형 — $\\ce{2NO2(g) &lt;=&gt; N2O4(g)}$</h2>
  <p class="f22">적갈색 이산화 질소($\\ce{NO2}$)를 밀폐 용기에 넣고 두면, 색이 점점 옅어지다가 어느 순간부터 <b>더 이상 변하지 않는다</b>.</p>
  <div class="stages mt8">[[C]]</div>
  <p class="small mt8">$\\mathrm{N}$ 원자 수: $12=8+2\\times2=6+3\\times2$ (보존) · 모형: $\\mathrm{N}$ 파란 공, $\\mathrm{O}$ 빨간 공 · 화살표 길이 = 반응 속도</p>
  <div class="answer step mt8">색이 변하지 않아도 $\\ce{NO2}$ 두 개가 결합하는 반응과 $\\ce{N2O4}$가 분해되는 반응은 <b>같은 속도로 계속</b> 일어난다.</div>
</section>''', S=SECE, C=st))

# ---------- 그래프 ----------
def kin(n=80,tmax=3.2):
    m=0; dt=0.0005; t=0; out=[(0,1,0)]; k=1
    steps=int(tmax/dt); every=steps//n
    for i in range(1,steps+1):
        nn=1-2*m; m+=dt*(nn*nn-m); t+=dt
        if i%every==0: out.append((t,1-2*m,m))
    return out
KIN=kin()
def graph(kind,W=560,H=230,t1lab=True,anim=True,labels=True):
    X0,Y0,X1,Y1=64,192,W-24,20; tmax=3.2
    X=lambda t:X0+(X1-X0)*t/tmax
    o=''
    t1=1.45
    o+=f'<rect x="{f(X(t1))}" y="{Y1}" width="{f(X1-X(t1))}" height="{Y0-Y1}" fill="#FFE45C" fill-opacity=".25"/>'
    o+=f'<path d="M{f(X(t1))} {Y1} V{Y0}" stroke="#5B6B7F" stroke-width="2" stroke-dasharray="6 5"/>'
    o+=arw(X0,Y0,X1+14,Y0,'ink',2)+arw(X0,Y0,X0,Y1-10,'ink',2)
    o+=tex(X(t1),Y0+24,'$t_1$',20,mix=True)
    o+=tex(X1+6,Y0+26,'시간',19,anchor='end',fill=INK)
    o+=tex((X(t1)+X1)/2,Y1+22,'평형',19,fill='#8A6D00',weight=700)
    if kind=='c':
        o+=tex(X0+12,Y1+4,'농도',19,anchor='start',fill=INK)
        sc=lambda v:Y0-v*150
        pa=path([(X(t),sc(a)) for t,a,b in KIN]); pb=path([(X(t),sc(b)) for t,a,b in KIN])
        A=' data-anim="draw" data-dur="1.6" data-delay=".3"' if anim else ''
        o+=f'<path d="{pa}" fill="none" stroke="{NO2C}" stroke-width="4"{A}/>'
        o+=f'<path d="{pb}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-dasharray="12 6"{A}/>'
        if labels:
            o+=tex(X1-4,sc(0.5)-10,'$[\\ce{NO2}]$',20,anchor='end',fill=NO2C)
            o+=tex(X1-4,sc(0.25)+26,'$[\\ce{N2O4}]$',20,anchor='end',fill=INK)
    else:
        o+=tex(X0+12,Y1+4,'반응 속도',19,anchor='start',fill=INK)
        sc=lambda v:Y0-v*150
        pa=path([(X(t),sc(a*a)) for t,a,b in KIN]); pb=path([(X(t),sc(b)) for t,a,b in KIN])
        A=' data-anim="draw" data-dur="1.6" data-delay=".3"' if anim else ''
        o+=f'<path d="{pa}" fill="none" stroke="{FIELD}" stroke-width="4"{A}/>'
        o+=f'<path d="{pb}" fill="none" stroke="{BFIELD}" stroke-width="4" stroke-dasharray="12 6"{A}/>'
        o+=tex(X(0.35)+8,sc(0.62),'정반응 속도',19,anchor='start',fill=FIELD,weight=700)
        o+=tex(X(0.5)+6,sc(0.10)+30,'역반응 속도',19,anchor='start',fill=BFIELD,weight=700)
    return o
add(T('''<!-- ════════ 18. 그래프 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="농도와 반응 속도 그래프">
  <h2><span class="no">3</span>평형에 도달하는 과정을 그래프로</h2>
  <div class="row">
    <div class="col" style="flex:0 0 580px">
      <svg class="fig" viewBox="0 0 560 230" style="width:560px" aria-label="이산화 질소 농도는 줄고 사산화 이질소 농도는 늘다가 t1 이후 일정한 농도-시간 그래프">[[G1]]</svg>
      <svg class="fig mt8" viewBox="0 0 560 230" style="width:560px" aria-label="정반응 속도는 줄고 역반응 속도는 늘어 t1에서 같아지는 반응 속도-시간 그래프">[[G2]]</svg>
    </div>
    <div class="col">
      <p class="f21">밀폐 용기에 $\\ce{NO2(g)}$만 넣었을 때 <span class="small">(눈금 없는 정성 그래프)</span></p>
      <p class="f21 mt12"><b>Q</b> ① $t_1$ 이후 두 물질의 농도는?</p>
      <p class="f21 step cm311-a">→ 각각 <span class="ans">일정</span>하다. 두 농도가 같지는 않다.</p>
      <p class="f21 mt12"><b>Q</b> ② $t_1$ 이후 정반응 속도와 역반응 속도는?</p>
      <p class="f21 step cm311-a">→ <span class="ans">같다</span>.</p>
      <p class="f21 mt12"><b>Q</b> ③ $t_1$ 이후 반응은 멈추었을까?</p>
      <p class="f21 step cm311-a">→ 아니다. 두 반응이 같은 속도로 <span class="ans">계속</span> 일어난다.</p>
    </div>
  </div>
</section>''', S=SECE, G1=graph('c'), G2=graph('r')))

# ---------- 19. 화학 평형 상태의 특징 ----------
add(T('''<!-- ════════ 19. 특징 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="화학 평형 상태의 특징">
  <h2><span class="no">3</span>화학 평형 상태의 특징</h2>
  <p class="f22">가역 반응에서 <mark>정반응 속도와 역반응 속도가 같아 반응물과 생성물의 농도가 일정하게 유지되는 상태</mark>를 <b>화학 평형 상태</b>라고 한다.</p>
  <table class="tight mt16 cm311-feat">
    <tr><th style="width:250px">보는 수준</th><th>평형 상태의 특징</th></tr>
    <tr><td><b>거시적</b><br><span class="small">눈으로 관찰</span></td><td class="l">· 색, 농도 같은 성질이 일정하다 → 겉으로는 반응이 멈춘 것처럼 보인다.<br><span class="step" data-g="f1">· 닫힌 용기에서 반응물 쪽에서 출발해도, 생성물 쪽에서 출발해도 평형에 도달한다.</span></td></tr>
    <tr><td><b>미시적</b><br><span class="small">입자 수준</span></td><td class="l"><span class="step" data-g="f2">· 정반응과 역반응이 <b>같은 속도로 계속</b> 일어난다 → <b>동적 평형</b><br>· 반응물과 생성물이 함께 존재한다.</span></td></tr>
  </table>
  <div class="note q mt16 step" data-g="f3"><b>주의</b> 평형 상태에서 반응물과 생성물의 농도는 <b>일정</b>하지만 <b>같은</b> 것은 아니다. 또 화학 평형은 물질이 드나들지 않는 <b>닫힌 계</b>에서 이루어진다.</div>
</section>''', S=SECE))

# ---------- 20. 확인하기: 오개념 ----------
add(T('''<!-- ════════ 20. 확인하기 오개념 ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 친구들의 생각">
  <h2><span class="tag q">확인하기</span>평형에 대한 친구들의 생각</h2>
  <p class="f22" data-q><b>Q</b> 밀폐 용기 속 $\\ce{2NO2(g) &lt;=&gt; N2O4(g)}$ 반응이 평형에 도달했다. 옳게 말한 친구는 누구일까?</p>
  <div class="row mt12">
    <div class="col"><div class="card cm311-bub"><h3>학생 A</h3><p class="f21">"평형에 도달하면 반응이 멈춰."</p>
      <p class="f21 step c-plus" data-g="m2">× 반응은 계속된다. 두 속도가 같아 농도가 변하지 않을 뿐이다.</p></div></div>
    <div class="col"><div class="card cm311-bub"><h3>학생 B</h3><p class="f21">"평형에서는 반응물과 생성물의 농도가 같아져."</p>
      <p class="f21 step c-plus" data-g="m2">× 농도는 일정할 뿐 같지 않다.</p></div></div>
    <div class="col"><div class="card cm311-bub"><h3>학생 C</h3><p class="f21">"평형에서도 정반응과 역반응이 같은 속도로 계속 일어나."</p>
      <p class="f21 step cm311-a" data-g="m2">○ 동적 평형이다.</p></div></div>
  </div>
  <div class="answer step mt16" data-g="m1">옳게 말한 친구: <b>학생 C</b></div>
</section>'''))

# ---------- 21. 실험실 평형 도달 ----------
add(T('''<!-- ════════ 21. 실험실: 평형 도달 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="실험실: 평형에 도달하기">
  <h2><span class="tag">실험실</span>평형에 도달하기 — $\\ce{2NO2 &lt;=&gt; N2O4}$</h2>
  <div class="lab" data-lab="cm311eq">
    <div class="lab-ctl" style="flex:0 0 430px">
      <div class="ctl"><div class="lbl"><span>처음 $\\ce{NO2}$ 분자 수</span><output data-o="a0"></output></div><input type="range" min="0" max="40" step="4" value="40" data-i="a0" aria-label="처음 이산화 질소 분자 수"></div>
      <div class="ctl"><div class="lbl"><span>처음 $\\ce{N2O4}$ 분자 수</span><output data-o="b0"></output></div><input type="range" min="0" max="20" step="2" value="0" data-i="b0" aria-label="처음 사산화 이질소 분자 수"></div>
      <div class="cm311-seg"><button class="btn cm311-act" data-act="run">시작</button><button class="btn" data-act="reset">처음부터</button><button class="btn" data-act="rec">측정 기록</button></div>
      <table class="readout cm311-read">
        <tr><th>분자 수 $\\ce{NO2}$ · $\\ce{N2O4}$</th><td><output data-o="cnt"></output></td></tr>
        <tr><th>누적 반응 횟수 정 · 역</th><td><output data-o="tot"></output></td></tr>
      </table>
      <output class="kind cm311-msg" data-o="msg"></output>
      <table class="tight cm311-log mt8"><thead><tr><th>처음 $\\ce{NO2}$·$\\ce{N2O4}$</th><th>평형 $\\ce{NO2}$·$\\ce{N2O4}$</th><th>시간</th></tr></thead><tbody data-o="log"></tbody></table>
    </div>
    <div class="col" style="flex:0 0 640px">
      <div class="lab-fig" style="width:640px;height:420px">
        <svg viewBox="0 0 640 420" width="640" height="420" aria-label="밀폐 상자 속 분자 운동과 분자 수, 반응 속도 그래프"></svg>
        <div class="ov" data-ov="t1" style="font-size:19px">분자 수</div>
        <div class="ov" data-ov="t2" style="font-size:19px">반응 속도 (회/s)</div>
        <div class="ov" data-ov="la" style="font-size:19px;color:#B5562A">$\\ce{NO2}$</div>
        <div class="ov" data-ov="lb" style="font-size:19px">$\\ce{N2O4}$</div>
        <div class="ov" data-ov="lf" style="font-size:19px;color:#2E9E6A">정반응</div>
        <div class="ov" data-ov="lr" style="font-size:19px;color:#7B4FC8">역반응</div>
        <div class="ov" data-ov="tx" style="font-size:18px;color:#5B6B7F">시간 (s)</div>
        <div class="ov" data-ov="tx2" style="font-size:18px;color:#5B6B7F">시간 (s)</div>
        <div class="ov" data-ov="leg" style="font-size:18px;color:#5B6B7F">● N 파랑 &nbsp;● O 빨강 · 상자 색 = $\\ce{NO2}$의 적갈색</div>
      </div>
    </div>
  </div>
</section>''', S=SECE))

# ---------- 탐구 ----------
def cyl(x,vol,lab,y0=40,h=170,w=46,tubeL=None):
    o=f'<rect x="{x-w/2-10}" y="{y0+h}" width="{w+20}" height="8" rx="3" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/>'
    wh=h*vol/100
    if vol>0: o+=f'<rect x="{x-w/2+2}" y="{f(y0+h-wh)}" width="{w-4}" height="{f(wh)}" fill="#BFDDF2"/>'
    o+=f'<path d="M{x-w/2} {y0} V{y0+h} H{x+w/2} V{y0}" fill="none" stroke="#7E8B98" stroke-width="2.5"/>'
    for k in range(1,10):
        yy=y0+h-h*k/10; o+=f'<path d="M{x+w/2-10} {f(yy)} H{x+w/2}" stroke="#5B6B7F" stroke-width="1.2"/>'
    o+=tex(x,y0+h+34,lab,24,weight=700,fill=INK)
    return o
def ptube(x,y1,y2,w,cl='#7E8B98'):
    return f'<rect x="{x-w/2}" y="{y1}" width="{w}" height="{y2-y1}" fill="#FFFFFF" fill-opacity=".5" stroke="{cl}" stroke-width="2"/>'
p1=cyl(80,50,'A',y0=50,h=160)+cyl(200,0,'B',y0=50,h=160)+tex(80,38,'50 mL',24,fill=MUTED)
p2=cyl(80,50,'A',y0=50,h=160)+cyl(200,0,'B',y0=50,h=160)+ptube(80,36,208,12)+ptube(200,36,208,7)+tex(80,28,'굵은 관',24,fill=MUTED)+tex(200,28,'가는 관',24,fill=MUTED)
p3=cyl(80,42,'A',y0=50,h=160)+cyl(200,8,'B',y0=50,h=160)
p3+=f'<g data-anim="move" data-from="-60,0" data-dur="1.2" data-delay=".4" data-ease="io">'+ptube(140,44,120,12)+arw(152,70,182,70,'field',3)+'</g>'
p3+=arw(176,150,104,150,'bfield',3)
p3+=tex(140,32,'A → B',24,fill=FIELD,weight=700)+tex(140,180,'B → A',24,fill=BFIELD,weight=700)
g4='<path d="M40 30 V200 H260" fill="none" stroke="#16233D" stroke-width="2"/>'
pts=[(0,50,0),(2,35.7,14.3),(4,27,23),(6,21.7,28.3),(8,18.4,31.6),(10,16.4,33.6),(15,14.2,35.8),(20,13.5,36.5)]
GX=lambda n:44+n*10.5; GY=lambda v:200-v*3.2
g4+=f'<path d="{path([(GX(n),GY(a)) for n,a,b in pts])}" fill="none" stroke="#16233D" stroke-width="3"/>'
g4+=f'<path d="{path([(GX(n),GY(b)) for n,a,b in pts])}" fill="none" stroke="#0E7490" stroke-width="3" stroke-dasharray="9 5"/>'
g4+=tex(260,232,'횟수',24,anchor='end',fill=MUTED)+tex(50,28,'부피',24,anchor='start',fill=MUTED)
st=''.join(f'<div class="stage"><h3>{a}</h3><svg viewBox="0 0 280 250" style="height:180px" aria-label="{c2}">{c}</svg><p>{b}</p></div>' for a,b,c,c2 in [
 ('①','눈금실린더 A에 물 50 mL를 넣고, B는 비워 둔다.',p1,'물 50 mL가 든 눈금실린더 A와 빈 B'),
 ('②','굵은 관은 A에, 가는 관은 B에 바닥까지 넣고 윗구멍을 손가락으로 막아 동시에 들어 올린다.',p2,'A에 굵은 관, B에 가는 관을 넣음'),
 ('③','굵은 관의 물은 B로, 가는 관의 물은 A로 동시에 옮긴다.',p3,'굵은 관의 물은 B로, 가는 관의 물은 A로 옮김'),
 ('④','②–③을 되풀이하며 A, B의 부피를 기록하고 그래프로 나타낸다.',g4,'옮긴 횟수에 따른 부피 그래프')])

add(T('''<!-- ════════ 22. 탐구 목표 ════════ -->
<section class="slide" data-sec="01 · 탐구" data-title="탐구: 동적 평형 모형 (목표·준비)">
  <h2><span class="tag">탐구</span>동적 평형 모형 만들기</h2>
  <div class="row">
    <div class="col">
      <h3>목표</h3>
      <p class="f22">물 옮기기 모형으로, 겉보기 변화가 없는 상태에서도 두 방향의 이동이 계속됨을 확인하고 동적 평형을 설명할 수 있다.</p>
      <h3 class="mt16">준비물</h3>
      <p class="f21">100 mL 눈금실린더 2개(A, B), 안지름이 다른 유리관 2개(굵은 관, 가는 관), 물, 비커, 활동지</p>
    </div>
    <div class="col" style="flex:0 0 520px">
      <table class="tight cm311-var">
        <tr><th>조작 변인</th><td class="l">유리관의 굵기, 처음 물을 넣는 쪽</td></tr>
        <tr><th>종속 변인</th><td class="l">두 눈금실린더 속 물의 부피</td></tr>
        <tr><th>통제 변인</th><td class="l">전체 물의 양(50 mL), 관을 바닥까지 넣는 방법</td></tr>
      </table>
      <div class="note q mt16"><b>안전</b> 보안경을 쓰고, 끝을 불에 다듬은 유리관을 쓴다. 깨진 유리는 깨진 유리 전용 통에 버린다. 쏟은 물은 바로 닦는다. 물만 쓰므로 실험 뒤 물은 개수대에 버린다.</div>
    </div>
  </div>
</section>'''))
add(T('''<!-- ════════ 23. 탐구 과정 ════════ -->
<section class="slide" data-sec="01 · 탐구" data-title="탐구: 과정">
  <h2><span class="tag">탐구</span>과정</h2>
  <div class="cm311-s4">[[C]]</div>
  <p class="small mt12">관 속에 담기는 물의 양은 눈금실린더 속 물의 높이에 비례한다. 물이 많은 쪽에서 더 많이 퍼 올려진다.</p>
</section>''', C=st))

add('''<!-- ════════ 24. 실험실: 물 옮기기 ════════ -->
<section class="slide" data-sec="01 · 탐구" data-title="실험실: 물 옮기기 모형">
  <h2><span class="tag">탐구</span>물 옮기기 모형 실험실</h2>
  <div class="lab" data-lab="cm311water">
    <div class="lab-ctl" style="flex:0 0 440px">
      <div class="ctl"><div class="lbl"><span>A에 넣는 관 지름</span><output data-o="da"></output></div><input type="range" min="4" max="12" step="1" value="10" data-i="da" aria-label="A에 넣는 관 지름"></div>
      <div class="ctl"><div class="lbl"><span>B에 넣는 관 지름</span><output data-o="db"></output></div><input type="range" min="4" max="12" step="1" value="6" data-i="db" aria-label="B에 넣는 관 지름"></div>
      <div class="cm311-seg"><span class="small">처음 물 50 mL를</span><button class="btn on" data-st="A">A에</button><button class="btn" data-st="B">B에</button></div>
      <div class="cm311-seg"><button class="btn cm311-act" data-act="one">1회 옮기기</button><button class="btn cm311-act" data-act="five">5회 옮기기</button><button class="btn" data-act="reset">처음부터</button></div>
      <table class="readout cm311-read">
        <tr><th>옮긴 횟수</th><td><output data-o="n"></output></td></tr>
        <tr><th>부피 A · B</th><td><output data-o="v"></output></td></tr>
        <tr class="hl"><th>이번 회 A→B · B→A</th><td><output data-o="mv"></output></td></tr>
      </table>
      <output class="kind cm311-msg" data-o="msg"></output>
    </div>
    <div class="col" style="flex:0 0 630px">
      <div class="lab-fig" style="width:630px;height:300px">
        <svg viewBox="0 0 630 300" width="630" height="300" aria-label="두 눈금실린더의 물 높이와 옮긴 횟수에 따른 부피 그래프"></svg>
        <div class="ov" data-ov="ya" style="font-size:19px">부피 (mL)</div>
        <div class="ov" data-ov="xa" style="font-size:18px;color:#5B6B7F">옮긴 횟수</div>
        <div class="ov" data-ov="la" style="font-size:19px">A</div>
        <div class="ov" data-ov="lb" style="font-size:19px;color:#0E7490">B</div>
        <div class="ov" data-ov="ca" style="font-size:20px;font-weight:700">A</div>
        <div class="ov" data-ov="cb" style="font-size:20px;font-weight:700">B</div>
      </div>
      <table class="tight cm311-log mt8"><thead><tr><th>횟수</th><th>A (mL)</th><th>B (mL)</th><th>A→B (mL)</th><th>B→A (mL)</th></tr></thead><tbody data-o="log"></tbody></table>
    </div>
  </div>
</section>''')

# 25 결과
g=''
GX=lambda n:70+n*22; GY=lambda v:210-v*3.6
g+=arw(70,210,530,210,'ink',2)+arw(70,210,70,14,'ink',2)
for v in (10,20,30,40,50):
    g+=f'<path d="M66 {f(GY(v))} H74" stroke="#16233D" stroke-width="2"/>'+tex(60,GY(v)+6,str(v),18,anchor='end',fill=INK)
for n in (0,5,10,15,20):
    g+=f'<path d="M{GX(n)} 206 V214" stroke="#16233D" stroke-width="2"/>'+tex(GX(n),234,str(n),18,fill=INK)
g+=tex(530,262,'옮긴 횟수',19,anchor='end',fill=INK)+tex(80,22,'부피 [mL]',19,anchor='start',fill=INK)
sa=''.join(f'<circle cx="{f(GX(n))}" cy="{f(GY(a))}" r="5" fill="#16233D"/>' for n,a,b in pts)
sb=''.join(f'<rect x="{f(GX(n)-5)}" y="{f(GY(b)-5)}" width="10" height="10" fill="#0E7490"/>' for n,a,b in pts)
g+=f'<g class="step" data-g="r1"><path d="{path([(GX(n),GY(a)) for n,a,b in pts])}" fill="none" stroke="#16233D" stroke-width="3"/>{sa}<path d="{path([(GX(n),GY(b)) for n,a,b in pts])}" fill="none" stroke="#0E7490" stroke-width="3" stroke-dasharray="9 5"/>{sb}'
g+=tex(GX(20)+10,GY(13.5)+6,'A',20,anchor='start',fill=INK,weight=700)+tex(GX(20)+10,GY(36.5)+6,'B',20,anchor='start',fill='#0E7490',weight=700)+'</g>'
rows_n=''.join(f'<td>{n}</td>' for n,a,b in pts)
rows_a=''.join(f'<td><span class="blank"><span class="step" data-g="r0">{a:.1f}</span></span></td>' if n else f'<td>{a:.1f}</td>' for n,a,b in pts)
rows_b=''.join(f'<td><span class="blank"><span class="step" data-g="r0">{b:.1f}</span></span></td>' if n else f'<td>{b:.1f}</td>' for n,a,b in pts)
add(T('''<!-- ════════ 25. 결과 ════════ -->
<section class="slide" data-sec="01 · 탐구" data-title="탐구: 결과 및 정리">
  <h2><span class="tag">탐구</span>결과 및 정리</h2>
  <p class="f21">예: 굵은 관 지름 10 mm, 가는 관 6 mm, 눈금실린더 안지름 25 mm (실험실 값으로 채워도 된다)</p>
  <table class="tight mt8 cm311-res">
    <tr><th>옮긴 횟수</th>[[N]]</tr>
    <tr><th>A의 부피(mL)</th>[[A]]</tr>
    <tr><th>B의 부피(mL)</th>[[B]]</tr>
  </table>
  <div class="row mt12">
    <div class="col" style="flex:0 0 560px"><svg class="fig" viewBox="0 0 560 270" style="width:540px" aria-label="옮긴 횟수에 따라 A는 줄고 B는 늘다가 일정해지는 부피 그래프">[[G]]</svg></div>
    <div class="col">
      <p class="f21"><b>Q</b> ① 15회 이후 A, B의 부피는 어떻게 되는가?</p>
      <p class="f21 step cm311-a" data-g="r2">→ 거의 <span class="ans">일정</span>하다.</p>
      <p class="f21 mt12"><b>Q</b> ② 그때도 물을 옮기고 있는가?</p>
      <p class="f21 step cm311-a" data-g="r3">→ 그렇다. A → B로 옮기는 양과 B → A로 옮기는 양이 <b>같아졌다</b>(각각 약 2.1 mL).</p>
    </div>
  </div>
</section>''', N=rows_n, A=rows_a, B=rows_b, G=g))

add('''<!-- ════════ 26. 결론 ════════ -->
<section class="slide" data-sec="01 · 탐구" data-title="탐구: 결론 도출">
  <h2><span class="tag">탐구</span>결론 도출</h2>
  <div class="row">
    <div class="col" style="flex:0 0 470px">
      <table class="tight cm311-mapt">
        <tr><th>모형</th><th>화학 반응</th></tr>
        <tr><td>A의 물</td><td><span class="blank"><span class="step" data-g="z1">반응물</span></span></td></tr>
        <tr><td>B의 물</td><td><span class="blank"><span class="step" data-g="z1">생성물</span></span></td></tr>
        <tr><td>A → B 옮기기</td><td><span class="blank"><span class="step" data-g="z1">정반응</span></span></td></tr>
        <tr><td>B → A 옮기기</td><td><span class="blank"><span class="step" data-g="z1">역반응</span></span></td></tr>
        <tr><td>한 번에 옮기는 양</td><td><span class="blank"><span class="step" data-g="z1">반응 속도</span></span></td></tr>
        <tr><td>부피가 일정한 상태</td><td><span class="blank"><span class="step" data-g="z1">화학 평형 상태</span></span></td></tr>
      </table>
    </div>
    <div class="col">
      <p class="f21"><b>Q</b> 처음 물을 B에 넣고 시작하면 어떻게 될까?</p>
      <p class="f21 step cm311-a" data-g="z2">→ 같은 부피(A 약 13 mL, B 약 37 mL)에 도달한다. 역반응 쪽에서 출발해도 같은 평형이다.</p>
      <p class="f21 mt12"><b>Q</b> 이 모형의 한계는 무엇일까?</p>
      <p class="f21 step cm311-a" data-g="z3">→ 실제 입자는 한 번에 '퍼서' 옮겨지지 않고, 끊임없이 무작위로 충돌하며 반응한다. 또 두 부피가 <b>같아지는 것이 평형은 아니다</b>.</p>
      <div class="card mt12"><h3>평가 기준 예시</h3>
        <p class="f21"><b>상</b> 부피가 일정한 것과 옮기기가 계속되는 것을 구분해 동적 평형으로 설명한다.</p>
        <p class="f21"><b>중</b> 부피 변화를 표와 그래프로 정리한다. <b>하</b> 기록만 한다.</p></div>
    </div>
  </div>
</section>''')

# ---------- 27–29 확인 문제 ----------
add('''<!-- ════════ 27. 확인 문제 01 ════════ -->
<section class="slide" data-sec="01 · 확인 문제" data-title="확인 문제 01">
  <h2><span class="tag q">확인 문제 01</span>가역 반응 고르기</h2>
  <p class="f22">다음은 몇 가지 현상이다. 가역 반응과 관련된 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?</p>
  <div class="row mt8">
    <div class="col">
      <div class="bogi"><p>ㄱ. 황산 구리(II) 오수화물을 가열하면 흰색이 되고, 여기에 물을 떨어뜨리면 다시 푸른색이 된다.</p><p>ㄴ. 메테인이 연소하여 이산화 탄소와 물이 생성된다.</p><p>ㄷ. 석회 동굴 천장에 종유석이 자란다.</p></div>
      <div class="choices"><span>① ㄱ</span><span>② ㄴ</span><span>③ ㄱ, ㄷ</span><span>④ ㄴ, ㄷ</span><span>⑤ ㄱ, ㄴ, ㄷ</span></div>
    </div>
    <div class="col stack" style="flex:0 0 380px"><div class="board" style="min-height:230px"></div></div>
  </div>
  <div class="answer step mt12"><b>정답 ③ ㄱ, ㄷ</b> <span class="small">ㄷ: 석회 동굴 생성 반응의 역반응 · ㄴ: 연소는 비가역 반응</span></div>
</section>''')
add(T('''<!-- ════════ 28. 확인 문제 02 ════════ -->
<section class="slide" data-sec="01 · 확인 문제" data-title="확인 문제 02">
  <h2><span class="tag q">확인 문제 02</span>평형에 도달하는 그래프</h2>
  <p class="f22">그림은 밀폐 용기에 $\\ce{NO2(g)}$를 넣었을 때, 반응 $\\ce{2NO2(g) &lt;=&gt; N2O4(g)}$에서 시간에 따른 농도를 나타낸 것이다. 이에 대한 설명으로 옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?</p>
  <div class="row mt8">
    <div class="col" style="flex:0 0 520px"><svg class="fig" viewBox="0 0 560 230" style="width:500px" aria-label="이산화 질소와 사산화 이질소 농도가 t1 이후 일정한 그래프">[[G]]</svg></div>
    <div class="col">
      <div class="bogi"><p>ㄱ. $t_1$ 이후 정반응 속도와 역반응 속도가 같다.</p><p>ㄴ. $t_1$ 이후 $\\ce{NO2}$와 $\\ce{N2O4}$의 농도는 같다.</p><p>ㄷ. $t_1$ 이후 용기 속 기체의 색이 일정하다.</p></div>
      <div class="choices"><span>① ㄱ</span><span>② ㄴ</span><span>③ ㄱ, ㄴ</span><span>④ ㄱ, ㄷ</span><span>⑤ ㄴ, ㄷ</span></div>
      <div class="board mt8" style="min-height:60px"></div>
    </div>
  </div>
  <div class="answer step mt8"><b>정답 ④ ㄱ, ㄷ</b> <span class="small">ㄴ: 평형에서 농도는 일정하지만 같지 않다.</span></div>
</section>''', G=graph('c',anim=False)))
add('''<!-- ════════ 29. 확인 문제 03 ════════ -->
<section class="slide" data-sec="01 · 확인 문제" data-title="확인 문제 03 (서술형)">
  <h2><span class="tag q">확인 문제 03</span>서술형</h2>
  <div class="row stretch" style="height:250px">
    <div class="col stack">
      <p class="f22">마개를 닫은 용기에 물을 넣고 오래 두었더니 수면의 높이가 더 이상 변하지 않았다. 이 상태를 <b>동적 평형</b>이라고 하는 까닭을 <b>증발 속도</b>와 <b>응축 속도</b>를 사용하여 서술하시오.</p>
      <div class="board mt8"></div>
    </div>
  </div>
  <div class="answer step cm311-left"><b>예시 답안</b> 수면의 높이가 일정하여 겉으로는 변화가 없어 보이지만, 물의 증발과 수증기의 응축은 계속 일어나고 있으며 증발 속도와 응축 속도가 같기 때문이다.<br><span class="small">채점 요소: ① 겉보기 변화 없음 ② 증발과 응축이 계속 일어남 ③ 두 속도가 같음</span></div>
</section>''')

# ---------- 30–32 ----------
add('''<!-- ════════ 30. 소단원 마무리 ════════ -->
<section class="slide" data-sec="01 · 소단원 마무리" data-title="소단원 마무리">
  <h2><span class="tag">소단원 마무리</span>몸으로, 화면으로 평형 나타내기</h2>
  <div class="row">
    <div class="col">
      <div class="card"><h3>창의력 키우기</h3>
        <p class="f21">가역 반응과 동적 평형을 몸으로 나타내는 놀이를 만들어 보자.</p>
        <p class="f21 mt8">예: 두 모둠이 공을 같은 빠르기로 주고받으면 모둠마다 가진 공의 수가 일정하게 유지된다.</p>
        <p class="small mt8">놀이에서 반응물·생성물·정반응·역반응·평형이 각각 무엇인지 정리하자.</p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h3>디지털 소양 키우기</h3>
        <p class="f21">온라인 모의실험(또는 오늘의 실험실)에서 처음 조건을 바꾸어 가며 평형에 도달하는 그래프를 저장하자.</p>
        <p class="f21 mt8">여러 그래프의 공통점을 한 문단으로 써서 모둠 게시판에 공유하자.</p>
        <p class="small mt8">다른 사람의 화면이나 자료를 쓸 때는 출처를 밝힌다.</p>
      </div>
    </div>
  </div>
</section>''')
add('''<!-- ════════ 31. 스스로 정리 ════════ -->
<section class="slide" data-sec="01 가역 반응과 화학 평형 · 마무리" data-title="스스로 정리">
  <h2><span class="tag ink">스스로 정리</span>1. 화학 평형 — 개념 지도</h2>
  <div class="cm311-map">
    <div class="cm311-node cm311-main"><b>01 가역 반응과 화학 평형</b> <span class="small">(오늘)</span>
      <p class="f21 mt8" data-q>정반응과 역반응이 모두 일어나는 반응: ❶ <span class="blank"><span class="step">가역 반응</span></span></p>
      <p class="f21" data-q>역반응이 거의 일어나지 않는 반응: ❷ <span class="blank"><span class="step">비가역 반응</span></span></p>
      <p class="f21" data-q>겉보기 변화는 없지만 두 반응이 계속 일어나는 상태: ❸ <span class="blank"><span class="step">동적 평형</span></span></p>
      <p class="f21" data-q>물과 수증기 ❹ <span class="blank"><span class="step">상평형</span></span>, 포화 용액 ❺ <span class="blank"><span class="step">용해 평형</span></span></p>
      <p class="f21" data-q>화학 평형: ❻ <span class="blank"><span class="step">정반응 속도</span></span> = 역반응 속도, 농도가 ❼ <span class="blank"><span class="step">일정</span></span>하다.</p>
    </div>
    <div class="cm311-arr">→</div>
    <div class="cm311-node cm311-dim">02 화학 평형과 평형 상수<br><span class="small">(다음 시간)</span></div>
    <div class="cm311-arr">→</div>
    <div class="cm311-node cm311-dim">03 화학 반응의 진행 방향 예측<br><span class="small">반응 지수</span></div>
  </div>
</section>''')
add('''<!-- ════════ 32. 스스로 점검하기 ════════ -->
<section class="slide" data-sec="01 가역 반응과 화학 평형 · 마무리" data-title="스스로 점검하기">
  <h2><span class="tag q">스스로 점검하기</span>오늘 배운 것 점검하기</h2>
  <div class="chips col1">
    <button class="chk">[지식·이해] 가역 반응과 비가역 반응을 예를 들어 구분할 수 있다.</button>
    <button class="chk">[과정·기능] 모형 실험 자료를 표와 그래프로 나타내고 동적 평형으로 해석하였다.</button>
    <button class="chk">[가치·태도] 생활 속 가역 반응과 평형의 예를 찾아보는 데 흥미를 가졌다.</button>
  </div>
  <div class="card mt16">
    <p class="f21"><b>Q</b> 평형 상태에서 반응이 멈추었다는 말이 틀린 까닭은? <span class="step">→ 정반응과 역반응이 같은 속도로 계속 일어나기 때문이다.</span></p>
    <p class="f21 mt8"><b>Q</b> 평형 상태에서 '일정한 것'과 '같은 것'은? <span class="step">→ 농도는 일정하고, 정반응 속도와 역반응 속도는 같다.</span></p>
    <p class="f21 mt8"><b>Q</b> 비가역 반응의 예 두 가지는? <span class="step">→ 메테인의 연소, 마그네슘과 염산의 반응 (설탕 가열)</span></p>
  </div>
  <div class="note puzzle mt16"><b>다음 시간</b> 평형 상태에서 반응물과 생성물의 농도 사이에는 어떤 규칙이 있을까? 처음 넣은 양을 바꾸어도 변하지 않는 값을 찾아보자.</div>
</section>''')
