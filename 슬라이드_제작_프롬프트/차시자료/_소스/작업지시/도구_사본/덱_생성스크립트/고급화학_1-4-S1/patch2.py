p='tpl.html'; s=open(p,encoding='utf-8').read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:80]); s=s.replace(a,b)
# S7
R('''      <div class="formula sm step">$\\mathrm{B^-} + \\mathrm{H{-}C{-}C{-}X} \\longrightarrow \\mathrm{C{=}C} + \\mathrm{H{-}B} + \\mathrm{X^-}$<div class="unit">제거: 염기가 β 수소를 떼어 냄</div></div>
    </div>
  </div>
  <div class="note step f21">메커니즘 이름의 숫자 1, 2는 <b>단계 수가 아니라 속도 결정 단계에 참여하는 입자 수</b>(분자도)이다.</div>
  <div class="row mt8">
    <p class="f21" style="flex:0 0 560px"><b>Q</b> $\\mathrm{S_N2}$에서 S, N은 무엇을 뜻할까?</p>
    <div class="answer step" style="flex:1">S 치환, N 친핵성 — 2는 속도 결정 단계의 분자도</div>
  </div>''','''      <div class="formula sm step">$\\mathrm{B^-} + \\mathrm{H{-}C{-}C{-}X} \\longrightarrow \\mathrm{C{=}C} + \\mathrm{H{-}B} + \\mathrm{X^-}$<div class="unit">제거: 염기가 β 수소를 떼어 냄</div></div>
      <div class="note step">메커니즘 이름의 숫자 1, 2는 <b>단계 수가 아니라 속도 결정 단계에 참여하는 입자 수</b>(분자도)이다.</div>
    </div>
  </div>
  <div class="row">
    <p class="f21" style="flex:0 0 520px"><b>Q</b> $\\mathrm{S_N2}$에서 S, N은 무엇을 뜻할까?</p>
    <div class="answer step" style="flex:1">S 치환, N 친핵성 — 2는 속도 결정 단계의 분자도</div>
  </div>''')
# S8
R('<p class="f21 step">→ <b>이분자 친핵성 치환 반응($\\mathrm{S_N2}$)</b>: 중간체 없이','<p class="f21 step"><b>이분자 친핵성 치환 반응($\\mathrm{S_N2}$)</b>: 중간체 없이')
# S13
R('''  <div class="row">
    <p class="f21" style="flex:1">$\\ce{(CH3)3CBr}$은 물과 매우 빠르게 반응한다 — $\\ce{CH3Br}$보다 <b>100만 배 이상</b> 빠르고, 속도는 $\\ce{(CH3)3CBr}$의 농도에만 비례한다.</p>
    <div class="formula sm" style="flex:0 0 260px">$v=k[\\mathrm{RX}]$</div>
  </div>''','''  <p class="f21">$\\ce{(CH3)3CBr}$은 물과 반응하는 속도가 $\\ce{CH3Br}$보다 <b>100만 배 이상</b> 빠르고, $\\ce{(CH3)3CBr}$의 농도에만 비례한다: $v=k[\\mathrm{RX}]$</p>''')
R('''  <div class="formula sm step mt8">$\\ce{(CH3)3CBr + 2H2O -&gt; (CH3)3COH + H3O+ + Br-}$</div>
  <div class="row mt8">
    <p class="f21" style="flex:0 0 520px"><b>Q</b> 물의 농도가 속도식에 없는 까닭은?</p>''','''  <div class="formula sm step">$\\ce{(CH3)3CBr + 2H2O -&gt; (CH3)3COH + H3O+ + Br-}$</div>
  <div class="row">
    <p class="f21" style="flex:0 0 520px"><b>Q</b> 물의 농도가 속도식에 없는 까닭은?</p>''')
# S18
R('''  <div class="row step ac14s1-three mt8">
    <div class="card"><b>$\\mathrm{E2}$</b> C–H와 C–X가 <b>동시에</b></div>''','''  <div class="row step ac14s1-three">
    <div class="card"><b>$\\mathrm{E2}$</b> C–H와 C–X가 <b>동시에</b></div>''')
R('''    <p class="f21" style="flex:0 0 560px"><b>Q</b> 2-브로모뷰테인에서 β 탄소는 몇 개일까?</p>
    <div class="answer step" style="flex:1">2개(C1, C3) → 1-뷰텐 또는 2-뷰텐</div>''','''    <p class="f21" style="flex:0 0 560px"><b>Q</b> 2-브로모뷰테인에서 β 탄소는 몇 개일까?</p>
    <div class="answer step" style="flex:1">2개($\\mathrm{C1}$, $\\mathrm{C3}$) → 1-뷰텐 또는 2-뷰텐</div>''')
R('<h2><span class="tag alt">심화</span>제거 반응과 자이체프 규칙 <span class="small c-muted">[심화]</span></h2>\n  {{ZAIT}}','<h2><span class="tag alt">심화</span>제거 반응과 자이체프 규칙 <span class="small c-muted">[심화]</span></h2>\n  <div class="ac14s1-fig">{{ZAIT}}</div>')
# S19
R('''    <div class="card step"><b>③ anti 동일 평면</b><br><span class="small">H, C, C, X가 한 평면, H와 X는 반대쪽(엇갈린 배치)</span></div>
  </div>
  <p class="small mt8">사이클로헥세인 고리에서는 H와 X가 모두 축방향일 때만 anti 동일 평면이 되며, 이 조건이 자이체프 규칙보다 우선한다(멘틸 클로라이드 → 2-멘텐만).</p>
  <div class="row">''','''    <div class="card step"><b>③ anti 동일 평면</b><br><span class="small">H, C, C, X가 한 평면, H와 X는 반대쪽(엇갈린 배치). 고리에서는 H·X가 모두 축방향일 때만 — 자이체프 규칙보다 우선</span></div>
  </div>
  <div class="row mt8">''')
R('<h2><span class="tag alt">심화</span>$\\mathrm{E2}$: 한 단계, anti 동일 평면 <span class="small c-muted">[심화]</span></h2>\n  {{E2}}','<h2><span class="tag alt">심화</span>$\\mathrm{E2}$: 한 단계, anti 동일 평면 <span class="small c-muted">[심화]</span></h2>\n  <div class="ac14s1-fig">{{E2}}</div>')
# S20
R('''  <div class="row">
    <div class="col" style="flex:0 0 820px">{{E1}}</div>
    <div class="col stack">
      <div class="card step"><p class="small">80 % 에탄올 수용액, 65 °C</p><p class="f21"><b>치환 : 제거</b><br>≈ <b>64 : 36</b></p></div>
    </div>
  </div>''','''  <div class="row">
    <div class="col" style="flex:0 0 800px">{{E1}}</div>
    <div class="col stack">
      <div class="card step"><p class="small">80 % 에탄올 수용액, 65 °C</p><p class="f21"><b>치환 : 제거</b><br>≈ <b>64 : 36</b></p></div>
    </div>
  </div>''')
R('''  <div class="formula sm step">$\\ce{(CH3)3CCl + H2O -&gt; (CH3)2C=CH2 + H3O+ + Cl-}$<div class="unit">알코올 + 진한 황산 가열(탈수 반응)도 탄소 양이온을 거치는 $\\mathrm{E1}$이다.</div></div>
  <div class="row mt8">''','''  <div class="formula sm step">$\\ce{(CH3)3CCl + H2O -&gt; (CH3)2C=CH2 + H3O+ + Cl-}$<div class="unit">알코올 + 진한 황산 가열(탈수 반응)도 탄소 양이온을 거치는 $\\mathrm{E1}$이다.</div></div>
  <div class="row">''')
# S21
R('''  <p class="f21 step">이탈기가 –OH처럼 나빠 $\\mathrm{E1}$·$\\mathrm{E2}$가 어렵고, <b>카보닐기가 옆 수소를 산성으로</b> 만들 때 일어난다. 음전하가 카보닐 산소까지 퍼져 공명으로 안정하다. 생체의 제거 반응은 대부분 $\\mathrm{E1cB}$이다.</p>
  <div class="formula sm step">$\\ce{(CH3)2C(OH)CH2COCH3 -&gt;[OH-] (CH3)2C=CHCOCH3 + H2O}$</div>
  <div class="row mt8">''','''  <p class="f21 step">이탈기가 –OH처럼 나빠 $\\mathrm{E1}$·$\\mathrm{E2}$가 어렵고, <b>카보닐기가 옆 수소를 산성으로</b> 만들 때 일어난다(음전하가 카보닐 산소까지 퍼져 공명으로 안정). 생체의 제거 반응은 대부분 $\\mathrm{E1cB}$이다.</p>
  <div class="row">
    <div class="formula sm step" style="flex:0 0 560px">$\\ce{(CH3)2C(OH)CH2COCH3 -&gt;[OH-] (CH3)2C=CHCOCH3 + H2O}$</div>
  </div>
  <div class="row">''')
# S24 예측 버튼
R('<button class="btn" data-p="SN2">SN2</button><button class="btn" data-p="SN1">SN1</button><button class="btn" data-p="E2">E2</button><button class="btn" data-p="E1">E1</button>','<button class="btn" data-p="SN2">$\\mathrm{S_N2}$</button><button class="btn" data-p="SN1">$\\mathrm{S_N1}$</button><button class="btn" data-p="E2">$\\mathrm{E2}$</button><button class="btn" data-p="E1">$\\mathrm{E1}$</button>')
# S26
R('''  <div class="board" style="height:70px"></div>
  <div class="answers">
    <div class="answer step">(라)''','''  <div class="board" style="height:24px"></div>
  <div class="answers">
    <div class="answer step">(라)''')
R('<div class="step">{{SN2I}}</div>','<div class="step ac14s1-fig">{{SN2I}}</div>')
# S27
R('<div class="formula sm step">$\\ce{(CH3)3COH + HBr -&gt; (CH3)3CBr + H2O}$</div>','<div class="formula sm step ac14s1-fs">$\\ce{(CH3)3COH + HBr -&gt; (CH3)3CBr + H2O}$</div>')
# S30
R('''  <div class="answers">
    <div class="answer step">1차 H 9개 × 1 = 9, 3차 H 1개 × 5 = 5 → 9 : 5</div>
    <div class="answer step">1-클로로-2-메틸프로페인 약 64 %, 2-클로로-2-메틸프로페인 약 36 % — 1차 H의 개수가 많다.</div>
  </div>
  <div class="board" style="height:20px"></div>''','''  <div class="row">
    <div class="board" style="flex:0 0 200px;height:60px"></div>
    <div class="answers" style="flex:1">
      <div class="answer step">1차 H 9개 × 1 = 9, 3차 H 1개 × 5 = 5 → 9 : 5</div>
      <div class="answer step">1-클로로- 약 64 %, 2-클로로-2-메틸프로페인 약 36 %</div>
    </div>
  </div>''')
R('''      <p class="f21 step mt8">브로민화의 수소 떼기는 <b>흡열</b> → 전이 상태가 라디칼과 비슷(해먼드) → 선택성이 크다.</p>''','''      <p class="f21 step mt8">브로민화의 수소 떼기는 <b>흡열</b> → 전이 상태가 라디칼과 비슷(해먼드) → 선택성이 크다.</p>
      <p class="small step">반응성은 3차 H가 크지만 1차 H의 개수가 많다.</p>''')
# S32
R('''    <div class="col" style="flex:0 0 560px">{{MARK}}</div>
    <div class="col" style="flex:0 0 400px">{{EMARK}}</div>''','''    <div class="col" style="flex:0 0 560px">{{MARK}}</div>
    <div class="col" style="flex:0 0 360px">{{EMARK}}</div>''')
R('''  <div class="formula sm step">$\\ce{(CH3)2C=CH2 + HBr -&gt; (CH3)3CBr}$</div>
  <div class="row mt8">
    <p class="f21" style="flex:0 0 520px"><b>Q</b> 프로펜에 HBr이 첨가되면 주생성물은?</p>''','''  <div class="row">
    <div class="formula sm step" style="flex:0 0 420px">$\\ce{(CH3)2C=CH2 + HBr -&gt; (CH3)3CBr}$</div>
    <p class="f21" style="flex:1"><b>Q</b> 프로펜에 HBr이 첨가되면 주생성물은?</p>
  </div>
  <div class="row">''')
R('<div class="answer step" style="flex:1">2-브로모프로페인 $\\ce{CH3CHBrCH3}$(2차 탄소 양이온을 거침)</div>','<div class="answer step" style="flex:0 0 700px;margin-left:auto">2-브로모프로페인 $\\ce{CH3CHBrCH3}$(2차 탄소 양이온을 거침)</div>')
# S35
R('<div class="formula sm">$\\ce{HC#C- + CH3Br -&gt; HC#CCH3 + Br-}$</div>','<div class="formula sm ac14s1-fs">$\\ce{HC#C- + CH3Br -&gt; HC#CCH3 + Br-}$</div>')
R('''  <div class="board" style="height:16px"></div>
</section>''','''</section>''')
R('''  <div class="card mt8"><p class="f21"><span class="tag ex">예제</span>2-뷰틴 → (가) cis-2-뷰텐, (나) trans-2-뷰텐, 1-뷰틴 → (다) 2-뷰탄온의 시약은?</p></div>''','''  <div class="row mt8">
    <div class="card" style="flex:1"><p class="f21"><span class="tag ex">예제</span>2-뷰틴 → (가) cis-2-뷰텐, (나) trans-2-뷰텐, 1-뷰틴 → (다) 2-뷰탄온의 시약은?</p></div>
    <div class="board" style="flex:0 0 220px;height:56px"></div>
  </div>''')
# S36 / S37
R('''    <div class="col" style="flex:0 0 600px">{{ALLYL}}</div>
    <div class="col" style="flex:0 0 400px">{{EDIENE}}</div>''','''    <div class="col" style="flex:0 0 600px">{{ALLYL}}</div>
    <div class="col" style="flex:0 0 380px">{{EDIENE}}</div>''')
R('''  <div class="formula sm step mt8">$\\ce{CH2=CHCH=CH2 + CH2=CH2 -&gt; C6H10}$ &nbsp;·&nbsp; $\\ce{C4H6 + C3H4O -&gt; C7H10O}$<div class="unit">1,3-뷰타다이엔 + 프로펜알(아크롤레인), 100 °C 부근 → 3-사이클로헥센-1-카브알데하이드</div></div>
  <div class="row mt8">''','''  <div class="formula sm step">$\\ce{CH2=CHCH=CH2 + CH2=CH2 -&gt; C6H10}$ &nbsp;·&nbsp; $\\ce{C4H6 + C3H4O -&gt; C7H10O}$<div class="unit">1,3-뷰타다이엔 + 프로펜알(아크롤레인), 100 °C 부근 → 3-사이클로헥센-1-카브알데하이드</div></div>
  <div class="row">''')
R('''  <div class="row ac14s1-three step mt8">
    <div class="card"><span class="f21">① 다이엔은''','''  <div class="row ac14s1-three step">
    <div class="card"><span class="f21">① 다이엔은''')
R('<h2><span class="tag alt">심화</span>딜스–알더 반응: 한 단계로 고리를 만든다 <span class="small c-muted">[심화]</span></h2>\n  {{DA}}','<h2><span class="tag alt">심화</span>딜스–알더 반응: 한 단계로 고리를 만든다 <span class="small c-muted">[심화]</span></h2>\n  <div class="ac14s1-fig">{{DA}}</div>')
# S38
R('<div class="answer step">2) 덜 치환된 C3 → 3-메틸-2-뷰탄올','<div class="answer step">2) 덜 치환된 $\\mathrm{C3}$ → 3-메틸-2-뷰탄올')
# S40
R('[지식·이해] SN2·SN1·E2·E1·E1cB의','[지식·이해] $\\mathrm{S_N2}$·$\\mathrm{S_N1}$·$\\mathrm{E2}$·$\\mathrm{E1}$·$\\mathrm{E1cB}$의')
open(p,'w',encoding='utf-8').write(s)
