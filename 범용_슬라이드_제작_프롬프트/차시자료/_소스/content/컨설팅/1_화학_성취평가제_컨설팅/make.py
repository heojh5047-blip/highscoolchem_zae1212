# 화학 성취평가제 컨설팅 덱 생성 — 근거: 「성취평가제 운영 내실화를 위한 교과 맞춤형 컨설팅」(한영고 화학) 자료 1~13쪽
import os, math
D = os.path.dirname(os.path.abspath(__file__))
INK, PLUS, MINUS, FIELD, EQUI, GRAV, MUTED = '#16233D', '#D7263D', '#1F6FD1', '#2E9E6A', '#E08A2C', '#8C99A6', '#5B6B7F'
LV = {'A': '#2B2F7E', 'B': '#4950B8', 'C': '#6F7BD0', 'D': '#9CA6E2', 'E': '#C7CEF0'}   # 자료의 성취수준 남보라 단계 색
def tx(x, y, t, size=20, anchor='start', weight=None, fill=None):
    w = f' data-weight="{weight}"' if weight else ''; f = f' fill="{fill}"' if fill else ''
    return f'<text class="tex" x="{x}" y="{y}" data-mix="{t}" data-size="{size}" data-anchor="{anchor}"{w}{f}></text>'
def src(p): return f'<p class="small cs1-src">출처: 컨설팅 자료 {p}</p>'
def lvdot(l): return f'<span class="cs1-lv" style="background:{LV[l]};color:{"#fff" if l in "ABC" else INK}">{l}</span>'
S = []

# 1 표지 (성과보고회 시안 E 재구성)
S.append(f'''<section class="slide cover cs1-cover" data-sec="표지" data-title="표지">
  <div class="wrap">
    <span class="cs1-pill">2022 개정 교육과정 일반선택과목 「화학」</span>
    <h1><span class="pre">성취평가제 운영 내실화를 위한</span><br>교과 맞춤형 컨설팅</h1>
    <p class="sub">한영고등학교 성취평가제 컨설팅 · 화학</p>
  </div>
  <svg class="road" viewBox="0 0 1280 120" width="1280" height="120" aria-hidden="true" data-audit="skip">
    <path d="M0 60 H1280" stroke="#CFD8E1" stroke-width="6"/>
    <g data-anim="draw" data-dur="1.6"><path d="M96 60 H1184" stroke="{MINUS}" stroke-width="6" stroke-linecap="round"/></g>
    <circle cx="200" cy="60" r="16" fill="#fff" stroke="{MINUS}" stroke-width="5"/><circle cx="520" cy="60" r="16" fill="#fff" stroke="{MINUS}" stroke-width="5"/><circle cx="840" cy="60" r="16" fill="#fff" stroke="{MINUS}" stroke-width="5"/><circle cx="1120" cy="60" r="22" fill="{FIELD}"/>
    {tx(200,112,'이해',22,'middle','700')}{tx(520,112,'진단',22,'middle','700')}{tx(840,112,'설계',22,'middle','700')}{tx(1120,24,'협의',24,'middle','800',FIELD)}
  </svg>
  <div class="who"><span><b>여수고등학교</b> · 교사 허재형</span><span class="cs1-muted">2026. 11. 27.(금)</span></div>
</section>''')

# 2 목차
S.append('''<section class="slide" data-sec="목차" data-title="목차">
  <h2><span class="tag alt">목차</span>오늘 함께 살펴볼 것</h2>
  <div class="cs1-toc">
    <div class="it"><h3>이해</h3><p>Ⅰ 성취평가제의 의의<br>Ⅱ 성취평가제가 지향하는 평가<br>Ⅳ 2022 개정 화학 교육과정과 성취평가</p></div>
    <div class="it"><h3>진단</h3><p>Ⅲ 성취평가제 모니터링의 의미<br>Ⅸ 학교 성취평가 운영 결과 공유</p></div>
    <div class="it"><h3>설계</h3><p>Ⅴ 성취수준에 근거한 지필평가<br>Ⅵ 성취수준에 근거한 수행평가<br>Ⅶ 추정분할점수의 이해<br>Ⅷ 추정분할점수 산출의 실제</p></div>
    <div class="it hl"><h3>협의</h3><p>Ⅸ 함께 협의할 방향<br>Ⅹ 성취평가제 운영의 발전 방향</p></div>
  </div>
  <p class="small cs1-src">컨설팅 자료의 Ⅰ~Ⅹ장을 이해 → 진단 → 설계 → 협의 흐름으로 묶었습니다.</p>
</section>''')

# 3 Ⅰ 의의
S.append(f'''<section class="slide" data-sec="Ⅰ · 성취평가제의 의의" data-title="성취평가제의 의의">
  <h2><span class="no">1</span>성취평가제는 '무엇을 할 수 있는가'를 알려 준다</h2>
  <div class="row">
    <div class="col">
      <div class="cs1-tl3">
        <div class="it"><b>2011</b><p>중등학교 학사관리 선진화 방안 발표</p></div>
        <div class="it"><b>2012</b><p>성취평가제 도입<br>(고등학교 전문교과부터)</p></div>
        <div class="it hl"><b>2014</b><p>고등학교 보통교과로 확대</p></div>
      </div>
      <p class="f21" style="margin-top:18px">도입 배경: 창의·인성 교육을 활성화하고 학생의 성취를 정확하고 타당하게 평가하려는 교육적 요구</p>
    </div>
    <div class="col" style="flex:0 0 470px">
      <div class="formula sm" style="margin-top:0;text-align:left;font-size:25px">국가 교육과정의 <mark>성취기준</mark>을 준거로<br>학생이 무엇을 알고 할 수 있는지,<br>어느 정도 도달했는지를 판단</div>
      <p class="f21">점수의 서열이 아니라 <b>성취 정도에 관한 정보</b>를 제공하는 것이 의의입니다.</p>
    </div>
  </div>
  {src('1쪽 Ⅰ. 성취평가제의 의의')}
</section>''')

# 4 Ⅱ 준거 vs 규준 — 그림
def bell():
    pts = []; mu, sd = 250, 62
    for i in range(0, 101):
        x = 40 + i * 4.2
        y = 230 - 170 * math.exp(-((x - mu) ** 2) / (2 * sd * sd))
        pts.append(f'{x:.1f},{y:.1f}')
    edges = [40, 124, 208, 292, 376, 460]
    lab = [('5등급', '10%'), ('4등급', '24%'), ('3등급', '32%'), ('2등급', '24%'), ('1등급', '10%')]
    out = [f'<polyline points="{" ".join(pts)}" fill="none" stroke="#0E7490" stroke-width="4"/>']
    for e in edges[1:-1]: out.append(f'<line x1="{e}" y1="60" x2="{e}" y2="232" stroke="#8C99A6" stroke-width="1.5" stroke-dasharray="4 4"/>')
    out.append('<line x1="30" y1="232" x2="470" y2="232" stroke="#16233D" stroke-width="2"/>')
    for k, (g, p) in enumerate(lab):
        cx = (edges[k] + edges[k + 1]) / 2
        out.append(tx(cx, 262, g, 20, 'middle', '700', '#0E7490') + tx(cx, 290, p, 20, 'middle'))
    return ''.join(out)
ladder = []
for k, l in enumerate('ABCDE'):
    y = 40 + k * 50
    ladder.append(f'<rect x="200" y="{y}" width="64" height="42" rx="6" fill="{LV[l]}"/>' + tx(232, y + 29, l, 22, 'middle', '800', '#fff' if l in 'ABC' else INK))
    ladder.append(f'<g data-arw="330,{y+21},274,{y+21},rd,3"></g>')
ladder.append(f'<g data-arw="60,61,190,61,plus,4"></g>' + tx(60, 46, '개인 성취율', 20) + tx(340, 128, '기준 성취율', 20))
S.append(f'''<section class="slide" data-sec="Ⅱ · 성취평가제가 지향하는 평가" data-title="준거참조평가와 규준참조평가">
  <h2><span class="no">2</span>'누가 더 잘했나'가 아니라 '어느 정도 성취했나'</h2>
  <div class="row">
    <div class="col pane grav"><h3 style="text-align:center">석차 5등급제 — 집단 안의 <span style="color:#0E7490">서열</span></h3>
      <svg class="fig" viewBox="0 0 480 300" style="width:400px;display:block;margin:0 auto" aria-label="정규분포 위의 석차 5등급 비율">{bell()}</svg></div>
    <div class="col pane minus"><h3 style="text-align:center">성취평가제 — 성취기준에 <span style="color:#1F6FD1">도달한 정도</span></h3>
      <svg class="fig" viewBox="0 0 480 300" style="width:400px;display:block;margin:0 auto" aria-label="성취수준 A~E 사다리와 개인 성취율">{''.join(ladder)}</svg></div>
  </div>
  <table class="tight" style="margin-top:12px">
    <tr><th class="l">구분</th><th>준거참조평가</th><th>규준참조평가</th></tr>
    <tr><td class="l">핵심 질문</td><td>무엇을 어느 정도 성취했는가?</td><td>집단에서 상대적 위치는 어디인가?</td></tr>
    <tr><td class="l">판단 준거</td><td>사전에 설정한 성취기준과 성취수준</td><td>비교 집단의 성적 분포</td></tr>
  </table>
  {src('1~2쪽 Ⅱ-1 · 그림은 자료 2쪽을 다시 그림')}
</section>''')

# 5 Ⅱ 연계·전문성
S.append(f'''<section class="slide" data-sec="Ⅱ · 성취평가제가 지향하는 평가" data-title="교육과정·수업·평가 연계">
  <h2><span class="no">3</span>성취수준은 점수를 매긴 뒤가 아니라 <mark>설계하기 전에</mark> 공유한다</h2>
  <div class="cs1-steps">
    <div class="it"><span class="n">1</span><p>교과별 성취기준에 근거하여 교수·학습 설계<br>(교육과정 재구성)</p></div>
    <div class="it"><span class="n">2</span><p>성취기준에 도달하기 위한 교수·학습 활동 전개</p></div>
    <div class="it"><span class="n">3</span><p>성취평가제에 적절한 평가 계획 수립 및 평가도구 제작</p></div>
    <div class="it"><span class="n">4</span><p>평가 실시·성적 산출, 성취기준에 근거한 피드백</p></div>
  </div>
  <div class="row" style="margin-top:20px">
    <div class="col card"><h3>화학에서 중요한 성취 증거</h3><p class="f21">계산을 정확히 하는 능력만이 아니라 <b>화학 개념 설명 · 자료 해석 · 탐구 수행</b></p></div>
    <div class="col card"><h3>교사의 평가 전문성</h3><p class="f21">성취기준·수업·평가도구가 타당했는지 진단하고 개선, <b>교과협의</b>로 판단의 일관성을 높임</p></div>
  </div>
  {src('2~3쪽 Ⅱ-2·3')}
</section>''')

# 6 Ⅲ 모니터링 지표
S.append(f'''<section class="slide" data-sec="Ⅲ · 모니터링의 의미" data-title="모니터링 지표">
  <h2><span class="no">4</span>모니터링 지표는 판정이 아니라 <mark>협의의 출발점</mark></h2>
  <p class="f22">평가 운영의 타당성과 신뢰도를 높이기 위해 평가 결과와 운영 과정을 살피고 필요한 지원을 제공합니다.</p>
  <table class="tight" style="margin-top:14px">
    <tr><th style="width:150px">구분</th><th class="l">주요 지표</th></tr>
    <tr><td><b>필수지표</b></td><td class="l">지표1: 성취수준 A의 비율이 높음(전국 평균 23.9%)<br>지표2: 과목 평균이 성취수준 A 분할점수보다 높음<br>지표3: 과목 평균이 높음</td></tr>
    <tr><td><b>특성지표</b></td><td class="l">지표4: 성취수준 A 분할점수가 낮음<br>지표5: 전년도에 비해 과목 평균에는 큰 변동이 없으나, 성취수준 A 비율이 증가함<br>지표6: 전년도에 비해 성취수준 A 비율이 증가하였으며, 성취수준 A 분할점수가 감소함</td></tr>
  </table>
  {src('3쪽 Ⅲ-1 모니터링과 학교 지원')}
</section>''')

# 7 Ⅲ 지표 해석 (예시 그림)
sd = []
sd.append('<line x1="70" y1="290" x2="520" y2="290" stroke="#16233D" stroke-width="2"/>')
for yv, lab, dash in ((250, '전국 평균', None), (190, '전국 평균 + 1표준편차', '7 6'), (130, '전국 평균 + 2표준편차', '7 6')):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    sd.append(f'<line x1="70" y1="{yv}" x2="400" y2="{yv}" stroke="{PLUS}" stroke-width="2.5"{d}/>' + tx(410, yv + 7, lab, 18, fill=PLUS))
sd.append(f'<g data-anim="scale" data-from="1,0" data-o="190,290" data-dur="1.1" data-ease="out"><rect x="150" y="70" width="80" height="220" rx="5" fill="{LV["B"]}"/></g>' + tx(190, 58, '82.7%', 26, 'middle', '800', LV['A']))
sd.append(tx(190, 318, '학교 A 비율', 18, 'middle'))
S.append(f'''<section class="slide" data-sec="Ⅲ · 모니터링의 의미" data-title="지표 해석의 유의점">
  <h2><span class="tag ex">예시</span>"성취수준 A 비율이 매우 높다" — 그다음은?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 640px"><svg class="fig" viewBox="0 0 640 330" style="width:640px" aria-label="학교 A 비율과 전국 평균, 표준편차 선을 비교한 예시 그림">{''.join(sd)}</svg>
      <p class="small">예시 그림(크기 비례 아님) — 자료 4쪽 그림을 다시 그림</p></div>
    <div class="col stack">
      <div class="card"><h3>지표 해석의 유의점</h3><p class="f21">전국 평균·표준편차는 <b>참고 정보</b>. 학생 특성, 평가도구, 분할점수 산출 과정이 학교마다 다르므로 지표만으로 적절성을 단정하지 않습니다.</p></div>
      <div class="note puzzle" style="margin-top:12px">A 비율이 높다는 이유로 <b>비율을 낮추거나 전국 평균에 맞추는 것</b>은 준거참조평가의 취지와 다릅니다.</div>
    </div>
  </div>
  <div class="note q" style="margin-top:12px"><b>협의 질문</b> 우리 학교의 평가 결과는 학생이 무엇을 알고 할 수 있는지 충분히 설명하고 있는가?</div>
  {src('4쪽 Ⅲ-2·3')}
</section>''')

# 8 Ⅳ 용어
terms = [('성취기준', '학생이 학습을 통해 성취해야 할 내용과 수행'), ('성취수준', '성취기준에 도달한 정도를 수준별로 진술한 특성'), ('학기단위 성취수준', '한 학기 동안 학습하는 성취기준을 종합한 수준별 수행 특성'),
         ('성취율', '교육과정에 대한 성취 정도를 나타내는 비율'), ('분할점수', '성취수준 간 경계를 구분하는 평가 점수'), ('성취도', '평가 결과를 성취수준에 따라 나타낸 결과')]
S.append(f'''<section class="slide" data-sec="Ⅳ · 2022 개정 화학과 성취평가" data-title="주요 용어">
  <h2><span class="no">5</span>먼저 말을 맞춥니다 — 주요 용어</h2>
  <table class="tight"><tr><th style="width:260px">용어</th><th class="l">의미</th></tr>
    {''.join(f'<tr><td><b>{a}</b></td><td class="l">{b}</td></tr>' for a, b in terms)}</table>
  <div class="note" style="margin-top:14px"><b>성취율</b>은 교육과정 기준, <b>분할점수</b>는 평가 점수 기준 — 둘을 구분해야 추정분할점수가 이해됩니다.</div>
  {src('5쪽 Ⅳ-1')}
</section>''')

# 9 Ⅳ 내용 체계
S.append(f'''<section class="slide" data-sec="Ⅳ · 2022 개정 화학과 성취평가" data-title="화학 내용 체계">
  <h2><span class="no">6</span>일반선택 「화학」 — 4개 영역, 15개 성취기준</h2>
  <div class="cs1-grid2">
    <div class="card"><h3>화학의 언어</h3><p class="f21">화학의 유용성, 몰, 화학 반응의 양적 관계</p></div>
    <div class="card"><h3>물질의 구조와 성질</h3><p class="f21">화학 결합, 전기 음성도, 분자 구조와 성질</p></div>
    <div class="card"><h3>화학 평형</h3><p class="f21">동적 평형, 평형 상수, 반응 지수, 평형 이동</p></div>
    <div class="card"><h3>역동적인 화학 반응</h3><p class="f21">pH, 몰 농도, 중화 반응, 중화 적정</p></div>
  </div>
  <div class="formula sm" style="margin-top:22px">수업·평가의 준거 = 일반선택 화학의 <mark>15개 성취기준과 성취수준 진술문</mark></div>
  <p class="f21" style="text-align:center">통합과학의 연수 절차는 활용하되, 지식·이해 / 과정·기능 / 가치·태도가 수업과 평가에 고르게 반영되도록</p>
  {src('5쪽 Ⅳ-2')}
</section>''')

# 10 Ⅴ 지필 문항 타겟팅
rowsV = [('A', '$Q$의 의미를 $K$와 비교하여 설명하고 반응 방향 예측', '$Q$와 $K$를 비교하여 반응 방향과 근거 설명'),
         ('B', '$Q$를 구하고 $K$와 비교', '$Q$ 계산 후 $K$와 크기 비교'), ('C', '$Q$를 구함', '주어진 농도로 $Q$ 계산'),
         ('D', '반응 방향 예측에 $Q$가 활용됨을 말함', '$Q$의 활용 목적 말하기'), ('E', '현재 상태를 $Q$로 표현할 수 있음을 말함', '현재 상태를 나타내는 값의 명칭 확인')]
S.append(f'''<section class="slide" data-sec="Ⅴ · 성취수준에 근거한 지필평가" data-title="지필평가 문항 타겟팅">
  <h2><span class="no">7</span>문항 타겟팅 — 계산량이 아니라 <mark>수행 특성</mark>으로</h2>
  <div class="std"><span class="code">12화학03-03</span>반응 지수의 의미를 알고, 이를 평형 상수와 비교하여 반응의 진행 방향을 예측할 수 있다.</div>
  <table class="tight" style="margin-top:12px"><tr><th style="width:80px">수준</th><th class="l">성취수준의 주요 수행 특성</th><th class="l">문항 요구 예시</th></tr>
    {''.join(f'<tr><td>{lvdot(l)}</td><td class="l">{a}</td><td class="l">{b}</td></tr>' for l, a, b in rowsV)}</table>
  <div class="note puzzle" style="margin-top:10px">복잡한 $Q$ 계산도 C 수준 수행을 확인하는 문항일 수 있고, 간단한 반응 방향 예측도 A 수준 수행을 확인할 수 있습니다.</div>
  <p class="small cs1-src">출처: 컨설팅 자료 6쪽 Ⅴ · 표는 공식 진술문의 핵심을 요약한 예시</p>
</section>''')

# 11 Ⅵ 수행평가
S.append(f'''<section class="slide" data-sec="Ⅵ · 성취수준에 근거한 수행평가" data-title="수행평가 설계 예시">
  <h2><span class="no">8</span>수행평가 — 관찰 가능한 행동으로 채점기준을</h2>
  <div class="std"><span class="code">12화학04-02</span>몰 농도의 의미를 이해하고, 원하는 몰 농도의 용액을 만들 수 있다. <b>과제</b> 0.10 M 염화 나트륨 수용액 100 mL 제조 + 계산 근거·실험 절차 설명 → 후속: 조건 변경</div>
  <div class="row" style="margin-top:12px">
    <div class="col"><table class="tight"><tr><th class="l">평가 요소</th><th class="l">관찰 가능한 수행 증거</th></tr>
      <tr><td class="l">개념 이해</td><td class="l">목표 농도와 부피로 용질의 질량 계산</td></tr>
      <tr><td class="l">실험 계획</td><td class="l">도구 선택, 제조 절차 구성</td></tr>
      <tr><td class="l">실험 수행</td><td class="l">질량 측정, 용해, 용액 이동·표선 맞추기</td></tr>
      <tr><td class="l">조건 변화 적용</td><td class="l">다른 농도의 용액 제조 방법 제시</td></tr></table></div>
    <div class="col" style="flex:0 0 380px"><h3>성취수준과의 연계</h3>
      <ul class="cs1-lvlist">
        <li>{lvdot('A')}실험 설계·수행 + 조건 변화 적용</li><li>{lvdot('B')}조건 변경을 통한 용액 제조</li><li>{lvdot('C')}주어진 농도의 용액 제조</li><li>{lvdot('D')}제시된 절차에 따른 제조</li><li>{lvdot('E')}몰 농도 표현 인식, 실험 참여</li></ul></div>
  </div>
  <p class="small cs1-src">출처: 컨설팅 자료 7쪽 Ⅵ · 가치·태도는 발표·성찰 기록 등 관찰 가능한 증거로</p>
</section>''')

# 12 Ⅶ 고정 vs 추정 (그림)
lad = []
for k, (l, r, sc) in enumerate(zip('ABCDE', ['90% 이상', '80% 이상', '70% 이상', '60% 이상', '40% 이상'], [90, 80, 70, 60, 40])):
    y = 30 + k * 56
    lad.append(f'<rect x="330" y="{y}" width="80" height="46" rx="6" fill="{LV[l]}"/>' + tx(370, y + 32, l, 24, 'middle', '800', '#fff' if l in 'ABC' else INK))
    lad.append(f'<rect x="420" y="{y}" width="130" height="46" rx="6" fill="#EEF1FB"/>' + tx(485, y + 30, r, 19, 'middle', '700'))
    lad.append(f'<line x1="120" y1="{y+23}" x2="326" y2="{y+23}" stroke="{PLUS}" stroke-width="1.5" stroke-dasharray="5 4"/>' + tx(108, y + 30, f'{sc}점', 21, 'end', '800'))
    lad.append(f'<line x1="554" y1="{y+23}" x2="700" y2="{y+23}" stroke="{PLUS}" stroke-width="1.5" stroke-dasharray="5 4"/><rect x="704" y="{y+8}" width="60" height="30" rx="5" fill="#fff" stroke="{INK}" stroke-width="2"/>' + tx(774, y + 30, '점', 19))
lad.append(tx(160, 330, '고정분할점수: 성취율 = 점수', 19, 'middle', '700', '#0E7490') + tx(680, 330, '추정분할점수: 평가도구 내용 분석', 19, 'middle', '700', LV['B']))
S.append(f'''<section class="slide" data-sec="Ⅶ · 추정분할점수의 이해" data-title="고정분할점수와 추정분할점수">
  <h2><span class="no">9</span>추정분할점수는 기준을 낮추는 제도가 아니다</h2>
  <svg class="fig" viewBox="0 0 820 340" style="width:820px;display:block;margin:0 auto" aria-label="성취수준별 기준 성취율과 고정·추정 분할점수 비교">{''.join(lad)}</svg>
  <div class="row" style="margin-top:6px">
    <div class="col note"><b>고정</b> 성취율 90·80·70·60·40%를 점수 90·80·70·60·40점에 그대로 대응(40% 미만은 미도달)</div>
    <div class="col note puzzle"><b>추정</b> 교과 특성·문항 난이도를 고려해 그 성취에 해당하는 점수를 교사 협의로 추정</div>
  </div>
  <p class="small cs1-src">출처: 컨설팅 자료 8~9쪽 Ⅶ-1·3(그림은 stas.moe.go.kr 자료를 재구성한 자료 9쪽 그림을 다시 그림) · E·미도달 처리는 해당 학년도 학업성적관리 지침 확인</p>
</section>''')

# 13 Ⅶ MCP + 절차
S.append(f'''<section class="slide" data-sec="Ⅶ · 추정분할점수의 이해" data-title="최소능력자와 산출 절차">
  <h2><span class="no">10</span>최소능력자(MCP) — 그 수준에 <mark>가까스로</mark> 도달한 가상의 학생</h2>
  <div class="row">
    <div class="col pane plus"><h3 class="cs1-no">✕ 아닙니다</h3><p class="f21">그 수준의 평균적인 학생, 가장 우수한 학생, 우리 반의 특정 학생</p></div>
    <div class="col pane elec"><h3 class="cs1-ok">○ 이렇게 상정합니다</h3><p class="f21">학기단위 성취수준 진술문에 근거한 기대 수행 특성을 협의</p></div>
  </div>
  <div class="card q" style="margin-top:14px"><p class="f21"><b>화학 협의 예시(반응 지수)</b> C 수준 경계 학생 = 주어진 농도로 $Q$를 계산할 수 있는 학생 · B 수준 경계 학생 = $Q$를 계산하고 $K$와 비교할 수 있는 학생</p></div>
  <div class="cs1-steps c5" style="margin-top:16px">
    <div class="it"><span class="n">1</span><p>학기단위 성취수준 진술문 확인</p></div><div class="it"><span class="n">2</span><p>성취수준별 최소능력 특성 확인</p></div>
    <div class="it"><span class="n">3</span><p>평가 문항 검토</p></div><div class="it"><span class="n">4</span><p>성취수준별 예상 정답률 추정</p></div><div class="it hl"><span class="n">5</span><p>성취수준별 분할점수 설정</p></div>
  </div>
  {src('8~9쪽 Ⅶ-2·3, 11쪽 Ⅶ-4')}
</section>''')

# 14 Ⅶ 타겟팅 예시 (자료 10쪽)
items = [(1,'쉬움','3.1','CCC'),(2,'보통','3.5','BCB'),(3,'어려움','3.8','ACB'),(4,'보통','3.5','CBB'),(5,'보통','3.6','BBB'),(6,'보통','3.5','AAA'),(7,'쉬움','3.3','CCC'),
         (8,'어려움','4.1','AAA'),(9,'쉬움','3.3','CBB'),(10,'보통','3.6','BBB'),(11,'쉬움','3.1','CCC'),(12,'어려움','3.8','BBB'),(13,'보통','3.5','BBB'),(14,'어려움','4.1','AAA')]
def irow(it): n,d,b,t=it; return f'<tr><td>{n}</td><td>{d}</td><td>{b}</td><td>{lvdot(t[0])}</td><td>{lvdot(t[1])}</td><td style="background:#F4F5FB">{lvdot(t[2])}</td></tr>'
hdr = '<tr><th>번호</th><th>난이도</th><th>배점</th><th>교사1</th><th>교사2</th><th>종합</th></tr>'
S.append(f'''<section class="slide" data-sec="Ⅶ · 추정분할점수의 이해" data-title="문항 타겟팅 예시">
  <h2><span class="tag ex">예시</span>두 교사의 타겟팅이 얼마나 일치하나</h2>
  <div class="row">
    <div class="col"><table class="tight cs1-mini">{hdr}{''.join(irow(i) for i in items[:7])}</table></div>
    <div class="col"><table class="tight cs1-mini">{hdr}{''.join(irow(i) for i in items[7:])}</table></div>
    <div class="col" style="flex:0 0 300px">
      <div class="cs1-stat"><span>문항 수 · 배점</span><b>28문항 · 100점</b></div>
      <div class="cs1-stat"><span>교사1-2 가중 일치도</span><b>0.682</b></div>
      <div class="cs1-stat"><span>급내상관계수(ICC)</span><b>0.809</b></div>
      <div class="cs1-stat"><span>Fleiss' Kappa</span><b>0.722</b></div>
    </div>
  </div>
  <div class="note" style="margin-top:12px"><b>판별 수준</b> 그 문항을 약 2/3가 맞힐 성취수준 · <b>종합</b> 타겟팅을 모으면 평균 성취수준이 산출 · 일치도가 상관성 있도록 협의</div>
  <p class="small cs1-src">출처: 컨설팅 자료 10쪽(1차 지필 1~14번, 모두 선택형)</p>
</section>''')

# 15 Ⅶ 유형·난이도별 정답률
rows15 = [('CCCACB','3.50','선택형','쉬움','20.1',[80,70,60,50,40]),('CAAAABBBC','4.22','선택형','보통','36.1',[73,63,53,43,33]),('BAA','4.67','선택형','어려움','13.8',[69,59,49,39,29]),
          ('D','2.00','서답형','쉬움','2',[80,70,60,50,40]),('CCCB','3.25','서답형','보통','22',[68,58,48,38,28]),('B','4.00','서답형','어려움','6',[60,50,40,30,20])]
S.append(f'''<section class="slide" data-sec="Ⅶ · 추정분할점수의 이해" data-title="유형·난이도별 정답률">
  <h2><span class="tag ex">예시</span>유형·난이도별 타겟팅 평균 → 수준별 정답률</h2>
  <table class="tight"><tr><th>타겟팅</th><th>평균점</th><th>유형</th><th>난이도</th><th>배점합</th>{''.join(f'<th style="background:{LV[l]};color:{"#fff" if l in "ABC" else INK}">{l}({5-k})</th>' for k,l in enumerate('ABCDE'))}</tr>
    {''.join(f'<tr><td><span data-audit="skip">{a}</span></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td>' + ''.join(f'<td style="background:#FFF8E6">{v}</td>' for v in f) + '</tr>' for a,b,c,d,e,f in rows15)}</table>
  <div class="note" style="margin-top:14px">유형과 난이도별로 타겟팅 평균점을 확인한 뒤, 그 타겟팅에 맞게 <b>성취수준별 정답률</b>을 작성하여 분할점수를 산출합니다. 평균점은 A=5 … E=1로 환산한 값입니다.</div>
  <p class="small cs1-src">출처: 컨설팅 자료 10쪽 하단 표(1차 시험)</p>
</section>''')

# 16 Ⅷ 산출 절차
S.append(f'''<section class="slide" data-sec="Ⅷ · 추정분할점수 산출의 실제" data-title="산출 절차">
  <h2><span class="no">11</span>추정분할점수 산출 7단계</h2>
  <div class="flow" style="margin-top:6px">
    <span class="fnode">학기단위 성취수준 확인</span><span class="farr">→</span><span class="fnode">최소능력자 특성 합의</span><span class="farr">→</span><span class="fnode">문항 검토</span><span class="farr">→</span><span class="fnode">문항 범주화</span><span class="farr">→</span>
    <span class="fnode">기대 정답률·기대 점수 추정</span><span class="farr">→</span><span class="fnode">교사별 결과 협의·재평정</span><span class="farr">→</span><span class="fnode hl">최종 분할점수 산출·근거 기록</span>
  </div>
  <div class="row" style="margin-top:20px">
    <div class="col card"><h3>문항 타겟팅</h3><p class="f21">문항의 수행 요구를 판단하는 과정</p></div>
    <div class="col card"><h3>기대 정답률</h3><p class="f21">그 수준의 최소능력자가 문항을 해결할 가능성을 추정 — 상위 수준 문항도 <b>부분 점수·정답 가능성</b>을 고려</p></div>
    <div class="col card"><h3>기대 점수</h3><p class="f21">선택형: 배점 × 기대 정답률의 합<br>서답형: 기대 부분 점수의 합</p></div>
  </div>
  {src('11쪽 Ⅷ-1·2')}
</section>''')

# 17 Ⅷ 기대 점수 계산기 (실험실)
items17 = [('몰의 정의', 3, 95), ('평형 상수식', 3, 90), ('평형 상수 계산', 4, 85), ('$Q$와 $K$ 비교', 5, 75), ('평형 이동 예측', 5, 65)]
rr = ''.join(f'<tr><td class="l">{n}</td><td>{b}</td><td style="width:330px"><input type="range" min="0" max="100" step="5" value="{v}" data-i="r{k}" data-b="{b}" aria-label="{n} 기대 정답률" style="width:200px;vertical-align:middle"> <output data-o="r{k}"></output></td><td><output data-o="s{k}"></output></td></tr>' for k,(n,b,v) in enumerate(items17))
S.append(f'''<section class="slide" data-sec="Ⅷ · 추정분할점수 산출의 실제" data-title="기대 점수 계산기">
  <h2><span class="tag">해 보기</span>A 경계 학생의 기대 점수는?</h2>
  <div class="lab" data-lab="cs1exp" style="display:block">
    <table class="tight"><tr><th class="l">가상 문항</th><th>배점</th><th>A 경계 학생 기대 정답률</th><th>기대 점수</th></tr>{rr}
      <tr style="background:#FFF8D6"><td class="l"><b>합계</b></td><td>20</td><td>—</td><td><b><output data-o="sum"></output></b></td></tr></table>
    <div class="row" style="margin-top:14px;align-items:center">
      <div class="res" style="flex:0 0 380px"><div class="small">100점 환산 = A 분할점수 후보</div><div class="big"><output data-o="conv"></output></div></div>
      <div class="col note">처음 값은 자료의 설명용 가상 평정값(합계 15.95, 환산 79.75점)입니다. 고정된 권장 정답률이 아닙니다. <button class="btn" data-act="reset" style="margin-left:8px">처음으로</button></div>
    </div>
  </div>
  {src('11쪽 Ⅷ-2 표(가상 문항) · 서답형은 $Q$ 계산, $K$ 비교, 방향 예측, 근거 설명을 각각 채점하면 부분 점수 가능')}
</section>''')

# 18 Ⅷ 교과협의
S.append(f'''<section class="slide" data-sec="Ⅷ · 추정분할점수 산출의 실제" data-title="교과협의의 역할">
  <h2><span class="no">12</span>교과협의 — 차이를 줄이되, 목표 비율에 맞추지 않는다</h2>
  <div class="stages">
    <div class="stage"><h3>독립 평정</h3><p>교사별로 먼저 따로 평정합니다.</p></div>
    <div class="stage"><h3>근거 공유·재평정</h3><p>차이가 나는 문항의 근거를 공유하고 필요하면 재평정합니다.</p></div>
    <div class="stage"><h3>근거 기록</h3><p>평가 영역별 반영비율과 최종 산출 근거를 확인해 기록합니다.</p></div>
  </div>
  <div class="pane plus" style="margin-top:20px"><p class="f22"><b class="cs1-no">✕</b> 특정 성취도 비율을 목표로 평정값을 조정하지 않습니다.</p></div>
  {src('11쪽 Ⅷ-3')}
</section>''')

# 19 Ⅸ 학교 결과 (그림)
ratio = {'A': 43.14, 'B': 21.57, 'C': 12.75, 'D': 21.57, 'E': 0.98}
g = ['<line x1="50" y1="250" x2="520" y2="250" stroke="#16233D" stroke-width="2"/>']
for v in (0, 10, 20, 30, 40, 50):
    y = 250 - v * 4.4; g.append(f'<line x1="50" y1="{y}" x2="520" y2="{y}" stroke="#E3E7EE" stroke-width="1"/>' + tx(42, y + 6, f'{v}', 18, 'end', fill=MUTED))
for k, l in enumerate('ABCDE'):
    x = 80 + k * 90; h = ratio[l] * 4.4
    g.append(f'<g data-anim="scale" data-from="1,0" data-o="{x+30},250" data-dur="1" data-delay="{k*0.1:.1f}" data-ease="out"><rect x="{x}" y="{250-h:.1f}" width="60" height="{h:.1f}" rx="4" fill="{LV[l]}"/></g>')
    g.append(tx(x + 30, 240 - h, f'{ratio[l]}', 19, 'middle', '700') + tx(x + 30, 278, l, 20, 'middle', '800'))
cut = {'A': (67, 80), 'B': (55, 72), 'C': (44, 64), 'D': (30, 54)}
c2 = ['<line x1="50" y1="250" x2="520" y2="250" stroke="#16233D" stroke-width="2"/>']
for v in (0, 20, 40, 60, 80):
    y = 250 - v * 2.6; c2.append(f'<line x1="50" y1="{y}" x2="520" y2="{y}" stroke="#E3E7EE" stroke-width="1"/>' + tx(42, y + 6, f'{v}', 18, 'end', fill=MUTED))
for k, l in enumerate('ABCD'):
    x = 80 + k * 112; s, j = cut[l]
    c2.append(f'<rect x="{x}" y="{250-s*2.6:.1f}" width="40" height="{s*2.6:.1f}" rx="4" fill="{LV["B"]}"/><rect x="{x+44}" y="{250-j*2.6:.1f}" width="40" height="{j*2.6:.1f}" rx="4" fill="{GRAV}"/>')
    c2.append(tx(x + 20, 242 - s * 2.6, str(s), 18, 'middle', '700') + tx(x + 64, 242 - j * 2.6, str(j), 18, 'middle', '700') + tx(x + 42, 276, l, 20, 'middle', '800'))
c2.append(f'<rect x="360" y="6" width="18" height="18" rx="3" fill="{LV["B"]}"/>' + tx(384, 22, '학교', 18) + f'<rect x="436" y="6" width="18" height="18" rx="3" fill="{GRAV}"/>' + tx(460, 22, '점검단', 18))
S.append(f'''<section class="slide" data-sec="Ⅸ · 학교 성취평가 운영 결과" data-title="학교 운영 결과">
  <h2><span class="no">13</span>한영고 화학 — A 비율은 높고, A 분할점수는 낮다</h2>
  <div class="row">
    <div class="col pane grav"><h3 style="text-align:center">성취도 비율 (%)</h3><svg class="fig" viewBox="0 0 540 290" style="width:100%" aria-label="성취수준별 성취도 비율 막대그래프">{''.join(g)}</svg></div>
    <div class="col pane grav"><h3 style="text-align:center">최종 분할점수 (점) — 학교 vs 점검단</h3><svg class="fig" viewBox="0 0 540 290" style="width:100%" aria-label="학교와 점검단의 성취수준별 분할점수 비교 막대그래프">{''.join(c2)}</svg></div>
  </div>
  <div class="note" style="margin-top:12px">과목 원점수 평균 <b>60점</b>, 표준편차 <b>16점</b> · A 비율이 전국평균보다 <b>1표준편차 이상 높고(지표1)</b>, A 분할점수가 <b>2표준편차 이상 낮음</b></div>
  <p class="small cs1-src">출처: 컨설팅 자료 12쪽 Ⅸ 표·그림을 다시 그림 · E 분할점수는 학교·점검단 모두 0</p>
</section>''')

# 20 Ⅸ 우수한 점 + 협의 방향
S.append(f'''<section class="slide" data-sec="Ⅸ · 학교 성취평가 운영 결과" data-title="우수한 점과 협의 방향">
  <h2><span class="no">14</span>잘한 점은 살리고, 근거를 함께 맞춥니다</h2>
  <div class="row stretch">
    <div class="col pane elec"><h3 class="cs1-ok">○ 우수한 점</h3><ul class="f21">
      <li>1차 지필: 기본 개념부터 양적 관계 분석, 분자 구조 추론까지 다양한 유형</li>
      <li>2차 지필: 그래프·입자 모형·실험 자료로 과정·기능까지 확인</li>
      <li>수행평가: 화학의 유용성 조사, 분자 구조 모델링, 표준 용액 만들기 — 교육과정 연계 탐구</li>
      <li>A 분할점수는 점검단과 일치</li></ul></div>
    <div class="col pane minus"><h3 style="color:var(--minus)">함께 협의할 방향</h3><ul class="f21">
      <li>성취수준별 <b>경계 학생</b>의 기대 정답률·수행 정도 교과협의</li>
      <li><b>D·E 수준</b> 성취 특성을 확인하는 평가 요소 보완</li>
      <li>수행평가 <b>채점기준 구체화</b></li>
      <li>2차 12번: 출제 의도를 존중하며 전류의 세기·중화점 관계 조건이나 자료 제시 권장</li></ul></div>
  </div>
  <p class="small cs1-src">출처: 컨설팅 자료 12~13쪽 Ⅸ-1·2</p>
</section>''')

# 21 Ⅹ 환류
S.append(f'''<section class="slide" data-sec="Ⅹ · 발전 방향" data-title="평가 결과의 환류">
  <h2><span class="no">15</span>평가는 성취도 산출로 끝나지 않는다</h2>
  <div class="cs1-steps">
    <div class="it"><span class="n">1</span><p>학생의 응답·수행 결과 분석</p></div>
    <div class="it"><span class="n">2</span><p>개념 이해·탐구 과정에서 보완할 부분 파악</p></div>
    <div class="it"><span class="n">3</span><p>다음 수업·평가 설계에 반영</p></div>
    <div class="it hl"><span class="n">4</span><p>예상 정답률과 실제 정답률의 차이 → 차기 평가 개선 자료</p></div>
  </div>
  <div class="pane plus" style="margin-top:22px"><p class="f22"><b class="cs1-no">✕</b> 사후에 성취도 분포에 맞추어 분할점수를 <b>임의로 변경</b>하는 것과는 구분합니다.</p></div>
  {src('13쪽 Ⅹ-1')}
</section>''')

# 22 Ⅹ 체크리스트
chk = ['학기단위 성취수준이 수업과 평가의 준거로 활용되고 있는가?', '문항의 수행 요구와 성취수준 진술문을 연결하고 있는가?', '다양한 수준의 성취를 확인할 평가 증거를 확보하고 있는가?',
       '수행평가의 채점기준이 관찰 가능한 수행으로 구체화되어 있는가?', '경계 학생의 기대 수행과 분할점수 산출 근거를 공유하고 있는가?', '평가 결과를 학생의 학습 지원과 다음 수업 개선에 활용하는가?']
S.append(f'''<section class="slide" data-sec="Ⅹ · 발전 방향" data-title="교과협의 체크리스트" data-tpl="check">
  <h2><span class="tag ink">정리</span>교과협의에서 함께 살펴볼 여섯 가지</h2>
  <div class="chips col1">{''.join(f'<button class="chk">{c}</button>' for c in chk)}</div>
  {src('13쪽 Ⅹ-2')}
</section>''')

# 23 질의응답
S.append('''<section class="slide cs1-qa" data-sec="질의응답" data-title="질의응답">
  <div class="cs1-qawrap">
    <p class="cs1-qabig">질의응답</p>
    <p class="f22 cs1-muted">우리 학교의 평가 결과는 학생이 무엇을 알고 할 수 있는지 충분히 설명하고 있는가?</p>
    <p class="cs1-who"><b>여수고등학교</b> · 교사 허재형</p>
  </div>
</section>''')

open(os.path.join(D, 'slides.html'), 'w', encoding='utf-8').write('<!-- 화학 성취평가제 컨설팅 (한영고) — make.py로 생성 -->\n' + '\n\n'.join(S) + '\n')
print(len(S), '장')
