# 교과서 재검토: slides.tpl.html 2단계 — 15쪽 이후 슬라이드 교체·순서 변경
import sys, re
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def blk(start, end):
    i = s.index(start); j = s.index(end)
    return s[i:j]
b15 = blk('<!-- ════════ 15. 확인하기', '<!-- ════════ 16.')
b16 = blk('<!-- ════════ 16.', '<!-- ════════ 17.')
b17 = blk('<!-- ════════ 17.', '<!-- ════════ 18.')
b18 = blk('<!-- ════════ 18.', '<!-- ════════ 19.')
b19 = blk('<!-- ════════ 19.', '<!-- ════════ 20.')
b20 = blk('<!-- ════════ 20.', '<!-- ════════ 21.')
b21 = blk('<!-- ════════ 21.', '<!-- ════════ 22.')
b22 = blk('<!-- ════════ 22.', '<!-- ════════ 23.')
tail = s[s.index('<!-- ════════ 23.'):s.index('<!-- ════════ 30.')]
rest = s[s.index('<!-- ════════ 30.'):]
head = s[:s.index('<!-- ════════ 15. 확인하기')]

N17 = '''<!-- ════════ 17. 항생제와 백신 ════════ -->
<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="항생제와 백신의 개발">
  <h2><span class="no">4</span>항생제와 백신의 개발</h2>
  {{timeline}}
  <div class="row mt12">
    <div class="col"><div class="card"><h3>항생제</h3><p class="f21">과거에는 세균이나 바이러스로 인한 <b>감염병</b>으로 사망하는 사람이 많았다. 최초의 항생제인 <b>페니실린</b>이 발견된 후, 페니실린의 <b>분자 구조를 변형</b>하여 성능을 개량한 항생제가 대량 생산되면서 수많은 사람의 목숨을 구했다.</p></div></div>
    <div class="col"><div class="card step"><h3>백신</h3><p class="f21">백신에 사용되는 생체 물질의 구조 일부분을 화학적으로 <b>합성, 변형</b>하여 백신이 인체 내에서 잘 작용하게 만드는 기술은 새로운 감염병에 대응하는 백신을 <b>빠르게 개발</b>하는 데 도움을 주었다.</p></div></div>
  </div>
  <div class="answer step mt12">→ 화학은 감염병을 이겨 내고 인류의 <b>수명을 늘리는</b> 데 기여하였다.</div>
</section>

'''
N15 = '''<!-- ════════ 15. 확인하기 (교과서 15쪽) ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 화학과 우리 사회의 발전" data-tpl="check">
  <h2><span class="tag q">확인하기</span>화학과 우리 사회의 발전</h2>
  <ol class="cm111-ox mt8">
    <li class="f22">( <span class="blank"><span class="step">암모니아</span></span> ) 합성법이 개발되면서 인류의 식량 생산량이 늘어났다.</li>
    <li class="f22">최초의 항생제로, 감염병을 치료하는 데 사용한 물질은 무엇인지 써 보자. <span class="blank"><span class="step">페니실린</span></span></li>
  </ol>
  <h3 class="mt16">더 확인하기 — 옳은 것은 ○, 옳지 않은 것은 ×</h3>
  <ol class="cm111-ox">
    <li class="f22">공기 중의 질소 $\\ce{N2}$는 식물이 직접 흡수해 쓸 수 있다. <span class="blank"><span class="step">× — 암모니아 등으로 바꾸어야 쓸 수 있다</span></span></li>
    <li class="f22">나일론과 같은 합성 섬유는 대량 생산이 어려워 천연 섬유를 대체하지 못했다. <span class="blank"><span class="step">× — 대량 생산할 수 있고 수명이 길다</span></span></li>
    <li class="f22">철의 제련에서 산화 철(III)은 산소를 잃고 철이 된다. <span class="blank"><span class="step">○</span></span></li>
  </ol>
</section>

'''
N16 = '''<!-- ════════ 16. 지속가능한 미래를 만드는 화학 ════════ -->
<section class="slide" data-sec="01 · 지속가능한 미래를 만드는 화학" data-title="지속가능한 미래를 만드는 화학">
  <h2>지속가능한 미래를 만드는 화학</h2>
  <p class="f22">과학기술이 발전하면서 인류는 이전에 경험하지 못한 편리함을 누리고 있다. 하지만 <b>화석 연료</b>를 과도하게 사용하면서 이산화 탄소 등 <b>온실 가스</b>의 배출량이 크게 증가해 <b class="c-plus">급격한 기후 변화</b>라는 위기를 맞게 되었다.</p>
  <p class="f22 mt12"><b>Q</b> 이러한 문제를 극복하기 위해 화학은 어떤 역할을 하고 있을까?</p>
  <table class="tight mt12 cm111-new">
    <tr><th>화학의 역할</th><th>예</th></tr>
    <tr><td class="l step" data-g="n1">⑤ 화석 연료의 사용을 줄이고 <b>대체 에너지</b>의 사용을 늘려 이산화 탄소 배출을 줄인다</td><td class="l step" data-g="n1">에너지 효율이 높은 태양 전지 소재 개발</td></tr>
    <tr><td class="l step" data-g="n2">⑥ 대기 중에 방출된 <b>이산화 탄소의 농도를 낮춘다</b></td><td class="l step" data-g="n2">탄소 포집·활용·저장(CCUS) 기술</td></tr>
  </table>
  <div class="answer step">화학은 인류의 <b>지속가능한 미래</b>를 만드는 일에서 핵심적인 역할을 한다.</div>
</section>

'''
# 18 에너지: 태양 전지를 앞으로
b18 = b18.replace('data-sec="01 · 화학과 현대 사회" data-title="화학과 에너지"', 'data-sec="01 · 지속가능한 미래를 만드는 화학" data-title="대체 에너지와 화학"')
b18 = b18.replace('<h2><span class="no">5</span>화학과 에너지</h2>', '<h2><span class="no">5</span>대체 에너지와 화학</h2>')
old_cards = b18[b18.index('      <h3>새로운 에너지</h3>'):b18.index('      <div class="answer step mt12">')]
b18 = b18.replace(old_cards, '''      <h3>대체 에너지</h3>
      <div class="card step" data-g="e1"><p class="f21"><b>태양 전지</b> 햇빛을 전기로 바꾼다. 에너지 효율이 높은 <b>태양 전지 소재</b>를 개발하기 위해서는 화학의 역할이 필수적이다.</p></div>
      <div class="card step mt8" data-g="e2"><p class="f21"><b>수소 연료 전지</b> 수소와 산소가 반응하여 전기를 만들고 물만 생긴다.</p><div class="formula sm cm111-eq2">$\\ce{2H2(g) + O2(g) -> 2H2O(l)}$</div></div>
      <div class="card step mt8" data-g="e2"><p class="f21"><b>화학 전지</b> 리튬 이온 전지처럼 전기를 저장해 여러 번 충전해 쓴다.</p></div>
''')
b18 = b18.replace('화학은 에너지를 얻는 새로운 물질과 반응을 찾아 <b>지속가능한 에너지</b> 문제 해결에 기여한다.', '화학은 화석 연료 사용을 줄이고 <b>대체 에너지</b> 사용을 늘려 이산화 탄소 배출을 줄이는 데 기여한다.')
N19 = '''<!-- ════════ 19. 탄소 포집·활용·저장 ════════ -->
<section class="slide" data-sec="01 · 지속가능한 미래를 만드는 화학" data-title="탄소 포집·활용·저장(CCUS)">
  <h2><span class="no">6</span>탄소 포집·활용·저장(CCUS) 기술</h2>
  <p class="f22">대기 중에 방출된 이산화 탄소의 농도를 낮추는 기술인 <b>탄소 포집·활용·저장</b>(CCUS, Carbon Capture·Utilization·Storage) 기술을 발전시키는 데도 화학이 중요한 역할을 한다.</p>
  <div class="stages mt8">
    <div class="stage"><h3>포집</h3>{{cc1}}<p>공장이나 발전소에서 나오는 $\\ce{CO2}$를 모은다.</p></div>
    <div class="stage"><h3>활용</h3>{{cc2}}<p>포집한 $\\ce{CO2}$로 <b>섬유나 건축 자재</b> 등 유용한 물질을 만든다.</p></div>
    <div class="stage"><h3>저장</h3>{{cc3}}<p>$\\ce{CO2}$가 대기 중으로 빠져나가지 못하도록 <b>땅속 깊이</b> 저장한다.</p></div>
  </div>
  <div class="answer step mt12">이 기술들에는 <b>이산화 탄소와 관련된 화학 반응</b>이 이용된다.</div>
</section>

'''
N19b = '''<!-- ════════ 19b. 확인하기 (교과서 17쪽) ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 지속가능한 미래를 만드는 화학" data-tpl="check">
  <h2><span class="tag q">확인하기</span>지속가능한 미래를 만드는 화학</h2>
  <ol class="cm111-ox mt12">
    <li class="f22">에너지 효율이 높은 태양 전지 소재를 개발하는 데 ( <span class="blank"><span class="step">화학</span></span> )이/가 이용된다.</li>
    <li class="f22">대기 중에 방출된 ( <span class="blank"><span class="step">이산화 탄소</span></span> )의 농도를 낮추는 탄소 포집·활용·저장 기술에 화학이 활용된다.</li>
  </ol>
  <div class="note puzzle step mt16"><b>생각해 보기</b> 기후 변화의 원인이 된 화석 연료의 연소도 화학 반응이다. 그 문제를 줄이는 물질과 기술을 찾는 것도 화학의 몫이다.</div>
</section>

'''
N21 = '''<!-- ════════ 21. 정리 표 ════════ -->
<section class="slide" data-sec="01 · 지속가능한 미래를 만드는 화학" data-title="정리: 화학이 기여한 사례">
  <h2><span class="tag ink">정리</span>화학이 기여한 사례</h2>
  <table class="tight cm111-sum">
    <tr><th>사례</th><th>인류의 문제</th><th>화학의 기여</th><th>사회의 발전</th></tr>
    <tr><td>① 암모니아의 합성</td><td class="l">식량 부족</td><td class="l step" data-g="r1">질소 비료의 대량 생산</td><td class="l step" data-g="r1">식량 생산량 증가, 원료·냉매로 이용</td></tr>
    <tr><td>② 합성 섬유의 개발</td><td class="l">섬유 수요 증가</td><td class="l step" data-g="r2">대량 생산, 긴 수명, 다양한 기능</td><td class="l step" data-g="r2">천연 섬유 대체, 운동복·우주복</td></tr>
    <tr><td>③ 철의 제련</td><td class="l">이동·생활 공간</td><td class="l step" data-g="r3">철의 대량 생산과 가공</td><td class="l step" data-g="r3">철도·교량·선박, 고층 건물</td></tr>
    <tr><td>④ 항생제와 백신</td><td class="l">감염병</td><td class="l step" data-g="r4">페니실린 구조 변형, 백신 물질 합성</td><td class="l step" data-g="r4">수많은 목숨을 구함, 백신 빠른 개발</td></tr>
    <tr><td>⑤ 대체 에너지</td><td class="l">기후 변화</td><td class="l step" data-g="r5">태양 전지 소재 개발</td><td class="l step" data-g="r5">이산화 탄소 배출 감소</td></tr>
    <tr><td>⑥ CCUS</td><td class="l">기후 변화</td><td class="l step" data-g="r6">$\\ce{CO2}$의 포집·활용·저장</td><td class="l step" data-g="r6">대기 중 $\\ce{CO2}$ 농도 감소</td></tr>
  </table>
</section>

'''
b22 = b22.replace('<h2><span class="tag q">확인하기</span>\'화학 물질\'은 모두 몸에 해로울까?</h2>', '<h2><span class="tag">생각해 보기</span>\'화학 물질\'은 모두 몸에 해로울까?</h2>')
b22 = b22.replace('data-sec="01 · 확인하기" data-title="화학 물질은 모두 해로울까?"', 'data-sec="01 · 지속가능한 미래를 만드는 화학" data-title="생각해 보기: 화학 물질은 모두 해로울까?"')
assert '생각해 보기</span>' in b22 and 'data-title="생각해 보기' in b22
s = head + N17 + N15 + N16 + b18 + N19 + N19b + N21 + b22 + tail + rest
open(p, 'w', encoding='utf-8').write(s)
print('ok')
