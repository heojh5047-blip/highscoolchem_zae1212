#!/usr/bin/env python3
# 3-2-3 slides.html 생성기 (그림 좌표 계산). 출력: 덱 폴더 slides.html
import math, random, sys
OUT = sys.argv[1]

def A(x, y, r, el, lab='-'):
    return f'<g data-atom="{x:.1f},{y:.1f},{r},{el},{lab}"></g>'
def two(x, y, r, el, a=0, k=0.75):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    d = k * r
    return A(x - d*c, y - d*s, r, el) + A(x + d*c, y + d*s, r, el)
def n2(x, y, a=0, r=12): return two(x, y, r, 'N', a)
def h2(x, y, a=0, r=9): return two(x, y, r, 'H', a, 0.72)
def o2(x, y, a=0, r=8): return two(x, y, r, 'O', a)
def nh3(x, y, r=12, rh=9):
    return A(x-14, y+9, rh, 'H') + A(x+14, y+9, rh, 'H') + A(x, y-15, rh, 'H') + A(x, y, r, 'N')
def T(x, y, mix, size=20, anchor='middle', fill='#16233D', w=None, halo=False, step=None, extra=''):
    s = f'<text class="tex{" step" if step else ""}"' + (f' data-g="{step}"' if step and step is not True else '')
    s += f' x="{x}" y="{y}" data-mix="{mix}" data-size="{size}" data-anchor="{anchor}" fill="{fill}"'
    if w: s += f' data-weight="{w}"'
    if halo: s += ' data-halo="1"'
    return s + extra + '></text>'
def hb(x, y, r=16, ox=False, lab=True, size=18):
    s = ''
    if ox:
        for a in (45, 135, 225, 315):
            c, sn = math.cos(math.radians(a)), math.sin(math.radians(a))
            s += o2(x + (r+6)*c, y + (r+6)*sn, a+90, 5)
    s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9C6B8E" stroke="#6E4A64" stroke-width="1.5"/>'
    if lab: s += T(x, y + 6, 'Hb', size, fill='#FFFFFF', w=700)
    return s
def flower(cx, cy, R, col, n, seed):
    rnd = random.Random(seed); s = ''
    pts = []
    while len(pts) < n:
        a = rnd.random()*6.283; rr = R*math.sqrt(rnd.random())
        p = (cx + rr*math.cos(a), cy + rr*math.sin(a)*0.85)
        if all((p[0]-q[0])**2 + (p[1]-q[1])**2 > 15**2 for q in pts): pts.append(p)
    for (x, y) in pts:
        for k in range(4):
            a = math.radians(45 + 90*k + rnd.random()*20)
            s += f'<circle cx="{x+6*math.cos(a):.1f}" cy="{y+6*math.sin(a):.1f}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="1"/>'
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="#FFFFFF"/>'
    return s

H = []
def add(s): H.append(s)

# ───────── 1. 표지
cover_box = ''
for (x, y) in [(330, 340), (440, 330), (360, 420), (465, 425)]:
    cover_box += nh3(x, y, 11, 8)
add(f'''<!-- ════════ 1. 표지 ════════ -->
<section class="slide cover" data-sec="Ⅲ. 화학 평형" data-title="표지">
  <div class="cover-text">
    <div class="kicker">Ⅲ. 화학 평형 › 2. 화학 평형 이동 › 03</div>
    <h1 class="cm323-h1">일상생활 속의<br><span class="acc">화학 평형 이동</span></h1>
    <p class="sub">우리 몸과 공장에서 평형은 어떻게 쓰일까?</p>
    <p class="meta">고등학교 화학 124–126쪽</p>
  </div>
  <svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="산소와 결합하는 적혈구, 암모니아 분자가 든 반응 용기"><circle cx="270" cy="270" r="250" fill="#EEF3F8"/>
  <ellipse cx="185" cy="185" rx="92" ry="62" fill="#C8434A"/><ellipse cx="185" cy="185" rx="50" ry="26" fill="#A8323A"/>
  <g data-anim="move" data-from="-40,-30" data-dur="2" data-rep="alt" data-ease="sine">{o2(95,95,30,11)}{o2(290,105,-20,11)}{o2(270,265,60,11)}</g>
  {T(185,290,'적혈구',24,w=700)}
  <rect x="285" y="290" width="215" height="170" rx="18" fill="#FFFFFF" stroke="#7E8B98" stroke-width="4"/>
  <g data-anim="fade" data-dur="1.6" data-delay=".4">{cover_box}</g>
  {T(150,440,'$\\ce{N2 + 3H2 &lt;=&gt; 2NH3}$',26)}
  </svg>
</section>
''')

# ───────── 2. 목표
add('''<!-- ════════ 2. 학습 목표 ════════ -->
<section class="slide" data-sec="03 일상생활 속의 화학 평형 이동" data-title="학습 목표">
  <h2>학습 목표</h2>
  <div class="std"><span class="code">[12화학03-04]</span>농도, 압력, 온도 변화에 따른 화학 평형의 이동을 이해하고, 이를 일상생활 속 현상을 설명하는 데 적용하여 화학의 유용함을 느낄 수 있다.</div>
  <ol class="goals mt12">
    <li><b>생명 현상</b>과 <b>산업 현장</b>에서 화학 평형 이동을 이용한 사례를 설명할 수 있다.</li>
    <li>일상생활 속의 화학 평형 이동을 이용한 사례를 통해 <b>화학의 유용함</b>을 인식할 수 있다.</li>
  </ol>
  <h3 class="mt16">오늘의 흐름</h3>
  <div class="flow">
    <div class="fnode hl">헤모글로빈</div><div class="farr">→</div>
    <div class="fnode hl">고산병</div><div class="farr">→</div>
    <div class="fnode hl">수득률</div><div class="farr">→</div>
    <div class="fnode hl">암모니아 합성</div><div class="farr">→</div>
    <div class="fnode">실험실</div><div class="farr">→</div>
    <div class="fnode">문항</div>
  </div>
  <div class="note mt20"><b>지난 시간</b> 농도, 압력, 온도가 변하면 그 변화가 감소하는 방향으로 화학 평형이 이동한다(르샤틀리에 원리).</div>
</section>
''')

# ───────── 3. 생각 열기 (수국)
def plant(cx, col, seed, soil, soilcol):
    s = f'<path d="M{cx} 250 V170" stroke="#3E7D4A" stroke-width="6"/>'
    s += f'<ellipse cx="{cx-34}" cy="205" rx="30" ry="12" fill="#5FA35F" transform="rotate(-25 {cx-34} 205)"/><ellipse cx="{cx+34}" cy="215" rx="30" ry="12" fill="#5FA35F" transform="rotate(25 {cx+34} 215)"/>'
    s += f'<g data-anim="fade" data-dur="1.6" data-delay=".5">{flower(cx, 120, 62, col, 22, seed)}</g>'
    s += f'<rect x="{cx-110}" y="250" width="220" height="40" rx="8" fill="{soilcol}"/>'
    s += T(cx, 277, soil, 21, fill='#FFFFFF', w=700)
    return s
add(f'''<!-- ════════ 3. 생각 열기 ════════ -->
<section class="slide" data-sec="03 일상생활 속의 화학 평형 이동 · 도입" data-title="생각 열기: 수국의 색">
  <h2><span class="tag">생각 열기</span>같은 수국인데 왜 색이 다를까?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 560px"><svg class="fig" viewBox="0 0 560 300" style="width:540px" aria-label="산성 토양의 파란색 수국과 염기성 토양의 분홍색 수국"><rect x="0" y="0" width="560" height="300" rx="18" fill="#F4F6F8"/>{plant(140,'#5B8DEF',3,'산성 토양','#7A5A3A')}{plant(420,'#E98BB5',7,'염기성 토양','#A08060')}</svg></div>
    <div class="col">
      <p class="f22">수국은 <b>산성 토양</b>에서는 파란색 꽃이 피고, <b>염기성 토양</b>에서는 분홍색 꽃이 핀다.</p>
      <div class="card q mt16"><p class="f22"><b>Q</b> 토양에 따라 수국꽃의 색이 달라지는 것도 화학 평형 이동과 관련이 있을까?</p></div>
      <p class="f21 step cm323-a mt12">→ 관련이 있다. 토양의 산성도가 다르면 토양 속 수소 이온 농도가 달라지므로, 농도 변화에 의한 화학 평형 이동이 일어난다. 원리는 소단원 마무리(창의력 키우기)에서 조사한다.</p>
    </div>
  </div>
  <p class="f22 mt16">일상생활에서 일어나는 여러 가지 현상을 화학 평형 이동으로 설명할 수 있다. 오늘은 <b>몸속 생명 현상</b>과 <b>산업 현장</b>의 예를 살펴본다.</p>
</section>
''')

# ───────── 4. 연결
add('''<!-- ════════ 4. 연결 ════════ -->
<section class="slide" data-sec="03 일상생활 속의 화학 평형 이동 · 도입" data-title="연결: 르샤틀리에 원리 다시 보기">
  <h2><span class="tag alt">연결</span>르샤틀리에 원리 다시 보기</h2>
  <div class="row">
    <div class="col">
      <table class="tight cm323-tb">
        <tr><th>조건 변화</th><th>평형이 이동하는 방향</th></tr>
        <tr data-q><td class="l">반응물의 농도 증가</td><td><span class="blank"><span class="step">그 농도가 감소하는 방향(정반응)</span></span></td></tr>
        <tr data-q><td class="l">기체의 압력 증가</td><td><span class="blank"><span class="step">전체 기체 분자 수가 감소하는 방향</span></span></td></tr>
        <tr data-q><td class="l">온도를 낮춤</td><td><span class="blank"><span class="step">온도를 높이는 방향(발열 반응 쪽)</span></span></td></tr>
      </table>
      <p class="f22 mt16">평형 이동은 실험실 밖에서도 일어난다. 몸속에서 일어나는 생명 현상도 화학 평형 이동과 관련이 있고, 산업 현장에서는 생성물의 수득률을 높이는 공정을 설계하는 데 화학 평형 이동을 적용한다.</p>
    </div>
    <div class="col stack" style="flex:0 0 330px">
      <div class="card"><p class="f22"><b>① 생명 현상</b></p><p class="f21">혈액이 몸 구석구석에 산소를 공급하는 과정</p></div>
      <div class="card mt12"><p class="f22"><b>② 산업 현장</b></p><p class="f21">암모니아를 더 많이 얻는 조건 찾기</p></div>
    </div>
  </div>
</section>
''')

# ───────── 5. 헤모글로빈
lungO2 = ''.join(o2(x, y, a) for (x, y, a) in [(45,95,20),(80,140,-30),(40,185,60),(95,215,0),(60,250,-50),(110,90,80)])
cells = ''.join(f'<ellipse cx="{x}" cy="190" rx="22" ry="13" fill="#C8434A" stroke="#8E2A30" stroke-width="1.5"/>' for x in (190, 260, 330, 400))
tissue = ''.join(f'<circle cx="{x}" cy="{y}" r="22" fill="#F6D0C4" stroke="#D9A08E" stroke-width="2"/>' for (x, y) in [(500,95),(530,140),(495,185),(530,230),(495,265)])
add(f'''<!-- ════════ 5. 헤모글로빈 ════════ -->
<section class="slide" data-sec="03 · 생명 현상과 화학 평형 이동" data-title="헤모글로빈과 산소 운반">
  <h2><span class="no">1</span>혈액은 산소를 어떻게 운반할까?</h2>
  <div class="formula sm">$\\ce{{Hb(aq) + 4O2(g) &lt;=&gt; Hb(O2)4(aq)}}$<div class="unit">산소는 적혈구 속 헤모글로빈($\\ce{{Hb}}$)이 운반한다. $\\ce{{Hb(O2)4}}$: 산화 헤모글로빈</div></div>
  <div class="row mt8">
    <div class="col" style="flex:0 0 600px"><svg class="fig" viewBox="0 0 580 300" style="width:580px" aria-label="폐에서 산소와 결합한 적혈구가 혈관을 따라 조직으로 이동해 산소를 내놓음">
      <defs><linearGradient id="grad-cm323-05" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#D9534F"/><stop offset="1" stop-color="#8E3B5A"/></linearGradient></defs>
      <path d="M20 60 Q20 30 60 35 L130 45 Q160 50 160 90 V250 Q160 285 120 285 H50 Q20 285 20 250 Z" fill="#F7D6D6" stroke="#D99A9A" stroke-width="2"/>
      {lungO2}
      <rect x="160" y="165" width="300" height="50" fill="url(#grad-cm323-05)"/>
      <path d="M160 165 H460 M160 215 H460" stroke="#7A2A35" stroke-width="2"/>
      <g data-anim="move" data-from="-70,0" data-dur="2.4" data-rep="loop" data-ease="lin">{cells}</g>
      {tissue}
      <g data-arw="185,150,435,150,ink,2.5"></g>{T(310,138,'혈액의 흐름',19)}
      {T(90,25,'폐 (산소 많음)',20,w=700)}
      {T(510,45,'조직 (산소 적음)',20,w=700)}
      <g class="step" data-g="lung"><g data-arw="130,200,175,200,field,3.5"></g>{T(165,245,'정반응: 산소와 결합',19,anchor='start',fill='#2E9E6A',w=700,halo=True)}</g>
      <g class="step" data-g="tis"><g data-arw="445,200,478,200,bfield,3.5"></g>{T(470,280,'역반응: 산소를 내놓음',19,anchor='end',fill='#7B4FC8',w=700,halo=True)}</g>
    </svg>
    <p class="small">적혈구는 크기 비례 아님. 빨간 공 두 개 = $\\ce{{O2}}$</p></div>
    <div class="col">
      <p class="f21"><b>Q</b> 산소 농도가 높은 <b>폐</b>에서는 어느 반응이 우세할까?</p>
      <p class="f21 step cm323-a" data-g="lung">→ <span class="ans">정반응</span>. $\\ce{{O2}}$ 농도가 크므로 그 농도가 감소하는 방향으로 진행해 산화 헤모글로빈이 생성된다.</p>
      <p class="f21 mt16"><b>Q</b> 산소 농도가 낮은 <b>조직</b>에서는?</p>
      <p class="f21 step cm323-a" data-g="tis">→ <span class="ans">역반응</span>. 산화 헤모글로빈이 산소를 내놓아 조직에 산소를 공급한다.</p>
    </div>
  </div>
</section>
''')

# ───────── 6. 고산병 단계 카드
def card(nO2, nOx, nHb, seed):
    rnd = random.Random(seed); s = '<rect x="0" y="0" width="300" height="200" rx="12" fill="#F4F6F8"/>'
    s += '<rect x="0" y="110" width="300" height="90" rx="12" fill="#F3DCDC"/>'
    s += T(14, 30, '공기', 18, anchor='start', fill='#5B6B7F')
    s += T(14, 132, '혈액', 18, anchor='start', fill='#5B6B7F')
    pos = []
    while len(pos) < nO2:
        p = (70 + rnd.random()*210, 24 + rnd.random()*66)
        if all((p[0]-q[0])**2 + (p[1]-q[1])**2 > 30**2 for q in pos): pos.append(p)
    s += '<g data-anim="move" data-from="6,-4" data-dur="1.4" data-rep="alt" data-ease="sine">' + ''.join(o2(x, y, rnd.random()*180) for (x, y) in pos) + '</g>'
    xs = [40 + 52*i for i in range(nOx + nHb)]
    for i, x in enumerate(xs):
        s += hb(x, 162, 14, ox=i < nOx, size=17)
    return s
add(f'''<!-- ════════ 6. 고산병 ════════ -->
<section class="slide" data-sec="03 · 생명 현상과 화학 평형 이동" data-title="고지대와 고산병">
  <h2><span class="no">1</span>고지대에 가면 — 고산병과 적응</h2>
  <div class="stages cm323-cards">
    <div class="stage"><h3>① 평지</h3><svg class="fig" viewBox="0 0 300 200" aria-label="산소가 많고 산화 헤모글로빈이 많음">{card(8,3,1,1)}</svg>
      <p class="key">산소 농도가 높아 정반응이 잘 일어난다. 산화 헤모글로빈이 충분하다.</p></div>
    <div class="stage"><h3>② 고지대에 막 갔을 때</h3><svg class="fig" viewBox="0 0 300 200" aria-label="산소가 적고 산화 헤모글로빈이 줄어듦">{card(3,2,2,2)}</svg>
      <p class="key"><b>Q</b> 산소 농도가 낮으면 어느 반응이 잘 일어나지 못할까?</p>
      <p class="key step cm323-a">→ 정반응. 산화 헤모글로빈이 덜 생겨 조직에 산소를 충분히 공급하지 못한다 → 구토·현기증(<b>고산병</b>)</p></div>
    <div class="stage"><h3>③ 3주 이상 지낸 뒤</h3><svg class="fig" viewBox="0 0 300 200" aria-label="헤모글로빈이 늘어 산화 헤모글로빈이 다시 많아짐">{card(3,3,2,3)}</svg>
      <p class="key"><b>Q</b> 몸속 헤모글로빈의 양이 늘면?</p>
      <p class="key step cm323-a">→ 반응물이 늘어 다시 정반응이 잘 일어난다. 조직에 산소를 원활하게 공급한다.</p></div>
  </div>
  <p class="small mt4">보라색 공 $\\ce{{Hb}}$, 둘레에 $\\ce{{O2}}$ 4개가 붙은 것 = $\\ce{{Hb(O2)4}}$ (개수는 경향만 나타냄)</p>
  <p class="f22 step mt8"><mark>우리 몸은 외부 환경 변화에 대응해 자신의 상태를 일정하게 유지하려는 항상성이 있다.</mark></p>
</section>
''')

# ───────── 7. 수득률
add('''<!-- ════════ 7. 수득률 ════════ -->
<section class="slide" data-sec="03 · 산업 현장과 화학 평형 이동" data-title="수득률">
  <h2><span class="no">2</span>공장에서는 왜 수득률이 중요할까?</h2>
  <p class="f22">공장에서는 원하는 생성물을 많이 얻어야 한다. 그런데 가역 반응은 평형에 도달하면 반응물이 남는다.</p>
  <p class="f22 mt8"><mark>수득률: 화학 반응식으로부터 계산하여 얻을 수 있는 이론적인 생성물의 양과 실제로 얻어 낸 생성물의 양의 비율</mark></p>
  <div class="formula mt8">$\\text{수득률}(\\%)=\\dfrac{\\text{실제로 얻은 생성물의 양}}{\\text{이론적인 생성물의 양}}\\times100$</div>
  <div class="row mt8">
    <div class="col">
      <p class="f21"><b>예</b> $\\ce{N2}$ 1 몰과 $\\ce{H2}$ 3 몰을 반응시켰더니 $\\ce{NH3}$ 0.5 몰을 얻었다. 이론적인 양과 수득률은?</p>
      <p class="f21 step cm323-a">→ 계수비 $1:3:2$이므로 이론적으로 $\\ce{NH3}$ 2 몰, 수득률 $=\\dfrac{0.5}{2}\\times100=25\\ \\%$</p>
    </div>
    <div class="col">
      <p class="f21"><b>Q</b> 반응 시간을 아무리 길게 해도 수득률이 100 %가 되지 않는 까닭은?</p>
      <p class="f21 step cm323-a">→ 가역 반응이라 평형에 도달하면 반응물과 생성물이 함께 남는다. 그래서 <b>평형을 정반응 쪽으로 이동</b>시켜 수득률을 높인다.</p>
    </div>
  </div>
</section>
''')

# ───────── 8. 암모니아 합성 반응
left = n2(80, 110, 0) + h2(150, 70, 30) + h2(160, 150, -20) + h2(215, 105, 70)
right = nh3(390, 95) + nh3(470, 125)
add(f'''<!-- ════════ 8. 암모니아 합성 ════════ -->
<section class="slide" data-sec="03 · 산업 현장과 화학 평형 이동" data-title="암모니아 합성 반응">
  <h2><span class="no">2</span>암모니아 합성 — 수득률을 높이려면?</h2>
  <div class="formula">$\\ce{{N2(g) + 3H2(g) &lt;=&gt;[\\text{{에너지 방출}}][\\text{{에너지 흡수}}] 2NH3(g)}}$</div>
  <div class="row mt8">
    <div class="col" style="flex:0 0 560px"><svg class="fig" viewBox="0 0 560 230" style="width:540px" aria-label="질소 분자 1개와 수소 분자 3개가 암모니아 분자 2개가 됨">
      <rect x="20" y="20" width="230" height="170" rx="14" fill="#FFFFFF" stroke="#8C99A6" stroke-width="2" stroke-dasharray="7 5"/>
      <rect x="320" y="20" width="220" height="170" rx="14" fill="#FFFFFF" stroke="#8C99A6" stroke-width="2" stroke-dasharray="7 5"/>
      {left}
      <g data-anim="pop" data-dur="1.2" data-delay=".4" data-o="430,110">{right}</g>
      {T(285,112,'$\\ce{&lt;=&gt;}$',30)}
      {T(135,218,'분자 4개',21,w=700)}{T(430,218,'분자 2개',21,w=700)}
      {A(270,155,9,'H')}{T(286,162,'H',18,anchor='start')}{A(270,185,12,'N')}{T(288,192,'N',18,anchor='start')}
    </svg></div>
    <div class="col">
      <p class="f21 step">① 전체 기체 분자 수가 <b>4 → 2로 감소</b>한다.</p>
      <p class="f21 step">② 정반응은 에너지를 <b>방출</b>하는 반응(발열)이다.</p>
      <p class="f21 mt12"><b>Q</b> 수득률을 높이려면 압력은?</p>
      <p class="f21 step cm323-a">→ <span class="ans">높인다</span>. 압력이 감소하는 방향, 즉 분자 수가 적은 정반응 쪽으로 이동한다.</p>
      <p class="f21 mt8"><b>Q</b> 온도는?</p>
      <p class="f21 step cm323-a">→ <span class="ans">낮춘다</span>. 온도를 높이는 방향, 즉 발열 반응인 정반응 쪽으로 이동한다.</p>
    </div>
  </div>
  <p class="small">원자 수: N $2=2$, H $6=6$ (원자는 보존되고 분자 수만 줄어든다)</p>
</section>
''')

# ───────── 9. 현실의 조건
add('''<!-- ════════ 9. 현실의 조건 ════════ -->
<section class="slide" data-sec="03 · 산업 현장과 화학 평형 이동" data-title="현실의 조건과 촉매">
  <h2><span class="no">2</span>압력은 높게, 온도는 낮게? — 현실의 문제</h2>
  <table class="tight cm323-tb">
    <tr><th>조건</th><th>평형만 생각하면</th><th>실제 문제</th><th>산업 현장의 선택</th></tr>
    <tr data-q><td>압력</td><td>높을수록 좋다</td><td class="l"><span class="blank"><span class="step" data-g="p">큰 압력을 견디는 반응 용기가 필요해 비용이 많이 든다.</span></span></td><td><span class="blank"><span class="step" data-g="p2">적정 압력 (예: 약 200 기압)</span></span></td></tr>
    <tr data-q><td>온도</td><td>낮을수록 좋다</td><td class="l"><span class="blank"><span class="step" data-g="t">반응 속도가 느려져 생산 효율이 떨어진다.</span></span></td><td><span class="blank"><span class="step" data-g="t2">적정 온도 (예: 약 450 °C)</span></span></td></tr>
  </table>
  <div class="answer step mt16">적정 압력과 온도에서 <b>촉매</b>를 사용하여 암모니아를 합성한다.</div>
  <div class="row mt16">
    <div class="col"><div class="note"><b>촉매</b> 화학 반응에서 반응 속도를 조절하는 물질</div></div>
    <div class="col"><div class="note"><span class="tag alt">연계</span>『물질과 에너지』 '반응 속도' 단원에서 촉매와 반응 속도를 학습한다.</div></div>
  </div>
  <p class="small mt8">온도·압력 값은 산업 현장의 한 예이다(교과서는 "적정 압력과 온도"). 하버가 쓴 장치는 130~300 기압, 400~500 °C였다.</p>
</section>
''')

# ───────── 10. 예측: 촉매
def gx(t): return 70 + t*4.2
def gy(v): return 240 - v*1.8
fast = 'M' + ' L'.join(f'{gx(t):.1f} {gy(100*(1-math.exp(-t/9))):.1f}' for t in range(0, 101, 2))
slow = 'M' + ' L'.join(f'{gx(t):.1f} {gy(100*(1-math.exp(-t/45))):.1f}' for t in range(0, 101, 2))
add(f'''<!-- ════════ 10. 예측: 촉매 ════════ -->
<section class="slide" data-sec="03 · 산업 현장과 화학 평형 이동" data-title="예측: 촉매와 수득률">
  <h2><span class="tag q">예측</span>촉매를 넣으면 수득률이 커질까?</h2>
  <div class="row">
    <div class="col">
      <p class="f22"><b>Q</b> 암모니아 합성에 촉매를 넣으면 <b>평형에서</b> 얻는 암모니아의 양(수득률)은 어떻게 될까?</p>
      <div class="choices cm323-col mt8"><span>① 커진다.</span><span>② 변하지 않는다.</span><span>③ 작아진다.</span></div>
      <div class="answer step mt12">정답 ② 변하지 않는다</div>
      <p class="f21 step mt8">촉매는 정반응과 역반응을 <b>모두</b> 빠르게 하여 평형에 <b>빨리 도달</b>하게 할 뿐, 평형을 이동시키지 않는다.</p>
      <p class="f21 step mt8">그래도 촉매를 쓰는 까닭: 온도를 너무 높이지 않고도 빨리 반응시킬 수 있다.</p>
    </div>
    <div class="col" style="flex:0 0 520px"><svg class="fig" viewBox="0 0 520 300" style="width:510px" aria-label="촉매가 있으면 암모니아의 양이 빨리 늘지만 두 경우 모두 같은 평형값에 도달함">
      <path d="M{gx(0)} {gy(100)} H{gx(100)}" stroke="#5B6B7F" stroke-width="1.5" stroke-dasharray="6 5"/>
      {T(gx(100),gy(100)-10,'평형에서의 양',19,anchor='end',fill='#5B6B7F')}
      <g data-arw="70,240,500,240,ink,2"></g><g data-arw="70,240,70,25,ink,2"></g>
      {T(495,272,'시간',20,anchor='end')}{T(80,30,'$\\ce{NH3}$의 양',20,anchor='start')}
      <g class="step"><path d="{slow}" fill="none" stroke="#5B6B7F" stroke-width="3.5" stroke-dasharray="9 6" data-anim="draw" data-on="step" data-dur="2.2"/>{T(330,175,'촉매 없음',20,fill='#5B6B7F',w=700,halo=True)}
      <path d="{fast}" fill="none" stroke="#2E9E6A" stroke-width="4" data-anim="draw" data-on="step" data-dur="1.4"/>{T(140,90,'촉매 있음',20,fill='#2E9E6A',w=700,halo=True)}</g>
    </svg></div>
  </div>
</section>
''')

# ───────── 11. 생산 공정
add(f'''<!-- ════════ 11. 생산 공정 ════════ -->
<section class="slide" data-sec="03 · 산업 현장과 화학 평형 이동" data-title="암모니아 생산 공정">
  <h2><span class="no">2</span>암모니아 생산 공정</h2>
  <div class="row">
    <div class="col" style="flex:0 0 620px"><svg class="fig" viewBox="0 0 620 360" style="width:610px" aria-label="압축기, 촉매가 든 반응 용기, 냉각기를 거쳐 액체 암모니아를 얻고 남은 기체를 다시 보내는 공정">
      <path d="M10 150 H70" stroke="#7E8B98" stroke-width="10"/>
      <path d="M130 150 H190 M240 50 V30 H430 V60 M410 250 V320 H100 V185" fill="none" stroke="#7E8B98" stroke-width="10" stroke-linejoin="round"/>
      <g data-anim="dash" data-flow="1" data-speed="40"><path d="M10 150 H70 M130 150 H190 M240 50 V30 H430 V60 M410 250 V320 H100 V185" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="10 12"/></g>
      <circle cx="100" cy="150" r="34" fill="#E6EBF0" stroke="#5B6B7F" stroke-width="3"/>
      <g data-anim="spin" data-speed="90" data-o="100,150"><path d="M100 150 L100 122 M100 150 L124 164 M100 150 L76 164" stroke="#5B6B7F" stroke-width="5" stroke-linecap="round"/></g>
      <rect x="190" y="50" width="100" height="220" rx="40" fill="#F4F6F8" stroke="#5B6B7F" stroke-width="3"/>
      <g stroke="#8C99A6" stroke-width="2"><path d="M200 130 H280 M200 150 H280 M200 170 H280 M200 190 H280 M220 120 V200 M240 120 V200 M260 120 V200"/></g>
      <rect x="370" y="60" width="100" height="190" rx="18" fill="#F4F6F8" stroke="#5B6B7F" stroke-width="3"/>
      <path d="M380 90 q40 15 80 0 M380 120 q40 15 80 0 M380 150 q40 15 80 0 M380 180 q40 15 80 0 M380 210 q40 15 80 0" fill="none" stroke="#7FA9C2" stroke-width="5"/>
      <path d="M470 250 V290 L500 320 V345" fill="none" stroke="#7E8B98" stroke-width="10" stroke-linejoin="round"/>
      <g data-anim="move" data-from="0,-14" data-dur="1.2" data-rep="loop"><ellipse cx="500" cy="340" rx="7" ry="9" fill="#9FC3DD"/></g>
      {T(100,207,'압축기',20,w=700)}{T(240,295,'반응 용기',20,w=700)}{T(240,232,'촉매',19,fill='#5B6B7F')}{T(420,278,'냉각기',20,w=700,anchor='end')}
      {T(8,100,'$\\ce{N2(g)}$, $\\ce{H2(g)}$',19,anchor='start')}{T(335,20,'$\\ce{N2(g)}$, $\\ce{H2(g)}$, $\\ce{NH3(g)}$',19)}
      {T(255,345,'다시 보냄: $\\ce{N2(g)}$, $\\ce{H2(g)}$',19,halo=True)}{T(515,332,'$\\ce{NH3(l)}$',20,anchor='start',w=700)}
      <circle class="step" data-g="s1" cx="100" cy="150" r="44" fill="none" stroke="#E08A2C" stroke-width="4"/>
      <circle class="step" data-g="s3" cx="420" cy="155" r="70" fill="none" stroke="#E08A2C" stroke-width="4"/>
    </svg></div>
    <div class="col">
      <p class="f21 step" data-g="s1"><b>① 압축기</b> 압력을 높여 전체 기체 분자 수가 적은 쪽으로 평형을 이동시킨다 → 정반응 우세</p>
      <p class="f21 step mt8"><b>② 반응 용기</b> 촉매로 평형에 빨리 도달하게 한다.</p>
      <p class="f21 mt8"><b>Q</b> 냉각기에서 암모니아를 액체로 만들어 빼내면?</p>
      <p class="f21 step cm323-a" data-g="s3">→ 생성물을 제거하므로 <b>정반응</b>이 우세하게 진행한다.</p>
      <p class="f21 step mt8"><b>④</b> 반응하지 않은 $\\ce{{N2}}$, $\\ce{{H2}}$는 다시 보내 재사용한다.</p>
    </div>
  </div>
</section>
''')

# ───────── 12. 실험실
add('''<!-- ════════ 12. 실험실 ════════ -->
<section class="slide" data-sec="03 · 실험실" data-title="실험실: 암모니아 합성 조건">
  <h2><span class="tag">실험실</span>암모니아 합성 조건 실험실</h2>
  <div class="lab cm323-lab" data-lab="cm323nh3">
    <div class="lab-ctl" style="flex:0 0 372px">
      <div class="ctl"><div class="lbl"><span>온도</span><output data-o="tv"></output></div><input type="range" min="200" max="600" step="50" value="450" data-i="t" aria-label="온도"></div>
      <div class="ctl"><div class="lbl"><span>압력</span><output data-o="pv"></output></div><input type="range" min="10" max="400" step="10" value="200" data-i="p" aria-label="압력"></div>
      <div class="cm323-seg"><button class="btn" data-act="cat">촉매 있음</button><button class="btn cm323-add" data-act="rec">기록하기</button><button class="btn cm323-rs" data-act="reset">처음부터</button></div>
      <div class="res"><div class="small">평형 수득률</div><div class="big"><output data-o="y"></output></div><p class="small"><output data-o="sub"></output></p><output class="kind cm323-msg" data-o="msg"></output></div>
    </div>
    <div class="col" style="flex:0 0 704px">
      <div class="lab-fig" style="width:704px;height:304px"><svg viewBox="0 0 700 300" width="700" height="300" aria-label="압력에 따른 평형 수득률 그래프와 반응 용기 속 분자 모형"></svg></div>
      <table class="tight cm323-log mt8"><thead><tr><th>실험</th><th>온도</th><th>압력</th><th>촉매</th><th>평형 수득률</th><th>한 번 지날 때</th></tr></thead><tbody data-o="log"></tbody></table>
    </div>
  </div>
</section>
''')

# ───────── 13. 실험실 정리
add('''<!-- ════════ 13. 실험실 정리 ════════ -->
<section class="slide" data-sec="03 · 실험실" data-title="실험실 정리" data-tpl="check">
  <h2><span class="tag">실험실</span>실험실 자료로 생각하기</h2>
  <p class="f21"><b>1.</b> 평형 수득률이 가장 큰 조건은 무엇일까?</p>
  <p class="f21 step cm323-a">→ 온도는 낮게, 압력은 높게. 200 °C, 400 기압에서 약 97 %이다.</p>
  <p class="f21 mt12"><b>2.</b> 200 °C에서는 평형 수득률이 매우 큰데도 이 온도를 쓰지 않는 까닭은?</p>
  <p class="f21 step cm323-a">→ 반응 속도가 너무 느려 정해진 시간 안에 얻는 양(한 번 지날 때 수득률)이 거의 없다.</p>
  <p class="f21 mt12"><b>3.</b> 약 450 °C, 200 기압에서 촉매를 쓰는 까닭을 실험실 자료로 설명해 볼까?</p>
  <p class="f21 step cm323-a">→ 평형 수득률은 약 44 %로 크지 않지만 반응이 빨라 한 번 지날 때 얻는 양이 가장 많은 편(약 38 %)이고, 200 기압은 감당할 수 있는 비용의 압력이다. 남은 기체는 다시 보내 반응시킨다.</p>
  <p class="small mt12">실험실의 평형 수득률은 문헌 자료($\\ce{N2}:\\ce{H2}=1:3$), 반응 속도와 한 번 지날 때 수득률은 수업용 모의값이다.</p>
</section>
''')

# ───────── 14. 확인하기
add('''<!-- ════════ 14. 확인하기 ════════ -->
<section class="slide" data-sec="03 · 확인하기" data-title="확인하기" data-tpl="check">
  <h2><span class="tag q">확인하기</span>일상생활 속의 화학 평형 이동</h2>
  <ol class="cm323-ox">
    <li data-q>혈액이 체내에 산소를 공급하는 과정에서 화학 평형 이동이 관여한다. ( ○, × ) <span class="blank"><span class="step"><b class="c-field">○</b></span></span></li>
    <li data-q>암모니아 합성 과정은 전체 기체 분자 수가 감소하는 반응이므로 수득률을 높이려면 기체의 압력을 ( 높여야, 낮춰야 ) 한다. <span class="blank"><span class="step"><b class="c-field">높여야</b></span></span></li>
  </ol>
  <div class="board mt16" style="height:200px"></div>
</section>
''')

# ───────── 15. 창의력 (수국)
add(f'''<!-- ════════ 15. 소단원 마무리 창의력 ════════ -->
<section class="slide" data-sec="03 · 소단원 마무리" data-title="소단원 마무리: 창의력 키우기">
  <h2><span class="tag">소단원 마무리</span>창의력 키우기 — 수국꽃의 색</h2>
  <div class="card q"><p class="f22">수국꽃의 색이 토양의 액성에 따라 달라지는 원리를 조사하고, 파란색 수국꽃을 분홍색으로 변화시키는 방법을 설명해 보자.</p></div>
  <div class="formula sm mt8">$\\ce{{Al(OH)3(s) &lt;=&gt; Al^3+(aq) + 3OH-(aq)}}$</div>
  <div class="row mt8">
    <div class="col">
      <p class="f21"><b>Q</b> 조사 예시는?</p>
      <ul class="cm323-list">
        <li class="step"><b>원리</b>: 수국꽃의 분홍색 색소(델피니딘)는 $\\ce{{Al^3+}}$과 결합하면 <b>파란색</b>으로 변한다. <b>산성 토양</b>일수록 뿌리로 흡수되는 $\\ce{{Al^3+}}$이 많아져 파란색이 된다.</li>
        <li class="step"><b>염기성 토양</b>: $\\ce{{Al^3+}}$이 $\\ce{{OH-}}$과 결합해 물에 녹지 않는 앙금($\\ce{{Al(OH)3}}$)이 되므로 원래 색소의 색인 <b>분홍색</b>을 띤다.</li>
        <li class="step"><b>방법</b>: 토양을 염기성으로 바꿔(예: 석회) 토양 속 $\\ce{{Al^3+}}$ 농도를 감소시키면 꽃의 색이 분홍색으로 변할 수 있다.</li>
      </ul>
    </div>
    <div class="col" style="flex:0 0 400px">
      <p class="f21"><b>Q</b> 석회를 뿌려 $\\ce{{OH-}}$이 늘면 평형은?</p>
      <p class="f21 step cm323-a">→ $\\ce{{OH-}}$ 농도가 감소하는 <span class="ans">역반응</span> 쪽으로 이동해 $\\ce{{Al^3+}}$이 줄어든다.</p>
      <div class="note mt8">석회를 다룰 때는 장갑과 보안경을 쓴다.</div>
    </div>
  </div>
</section>
''')

# ───────── 16. 디지털 소양
add('''<!-- ════════ 16. 소단원 마무리 디지털 소양 ════════ -->
<section class="slide" data-sec="03 · 소단원 마무리" data-title="소단원 마무리: 디지털 소양 키우기">
  <h2><span class="tag">소단원 마무리</span>디지털 소양 키우기 — 수득률을 높인 사례</h2>
  <div class="card q"><p class="f22">산업 현장에서 화학 평형 이동을 이용해 수득률을 높인 사례를 조사해 보자. <b>Q</b> 어떤 사례가 있을까?</p></div>
  <table class="tight cm323-tb mt12">
    <tr><th>사례</th><th>반응</th><th>수득률을 높인 방법</th></tr>
    <tr class="step"><td>수소 생산<br>(암모니아 분해)</td><td>$\\ce{2NH3(g) &lt;=&gt; N2(g) + 3H2(g)}$</td><td class="l">분리막으로 수소를 생산과 동시에 빼내(정제) 생성물의 농도를 낮춘다 → 정반응 우세</td></tr>
    <tr class="step"><td>황산 제조</td><td>$\\ce{2SO2(g) + O2(g) &lt;=&gt; 2SO3(g)}$</td><td class="l">산소를 넉넉히 넣고, 적정 온도에서 촉매(산화 바나듐(V))를 쓴다.</td></tr>
    <tr class="step"><td>메탄올 합성</td><td>$\\ce{CO(g) + 2H2(g) &lt;=&gt; CH3OH(g)}$</td><td class="l">분자 수가 줄어드는 반응 → 압력을 높이고, 생긴 메탄올을 냉각해 빼낸다.</td></tr>
  </table>
  <p class="f21 step mt12">공유할 때는 반응식, 바꾼 조건, 평형 이동 방향, 자료의 출처를 함께 적는다. 산업 사례가 찾기 어려우면 생명 현상 사례도 함께 찾아보자.</p>
</section>
''')

# ───────── 17. 포트폴리오 이야기
bars = ''
for i, (lab, h, x) in enumerate([('평지', 150, 30), ('고지대', 105, 115)]):
    bars += f'<g data-anim="scale" data-from="1,0" data-o="{x+30},230" data-dur="1.2" data-delay="{.3*i}"><rect x="{x}" y="{230-h}" width="60" height="{h}" fill="#7FA9C2"/></g>' + T(x+30, 256, lab, 19)
add(f'''<!-- ════════ 17. 포트폴리오 이야기 ════════ -->
<section class="slide" data-sec="03 · 포트폴리오 이야기" data-title="포트폴리오 이야기: 고지대와 축구 경기">
  <h2><span class="tag">포트폴리오 이야기</span>생활 속 과학 — 고지대와 축구 경기</h2>
  <div class="row">
    <div class="col">
      <ul class="cm323-list">
        <li>멕시코, 볼리비아, 남아프리카 공화국처럼 고지대에 도시가 있는 나라도 월드컵 같은 대형 국제 대회를 유치하려고 노력한다.</li>
        <li>고도가 높은 지역은 평지에 비해 산소가 부족하다. 이곳에서 축구를 하면 조금만 뛰어도 숨이 차고 쉽게 피로해진다.</li>
        <li>높은 고도에 적응한 그 지역 선수에 비해 다른 나라 선수들은 체력 부담이 크다. 한때 국제축구연맹(FIFA)에서 월드컵 개최지의 고도 제한을 두자는 의견도 나왔다.</li>
        <li>선수들은 경기 3주~4주 전에 미리 가서 신체 적응 훈련을 하고, 저산소실 훈련, 고도 차이를 이용한 훈련 등을 연구한다.</li>
      </ul>
      <p class="f21 mt12 c-muted">→ 다음 장: 선수의 몸에 생기는 변화를 화학 평형 이동으로 설명해 보자.</p>
    </div>
    <div class="col" style="flex:0 0 330px"><svg class="fig" viewBox="0 0 300 280" style="width:300px" aria-label="평지보다 고지대의 공기 속 산소의 양이 적음">
      <path d="M190 230 L235 90 L255 130 L295 60 V230 Z" fill="#C9D3DD"/><path d="M235 90 l-9 28 h18 Z M295 60 l-8 22 h8 Z" fill="#FFFFFF"/>
      {bars}
      {T(150,30,'공기 속 산소의 양',19,w=700)}{T(150,55,'(같은 부피, 크기 비교)',18,fill='#5B6B7F')}
      <circle cx="250" cy="208" r="16" fill="#FFFFFF" stroke="#16233D" stroke-width="2"/><path d="M250 199 l8 6 -3 9 h-10 l-3 -9 Z" fill="#16233D"/>
    </svg></div>
  </div>
</section>
''')

# ───────── 18. 활동하기
add('''<!-- ════════ 18. 포트폴리오 이야기 활동하기 ════════ -->
<section class="slide" data-sec="03 · 포트폴리오 이야기" data-title="활동하기: 고지대 적응 훈련 조사">
  <h2><span class="tag">포트폴리오 이야기</span>활동하기 (조사)</h2>
  <div class="card q"><p class="f22">운동선수들이 고지대에 미리 적응하거나 경기력을 향상하기 위해 어떤 훈련을 했는지 찾아보고, 이때 선수의 신체에 생기는 변화를 화학 평형 이동으로 설명해 보자.</p></div>
  <div class="formula sm mt8">$\\ce{Hb(aq) + 4O2(g) &lt;=&gt; Hb(O2)4(aq)}$</div>
  <p class="f21 mt8"><b>Q</b> 예시 결과는?</p>
  <ul class="cm323-list">
    <li class="step"><b>훈련</b>: 경기 3주~4주 전 고지대 적응 훈련, 저산소실 훈련(예: 2010 남아프리카 공화국 월드컵에 대비해 파주 트레이닝센터에 만든 저산소실), 탄수화물 위주 식단</li>
    <li class="step"><b>신체 변화</b>: 적혈구와 헤모글로빈의 양이 늘어난다.</li>
    <li class="step"><b>평형 이동</b>: 반응물 $\\ce{Hb}$의 농도가 커져 정반응이 우세 → 고지대에서도 산화 헤모글로빈의 양이 평소와 비슷해져 조직이 평소처럼 산소를 공급받는다.</li>
    <li class="step"><b>평지로 돌아오면</b>: 산소 농도도 높아 정반응이 더 잘 일어나 경기력에 도움이 될 수 있다.</li>
  </ul>
</section>
''')

# ───────── 19. 중단원 마무리 07
add(f'''<!-- ════════ 19. 중단원 마무리 07 ════════ -->
<section class="slide" data-sec="03 · 중단원 마무리" data-title="중단원 마무리 07">
  <h2><span class="tag q">중단원 마무리 07</span>수득률 그래프로 반응 찾기</h2>
  <div class="row">
    <div class="col" style="flex:0 0 400px">
      <p class="f21">그림은 어떤 화학 반응에서 온도와 압력을 변화시켰을 때 생성물의 수득률을 나타낸 것이다. 이러한 수득률을 나타내는 반응은?</p>
      <svg class="fig mt8" viewBox="0 0 380 220" style="width:370px" aria-label="압력이 변해도 수득률이 일정하고, 100 °C의 수득률이 300 °C보다 큼">
        <g data-arw="50,190,360,190,ink,2"></g><g data-arw="50,190,50,15,ink,2"></g>
        {T(60,25,'수득률',19,anchor='start')}{T(355,212,'압력',19,anchor='end')}
        <g data-anim="draw" data-dur="1.2"><path d="M55 70 H300" stroke="#16233D" stroke-width="4"/><path d="M55 120 H300" stroke="#5B6B7F" stroke-width="4" stroke-dasharray="10 6"/></g>
        {T(308,77,'100 °C',19,anchor='start')}{T(308,127,'300 °C',19,anchor='start',fill='#5B6B7F')}
      </svg>
      <div class="board mt4"></div>
    </div>
    <div class="col">
      <div class="choices cm323-col" style="gap:22px">
        <span>① $\\ce{{N2O4(g) &lt;=&gt;[\\text{{에너지 흡수}}][\\text{{에너지 방출}}] 2NO2(g)}}$</span>
        <span>② $\\ce{{N2(g) + O2(g) &lt;=&gt;[\\text{{에너지 흡수}}][\\text{{에너지 방출}}] 2NO(g)}}$</span>
        <span>③ $\\ce{{H2(g) + Cl2(g) &lt;=&gt;[\\text{{에너지 방출}}][\\text{{에너지 흡수}}] 2HCl(g)}}$</span>
        <span>④ $\\ce{{N2(g) + 3H2(g) &lt;=&gt;[\\text{{에너지 방출}}][\\text{{에너지 흡수}}] 2NH3(g)}}$</span>
        <span>⑤ $\\ce{{2SO2(g) + O2(g) &lt;=&gt;[\\text{{에너지 방출}}][\\text{{에너지 흡수}}] 2SO3(g)}}$</span>
      </div>
      <p class="f21 step mt8"><b>단서 1</b> 압력이 변해도 수득률이 같다 → 전체 기체 분자 수가 같은 반응 → ②, ③ (①: 1 → 2, ④: 4 → 2, ⑤: 3 → 2)</p>
      <p class="f21 step mt4"><b>단서 2</b> 온도가 낮을수록 수득률이 크다 → 정반응이 에너지를 방출하는 반응 → ③</p>
      <div class="answer step mt8">정답: ③</div>
    </div>
  </div>
</section>
''')

# ───────── 20. 확인 문제 01
add('''<!-- ════════ 20. 확인 문제 01 ════════ -->
<section class="slide" data-sec="03 · 확인 문제" data-title="확인 문제 01">
  <h2><span class="tag q">확인 문제 01</span>헤모글로빈과 화학 평형 이동</h2>
  <div class="formula sm">$\\ce{Hb(aq) + 4O2(g) &lt;=&gt; Hb(O2)4(aq)}$</div>
  <div class="row mt8">
    <div class="col">
      <p class="f21">이에 대한 설명으로 옳은 것만을 &lt;보기&gt;에서 있는 대로 고르면?</p>
      <div class="bogi f22 mt8">ㄱ. 폐에서는 정반응이 우세하게 진행한다.<br>ㄴ. 고지대에 막 도착하면 산화 헤모글로빈이 생성되는 반응이 잘 일어나지 못한다.<br>ㄷ. 고지대에서 지내며 헤모글로빈의 양이 늘면 역반응이 우세하게 진행한다.</div>
    </div>
    <div class="col stack" style="flex:0 0 400px">
      <p class="f21 step">ㄱ ○ 폐는 산소 농도가 높다.</p>
      <p class="f21 step">ㄴ ○ 산소 농도가 낮아 정반응이 잘 일어나지 못한다.</p>
      <p class="f21 step">ㄷ × 반응물이 늘면 정반응이 우세하다.</p>
      <div class="board mt4"></div>
    </div>
  </div>
  <div class="answer step mt8">정답: ㄱ, ㄴ</div>
</section>
''')

# ───────── 21. 확인 문제 02
rows = [('(1) 압력을 높인다.', '<b class="c-field">정반응</b>', '커짐'),
        ('(2) 온도를 높인다.', '<b class="cm323-bf">역반응</b>', '작아짐'),
        ('(3) 생성된 $\\ce{NH3}$를 제거한다.', '<b class="c-field">정반응</b>', '커짐'),
        ('(4) $\\ce{N2}$를 더 넣는다.', '<b class="c-field">정반응</b>', '커짐(수소 기준)'),
        ('(5) 촉매를 넣는다.', '이동 없음', '그대로')]
tr = ''.join(f'<tr data-q><td class="l">{a}</td><td><span class="blank"><span class="step" data-g="r{i}">{b}</span></span></td><td><span class="blank"><span class="step" data-g="r{i}">{c}</span></span></td></tr>' for i, (a, b, c) in enumerate(rows))
add(f'''<!-- ════════ 21. 확인 문제 02 ════════ -->
<section class="slide" data-sec="03 · 확인 문제" data-title="확인 문제 02" data-tpl="check">
  <h2><span class="tag q">확인 문제 02</span>암모니아의 수득률을 바꾸는 조건</h2>
  <div class="formula sm">$\\ce{{N2(g) + 3H2(g) &lt;=&gt;[\\text{{에너지 방출}}][\\text{{에너지 흡수}}] 2NH3(g)}}$</div>
  <p class="f22 mt8">이 반응이 평형을 이루고 있다. 다음 변화에서 우세하게 진행하는 반응과 암모니아 수득률의 변화는?</p>
  <div class="row mt8">
    <div class="col" style="flex:0 0 760px">
      <table class="tight cm323-tb"><tr><th>변화</th><th>우세한 반응</th><th>수득률</th></tr>{tr}</table>
    </div>
    <div class="col stack"><div class="board"></div></div>
  </div>
</section>
''')

# ───────── 22. 함께 풀어 보기
add('''<!-- ════════ 22. 함께 풀어 보기 ════════ -->
<section class="slide" data-sec="03 일상생활 속의 화학 평형 이동 · 마무리" data-title="함께 풀어 보기">
  <h2><span class="tag ink">함께 풀어 보기</span>2. 화학 평형 이동 — 핵심 내용 정리</h2>
  <div class="cm323-map">
    <div class="cm323-side">
      <div class="cm323-node cm323-dim">1 농도·압력 변화와 화학 평형 이동 <span class="small">(113쪽)</span><br><span class="small">1 정반응 · 2 역반응 · 3 감소 · 4 증가</span></div>
      <div class="cm323-node cm323-dim">2 온도 변화와 화학 평형 이동 <span class="small">(120쪽)</span><br><span class="small">5 방출 · 6 흡수</span></div>
    </div>
    <div class="cm323-node cm323-main"><b>3 일상생활 속의 화학 평형 이동</b> <span class="small">(124쪽 · 오늘)</span>
      <p class="f21 mt8">(1) 혈액이 체내에 산소를 공급하는 과정에서 화학 평형 이동이 관여한다.</p>
      <p class="f21 mt4" data-q>폐(산소 많음)에서는 <span class="blank"><span class="step">정반응</span></span>, 조직(산소 적음)에서는 <span class="blank"><span class="step">역반응</span></span>이 우세하다.</p>
      <p class="f21 mt12">(2) 암모니아를 합성할 때 화학 평형 이동의 원리를 이용하여 수득률을 높일 수 있다.</p>
      <p class="f21 mt4" data-q>압력을 <span class="blank"><span class="step">높이고</span></span>, 온도를 <span class="blank"><span class="step">낮추고</span></span>, 생성된 암모니아를 <span class="blank"><span class="step">제거</span></span>한다.</p>
      <p class="small mt4">실제로는 반응 속도 때문에 적정 온도에서 촉매를 쓴다.</p>
    </div>
  </div>
  <p class="small mt8">교과서 「함께 풀어 보기」 3번 묶음에는 빈칸이 없어 덱이 빈칸을 만들었다. 핵심 내용으로 간단한 문제를 만들어 공유 플랫폼에 올리고 친구들과 함께 풀어 보자.</p>
</section>
''')

# ───────── 23. 스스로 점검하기
add('''<!-- ════════ 23. 스스로 점검하기 ════════ -->
<section class="slide" data-sec="03 일상생활 속의 화학 평형 이동 · 마무리" data-title="스스로 점검하기">
  <h2><span class="tag q">스스로 점검하기</span>2. 화학 평형 이동</h2>
  <div class="chips col1">
    <button class="chk">[지식·이해] 화학 평형 이동을 이해하고, 르샤틀리에 원리를 이용하여 화학 평형 이동을 설명했다.</button>
    <button class="chk">[과정·기능] 농도, 압력, 온도 변화에 따른 화학 평형 이동을 실험하고, 변인에 따른 평형 이동 방향을 예측했다.</button>
    <button class="chk">[가치·태도] 생명 현상과 산업 현장에서 화학 평형 이동을 이용한 사례를 조사하여 과학 지식이 일상생활의 문제 해결에 활용됨을 인식했다.</button>
  </div>
  <div class="card mt12">
    <p class="f21"><b>Q</b> 폐와 조직에서 우세한 반응은? <span class="step">→ 폐는 정반응, 조직은 역반응</span></p>
    <p class="f21 mt8"><b>Q</b> 암모니아 수득률을 높이는 압력과 온도는? <span class="step">→ 높은 압력, 낮은 온도 (실제로는 적정 온도와 촉매)</span></p>
    <p class="f21 mt8"><b>Q</b> 촉매는 평형을 이동시킬까? <span class="step">→ <span class="ans">아니다</span>. 평형에 빨리 도달하게 할 뿐이다.</span></p>
  </div>
  <div class="note puzzle mt12">평가 결과가 아쉽다면 '2. 화학 평형 이동'을 다시 한번 학습해 보자. <b>다음 시간</b> Ⅲ. 화학 평형 대단원 마무리</div>
</section>
''')

open(OUT, 'w', encoding='utf-8').write('\n'.join(H))
print('slides', sum(s.count('<section') for s in H))
