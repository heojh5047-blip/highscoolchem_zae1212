p='tpl.html'; s=open(p,encoding='utf-8').read()
R=[]
def r(a,b): 
    global s
    assert a in s, a[:80]; s=s.replace(a,b)
r('<div class="fnode">열화학 반응식·표준 상태</div>','<div class="fnode">열화학 반응식</div><div class="farr">→</div>\n    <div class="fnode">표준 상태</div>')
r('<div class="fnode">표준 생성 엔탈피</div><div class="farr">→</div>\n    <div class="fnode">헤스 법칙</div><div class="farr">→</div>\n    <div class="fnode hl">중화열 실험실</div><div class="farr">→</div>\n    <div class="fnode">연습 문제</div>',
  '<div class="fnode">표준 생성 엔탈피</div><div class="farr">→</div>\n    <div class="fnode">헤스 법칙</div><div class="farr">→</div>\n    <div class="fnode hl">중화열 실험실</div>')
# S8
r('<div class="formula sm">$\\ce{Zn(s) + I2(s) -> ZnI2(s)}\\quad\\Delta H=-208\\ \\text{kJ}$</div>','<div class="formula sm">$\\ce{Zn(s) + I2(s) -> ZnI2(s)}$<div class="unit">$\\Delta H=-208\\ \\text{kJ}$</div></div>')
# S11
a=s.index('  <div class="row stretch mt8">\n    <div class="col">\n      <div class="card q"><p class="f21"><b>Q</b> 같은 반응의 계수를 2배')
b=s.index('</section>',a)
s=s[:a]+'''  <div class="card q mt8"><p class="f21"><b>Q</b> 같은 반응의 계수를 2배 하여 쓰면 $\\Delta H$는?</p>
    <p class="f21 step">→ $\\ce{2CH4(g) + 4O2(g) -> 2CO2(g) + 4H2O(l)}$ <span class="ans">$\\Delta H=-1780\\ \\text{kJ}$</span> — 계수가 2배이면 $\\Delta H$도 2배</p></div>
  <div class="card q mt8"><p class="f21"><b>Q</b> 역반응의 $\\Delta H$는?</p>
    <p class="f21 step">→ $\\ce{CO2(g) + 2H2O(l) -> CH4(g) + 2O2(g)}$ <span class="ans">$\\Delta H=+890\\ \\text{kJ}$</span> — 크기는 같고 부호가 반대</p></div>
'''+s[b:]
# S12
r('<div class="formula sm">$\\begin{aligned}&amp;\\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(g)}&amp;&amp;\\Delta H=-802\\ \\text{kJ}\\\\&amp;\\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)}&amp;&amp;\\Delta H=-890\\ \\text{kJ}\\end{aligned}$</div>',
  '<div class="card"><p class="f21">$\\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(g)}$ $\\ \\Delta H=-802\\ \\text{kJ}$</p><p class="f21">$\\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)}$ $\\ \\Delta H=-890\\ \\text{kJ}$</p></div>')
r('<p class="f21 step">→ $25\\ {}^\\circ\\text{C}$에서 $\\ce{H2O(g)}$ 1 mol의 엔탈피가 $\\ce{H2O(l)}$ 1 mol보다 $44\\ \\text{kJ}$ 높다.','<p class="f21 step">→ $25\\ {}^\\circ\\text{C}$에서 $\\ce{H2O(g)}$ 1 mol의 엔탈피가 $\\ce{H2O(l)}$ 1 mol보다 <span class="ans">$44\\ \\text{kJ}$ 높다</span>.')
# S13
r('<div class="formula sm">$\\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)}$<div class="unit">$\\Delta H^\\circ=-890\\ \\text{kJ}$ ($25\\ {}^\\circ\\text{C}$)</div></div>',
  '<div class="card"><p class="f21">예: $\\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)}$<br>$\\Delta H^\\circ=-890\\ \\text{kJ}$ ($25\\ {}^\\circ\\text{C}$)</p></div>')
r('<div class="col stack" style="flex:0 0 620px">\n      <p class="f21">반응 엔탈피는 압력 조건에 따라','<div class="col stack" style="flex:0 0 600px">\n      <p class="f21">반응 엔탈피는 압력 조건에 따라')
# S15
r('  <p class="small c-muted">예시 결과 — 조사한 자료의 출처를 함께 적고, 장단점 글은 900자 이내로 쓴다.</p>\n','')
r('<th>장점(예시)</th><th>단점(예시)</th>','<th>장점 (예시 결과)</th><th>단점 (예시 결과)</th>')
# S16
r('<div class="formula sm">$\\begin{aligned}&amp;\\mathrm{C}_\\text{흑연}(s)+\\ce{O2(g) -> CO2(g)}&amp;&amp;\\Delta H=-394\\ \\text{kJ}\\\\&amp;\\mathrm{C}_\\text{다이아몬드}(s)+\\ce{O2(g) -> CO2(g)}&amp;&amp;\\Delta H=-396\\ \\text{kJ}\\end{aligned}$</div>',
  '<div class="card"><p class="f21">$\\mathrm{C}_\\text{흑연}(s)+\\ce{O2(g) -> CO2(g)}$ $\\ \\Delta H=-394\\ \\text{kJ}$</p><p class="f21">$\\mathrm{C}_\\text{다이아몬드}(s)+\\ce{O2(g) -> CO2(g)}$ $\\ \\Delta H=-396\\ \\text{kJ}$</p></div>')
# S18
r('<div class="formula sm">$\\ce{1/2N2(g) + O2(g) -> NO2(g)}$<div class="unit">$\\Delta H_\\mathrm{f}^\\circ=+34\\ \\text{kJ/mol}$</div></div>\n      <div class="formula sm">$\\mathrm{C}_\\text{흑연}(s)+\\ce{2H2(g) + 1/2O2(g) -> CH3OH(l)}$<div class="unit">$\\Delta H_\\mathrm{f}^\\circ=-239\\ \\text{kJ/mol}$</div></div>',
  '<div class="card"><p class="f21">$\\ce{1/2N2(g) + O2(g) -> NO2(g)}$<br>$\\Delta H_\\mathrm{f}^\\circ=+34\\ \\text{kJ/mol}$</p><p class="f21 mt8">$\\mathrm{C}_\\text{흑연}(s)+\\ce{2H2(g) + 1/2O2(g) -> CH3OH(l)}$<br>$\\Delta H_\\mathrm{f}^\\circ=-239\\ \\text{kJ/mol}$</p></div>')
# S21
r('<div class="formula sm">$\\begin{aligned}\\Delta H^\\circ_\\text{반응}','<div class="card"><p class="f21">$\\begin{aligned}\\Delta H^\\circ_\\text{반응}')
r('+(-394\\ \\text{kJ})+(-572\\ \\text{kJ})\\end{aligned}$</div>','+(-394\\ \\text{kJ})+(-572\\ \\text{kJ})\\end{aligned}$</p></div>')
r('<div class="formula sm step">$\\Delta H^\\circ_\\text{반응}=\\sum n_\\mathrm{p}\\Delta H_\\mathrm{f}^\\circ(\\text{생성물})-\\sum n_\\mathrm{r}\\Delta H_\\mathrm{f}^\\circ(\\text{반응물})$<div class="unit">',
  '<div class="card step"><p class="f22">$\\Delta H^\\circ_\\text{반응}=\\sum n_\\mathrm{p}\\Delta H_\\mathrm{f}^\\circ(\\text{생성물})-\\sum n_\\mathrm{r}\\Delta H_\\mathrm{f}^\\circ(\\text{반응물})$</p><div class="small">')
# S23
r('<p class="f21 step">$\\Delta H^\\circ=\\left[\\Delta H_\\mathrm{f}^\\circ(\\ce{Al2O3})+2\\times0\\right]-\\left[2\\times0+\\Delta H_\\mathrm{f}^\\circ(\\ce{Fe2O3})\\right]=(-1676)-(-826)$</p>',
  '<p class="f21 step">$\\Delta H^\\circ=\\left[\\Delta H_\\mathrm{f}^\\circ(\\ce{Al2O3})+2\\times0\\right]-\\left[2\\times0+\\Delta H_\\mathrm{f}^\\circ(\\ce{Fe2O3})\\right]$<br>$\\qquad=(-1676\\ \\text{kJ})-(-826\\ \\text{kJ})$</p>')
# S27
r('<div class="formula sm">$\\Delta H\\approx\\sum\\Delta H_\\mathrm{B}(\\text{끊는 결합})-\\sum\\Delta H_\\mathrm{B}(\\text{생기는 결합})$</div>',
  '<div class="card"><p class="f22">$\\Delta H\\approx\\sum\\Delta H_\\mathrm{B}(\\text{끊는 결합})-\\sum\\Delta H_\\mathrm{B}(\\text{생기는 결합})$</p></div>')
# S28
r('<p class="f21 mt8">폭탄먼지 벌레는 위협을 받으면 효소의 작용으로 발열 반응을 일으켜 혼합 용액을 끓이고 증기 스프레이를 뿜는다. 생성물 벤조퀴논 $\\ce{C6H4O2}$는 퇴치제로 작용한다.</p>\n  <div class="formula sm">$\\ce{C6H4(OH)2(aq) + H2O2(aq) -> C6H4O2(aq) + 2H2O(l)}$</div>\n  <div class="row mt8">',
  '<p class="f21 mt8">폭탄먼지 벌레는 위협을 받으면 효소의 작용으로 아래 발열 반응을 일으켜 끓는 증기 스프레이를 뿜고, 생성물 벤조퀴논 $\\ce{C6H4O2}$로 적을 쫓는다.</p>\n  <p class="f22 mt4" style="text-align:center">$\\ce{C6H4(OH)2(aq) + H2O2(aq) -> C6H4O2(aq) + 2H2O(l)}$</p>\n  <div class="row mt4">')
# S30
r('<p class="f21"><b>탐구 문제</b> 같은 생성물을 얻는 서로 다른 경로의 반응열은 정말 같을까? <b>Q</b> 가설은?</p>\n      <p class="f21 step">→ 엔탈피는 상태 함수이므로, 고체 $\\ce{NaOH}$를 염산과 직접 반응시킨 반응열은 용해열과 중화열의 합과 같을 것이다.</p>',
  '<p class="f21"><b>탐구 문제</b> 같은 생성물을 얻는 다른 경로의 반응열은 같을까? <b>Q</b> 가설은?</p>\n      <p class="f21 step">→ 엔탈피는 상태 함수이므로 직접 반응의 반응열 = 용해열 + 중화열일 것이다.</p>')
r('<p class="f21"><b>안전</b> 고체 $\\ce{NaOH}$와 염산은 피부와 눈을 손상시킨다 → 보안경·장갑 착용. $\\ce{NaOH}$는 공기 중 수분을 흡수하므로 빠르게 재어 바로 넣는다. 다 쓴 용액은 중화해 폐수통에 모은다.</p>',
  '<p class="f21"><b>안전</b> 고체 $\\ce{NaOH}$와 염산은 피부·눈을 손상시킨다 → 보안경·장갑. $\\ce{NaOH}$는 수분을 흡수하므로 빠르게 재어 바로 넣는다. 쓴 용액은 중화해 폐수통에.</p>')
# S31
r('<div class="stage"><h3>① 용해 $\\Delta H_1$</h3><p class="f21">증류수 100 mL + 고체 $\\ce{NaOH}$ 2.00 g</p>','<div class="stage"><h3>① 용해 $\\Delta H_1$</h3><p class="f19">증류수 100 mL + 고체 $\\ce{NaOH}$ 2.00 g</p>')
r('<p class="f21">$1.0\\ \\text{M}$ $\\ce{NaOH}$ 50 mL + $1.0\\ \\text{M}$ $\\ce{HCl}$ 50 mL</p>','<p class="f19">$1.0\\ \\text{M}$ $\\ce{NaOH}$ 50 mL + $1.0\\ \\text{M}$ $\\ce{HCl}$ 50 mL</p>')
r('<p class="f21">$0.50\\ \\text{M}$ $\\ce{HCl}$ 100 mL + 고체 $\\ce{NaOH}$ 2.00 g</p>','<p class="f19">$0.50\\ \\text{M}$ $\\ce{HCl}$ 100 mL + 고체 $\\ce{NaOH}$ 2.00 g</p>')
r('<p class="f21">온도는 1초 간격으로 기록한다. 용액의 밀도 $1.00\\ \\text{g/mL}$, 비열 $4.18\\ \\text{J/(g}\\cdot{}^\\circ\\text{C)}$로 가정한다.</p>\n      <div class="formula sm">$q=mc\\Delta T,\\quad\\Delta H=-\\dfrac{q}{n}$<div class="unit">$n$: 반응한 $\\ce{NaOH}$(또는 생긴 물)의 양 $0.0500\\ \\text{mol}$, 구경꾼 이온 $\\ce{Na+}$·$\\ce{Cl-}$</div></div>',
  '<div class="formula sm">$q=mc\\Delta T,\\quad\\Delta H=-\\dfrac{q}{n}$<div class="unit">1초 간격 기록, 밀도 $1.00\\ \\text{g/mL}$, 비열 $4.18\\ \\text{J/(g}\\cdot{}^\\circ\\text{C)}$, $n=0.0500\\ \\text{mol}$</div></div>')
# S38
a=s.index('    <div class="col stack">\n      <p class="f21 step">(가) 그대로: $-1273$</p>')
b=s.index('</section>',a)
s=s[:a]+'''    <div class="col stack">
      <p class="f21 step">(가) + (나)의 역반응 + (다) × 3 + (라) × 3</p>
      <p class="f21 step">지워지는 물질: $\\ce{B2O3(s)}$, $\\ce{3O2(g)}$, $\\ce{3H2O(l)}$, $\\ce{3H2O(g)}$ → 목표 반응식</p>
      <p class="f21 step">$\\Delta H=(-1273)+(+2035)+3(-286)+3(+44)$</p>
      <div class="answer step">$\\Delta H=+36\\ \\text{kJ}$</div>
    </div>
  </div>
'''+s[b:]
r('<div class="col stack" style="flex:0 0 500px">\n      <table class="tight ac312-c">\n        <tr><th>자료</th>','<div class="col stack" style="flex:0 0 590px">\n      <table class="tight ac312-c">\n        <tr><th>자료</th>')
open(p,'w',encoding='utf-8').write(s)
