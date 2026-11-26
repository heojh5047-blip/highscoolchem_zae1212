import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    c=s.count(a)
    assert c==n,(c,a[:60])
    s=s.replace(a,b)
# S2
R('''<div class="note puzzle mt12"><b>단원을 여는 질문</b> 혈액의 pH는 왜 7.4 근처에서 거의 변하지 않을까? 이 단원을 마치면 <b>화학 평형</b>으로 설명할 수 있다.</div>''',
'''<div class="note puzzle mt12"><b>단원을 여는 이야기</b> 바다는 산업 활동으로 생기는 이산화 탄소를 상당량 흡수하여 지구의 기후 변화를 늦추는 데 크게 기여한다. 바다가 이렇게 많은 이산화 탄소를 흡수하는 것은 <b>산 염기 평형</b>과 관련이 있다. 이 단원에서는 산과 염기, 중화 반응을 화학 평형의 원리로 설명하고, 이런 반응이 생명체의 항상성과 지구 생태의 지속가능성에 어떤 영향을 미치는지 알아본다.</div>''')
# S3
R('<span class="small">산, 염기와 중화 반응</span>','<span class="small">변화와 다양성</span>')
R('<span class="small">화학 평형, pH, 중화 반응</span>','<span class="small">화학 평형, 역동적인 화학 반응</span>')
R('''    <li>브뢴스테드·라우리 정의로 산과 염기를 구별한다.</li>
    <li>이온화 상수로 산과 염기의 상대적 세기를 추론하고, 약산과 약염기 수용액의 pH를 구한다.</li>
    <li>중화 적정 실험의 pH 변화를 데이터에 근거하여 해석한다.</li>
    <li>이온화 상수로 염의 가수 분해를 설명한다.</li>
    <li>화학 평형으로 생체 내 완충 작용을 설명한다.</li>''',
'''    <li><b>지식·이해</b> 브뢴스테드·라우리 산과 염기를 구분하고, 이온화 상수를 이용해 약산과 약염기 수용액의 pH를 구하는 방법과 염의 가수 분해를 설명할 수 있다.</li>
    <li><b>과정·기능</b> 이온화 상수를 이용해 산과 염기의 상대적인 세기를 추론하고, 중화 적정 실험의 pH 변화를 시각화하고 해석할 수 있다.</li>
    <li><b>가치·태도</b> 생체 내 완충 작용과 지구 생태의 지속가능성을 산 염기 평형의 관점에서 이해하려는 태도를 가질 수 있다.</li>''')
R('''<div class="note mt12">이 단원의 모든 내용은 <b>화학 평형</b>이 바탕이다. 산과 염기의 반응도 정반응과 역반응이 함께 일어나는 가역 반응으로 본다.</div>''',
'''<div class="note mt12"><b>포트폴리오</b> 이 단원을 학습하면서 나만의 특기를 발휘한 포트폴리오를 만들어 보자. — 28쪽 생활 속 과학 이야기 · 29쪽 화학과 나의 미래 · 34–35쪽 프로젝트</div>''')
# S4
R('<li><b>짝산–짝염기 쌍</b>과','<li><b>짝산·짝염기 쌍</b>과')
R('<div class="fnode">짝산과 짝염기</div>','<div class="fnode">짝산·짝염기 쌍</div>')
# S5 생각 열기 -> 교과서 도입 질문
a=s.index('<!-- ════════ 5. 생각 열기'); b=s.index('<!-- ════════ 6. 연결')
s=s[:a]+'''<!-- ════════ 5. 생각 열기 ════════ -->
<section class="slide" data-sec="01 산과 염기 · 도입" data-title="생각 열기: 제빵 소다는 왜 염기일까?">
  <h2><span class="tag">생각 열기</span>제빵 소다는 왜 염기의 성질을 띨까?</h2>
  <div class="row">
    <div class="col">
      <div class="card"><p class="f22">제빵 소다($\\ce{NaHCO3}$)를 물에 녹여 맛보니 <b>쓴맛</b>이 나고, 손으로 만져 보니 <b>미끈거리는</b> 느낌이 났다.</p>
        <p class="f22 mt12">그런데 제빵 소다의 화학식에는 수산화 이온($\\ce{OH-}$)이 포함되어 있지 않다.</p></div>
      <div class="formula sm mt12">$\\ce{NaHCO3(aq) -> Na+(aq) + HCO3-(aq)}$</div>
      <p class="small center">물에 녹으면 $\\ce{Na+}$과 $\\ce{HCO3-}$으로 나뉜다 — 어디에도 $\\ce{OH-}$이 없다.</p>
    </div>
    <div class="col" style="flex:0 0 470px">
      <h3>알고 있는 낱말에 ✓</h3>
      <div class="chips"><button class="chk">산</button><button class="chk">염기</button><button class="chk">$\\ce{H+}$</button><button class="chk">$\\ce{OH-}$</button><button class="chk">중화 반응</button></div>
      <div class="note q mt16"><b>안전</b> 실험실에서는 물질을 맛보거나 맨손으로 만지지 않는다. 염기 수용액은 미끈거리므로 장갑을 낀다.</div>
    </div>
  </div>
  <p class="f22 mt12" data-q><b>Q</b> 제빵 소다의 화학식에는 $\\ce{OH-}$이 없는데 왜 염기의 성질이 나타날까?</p>
  <div class="answer step">$\\ce{HCO3-}$이 물 분자에게서 <b>$\\ce{H+}$을 받으면</b> $\\ce{OH-}$이 생긴다. <span class="small">— 이것을 설명하려면 $\\ce{OH-}$을 내놓는 물질만 염기로 보는 정의를 넓혀야 한다(해 보기에서 확인).</span></div>
</section>

'''+s[b:]
# S6
R('<p class="f22">물에 녹아 $\\ce{H+}$을 내놓는 물질</p>','<p class="f22">물에 녹았을 때 수소 이온($\\ce{H+}$)을 내놓는 물질</p>')
R('<p class="f22">물에 녹아 $\\ce{OH-}$을 내놓는 물질</p>','<p class="f22">물에 녹았을 때 수산화 이온($\\ce{OH-}$)을 내놓는 물질</p>')
R('<h2><span class="tag alt">연결</span>아레니우스 정의 다시 보기</h2>','<h2><span class="tag alt">연결</span>아레니우스 정의 다시 보기</h2>\n  <p class="small">스웨덴의 과학자 아레니우스가 정의하였다. 이 정의는 수용액에만 적용된다.</p>')
# data-sec
R('data-sec="01 · 브뢴스테드·라우리 산 염기"','data-sec="01 · 브뢴스테드·라우리 산과 염기"',5)
R('data-sec="01 · 짝산과 짝염기"','data-sec="01 · 짝산·짝염기 쌍"',2)
# S7
R('<p class="f21 step" data-g="l2">→ <span class="ans">수용액이 아니므로 아레니우스 정의로는 설명할 수 없다.</span></p>',
  '<p class="f21 step" data-g="l2">→ <span class="ans">아레니우스 정의는 수용액에만 적용되므로 이 반응은 설명할 수 없다.</span></p>')
# S8
R('<h2><span class="no">1</span>브뢴스테드·라우리 산 염기 정의</h2>','<h2><span class="no">1</span>브뢴스테드·라우리 산과 염기</h2>')
R('<mark>산은 양성자($\\ce{H+}$)를 내놓는 물질(양성자 주개)이고, 염기는 양성자를 받는 물질(양성자 받개)이다.</mark>',
  '<mark>다른 물질에 양성자($\\ce{H+}$)를 제공하는 물질을 <b>산</b>, 다른 물질로부터 양성자($\\ce{H+}$)를 제공받는 물질을 <b>염기</b>라고 한다.</mark>')
R('<p class="small">수소 원자는 양성자 1개와 전자 1개로 되어 있어, 전자를 잃으면 양성자만 남는다.</p>',
  '<p class="small">양성자와 전자를 하나씩 가진 수소 원자가 전자를 잃으면 양성자만 남는다. 그래서 브뢴스테드·라우리 정의에서는 수소 이온($\\ce{H+}$)을 양성자($\\ce{H+}$)로 표현하기도 한다.</p>')
R('<p class="small mt12">1923년 덴마크의 브뢴스테드와 영국의 라우리가 각각 제안하였다.</p>',
  '<p class="small mt12">1923년 덴마크의 과학자 브뢴스테드가 아레니우스의 정의보다 확장된 산과 염기 정의를 발표했고, 같은 시기에 영국의 과학자 라우리도 같은 이론을 발표했다.</p>')
# S9 title fig label
R('<h2><span class="no">1</span>염화 수소가 물에 녹을 때</h2>','<h2><span class="no">1</span>염화 수소가 물에 녹을 때 <span class="small">(그림 Ⅰ-1)</span></h2>')
R('<div class="answer step" data-g="g1">물은 $\\ce{H+}$을 받으므로 <b>염기</b>이다. 아레니우스 정의에서는 볼 수 없던 물의 역할이다.</div>',
  '<div class="answer step" data-g="g1">염화 수소는 물에 양성자($\\ce{H+}$)를 제공하므로 <b>산</b>, 물은 염화 수소로부터 양성자를 제공받으므로 <b>염기</b>로 작용한다.</div>')
# S11 해 보기 흰 연기 -> 자료 읽기 그림 I-2
a=s.index('<!-- ════════ 11. 해 보기'); b=s.index('<!-- ════════ 12. 확인하기')
s=s[:a]+'''<!-- ════════ 11. 자료 읽기: 그림 Ⅰ-2 ════════ -->
<section class="slide" data-sec="01 · 자료 읽기" data-title="자료 읽기: 염화 수소와 암모니아의 반응">
  <h2><span class="tag">자료 읽기</span>염화 수소와 암모니아의 반응 <span class="small">(그림 Ⅰ-2)</span></h2>
  <div class="row">
    <div class="col" style="flex:0 0 340px">
      <svg class="fig" viewBox="0 0 320 340" style="width:320px" aria-label="염화 수소의 수소 이온이 암모니아로 옮겨 가 암모늄 이온과 염화 이온이 된다">
        {{nh4cl}}
      </svg>
    </div>
    <div class="col">
      <p class="f22">브뢴스테드·라우리 정의를 이용하면 염화 수소($\\ce{HCl}$)와 암모니아($\\ce{NH3}$)의 반응처럼 <b>수용액이 아닌 상태</b>에서 일어나는 반응도 산 염기 반응으로 설명할 수 있다.</p>
      <div class="formula sm mt12">$\\ce{HCl(g) + NH3(g) -> NH4Cl(s)}$</div>
      <p class="f22 mt12" data-q><b>Q</b> 그림 Ⅰ-2에서 브뢴스테드·라우리 산과 염기로 작용한 물질을 찾아보자.</p>
      <table class="tight rm11-tb mt8">
        <tr><th style="width:200px">산</th><th style="width:200px">염기</th></tr>
        <tr><td><span class="blank"><span class="step" data-g="t2">$\\ce{HCl}$</span></span></td><td><span class="blank"><span class="step" data-g="t2">$\\ce{NH3}$</span></span></td></tr>
      </table>
      <p class="f21 mt12 step" data-g="t3">$\\ce{HCl}$은 $\\ce{NH3}$에 양성자($\\ce{H+}$)를 제공하고, $\\ce{NH3}$는 이를 제공받는다. 생긴 $\\ce{NH4+}$과 $\\ce{Cl-}$이 이온 결합 고체 $\\ce{NH4Cl}$(흰 연기)을 이룬다.</p>
    </div>
  </div>
</section>

<!-- ════════ 12. 해 보기: 브뢴스테드·라우리 산과 염기 구분하기 ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기: 브뢴스테드·라우리 산과 염기 구분하기">
  <h2><span class="tag">해 보기</span>브뢴스테드·라우리 산과 염기 구분하기</h2>
  <p class="f22">탄산수소 이온($\\ce{HCO3-}$)이 물에 녹으면 다음과 같은 평형을 이룬다.</p>
  <table class="rm11-hb mt8">
    <tr><td>$\\ce{HCO3-(aq)}$</td><td>$+$</td><td>$\\ce{H2O(l)}$</td><td>$\\ce{&lt;=&gt;}$</td><td>$\\ce{H2CO3(aq)}$</td><td>$+$</td><td>$\\ce{OH-(aq)}$</td></tr>
    <tr><td><span class="blank"><span class="step" data-g="h1"><b class="c-minus">염기</b></span></span></td><td></td><td><span class="blank"><span class="step" data-g="h1"><b class="c-plus">산</b></span></span></td><td></td><td><span class="blank"><span class="step" data-g="h2"><b class="c-plus">산</b></span></span></td><td></td><td><span class="blank"><span class="step" data-g="h2"><b class="c-minus">염기</b></span></span></td></tr>
  </table>
  <p class="f21 mt12" data-q><b>1.</b> 정반응에서 브뢴스테드·라우리 산과 염기로 작용한 물질을 찾아 빈칸에 각각 써 보자.</p>
  <p class="f21 mt8" data-q><b>2.</b> 역반응에서 브뢴스테드·라우리 산과 염기로 작용한 물질을 찾아 빈칸에 각각 써 보자.</p>
  <p class="f21 mt8" data-q><b>3.</b> 1의 산과 2의 염기, 2의 산과 1의 염기를 각각 짝 짓고, 어떤 관계가 있는지 설명해 보자.</p>
  <div class="answer step" data-g="h3"><b>3</b> <span class="rm11-p2">$\\ce{H2O}$ – $\\ce{OH-}$</span>, <span class="rm11-p1">$\\ce{H2CO3}$ – $\\ce{HCO3-}$</span> — 두 물질은 양성자($\\ce{H+}$) 하나만큼 차이 나며, 양성자를 주고받아 서로 바뀐다.</div>
</section>

'''+s[b:]
# old S12 확인하기 (invented) 제거
a=s.index('<!-- ════════ 12. 확인하기: 산과 염기 찾기'); b=s.index('<!-- ════════ 13. 짝산과 짝염기')
s=s[:a]+s[b:]
# S13
R('<h2><span class="no">2</span>짝산과 짝염기</h2>','<h2><span class="no">2</span>짝산·짝염기 쌍</h2>')
R('data-title="짝산과 짝염기"','data-title="짝산·짝염기 쌍"')
R('<mark>$\\ce{H+}$ 하나의 이동으로 서로 바뀌는 산과 염기의 쌍을 짝산–짝염기 쌍이라고 한다.</mark>',
  '<mark>$\\ce{HCO3-}$과 $\\ce{H2CO3}$, $\\ce{H2O}$과 $\\ce{OH-}$처럼 양성자($\\ce{H+}$)의 이동이 일어나는 한 쌍의 산과 염기를 <b>짝산·짝염기 쌍</b>이라고 한다.</mark>')
R('aria-label="아세트산과 물의 반응식 아래에 산1, 염기2, 염기1, 산2를 쓰고 짝산–짝염기 쌍을 괄호선으로 이은 그림"',
  'aria-label="탄산수소 이온과 물의 반응식 아래에 염기1, 산2, 산1, 염기2를 쓰고 짝산·짝염기 쌍을 괄호선으로 이은 그림"')
R('<p class="f21 step" data-g="g1"><b>정반응</b> $\\ce{CH3COOH}$가 $\\ce{H2O}$에게 $\\ce{H+}$을 내준다.</p>',
  '<p class="f21 step" data-g="g1"><b>정반응</b> $\\ce{H2O}$이 $\\ce{HCO3-}$에게 $\\ce{H+}$을 제공한다.</p>')
R('<p class="f21 step" data-g="g2"><b>역반응</b> $\\ce{H3O+}$이 $\\ce{CH3COO-}$에게 $\\ce{H+}$을 내준다 — 역반응에도 산과 염기가 있다.</p>',
  '<p class="f21 step" data-g="g2"><b>역반응</b> $\\ce{H2CO3}$이 $\\ce{OH-}$에게 $\\ce{H+}$을 제공한다 — 역반응에도 산과 염기가 있다.</p>')
R('<div class="note step mt8" data-g="g3">$\\ce{CH3COO-}$은 $\\ce{CH3COOH}$의 <b>짝염기</b>, $\\ce{CH3COOH}$는 $\\ce{CH3COO-}$의 <b>짝산</b>이다. $\\ce{H2O}$와 $\\ce{H3O+}$도 짝산–짝염기 쌍이다.</div>',
  '<div class="note step mt8" data-g="g3">$\\ce{HCO3-}$은 $\\ce{H2CO3}$의 <b>짝염기</b>, $\\ce{H2CO3}$은 $\\ce{HCO3-}$의 <b>짝산</b>이다. $\\ce{OH-}$은 $\\ce{H2O}$의 짝염기이다.</div>')
# S14, S15, S16
R('data-title="짝산–짝염기 쌍 찾기"','data-title="짝산·짝염기 쌍 찾기"')
R('<h2><span class="no">2</span>짝산–짝염기 쌍 찾기</h2>','<h2><span class="no">2</span>짝산·짝염기 쌍 찾기</h2>')
R('aria-label="플루오린화 수소와 암모니아의 반응식 아래에 산과 염기, 짝산–짝염기 쌍을 표시한 그림"','aria-label="플루오린화 수소와 암모니아의 반응식 아래에 산과 염기, 짝산·짝염기 쌍을 표시한 그림"')
R('짝산–짝염기 쌍을 모두 찾아보자.','짝산·짝염기 쌍을 모두 찾아보자.')
R('''<!-- ════════ 16. 확인하기: 짝산–짝염기 표 ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-tpl="check" data-title="확인하기: 짝산과 짝염기 쓰기">
  <h2><span class="tag q">확인하기</span>짝산과 짝염기 쓰기</h2>''',
'''<!-- ════════ 16. 연습 해 보기: 짝산·짝염기 표 ════════ -->
<section class="slide" data-sec="01 · 연습 해 보기" data-tpl="check" data-title="연습 해 보기: 짝산과 짝염기 쓰기">
  <h2><span class="tag ex">연습 해 보기</span>짝산과 짝염기 쓰기</h2>''')
# S17
R('<mark>반응하는 물질에 따라 산으로도, 염기로도 작용하는 물질을 양쪽성 물질이라고 한다.</mark>',
  '<mark>물처럼 산으로도 작용할 수 있고 염기로도 작용할 수 있는 물질을 <b>양쪽성 물질</b>이라고 한다.</mark>')
# S19
R('<h2><span class="no">1</span>두 정의 비교 — 확장성과 유용성</h2>','<h2><span class="no">1</span>산과 염기 정의의 확장 — 두 정의 비교</h2>')
R('<td class="step" data-g="v1">$\\ce{H+}$을 내놓음 (주개)</td>','<td class="step" data-g="v1">다른 물질에 $\\ce{H+}$을 제공함</td>')
R('<td class="step" data-g="v1">$\\ce{H+}$을 받음 (받개)</td>','<td class="step" data-g="v1">다른 물질로부터 $\\ce{H+}$을 제공받음</td>')
# 확인하기(교과서) 삽입: 실험실 앞
R('<!-- ════════ 20. 실험실 ════════ -->','''<!-- ════════ 확인하기 (교과서) ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-tpl="check" data-title="확인하기">
  <h2><span class="tag q">확인하기</span>브뢴스테드·라우리 산과 염기</h2>
  <p class="f22 mt12" data-q><b>1</b> 브뢴스테드·라우리 정의에 따르면 다른 물질에 양성자($\\ce{H+}$)를 제공하는 물질은 ( <span class="blank"><span class="step">산</span></span> ), 다른 물질로부터 양성자($\\ce{H+}$)를 제공받는 물질은 ( <span class="blank"><span class="step">염기</span></span> )이다.</p>
  <p class="f22 mt28" data-q><b>2</b> 양성자($\\ce{H+}$)의 이동이 일어나는 한 쌍의 산과 염기를 ( <span class="blank rm11-w1"><span class="step">짝산·짝염기 쌍</span></span> )(이)라고 한다.</p>
  <div class="note mt28">$\\ce{HCO3-(aq) + H2O(l) <=> H2CO3(aq) + OH-(aq)}$ — <span class="rm11-p1">$\\ce{HCO3-}$/$\\ce{H2CO3}$</span>, <span class="rm11-p2">$\\ce{H2O}$/$\\ce{OH-}$</span>가 짝산·짝염기 쌍이다.</div>
</section>

<!-- ════════ 20. 실험실 ════════ -->''')
R('<tr><th>짝산–짝염기 쌍</th>','<tr><th>짝산·짝염기 쌍</th>')
R('<th>짝산–짝염기 쌍</th></tr></thead>','<th>짝산·짝염기 쌍</th></tr></thead>')
# S23
R('$\\ce{NH3}$는 물에게서 $\\ce{H+}$을 받으므로(양성자 받개) 브뢴스테드·라우리 염기이고','$\\ce{NH3}$는 물로부터 $\\ce{H+}$을 제공받으므로 브뢴스테드·라우리 염기이고')
# S24 소단원 마무리
a=s.index('<!-- ════════ 24. 소단원 마무리'); b=s.index('<!-- ════════ 25. 스스로 정리')
s=s[:a]+'''<!-- ════════ 24. 소단원 마무리 ════════ -->
<section class="slide" data-sec="01 · 소단원 마무리" data-title="소단원 마무리">
  <h2><span class="tag">소단원 마무리</span>아레니우스 염기와 브뢴스테드·라우리 염기</h2>
  <div class="row">
    <div class="col">
      <div class="card"><h3>창의력 키우기</h3>
        <p class="f21">수산화 나트륨($\\ce{NaOH}$)은 물($\\ce{H2O}$)에 녹아 수산화 이온($\\ce{OH-}$)을 내놓는 아레니우스 염기이다. 수산화 나트륨을 브뢴스테드·라우리 염기로 정의할 수 있을지 토의해 보자.</p>
        <p class="small mt8 step">토의 실마리: $\\ce{NaOH}$가 내놓은 $\\ce{OH-}$은 $\\ce{H3O+}$에게서 양성자를 제공받는다($\\ce{OH- + H3O+ -> 2H2O}$). 양성자를 직접 받는 것은 $\\ce{NaOH}$인가, $\\ce{OH-}$인가?</p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h3>디지털 소양 키우기</h3>
        <p class="f21">아레니우스 산과 염기 정의로 설명할 수 없지만, 브뢴스테드·라우리 산과 염기 정의로 설명할 수 있는 화학 반응식을 조사하고 발표해 보자.</p>
        <p class="small mt8 step">예: $\\ce{HCl(g) + NH3(g) -> NH4Cl(s)}$ (수용액이 아님), $\\ce{HCO3- + H2O <=> H2CO3 + OH-}$ ($\\ce{OH-}$을 가지지 않은 염기). 조사한 자료의 출처를 밝히고, 원자 수와 전하가 맞는지 확인한다.</p>
      </div>
    </div>
  </div>
</section>

'''+s[b:]
# S25, S26
R('<span class="step">양성자($\\ce{H+}$)를 내놓는 물질</span>','<span class="step">양성자($\\ce{H+}$)를 제공하는 물질</span>')
R('<span class="step">양성자를 받는 물질</span>','<span class="step">양성자($\\ce{H+}$)를 제공받는 물질</span>')
R('<span class="step">짝산–짝염기</span>','<span class="step">짝산·짝염기</span>')
R('반응식에서 짝산–짝염기 쌍을 찾아 표시할 수 있다.','반응식에서 짝산·짝염기 쌍을 찾아 표시할 수 있다.')
assert '짝산–' not in s, [l for l in s.split('\n') if '짝산–' in l]
assert '주개' not in s and '받개' not in s
open(p,'w',encoding='utf-8').write(s)
print('ok')
