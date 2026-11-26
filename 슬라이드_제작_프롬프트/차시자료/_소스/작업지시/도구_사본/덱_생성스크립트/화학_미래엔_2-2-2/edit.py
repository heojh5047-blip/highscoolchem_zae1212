# 교과서(72–77쪽, 중단원 마무리 85–86쪽) 대조 반영: orig/slides.html → slides.html (NH3 그림 등 직접 고친 내용은 그대로 둔다)
import os, re, json
W = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(W, 'orig', 'slides.html'), encoding='utf-8').read()
FIG = json.load(open(os.path.join(W, 'figs_new.json'), encoding='utf-8'))

parts = re.split(r'(?=<!-- ════════ )', src)
parts = [p for p in parts if p.strip()]
assert len(parts) == 33, len(parts)
S = {i + 1: p for i, p in enumerate(parts)}

def rep(i, a, b, n=1):
    assert S[i].count(a) == n, (i, a[:60], S[i].count(a))
    S[i] = S[i].replace(a, b)

def svg_inner(i, label_start, new_inner, new_label=None):
    """aria-label이 label_start로 시작하는 svg의 내용을 바꾼다"""
    m = re.search(r'(<svg[^>]*aria-label=")(' + re.escape(label_start) + r'[^"]*)("[^>]*>)(.*?)(</svg>)', S[i], re.S)
    assert m, (i, label_start)
    lab = new_label or m.group(2)
    S[i] = S[i][:m.start()] + m.group(1) + lab + m.group(3) + new_inner + m.group(5) + S[i][m.end():]

# ── S2 학습 목표: 교과서 72쪽 목표 문장 ──
rep(2, '''    <li><b>전자쌍 반발 이론</b>으로 중심 원자 주위의 전자쌍 배치를 설명할 수 있다.</li>
    <li>중심 원자의 <b>공유 전자쌍</b>과 <b>비공유 전자쌍</b> 수로 분자 구조와 결합각을 추론할 수 있다.</li>
    <li>소프트웨어로 분자 구조를 모델링하여 <b>3차원 모형</b>으로 나타낼 수 있다.</li>''',
'''    <li><b>전자쌍 반발 이론</b>을 근거로 분자 구조를 추론해 모형으로 나타낼 수 있다.</li>
    <li><b>소프트웨어</b>를 활용해 여러 가지 분자 구조를 모델링할 수 있다.</li>
    <li>중심 원자의 <b>전자쌍 종류와 수</b>에 따른 분자 구조를 설명할 수 있다.</li>''')

# ── S6 해 보기: 교과서 72쪽 「전자쌍 수에 따른 분자 구조 알아보기」(털실 철사) ──
S[6] = '''<!-- ════════ 6. 해 보기: 털실 철사 ════════ -->
<section class="slide" data-sec="02 · 해 보기" data-title="해 보기: 전자쌍 수에 따른 분자 구조">
  <h2><span class="tag">해 보기</span>전자쌍 수에 따른 분자 구조 알아보기 <span class="small c-muted">탐구 능력 · 의사 결정 능력</span></h2>
  <p class="f21">10 cm 정도의 털실 철사 2개, 3개, 4개의 한쪽 끝을 각각 묶고, 모든 철사가 최대한 멀리 떨어지도록 배열한 다음 인접한 철사 사이의 각도를 재자. <span class="small">(매듭 = 중심 원자, 철사 = 중심 원자 주위의 전자쌍)</span></p>
  <div class="card mt8">
    <p class="f21" data-q><b>Q1</b> 철사들 사이에는 어떤 힘이 작용한다고 볼 수 있을까? <span class="step" data-g="w1">→ <b>서로 밀어내는 힘</b>(반발력)</span></p>
    <p class="f21 mt8" data-q><b>Q2</b> 묶음을 이루는 철사의 개수와 각도 사이에 어떤 관계가 있는가? <span class="step" data-g="w2">→ 철사가 많을수록 각도가 작아진다.</span></p>
    <p class="f21 mt8" data-q><b>Q3</b> 철사들의 끝점을 선으로 연결하면 어떤 모양이 될까? <span class="step" data-g="w4">→ 선분, 정삼각형, 정사면체</span></p>
  </div>
  <div class="stages mt8">
    <div class="stage"><h3>털실 철사 2개</h3><svg viewBox="0 0 300 200" aria-label="매듭에서 반대 방향으로 뻗은 철사 두 개">@w2@</svg><p class="key step" data-g="w2">$180^\\circ$</p></div>
    <div class="stage"><h3>털실 철사 3개</h3><svg viewBox="0 0 300 200" aria-label="한 평면에서 세 방향으로 뻗은 철사 세 개">@w3@</svg><p class="key step" data-g="w2">$120^\\circ$</p></div>
    <div class="stage"><h3>털실 철사 4개</h3><svg viewBox="0 0 300 200" aria-label="정사면체의 꼭짓점 방향으로 뻗은 철사 네 개">@w4@</svg><p class="key step" data-g="w2">$109.5^\\circ$</p></div>
  </div>
  <p class="small mt8">안전: 안전 장갑을 끼고 철사 끝에 손이 찔리지 않도록 한다. 철사가 구부러지지 않게 배열한다.</p>
</section>

'''
for k in ('w2', 'w3', 'w4'):
    S[6] = S[6].replace('@' + k + '@', FIG[k])

# ── S7 자료 읽기(그림 II-14) ──
rep(7, '<h2><span class="no">1</span>전자쌍 수와 전자쌍 배치</h2>', '<h2><span class="tag">자료 읽기</span>전자쌍 반발 이론에 따른 전자쌍의 배치</h2>')
rep(7, '<th style="width:190px">전자쌍 수</th>', '<th style="width:190px">공유 전자쌍 수</th>')
rep(7, '<tr><th>전자쌍 사이 각</th>', '<tr><th>인접한 두 전자쌍이 이루는 각</th>')
rep(7, '<p class="small mt12">중심 원자가 $\\mathrm{Be}$이면 전자쌍 2개, $\\mathrm{B}$이면 전자쌍 3개로 옥텟 규칙의 예외이다. 이 단원은 이 두 경우와 옥텟 규칙을 따르는 중심 원자만 다룬다.</p>',
    '<p class="f21 mt12" data-q><b>자료 읽기</b> 중심 원자 주위의 공유 전자쌍이 각각 2개, 3개, 4개일 때 중심 원자와 인접한 두 전자쌍이 이루는 각은 각각 몇 °일까?</p>\n  <p class="small mt8">중심 원자가 $\\mathrm{Be}$이면 전자쌍 2개, $\\mathrm{B}$이면 전자쌍 3개로 옥텟 규칙의 예외이다. 이 단원은 이 두 경우와 옥텟 규칙을 따르는 중심 원자만 다룬다.</p>')

# ── S8: 교과서 확인하기가 아니므로 「연결」로 ──
rep(8, '<h2><span class="tag q">확인하기</span>메테인의 결합각은 $90^\\circ$일까?</h2>', '<h2><span class="tag alt">연결</span>메테인의 결합각은 $90^\\circ$일까?</h2>')

# ── S9 BeF2 → BeCl2 (교과서 76쪽 사례) ──
rep(9, 'data-title="BeF₂: 선형"', 'data-title="BeCl₂: 선형"')
rep(9, '공유 전자쌍만 있을 때 ① $\\ce{BeF2}$', '공유 전자쌍만 있을 때 ① $\\ce{BeCl2}$')
svg_inner(9, '플루오린화 베릴륨의 루이스', FIG['lw_becl2'], '염화 베릴륨의 루이스 전자점식: 베릴륨 양쪽에 공유 전자쌍, 염소마다 비공유 전자쌍 세 개')
rep(9, '<div class="note mt12 step" data-g="m9">염화 베릴륨 $\\ce{BeCl2}$도 같은 까닭으로 선형이다.</div>', '<div class="note mt12 step" data-g="m9">플루오린화 베릴륨 $\\ce{BeF2}$도 같은 까닭으로 선형이다.</div>')
rep(9, 'aria-label="플루오린, 베릴륨, 플루오린이 일직선으로', 'aria-label="염소, 베릴륨, 염소가 일직선으로')
rep(9, ',24,F"></g>', ',29,Cl"></g>', 2)

# ── S10 BF3 → BCl3 ──
rep(10, 'data-title="BF₃: 평면 삼각형"', 'data-title="BCl₃: 평면 삼각형"')
rep(10, '공유 전자쌍만 있을 때 ② $\\ce{BF3}$', '공유 전자쌍만 있을 때 ② $\\ce{BCl3}$')
svg_inner(10, '플루오린화 붕소의 루이스', FIG['lw_bcl3'], '삼염화 붕소의 루이스 전자점식: 붕소 둘레에 공유 전자쌍 세 개, 염소마다 비공유 전자쌍 세 개')
rep(10, '염화 붕소 $\\ce{BCl3}$도 평면 삼각형이다. 네 원자가 모두 한 평면에 있다.', '네 원자가 모두 한 평면에 있다. 플루오린화 붕소 $\\ce{BF3}$도 평면 삼각형이다.')
rep(10, 'aria-label="붕소를 가운데 두고 플루오린 세 개가', 'aria-label="붕소를 가운데 두고 염소 세 개가')
rep(10, ',24,F"></g>', ',29,Cl"></g>', 3)

# ── S11 CH4 ──
rep(11, 'data-title="CH₄: 정사면체형"', 'data-title="CH₄: 정사면체"')

# ── S12: 교과서 확인하기(73쪽) 1·2 → S8 뒤로 옮김 ──
S[12] = '''<!-- ════════ 확인하기 (73쪽) ════════ -->
<section class="slide" data-sec="02 · 확인하기" data-title="확인하기: 전자쌍 반발 이론" data-tpl="check">
  <h2><span class="tag q">확인하기</span>전자쌍 반발 이론</h2>
  <div class="card">
    <ol class="cm222-ox">
      <li>분자에서 중심 원자의 전자쌍은 ( <span class="blank"><span class="step" data-g="c1">반발력</span></span> )을/를 최소화하도록 배치된다.</li>
      <li>중심 원자 주위에 2개의 공유 전자쌍만 존재할 때 공유 전자쌍의 배치가 어떤 모양인지 써 보자. <span class="step" data-g="c2">→ <b class="c-field">선형</b> <span class="small">두 전자쌍이 서로 반대 방향($180^\\circ$)에 놓인다.</span></span></li>
    </ol>
  </div>
  <div class="note mt16 step" data-g="c2"><b>더 생각하기</b> 평면에 그린 루이스 전자점식으로는 결합각을 알 수 없다. 전자쌍은 3차원 공간에서 서로 가장 멀리 떨어지도록 놓인다.</div>
</section>

'''

# ── S13–S19: 「중심 원자에 공유 전자쌍과 비공유 전자쌍이 함께 있을 때」(77쪽 소제목) ──
for i in range(13, 18):
    rep(i, 'data-sec="02 · 중심 원자에 비공유 전자쌍이 있을 때"', 'data-sec="02 · 공유 전자쌍과 비공유 전자쌍이 함께 있을 때"')
rep(15, '비공유 전자쌍이 있을 때 ① $\\ce{NH3}$', '비공유 전자쌍이 함께 있을 때 ① $\\ce{NH3}$')
rep(16, '비공유 전자쌍이 있을 때 ② $\\ce{H2O}$', '비공유 전자쌍이 함께 있을 때 ② $\\ce{H2O}$')
rep(15, 'data-title="NH₃: 삼각뿔형"', 'data-title="NH₃: 삼각뿔"')

# ── S18–S19 다중 결합: 교과서 76쪽은 「공유 전자쌍만 있을 때」 안에서 CO2를 다룬다 → CH4 뒤로 옮김 ──
for i in (18, 19):
    rep(i, 'data-sec="02 · 다중 결합이 있을 때"', 'data-sec="02 · 중심 원자에 공유 전자쌍만 있을 때"')
rep(18, '<h2><span class="no">4</span>다중 결합이 있을 때 ① $\\ce{CO2}$, $\\ce{HCN}$</h2>', '<h2><span class="no">2</span>공유 전자쌍만 있을 때 ④ 다중 결합 $\\ce{CO2}$, $\\ce{HCN}$</h2>')
rep(18, '<mark>2중 결합이나 3중 결합은 한 방향을 향하는 전자쌍 묶음이므로 전자쌍 하나처럼 취급한다.</mark>',
    '<mark>전자쌍 반발 이론으로 분자 구조를 결정할 때 이중 결합이나 삼중 결합은 하나의 결합으로 취급한다.</mark>')
rep(19, '<h2><span class="no">4</span>다중 결합이 있을 때 ② $\\ce{HCHO}$</h2>', '<h2><span class="no">2</span>공유 전자쌍만 있을 때 ⑤ 다중 결합 $\\ce{HCHO}$</h2>')

# ── S20 정리 표: 예 분자 ──
rep(20, '<td>$\\ce{BeF2}$, $\\ce{CO2}$</td><td>$\\ce{BF3}$, $\\ce{HCHO}$</td>', '<td>$\\ce{BeCl2}$, $\\ce{CO2}$</td><td>$\\ce{BCl3}$, $\\ce{HCHO}$</td>')

# ── S21 OF2: 교과서에 없는 덱 연습 → 「더 해 보기」 ──
rep(21, '<span class="tag ex">연습 해 보기</span>', '<span class="tag ex">더 해 보기</span>')
rep(21, 'data-title="연습 해 보기: OF₂"', 'data-title="더 해 보기: OF₂"')

# ── S22: 교과서 확인하기(77쪽) 1·2 ──
S[22] = '''<!-- ════════ 확인하기 (77쪽) ════════ -->
<section class="slide" data-sec="02 · 확인하기" data-title="확인하기: 분자 구조와 결합각" data-tpl="check">
  <h2><span class="tag q">확인하기</span>분자 구조와 결합각</h2>
  <div class="card">
    <ol class="cm222-ox">
      <li>사염화 탄소($\\ce{CCl4}$)의 분자 구조는 ( <span class="blank"><span class="step" data-g="c1">정사면체</span></span> )이다. <span class="step small" data-g="c1">중심 원자 $\\mathrm{C}$: 공유 전자쌍 4개, 비공유 전자쌍 0개</span></li>
      <li>사염화 탄소($\\ce{CCl4}$)와 삼염화 질소($\\ce{NCl3}$) 중 결합각이 더 큰 분자를 써 보자. <span class="step" data-g="c2">→ <b class="c-field">$\\ce{CCl4}$</b></span></li>
    </ol>
  </div>
  <table class="tight mt16 cm222-q2 step" data-g="c2">
    <tr><th>분자</th><th>중심 원자의 공유 · 비공유 전자쌍</th><th>분자 구조</th><th>결합각</th></tr>
    <tr><td>$\\ce{CCl4}$</td><td>4 · 0</td><td>정사면체</td><td>$109.5^\\circ$</td></tr>
    <tr><td>$\\ce{NCl3}$</td><td>3 · 1</td><td>삼각뿔</td><td>$109.5^\\circ$보다 작다</td></tr>
  </table>
  <p class="small mt12 step" data-g="c2">$\\ce{NCl3}$은 중심 원자의 비공유 전자쌍이 공유 전자쌍을 더 세게 밀어내 결합각이 작아진다.</p>
</section>

'''

# ── S23 탐구 목표·준비: 교과서 74쪽 ──
rep(23, '<h2><span class="tag">탐구</span>소프트웨어를 활용해 분자 구조 모델링하기 <span class="small c-muted">[필수 탐구]</span></h2>',
    '<h2><span class="tag">탐구</span>소프트웨어를 활용해 분자 구조 모델링하기 <span class="small c-muted">모의실험 · [필수 탐구]</span></h2>')
rep(23, '<p class="f22">분자 모델링 소프트웨어로 여러 분자의 3차원 구조를 만들고 결합각을 측정하여, 전자쌍 반발 이론으로 예측한 구조와 비교할 수 있다.</p>',
    '<p class="f22">전자쌍 반발 이론을 근거로 분자 구조를 추론하고, 분자 구조를 모델링할 수 있다.</p>\n      <p class="small mt8">탐구 능력: 정보 수집·변환·해석 · 문제 해결 능력 · 의사 결정 능력</p>')
rep(23, '<p class="f21">컴퓨터나 태블릿, 분자 모델링 소프트웨어(웹 프로그램 또는 이 덱의 실험실), 활동지</p>',
    '<p class="f21">스마트 기기 — \'분자 구조 모델링\', \'분자 구조 모의실험\' 등을 검색해 분자 구조 모델링 프로그램을 실행한다(이 덱의 실험실로도 할 수 있다).</p>')

# ── S24 과정: 실험 1·2 ──
S[24] = '''<!-- ════════ 24. 탐구 과정 ════════ -->
<section class="slide" data-sec="02 · 탐구" data-title="탐구: 과정">
  <h2><span class="tag">탐구</span>과정</h2>
  <div class="row">
    <div class="col">
      <div class="card"><h3>실험 1 중심 원자에 공유 전자쌍만 존재하는 분자</h3>
        <p class="f21"><b>1</b> 전자쌍 반발 이론을 바탕으로 염화 베릴륨($\\ce{BeCl2}$), 삼염화 붕소($\\ce{BCl3}$), 메테인($\\ce{CH4}$)의 분자 구조를 추론해 분자 모형으로 나타낸다. <span class="small">(루이스 전자점식 → 중심 원자의 공유 전자쌍 수 → 분자 모형)</span></p>
        <p class="f21 mt8"><b>2</b> 세 분자를 분자 구조 모델링 프로그램으로 모델링해 보고, 분자 구조와 결합각을 확인한다.</p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h3>실험 2 공유 전자쌍과 비공유 전자쌍이 함께 존재하는 분자</h3>
        <p class="f21"><b>1</b> 암모니아($\\ce{NH3}$)와 물($\\ce{H2O}$)의 분자 구조를 추론해 분자 모형으로 나타낸다. <span class="small">(중심 원자의 공유 전자쌍 · 비공유 전자쌍 수)</span></p>
        <p class="f21 mt8"><b>2</b> 두 분자를 모델링 프로그램으로 모델링해 보고, 분자 구조와 결합각을 확인한다.</p>
      </div>
    </div>
  </div>
  <div class="row mt16">
    <div class="col"><div class="note puzzle"><b>도움말</b> 비공유 전자쌍도 공유 전자쌍과 함께 반발력이 가장 작도록 배치하여 분자 구조를 추론한다.</div></div>
    <div class="col" style="flex:0 0 470px"><div class="note"><b>결합각</b> 원자가 3개 이상 결합한 분자에서 중심 원자의 핵과, 중심 원자와 결합한 두 원자의 핵을 연결한 선이 이루는 각</div></div>
  </div>
  <p class="small mt12">더 해 보기: $\\ce{CO2}$, $\\ce{HCN}$, $\\ce{HCHO}$, $\\ce{NF3}$, $\\ce{OF2}$</p>
</section>

'''

# ── S26 결과: 교과서 분자 5종 ──
rep(26, '<tr><td>$\\ce{BeF2}$</td>', '<tr><td>$\\ce{BeCl2}$</td>')
rep(26, '<tr><td>$\\ce{BF3}$</td>', '<tr><td>$\\ce{BCl3}$</td>')
S[26] = re.sub(r'\n    <tr><td>\$\\ce\{CO2\}\$</td>.*?</tr>', '', S[26])
rep(26, '<h2><span class="tag">탐구</span>결과 및 정리</h2>', '<h2><span class="tag">탐구</span>결과 — 실험 1·2</h2>')
rep(26, '<th>분자</th><th>공유 전자쌍(묶음)</th>', '<th>분자</th><th>공유 전자쌍</th>')

# ── S27 정리: 교과서 75쪽 정리 1–3 + 스스로 평가하기 ──
S[27] = '''<!-- ════════ 27. 정리 ════════ -->
<section class="slide" data-sec="02 · 탐구" data-title="탐구: 정리">
  <h2><span class="tag">탐구</span>정리</h2>
  <div class="row">
    <div class="col">
      <p class="f21"><b>실험 1</b> 추론한 분자 구조와 모델링한 결과를 비교하고, 전자쌍 반발 이론이 유용한지 토의해 보자.</p>
      <p class="f21 step cm222-a">→ 추론한 구조(선형 $180^\\circ$, 평면 삼각형 $120^\\circ$, 정사면체 $109.5^\\circ$)와 모델링 결과가 같다. 루이스 전자점식만으로는 알 수 없는 입체 구조를 예측할 수 있어 유용하다.</p>
      <p class="f21 mt12"><b>실험 2 · 2</b> $\\ce{BeCl2}$과 $\\ce{H2O}$은 분자를 구성하는 원자 수가 같지만 분자 구조가 다른 까닭은?</p>
      <p class="f21 step cm222-a">→ $\\ce{BeCl2}$의 중심 원자에는 공유 전자쌍 2개만 있어 선형이고, $\\ce{H2O}$의 중심 원자에는 비공유 전자쌍 2개가 더 있어 전자쌍 4개가 사면체 방향으로 배치되므로 굽은 형이다.</p>
      <p class="f21 mt12"><b>실험 2 · 3</b> $\\ce{CH4}$, $\\ce{NH3}$, $\\ce{H2O}$의 중심 원자의 전자쌍은 모두 4개인데 결합각이 서로 다른 까닭은?</p>
      <p class="f21 step cm222-a">→ 비공유 전자쌍이 공유 전자쌍보다 공간을 더 많이 차지해 반발력이 크다. 비공유 전자쌍 수가 0, 1, 2로 많아질수록 결합각이 $109.5^\\circ$, $107^\\circ$, $104.5^\\circ$로 작아진다.</p>
    </div>
    <div class="col" style="flex:0 0 360px">
      <div class="card"><h3>스스로 평가하기</h3>
        <p class="f21"><b>지식·이해</b> 분자 구조를 추론하고, 그 근거를 전자쌍 반발 이론으로 설명했는가?</p>
        <p class="f21 mt8"><b>과정·기능</b> 분자 구조 모델링 프로그램을 올바르게 사용해 분자 구조를 모델링했는가?</p>
        <p class="f21 mt8"><b>가치·태도</b> 분자 구조를 추론하고 분자를 모델링하는 과정에 즐거움을 느끼며 참여했는가?</p>
      </div>
    </div>
  </div>
</section>

'''

# ── S28–S30: 확인 문제 01–03 → 교과서 중단원 마무리 04–06 ──
S[28] = '''<!-- ════════ 중단원 마무리 04 ════════ -->
<section class="slide" data-sec="02 · 중단원 마무리" data-title="중단원 마무리 04">
  <h2><span class="tag q">중단원 마무리 04</span>전자쌍 반발 이론과 분자 구조</h2>
  <p class="f22">다음 중 분자 구조가 <u>다른</u> 하나는?</p>
  <div class="choices mt8"><span>① $\\ce{BeCl2}$</span><span>② $\\ce{HCN}$</span><span>③ $\\ce{H2O}$</span><span>④ $\\ce{CS2}$</span><span>⑤ $\\ce{CO2}$</span></div>
  <div class="row stretch mt12" style="height:310px">
    <div class="col stack"><div class="board"></div></div>
    <div class="col" style="flex:0 0 520px">
      <table class="tight cm222-q2">
        <tr><th>분자</th><th>중심 원자의 공유 · 비공유</th><th>분자 구조</th></tr>
        <tr><td>$\\ce{BeCl2}$</td><td class="step" data-g="q1">2 · 0</td><td class="step" data-g="q1">선형</td></tr>
        <tr><td>$\\ce{HCN}$</td><td class="step" data-g="q1">2 · 0 <span class="small">(단일 + 삼중)</span></td><td class="step" data-g="q1">선형</td></tr>
        <tr><td>$\\ce{H2O}$</td><td class="step" data-g="q1">2 · 2</td><td class="step" data-g="q1">굽은 형</td></tr>
        <tr><td>$\\ce{CS2}$</td><td class="step" data-g="q1">2 · 0 <span class="small">(이중 2개)</span></td><td class="step" data-g="q1">선형</td></tr>
        <tr><td>$\\ce{CO2}$</td><td class="step" data-g="q1">2 · 0 <span class="small">(이중 2개)</span></td><td class="step" data-g="q1">선형</td></tr>
      </table>
    </div>
  </div>
  <div class="answer step"><b>정답 ③ $\\ce{H2O}$</b> <span class="small">나머지는 모두 선형이고, $\\ce{H2O}$만 중심 원자에 비공유 전자쌍이 2개 있어 굽은 형이다.</span></div>
</section>

'''
S[29] = '''<!-- ════════ 중단원 마무리 05 서술형 ════════ -->
<section class="slide" data-sec="02 · 중단원 마무리" data-title="중단원 마무리 05 (서술형)">
  <h2><span class="tag q">중단원 마무리 05</span>서술형</h2>
  <p class="f22">그림은 2주기 원소 $\\mathrm{X}$와 3주기 원소 $\\mathrm{Y}$로 이루어진 분자의 루이스 전자점식을 나타낸 것이다. 이에 대한 설명으로 옳지 <u>않은</u> 것을 골라 옳게 고쳐 보자. (단, $\\mathrm{X}$, $\\mathrm{Y}$는 임의의 원소 기호이다.)</p>
  <div class="row mt8">
    <div class="col" style="flex:0 0 300px">
      <svg class="fig" viewBox="120 0 220 190" style="width:220px" aria-label="X 둘레에 Y 세 개가 공유 전자쌍으로 결합하고 X 위에 비공유 전자쌍 한 개, Y마다 비공유 전자쌍 세 개">@lw_xy3@</svg>
    </div>
    <div class="col">
      <div class="bogi"><p>(가) 결합각은 $109.5^\\circ$보다 작다.</p><p>(나) 분자 구조는 평면 삼각형이다.</p><p>(다) 중심 원자에 3개의 공유 전자쌍이 있다.</p></div>
      <div class="board mt8" style="min-height:120px"></div>
    </div>
  </div>
  <div class="answer step cm222-left"><b>예시 답안</b> (나) — 중심 원자 $\\mathrm{X}$에 공유 전자쌍 3개와 비공유 전자쌍 1개가 있어 전자쌍 4개가 사면체 방향으로 배치되므로, 분자 구조는 <b>삼각뿔</b>이다. <span class="small">(가)·(다)는 옳다. 예: $\\ce{NCl3}$</span></div>
</section>

'''.replace('@lw_xy3@', FIG['lw_xy3'])
S[30] = '''<!-- ════════ 중단원 마무리 06 ════════ -->
<section class="slide" data-sec="02 · 중단원 마무리" data-title="중단원 마무리 06">
  <h2><span class="tag q">중단원 마무리 06</span>전자쌍 반발 이론과 분자 구조</h2>
  <p class="f22">그림은 2주기 원소 $\\mathrm{X}$~$\\mathrm{Z}$와 수소($\\ce{H}$)로 이루어진 분자 (가)~(다)의 분자 구조와 모형을 나타낸 것이다. (가)~(다)에 대한 설명으로 옳은 것은? (단, $\\mathrm{X}$~$\\mathrm{Z}$는 임의의 원소 기호이다.)</p>
  <div class="row mt8">
    <div class="col" style="flex:0 0 600px">
      <svg class="fig" viewBox="0 0 600 220" style="width:600px" aria-label="(가) 삼각뿔 X와 수소 세 개, (나) 평면 삼각형 Y와 수소 세 개, (다) 굽은 형 Z와 수소 두 개의 공-막대 모형">@q06@
        <text class="tex" x="100" y="182" data-mix="삼각뿔" data-size="20" data-anchor="middle"></text><text class="tex" x="100" y="210" data-mix="(가)" data-size="20" data-anchor="middle"></text>
        <text class="tex" x="300" y="182" data-mix="평면 삼각형" data-size="20" data-anchor="middle"></text><text class="tex" x="300" y="210" data-mix="(나)" data-size="20" data-anchor="middle"></text>
        <text class="tex" x="500" y="182" data-mix="굽은 형" data-size="20" data-anchor="middle"></text><text class="tex" x="500" y="210" data-mix="(다)" data-size="20" data-anchor="middle"></text>
      </svg>
    </div>
    <div class="col"><div class="board" style="min-height:220px"></div></div>
  </div>
  <div class="choices col1 mt8"><span>① (가)의 중심 원자에 비공유 전자쌍이 존재한다.</span><span>② (나)의 중심 원자에 4개의 전자쌍이 존재한다.</span><span>③ (다)의 모든 원자는 같은 평면에 위치하지 않는다.</span><span>④ 결합각은 (다)가 (가)보다 크다.</span><span>⑤ 중심 원자의 비공유 전자쌍 수는 (나)와 (다)가 같다.</span></div>
  <div class="answer step"><b>정답 ①</b> <span class="small">(가) $\\mathrm{X}$: 공유 3 · 비공유 1 · (나) $\\mathrm{Y}$: 공유 3 · 비공유 0 → 전자쌍 3개 · (다) 원자 3개는 늘 한 평면 · 결합각 (가) $107^\\circ$ &gt; (다) $104.5^\\circ$ · 비공유 전자쌍 (나) 0개, (다) 2개</span></div>
</section>

'''.replace('@q06@', FIG['q06'])

# ── S31 소단원 마무리: 교과서 77쪽 ──
S[31] = '''<!-- ════════ 31. 소단원 마무리 ════════ -->
<section class="slide" data-sec="02 · 소단원 마무리" data-title="소단원 마무리">
  <h2><span class="tag">소단원 마무리</span>창의력 키우기 · 디지털 소양 키우기</h2>
  <div class="row">
    <div class="col">
      <div class="card"><h3>창의력 키우기</h3>
        <p class="f21">우리 주변에서 여러 가지 분자 구조를 표현할 수 있는 물체를 찾아보자.</p>
        <p class="f21 mt12 step" data-g="m1"><b>예시</b> 선형 — 역기 봉과 원판 · 평면 삼각형 — 세 날개 선풍기 · 정사면체 — 삼각 김밥 포장, 테트라포드 · 삼각뿔 — 세 다리 카메라 삼각대 · 굽은 형 — 부메랑</p>
        <p class="small mt8 step" data-g="m1">물체의 중심과 끝이 무엇(중심 원자, 결합한 원자)에 해당하는지 함께 설명한다.</p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h3>디지털 소양 키우기</h3>
        <p class="f21">과학자들이 분자 구조 모델링을 연구에 활용하는 다양한 사례를 찾아 공유 플랫폼을 활용하여 공유해 보자.</p>
        <p class="f21 mt12 step" data-g="m2"><b>예시</b> 신약 개발에서 약 분자가 단백질에 맞물리는 모양 예측 · 새로운 소재·촉매의 구조 설계 · 단백질의 입체 구조 예측</p>
        <p class="small mt8 step" data-g="m2">찾은 자료의 출처를 밝히고, 믿을 만한 기관의 자료인지 확인한다.</p>
      </div>
    </div>
  </div>
</section>

'''

# ── S32 스스로 정리 → 「함께 풀어 보기」(85쪽 02 묶음, 빈칸 ❸–❻) ──
S[32] = '''<!-- ════════ 32. 함께 풀어 보기 ════════ -->
<section class="slide" data-sec="02 전자쌍 반발 이론과 분자 구조 · 마무리" data-title="함께 풀어 보기">
  <h2><span class="tag ink">함께 풀어 보기</span>분자의 구조와 성질 — 02 전자쌍 반발 이론과 분자 구조</h2>
  <div class="cm222-map">
    <div class="cm222-node cm222-dim">01 루이스 전자점식<br><span class="small">원자가 전자, 공유·비공유 전자쌍</span></div>
    <div class="cm222-arr">→</div>
    <div class="cm222-node cm222-main" data-q><b>(1)</b> ❸ <span class="blank"><span class="step">전자쌍 반발 이론</span></span> : 분자의 중심 원자의 전자쌍들이 가능한 한 서로 멀리 떨어져 배치된다는 것에 근거해 분자 구조를 예측하는 이론</div>
    <div class="cm222-arr">→</div>
    <div class="cm222-node cm222-dim">03 분자 구조에 따른 물질의 성질<br><span class="small">(다음 시간)</span></div>
  </div>
  <p class="f21 mt12"><b>(2) 분자 구조</b></p>
  <table class="tight mt8 cm222-sum">
    <tr><th>분자 구조</th><td>선형</td><td>❹ <span class="blank"><span class="step">평면 삼각형</span></span></td><td>정사면체</td><td>삼각뿔</td><td>굽은 형</td></tr>
    <tr><th>결합각</th><td>$180^\\circ$</td><td>$120^\\circ$</td><td>$109.5^\\circ$</td><td>$107^\\circ$</td><td>$104.5^\\circ$</td></tr>
    <tr><th>중심 원자의 전자쌍 수<br><span class="small">(공유, 비공유)</span></th><td>2, 0</td><td>3, 0</td><td>❺ <span class="blank"><span class="step">4</span></span>, 0</td><td>3, ❻ <span class="blank"><span class="step">1</span></span></td><td>2, 2</td></tr>
    <tr><th>예</th><td>$\\ce{BeCl2}$</td><td>$\\ce{BCl3}$</td><td>$\\ce{CH4}$</td><td>$\\ce{NH3}$</td><td>$\\ce{H2O}$</td></tr>
  </table>
  <p class="small mt12">중단원 마무리 「함께 풀어 보기」(85쪽) 02 묶음. 제시된 핵심 내용으로 간단한 문제를 만들고, 공유 플랫폼에 공유하여 친구들과 함께 풀어 보자. · 더하기: 반발력 비공유–비공유 &gt; 비공유–공유 &gt; 공유–공유 · 이중·삼중 결합은 하나의 결합으로 취급</p>
</section>

'''

# ── S33 스스로 점검하기 ──
rep(33, '$\\ce{BF3}$와 $\\ce{NH3}$는', '$\\ce{BCl3}$와 $\\ce{NH3}$는')
rep(33, '<button class="chk">[과정·기능] 소프트웨어로 분자 구조를 모델링하고 결합각을 측정하였다.</button>', '<button class="chk">[과정·기능] 분자 구조 모델링 프로그램으로 분자 구조를 모델링하고 결합각을 확인했다.</button>')

# ── 순서: 확인하기(73쪽)를 S8 뒤로, 다중 결합(S18·S19)을 CH4(S11) 뒤로 ──
order = [1, 2, 3, 4, 5, 6, 7, 8, 12, 9, 10, 11, 18, 19, 13, 14, 15, 16, 17, 22, 20, 21] + list(range(23, 34))
assert sorted(order) == list(range(1, 34))
out = ''.join(S[i] for i in order)

out = out.replace('사염화 탄소 $\\ce{CCl4}$, 실레인 $\\ce{SiH4}$도', '실레인 $\\ce{SiH4}$도').replace('. BeF2 ═', '. BeCl2 ═').replace('. BF3 ═', '. BCl3 ═')
# ── 교과서 표기 ──
for a, b in (('정사면체형', '정사면체'), ('삼각뿔형', '삼각뿔'), ('2중 결합', '이중 결합'), ('3중 결합', '삼중 결합')):
    out = out.replace(a, b)
# 슬라이드 번호 주석 정리
n = [0]
def num(m):
    n[0] += 1
    return f'<!-- ════════ {n[0]}. '
out = re.sub(r'<!-- ════════ (?:\d+\. )?', num, out)
open(os.path.join(W, 'slides.html'), 'w', encoding='utf-8').write(out)
print('slides', out.count('<section'), 'bytes', len(out))
