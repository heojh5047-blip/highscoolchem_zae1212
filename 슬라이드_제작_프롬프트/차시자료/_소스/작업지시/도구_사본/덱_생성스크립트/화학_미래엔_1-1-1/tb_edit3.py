# 교과서 재검토: 3단계 — 해 보기(17쪽), 소단원 마무리, 중단원 마무리 01–03(28쪽), 스스로 정리·점검
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
head = s[:s.index('<!-- ════════ 23.')]
T = r'''<!-- ════════ 23. 해 보기 ① ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기 ① 분야 고르고 정리하기">
  <h2><span class="tag">해 보기</span>화학이 현대 과학·기술·사회의 발전에 기여한 사례 조사하기 <span class="small c-muted">문제 해결 능력 | 의사 결정 능력</span></h2>
  <div class="row mt8">
    <div class="col">
      <p class="f21"><b>1.</b> 모둠별로 다음 분야 중 한 가지를 선택하고, 선택한 분야에서 화학이 인류의 문제를 해결한 사례를 조사해 보자.</p>
      <div class="chips mt8"><button class="chk">의류</button><button class="chk">식량</button><button class="chk">주거</button><button class="chk">건강</button><button class="chk">환경</button><button class="chk">기타</button></div>
      <p class="f21 mt12"><b>2.</b> 조사한 사례를 다음 항목에 따라 구체적으로 정리해 보자.</p>
      <ul class="cm111-ul f21">
        <li>화학이 해결한 문제는 무엇인가?</li>
        <li>화학이 문제 해결에 어떻게 기여했는가?</li>
        <li>그 후로 사회가 어떻게 발전했는가?</li>
      </ul>
    </div>
    <div class="col" style="flex:0 0 430px">
      <div class="card"><p class="f21"><b>준비물</b> 스마트 기기</p><p class="f21 mt8"><b>도움 자료</b> 활동 전에 178쪽 디지털 리터러시 도움 자료를 먼저 읽어 보자.</p></div>
      <div class="note q mt8"><b>조사할 때 지킬 것</b>
        <ul class="cm111-ul">
          <li>믿을 만한 자료(공공 기관, 학회, 과학 잡지)를 쓴다.</li>
          <li>자료마다 출처(만든 곳, 날짜)를 적는다.</li>
          <li>생성형 인공지능의 답은 다른 자료로 확인한다.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ════════ 24. 해 보기 ② ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기 ② 발표하고 고치기">
  <h2><span class="tag">해 보기</span>화학이 기여한 사례 조사하기 — 발표하고 고치기</h2>
  <div class="cm111-s4">
    <div class="stage" data-anim="pop" data-o="0,0" data-dur=".6" data-delay=".2" data-ease="back"><h3>1–2 조사·정리</h3><p>분야를 하나 고르고, 세 항목(해결한 문제 · 기여 · 사회의 발전)에 따라 정리한다.</p></div>
    <div class="stage" data-anim="pop" data-dur=".6" data-delay=".45" data-ease="back"><h3>3 발표</h3><p>공유 플랫폼을 활용해 모둠에서 공동으로 발표 자료를 만들어 발표한다.</p></div>
    <div class="stage" data-anim="pop" data-dur=".6" data-delay=".7" data-ease="back"><h3>4 질문·의견</h3><p>다른 모둠의 발표를 들으면서 공유 플랫폼에 질문이나 의견을 남기고, 우리 모둠 자료를 고치는 데 도움이 될 내용을 쓴다.</p></div>
    <div class="stage" data-anim="pop" data-dur=".6" data-delay=".95" data-ease="back"><h3>5 수정·공유</h3><p>4의 내용을 바탕으로 우리 모둠의 자료를 수정하고, 최종 자료를 공유 플랫폼에 공유한다.</p></div>
  </div>
  <h3 class="mt16">정리 틀 (과정 2의 세 항목)</h3>
  <div class="flow cm111-frame">
    <div class="fnode">화학이 해결한 문제</div><div class="farr">→</div>
    <div class="fnode hl">화학의 기여<br><span class="small">물질·반응·기술</span></div><div class="farr">→</div>
    <div class="fnode">그 후 사회의 발전</div>
  </div>
</section>

<!-- ════════ 25. 해 보기 ③ ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기 ③ 예시 결과와 평가">
  <h2><span class="tag">해 보기</span>화학이 기여한 사례 조사하기 — 예시 결과와 평가</h2>
  <div class="row">
    <div class="col">
      <h3>예시 결과 — 분야: 식량 「비닐의 이용」</h3>
      <div class="cm111-news">
        <div class="cm111-nc"><b>해결한 문제</b><p>추운 계절에는 채소와 과일을 기르기 어려웠다.</p></div>
        <div class="cm111-nc step"><b>화학의 기여</b><p>석유에서 얻은 원료로 얇고 투명한 비닐(플라스틱 필름)을 대량으로 만들었다.</p></div>
        <div class="cm111-nc step"><b>사회의 발전</b><p>비닐하우스로 계절과 관계없이 농작물을 길러 생산량이 늘었다.</p></div>
        <div class="cm111-nc step"><b>질문·의견(과정 4)</b><p>다 쓴 비닐은 어떻게 처리할까? → 재활용 방법을 자료에 더한다.</p></div>
      </div>
    </div>
    <div class="col" style="flex:0 0 470px">
      <h3>평가 기준</h3>
      <table class="tight cm111-rub">
        <tr><th>항목</th><th>잘함의 모습</th></tr>
        <tr><td>정확성</td><td class="l">물질·반응을 바르게 설명한다</td></tr>
        <tr><td>기여</td><td class="l">사회가 어떻게 발전했는지 밝힌다</td></tr>
        <tr><td>출처</td><td class="l">믿을 만한 자료와 출처를 밝힌다</td></tr>
        <tr><td>소통</td><td class="l">질문·의견을 반영해 자료를 고친다</td></tr>
      </table>
      <h3 class="mt12">동료 평가</h3>
      <div class="chips"><button class="chk">새로 알게 된 점</button><button class="chk">더 궁금한 점</button><button class="chk">칭찬할 점</button></div>
    </div>
  </div>
</section>

<!-- ════════ 26. 소단원 마무리 ════════ -->
<section class="slide" data-sec="01 · 소단원 마무리" data-title="소단원 마무리">
  <h2><span class="tag">소단원 마무리</span>이산화 탄소 활용과 미래 사회</h2>
  <div class="row stretch">
    <div class="col">
      <div class="card"><h3>창의력 키우기</h3>
        <p class="f21">대기 중의 이산화 탄소를 포집해 활용하는 여러 가지 분야를 찾아보자.</p>
        <p class="f21 step mt8 c-muted">예) 건축 자재(콘크리트·벽돌), 섬유·플라스틱의 원료, 연료(메탄올), 비료(요소), 탄산음료·드라이아이스, 온실의 작물 재배</p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h3>디지털 소양 키우기</h3>
        <p class="f21">화학이 만든 미래 사회는 어떤 모습일지 상상해 간단한 기사를 작성하고, 공유 플랫폼을 활용해 작성한 기사를 공유해 보자.</p>
        <p class="f21 step mt8 c-muted">예) 「2050년, 공장 굴뚝의 이산화 탄소로 지은 아파트에 입주」 — 무엇이 · 어떤 화학 기술로 · 생활이 어떻게 바뀌었나</p>
      </div>
    </div>
  </div>
</section>

<!-- ════════ 27. 중단원 마무리 01 ════════ -->
<section class="slide" data-sec="01 · 중단원 마무리" data-title="중단원 마무리 01">
  <h2><span class="tag q">중단원 마무리 01</span>학문 분야</h2>
  <p class="f22">다음은 어떤 학문 분야의 발전이 가져온 생활의 변화에 대한 설명이다.</p>
  <div class="row mt8">
    <div class="col">
      <div class="bogi"><p>(　　　)이/가 발전하면서 합성 섬유로 만든 옷을 입고, 화학 전지로 작동하는 스마트폰을 이용해 소통하며, 합성 의약품으로 질병을 치료할 수 있게 되었다.</p></div>
      <p class="f22 mt8">(　　　) 안에 들어갈 학문 분야로 가장 적절한 것은?</p>
      <div class="choices"><span>① 수학</span><span>② 물리학</span><span>③ 화학</span><span>④ 생명과학</span><span>⑤ 지구과학</span></div>
    </div>
    <div class="col stack" style="flex:0 0 340px"><div class="board" style="min-height:200px"></div></div>
  </div>
  <div class="answer step"><b>정답 ③ 화학</b> <span class="small">합성 섬유, 화학 전지, 합성 의약품은 모두 물질을 만들고 그 성질을 활용하는 화학의 성과이다.</span></div>
</section>

<!-- ════════ 28. 중단원 마무리 02 ════════ -->
<section class="slide" data-sec="01 · 중단원 마무리" data-title="중단원 마무리 02">
  <h2><span class="tag q">중단원 마무리 02</span>화학이 해결한 문제</h2>
  <p class="f22">화학이 인류의 문제를 해결하고 인류 문명의 발전에 영향을 미친 예로 <u>옳지 않은</u> 것은?</p>
  <div class="row mt8">
    <div class="col">
      <ol class="cm111-ch f21">
        <li>① 항생제, 백신 개발로 인류의 수명이 증가했다.</li>
        <li>② 합성 섬유의 개발로 천연 섬유의 단점을 보완했다.</li>
        <li>③ 화학 비료를 대량 생산 하게 되어 식량 부족 문제 해결에 기여했다.</li>
        <li>④ 철광석의 제련으로 대형 선박, 교량이 만들어져 교통이 발달했다.</li>
        <li>⑤ 화석 연료의 사용량이 증가하여 대기 중 이산화 탄소의 양이 감소했다.</li>
      </ol>
    </div>
    <div class="col stack" style="flex:0 0 340px"><div class="board" style="min-height:220px"></div></div>
  </div>
  <div class="answer step"><b>정답 ⑤</b> <span class="small">화석 연료를 많이 쓰면 대기 중 이산화 탄소의 양은 <b>증가</b>한다 — 이것은 화학이 해결해야 할 문제이다.</span></div>
</section>

<!-- ════════ 29. 중단원 마무리 03 서술형 ════════ -->
<section class="slide" data-sec="01 · 중단원 마무리" data-title="중단원 마무리 03 (서술형)">
  <h2><span class="tag q">중단원 마무리 03</span>서술형 — 신문 기사</h2>
  <div class="row">
    <div class="col">
      <div class="bogi f21"><p>정부간 기후 변화 협의체(IPCC)는 최근 발표한 종합 보고서에서 지구의 평균 온도 상승 폭이 21세기 내에 1.5 °C를 넘을 가능성이 크다고 예측했다. …… 지구 온난화의 주요 원인은 이산화 탄소와 같은 온실 가스의 배출이다. 1850년부터 2019년까지 인간 활동으로 배출된 온실 가스의 양은 약 2400 Gt(기가톤)인데, 이 중 절반가량은 1990년~2019년에 배출된 것으로 추정된다. 즉, 이산화 탄소의 배출량뿐만 아니라 배출량이 증가하는 속도도 점점 빨라지고 있다.</p><p class="small">(자료 출처: 『연합뉴스』, 2023. 03. 21.)</p></div>
      <p class="f22 mt8">기사에 제시된 인류의 문제를 해결하기 위해 화학이 할 수 있는 일을 한 가지 설명해 보자.</p>
    </div>
    <div class="col stack" style="flex:0 0 330px"><div class="board" style="min-height:260px"></div></div>
  </div>
  <div class="answer step cm111-left"><b>예시 답안</b> 탄소 포집·활용·저장(CCUS) 기술로 공장이나 발전소에서 나오는 이산화 탄소를 모아 건축 자재 같은 유용한 물질로 바꾸거나 땅속 깊이 저장하여 대기 중 이산화 탄소의 농도를 낮춘다. (또는 에너지 효율이 높은 태양 전지 소재를 개발해 화석 연료 사용을 줄인다.)<br><span class="small">채점 요소: 문제(온실 가스·이산화 탄소 증가) 인식 · 화학의 기술이나 물질 제시 · 이산화 탄소를 줄이는 원리</span></div>
</section>

'''
rest = s[s.index('<!-- ════════ 30.'):]
# 스스로 정리 — 중단원 마무리 「01 화학과 현대 과학·기술·사회」 빈칸 ❶–❹
old30 = rest[:rest.index('<!-- ════════ 31.')]
new30 = r'''<!-- ════════ 30. 스스로 정리 ════════ -->
<section class="slide" data-sec="01 화학과 현대 과학·기술·사회 · 마무리" data-title="스스로 정리">
  <h2><span class="tag ink">스스로 정리</span>01 화학과 현대 과학·기술·사회</h2>
  <h3>(1) 화학과 우리 사회의 발전</h3>
  <table class="tight cm111-sum2">
    <tr><th>❶ <span class="blank"><span class="step">암모니아</span></span>의 합성</th><th>합성 섬유의 개발</th><th>❷ <span class="blank"><span class="step">철광석</span></span>의 제련</th><th>의약품의 개발</th></tr>
    <tr><td class="l">질소 비료의 대량 생산으로 식량 생산량 증가 · 비료, 세정제의 원료나 냉동 장치의 냉매로 이용</td><td class="l">대량 생산이 가능하고 섬유의 수명이 길어서 천연 섬유를 대체 · 다양한 기능을 갖춘 합성 섬유 개발</td><td class="l">철을 이용해 철도, 대형 교량, 선박 등이 만들어져 사람과 물자의 이동이 활발 · 고층 건물</td><td class="l" data-q>❸ <span class="blank"><span class="step">페니실린</span></span>의 분자 구조를 변형하여 성능을 개량한 항생제 생산 · 새로운 감염병 백신을 빠르게 개발</td></tr>
  </table>
  <h3 class="mt12">(2) 지속가능한 미래를 만드는 화학</h3>
  <p class="f21" data-q>화학은 태양 전지 등 대체 에너지 개발에 도움을 주고, 탄소 포집·활용·저장(CCUS) 기술 등 대기 중 ❹ <span class="blank"><span class="step">이산화 탄소</span></span>의 농도를 낮추는 기술 개발에서 핵심적인 역할을 한다.</p>
  <div class="note mt8"><b>함께 풀어 보기</b> 제시된 핵심 내용과 관련된 간단한 문제를 만들고, 공유 플랫폼에 공유하여 친구들과 함께 풀어 보자. <span class="small">다음 시간: 02 몰과 물질의 양</span></div>
</section>

'''
rest = rest.replace(old30, new30)
rest = rest.replace('<button class="chk">[지식·이해] 화학이 식량·의류·주거 문제를 해결한 사례를 설명할 수 있다.</button>',
                    '<button class="chk">[지식·이해] 화학이 인류의 문제를 해결하고 과학·기술·사회의 발전에 기여한 사례를 설명할 수 있다.</button>')
rest = rest.replace('<button class="chk">[가치·태도] 화학이 사회에 미치는 영향을 균형 있게 생각하고 화학에 흥미를 가졌다.</button>',
                    '<button class="chk">[가치·태도] 화학 관련 일상생활 문제를 인식하고, 이를 과학적으로 해결하려는 태도를 가졌다.</button>')
rest = rest.replace('<p class="f21 mt8"><b>Q</b> 나일론은 의류 문제 해결에 어떻게 기여했나? <span class="step">→ 질기고 값싼 합성 섬유를 대량으로 만들게 했다.</span></p>',
                    '<p class="f21 mt8"><b>Q</b> 대기 중 이산화 탄소의 농도를 낮추는 화학 기술은? <span class="step">→ 탄소 포집·활용·저장(CCUS) 기술</span></p>')
assert 'CCUS) 기술</span>' in rest and '과학적으로 해결하려는 태도를 가졌다' in rest
open(p, 'w', encoding='utf-8').write(head + T + rest)
print('ok')
