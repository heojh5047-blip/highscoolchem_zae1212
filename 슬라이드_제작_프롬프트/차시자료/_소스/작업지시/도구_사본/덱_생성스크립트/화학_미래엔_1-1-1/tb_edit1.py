# 교과서 재검토: slides.tpl.html 문장 교체 (1단계 — 앞부분)
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
R = []
def r(a, b):
    R.append((a, b))
r('<p class="meta">고등학교 화학 13–17쪽</p>', '<p class="meta">고등학교 화학 10–17쪽, 27–28쪽</p>')
# S2 대단원 도입
r('''  <p class="f22">화학자들은 원소 기호, 화학식, 화학 반응식, 몰이라는 <b>공통의 언어</b>로 물질과 그 변화를 이야기한다. 이 단원에서는 화학이 우리 삶에 얼마나 쓸모 있는지 알아보고, 화학의 언어인 <b>몰</b>과 <b>화학 반응식</b>으로 물질의 양과 반응의 양적 관계를 나타내 본다.</p>''',
  '''  <p class="f22">화학 실험을 수행할 때는 물질의 양을 정확하게 나타내는 것이 중요하다. <b>화학에서 물질의 양은 어떻게 표현할까?</b></p>''')
r('''<p class="f21"><b>핵심 아이디어</b> 몰은 화학 반응에 참여하는 물질의 양을 나타내는 단위로, 과학·공학·의학 등에서 <b>표준화된 소통의 도구</b>로 활용된다.</p>''',
  '''<p class="f21"><b>이 단원의 핵심 아이디어</b> 몰은 화학 반응에 참여하는 물질의 양을 나타내는 <b>표준 단위</b>이다. 이 단원에서 물질의 양을 몰 단위로 나타내고, 몰이 과학·공학·의학 등 화학 반응과 관련된 여러 분야에서 <b>소통의 도구</b>로 활용되고 있음을 알아보자.</p>''')
# S3 포트폴리오
r('''      <table class="tight cm111-pf">
        <tr><th>소단원</th><th>모을 것</th></tr>
        <tr><td>1-01</td><td class="l">화학이 기여한 사례 조사·발표 자료 <b>(오늘)</b></td></tr>
        <tr><td>1-02</td><td class="l">몰 환산 카드 (입자 수·질량·기체의 부피)</td></tr>
        <tr><td>2-01</td><td class="l">화학 반응식 쓰기 카드</td></tr>
        <tr><td>2-02</td><td class="l">화학 반응의 양적 관계 실험 보고서</td></tr>
      </table>
      <p class="small mt8">포트폴리오는 배운 것을 모아 두고 스스로 성장을 돌아보는 기록이다. 단원이 끝날 때 다시 펼쳐 본다.</p>''',
  '''      <p class="f21">이 단원을 학습하면서 <b>나만의 특기를 발휘한 포트폴리오</b>를 만들어 보자.</p>
      <table class="tight cm111-pf mt8">
        <tr><th>쪽</th><th>포트폴리오 활동</th></tr>
        <tr><td>26쪽</td><td class="l">최신 과학 이야기</td></tr>
        <tr><td>40쪽</td><td class="l">화학과 나의 미래</td></tr>
        <tr><td>48–49쪽</td><td class="l">프로젝트</td></tr>
      </table>
      <p class="small mt8">오늘 「해 보기」에서 만든 조사·발표 자료도 함께 모아 두고, 단원이 끝날 때 다시 펼쳐 본다.</p>''')
# S4 중단원 도입
r('''  <div class="card q"><p class="f22">우리 주변의 물건은 화학과 어떤 관계가 있을까? 그리고 셀 수 없이 작은 원자와 분자의 양은 어떻게 나타낼까?</p></div>''',
  '''  <div class="card q"><p class="f22">캠핑할 때 사용하는 텐트, 연료 등은 모두 화학과 관련되어 있다. <b>우리 생활에서 화학과 관련된 또 다른 물건에는 어떤 것이 있을까?</b></p></div>''')
r('''        <tr><th>소단원</th><th>배울 것</th><th>쪽</th></tr>
        <tr class="cm111-cur"><td>01 화학과 현대 과학·기술·사회</td><td class="l">화학이 인류의 문제를 해결한 사례를 조사·발표하기</td><td><b>13–17 (오늘)</b></td></tr>
        <tr><td>02 몰과 물질의 양</td><td class="l">입자 수·질량·기체의 부피를 몰로 나타내기</td><td>18–26</td></tr>''',
  '''        <tr><th>소단원</th><th>이 단원의 핵심 내용</th><th>쪽</th></tr>
        <tr class="cm111-cur"><td>01 화학과 현대 과학·기술·사회</td><td class="l">화학과 현대 과학·기술·사회</td><td><b>13–17 (오늘)</b></td></tr>
        <tr><td>02 몰과 물질의 양</td><td class="l">몰 · 몰질량 · 몰과 기체의 부피</td><td>18–26</td></tr>''')
r('''<div class="col"><div class="note big">매일 쓰는 물건 하나하나에 화학이 들어 있다. 오늘은 화학이 <b>어떤 문제를 어떻게 해결했는지</b> 사례를 찾아본다.</div></div>''',
  '''<div class="col"><h3>이전 학습 내용 — 알고 있는 내용에 ✓</h3><div class="chips"><button class="chk">원소</button><button class="chk">원자</button><button class="chk">분자</button><button class="chk">화합물</button></div>
      <p class="small mt8"><b>이 단원의 학습 목표</b> [지식·이해] 화학이 현대 과학·기술·사회에 미친 영향을 알고, 몰을 이용해 물질의 양을 표현할 수 있다. [과정·기능] 화학이 기여한 사례를 조사하고, 물질의 몰질량을 탐색할 수 있다. [가치·태도] 화학의 유용성을 깨닫고, 몰이 유용한 단위임을 인식할 수 있다.</p></div>''')
# S5 학습 목표
r('''    <li>화학이 <b>식량·의류·주거</b> 문제를 해결하는 데 기여한 사례를 설명할 수 있다.</li>
    <li>화학이 <b>건강·에너지·환경·첨단 기술</b> 등 현대 과학·기술·사회의 발전에 기여한 사례를 설명할 수 있다.</li>
    <li>화학이 기여한 사례를 <b>조사·발표</b>하며 화학을 배워야 하는 까닭을 말할 수 있다.</li>''',
  '''    <li>화학이 <b>인류의 문제를 해결한 사례</b>를 제시할 수 있다.</li>
    <li>화학이 <b>과학·기술·사회의 발전에 기여한 사례</b>를 설명할 수 있다.</li>
    <li>화학 관련 일상생활 문제를 인식하고, 이를 <b>과학적으로 해결</b>하려는 태도를 가질 수 있다.</li>''')
r('''    <div class="fnode hl">식량 · 의류 · 주거</div><div class="farr">→</div>
    <div class="fnode hl">건강 · 에너지 · 환경 · 첨단 소재</div><div class="farr">→</div>
    <div class="fnode">조사·발표</div><div class="farr">→</div>
    <div class="fnode">확인 문제</div>''',
  '''    <div class="fnode hl">화학과 우리 사회의 발전</div><div class="farr">→</div>
    <div class="fnode hl">지속가능한 미래를<br>만드는 화학</div><div class="farr">→</div>
    <div class="fnode">해 보기</div><div class="farr">→</div>
    <div class="fnode">중단원 마무리</div>''')
# S6 생각 열기 → 영양제 + S6b 자료 읽기
old6 = s[s.index('<!-- ════════ 6. 생각 열기'):s.index('<!-- ════════ 7. 연결')]
new6 = '''<!-- ════════ 6. 생각 열기: 영양제 ════════ -->
<section class="slide" data-sec="01 화학과 현대 과학·기술·사회 · 도입" data-title="생각 열기: 영양제와 화학">
  <h2><span class="tag">생각 열기</span>영양제를 만드는 과정에서 화학은 어떤 역할을 할까?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 260px"><svg class="fig" viewBox="0 0 240 200" style="width:240px" aria-label="영양제 알약 그림"><circle cx="120" cy="100" r="90" fill="#F4F7FA" stroke="#C9D3DD" stroke-width="2"/>{{pillbig}}</svg></div>
    <div class="col">
      <p class="f22">우리는 주로 음식으로 영양소를 섭취하지만, 영양제로 부족한 영양소를 보충하기도 한다.</p>
      <p class="f22 mt12"><b>Q</b> 알약 하나에 담긴 비타민은 어디에서 왔을까? 영양제를 만드는 과정에서 화학이 하는 일을 떠올려 보자.</p>
      <div class="card tip step mt8"><p class="f21">영양소가 되는 물질의 구조를 밝혀 <b>합성</b>하거나 원료에서 <b>분리·정제</b>하고, 성분의 양을 정확히 재어 알약으로 만든다. 성분이 변하지 않도록 보관하는 방법을 찾는 것도 화학의 일이다.</p></div>
    </div>
  </div>
  <div class="answer step">→ 화학은 우리 생활에 필요한 <b>물질을 만들고</b>, 물질의 성질을 이용해 유용한 <b>기술</b>로 활용한다.</div>
</section>

<!-- ════════ 6b. 자료 읽기: 화학과 우리 생활 ════════ -->
<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="자료 읽기: 화학과 우리 생활">
  <h2><span class="tag">자료 읽기</span>화학과 우리 생활</h2>
  <p class="f22">우리는 합성 섬유로 만든 옷을 입고, 화학 전지로 작동하는 스마트폰으로 소통하며, 아플 때 합성 의약품의 도움을 받는다.</p>
  {{life6}}
  <table class="tight cm111-life">
    <tr><td>유리, 철근 콘크리트로 만든 건물에서 생활한다.</td><td>세탁소에서 세제나 특수 용매로 옷의 오염을 제거한다.</td><td>아플 때 화학 반응으로 합성한 의약품을 복용한다.</td><td>합성 섬유로 만든 기능성 옷을 입는다.</td><td>화학 전지로 작동하는 스마트 기기를 사용한다.</td><td>연료의 연소 반응으로 작동하는 자동차를 탄다.</td></tr>
  </table>
  <p class="f22 mt8"><b>Q</b> 화학의 발전이 없었다면 이 모습이 어떻게 달라질지 이야기해 보자.</p>
  <div class="answer step">예) 건물은 나무와 흙으로, 옷은 천연 섬유로만 만들고, 감염병에 걸려도 치료하기 어렵다 — 화학의 혜택이 없다면 <b>지금과 전혀 다른 삶</b>이 된다.</div>
</section>

'''
s = s.replace(old6, new6)
# S7 hub
r('''<section class="slide" data-sec="01 화학과 현대 과학·기술·사회 · 도입" data-title="화학은 무엇을 연구할까?">
  <h2><span class="tag alt">연결</span>화학은 무엇을 연구할까?</h2>''',
  '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="화학과 우리 사회의 발전">
  <h2>화학과 우리 사회의 발전</h2>''')
r('''      <p class="f22"><mark>화학은 물질의 구성, 구조, 성질과 변화를 연구하는 학문이다.</mark></p>
      <p class="f22 mt12">화학자는 물질을 이루는 원자와 분자를 이해하여 <b>새로운 물질</b>을 만들고, <b>새로운 반응</b>을 찾아낸다.</p>
      <p class="f22 mt16"><b>Q</b> 인구가 늘고 생활이 바뀔 때마다 인류가 먼저 부딪힌 문제는 무엇이었을까?</p>
      <div class="answer step">먹고, 입고, 사는 문제 — <b>식량·의류·주거</b></div>
      <p class="f21 step mt8">→ 화학이 먼저 해결한 의식주 문제부터 살펴보자.</p>''',
  '''      <p class="f22"><mark>화학은 물질의 성질과 변화를 연구하고, 우리 생활에 필요한 물질을 만들거나 물질의 새로운 특성을 발견하여 유용한 기술로 활용하는 학문이다.</mark></p>
      <p class="f22 mt12">화학은 우리의 삶을 편하게 할 뿐만 아니라, 인류가 극복해야 할 문제를 해결하고 인류 문명이 발전하는 데에도 큰 영향을 미쳤다.</p>
      <p class="f22 mt16"><b>Q</b> 인구가 늘면서 인류가 부딪힌 문제는 무엇이었을까?</p>
      <div class="answer step">식량 부족, 옷감 부족, 살 곳과 교통, 감염병 — 화학이 해결한 <b>네 가지 사례</b>를 살펴보자.</div>''')
# S8 식량
r('''<section class="slide" data-sec="01 · 화학과 식량 문제" data-title="식량 문제와 질소">
  <h2><span class="no">1</span>화학과 식량 문제</h2>''',
  '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="암모니아의 합성: 식량 문제와 질소">
  <h2><span class="no">1</span>암모니아의 합성 — 식량 부족 문제</h2>''')
r('''<p class="f22">18세기 이후 세계 인구가 빠르게 늘면서 식량이 부족해졌다.''', '''<p class="f22">산업 혁명 이후 인구가 급격히 증가하면서 인류는 <b>식량 부족 문제</b>에 처했다.''')
r('''<div class="card tip step mt8"><p class="f21">1909년 독일의 <b>하버</b>가 질소와 수소로 <b>암모니아</b>를 합성하는 방법을 개발하였고, <b>보슈</b>가 이를 공장에서 대량으로 생산하는 공정을 완성하였다(1913년 공장 가동). 이것을 <b>하버·보슈 공정</b>이라고 한다.</p></div>''',
  '''<div class="card tip step mt8"><p class="f21">이를 해결한 것은 화학이었다. 20세기 초 공기 중의 질소를 이용한 <b>암모니아 합성법</b>이 개발되었다. 독일의 <b>하버</b>가 질소와 수소로 암모니아를 합성하는 방법을 개발하고(1909년), <b>보슈</b>가 공장에서 대량 생산하는 공정을 완성하여 <b>하버·보슈 공정</b>이라고 부른다.</p></div>''')
r('''<section class="slide" data-sec="01 · 화학과 식량 문제" data-title="하버·보슈 공정">''', '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="하버·보슈 공정">''')
r('''<section class="slide" data-sec="01 · 화학과 식량 문제" data-title="질소 비료와 식량 생산">
  <h2><span class="no">1</span>질소 비료와 식량 생산</h2>''', '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="질소 비료와 암모니아의 쓰임">
  <h2><span class="no">1</span>질소 비료와 암모니아의 쓰임</h2>''')
r('''<div class="card step"><h3 class="c-field">화학이 해결한 것</h3><p class="f21">오늘날 세계 인구의 <b>약 절반</b>이 하버·보슈 공정으로 만든 비료 덕분에 식량을 얻는다고 추정된다.</p></div>''',
  '''<div class="card step"><h3 class="c-field">화학이 해결한 것</h3><p class="f21">질소 비료를 대량으로 생산하게 되어 식량 생산량이 <b>획기적으로</b> 늘어났다. 오늘날 세계 인구의 약 절반이 이 비료 덕분에 식량을 얻는다고 추정된다.</p></div>''')
r('''<div class="note mt16">화학은 농약, 비닐하우스 필름(플라스틱), 식품 포장재와 보존제로도 식량 문제 해결을 돕는다.</div>''',
  '''<div class="note mt16"><b>오늘날 암모니아의 쓰임</b> 비료나 세정제 등 다양한 물질을 생산하는 <b>원료</b>로 쓰고, 아이스크림 공장처럼 냉동 장치를 사용하는 곳에서 <b>냉매</b>로 쓴다.</div>''')
r('''<section class="slide" data-sec="01 · 모의실험" data-title="모의실험: 암모니아 합성 입자 모형">''', '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="모의실험: 암모니아 합성 입자 모형">''')
r('''<h2><span class="tag">모의실험</span>암모니아 합성 입자 모형</h2>''', '''<h2><span class="tag">모의실험</span>암모니아 합성 입자 모형 <span class="small c-muted">더 알아보기 — 시간에 따라 건너뛰어도 된다</span></h2>''')
# S12 섬유
r('''<section class="slide" data-sec="01 · 화학과 의류 문제" data-title="합성 섬유">
  <h2><span class="no">2</span>화학과 의류 문제 — 합성 섬유</h2>''', '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="합성 섬유의 개발">
  <h2><span class="no">2</span>합성 섬유의 개발</h2>''')
r('''<p class="f22">면, 양털, 비단 같은 <b>천연 섬유</b>는 생산량이 기후와 땅의 넓이에 따라 제한되고, 쉽게 해지거나 줄어드는 단점이 있었다.</p>''',
  '''<p class="f22">인구가 증가하면서 옷을 만드는 섬유의 수요도 늘어났지만, 면이나 비단과 같은 <b>천연 섬유</b>로는 이를 충족하기가 어려웠다.</p>''')
r('''<p class="f22 mt8 step" data-g="c1">1930년대에 미국의 <b>캐러더스</b>가 최초의 합성 섬유인 <b>나일론</b>을 개발하였다. 석탄, 물, 공기에서 얻은 원료로 만든 나일론은 '거미줄보다 가늘고 강철보다 강한 섬유'로 소개되었다.</p>''',
  '''<p class="f22 mt8 step" data-g="c1"><b>나일론</b>과 같은 합성 섬유는 천연 섬유와 달리 <b>대량으로 생산</b>할 수 있고 섬유의 <b>수명도 길어서</b> 천연 섬유를 대체해 널리 쓰이게 되었다. (나일론: 1930년대 미국의 캐러더스가 개발)</p>''')
r('''<p class="small mt8">오늘날에는 비는 막고 땀은 내보내는 방수·투습 섬유, 방탄 섬유 같은 기능성 섬유도 화학으로 만든다.</p>''',
  '''<p class="small mt8">방수가 되면서도 땀의 배출이 원활한 섬유, 외부 환경이 변해도 체온 유지를 도와주는 섬유 등 다양한 기능을 갖춘 합성 섬유가 개발되어 <b>운동복, 우주복</b> 등에 쓰인다.</p>''')
# S13 철
r('''<section class="slide" data-sec="01 · 화학과 주거 문제" data-title="철의 제련">
  <h2><span class="no">3</span>화학과 주거 문제 — 철의 제련</h2>''', '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="철의 제련">
  <h2><span class="no">3</span>철의 제련</h2>''')
r('''<p class="f22">철광석의 주성분인 산화 철(III) $\\ce{Fe2O3}$를 코크스(탄소)와 함께 용광로에 넣고 뜨거운 공기를 불어 넣으면, 산화 철에서 <b>산소가 떨어져 나가</b> 철을 얻는다. 이것을 <b>철의 제련</b>이라고 한다.</p>''',
  '''<p class="f22">철광석을 제련해 철을 생산하는 것은 인류가 <b>2천 년 이상</b> 활용한 화학 반응이다. 철광석의 주성분인 산화 철(III) $\\ce{Fe2O3}$를 코크스(탄소)와 함께 용광로에 넣고 뜨거운 공기를 불어 넣으면, 산화 철에서 <b>산소가 떨어져 나가</b> 철을 얻는다.</p>''')
r('''<div class="answer step">값싸고 단단한 철을 대량으로 얻어 건물의 뼈대(철근, 철골), 다리, 기계를 만들게 되었다.</div>''',
  '''<div class="answer step">18세기 이후 제련·가공 기술이 발달하여 <b>철도, 대형 교량, 선박</b>이 만들어져 사람과 물자의 이동이 활발해졌고, <b>고층 건물</b>로 대도시에서도 충분한 생활 공간을 제공하게 되었다.</div>''')
r('''<section class="slide" data-sec="01 · 화학과 주거 문제" data-title="건축 재료와 화학">
  <h2><span class="no">3</span>건축 재료와 화학</h2>''', '''<section class="slide" data-sec="01 · 화학과 우리 사회의 발전" data-title="건축 재료와 화학">
  <h2><span class="no">3</span>철과 함께 쓰는 건축 재료 <span class="small c-muted">더 알아보기</span></h2>''')
r('''<div class="answer step mt12">화학이 만든 건축 재료로 많은 사람이 <b>튼튼하고 따뜻한 집</b>에서 살게 되었다.</div>''',
  '''<div class="answer step mt12">유리, 철근 콘크리트 같은 화학이 만든 재료로 많은 사람이 <b>튼튼한 건물</b>에서 생활한다.</div>''')
for a, b in R:
    if s.count(a) != 1:
        sys.exit('NOT FOUND/DUP: ' + a[:80])
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('ok', len(R))
