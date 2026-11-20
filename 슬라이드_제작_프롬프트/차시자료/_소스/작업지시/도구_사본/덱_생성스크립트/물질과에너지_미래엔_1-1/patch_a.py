import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
parts = re.split(r'(?=<!-- ════════ )', s)
head, secs = parts[0], parts[1:]
def num(x): return int(re.match(r'<!-- ════════ (\d+)', x).group(1))
D = {num(x): x for x in secs}
N = {}
N[2] = '''<!-- ════════ 2. 대단원 도입 ════════ -->
<section class="slide" data-sec="Ⅰ. 물질의 세 가지 상태 · 도입" data-title="대단원 도입: 학습할 내용">
  <h2>Ⅰ. 물질의 세 가지 상태</h2>
  <p class="f22">에스프레소 기계는 물을 끓여 만든 <b>수증기의 압력</b>으로 커피를 추출한다. 이 단원에서는 물질이 온도와 압력에 따라 기체, 액체, 고체 상태로 존재한다는 것을 알고, 물질의 상태가 일상생활에 어떤 영향을 주는지 알아본다.</p>
  <div class="center mt8">{{STATES}}</div>
  <div class="flow mt8">
    <div class="fnode hl">01 기체의 성질</div><div class="farr">→</div>
    <div class="fnode">02 혼합 기체의 부분 압력과 몰분율</div><div class="farr">→</div>
    <div class="fnode">03 액체의 분자 간 상호작용</div><div class="farr">→</div>
    <div class="fnode">04 고체의 종류와 구조</div>
  </div>
  <p class="f22 mt12"><b>Q</b> 같은 물질이 기체, 액체, 고체로 존재할 수 있는 까닭은 무엇일까?</p>
  <div class="answer step">입자 사이의 거리와 상호작용, 그리고 <b>온도와 압력</b>에 따라 달라진다.</div>
</section>

'''
N[3] = '''<!-- ════════ 3. 단원 연계·학습 목표 ════════ -->
<section class="slide" data-sec="Ⅰ. 물질의 세 가지 상태 · 도입" data-title="대단원 도입: 단원 연계와 목표">
  <h2>단원 연계와 이 단원의 학습 목표</h2>
  <div class="flow">
    <div class="fnode">중학교 과학<br><span class="small">물질의 상태 변화, 기체의 성질, 물질의 특성</span></div><div class="farr">→</div>
    <div class="fnode">통합과학1<br><span class="small">물질과 규칙성</span></div><div class="farr">→</div>
    <div class="fnode">화학<br><span class="small">화학의 언어, 물질의 구조와 성질</span></div><div class="farr">→</div>
    <div class="fnode hl">물질과 에너지<br><span class="small">물질의 세 가지 상태</span></div>
  </div>
  <table class="tight em11-goal mt16">
    <tr><th>지식·이해</th><td class="l">물질이 온도와 압력에 따라 기체, 액체, 고체 상태로 존재한다는 것을 알고, 각 상태의 성질을 설명할 수 있다.</td></tr>
    <tr><th>과정·기능</th><td class="l">이상 기체 방정식을 활용해 기체의 종류를 확인하고, 물질의 끓는점에 영향을 주는 요인을 추론하며, 고체를 결합의 종류에 따라 분류할 수 있다.</td></tr>
    <tr><th>가치·태도</th><td class="l">물질의 세 가지 상태가 일상생활에 미치는 영향에 호기심을 갖고, 기체, 액체, 고체의 성질이 유용하게 쓰인다는 것을 인식할 수 있다.</td></tr>
  </table>
  <div class="note mt12"><b>학습 과제물</b> 이 단원을 학습하면서 나만의 특기를 발휘한 학습 과제물을 만들어 보자: 36쪽 예술과 화학 이야기 · 37쪽 화학과 나의 미래 · 42–43쪽 프로젝트</div>
</section>

'''
N[4] = '''<!-- ════════ 4. 학습 목표 ════════ -->
<section class="slide" data-sec="01 기체의 성질" data-title="학습 목표">
  <h2>학습 목표</h2>
  <div class="std"><span class="code">[12물에01-01]</span>기체의 온도, 압력, 부피, 몰수 사이의 관계를 통합적으로 이해하고, 이상 기체 방정식을 근사적으로 활용하는 사례를 조사하여 화학의 유용함을 인식할 수 있다.</div>
  <ol class="goals mt12">
    <li>기체의 압력, 온도, 양(mol), 부피 사이의 관계를 통합적으로 설명할 수 있다.</li>
    <li>이상 기체 방정식을 근사적으로 활용하는 사례를 조사하여 화학의 유용함을 인식할 수 있다.</li>
  </ol>
  <h3 class="mt16">이번 시간(첫째 덱)의 흐름</h3>
  <div class="flow">
    <div class="fnode">기체의 압력</div><div class="farr">→</div>
    <div class="fnode hl">압력과 부피(보일 법칙)</div><div class="farr">→</div>
    <div class="fnode hl">온도와 부피(샤를 법칙)</div><div class="farr">→</div>
    <div class="fnode hl">양과 부피(아보가드로 법칙)</div>
  </div>
  <div class="note mt16"><b>다음 시간(둘째 덱)</b> 세 법칙을 종합한 <b>이상 기체 방정식</b>과 그 활용, 탐구 「기체의 종류를 확인할 수 있는 실험을 설계하고 수행하기」</div>
</section>

'''
N[5] = '''<!-- ════════ 5. 생각 열기 ════════ -->
<section class="slide" data-sec="01 기체의 성질 · 도입" data-title="생각 열기: 증기 기관">
  <h2><span class="tag">생각 열기</span>증기 기관은 기체의 어떤 성질을 이용할까?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 540px">{{STEAM}}</div>
    <div class="col">
      <p class="f22">18세기에 증기 기관이 발전하면서 산업 혁명이 일어났고, 인류의 생활에 큰 변화가 일어났다.</p>
      <p class="f22 mt12" data-q><b>Q</b> 산업 혁명을 이끈 증기 기관의 원리는 기체의 어떤 성질을 이용한 것일까?</p>
    </div>
  </div>
  <div class="answer step">기체는 분자 사이의 거리가 가장 멀고 분자가 가장 자유롭게 운동한다. 그래서 <b>온도나 압력</b>에 따라 <b>부피가 크게 변한다</b>.<br><span class="small">뜨거운 수증기가 부피를 늘리며 피스톤을 민다. 기체의 압력, 온도, 양, 부피는 어떤 관계일까?</span></div>
</section>

'''
N[9] = '''<!-- ════════ 9. 보일의 J자 관 실험·자료 읽기 ════════ -->
<section class="slide" data-sec="01 · 기체의 압력과 부피" data-title="보일의 J자 관 실험">
  <h2><span class="no">1</span>보일의 J자 관 실험</h2>
  <div class="row">
    <div class="col" style="flex:0 0 380px">{{JTUBE}}</div>
    <div class="col">
      <p class="f21">한쪽 끝이 막힌 J자 관의 열린 쪽에 수은을 넣으면, 막힌 쪽 기체에 가해지는 외부 압력이 커진다. 외부 압력과 평형을 이루는 기체의 압력이 커지므로 기체의 부피가 줄어든다.</p>
      <p class="f21 mt8"><span class="tag" style="font-size:18px;padding:2px 10px;border-radius:8px;background:var(--field);color:#fff">자료 읽기</span> 그래프에서 압력이 $P$, $2P$일 때 (압력 × 부피)를 각각 구해 보자.</p>
      <div class="answer step" data-g="r1">$P\\times V=PV$, &nbsp; $2P\\times\\dfrac{1}{2}V=PV$ — 같다.</div>
    </div>
    <div class="col" style="flex:0 0 400px">{{BOYREL}}</div>
  </div>
</section>

'''
N[12] = '''<!-- ════════ 12. 확인하기 (9쪽) ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 보일 법칙" data-tpl="check">
  <h2><span class="tag q">확인하기</span>보일 법칙</h2>
  <p class="f22" data-q><b>1</b> 일정한 온도에서 일정량의 기체의 부피는 압력과 <span class="blank"><span class="step">반비례</span></span> 관계에 있는데, 이것을 <span class="blank"><span class="step">보일</span></span> 법칙이라고 한다.</p>
  <p class="f22 mt16"><b>2</b> 20 °C, 1 기압에서 부피가 2 L인 질소 기체가 있다. 같은 온도에서 이 질소 기체의 부피가 5 L로 되었을 때, 기체의 압력은 몇 기압인가?</p>
  <div class="row stretch mt8" style="height:220px">
    <div class="col stack" style="flex:0 0 560px">
      <p class="f22 step">$P_1V_1=P_2V_2$ → $1\\ \\text{atm}\\times2\\ \\text{L}=P_2\\times5\\ \\text{L}$</p>
      <p class="f22 step">$P_2=\\dfrac{1\\times2}{5}=0.4\\ \\text{atm}$</p>
    </div>
    <div class="col stack"><div class="board"></div></div>
  </div>
  <div class="answer step">0.4 기압</div>
</section>

'''
N[14] = '''<!-- ════════ 14. 연결: 달걀 ════════ -->
<section class="slide" data-sec="01 · 기체의 온도와 부피" data-title="뜨거운 물에서 깨지는 달걀">
  <h2><span class="tag alt">연결</span>뜨거운 물에 넣은 달걀이 깨지는 까닭은?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 520px">{{EGG}}</div>
    <div class="col">
      <p class="f22">냉장고에서 꺼낸 달걀을 바로 뜨거운 물에 넣어 삶으면 달걀이 깨진다.</p>
      <p class="f22 mt12" data-q><b>Q</b> 달걀 속 기체의 무엇이 변해서 껍데기가 깨졌을까?</p>
      <div class="card tip step mt12"><p class="f22">온도가 높아져 달걀 속 기체의 <b>부피</b>가 급격하게 늘어났다.</p></div>
    </div>
  </div>
  <div class="answer step">→ 기체는 온도에 따라 부피가 크게 변한다. 기체의 <b>온도와 부피</b> 사이에는 어떤 관계가 있을까?</div>
</section>

'''
N[15] = '''<!-- ════════ 15. 해 보기 (10쪽) ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기: 온도와 부피의 관계">
  <h2><span class="tag">해 보기</span>기체의 온도와 부피의 관계 알아보기</h2>
  <div class="row">
    <div class="col">
      <p class="f21">외부 압력과 실린더 속 기체의 양이 일정할 때, 온도와 부피의 관계를 알아보는 모의실험 결과이다.</p>
      <table class="tight em11-data mt8">
        <tr><th>온도 [°C]</th><td>0</td><td>91</td><td>182</td><td>273</td></tr>
        <tr><th>부피(상댓값)</th><td>$3V$</td><td>$4V$</td><td>$5V$</td><td>$6V$</td></tr>
      </table>
      <p class="f21 mt12" data-q><b>1</b> 기체의 온도와 부피의 관계를 그래프로 나타내 보자.</p>
      <p class="f21 mt8" data-q><b>2</b> 그래프를 이용하여 기체의 부피가 0이 되는 온도를 예상해 보자.</p>
      <div class="answer step" data-g="c1">→ 약 $-273\\ {}^\\circ\\text{C}$</div>
      <p class="small mt8">검색·누리집: 「샤를 법칙 모의실험」으로 온도에 따른 부피와 분자 운동 변화를 확인해 보자(24번 실험실 Ⅱ).</p>
    </div>
    <div class="col" style="flex:0 0 540px">{{TDATA}}</div>
  </div>
</section>

'''
N[16] = '''<!-- ════════ 16. 절대 온도 ════════ -->
<section class="slide" data-sec="01 · 기체의 온도와 부피" data-title="절대 온도">
  <h2><span class="no">2</span>샤를의 발견과 절대 온도</h2>
  <p class="f21">샤를은 일정한 압력에서 일정량의 기체의 부피가 기체의 종류에 관계없이 온도가 1 °C 높아질 때마다 0 °C 때 부피의 $\\dfrac{1}{273}$씩 증가한다는 것을 알아냈다.</p>
  <div class="formula sm">$V_t=V_0+\\dfrac{V_0}{273}t$<span class="unit">$V_t$: $t\\ {}^\\circ\\text{C}$에서 기체의 부피, $V_0$: $0\\ {}^\\circ\\text{C}$에서 기체의 부피</span></div>
  <div class="row">
    <div class="col center"><h3>(가) 섭씨온도와 기체의 부피</h3>{{VTA}}</div>
    <div class="col center step" data-g="a1"><h3>(나) 절대 온도와 기체의 부피</h3>{{VTB}}</div>
  </div>
  <p class="f21 step" data-g="a1">부피가 0이 되는 $-273\\ {}^\\circ\\text{C}$를 <mark>절대 영도</mark>라 하고, 절대 영도를 0으로 하여 섭씨온도와 같은 간격으로 나타내는 온도를 <mark>절대 온도</mark>(단위 K)라고 한다. &nbsp; $T(\\text{K})=t({}^\\circ\\text{C})+273$</p>
</section>

'''
N[18] = '''<!-- ════════ 18. 본문 문제 (11쪽) ════════ -->
<section class="slide" data-sec="01 · 기체의 온도와 부피" data-title="문제: 샤를 법칙">
  <h2><span class="tag ex">문제</span>샤를 법칙으로 부피 구하기</h2>
  <p class="f22">27 °C에서 부피가 5 L인 기체가 있다. 같은 압력에서 기체의 온도를 87 °C로 높이면 기체의 부피는 몇 L가 되는가?</p>
  <div class="row stretch mt12" style="height:310px">
    <div class="col stack" style="flex:0 0 580px">
      <p class="f22 step"><b>절대 온도로</b> $T_1=27+273=300\\ \\text{K}$, $T_2=87+273=360\\ \\text{K}$</p>
      <p class="f22 step"><b>관계</b> 압력·기체의 양 일정 → $\\dfrac{V_1}{T_1}=\\dfrac{V_2}{T_2}$</p>
      <p class="f22 step"><b>계산</b> $V_2=V_1\\times\\dfrac{T_2}{T_1}=5\\times\\dfrac{360}{300}=6\\ \\text{L}$</p>
      <div class="note q step"><b>주의</b> 섭씨온도를 그대로 넣으면 $5\\times\\dfrac{87}{27}\\approx16\\ \\text{L}$ — 틀린 답이다.</div>
    </div>
    <div class="col stack"><div class="board"></div></div>
  </div>
  <div class="answer step">$6\\ \\text{L}$</div>
</section>

'''
N[22] = '''<!-- ════════ 22. 본문 문제 (12쪽) ════════ -->
<section class="slide" data-sec="01 · 기체의 양과 부피" data-title="문제: 아보가드로 법칙">
  <h2><span class="tag ex">문제</span>기체의 부피로 양(mol) 구하기</h2>
  <p class="f22">0 °C, 1 기압의 이산화 탄소($\\ce{CO2}$) 기체 16.8 L에 들어 있는 이산화 탄소의 양은 몇 mol인가?</p>
  <div class="row stretch mt12" style="height:280px">
    <div class="col stack" style="flex:0 0 560px">
      <p class="f22 step"><b>관계</b> 0 °C, 1 기압에서 기체 1 mol의 부피 = 22.4 L</p>
      <p class="f22 step"><b>계산</b> $n=\\dfrac{16.8\\ \\text{L}}{22.4\\ \\text{L/mol}}=0.75\\ \\text{mol}$</p>
    </div>
    <div class="col stack"><div class="board"></div></div>
  </div>
  <div class="answer step">$0.75\\ \\text{mol}$</div>
</section>

<!-- ════════ 22b. 확인하기 (12쪽) ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 절대 온도·아보가드로" data-tpl="check">
  <h2><span class="tag q">확인하기</span>절대 온도와 아보가드로 법칙</h2>
  <p class="f22" data-q><b>1</b> 절대 영도를 0으로 하여 섭씨온도와 같은 간격으로 나타낸 온도를 <span class="blank"><span class="step">절대 온도</span></span>(이)라고 한다.</p>
  <p class="f22 mt28" data-q><b>2</b> 일정한 온도와 압력에서 기체의 부피는 양(mol)에 ( 비례한다, 반비례한다 ). <span class="blank"><span class="step">비례한다</span></span></p>
  <p class="f22 mt28" data-q><b>3</b> (더 해 보기) 압력이 일정할 때 10 °C의 기체를 20 °C로 가열하면 부피는 몇 배가 될까? <span class="blank"><span class="step">약 1.04배</span></span> <span class="small step">$\\dfrac{293}{283}\\approx1.04$ — 2배가 아니다.</span></p>
</section>

'''
for k, v in N.items():
    D[k] = v
D.pop(13, None)   # ○× 확인하기 → 교과서 확인하기(12)로 대체
D.pop(19, None)   # 섭씨 오개념 → 22b의 3번 문항으로 합침
out = head + ''.join(D[k] for k in sorted(D))
# 표기: 교과서 식 꼴 (k는 상수)
out = out.replace("$V=k'T$ &nbsp; $\\left(\\dfrac{V}{T}=k'\\right)$", "$V\\propto T$ &nbsp; 또는 &nbsp; $V=kT$<span class=\"unit\">$k$는 상수</span>")
out = out.replace("$V=k''n$<span class=\"unit\">온도와 압력이 일정할 때</span>", "$V\\propto n$ &nbsp; 또는 &nbsp; $V=kn$<span class=\"unit\">$k$는 상수 (온도와 압력이 일정할 때)</span>")
out = out.replace('<div class="formula">$PV=k$<span class="unit">$k$: 온도와 기체의 양에 따라 정해지는 상수</span></div>', '<div class="formula">$V\\propto\\dfrac{1}{P}$ &nbsp; 또는 &nbsp; $PV=k$<span class="unit">$k$는 상수 (온도와 기체의 양에 따라 정해짐)</span></div>')
out = out.replace("<td>$V=k'T$</td>", "<td>$V=kT$</td>").replace("<td>$V=k''n$</td>", "<td>$V=kn$</td>")
out = out.replace("<span class=\"step\">$k'T$</span>", "<span class=\"step\">$kT$</span>").replace("<span class=\"step\">$k''n$</span>", "<span class=\"step\">$kn$</span>")
out = out.replace('<p class="small mt8">과학사: 샤를(Charles, J.)이 1787년에 발견하였고, 게이뤼삭이 1802년에 발표하였다.</p>', '<p class="small mt8">샤를(Charles, J. A. C., 1746~1823): 프랑스의 과학자. 기체의 부피와 온도의 관계를 밝혔으며, 1783년에 수소 기구를 띄워 날렸다.</p>')
out = out.replace('<div class="note mt8"><b>과학사</b> 1662년 보일(Boyle, R.)이 공기의 압력과 부피를 측정하여 이 관계를 밝혔다.</div>', '<div class="note mt8"><b>보일</b>(Boyle, R., 1627~1691) 영국의 과학자. 실험 결과를 바탕으로 1662년에 보일 법칙을 발표했다. 객관적인 검증을 중시한 연구 태도는 화학이 과학의 한 영역으로 자리 잡는 기반이 되었다.</div>')
out = out.replace('<span class="unit">$=101.3\\ \\text{kPa}$</span>', '<span class="unit">$=101325\\ \\text{Pa}$, &nbsp; $1\\ \\text{Pa}=1\\ \\text{N/m}^2$</span>')
open(p, 'w', encoding='utf-8').write(out)
print(len(D), 'sections')
