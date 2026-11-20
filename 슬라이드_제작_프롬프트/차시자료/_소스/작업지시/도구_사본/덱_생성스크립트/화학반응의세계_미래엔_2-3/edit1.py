import sys
p='tpl.html'; s=open(p,encoding='utf-8').read()
R=[
('<p class="f21 step" data-g="v1">→ <span class="ans">아연판</span> 표면</p>',
 '<p class="f21 step" data-g="v1">→ <span class="ans">아연판</span>에서만 생긴다(구리판에서는 생기지 않는다)</p>'),
('<p class="f21 step" data-g="v2">→ 주로 <span class="ans">구리판</span> 표면</p>',
 '<p class="f21 step" data-g="v2">→ 대부분 <span class="ans">구리판</span>에서 생기고, 아연판에서는 소량만 생긴다</p><p class="small step" data-g="v2">기포가 <b>더 많이</b> 생기는 금속판이 어느 쪽인지 살펴본다.</p>'),
('<tr><th>기포 발생 위치</th><td>아연판 표면</td><td>구리판 표면</td></tr>',
 '<tr><th>기포 발생 위치</th><td>아연판에서만</td><td>대부분 구리판 (아연판은 소량)</td></tr>'),
('<p class="f22 mt16"><b>3</b> 실험 2에서 산화 반응과 환원 반응이 일어나는 곳은?</p>',
 '<p class="f22 mt16"><b>3</b> 산화 반응과 환원 반응이 일어나는 곳은? <span class="small">실험 1에서는 두 반응이 모두 아연판에서 일어난다. 실험 2에서는?</span></p>'),
('<p class="small step mt8">또는 전극을 서로 다른 전해질에 담가 수소 기체가 생기지 않게 만든다 → 다니엘 전지</p>',
 '<p class="small step mt8">산화제로도 분극을 완전히 없애지는 못한다. 이를 해결하려는 노력에서 전극을 서로 다른 전해질에 담근 다니엘 전지가 나왔다.</p>'),
('6홈판의 두 홈에 황산 아연 수용액과 황산 구리(II) 수용액을 넣고 아연판과 구리판을 꽂은 뒤',
 '6홈판의 두 홈에 황산 마그네슘 수용액과 황산 구리(II) 수용액을 넣고 마그네슘판과 구리판을 꽂은 뒤'),
('<tr><th>(−)극</th><td><span class="step" data-g="d1">아연판</span></td><td><span class="step" data-g="d1">$1\\ \\text{M}$ 황산 아연</span></td></tr>',
 '<tr><th>(−)극</th><td><span class="step" data-g="d1">마그네슘판</span></td><td><span class="step" data-g="d1">$1\\ \\text{M}$ 황산 마그네슘</span></td></tr>'),
('설계 예시 — 모둠마다 금속판 짝을 바꾼다(마그네슘–구리, 마그네슘–아연 …).',
 '설계 예시 — 모둠마다 금속판 짝을 바꾼다(아연–구리, 마그네슘–아연 …). 한 가지 전해질(볼타 전지 꼴)과 반쪽 전지 연결(다니엘 전지 꼴) 중 하나를 골라 비교해도 좋다.'),
('<tr><th>(−)극</th><td>아연판</td><td>황산 아연 수용액</td><td class="l"><span class="step" data-g="m1">아연판 표면이 거칠어지고 조금씩 얇아진다(산화)</span></td><td rowspan="2"><span class="step" data-g="m2">약 1.0</span></td></tr>',
 '<tr><th>(−)극</th><td>마그네슘판</td><td>$1\\ \\text{M}$ 황산 마그네슘 수용액</td><td class="l"><span class="step" data-g="m1">표면에 어두운 얼룩이 생기고, 시간이 지날수록 두께가 얇아진다(산화)</span></td><td rowspan="2"><span class="step" data-g="m2">2.71</span></td></tr>'),
('<tr><th>(+)극</th><td>구리판</td><td>황산 구리(II) 수용액</td><td class="l"><span class="step" data-g="m1">구리판 표면에 붉은 구리가 석출된다(환원)</span></td></tr>',
 '<tr><th>(+)극</th><td>구리판</td><td>$1\\ \\text{M}$ 황산 구리(II) 수용액</td><td class="l"><span class="step" data-g="m1">석출된 구리가 구리판에 달라붙고, 수용액의 푸른색이 점점 옅어진다(환원)</span></td></tr>'),
('<p class="f22 mt16"><b>Q</b> 측정값(약 1.0 V)이 표준 전지 전위 $+1.10\\ \\text{V}$보다 조금 작은 까닭은?</p>',
 '<p class="f22 mt16"><b>Q</b> 실제로 잰 값이 표준 전지 전위($+2.71\\ \\text{V}$)보다 작게 나오기도 하는 까닭은?</p>'),
('→ 금속판 표면의 산화막·불순물, 거름종이 염다리와 용액의 저항(전극 사이 거리), 실제 농도·온도가 표준 상태와 다른 점 등 때문이다.',
 '→ 금속판 표면의 산화막·불순물(특히 마그네슘판), 거름종이 염다리와 용액의 저항(전극 사이 거리), 실제 농도·온도가 표준 상태와 다른 점 등 때문이다.'),
('<p class="small step mt8">결과 예시는 덱이 만든 값이다. 수업에서는 모둠이 잰 값을 넣는다.</p>',
 '<p class="small step mt8">전압계를 반대로 이으면 바늘이 0 아래로 내려가거나(아날로그) 음수가 나온다(디지털) → 두 극을 바꾸어 잇는다. 수업에서는 모둠이 잰 값을 넣는다.</p>'),
('<tr><td>1</td><td>아연판</td><td>구리판</td><td>황산 아연 | 황산 구리(II)</td><td>1.09</td><td><span class="step" data-g="c1">1.10</span></td></tr>\n    <tr><td>2</td><td>마그네슘판</td><td>구리판</td><td>황산 마그네슘 | 황산 구리(II)</td><td>2.69</td><td><span class="step" data-g="c1">2.71</span></td></tr>',
 '<tr><td>1</td><td>마그네슘판</td><td>구리판</td><td>황산 마그네슘 | 황산 구리(II)</td><td>2.69</td><td><span class="step" data-g="c1">2.71</span></td></tr>\n    <tr><td>2</td><td>아연판</td><td>구리판</td><td>황산 아연 | 황산 구리(II)</td><td>1.09</td><td><span class="step" data-g="c1">1.10</span></td></tr>'),
('<div class="card tip step"><p class="f21">전지 전위는 두 반쪽 전지의 <b>표준 환원 전위 차이</b>로 정해진다.',
 '<div class="card tip step"><p class="f21">금속은 종류에 따라 산화되는 정도가 달라 표준 환원 전위도 다르다. 전지 전위는 두 반쪽 전지의 <b>표준 환원 전위 차이</b>로 정해진다.'),
('→ 전압만 보면 마그네슘–구리 전지(2.69 V). 하지만 마그네슘은 물과도 반응하여 쉽게 닳고 산화막이 생긴다. 전압의 안정성과 가격까지 따지면 아연–구리 전지를 고를 수도 있다 — <b>조건을 정하는 기준에 따라 선정 결과가 달라진다</b>.',
 '→ <b>예시</b> 모둠 1의 마그네슘–구리 전지. 금속판의 가격이 저렴하면서도 전지 전위가 가장 높아 낮은 비용으로 높은 전압을 얻을 수 있다. 전압이 일정하게 유지되는 정도 등 다른 조건을 우선하면 선정 결과가 달라질 수 있다 — <b>기준에 따라 가장 효율적인 전지가 달라진다</b>.'),
('<div class="stage step" data-g="f1"><h3>전극</h3><p>금속의 종류(전위차), 표면적(넓을수록 전류 큼), 표면 상태(산화막 제거)</p></div>',
 '<div class="stage step" data-g="f1"><h3>전극</h3><p>표준 환원 전위가 높은 전극 신소재 개발(전지 전위 향상), 표면 상태(산화막 제거)</p></div>'),
('<div class="stage step" data-g="f1"><h3>전해질·염다리</h3><p>이온의 농도·이동 속도, 염다리의 이온 종류, 전극 사이 거리(내부 저항)</p></div>',
 '<div class="stage step" data-g="f1"><h3>전해질·분리막</h3><p>전해질과 분리막의 성능을 개선해 이온 전도성 향상, 전극 사이 거리(내부 저항)</p></div>'),
('<div class="stage step" data-g="f1"><h3>쓰임과 환경</h3><p>무게·크기, 사용 온도, 재료 가격과 자원의 양, 폐전지·폐액 처리</p></div>',
 '<div class="stage step" data-g="f1"><h3>온도·설계</h3><p>최적의 효율을 내는 온도 범위 유지, 여러 셀을 직렬연결할 때 모든 셀의 충전·방전이 균일하도록 설계</p></div>'),
('<p class="f21 step mt8"><b>예시</b> (−)극: 아연이 산화된다. (+)극: 이산화 망가니즈($\\ce{MnO2}$)가 환원된다(전해질 수산화 칼륨).</p>\n        <p class="f21 step mt8">$E^\\circ_\\text{전지}=E^\\circ_{(+)\\text{극}}-E^\\circ_{(-)\\text{극}}$에 부록 표의 두 값을 넣는다 → 약 1.5 V. 건전지에 적힌 전압(1.5 V)과 비교해 본다.</p>',
 '<p class="f21 step mt8"><b>예시</b> (−)극: $\\ce{Zn(s) + 2OH-(aq) -> ZnO(s) + H2O(l) + 2e-}$ &nbsp;$E^\\circ=-1.26\\ \\text{V}$<br>(+)극: $\\ce{2MnO2(s) + H2O(l) + 2e- -> Mn2O3(s) + 2OH-(aq)}$ &nbsp;$E^\\circ=+0.15\\ \\text{V}$</p>\n        <p class="f21 step mt8">$E^\\circ_\\text{전지}=E^\\circ_\\text{환원 전극}-E^\\circ_\\text{산화 전극}=0.15-(-1.26)=1.41\\ \\text{V}$</p>'),
('<p class="f21 step mt8"><b>예시</b> 나트륨·칼륨은 리튬처럼 1족 원소로 이온화 경향이 커서 큰 전압을 낼 수 있고, 매장량이 많아 값이 싸다.</p>',
 '<p class="f21 step mt8"><b>예시</b> 리튬은 매장량이 한정적이다. 나트륨·칼륨은 리튬과 같은 1족 알칼리 금속이라 성질이 비슷해 같은 원리로 전지를 만들 수 있고, 바닷물에 풍부하다.</p>'),
('<p class="f21 step mt8">다만 이온이 크고 무거워 같은 무게에 담는 에너지가 적다 → 나트륨 이온 전지는 에너지 저장 장치용으로 연구·생산되고 있다. (검색한 자료의 출처를 함께 적는다.)</p>',
 '<p class="f21 step mt8">다만 리튬보다 무겁고 에너지 밀도가 낮아 더 많은 연구가 필요하다. (검색한 자료의 출처를 함께 적는다.)</p>'),
('<div class="formula sm step">$\\ce{H2(g) + 1/2O2(g) -> H2O(l)}$</div>',
 '<div class="formula sm step">$\\ce{2H2(g) + O2(g) -> 2H2O(l)}$</div>'),
('⑴ 두 반쪽 반응식을 더하면 전자 2개와 $\\ce{2H+}$이 지워진다.',
 '⑴ 두 반쪽 반응식을 더하면 전자 2개와 $\\ce{2H+}$이 지워지고, 계수를 정수로 맞춘다($\\ce{H2 + 1/2O2 -> H2O}$로 써도 같다).'),
('<p class="small step mt8">채점 요소: ① 수소 기체가 구리판 표면에 달라붙음 ② 수소 이온의 환원을 방해함 — 두 요소를 모두 쓰면 완전한 답</p>',
 '<p class="small step mt8">채점 요소: ① (+)극에서 발생한 수소 기체가 금속판 표면에 달라붙음 ② 수소 이온의 환원을 방해함 — 두 요소를 모두 쓰면 완전한 답</p>'),
]
for a,b in R:
    n=s.count(a)
    if n!=1: print('MISS',n,a[:60]); continue
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
g=open('gen.py',encoding='utf-8').read()
A=[("W = [(110, 'Zn', r'\\ce{ZnSO4(aq)}', 'w'), (280, 'Cu', r'\\ce{CuSO4(aq)}', 'cu'), (450, 'Mg', r'\\ce{MgSO4(aq)}', 'w')]",
    "W = [(110, 'Mg', r'\\ce{MgSO4(aq)}', 'w'), (280, 'Cu', r'\\ce{CuSO4(aq)}', 'cu'), (450, 'Zn', r'\\ce{ZnSO4(aq)}', 'w')]"),
   ("mix='(−)극 · 아연판'","mix='(−)극 · 마그네슘판'")]
for a,b in A:
    if g.count(a)!=1: print('GMISS',a[:50]); continue
    g=g.replace(a,b)
open('gen.py','w',encoding='utf-8').write(g)
print('done')
